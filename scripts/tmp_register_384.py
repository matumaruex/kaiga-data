#!/usr/bin/env python3
"""One-off source-reviewed registration for #384-386. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-384-386-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-384-386-20261112/"+EVIDENCE
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
  "764089": {
    "number": 386,
    "japanese": "愚かさの寓意",
    "artist": "Unknown Cuzco painter, after Boetius Adams Bolswert",
    "culture": "Peru (Cuzco)",
    "situation": "クスコ派の寓意画で、道化姿の人間の魂と神の愛を表す翼ある人物の対比を読みたい",
    "meaning": "Met作品別Overviewによれば、この画は1624年初刊のイエズス会士ヘルマン・フーゴーの寓意集『Pia Desideria』に含まれた、ボエティウス・アダムス・ボルスウェルトの版画をもとにした。道化として表される人間の魂アニマと、神の愛アモル・ディウィナの対決。赤い道化帽、棒馬、風車玩具と猫の籠は欲望と軽率さの徴で、アモルは顔を覆って天を指す。失われた図像連作の一部だった可能性は推定で、ボルスウェルトをこの油彩画の作者としない。",
    "visual": "公式API主画像では、左側に赤い羽飾りの道化帽と華やかな服の人物が棒馬にまたがり、長い棒を上へ掲げる。右側に翼のある人物が立ち、顔の一部を手で覆いながらもう一方の手を上に挙げる。二人の間には樹木、暗い背景と地面がある。",
    "caution": "この絵の制作者は不明のクスコ画家。ボルスウェルトの版画に『基づく』作品で、彼を画家本人と混同しない。道化は実在人物ではなく魂の寓意。複数作品からなる連作だったと断定しない。",
    "emotions": [
      "不安"
    ],
    "tones": [
      "緊張"
    ],
    "themes": [
      "愛情",
      "他者との距離"
    ],
    "text": "鮮やかな赤い帽子をかぶった人物が、おもちゃの馬にまたがり、長い棒を高く掲げています。その向かいでは、翼を持つ人物が顔を覆いながら天へ手を向けています。対照的な身ぶりの間に、何かを戒めるような緊張感が生まれています。\n\n18世紀のペルー・クスコで描かれた《愚かさの寓意》です。人間の魂を擬人化した「アニマ」は、道化の姿で表されています。対する神の愛を表すアモルは、顔を覆い、もう一方の手で天を指しています。画中の帽子、風車の玩具、籠に入れた猫などは、軽率さや世俗的な欲望を示すものと解釈されています。\n\nこの図は、17世紀に広く読まれた宗教的な寓意集『ピア・デシデリア』の版画に基づいています。版画を制作したボルスウェルトは、この油彩画の作者ではありません。足元には祈りに関わる聖書の言葉が書かれています。楽しげにも見える道化の動きと、向かいの人物の厳しい仕草を行き来しながら、二つの意味がぶつかる場面を見てみてください。",
    "checks": [
      [
        "a confrontation between Anima (the human soul), who appears as a fool",
        "人間の魂を擬人化した「アニマ」は、道化の姿で表されています。",
        "Met artwork Overview: Anima personification"
      ],
      [
        "Amor covers her face in shame and points heavenward",
        "対する神の愛を表すアモルは、顔を覆い、もう一方の手で天を指しています。",
        "Met artwork Overview: Amor divina gestures"
      ]
    ]
  },
  "825596": {
    "number": 385,
    "japanese": "二羽の鳩",
    "artist": "Unidentified Mughal court painter",
    "culture": "India (Mughal court)",
    "situation": "ムガル宮廷の細密画で二羽の鳩の羽毛や足輪を見比べたい",
    "meaning": "Met作品別Overviewは17世紀インドの自然の観察を描いた作品として、ムガル皇帝たちが植物と動物を記録する絵を好んだと説明。画面左の鳩の脚に二個の金の足輪があり、宮廷で飼われた鳥だった可能性を示すが確証とは書かれていない。作者個人の氏名は作品ページにもMet APIにもない。",
    "visual": "公式API主画像に、縦長の薄茶色い紙の上で灰白色の首と青灰色の翼を持つ鳩が二羽前後に重なり、左手前の鳩は大きく、後ろの鳩は小さめに見える。羽の短い線が丁寧に描かれる。脚元も描写されるが金の足輪の解釈は美術館本文に基づく。",
    "caution": "足輪を根拠に皇帝個人の所有だと断定しない。二羽の関係性・性別や画家の心理を推測しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "落ち着き"
    ],
    "themes": [
      "自然"
    ],
    "text": "薄茶色の紙の上に、二羽の鳩が体を少し重ねるように立っています。青灰色の羽は一枚一枚細かく描き分けられ、明るい胸から濃い翼へと色が移っていきます。よく似た二羽も、頭の位置や体の大きさを見比べると違いが見えてきます。\n\n17世紀半ばのインドで描かれた作品です。ムガル皇帝たちは、身近な世界を描く絵、とくに動植物の観察画にも関心を寄せていました。こうした作品は、宮廷の周囲にいた生き物の姿を詳しく記録する役割も担っていました。\n\n左側の鳩の脚には、二つの金色の足輪が描かれています。美術館はこれを、皇帝のもとで飼われていた鳥かもしれないと考える手掛かりとして説明します。ただし、誰が飼っていたかを確定するものではありません。鳩の脚元から羽の重なりへと視線を戻すと、小さな違いを記録する画家の細かな観察が伝わってきます。",
    "checks": [
      [
        "Mughal emperors were particularly fond of paintings depicting their world",
        "ムガル皇帝たちは、身近な世界を描く絵、とくに動植物の観察画にも関心を寄せていました。",
        "Met artwork Overview: Mughal court and natural history images"
      ],
      [
        "The pigeon at left has two golden anklets on its feet",
        "左側の鳩の脚には、二つの金色の足輪が描かれています。",
        "Met artwork Overview: gold anklets of pigeon at left"
      ]
    ]
  },
  "910553": {
    "number": 384,
    "japanese": "松林の鹿",
    "artist": "Unidentified Korean artist",
    "culture": "Korea (Joseon dynasty)",
    "situation": "朝鮮王朝期の白い鹿と松、赤い太陽に込められた吉祥の意味をゆっくり鑑賞したい",
    "meaning": "Met作品別Overviewは、16〜17世紀朝鮮の白鹿二頭を、道教やシャーマニズムで神々の使いや乗り物と見なされた鹿の伝統と結び付ける。松、花木、青緑色の山、川、霊芝、赤い太陽が吉祥の風景をつくり、誕生日など人生の節目の贈答・展示に用いられた種類の画と説明。ただし、この一幅が実際に誰かへ贈られたという来歴ではない。顔料は抑制され細かな墨描写が特徴。",
    "visual": "公式Met API主画像から確認した縦長の掛軸。下寄りには白い鹿が二頭立ち、傍らに太い松の幹と枝、地面の岩と植物。奥には淡い山並みと水辺が伸び、空の上方に赤い太陽が見える。広い薄茶色の表装は画中の地面とは区別する。",
    "caution": "鹿が神々の使いや乗り物と考えられたことは所蔵館の解説に基づく。この特定の絵が実際に誕生日の贈り物だったとは断定せず、象徴の宗教的意味をひとつに限定しない。",
    "emotions": [
      "希望"
    ],
    "tones": [
      "落ち着き"
    ],
    "themes": [
      "自然",
      "時間"
    ],
    "text": "松の太い幹のそばに、白い鹿が二頭、静かに立っています。枝は画面の上方へ広がり、その奥には青緑色の山と水辺が重なります。赤い太陽や点在する草花まで目を移すと、自然のさまざまなものが一枚の中に集められていることに気づきます。\n\nこの絵は、16〜17世紀の朝鮮で描かれた作者不明の掛軸です。道教やシャーマニズムの伝統では、鹿は神々の使いや乗り物として尊ばれていました。ここに描かれた二頭の鹿も、吉祥を示す白い姿で表されています。松や霊芝なども、長寿や幸運を願う画題に結びついています。\n\n美術館は、この種の吉祥画が誕生日など人生の節目に贈られ、飾られたと説明しています。ただし、この絵が誰に贈られたかまでは分かりません。白い鹿の輪郭と松の幹の細かな墨線、遠景の淡い色彩を見比べると、お祝いの意味と落ち着いた風景が一緒に表された様子が見えてきます。",
    "checks": [
      [
        "deer are revered as messengers and vehicles, of the gods",
        "道教やシャーマニズムの伝統では、鹿は神々の使いや乗り物として尊ばれていました。",
        "Met artwork Overview: deer as divine messengers"
      ],
      [
        "These deer, already distinguished by their auspicious white color",
        "ここに描かれた二頭の鹿も、吉祥を示す白い姿で表されています。",
        "Met artwork Overview: auspicious white deer"
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
          "For met-764089, Met distinguishes the unknown Cuzco painter from Boetius Adams Bolswert, the engraver whose composition was followed."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==383,"main must have exactly 383 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：386作品**。mainへの統合後、DBとREADMEの登録数を正本とする。
- **次：387作品目から候補調査**。作品別のMet公式解説の実際の主張、JPEG画像・権利・既登録作品との重複をそれぞれ確認。
- 今回384〜386：`met-910553`《松林の鹿》（16〜17世紀、朝鮮）、`met-825596`《二羽の鳩》（1650年頃、インド）、`met-764089`《愚かさの寓意》（18世紀、ペルー・クスコ）。朝鮮絵画は作者不明で、ペルー絵画もボルスウェルト版画に基づく不明画家の作品。
- Met作品別Overviewを実際に読み、作品ごとに二つの短い英文を独自の日本語解説の対応主張と照合。作品PD・Met公式JPEG Open Access CC0と、現代の美術館の解説文の権利は区別した。
- 原寸・表示JPEGの全SHA256/バイト数/寸法と縮小RMSを記録し、APIの画像サムネイルを直接見て被写体を確認。実画像研究は[384〜386の調査記録](artwork-research-evidence/met-384-386-2026-11-12.json)を参照。
- 作品別の別工程監査は同じAIであり、専門家や人間の査読ではない。従来383作品と画像台帳の以前の記録を変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-384.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==386,"final count mismatch")
    print("ALL PASS: 386 new total, existing 383 preserved",flush=True)
if __name__=="__main__":
    main()
