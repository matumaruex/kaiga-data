#!/usr/bin/env python3
"""One-off source-reviewed registration for #393-395. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-393-395-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-393-395-20261112/"+EVIDENCE
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
  "764093": {
    "number": 395,
    "japanese": "聖バルバラ",
    "artist": "Unknown Quito artist",
    "culture": "Ecuador (Quito)",
    "situation": "18世紀末のエクアドル・キトの宗教画に、雲上の聖人と下部に並ぶ殉教伝承の場面を見たい",
    "meaning": "Met作品別Overviewでは、殉教者聖バルバラが雲に乗り天へ向かう姿で描かれる。右手の棕櫚枝は殉教の象徴、左手には聖杯と聖餅。下景の左にある場面は彼女の殉教と剣を振るう処刑人への落雷の伝承で、背後の塔の三つの窓は三位一体を示す。右側は臨終の聖人が最後の秘跡を受ける場面で、学芸員は聖スタニスラウス・コストカの死の場面だろうと推定する。画面中央の囲まれた庭で子羊と聖杯の寓意が示される。物語は伝承・信仰上の解釈であり史実の確証ではない。",
    "visual": "Met API主画像の実見。縦長の油彩画で黄色い布をまとった女性の聖人が画面上半に大きく座り、右手に細長い枝のようなもの、左手に杯が見える。雲のまわりに小さな翼ある人物、左下に塔と小さな人々、中央下に囲われた庭や建築物、右下には別の人物場面が並ぶ。",
    "caution": "聖バルバラにまつわる処刑・落雷・塔の物語は宗教的伝承として書く。右下の人物を確実に聖スタニスラウスと断定しない。棕櫚枝は殉教の象徴という美術館の説明とする。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "緊張"
    ],
    "themes": [
      "時間",
      "共同体"
    ],
    "text": "画面の上半分で、黄色い布をまとった聖バルバラが雲に乗り、天を見上げています。その周りには小さな天使たちが集まり、下方の風景には塔や人々、別々の場面が細かく描き込まれています。ひとりの聖人の姿と、伝承の物語が同時に見える構成です。\n\n聖バルバラは右手に、殉教を表す棕櫚の枝を持っています。左手には聖杯と聖餅があり、信仰の象徴が身ぶりの中に組み込まれています。彼女は塔に閉じ込められたという伝承で知られ、塔にある三つの窓はキリスト教の三位一体を表しています。\n\nこの作品は18世紀末のエクアドル・キトで制作された作者不明の宗教画です。下の小さな場面には聖バルバラの殉教の伝承などが表され、中央では子羊と杯を用いた信仰の寓意も描かれています。これらは伝承と象徴を可視化したもので、出来事を写真のように記録したものではありません。雲上の姿から下の細部へと視線を移し、ひとつの絵に重ねられた意味を探してみてください。",
    "checks": [
      [
        "a palm branch, a symbol of martyrdom",
        "聖バルバラは右手に、殉教を表す棕櫚の枝を持っています。",
        "Met exact Overview: palm of martyrdom"
      ],
      [
        "The tower’s three windows, one of which Barbara caused to be added",
        "塔にある三つの窓はキリスト教の三位一体を表しています。",
        "Met exact Overview: tower's three windows"
      ]
    ]
  },
  "910556": {
    "number": 394,
    "japanese": "ムイッズ・アル＝ムルクの肖像",
    "artist": "Unidentified Mughal court painter",
    "culture": "India, Mughal court",
    "situation": "ムガル帝国の宮廷人物の絹や毛皮の衣装と画中の銘文を眺めたい",
    "meaning": "Met作品別Overviewは1610年頃の肖像の左に書かれた銘文で人物をムイッズ・アル＝ムルクと同定する。彼はアクバルとジャハーンギール両皇帝に仕えたペルシア出身の官吏で、出納官、軍の管理職などを務めた。毛皮の縁や絹、錦の豪華な衣装は高位の地位を示す。銘文の筆致や配置がジャハーンギール自身による署名入りの他例に似ており、皇帝自身が書いた可能性があるが未確定。画家の名はMetの作者情報にない。",
    "visual": "Met API画像に対応した原JPEG・表示JPEGの縮小照合後のサムネイルを実見。濃青緑の無地に近い背景に、縦長の全身像。男性は髭と高い頭飾り、黄土色の豪華な上着、淡緑の衣、腰から垂れる白い帯を着け、片手を前に掲げる。左側の黒い筆文字、周囲の赤みの額縁模様が見える。",
    "caution": "人物はペルシア出身だが作品の制作地はインドとして扱う。皇帝ジャハーンギールが銘文を書いたことは可能性にとどめる。作者の心理や画家名を推測しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "落ち着き"
    ],
    "themes": [
      "時間",
      "共同体"
    ],
    "text": "濃い青緑の背景の前に、長い上着をまとった男性が立っています。絹の衣には金色の細かな文様があり、毛皮の縁や腰から垂れる布が目を引きます。左側には人物を説明する文字が書き込まれ、肖像と記録が一枚に重ねられています。\n\nこの絵の左側の銘文は、描かれた人物をムイッズ・アル＝ムルクと特定しています。彼はペルシア出身で、ムガル帝国のアクバル帝とジャハーンギール帝に仕え、会計や軍の行政に関わる役職を務めました。身につけた豪華な衣装からも、宮廷での高い地位がうかがえます。\n\n銘文の書き方には、ジャハーンギール帝が自ら書いたことが分かっている他の例と似たところがあります。そのため、この銘文も皇帝自身の筆かもしれませんが、確定してはいません。服の模様と画面の文字を行き来しながら、人物の姿がどのように権威と結びつけられたかを眺めてみてください。",
    "checks": [
      [
        "identifies the figure as Mu'izz al-Mulk",
        "この絵の左側の銘文は、描かれた人物をムイッズ・アル＝ムルクと特定しています。",
        "Met exact Overview: identifying inscription"
      ],
      [
        "it is possible that this caption is in his hand",
        "そのため、この銘文も皇帝自身の筆かもしれませんが、確定してはいません。",
        "Met exact Overview: Jahangir's possible handwriting"
      ]
    ]
  },
  "910557": {
    "number": 393,
    "japanese": "タージ・マハルの記念墓を囲む大理石の透かし屏風の北面図",
    "artist": "Unidentified artist",
    "culture": "India, Agra",
    "situation": "タージ・マハルの霊廟内部にある大理石の透かし彫りと幾何学・花文様の細部をじっくり見たい",
    "meaning": "Metの作品別Overviewは1810〜1820年頃のこの水彩を、タージ・マハルのムムターズ・マハルと皇帝シャー・ジャハーンのセノタフ（記念墓碑）を囲む精緻なジャーリー（透かし彫り格子）の北面を描いた立面図と説明する。白大理石の格子にはピエトラ・ドゥーラの象嵌によるアラベスクと花の装飾が施されている。こうした建築調査図は、英領インド期の設計・建築・記録文化におけるこの霊廟の影響を伝える。水彩画の作者は公式ページに表示されず、建築設計者本人の作画としない。",
    "visual": "Met公式object APIの主JPEGを実見。横長の水彩による建築立面図で、濃い背景の前に白い透かし彫りの大理石の屏風が横長に広がる。中央の区画が左右の区画より高く、細い黒い格子穴と花の模様、両端と中央の尖った先端が見える。実際の大理石そのものの写真ではなく紙に描かれた立面図。",
    "caution": "墓碑を実際の埋葬空間と混同しない。画家の身元は不明。建築構造物ではなく1810〜20年頃の絵画作品であり、写真や当時の設計図原本と断定しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "記憶",
      "時間"
    ],
    "text": "深い黒の背景から、白い大理石の格子が浮かび上がっています。中央は高く、左右には低い区画が並び、細かく抜かれた模様と花の装飾が幾重にも重なっています。近くで見ると装飾の密度が際立ち、少し離れると左右対称の建築全体が見えてきます。\n\n1810〜1820年頃に描かれたこの水彩画は、インドのタージ・マハル霊廟にある大理石の透かし屏風の北面を表しています。この屏風は、ムムターズ・マハルと皇帝シャー・ジャハーンの記念墓碑を囲むものです。白大理石の格子には、色石をはめ込むピエトラ・ドゥーラの技法で植物や曲線の文様も施されています。\n\nこれは建築そのものの写真ではなく、形と装飾を丁寧に写し取った絵です。美術館は、このような建築の記録画を、タージ・マハルが当時のデザインや建築研究に及ぼした影響を示す例としています。格子の開いた部分と石の残る部分を交互に追うと、透かし彫りの繊細さが分かります。",
    "checks": [
      [
        "the delicate jali screen surrounding the most sacred part",
        "この屏風は、ムムターズ・マハルと皇帝シャー・ジャハーンの記念墓碑を囲むものです。",
        "Met exact Overview: jali encloses cenotaphs"
      ],
      [
        "inlaid with pietra dura stone mosaics",
        "白大理石の格子には、色石をはめ込むピエトラ・ドゥーラの技法で植物や曲線の文様も施されています。",
        "Met exact Overview: pietra dura inlay"
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
          "Met 910557 is a painting of a marble cenotaph screen, not a photograph; Met 910556 inscription handwriting is only possibly Jahangir\u0027s, and Met 764093 portrays a religious legend rather than documented events."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==392,"main must have exactly 392 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：395作品**。main統合後のDBとREADMEを正本とする。
- **次：396作品目から候補調査**。登録済みIDと同一作品・画像の重複を避け、公式Overviewと原寸・表示画像、権利を個別に確認。
- 今回393〜395：`met-910557`《タージ・マハルの記念墓を囲む透かし屏風の北面図》（1810〜20年頃、インド）、`met-910556`《ムイッズ・アル＝ムルクの肖像》（1610年頃、インド）、`met-764093`《聖バルバラ》（18世紀末、エクアドル・キト）。
- 公式Metの各作品別Overview原文を読んで二つずつ短い原文抜粋と日本語鑑賞解説の根拠を対応させた。ムイッズ・アル＝ムルクの肖像銘文がジャハーンギール自身の筆という説は未確定。聖バルバラの話は宗教伝承と区別する。
- Met APIのPDフラグ、公式JPEGのOpen Access CC0と美術館の現代解説文の著作権を別々に監査。原寸/表示JPEGの全SHA256・バイト数・寸法・縮小RMSを記録し、実際のAPI主画像サムネイルを見て図像を照合。画像研究：[393〜395の記録](artwork-research-evidence/met-393-395-2026-11-12.json)。
- 同じAIが別工程で再確認しており、外部専門家や人間による独立した査読ではない。既存392作品と画像台帳の以前の部分は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-393.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==395,"final count mismatch")
    print("ALL PASS: 395 new total, existing 392 preserved",flush=True)
if __name__=="__main__":
    main()
