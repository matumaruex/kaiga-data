#!/usr/bin/env python3
"""Audit official Met full-resolution images for the registered Met artworks.

Read-only with respect to the artwork catalog. A partial JPEG fetch can reliably
read image dimensions, but does NOT prove full-file integrity or visual fidelity.
"""
from __future__ import annotations

import concurrent.futures
import io
import json
import re
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "docs/met-original-image-audit.json"
OUT_MD = ROOT / "docs/met-original-image-audit.md"
ITEMS = [x for x in json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))["artworks"] if x["id"].startswith("met-")]
OLD = {x["id"]:x for x in json.loads((ROOT / "docs/image-dimensions-audit.json").read_text(encoding="utf-8"))["records"]}
USER_AGENT = "KaigaImageAudit/1.0 (+https://github.com/matumaruex/kaiga-data; educational museum-image verification)"
API_BASE = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
HEADER = {"User-Agent":USER_AGENT,"Accept":"application/json,image/jpeg,*/*"}
LIMIT = 196608
MAX_DOWNLOAD = 20_000_000

def fetch(url, ranged=False):
    hdr = dict(HEADER)
    if ranged:
        hdr["Range"] = f"bytes=0-{LIMIT-1}"
        hdr["Accept"] = "image/jpeg,*/*"
    last=None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=hdr),timeout=25) as res:
                raw=res.read(LIMIT if ranged else MAX_DOWNLOAD + 1)
                return raw,dict(res.headers),res.status
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError) as exc:
            last=exc
            if isinstance(exc,urllib.error.HTTPError) and exc.code not in (403,429,500,502,503,504):
                break
            time.sleep([1.2,3.2,6.4][attempt])
    raise RuntimeError(f"{type(last).__name__}: {str(last)[:130]}")

def get_jpeg_dimensions(raw):
    # JPEG SOF occurs in headers before the compressed image data.
    with Image.open(io.BytesIO(raw)) as im:
        if im.format!="JPEG": raise ValueError(f"Unexpected image format: {im.format}")
        return im.size

def inspect(art):
    ident=art["id"]; old=OLD.get(ident,{})
    row={"id":ident,"title":art["facts"]["title_original"],"old_url":art["image"]["display_url"],
        "old_width":old.get("width"),"old_height":old.get("height"),"old_pixels":(old.get("width") or 0)*(old.get("height") or 0),
        "official_api":False,"original_url":None,"status":"not_checked"}
    try:
        data,_,_=fetch(API_BASE + str(art["source"]["artwork_id"]))
        info=json.loads(data)
        if info.get("objectID") != art["source"]["artwork_id"]:
            raise ValueError("API objectID different")
        if info.get("isPublicDomain") is not True:
            row["status"]="no_public_domain";return row
        row["official_api"]=True
        row["official_title"]=info.get("title")
        row["original_url"]=info.get("primaryImage") or None
        row["official_small_url"]=info.get("primaryImageSmall") or None
        row["same_small_as_registered"]=info.get("primaryImageSmall")==art["image"]["display_url"]
        row["same_accession"]=info.get("accessionNumber")==art["facts"].get("accession_number")
        if not row["original_url"]:
            row["status"]="official_no_original";return row
        if not row["original_url"].startswith("https://images.metmuseum.org/"):
            row["status"]="unexpected_original_host";return row
    except Exception as exc:
        # A predictable substitution helps triage. It is NOT proof of an
        # official API record, and must not be used for automatic replacement.
        row["api_error"]=str(exc)[:180]
        small=art["image"]["display_url"]
        if "/web-large/" not in small:
            row["status"]="api_failed_and_no_candidate";return row
        row["original_url"]=small.replace("/web-large/","/original/")
        row["url_source"]="derived_from_small_not_api_confirmed"
    try:
        raw,headers,http_status=fetch(row["original_url"],ranged=True)
        if len(raw) < 1000 or raw[:3]!=b"\xff\xd8\xff":
            raise ValueError("JPEG header is missing")
        w,h=get_jpeg_dimensions(raw)
        row.update(status="measured",width=w,height=h,
            pixels=w*h,megapixels=round(w*h/1_000_000,3),
            long_edge=max(w,h),short_edge=min(w,h),
            http_status=http_status,content_type=headers.get("Content-Type"),
            content_range=headers.get("Content-Range"),
            content_length_header=headers.get("Content-Length"),
            first_bytes_examined=len(raw),
            pixel_multiplier=round(w*h/row["old_pixels"],1) if row["old_pixels"] else None)
        row["resolution_improved"]=bool(row["old_pixels"] and w*h>row["old_pixels"]*1.5)
        row["sufficient_for_mobile_detail"]=min(w,h)>=900 and w*h>=1_000_000
        row["can_auto_update_metadata"]=bool(row["official_api"] and row["same_small_as_registered"] and row["same_accession"] and row["resolution_improved"])
    except Exception as exc:
        row["status"]="original_fetch_or_decode_error"
        row["image_error"]=str(exc)[:180]
    return row

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        records=list(pool.map(inspect,ITEMS))
    summary=dict(total=len(records),api_confirmed=sum(x["official_api"] for x in records),
        original_measured=sum(x["status"]=="measured" for x in records),
        larger_image=sum(x.get("resolution_improved",False) for x in records),
        full_res_mobile_detail=sum(x.get("sufficient_for_mobile_detail",False) for x in records),
        ready_for_next_verification=sum(x.get("can_auto_update_metadata",False) for x in records),
        api_problem=sum(bool(x.get("api_error")) for x in records),
        image_problem=sum(x["status"]=="original_fetch_or_decode_error" for x in records),
        official_small_image_diff=sum(x.get("same_small_as_registered") is False for x in records),
        accession_diff=sum(x.get("same_accession") is False for x in records))
    measured=[x for x in records if x["status"]=="measured"]
    if measured:
        factors=sorted(x["pixel_multiplier"] for x in measured if x.get("pixel_multiplier") is not None)
        summary["median_pixel_multiplier"]=factors[len(factors)//2] if factors else None
        summary["median_original_megapixels"]=sorted(x["megapixels"] for x in measured)[len(measured)//2]
    result={"checked_utc":datetime.now(timezone.utc).isoformat(),
      "warning":"Dimensions checked using partial JPEG bytes only. The full original JPEG was not downloaded or visually approved. Never switch production URLs automatically based only on this audit.",
      "summary":summary,"records":records}
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# メトロポリタン美術館 249作品・公式高解像度版の検査","",
        "検査日時（UTC）: "+result["checked_utc"],"",
        "## 集計","",
        *[f"- {k}: **{v}**" for k,v in summary.items()],"",
        "## 制約","",
        "Met Object APIの primaryImage URLにアクセスして、JPEGヘッダからピクセル寸法を調査した。ヘッダの部分取得だけでは画像ファイル全体の破損や、色・切り抜き・同一作品かの最終目視確認を保証しない。",
        "API取得に失敗した時の /web-large/ → /original/ 置換URLは推定扱い。実際に取得できても正規のAPIレコードとの照合完了とは見なさない。",
        "## 対応を要する作品","",
        "|ID|作品|状態|補足|","|---|---|---|---|"]
    concerns=[r for r in records if r["status"]!="measured" or not r.get("can_auto_update_metadata",False)]
    for x in concerns[:249]:
        msg=x.get("api_error") or x.get("image_error") or ("APIの縮小版URL/作品番号の差異" if x.get("official_api") else "API未照合")
        lines.append("|"+x["id"]+"|"+x["title"].replace("|","/")[:50]+"|"+x["status"]+"|"+str(msg).replace("|","/")[:120]+"|")
    lines+=["","## 解像度改善効果（改善倍率が大きい順、上位25件）","",
        "|ID|旧解像度|高解像度版|画素数倍率|","|---|---:|---:|---:|"]
    for x in sorted(measured,key=lambda t:t.get("pixel_multiplier") or 0,reverse=True)[:25]:
        lines.append(f'|{x["id"]}|{x.get("old_width")}×{x.get("old_height")}|{x["width"]}×{x["height"]}|{x.get("pixel_multiplier")}|')
    lines+=["","全249件の原画像URL・取得結果・解像度は `docs/met-original-image-audit.json` に保存。アプリの画像URLは変更していない。",""]
    OUT_MD.write_text("\n".join(lines),encoding="utf-8")
    print("SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)
    print("SAMPLES "+json.dumps(measured[:6],ensure_ascii=False),flush=True)
    print("PROBLEMS "+json.dumps(concerns[:12],ensure_ascii=False),flush=True)

if __name__=="__main__": main()
