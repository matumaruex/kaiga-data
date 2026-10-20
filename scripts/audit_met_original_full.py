#!/usr/bin/env python3
"""Validate complete high-resolution Met JPEGs and add optional high_resolution metadata."""
import argparse, concurrent.futures, hashlib, io, json, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parents[1]
AP=ROOT/"data/artworks.json"
RP=ROOT/"data/image-sources.json"
MP=ROOT/"docs/met-original-image-audit.json"
OP=ROOT/"docs/met-original-full-jpeg-audit.json"
OPMD=ROOT/"docs/met-original-full-jpeg-audit.md"
HEADERS={"User-Agent":"KaigaMuseumVerify/1.0 (https://github.com/matumaruex/kaiga-data)"}
MAX_BYTES=16*1024*1024
VERIFICATION="complete_jpeg_sha256_and_downscale_match"

def fetch(url):
    last=None
    for delay in (0,1.5,3,6):
        if delay: time.sleep(delay)
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS), timeout=55) as resp:
                if resp.status!=200: raise ValueError("HTTP "+str(resp.status))
                raw=resp.read(MAX_BYTES+1)
                if len(raw)>MAX_BYTES: raise ValueError("Over 16MiB maximum")
                return raw
        except (urllib.error.URLError,TimeoutError,ValueError,OSError) as e:
            last=e
            if isinstance(e,urllib.error.HTTPError) and e.code not in (403,429,500,502,503,504):break
    raise RuntimeError(type(last).__name__+": "+str(last)[:100])

def decode(raw):
    if len(raw)<1024 or not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):
        raise ValueError("Missing JPEG start/end signature")
    with Image.open(io.BytesIO(raw)) as check:
        if check.format!="JPEG": raise ValueError("Not JPEG")
        check.verify()
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        return im.convert("RGB")

def check(pair):
    art,entry=pair
    id=art["id"]
    row={"id":id,"title":art["facts"]["title_original"],"status":"needs_review",
         "original_url":entry.get("original_url"),"official_api_confirmed":bool(entry.get("official_api")),
         "original_valid":False,"small_valid":False,"promotable":False}
    try:
        original_url=entry["original_url"]
        small_url=art["image"]["display_url"]
        if entry.get("status")!="measured" or small_url.replace("/web-large/","/original/")!=original_url:
            raise ValueError("Original not confirmed as equivalent filename")
        if "/web-large/" not in small_url or not original_url.startswith("https://images.metmuseum.org/"):
            raise ValueError("Unexpected Met file path")
        if not art["facts"]["is_public_domain_at_source"] or art["facts"]["type"]!="Painting":
            raise ValueError("Rights or type not approved in catalog")
        raw=fetch(original_url)
        original=decode(raw)
        if list(original.size)!=[entry["width"],entry["height"]]:raise ValueError("Original dimensions changed")
        row.update(original_valid=True,width=original.width,height=original.height,
            original_bytes=len(raw),original_sha256=hashlib.sha256(raw).hexdigest())
        lowraw=fetch(small_url)
        low=decode(lowraw)
        if hashlib.sha256(lowraw).hexdigest()!=art["image"]["sha256"] or len(lowraw)!=art["image"]["byte_length"]:
            raise ValueError("Registered small-image bytes changed")
        row["small_valid"]=True
        aspect_diff=abs(original.width/original.height-low.width/low.height)
        img1=original.resize((128,128),Image.Resampling.LANCZOS)
        img2=low.resize((128,128),Image.Resampling.LANCZOS)
        delta=round(sum(ImageStat.Stat(ImageChops.difference(img1,img2)).mean)/3,2)
        factor=round(original.width*original.height/(low.width*low.height),2)
        row.update(mean_rgb_delta=delta,aspect_difference=round(aspect_diff,4),pixel_multiplier=factor)
        if aspect_diff>0.025 or delta>24:raise ValueError("Possible content/crop mismatch")
        if factor<=1.5:
            row["status"]="no_improvement"
        else:
            row["status"]="verified"
            row["promotable"]=True
    except Exception as e:
        row["error"]=str(e)[:180]
    return row

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--promote",action="store_true")
    args=parser.parse_args()
    db=json.loads(AP.read_text(encoding="utf-8"))
    reg=json.loads(RP.read_text(encoding="utf-8"))
    audit=json.loads(MP.read_text(encoding="utf-8"))
    met={x["id"]:x for x in audit["records"]}
    rec={x["id"]:x["image_source"] for x in reg["records"]}
    pairs=[(a,met[a["id"]]) for a in db["artworks"] if a["id"].startswith("met-")]
    if len(pairs)!=249:raise RuntimeError("Expected 249 works")
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
        result=list(ex.map(check,pairs))
    byid={r["id"]:r for r in result}
    now=datetime.now(timezone.utc).isoformat()
    promoted=[]
    if args.promote:
        for a in db["artworks"]:
            r=byid.get(a["id"])
            if not r or not r["promotable"]:continue
            old=rec[a["id"]]
            if old["sha256"]!=a["image"]["sha256"]:raise RuntimeError("Legacy image hash mismatch")
            if a["image"].get("high_resolution") or old.get("high_resolution"):
                if a["image"].get("high_resolution")!=old.get("high_resolution"):
                    raise RuntimeError("Prior high-res inconsistent: "+a["id"])
                continue
            meta={"url":r["original_url"],"sha256":r["original_sha256"],
                "byte_length":r["original_bytes"],"width":r["width"],"height":r["height"],
                "verification":VERIFICATION,
                "source_identity_basis":("Met API primaryImage" if r["official_api_confirmed"] else "prior Met PD record + matching filenames and downscale imagery; current API blocked"),
                "last_full_sha_checked_on":now[:10],"human_visual_checked":False}
            a["image"]["high_resolution"]=dict(meta)
            old["high_resolution"]=dict(meta)
            promoted.append(a["id"])
        if promoted:
            AP.write_text(json.dumps(db,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            RP.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    bad=[x for x in result if x["status"]=="needs_review"]
    nochange=[x for x in result if x["status"]=="no_improvement"]
    good=[x for x in result if x["status"]=="verified"]
    summary={"total":len(result),"full_original_valid":sum(x["original_valid"] for x in result),
        "small_sha256_verified":sum(x["small_valid"] for x in result),
        "upgradable":len(good),"no_improvement":len(nochange),"needs_review":len(bad),
        "promoted":len(promoted),"upgradable_without_current_api":sum(not x["official_api_confirmed"] for x in good)}
    OP.write_text(json.dumps({"checked_utc":now,"method":"Full JPEG SHA256, Pillow verify, registered small JPEG SHA256, downscaled RGB and aspect match; NOT manual visual approval.","summary":summary,"records":result},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Met249件：高解像度JPEG全量照合","",f"UTC: {now}","",*[f"- {k}: {v}" for k,v in summary.items()],"",
      "元の画像台帳のSHA256と縮小版は保存したまま、合格作品だけ high_resolution を追加。","画像の構図と色の人間の最終審査は未了。","",
      "## 保留・改善なし",""]
    for r in bad+nochange:lines.append(f'- {r["id"]}: {r["title"]} / {r.get("error",r["status"])}')
    lines+=["","画像別のSHA256と差分は met-original-full-jpeg-audit.json を参照。",""]
    OPMD.write_text("\n".join(lines),encoding="utf-8")
    print("SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)
    print("REVIEW "+json.dumps(bad[:20],ensure_ascii=False),flush=True)

if __name__=="__main__":main()
