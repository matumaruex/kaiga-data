#!/usr/bin/env python3
"""通常チャットで制作する解説の下書き管理。AI呼び出し・自動生成は行わない。"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"pending", "verified", "needs_revision"}
REVIEW_KEYS = {"content_status", "source_status", "rights_status", "reviewed_on"}
VISITOR_KEYS = {"language", "text", "source_urls", "review"}
EVIDENCE_KEYS = {"claim", "source_url", "source_location", "checked_against_source"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def records(root):
    result = load(root / "data/artworks.json")["artworks"]
    if len(set(x["id"] for x in result)) != len(result):
        raise ValueError("作品DBのIDが重複しています")
    return result


def drafts(root):
    return sorted((root / "drafts/visitor-explanations").glob("*.json"))


def valid_url(url):
    if not isinstance(url, str):
        return False
    p = urlparse(url)
    return p.scheme == "https" and bool(p.netloc) and not p.username


def check_file(path, by_id):
    problems = []
    try:
        data = load(path)
    except (OSError, ValueError, UnicodeError) as exc:
        return [f"{path.name}: JSON読込エラー: {exc}"]
    if not isinstance(data, dict) or set(data) != {"id", "visitor_explanation", "evidence"}:
        return [f"{path.name}: id, visitor_explanation, evidence の3項目が必要"]
    ident = data["id"]
    if not isinstance(ident, str) or not re.fullmatch(r"(?:aic|met)-[0-9]+", ident):
        return [f"{path.name}: 不正なID"]
    if path.name != ident + ".json":
        problems.append(f"{ident}: ファイル名とIDが不一致")
    if ident not in by_id:
        problems.append(f"{ident}: DBに未登録")
    visitor = data["visitor_explanation"]
    if not isinstance(visitor, dict) or set(visitor) != VISITOR_KEYS:
        return problems + [f"{ident}: 解説構造が不正"]
    if ident in by_id and "visitor_explanation" in by_id[ident]:
        if by_id[ident]["visitor_explanation"] != visitor:
            problems.append(f"{ident}: 既存解説の上書きを禁止")
    if visitor["language"] != "ja" or not isinstance(visitor["text"], str) or not visitor["text"].strip():
        problems.append(f"{ident}: 日本語本文が空または不正")
    urls = visitor["source_urls"]
    if not isinstance(urls, list) or not urls or any(not valid_url(u) for u in urls) or len(urls) != len(set(urls)):
        problems.append(f"{ident}: 出典URLの欠落・重複・形式不正")
        urls = []
    rev = visitor["review"]
    if not isinstance(rev, dict) or set(rev) != REVIEW_KEYS:
        problems.append(f"{ident}: レビュー欄が不正")
    else:
        if any(rev[x] not in STATUSES for x in ("content_status", "source_status", "rights_status")):
            problems.append(f"{ident}: ステータスが不正")
        if not isinstance(rev["reviewed_on"], str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", rev["reviewed_on"]):
            problems.append(f"{ident}: レビュー日が不正")
        if rev["content_status"] == "verified" and rev["source_status"] != "verified":
            problems.append(f"{ident}: 原資料未確認なのに本文をverifiedにできない")
    evidence = data["evidence"]
    if not isinstance(evidence, list) or not evidence:
        problems.append(f"{ident}: 出典の該当箇所を示す根拠メモが必要")
        evidence = []
    for i, e in enumerate(evidence, 1):
        if not isinstance(e, dict) or set(e) != EVIDENCE_KEYS:
            problems.append(f"{ident}: 根拠{i}の構造が不正")
            continue
        if any(not isinstance(e[k], str) or not e[k].strip() for k in ("claim", "source_location")):
            problems.append(f"{ident}: 根拠{i}の主張または出典該当箇所が空")
        if not valid_url(e["source_url"]) or e["source_url"] not in urls:
            problems.append(f"{ident}: 根拠{i}のURLと出典一覧が不一致")
        if type(e["checked_against_source"]) is not bool:
            problems.append(f"{ident}: 根拠{i}の照合フラグが不正")
    if isinstance(rev, dict) and rev.get("source_status") == "verified":
        if not evidence or any(not isinstance(e, dict) or e.get("checked_against_source") is not True for e in evidence):
            problems.append(f"{ident}: 原資料未照合のままverifiedにできない")
    return problems


def validate(root, selected=None):
    by_id = {r["id"]: r for r in records(root)}
    paths = [p for p in drafts(root) if selected is None or p.stem in selected]
    errors = []
    for p in paths:
        errors.extend(check_file(p, by_id))
    if selected is not None:
        errors.extend(f"{ident}: 下書きがありません" for ident in sorted(selected - {p.stem for p in paths}))
    return errors, len(paths)


def status(root):
    all_records = records(root)
    done = {r["id"] for r in all_records if "visitor_explanation" in r}
    staged = {p.stem for p in drafts(root)}
    errors, _ = validate(root)
    print(f"登録済み: {len(done)}/{len(all_records)}件")
    print(f"下書き済み（未登録）: {len(staged - done)}件")
    print(f"未着手: {len({r['id'] for r in all_records} - done - staged)}件")
    print(f"下書き形式: {'要修正' if errors else 'OK（史実の正確性は未保証）'}")
    for error in errors:
        print("- " + error)
    return bool(errors)


def next_batch(root, count):
    staged = {p.stem for p in drafts(root)}
    available = [r for r in records(root) if "visitor_explanation" not in r and r["id"] not in staged]
    groups = {"aic": [], "met": []}
    for r in sorted(available, key=lambda r: (str(r.get("facts", {}).get("artist", "")).casefold(), r["id"])):
        groups.setdefault(r["id"].split("-")[0], []).append(r)
    selected, used_artists = [], set()
    while len(selected) < count and any(groups.values()):
        for museum, group in groups.items():
            if len(selected) >= count or not group:
                continue
            index = next((i for i, r in enumerate(group) if r.get("facts", {}).get("artist") not in used_artists), 0)
            r = group.pop(index)
            selected.append(r)
            used_artists.add(r.get("facts", {}).get("artist"))
    print(f"次の未作成候補: {len(selected)}件（制作前に資料・主題のバランスを再確認）")
    for r in selected:
        fact = r.get("facts", {})
        interpretation = r.get("curation", {}).get("meaning_basis", {}).get("scholarly_interpretation", {})
        print(f"- {r['id']}｜{fact.get('artist','?')}｜{fact.get('title_original','?')}｜{fact.get('creation_date_display','?')}")
        if valid_url(interpretation.get("source_url")):
            print(f"  参考URL候補（内容未照合）: {interpretation['source_url']}")
    return 0


def explanation_sha256(visitor):
    """本文・出典・レビュー状態を含む、承認対象の版を識別する。"""
    canonical = json.dumps(visitor, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_approvals(root):
    """個別承認済みの作品IDと、その承認時点の解説のSHA-256を取得する。"""
    path = root / "data/visitor-explanation-approvals.json"
    if not path.is_file():
        raise ValueError("個別承認台帳がありません（data/visitor-explanation-approvals.json）")
    data = load(path)
    if not isinstance(data, dict) or set(data) != {"approvals"} or not isinstance(data["approvals"], list):
        raise ValueError("個別承認台帳の形式が不正です")
    approved = {}
    for item in data["approvals"]:
        if not isinstance(item, dict) or set(item) != {"id", "visitor_sha256"}:
            raise ValueError("個別承認台帳の項目形式が不正です")
        ident, digest = item["id"], item["visitor_sha256"]
        if not isinstance(ident, str) or not re.fullmatch(r"(?:aic|met)-[0-9]+", ident):
            raise ValueError("個別承認台帳の作品IDが不正です")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{ident}: 個別承認のSHA-256が不正です")
        if ident in approved:
            raise ValueError(f"{ident}: 個別承認台帳で作品IDが重複しています")
        approved[ident] = digest
    return approved


def fingerprint(root, selected):
    """ユーザーが確認した下書きの版を承認台帳に記録するための照合用出力。"""
    errors, _ = validate(root, selected)
    if errors:
        raise ValueError("下書き検査不合格: " + "; ".join(errors))
    for ident in sorted(selected):
        visitor = load(root / "drafts/visitor-explanations" / (ident + ".json"))["visitor_explanation"]
        review = visitor["review"]
        print(
            f"{ident} {explanation_sha256(visitor)} "
            f"content={review['content_status']} source={review['source_status']} "
            f"rights={review['rights_status']}"
        )
    return 0


def promote(root, selected, approved):
    if not approved or not selected:
        raise ValueError("承認後にのみ、--idsと--approvedの両方を指定")
    errors, count = validate(root, selected)
    if errors:
        raise ValueError("下書き検査不合格: " + "; ".join(errors))
    approvals = load_approvals(root)
    for ident in sorted(selected):
        visitor = load(root / "drafts/visitor-explanations" / (ident + ".json"))["visitor_explanation"]
        review = visitor["review"]
        if review["content_status"] != "verified" or review["source_status"] != "verified":
            raise ValueError(f"{ident}: 本文と出典の両方がverifiedでなければ登録できません")
        if review["rights_status"] == "needs_revision":
            raise ValueError(f"{ident}: 権利に要修正事項があります")
        if ident not in approvals:
            raise ValueError(f"{ident}: ユーザーの個別承認が台帳にありません")
        if approvals[ident] != explanation_sha256(visitor):
            raise ValueError(f"{ident}: 承認後に本文・出典・レビュー状態が変わっています。再承認が必要")

    target = root / "data/artworks.json"
    data = load(target)
    original = copy.deepcopy(data)
    index = {r["id"]: r for r in data["artworks"]}
    for ident in sorted(selected):
        if "visitor_explanation" in index[ident]:
            raise ValueError(f"{ident}: 本番DBに既に解説があります")
        index[ident]["visitor_explanation"] = load(root / "drafts/visitor-explanations" / (ident + ".json"))["visitor_explanation"]
    for old, new in zip(original["artworks"], data["artworks"]):
        clone = copy.deepcopy(new)
        if old["id"] in selected:
            clone.pop("visitor_explanation")
        if old != clone:
            raise ValueError(f"{old['id']}: 解説以外の欄に差分")
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{count}件をローカルDBに反映。Git差分と既存検証器の成功を確認し、承認済み変更のみマージ。")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("status")
    nxt = commands.add_parser("next")
    nxt.add_argument("--size", type=int, default=5)
    commands.add_parser("check")
    fp = commands.add_parser("fingerprint")
    fp.add_argument("--ids", nargs="+", required=True)
    pub = commands.add_parser("promote")
    pub.add_argument("--ids", nargs="+", required=True)
    pub.add_argument("--approved", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == "status":
            return int(status(root))
        if args.action == "next":
            if not 1 <= args.size <= 20:
                parser.error("--size は1～20で指定してください")
            return next_batch(root, args.size)
        if args.action == "check":
            errors, number = validate(root)
            print(f"下書き{number}件の形式検査: {'OK' if not errors else 'NG'}（内容真偽の保証ではありません）")
            for e in errors:
                print("- " + e)
            return int(bool(errors))
        if args.action == "fingerprint":
            return fingerprint(root, set(args.ids))
        return promote(root, set(args.ids), args.approved)
    except (KeyError, ValueError, OSError, TypeError) as exc:
        parser.exit(1, f"エラー: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
