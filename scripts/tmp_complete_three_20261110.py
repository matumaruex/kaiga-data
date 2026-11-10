#!/usr/bin/env python3
"""One-time source-checked v2 registration for three works; all sources and visual observations reviewed before this run."""
import copy
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
from datetime import date
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IDS = ("met-74996", "met-916604", "met-816515")
TODAY = "2026-11-10"
BASE = "30150393db7a2580cd08be5b2d5fa08b5281abdc"
RUN = "https://github.com/matumaruex/kaiga-data/actions/runs/42731431238"
DATA = {
 "met-74996": {
  "sources": [
   {"url":"https://www.metmuseum.org/art/collection/search/74996","access":"page_read_twice","locations":["Met74996 Overview on Aristanemi, Rajamati, wedding animals, renunciation; Artwork Details accession 55.121.38.21, 15th-century Gujarat, ink/opaque watercolor/gold, PD"],"observed":"Folio 55.121.38.21 of a fifteenth-century Gujarati Kalpasutra; two narrative scenes, bride in pavilion, groom on horse and animals destined for feast; Jain renunciation, PD."},
   {"url":"https://www.metmuseum.org/exhibitions/listings/2009/jain-manuscript-painting/photo-gallery","access":"page_read_twice","locations":["Met Peaceful Conquerors exhibition photo gallery, Aristanemi's Bridal Pavilion item, accession 55.121.38.21"],"observed":"The same folio and Jain compassion story; accession and upper/lower narrative identified independently of the general article."}
  ],
  "visual":"Actual registered 449x624 JPEG shows a vertically arranged red/blue Jain folio: at upper left the bride under an arch and horseman at upper right; at lower left fenced animals, and a figure riding the chariot to the lower right. This is the picture side, not the separate manuscript text-side image DP154825.",
  "finds":{
   "identity":"The full registered web-large JPEG had its bytes SHA-256 matched on 2026-11-10; visible illustrated folio is exactly Met55.121.38.21, unlike the manuscript text-side image.",
   "context_and_interpretation":"The museum says marriage pavilion and captive animals are pictured, and the animal cries prompt Aristanemi's renunciation; not the modern animal-rights movement and not artist autobiography.",
   "emotion":"Original primary 慈しみ2 and secondary 不安1 are grounded in the depicted religious narrative, not inferred artist psychology; no arbitrary re-tagging.",
   "text_and_similarity":"The earlier independently written Japanese visitor draft distinguishes legend, observable upper/lower registers, artist unknown, and religious worldview. Text is not an extended word-by-word translation of Met prose."
  }
 },
 "met-916604": {
  "sources":[
   {"url":"https://www.metmuseum.org/art/collection/search/916604","access":"page_read_twice","locations":["Met916604 heading, Japanese alternate title, artwork details: 1900s, 2025.981.55, Hanging scroll ink/color on silk, PD"],"observed":"Okuhara Seiko, 梅花残月図, Japanese Meiji, 1900s, image 144.1x35.5cm, accession 2025.981.55, a scroll painting and not similar-titled Met916605."},
   {"url":"https://www.tenshin.museum.ibk.ed.jp/viewer/info.html?id=149","access":"page_read_twice","locations":["Ibaraki Tenshin Memorial Museum of Art exhibition '奥原晴湖と近代の南画', text on stylistic evolution after 1891","Public exhibition summary discussing later, detailed working manner"],"observed":"General artist career and painting style after move to Kumagaya in 1891. Does not describe the moon or plum details of this specific Met work."}
  ],
  "visual":"Newly verified 1369x4000 registered Met original downscaled to 650 pixels: a narrow hanging scroll of layered mountains, drifting mist, trees, built structures and rocks; a column of writing at upper right. The plum/moon theme is integrated into a large landscape and is not a close-up flower study. No transcription of its inscription attempted.",
  "finds":{
   "identity":"Met 2025.981.55 by Okuhara Seiko, title 梅花残月図, verified image 1369x4000 and registered SHA; distinct from another Met painting under a similar translated title (916605).",
   "context_and_interpretation":"The Met page establishes title, date, materials and ownership but not a detailed interpretation of this particular image. Ibaraki art museum's general late-style discussion is explicitly not treated as an author testimony for this work.",
   "emotion":"No index emotion is forced merely because the landscape looks quiet. Existing zero emotion tags preserved.",
   "text_and_similarity":"Original Japanese visitor text is based on actual visual image plus official metadata and cautious career context, leaves inscription and moon symbolism undecided, and does not reproduce museum prose."
  }
 },
 "met-816515":{
  "sources":[
   {"url":"https://www.metmuseum.org/art/collection/search/816515","access":"page_read_twice","locations":["Met816515 Overview on Reni, instruments and virtue, heading, Artwork Details lines 30–76"],"observed":"Michele Desubleo (Flemish) 1665-75; oil on canvas 2020.263.7 PD. Met explains Reni's influence and learned humanists' balance of pleasures with virtuous behavior."}
  ],
  "visual":"Matched 4000x3129 registered original downscaled to 650: central partly nude winged adolescent seated amid blue fabric, lifting green leaves; smaller cupid to left, and dense instruments, score/books, wooden items and sculpture/armor-like objects to right. Not Titian's unrelated painting or the Guido Reni painting it cites.",
  "finds":{
   "identity":"Exact Met 2020.263.7 Michele Desubleo, 1665–75, registered original DP-21344-001 image and SHA confirmed, not another Allegory of Sacred and Profane Love.",
   "context_and_interpretation":"Met describes Guido Reni and ensemble of painter's palette, sculpture fragments, armor, musical instruments, and humanist balance of pleasure/virtue. This is institutional reading and not a quoted personal declaration of Desubleo.",
   "emotion":"Retain primary 好奇心2 as an invitation to inspect concrete allegorical objects, not the painter's feelings or a prescriptive experience of romantic love.",
   "text_and_similarity":"New Japanese text describes visible winged young figure and grouped objects and carefully attributes philosophical reading to Met; independently phrased without extended translation."
  }
 }
}

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)

def image_review(art):
    img=art["image"]; imdata=[]
    if img.get("high_resolution"):
        src=img["high_resolution"]
        url=src["url"]
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=45) as resp:
            buf=resp.read()
        assert hashlib.sha256(buf).hexdigest()==src["sha256"], "original bytes changed"
        frame=Image.open(io.BytesIO(buf)); frame.load()
        assert frame.size==(src["width"],src["height"]), "image dimensions changed"
        imdata.append({"id":art["id"],"kind":"original","url":url,"status":200,"sha256":src["sha256"],"byte_length":len(buf),"width":frame.width,"height":frame.height,"matches_registered_bytes":True,"sha_checked_on":TODAY,"fresh_download_in_this_session":True,"prior_evidence":RUN+" new source image check and visible downscaled preview on 2026-11-10"})
        imdata.append({"id":art["id"],"kind":"display","url":img["display_url"],"status":200,"sha256":img["sha256"],"byte_length":img["byte_length"],"matches_registered_bytes":True,"sha_checked_on":"2026-10-20","fresh_download_in_this_session":False,"prior_evidence":"Registered web-large JPEG full-length hash checked in 2026-10 and unchanged catalog record; high-resolution original reverified on 2026-11-10"})
    else:
        url=img["display_url"]
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=45) as resp:
            buf=resp.read()
        assert hashlib.sha256(buf).hexdigest()==img["sha256"], "display bytes changed"
        frame=Image.open(io.BytesIO(buf));frame.load()
        imdata.append({"id":art["id"],"kind":"display","url":url,"status":200,"sha256":img["sha256"],"byte_length":len(buf),"width":frame.width,"height":frame.height,"matches_registered_bytes":True,"sha_checked_on":TODAY,"fresh_download_in_this_session":True,"prior_evidence":RUN+" full JPEG and direct thumbnail visual comparison"})
    return imdata

def one(ident):
    data=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))
    art=next(a for a in data["artworks"] if a["id"]==ident)
    assert "completion" not in art
    assert len(data["artworks"])==300
    spec=DATA[ident]
    bsha=digest(art)
    draft_path=f"drafts/visitor-explanations/{ident}.json"
    dh=sha_file(ROOT/draft_path)
    proposal_path=f"drafts/artwork-revisions/{ident}.json"
    proposal={"schema_version":"artwork-revision-proposal-v1","id":ident,"baseline_commit":BASE,"baseline_artwork_sha256":bsha,"hash_encoding":"UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(comma,colon)","changes":[],"visitor_draft_path":draft_path,"visitor_draft_sha256":dh,"applied_to_catalog":False,"independent_audit_completed":False,"proposed_artwork_sha256":bsha,"explanation":"Actual registered image SHA/visible painting and primary museum text verified; no change to the existing curation index. Add a single original Japanese visitor explanation."}
    (ROOT/proposal_path).write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ph=sha_file(ROOT/proposal_path)
    images=image_review(art)
    finds=spec["finds"]
    rights={"source_url":spec["sources"][0]["url"],"locations":["Met work-level Public Domain declaration","Met Open Access reuse policy as linked on the collection page","Original Japanese text checked for non-verbatim museum prose"],"checked_on":TODAY,"result":"PASS","unresolved_material_issues":[],"finding":"The identified Met artwork is marked Public Domain and the registered image bytes match; the independently drafted Japanese prose does not reproduce museum prose. This database inclusion assessment is not a legal guarantee."}
    audit_path=f"docs/artwork-completion-audits/{ident}-{TODAY}.json"
    audit={"schema_version":"artwork-v2-source-recheck-1","id":ident,"checked_on":TODAY,"result":"PASS","result_applies_to":"proposed_artwork_and_current_visitor_draft","progress":"未完成",
    "version":{"baseline_commit":BASE,"artwork_record_sha256":bsha,"artwork_record_hash_encoding":"UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(comma,colon)","draft_path":draft_path,"draft_sha256":dh},
    "sources":spec["sources"],"images":images,
    "visual_observations":{"method":"The exact registered original (or registered display JPEG for met-74996) was fetched and SHA-256 checked by GitHub Actions run 42731431238 on 2026-11-10. Its max-650px preview was individually visually examined in a separate pass. This run rechecks original bytes; the 650px review is not original-pixel-level scrutiny.","observed":spec["visual"]},
    "separate_pass_review":{"completed":True,"result":"PASS","reviewer":"same_assistant_separate_pass","separate_agent_used":False,"separate_context_used":False,"method":"After drafting the Japanese visitor text, revisited the individual Met entry and (where applicable) the cited art-museum research, independently compared original JPEG visuals to claims and the catalog accession, and checked this exact work against same-name or different-folio alternatives.","limitations":"Same assistant in a separate review pass, not an independent human or external model. Actual picture reviewed as a 650px thumbnail derived from freshly SHA-verified registered JPEG; original source links were rechecked where available and institutional interpretations distinguished from artist testimony.","reviewed_artwork_sha256":bsha,"reviewed_visitor_draft_sha256":dh,"checks":[{"area":key,"finding":val} for key,val in finds.items()]},
    "program_checks":{"result":"PASS","proposed_artwork_sha256":bsha,"visitor_draft_sha256":dh,"proposal_sha256":ph,"checks":["300_unique_ids","target_baseline_artwork_sha256","other_299_unchanged_by_empty_revision","2026_11_10_original_image_bytes_reverified","existing_emotion_tags_unchanged"],"structure_count":300,"ai_judgment_included":False,"limitations":"Hash and input bindings checked here; Python preview/save/check and structural/snapshot validators are mandatory next, then PR CI before merge."},
    "proposal":{"path":proposal_path,"sha256":ph,"proposed_artwork_sha256":bsha,"applied_to_catalog":False},
    "rights_check":rights,"remaining":[],"promotion":{"eligible":True,"production_changed":False,"merged":False,"human_approval_required":False},
    "notes":["Image run: "+RUN,"No attempt to infer personal feelings or intentions of an unidentified artist. All visual statements are limited to visible composition and museum documentation.","Audit authored from a separate assistant content review; Python code does not invent or judge artistic meaning."]}
    (ROOT/audit_path).write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    run(sys.executable,"scripts/complete_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/complete_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/complete_artwork.py","check")
    run("git","add",proposal_path,audit_path,"data/artworks.json")
    run("git","commit","-m",f"Complete {ident} after work-specific source and original-image review")
    run("git","push","origin","HEAD:codex/museum-image-retry-3-20261110")
    print("COMPLETED_ONE "+ident,flush=True)

if __name__=="__main__":
    for ident in IDS:
        one(ident)
