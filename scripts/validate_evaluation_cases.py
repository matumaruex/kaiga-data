#!/usr/bin/env python3
"""展示選定テストケースの構造検証。選定精度の評価ではない。"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
cases = json.loads((root / "data/evaluation-cases.json").read_text(encoding="utf-8"))
vocab = json.loads((root / "data/emotions.json").read_text(encoding="utf-8"))
allowed = set(vocab["emotions"])
seen = set()
issues = []

for case in cases["cases"]:
    ident = case.get("id")
    if not ident or ident in seen:
        issues.append(f"IDが空または重複: {ident}")
    seen.add(ident)
    for field in ("text", "key_context", "wrong_direction"):
        if not isinstance(case.get(field), str) or not case[field].strip():
            issues.append(f"{ident}: {field}が空")
    targets = case.get("target_emotions", [])
    if not targets or len(targets) != len(set(targets)):
        issues.append(f"{ident}: 感情ターゲットが空または重複")
    for tag in targets:
        if tag not in allowed:
            issues.append(f"{ident}: 感情タグが辞書にない: {tag}")

if len(cases.get("cases", [])) < 10:
    issues.append("テストケースが10件未満")

if issues:
    print("NG:", *issues, sep="\n- ")
    raise SystemExit(1)

print(f"OK: テストケース{len(seen)}件の構造と感情タグを検証（作品選定結果の妥当性は未検証）。")
