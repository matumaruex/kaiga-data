#!/usr/bin/env python3
"""Read-only source audit for newly added Met paintings, batch 018.
Official Met Object API is authoritative for identity, rights, classification,
accession, dates, and primary JPEG URL. Download full web-large JPEG and SHA256.
This does not approve image depiction, interpretations or legal publication.
"""
import concurrent.futures
import hashlib
import json
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
HEADERS = {"User-Agent": "KaigaData-SourceAudit/1.0 (https://github.com/matumaruex/kaiga-data)", "Accept": "application/json,image/jpeg,*/*"}
OUT = ROOT / "artifacts" / "batch018-live-check.json"

def download(url, cap=15_000_000):
    host = urllib.parse.urlparse(url)
    if host.scheme != "https" or host.hostname not in ("collectionapi.metmuseum.org", "images.metmuseum.org"):
        raise ValueError("unexpected official source hostname")
    last = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=35) as response:
                if response.status != 200:
                    raise ValueError("bad HTTP status " + str(response.status))
                b = response.read(cap + 1)
                if len(b) > cap:
                    raise ValueError("file exceeds size cap")
                return b, response.headers.get("Content-Type", "")
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429,500,502,503,504):
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("retry exhausted: " + str(last))

def norm(v):
    return " ".join("".join(c for c in unicodedata.normalize("NFKD",str(v or "").casefold()) if not unicodedata.combining(c)).split())

def inspect(c):
    ident = c["candidate_id"]
    result = {"id": ident, "object_id": c["museum_object_id"], "metadata_ok": False, "image_ok": False, "problems": []}
    try:
        raw, typ = download(API + str(c["museum_object_id"]), 1_500_000)
        item = json.loads(raw)
        for field in ("objectID", "title", "artistDisplayName", "objectDate", "accessionNumber", "isPublicDomain", "classification", "objectName", "medium", "primaryImageSmall", "primaryImage"):
            result[field] = item.get(field)
        matches = {
          "objectID": item.get("objectID") == c["museum_object_id"],
          "title": norm(item.get("title")) == norm(c["title_original"]),
          "artist": norm(c["artist"]) in norm(item.get("artistDisplayName")),
          "public_domain": item.get("isPublicDomain") is True,
          "painting_class": norm(item.get("classification")) == "paintings" or (not norm(item.get("classification")) and norm(item.get("objectName")) == "painting" and "oil on canvas" in norm(item.get("medium"))),
          "accession": bool(item.get("accessionNumber")),
        }
        result["metadata_checks"] = matches
        result["metadata_ok"] = all(matches.values())
        result["problems"] += [k + " mismatch" for k, valid in matches.items() if not valid]
        u = item.get("primaryImageSmall") or item.get("primaryImage") or ""
        if urllib.parse.urlparse(u).hostname != "images.metmuseum.org":
            result["problems"].append("primary image is not official")
            return result
        jpeg, mime = download(u)
        if len(jpeg) <= 5000 or not jpeg.startswith(bytes((255,216,255))) or not jpeg.endswith(bytes((255,217))):
            raise ValueError("incomplete JPEG")
        if "jpeg" not in mime.lower() and "jpg" not in mime.lower():
            raise ValueError("not a JPEG content-type: " + mime)
        result.update(image_url_verified=u,image_sha256=hashlib.sha256(jpeg).hexdigest(),
                      image_bytes=len(jpeg),image_content_type=mime,image_ok=True)
    except Exception as exc:
        result["problems"].append(type(exc).__name__ + ": " + str(exc)[:200])
    return result

def main():
    j = json.loads((ROOT/"data/candidates-batch-018.json").read_text("utf-8"))
    cs = j["works"]
    if len(cs) != 18 or len({x["candidate_id"] for x in cs}) != 18:
        raise ValueError("Expect exactly 18 distinct candidate IDs")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(inspect,cs))
    for row in rows:
        print(row["id"], "metadata",row["metadata_ok"],"image",row["image_ok"],"problems:", row["problems"],flush=True)
    report={"batch":"batch-018","official_api":API,"checked":len(rows),"metadata_pass":sum(x["metadata_ok"] for x in rows),
            "image_pass":sum(x["image_ok"] for x in rows),"results":rows,
            "scope":"Current Met Object API and complete official primary JPEG, byte length, digest. No human visual/interpretation approval."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("BATCH018_JSON_START",flush=True)
    print(json.dumps(report,ensure_ascii=False,separators=(",",":")),flush=True)
    print("BATCH018_JSON_END",flush=True)
    print("BATCH018_SUMMARY",report["metadata_pass"],report["image_pass"],len(rows),flush=True)
    if report["metadata_pass"]!=len(rows) or report["image_pass"]!=len(rows):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
