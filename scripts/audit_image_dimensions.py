#!/usr/bin/env python3
"""Inspect all catalog display JPEGs: live download, SHA256, dimensions and contact sheets.

This is a technical quality audit, NOT human approval of artwork/cropping/colors.
Does not edit artwork records or image source records.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import io
import json
import math
import os
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
ARTS = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))["artworks"]
OUT_JSON = ROOT / "docs/image-dimensions-audit.json"
OUT_MD = ROOT / "docs/image-dimensions-audit.md"
CONTACT = ROOT / "artifacts/image-contact-sheets"
CONTACT.mkdir(parents=True, exist_ok=True)
HEADER = {"User-Agent": "KaigaImageQA/1.0 (github.com/matumaruex/kaiga-data; museum image research)", "Accept": "image/jpeg,image/*;q=0.8"}
MAX_BYTES = 8_000_000

def get_image(url):
    last = None
    for i in range(5):
        try:
            req = urllib.request.Request(url, headers=HEADER)
            with urllib.request.urlopen(req, timeout=28) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise RuntimeError("Exceeded 8MB download cap")
                return raw
        except (TimeoutError, urllib.error.URLError, RuntimeError, OSError) as exc:
            last = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                break
            time.sleep(min(16, 2 ** i + (i % 3) * 0.25))
    raise RuntimeError(f"{type(last).__name__}: {str(last)[:180]}")

def inspect(index_and_art):
    index, art = index_and_art
    ident = art["id"]
    info = art["image"]
    result = {
        "index": index, "id": ident, "title": art["facts"]["title_original"],
        "museum": art["source"]["museum"],
        "url": info["display_url"], "status": "failed"
    }
    try:
        raw = get_image(info["display_url"])
        sha = hashlib.sha256(raw).hexdigest()
        result["downloaded_bytes"] = len(raw)
        result["sha256_match"] = sha == info.get("sha256")
        result["bytes_match"] = len(raw) == info.get("byte_length")
        if not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):
            raise ValueError("JPEG signature/end marker invalid")
        with Image.open(io.BytesIO(raw)) as im:
            if im.format != "JPEG":
                raise ValueError(f"Not JPEG: {im.format}")
            im.load()
            w,h = im.size
            rgb = im.convert("RGB")
            reduced = ImageOps.contain(rgb,(160,175),Image.Resampling.LANCZOS)
            result.update(width=w,height=h,long_edge=max(w,h),short_edge=min(w,h),
                megapixels=round(w*h/1_000_000,3),aspect_ratio=round(max(w,h)/min(w,h),2),
                bits_per_pixel=round(len(raw)*8/(w*h),2),
                status="ok" if result["sha256_match"] and result["bytes_match"] else "integrity_mismatch")
            flags = []
            if min(w,h) < 600: flags.append("short_edge_under_600")
            elif min(w,h) < 900: flags.append("short_edge_under_900")
            if max(w,h) < 1200: flags.append("long_edge_under_1200")
            if w*h < 1_000_000: flags.append("under_1_megapixel")
            if max(w,h)/min(w,h) > 3.5: flags.append("extreme_aspect_ratio_check_zoom")
            if len(raw)*8/(w*h) < 0.45: flags.append("low_bpp_inspect_compression")
            if not result["sha256_match"]: flags.append("hash_mismatch")
            if not result["bytes_match"]: flags.append("byte_size_mismatch")
            result["flags"] = flags
            return result, reduced
    except Exception as exc:
        result["error"] = str(exc)[:320]
        result["flags"] = ["download_or_decode_failure"]
        return result, None

def save_contacts(rows):
    # Each JPG sheet is 5x5; worksheet includes artwork ID and pixel size.
    paths = []
    for begin in range(0,len(rows),25):
        subset = rows[begin:begin+25]
        sheet = Image.new("RGB",(5*216,5*222),(239,239,239))
        d = ImageDraw.Draw(sheet)
        for j,(rec,thumb) in enumerate(subset):
            x=(j%5)*216; y=(j//5)*222
            d.rectangle((x+2,y+2,x+213,y+218),outline=(160,160,160),width=1)
            if thumb is not None:
                sheet.paste(thumb,(x+108-thumb.width//2,y+5))
            d.text((x+6,y+184),rec["id"],fill=(10,10,10))
            d.text((x+6,y+198),f'{rec.get("width","?")} x {rec.get("height","?")}',fill=(10,10,10))
        name=f"sheet-{begin//25+1:02}.jpg"
        sheet.save(CONTACT/name,quality=83,optimize=True)
        paths.append(name)
    return paths

def main():
    total=len(ARTS)
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
        rows = list(executor.map(inspect,enumerate(ARTS,1)))
    records=[r for r,_ in rows]
    success=[r for r in records if r["status"]=="ok"]
    failures=[r for r in records if r["status"]=="failed"]
    mismatches=[r for r in records if r["status"]=="integrity_mismatch"]
    flags=Counter(flag for r in records for flag in r["flags"])
    widths=sorted(r["short_edge"] for r in success)
    areas=sorted(r["megapixels"] for r in success)
    contact_paths=save_contacts(rows)
    summary={
        "total":total,"ok":len(success),"failed":len(failures),
        "integrity_mismatch":len(mismatches),
        "short_edge_under_600":sum(r["short_edge"]<600 for r in success),
        "short_edge_under_900":sum(r["short_edge"]<900 for r in success),
        "under_1_megapixel":sum(r["megapixels"]<1 for r in success),
        "long_edge_under_1200":sum(r["long_edge"]<1200 for r in success),
        "low_bpp_under_0_45":sum(r["bits_per_pixel"]<0.45 for r in success),
        "extreme_aspect_over_3_5":sum(r["aspect_ratio"]>3.5 for r in success),
        "median_short_edge":widths[len(widths)//2] if widths else None,
        "median_megapixels":areas[len(areas)//2] if areas else None,
        "flags":dict(flags)
    }
    payload={
        "checked_utc":datetime.now(timezone.utc).isoformat(),
        "method":"Live download JPEG + SHA256/byte_length match, Pillow decode + dimensions. No human final image/crop/color review.",
        "summary":summary,"contact_sheets":contact_paths,"records":records
    }
    OUT_JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    flagged=sorted((r for r in records if r["status"]=="ok"),key=lambda r:(r["short_edge"],r["long_edge"]))
    lines=[
        "# 300作品・画像解像度／データ完全性チェック",
        "",f"検査日時（UTC）：{payload['checked_utc']}",
        "",f"- 合格（JPEG読み込み+ハッシュ・容量一致）: **{len(success)}/{total}件**",
        f"- 取得・デコード失敗：**{len(failures)}件** ／ ハッシュ・容量不一致：**{len(mismatches)}件**",
        f"- 短辺600px未満：**{summary['short_edge_under_600']}件**",
        f"- 短辺900px未満：**{summary['short_edge_under_900']}件**",
        f"- 100万画素未満：**{summary['under_1_megapixel']}件**",
        f"- 長辺1200px未満：**{summary['long_edge_under_1200']}件**",
        f"- 短辺中央値：**{summary['median_short_edge']}px**",
        "",
        "## 検査の限界",
        "ファイルの読み込み・解像度・圧縮率は検査可能だが、画像の切り抜き／額縁／色再現／作品同一性は目視承認ではない。",
        "極端に縦長・横長の絵画もあるため、短辺の小ささだけで不合格にはしない。",
        "## 解像度確認の優先候補（短辺の小さい順、最大80件）","",
        "|ID|作品|幅×高さ|容量KB|画素数MP|注意|","|---|---|---:|---:|---:|---|"
    ]
    for r in flagged[:80]:
        lines.append(f'|{r["id"]}|{r["title"].replace("|","/")[:58]}|{r["width"]}×{r["height"]}|{round(r["downloaded_bytes"]/1024)}|{r["megapixels"]}|{", ".join(r["flags"])}|')
    if failures or mismatches:
        lines.extend(["","## 取得失敗・完全性不一致",""])
        for r in failures+mismatches:
            lines.append(f'- {r["id"]} {r["title"]}: {r.get("error",r["status"])}')
    lines.extend(["","詳細は `docs/image-dimensions-audit.json`、全画像の縮小コンタクトシートはCI成果物を確認。",""])
    OUT_MD.write_text("\n".join(lines),encoding="utf-8")
    print("SUMMARY "+json.dumps(summary,ensure_ascii=False),flush=True)
    print("LOWEST_DIM "+json.dumps(flagged[:18],ensure_ascii=False),flush=True)
    print(f"CONTACT SHEETS {len(contact_paths)}",flush=True)

if __name__=="__main__":
    main()
