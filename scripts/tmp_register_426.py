#!/usr/bin/env python3
"""One-off source-reviewed registration for #426-428. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-426-428-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-426-428-20261113/"+EVIDENCE
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
  "437180": {
    "number": 426,
    "japanese": "アダムとエヴァへの叱責",
    "artist": "Charles Joseph Natoire",
    "culture": "France (eighteenth-century history painting)",
    "situation": "エデンの園で叱責されるアダムとエヴァの姿を、涙や身振りと18世紀フランスの絵画表現から読みたい",
    "meaning": "Metの作品別Overviewは、1740年の銅板油彩をシャルル＝ジョゼフ・ナトワールが師フランソワ・ルモワーヌをたたえるために描いたとみられる作品として紹介する。大きさ・支持体が同じルモワーヌの別作品（禁断の果実をエヴァから受け取るアダムの場面）と対になる。絵では上方から天使と神がアダムとエヴァを叱責する。エヴァの頬に光る一粒の涙と柔らかな肌の赤みは、アダムの引き締まった筋肉と対照をなす。師への献呈の意図は所蔵館の解釈で、作者自身の記録の引用ではない。宗教物語の出来事を史実として断定しない。",
    "visual": "Met公式APIによる同一作品の原寸・表示JPEGを全バイトで照合、縮小RMSと実際の主画像サムネイルを確認した。縦長の銅板絵画。上部左には雲に囲まれ赤い布を背にした厳しい表情の大きな人物、その下には翼ある使者。画面下部にエヴァが座り、右のアダムが両手を合わせる。二人の足元には動物と草があり、右上の木と遠くの風景が奥行きを生む。小画像の涙の細部はMetの解説に基づく。",
    "caution": "ルモワーヌの絵と『対』として制作されたとMetが解説するが注文者・目的は推測を含む。禁断の果実を渡す場面そのものは別の絵に描かれ、ここでの主題は叱責。聖書の出来事を歴史的目撃記録として説明しない。",
    "emotions": [
      "緊張"
    ],
    "tones": [
      "緊張",
      "静けさ"
    ],
    "themes": [
      "時間",
      "他者との距離"
    ],
    "text": "木々の生い茂る園で、上から現れた人物に向かい、アダムが手を合わせています。エヴァは地面に座り、うつむきがちに顔を向けています。身体の力の入り方を見比べると、二人が同じ場面でも異なる姿で感情を表されていることが分かります。\n\nフランスの画家シャルル＝ジョゼフ・ナトワールが1740年に描いた《アダムとエヴァへの叱責》です。ナトワールは画家フランソワ・ルモワーヌの工房で学び、この作品も師への敬意を表すために描いたと美術館は考えています。ルモワーヌには、同じ大きさの銅板に、アダムがエヴァから禁断の果実を受け取る別の場面を描いた作品があります。\n\nエヴァの頬には涙が一粒光り、その柔らかな肌は、筋肉を強調したアダムの身体と対照をなしています。二人の身ぶりには、罪をめぐる聖書の物語だけでなく、18世紀の画家が人の感情をどう描いたかも表れています。これは宗教物語を題材にした絵であり、出来事を実際に見て描いた記録ではありません。",
    "checks": [
      [
        "trained in the studio of François Le Moyne",
        "ナトワールは画家フランソワ・ルモワーヌの工房で学び",
        "Met exact Overview: Natoire trained under Le Moyne"
      ],
      [
        "a tear glistening on her cheek, contrasted with Adam’s taut musculature",
        "エヴァの頬には涙が一粒光り、その柔らかな肌は、筋肉を強調したアダムの身体と対照をなしています。",
        "Met exact Overview: Eve tear contrasting Adam's muscles"
      ]
    ]
  },
  "670983": {
    "number": 427,
    "japanese": "京都四季遊楽図巻",
    "artist": "Maruyama Ōkyo 円山応挙",
    "culture": "Japan (Edo period)",
    "situation": "江戸時代の京都の春の花見・夏の納涼・秋の盆踊り・冬の正月準備を巻物で追い、当時の人々の楽しみを探したい",
    "meaning": "Met個別作品Overviewによると円山応挙（1733～1795）は若い頃に京都の玩具店で働き、その後、和画に中国画と西洋の遠近法・写実を取り入れた円山派を創始した。この長さ約5.55メートルの墨画は、名古屋の徳川美術館に所蔵される1777年の彩色絵巻に対する下絵、またはそれを素描風に写した別本と説明され、どちらかは確定していない。場面は右から左へ、保津川沿いの春の桜見物、鴨川での夏の納涼、盆踊りに示される初秋、そして松の苗飾りを整える冬の新年準備へと続く。主画像は絵巻の全長を横長に表示し、人物は非常に小さく見えるが、各場面を拡大して観察できる。",
    "visual": "Met APIの原寸・表示JPEGを完全取得して各SHA256/バイト数・サイズ・縮小RGB RMSで照合し、実際の公式主画像を確認。横に非常に長い黄土色の巻物全景に、灰墨の細い人物や木々・建築・舟などが途切れず描かれる。主サムネイルでは各人の細部を特定できないので四季の場面と位置はMet公式作品別Overviewを根拠にした。全長554.8cmの巻物を一作品として扱い、複数画像を別作品としては数えない。",
    "caution": "1777年の徳川美術館彩色本そのものとは別。習作か素描風模写かは所蔵館も二択で断定していない。全長を1枚に収めたMetの主JPEGでは人の細部が判読しづらいため、直接確認できた事実と学芸員解説を区別する。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい",
      "余韻"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "横に長い巻物を右から左へ追うと、京都の人々の暮らしが季節とともに移っていきます。春には保津川の岸で桜を楽しみ、夏には鴨川の水辺で涼みます。初秋には盆踊りが描かれ、冬には新年に向けた松の飾りを整える姿が続きます。\n\n作者は江戸時代の京都で活躍した円山応挙です。応挙は中国画の技法や西洋の遠近法にも学び、人物や風景をいきいきと描く円山派を築きました。この絵巻は1770年代後半から1780年代初めの墨画で、徳川美術館にある1777年の彩色版の下絵、またはそれを素描風に写した別の絵と考えられています。どちらなのかは決まっていません。\n\n巻物には一度にすべてを見る絵とは違い、少しずつ開きながら場面に出会う楽しみがあります。墨の細い線で表された人々の姿をたどると、京都の四季の楽しみが連続する時間として感じられます。ここに表示される全景画像では一人ひとりは小さく見えるため、拡大して探すのも面白いでしょう。",
    "checks": [
      [
        "either Ōkyo’s preparatory drawing for, or a sketchlike copy of",
        "この絵巻は1770年代後半から1780年代初めの墨画で、徳川美術館にある1777年の彩色版の下絵、またはそれを素描風に写した別の絵と考えられています。",
        "Met exact Overview: uncertain preparatory drawing versus sketch copy"
      ],
      [
        "early autumn is represented by traditional Obon dances",
        "初秋には盆踊りが描かれ",
        "Met exact Overview: Obon dancing marks early autumn"
      ]
    ]
  },
  "853195": {
    "number": 428,
    "japanese": "竹猿猴図",
    "artist": "Sesson Shūkei 雪村周継",
    "culture": "Japan (sixteenth-century ink painting)",
    "situation": "墨一色の竹と猿の絵で、猿の手が水面に届かない理由と禅の『水の月』のたとえを味わいたい",
    "meaning": "Met作品別Overviewは16世紀の画僧・雪村周継の水墨掛軸に、竹の近くの蔓からぶら下がった一匹のテナガザルが描かれ、下へ伸ばした左手は水面に映る月の影を捕まえようとしているのではないかと説明する。これは禅仏教で目覚めない心が実体のないものを追い求める愚かさを説く画題だとされる。ただし画面に月の反射が明確に描かれているとは断定せず、猿の意図もMetによる図像解釈として書く。雪村は東北で育ち、のちに鎌倉・小田原へ移り、当地の禅院や武家が収集した13世紀中国の牧谿らの画法を研究。右下には『周継』を示す朱印がある。",
    "visual": "Met公式APIの同作品の原寸・表示JPEGを全ダウンロード、ハッシュ・寸法・縮小RMSで照合し、真の主画像サムネイルを目視。縦長の掛軸の中央には淡墨の木か大きな竹と、下方の左寄りにふんわりした毛の猿が枝から垂れ、画面の右側には細い竹の葉。白い地の広い余白と上部の暗い枝がある。水面の月の反射は主画像で明確には見えないため、伝統図像に基づく解釈として扱う。",
    "caution": "月や水面に映る反射が明瞭に描かれているかを断定しない。猿の思考や禅の教義は象徴として紹介し、実際に動物が『悟り』を求めると主張しない。画家の『雪村』は雪舟とは別人であることに注意。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "自然",
      "時間"
    ],
    "text": "白い余白の中で、毛のふわりとしたテナガザルが蔓にぶら下がっています。近くには細く伸びる竹の葉。猿は片手を下へ伸ばしていますが、その先に何があるのか、画面からははっきり分かりません。墨の濃淡だけで、柔らかな毛と細い枝が描き分けられています。\n\nこの絵は16世紀の画僧・雪村周継による《竹猿猴図》です。美術館は、猿が水面に映った月の影をつかもうとしているのかもしれないと説明しています。水に映る月を求める猿は、禅の教えで、実体のないものにとらわれる心を表すことがあります。ただし、この絵で月の姿がはっきり見えるわけではありません。\n\n雪村は中国の画家・牧谿らの水墨画を研究し、独自の表現を育てました。画面右下には『周継』と読める朱印も残ります。猿が手を伸ばす先の余白に目を向けると、見えているものと想像するものの間に、この絵の面白さがあるように感じられます。",
    "checks": [
      [
        "probably the reflection of the moon in the water below",
        "美術館は、猿が水面に映った月の影をつかもうとしているのかもしれないと説明しています。",
        "Met exact Overview: only probable moon reflection"
      ],
      [
        "the delusional nature of the unawakened mind",
        "水に映る月を求める猿は、禅の教えで、実体のないものにとらわれる心を表すことがあります。",
        "Met exact Overview: Zen teaching on delusion"
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
          "Met 437180 is an oil-on-copper 1740 biblical scene honoring Le Moyne, and his earlier companion work is a distinct painting; Met 670983 could be Ōkyo’s preliminary ink draft or a sketchlike copy of a 1777 colored scroll, not the same scroll; Met 853195 suggests rather than shows the reflected moon and links the monkey to a traditional Zen metaphor."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==425,"main must have exactly 425 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：428作品**。mainへの統合後はDBとREADMEが正本。
- **次：429作品目から候補調査**。既登録ID・実JPEG画像SHA・Met作品別Overview・原寸/表示JPEGと利用権利の確認を継続。
- 今回426〜428：`met-437180` ナトワール《アダムとエヴァへの叱責》（1740年、フランス、銅板油彩）、`met-670983` 円山応挙《京都四季遊楽図巻》（1770年代後半〜1780年代初め、日本、長大な墨画巻物）、`met-853195` 雪村周継《竹猿猴図》（16世紀、日本、墨画掛軸）。
- 個別Met公式Overviewを作品ごとに直接照合し、二つずつ短い英文引用と日本語説明の重要主張を対応。ナトワール作の師ルモワーヌへの敬意は所蔵館の解釈。応挙の絵巻が1777年彩色本の下絵か後の素描風模写かは不明で、四季の場面は長い絵巻を右から左へ観る。雪村の猿が水面の月を取ろうとするという説明は禅の伝統図像にもとづく推測で、月が画面にはっきり見えるとは言わない。
- Met作品PD・公式Open Access JPEGのCC0・現代美術館解説文の権利を分けて検証。原寸・表示JPEGの全SHA256、バイト数、寸法、縮小RGB RMS、公式主画像のサムネイル実見は[426〜428画像調査](artwork-research-evidence/met-426-428-2026-11-13.json)を参照。研究記録には今回不採用とした肖像・書・印刷物・工芸・重複作品等も含む。
- 二次監査は同一AIによる別工程であり、人間・独立専門家・別モデルによる査読ではない。既存425作品と過去画像台帳は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-426.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==428,"final count mismatch")
    print("ALL PASS: 428 new total, existing 425 preserved",flush=True)
if __name__=="__main__":
    main()
