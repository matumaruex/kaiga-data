#!/usr/bin/env python3
"""作品データの形式・参照関係を検証（外部URLの実疎通確認は行わない）。"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))
vocab = json.loads((ROOT / "data/emotions.json").read_text(encoding="utf-8"))
image_registry = json.loads((ROOT / "data/image-sources.json").read_text(encoding="utf-8"))
KNOWN_ARTIST_NAMES = {
    "Auguste Renoir": "Pierre-Auguste Renoir",
    "Pierre-Auguste Renoir": "Pierre-Auguste Renoir",
    "Edouard Manet": "Édouard Manet",
    "Édouard Manet": "Édouard Manet",
    "Paul Cezanne": "Paul Cézanne",
    "Paul Cézanne": "Paul Cézanne",
    "Rembrandt (Rembrandt van Rijn)": "Rembrandt van Rijn",
    "Rembrandt van Rijn": "Rembrandt van Rijn",
    "Domenico Theotokópoulos, called El Greco": "El Greco",
    "El Greco": "El Greco",
}
errors = []
seen = set()
duplicated_meaning_ids = []

if data.get("schema_version") != vocab.get("schema_version"):
    errors.append("スキーマのバージョンが不一致")

# Met's artistDisplayName can be simplified; their human-readable artwork
# pages explicitly qualify these two attributions. Keep the uncertainty.
OFFICIAL_ATTRIBUTION_GUARDS = {
    "met-437412": "Style of Rembrandt (Rembrandt van Rijn)",
    "met-57280": "School of Katsushika Hokusai",
}

for art in data.get("artworks", []):
    ident = art["id"]
    if ident in seen:
        errors.append(f"{ident}: 重複ID")
    seen.add(ident)
    if art["source"]["artwork_id"] != int(ident.split("-")[-1]):
        errors.append(f"{ident}: ID不一致")
    # Original attribution remains untouched; aliases are display/selection metadata only.
    author_name = art["facts"].get("artist")
    author_canonical = art["facts"].get("artist_canonical")
    expected = KNOWN_ARTIST_NAMES.get(author_name)
    if expected and author_canonical != expected:
        errors.append(f"{ident}: 作者名の正規形が未設定または不一致")
    if author_canonical is not None and (
        not isinstance(author_canonical, str) or not author_canonical.strip()
    ):
        errors.append(f"{ident}: 作者名の正規形が空または不正")
    if author_name == "Unidentified artist" and author_canonical:
        errors.append(f"{ident}: 作者不詳を特定の同一人物として登録しない")
    if ident in OFFICIAL_ATTRIBUTION_GUARDS:
        if art["facts"].get("artist") != OFFICIAL_ATTRIBUTION_GUARDS[ident]:
            errors.append(f"{ident}: Met公式作品ページの不確実性を含む帰属表記と異なる")
        if art["facts"].get("artist_canonical"):
            errors.append(f"{ident}: School/Style作品を本人の確定作として統合している")
    if art["facts"]["type"] != "Painting":
        errors.append(f"{ident}: 絵画ではない")
    if art["facts"]["is_public_domain_at_source"] is not True:
        errors.append(f"{ident}: 公開条件未確認")
    image = art["image"]
    if ident.startswith("aic-"):
        if not re.fullmatch(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}", image["image_id"]):
            errors.append(f"{ident}: シカゴの画像UUIDが不正")
    elif ident.startswith("met-"):
        if art["source"].get("museum") != "Metropolitan Museum of Art":
            errors.append(f"{ident}: Met所蔵館名の不一致")
        if image.get("image_id") != f"met-{art['source']['artwork_id']}-primary":
            errors.append(f"{ident}: Met primary image identity mismatch")
    else:
        errors.append(f"{ident}: 未対応の美術館ID")
    image_source = next((x for x in image_registry["records"] if x["id"] == ident), None)
    if image_source is None:
        errors.append(f"{ident}: 画像出典台帳に作品がない")
    elif image.get("display_url", "").startswith("https://www.artic.edu/iiif/"):
        if image["image_id"] not in image["display_url"]:
            errors.append(f"{ident}: 公式画像URLとIDが不一致")
    else:
        if not image.get("display_url", "").startswith("https://"):
            errors.append(f"{ident}: 表示画像のURLが不正")
        expected_path = f"/artworks/{ident[4:]}.jpg" if ident.startswith("aic-") else f"/artworks/{ident}.jpg"
        if image.get("source_registry_id") != ident or image.get("local_path") != expected_path:
            errors.append(f"{ident}: 別ソース画像の参照が不正")
        if image_source and image.get("sha256") != image_source["image_source"].get("sha256"):
            errors.append(f"{ident}: 画像のSHA256が画像台帳と一致しない")
        if image_source and image.get("display_url") not in (
            image_source["image_source"].get("verified_download_url"),
            image_source["image_source"].get("download_url")
        ):
            errors.append(f"{ident}: 表示画像URLが画像台帳と不一致")
    # 制作意図と学術解釈、感情タグを混同しないための契約。
    meaning = art["curation"].get("meaning_basis")
    groups = art["curation"].get("emotion_categories")
    if not isinstance(meaning, dict) or not isinstance(groups, dict):
        errors.append(f"{ident}: 制作意図・根拠・主補助タグの分類がない")
    else:
        author = meaning.get("author_intent", {})
        if not isinstance(author, dict):
            errors.append(f"{ident}: 作者の意思の状態が不正")
        elif author.get("status") == "not_verified_for_this_work":
            if author.get("summary") is not None or author.get("source_url") is not None:
                errors.append(f"{ident}: 作者の意図が未確認なのに資料や本文を断定")
        elif author.get("status") in ("related_motif_or_series", "related_artistic_program", "direct_for_this_work"):
            if not isinstance(author.get("summary"), str) or not author["summary"].strip() or not str(author.get("source_url") or "").startswith("https://"):
                errors.append(f"{ident}: 関連題材への本人証言に出典がない")
        else:
            errors.append(f"{ident}: 本人記録の分類が不正")
        scholarly = meaning.get("scholarly_interpretation", {})
        if not isinstance(scholarly, dict) or not isinstance(scholarly.get("summary"), str) or not scholarly["summary"].strip() or not str(scholarly.get("source_url") or "").startswith("https://"):
            errors.append(f"{ident}: 専門家の解釈・根拠の記載がない")
        for label in ("creation_context", "visual_clues", "uncertainty_note"):
            if not isinstance(meaning.get(label), str) or not meaning[label].strip():
                errors.append(f"{ident}: {label}が空")
        # 同文は形式上の自動不合格にせず、品質再調査の対象として記録。
        if (
            isinstance(scholarly, dict)
            and isinstance(scholarly.get("summary"), str)
            and isinstance(meaning.get("creation_context"), str)
            and scholarly["summary"].strip() == meaning["creation_context"].strip()
        ):
            duplicated_meaning_ids.append(ident)
            if art["review"].get("ai_content_review_status") != "needs_revision":
                errors.append(f"{ident}: 同文を要修正として記録していない")
        primary = groups.get("primary")
        secondary = groups.get("secondary")
        if not isinstance(primary, list) or len(primary) > 2 or not isinstance(secondary, list) or len(secondary) > 2:
            errors.append(f"{ident}: 主0〜2・補助0〜2の制限違反")
        else:
            tags = primary + secondary
            if len(tags) != len(set(tags)) or set(tags) != set(art["curation"].get("emotions", [])):
                errors.append(f"{ident}: 主補助タグと旧検索索引が不一致")
            weights = art["curation"].get("emotion_strengths", {})
            for tag in primary:
                if type(weights.get(tag)) is not int or weights[tag] not in (2, 3):
                    errors.append(f"{ident}: 主タグ {tag} に根拠強度2〜3がない")
            for tag in secondary:
                if weights.get(tag) != 1:
                    errors.append(f"{ident}: 補助タグ {tag} は強度1とする")
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
        if "summary_for_ai" in profile:
            errors.append(f"{ident}: 廃止したsummary_for_aiが残っている")
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
        if profile.get("review_status") not in (
            "evidence_review_pending", "evidence_reviewed", "evidence_review_needs_revision"
        ):
            errors.append(f"{ident}: 検索プロフィールの資料レビュー状態が不正")
    for obsolete in ("interpretation", "alternate_reading", "source_context_note"):
        if obsolete in art["curation"]:
            errors.append(f"{ident}: 廃止した項目 {obsolete} が残っている")
    # 各タグに必ず1〜3の強度を持たせ、作品選定で弱い印象を同列に扱わない
    weight = art["curation"].get("emotion_strengths", {})
    if set(weight) != set(art["curation"]["emotions"]):
        errors.append(f"{ident}: 感情タグと強度が不一致")
    for tag, score in weight.items():
        if type(score) is not int or score not in (1, 2, 3):
            errors.append(f"{ident}: {tag}に不正な強度")
    if not art["curation"].get("evidence_url", "").startswith("https://"):
        errors.append(f"{ident}: 参照資料URLがない")
    review = art["review"]
    if review.get("curatorial_review_status") not in ("provisional", "approved", "needs_revision"):
        errors.append(f"{ident}: キュレーション状態が不正")
    if "interpretation_human_approved" in review:
        errors.append(f"{ident}: 廃止した人間承認フラグが残っている")
    for field in (
        "ai_content_review_status",
        "source_evidence_review_status",
        "image_subject_match_status",
    ):
        if review.get(field) not in ("pending", "verified", "needs_revision"):
            errors.append(f"{ident}: {field} の検証状態が不正")
    # approved は証拠と内容の確認済みを意味する（人間の承認ではない）。
    if review.get("curatorial_review_status") == "approved" and any(
        review.get(field) != "verified"
        for field in (
            "ai_content_review_status",
            "source_evidence_review_status",
            "image_subject_match_status",
        )
    ):
        errors.append(f"{ident}: 証拠検証待ちの作品を公開承認済みにしている")
    for section, keys in (
        ("facts", ("title_original", "artist", "creation_date_display")),
    ):
        if any(not art[section].get(key) for key in keys):
            errors.append(f"{ident}: {section}に必須項目の欠損")

if errors:
    print("NG:", *errors, sep="\n- ")
    raise SystemExit(1)
print(f"OK: {len(seen)}件。ID・形式・タグ・資料検証状態・必須項目を検証。")
print(f"要精査: 専門家の解釈と制作背景が同文 {len(duplicated_meaning_ids)}件。")
print("注記: 形式検証は原資料の正しさ、実画像との一致、解釈の妥当性を保証しない。")
