#!/usr/bin/env python3
"""One-off source-reviewed registration for #387-389. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-12"
EVIDENCE="docs/artwork-research-evidence/met-387-389-2026-11-12.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-387-389-20261112/"+EVIDENCE
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
  "44760": {
    "number": 387,
    "japanese": "花鳥図（十曲屏風）",
    "artist": "Unidentified artist",
    "culture": "Korea, Joseon dynasty",
    "situation": "朝鮮王朝末期の花鳥画屏風で、鳥のつがいと季節の草花に込められた願いを眺めたい",
    "meaning": "Met作品別Overviewによると、朝鮮の花鳥画屏風は朝鮮王朝後期に普及し、20世紀まで人気があった。十曲の各扇には花木、草、葦などと一組以上の鳥のつがいが描かれ、虫や第5扇の水生生物も登場する。富・出世・長寿・子孫繁栄などの吉祥、鴛鴦などの雌雄対が婚礼や新婚の部屋にふさわしいとされた象徴を解説。特定の婚礼で実際に用いられたという来歴ではない。",
    "visual": "Met APIの原寸・表示画像から作成した実画像サムネイルを確認。横長の十曲屏風が一画面に収まり、淡い黄土色の縦長パネルが十枚並び、各扇の足もとに植物の緑と鳥が点在し、枝や葦が上へ伸びる。幅広い屏風の縁は図柄の一部ではない。",
    "caution": "十枚を独立作品として数えず一作品の十曲屏風として扱う。画中の鳥のつがいを全て鴛鴦だと決め付けず、婚礼で実際に使われたと断言しない。制作年代の範囲は19世紀末〜20世紀初頭のまま保つ。",
    "emotions": [
      "期待"
    ],
    "tones": [
      "落ち着き"
    ],
    "themes": [
      "自然",
      "愛情"
    ],
    "text": "淡い金色を帯びた十枚の画面に、花をつけた木や草、その周囲を行き交う鳥たちが描かれています。横に視線を動かすと、鳥の位置と植物の形が一枚ずつ変わり、屏風全体にゆるやかなリズムが生まれています。\n\n朝鮮王朝末期から20世紀初めにかけて作られた、作者不明の十曲屏風です。各扇には、植物のそばにいる一組以上の鳥のつがいが描かれています。鳥のほか、虫や水辺の生き物も加わり、自然の多彩な姿が細やかに表されています。\n\n花や鳥の多くの意匠は、富や長寿などを願う意味を帯びています。とりわけ雌雄の鳥が一緒にいる図柄は、婚礼や新婚の部屋にもふさわしいとされました。ただし、この屏風が特定の結婚式に使われたと分かっているわけではありません。一扇ずつ眺めた後、少し離れて十枚が作るつながりを見てみてください。",
    "checks": [
      [
        "Each panel portrays one or more pairs of birds",
        "各扇には、植物のそばにいる一組以上の鳥のつがいが描かれています。",
        "Met exact artwork Overview: bird pairs in each panel"
      ],
      [
        "Many of the motifs have poetic meaning and embody wishes",
        "花や鳥の多くの意匠は、富や長寿などを願う意味を帯びています。",
        "Met exact artwork Overview: auspicious motifs"
      ]
    ]
  },
  "456967": {
    "number": 388,
    "japanese": "異なる信仰の聖者たちの集い",
    "artist": "Mir Kalan Khan",
    "culture": "India, Lucknow (attributed)",
    "situation": "18世紀インドの聖者たちの集まりを描いた細密画で、異なる伝統の人物を囲む空間と画家の移動を考えたい",
    "meaning": "Met作品別Overviewによると、異なる信仰の聖者たちが会する既存の有名なムガル絵画をもとにした図。主な人物は画面右からラヴィダース、セーナー、ナームデーヴ、アウガル、カマール、カビールと同定される。画家ミール・カラン・ハーンはムガル宮廷で学んでからラクナウへ移り、シュジャー・ウッダウラとアーサフ・ウッダウラの宮廷画家として模倣される画風を形成。この絵を実際に人物が一堂に会した記録と扱わない。所在地帰属はラクナウと推定。",
    "visual": "Met APIで作品に対応する原寸/表示JPEGを照合してサムネイルを直接確認。縦長の装飾的な額縁の内側に、緑の樹木と淡いアーチ状の建造物があり、その前で白い衣の人物を含む複数の男性が左右に向き合うように座る。金色の模様ある縁飾りも確認。",
    "caution": "描かれた聖者たちが本当に同じ日時に集会した歴史的記録とは扱わない。画家の制作地はMetの『Attributed to India, Lucknow』として推定にとどめ、宗教的同一性や作者の信条を推測しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "共同体",
      "他者との距離"
    ],
    "text": "緑の木々と淡い色の建物を背に、白い衣をまとった人々が向かい合うように座っています。頭上の枝、中央の入口、画面を囲む細かな装飾が、集まりの場をひとつの静かな空間としてまとめています。\n\nこの絵は、異なる信仰の聖者たちが集まるというムガル絵画の知られた構図を踏まえています。メトロポリタン美術館は、人物を右からラヴィダース、セーナー、ナームデーヴ、アウガル、カマール、カビールと同定しています。ただし、彼らがこの場所で実際に集まったことを記録した絵ではなく、先行する主題の描き直しです。\n\n画家ミール・カラン・ハーンはムガル宮廷で学んだ後、ラクナウへ移りました。そこで支配者たちに仕える宮廷画家として活動し、後に模倣される画風を築きました。人物同士の向きや間隔に注目すると、異なる伝統をもつ人々を一画面に配置する工夫が見えてきます。",
    "checks": [
      [
        "based upon a well-known Mughal painting on the theme",
        "この絵は、異なる信仰の聖者たちが集まるというムガル絵画の知られた構図を踏まえています。",
        "Met exact artwork Overview: source composition"
      ],
      [
        "the artist Mir Kalan Khan moved to Lucknow",
        "画家ミール・カラン・ハーンはムガル宮廷で学んだ後、ラクナウへ移りました。",
        "Met exact artwork Overview: court artist moved"
      ]
    ]
  },
  "764091": {
    "number": 389,
    "japanese": "バルバネラの聖母",
    "artist": "Unknown Cuzco artist",
    "culture": "Peru, Cuzco",
    "situation": "18世紀ペルー・クスコ派の聖母像に、樫の木・湧き水・鳥と巡礼地を織り込んだ宗教画の読み方を知りたい",
    "meaning": "Met作品別Overviewは、悔い改めて隠修士となった元盗賊ヌーニョ・オニェスが、幻視で示された樫の樹洞に隠されたバルバネラの聖母像を発見する逸話と説明。湧き水と蜜蜂が像の所在を知らせ、木々に描かれた鮮やかな熱帯鳥は伝説には登場しないが聖域を示す。左中景の教会はバルバネラ修道院。描写された山並みをスペインのラ・リオハの厳密な地理再現としない。所蔵館はフランドルの図像モデルによる可能性が高いとする。",
    "visual": "Met APIの原寸/表示JPEGから生成されたサムネイルで中央の装飾的な冠をいただく聖母子が大きな木の幹の空洞のような場所に立つ。枝には赤や黄色の鳥、左側に屋根のある建物、右側に跪く黒褐色の衣の人物、背景には青い山と森がある。外側の黒い余白は画中の闇とは区別する。",
    "caution": "『発見』は伝承の物語として記す。ペルーの自然を忠実に写生したものと断定せず、人物のモデル特定や宗教的奇跡を歴史的事実として保証しない。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "自然",
      "時間"
    ],
    "text": "大きな樹木の下に、冠をいただいた聖母子の像が現れています。枝には鮮やかな色の鳥たちが止まり、左には建物、右には跪く人物が描かれています。遠くの山まで続く豊かな景色の中に、聖なる像を発見する物語が組み込まれています。\n\nこれは18世紀後半のペルー・クスコで描かれた《バルバネラの聖母》です。伝承によれば、かつて盗賊だったヌーニョ・オニェスは悔い改めて隠修士となり、幻視に導かれて聖母像を発見しました。聖母像は、樫の木の洞に隠されていたと伝えられています。湧き水と木の洞の蜜蜂が、その場所を知らせるしるしとなります。\n\n枝にいる色鮮やかな熱帯の鳥は、発見譚には登場しないものの、この場所の神聖さを伝えています。左に見える教会は、聖母像を祀るバルバネラ修道院です。山や木は実際の地形の忠実な記録というより、古い図像の伝統をもとに組み立てられた風景と考えられています。鳥と木と小さな人物をたどると、物語の発見の瞬間が見えてきます。",
    "checks": [
      [
        "Hidden in the hollow of an oak tree",
        "聖母像は、樫の木の洞に隠されていたと伝えられています。",
        "Met exact artwork Overview: oak-tree hollow"
      ],
      [
        "the brightly colored tropical birds in the tree’s branches",
        "枝にいる色鮮やかな熱帯の鳥は、発見譚には登場しないものの、この場所の神聖さを伝えています。",
        "Met exact artwork Overview: tropical birds"
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
          "For met-44760, one official primary JPEG shows the full ten-panel screen, not a single individual painting; for met-456967, the meeting is a painted iconographic theme rather than a documentary record."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==386,"main must have exactly 386 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-12時点）

- **完成登録：389作品**。mainへの統合後のDBとREADMEを正本とする。
- **次：390作品目から候補調査**。実作品の重複確認、所蔵館公式Overviewの主張、画像・権利照合を作品ごとに継続。
- 今回387〜389：`met-44760`《花鳥図（十曲屏風）》（19世紀末〜20世紀初頭、朝鮮）、`met-456967`《異なる信仰の聖者たちの集い》（1770〜75年頃、インド）、`met-764091`《バルバネラの聖母》（1770〜80年頃、ペルー）。
- 三作品ともMetの個別公式Overview本文を実際に読み、二つずつの短い原文抜粋と独自の日本語解説の主張を結び付けた。作品PD・Met公式画像CC0・美術館現代文章の権利は区別して監査。
- 公式APIの画像URLから原寸・表示JPEGを全取得してSHA256とバイト数・寸法・縮小RMSを記録し、サムネイルを実見して図像とIDを照合。実画像研究は[387〜389の調査記録](artwork-research-evidence/met-387-389-2026-11-12.json)を参照。
- 作品別の別工程監査は同じAIによるもので、独立した人間・外部の専門家の査読ではない。既存386作品と画像台帳の以前の登録は変更していない。
"""
    temp=ROOT/"tmp-artwork-resume-387.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==389,"final count mismatch")
    print("ALL PASS: 389 new total, existing 386 preserved",flush=True)
if __name__=="__main__":
    main()
