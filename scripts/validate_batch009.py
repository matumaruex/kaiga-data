#!/usr/bin/env python3
"""第9群の候補18点と試験登録13点、ハッシュ・権利・保留状態の整合検証。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

arts = {x["id"]: x for x in read("data/artworks.json")["artworks"]}
img = {x["id"]: x for x in read("data/image-sources.json")["records"]}
candidates = read("data/candidates-batch-009.json")["works"]
checks = {x["id"]: x for x in read("docs/batch009-online-result.json")["results"]}
problems = []
seen = set()
added = 0
for item in candidates:
    ident = item["candidate_id"]
    if ident in seen:
        problems.append(f"{ident}: duplicate candidate")
    seen.add(ident)
    check = checks.get(ident)
    if not check:
        problems.append(f"{ident}: no online research result")
        continue
    reg_status = item["registration_status"]
    if reg_status == "registered_provisional":
        added += 1
        work, source = arts.get(ident), img.get(ident)
        if not work or not source:
            problems.append(f"{ident}: missing catalog or image record")
            continue
        digest = check.get("image_sha256")
        if not all((check.get("museum_record_verified"),check.get("image_verified"),
                    item.get("official_api_live_checked"),item.get("actual_image_download_verified"))):
            problems.append(f"{ident}: falsely registered without API/JPEG")
        if item.get("image_sha256") != digest or work["image"]["sha256"] != digest or source["image_source"].get("sha256") != digest:
            problems.append(f"{ident}: image hash inconsistent")
        if source["image_source"].get("verified_download_url") != check.get("image_url_verified"):
            problems.append(f"{ident}: source URL and verified primary image differ")
        if work["image"]["display_url"] != check.get("image_url_verified"):
            problems.append(f"{ident}: catalog display image does not match")
        if check.get("isPublicDomain") is not True or work["facts"]["is_public_domain_at_source"] is not True:
            problems.append(f"{ident}: non-open-access work promoted")
    elif reg_status.startswith("held_"):
        if ident in arts or ident in img:
            problems.append(f"{ident}: held work promoted")
        if ident == "met-771516" and check.get("isPublicDomain") is not False:
            problems.append("PD false hold has inconsistent official flag")
        if item.get("image_sha256") != check.get("image_sha256"):
            problems.append(f"{ident}: candidate held image digest mismatch")
    else:
        problems.append(f"{ident}: unknown review status")
if len(candidates) != 18 or len(seen) != 18 or added != 13 or len(arts) < 83:
    problems.append(f"unexpected counts: {len(candidates)} candidates, {added} registered, {len(arts)} artworks")
if problems:
    print("FAIL", *problems, sep=chr(10) + "- ")
    raise SystemExit(1)
print(f"PASS: {len(arts)} registered, 18 batch009 candidates, 13 added, 5 held; SHA256 and rights aligned.")
print("Human visual inspection, author intent and publication review are separate.")
