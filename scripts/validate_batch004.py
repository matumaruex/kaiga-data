#!/usr/bin/env python3
"""第4群10候補: ID/主補助タグ・シカゴ現行API・Commons JPEGを独立して検証する。"""
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
HEADERS = {"User-Agent":"KaigaMuseumResearch/0.1 (rights-and-metadata verification; contact via GitHub matumaruex/kaiga-data)", "Accept":"application/json,image/jpeg,*/*"}
def fetch(url, limit=6000000):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req,timeout=30) as rsp:
        if rsp.status != 200: raise RuntimeError("HTTP "+str(rsp.status))
        raw=rsp.read(limit+1)
        if len(raw)>limit: raise ValueError("response size limit exceeded")
        return raw, rsp.headers.get("Content-Type","")
def title_norm(x):
    return re.sub(r"[^a-z0-9]+","",str(x).lower())
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--online",action="store_true")
    p.add_argument("--require-all",action="store_true")
    p.add_argument("--output",default="artifacts/batch004-live-verification.json")
    args=p.parse_args()
    works=json.loads((ROOT/"data/candidates-batch-004.json").read_text(encoding="utf-8"))["works"]
    catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    vocabulary=json.loads((ROOT/"data/emotions.json").read_text(encoding="utf-8"))["emotions"]
    existing={x["id"] for x in catalog}
    ids=set()
    errors=[]
    for a in works:
        id_=a["id"];src=a["source"];image=a["image"];tags=a["emotion_categories"]
        if id_ in existing or id_ in ids or id_!="aic-"+str(src["artwork_id"]): errors.append(id_+" duplicate or bad ID")
        ids.add(id_)
        if not a["facts_provisional"]["accession_number"] in image["commons_file_title"]: errors.append(id_+" image accession mismatch")
        if not (1<=len(tags["primary"])<=2 and len(tags["secondary"])<=2): errors.append(id_+" primary/secondary limit")
        both=tags["primary"]+tags["secondary"]
        if len(both)!=len(set(both)) or any(t not in vocabulary for t in both): errors.append(id_+" unknown/duplicate emotion")
        if a["meaning_basis"]["author_intent"]["status"]!="not_verified_for_this_work" or a["meaning_basis"]["author_intent"]["summary"] is not None: errors.append(id_+" fabricated author quote")
        if not a["meaning_basis"]["scholarly_interpretation"]["source_url"].startswith("https://"): errors.append(id_+" no expert source")
        if a["review"]["interpretation_human_approved"] is not False: errors.append(id_+" approval flag")
    if errors: raise ValueError("; ".join(errors))
    print("STRUCTURE OK: "+str(len(works))+" candidate records; no new exhibition entries.",flush=True)
    if not args.online: return
    records=[]
    for i,a in enumerate(works,1):
        n=a["source"]["artwork_id"];id_=a["id"]
        record={"id":id_,"api_ok":False,"image_ok":False,"accession_number":a["facts_provisional"]["accession_number"],"commons_file_title":a["image"]["commons_file_title"]}
        try:
            url=a["source"]["api_url"]+"?fields=id,title,artist_title,date_display,artwork_type_title,image_id,is_public_domain"
            buf,_=fetch(url)
            j=json.loads(buf)["data"]
            if j["id"]!=n: raise ValueError("artwork ID mismatch")
            if title_norm(j["title"])!=title_norm(a["facts_provisional"]["title"]): raise ValueError("title mismatch: "+j["title"])
            if j.get("is_public_domain") is not True or (j.get("artwork_type_title") or "").lower()!="painting": raise ValueError("not PD painting")
            if not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",j.get("image_id") or ""): raise ValueError("invalid image uuid")
            record.update(api_ok=True,official={"id":n,"title":j["title"],"artist_title":j.get("artist_title"),"date_display":j.get("date_display"),"artwork_type_title":j["artwork_type_title"],"is_public_domain":True,"image_id":j["image_id"]})
            print(f"[{i}/{len(works)}] API OK {id_}: {j['title']} | {j.get('artist_title')} | image_id={j['image_id']}",flush=True)
        except Exception as exc:
            record["api_error"]=type(exc).__name__+": "+str(exc)[:200]
            print(f"[{i}/{len(works)}] API PENDING {id_}: {record['api_error']}",flush=True)
        try:
            query=urllib.parse.urlencode({"action":"query","format":"json","prop":"imageinfo","titles":a["image"]["commons_file_title"],"iiprop":"url|size|mime|extmetadata","iiurlwidth":"960"})
            buf,_=fetch("https://commons.wikimedia.org/w/api.php?"+query)
            page=next(iter(json.loads(buf)["query"]["pages"].values()))
            if "missing" in page or not page.get("imageinfo"): raise ValueError("Commons file not found")
            meta=page["imageinfo"][0]
            if meta.get("mime")!="image/jpeg": raise ValueError("not JPEG")
            url=meta.get("thumburl") or meta["url"]
            raw,_=fetch(url)
            if len(raw)<1024 or raw[:3]!=bytes((0xff,0xd8,0xff)): raise ValueError("invalid JPEG")
            lic=meta.get("extmetadata",{}).get("LicenseShortName",{}).get("value","")
            record.update(image_ok=True,image={"download_url":url,"size_bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"commons_page_url":a["image"]["commons_file_page"],"verified_file_title":page.get("title"),"license_short_name":lic})
            print(f"[{i}/{len(works)}] IMAGE OK {id_}: {len(raw)}B SHA256={record['image']['sha256']} LICENSE={lic} URL={url}",flush=True)
        except Exception as exc:
            record["image_error"]=type(exc).__name__+": "+str(exc)[:200]
            print(f"[{i}/{len(works)}] IMAGE PENDING {id_}: {record['image_error']}",flush=True)
        records.append(record)
        time.sleep(.25)
    out=ROOT/args.output
    out.parent.mkdir(parents=True,exist_ok=True)
    result={"checked":len(records),"api_passed":sum(x["api_ok"] for x in records),"image_passed":sum(x["image_ok"] for x in records),"both_passed":sum(x["api_ok"] and x["image_ok"] for x in records),"records":records}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"SUMMARY: API {result['api_passed']}/{len(records)} IMAGE {result['image_passed']}/{len(records)} BOTH {result['both_passed']}/{len(records)}",flush=True)
    if args.require_all and result["both_passed"]!=len(records):raise SystemExit(1)

if __name__=="__main__":main()
