#!/usr/bin/env python3
"""Register one newly researched artwork, only with source- and version-bound v2 evidence.

This command does not research, generate text, inspect image pixels, or declare
copyright clearance. An actual separate review pass supplies the evidence.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

try:
    from . import visitor_draft_queue as drafts
except ImportError:
    import visitor_draft_queue as drafts

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^(aic|met)-[1-9][0-9]*$")
SHA = re.compile(r"^[0-9a-f]{64}$")
REVIEW_AREAS = {"identity", "image_match", "historical_interpretation", "emotion",
                "visitor_text", "rights"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_sha(record):
    clean = {k: v for k, v in record.items() if k != "completion"}
    return hashlib.sha256(json.dumps(clean, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def source_path(root, relative, parent):
    require(isinstance(relative, str) and relative.startswith(parent)
            and ".." not in Path(relative).parts, "unsafe evidence path")
    p = (root / relative).resolve()
    require(p.is_relative_to(root.resolve()) and p.is_file(), "missing evidence file: " + relative)
    return p


def checked_inputs(root, relative, *, need_baseline):
    path = source_path(root, relative, "docs/artwork-completion-audits/")
    audit = load(path)
    require(audit.get("schema_version") == "artwork-v2-new-registration-1",
            "unsupported new-artwork audit")
    ident = audit.get("id")
    require(isinstance(ident, str) and ID.fullmatch(ident), "unsupported artwork ID")
    require(audit.get("result") == "PASS"
            and audit.get("unresolved_material_issues") == [],
            "content problems or incomplete audit")
    candidate_path = source_path(root, audit.get("candidate_path"),
                                 "drafts/artwork-additions/")
    require(candidate_path.name == ident + ".json", "candidate identity path mismatch")
    require(file_sha(candidate_path) == audit.get("candidate_sha256"),
            "candidate changed after review")
    proposal = load(candidate_path)
    require(proposal.get("schema_version") == "artwork-addition-proposal-v1"
            and proposal.get("id") == ident, "invalid proposal identity")
    art, image_record = proposal["artwork"], proposal["image_record"]
    require(art["id"] == ident and image_record["id"] == ident,
            "artwork and image registry IDs differ")
    require("completion" not in art, "proposal must not contain a completion flag")
    require(art["facts"]["is_public_domain_at_source"] is True
            and art["facts"]["type"] == "Painting", "public-domain painting required")
    official = art["source"]["artwork_url"]
    source = image_record["image_source"]
    require(drafts.valid_url(official)
            and image_record["official_artwork_url"] == official, "official URL mismatch")
    museum = art["source"]["museum"]
    object_id = int(ident.split("-", 1)[1])
    require(art["source"]["artwork_id"] == object_id, "official object ID mismatch")
    if ident.startswith("met-"):
        require(official == "https://www.metmuseum.org/art/collection/search/" + str(object_id)
                and museum == "Metropolitan Museum of Art"
                and source["type"] == "met_open_access"
                and art["image"]["image_id"] == ident + "-primary",
                "unsupported Met object identity or image source")
        require(source.get("verified_download_url", "").startswith(
                "https://images.metmuseum.org/"), "Met official image URL required")
    else:
        require(official == "https://www.artic.edu/artworks/" + str(object_id)
                and source["type"] == "wikimedia_commons"
                and source.get("commons_file_page", "").startswith(
                    "https://commons.wikimedia.org/wiki/File:"),
                "Chicago image requires accession-matched Commons rights evidence")
        require(re.fullmatch(r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}",
                             art["image"]["image_id"]) is not None,
                "Chicago IIIF image identifier missing")

    require(image_record.get("in_shared_catalog") is True
            and image_record.get("official_artwork_url") == art["source"]["artwork_url"],
            "new image must be registered to this artwork")
    require(art["image"]["source_registry_id"] == ident, "image registry link missing")
    require(art["image"]["display_url"] in
            (source.get("verified_download_url"), source.get("download_url")),
            "display URL not bound to registered image")
    require(art["image"]["sha256"] == source.get("sha256")
            and art["image"]["byte_length"] == source.get("byte_length")
            and SHA.fullmatch(art["image"]["sha256"]), "JPEG digest and byte count mismatch")
    high = art["image"].get("high_resolution")
    high_src = source.get("high_resolution")
    require((high is None) == (high_src is None), "high-resolution registry mismatch")
    if high is not None:
        require(all(high.get(k) == high_src.get(k) for k in
                    ("url", "sha256", "byte_length", "width", "height", "verification")),
                "high-resolution bytes or dimensions changed")
        require(high["verification"] == "complete_jpeg_sha256_and_downscale_match",
                "high-resolution verification required")
    require(source.get("license_url") and drafts.valid_url(source["license_url"])
            and source.get("license_label"), "image license evidence missing")
    require(source.get("official_image_page") or source.get("commons_file_page"),
            "image source page required")

    draft_path = source_path(root, audit.get("draft_path"),
                             "drafts/visitor-explanations/")
    require(draft_path.name == ident + ".json"
            and file_sha(draft_path) == audit.get("draft_sha256"),
            "visitor draft changed after review")
    draft = load(draft_path)
    require(not drafts.check_file(draft_path, {ident: {"id": ident}}),
            "visitor draft evidence is invalid")
    require(draft["visitor_explanation"] == art.get("visitor_explanation"),
            "visitor text does not match reviewed draft")
    require(all(e["checked_against_source"] is True for e in draft["evidence"]),
            "unread visitor text evidence")
    visitor = art["visitor_explanation"]
    require(all(visitor["review"][k] == "verified" for k in
                ("content_status", "source_status", "rights_status")),
            "new visitor text needs all three reviews verified")

    sources = audit.get("source_evidence", [])
    require(isinstance(sources, list) and sources
            and all(drafts.valid_url(s.get("url")) and s.get("location")
                    and s.get("finding") and s.get("checked_against_source") is True
                    for s in sources), "review must cite independently checked source locations")
    source_urls = {s["url"] for s in sources}
    require(set(visitor["source_urls"]) <= source_urls
            and official in source_urls
            and art["curation"]["evidence_url"] in source_urls
            and art["curation"]["meaning_basis"]["scholarly_interpretation"]["source_url"]
            in source_urls, "visitor and selection sources need directly checked evidence")
    rights = audit.get("rights", {})
    for section in ("artwork", "image", "text"):
        detail = rights.get(section, {})
        require(detail.get("verified") is True and detail.get("finding")
                and drafts.valid_url(detail.get("source_url"))
                and detail["source_url"] in source_urls,
                "insufficient evidence for " + section + " rights")
    require(rights["artwork"]["public_domain"] is True
            and rights["image"]["permitted_for_site_use"] is True
            and rights["text"]["independent_japanese_prose"] is True,
            "work, JPEG and explanatory text rights must be assessed separately")
    require(rights["image"]["source_url"] == source["license_url"],
            "image rights must match the exact image registry record")
    require(audit.get("separate_pass_review", {}).get("result") == "PASS"
            and audit["separate_pass_review"].get("method")
            and audit["separate_pass_review"].get("limitations")
            and REVIEW_AREAS <= set(audit["separate_pass_review"].get("areas", [])),
            "separate source/visual/content review incomplete")
    image_evidence = audit.get("image_evidence", [])
    required_images = [("display", art["image"]["display_url"],
                        art["image"]["sha256"], art["image"]["byte_length"])]
    if high is not None:
        required_images.append(("original", high["url"], high["sha256"], high["byte_length"]))
    require(len(image_evidence) == len(required_images), "all image variants need evidence")
    for kind, url, digest, size in required_images:
        evidence = next((e for e in image_evidence if e.get("kind") == kind), None)
        require(evidence is not None and evidence.get("url") == url
                and evidence.get("sha256") == digest and evidence.get("byte_length") == size
                and evidence.get("download_status") == 200
                and evidence.get("full_bytes_sha256_checked") is True
                and evidence.get("image_subject_visually_compared") is True
                and evidence.get("observation") and evidence.get("checked_on"),
                kind + " JPEG/visual evidence missing")
    if need_baseline:
        data_path, registry_path = root / "data/artworks.json", root / "data/image-sources.json"
        baseline = audit.get("baseline", {})
        require(baseline.get("artworks_sha256") == file_sha(data_path)
                and baseline.get("image_registry_sha256") == file_sha(registry_path),
                "database changed since the candidate was checked")
    return audit, art, image_record


def render_summary(readme, total):
    start, end = "<!-- EXPANSION_COUNT_START -->", "<!-- EXPANSION_COUNT_END -->"
    require(readme.count(start) == 1 and readme.count(end) == 1,
            "README dynamic count markers missing")
    before, rest = readme.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n**v2完成登録：" + str(total) + "作品**\n" + end + after


def candidate_files(root, audit_file):
    relative = str(audit_file.relative_to(root))
    _, art, image_record = checked_inputs(root, relative, need_baseline=True)
    data = load(root / "data/artworks.json")
    registry = load(root / "data/image-sources.json")
    baseline = set(load(root / "data/baseline-300-ids.json")["ids"])
    ident = art["id"]
    require(ident not in baseline, "original 300 works cannot be added again")
    require(ident not in {a["id"] for a in data["artworks"]}
            and ident not in {r["id"] for r in registry["records"]},
            "artwork ID already registered")
    require(all(a["source"]["artwork_url"] != art["source"]["artwork_url"]
                for a in data["artworks"]), "this official object already exists")
    require(all(a["facts"]["title_original"] != art["facts"]["title_original"]
                or a["facts"]["artist"] != art["facts"]["artist"]
                for a in data["artworks"]), "identical title and artist need manual disambiguation")
    require(all(a["image"]["sha256"] != art["image"]["sha256"]
                for a in data["artworks"]), "identical JPEG already registered")

    snapshot = copy.deepcopy(art)
    snapshot["completion"] = {
        "schema_version": "artwork-completion-v2-new-1",
        "audit_path": str(audit_file.relative_to(root)),
        "audit_sha256": file_sha(audit_file),
        "record_sha256": record_sha(art),
    }
    data["artworks"].append(snapshot)
    registry["records"].append(image_record)
    readme = render_summary((root / "README.md").read_text(encoding="utf-8"),
                            len(data["artworks"]))
    return {
        "data/artworks.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        "data/image-sources.json": json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        "README.md": readme,
    }


def validate_candidate(root, files):
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        shutil.copytree(root / "data", temp / "data")
        shutil.copytree(root / "scripts", temp / "scripts",
                        ignore=shutil.ignore_patterns("__pycache__"))
        for filename, value in files.items():
            path = temp / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
        for name in ("validate_artworks.py", "check_image_sources.py",
                     "check_catalog_snapshot.py"):
            run = subprocess.run([sys.executable, str(temp / "scripts" / name)],
                                 cwd=temp, capture_output=True, text=True, timeout=60)
            require(run.returncode == 0,
                    name + " failed:\n" + run.stdout + run.stderr)


def save_files(root, files):
    previous = {name: (root / name).read_bytes() for name in files}
    staging = {}
    try:
        # Pre-build all files, then replace; Git commit is the publication boundary.
        for name, content in files.items():
            f = root / name
            fd, tmp = tempfile.mkstemp(prefix="." + f.name, dir=f.parent)
            with os.fdopen(fd, "wb") as stream:
                stream.write(content.encode("utf-8"))
                stream.flush()
                os.fsync(stream.fileno())
            staging[name] = tmp
        require(all((root / name).read_bytes() == value for name, value in previous.items()),
                "files changed during validation")
        for name, tmp in staging.items():
            os.replace(tmp, root / name)
    except Exception:
        for name, value in previous.items():
            (root / name).write_bytes(value)
        raise
    finally:
        for tmp in staging.values():
            if os.path.exists(tmp):
                os.unlink(tmp)


def verify_saved(root, art):
    completion = art.get("completion", {})
    require(completion.get("schema_version") == "artwork-completion-v2-new-1",
            "new-artwork completion marker missing")
    require(record_sha(art) == completion.get("record_sha256"),
            "registered artwork changed without re-audit")
    audit_file = source_path(root, completion.get("audit_path", ""),
                             "docs/artwork-completion-audits/")
    require(file_sha(audit_file) == completion.get("audit_sha256"),
            "registration audit changed")
    audit, original, image = checked_inputs(root, str(audit_file.relative_to(root)),
                                            need_baseline=False)
    require(audit["id"] == art["id"] and original == {k: v for k, v in art.items()
                                                    if k != "completion"},
            "reviewed artwork does not match stored record")
    registry = load(root / "data/image-sources.json")["records"]
    match = [r for r in registry if r["id"] == art["id"]]
    require(len(match) == 1 and match[0] == image,
            "reviewed image record does not match stored registry")


def check(root):
    baseline = set(load(root / "data/baseline-300-ids.json")["ids"])
    additions = [a for a in load(root / "data/artworks.json")["artworks"]
                 if a["id"] not in baseline]
    for art in additions:
        verify_saved(root, art)
    print("PASS: " + str(len(additions)) + " registered v2 additions")
    return len(additions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["preview", "save", "check"])
    parser.add_argument("--audit")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.action == "check":
            check(root)
            return 0
        require(args.audit, "preview/save requires --audit")
        audit_path = source_path(root, args.audit,
                                 "docs/artwork-completion-audits/")
        files = candidate_files(root, audit_path)
        validate_candidate(root, files)
        if args.action == "save":
            save_files(root, files)
            print("SAVED: one new artwork, updated image registry and README")
        else:
            print("PASS: one new artwork; no files changed")
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as e:
        parser.exit(1, "FAIL: " + str(e) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
