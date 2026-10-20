#!/usr/bin/env python3
"""第14群13候補、API/JPEG9件成功、登録9、保留4件、画像ハッシュ・状態の照合。"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((root/p).read_text(encoding="utf-8"))
catalog={x["id"]:x for x in load("data/artworks.json")["artworks"]}
registry={x["id"]:x for x in load("data/image-sources.json")["records"]}
candidates=load("data/candidates-batch-014.json")["works"]
result=load("docs/batch014-online-result.json")
proof={x["id"]:x for x in result["results"]}
errors=[]
if len(candidates)!=13 or result.get("checked")!=13 or result.get("metadata_pass")!=9 or result.get("images_pass")!=9 or len(proof)!=13:
    errors.append("Expected 13 candidates and 9 matching official records and JPEGs")
registered=held=0
for c in candidates:
    key=c["candidate_id"]
    p=proof.get(key)
    if not p:
        errors.append(key+": missing proof")
        continue
    if c.get("api_public_domain_flag") is not p.get("isPublicDomain") or c.get("accession_number")!=p.get("accessionNumber"):
        errors.append(key+": candidate vs official identity discrepancy")
    state=c.get("registration_status","")
    if state=="registered_provisional":
        registered+=1
        a=catalog.get(key)
        i=registry.get(key)
        if not a or not i or not p.get("museum_record_verified") or not p.get("image_verified") or p.get("isPublicDomain") is not True:
            errors.append(key+": unverified item in official catalog")
            continue
        if len({a["image"].get("sha256"),i["image_source"].get("sha256"),c.get("image_sha256"),p.get("image_sha256")})!=1:
            errors.append(key+": JPEG SHA256 mismatch")
        if len({a["image"].get("display_url"),i["image_source"].get("verified_download_url"),c.get("official_primary_image_url"),p.get("image_url_verified")})!=1:
            errors.append(key+": primary JPEG URL mismatch")
        if a["facts"].get("accession_number")!=p.get("accessionNumber") or i.get("accession_number")!=p.get("accessionNumber"):
            errors.append(key+": accession mismatch")
        if key=="met-829381" and "Unidentified court artist" not in a["facts"]["artist"]:
            errors.append(key+": inscription credit incorrectly attributed to painter")
        if key=="met-435765" and "Workshop" not in a["facts"]["artist"]:
            errors.append(key+": workshop incorrectly attributed to painter")
    elif state.startswith("held_"):
        held+=1
        if key in catalog or key in registry:
            errors.append(key+": held candidate promoted")
        if not c.get("curatorial_review_note"):
            errors.append(key+": reason for holding not recorded")
        if state=="held_official_pd_false" and p.get("isPublicDomain") is not False:
            errors.append(key+": rights hold contradicts proof")
        if state=="held_official_metadata_classification_unresolved" and p.get("museum_record_verified"):
            errors.append(key+": metadata hold contradicts proof")
    else:
        errors.append(key+": invalid candidate status")
if registered!=9 or held!=4 or len(catalog)<136 or len(registry)<137:
    errors.append(f"totals wrong: registered {registered}, held {held}, catalog {len(catalog)}, images {len(registry)}")
if errors:
    raise SystemExit("FAIL:\n"+"\n".join(errors))
print("PASS: Batch014 13 candidates / 9 official API+JPEG / 9 registered / 4 held; content identity, image SHA256 and review flags match.")
