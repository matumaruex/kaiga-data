#!/usr/bin/env python3
"""One-off source-reviewed registration for #411-413. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-411-413-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-411-413-20261113/"+EVIDENCE
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
  "49079": {
    "number": 411,
    "japanese": "山水図",
    "artist": "Soga Shōhaku",
    "culture": "Japan (Edo period)",
    "situation": "曽我蕭白の初期の山水図で、中国風の楼閣と山並みを見ながら画風の変化を感じたい",
    "meaning": "メトロポリタン美術館の個別Overviewは、1761～63年頃に曽我蕭白が30代初めに制作した山水図として、狩野派の技術的な影響と、湖畔に中国風の楼閣を配し背景に急峻な山を描く構図を指摘する。のちの奇抜な蕭白の絵と異なる保守的な筆づかいゆえに真作を疑う研究者もいるが、作品の署名と印章は初期の作品であることを示すと学芸員は判断する。帰属に議論があった経緯は隠さず、所蔵館の現在の帰属を明示する。",
    "visual": "Met APIの原寸・表示JPEGを完全取得し、SHA256と縮小RGB RMSで照合。公式主画像の縮小版を直接確認。淡い黄土色の横長画面に、中央付近の複数の緑色の重なる険しい山があり、左の湖畔と右の樹木・屋根のある楼閣が見える。濃い山の輪郭と薄い遠山の対比、画面の右上に小さな落款と印が見える。",
    "caution": "題名は一般的な山水図。作者帰属には過去に異論が出たが、Met公式個別ページの現在の表記は曽我蕭白本人。前年登録のmet-39581《滝を眺める中国の文人》は蕭白の追随者による別の二曲屏風であり、本作とは別。同題の別山水図と混同しない。",
    "emotions": [
      "安心"
    ],
    "tones": [
      "静けさ",
      "落ち着き"
    ],
    "themes": [
      "自然",
      "時間"
    ],
    "text": "淡い地の中から、濃い墨と緑で描かれた険しい山が重なって立ち上がっています。山裾には水辺が広がり、右側には木立と中国風の建物が小さく見えます。山の力強い輪郭と、遠景のかすかな色の違いをたどると、奥行きのある風景が広がります。\n\n江戸時代の画家・曽我蕭白が、1761～63年頃に描いた山水図です。この作品には、狩野派の技法から学んだ跡が見られます。湖畔の楼閣と急峻な山を組み合わせた構図には、のちに蕭白が好んだ表現の兆しも見つけられます。\n\n後年の奔放な筆づかいに比べて穏やかなため、かつては作者を疑う意見もありました。しかし、署名と印章は初期の蕭白作品であることを示すと美術館は説明しています。激しい個性を感じる後年の絵と比べると、画家が画風を作っていった道のりも想像できます。",
    "checks": [
      [
        "demonstrates his indebtedness to Kano School technique",
        "この作品には、狩野派の技法から学んだ跡が見られます。",
        "Exact Met Overview: indebtedness to Kano School technique"
      ],
      [
        "the signature and seal all point to work of his early career",
        "しかし、署名と印章は初期の蕭白作品であることを示すと美術館は説明しています。",
        "Exact Met Overview: signature/seal and early-career attribution"
      ]
    ]
  },
  "382608": {
    "number": 413,
    "japanese": "花とカタツムリと昆虫の静物",
    "artist": "Joris Hoefnagel",
    "culture": "Netherlandish (Antwerp-born artist)",
    "situation": "小さな花束に描かれたカタツムリと蝶や虫の繊細さを見ながら、母に捧げた絵の意味を知りたい",
    "meaning": "Met作品別Overviewによるとヨーリス・フーフナーヘルの1589年制作の小品は16世紀末の精確な自然観察を示す。花束の左右対称の配置は当時の好みに沿い、一部の花の大きさの差と他作品でのモティーフ再利用から、個々の花を別々に観察した習作を組み合わせた可能性が高い。台座のラテン語銘文は母への『愛の記念』として制作したと示す。単なる植物図鑑ではなく親しい相手への個人的献呈として描かれたが、誕生日の贈り物だったかどうかはMet作品個別Overviewからは確定しない。",
    "visual": "Met APIの原寸と表示JPEGを全ダウンロードしてSHA256・バイト数・寸法・縮小RMSを照合し、実際の公式サムネイルを確認。縦長の小さな画面中央に大きなピンク色のバラと青い小花、周囲にクリーム色の花。下部の丸い花器には翅を広げた虫、左右の縁には小さな蝶やトンボに似た虫、右上に殻のあるカタツムリ。最下部に黒地に金色のラテン語銘文がある。実物はヴェラムへの水彩・不透明水彩・金彩で油彩ではない。",
    "caution": "母に宛てた献呈は銘文で確認できるが、特定の記念日、花それぞれの象徴、実物の植物の分類を推測で断定しない。メトロポリタン美術館の言う個々の花の研究の組み合わせは根拠ある推察。制作は1589年、個々のモチーフと贈り先の話を区別。",
    "emotions": [
      "慈しみ"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "愛情",
      "自然",
      "記憶"
    ],
    "text": "小さな画面いっぱいに、淡いピンクの大きな花と青い小花が咲いています。周囲にはカタツムリや蝶などの虫が集まり、下の花器にも羽を広げた虫の姿があります。一見すると整った花束ですが、細部を見ていくと、それぞれの生き物が違う形で描き分けられています。\n\n1589年にネーデルラント出身の画家ヨーリス・フーフナーヘルが描いた作品です。個々の花を別々に観察して描いた習作を組み合わせ、花束の構図にしたと考えられています。精密な自然の描写と、左右の釣り合いを意識した配置が特徴です。\n\n台座のラテン語銘文によれば、この作品は母に捧げる「愛の記念」として描かれました。花や虫の形を詳しく記録するだけでなく、親しい相手を思う気持ちも込められた絵です。画面の下の文字から花束へと視線を戻すと、静物の意味が少し違って見えてきます。",
    "checks": [
      [
        "he used individual flower studies to form his bouquet",
        "個々の花を別々に観察して描いた習作を組み合わせ、花束の構図にしたと考えられています。",
        "Exact Met Overview: combined individual flower studies"
      ],
      [
        "made this drawing for his mother ‘as a monument of love’",
        "この作品は母に捧げる「愛の記念」として描かれました。",
        "Exact Met Overview: Latin inscription dedicates image to mother"
      ]
    ]
  },
  "901386": {
    "number": 412,
    "japanese": "コーエン家の屋上から望むテトゥアン",
    "artist": "David Roberts",
    "culture": "Morocco (Tétouan), depicted by a British Scottish painter",
    "situation": "1833年のモロッコの街を屋上から描いた横長の水彩画で、建物・人々・小さな祝祭の気配を眺めたい",
    "meaning": "Met個別Overviewによれば英国スコットランド出身のデイヴィッド・ロバーツは1833年の初めての北アフリカ旅行中にテトゥアンを訪れた。地元のイスラム当局への登録が必要と知り、セファルディ系ユダヤ人共同体のつながりを通じコーエン家に滞在先と保護を得た。滞在8日間に屋上を中心に数点を描き、うち4点は後にトマス・ロスコーの『スペインとモロッコ』（1838年）の挿絵版画に使われた。屋上の格子状の構造物には植物と布が見え、訪問が過越祭の時期と重なるため音楽が祭りに関係する可能性を美術館が示すが、確定事実にはしない。",
    "visual": "Met公式APIの主画像の実JPEGを取得し、原寸・表示のサイズ、全SHA256と縮小RMSを照合。横長の明るい灰茶色のモロッコの屋根と街並みが遠くまで広がり、左に立つ少人数の人物、画面右寄りに濃い色の小さな人々が集まる屋上の格子と布、遠景に淡い山並みがある。水彩は紙の余白に近い淡色で、写真ではなく画家の観察による描写。",
    "caution": "作者はスコットランド出身でありモロッコ生まれの画家としない。過越祭に関連した奏楽かどうかはMetが『かもしれない』とする仮説。作品は水彩素描であって油彩写真ではない。絵がどこまで正確な街の測量を再現するか断定しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "にぎわい"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "明るい空の下に、淡い色の建物の屋根が遠くまで続いています。広い街並みの中で目を凝らすと、屋上に集まった小さな人々や、布を掛けた格子状の場所が見つかります。手前から遠くの山まで、薄い水彩の重なりで表されています。\n\nスコットランド出身の画家デイヴィッド・ロバーツは、1833年に初めて北アフリカを訪れ、この眺めを描きました。モロッコのテトゥアンでは、地元のユダヤ人共同体とのつながりを通じてコーエン家に滞在し、屋上などから街の景色をスケッチしました。作品は1833年4月10日付の水彩画です。\n\n画家の訪問がユダヤ教の過越祭と重なっていたため、美術館は画中の奏楽が祭りに関係した可能性を示しています。ただし、実際にどの行事だったかは分かりません。屋上の人影を探してから街全体に目を戻すと、日々の暮らしの一場面と広い都市の姿を同時に感じられます。",
    "checks": [
      [
        "Roberts made this panoramic view during his first visit",
        "ロバーツは、1833年に初めて北アフリカを訪れ、この眺めを描きました。",
        "Exact Met Overview: first North Africa visit"
      ],
      [
        "the musicians may be performing for a related celebration",
        "美術館は画中の奏楽が祭りに関係した可能性を示しています。",
        "Exact Met Overview: Passover-period music only a possibility"
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
      "creation_date_display":spec.get("date_display",api["objectDate"]),"type":"Painting",
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
          "Met 49079 signature and seal support original early Soga Shōhaku despite previous doubts; Met 901386 Passover music is a curatorial possibility rather than an established event; Met 382608 is a miniature watercolor dedication to the artist’s mother, not an oil canvas."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==410,"main must have exactly 410 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：413作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：414作品目から候補調査**。既登録ID・同画像SHA・作品別のMet Overview・画像原寸/表示と権利を個別に検証する。
- 今回411〜413：`met-49079` 曽我蕭白《山水図》（1761〜63年頃、日本）、`met-901386` デイヴィッド・ロバーツ《コーエン家の屋上から望むテトゥアン》（1833年、モロッコを描いたスコットランド人の水彩）、`met-382608` フーフナーヘル《花とカタツムリと昆虫の静物》（1589年、ネーデルラント）。
- 個別Met作品ページのOverview本文を実際に確認し、作品ごとに短い原文引用二箇所を独自日本語解説の主張と対応付けた。49079は過去に帰属異論がある一方、署名・印章からMetは蕭白の初期作とする（前回登録の追随者の別作品と混同しない）。901386の過越祭の音楽は仮説と扱い、382608の母への献呈はラテン語銘文から説明。
- 作品PD表示・Met公式JPEGのCC0 Open Access・美術館現代解説文の権利を別々に扱い、原寸/表示JPEGの全SHA256、バイト数、寸法、縮小RMS、API画像の実見を保存。研究記録：[411〜413画像調査](artwork-research-evidence/met-411-413-2026-11-13.json)。研究ログには今回未登録のモロッコの写本候補も含む。
- 二次監査は同じAIによる別工程で、独立した人間・専門家・別モデルの査読ではない。既存410作品と過去の画像台帳の記録は不変。
"""
    temp=ROOT/"tmp-artwork-resume-411.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==413,"final count mismatch")
    print("ALL PASS: 413 new total, existing 410 preserved",flush=True)
if __name__=="__main__":
    main()
