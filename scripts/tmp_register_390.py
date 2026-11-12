#!/usr/bin/env python3
"""One-off source-reviewed registration for #390-392. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-390-392-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-390-392-20261112/"+EVIDENCE
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

SPEC={int(k):v for k,v in {
  "764095": {
    "number": 391,
    "japanese": "十字架を担うキリスト（《転倒の主》）",
    "artist": "Unknown Cuzco artist",
    "culture": "Peru (Cuzco)",
    "situation": "18世紀クスコ派の祭壇図で、キリストの彫像と飾り立てられた聖所をどのように絵で表したかを知りたい",
    "meaning": "メトロポリタン美術館の作品別Overviewによれば、本作は『statue painting』すなわち信仰を集める聖像の姿を絵に写した作品。クスコのサン・フランシスコ教会で崇敬されたナザレのキリスト彫像を『真の似姿』として描くことで、原像の奇跡的な力も備わると信じられた。祭壇の階段と天蓋の下にキリスト像があり、周囲には他の彫像、銀製装飾、ろうそく、花、羽根などが密に描かれる。実際に奇跡があったと断定するものではない。",
    "visual": "Met公式APIの主画像は黒い外縁を持つ縦長の華やかな祭壇。中央上寄りには下向きの顔のキリスト像が衣をまとう姿、周囲に多数の小さな聖像や左右対称に積まれた銀色・色彩豊かな飾り、下部に階段状の台座が見える。画面外の黒い余白と絵の暗い室内を区別して眺めた。",
    "caution": "絵が現実の彫像の忠実な『似姿』と信じられたという文化史上の事実と、奇跡の実在を混同しない。作品を現物の彫像や祭壇の写真と呼ばない。作者は不明のクスコ画家。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "重苦しさ"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "中央に立つキリストの聖像を、銀色の飾りや小さな像、花やろうそくがぎっしりと取り囲んでいます。人物だけでなく、そこにある祭壇や天蓋の形まで細かく表され、信仰の場全体を一枚の画面に収めています。\n\n1770〜75年頃にペルーのクスコで制作されたこの作品は、彫刻の聖像を描いた「聖像画」の一種です。クスコのサン・フランシスコ教会で崇敬されたナザレのキリスト像を、その祭壇ごと描いています。キリストの聖像は、階段状の祭壇の上にある天蓋の下に置かれています。\n\n当時、このような絵は聖像の「真の似姿」と考えられ、元の像と同じ奇跡の力を持つと信じられることがありました。これは信仰の歴史を示すもので、奇跡の事実を証明するものではありません。中心のキリスト像から周囲の小さな装飾へ目を移すと、何を大切にして礼拝の場が整えられていたかが伝わってきます。",
    "checks": [
      [
        "This work belongs to the genre of \"statue painting\"",
        "1770〜75年頃にペルーのクスコで制作されたこの作品は、彫刻の聖像を描いた「聖像画」の一種です。",
        "Met exact Overview: genre of statue painting"
      ],
      [
        "The sacred image of the Nazarene is displayed beneath a baldachin",
        "キリストの聖像は、階段状の祭壇の上にある天蓋の下に置かれています。",
        "Met exact Overview: Nazarene beneath a baldachin"
      ]
    ]
  },
  "825597": {
    "number": 390,
    "japanese": "皇帝の謁見式に集まる従者たち",
    "artist": "Hunhar",
    "culture": "India, Mughal court",
    "situation": "ムガル帝国の宮廷儀礼で、象や馬、奏楽者、随員たちがどのように配置されていたかを見たい",
    "meaning": "メトロポリタン美術館の個別Overviewによると、画家フンハルによる1645年頃の絵はシャー・ジャハーン朝の宮廷年代記『パードシャーナーマ』に関係する見開き構図の右側の断片で、欠けた左側にペルシア使節を謁見する皇帝が描かれたとされる。現存画面には使節団のペルシア人（大きなターバン）、ムガル廷臣、馬丁、馬と象がおり、門上のナッカールハーナ（太鼓の家）の楽人が一行を迎える。皇帝をこの主画像に描かれていると断定しない。",
    "visual": "公式Met APIに結び付くJPEGを見たところ、縦長の色鮮やかな画面の中央に象と鞍飾り、前方・左右に巻物状の頭巾や鮮やかな衣の人物が集まり、上部の建物の窓や欄に楽人らしい一団が並ぶ。金色・紫色の装飾や奥の建物が細かく描かれる。右側断片のみなので、欠けた皇帝のいる別頁を今ある画像と混同しない。",
    "caution": "見開きの失われた左半にあるはずの皇帝・ペルシア大使の謁見場面が見えているかのように描写しない。写実的な宮廷写真や人物個人の心理として扱わない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "象と飾り立てられた馬の周りに、華やかな衣装の人々が集まっています。画面の上部、門のような建物に目を上げると、音楽を奏でる一団も見つかります。人々の列と動物の姿を追ううちに、宮廷の儀礼が多くの役割を持つ人々によって支えられていたことが感じられます。\n\nこの絵は、17世紀のムガル帝国を描いた画家フンハルによる1645年頃の作品です。本来の見開き構図の右側にあたる断片で、失われた左側には、皇帝シャー・ジャハーンがペルシアの使節を迎える場面が続いていたと説明されています。つまり、現在の主画像に皇帝本人が見えるわけではありません。\n\n現存する側には、大きなターバンを巻いた使節団の人物やムガル宮廷の廷臣、従者たちが描かれています。門の上の楽人たちは一行を音楽で迎えています。人物が画面の外側へ向いている様子からも、描かれなかった左半分の存在を想像できるでしょう。",
    "checks": [
      [
        "The painting is a fragment of the right-hand side",
        "本来の見開き構図の右側にあたる断片で、失われた左側には、皇帝シャー・ジャハーンがペルシアの使節を迎える場面が続いていたと説明されています。",
        "Met exact Overview: right-hand fragment of two-page composition"
      ],
      [
        "An animated group of musicians welcome the party",
        "門の上の楽人たちは一行を音楽で迎えています。",
        "Met exact Overview: musicians in the drum house"
      ]
    ]
  },
  "910555": {
    "number": 392,
    "japanese": "三十六歌仙図屏風",
    "artist": "Studio of Kano Takanobu (painting); Konoe Nobutada (inscriptions)",
    "culture": "Japan, Momoyama period",
    "situation": "桃山時代の屏風で、三十六人の和歌の名手を描いた人物と近衛信尹の書を合わせて眺めたい",
    "meaning": "Met個別Overviewによれば、狩野孝信の工房が絵を描き、近衛信尹が和歌を書いた17世紀初頭の六曲一双屏風。藤原公任が選んだ三十六歌仙は、僧侶二人、女性五人、その他宮廷の男性を含む。大画面の折り畳み屏風形式として現存する初期の優品。柿本人麻呂と紀貫之の歌が端にある。公式のprimaryImage（DP-35700-001）は対の屏風の一方を写した横長画像で、対の全体を1枚に載せた画像ではない。右から左に鑑賞する形式。画家と書き手は別人で、単独の狩野孝信の直筆作としない。",
    "visual": "Met公式API主画像のサムネイルでは、横長の金茶色の六曲屏風の一方に、色彩豊かな衣をまとう貴族らしき人物が横に並んで座り、その上に筆文字の歌が段をなして記されている。金や茶の下地、画面の左右端の装飾枠が見える。二枚のうちの一方だけで、全36人がこの主画像に写っていると誤認しない。",
    "caution": "作品は一双の屏風なのに、配信するprimary JPEGはその一方だけ。36人の歌人が現在の1画像に全員描かれていると書かない。絵は狩野孝信工房、詞書は近衛信尹の仕事として明記。作品別ページにある和歌の全訳は転載しない。",
    "emotions": [
      "懐かしさ"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "記憶",
      "時間"
    ],
    "text": "横に広がる金茶色の画面に、色鮮やかな衣を着た人々が腰を下ろしています。その上には筆で書かれた和歌が配され、絵と文字が一緒になって人物の姿を伝えています。視線を右から左へ進めると、歌人たちが少しずつ現れてくる構成です。\n\nこれは、平安時代の優れた和歌の作者三十六人を描く、17世紀初めの《三十六歌仙図屏風》です。絵は狩野孝信の工房が制作し、詞書は近衛信尹が担当しました。三十六歌仙には僧侶二人、宮廷の女性五人なども含まれ、古くからの和歌文化を人物像とともに伝えています。\n\n作品は六曲屏風の一双、つまり二つの屏風を組み合わせたものです。ここで使われている公式の主画像は、そのうち一方だけを写しています。画面に見える人物と歌をたどりながら、もう一方にも歌仙の姿と歌が続いていることを思い描いてみてください。",
    "checks": [
      [
        "This pair of screens portraying the Thirty-Six Poetic Immortals",
        "作品は六曲屏風の一双、つまり二つの屏風を組み合わせたものです。",
        "Met exact Overview: pair of screens for the Thirty-Six Poetic Immortals"
      ],
      [
        "Two were famous monks, five were court ladies",
        "三十六歌仙には僧侶二人、宮廷の女性五人なども含まれ、古くからの和歌文化を人物像とともに伝えています。",
        "Met exact Overview: composition of thirty-six poets"
      ]
    ]
  }
}.items()}

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
          "Met 825597 original right-hand fragment does not show emperor on missing left; Met 910555 primary JPEG shows only one of the pair of six-fold screens, with separate studio painting and Nobutada calligraphy."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==389,"main must have exactly 389 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：392作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：393作品目から候補調査**。既登録との重複、Met作品別Overview原文、原寸/表示画像と権利を個別に確かめる。
- 今回390〜392：`met-825597` フンハル《皇帝の謁見式に集まる従者たち》（1645年頃、ムガル帝国）、`met-764095`《十字架を担うキリスト（転倒の主）》（1770〜75年頃、ペルー）、`met-910555`《三十六歌仙図屏風》（17世紀初頭、日本）。
- `met-825597` は見開き右側の断片で皇帝がいる左側は主画像に写らない。`met-910555` は六曲一双のうち公式主JPEGに写るのが一隻だけ。日本作品は絵の制作（狩野孝信工房）と書（近衛信尹）を区別。
- 個別Met作品ページのOverview本文を読んで二つずつの短い原文抜粋と日本語解説の対応箇所を監査。Met API上で作品PD確認、公式JPEGのCC0と現代の館解説文の権利を区別。
- 公式原寸・表示JPEGの全バイトSHA256、バイト数、画像寸法、原寸→表示の縮小RMS、原画像の実見を記録。根拠は[390〜392の画像調査](artwork-research-evidence/met-390-392-2026-11-12.json)。
- 同じAIの別工程による審査であり、外部専門家や人間による査読ではない。既存389作品・画像台帳の以前の部分は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-390.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==392,"final count mismatch")
    print("ALL PASS: 392 new total, existing 389 preserved",flush=True)
if __name__=="__main__":
    main()
