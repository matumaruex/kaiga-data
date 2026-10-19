#!/usr/bin/env python3
"""Batch 019: verify official Met Object API and primary web-large JPEG integrity.
Does not register works or imply artwork interpretation/publication approval."""
import concurrent.futures
import hashlib
import json
import time
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
api="https://collectionapi.metmuseum.org/public/collection/v1/objects/"
HEAD={"User-Agent":"KaigaData-ArtworkAudit/0.5 (matumaruex/kaiga-data)","Accept":"application/json,image/jpeg"}
def retrieve(url,limit=12_000_000):
    err=None
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=25) as f:
                b=f.read(limit+1)
                if f.status!=200 or len(b)>limit:raise ValueError("Bad HTTP or size")
                return b,f.headers.get("Content-Type","")
        except Exception as e:err=e;time.sleep(i+1)
    raise err
def check(c):
    id=c["museum_object_id"]
    r={"id":c["candidate_id"],"metadata_verified":False,"image_verified":False,"problems":[]}
    try:
        body,_=retrieve(api+str(id),1_500_000)
        x=json.loads(body)
        for key in ("objectID","title","artistDisplayName","objectDate","accessionNumber","isPublicDomain","classification","objectName","medium","primaryImageSmall","primaryImage"):
            r[key]=x.get(key)
        cls=(x.get("classification") or "").casefold()
        medium=(x.get("medium") or "").casefold()
        ispaint=cls=="paintings" or (not cls and x.get("objectName")=="Painting" and ("oil" in medium or "tempera" in medium))
        flags={"id":x.get("objectID")==id,"painting":ispaint,"pd":x.get("isPublicDomain") is True,"accession":bool(x.get("accessionNumber")),"title":bool(x.get("title")),"artist":bool(x.get("artistDisplayName")) or not x.get("artistDisplayName")}
        r["metadata_checks"]=flags
        r["metadata_verified"]=all(flags.values())
        if not r["metadata_verified"]:r["problems"] += [k+" mismatch" for k,v in flags.items() if not v]
        u=x.get("primaryImageSmall") or ""
        if not u.startswith("https://images.metmuseum.org/"):raise ValueError("No official primary JPEG")
        image,mime=retrieve(u)
        if len(image)<5000 or not image.startswith(bytes((255,216,255))) or not image.endswith(bytes((255,217))):raise ValueError("Incomplete JPEG")
        if "jpeg" not in mime.lower():raise ValueError("Not image/jpeg: "+mime)
        r.update(image_verified=True,image_url_verified=u,image_sha256=hashlib.sha256(image).hexdigest(),image_bytes=len(image),image_content_type=mime)
    except Exception as e:r["problems"].append(type(e).__name__+": "+str(e)[:140])
    return r
def main():
    cs=json.loads((ROOT/"data/candidates-batch-021.json").read_text("utf-8"))["works"]
    if len(cs)!=20:raise ValueError("Expected 20 candidates")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as p:rows=list(p.map(check,cs))
    report={"checked":len(rows),"metadata_pass":sum(x["metadata_verified"] for x in rows),"image_pass":sum(x["image_verified"] for x in rows),"results":rows}
    (ROOT/"artifacts").mkdir(exist_ok=True)
    (ROOT/"artifacts"/"batch021-evidence.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n","utf-8")
    for r in rows:print("CHECK",r["id"],r.get("title"),"meta",r["metadata_verified"],"image",r["image_verified"],r["problems"],flush=True)
    print("BATCH021_EVIDENCE_START",flush=True)
    print(json.dumps(report,ensure_ascii=False,separators=(",",":")),flush=True)
    print("BATCH021_EVIDENCE_END",flush=True)
    if report["metadata_pass"]!=20 or report["image_pass"]!=20:raise SystemExit("Not all candidates ready")
if __name__=="__main__":main()
