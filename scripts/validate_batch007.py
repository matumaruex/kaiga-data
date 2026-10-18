#!/usr/bin/env python3
"""第7群11候補・公式API/JPEG結果・60作品DB・画像台帳の整合検査（ローカルのみ）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

db = load("data/artworks.json")
catalog = {a["id"]: a for a in db["artworks"]}
registry = {x["id"]: x for x in load("data/image-sources.json")["records"]}
candidates = load("data/candidates-batch-007.json")["works"]
results = {x["id"]: x for x in load("docs/batch007-online-result.json")["results"]}
errors = []
seen = set()
registered = 0
for candidate in candidates:
    ident = candidate["candidate_id"]
    if ident in seen:
        errors.append(f"{ident}: duplicate candidate ID")
    seen.add(ident)
    obj = results.get(ident, {})
    if obj.get("museum_record_verified") is not True or obj.get("image_verified") is not True:
        errors.append(f"{ident}: official metadata or primary JPEG not verified")
    if candidate.get("official_api_live_checked") is not True or candidate.get("actual_image_download_verified") is not True:
        errors.append(f"{ident}: candidate verification flags are not true")
    if candidate.get("image_sha256") != obj.get("image_sha256") or candidate.get("official_primary_image_url") != obj.get("image_url_verified"):
        errors.append(f"{ident}: candidate and report image mismatch")
    status = candidate.get("registration_status")
    if status == "registered_provisional":
        registered += 1
        art = catalog.get(ident)
        reg = registry.get(ident)
        if not art or not reg:
            errors.append(f"{ident}: registered candidate not in catalog/image registry")
            continue
        img = reg.get("image_source", {})
        if art["image"].get("sha256") != obj.get("image_sha256") or img.get("sha256") != obj.get("image_sha256"):
            errors.append(f"{ident}: catalog/image registry digest mismatch")
        if art["image"].get("display_url") != obj.get("image_url_verified"):
            errors.append(f"{ident}: primary display image URL mismatch")
        if art["source"]["artwork_id"] != candidate["museum_object_id"]:
            errors.append(f"{ident}: Met ID mismatch")
        if img.get("verified_download_url") != obj.get("image_url_verified"):
            errors.append(f"{ident}: registry image URL mismatch")
        if img.get("type") != "met_open_access":
            errors.append(f"{ident}: registry source type mismatch")
        if art["review"].get("visual_checked") is not False:
            errors.append(f"{ident}: human visual approval improperly implied")
    elif status in ("held_two_panel_image_completeness", "held_insufficient_emotion_basis"):
        if ident in catalog or ident in registry:
            errors.append(f"{ident}: held candidate promoted incorrectly")
    else:
        errors.append(f"{ident}: unknown registration status {status!r}")
if len(seen) != 11 or registered != 9 or len(catalog) != 60:
    errors.append(f"expected 11 candidate, 9 new registrations and 60 catalog; got {len(seen)}, {registered}, {len(catalog)}")
if errors:
    print("NG:", *errors, sep=chr(10) + "- ")
    raise SystemExit(1)
print(f"OK: {len(catalog)} artworks, {len(seen)} Met candidates, {registered} registered, 2 held, 11 API/JPEG hashes verified.")
print("This test does not replace a human visual, curatorial, or legal release review.")
