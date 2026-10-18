#!/usr/bin/env python3
"""共有画像台帳の検証。既存アプリの確定ハッシュを保ったまま、公開配信元を確認する。

デフォルトはデータ構造だけ。--online で画像JPEGを取得し、
取得時点のSHA256と成功・失敗をレポートする（JSON本体は更新しない）。
--output-dir を指定すると各作品をJPEGとして保存でき、アプリに同梱できる。
"""
import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADERS = {
    "User-Agent": "KaigaMuseumResearch/0.1 (artworks open-access image verification; contact via GitHub matumaruex/kaiga-data)",
    "Accept": "application/json,image/jpeg,*/*"
}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=24) as response:
        if response.status != 200:
            raise ValueError("HTTP " + str(response.status))
        raw = response.read(6_000_000)
        if len(raw) >= 6_000_000:
            raise ValueError("large response / truncated")
        return raw, response.headers.get("Content-Type", "")

def image_from_commons(title):
    query = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "titles": title, "iiprop": "url|size|mime", "iiurlwidth": "960"
    })
    payload, mime = get("https://commons.wikimedia.org/w/api.php?" + query)
    info = json.loads(payload)
    page = next(iter(info["query"]["pages"].values()))
    if "missing" in page or "imageinfo" not in page:
        raise ValueError("Commons file is missing")
    asset = page["imageinfo"][0]
    if asset.get("mime") != "image/jpeg":
        raise ValueError("Commons file is not JPEG")
    url = asset.get("thumburl") or asset["url"]
    return url, {"image_page_title": page.get("title"), "width": asset.get("width"), "height": asset.get("height")}

def validate(records, exhibition_ids, candidate_ids):
    issues = []
    names = set()
    for art in records:
        ident = art.get("id", "")
        if ident in names: issues.append(f"{ident}: duplicate image source")
        names.add(ident)
        src = art.get("image_source", {})
        if not ident.startswith("aic-") or not art.get("official_artwork_url", "").endswith(ident[4:]):
            issues.append(f"{ident}: artwork identity")
        accession = art.get("accession_number", "")
        if not re.fullmatch(r"[0-9]{4}\\.[0-9]+", accession):
            issues.append(f"{ident}: unknown Chicago accession number")
        if not src.get("license_url", "").startswith("https://"):
            issues.append(f"{ident}: missing license evidence URL")
        if src.get("last_http_sha_checked_on") and not SHA_RE.fullmatch(src.get("sha256") or ""):
            issues.append(f"{ident}: missing verified image digest")
        if src.get("last_http_sha_checked_on") and (src.get("byte_length") or 0) < 1024:
            issues.append(f"{ident}: missing verified image size")
        if src.get("type") == "pinned_public_mirror":
            if not src.get("download_url", "").startswith("https://raw.githubusercontent.com/haranishi/hundred-days/"):
                issues.append(f"{ident}: mirror is not pinned/public")
            if not SHA_RE.fullmatch(src.get("sha256") or "") or (src.get("byte_length") or 0) < 3000:
                issues.append(f"{ident}: missing checksum or size")
            if art.get("verification") not in ("source_app_tested_recheck_pending", "source_app_tested_mirror_rechecked"):
                issues.append(f"{ident}: status for mirror")
        elif src.get("type") == "wikimedia_commons":
            if accession and accession not in src.get("file_title", ""):
                issues.append(f"{ident}: Commons image is not the verified Chicago edition")
            if not src.get("file_title", "").startswith("File:"):
                issues.append(f"{ident}: missing Commons filename")
            if not src.get("commons_file_page", "").startswith("https://commons.wikimedia.org/wiki/File:"):
                issues.append(f"{ident}: missing Commons page")
            if art.get("verification") not in ("commons_page_found_image_http_pending", "commons_image_http_verified"):
                issues.append(f"{ident}: status for Commons")
        else: issues.append(f"{ident}: unsupported image source")
        if not src.get("license_label") or not src.get("commons_file_page"):
            issues.append(f"{ident}: no rights/source citation")
        if art.get("in_shared_catalog") != (ident in exhibition_ids or ident in candidate_ids):
            issues.append(f"{ident}: unexpected catalog membership")
    if not exhibition_ids.issubset(names) or not candidate_ids.issubset(names):
        issues.append("not every curated artwork has a recorded image source")
    if issues:
        raise ValueError("\n".join(issues))
    print(f"STRUCTURE OK: {len(records)} image records; {len(exhibition_ids | candidate_ids)} curated artworks covered", flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--require-all", action="store_true")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--report", default="artifacts/verified-image-sources.json")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "data/image-sources.json").read_text(encoding="utf-8"))
    exhibition = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))
    candidates = json.loads((ROOT / "data/candidates-batch-002.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    validate(records, {a["id"] for a in exhibition["artworks"]}, {a["id"] for a in candidates["works"]})
    if not args.online: return

    output = Path(args.output_dir) if args.output_dir else None
    if output is not None: output.mkdir(parents=True, exist_ok=True)
    result = []
    for index, rec in enumerate(records, 1):
        ident = rec["id"]
        item = {"id": ident, "source_kind": rec["image_source"]["type"], "success": False}
        try:
            src = rec["image_source"]
            url, extra = (src["download_url"], {}) if src["type"] == "pinned_public_mirror" else image_from_commons(src["file_title"])
            raw, mime = get(url)
            if len(raw) < 1024 or raw[:3] != bytes((0xff, 0xd8, 0xff)):
                raise ValueError("not JPEG content")
            sha = hashlib.sha256(raw).hexdigest()
            if src.get("sha256") and sha != src["sha256"]:
                raise ValueError("SHA256 does not match source app")
            if src.get("byte_length") and len(raw) != src["byte_length"]:
                raise ValueError("size does not match source app")
            if output is not None:
                (output / f"{ident.removeprefix('aic-')}.jpg").write_bytes(raw)
            item.update(success=True, downloaded_bytes=len(raw), sha256=sha, download_url=url, **extra)
            print(f"[{index}/{len(records)}] OK {ident} {len(raw)}B SHA256={sha} URL={url}", flush=True)
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
            item["error"] = type(exc).__name__ + ": " + str(exc)[:160]
            print(f"[{index}/{len(records)}] PENDING {ident}: {item['error']}", flush=True)
        result.append(item)
        time.sleep(0.3)
    report = {
        "checked": len(records), "passed": sum(1 for r in result if r["success"]),
        "failed": sum(1 for r in result if not r["success"]), "results": result
    }
    target = ROOT / args.report
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SUMMARY: {report['passed']}/{report['checked']} images downloaded and checked; report {args.report}", flush=True)
    if args.require_all and report["failed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
