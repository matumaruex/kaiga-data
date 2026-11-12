#!/usr/bin/env python3
"""One-off source-reviewed registration for #381-383. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-381-383-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-381-383-20261112/"+EVIDENCE
LICENSE_URL="https://www.metmuseum.org/hubs/open-access"

def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(p,obj):
    f=ROOT/p
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def run(*args):
    print("RUN", *args, flush=True)
    subprocess.run(args,cwd=ROOT,check=True)
def check(c,m):
    if not c:raise ValueError(m)

SPEC={
451023:{
  "number":381,
  "japanese":"恋人たち",
  "artist":"Riza-yi 'Abbasi",
  "culture":"Iran (Isfahan)",
  "situation":"サファヴィー朝の絵画に描かれた、二人の親密さと人物を結ぶ線の表現を見たい",
  "meaning":"メトロポリタン美術館の作品別Overviewは、リザーイー・アッバースィーの流麗な描線と独特な色彩、1630年のサファヴィー朝宮廷での官能的題材の扱いを説明する。寄り添う二人が一つの輪郭に収まる構図は美術館の指摘。人物の身元や作者の体験は資料にない。",
  "visual":"縦長の紙面で、頭を寄せる二人が互いに腕を回し、青い帽子、緑と茶の衣服、金色の細い植物文様、左下の文字と器が見える。画像端の模様のある縁も確認。",
  "caution":"二人の実在の身元や画家の私生活を断定しない。宮廷文化の解釈は所蔵館の記述として扱う。",
  "emotions":["慈しみ"],"tones":["落ち着き"],"themes":["愛情","他者との距離"],
  "text":"寄り添う二人の姿が、ひと続きの柔らかな輪郭線の中に収められています。頭を傾ける仕草や重なる袖に目を向けると、人物同士の距離がごく近く感じられます。金色の雲や草花は、親密な場面の周囲に静かな装飾を添えています。\n\n《恋人たち》は、17世紀イランの画家リザーイー・アッバースィーが1630年に描いた作品です。メトロポリタン美術館は、書のように流れる線と独特な色彩をこの画家の特徴として説明しています。二人の身体はひとつの輪郭の中で重なり、どこからが一方の形なのか曖昧になるほど密着しています。\n\n美術館はこの抱擁を、当時のサファヴィー朝宮廷で官能的な主題への態度が変わっていた時期と結びつけています。ただし、モデルとなった二人の身元や画家自身の恋愛体験を示すものではありません。指先と衣の境目をたどりながら、線が二人を結ぶ働きを見てみてください。",
  "checks":[
    ["with his inventive use of calligraphic line and unusual palette","書のように流れる線と独特な色彩をこの画家の特徴として説明しています。","Overview: calligraphic line and palette"],
    ["the figures are inextricably bound together, merged volumes confined within one outline","二人の身体はひとつの輪郭の中で重なり、どこからが一方の形なのか曖昧になるほど密着しています。","Overview: figures within one outline"]
  ]
},
74725:{
  "number":382,
  "japanese":"イノシシを狩る君主と従者たち",
  "artist":"Unidentified Mewar court artist",
  "culture":"Western India, Rajasthan, Udaipur",
  "situation":"18世紀初めのメーワール地方の狩猟を、墨線と俯瞰した構図から読みたい",
  "meaning":"Metの作品別Overviewによると、輪光で示された君主と従者たちがイノシシを狩る場面。君主は旗持ちとともに画面内に二度描かれ、同一人物の異なる場面を示す。俯瞰図と軽快な動きが特長で、現場写生または別作品の下図であった可能性はあるが断定されていない。",
  "visual":"横長の黄ばんだ紙に細い墨線で騎馬隊、徒歩の人々、イノシシが散在する。左上の建物と遠景の丘、小さく描かれた複数の群像と広い空白を確認。",
  "caution":"準備画や野外での実地写生を確定事実にしない。暴力性を描いているが作者本人の感情を推定しない。",
  "emotions":[],"tones":["緊張"],"themes":["共同体","自然"],
  "text":"薄い墨の紙面に、小さな人馬とイノシシが幾つもの群れをなして現れます。地平の丘や建物はわずかな線で示され、遠くの狩りまで見渡すような広い構図になっています。細かな線を追うにつれて、画面のあちこちで異なる出来事が進んでいることに気づきます。\n\n18世紀初めのインド・ラージャスターン地方、ウダイプル宮廷の狩猟図です。美術館の解説によれば、旗持ちを従えた君主が画面内に二度登場し、狩りの異なる場面を示しています。空から見下ろすような視点と、人馬の軽快な動きが特徴です。\n\nこの作品は墨の濃淡による素描に近い画面を持っています。美術館は、野外で実見しながら描かれ、別の完成作品のための準備画だった可能性を示しますが、制作手順が確定しているわけではありません。繰り返し描かれた君主の位置を探すと、一枚の紙に時間の流れを収める工夫が見えてきます。",
  "checks":[
    ["The ruler, attended by standard bearers, appears twice in the composition","旗持ちを従えた君主が画面内に二度登場し、狩りの異なる場面を示しています。","Overview: ruler repeated at two stages"],
    ["The aerial view, fluid action, and confidently executed figures","空から見下ろすような視点と、人馬の軽快な動きが特徴です。","Overview: aerial view and movement"]
  ]
},
764086:{
  "number":383,
  "japanese":"聖ボナヴェントゥラとパドヴァの聖アントニウス",
  "artist":"Follower of Basilio Santa Cruz Pumacallao",
  "culture":"Peru (Cuzco)",
  "situation":"17世紀クスコ派の宗教絵画で、翼を持つ二人の聖人と楽器の細部を見たい",
  "meaning":"Met作品別Overviewでは翼を持つフランシスコ会の二人、左の聖ボナヴェントゥラは赤い頭巾、右の聖アントニウスは百合が目印となる。両者はビウエラ系の楽器を弾く。大きな無原罪の聖母と異端の敗北の寓意画の断片で、作者はバシリオ本人と断定されず『Follower of』と帰属される。",
  "visual":"暗い四角い画面に翼を持つ二人の半身像。左の赤い頭巾と小さな弦楽器、右の褐色の衣と大きな弦楽器、両者の上部の羽根と端の暗い地を実画像で確認。",
  "caution":"作者をバシリオ本人と断定しない。現存画面は大きな寓意画の一部であり元の全体画面と混同しない。楽器の具体的形状は公式の名称に従う。",
  "emotions":["畏敬"],"tones":["静けさ"],"themes":["共同体","時間"],
  "text":"暗い地の上に、翼を持つ二人の修道士が楽器を手に並んでいます。左の人物は赤い頭巾と小さな弦楽器を、右の人物は弓で奏でる楽器を持っています。衣の色と楽器の形の違いを見比べると、二人の役割が少しずつ読み取れます。\n\n描かれているのは聖ボナヴェントゥラとパドヴァの聖アントニウスです。美術館の解説は、二人が翼を持つフランシスコ会の聖人として表されていると説明しています。赤い頭巾と百合の枝は、それぞれの聖人を見分ける手掛かりです。\n\nこの絵は、聖母マリアとフランシスコ会の聖人たちを主題にした大きな寓意画の一部分と考えられています。17世紀後半のペルー・クスコで、バシリオ・サンタ・クルス・プマカリャオの周辺に連なる画家が制作したとされます。小さく残された画面の外側に、かつて続いていた物語を想像してみてください。",
  "checks":[
    ["This painting depicts two winged Franciscans","二人が翼を持つフランシスコ会の聖人として表されていると説明しています。","Overview: winged Franciscan saints"],
    ["The painting is a fragment from a large and complex allegorical composition","この絵は、聖母マリアとフランシスコ会の聖人たちを主題にした大きな寓意画の一部分と考えられています。","Overview: surviving fragment of allegory"]
  ]
}
}

def prepare(meta,spec,baseline):
    number=spec["number"]
    ident="met-"+str(meta["id"])
    official="https://www.metmuseum.org/art/collection/search/"+str(meta["id"])
    api=meta["api"]
    images=meta["images"]
    check(api["objectID"]==meta["id"],"Met ID mismatch")
    check(api["isPublicDomain"] is True,"Not PD "+ident)
    check(api["primaryImage"]==images["original"]["url"] and api["primaryImageSmall"]==images["display"]["url"],"image URLs mismatch")
    check(not meta.get("error"),"research error "+ident)
    check(images["rgb_resize_rms"]<20,"RMS excessive "+ident)
    existing=load("data/artworks.json")["artworks"]
    registry=load("data/image-sources.json")["records"]
    check(len(existing)==number-1,"sequential baseline not "+str(number-1))
    check(not any(a["id"]==ident or a["source"]["artwork_url"]==official for a in existing),"duplicate ID")
    check(not any(a["facts"]["title_original"]==api["title"] and a["facts"]["artist"]==spec["artist"] for a in existing),"duplicate title/artist")
    check(not any(a["image"]["sha256"]==images["display"]["sha256"] for a in existing),"duplicate image sha")
    check(not any(x["id"]==ident for x in registry),"image registry duplicate")
    base=copy.deepcopy(load("drafts/artwork-additions/met-845805.json"))
    art=base["artwork"]
    art["id"]=ident
    art["source"]={"museum":"Metropolitan Museum of Art","artwork_id":meta["id"],"artwork_url":official,
      "api_url":"https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(meta["id"]),
      "record_checked_on":DATE}
    art["facts"]={"title_original":api["title"],"title_ja_provisional":spec["japanese"],"artist":spec["artist"],
      "creation_date_display":api["objectDate"],"type":"Painting",
      "is_public_domain_at_source":True,"culture":api["culture"] or spec["culture"],"accession_number":api["accessionNumber"]}
    observation=spec["visual"]+" Met公式原寸と表示JPEGを全バイトSHA256で取得し、縮小RMS="+str(round(images["rgb_resize_rms"],4))+"で対応確認。"
    high={"url":images["original"]["url"],"sha256":images["original"]["sha256"],
      "byte_length":images["original"]["byte_length"],"width":images["original"]["width"],
      "height":images["original"]["height"],"verification":"complete_jpeg_sha256_and_downscale_match",
      "source_identity_basis":"Same Met API primary original/display, RGB downscale RMS "+str(round(images["rgb_resize_rms"],5)),
      "last_full_sha_checked_on":DATE,"human_visual_checked":False}
    art["image"]={"image_id":ident+"-primary","iiif_base":None,"iiif_reference_url":None,
       "display_url":images["display"]["url"],"source_registry_id":ident,
       "local_path":"/artworks/"+ident+".jpg",
       "sha256":images["display"]["sha256"],"byte_length":images["display"]["byte_length"],
       "live_image_checked":True,"live_check_scope":"Live Met API and both actual official JPEG full SHA256/bytes, resize RMS and same-AI viewed thumbnails: "+RESEARCH_URL,
       "source_accession_number":api["accessionNumber"],"high_resolution":high}
    primary=spec["emotions"]
    art["curation"]={"emotions":primary,"emotion_strengths":{x:(2 if ident=="met-451023" else 1) for x in primary},
       "tones":spec["tones"],"themes":spec["themes"],"evidence_url":official,
       "search_profile":{"fitting_situations":[{"situation":spec["situation"],"reason":spec["meaning"],"strength":2}],
         "selection_cautions":[spec["caution"]],"review_status":"evidence_reviewed"},
       "meaning_basis":{"author_intent":{"status":"not_verified_for_this_work","summary":None,"source_url":None},
         "scholarly_interpretation":{"summary":spec["meaning"],"source_url":official},
         "creation_context":api["objectDate"]+"; "+spec["culture"]+"; "+api["medium"]+"; accession "+api["accessionNumber"],
         "visual_clues":observation,"uncertainty_note":spec["caution"]},
       "emotion_categories":{"primary":(primary if ident=="met-451023" else []),"secondary":([] if ident=="met-451023" else primary)}}
    art["review"]={"facts_checked_against_museum_api":True,"source_public_domain_flag_checked":True,
      "visual_checked":False,"curatorial_reviewed_on":DATE,"curatorial_review_status":"provisional",
      "curatorial_review_note":"Same AI conducted separate real-page and JPEG thumbnail review; not human or independent expert. "+RESEARCH_URL}
    visitor={"language":"ja","text":spec["text"],"source_urls":[official],
      "review":{"content_status":"verified","source_status":"verified","rights_status":"verified","reviewed_on":DATE}}
    art["visitor_explanation"]=visitor
    check(sum(len(x[0].split()) for x in spec["checks"])<=25,"quote words exceeded")
    for src,claim,section in spec["checks"]:
       check(claim in visitor["text"] and len(src.split())>=6 and len(src.strip())>=35,"claim excerpt mismatch")
    record={"id":ident,"title":api["title"],"official_artwork_url":official,"origin":"met_official_primary",
      "in_shared_catalog":True,"verification":"met_primary_jpeg_http_verified",
      "image_source":{"type":"met_open_access","official_image_page":official,
        "license_label":"The Met Open Access / CC0 (Public Domain work, official primary JPEG)",
        "license_url":LICENSE_URL,"verified_download_url":images["display"]["url"],
        "sha256":images["display"]["sha256"],"byte_length":images["display"]["byte_length"],
        "last_http_sha_checked_on":DATE,"last_verification_evidence":RESEARCH_URL,
        "license_review_status":"official_OA_confirmed_release_review_pending","high_resolution":high},
       "accession_number":api["accessionNumber"]}
    proposal={"schema_version":"artwork-addition-proposal-v1","id":ident,"artwork":art,"image_record":record}
    draft={"id":ident,"visitor_explanation":visitor,
      "evidence":[{"claim":spec["meaning"],"source_url":official,
        "source_location":"Exact Met artwork Overview: "+" | ".join(x[2] for x in spec["checks"]),
        "checked_against_source":True}]}
    candidate_path="drafts/artwork-additions/"+ident+".json"
    draft_path="drafts/visitor-explanations/"+ident+".json"
    dump(candidate_path,proposal)
    dump(draft_path,draft)
    checks=[{"source_url":official,"source_excerpt":q,"visitor_claim":cl,"source_section":sec} for q,cl,sec in spec["checks"]]
    area={"identity":ident+" "+api["title"]+"; "+spec["artist"]+"; "+api["objectDate"]+"; accession "+api["accessionNumber"]+". Correct attribution uncertainty as on exact artwork page.",
       "image_match":observation+" Actual Met JPEG identities and size checked in "+RESEARCH_URL,
       "historical_interpretation":spec["meaning"]+" Limits: "+spec["caution"],
       "emotion":"Emotion tags are curator-facing possibilities, not claims about artist psychology: "+repr(spec["emotions"]),
       "visitor_text":"Japanese visitor prose separately checked against actual Met Overview and image with two concise verbatim excerpts.",
       "rights":"Object flagged Public Domain by Met page/API; primary image under Met Open Access CC0; modern Overview protected, independently authored Japanese prose."}
    audit={"schema_version":"artwork-v2-new-registration-2","id":ident,"checked_on":DATE,
       "result":"PASS","unresolved_material_issues":[],"candidate_path":candidate_path,"candidate_sha256":sha(candidate_path),
       "draft_path":draft_path,"draft_sha256":sha(draft_path),"baseline":baseline,
       "official_text_checks":checks,
       "source_evidence":[
         {"url":official,"location":"Exact artwork Overview and Object Information: "+"; ".join(x[2] for x in spec["checks"]),
           "finding":spec["meaning"]+" Actual image observation: "+observation,"checked_against_source":True},
         {"url":art["source"]["api_url"],"location":"Exact Met object API ID, artwork public-domain flag and primary JPEG URLs",
           "finding":"Actual official API data and full original/display SHA256, sizes, dimensions and RMS checked in "+RESEARCH_URL,
           "checked_against_source":True},
         {"url":LICENSE_URL,"location":"Met Open Access policy for images of public-domain works",
           "finding":"Met primary image CC0/Open Access. Modern explanatory Overview is a separate copyrighted text.",
           "checked_against_source":True}],
       "rights":{"artwork":{"verified":True,"public_domain":True,"source_url":official,"finding":"Public Domain on exact object web page and isPublicDomain true via live Met API."},
         "image":{"verified":True,"permitted_for_site_use":True,"source_url":LICENSE_URL,
           "finding":"Met original and display primary JPEG under Open Access CC0, with actual complete fingerprints and observed matching thumbnails: "+RESEARCH_URL},
         "text":{"verified":True,"independent_japanese_prose":True,"source_url":official,
           "finding":"Original Japanese interpretive explanation; two short English primary-Overview excerpts only in internal audit; no lengthy museum text reused. Not a legal opinion."}},
       "separate_pass_review":{"result":"PASS",
          "method":"Same AI's separate pass reread the exact official artwork Overview and object details, matched two exact short source passages to distinct Japanese claims, and viewed thumbnails from the actual fetched API primary display JPEG with full original/display byte hashes and resized RGB comparison.",
          "limitations":"No separate model, human scholarly reviewer, lawyer, or final site-release approval. Online museum-page fetch can be rate-limited in GitHub Actions; user-visible prose is independent, not an official translation.",
          "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],"findings":area},
       "image_evidence":[{"kind":kind,"url":images[kind]["url"],"sha256":images[kind]["sha256"],
         "byte_length":images[kind]["byte_length"],"download_status":200,"full_bytes_sha256_checked":True,
         "image_subject_visually_compared":True,"checked_on":DATE,
         "observation":observation+" Confirmed image belongs to Met artwork "+str(meta["id"])+", not lookalike search results."} for kind in ("display","original")],
       "notes":["Sequential registration #"+str(number)+"; earlier artwork and registry prefixes retained.",
          "Individual official Overview was directly reread from Met webpage and excerpts checked against actual Japanese visitor text.",
          "Research image thumbnails were generated from actual Met API primary display JPEG and observed; separate review by same AI, not an independent human auditor.",
          "For met-764086, Met webpage states Follower of Basilio Santa Cruz Pumacallao, although API artistDisplayName omits the attribution prefix."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==380,"main must have exactly 380 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：383作品**。main統合後の作品DBとREADMEを正本とする。
- **次：384作品目から候補調査**。重複、Met作品別Overviewの実際の主張、JPEGと権利の照合を作品ごとに続ける。
- 今回381〜383：`met-451023` リザーイー・アッバースィー《恋人たち》（1630年、イラン）、`met-74725`《イノシシを狩る君主と従者たち》（インド、18世紀初め）、`met-764086`《聖ボナヴェントゥラとパドヴァの聖アントニウス》（17世紀クスコ、作者はバシリオ本人でなくFollower）。
- 各作品のMet作品別Overviewを直接読んで日本語解説の二つずつの主張に短い実際の英文を対応させた。Met API作品PD、Met Open Access画像CC0、現代の美術館文章の権利は分離して記録。
- 原寸/表示JPEGの全バイトSHA256とバイト数、実寸、縮小RMS、**公式API画像から生成したサムネイルの実見**で画像照合。研究記録：[`381–383`画像監査](artwork-research-evidence/met-381-383-2026-11-12.json)。
- 作品ごとの別工程監査は同じAIによるもので、外部専門家・人間の査読ではない。既存380作品と以前の画像台帳部分は変えない。

"""
    temp=ROOT/"tmp-artwork-resume-381.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==383,"final count mismatch")
    print("ALL PASS: 383 new total, existing 380 preserved",flush=True)
if __name__=="__main__":
    main()
