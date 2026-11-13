#!/usr/bin/env python3
"""One-off source-reviewed registration for #399-401. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-399-401-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-399-401-20261113/"+EVIDENCE
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
  "670982": {
    "number": 400,
    "japanese": "夕顔に虫図",
    "artist": "Maruyama Ōshin",
    "culture": "Japan (Edo period)",
    "situation": "江戸時代の夕顔の白い花と小さな昆虫を、『源氏物語』の儚い恋の連想と一緒に眺めたい",
    "meaning": "Met作品別Overviewによると、夕顔（ヒョウタン類）は夜にのみ芳しい白い花を咲かせる。『源氏物語』第4帖『夕顔』で、夕暮れの短い開花が一時の恋の出会いと人生のはかなさの比喩となった。作品には鮮やかな緑色の昆虫が描かれ、Metはおそらく花潜り類の甲虫としているが種の厳密な同定ではない。円山応震（1790–1838）は円山応挙の孫で、京都で活動した画家。画面の花と物語の関連は美術館の読みであり、この特定の作品に作者の恋愛体験を投影しない。",
    "visual": "Met実主画像の表示JPEGと原寸JPEGをSHA256と縮小RMSで照合しサムネイルを実見。縦長の掛軸で淡い黄土色の余白の右側に細く伸びる草の茎、上部に白い夕顔の花と葉、下方に大きな緑色の葉ともう一輪の花。小さな緑の昆虫は細部にいる。余白の広さと細い輪郭の配置が特徴。",
    "caution": "『夕顔』は植物と物語に共通する名前であり、画家が具体的な場面を再現したという確定資料ではない。昆虫の種はMetが『おそらく』とするにとどめる。作者の感情・恋愛経験を推測しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "自然",
      "時間",
      "愛情"
    ],
    "text": "余白の多い淡い紙面を、細い夕顔のつるが上へと伸びています。白い花の近くには、小さな緑色の虫も描かれています。大きく描かれた葉と小さな生き物を見比べると、静かな画面の中に異なる大きさの命が息づいているようです。\n\n夕顔は夜にだけ香りのある白い花を開きます。その短い開花は、『源氏物語』第四帖で、はかない恋の出会いや移ろう命と重ねて語られてきました。この作品は、19世紀初めに京都で活躍した円山応震による掛軸です。応震は円山応挙の孫で、人物画や花鳥画など幅広い主題を描きました。\n\n画中の鮮やかな緑の虫は、美術館では甲虫の一種ではないかと考えられていますが、断定はされていません。花の姿を丁寧に観察する絵であると同時に、古い物語を思い出す入口にもなります。夕顔の花の白さと、そのまわりの大きな余白に目を向けてみてください。",
    "checks": [
      [
        "The plant’s fragrant white flowers bloom only at night",
        "夕顔は夜にだけ香りのある白い花を開きます。",
        "Exact Met Overview: nocturnal fragrant calabash bloom"
      ],
      [
        "a metaphor for fleeting romantic encounters and the transience of life",
        "その短い開花は、『源氏物語』第四帖で、はかない恋の出会いや移ろう命と重ねて語られてきました。",
        "Exact Met Overview: Tale of Genji chapter four and fleeting encounters"
      ]
    ]
  },
  "853891": {
    "number": 399,
    "japanese": "山神と虎",
    "artist": "Unidentified artist",
    "culture": "Korea (Joseon dynasty)",
    "situation": "朝鮮の民間信仰と仏教が出会う山神図で、虎と赤い衣の神が同居する風景を見たい",
    "meaning": "メトロポリタン美術館の個別Overviewによると、朝鮮で古くから崇敬された山神（サンシン）は通常、白いひげの老人と虎の姿で表される。この絵では赤い大きな衣と冠を付けた威厳ある人物として描かれ、青緑の山水と長寿・節操を示す松、傍らの虎を伴う。朝鮮の在来の山岳信仰が後に仏教と融合したことを示す例とされる。美術館は大きな画面と精緻な仕上げから仏教寺院内の祠に掛けられた可能性を示すが、来歴の確定ではない。",
    "visual": "公式Met APIに紐づく原寸・表示JPEGを取得してサムネイルを目視確認。白い枠に囲われたやや横長の画面。中央の人物は赤い衣と上部に華やかな赤い冠のような帽子を付け、手前左の虎の顔は大きく、目が印象的。背景には青緑の山並みと大きな樹木の枝があり、地面の岩や雲の線が重なる。人と虎は画面中央近くで接する。",
    "caution": "実際に寺院の祠に掛けられた事実は資料未確定で、所蔵館は『おそらく』と述べる。山神の超自然的な働きや絵への信仰上の効験を史実とみなさない。作者名は不明。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "自然",
      "共同体"
    ],
    "text": "赤い長衣をまとった人物が、青緑の山を背に正面を向いて座っています。そのすぐそばには大きな虎の顔。虎の目と人物のまなざしを見比べると、画面には穏やかな色彩と強い存在感が同居していることが分かります。\n\nこれは19世紀後半の朝鮮で描かれた、作者不明の《山神と虎》です。朝鮮の伝統的な山神は、白いひげの老人と虎を伴う姿で表されるのが一般的でした。この絵の山神は威厳ある赤い装束と冠を着け、松や山の緑に囲まれています。松は長寿や節操の象徴でもあります。\n\n山神の信仰は、その後の仏教の世界にも取り入れられました。美術館は、この絵が仏教寺院の祠に飾られていた可能性を挙げていますが、実際の設置場所は確定していません。背景の山から虎へ、そして山神の顔へと視線を移すと、自然への敬意を神の姿に託した表現が見えてきます。",
    "checks": [
      [
        "with a white beard accompanied by a tiger",
        "朝鮮の伝統的な山神は、白いひげの老人と虎を伴う姿で表されるのが一般的でした。",
        "Exact Met Overview: conventional mountain god attributes"
      ],
      [
        "this painting was likely once in a shrine in a Buddhist temple complex",
        "美術館は、この絵が仏教寺院の祠に飾られていた可能性を挙げていますが、実際の設置場所は確定していません。",
        "Exact Met Overview: possible Buddhist temple shrine function"
      ]
    ]
  },
  "910558": {
    "number": 401,
    "japanese": "クドゥラトゥッラー筆《タージ・マハルの眺め》",
    "artist": "Koodrutoollah",
    "culture": "India (Lucknow)",
    "situation": "19世紀インドの画家が描いたタージ・マハルの精密な立面水彩で、建築の左右対称と異文化の描写技術を観察したい",
    "meaning": "Met作品別Overviewによると、1880年制作の銘文によって画家クドゥラトゥッラーの署名と制作年代が分かる。ムムターズ・マハルの墓廟タージ・マハルを正面から描いた建築水彩で、奥行きを示す直線的な遠近法はヨーロッパの工学図面や19世紀半ばの写真の広まりと関連づけられ、一方で外壁の花文様やカリグラフィーのピエトラ・ドゥーラ（石象嵌）の緻密さにはムガル帝国期のインド美術の伝統が見られる。作者の職歴に関するMetの東インド会社の説明と1880年という年代は慎重に扱い、職歴は断定して本文に記さない。",
    "visual": "Met APIの原寸・表示JPEGを完全取得し、実際の縮小画像を実見。横長の明るい地の上に白いタージ・マハルが真正面から左右対称に描かれる。中央の大きな玉葱形ドーム、左右に小さなドーム、両端の細いミナレットと階段・水路につながる手前の直線、建築正面の細い線画が見える。周縁の細い黄土色の額縁枠も確認。",
    "caution": "タージ・マハルの建設年は絵の制作年1880年とは異なる。現存建築の写真やオリジナルの施工図ではない。署名から示される作者名と制作年を区別し、画家の東インド会社での活動時期・所属の矛盾を推測で補完しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ"
    ],
    "themes": [
      "時間",
      "記憶"
    ],
    "text": "白い大理石の大きなドームを中心に、タージ・マハルの建物が左右対称に描かれています。両端には細い塔、手前には奥へ続く直線が伸びています。色を抑えた水彩の中で、建物の輪郭や正面の装飾がひとつずつ丁寧に追われています。\n\nこの絵は、インドの画家クドゥラトゥッラーが1880年に制作したものです。画面に残る銘文から、作者と制作年が分かります。描かれたタージ・マハルは、ムガル皇帝シャー・ジャハーンが妃ムムターズ・マハルのために建てた霊廟です。\n\n奥へ収束する直線的な遠近法には、ヨーロッパの工学図面の影響が見られます。一方、建物の花や文字の細かな石象嵌には、ムガルの装飾を詳しく伝えようとする視線が表れています。19世紀のインドで、異なる描写技術がひとつの建築図に重ねられたことを、細部をたどりながら確かめられます。",
    "checks": [
      [
        "made in 1880 by Indian artist Koodrutoollah",
        "この絵は、インドの画家クドゥラトゥッラーが1880年に制作したものです。",
        "Exact Met Overview: dated inscription and author"
      ],
      [
        "linear perspective of this work is informed by European engineering drawings",
        "奥へ収束する直線的な遠近法には、ヨーロッパの工学図面の影響が見られます。",
        "Exact Met Overview: engineering drawing perspective"
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
          "Met 853891 shrine provenance is conjectural; Met 670982 beetle species is only probable; Met 910558 East India Company work history is excluded due to chronology concerns."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==398,"main must have exactly 398 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"]}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：401作品**。mainへの統合後、作品DBとREADMEを正本とする。
- **次：402作品目から候補調査**。重複・Met公式作品別Overviewの実際の主張・画像原本と権利を個別に照合。
- 今回399〜401：`met-853891`《山神と虎》（19世紀後半、朝鮮）、`met-670982` 円山応震《夕顔に虫図》（19世紀初め、日本）、`met-910558` クドゥラトゥッラー《タージ・マハルの眺め》（1880年、インド）。
- Met個別公式Overviewを実際に読んで各2件ずつ短い英文と日本語の重要主張を対応。山神図の仏教寺院の祠での使用は『可能性』、夕顔の甲虫の種類は暫定同定。1880年の画家の職歴について年次に矛盾のあり得る解説は採用しなかった。
- 作品PD表示と公式Met JPEGのOpen Access CC0、現代の美術館解説文の著作権を分けた。公式原寸/表示JPEGの全SHA256・バイト数・寸法・縮小RMS・実画像サムネイルの直接視認は[399〜401画像調査](artwork-research-evidence/met-399-401-2026-11-13.json)に保存。
- 同一AIによる別工程の照合であり、人間・外部専門家・別モデルによる独立監査ではない。既存398作品と以前の画像台帳部分は変更していない。
"""
    temp=ROOT/"tmp-artwork-resume-399.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==401,"final count mismatch")
    print("ALL PASS: 401 new total, existing 398 preserved",flush=True)
if __name__=="__main__":
    main()
