#!/usr/bin/env python3
"""未検証候補と展示データの整合性を検証。ネットワーク検証はしない。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
current = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))
candidates = json.loads((ROOT / "data/candidates-batch-002.json").read_text(encoding="utf-8"))
vocabulary = json.loads((ROOT / "data/emotions.json").read_text(encoding="utf-8"))
issues = []
live_ids = {x["id"] for x in current["artworks"]}
ids = set()
for art in candidates["works"]:
    ident = art["id"]
    if ident in ids:
        issues.append(f"{ident}: 候補内の重複")
    ids.add(ident)
    if ident in live_ids:
        issues.append(f"{ident}: 本登録にも重複")
    if ident != f'aic-{art["source"]["artwork_id"]}':
        issues.append(f"{ident}: 作品IDが不一致")
    if art["status"] != "candidate_unverified":
        issues.append(f"{ident}: 未検証候補なのに状態が違う")
    v = art["verification"]
    if any(v[k] for k in ("api_metadata_checked", "is_public_domain_confirmed", "image_id_confirmed", "image_live_checked", "curation_human_approved")):
        issues.append(f"{ident}: 未確認項目が確認済みと記録されている")
    if not art["facts_from_museum_sample"].get("title") or not art["facts_from_museum_sample"].get("artist"):
        issues.append(f"{ident}: 作品名・画家名が空")
    c = art["curation"]
    for tag, weight in c["emotion_strengths"].items():
        if tag not in vocabulary["emotions"] or type(weight) is not int or weight not in (1, 2, 3):
            issues.append(f"{ident}: 感情タグまたは重みが不正 {tag}")
    for group in ("tones", "themes"):
        if any(tag not in vocabulary[group] for tag in c[group]):
            issues.append(f"{ident}: {group}に未登録のタグ")
    if not c["interpretation"] or not c["alternate_reading"] or not c["review_concern"]:
        issues.append(f"{ident}: 解釈・別解・注意点が不足")

if issues:
    print("NG:", *issues, sep="\n - ")
    raise SystemExit(1)
print(f"OK：本登録{len(live_ids)}件、候補{len(ids)}件。重複なし、タグ・必須情報・未検証状態の形式チェック完了。")
print("※作品の現物、権利、画像、解釈の正しさはこの形式チェックでは確認できません。")
