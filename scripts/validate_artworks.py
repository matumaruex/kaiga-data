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
    # AIによる再選定と通常のタグ検索が同じ元データを使えるか
    profile = art["curation"].get("search_profile")
    if not isinstance(profile, dict):
        errors.append(f"{ident}: 検索プロフィールがない")
    else:
        if not isinstance(profile.get("summary_for_ai"), str) or not profile["summary_for_ai"].strip():
            errors.append(f"{ident}: AI向け説明が空")
        situations = profile.get("fitting_situations", [])
        if not isinstance(situations, list) or not situations:
            errors.append(f"{ident}: 適合する状況の説明がない")
        else:
            for situation in situations:
                if not isinstance(situation, dict) or any(
                    not isinstance(situation.get(field), str) or not situation[field].strip()
                    for field in ("situation", "reason")
                ) or type(situation.get("strength")) is not int or situation["strength"] not in (1, 2, 3):
                    errors.append(f"{ident}: 状況と理由または強度が不正")
        cautions = profile.get("selection_cautions", [])
        if not isinstance(cautions, list) or not cautions or any(not isinstance(c, str) or not c.strip() for c in cautions):
            errors.append(f"{ident}: 選定上の注意点が空")
        if profile.get("review_status") not in ("draft_not_human_approved", "draft_source_unverified", "human_approved"):
            errors.append(f"{ident}: 検索プロフィールのレビュー状態が不正")
    # 各タグに必ず1〜3の強度を持たせ、作品選定で弱い印象を同列に扱わない
    weight = art["curation"].get("emotion_strengths", {})
    if set(weight) != set(art["curation"]["emotions"]):
        errors.append(f"{ident}: 感情タグと強度が不一致")
    for tag, score in weight.items():
        if type(score) is not int or score not in (1, 2, 3):
            errors.append(f"{ident}: {tag}に不正な強度")
    if not art["curation"].get("evidence_url", "").startswith("https://"):
        errors.append(f"{ident}: 参照資料URLがない")
    if art["review"].get("curatorial_review_status") not in ("provisional", "approved", "needs_revision"):
        errors.append(f"{ident}: キュレーション状態が不正")
    if art["review"].get("interpretation_human_approved") is True and art["review"].get("curatorial_review_status") != "approved":
        errors.append(f"{ident}: 未承認なのに承認済み")
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
