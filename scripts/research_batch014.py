#!/usr/bin/env python3
"""第14群13候補: Met公式Object API・オープンJPEGの直接取得とSHA256検証。

検証結果のみ docs/batch014-online-result.json に保存する。作品の自動昇格はしない。
"""
import concurrent.futures
import hashlib
import json
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/candidates-batch-014.json"
OUTPUT = ROOT / "docs/batch014-online-result.json"
HEADERS = {"User-Agent": "KaigaArtworkResearch/0.3 (met open access; matumaruex/kaiga-data)", "Accept": "application/json,image/jpeg,*/*"}

def load(url, limit=12000000):
    p = urllib.parse.urlparse(url)
    if p.scheme != "https":
        raise ValueError("Non-HTTPS address")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=28) as stream:
                if stream.status != 200:
                    raise ValueError("HTTP " + str(stream.status))
                b = stream.read(limit + 1)
                if len(b) > limit:
                    raise ValueError("Too large")
                return b, str(stream.headers.get("Content-Type", ""))
        except (urllib.error.HTTPError, TimeoutError) as exc:
            if attempt == 2 or isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                raise
            time.sleep(2 + attempt * 2)

def norm(s):
    return " ".join(str(s or "").casefold().split())

def verify(c):
    oid = c["museum_object_id"]
    item = {"id": c["candidate_id"], "museum_record_verified": False, "image_verified": False,
            "eligible_for_review": False, "warnings": [], "official_api_url": c["official_api_url"]}
    raw, _ = load(c["official_api_url"], 1200000)
    obj = json.loads(raw)
    for key in ("objectID", "title", "artistDisplayName", "objectDate", "accessionNumber", "isPublicDomain",
                "classification", "objectName", "medium", "primaryImage", "primaryImageSmall"):
        item[key] = obj.get(key)
    item["additional_image_count"] = len(obj.get("additionalImages") or [])
    cls = norm(obj.get("classification"))
    med = norm(obj.get("medium"))
    painting = cls in ("paintings", "painting") or cls.startswith("paintings-") or (
        not cls and norm(obj.get("objectName")) == "painting" and "oil" in med and "canvas" in med)
    expected_artist = norm(c["artist"])
    actual_artist = norm(obj.get("artistDisplayName"))
    artist_match = expected_artist.startswith(("unidentified artist", "unknown")) and not actual_artist or (
        expected_artist and (expected_artist in actual_artist or expected_artist.removeprefix("attributed to ") in actual_artist or expected_artist.removeprefix("copy after ") in actual_artist))
    checks = {"object_id":obj.get("objectID") == oid, "title":norm(obj.get("title")) == norm(c["title_original"]),
              "artist":bool(artist_match), "accession":bool(obj.get("accessionNumber")),
              "public_domain":obj.get("isPublicDomain") is True, "painting":painting}
    item["metadata_checks"] = checks
    item["museum_record_verified"] = all(checks.values())
    if not item["museum_record_verified"]:
        item["warnings"].append("metadata mismatch: " + ",".join(k for k,v in checks.items() if not v))
        return item
    url = obj.get("primaryImageSmall") or obj.get("primaryImage") or ""
    if urllib.parse.urlparse(url).hostname != "images.metmuseum.org":
        item["warnings"].append("missing primary JPEG on expected image host")
        return item
    jpeg, mime = load(url)
    if len(jpeg) <= 5000 or not jpeg.startswith(bytes((255, 216, 255))) or not jpeg.endswith(bytes((255, 217))):
        raise ValueError("Incomplete or invalid JPEG")
    if "jpeg" not in mime.lower() and "jpg" not in mime.lower():
        raise ValueError("Incorrect JPEG Content-Type " + mime)
    item.update({"image_verified":True, "eligible_for_review":True, "image_url_verified":url,
                 "image_sha256":hashlib.sha256(jpeg).hexdigest(),"image_bytes":len(jpeg),
                 "image_content_type":mime,"image_identity_basis":"primaryImageSmall of matching Met objectID"})
    return item

def main():
    candidates = json.loads(INPUT.read_text(encoding="utf-8"))["works"]
    if len(candidates) != 13 or len({c["candidate_id"] for c in candidates}) != 13:
        raise ValueError("Expected 13 unique candidates")
    def safe(c):
        try:
            return verify(c)
        except Exception as exc:
            return {"id":c["candidate_id"],"museum_record_verified":False, "image_verified":False,
                    "eligible_for_review":False,"error":type(exc).__name__ + ": " + str(exc)[:200]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result = list(pool.map(safe, candidates))
    for item in result:
        print(item["id"], "meta", item["museum_record_verified"], "jpeg", item["image_verified"],
              item.get("error") or item.get("warnings"), flush=True)
    report = {"batch":"batch-014", "created_utc_by_github_actions":True,
              "source":"Met Official Object API and matching primary JPEG", "checked":len(result),
              "metadata_pass":sum(r["museum_record_verified"] for r in result),
              "images_pass":sum(r["image_verified"] for r in result),
              "eligible_for_curatorial_review":sum(r["eligible_for_review"] for r in result),
              "note":"HTTP, identity, JPEG and SHA256 verification are NOT human viewing or artistic review.",
              "results":result}
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")
    print("BATCH014_JSON_REPORT_START", flush=True)
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":")), flush=True)
    print("BATCH014_JSON_REPORT_END", flush=True)
    print("RESULT", report["metadata_pass"], report["images_pass"], len(result), flush=True)

if __name__ == "__main__":
    main()
