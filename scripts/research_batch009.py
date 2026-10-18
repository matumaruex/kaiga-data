#!/usr/bin/env python3
"""The Met第9群: 現行公式APIの作品同定とオープン画像JPEGの実取得を検証。

読み取り専用。結果JSONを docs/batch009-online-result.json に書く。
元の51登録や候補の確認フラグは変更しない。
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
CANDIDATES = ROOT / "data/candidates-batch-009.json"
RESULT = ROOT / "docs/batch009-online-result.json"
HEADERS = {"User-Agent": "KaigaArtworkResearch/0.2 (open access data; matumaruex/kaiga-data)",
           "Accept": "application/json, image/jpeg, */*"}
EXPECTED_TYPES = {"paintings", "painting"}


def download(url, maxbytes=8_000_000, attempts=3):
    if urllib.parse.urlparse(url).scheme != "https":
        raise ValueError("HTTPS required")
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise ValueError(f"HTTP={response.status}")
                data = response.read(maxbytes + 1)
                if len(data) > maxbytes:
                    raise ValueError("file exceeds safety limit")
                return data, response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise
            time.sleep(2 + attempt * 3)


def check(c):
    oid = c["museum_object_id"]
    item = {"id": c["candidate_id"], "official_object_id": oid,
            "museum_record_verified": False, "image_verified": False,
            "eligible_for_review": False, "warnings": []}
    url = c["official_api_url"]
    raw, mime = download(url, maxbytes=1_000_000)
    record = json.loads(raw)
    fields = ("objectID", "title", "artistDisplayName", "objectDate",
              "accessionNumber", "isPublicDomain", "classification",
              "primaryImageSmall", "primaryImage", "medium")
    for key in fields:
        item[key] = record.get(key)
    item["additional_image_count"] = len(record.get("additionalImages") or [])
    item["official_api_url"] = url
    checks = {
        "object_id": record.get("objectID") == oid,
        "title": " ".join(str(record.get("title", "")).casefold().split()) == " ".join(c["title_original"].casefold().split()),
        "accession": record.get("accessionNumber") == c["accession_number"],
        "public_domain": record.get("isPublicDomain") is True,
        "painting": str(record.get("classification", "")).lower() in EXPECTED_TYPES
            or str(record.get("classification", "")).lower().startswith("paintings-")
            or (
                str(record.get("classification", "")).strip() == ""
                and "canvas" in str(record.get("medium", "")).lower()
                and any(m in str(record.get("medium", "")).lower() for m in ("oil", "tempera"))
            ),
    }
    if not c["artist"].casefold().startswith(("unidentified", "unknown")):
        artist = str(record.get("artistDisplayName", "")).casefold().strip()
        checks["artist"] = bool(artist) and c["artist"].casefold().removeprefix("attributed to ").strip() in artist
    item["metadata_checks"] = checks
    item["museum_record_verified"] = all(checks.values())
    if not item["museum_record_verified"]:
        item["warnings"].append("Official metadata mismatch: " + ",".join(
            k for k, v in checks.items() if not v))
        return item
    image_url = record.get("primaryImageSmall") or record.get("primaryImage")
    if not image_url:
        item["warnings"].append("Official API has no primary public image URL")
        return item
    parsed = urllib.parse.urlparse(image_url)
    if parsed.hostname not in {"images.metmuseum.org", "collectionapi.metmuseum.org"}:
        item["warnings"].append("Unexpected image host")
        return item
    image, content_type = download(image_url)
    if len(image) <= 5000 or image[:3] != bytes((255, 216, 255)) or image[-2:] != bytes((255, 217)):
        raise ValueError("Image is not a complete JPEG")
    if "jpeg" not in content_type.lower() and "jpg" not in content_type.lower():
        raise ValueError("Image MIME not JPEG")
    item["image_verified"] = True
    item["image_url_verified"] = image_url
    item["image_content_type"] = content_type
    item["image_bytes"] = len(image)
    item["image_sha256"] = hashlib.sha256(image).hexdigest()
    item["image_identity_basis"] = "primaryImageSmall from matching official Met object ID"
    item["eligible_for_review"] = True
    if oid in (771516, 436761, 435602):
        item["eligible_for_review"] = False
        item["warnings"].append("Multi-panel or multi-scene artwork; complete image sequence required")
    if item["additional_image_count"] and oid in (771516, 436761, 435602, 436840):
        item["warnings"].append("Multiple images; main JPEG may not represent all object details")
    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()
    works = json.loads(CANDIDATES.read_text(encoding="utf-8"))["works"]
    ids = [c["candidate_id"] for c in works]
    if len(ids) != len(set(ids)) or len(ids) != 18:
        raise ValueError("Candidate ID count/uniqueness mismatch")
    if not args.online:
        print(f"STRUCTURE OK: {len(ids)} Met candidate records")
        return
    results = []
    for idx, c in enumerate(works, 1):
        try:
            result = check(c)
        except Exception as exc:
            result = {"id": c["candidate_id"], "museum_record_verified": False,
                      "image_verified": False, "eligible_for_review": False,
                      "error": type(exc).__name__ + ": " + str(exc)[:200]}
        results.append(result)
        label = "VERIFIED" if result["eligible_for_review"] else "PENDING"
        print(f"[{idx}/{len(works)}] {label} {c['candidate_id']} "
              f"api={result['museum_record_verified']} jpeg={result['image_verified']} "
              f"sha256={result.get('image_sha256', '')} "
              f"reason={result.get('error') or ';'.join(result.get('warnings', []))}", flush=True)
        time.sleep(0.8)
    report = {
        "batch": "batch-009", "created_utc_by_github_actions": True,
        "source": "Met Open Access Object API / matching primary JPEG",
        "note": "HTTP+JPEG+SHA256 verification is distinct from human visual approval and interpretation.",
        "checked": len(results),
        "metadata_pass": sum(x["museum_record_verified"] for x in results),
        "images_pass": sum(x["image_verified"] for x in results),
        "eligible_for_curatorial_review": sum(x["eligible_for_review"] for x in results),
        "results": results,
    }
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")
    print(f"TOTAL metadata={report['metadata_pass']}/18 images={report['images_pass']}/18 "
          f"review-ready={report['eligible_for_curatorial_review']}/18", flush=True)
    if args.require_all and report["metadata_pass"] != len(works):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
