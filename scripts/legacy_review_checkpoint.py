#!/usr/bin/env python3
"""Read-only v1 -> v2 evidence checkpoint for the ongoing 100 visitor drafts.

Use against a checkout containing draft PR #3's saved files:
  python3 scripts/legacy_review_checkpoint.py
  python3 scripts/legacy_review_checkpoint.py --write /tmp/checkpoint.json
  python3 scripts/legacy_review_checkpoint.py --verify /tmp/checkpoint.json

No statuses are promoted and no original file is modified. In particular, a
preliminary rights screen is NOT a finished rights review, and a past audit of
a different draft hash is historical evidence, NOT approval of the current text.
"""
import argparse
import hashlib
import json
import subprocess
from difflib import SequenceMatcher
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("docs/visitor-content-audit-2026-10-27")
TRIAGE = {"priority_rewrite_or_review", "further_review_required"}
AUDIT = {"no_text_issue_found", "needs_revision", "needs_more_evidence"}
FOLLOWUP_RESULTS = {"checked_for_similarity", "needs_revision", "needs_more_evidence"}


def load(path):
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def unique_index(items, name, allowed_ids=None):
    result = {}
    for item in items:
        ident = item["id"]
        if ident in result:
            raise ValueError(f"{name}: duplicate id {ident}")
        if allowed_ids is not None and ident not in allowed_ids:
            raise ValueError(f"{name}: unexpected id {ident}")
        result[ident] = item
    return result


def read_groups(root, pattern, allowed, expected_batches):
    group = {}
    for path in sorted((root / BASE).glob(pattern)):
        content = load(path)
        num = content["batch"]
        if num in group:
            raise ValueError(f"{pattern}: duplicate batch {num}")
        if num not in expected_batches:
            raise ValueError(f"{pattern}: unexpected batch {num}")
        group[num] = (path, content)
    if set(group) != expected_batches:
        raise ValueError(f"{pattern}: missing batches {sorted(expected_batches - set(group))}")
    values = []
    for num in sorted(group):
        path, content = group[num]
        for item in content["items"]:
            if "verdict" in item and item["verdict"] not in AUDIT:
                raise ValueError(f"{path}: unsupported content verdict for {item['id']}")
            if "triage" in item and item["triage"] not in TRIAGE:
                raise ValueError(f"{path}: unsupported rights triage for {item['id']}")
            values.append({**item, "_file": str(path.relative_to(root))})
    return unique_index(values, pattern, allowed)


def load_followups(root, allowed):
    """Optional future *individual* rights/similarity followups, append-only.

    These are editorial evidence, never legal clearance or a v2 PASS.
    Files must explicitly identify the draft SHA reviewed, not just its title.
    """
    group = defaultdict(list)
    directory = root / BASE / "rights-followups-v2"
    for path in sorted(directory.glob("*.json")):
        item = load(path)
        ident = item["id"]
        if ident not in allowed:
            raise ValueError(f"{path}: unknown artwork id {ident}")
        if item.get("result") not in FOLLOWUP_RESULTS:
            raise ValueError(f"{path}: unknown followup result")
        digest = item.get("draft_sha256", "")
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError(f"{path}: invalid draft SHA")
        if not item.get("review_scope") or not item.get("observations"):
            raise ValueError(f"{path}: record actual scope and observations")
        if not isinstance(item.get("source_urls"), list):
            raise ValueError(f"{path}: source_urls must be a list")
        group[ident].append({**item, "_file": str(path.relative_to(root))})
    return group


def describe_changes(root, baseline_commit, relpath, current):
    """Compare the old draft at the original review commit without altering either file.

    If Git history is unavailable, leave the comparison unknown rather than
    declaring a changed file fully unchecked. 'Metadata only' still is not
    proof of rights clearance.
    """
    unknown = {
        "baseline_available": False, "text_changed": None,
        "source_urls_changed": None, "evidence_changed": None,
        "review_metadata_changed": None, "changed_paragraphs": [],
        "recheck_scope": "unknown_without_baseline",
    }
    if not baseline_commit:
        return unknown
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "show", f"{baseline_commit}:{relpath.as_posix()}"],
            capture_output=True, check=False,
        )
    except OSError:
        return unknown
    if proc.returncode != 0:
        return unknown
    try:
        previous = json.loads(proc.stdout)
    except (ValueError, UnicodeError):
        return unknown
    old = previous["visitor_explanation"]
    new = current["visitor_explanation"]
    text_changed = old["text"] != new["text"]
    urls_changed = old["source_urls"] != new["source_urls"]
    evidence_changed = previous.get("evidence") != current.get("evidence")
    review_changed = old.get("review") != new.get("review")
    hunks = []
    if text_changed:
        left = old["text"].split("\n\n")
        right = new["text"].split("\n\n")
        for op, a, b, c, d in SequenceMatcher(None, left, right).get_opcodes():
            if op != "equal":
                hunks.append({
                    "change": op,
                    "previous_paragraphs": left[a:b],
                    "current_paragraphs": right[c:d],
                })
    if not text_changed and not urls_changed:
        scope = "unchanged_text_and_sources"
    elif text_changed:
        scope = "recheck_changed_paragraphs_and_dependencies"
    else:
        scope = "recheck_changed_source_references"
    return {
        "baseline_available": True, "text_changed": text_changed,
        "source_urls_changed": urls_changed, "evidence_changed": evidence_changed,
        "review_metadata_changed": review_changed, "changed_paragraphs": hunks,
        "recheck_scope": scope,
    }


def build(root):
    root = Path(root).resolve()
    manifest = load(root / BASE / "manifest.json")
    originals = manifest["items"]
    items = unique_index(originals, "manifest")
    if len(items) != 100 or manifest.get("total_items") != 100:
        raise ValueError("expected exactly the saved 100-work PR #3 manifest")
    expected_batches = {item["batch"] for item in originals}
    content = read_groups(root, "batches/[0-9][0-9].json", items, expected_batches)
    screens = read_groups(root, "text-rights-screen-[0-9][0-9].json", items, expected_batches)
    if set(content) != set(items) or set(screens) != set(items):
        raise ValueError("manifest, historical content audits, and rights screens must have identical IDs")
    followups = load_followups(root, items)

    records = []
    for original in originals:
        ident = original["id"]
        relpath = Path(original["path"])
        if relpath.as_posix() != f"drafts/visitor-explanations/{ident}.json":
            raise ValueError(f"{ident}: unexpected draft path {relpath}")
        draft_path = root / relpath
        raw = draft_path.read_bytes()
        draft = json.loads(raw)
        if draft["id"] != ident:
            raise ValueError(f"{ident}: ID does not match its draft file")
        current_sha = hashlib.sha256(raw).hexdigest()
        changes = describe_changes(root, manifest.get("baseline_commit"), relpath, draft)
        prior = content[ident]
        screen = screens[ident]
        prior_current = prior["draft_sha256"] == current_sha
        screen_current = screen["draft_file_sha256"] == current_sha
        if screen["rights_status"] != "pending":
            raise ValueError(f"{ident}: legacy rights clearance must not be inferred")
        if screen["triage"] not in TRIAGE:
            raise ValueError(f"{ident}: unexpected triage")
        events = []
        for event in followups.get(ident, []):
            events.append({
                "record_file": event["_file"],
                "draft_sha256": event["draft_sha256"],
                "matches_current_draft": event["draft_sha256"] == current_sha,
                "result": event["result"],
                "review_scope": event["review_scope"],
                "observations": event["observations"],
                "source_urls": event["source_urls"],
            })
        records.append({
            "id": ident,
            "draft_path": str(relpath),
            "current_draft_sha256": current_sha,
            "manifest_sha256": original["sha256"],
            "manifest_matches_current_draft": original["sha256"] == current_sha,
            "changes_since_original_review": changes,
            "historical_content_audit": {
                "historically_reviewed": True,
                "record_file": prior["_file"],
                "draft_sha256": prior["draft_sha256"],
                "matches_current_draft": prior_current,
                "verdict": prior["verdict"],
                "support_summary": prior.get("support_summary"),
                "sources": prior.get("sources", []),
                "findings": prior.get("findings", []),
            },
            "historical_rights_prescreen": {
                "historically_screened": True,
                "record_file": screen["_file"],
                "draft_sha256": screen["draft_file_sha256"],
                "matches_current_draft": screen_current,
                "triage": screen["triage"],
                "reason": screen["reason"],
                "primary_source_url": screen["primary_source_url"],
                "source_scope": screen["source_scope"],
                "rights_clearance": "NOT_ASSESSED",
            },
            "subsequent_similarity_followups": events,
            "needs_independent_v2_audit": True,
            "eligible_for_auto_promotion": False,
        })

    totals = Counter(record["historical_rights_prescreen"]["triage"] for record in records)
    if totals != Counter({"priority_rewrite_or_review": 57, "further_review_required": 43}):
        raise ValueError(f"rights-screen original groups differ from the saved 57/43 triage: {dict(totals)}")
    return {
        "schema_version": "legacy-review-evidence-checkpoint-v2",
        "purpose": "Carry forward actual evidence by artwork ID and text SHA, never rename a pending check into PASS",
        "scope": "draft PR #3's 100 unmerged visitor explanations",
        "counts": {
            "records": len(records),
            "priority_originally_flagged": totals["priority_rewrite_or_review"],
            "other_rights_screened": totals["further_review_required"],
            "historical_content_audits_matching_current": sum(
                r["historical_content_audit"]["matches_current_draft"] for r in records
            ),
            "rights_prescreens_matching_current": sum(
                r["historical_rights_prescreen"]["matches_current_draft"] for r in records
            ),
            "changes_with_baseline_available": sum(
                r["changes_since_original_review"]["baseline_available"] for r in records
            ),
            "actual_text_edits_from_baseline": sum(
                r["changes_since_original_review"]["text_changed"] is True for r in records
            ),
            "unchanged_text_and_sources": sum(
                r["changes_since_original_review"]["recheck_scope"] == "unchanged_text_and_sources"
                for r in records
            ),
            "current_draft_similarity_followups_saved": sum(
                any(e["matches_current_draft"] for e in r["subsequent_similarity_followups"])
                for r in records
            ),
            "v2_complete": 0,
        },
        "artworks": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", metavar="FILE", type=Path, help="write an additive checkpoint; never edits drafts")
    group.add_argument("--verify", metavar="FILE", type=Path, help="compare a saved checkpoint to latest drafts")
    args = parser.parse_args()
    snapshot = build(args.root)
    if args.verify:
        if load(args.verify) != snapshot:
            parser.error("checkpoint stale: underlying text/audit/followup changed; rebuild after reviewing changes")
    if args.write:
        if args.write.exists():
            parser.error("refusing to overwrite an existing checkpoint; choose a new filename")
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(snapshot["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
