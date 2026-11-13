#!/usr/bin/env python3
"""One-off source-reviewed registration for #429-431. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-429-431-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-429-431-20261113/"+EVIDENCE
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
  "437182": {
    "number": 429,
    "japanese": "女性の肖像",
    "artist": "Jean Marc Nattier",
    "culture": "France (18th-century portrait)",
    "situation": "18世紀フランスの女性肖像に描かれた青いリボンと花、柔らかな肌の表現から、流行と個性の関係を考えたい",
    "meaning": "Metの個別Overviewによると、ナティエはフランスの貴族女性の肖像を数多く手がけ、作品では一人ひとりの差異よりも、白い肌と赤い頬、白粉をつけた髪と穏やかな目鼻立ちを共有する流行が重要だった。本作は1753年の晩年の肖像で、木の幹に署名と年が記されている。色鮮やかな花が周囲に配され、青いリボンが首と肩の素肌を際立たせる。美術館は絵具の下から見える描き直し（ペンティメント）が髪とリボンの位置にあると指摘する。描かれた女性の実際の氏名は題名にもOverviewにも明記されていない。",
    "visual": "Met公式APIから得た原寸と表示用JPEGを実ダウンロードしSHA256・バイト数・画像サイズ・縮小RMSを記録、主画像のサムネイルを直接確認。暗い緑の背景の前に白く粉を吹いたようなまとめ髪の若い女性。胸元に水色の布、首元に小さな濃青のリボン。両手には淡い花束、手前にも花と小さなかごがあり、画面左側に木の幹がある。描き直しはサムネイルでは判読できず公式Overviewの説明に基づく。",
    "caution": "『個性より共通した流行』は画家の描いた多くの肖像をめぐるMetの様式的解釈であり、描かれた女性の実際の人格を否定しない。木にある署名・年はMetによる情報。透けて見える描き直しの細部は主サムネイルでは確認不能。女性の身元や職業は断定しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "日常",
      "他者との距離"
    ],
    "text": "暗い緑の背景から、淡い青の布をまとった女性が静かに浮かび上がります。首元には小さな青いリボン、手元には色とりどりの花。白い肌とほのかに赤い頬、粉をまとった髪が、当時の上流社会の装いを伝えています。\n\nこの絵はフランスの画家ジャン＝マルク・ナティエが1753年に描いた肖像画です。ナティエの肖像では、人物ごとの違いを際立たせるより、白い肌や赤い頬など、共通する流行の美しさが重んじられました。画面左の木の幹には、画家の署名と制作年が記されています。\n\n美術館は、青いリボンと髪の位置が制作途中で何度か描き直されたことを指摘しています。表面に残る薄い痕跡から、完成した姿の背後に画家の試行錯誤が見えてきます。ただし、描かれた女性の名前は明らかではありません。リボンや花に目を向けると、この時代に理想とされた美しさの形が感じられます。",
    "checks": [
      [
        "Conformity rather than individuality was a hallmark of Nattier’s enormous success",
        "ナティエの肖像では、人物ごとの違いを際立たせるより、白い肌や赤い頬など、共通する流行の美しさが重んじられました。",
        "Met exact artwork Overview: preferred shared aristocratic portrait conventions"
      ],
      [
        "Nattier made several adjustments to the position of the ribbon and hair",
        "美術館は、青いリボンと髪の位置が制作途中で何度か描き直されたことを指摘しています。",
        "Met exact artwork Overview: ribbon and hair pentimenti"
      ]
    ]
  },
  "853196": {
    "number": 430,
    "japanese": "菊の和歌",
    "artist": "Shōren’in Sonchō Hosshinnō 青蓮院尊朝法親王",
    "culture": "Japan (court calligraphy, late 16th century)",
    "situation": "一輪の菊を描くのではなく、菊の花が終わる季節を言葉と文字の筆跡で表した和歌を眺めたい",
    "meaning": "Met個別Overviewによれば、16世紀後半の尊朝法親王による和歌懐紙であり、菊が散った後の一年を回想する歌が墨書される。尊朝は和歌の通常の仮名のかわりに、漢字を音で用いる古い草仮名（そうがな）を筆記し、濃く太い仮名が漢字と同じほどの視覚的な重みを持つよう工夫した。青蓮院は室町後期の宮廷書法の主要な拠点であり、尊朝は王家に生まれ、青蓮院の皇族僧として書を学び後進に伝えた。制作された歌会の日付や具体的な状況を示す史料は残らず、菊と皇室の家紋との関係は美術館の図像的な読みとして提示される。",
    "visual": "Met作品ID853196の公式原寸・表示JPEGを全バイト取得し、SHA256・寸法・縮小RGB RMSを保存、実際の主画像サムネイルを確認。薄黄色の正方形に近い書面の上部に右から墨書の題字があり、下部に流れるような複数行の墨の線。周囲は緑と金色の布に表装され、字の太さは太細が対照的。花の実物が写生されているのではなく和歌の文字の書。",
    "caution": "『菊の和歌』は書の作品であり、菊の花を描いた花鳥画ではない。歌会や制作の個別状況は不明で、皇室の菊紋との連想も推論として扱う。詩の日本語の正確な表記は原文に拠るが、本文では内容を簡潔に意訳するにとどめる。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "余韻"
    ],
    "themes": [
      "時間",
      "記憶"
    ],
    "text": "淡い紙の上を、濃い墨の文字がゆっくりと流れています。菊の花を描いた絵ではなく、菊が咲き終えた後に過ぎる一年を思う和歌を、筆の線そのもので見せる作品です。字の強い部分と細い部分を見比べてみてください。\n\n16世紀後半、皇族で青蓮院の僧でもあった尊朝法親王が記した和歌懐紙です。尊朝は草仮名と呼ばれる、漢字を音として使う古い仮名表記を取り入れ、仮名が漢字と同じような力強さを持つ書き方を試みました。青蓮院は、当時の宮廷書法を学ぶ重要な場所でした。\n\n美術館は、この和歌がどの歌会で、どんな事情から書かれたのかを示す記録は残っていないと説明しています。皇族が菊について詠むことは皇室の菊の紋章も連想させますが、特定の催しを証明するものではありません。歌の意味と墨の線を交互に見ると、書が言葉と造形の両方を伝えることに気づけます。",
    "checks": [
      [
        "by employing sōgana, highly cursive Chinese characters (kanji) used phonetically",
        "尊朝は草仮名と呼ばれる、漢字を音として使う古い仮名表記を取り入れ、仮名が漢字と同じような力強さを持つ書き方を試みました。",
        "Met exact artwork Overview: phonetic sōgana"
      ],
      [
        "We have no surviving evidence documenting the circumstances or poetry gathering",
        "美術館は、この和歌がどの歌会で、どんな事情から書かれたのかを示す記録は残っていないと説明しています。",
        "Met exact artwork Overview: no recorded performance circumstance"
      ]
    ]
  },
  "853894": {
    "number": 431,
    "japanese": "祖先祭祀の祠を描いた絵",
    "artist": "Unidentified Korean artist",
    "culture": "Korea (Joseon dynasty)",
    "situation": "朝鮮王朝時代の祭祀の祠と供物を描いた色彩画から、祖先を敬う儀礼と持ち運べる絵の役割を知りたい",
    "meaning": "Met個別Overviewによると、儒教の『孝』は親や祖父母への敬意と尊重を重視し、朝鮮王朝の社会では祖先を祭る祭祀（チェサ）が重要な儀礼だった。祭祀は祠堂（サダン）で祖先の名を書いた位牌を置き、食べ物や酒などの供物を備えた台を前にして行われた。この19世紀の絵は祠堂の外観と供物台を描き、家庭に祠堂を設けない人や、家を離れて儀礼を行う人が祠堂に代えるためにも使ったという。特定家族に結びつく絵であるかは作品ページに明記されず、作者の姓名も不明。",
    "visual": "Met公式APIの主原寸/表示JPEGの完全SHA256と縮小RGB RMSを照合して、実際の主画像サムネイルを確認。額装の縦長の絵。上部に漢字風の文字と模様の帯、その下に屋根と柱を描いた正面向きの建物、中央には花・器・供物を載せた台が整然と並び、左右の植物や飾りと下部の脚付きの台が見える。人間の人物像は主題の中心ではない。",
    "caution": "祭祀の実際の開催場面ではなく、祠堂と供物台を表した絵。どの家の祖先やどの氏族の絵だったかを推測しない。祭礼の効験を事実として述べない。祭祀の重要性は朝鮮王朝の儒教的社会制度の文脈。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "静けさ",
      "落ち着き"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "正面を向いた小さな祠の絵には、屋根と柱、器を並べた供物台が整った形で描かれています。上の帯には文字が置かれ、左右の植物や色彩の模様が建物を囲みます。人の姿を描くより、儀礼の場所そのものを画面の中心に据えていることが特徴です。\n\n19世紀の朝鮮で作られた《祖先祭祀の祠を描いた絵》です。儒教では親や祖父母を敬う「孝」が重視され、祖先を祭るチェサという儀礼は朝鮮王朝の社会で重要な役割を担いました。祠堂では祖先の位牌を置き、食べ物や飲み物を供える台を設けていました。\n\nこのような絵は、自宅に専用の祠堂がない人や、家から離れた場所で祭祀を行う人が、実際の祠堂の代わりに使うことがありました。ただし、どの家の儀礼で使われた絵なのかは分かりません。建物の形と供物の配置を見比べると、祖先とのつながりを絵で表そうとした文化が見えてきます。",
    "checks": [
      [
        "Ceremonial rituals honoring one’s ancestors, called jesa",
        "祖先を祭るチェサという儀礼は朝鮮王朝の社会で重要な役割を担いました。",
        "Met exact artwork Overview: jesa ancestor ceremonies"
      ],
      [
        "Ancestral shrine paintings were used as substitutes by people who did not have a sadang",
        "このような絵は、自宅に専用の祠堂がない人や、家から離れた場所で祭祀を行う人が、実際の祠堂の代わりに使うことがありました。",
        "Met exact artwork Overview: portable stand-in for ancestral shrine"
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
          "Met 437182 notes ribbon and hair pentimenti without giving sitter name; met-853196 is an ink calligraphy waka sheet and has no evidence identifying a particular poetry gathering; met-853894 depicts the ancestral shrine and offerings as an alternate support for jesa rituals, not an identified family ceremony."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==428,"main must have exactly 428 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：431作品**。mainへの統合後はDBとREADMEを正本とする。
- **次：432作品目から候補調査**。Met公式作品別Overviewの原文・既登録ID・公式JPEG両サイズ・権利と画像台帳を作品別に照合。
- 今回429〜431：`met-437182` ナティエ《女性の肖像》（1753年、フランス）、`met-853196` 尊朝法親王《菊の和歌》（16世紀後半、日本、和歌懐紙の書）、`met-853894`《祖先祭祀の祠を描いた絵》（19世紀、朝鮮）。
- 作品別Met公式Overviewの実文面を確認し、各2箇所の短い原文英文を独自日本語鑑賞文の重要主張に対応。ナティエのリボンと髪には描き直しの痕が残る。尊朝の和歌懐紙は書であり菊の花の絵ではなく、歌会の事情は未確認。祖先祭祀の祠の絵は家に祠堂がない、または遠方で儀礼を行う人の代替として使われた。
- 作品PD表示とMet公式JPEGのOpen Access CC0、所蔵館の現代解説文の著作権は分離。原寸・表示用JPEGの全バイトSHA256・ファイルサイズ・寸法・縮小RMS・公式画像サムネイルの実見は[429〜431画像調査](artwork-research-evidence/met-429-431-2026-11-13.json)に記録。候補調査から除外した重複・画像不適合・権利制限作品も研究ファイルに含まれる。
- 同じAIによる別工程の再確認であり、外部の人間・専門家・別モデルによる独立査読ではない。既存428作品と画像台帳の過去記録は不変。
"""
    temp=ROOT/"tmp-artwork-resume-429.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==431,"final count mismatch")
    print("ALL PASS: 431 new total, existing 428 preserved",flush=True)
if __name__=="__main__":
    main()
