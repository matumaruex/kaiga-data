#!/usr/bin/env python3
"""Resolve Met-823663 stale web-large hash without changing historical image data."""
import hashlib,io,json,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
R=Path(__file__).resolve().parents[1]
AP=R/"data/artworks.json"; RP=R/"data/image-sources.json"
REPORT=R/"docs/met-original-full-jpeg-audit.json"
LOG=R/"docs/met-823663-followup.json"
ID="met-823663"
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"KaigaImageFollowup/1.0"})
    with urllib.request.urlopen(req,timeout=60) as response:return response.read(16*1024*1024)
def img(raw):
    if not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):raise ValueError("JPEG signature")
    with Image.open(io.BytesIO(raw)) as v:
        v.load(); return v.convert("RGB")
db=json.loads(AP.read_text(encoding="utf-8"))
reg=json.loads(RP.read_text(encoding="utf-8"))
audit=json.loads(REPORT.read_text(encoding="utf-8"))
old=next(a for a in db["artworks"] if a["id"]==ID)
rec=next(a["image_source"] for a in reg["records"] if a["id"]==ID)
r=next(a for a in audit["records"] if a["id"]==ID)
if not r["official_api_confirmed"] or not r["original_valid"] or old["image"]["sha256"]!=rec["sha256"]:
    raise RuntimeError("Prior official or legacy verification missing")
a=get(r["original_url"]); original=img(a)
if hashlib.sha256(a).hexdigest()!=r["original_sha256"] or len(a)!=r["original_bytes"]:
    raise RuntimeError("Original bytes changed since audit")
b=get(old["image"]["display_url"]); small=img(b)
delta=sum(ImageStat.Stat(ImageChops.difference(
  original.resize((128,128),Image.Resampling.LANCZOS),
  small.resize((128,128),Image.Resampling.LANCZOS))).mean)/3
aspect=abs(original.width/original.height-small.width/small.height)
promote=aspect<=0.025 and delta<=24 and original.width*original.height>1.5*small.width*small.height
out={"id":ID,"current_small_sha256":hashlib.sha256(b).hexdigest(),
     "recorded_old_small_sha256":old["image"]["sha256"],
     "original_sha256":r["original_sha256"],
     "pixel_distance":round(delta,3),"aspect_difference":round(aspect,4),
     "approved_for_high_resolution":promote,
     "note":"Old low-res SHA256 remains unchanged as historical evidence. Current Met small JPEG bytes appear to have been re-encoded."}
if promote:
    high={"url":r["original_url"],"sha256":r["original_sha256"],
        "byte_length":r["original_bytes"],"width":original.width,"height":original.height,
        "verification":"complete_jpeg_sha256_and_downscale_match",
        "source_identity_basis":"Met Object API, complete original JPEG, present low-res content comparison; old low-res hash stale",
        "last_full_sha_checked_on":datetime.now(timezone.utc).date().isoformat(),
        "human_visual_checked":False}
    old["image"]["high_resolution"]=high
    rec["high_resolution"]=dict(high)
    AP.write_text(json.dumps(db,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    RP.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
LOG.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(out,ensure_ascii=False))
if not promote:raise SystemExit(2)
