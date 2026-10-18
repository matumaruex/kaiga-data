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
    # 候補は作成時の履歴（スナップショット）。昇格後も記録を残すため、本登録との重複は正常。
    # 現在の登録状況は data/artworks.json を正とする。
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
    snapshots = art.get("archived_api_metadata")
    if snapshots is not None:
        rows = snapshots.get("archive_sources", [])
        if len(rows) != 2 or len(set(r["source"] for r in rows)) != 2:
            issues.append(f"{ident}: 過去APIスナップショットの数/出典に異常")
        images = {r["image_id"] for r in rows}
        consistent = len(images) == 1
        if snapshots.get("image_id_consistent_between_archives") != consistent:
            issues.append(f"{ident}: 画像ID一致フラグに矛盾")
        expected_id = next(iter(images)) if consistent else None
        if snapshots.get("image_id_candidate") != expected_id:
            issues.append(f"{ident}: 画像ID候補の不整合")
        if bool(snapshots.get("image_url_candidate")) != consistent:
            issues.append(f"{ident}: 画像URL候補の有無が矛盾")
        if consistent and expected_id not in snapshots.get("image_url_candidate", ""):
            issues.append(f"{ident}: 画像URLとIDが不一致")
        if not all(r.get("is_public_domain") is True and r.get("artwork_type_title") == "Painting" for r in rows):
            issues.append(f"{ident}: 過去複製にPD/作品分類の不一致")
        if v.get("has_conflicting_historical_image_ids") != (not consistent):
            issues.append(f"{ident}: 画像ID衝突フラグが矛盾")
        if v.get("api_metadata_checked") or v.get("is_public_domain_confirmed") or v.get("image_id_confirmed"):
            issues.append(f"{ident}: 過去の複製のみで公式現在データ確認済みにしている")

if issues:
    print("NG:", *issues, sep="\n - ")
    raise SystemExit(1)
print(f"OK：本登録{len(live_ids)}件、候補履歴{len(ids)}件（すでに本登録された候補{len(ids & live_ids)}件）。候補内の重複なし、タグ・必須情報を検証。")
print("※作品の現物、権利、画像、解釈の正しさはこの形式チェックでは確認できません。")
