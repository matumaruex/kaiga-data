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
IDS = ("met-45697", "met-670921", "met-436680")
TODAY = "2026-11-10"
BASE = "85b3e71aca1675309b702936a4ae730eb3829dd8"
RUN = "https://github.com/matumaruex/kaiga-data/actions/runs/42733477884"
DATA = json.loads(r'''{"met-45697":{"sources":[{"url":"https://www.metmuseum.org/art/collection/search/45697","access":"page_read_twice","locations":["Met45697 heading and Artwork Details lines 28–38, 67–77"],"observed":"Isei (Japan mid-16th century), Chinese Children at Play, 29.100.451, framed ink and color on paper, PD. No individual symbolic research stated."},{"url":"https://www.metmuseum.org/art/collection/search/45696","access":"page_read_twice","locations":["Met45696 heading/details showing no.29.100.450"],"observed":"Different same-titled painting by Isei; different Met accession and dimensions."}],"visual":"The matching original shows a tall brown-ground framed work with five Chinese-costumed children and several play objects including a small animal at lower left, a horse-shaped toy at right. Actual SHA-confirmed JPEG was viewed as 720px thumbnail; no specific game names inferred.","finds":{"identity":"Met 29.100.451 exact match; same-name 29.100.450 is distinct; original JPEG SHA verified.","context_and_interpretation":"Museum verifies mid-sixteenth-century Japanese origin and Chinese subject, but not detailed child-game names or allegory. Scholarly interpretation is limited accordingly.","emotion":"Original primary 喜び2 matches concrete play motif, not claimed artist emotion.","text_and_similarity":"Independent Japanese prose based on official metadata and observed image, no lengthy copying; distinguishes same-name works."},"revisions":[{"path":["curation","meaning_basis","scholarly_interpretation"],"after":{"summary":"Metは伊勢（Isei）の中国風の子どもの遊戯画と同定するが、個々の遊びの名前や象徴について作品固有の専門解説は確認できない。現画面に唐子が遊び道具の周囲に集まる姿が見えることと、社会的意味の専門的解釈とは区別する。","source_url":"https://www.metmuseum.org/art/collection/search/45697"},"reason":"旧解釈が制作背景と同文。研究未確認範囲を明示する。","source_urls":["https://www.metmuseum.org/art/collection/search/45697"]},{"path":["curation","meaning_basis","creation_context"],"after":"室町時代、16世紀半ばの日本で伊勢（Isei）が紙に墨と彩色で描いた額装絵画。Metには同作者・同題だが別作品29.100.450もあり、本作は29.100.451。","reason":"時代・制作形式・異版識別を記録。","source_urls":["https://www.metmuseum.org/art/collection/search/45697","https://www.metmuseum.org/art/collection/search/45696"]},{"path":["curation","meaning_basis","visual_clues"],"after":"褐色の画面に集まる唐子、異なる衣装や身振り、馬形の遊具や小動物のような姿。特定の遊戯名は確認できない。","reason":"現物JPEG目視の固有観察。","source_urls":["https://www.metmuseum.org/art/collection/search/45697"]}]},"met-670921":{"sources":[{"url":"https://www.metmuseum.org/art/collection/search/670921","access":"page_read_twice","locations":["Met670921 object heading and Artwork Details lines 36–46, 67–79"],"observed":"Okada Hankō, Farewell Gift to Tani Bunji, 1833, accession 2015.300.179, ink/color paper hanging scroll, PD."},{"url":"https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf","access":"page_read_twice","locations":["Nakamura 19K23006 research report section 4 extracted lines 191–195; PDF screenshot unavailable, extracted text checked"],"observed":"Research expressly names 岡田半江筆『谷文二先生送別画』 (Farewell Gift to Tani Bunji), Met, 1833, discussing late Edo farewell landscapes and ideal/reality."},{"url":"https://www.tv-tokyo.co.jp/kantei/smp/kaiun_db/otakara/20140401/07.html","access":"page_read_twice","locations":["TV Tokyo 2014/04/01 article 鑑定士総評"],"observed":"谷文二 is son of 谷文晁, not the same painter. Identity support only, not this work's interpretation."}],"visual":"Original matching 4000x3002 JPEG reviewed as 720px image: horizontally oriented literati landscape painted on a patterned scroll mounting, poem/inscription on upper left, houses among woods, buildings and watercourse leading to pagoda at upper right. Written text not fully deciphered.","finds":{"identity":"Met2015.300.179 is addressed to 谷文二 (Tani Bunji), not 谷文晁 (Tani Buncho); original Japanese title was wrong and requires a separately versioned fact correction.","context_and_interpretation":"Osaka University KAKENHI report explicitly treats this exact 1833 farewell work as an example of late-Edo literati farewell painting in a lineage of ideal and real. No evidence for artist's inner sorrow or real landscape location.","emotion":"Existing zero emotion tags justified; farewell topic not sufficient to attribute sorrow.","text_and_similarity":"New original Japanese interpretation distinguishes recipient and father, identifies visible inscription/landscape but does not invent translation."},"revisions":[{"path":["curation","meaning_basis","scholarly_interpretation"],"after":{"summary":"中村真菜美の江戸時代の送別画研究報告は、岡田半江筆《谷文二先生送別画》（1833年、Met蔵）を挙げ、送別画における理想化された画面と現実の出来事の関係を考察する作例の一つに位置づける。作者の直接証言やその日に描いた実景の証明ではない。","source_url":"https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf"},"reason":"制作背景と同文だった専門解釈を研究報告で置換。","source_urls":["https://www.metmuseum.org/art/collection/search/670921","https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf"]},{"path":["curation","meaning_basis","creation_context"],"after":"1833年、岡田半江が谷文二（Tani Bunji）に贈った送別の紙本墨彩掛軸（Met2015.300.179）。谷文二は谷文晁とは別人で文晁の息子。送別宴の実際の様子をこの絵がそのまま記録したとは限らない。","reason":"誤っていた受け手の同定と背景を訂正。","source_urls":["https://www.metmuseum.org/art/collection/search/670921","https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf","https://www.tv-tokyo.co.jp/kantei/smp/kaiun_db/otakara/20140401/07.html"]},{"path":["curation","meaning_basis","visual_clues"],"after":"横長の山水画面の左上に詩文や落款と見られる文字群。建物群、木々、水辺、右奥の塔を描く。地名・詩文全文の同定は未実施。","reason":"2026-11-10実画像を照合し画面固有の観察点を整理。","source_urls":["https://www.metmuseum.org/art/collection/search/670921"]},{"path":["curation","search_profile","fitting_situations"],"after":[{"situation":"江戸の画家の交流と送別の文化に触れたい","reason":"1833年の岡田半江による谷文二宛ての送別山水画。詩文と山水の組合せが文人の交遊を考える入口となる。","strength":1}],"reason":"谷文晁と谷文二の取り違えを防止。","source_urls":["https://www.metmuseum.org/art/collection/search/670921","https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf"]},{"path":["curation","meaning_basis","uncertainty_note"],"after":"送別の史実と画家自身の悲嘆・未練は区別する。描かれた実在の場所、詩文の全文、具体的な送別会の状況、作者の個別意図を直接示す資料は今回は確認できない。谷文二は谷文晁と別人。","reason":"直接裏付けできない部分を明示。","source_urls":["https://www.metmuseum.org/art/collection/search/670921","https://kaken.nii.ac.jp/en/file/KAKENHI-PROJECT-19K23006/19K23006seika.pdf"]}]},"met-436680":{"sources":[{"url":"https://www.metmuseum.org/art/collection/search/436680","access":"page_read_twice","locations":["Met436680 heading and Overview lines 28–39, Details lines 68–76"],"observed":"Samuel van Hoogstraten ca.1670, Met1992.133, angel foretells Mary's death, Catholic private devotion; artist Protestant, PD."},{"url":"https://www.metmuseum.org/ja/essays/michiel-sweerts-and-biblical-subjects-in-dutch-art","access":"page_read_twice","locations":["Met art historical essay about Catholic devotional pictures, mention 1992.133"],"observed":"Painting identified as a Catholic private devotional object; supports Met-specific interpretation."}],"visual":"The matching original shows Virgin kneeling at lower right with hands crossed over her chest and a winged angel at upper left amid dark clouds holding a long palm-like branch. Viewed 720px derivative of the registered hash-matched 2999x3721 original.","finds":{"identity":"Exact Met1992.133, original SHA matches and angel/Marian scene seen.","context_and_interpretation":"Met's specific rare death-announcement reading and Catholic private devotion supported, unlike ordinary Incarnation Annunciation; artist religious denomination distinct from intended patron.","emotion":"No emotion tags in catalog, left unchanged rather than reading grief from death scene.","text_and_similarity":"Japanese text original, does not quote long Met paragraphs and clearly attributes museum's interpretation."},"revisions":[]}}''')

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
    if ident=="met-670921":
        assert art["facts"]["title_ja_provisional"]=="谷文晁への送別の贈り物"
        art["facts"]["title_ja_provisional"]="谷文二先生送別画"
        (ROOT/"data/artworks.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        run(sys.executable,"scripts/validate_artworks.py")
        run(sys.executable,"scripts/check_catalog_snapshot.py")
        run("git","add","data/artworks.json")
        run("git","commit","-m","Correct farewell gift recipient from Tani Buncho to Tani Bunji")
        run("git","push","origin","HEAD:codex/museum-complete-next3-20261110")
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
    "visual_observations":{"method":"The exact registered original (or registered display JPEG for met-74996) was fetched and SHA-256 checked by GitHub Actions run 42733477884 on 2026-11-10. Its max-650px preview was individually visually examined in a separate pass. This run rechecks original bytes; the 650px review is not original-pixel-level scrutiny.","observed":spec["visual"]},
    "separate_pass_review":{"completed":True,"result":"PASS","reviewer":"same_assistant_separate_pass","separate_agent_used":False,"separate_context_used":False,"method":"After drafting the Japanese visitor text, revisited the individual Met entry and (where applicable) the cited art-museum research, independently compared original JPEG visuals to claims and the catalog accession, and checked this exact work against same-name or different-folio alternatives.","limitations":"Same assistant in a separate review pass, not an independent human or external model. Actual picture reviewed as a 650px thumbnail derived from freshly SHA-verified registered JPEG; original source links were rechecked where available and institutional interpretations distinguished from artist testimony.","reviewed_artwork_sha256":psha,"reviewed_visitor_draft_sha256":dh,"checks":[{"area":key,"finding":val} for key,val in finds.items()]},
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
    run("git","push","origin","HEAD:codex/museum-complete-next3-20261110")
    print("COMPLETED_ONE "+ident,flush=True)

if __name__=="__main__":
    for ident in IDS:
        one(ident)
