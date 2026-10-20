#!/usr/bin/env python3
"""第13群12候補、公式API/JPEG10成功、試験登録9、保留3の整合検証。"""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((root/path).read_text(encoding="utf-8"))
catalog = {x["id"]:x for x in load("data/artworks.json")["artworks"]}
registry = {x["id"]:x for x in load("data/image-sources.json")["records"]}
candidates = load("data/candidates-batch-013.json")["works"]
report = load("docs/batch013-online-result.json")
proofs = {x["id"]:x for x in report["results"]}
errors = []
if len(candidates)!=12 or report.get("checked")!=12 or len(proofs)!=12 or report.get("metadata_pass")!=10 or report.get("images_pass")!=10:
    errors.append("Expected 12 candidates and 10 independently verified Met API/JPEG pairs")
registered=held=0
for c in candidates:
    key=c["candidate_id"]
    p=proofs.get(key)
    if not p:
        errors.append(key+": missing proof")
        continue
    if c.get("api_public_domain_flag") is not p.get("isPublicDomain") or c.get("accession_number")!=p.get("accessionNumber"):
        errors.append(key+": official ID/accession/public domain inconsistency")
    state=c.get("registration_status","")
    if state=="registered_provisional":
        registered+=1
        a=catalog.get(key)
        img=registry.get(key)
        if not a or not img or not p.get("museum_record_verified") or not p.get("image_verified") or p.get("isPublicDomain") is not True:
            errors.append(key+": unverified artwork or image was registered")
            continue
        if len({a["image"].get("sha256"),img["image_source"].get("sha256"),c.get("image_sha256"),p.get("image_sha256")})!=1:
            errors.append(key+": primary image digest mismatch")
        if len({a["image"].get("display_url"),img["image_source"].get("verified_download_url"),c.get("official_primary_image_url"),p.get("image_url_verified")})!=1:
            errors.append(key+": verified primary image URL mismatch")
        if a["facts"].get("accession_number")!=p.get("accessionNumber") or img.get("accession_number")!=p.get("accessionNumber"):
            errors.append(key+": accession mismatch")
        if a["facts"].get("is_public_domain_at_source") is not True:
            errors.append(key+": missing PD confirmation")
    elif state.startswith("held_"):
        held+=1
        if key in catalog or key in registry:
            errors.append(key+": held artwork promoted to catalog or image registry")
        if not c.get("curatorial_review_note"):
            errors.append(key+": no hold reason")
        if state=="held_official_pd_false" and p.get("isPublicDomain") is not False:
            errors.append(key+": official rights hold contradicts API")
        if state=="held_insufficient_scholarly_context" and (not p.get("museum_record_verified") or not p.get("image_verified")):
            errors.append(key+": expected passing online checks for content hold")
    else:
        errors.append(key+": unknown state "+state)
if registered!=9 or held!=3 or len(catalog)<127 or len(registry)<128:
    errors.append(f"wrong counts {registered} registered {held} held catalog {len(catalog)} images {len(registry)}")
if errors:
    raise SystemExit("FAIL:\n"+"\n".join(errors))
print(f"PASS: Batch013 12 candidates, 10 official API/JPEG verified, {registered} registered, {held} held.")
