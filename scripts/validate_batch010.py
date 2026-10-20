#!/usr/bin/env python3
"""第10群の31候補・試験登録17件・保留14件と公式画像/権利の相互整合検証。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

catalog = {x["id"]: x for x in load("data/artworks.json")["artworks"]}
registry = {x["id"]: x for x in load("data/image-sources.json")["records"]}
candidates = load("data/candidates-batch-010.json")["works"]
report = load("docs/batch010-online-result.json")
results = {x["id"]: x for x in report["results"]}
errors = []
registered, held = 0, 0
if report.get("checked") != 31 or report.get("metadata_pass") != 25 or report.get("images_pass") != 25:
    errors.append("Official API/JPEG verification totals differ from examined batch")
if len(candidates) != 31 or len(results) != 31:
    errors.append("Batch010 candidate count mismatch")
for candidate in candidates:
    key = candidate["candidate_id"]
    proof = results.get(key)
    if not proof:
        errors.append(f"{key}: missing official proof")
        continue
    state = candidate["registration_status"]
    if state == "registered_provisional":
        registered += 1
        artwork, image = catalog.get(key), registry.get(key)
        if artwork is None or image is None:
            errors.append(f"{key}: missing registered artwork/image")
            continue
        if not proof.get("museum_record_verified") or not proof.get("image_verified") or proof.get("isPublicDomain") is not True:
            errors.append(f"{key}: official API, JPEG or PD proof invalid")
        if not proof.get("eligible_for_review"):
            errors.append(f"{key}: image display eligibility not satisfied")
        digests = [proof.get("image_sha256"),candidate.get("image_sha256"),
                   artwork["image"].get("sha256"),image["image_source"].get("sha256")]
        if not all(digests) or len(set(digests)) != 1:
            errors.append(f"{key}: SHA256 mismatch")
        actual_url = proof.get("image_url_verified")
        if not actual_url or artwork["image"].get("display_url") != actual_url or image["image_source"].get("verified_download_url") != actual_url:
            errors.append(f"{key}: primary JPEG URL mismatch")
        if candidate.get("accession_number") != proof.get("accessionNumber") or artwork["facts"].get("accession_number") != proof.get("accessionNumber"):
            errors.append(f"{key}: museum accession mismatch")
        if not candidate.get("official_api_live_checked") or not candidate.get("actual_image_download_verified"):
            errors.append(f"{key}: candidate falsely claims verification status")
        if artwork["facts"].get("is_public_domain_at_source") is not True:
            errors.append(f"{key}: catalog PD not true")
        if image["image_source"].get("type") != "met_open_access":
            errors.append(f"{key}: image host/source type mismatch")
    elif isinstance(state, str) and state.startswith("held_"):
        held += 1
        if key in catalog or key in registry:
            # Historical batch010 hold was on unsupported joy/expectation tagging.
            # Batch020 separately reassessed met-438130 as a zero-emotion work.
            # Retain the historical held status; require independent current evidence.
            latest_candidates = {x["candidate_id"]: x for x in load("data/candidates-batch-020.json")["works"]}
            latest_reports = {x["id"]: x for x in load("docs/batch020-online-result.json")["results"]}
            current = catalog.get(key)
            current_image = registry.get(key)
            newer = latest_candidates.get(key)
            newer_proof = latest_reports.get(key)
            justified = (
                key == "met-438130"
                and current is not None and current_image is not None
                and newer is not None and newer_proof is not None
                and newer.get("registration_status") == "registered_provisional"
                and newer.get("provisional_emotions") == {"primary": [], "secondary": []}
                and current["curation"]["emotions"] == []
                and current["curation"]["emotion_categories"] == {"primary": [], "secondary": []}
                and newer_proof.get("metadata_verified") is True
                and newer_proof.get("image_verified") is True
                and newer_proof.get("isPublicDomain") is True
                and newer_proof.get("classification") == "Paintings"
                and current["image"]["sha256"] == newer_proof.get("image_sha256")
                and current_image["image_source"]["sha256"] == newer_proof.get("image_sha256")
                and current["image"]["display_url"] == newer_proof.get("image_url_verified")
            )
            if not justified:
                errors.append(f"{key}: held item promoted without justified independent reassessment")
        if state == "held_official_pd_false" and proof.get("isPublicDomain") is not False:
            errors.append(f"{key}: rights hold contradicts official API")
        if candidate.get("image_sha256") != proof.get("image_sha256"):
            errors.append(f"{key}: held image SHA mismatch")
    else:
        errors.append(f"{key}: invalid status {state}")
if len(catalog) < 100 or len(registry) < 101 or registered != 17 or held != 14:
    errors.append(f"unexpected totals: catalog {len(catalog)}, image {len(registry)}, batch {registered}+{held}")
if errors:
    print("FAIL:", *errors, sep="\n- ")
    raise SystemExit(1)
print(f"PASS: {len(catalog)} provisional artworks, {len(registry)} image-source records; batch010 registered {registered}, held {held}; 25 official JPEGs verified.")
print("Image hashes and official PD flags do not establish the content or publication review state.")
