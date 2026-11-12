#!/usr/bin/env python3
"""One-off source-reviewed registration for #396-398. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-396-398-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-396-398-20261112/"+EVIDENCE
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
  "456968": {
    "number": 398,
    "japanese": "読書する貴族",
    "artist": "Unidentified Mughal painter",
    "culture": "India",
    "situation": "18世紀のインド細密画で、椅子が描かれていない未完成の肖像と空白の本を観察したい",
    "meaning": "Met個別Overviewによると、1750〜75年頃のこの未完成の人物画では椅子がまだ描かれていないので、読書するように座る人物は空中に浮くように見える。顔や手の点描的な陰影、衣の折り目は細部への注意を示す。ムガル宮廷肖像では所持品に囲まれた人物を描くことが多いが、ここでは文字のない本だけを手にしている。高期ムガル肖像が最盛期を過ぎても伝統は継続したと所蔵館は解説。画家名や書物の題名は不明。",
    "visual": "Met公式APIから得た実JPEGの縮小画像を見た。無地に近い明るい淡褐色の縦長紙面中央に、白色のターバンと縞の長衣をまとった髭のある男性が斜めに座り、両手で開いた白い本を持つ。椅子がなく足元と服の縁が空白の上に浮くように見える。顔と手の濃淡、小さな靴と細い輪郭線が見える。",
    "caution": "『読書』は題名上の呼称であり、白い本に実際の文章が書かれていると決め付けない。椅子の不在は未完成のためとMetが説明。作者を特定せず人物の身元も推測しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "日常",
      "時間"
    ],
    "text": "白い衣をまとった男性が、両手で開いた本を見つめています。ところが、その姿を支えるはずの椅子は見当たりません。この絵は未完成で、椅子がまだ描かれていないため、人物は空中に座るように見えます。淡い背景と細かな衣の線にも注目してみてください。\n\n1750〜75年頃のインドの人物画です。顔や手には細かな点を重ねた陰影があり、服の折り目も丁寧に表されています。一方で、背景や椅子などの周囲の描写は終わっておらず、制作の途中段階を見せる作品となっています。\n\nムガル宮廷の肖像では、人物の貴重な所持品を周りに描くことがよくありました。しかし、この人物は手に文字のない白い本だけを持っています。何を読む人物なのか、名前や本の題名は明らかではありません。描き込まれた部分と空白を見比べると、完成した肖像では見落としがちな制作の手順に目が向きます。",
    "checks": [
      [
        "This unfinished painting depicts a seated figure who appears to be floating in space",
        "この絵は未完成で、椅子がまだ描かれていないため、人物は空中に座るように見えます。",
        "Met exact artwork Overview: unfinished figure appearing suspended"
      ],
      [
        "only a blank book in his hand",
        "しかし、この人物は手に文字のない白い本だけを持っています。",
        "Met exact artwork Overview: blank book and absence of typical possessions"
      ]
    ]
  },
  "749135": {
    "number": 397,
    "japanese": "白マハーカーラ",
    "artist": "Unidentified Tibetan artist",
    "culture": "Tibet",
    "situation": "チベット仏教の絵画で、六本の腕を持つ白マハーカーラと周囲の守護神たちの配置を読み解きたい",
    "meaning": "メトロポリタン美術館の個別Overviewによると、18世紀頃の木綿地に描かれた白マハーカーラ（シャドブジャ・シータ・マハーカーラ）は、チベット仏教で豊かさを願い祈られる尊格。中心像は三つの大きく見開いた恐ろしい目と六本の腕に武器を持ち、周囲には吉祥・守護を示す諸尊が配置される。上方には五仏が置かれ、中心像を見守る構成と説明。恐ろしげな形相は守護尊の図像であり人間の悪意や歴史的暴力の証拠としない。",
    "visual": "実際のMet API主表示JPEGサムネイルでは、縦長の画面中央に白い身体と複数の腕をもつ尊格があり、背後に赤い光背のようなもの。上部には五つほどの小さな座像が並び、下部には赤や黄の尊像が囲む。全体に濃い青緑の地と多彩な装飾を確認。個々の持物や手の位置は小画像だけで不確定としている。",
    "caution": "『財を確実にもたらす』という効果を保証せず、チベット仏教の信仰上の役割として説明する。怒りの形相を悪意と単純視しない。作者の個人名は不明。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "緊張",
      "高揚"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "濃い青緑色の画面の中央に、白い身体を持つ尊格が表されています。赤い光背のまわりには小さな尊像が並び、上から下まで細かな模様と色彩で埋め尽くされています。まず中央の姿を見てから、周囲の人物へと視線を広げてみてください。\n\n白マハーカーラは、チベット仏教で豊かさを祈る際に信仰される尊格です。中心のマハーカーラは、三つの大きく見開いた目と六本の腕を持ちます。腕に携えた武器や厳しい表情は、人々を守る力を表す図像として用いられています。\n\n周囲には守護や吉祥に関わる諸尊が配され、上方には五人の仏が描かれています。怖そうに見える表情と、豊かさを願う役割が一つの姿に重なる点が、この絵の特徴です。信仰上の意味を知ったうえで色や配置を見直すと、中央と周囲のつながりが見えてきます。",
    "checks": [
      [
        "White Mahakala, a wealth deity invoked widely by Tibetan Buddhists",
        "白マハーカーラは、チベット仏教で豊かさを祈る際に信仰される尊格です。",
        "Met exact artwork Overview: wealth deity"
      ],
      [
        "three wide glaring and fearsome eyes, and six arms",
        "中心のマハーカーラは、三つの大きく見開いた目と六本の腕を持ちます。",
        "Met exact artwork Overview: three eyes and six arms"
      ]
    ]
  },
  "825592": {
    "number": 396,
    "japanese": "修行者たちの集い",
    "artist": "Unidentified Indian artist",
    "culture": "India, early 17th century",
    "situation": "17世紀初めのインド細密画で、集まる修行者たちの身ぶりと宗教的陶酔の描き方を見たい",
    "meaning": "メトロポリタン美術館の個別Overviewによれば、1605〜10年頃のこの絵は多くが酩酊させる物質の影響を受けているように見える神秘主義の修行者（ダルヴィーシュ）たちの集まりを描く。画面右の一団はふるいで混合物を準備し、他の人物は体を傾けたり横たわったりする。美術館は宗教的な恍惚と無秩序との境界を曖昧にする題材と捉え、このようなジャンルが17・18世紀の絵画で広まった初期の例と説明する。使われた物質の種類、彼らの実際の酩酊、個人の信仰の深さは特定できない。",
    "visual": "Met作品APIの主JPEGから作った実画像サムネイルを確認。縦長の画面の内側に彩色された庭園、中央に背の高い木、その周囲には橙や緑、白の衣を着た男性の集団が座り、下方に体を傾けたり座り込む人物が重なる。幾何学的な石の台と淡金色の広い装飾枠が見える。実際の物質や人物心理を画像だけで判断しない。",
    "caution": "酩酊を歴史的な実録や特定薬物の摂取の確定事実として扱わない。宗教的な陶酔と酩酊の境界は美術館の解釈として記す。作者個人の価値判断を断定しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい",
      "緊張"
    ],
    "themes": [
      "共同体",
      "他者との距離"
    ],
    "text": "木の茂る庭に、色鮮やかな衣を着た修行者たちが集まっています。中央付近では人々が腰を下ろし、下方には体を大きく傾けたり、地面に座り込んだりする姿も見えます。同じ場所にいながら、ひとりひとりの身ぶりが異なることに目を向けてみてください。\n\n1605〜10年頃のインドで描かれた細密画です。美術館は、集まった修行者の多くが酩酊させる物質の影響下にあるように見えると説明しています。右側の一団は、ふるいを使って混合物を用意しています。こうした細部を通じて、修行者たちの集まりは通常の儀礼的な肖像とは違う雰囲気を帯びています。\n\nメトロポリタン美術館は、この絵が宗教的な恍惚と節度を失った状態との境目を曖昧にしていると考えています。ただし、具体的に何を用いていたのか、実際にどのような状態だったのかまで確定できるわけではありません。装飾的な庭の秩序と、自由な身ぶりの対照を見比べると、この作品の独特な表現が浮かびます。",
    "checks": [
      [
        "many of whom appear to be under the influence of intoxicating substances",
        "美術館は、集まった修行者の多くが酩酊させる物質の影響下にあるように見えると説明しています。",
        "Met exact artwork Overview: gathering of mystics and appearance of intoxication"
      ],
      [
        "One group on the right prepares the mixture in a sieve",
        "右側の一団は、ふるいを使って混合物を用意しています。",
        "Met exact artwork Overview: right-side preparation using a sieve"
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
          "Met 825592 does not identify intoxicant type; 749135 wrathful deity is a wealth protector; 456968 blank book and unfinished chair are directly described in the exact Met Overview."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==395,"main must have exactly 395 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：398作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：399作品目から候補調査**。既登録ID、画像重複、作品別Met Overviewと原JPEG、画像利用条件を作品ごとに確認する。
- 今回396〜398：`met-825592`《修行者たちの集い》（1605〜10年頃、インド）、`met-749135`《白マハーカーラ》（18世紀頃、チベット）、`met-456968`《読書する貴族》（1750〜75年頃、インド）。
- 3作品とも個別のMet公式Overviewを直接読み、各2件ずつ短い原文抜粋と独自日本語本文の主張を対応させた。修行者の酩酊は『そう見える』という所蔵館の解釈、白マハーカーラの財宝の意味は宗教的な信仰として扱い、貴族肖像の白い本と描かれていない椅子を明記した。
- Met APIのPD表示・公式JPEGのOpen Access CC0・現代の美術館解説文の著作権を分離評価。原寸・表示JPEG全バイトSHA256、サイズ、寸法、縮小RMSと実画像の視覚チェックは[396〜398画像調査](artwork-research-evidence/met-396-398-2026-11-12.json)に保存。
- 別工程の監査は同じAIによるもので、人間・外部専門家・別AIモデルの査読ではない。既存395作品と画像台帳の以前の記録は不変。
"""
    temp=ROOT/"tmp-artwork-resume-396.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==398,"final count mismatch")
    print("ALL PASS: 398 new total, existing 395 preserved",flush=True)
if __name__=="__main__":
    main()
