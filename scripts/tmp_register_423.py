#!/usr/bin/env python3
"""One-off source-reviewed registration for #423-425. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-423-425-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-423-425-20261113/"+EVIDENCE
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
  "437181": {
    "number": 425,
    "japanese": "マルソリエ夫人と娘",
    "artist": "Jean Marc Nattier",
    "culture": "France (18th-century court portraiture)",
    "situation": "18世紀フランスの母と娘が化粧や衣装を通じて上流社会の振る舞いを学ぶ様子を、華やかな布と人物の視線から眺めたい",
    "meaning": "Met作品別Overviewによるとジャン＝マルク・ナティエが1749年に描き1750年のサロンで公開した、マルソリエ夫人と娘の肖像。18世紀ヨーロッパの上流社会では、友人や知人の前で化粧や身支度を仕上げることは社交の一部だった。この絵では母親が娘へそうした社交儀礼を教え、豪華な衣服と金色の化粧道具が美と礼儀や消費力を示す。マルソリエ夫人は富裕な織物商と結婚し、娘は後にシャミイ侯爵夫人となった。ナティエはフランス王家に好まれた肖像画家で、その選択に家の社会的な上昇志向がうかがえる。娘が実際にこの場で化粧を学ぶ日を記録した絵ではなく演出された肖像である。",
    "visual": "Met公式APIの原寸/表示JPEGをダウンロードして完全SHA256と寸法/リサイズRMSを確認した主画像を視認。縦長の画面で左に青いスカートと白い肩衣の母親が座り、右に黄土色の布をまとう少女が金色の盆を差し出している。金の器具と衣装の艶、暗い幕、背景右の柱と空の気配がある。母娘の顔立ちや絵の小道具を丁寧に見せる。",
    "caution": "完成年1749年とサロンでの展示年1750年を区別。社交儀礼の演出であり、特定の日の家庭の出来事をそのまま記録したものと断定しない。豪華な姿の解説は上流社交の歴史的文脈として扱い、親子の感情を勝手に決めない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "落ち着き",
      "にぎわい"
    ],
    "themes": [
      "共同体",
      "日常"
    ],
    "text": "青い衣をまとった母親の隣に、金色の盆を差し出す少女が座っています。二人の衣装には光を受ける絹のような艶があり、化粧道具や大きな幕も華やかです。母親の手元から娘の持つ盆へ目を移すと、身支度のひと場面を切り取ったように見えます。\n\n1749年にフランスの肖像画家ジャン＝マルク・ナティエが描いた《マルソリエ夫人と娘》です。18世紀の上流社会では、友人や知人の前で化粧や身支度を仕上げることも、社交の一部でした。この絵では母親が、そうした振る舞いを娘に伝える姿を演出しています。作品は翌1750年のサロンにも出品されました。\n\nマルソリエ家は、王家に好まれた肖像画家を依頼することで、貴族社会に近づくことを望んでいました。娘は後にシャミイ侯爵夫人となります。華やかな布や化粧道具は、美しさだけでなく、当時の礼儀や身分を見せる役割も担っていました。二人の姿から、肖像画が家族の理想をどう描いたか考えてみてください。",
    "checks": [
      [
        "applying makeup and finishing dressing before friends and associates",
        "18世紀の上流社会では、友人や知人の前で化粧や身支度を仕上げることも、社交の一部でした。",
        "Met exact Overview: public toilette elite sociability"
      ],
      [
        "the Marsolliers aspired to aristocracy",
        "マルソリエ家は、王家に好まれた肖像画家を依頼することで、貴族社会に近づくことを望んでいました。",
        "Met exact Overview: aristocratic aspirations"
      ]
    ]
  },
  "456969": {
    "number": 424,
    "japanese": "『二聖都の案内』彩飾写本",
    "artist": "Text by Muhi al-Din Lari; illuminator unknown",
    "culture": "Central Asia (probably Bukhara; text composed in India)",
    "situation": "16世紀のイスラム巡礼案内に描かれた聖地の鳥瞰図から、道案内と絵の模様の関係を知りたい",
    "meaning": "Met作品別Overviewによれば『フフトゥーフ・アル＝ハラマイン（二聖都の案内）』はメッカとメディナの重要な場所、巡礼の儀礼を解説する詩文である。詩人ムヒー・アッディーン・ラーリーがインドで1505〜06年に文章を完成したが、この展示品は後の16世紀に複写された彩飾写本で、初期にブハラで制作されたと考えられる一例。主画像は40頁目で、中央の黒いカアバを囲む聖域・建造物を鳥瞰図で示し、巡礼者が場所を識別できるよう装飾や文字による目印を置く。地図のような図であり、当時の厳密な測量図・現地写真ではない。",
    "visual": "Met公式APIが指す原寸・表示JPEGのSHA256/画像サイズ/縮小RMSを照合し、そのサムネイルを直接確認。縦長の古い羊皮紙風の頁の中央に、黒い四角いカアバらしい建造物が黄色や青い幾何学的区画とともに描かれ、周辺に複数の細いミナレットと彩色の門が配置される。主要な装飾は金・青・赤を含む。本の全ページやメディナの風景までこの一枚に描かれているわけではない。",
    "caution": "詩の作者ムヒー・アッディーン・ラーリーと、この写本の写字生・挿絵画家は同一とは確認できない。テキストの完成地インドと、本写本の推定制作地ブハラ、聖地の実所在地メッカ/メディナを区別。主画像は40頁で全巻の内容を示すものではなく、実寸測量地図ではない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "時間",
      "共同体"
    ],
    "text": "黄みを帯びた写本の頁に、青や金色を使った建物の図が描かれています。中央には黒い立方体のカアバ、その周りには小さな塔や壁が整然と並びます。上から見下ろすような構図で、建物の位置と装飾が一緒に示されています。\n\nこの写本は、イスラム教の二つの聖地メッカとメディナを詩で案内する『フフトゥーフ・アル＝ハラマイン』です。巡礼の際に訪ねる場所や儀礼を知るための書物で、本文は1505～06年にムヒー・アッディーン・ラーリーがインドで完成させました。ここにあるのは、その後の16世紀に写された一冊です。\n\nこの写本は、中央アジアのブハラで作られた初期の写しのひとつと考えられています。ただし、詩を書いた人物が絵も描いたとは分かっていません。今見えるのは40頁目の図で、建物の姿は巡礼の場所を見分ける助けにもなりました。地図のような絵の中に、信仰と旅を結びつける工夫が感じられます。",
    "checks": [
      [
        "poetic description of the two holy Muslim sites",
        "この写本は、イスラム教の二つの聖地メッカとメディナを詩で案内する『フフトゥーフ・アル＝ハラマイン』です。",
        "Met exact Overview: poetic description of Mecca and Medina"
      ],
      [
        "one of the first copies thought to have been made in Bukhara",
        "この写本は、中央アジアのブハラで作られた初期の写しのひとつと考えられています。",
        "Met exact Overview: Bukhara production tentative"
      ]
    ]
  },
  "733038": {
    "number": 423,
    "japanese": "『マリアのオルガン』祈祷書",
    "artist": "Attributed to Baselyos (scribe); illumination maker uncertain",
    "culture": "Ethiopia (Lasta region)",
    "situation": "エチオピアの鮮やかな赤と黒の彩飾祈祷書で、正面を向いた聖人の姿と写本を作る人の工夫を見たい",
    "meaning": "Met作品別Overviewによれば17世紀後半のエチオピア正教の聖母マリアへの祈祷書『Arganonä Maryam』。詩文は15世紀の聖人アバ・ギヨルギス・オブ・セグラに伝統的に帰せられ、この写本の最初の葉の裏に彼の姿が描かれている。冒頭の主画像では正面向きの聖人が、上げた両手と幾何学模様の衣で表される。赤・黒・黄土・白の少ない色と鋭い幾何学文様が特徴で、聖母マリアを称賛する書物にもかかわらずマリア本人の姿は描かれていない。写字生バセリョスの名は奥付にあり、彩飾担当の『Ground Hornbill Master』と同一人物かどうかは学術上の議論がある。",
    "visual": "Met作品APIの原寸/表示JPEGを取得しSHA256、バイト数、画像寸法と縮小RMSを照合して実サムネイルを視認。見開きでなく縦長の一葉。黄土色の地に、中央の正面を向いた赤褐色の顔、黒いひげ、赤い光背、上げた両手の聖人。黒い上衣に赤黄の三角の幾何学模様が並び、左右は赤・黒・黄の帯状の枠。主画像にマリアを描いたと誤認しない。",
    "caution": "『聖母に捧げた本』でありながら主画像の聖人はマリアではない。伝統的な著作帰属と写字生、彩飾担当を混同しない。バセリョスとGround Hornbill Masterの同一性は議論中。祈りの効験は信仰上のもので実証とはしない。",
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
    "text": "赤と黒、黄土色で描かれた聖人が、正面からこちらを見つめています。両手を高く上げた姿の周囲には、三角形や十字を組み合わせた模様が幾重にも並びます。色の数は多くありませんが、細い線と繰り返す図形が強い印象を残します。\n\nこれは17世紀後半のエチオピア正教の祈祷書『マリアのオルガン』に収められた彩飾です。聖母マリアをたたえる本ですが、この写本にはマリア自身の姿は描かれていません。画面の人物は、祈りの詩を著したと伝えられる聖人アバ・ギヨルギス・オブ・セグラで、最初の葉の裏側に描かれています。\n\n写本にはバセリョスという写字生の名前が残りますが、文字を書いた人と絵を描いた人が同一だったかは確定していません。幾何学模様の衣や縁飾りは、この写本独自の力強い造形を見せています。開かれた一頁から、祈りの言葉と絵の形が結びついていたことを感じられます。",
    "checks": [
      [
        "He is depicted in the illumination on the reverse of the first folio",
        "画面の人物は、祈りの詩を著したと伝えられる聖人アバ・ギヨルギス・オブ・セグラで、最初の葉の裏側に描かれています。",
        "Met exact Overview: Giyorgis image on first folio verso"
      ],
      [
        "this work does not include her image",
        "聖母マリアをたたえる本ですが、この写本にはマリア自身の姿は描かれていません。",
        "Met exact Overview: manuscript excludes Virgin image"
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
          "Met 733038 depicts Giyorgis of Sägla and not Mary, while Baselyos vs illuminator identity is debated; Met 456969 reproduces a 1505-06 text in a later copy probably produced in Bukhara, and only page 40 is in the primary JPEG; Met 437181 dates to 1749 but appeared in the 1750 Salon, and depicts social display rather than a dated family event."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==422,"main must have exactly 422 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：425作品**。mainへの統合後はDBとREADMEが正本。
- **次：426作品目から候補調査**。既登録ID・画像SHA・Met作品別Overviewの実文面・公式原寸/表示JPEGと権利を個別に照合。
- 今回423〜425：`met-733038`《マリアのオルガン》祈祷書（17世紀後半、エチオピア・ラスタ）、`met-456969`《二聖都の案内》彩飾写本（16世紀、ブハラで写された可能性）、`met-437181` ナティエ《マルソリエ夫人と娘》（1749年、フランス）。
- Met個別作品Overviewの原文を実際に読み、各2箇所ずつ短い英語引用を独自日本語解説の正確な主張と対応。733038は聖母マリアをたたえる書物だが主画像の聖人はマリアではなくアバ・ギヨルギス。写字生バセリョスと彩飾画家の同一性は不明。456969の文の完成は1505〜06年インド、実写本は後の16世紀制作でブハラ帰属は推定。437181は1749年制作・1750年のサロン発表。
- Met API作品PD・公式Open Access JPEGのCC0・現代美術館解説文の権利を区別して監査。原寸・表示用JPEGのSHA256・バイト数・寸法・縮小RGB RMSと実公式画像サムネイルの目視は[423〜425画像調査](artwork-research-evidence/met-423-425-2026-11-13.json)を参照。研究記録には重複・貸出・権利制限による除外候補を含む。
- 監査は同じAIによる別工程であり、人間・独立専門家・別モデルによる独立査読ではない。既存422作品と以前の画像台帳を変更していない。
"""
    temp=ROOT/"tmp-artwork-resume-423.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==425,"final count mismatch")
    print("ALL PASS: 425 new total, existing 422 preserved",flush=True)
if __name__=="__main__":
    main()
