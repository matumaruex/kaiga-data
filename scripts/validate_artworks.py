#!/usr/bin/env python3
"""作品データの形式・参照関係を検証（外部URLの実疎通確認は行わない）。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))
vocab = json.loads((ROOT / "data/emotions.json").read_text(encoding="utf-8"))
errors = []
seen = set()

if data.get("schema_version") != vocab.get("schema_version"):
    errors.append("スキーマのバージョンが不一致")

for art in data.get("artworks", []):
    ident = art["id"]
    if ident in seen:
        errors.append(f"{ident}: 重複ID")
    seen.add(ident)
    if art["source"]["artwork_id"] != int(ident.split("-")[-1]):
        errors.append(f"{ident}: ID不一致")
    if art["facts"]["type"] != "Painting":
        errors.append(f"{ident}: 絵画ではない")
    if art["facts"]["is_public_domain_at_source"] is not True:
        errors.append(f"{ident}: 公開条件未確認")
    image = art["image"]
    if not re.fullmatch(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}", image["image_id"]):
        errors.append(f"{ident}: 画像IDの形式が不正")
    if image["image_id"] not in image["display_url"]:
        errors.append(f"{ident}: 画像URLとIDが不一致")
    for category in ("emotions", "tones", "themes"):
        values = art["curation"][category]
        if len(values) != len(set(values)):
            errors.append(f"{ident}: {category}のタグ重複")
        for tag in values:
            if tag not in vocab[category]:
                errors.append(f"{ident}: 未登録タグ {category}/{tag}")
    for section, keys in (
        ("facts", ("title_original", "artist", "creation_date_display")),
        ("curation", ("interpretation", "alternate_reading", "source_context_note")),
    ):
        if any(not art[section].get(key) for key in keys):
            errors.append(f"{ident}: {section}に必須項目の欠損")

if errors:
    print("NG:", *errors, sep="\n- ")
    raise SystemExit(1)
print(f"OK: {len(seen)}件。ID・形式・タグ・必須項目を検証。画像URLの実通信、感情解釈の妥当性は未検証。")
