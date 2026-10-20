#!/usr/bin/env python3
"""Read-only online delivery audit of 51 AIC display images.

No unreviewed update to artwork/image registry hashes: a new image may not be
the same artwork even if it can be decoded. This reports changed/blocked URLs.
"""
from __future__ import annotations
import concurrent.futures,hashlib,json,time,urllib.error,urllib.request
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/aic-image-live-audit.json"
ARTS=[x for x in json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"] if x["id"].startswith("aic-")]
HEAD={"User-Agent":"Mozilla/5.0 (compatible; ArtCollectionQA/1.0; +https://github.com/matumaruex/kaiga-data)","Accept":"image/jpeg,image/*;q=0.8"}
def inspect(a):
    r={"id":a["id"],"url":a["image"]["display_url"],"status":"failed"}
    last=None
    for wait in [0,2,5]:
        if wait:time.sleep(wait)
        try:
            req=urllib.request.Request(r["url"],headers=HEAD)
            with urllib.request.urlopen(req,timeout=28) as response:
                raw=response.read(16*1024*1024+1)
                if len(raw)>16*1024*1024:raise ValueError("Larger than 16MiB")
                if not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):
                    raise ValueError("JPEG signature/terminator wrong")
                digest=hashlib.sha256(raw).hexdigest()
                r.update(status="match" if digest==a["image"]["sha256"] and len(raw)==a["image"]["byte_length"] else "content_changed",
                         image_bytes=len(raw),sha256=digest,original_sha256=a["image"]["sha256"],
                         original_bytes=a["image"]["byte_length"])
                return r
        except (urllib.error.URLError,TimeoutError,ValueError,OSError) as exc:
            last=exc
            if isinstance(exc,urllib.error.HTTPError) and exc.code not in (403,429,500,502,503,504):
                break
    r["error"]=str(last)[:150]
    return r
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as workers:
        records=list(workers.map(inspect,ARTS))
    summary={"total":len(records),"match":sum(x["status"]=="match" for x in records),
      "content_changed":sum(x["status"]=="content_changed" for x in records),
      "failed":sum(x["status"]=="failed" for x in records)}
    payload={"checked_utc":datetime.now(timezone.utc).isoformat(),"summary":summary,"records":records,
        "caution":"A SHA256 mismatch or HTTP block is an actionable live-source issue; no automatic content change or visual approval."}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("SUMMARY "+json.dumps(summary,ensure_ascii=False))
    print("ISSUES "+json.dumps([x for x in records if x["status"]!="match"],ensure_ascii=False))
if __name__=="__main__":
    main()
