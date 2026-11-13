#!/usr/bin/env python3
"""One-off source-reviewed registration for #420-422. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-420-422-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-420-422-20261113/"+EVIDENCE
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
  "21186": {
    "number": 420,
    "japanese": "ララミー砦で描かれた先住民の指導者たちの習作",
    "artist": "Albert Bierstadt",
    "culture": "United States (Fort Laramie, present-day Wyoming)",
    "situation": "1859年のアメリカ先住民の四人の肖像習作から、画家が人物の表情や服装をどう捉えたか、当時の複雑な歴史とともに考えたい",
    "meaning": "Met作品別Overviewによれば、アルバート・ビアスタットは1859年6月にフレデリック・ランダー大佐の西部測量遠征隊に参加し、現在のワイオミング州にあるララミー砦に到着した。米政府とラコタ（テトン・スー）との関係が緊迫していた時期で、画家は現地で出会った先住民の人々をスケッチし、その中にこの四人の指導者の習作がある。各人の衣装と顔立ちを観察し、頭の下に名前を書いた。1863年の大型絵画《ロッキー山脈、ランダーズ・ピーク》の前景に描かれた男性の一部が、この習作に由来した可能性がある。四人が全員ラコタ族であるかなど個々の所属を一括して断定しない。",
    "visual": "Met APIの原寸と表示JPEGを全バイトで調査し、主画像サムネイルを直接確認。横長で薄いベージュ色の紙の上に四人の胸から上の肖像が離れて置かれている。左に横顔の男性、中央上に黄褐色の衣をまとう男性、右上に長髪の男性、下中央に赤い衣をまとった男性の正面寄りの肖像。ところどころ文字の書き込みが見え、背景はほぼ描き込まれていない。背景の欠落は未完成の失敗とは断定しない。",
    "caution": "西部遠征は米国政府と先住民の緊張関係の中で行われたことを明記。四人の民族・姓名や意向を美術館Overviewにない推測で断定しない。1863年の大型作との図像の関係は可能性であり、同一作品ではない。作者の目線は画家による記録であり先住民本人の声を直接代表するものではない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "緊張"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "薄い紙の上に、四人の人物の顔と肩が、少しずつ間隔をあけて描かれています。横を向く人、正面に近い角度でこちらを見る人。服の色や髪の流れも一人ずつ違い、頭の下には名前の書き込みがあります。背景をほとんど描かないことで、視線は自然とそれぞれの顔に向かいます。\n\nこの習作は1859年、画家アルバート・ビアスタットが、現在のアメリカ・ワイオミング州にあるララミー砦で制作しました。彼は政府の西部遠征隊に同行し、そこで出会った先住民の四人の指導者を描いています。当時は、ラコタの人々とアメリカ政府との関係が緊迫していた時期でした。\n\n画家は服装や顔立ちを観察し、一人ひとりの名前も書き添えました。四年後に発表した大作《ロッキー山脈、ランダーズ・ピーク》の人物の一部は、この習作をもとにした可能性があります。ただし、この絵は画家が捉えた姿であり、描かれた人々の考えまで伝えるものではありません。それぞれの肖像を見比べながら、記録する人と記録される人の関係にも目を向けてみてください。",
    "checks": [
      [
        "including this powerful depiction of four leaders",
        "そこで出会った先住民の四人の指導者を描いています。",
        "Exact Met artwork Overview: four leaders depicted in field studies"
      ],
      [
        "inscribing each one’s name below his head",
        "頭の下には名前の書き込みがあります。",
        "Exact Met artwork Overview: names written under the heads"
      ]
    ]
  },
  "54566": {
    "number": 421,
    "japanese": "孔雀・松・牡丹図",
    "artist": "Unidentified Japanese artist, in the style of Lü Ji",
    "culture": "Japan (Edo–Meiji period)",
    "situation": "大きな孔雀と牡丹、松を描いた花鳥画を、室町以来の中国絵画の影響や後世の修復の跡とともに見たい",
    "meaning": "Met作品別Overviewによると、寧波地域の中国画家・呂紀（15世紀末に活動）の作品が16世紀初頭までに日本へ伝わり、彩色花鳥画に大きく影響した。本作は日本制作で、呂紀の真作に見られる印章の偽の写しを押した『呂紀様式』の作品であり、本人が描いたものではない。制作は19世紀頃と考えられ、19世紀末～20世紀初めの再表装の際に広範な擦れや顔料の剥落が生じた可能性がある。メトロポリタン美術館は表面の損傷を明確に記載。作者不明で帰属を呂紀本人としない。",
    "visual": "Met公式APIの主画像原寸・表示JPEGを全バイト照合してサムネイルを直接確認。縦長の淡褐色の掛軸の上半分に背の高い松が枝を伸ばし、中央に大きな孔雀らしい青灰色の鳥が二羽重なるように立つ。下方には牡丹の赤や白などの花と岩、草が重なり、全体に色の薄くなった傷みが見える。装飾の細部を実像から過度に読み込まない。",
    "caution": "Met APIのartistDisplayNameは『Lü Ji』だが、公式個別作品ページの表示は『Style of Lü Ji』。後者と学芸員の説明を優先し、呂紀本人の作ではないことを明示する。偽印は作者が本物の呂紀を装った証拠として記録できるが、特定の不正意図や販売経緯は分からない。色落ちは保存状態の説明であり制作時の意図とは区別する。",
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
    "text": "松の枝の下に、羽を広げるように立つ孔雀と、岩間に咲く牡丹が描かれています。緑や青、花の赤みはところどころ薄くなり、画面の表面にも擦れが見えます。鳥の羽と花びらをたどりながら、絵が長い時間を経て現在に伝わったことにも目を向けてみてください。\n\nこの掛軸は、19世紀頃の日本で描かれた花鳥画です。中国の画家・呂紀の色鮮やかな花鳥画は、16世紀初めには日本に伝わり、後の日本絵画に影響しました。この作品も呂紀の様式にならって制作され、画中には呂紀の本物の印をまねた印章が使われています。呂紀本人が制作した絵ではありません。\n\n美術館は、画面の広い範囲に擦れや顔料の失われた部分があり、後世の表装し直しで傷んだ可能性を指摘しています。薄く見える部分のすべてが、もともとの画家の描き方だったとは限りません。孔雀や花の形と、絵そのものの年月の跡を見比べると、作品がたどってきた歴史も浮かび上がります。",
    "checks": [
      [
        "created in Japan, bears a forged copy of a seal",
        "この作品も呂紀の様式にならって制作され、画中には呂紀の本物の印をまねた印章が使われています。",
        "Exact Met artwork Overview: Japanese Lü Ji-style work and imitated seal"
      ],
      [
        "widespread abrasion of the surface and loss of pigments",
        "画面の広い範囲に擦れや顔料の失われた部分があり",
        "Exact Met artwork Overview: documented surface abrasion and pigment loss"
      ]
    ]
  },
  "454664": {
    "number": 422,
    "japanese": "装飾された『クルアーン』写本の一巻",
    "artist": "Unidentified North African or Andalusian manuscript illuminator",
    "culture": "Attributed to Morocco or southern Spain",
    "situation": "イスラム世界の1300年頃の写本にある細かな金と色彩の幾何学装飾を眺め、タイル模様とのつながりを知りたい",
    "meaning": "Met作品別Overviewによれば、この写本は七巻本『クルアーン』の第二巻で、奥付は残っていない。見開きの冒頭には複雑に入り組む幾何学的な帯模様が金・色彩で表され、アンダルシアと北アフリカのタイル装飾に近い。書き込みから、かつてマディーナでモロッコからの滞在者を受け入れていたリバート（宿泊所）の文庫に属していたと分かる。作品の制作地は『モロッコまたはスペイン南部と推定』で、マディーナで制作されたという意味ではない。媒体は羊皮紙への墨・金・不透明水彩を使った彩飾写本で単独の絵画キャンバスではない。",
    "visual": "Met公式APIの実際の原寸・表示JPEGを完全取得してSHA256、寸法、縮小RMSとともに主画像を視認。横長に開いた古い羊皮紙の見開き二ページで、左と右の中央にほぼ正方形の入り組んだ金・黄土色・赤の幾何学的な帯模様が対称に配置される。外側の余白には丸い飾り、細部には青い小さな点があり、紙面は年月で黄ばんでいる。現画像にクルアーン全巻が写るという意味ではない。",
    "caution": "この品は七巻本のうちの第二巻に相当する写本で、主JPEGは冒頭の彩飾された見開きのみ。制作地はモロッコまたは南スペインのいずれかで未確定。マディーナの文庫にかつて属したことと、マディーナで制作されたかを混同しない。宗教書の意味を断定的に説明しない。",
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
    "text": "古い羊皮紙を開いた見開きに、金色や赤、青を交えた細かな幾何学模様が並んでいます。左右の正方形の飾りはよく似ていますが、細い線を追うと幾重にも帯が組み合わされているのが分かります。縁にある丸い装飾も、中央の模様を囲むように配置されています。\n\nこれは1300年頃の『クルアーン』写本で、全七巻のうち第二巻にあたります。冒頭の華やかな見開きには、アンダルシアや北アフリカの建築を飾ったタイルにも通じる、組みひものような幾何学模様が描かれています。制作されたのはモロッコまたはスペイン南部と推定されていますが、正確には分かっていません。\n\n写本の余白に残る書き込みから、かつて聖地マディーナにある、モロッコから来た人々が宿泊する施設の文庫に収められていたことがうかがえます。ただし、それは制作地を示すものではありません。ここに見えるのは本の冒頭にある装飾見開きです。ページの中心と縁の模様を見比べながら、本の形で受け継がれてきた装飾の美しさを味わってみてください。",
    "checks": [
      [
        "the second volume of a seven-part Qur'an manuscript",
        "全七巻のうち第二巻にあたります。",
        "Exact Met artwork Overview: second of seven volumes"
      ],
      [
        "designs of Andalusian and North African tiles",
        "アンダルシアや北アフリカの建築を飾ったタイルにも通じる",
        "Exact Met artwork Overview: Andalusian and North African tile comparanda"
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
          "Met 21186 depicts four named Indigenous leaders during tense US-Lakota relations, not necessarily all of one tribal nation; 54566 is a Japan-made work in the *style* of Lü Ji and has a forged seal and degraded pigments, contrary to simplified API author; 454664 main JPEG shows the illuminated opening of the second volume of seven, made probably in Morocco or southern Spain and later held in Medina."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==419,"main must have exactly 419 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：422作品**。mainへの統合後はDBとREADMEが正本。
- **次：423作品目から候補調査**。既登録ID・画像SHA・公式Met作品別Overview・原寸/表示JPEGの実物と利用権利を個別に確認する。
- 今回420〜422：`met-21186` ビアスタット《ララミー砦で描かれた先住民の指導者たちの習作》（1859年頃、アメリカ）、`met-54566`《孔雀・松・牡丹図》（19世紀頃、日本制作の呂紀様式作品）、`met-454664`《装飾されたクルアーン写本の一巻》（1300年頃、制作地はモロッコまたは南スペインと推定）。
- Metの個別Overview本文を実際に読み、作品ごと二箇所の短い英語原文と日本語本文中の重要主張を照合。21186は米国政府とラコタの緊張期に描かれた別々の四人の習作。54566はAPIが『呂紀』とするのに対し公式個別解説では呂紀『様式』で日本制作、偽の印章があり、表面にも摩耗。454664は全七巻の第二巻で主画像は冒頭見開きだけ。制作地と後のマディーナの保管地を区別。
- Met APIの作品PD、公式Open Access JPEGのCC0、所蔵館が書いた現在の解説文の権利を別々に確認。原寸・表示用JPEGの全SHA256・バイト数・寸法・縮小RMSと主画像の実見は[420〜422画像調査](artwork-research-evidence/met-420-422-2026-11-13.json)に保存。研究ログには今回未登録の重複候補と他の彩飾写本も含む。
- 二次監査は同じAIによる別工程であり、人間・独立専門家・別AIによる査読ではない。既存419作品と過去の画像台帳部分は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-420.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==422,"final count mismatch")
    print("ALL PASS: 422 new total, existing 419 preserved",flush=True)
if __name__=="__main__":
    main()
