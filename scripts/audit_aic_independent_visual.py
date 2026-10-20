#!/usr/bin/env python3
"""Read-only identity comparison: registered AIC images vs independent AIC IIIF images.
This cannot automatically confer artwork verified status; inspect evidence manually.
Writes only artifacts/; does not change data/artworks.json or data/image-sources.json.
"""
import hashlib
import io
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/aic-independent-visual"
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "ArtCollectionAudit/1.0 (https://github.com/matumaruex/kaiga-data)", "Accept": "application/json,image/jpeg,image/*;q=0.8"}
TIMEOUT = 18

def fetch(url, max_bytes=18_000_000):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = resp.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("response exceeds maximum allowed bytes")
    return data

def error_name(ex):
    if isinstance(ex, urllib.error.HTTPError):
        return "HTTP_" + str(ex.code)
    return type(ex).__name__ + ": " + str(ex)[:120]

def dhash(img):
    gray = ImageOps.grayscale(img).resize((9,8), Image.Resampling.LANCZOS)
    p = list(gray.getdata())
    return sum((1 << (y*8+x)) for y in range(8) for x in range(8) if p[y*9+x] > p[y*9+x+1])

def difference(a,b):
    pa, pb = dhash(a), dhash(b)
    hd=(pa ^ pb).bit_count()
    a1=ImageOps.grayscale(a).resize((64,64))
    b1=ImageOps.grayscale(b).resize((64,64))
    mad=round(sum(abs(x-y) for x,y in zip(a1.getdata(),b1.getdata()))/(64*64),2)
    return hd, mad

def first_image(urls):
    errors=[]
    for url in urls:
        try:
            raw=fetch(url)
            im=Image.open(io.BytesIO(raw))
            im.load()
            return im.convert("RGB"),raw,url,errors
        except Exception as ex:
            errors.append(url.split("/")[2] + ": " + error_name(ex))
    return None,None,None,errors

def panel(src, official, r):
    im=Image.new("RGB",(760,274),"#f0f0f0")
    draw=ImageDraw.Draw(im)
    draw.text((8,6),r["id"]+" | "+r["title"][:49],fill="black")
    for i,(painting,name) in enumerate([(src,"REGISTERED"),(official,"AIC IIIF")]):
        bx=8+i*380
        draw.text((bx,24),name,fill="black")
        if painting:
            thumb=painting.copy()
            thumb.thumbnail((355,224))
            im.paste(thumb,(bx+(355-thumb.width)//2,45+(224-thumb.height)//2))
        else:
            draw.text((bx+50,120),"NOT RETRIEVED",fill="#aa2222")
    return im

def main():
    arts = json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    ids={a["id"] for a in arts if a["id"].startswith("aic-")}
    rows=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
    aics=sorted((r for r in rows if r["id"] in ids),key=lambda r:int(r["id"][4:]))
    print("Selected AIC artwork count",len(aics),flush=True)
    results=[]
    panels=[]
    api_blocked=0
    image_blocked=0
    for index,r in enumerate(aics):
        row={"id":r["id"],"title":r["title"],"registered_accession":r.get("accession_number"),"official_url":r.get("official_artwork_url")}
        source=r["image_source"]
        row["registered_image_sha256_expected"]=source.get("sha256")
        url=source.get("verified_download_url")
        src, src_raw, used, src_errors=first_image([url] if url else [])
        row["registered_image_fetch"]="ok" if src else "blocked"
        if src:
            row["registered_image_hash_match"]=hashlib.sha256(src_raw).hexdigest()==source.get("sha256")
            row["registered_image_bytes_match"]=len(src_raw)==source.get("byte_length")
            row["registered_dimensions"]=list(src.size)
        else:
            row["registered_image_errors"]=src_errors
        official=None
        if api_blocked>=3:
            row["official_api"]="skipped_after_three_access_errors"
        else:
            api_url="https://api.artic.edu/api/v1/artworks/"+r["id"][4:]+"?fields=id,title,image_id,main_reference_number,artist_display"
            try:
                obj=json.loads(fetch(api_url,1_500_000).decode("utf-8"))["data"]
                api_blocked=0
                row["official_api"]="ok"
                row["official_accession"]=obj.get("main_reference_number")
                row["official_title"]=obj.get("title")
                row["official_id_match"]=str(obj.get("id"))==r["id"][4:]
                row["official_accession_match"]=str(obj.get("main_reference_number"))==str(r.get("accession_number"))
                imid=obj.get("image_id")
                if imid and image_blocked<3:
                    base=[f"https://www.artic.edu/iiif/2/{imid}/full/400,/0/default.jpg",
                          f"https://lakeimagesweb.artic.edu/iiif/2/{imid}/full/400,/0/default.jpg"]
                    official,_,official_url,errors=first_image(base)
                    row["official_image_fetch"]="ok" if official else "blocked"
                    if official:
                        row["official_image_url"]=official_url
                        row["official_image_dimensions"]=list(official.size)
                        image_blocked=0
                    else:
                        image_blocked+=1
                        row["official_image_errors"]=errors
                elif not imid:
                    row["official_image_fetch"]="no_official_image_id"
                else:
                    row["official_image_fetch"]="skipped_after_three_access_errors"
            except Exception as ex:
                api_blocked+=1
                row["official_api"]=error_name(ex)
        if src and official:
            hd, mad=difference(src,official)
            row["visual_comparison"]="performed"
            row["dhash_distance_0_to_64"]=hd
            row["greyscale_mean_absolute_difference_0_to_255"]=mad
            row["visual_match_candidate"]= hd<=9 and mad<=42
        else:
            row["visual_comparison"]="not_performed"
        results.append(row)
        panels.append(panel(src,official,row))
        print(f'{index+1:02d}/{len(aics)} {r["id"]}: source={row["registered_image_fetch"]} AIC={row.get("official_image_fetch",row.get("official_api"))} visual={row["visual_comparison"]}',flush=True)
        time.sleep(1.0 if api_blocked<3 else 0.15)
    for i in range(0,len(panels),8):
        grid=Image.new("RGB",(1520,274*4),"white")
        for j,im in enumerate(panels[i:i+8]):
            grid.paste(im,((j%2)*760,(j//2)*274))
        grid.save(OUT/f"contact-{i//8+1:02d}.jpg",quality=84)
    counts={"total":len(results),"registered_decoded":sum(r["registered_image_fetch"]=="ok" for r in results),"registered_hash_match":sum(r.get("registered_image_hash_match",False) for r in results),"official_metadata_fetched":sum(r.get("official_api")=="ok" for r in results),"official_iiif_fetched":sum(r.get("official_image_fetch")=="ok" for r in results),"visual_compared":sum(r["visual_comparison"]=="performed" for r in results),"visual_match_candidates":sum(r.get("visual_match_candidate",False) for r in results),"visual_discrepancies_to_review":sum(r["visual_comparison"]=="performed" and not r.get("visual_match_candidate",False) for r in results)}
    payload={"utc":datetime.now(timezone.utc).isoformat(),"type":"read_only_aic_independent_image_audit","method":"registered downloaded JPEG versus official Chicago API and IIIF; dHash and grayscale MAD as triage only, not certified artwork identity","summary":counts,"records":results}
    (OUT/"result.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("AUDIT_SUMMARY "+json.dumps(counts),flush=True)

if __name__=="__main__":
    main()
