#!/usr/bin/env python3
"""第16群：20候補、公式画像16件合格、12登録、8保留の相互照合"""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
def read(p):return json.loads((r/p).read_text(encoding="utf-8"))
art={x["id"]:x for x in read("data/artworks.json")["artworks"]}
images={x["id"]:x for x in read("data/image-sources.json")["records"]}
cands=read("data/candidates-batch-016.json")["works"]
evi=read("docs/batch016-online-result.json")
proof={x["id"]:x for x in evi["results"]}
errors=[]
if len(cands)!=20 or len(proof)!=20 or evi.get("images_pass")!=16 or evi.get("metadata_pass")!=16:errors.append("research totals changed")
registered=held=0
for c in cands:
 k=c["candidate_id"];p=proof.get(k)
 if not p:errors.append(k+": proof missing");continue
 if c.get("api_public_domain_flag") is not p.get("isPublicDomain"):errors.append(k+": PD discrepancy")
 if c["registration_status"]=="registered_provisional":
  registered+=1;a=art.get(k);i=images.get(k)
  if not a or not i or not p.get("image_verified") or p.get("isPublicDomain") is not True:errors.append(k+": invalid registration");continue
  if len({a["image"]["sha256"],i["image_source"]["sha256"],c.get("image_sha256"),p.get("image_sha256")})!=1:errors.append(k+": SHA mismatch")
  if len({a["image"]["display_url"],i["image_source"]["verified_download_url"],c.get("official_primary_image_url"),p.get("image_url_verified")})!=1:errors.append(k+": URL mismatch")
  if a["review"]["visual_checked"] is not False or a["review"]["interpretation_human_approved"] is not False:errors.append(k+": human approval incorrectly asserted")
  if k=="met-853216" and "Tanomura" not in a["facts"]["artist"]:errors.append(k+": artist/painter attribution wrong")
  if k=="met-37906" and not a["facts"]["artist"].startswith("Style of"):errors.append(k+": author attribution wrong")
 elif c["registration_status"].startswith("held_"):
  held+=1
  if k in art or k in images:errors.append(k+": wrongly promoted")
  if not c.get("curatorial_review_note"):errors.append(k+": hold reason missing")
 else:errors.append(k+": unknown status")
if registered!=12 or held!=8 or len(art)<164 or len(images)<165:errors.append(f"counts {registered}/{held} artwork {len(art)} image {len(images)}")
if errors:raise SystemExit("FAIL:\n"+"\n".join(errors))
print("PASS: batch016 20 candidates / 16 official-image successes / 12 registered / 8 held")
