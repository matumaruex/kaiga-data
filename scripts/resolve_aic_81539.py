#!/usr/bin/env python3
"""Repair exactly one verified Wikimedia thumbnail re-encoding.

Keeps historical batch-005 source evidence untouched. Requires matching Met/AIC
accession file, an exact checksum captured in live audit, and a pixel comparison
against the corresponding Wikimedia full-size file. No automatic general repairs.
"""
import hashlib,io,json,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"data/artworks.json";REG=ROOT/"data/image-sources.json"
REPORT=ROOT/"docs/aic-image-live-audit.json"
OUT=ROOT/"docs/aic-81539-thumbnail-recheck.json"
ID="aic-81539"
OLD="6c79ad01bb8ba7d46b506656df003ac66c09ceb3a9d3b4f0b230b421f2809ed8"
CURRENT="37fa37553449fc55672d84c5991c42f8a4e04d60d5e9d730fabe77ebd79a6ca1"
AGENT={"User-Agent":"ArtMuseumIntegrityCheck/1.0 (+https://github.com/matumaruex/kaiga-data)"}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=AGENT),timeout=45) as response:
        if response.status!=200:raise RuntimeError("HTTP "+str(response.status))
        data=response.read(20*1024*1024+1)
    if len(data)>20*1024*1024:raise RuntimeError("Image exceeds limit")
    if not data.startswith(b"\xff\xd8\xff") or not data.endswith(b"\xff\xd9"):
        raise RuntimeError("Invalid JPEG signature/end")
    return data

def image(data):
    with Image.open(io.BytesIO(data)) as p:
        if p.format!="JPEG":raise RuntimeError("Not JPEG")
        p.load()
        return p.convert("RGB")

def main():
    data=json.loads(ART.read_text(encoding="utf-8"))
    registry=json.loads(REG.read_text(encoding="utf-8"))
    evidence=json.loads(REPORT.read_text(encoding="utf-8"))
    art=next(x for x in data["artworks"] if x["id"]==ID)
    record=next(x["image_source"] for x in registry["records"] if x["id"]==ID)
    checked=next(x for x in evidence["records"] if x["id"]==ID)
    if art["facts"]["title_original"]!="On the Bank of the Seine, Bennecourt" or art["facts"]["accession_number"]!="1922.427":
        raise RuntimeError("Artwork identity changed")
    if checked["sha256"]!=CURRENT or checked["status"]!="content_changed":
        raise RuntimeError("Measured source evidence changed")
    if art["image"]["sha256"]!=OLD or record["sha256"]!=OLD:
        raise RuntimeError("Historical hash changed; abort repair")
    if art["image"]["display_url"]!=record["verified_download_url"] or art["image"]["byte_length"]!=record["byte_length"]:
        raise RuntimeError("Original registry not aligned")
    parsed=urllib.parse.urlsplit(art["image"]["display_url"])
    if parsed.hostname!="thumb.wikimedia.org" or "/wikipedia/commons/thumb/f/f8/" not in parsed.path:
        raise RuntimeError("Unexpected Wikimedia thumbnail origin")
    original_path="/wikipedia/commons/"+parsed.path.split("/wikipedia/commons/thumb/",1)[1].rsplit("/",1)[0]
    original_url="https://upload.wikimedia.org"+original_path
    smallbytes=fetch(art["image"]["display_url"])
    fullbytes=fetch(original_url)
    small=image(smallbytes)
    full=image(fullbytes)
    current_sha=hashlib.sha256(smallbytes).hexdigest()
    if current_sha!=CURRENT or len(smallbytes)!=333233:
        raise RuntimeError("Wikimedia thumbnail changed again; refuse unsafe metadata update")
    if small.width!=960:raise RuntimeError("Unexpected thumbnail dimensions")
    aspect=abs(small.width/small.height-full.width/full.height)
    delta=sum(ImageStat.Stat(ImageChops.difference(
        small.resize((128,128),Image.Resampling.LANCZOS),
        full.resize((128,128),Image.Resampling.LANCZOS))).mean)/3
    if aspect>0.012 or delta>12:
        raise RuntimeError(f"Thumb does not reliably match original artwork (aspect={aspect}, delta={delta})")
    art["image"]["sha256"]=current_sha
    art["image"]["byte_length"]=len(smallbytes)
    record["sha256"]=current_sha
    record["byte_length"]=len(smallbytes)
    record["last_http_sha_checked_on"]=datetime.now(timezone.utc).date().isoformat()
    record["thumbnail_regeneration_note"]="Current Wikimedia thumbnail was re-encoded; prior verified checksum preserved in docs/aic-81539-thumbnail-recheck.json"
    ART.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    detail={"id":ID,"artwork_accession":"1922.427","checked_utc":datetime.now(timezone.utc).isoformat(),
        "thumbnail_url":art["image"]["display_url"],"original_url":original_url,
        "historical_sha256":OLD,"historical_bytes":332472,"updated_sha256":CURRENT,"updated_bytes":len(smallbytes),
        "original_sha256":hashlib.sha256(fullbytes).hexdigest(),
        "original_size":[full.width,full.height],"thumbnail_size":[small.width,small.height],
        "aspect_difference":round(aspect,6),"average_rgb_difference_128px":round(delta,4),
        "interpretation":"Same source filename, same artwork via image downscale comparison. Thumbnail bytes changed. No human visual approval."}
    OUT.write_text(json.dumps(detail,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(detail,ensure_ascii=False))

if __name__=="__main__":main()
