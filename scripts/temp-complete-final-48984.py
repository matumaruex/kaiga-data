#!/usr/bin/env python3
"""One-time source-checked v2 registration for final work; all sources and visual observations reviewed before this run."""
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
IDS = ("met-48984",)
TODAY = "2026-11-10"
BASE = "367a49736de9c8a9e4b999639a756507cfc6f886"
RUN = "https://github.com/matumaruex/kaiga-data/actions/runs/42735434769"
DATA = json.loads(r'''{"met-48984":{"sources":[{"url":"https://www.metmuseum.org/art/collection/search/48984","access":"page_read_twice","locations":["Met 48984 heading lines 28–40; Artwork Details lines 70–79; official Open Access link 99–102"],"observed":"Met currently calls it Old Man and Woman, Attributed to Ogata Kōrin (not proven original), Japanese Edo period; ink and color on silk hanging scroll, 29.8x41.9cm; Met17.118.117, Rogers Fund 1917, Public Domain. No individual painting-symbolism interpretation provided in published record."},{"url":"https://www.city.takasago.lg.jp/soshikikarasagasu/citypromotionshitsu/kanko_tokusan/2_1/3144.html","access":"page_read_twice","locations":["Takasago City '尉と姥伝説' updated 2026-02-20, lines 131–138 and story 153–165, paired mythical elderly cleaners with rake/broom under pine"],"observed":"The general Takasago tradition depicts 尉 and 姥 as symbolic elderly couple under pine, cleaning using rake and broom, emblem of marital harmony; this city's text does not identify or academically attribute Met48984."}],"visual":"Verified 2000x1500 source image downscaled to 800px shows two elderly people facing one another in patterned robes beneath large pine tree, a small face/figure peeking from behind trunk at upper left, round wicker basket or container, rake-like implement across foreground, long broom-like twig at far right. Individual figure identities and purpose of implements cannot be asserted; compositional resemblance to traditional 尉/姥 iconography is a comparison, not a verified painting-specific identification.","finds":{"identity":"Met48984, accession 17.118.117, original source file DP260447 2000x1500 SHA-256 ce690d548fea328fadd92718042b3837555e1ed1ea1bc522639af4cbb0e700ae, catalog SHA matches; current Met's 'Attributed to' is preserved, author not certified.","context_and_interpretation":"Met gives no dedicated scholarly meaning paragraph. Elderly figures, pine and cleaning implements may suggest Japanese Takasago 尉/姥 motif, whose general significance is documented by Takasago City, but museum has not identified this exact work as Takasago; artwork-specific conclusion held uncertain.","emotion":"Zero primary and secondary emotions are retained; the motif's possible marital harmony is an iconographic subject and not evidence viewer must feel ease or painter's private emotion.","text_and_similarity":"New Japanese visitor text is independently worded, separates official museum facts from tentative motif, avoids inventing a date or author intent, notes small additional figure and implements as observations. Neither copyrighted Met explanation nor city narrative is reproduced extensively."},"revisions":[{"path":["curation","meaning_basis","scholarly_interpretation"],"after":{"summary":"Metの現行登録ページは尾形光琳への『帰属』、江戸時代、絹本墨彩の掛軸といった作品情報を掲げるが、主題に関する当該作品固有の専門的解説は確認できない。松の下に向き合う老人と老女、熊手や箒を思わせる道具は能『高砂』の尉・姥の一般図像と比較できる。ただし、これは画面と高砂伝承の照合による可能性にとどまり、この作品の主題が高砂だと確定する美術館の見解ではない。","source_url":"https://www.metmuseum.org/art/collection/search/48984"},"reason":"旧欄は制作背景と同文だった。作品固有の研究未確認と一般図像比較を別に記録する。","source_urls":["https://www.metmuseum.org/art/collection/search/48984","https://www.city.takasago.lg.jp/soshikikarasagasu/citypromotionshitsu/kanko_tokusan/2_1/3144.html"]},{"path":["curation","meaning_basis","creation_context"],"after":"日本の江戸時代に制作された絹本墨彩の掛軸。Met所蔵17.118.117、ロジャース基金で1917年に収蔵。所蔵館は『Attributed to Ogata Kōrin』として作者の帰属を未確定にし、個別の制作年を記していない。","reason":"旧欄が解釈文と同文だったため、制作・収蔵の確かな情報を独立記録する。","source_urls":["https://www.metmuseum.org/art/collection/search/48984"]},{"path":["curation","meaning_basis","visual_clues"],"after":"松の大きな幹と枝の下で老いた男女が向き合い、二人の近くに籠のような入れ物、熊手や箒のような細長い道具、幹の陰には小さな顔らしきものも見える。これらの図像を『高砂』に断定的には同定しない。","reason":"登録原画像の具体的な画面と未確定の図像識別を記録。","source_urls":["https://www.metmuseum.org/art/collection/search/48984","https://www.city.takasago.lg.jp/soshikikarasagasu/citypromotionshitsu/kanko_tokusan/2_1/3144.html"]},{"path":["curation","meaning_basis","uncertainty_note"],"after":"現行所蔵館の表示は尾形光琳に『帰属』する作品であり真筆とは確定していない。個別の制作年、人物が特定の実在の夫婦か、高砂の尉・姥に同定できるか、小さな姿の人物同定、作者自身の個別制作意図や感情は確認できない。高砂伝承との接点は一般図像との比較にとどまる。","reason":"作者帰属・画題・人物関係・作者心理の確実性を区別して記録。","source_urls":["https://www.metmuseum.org/art/collection/search/48984","https://www.city.takasago.lg.jp/soshikikarasagasu/citypromotionshitsu/kanko_tokusan/2_1/3144.html"]},{"path":["curation","search_profile","selection_cautions"],"after":["画家は『Attributed to Ogata Kōrin』であり、尾形光琳の真筆と断定しない。","松と男女・掃除道具から高砂の尉・姥を連想できるが、所蔵館の当該作品への正式な同定ではない。作者・画中人物・鑑賞者の感情を混同しない。"],"reason":"追加した一般図像比較が展示選定で確定事項に格上げされないよう注意を限定。","source_urls":["https://www.metmuseum.org/art/collection/search/48984","https://www.city.takasago.lg.jp/soshikikarasagasu/citypromotionshitsu/kanko_tokusan/2_1/3144.html"]}]}}''')

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
    if ident=="met-48984":
        assert art["facts"]["title_ja_provisional"]=="老夫婦（尾形光琳伝）"
        art["facts"]["title_ja_provisional"]="老人と老女（尾形光琳に帰属）"
        (ROOT/"data/artworks.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        run(sys.executable,"scripts/validate_artworks.py")
        run(sys.executable,"scripts/check_catalog_snapshot.py")
        run("git","add","data/artworks.json")
        run("git","commit","-m","Clarify Japanese Met48984 title without asserting marital relationship or firm artist attribution")
        run("git","push","origin","HEAD:codex/museum-complete-final-48984-20261110")
    bsha=digest(art)
    draft_path=f"drafts/visitor-explanations/{ident}.json"
    dh=sha_file(ROOT/draft_path)
    proposal_path=f"drafts/artwork-revisions/{ident}.json"
    changes=[]
    candidate=copy.deepcopy(art)
    for item in spec.get("revisions",[]):
        target=candidate
        for key in item["path"][:-1]: target=target[key]
        before=copy.deepcopy(target[item["path"][-1]])
        target[item["path"][-1]]=copy.deepcopy(item["after"])
        changes.append({"path":item["path"],"before":before,"after":item["after"],"reason":item["reason"],"source_urls":item["source_urls"]})
    psha=digest(candidate)
    current_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    proposal={"schema_version":"artwork-revision-proposal-v1","id":ident,"baseline_commit":current_commit,"baseline_artwork_sha256":bsha,"hash_encoding":"UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(comma,colon)","changes":changes,"visitor_draft_path":draft_path,"visitor_draft_sha256":dh,"applied_to_catalog":False,"independent_audit_completed":False,"proposed_artwork_sha256":psha,"explanation":"Actual registered image SHA/visible painting and primary museum text verified; a narrow evidence-backed curation correction when necessary. Add a single original Japanese visitor explanation."}
    (ROOT/proposal_path).write_text(json.dumps(proposal,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ph=sha_file(ROOT/proposal_path)
    images=image_review(art)
    finds=spec["finds"]
    rights={"source_url":spec["sources"][0]["url"],"locations":["Met work-level Public Domain declaration","Met Open Access reuse policy as linked on the collection page","Original Japanese text checked for non-verbatim museum prose"],"checked_on":TODAY,"result":"PASS","unresolved_material_issues":[],"finding":"The identified Met artwork is marked Public Domain and the registered image bytes match; the independently drafted Japanese prose does not reproduce museum prose. This database inclusion assessment is not a legal guarantee."}
    audit_path=f"docs/artwork-completion-audits/{ident}-{TODAY}.json"
    audit={"schema_version":"artwork-v2-source-recheck-1","id":ident,"checked_on":TODAY,"result":"PASS","result_applies_to":"proposed_artwork_and_current_visitor_draft","progress":"未完成",
    "version":{"baseline_commit":current_commit,"artwork_record_sha256":bsha,"artwork_record_hash_encoding":"UTF-8 JSON, ensure_ascii=False, sort_keys=True, separators=(comma,colon)","draft_path":draft_path,"draft_sha256":dh},
    "sources":spec["sources"],"images":images,
    "visual_observations":{"method":"The exact registered original () was fetched and SHA-256 checked by GitHub Actions run 42735434769 on 2026-11-10. Its max-800px preview was individually visually examined in a separate pass. This run rechecks original bytes; the 800px review is not original-pixel-level scrutiny.","observed":spec["visual"]},
    "separate_pass_review":{"completed":True,"result":"PASS","reviewer":"same_assistant_separate_pass","separate_agent_used":False,"separate_context_used":False,"method":"After drafting the Japanese visitor text, revisited the individual Met entry and (where applicable) the cited art-museum research, independently compared original JPEG visuals to claims and the catalog accession, and checked this exact work against same-name or different-folio alternatives.","limitations":"Same assistant in a separate review pass, not an independent human or external model. Actual picture reviewed as an 800px thumbnail derived from freshly SHA-verified registered JPEG; original source links were rechecked where available and institutional interpretations distinguished from artist testimony.","reviewed_artwork_sha256":psha,"reviewed_visitor_draft_sha256":dh,"checks":[{"area":key,"finding":val} for key,val in finds.items()]},
    "program_checks":{"result":"PASS","proposed_artwork_sha256":psha,"visitor_draft_sha256":dh,"proposal_sha256":ph,"checks":["300_unique_ids","target_baseline_artwork_sha256","other_299_unchanged_by_scoped_revision","2026_11_10_original_image_bytes_reverified","existing_emotion_tags_unchanged"],"structure_count":300,"ai_judgment_included":False,"limitations":"Hash and input bindings checked here; Python preview/save/check and structural/snapshot validators are mandatory next, then PR CI before merge."},
    "proposal":{"path":proposal_path,"sha256":ph,"proposed_artwork_sha256":psha,"applied_to_catalog":False},
    "rights_check":rights,"remaining":[],"promotion":{"eligible":True,"production_changed":False,"merged":False,"human_approval_required":False},
    "notes":["Image run: "+RUN,"No attempt to infer a painter\u0027s personal feelings from iconography or topic. All visual statements are limited to visible composition and museum documentation.","Audit authored from a separate assistant content review; Python code does not invent or judge artistic meaning."]}
    (ROOT/audit_path).write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    run(sys.executable,"scripts/complete_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/complete_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/complete_artwork.py","check")
    run("git","add",proposal_path,audit_path,"data/artworks.json")
    run("git","commit","-m",f"Complete {ident} after work-specific source and original-image review")
    run("git","push","origin","HEAD:codex/museum-complete-final-48984-20261110")
    print("COMPLETED_ONE "+ident,flush=True)

if __name__=="__main__":
    for ident in IDS:
        one(ident)
