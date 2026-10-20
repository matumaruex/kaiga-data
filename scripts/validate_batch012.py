#!/usr/bin/env python3
"""第12群の10件の公式API証拠、8登録、2保留、画像台帳を厳格に照合。"""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((root/path).read_text(encoding="utf-8"))
artworks={a["id"]:a for a in read("data/artworks.json")["artworks"]}
images={i["id"]:i for i in read("data/image-sources.json")["records"]}
candidates=read("data/candidates-batch-012.json")["works"]
report=read("docs/batch012-online-result.json")
proof={x["id"]:x for x in report["results"]}
errors=[]
if len(candidates)!=10 or len(proof)!=10 or report["metadata_pass"]!=10 or report["images_pass"]!=10:
    errors.append("Source proof must contain 10 API/JPEG successes")
registered=held=0
for c in candidates:
    k=c["candidate_id"];p=proof.get(k)
    if not p or not p.get("museum_record_verified") or not p.get("image_verified") or not p.get("eligible_for_review") or p.get("isPublicDomain") is not True:
        errors.append(k+": incomplete original Met evidence")
        continue
    if c.get("image_sha256")!=p.get("image_sha256") or c.get("accession_number")!=p.get("accessionNumber"):
        errors.append(k+": candidate/proof mismatch")
    if c.get("registration_status")=="registered_provisional":
        registered+=1
        a=artworks.get(k);i=images.get(k)
        if not a or not i:
            errors.append(k+": missing registered artwork or registry")
            continue
        if a["facts"]["is_public_domain_at_source"] is not True:
            errors.append(k+": artwork not PD")
        if len({a["image"].get("sha256"),i["image_source"].get("sha256"),c.get("image_sha256"),p.get("image_sha256")})!=1:
            errors.append(k+": SHA256 mismatch")
        if len({a["image"].get("display_url"),i["image_source"].get("verified_download_url"),c.get("official_primary_image_url"),p.get("image_url_verified")})!=1:
            errors.append(k+": official image URL mismatch")
        if a["facts"].get("accession_number")!=p.get("accessionNumber") or i.get("accession_number")!=p.get("accessionNumber"):
            errors.append(k+": accession mismatch")
        if i["image_source"].get("type")!="met_open_access":
            errors.append(k+": incorrect image origin")
    elif str(c.get("registration_status") or "").startswith("held_"):
        held+=1
        if k in artworks or k in images:
            # Historical batch012 hold was about unsupported emotions, not identity/PD.
            # Batch021 independently verifies the same painting without emotion tags.
            latest = {x["candidate_id"]: x for x in read("data/candidates-batch-021.json")["works"]}
            recent_proofs = {x["id"]: x for x in read("docs/batch021-online-result.json")["results"]}
            a=artworks.get(k);i=images.get(k);new=latest.get(k);recent=recent_proofs.get(k)
            justified = (
                k == "met-45647" and a is not None and i is not None
                and new is not None and recent is not None
                and new.get("registration_status") == "registered_provisional"
                and new.get("provisional_emotions") == {"primary": [], "secondary": []}
                and new.get("historical_hold_preserved") is True
                and a["curation"]["emotions"] == []
                and a["curation"]["emotion_categories"] == {"primary": [], "secondary": []}
                and recent.get("metadata_verified") is True
                and recent.get("image_verified") is True
                and recent.get("isPublicDomain") is True
                and recent.get("classification") == "Paintings"
                and recent.get("image_sha256") == a["image"]["sha256"] == i["image_source"]["sha256"]
                and recent.get("image_url_verified") == a["image"]["display_url"] == i["image_source"]["verified_download_url"]
            )
            if not justified:errors.append(k+": held work promoted without justified independent tagless reassessment")
        if not c.get("curatorial_review_note"):
            errors.append(k+": missing hold reason")
    else:
        errors.append(k+": unknown registration state")
if registered!=8 or held!=2 or len(artworks)<118 or len(images)<119:
    errors.append(f"unexpected totals: {registered} registered, {held} held, {len(artworks)} artworks, {len(images)} images")
if errors:
    raise SystemExit("FAIL:\n"+"\n".join(errors))
print("PASS: Batch012 10 verified, 8 provisionally registered, 2 held; 118 artworks, 119 image records")
