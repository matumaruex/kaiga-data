#!/usr/bin/env python3
"""One-off source-reviewed registration for #414-416. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-414-416-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-414-416-20261113/"+EVIDENCE
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
  "853197": {
    "number": 415,
    "japanese": "松竹葡萄栗鼠図",
    "artist": "Unidentified Artist, probably Korean",
    "culture": "Korea and Japan (Joseon period; origin disputed)",
    "situation": "葡萄を食べるリスと松竹を描いた掛軸から、家族の繁栄や長寿を願う東アジアの吉祥図像を読みたい",
    "meaning": "Met個別作品Overviewでは18～19世紀の墨画の制作地が朝鮮か、日本で朝鮮・中国系図像に影響された作家によるものか専門家の間で議論されている。板倉聖哲は民画との様式上の関係から朝鮮18世紀～19世紀初めと推定するが確定していない。画中のリスは左前足で葡萄をつかみ食べ、濃淡や点で毛並みを表す。二本の尻尾があるように見える。葡萄とリスは子孫繁栄を象徴し、松は長寿、竹は忍耐やしなやかな強さを表す。箱書きの中国の禅僧に関する古い帰属は印章と作風が一致せず現在は支持されていない。",
    "visual": "Met公式APIの原寸/表示JPEGを全バイトハッシュとRGB縮小誤差で比較、実画像サムネイルを直接視認。縦長の掛軸の中央には松らしい曲がった幹と葡萄の房・葉が密に重なり、下方の枝にふっくらしたリスがいる。横へ伸びる細い竹の葉と灰墨の地色、枠の紙と上部の墨書が見える。小さな虫や葉の細部の同定は作品別Overviewに基づく。",
    "caution": "制作国・画家の氏名は確定せず、『おそらく朝鮮の画家』というMetの表記を採用し、文化欄はKorea and Japanと記録。箱書きの中国僧の旧帰属を現在の制作者として扱わない。葡萄とリスの象徴は東アジアの画題上の意味であり家庭の実際の事情を推定するものではない。",
    "emotions": [
      "希望"
    ],
    "tones": [
      "落ち着き",
      "静けさ"
    ],
    "themes": [
      "自然",
      "共同体"
    ],
    "text": "松の幹に絡みつく葡萄のつるから、いくつもの房が垂れ下がっています。枝の下には、葡萄を前足で抱えて食べるリス。墨の濃淡と小さな点で表した毛並みを追うと、リスの尻尾は二本あるようにも見えます。松の葉や竹の細い線にも注目してみてください。\n\nこの掛軸では、葡萄とリスの組み合わせが家族の繁栄を象徴します。葡萄の実の多さは実りや子孫を、常緑の松は長寿、竹は折れにくさを表す吉祥の意匠です。動物と植物が一緒になることで、自然の描写にさまざまな願いが重ねられています。\n\n制作は18～19世紀で、朝鮮の画家による可能性があると考えられていますが、日本の画家によるとする見方もあり、産地は確定していません。かつて箱書きから中国の僧に帰属されたこともありましたが、現在は作品の印章や作風と合わないと説明されています。確定していない歴史はそのまま残し、まずは小さなリスと多くの実が結ぶ図柄を眺めてみてください。",
    "checks": [
      [
        "the squirrel seems to have two tails",
        "リスの尻尾は二本あるようにも見えます。",
        "Exact Met Overview: squirrel appears to have two tails"
      ],
      [
        "The juxtaposition of grapes and squirrels symbolizes family prosperity",
        "この掛軸では、葡萄とリスの組み合わせが家族の繁栄を象徴します。",
        "Exact Met Overview: grapes and squirrels for family prosperity"
      ]
    ]
  },
  "853450": {
    "number": 416,
    "japanese": "無原罪の聖母を描いた修道女の胸飾り",
    "artist": "Nicolás Rodríguez Juárez",
    "culture": "Mexico (New Spain, early 18th century)",
    "situation": "18世紀初めのメキシコの修道女が身に着けた絵入り胸飾りから、信仰と装身具の規制が生んだ工芸の工夫を知りたい",
    "meaning": "Met作品別Overviewは1710年頃のニコラス・ロドリゲス・フアレスによる絵入りメダリオン（油彩・金彩の銅板、亀甲と銀の額）と説明。メキシコの無原罪懐胎修道会やヒエロニムス会の修道女は修道誓願の際や重要な宗教祝日に胸の上にこの種の絵を着けた。聖母との誓約を示し、旧約の『雅歌』8:6における『心に印を』の言葉に関連づけられる。教会当局が宝飾品を戒め、聖母像の絵を修道服に着けるよう命じたことをきっかけに大型の絵入り徽章が普及し、有力画家へ発注された。",
    "visual": "Met公式API主JPEGの原寸と表示版を完全ダウンロードしてハッシュと縮小RMSで照合し、実サムネイルを目視。ほぼ正円の広い褐色の亀甲額装と銀色の飾りが外周に並び、中央の小さな円形画面に青衣の聖母が赤や黄の人物と天使に囲まれている。絵そのものと額装、中央の絵と外側の飾りの違いを確認。",
    "caution": "通常のキャンバス画ではなく、銅板に描かれ、銀・亀甲の額を持つ身に着ける円形の宗教的な絵画作品。これが実際に誰という修道女の所有だったかは資料にない。『誓約の象徴』は歴史的宗教的な意味で実際の超自然的効験の主張ではない。",
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
    "text": "丸い褐色の額には、小さな銀色の飾りが幾重にも並んでいます。その中心には、青い衣の聖母を描いた小さな円形の絵があります。外側の光を反射する装飾と、内側の彩色された人物を見比べると、身に着けるための絵画として作られたことが伝わってきます。\n\nこれは1710年頃にメキシコの画家ニコラス・ロドリゲス・フアレスが制作した修道女の胸飾りです。胸の上に着けるこの絵入りの徽章は、聖母との結びつきを表す目印でした。無原罪懐胎修道会やヒエロニムス会の修道女たちは、修道誓願の時や大切な祝祭に、このような徽章を用いました。\n\n教会当局が高価な装身具を制限し、無原罪の聖母の絵を身に着けるよう求めたことも、この徽章の普及につながりました。絵は金彩を加えた銅板に描かれ、周囲は亀甲と銀の額で飾られています。宝飾品の代わりに作られた絵が、やがて独自の美しさを備えていったことを感じられるでしょう。",
    "checks": [
      [
        "Worn over the heart, the badge was the visible symbol",
        "胸の上に着けるこの絵入りの徽章は、聖母との結びつきを表す目印でした。",
        "Exact Met Overview: badge worn over the heart"
      ],
      [
        "Instructed to wear images of the Virgin of the Immaculate Conception",
        "教会当局が高価な装身具を制限し、無原罪の聖母の絵を身に着けるよう求めたことも、この徽章の普及につながりました。",
        "Exact Met Overview: institutional instruction to wear painted Virgin image"
      ]
    ]
  },
  "895417": {
    "number": 414,
    "japanese": "白衣楊柳観音図",
    "artist": "Suzuki Shūitsu 鈴木守一",
    "culture": "Japan (Edo–Meiji transition)",
    "situation": "鈴木守一の絹本に描かれた白衣楊柳観音と、絵で表現した表装の仕掛けをゆっくり鑑賞したい",
    "meaning": "メトロポリタン美術館の作品別Overviewによれば、鈴木守一（1823～1889）は雲上に降りる白衣観音を、片手に柳、もう一方に浄水を収めた瓶を持つ楊柳観音として描いた。柳が病や邪悪を避け、甘露が癒やしをもたらすというのは信仰上の象徴。通常の掛軸表装に見える外側の垂れ（風帯）・藍色の経文帯・大きな蓮華までも、一枚の絹に描いた『描表装』という錯視的な工夫。青い帯は『法華経』観音経を画家自身が金字で書写し、白衣の細い線は胡粉、瓶の液体は薄い雲母、光背の金線は盛り上げて表される。鈴木其一の子として江戸琳派を受け継いだ。",
    "visual": "Met APIから得た原寸と表示用主JPEGの全バイトSHA256・リサイズRMSを照合し実際の主画像サムネイルを視認。非常に縦長で薄い地色の中ほどに白い衣の観音が雲の上に立つ。上部には濃い青の横帯と紐のような垂れが描かれ、下部右に大きな白蓮の花が続き、外側には縞模様の濃い縁取りがある。『表装に見える描写』と実際の外装は区別。",
    "caution": "柳による除災や甘露による治癒を実証された医学的効能として述べない。外側の装飾的表装の多くは絵として描かれている。制作年代はMetの19世紀中〜後期にとどめ、鈴木其一本人の作品と取り違えない。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "時間",
      "自然"
    ],
    "text": "淡い地色の中央に、白い衣をまとった観音が雲の上へ静かに姿を現しています。手には柳の枝と小さな瓶。長く垂れる衣の線や、画面の下で大きく咲く白い蓮をたどると、限られた色彩の中に細かな技が詰まっていることが分かります。\n\nこの作品は、江戸琳派の画風を受け継いだ鈴木守一が19世紀中頃から後半に描いた《白衣楊柳観音図》です。柳の枝は災厄や病を遠ざけると信じられました。瓶に入る甘露も、苦しみを癒やすものとして仏教の図像に用いられています。これらは宗教的な象徴で、実際の治療効果を示すものではありません。\n\n一見すると普通の掛軸の表装に見える部分まで、実際は絹地に描かれた「描表装」です。藍色の帯には守一自身が『法華経』観音経を金色で書き、外側の垂れや下の蓮の花にも、絵と装飾の境界を曖昧にする仕掛けがあります。少し離れて全体を見た後に近づくと、表装そのものが作品の一部として働いていることに気づけます。",
    "checks": [
      [
        "The willow branch is believed to ward off evil and illness",
        "柳の枝は災厄や病を遠ざけると信じられました。",
        "Exact Met Overview: belief concerning willow branch"
      ],
      [
        "are painted using a convention called “painted mounting”",
        "一見すると普通の掛軸の表装に見える部分まで、実際は絹地に描かれた「描表装」です。",
        "Exact Met Overview: painted mounting illusion"
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
          "Met 895417 uses painted silk mounting rather than physical mounting; met-853197 country and old Sotsuon attribution remain unproven; met-853450 is a wearable oil-and-gold copper badge in a tortoiseshell and silver frame rather than canvas."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==413,"main must have exactly 413 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：416作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：417作品目から候補調査**。重複・作品別Met公式Overview原文・JPEG全ファイルの照合・画像利用条件を個別に確認。
- 今回414〜416：`met-895417` 鈴木守一《白衣楊柳観音図》（19世紀中〜後期、日本）、`met-853197`《松竹葡萄栗鼠図》（18〜19世紀、朝鮮か日本かは未確定）、`met-853450` ニコラス・ロドリゲス・フアレス《無原罪の聖母を描いた修道女の胸飾り》（1710年頃、メキシコ）。
- 作品個別Met Overviewの実文面を確認し、二箇所ずつの短い英文と日本語解説の重要主張を照合した。観音の柳・甘露は信仰上の象徴、表装は絹に描かれた『描表装』。松竹葡萄栗鼠図の国・作者は論争中で朝鮮が有力とされるが断定しない。胸飾りは油彩・金彩の銅板画と亀甲・銀の額で、一般的な平面キャンバス画ではない。
- Met作品PD、公式JPEGのOpen Access CC0、現代の美術館解説文の著作権を分離して監査。原寸/表示JPEGの全SHA256とファイルサイズ、画像寸法、縮小RMS、同一公式画像のサムネイル実見は[414〜416画像調査](artwork-research-evidence/met-414-416-2026-11-13.json)に記録。研究ファイルには登録対象外となった候補も含む。
- 作品別の別工程確認は同一AIによるもので、独立した人間・専門家・別AIによる検査ではない。既存413作品と過去の画像台帳部分は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-414.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==416,"final count mismatch")
    print("ALL PASS: 416 new total, existing 413 preserved",flush=True)
if __name__=="__main__":
    main()
