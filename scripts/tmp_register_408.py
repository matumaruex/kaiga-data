#!/usr/bin/env python3
"""One-off source-reviewed registration for #408-410. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-408-410-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-408-410-20261113/"+EVIDENCE
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
  "437979": {
    "number": 409,
    "japanese": "月夜の船",
    "artist": "Ivan Konstantinovich Aivazovsky (Hovhannes Aivazian)",
    "culture": "Armenian-born in Feodosia, Russian Empire (now Ukraine); Black Sea painter",
    "date_display": "undated (year not specified in Met object record)",
    "situation": "月明かりの海と沖合の蒸気船が描かれた、19世紀の画家アイヴァゾフスキーの小さな風景画を味わいたい",
    "meaning": "Met作品別Overviewによればアルメニア系で当時ロシア帝国領だったクリミア半島フェオドシヤ生まれの海景画家イワン・アイヴァゾフスキー（1817–1900）が制作した作品。彼は帆船を好んで描いたが、ときにはこの作品のように近代的な蒸気船も題材にした。黒海沿岸の港町で育った経験が彼の海への親近感を育てたとされ、幅広い都市で活動したのち故郷のフェオドシヤに拠点を保ち、1880年にそこに美術館を開いた。所蔵館は本作品の制作年を示していないため、特定年と同館の1880年開館を混同しない。絵の海域を黒海の特定場所と断定しない。",
    "visual": "Met API原寸・表示JPEGを実取得、SHA256と縮小RMSで照合し、公式主画像を視認。幅広い小さな油彩画で青灰色の月夜、左上寄りに丸い黄白色の月、その光が前景の波打つ海に反射する。画面右寄りの遠くの水平線には細長い船体・マスト・煙突状の構造物の船があり、手前には暗い岸辺がある。波に光る細い帯と暗い空が印象的。",
    "caution": "画家はアルメニア系でロシア帝国領クリミア（現在はウクライナの国際承認された領土）出身。作品の年代・描かれた海域はMetに明記なし。蒸気船の解釈は公式個別解説に従う。月の位置と海面の色彩は実画面の観察として区別する。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "自然",
      "時間"
    ],
    "text": "薄い月の光が、暗い海面の波に細く反射しています。遠くには、マストと煙突のある船の姿。近くの岸辺は暗く沈み、月から海へと続く明るさが画面の奥行きを生んでいます。\n\nこの小さな油彩画は、海景を数多く描いたイワン・アイヴァゾフスキーの作品です。帆船を好んだ画家でしたが、ときにはこの絵のような近代的な蒸気船も描きました。月明かりの海に機械の船が浮かぶところに、自然の光と新しい時代の風景が重なっています。\n\n画家は当時ロシア帝国領だったクリミア半島の港町フェオドシヤで、アルメニア系の家族に生まれました。黒海の近くで育ったことは、海を描く関心につながったと美術館は説明しています。ただし、この絵がどの海を描いたのか、正確にいつ制作されたかまでは分かりません。月の光と船の影をたどりながら、静かな海の広がりを感じてみてください。",
    "checks": [
      [
        "He preferred to depict sailing ships, but sometimes portrayed modern steamships",
        "帆船を好んだ画家でしたが、ときにはこの絵のような近代的な蒸気船も描きました。",
        "Exact Met artwork Overview: sailing ships versus steamships"
      ],
      [
        "the Black Sea port of Feodosia (Theodosia) in Crimea",
        "画家は当時ロシア帝国領だったクリミア半島の港町フェオドシヤで、アルメニア系の家族に生まれました。",
        "Exact Met artwork Overview: birthplace at Feodosia in Crimea"
      ]
    ]
  },
  "448485": {
    "number": 408,
    "japanese": "宮廷女性たちの集い",
    "artist": "Unidentified artist",
    "culture": "India (attributed)",
    "situation": "17〜18世紀のインド細密画に描かれた、宮廷女性たちの団らんと色鮮やかな織物や宝飾品を眺めたい",
    "meaning": "Metの個別作品Overviewによると17世紀末～18世紀初めのデイヴィス・アルバムの一葉は、宮廷女性たちが中国に影響を受けた鳳凰・雲模様の織物の上にもたれ、ザクロや桃を食べ、太鼓の音に耳を傾ける場面。女性たちだけでなく乳児の手足にも真珠・ルビー・金の宝飾があしらわれている。宮廷女性たちの生活をうかがわせる希少な図であるという解説で、描かれた特定の集まりを実際の日時の記録として断定していない。制作地は『Attributed to India』で画家名も不明。",
    "visual": "Metの実際の原寸JPEGと表示JPEGを取得してハッシュ・縮小RMSを比較し、API由来の主画像を視認。赤みを帯びた紙の中央の細長い彩色画面で、複数の女性が黄色や赤、白などの衣をまとって並び、下部に大きな太鼓、青い絨毯に似た布と花果・金の飾り、右側の緑の窓のような枠、周囲の広いアルバム紙縁が見える。細かな宝石・果物の種類は公式解説に基づく。",
    "caution": "制作地はインドと推定にとどまる。宮廷女性の実生活を写真のように忠実に記録したと断定しない。赤い外枠はアルバムの余白であり絵の場面の一部ではない。画家は不明。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい"
    ],
    "themes": [
      "共同体",
      "日常"
    ],
    "text": "鮮やかな色の衣服をまとった女性たちが、模様のある布の上に集まっています。果物を口に運ぶ人、音楽に耳を傾ける人がいて、画面の下には太鼓も見えます。人物の周りには、赤や青、金の細かな装飾が重なっています。\n\n17世紀末から18世紀初めにかけてのインドに帰属される細密画で、アルバムの一葉として残りました。女性たちが身を寄せる織物には、中国風の鳳凰や雲の模様が描かれています。ザクロや桃が用意され、室内の集まりの様子が色彩豊かに表されています。\n\n真珠やルビー、金の装身具は女性だけでなく、描かれた幼い子どもの手足にも施されています。美術館は、宮廷の女性たちの暮らしをうかがわせる珍しい場面として紹介しています。ただし、ここで特定の会合が実際に開かれたという記録ではありません。装身具と織物を見比べると、華やかな場面を細部から読み取れます。",
    "checks": [
      [
        "reclining on textiles with Chinese-inspired phoenixes and clouds",
        "女性たちが身を寄せる織物には、中国風の鳳凰や雲の模様が描かれています。",
        "Exact Met artwork Overview: Chinese-inspired textile designs"
      ],
      [
        "eating pomegranates and peaches, and listening to the drum",
        "ザクロや桃が用意され、室内の集まりの様子が色彩豊かに表されています。",
        "Exact Met artwork Overview: fruit and percussion in court gathering"
      ]
    ]
  },
  "449536": {
    "number": 410,
    "japanese": "『ヨハネによる福音書』の扉絵",
    "artist": "Sargis (illuminator)",
    "culture": "Armenia (Siwnik)",
    "situation": "14世紀初頭のアルメニアの彩飾写本で、動物の姿をした文字と四福音書記者の象徴を眺めたい",
    "meaning": "Metの個別作品Overviewは1300～1310年頃のアルメニアの写本彩飾画家サルギスによるヨハネ福音書の扉ページとして、最初の大きな頭文字と装飾枠に四福音書記者の象徴（マタイの天使、マルコの獅子、ルカの牛、ヨハネの鷲）を盛り込み、ビザンティン風の幾何学紋様を広げたと説明。文字そのものが鳥の形で書かれた部分があり、上部には孔雀に挟まれ祝福するキリストを置く。古代アルメニアの神学者は鳥を天へ飛び立つ魂の比喩として捉えた。日本語本文は福音書そのものの神学的事実と美術館による図像解釈を分けて書く。",
    "visual": "実際のMet APIの原寸と表示JPEGのサムネイルを視認。縦長の黄みを帯びた紙の上部に赤・青・金の入り組んだ装飾枠と小さな人物像があり、中央左に巨大な彩色頭文字のような装飾、下に細長い色付き文字列、右に植物や鳥のような細長い装飾がある。紙の隅はやや欠け、装飾文字の形はMet個別解説で確かめた。",
    "caution": "作品は彩色装飾を施した写本の1ページで、単独の油彩画や宗教書全巻ではない。メトロポリタン美術館によれば彩飾担当はサルギスで、写本本文の筆写者まで同一人物と断定しない。鳥の意味は伝統的な神学の象徴。",
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
    "text": "紙の上部には、赤や青、金色の細かな模様が重なり、文字の形そのものが絵のように装飾されています。ところどころに鳥や獣、人の姿が見え、文章を読み始める前から視線が細部へと引き込まれます。\n\nこの作品は、1300～1310年頃のアルメニアで制作された『ヨハネによる福音書』の彩飾された扉ページです。画家サルギスは、大きな頭文字とその周りに、四人の福音書記者を表す天使・獅子・牛・鷲を組み込みました。最初の言葉の中には、鳥の形に作られた文字もあります。\n\n上部には二羽の孔雀に囲まれ、人々を祝福するキリストが描かれています。美術館は、アルメニアの初期の神学者が鳥を天へ飛び立つ魂の象徴と捉えたことも紹介しています。幾何学的な模様と生き物の姿をたどると、文字を装飾することが宗教的な意味を伝える手段にもなっていたと分かります。",
    "checks": [
      [
        "the symbols of the four evangelists—an angel for Saint Matthew",
        "画家サルギスは、大きな頭文字とその周りに、四人の福音書記者を表す天使・獅子・牛・鷲を組み込みました。",
        "Exact Met artwork Overview: four evangelists represented by creatures"
      ],
      [
        "Bird-shaped letters form the first words of the text",
        "最初の言葉の中には、鳥の形に作られた文字もあります。",
        "Exact Met artwork Overview: bird-shaped initial letters"
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
          "Met 448485 is attributed to India rather than definitively sourced; Met 437979 is undated in the official API and object-page record; Met 449536 is a painted book folio, with Sargis credited as illuminator."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==407,"main must have exactly 407 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：410作品**。mainへ統合後のDBとREADMEを正本とする。
- **次：411作品目から候補調査**。作品別Met公式Overview、既登録との重複、画像原寸・表示JPEGと著作権を個別に確認。
- 今回408〜410：`met-448485`《宮廷女性たちの集い》（17世紀末〜18世紀初め、インドに帰属）、`met-437979` アイヴァゾフスキー《月夜の船》（制作年不詳、アルメニア系でクリミア出身の画家）、`met-449536` サルギス《ヨハネによる福音書の扉絵》（1300〜1310年、アルメニア）。
- 作品別Overviewの実際の本文を直接読んで各2箇所ずつ短い原文抜粋と独自日本語鑑賞文の重要主張を照合した。437979の公式作品年は空欄であり、推測した制作年は入れていない。449536は彩飾写本の一葉であり、油彩画ではないことを明示。
- Met APIの作品PD、公式JPEG Open Access CC0、所蔵館の現代解説文の著作権は別に扱った。原寸・表示JPEGを完全取得しSHA256、ファイルサイズ、寸法、縮小RMSを記録してサムネイルも直接確認。根拠は[408〜410画像調査](artwork-research-evidence/met-408-410-2026-11-13.json)。
- 作品別監査の再照合は同じAIが別工程として行っており、人間や独立した専門家・モデルの検証ではない。先行407作品と画像台帳の以前の記録は変更していない。研究ファイルには除外した重複候補も含む。
"""
    temp=ROOT/"tmp-artwork-resume-408.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==410,"final count mismatch")
    print("ALL PASS: 410 new total, existing 407 preserved",flush=True)
if __name__=="__main__":
    main()
