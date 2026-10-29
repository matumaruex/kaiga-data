#!/usr/bin/env python3
"""Save one evidence-checked existing artwork; never generate an AI judgment."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

try:
    from . import visitor_draft_queue as queue
except ImportError:
    import visitor_draft_queue as queue

ROOT = Path(__file__).resolve().parents[1]
AREAS = {"identity", "context_and_interpretation", "emotion", "text_and_similarity"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(root, relative):
    require(isinstance(relative, str) and not Path(relative).is_absolute(), "relative path required")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "path outside repository")
    return path


def load_bound(root, ref):
    path = local_path(root, ref["path"])
    require(file_hash(path) == ref["sha256"], "evidence file changed: " + ref["path"])
    return queue.load(path)


def checked_inputs(root, audit_path):
    audit_path = local_path(root, audit_path)
    audit = queue.load(audit_path)
    require(audit["schema_version"] == "artwork-v2-source-recheck-1", "unsupported audit")
    require(audit["result"] == "PASS" and audit["promotion"]["eligible"] is True
            and audit["remaining"] == [], "audit is not eligible for registration")
    require(audit["result_applies_to"] == "proposed_artwork_and_current_visitor_draft", "wrong audit scope")
    review = audit["separate_pass_review"]
    require(review["completed"] is True and review["result"] == "PASS"
            and bool(review["method"]) and bool(review["limitations"]), "source recheck missing")
    require(AREAS <= {x["area"] for x in review["checks"] if x.get("finding")}, "incomplete review")
    rights = audit["rights_check"]
    require(rights.get("result") == "PASS" and rights.get("unresolved_material_issues") == []
            and rights.get("finding") and rights.get("locations")
            and queue.valid_url(rights.get("source_url")), "rights assessment incomplete")
    require(audit["program_checks"]["result"] == "PASS", "prior program check failed")
    proposal = load_bound(root, audit["proposal"])
    version = audit["version"]
    require(proposal["schema_version"] == "artwork-revision-proposal-v1"
            and proposal["id"] == audit["id"], "proposal identity mismatch")
    require(proposal["baseline_artwork_sha256"] == version["artwork_record_sha256"], "baseline mismatch")
    draft_path = local_path(root, version["draft_path"])
    dh = file_hash(draft_path)
    require(dh == version["draft_sha256"] == proposal["visitor_draft_sha256"]
            == review["reviewed_visitor_draft_sha256"]
            == audit["program_checks"]["visitor_draft_sha256"], "draft changed")
    require(proposal["visitor_draft_path"] == version["draft_path"], "draft path mismatch")
    draft = queue.load(draft_path)
    require(draft["id"] == audit["id"], "draft identity mismatch")
    # Validate the draft independently of whether an identical saved copy exists.
    errors = queue.check_file(draft_path, {audit["id"]: {"id": audit["id"]}})
    require(not errors, "; ".join(errors))
    require(all(x["checked_against_source"] is True for x in draft["evidence"]), "unchecked source")
    require("needs_revision" not in draft["visitor_explanation"]["review"].values(), "draft needs revision")
    sources = {s["url"] for s in audit["sources"] if s.get("access") == "page_read_twice"
               and s.get("locations") and s.get("observed") and queue.valid_url(s.get("url"))}
    require(set(draft["visitor_explanation"]["source_urls"]) <= sources, "unread visitor source")
    ph = proposal["proposed_artwork_sha256"]
    require(ph == audit["proposal"]["proposed_artwork_sha256"]
            == review["reviewed_artwork_sha256"]
            == audit["program_checks"]["proposed_artwork_sha256"], "candidate hash mismatch")
    require(file_hash(local_path(root, audit["proposal"]["path"]))
            == audit["program_checks"]["proposal_sha256"], "program proposal mismatch")
    return audit, proposal, draft, sources


def record_hash(art):
    content = {k: v for k, v in art.items() if k != "completion"}
    return digest(content)


def validate_candidate(root, data):
    # Use the repository's real structural and snapshot validators on an isolated copy.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(root / "data", tmp / "data")
        shutil.copytree(root / "scripts", tmp / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(root / "README.md", tmp / "README.md")
        (tmp / "data/artworks.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        for name in ("validate_artworks.py", "check_catalog_snapshot.py"):
            run = subprocess.run([sys.executable, str(tmp / "scripts" / name)], capture_output=True, text=True)
            require(run.returncode == 0, run.stdout + run.stderr)


def build(root, relative):
    audit, proposal, draft, sources = checked_inputs(root, relative)
    data = queue.load(root / "data/artworks.json")
    ids = [a["id"] for a in data["artworks"]]
    require(len(ids) == len(set(ids)) and ids.count(audit["id"]) == 1, "catalog identity mismatch")
    index = ids.index(audit["id"])
    art = data["artworks"][index]
    require("completion" not in art, "already saved; use check to verify")
    require(digest(art) == audit["version"]["artwork_record_sha256"], "catalog version changed")
    require("visitor_explanation" not in art, "existing explanation replacement is not supported yet")
    candidate = copy.deepcopy(art)
    for change in proposal["changes"]:
        path = change["path"]
        require(path and path[0] == "curation", "only reviewed curation revisions supported")
        require(change.get("reason") and set(change["source_urls"]) <= sources, "unread revision source")
        target = candidate
        for key in path[:-1]:
            target = target[key]
        require(target[path[-1]] == change["before"], "proposal before-value mismatch")
        target[path[-1]] = copy.deepcopy(change["after"])
    require(digest(candidate) == proposal["proposed_artwork_sha256"], "proposal content mismatch")
    require(candidate["curation"]["evidence_url"] in sources, "unread selection source")
    image = candidate["image"]
    images = audit["images"]
    require(len(images) == 2 and {x["kind"] for x in images} == {"original", "display"}, "image evidence missing")
    for im in images:
        registered = image["high_resolution"] if im["kind"] == "original" else {
            "url": image["display_url"], "sha256": image["sha256"]}
        require(im["id"] == audit["id"] and im["status"] == 200 and im["matches_registered_bytes"] is True
                and im["sha256"] == registered["sha256"] and im["url"] == registered["url"], "image mismatch")
    require(audit["visual_observations"].get("observed"), "visual comparison missing")
    candidate["visitor_explanation"] = copy.deepcopy(draft["visitor_explanation"])
    # Preserve legacy review fields. This version-bound completion is the v2 authority.
    candidate["completion"] = {"schema_version": "artwork-completion-v2-1",
                               "audit_path": relative, "audit_sha256": file_hash(local_path(root, relative)),
                               "record_sha256": record_hash(candidate)}
    data["artworks"][index] = candidate
    original = queue.load(root / "data/artworks.json")
    require(all(a == b for a, b in zip(original["artworks"], data["artworks"])
                if a["id"] != audit["id"]), "unrelated artwork changed")
    validate_candidate(root, data)
    return data


def save(root, relative):
    target = root / "data/artworks.json"
    before = target.read_bytes()
    data = build(root, relative)
    require(target.read_bytes() == before, "catalog changed during validation")
    payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".artworks-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        require(target.read_bytes() == before, "catalog changed before write")
        os.replace(tmp, target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def check(root):
    counts = {"完成": 0, "未完成": 0, "保留": 0}
    holds = set()
    for path in (root / "docs/artwork-completion-audits").glob("*.json"):
        audit = queue.load(path)
        if audit.get("result") == "HOLD" and audit.get("remaining"):
            holds.add((audit["id"], audit["version"]["artwork_record_sha256"]))
    for art in queue.records(root):
        c = art.get("completion")
        if c is None:
            counts["保留" if (art["id"], digest(art)) in holds else "未完成"] += 1
            continue
        require(c.get("schema_version") == "artwork-completion-v2-1", "unsupported completion")
        require(record_hash(art) == c["record_sha256"], "saved artwork changed: " + art["id"])
        require(file_hash(local_path(root, c["audit_path"])) == c["audit_sha256"], "saved audit changed")
        audit, proposal, draft, _ = checked_inputs(root, c["audit_path"])
        require(audit["id"] == art["id"], "saved identity mismatch")
        require(art["visitor_explanation"] == draft["visitor_explanation"], "saved text mismatch")
        candidate = {k: v for k, v in art.items() if k not in {"completion", "visitor_explanation"}}
        require(digest(candidate) == proposal["proposed_artwork_sha256"], "saved candidate mismatch")
        counts["完成"] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("action", choices=["preview", "save", "check"])
    parser.add_argument("--audit")
    args = parser.parse_args()
    try:
        if args.action == "check":
            print(json.dumps(check(args.root), ensure_ascii=False))
        else:
            require(args.audit is not None, "--audit is required")
            if args.action == "save":
                save(args.root, args.audit)
            else:
                build(args.root, args.audit)
            print("PASS: one artwork " + ("saved" if args.action == "save" else "validated; no write"))
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
