#!/usr/bin/env python3
"""Keep the live handoff memo short; archive the previous snapshot on updates.

Example: python3 scripts/rotate_resume.py update --from /tmp/new-status.md
The input is ONLY the "## 現在の状態 ..." section. Existing history links are
retained automatically. This tool never edits artwork or audit records.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TITLE = "# 美術館データの再開地点\n\n"
HISTORY_HEADING = "## 過去の作業履歴"
JOURNAL_TITLE = "# 再開メモの更新履歴\n\n"
MAX_STATUS_CHARS = 3200
MAX_STATUS_LINES = 36
MAX_LIVE_CHARS = 5000


def require(value, message):
    if not value:
        raise ValueError(message)


def normalize_status(status):
    status = status.strip() + "\n"
    require(status.startswith("## 現在の状態"), "新しい状態は「## 現在の状態」で始める")
    require(status.count("\n## ") == 0, "現行メモの状態欄に過去の節を追加しない")
    require(len(status) <= MAX_STATUS_CHARS
            and len(status.splitlines()) <= MAX_STATUS_LINES,
            "現行状態が長すぎる。古い経緯は履歴に保存する")
    require("- " in status and "作品" in status,
            "現在の完成数・次の作業を示すメモが必要")
    return status


def split_resume(content):
    require(content.startswith(TITLE), "再開メモの冒頭形式が不正")
    rest = content[len(TITLE):]
    divider = "\n" + HISTORY_HEADING + "\n"
    require(rest.count(divider) == 1, "再開メモの履歴見出しが一つ必要")
    status, footer = rest.split(divider, 1)
    require(content.count("## 現在の状態") == 1,
            "現行状態の見出しが重複している")
    status = normalize_status(status)
    require(len(content) <= MAX_LIVE_CHARS, "再開メモが長すぎる。古い情報は履歴へ")
    require("history/resume-" in footer,
            "過去の再開履歴へのリンクが必要")
    return status, HISTORY_HEADING + "\n" + footer


def check(root):
    live = root / "docs/resume-artwork-work.md"
    require(live.is_file(), "再開メモがない")
    split_resume(live.read_text(encoding="utf-8"))
    require((root / "docs/history/resume-updates.md").is_file(),
            "更新履歴ファイルがない")
    print("PASS: current handoff stays short; history retained")
    return 0


def update(root, proposed, now=None):
    live = root / "docs/resume-artwork-work.md"
    journal = root / "docs/history/resume-updates.md"
    current_text = live.read_text(encoding="utf-8")
    current, footer = split_resume(current_text)
    new = normalize_status(proposed)
    if new == current:
        print("UNCHANGED: current handoff already matches")
        return False
    require(journal.is_file(), "更新履歴ファイルがない")
    old_journal = journal.read_text(encoding="utf-8")
    require(old_journal.startswith(JOURNAL_TITLE), "更新履歴の形式が不正")
    now = now or datetime.now(timezone.utc)
    stamp = now.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    old_status = current.replace("## 現在の状態", "#### 保存前の状態", 1)
    new_journal = old_journal.rstrip() + f"\n\n---\n\n### {stamp}\n\n" + old_status
    new_live = TITLE + new + "\n" + footer
    split_resume(new_live)  # refuse to write any invalid/overlong active document
    try:
        journal.write_text(new_journal, encoding="utf-8")
        live.write_text(new_live, encoding="utf-8")
    except OSError:
        journal.write_text(old_journal, encoding="utf-8")
        live.write_text(current_text, encoding="utf-8")
        raise
    print("UPDATED: latest state replaced; previous state archived")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    change = commands.add_parser("update")
    change.add_argument("--from", dest="source_file", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "check":
        return check(root)
    return int(not update(root, args.source_file.read_text(encoding="utf-8")) and False)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, UnicodeError) as exc:
        sys.exit("FAIL: " + str(exc))
