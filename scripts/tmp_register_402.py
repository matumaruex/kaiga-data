#!/usr/bin/env python3
"""One-off source-reviewed registration for #402-404. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-402-404-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-402-404-20261113/"+EVIDENCE
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
  "441967": {
    "number": 403,
    "japanese": "ハリングダールを望む風景",
    "artist": "Johan Christian Dahl",
    "culture": "Norway (Romantic landscape painting)",
    "situation": "山に囲まれたノルウェーの谷の夕空を眺めながら、画家が実際に歩いた場所を想像したい",
    "meaning": "Met作品別Overviewによるとノルウェー出身のヨハン・クリスチャン・ダール（1788～1857）は祖国の風景に親しみ、精神性を帯びた自然主義的なロマン主義風景を描いた。画家自身の日記では1844年8月23日に子どもたちと画家ペーダー・バルケとともにハリングダールを訪れスケッチした。同年10月には考古学者クリスチャン・ユルゲンセン・トムセンにこの作品を贈る意向を示した（offerした）と美術館が説明する。画面の特定の日没時刻やその場で油彩を完成させたことは判明しない。",
    "visual": "実際のMet公式原寸・表示JPEGから生成したサムネイルを目視確認。横長の油彩で濃い青灰色のノルウェー山々が幾重にも重なり、中心には谷。上部の雲の切れ間に桃色から金色の光、手前に針葉樹の梢や茶色い土の丘、右手の森が暗く描かれる。落日のように見えるが光源の時刻を厳密には断定しない。",
    "caution": "1844年の訪問日はダールの日記に基づくMetの情報。絵を描いた正確な日や現地で仕上げたかどうかまでは未確定。10月の相手への『申し出』と実際の贈呈完了を区別する。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "自然",
      "記憶"
    ],
    "text": "谷の奥へと、青灰色の山並みが幾重にも続いています。手前の木々は暗く、雲の切れ間には淡い桃色の光が残ります。山に囲まれた風景の広さと、足元に近い小さな木の姿を見比べると、遠くを眺める感覚が伝わってきます。\n\nこの風景を描いたのはノルウェーの画家ヨハン・クリスチャン・ダールです。彼は1844年8月23日、子どもたちと画家ペーダー・バルケを伴って、ハリングダールを訪れたことを日記に記しました。作品は同じ1844年の油彩画で、故郷の自然に対するダールの関心と、ロマン主義的な風景表現を示しています。\n\n同年10月、ダールは考古学者クリスチャン・ユルゲンセン・トムセンにこの作品を贈ることを申し出ました。ただし、絵を訪問当日に完成させたという記録ではありません。手前の暗い森から空の明るい部分へ視線を動かしながら、実際の旅の記憶が絵になった様子を想像してみてください。",
    "checks": [
      [
        "visited Hallingdal on August 23, 1844",
        "彼は1844年8月23日、子どもたちと画家ペーダー・バルケを伴って、ハリングダールを訪れたことを日記に記しました。",
        "Exact Met Overview: painter's dated diary journey"
      ],
      [
        "That October, Dahl offered this work to Christian Jürgensen Thomsen",
        "同年10月、ダールは考古学者クリスチャン・ユルゲンセン・トムセンにこの作品を贈ることを申し出ました。",
        "Exact Met Overview: offer to antiquarian Thomsen"
      ]
    ]
  },
  "853890": {
    "number": 402,
    "japanese": "狩猟図屏風",
    "artist": "Unidentified Korean artists",
    "culture": "Korea (Joseon dynasty)",
    "situation": "朝鮮時代の八曲狩猟図屏風で、騎馬の人々や珍しい動物を描いた想像力と身分表現を見たい",
    "meaning": "Metの個別作品Overviewによれば18～19世紀に狩猟は朝鮮の物語絵の題材となり、屏風は両班の武官に人気だった。本作は19世紀の八曲屏風で、疾走する馬に乗る男女が鹿・虎・猿・象を追う。右側の大きな人物と日傘のような覆いはその随行団での高位を示す。衣装と疎らな北方の山地から隣接する満洲系の人々を想像して描いた可能性があり、朝鮮半島にいない猿や象を含むため実際の狩猟を正確に記録した絵ではないと所蔵館が説明。",
    "visual": "Met公式APIの原寸と表示JPEGを実際に取得し、全画面のサムネイルを視認した。横長の八曲屏風に淡褐色の上部画面と白い下部余白があり、それぞれの扇に騎馬の人物、散在する動物、山の細かな線。画面右端にも人物の集団。サムネイルでは各動物の同定が困難なため、鹿・虎・猿・象の種類は公式Overviewに基づく。",
    "caution": "『満洲の人々の北方狩猟』は所蔵館の推定であり現実の現場記録や人物の身元とは断定しない。屏風の八つの扇を別々の八作品として登録しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい"
    ],
    "themes": [
      "自然",
      "共同体"
    ],
    "text": "横に長く広がる八曲屏風の中で、人々が馬を走らせ、動物を追っています。細い筆線で描かれた人物は小さいものの、画面のあちこちで違う動きが生まれています。右側では、周囲より大きく描かれた人物と、その上に差しかけられた覆いが目を引きます。\n\nこの作品は19世紀の朝鮮で描かれた狩猟図です。男性だけでなく女性も馬に乗り、鹿や虎などを追う姿が描かれています。狩猟画は当時、武官を含む両班層に好まれる屏風の題材でした。右端の人物が大きく描かれているのは、随行団の中での重要さを強調するためと説明されています。\n\n画中には、朝鮮半島に生息する鹿や虎だけでなく、猿や象も登場します。そのため美術館は、実際の狩猟を記録したというより、狩りの名手とされた満洲の人々を想像して描いた場面と考えています。騎馬の列をたどりながら、現実の風景と物語的な誇張が混ざる面白さを見てみてください。",
    "checks": [
      [
        "men and women on galloping horses stalking deer",
        "男性だけでなく女性も馬に乗り、鹿や虎などを追う姿が描かれています。",
        "Exact Met Overview: mounted women and men on the hunt"
      ],
      [
        "the image is a fanciful fiction grounded in the Manchus’ reputation",
        "そのため美術館は、実際の狩猟を記録したというより、狩りの名手とされた満洲の人々を想像して描いた場面と考えています。",
        "Exact Met Overview: imaginative Manchu hunting scene"
      ]
    ]
  },
  "854905": {
    "number": 404,
    "japanese": "阿閦如来（アクショービヤ）",
    "artist": "Unidentified Newari artist working in Tibet (per Met)",
    "culture": "Central Tibet (Vajrayana)",
    "situation": "チベット仏教の古い彩色布画で、青い阿閦如来と周囲の小さな仏たちに込められた知恵と方角の意味を知りたい",
    "meaning": "Met作品別Overviewは13世紀から14世紀初頭の中央チベットの布画について、阿閦如来を『不動の者』といい、金剛乗仏教における五智如来の一尊とする。青い身体、金剛杵（ヴァジュラ）の持物、東方を守護する役割を説明し、怒りを鎮めて智慧へ変容させる力の象徴と解説する。五智如来を表す一組の絵の一枚として祀られたという位置づけ。作者名は不明でMetの詳細欄ではチベットで働いたネワール系の画家とされる。近代にはチベット学者ジュゼッペ・トゥッチの調査旅行で収集されたが収集時期は1928～1948年の調査期間に限定して記す。",
    "visual": "Met公式APIと同一の原寸と表示JPEGを全バイト照合し、実際のサムネイルを視認。縦長の布画の中央に大きく青い仏が座り、赤い装飾の光背や座、左右の細身の人物、周囲の枠には小さな仏の像が多数段になって描かれる。密な細線と赤・金・青の対照が目立つ。小画像のみでは手の持物の細部は判読困難なため公式本文に従う。",
    "caution": "怒りを必ず消すという医学的・心理学的な効果の主張ではなく信仰上の象徴として扱う。画面に五智如来が全員大きく並ぶとはせず、セットを構成する一幅というMetの説明に従う。作者名は特定されていない。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "時間",
      "共同体"
    ],
    "text": "濃い青色の仏が、装飾された台座の中央に静かに座っています。赤い光背を囲んで小さな仏たちの姿が幾段にも並び、細かな模様が画面を埋めています。中心の大きな姿から周囲へ目を移すと、一枚の絵の中に多くの存在が秩序立てて配置されていることが分かります。\n\n阿閦如来は、その名に「不動の者」という意味を持つチベット仏教の尊格です。五智如来のひとりで、東方を守護し、金剛杵を持つ青い姿で表されます。怒りを鎮め、智慧へと変えていく力の象徴として理解されてきました。これは信仰上の意味であり、実際の効能を証明するものではありません。\n\nこの布画は13世紀から14世紀初頭に制作されました。美術館は、もともと五智如来を表す一組の絵の一枚だったと説明しています。作者の氏名は不明で、チベットで活動したネワール系の画家に結びつけられています。中央の青と周囲の赤を見比べると、古い仏教絵画の色と配置の工夫が感じられます。",
    "checks": [
      [
        "the power to pacify aggression and transmute it into wisdom",
        "怒りを鎮め、智慧へと変えていく力の象徴として理解されてきました。",
        "Exact Met Overview: transmuting aggression into wisdom"
      ],
      [
        "Akshobhya displays the vajra, serves as the protector of the East",
        "五智如来のひとりで、東方を守護し、金剛杵を持つ青い姿で表されます。",
        "Exact Met Overview: Akshobhya's vajra and eastern direction"
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
          "Met 853890 portrays a fanciful hunting story rather than historical Manchu field evidence; Met 441967 offered his painting, not definitely delivered; 854905 represents Buddhist wisdom symbolism, not established therapeutic efficacy."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==401,"main must have exactly 401 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：404作品**。mainへの統合後、作品DBとREADMEを正本とする。
- **次：405作品目から候補調査**。重複・Metの個別作品Overview・原寸と表示画像の同定・画像権利を作品ごとに確認。
- 今回402〜404：`met-853890`《狩猟図屏風》（19世紀、朝鮮）、`met-441967` ダール《ハリングダールを望む風景》（1844年、ノルウェー）、`met-854905`《阿閦如来》（13世紀～14世紀初頭、中央チベット）。
- 公式作品別Overview原文を実際に読んで各2件ずつ短い引用と日本語本文の主張を照合。朝鮮の狩猟図の満洲の人々は推定であり実録としない。ダールの1844年の旅と贈呈の申し出を区別。阿閦如来の宗教的効果を実証的効能とはしない。
- Met作品のPD表示、公式画像のOpen Access CC0と現在の美術館の解説文の著作権を分離。公式原寸・表示JPEGの全SHA256・バイト数・画像寸法・縮小RMSと、API主画像サムネイルの実見は[402〜404画像調査](artwork-research-evidence/met-402-404-2026-11-13.json)に保存。研究記録には今回登録しなかった予備候補も含む。
- 作品別の再審査は同じAIによる別工程で、外部専門家・人間・別モデルの独立査読ではない。既存401作品と以前の画像台帳の記録は不変。
"""
    temp=ROOT/"tmp-artwork-resume-402.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==404,"final count mismatch")
    print("ALL PASS: 404 new total, existing 401 preserved",flush=True)
if __name__=="__main__":
    main()
