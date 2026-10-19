#!/usr/bin/env python3
"""第15群21候補・オンライン20合格・16登録・5保留と画像のハッシュ整合を確認"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((root/p).read_text(encoding="utf-8"))
catalog={a["id"]:a for a in load("data/artworks.json")["artworks"]}
images={a["id"]:a for a in load("data/image-sources.json")["records"]}
batch=load("data/candidates-batch-015.json")["works"]
evidence=load("docs/batch015-online-result.json")
proof={x["id"]:x for x in evidence["results"]}
errors=[]
if len(batch)!=21 or len(proof)!=21 or evidence["images_pass"]!=20 or evidence["metadata_pass"]!=20:
    errors.append("Original research totals must be 21,20,20")
registered=held=0
for c in batch:
    k=c["candidate_id"];p=proof.get(k)
    if not p or c.get("api_public_domain_flag") is not p.get("isPublicDomain"):
        errors.append(k+": missing or mismatched rights proof")
        continue
    if c["registration_status"]=="registered_provisional":
        registered+=1
        a=catalog.get(k);i=images.get(k)
        if not a or not i or not p.get("image_verified") or p.get("isPublicDomain") is not True:
            errors.append(k+": invalid registration")
            continue
        if len({c.get("image_sha256"),p.get("image_sha256"),a["image"]["sha256"],i["image_source"]["sha256"]})!=1:
            errors.append(k+": mismatched SHA256")
        if len({c.get("official_primary_image_url"),p.get("image_url_verified"),a["image"]["display_url"],i["image_source"]["verified_download_url"]})!=1:
            errors.append(k+": mismatched image URLs")
        if a["review"]["visual_checked"] is not False or a["review"]["interpretation_human_approved"] is not False:
            errors.append(k+": human approval not established")
    elif str(c["registration_status"]).startswith("held_"):
        held+=1
        if k in catalog or k in images:
            errors.append(k+": held item was registered")
        if not c.get("curatorial_review_note"):
            errors.append(k+": no reason for hold")
    else:
        errors.append(k+": unknown status")
if registered!=16 or held!=5 or len(catalog)<152 or len(images)<153:
    errors.append(f"wrong counts {registered}/{held} catalog {len(catalog)} images {len(images)}")
if errors:
    raise SystemExit("FAIL:\n"+"\n".join(errors))
print("PASS: batch015 21 candidates / 20 official API-JPEG success / 16 registered / 5 held.")
