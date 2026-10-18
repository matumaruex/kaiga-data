#!/usr/bin/env python3
"""タグの分布を確認する診断ツール。感情に合う作品を選べることは保証しない。"""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
accepted = json.loads((root / "data/artworks.json").read_text(encoding="utf-8"))["artworks"]
pending = json.loads((root / "data/candidates-batch-002.json").read_text(encoding="utf-8"))["works"]
vocab = json.loads((root / "data/emotions.json").read_text(encoding="utf-8"))["emotions"]
accepted_ids = {art["id"] for art in accepted}

def scores(record):
    return record["curation"].get("emotion_strengths", {})

def count(records, minimum):
    c = Counter()
    for item in records:
        for tag, strength in scores(item).items():
            if isinstance(strength, int) and strength >= minimum:
                c[tag] += 1
    return c

pending = [item for item in pending if item["id"] not in accepted_ids]
for label, records in [("本登録（画像未視認の作品を含む）", accepted),
                       ("確認待ち候補（展示禁止）", pending)]:
    medium = count(records, 2)
    strong = count(records, 3)
    print(f"\n{label}: {len(records)}作品")
    for tag in vocab:
        print(f"  {tag:8}  中以上={medium[tag]:2d}  強={strong[tag]:2d}")
    lacking = [tag for tag in vocab if medium[tag] < 2]
    if lacking:
        print("注意：この集合だけでは候補の少ない感情: " + " / ".join(lacking))

print("\n※この出力はタグの偏りを測るだけ。複合感情、作品画像、鑑賞者の評価は判断できません。")
