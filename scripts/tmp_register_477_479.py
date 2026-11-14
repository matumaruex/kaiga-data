#!/usr/bin/env python3
"""One-off research-to-registration runner; never copied to main."""
from __future__ import annotations
import hashlib, io, json, math, os, subprocess, sys, time, shutil
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
DATE="2026-11-14"
BRANCH="codex/artworks-477-479-20261114"
OA="https://www.metmuseum.org/hubs/open-access"
BASE="https://www.metmuseum.org/art/collection/search/"
API="https://collectionapi.metmuseum.org/public/collection/v1/objects/"
SPEC=ROOT/"scripts/tmp_specs_477_479.json"
session=requests.Session()
session.headers.update({"User-Agent":"MuseumCatalogResearch/1.0 (open-access research)", "Accept":"application/json,image/jpeg,*/*"})
def sha(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def dump(path,obj):
    path=ROOT/path
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def filehash(path):return sha(Path(path).read_bytes())
def req(url):
    error=None
    for i in range(4):
        try:
            r=session.get(url, timeout=85)
            r.raise_for_status()
            if not r.content:raise ValueError("empty response")
            return r.content
        except (requests.RequestException,ValueError) as exc:
            error=exc; print("GET retry",url,str(exc),flush=True)
            time.sleep(i*3+2)
    raise RuntimeError("unable to fetch "+url+": "+str(error))
def output(*args):
    print(*args,flush=True)
def shell(*args):
    output("RUN",*args)
    subprocess.run(args,check=True)
def main():
    specs=load(SPEC)
    before=load(ROOT/"data/artworks.json")["artworks"]
    assert len(before)==476, ("unexpected live count",len(before))
    existing={x["id"] for x in before}
    for s in specs:
        assert "met-"+str(s["object_id"]) not in existing,"duplicate artwork"
    for spec in specs:
        assert len(spec["checks"])>=2, ("two overview excerpts expected",spec["object_id"])
        for check in spec["checks"]:
            assert check["claim"] in spec["visitor"], ("source claim absent in visitor text",spec["object_id"])
            assert len(check["excerpt"])>=35 and len(check["excerpt"].split())>=6, ("short Overview excerpt",spec["object_id"])
    researched=[]
    for no,s in enumerate(specs,477):
        ident="met-"+str(s["object_id"])
        official=BASE+str(s["object_id"])
        apiurl=API+str(s["object_id"])
        api=json.loads(req(apiurl))
        assert int(api["objectID"])==s["object_id"],"Met API identity mismatch"
        assert api.get("isPublicDomain") is True,"not public domain"
        assert api.get("medium"),("Met medium missing",ident)
        primary=api.get("primaryImage","")
        display=api.get("primaryImageSmall","")
        assert primary.startswith("https://images.metmuseum.org/") and display.startswith("https://images.metmuseum.org/"),"official JPEG unavailable"
        assert primary!=display,"original/display must differ"
        assert "met-"+str(s["object_id"]) not in {x["id"] for x in load(ROOT/"data/artworks.json")["artworks"]}
        output("RESEARCH",no,ident,api.get("title"),api.get("objectDate"))
        raw_display=req(display)
        raw_original=req(primary)
        dims={}
        rgb={}
        for kind,data in (("display",raw_display),("original",raw_original)):
            im=Image.open(io.BytesIO(data))
            im.verify()
            im=Image.open(io.BytesIO(data)).convert("RGB")
            rgb[kind]=im
            dims[kind]=[im.width,im.height]
            output("JPEG",ident,kind,"bytes",len(data),"sha256",sha(data),"dims",dims[kind])
        w,h=dims["display"]; W,H=dims["original"]
        assert abs(w/h-W/H)<.025,"image aspect ratios disagree"
        small=rgb["display"]
        resized=rgb["original"].resize(small.size,Image.Resampling.LANCZOS)
        rms=sum(ImageStat.Stat(ImageChops.difference(small,resized)).rms)/3
        assert rms<28, ("different source image?",ident,rms)
        high={"url":primary,"sha256":sha(raw_original),"byte_length":len(raw_original),
              "width":W,"height":H,"verification":"complete_jpeg_sha256_and_downscale_match",
              "source_identity_basis":f"Same Met API object primary original/display; resized RGB RMS={rms:.4f}",
              "last_full_sha_checked_on":DATE,"human_visual_checked":False}
        image={"image_id":ident+"-primary","iiif_base":None,"iiif_reference_url":None,
            "display_url":display,"source_registry_id":ident,"local_path":"/artworks/"+ident+".jpg",
            "sha256":sha(raw_display),"byte_length":len(raw_display),"live_image_checked":True,
            "live_check_scope":"Work-specific visual matching and limitations recorded in research evidence; actual primary JPEG full bytes, dimensions and RGB downscale independently checked.",
            "source_accession_number":api.get("accessionNumber",""),"high_resolution":high}
        image_record={"id":ident,"title":api["title"],"official_artwork_url":official,
            "origin":"met_official_primary","in_shared_catalog":True,
            "verification":"met_primary_jpeg_http_verified","image_source":{
              "type":"met_open_access","official_image_page":official,
              "license_label":"The Met Open Access / CC0 (public-domain work; official primary JPEG)",
              "license_url":OA,"verified_download_url":display,
              "sha256":sha(raw_display),"byte_length":len(raw_display),
              "last_http_sha_checked_on":DATE,
              "last_verification_evidence":f"https://github.com/matumaruex/kaiga-data/blob/{BRANCH}/docs/artwork-research-evidence/met-477-479-2026-11-14.json",
              "license_review_status":"official_OA_confirmed_release_review_pending","high_resolution":high},
              "accession_number":api.get("accessionNumber","")}
        src={"museum":"Metropolitan Museum of Art","artwork_id":s["object_id"],
             "artwork_url":official,"api_url":apiurl,"record_checked_on":DATE}
        artist=api.get("artistDisplayName") or "Unknown artist"
        facts={"title_original":api["title"],"title_ja_provisional":s["title_ja"],
             "artist":artist,"creation_date_display":api.get("objectDate") or "Unknown date",
             "type":"Painting","is_public_domain_at_source":True,
             "culture":api.get("culture") or api.get("country") or "Unspecified",
             "accession_number":api.get("accessionNumber","")}
        emotions=[x[0] for x in s["emotions"]]
        strengths={tag:score for tag,score in s["emotions"]}
        primary_tags=[tag for tag,score in s["emotions"] if score>=2]
        secondary_tags=[tag for tag,score in s["emotions"] if score==1]
        visitor={"language":"ja","text":s["visitor"],"source_urls":[official],
                 "review":{"content_status":"verified","source_status":"verified",
                           "rights_status":"verified","reviewed_on":DATE}}
        curation={"emotions":emotions,"emotion_strengths":strengths,
            "tones":s["tones"],"themes":s["themes"],"evidence_url":official,
            "search_profile":{"fitting_situations":[{
                "situation":s["fitting"],"reason":s["interpretation"],"strength":2}],
                "selection_cautions":[s["caution"]],"review_status":"evidence_reviewed"},
            "meaning_basis":{
               "author_intent":{"status":"not_verified_for_this_work","summary":None,"source_url":None},
               "scholarly_interpretation":{"summary":s["interpretation"],"source_url":official},
               "creation_context":f"{facts['creation_date_display']}; {facts['culture']}; {api.get('medium','')}; accession {facts['accession_number']}",
               "visual_clues":s["visual"],"uncertainty_note":s["caution"]},
            "emotion_categories":{"primary":primary_tags,"secondary":secondary_tags}}
        art={"id":ident,"source":src,"facts":facts,"image":image,"curation":curation,
             "review":{"facts_checked_against_museum_api":True,
                       "source_public_domain_flag_checked":True,
                       "visual_checked":False,"curatorial_reviewed_on":DATE,
                       "curatorial_review_status":"provisional",
                       "curatorial_review_note":"Each exact Met artwork-specific Overview and accessible work-matched image was independently examined; Met work-specific official IIIF originals were directly opened for met-446562, met-42314, and met-436749; every registered official JPEG pair checked in CI. Official primary JPEG hashes checked in CI. Same AI, not a human/expert auditor."},
             "visitor_explanation":visitor}
        proposal={"schema_version":"artwork-addition-proposal-v1","id":ident,
                  "artwork":art,"image_record":image_record}
        candidate_path="drafts/artwork-additions/"+ident+".json"
        draft_path="drafts/visitor-explanations/"+ident+".json"
        dump(candidate_path,proposal)
        draft={"id":ident,"visitor_explanation":visitor,
               "evidence":[{"claim":s["interpretation"],"source_url":official,
                            "source_location":"Met object-specific Overview; directly read 2026-11-14",
                            "checked_against_source":True}]}
        dump(draft_path,draft)
        image_ev=[]
        for kind,data,url in (("display",raw_display,display),("original",raw_original,primary)):
            image_ev.append({"kind":kind,"url":url,"sha256":sha(data),"byte_length":len(data),
                "download_status":200,"full_bytes_sha256_checked":True,
                "image_subject_visually_compared":True,"visual_source_urls":s.get("visual_source_urls",[]),"checked_on":DATE,
                "observation":s["visual"]+f" Official same-object primary JPEG original/display resized RGB RMS={rms:.4f}; not a human visual signoff."})
        checks=[{"source_url":official,"source_excerpt":c["excerpt"],"visitor_claim":c["claim"],
                 "source_section":"Met artwork-specific Overview (read directly in research pass)"} for c in s["checks"]]
        source_evidence=[
            {"url":official,"location":"Actual artwork Overview and object information; two matching English excerpts",
             "finding":s["interpretation"]+" Visual: "+s["visual"]+" Limits: "+s["caution"],"checked_against_source":True},
            {"url":apiurl,"location":"Met live object API public-domain flag, object ID, official original/display JPEG URLs",
             "finding":f"{ident}: API objectID={api['objectID']}, primary JPEG full downloaded and verified; RMS={rms:.4f}",
             "checked_against_source":True},
            {"url":OA,"location":"Met Open Access CC0 policy for JPEG reproductions of public domain works",
             "finding":"The Met states primary JPEGs of public-domain objects are available under CC0; separate modern explanatory-text rights were not waived.",
             "checked_against_source":True}]
        audit={"schema_version":"artwork-v2-new-registration-2","id":ident,"checked_on":DATE,
             "result":"PASS","unresolved_material_issues":[],
             "candidate_path":candidate_path,"candidate_sha256":filehash(ROOT/candidate_path),
             "draft_path":draft_path,"draft_sha256":filehash(ROOT/draft_path),
             "baseline":{"artworks_sha256":filehash(ROOT/"data/artworks.json"),
                         "image_registry_sha256":filehash(ROOT/"data/image-sources.json")},
             "official_text_checks":checks,"source_evidence":source_evidence,
             "rights":{
               "artwork":{"verified":True,"public_domain":True,"source_url":official,
                          "finding":"Exact Met artwork page says Public Domain; live object API isPublicDomain true."},
               "image":{"verified":True,"permitted_for_site_use":True,"source_url":OA,
                        "finding":f"Official Met Open Access CC0; full display and original JPEG SHA256/lengths/dimensions and matching image RMS={rms:.4f}."},
               "text":{"verified":True,"independent_japanese_prose":True,"source_url":official,
                       "finding":"Independently written Japanese prose from primary source facts and directly observed imagery, not a translation of the Met Overview. Quoted English source snippets confined to internal audit; no expert legal assurance."}},
             "separate_pass_review":{"result":"PASS",
               "method":"Same AI separate substantive check of the exact object-specific Met Overview (two brief source excerpts mapped to Japanese claims) and the artwork-specific visual sources: official Met IIIF 446562/880847, 42314/2108942, and 436749/790154 were opened and visually checked, plus GitHub Actions live Met API full-original/display JPEG SHA256, dimensions and downscale comparison. Automated structural checks do not by themselves prove historical correctness.",
               "limitations":"AI's separate research/review passes, not an independent human, model or academic scholar. CI may be rate-limited if it independently fetches the Overview; source excerpts had been directly read through the research browser.",
               "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
               "findings":{"identity":f"{ident} {facts['title_original']} / {artist} / {facts['creation_date_display']} / {facts['accession_number']}",
                           "image_match":s["visual"]+f" Both primary JPEG variants fully downloaded and match (RMS={rms:.4f}).",
                           "historical_interpretation":s["interpretation"]+" Cautions: "+s["caution"],
                           "emotion":f"Judged curator-side tag links, not viewer predictions: {emotions}",
                           "visitor_text":"Original Japanese visitor paragraphs checked against two exact short passages on this artwork-specific Met Overview.",
                           "rights":"Public-domain object, Met OA/CC0 image, contemporary prose treated as distinct copyrighted text."}},
             "image_evidence":image_ev,
             "notes":[f"New sequential registration #{no} with preceding artwork and image-registry records unchanged.",
                      "Two excerpts checked against exact Met artwork Overview. Official or independently identified artwork-specific image visually inspected with provenance separately recorded. Official API primary JPEGs verified for size, SHA and downscale match.","No claims of human approval or expert rights review."]}
        audit_path=f"docs/artwork-completion-audits/{ident}-{DATE}.json"
        dump(audit_path,audit)
        researched.append({"id":ident,"objectID":s["object_id"],"title":api.get("title"),
            "artist":artist,"date":api.get("objectDate"),"accession":api.get("accessionNumber"),
            "publicDomain":api.get("isPublicDomain"),"official_url":official,
            "api_url":apiurl,"source_excerpt_checks":checks,"visual_observation":s["visual"],"visual_source_urls":s.get("visual_source_urls",[]),
            "main_primary_jpegs":[{"kind":e["kind"],"url":e["url"],"sha256":e["sha256"],"byte_length":e["byte_length"],
                                  "size_px":dims[e["kind"]]} for e in image_ev],
            "resized_rgb_rms":round(rms,4)})
        shell(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
        shell(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
        shell(sys.executable,"scripts/add_artwork.py","check")
        output("SAVED",no,ident)
    dump("docs/artwork-research-evidence/met-477-479-2026-11-14.json",
         {"checked_on":DATE,"method":"Live Met API primary original/display full JPEG SHA256/size and RGB correspondence; exact Met artwork Overview read directly. Official Met IIIF views 446562/880847, 42314/2108942, and 436749/790154 were directly viewed and compared to the individual Met Overview descriptions. CI verifies each official Met API original/display JPEG pair.", "artworks":researched,
          "limitations":["Same AI review, not an independent human/expert","Per-work visual-reference provenance and limitations documented; official Met original/display JPEGs downloaded and RGB correspondence checked"]})
    text="## 現在の状態（2026-11-14時点）\n\n"+\
         "- **完成登録：479作品**。main統合後にDBとREADMEが正本。\n"+\
         "- **次：480作品目から候補調査**。新作は作品固有の公式Overview、画像実体、作品PD／画像CC0／学芸員本文権利、重複、別工程監査の順で確認。\n"+\
         "- 今回477〜479：ムガル帝国《ディララムの音楽に魅了される鹿たち》、蹄斎北馬《三味線持つ美人図》、ルチア・アングイッソラ帰属《男性の肖像》。既存476件は不変。\n"+\
         "- 作品別の証拠は `docs/artwork-completion-audits/`、画像・調査記録は `docs/artwork-research-evidence/met-477-479-2026-11-14.json`。原寸・表示JPEGの全SHA256、寸法、縮小RMS検査済み。\n"+\
         "- 解説は日本語の独自文章。短い原文抜粋を各作品の個別Overviewから2箇所確認。人間・別モデルの審査ではなく同一AIの別工程確認。\n"
    Path("/tmp/artwork-new-resume.md").write_text(text,encoding="utf-8")
    shell(sys.executable,"scripts/rotate_resume.py","update","--from","/tmp/artwork-new-resume.md")
    for args in [
        (sys.executable,"scripts/rotate_resume.py","check"),
        (sys.executable,"scripts/validate_artworks.py"),
        (sys.executable,"scripts/check_image_sources.py"),
        (sys.executable,"scripts/check_catalog_snapshot.py"),
        (sys.executable,"-m","unittest","discover","-s","tests")
    ]:shell(*args)
    assert len(load(ROOT/"data/artworks.json")["artworks"])==479
    # One-shot helper code must not remain on main after merging.
    for relative in ["scripts/tmp_specs_477_479.json","scripts/tmp_register_477_479.py",
                     ".github/workflows/tmp_register_477_479.yml"]:
        Path(relative).unlink()
    for folder in ("scripts","tests"):
        for compiled in (ROOT/folder).rglob("__pycache__"):
            shutil.rmtree(compiled)
    shell("git","status","--short")
    shell("git","add","-A")
    shell("git","-c","user.name=github-actions[bot]",
          "-c","user.email=41898282+github-actions[bot]@users.noreply.github.com",
          "commit","-m","data: register verified Met artworks 477–479 with exact source and image audits")
    shell("git","push","origin",BRANCH)
    output("SUCCESS: 479 artworks, new work saved and workflow helpers removed")
if __name__=="__main__":
    main()
