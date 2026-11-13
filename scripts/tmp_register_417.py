#!/usr/bin/env python3
"""One-off source-reviewed registration for #417-419. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-417-419-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-417-419-20261113/"+EVIDENCE
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
  "317829": {
    "number": 419,
    "japanese": "四面の絵を持つ携帯用二連イコン",
    "artist": "Unidentified Amhara or Tigrinya artist",
    "culture": "Ethiopia (Amhara or Tigrinya peoples)",
    "situation": "エチオピアの首から下げられる小さな宗教画で、聖母子と聖ゲオルギウス、裏面の受難や復活をつなぐ仕組みを知りたい",
    "meaning": "Metの個別Overviewは18世紀初めのエチオピアの二連の両面イコンとして、首から紐で下げて持ち歩く貴族の個人信仰用具と解説する。表と裏・外側のふたを合わせてキリスト教主題が四面描かれる。主画像の開いた片側には聖母子と剣を持つ大天使たち、左の内ふたには白馬に乗り竜を倒す聖ゲオルギウス。裏側には十字架上のキリストと両脇の聖母マリア、聖ヨハネ、別の面にはアダムとエヴァを起こす復活のキリスト。主画像だけで四面すべてが見えると誤解させない。エチオピアのゴンダールで17世紀後半に発達した、黒い太い輪郭と平面的なピンク・橙色の顔彩の様式を示す。",
    "visual": "Met公式APIの原寸・表示用の実JPEG全バイトハッシュ、寸法、縮小RMSを記録し、主画像サムネイルを直接視認。展示用の灰色背景の前に小さい絵入り木製容器が左右に開いており、左の小板には白馬で竜へ槍を向ける聖ゲオルギウス、右には正面を向く聖母子と左右の天使。外枠の黄色～金の縁、上部の筒状の吊り紐部分も見える。裏側の十字架や復活の絵はこの主JPEGでは見えない。",
    "caution": "同じエチオピアでも既登録met-309529の別作品（1997.81.1対68.128）なので画像と所蔵番号で区別。写真に写るのは開いた片面の二画面だけで、裏側の主題は公式Overviewを根拠に記述する。宗教的伝承の場面を史実だと断定しない。作者の氏名や特定宗派内の所有者は不明。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "小さな木の扉を開くと、左右に異なる宗教画が見えます。左には白馬に乗り槍を構える聖ゲオルギウス、右には幼いキリストを抱く聖母マリアと天使たち。人物の黒い輪郭と鮮やかな赤や金色が、手のひらほどの画面を印象深くしています。\n\nこれは18世紀初めのエチオピアで作られた携帯用のイコンです。紐で首から下げて持ち歩く個人用の宗教画として使われました。両面を合わせると四つの宗教的な場面が描かれ、聖母子や竜を倒す聖ゲオルギウスのほか、反対側にはキリストの磔刑や復活も表されています。\n\n今表示されている主画像には、開いた片側の二画面だけが写っています。エチオピアのゴンダールで発達した、太い輪郭線と平面的な色彩の様式も見どころです。身に着けるほど小さな品に、信仰の物語が幾重にも収められていることを想像してみてください。",
    "checks": [
      [
        "pendant icons worn suspended by a cord around the neck",
        "紐で首から下げて持ち歩く個人用の宗教画として使われました。",
        "Exact Met artwork Overview: suspension by neck cord"
      ],
      [
        "The double-sided pendant contains four painted surfaces depicting Christian subject matter",
        "両面を合わせると四つの宗教的な場面が描かれ",
        "Exact Met artwork Overview: four painted Christian surfaces"
      ]
    ]
  },
  "440727": {
    "number": 417,
    "japanese": "広い谷を見下ろすドイツの風景",
    "artist": "Fritz Petzholdt",
    "culture": "Danish painter, German landscape",
    "situation": "19世紀のデンマーク人画家が描いた静かなドイツの丘陵風景で、手前の崖と遠い山を見比べたい",
    "meaning": "メトロポリタン美術館の個別Overviewは、デンマーク黄金時代の絵画を牽引したクリストファー・ヴィルヘルム・エッカースベルグの弟子の中で、フリッツ・ペッツホルトが風景画に専念した唯一の画家だったと説明。この小さな風景の正確な場所は未確定だが、1829年と翌1830年に彼がスケッチをしたドイツで制作されたとみられる。作品は1829〜30年頃の紙に油彩で描いた画で、後にキャンバスへ貼り付けられている。ドイツの特定都市や谷の名前を推測しない。",
    "visual": "Metの原寸・表示JPEGのSHA256/サイズ/寸法/縮小RMSを確認し、実主画像のサムネイルを視認。横長の絵で左側の前景に褐色の切り立った丘、上面に緑の草と低い樹木、中央から右の奥に深く続く谷と霞む低山、上に淡い灰色の雲の空が見える。明るい右側と暗い左の崖に注目。近景には小さな道らしい線もあるが位置は特定しない。",
    "caution": "作者はデンマーク人、制作対象はドイツのどこかという区別。正確な描画場所はMet公式も未特定で、特定の村や渓谷を断定しない。作品の支持体は紙に油彩で後からキャンバスに貼ったもの。",
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
    "text": "手前には、草の生えた褐色の崖が横たわり、その奥へ緑の谷と低い山並みが続いています。左の暗い斜面から右の明るい遠景へ目を移すと、小さな画面の中にも広い空気が感じられます。雲の下には、遠い丘が淡く重なっています。\n\nこの絵は1829～30年頃、デンマーク人画家フリッツ・ペッツホルトが描いた風景画です。彼はデンマーク絵画の黄金時代を代表するエッカースベルグの弟子で、その門下では珍しく、風景画に専念した画家でした。紙に油彩で描かれ、のちにキャンバスへ貼り付けられています。\n\n美術館によると、描かれた場所の正確な位置はまだ分かっていません。ただし、画家が1829年と翌年に訪れてスケッチしたドイツの風景と考えられています。名前の分からない谷であっても、崖の近さと山の遠さを見比べるだけで、画家が捉えた景色の広がりを楽しめます。",
    "checks": [
      [
        "only Petzholdt devoted himself exclusively to landscape",
        "その門下では珍しく、風景画に専念した画家でした。",
        "Exact Met artwork Overview: exclusive devotion to landscape"
      ],
      [
        "the precise location of this small view has not been determined",
        "描かれた場所の正確な位置はまだ分かっていません。",
        "Exact Met artwork Overview: geographic location remains unknown"
      ]
    ]
  },
  "898273": {
    "number": 418,
    "japanese": "薔薇の枝にとまるナイチンゲール（両面彩飾葉）",
    "artist": "'Abdullah Bukhari",
    "culture": "Turkey (probably Istanbul, Ottoman Empire)",
    "situation": "18世紀オスマン帝国の薔薇とナイチンゲールの絵を、恋の詩に登場する『愛する者と愛される者』の象徴として見たい",
    "meaning": "Metの個別Overviewによると、『薔薇とナイチンゲール』は15〜18世紀のオスマンの恋愛詩で『愛する者と愛される者』を象徴する組み合わせである。画面の主画像は薔薇と鳥が描かれたアルバムの葉の片面を写し、裏面（verso）にはチューリップなどの花がある。鮮明な緑の尖った葉と、鳥や花を写実的に描く技法は1720年代以降のイスタンブール絵画の特徴。作者アブドゥッラー・ブハーリーの署名があり、収集家用アルバムの絵を多く描いた画家として美術館が説明。制作都市は『おそらくイスタンブール』にとどまる。",
    "visual": "Met公式object APIの主原寸/表示JPEGを全バイト取得してSHA256と縮小RMSを検査し、実際の主画像サムネイルを確認。縦長の紙面に青と白の波紋模様の大きなマーブル紙の縁。金色の細い二重枠の内側に小さな薔薇の枝があり、ピンクの蕾や開きかけの花の横に一羽の灰色の小鳥が横向きに止まっている。題名は『二羽のナイチンゲール』だが主JPEGには一羽が明瞭で、両面のすべての画像が写るわけではない。",
    "caution": "主JPEGは両面のうち薔薇と鳥を描いた片面のみ。裏面のチューリップを画像に直接写っていると説明しない。鳥の種や詩の具体的な一篇を断定せず、詩の伝統上の象徴として解説。制作地はMetの『おそらくイスタンブール』。",
    "emotions": [
      "慈しみ"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "愛情",
      "自然"
    ],
    "text": "青く波打つ模様の紙の中央に、小さな薔薇の枝が描かれています。蕾のそばには灰色の小鳥が止まり、花や葉の形は細い線で丁寧に表されています。周囲の華やかな紙の模様と、中央の静かな自然の描写を見比べてみてください。\n\nこの作品は、18世紀のオスマン帝国で活躍したアブドゥッラー・ブハーリーによる彩飾画です。薔薇とナイチンゲールは、当時の恋愛詩において「愛する者と愛される者」を象徴する組み合わせでした。鳥と花を写実的に描き、尖った緑の葉を配する表現は、1720年代からイスタンブールで発展した絵画の特徴とされています。\n\n画家は、収集家向けのアルバムに収める絵も多く制作しました。この作品も両面に絵のあるアルバムの一葉で、裏面にはチューリップなどの花が描かれています。ここに表示される主画像は薔薇のある片面です。花と小鳥の間のわずかな距離に、古い詩が重ねた意味を思い浮かべてみてください。",
    "checks": [
      [
        "symbolizing the \"loved and beloved one\"",
        "薔薇とナイチンゲールは、当時の恋愛詩において「愛する者と愛される者」を象徴する組み合わせでした。",
        "Exact Met artwork Overview: love-poetry symbolism"
      ],
      [
        "who mainly painted scenes for collectors’ albums",
        "画家は、収集家向けのアルバムに収める絵も多く制作しました。",
        "Exact Met artwork Overview: artist's collectors album production"
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
          "Met 440727 precise view location is uncertain; Met 898273 is double-sided and the primary JPEG only depicts the rose and nightingale side; Met 317829 depicts four icon surfaces but the primary JPEG only depicts two of them and this is not the older registered Ethiopian met-309529."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==416,"main must have exactly 416 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：419作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：420作品目から候補調査**。Metの作品別Overview、既登録作品と画像の重複、原寸/表示JPEGと権利の照合を作品ごとに継続。
- 今回417〜419：`met-440727` ペッツホルト《広い谷を見下ろすドイツの風景》（1829〜30年頃、デンマーク人画家によるドイツの風景）、`met-898273` アブドゥッラー・ブハーリー《薔薇とナイチンゲールの彩飾葉》（1725〜45年頃、オスマン帝国）、`met-317829`《四面の絵を持つ携帯用二連イコン》（18世紀初頭、エチオピア）。
- 個別Met Overviewの原文を実際に読み、短い英文2箇所ずつと独自日本語解説の対応主張を照合。ペッツホルトの風景の正確な場所は未特定、オスマンのアルバム葉は両面で主JPEGに見えるのは薔薇のある片側、エチオピア携帯イコンは四面あるが主JPEGには一方の二面だけ。
- Met APIで作品PD、公式Open Access JPEGのCC0、現代の美術館解説文の著作権を分けた。原寸・表示JPEGの全SHA256・サイズ・寸法・縮小RMSと、作品IDに紐づくサムネイルの直接実見を[417〜419画像調査](artwork-research-evidence/met-417-419-2026-11-13.json)に記録。研究には重複や画像URL不良で除外した候補も含む。
- 二次監査は同じAIが別工程で行ったもので、外部専門家・人間・別AIによる独立査読ではない。既存416作品と過去の画像台帳は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-417.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==419,"final count mismatch")
    print("ALL PASS: 419 new total, existing 416 preserved",flush=True)
if __name__=="__main__":
    main()
