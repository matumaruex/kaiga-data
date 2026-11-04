#!/usr/bin/env python3
"""Check downloaded JPEG bytes against catalog fingerprints for one requested work.

This is a mechanical image check, not an image-subject or rights assessment.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def jpeg_dimensions(payload):
    if not (payload.startswith(b"\xff\xd8") and payload.endswith(b"\xff\xd9")):
        raise ValueError("not a complete JPEG")
    i = 2
    while i + 4 <= len(payload):
        if payload[i] != 255:
            i += 1
            continue
        while i < len(payload) and payload[i] == 255:
            i += 1
        if i >= len(payload):
            break
        marker = payload[i]
        i += 1
        if marker == 0 or marker == 0xD9:
            break
        if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > len(payload):
            break
        seg_len = int.from_bytes(payload[i:i + 2], "big")
        if seg_len < 2 or i + seg_len > len(payload):
            break
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if seg_len < 7:
                raise ValueError("invalid JPEG SOF marker")
            height = int.from_bytes(payload[i + 3:i + 5], "big")
            width = int.from_bytes(payload[i + 5:i + 7], "big")
            return width, height
        i += seg_len
    raise ValueError("JPEG dimensions not found")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    parser.add_argument("--commit-message")
    args = parser.parse_args()
    match = re.search(r"\[verify-target:(met-\d+|aic-\d+)\]", args.commit_message or "")
    identifier = args.id or (match.group(1) if match else None)
    if not identifier or not re.fullmatch(r"(met|aic)-\d+", identifier):
        parser.error("--id or [verify-target:met-12345] in commit message required")
    db = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))
    works = [a for a in db["artworks"] if a["id"] == identifier]
    if len(works) != 1:
        raise ValueError("catalog ID not unique or missing: " + identifier)
    art = works[0]
    image = art["image"]
    items = [
        ("original", image["high_resolution"]),
        ("display", {"url": image["display_url"],
                     "sha256": image["sha256"],
                     "byte_length": image["byte_length"]}),
    ]
    report = {"id": identifier,
              "checked_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "HTTP JPEG byte SHA256, length, dimensions; not visual identity",
              "images": []}
    for kind, expected in items:
        req = Request(expected["url"], headers={"User-Agent": "Mozilla/5.0 (artwork-validation; academic research)"})
        with urlopen(req, timeout=45) as response:
            status = response.status
            mime = response.headers.get("Content-Type", "")
            payload = response.read()
        sha = hashlib.sha256(payload).hexdigest()
        width, height = jpeg_dimensions(payload)
        item = {"kind": kind, "url": expected["url"], "status": status,
                "content_type": mime, "sha256": sha, "byte_length": len(payload),
                "width": width, "height": height,
                "matches_registered_bytes": sha == expected["sha256"]}
        print(json.dumps(item, ensure_ascii=False), flush=True)
        if status != 200 or not item["matches_registered_bytes"]:
            raise ValueError(f"{kind}: current JPEG differs from registered SHA")
        if "byte_length" in expected and len(payload) != expected["byte_length"]:
            raise ValueError(f"{kind}: length differs from registered bytes")
        if "width" in expected and (width != expected["width"] or height != expected["height"]):
            raise ValueError(f"{kind}: pixel dimensions differ")
        report["images"].append(item)
    output = ROOT / "artifacts" / "verified-target-image.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS: two registered image byte fingerprints matched for " + identifier)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERROR: {exc}")
