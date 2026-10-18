#!/usr/bin/env python3
"""公式APIで作品分類・画像・PDを確認し、条件を満たす候補だけを本登録へ昇格。
初期状態は dry-run。--write の時のみ data/artworks.json を更新する。
第三者の追加ライセンスがある作品、通信不良作品を推測で登録しない。
"""
import argparse
import datetime
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.artic.edu/api/v1/artworks/"
IIIF = "https://www.artic.edu/iiif/2"
FIELDS = "id,title,artist_title,artist_display,date_display,is_public_domain,image_id,artwork_type_title"
IMAGE_RE = re.compile(r"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$")

def fetch_artwork(art_id):
    url = API + str(art_id) + "?" + urllib.parse.urlencode({"fields": FIELDS})
    request = urllib.request.Request(url, headers={"User-Agent": "KaigaData-Curation/0.1 (+open access research; respectful small batch)", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=18) as response:
        return json.load(response)["data"]

def verify(candidate, official):
    src = candidate["source"]
    if official.get("id") != src["artwork_id"]:
        return "ID不一致"
    if official.get("title", "").strip() != candidate["facts_from_museum_sample"]["title"].strip():
        return "公式CSVと現在の作品名が一致しない（手動確認）"
    artist = candidate["facts_from_museum_sample"]["artist"]
    if official.get("artist_title") != artist and artist not in (official.get("artist_display") or ""):
        return "公式CSVと現在の作者名が一致しない（手動確認）"
    if (official.get("artwork_type_title") or "").lower() != "painting":
        return "公式分類がPaintingではない"
    if official.get("is_public_domain") is not True:
        return "パブリックドメインと確認できない"
    if not IMAGE_RE.fullmatch(official.get("image_id") or ""):
        return "有効な画像IDがない"
    if not official.get("date_display"):
        return "制作年代情報なし"
    return None

def promote(candidate, official):
    src = candidate["source"]
    c = candidate["curation"]
    image_id = official["image_id"]
    today = datetime.date.today().isoformat()
    return {
        "id": candidate["id"],
        "source": {
            "museum": src["museum"],
            "artwork_id": src["artwork_id"],
            "artwork_url": src["official_artwork_url"],
            "api_url": src["api_url"],
            "record_checked_on": today,
        },
        "facts": {
            "title_original": official["title"],
            "title_ja_provisional": candidate["title_ja_provisional"],
            "artist": candidate["facts_from_museum_sample"]["artist"],
            "creation_date_display": official["date_display"],
            "type": "Painting",
            "is_public_domain_at_source": True,
        },
        "image": {
            "image_id": image_id, "iiif_base": IIIF,
            "display_url": f"{IIIF}/{image_id}/full/843,/0/default.jpg",
            "live_image_checked": False,
        },
        "curation": {
            "emotions": list(c["emotion_strengths"]),
            "emotion_strengths": c["emotion_strengths"],
            "tones": c["tones"], "themes": c["themes"],
            "interpretation": c["interpretation"],
            "alternate_reading": c["alternate_reading"],
            "source_context_note": "解釈は仮説。作品の史実・背景は参照ページと個別照合が必要。",
            "evidence_url": src["supplemental_museum_source_url"] or src["official_artwork_url"],
        },
        "review": {
            "facts_checked_against_museum_api": True,
            "source_public_domain_flag_checked": True,
            "visual_checked": False,
            "interpretation_human_approved": False,
            "curatorial_reviewed_on": today,
            "curatorial_review_status": "provisional",
            "curatorial_review_note": "自動で基本メタデータのみ照合。画像HTTP・実視認・解釈は未承認。注意: " + c["review_concern"],
        },
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="API検証に合格した候補だけ本登録ファイルに追記")
    args = parser.parse_args()
    data_path = ROOT / "data/artworks.json"
    candidates = json.loads((ROOT / "data/candidates-batch-002.json").read_text(encoding="utf-8"))["works"]
    data = json.loads(data_path.read_text(encoding="utf-8"))
    existing = {x["id"] for x in data["artworks"]}
    promoted = []
    for candidate in candidates:
        if candidate["id"] in existing:
            print("SKIP: 登録済み", candidate["id"])
            continue
        try:
            official = fetch_artwork(candidate["source"]["artwork_id"])
            problem = verify(candidate, official)
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
            problem = f"取得失敗: {type(exc).__name__}"
        if problem:
            print("PENDING:", candidate["id"], problem)
        else:
            record = promote(candidate, official)
            promoted.append(record)
            print("OK:", candidate["id"], record["facts"]["title_original"])
        time.sleep(0.25)
    print(f"確認結果: 合格{len(promoted)}件、未合格{len(candidates)-len(promoted)}件")
    if not args.write:
        print("dry-run: GitHubへ保存する前の確認のみ。--write でローカルのJSONを更新。")
        return
    if not promoted:
        print("合格作品なし。変更しません。")
        return
    data["artworks"].extend(promoted)
    # 本登録ファイルのみを変更し、候補ファイルは監査可能な履歴として残す。
    # コミットやデプロイは勝手にしない。
    updated = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    temp = data_path.with_suffix(".tmp")
    temp.write_text(updated, encoding="utf-8")
    temp.replace(data_path)
    print(f"data/artworks.json に{len(promoted)}件追記。差分・解釈・画像の人間確認後にコミットしてください。")

if __name__ == "__main__":
    main()
