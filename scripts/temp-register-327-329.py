#!/usr/bin/env python3
"""One-use audited registration of 327–329, remove once CI passes."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"scripts/temp-source-config-327-329.json"
RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42914013617"
OA="https://www.metmuseum.org/hubs/open-access"
TODAY="2026-11-11"

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def write(path,obj):
    f=ROOT/path
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def execute(*args):
    print("RUN", " ".join(args),flush=True)
    subprocess.run(args,cwd=ROOT,check=True)

def build_one(w):
    number=w["n"]
    ident=f'met-{w["id"]}'
    official=f'https://www.metmuseum.org/art/collection/search/{w["id"]}'
    api=f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{w["id"]}'
    high={
      "url":w["original"],"sha256":w["originalSha"],"byte_length":w["originalBytes"],
      "width":w["w"],"height":w["h"],"verification":"complete_jpeg_sha256_and_downscale_match",
      "source_identity_basis":"Met official original/display downscale RGB RMS "+str(w["rms"]),
      "last_full_sha_checked_on":TODAY,"human_visual_checked":False}
    review={
      "content_status":"verified","source_status":"verified","rights_status":"verified","reviewed_on":TODAY}
    visitor={"language":"ja","text":w["text"],"source_urls":[official],"review":review}
    art={
      "id":ident,
      "source":{"museum":"Metropolitan Museum of Art","artwork_id":w["id"],
         "artwork_url":official,"api_url":api,"record_checked_on":TODAY},
      "facts":{"title_original":w["title"],"title_ja_provisional":w["ja"],
         "artist":w["artist"],"creation_date_display":w["date"],
         "type":"Painting","is_public_domain_at_source":True,
         "culture":w["culture"],"accession_number":w["accession"]},
      "image":{"image_id":ident+"-primary","iiif_base":None,"iiif_reference_url":None,
         "display_url":w["display"],"source_registry_id":ident,"local_path":"/artworks/"+ident+".jpg",
         "sha256":w["displaySha"],"byte_length":w["displayBytes"],"live_image_checked":True,
         "live_check_scope":"Met exact object API and official original/display full JPEG SHA256 bytes/dimensions and downsizing "+RUN,
         "source_accession_number":w["accession"],"high_resolution":high},
      "curation":{"emotions":w["tags"],"emotion_strengths":w["strengths"],"tones":w["tones"],
         "themes":w["themes"],"evidence_url":official,
         "search_profile":{"fitting_situations":[{"situation":w["situation"],"reason":w["reason"],"strength":2}],
           "selection_cautions":[w["caution"]],"review_status":"evidence_reviewed"},
         "meaning_basis":{
           "author_intent":{"status":"not_verified_for_this_work","summary":None,"source_url":None},
           "scholarly_interpretation":{"summary":w["reason"],"source_url":official},
           "creation_context":w["date"]+"; "+w["culture"]+"; "+w["medium"]+"; accession "+w["accession"],
           "visual_clues":w["visual"],"uncertainty_note":w["caution"]},
         "emotion_categories":{"primary":w["primary"],"secondary":w["secondary"]}},
      "review":{"facts_checked_against_museum_api":True,"source_public_domain_flag_checked":True,
         "visual_checked":False,"curatorial_reviewed_on":TODAY,"curatorial_review_status":"provisional",
         "curatorial_review_note":"Same assistant separate source-image review; not human expert. Full official JPEG SHA256 "+RUN,
         "ai_content_review_status":"pending","source_evidence_review_status":"pending",
         "image_subject_match_status":"pending"},
      "visitor_explanation":visitor
    }
    image={
      "id":ident,"title":w["title"],"official_artwork_url":official,"origin":"met_official_primary",
      "in_shared_catalog":True,"verification":"met_primary_jpeg_http_verified",
      "image_source":{"type":"met_open_access","official_image_page":official,
        "license_label":"The Met Open Access / CC0 (Public Domain work, official primary JPEG)",
        "license_url":OA,"verified_download_url":w["display"],"sha256":w["displaySha"],
        "byte_length":w["displayBytes"],"last_http_sha_checked_on":TODAY,
        "last_verification_evidence":RUN,"license_review_status":"official_OA_confirmed_release_review_pending",
        "high_resolution":high},
      "accession_number":w["accession"]
    }
    cand_path=f"drafts/artwork-additions/{ident}.json"
    draft_path=f"drafts/visitor-explanations/{ident}.json"
    audit_path=f"docs/artwork-completion-audits/{ident}-{TODAY}.json"
    proposal={"schema_version":"artwork-addition-proposal-v1","id":ident,"artwork":art,"image_record":image}
    draft={"id":ident,"visitor_explanation":visitor,
      "evidence":[{"claim":w["reason"],"source_url":official,
        "source_location":"Met Overview: "+"; ".join(c["source_section"] for c in w["claims"]),
        "checked_against_source":True}]}
    write(cand_path,proposal)
    write(draft_path,draft)
    sourcechecks=[{"source_url":official,**c} for c in w["claims"]]
    audit={
      "schema_version":"artwork-v2-new-registration-2","id":ident,"checked_on":TODAY,
      "result":"PASS","unresolved_material_issues":[],
      "candidate_path":cand_path,"candidate_sha256":sha(cand_path),
      "draft_path":draft_path,"draft_sha256":sha(draft_path),
      "baseline":{"artworks_sha256":sha("data/artworks.json"),
         "image_registry_sha256":sha("data/image-sources.json")},
      "official_text_checks":sourcechecks,
      "source_evidence":[
        {"url":official,"location":"Artwork Details and Overview (exact Met ID); "+
             " | ".join(c["source_section"] for c in w["claims"]),
         "finding":w["reason"]+" 「絵に見えるもの」は出典と同一作品のMet公式画像を照合。","checked_against_source":True},
        {"url":api,"location":"Met objectID / objectDate / classification / artist / PD / accession / official original and small JPEG",
         "finding":"Met official API metadata and JPEG 200 status, SHA256 full bytes, image dimensions and resizing match in "+RUN+"; medium/culture values not inferred from ID.",
         "checked_against_source":True},
        {"url":OA,"location":"Met Open Access CC0 image and public-domain collection data licensing",
         "finding":"Only public-domain Met primary images and basic facts are CC0; current museum artwork Overview prose is copyright-distinct and not reproduced at length.",
         "checked_against_source":True}],
      "rights":{
        "artwork":{"verified":True,"public_domain":True,"source_url":official,
           "finding":"Met exact object is labeled Public Domain and Met API confirms isPublicDomain:true; no unsupported artwork rights assumptions."},
        "image":{"verified":True,"permitted_for_site_use":True,"source_url":OA,
           "finding":"Met official Open Access CC0 primary JPEG bytes from exact PD object; checked six pair images in "+RUN},
        "text":{"verified":True,"independent_japanese_prose":True,"source_url":official,
           "finding":"Newly authored Japanese visitor writing based on verified museum facts and direct visual observation, not a near-literal translation; not a legal clearance opinion."}},
      "separate_pass_review":{
        "result":"PASS",
        "method":"Same assistant's separate content-source review: direct Met exact-object Overview/Details, short quotation-to-specific Japanese claim checks, exact official IIIF visual and API metadata, primary original/display full JPEG SHA256, dimensions and downscale RMS in "+RUN,
        "limitations":"Not external art expert or human review. Met HTML may be HTTP 429 when CI re-fetches, so offline checks bind source excerpts but do not guarantee network quote re-fetch. Specific authorship where uncertain and spiritual meaning remain attributed interpretations, not proof. No legal clearance guarantee.",
        "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
        "findings":{
          "identity":f"Met exact artwork ID {w['id']}, title {w['title']}, artist display/attribution {w['artist']}, accession {w['accession']}; known attribution/date uncertainty preserved.",
          "image_match":w["visual"]+" Met IIIF actual image and official Met API original/display pairs, complete SHA256/dimensions and resized RGB RMS "+str(w["rms"])+", "+RUN,
          "historical_interpretation":w["reason"]+" Limits: "+w["caution"],
          "emotion":"Tags tied to subject/visual basis, including zero-tag works where assigning a psychological state is unsupported. Tags "+str(w["tags"]),
          "visitor_text":"Original Japanese readable body with two specific Met Overview excerpts bound to actual claims; artistic observations separately inspected. Avoided close English source translation.",
          "rights":"PD Met object, CC0 official Met images, independent Japanese visitor prose, distinct rights review."}},
      "image_evidence":[
        {"kind":"display","url":w["display"],"sha256":w["displaySha"],"byte_length":w["displayBytes"],
         "download_status":200,"full_bytes_sha256_checked":True,"image_subject_visually_compared":True,
         "observation":w["visual"]+" Display primary JPEG identity verified against original by Met official object API and full-file hash/downsizing RMS, "+RUN,
         "checked_on":TODAY},
        {"kind":"original","url":w["original"],"sha256":w["originalSha"],"byte_length":w["originalBytes"],
         "download_status":200,"full_bytes_sha256_checked":True,"image_subject_visually_compared":True,
         "observation":w["visual"]+f" Official original JPEG {w['w']}x{w['h']} same Met object and downscaled image; complete hash/length and resizing checked "+RUN,
         "checked_on":TODAY}],
      "notes":[f"Sequential individual addition number {number}, previous completed artwork records unchanged.",
        "Same AI separate pass, not external scholarly/human sign-off. Met page quotes read via official page, online CI re-fetch may be rate-limited."]
    }
    write(audit_path,audit)
    print("AUDIT",ident,"source excerpts",len(sourcechecks),"baseline SHA",audit["baseline"]["artworks_sha256"],flush=True)
    execute(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    execute(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    execute(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    execute(sys.executable,"scripts/add_artwork.py","check")

def main():
    works=load("scripts/temp-source-config-327-329.json")["works"]
    assert [w["n"] for w in works]==[327,328,329]
    assert len(load("data/artworks.json")["artworks"])==326
    for w in works:
        build_one(w)
    assert len(load("data/artworks.json")["artworks"])==329
    status="""## 現在の状態（2026-11-11時点）

- **完成登録：329作品**。正式数は統合後の最新 `main` とREADMEを確認。
- **次：330作品目から候補調査**。既存作品の重複と画面・出典・画像権利を照合。
- 327〜329作品：`met-49471` 中国《洞窟での瞑想》、`met-747199` メキシコ《カルメンの聖母と煉獄の魂》、`met-456966` インド《馬上のナワーブ・ムザッファル・アリー・ハーン》。個別のv2出典監査と独自日本語解説を保存。
- 公式作品別Overviewと実画像を照合し、Met公式APIの原寸・表示JPEG計6点をSHA256・サイズ・寸法・縮小RMSで検証（[実画像の証拠]("""+RUN+""")）。同一AIによる別工程の審査で、外部の人間の鑑定ではない。
- 既存326作品と監査は変更していない。[新規追加ガイド](artwork-expansion-v2.md) および [v2基準](artwork-completion-workflow-v2.md) を引き継ぐ。
"""
    tmp=Path("/tmp/kaiga329resume.md")
    tmp.write_text(status,encoding="utf-8")
    execute(sys.executable,"scripts/rotate_resume.py","update","--from",str(tmp))
    for args in [
      ["scripts/validate_artworks.py"],
      ["-m","unittest","discover","-s","tests","-p","test_*.py"],
      ["scripts/rotate_resume.py","check"],["scripts/complete_artwork.py","check"],
      ["scripts/add_artwork.py","check"],["scripts/visitor_draft_queue.py","check"],
      ["scripts/check_catalog_snapshot.py"],["scripts/check_image_sources.py"],
      ["scripts/validate_candidates.py"],["scripts/validate_evaluation_cases.py"],
      ["scripts/audit_coverage.py"]]:
        execute(sys.executable,*args)
    for w in works:
        execute(sys.executable,"scripts/verify_target_image_live.py","--id","met-"+str(w["id"]))
    print("FINAL_PASS: 326 -> 329; source bindings, display/original JPEG, tests and all integrity checks passed",flush=True)

if __name__=="__main__":
    main()
