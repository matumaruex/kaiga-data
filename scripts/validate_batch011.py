#!/usr/bin/env python3
"""第11群: Metの10件・公式画像SHA256・作品台帳間の照合。"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((root/path).read_text(encoding="utf-8"))
catalog={x["id"]:x for x in read("data/artworks.json")["artworks"]}
registry={x["id"]:x for x in read("data/image-sources.json")["records"]}
candidates=read("data/candidates-batch-011.json")["works"]
proof=read("docs/batch011-online-result.json")
results={x["id"]:x for x in proof["results"]}
errors=[]
if len(candidates)!=10 or len(results)!=10 or proof["metadata_pass"]!=10 or proof["images_pass"]!=10:
    errors.append("Batch011 must have 10 independently verified entries")
for c in candidates:
    k=c["candidate_id"]
    o,i,p=catalog.get(k),registry.get(k),results.get(k)
    if c.get("registration_status")!="registered_provisional" or not o or not i or not p:
        errors.append(k+": missing full registration")
        continue
    if not p.get("museum_record_verified") or not p.get("image_verified") or not p.get("eligible_for_review") or p.get("isPublicDomain") is not True:
        errors.append(k+": missing verified Met identity/public domain/JPEG")
    if any(x!=p.get("image_sha256") for x in (o["image"].get("sha256"),i["image_source"].get("sha256"),c.get("image_sha256"))):
        errors.append(k+": image digest mismatch")
    if any(x!=p.get("image_url_verified") for x in (o["image"].get("display_url"),i["image_source"].get("verified_download_url"),c.get("official_primary_image_url"))):
        errors.append(k+": source URL mismatch")
    if p.get("accessionNumber")!=o["facts"].get("accession_number") or p.get("accessionNumber")!=i.get("accession_number"):
        errors.append(k+": accession mismatch")
    if o["facts"].get("is_public_domain_at_source") is not True:
        errors.append(k+": missing public domain evidence")
    if o["curation"]["meaning_basis"]["author_intent"]["status"]=="not_verified_for_this_work" and o["curation"]["meaning_basis"]["author_intent"]["summary"] is not None:
        errors.append(k+": unverified author intent asserted")
if len(catalog)<110 or len(registry)<111:
    errors.append("Expected at least 110 registered artworks and 111 image entries")
if errors:
    raise SystemExit("FAIL:\\n"+"\\n".join(errors))
print("PASS: 10 verified Met artworks / primary image hashes and authoritative references; content review tracked separately.")
