#!/usr/bin/env python3
"""One-off source-reviewed registration for #432-434. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-432-434-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-432-434-20261113/"+EVIDENCE
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
  "437183": {
    "number": 434,
    "japanese": "狩猟の女神ディアナに扮したベルジュレ・ド・フルーヴィル夫人",
    "artist": "Jean Marc Nattier",
    "culture": "France (18th-century court portrait)",
    "situation": "18世紀フランスの女性がディアナ女神に扮した肖像で、弓や矢筒、豹の毛皮と当時の装いがどう組み合わされたか見たい",
    "meaning": "Met個別作品Overviewによれば1756年のナティエによるベルジュレ・ド・フルーヴィル夫人の肖像。狩猟の女神ディアナは女性の美徳と力を表し、一方でニンフに囲まれて森で水浴びする姿が官能的に描かれる場合もある。ナティエは多くの女性の肖像でディアナの姿を借り、現代風の髪型・化粧と、弓、矢筒、豹の毛皮などの小道具を重ね合わせて、日常を超えた神話的な存在として見せた。美術館はこの演出を仮装や演劇を愛する当時の社交界に特徴的だとする。夫はブーシェやユベール・ロベールなどの画家の重要なパトロンだった。実際の狩猟活動や女神への信仰心の証拠とはしない。",
    "visual": "Met公式APIの原寸JPEG・表示JPEGを完全ダウンロードし全SHA256、ファイルサイズ、寸法、縮小RMSを照合して主画像サムネイルを見た。縦長の油彩で背景左の大木と暗い森、中央に淡い肌の女性が赤い大きなスカートと白い衣をまとい、弓を立てて持つ。胸元にまだら模様の豹皮、肩の近くに矢筒、光を受けた顔と当時風にまとめられた髪が見える。",
    "caution": "肖像の人物は実在のベルジュレ・ド・フルーヴィル夫人だが、女神ディアナ本人の姿を見た絵ではない。弓矢や豹皮は肖像のための小道具であり、本人が狩猟家だったとは断定しない。ディアナを『貞淑さだけの象徴』と単純化せず、所蔵館の説明する複数の意味を尊重する。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "静けさ",
      "高揚"
    ],
    "themes": [
      "共同体",
      "他者との距離"
    ],
    "text": "森を背にした女性が、長い弓を手にこちらを見ています。赤い布が大きく広がり、胸元にはまだら模様の毛皮。上品にまとめた髪や化粧は18世紀の装いですが、弓や矢筒は神話の世界を思い起こさせます。\n\n1756年、フランスの画家ジャン＝マルク・ナティエが、ベルジュレ・ド・フルーヴィル夫人を狩猟の女神ディアナに見立てて描いた肖像画です。ナティエはほかの女性肖像でもディアナの姿を取り入れ、当時の髪型や化粧と、弓や矢筒、豹の毛皮などの小道具を組み合わせました。\n\n女神ディアナは女性の力や美徳を表す一方、神話の絵では森で水浴びする姿が描かれることもありました。美術館は、こうした仮装のような演出を、演劇や仮面舞踏を好んだ当時の社交界の文化と結びつけています。夫人が実際に狩猟をしたという意味ではありません。日常の装いと神話の道具の境目を眺めると、肖像画の見せ方の巧みさが感じられます。",
    "checks": [
      [
        "Nattier used her disguise when portraying many of his female sitters",
        "ナティエはほかの女性肖像でもディアナの姿を取り入れ、当時の髪型や化粧と、弓や矢筒、豹の毛皮などの小道具を組み合わせました。",
        "Met exact Overview: Diana disguise in multiple Nattier portraits"
      ],
      [
        "including the bow, quiver, and panther skin",
        "上品にまとめた髪や化粧は18世紀の装いですが、弓や矢筒は神話の世界を思い起こさせます。",
        "Met exact Overview: mythological props bow quiver panther-skin, but Japanese claim names only bow and quiver"
      ]
    ]
  },
  "845161": {
    "number": 433,
    "japanese": "蘭亭曲水図",
    "artist": "Hara Zaichū 原在中",
    "culture": "Japan (Edo period)",
    "situation": "1829年の日本の山水掛軸で、中国の蘭亭の宴と曲水に杯を流して詩を作る文人たちの様子を眺めたい",
    "meaning": "Met作品別Overviewによると原在中が1829年に描いた蘭亭曲水図は、中国の名書家・王羲之（約303〜361年）の伝説的な蘭亭の集いを想像して構成した風景。伝承では王羲之が41人を流れる小川のほとりへ招き、下流へ流れる杯の酒を飲みながら詩を作り、その序文が中国・日本の文人に長く記憶された。画中には青く輝く衣の人物たちが川岸に集まり、王羲之は亭の中で巻物を広げ筆を持っている。鮮やかな青と緑の山水色彩は古い中国の青緑山水（せいりょくさんすい）に由来。歴史的な集いの想像図であり1829年の京都で実際に集会が開かれた記録ではない。",
    "visual": "Met APIが紐づける原寸・表示JPEGの全SHA256、バイト長、寸法と縮小RMSを比較、主画像サムネイルを直接確認。縦長の絹本掛軸で背後に淡い山々、下の緑色の河畔と大きく曲がる水路の周囲に数多い青衣の小さな人物が散らばる。右寄りの木立のそばに屋根のある亭と人物、川岸の緑が目立つ。人物個々の同定はMet公式解説に基づく。",
    "caution": "描かれたのは古代中国の文人の集いを江戸時代の画家が想像した場面で、当日の記録や測量図ではない。王羲之と41人の集いは題材の歴史伝承として説明。『蘭亭序』の名声と実際の画面に描かれた小場面を区別し、杯の位置を実画像から断定しない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい",
      "静けさ"
    ],
    "themes": [
      "共同体",
      "自然",
      "時間"
    ],
    "text": "山に囲まれた緑の岸辺を、曲がりくねった小川が流れています。青い衣を着た人々が川のそばに集まり、木陰や小さな亭の中にも人物の姿が見えます。まず水の流れを追ってから、離れた場所にいる人々の動きに目を向けてみてください。\n\nこの絵は1829年に原在中が描いた《蘭亭曲水図》です。古代中国の書家・王羲之が友人たちを招いたと伝えられる宴を、江戸時代の画家が想像して表しています。伝承では、一同は流れる杯の酒を楽しみながら詩を作りました。王羲之は亭の中で巻物を広げ、筆を持つ姿として描かれています。\n\n人物の青い衣や深い緑の山々には、中国で古くから伝わる青緑山水の色彩が取り入れられています。王羲之が詩の集まりに寄せた序文は、後の中国と日本の文人にも大きな影響を与えました。曲がる川と人々の配置を眺めると、書と詩を楽しむ時間を絵にした工夫が見えてきます。",
    "checks": [
      [
        "where they composed poetry and drank wine from cups sent downstream",
        "伝承では、一同は流れる杯の酒を楽しみながら詩を作りました。",
        "Met exact Overview: wine cups and poetry in the winding stream gathering"
      ],
      [
        "Wang is shown seated within the pavilion, a scroll spread before him",
        "王羲之は亭の中で巻物を広げ、筆を持つ姿として描かれています。",
        "Met exact Overview: Wang Xizhi shown writing at pavilion"
      ]
    ]
  },
  "853895": {
    "number": 432,
    "japanese": "花鳥図屏風",
    "artist": "Unidentified Korean artist",
    "culture": "Korea (Joseon dynasty)",
    "situation": "朝鮮王朝の八面の花鳥屏風で、鶴や孔雀や鳳凰と草花に込められた吉祥の意味、季節の移ろいを眺めたい",
    "meaning": "Met個別作品Overviewによると、東アジアの花鳥画は10世紀までに確立し、朝鮮では18世紀から花鳥屏風が広まり20世紀まで好まれた。19世紀の本品は現在二組の四面屏風に分かれるが、元は八面が一続きの屏風であった。鴨・孔雀・鶏・架空の鳳凰のつがいは恋愛と子宝、鶴・松・霊芝・竹・蓮は長寿と徳の吉祥を示す。八面を右から左に追うと、新年の朝日と松のそばの鶴から始まり、秋の葉の中の鳳凰まで四季の移ろいをたどる読み方もできる。公式画像が見せる四面と、元の八面構成は混同しない。",
    "visual": "Met API公式主原寸・表示JPEGを全バイトSHA256、バイト長、寸法、縮小RMSで突き合わせた実画像サムネイルを視認。横長の画面は枠で区切られた四つの縦長の屏風面で、淡い紙地に赤や桃色の草花、鳥の組み合わせ、右端近くには赤い日輪と松らしい樹形、左端には花が描かれる。主画像は四面を示し、八面全体の細部はこの画像だけでは見られない。",
    "caution": "作者は不明。現在は四面ずつの二組に分かれた元八面の作品であり、四面しか存在しないと説明しない。花鳥の吉祥性は文化的象徴であり、家庭に実際の幸運が訪れると保証しない。主画像の四面だけを全体の八面の完全な再現と扱わない。",
    "emotions": [
      "好奇心"
    ],
    "tones": [
      "にぎわい",
      "余韻"
    ],
    "themes": [
      "自然",
      "時間",
      "愛情"
    ],
    "text": "花や果実の間に、さまざまな鳥たちが描かれています。淡い紙の上に赤や緑の色が重なり、一つひとつの画面が異なる季節や生き物を見せてくれます。鳥の姿を追いながら、草花の形や背景の余白も見比べてみてください。\n\n19世紀の朝鮮で描かれた花鳥図屏風です。現在は四面ずつの二組になっていますが、もとは八面が一続きの屏風でした。鴨や孔雀、鶏や想像上の鳳凰がつがいで描かれ、恋や子孫の繁栄を連想させます。鶴や松、竹や蓮などには、長寿や徳を願う意味が込められています。\n\n八面を右から左へたどると、鶴と松、新年の朝日から始まり、秋の葉の中の鳳凰へと移る四季の流れとしても読めます。今の主画像には二組のうち四面が写っています。色や鳥の配置を見ながら、元の長い屏風を少しずつ開いて鑑賞する様子を想像してみてください。",
    "checks": [
      [
        "these paintings would have originally been one screen with eight panels",
        "現在は四面ずつの二組になっていますが、もとは八面が一続きの屏風でした。",
        "Met exact Overview: original eight-panel screen later split into two sets"
      ],
      [
        "Pairs of ducks, peacocks, chickens, and mythological phoenixes",
        "鴨や孔雀、鶏や想像上の鳳凰がつがいで描かれ、恋や子孫の繁栄を連想させます。",
        "Met exact Overview: paired birds and their symbolic meanings"
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
          "Met 853895 once formed a single eight-panel screen, now two four-panel sets, with bird/flower auspicious symbolism; Met 845161 imagines Wang Xizhi’s Orchid Pavilion gathering from ancient Chinese tradition, not a firsthand scene; Met 437183 portrays Madame Bergeret de Frouville as Diana, with painted disguise props and no proof of actual hunting activity."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==431,"main must have exactly 431 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：434作品**。main統合後はDBとREADMEが正本。
- **次：435作品目から候補調査**。Met作品別公式Overview・重複・公式原寸と表示JPEG・パブリックドメイン/CC0・著作権を作品ごとに確認。
- 今回432〜434：`met-853895`《花鳥図屏風》（19世紀、朝鮮、元八面のうち主画像は四面）、`met-845161` 原在中《蘭亭曲水図》（1829年、日本、古代中国の文人の宴を想像して描いた掛軸）、`met-437183` ナティエ《狩猟の女神ディアナに扮したベルジュレ・ド・フルーヴィル夫人》（1756年、フランス）。
- 作品ごとの公式Met Overviewを直接読み、二箇所の短い英文抜粋を独自の日本語鑑賞解説と照合。朝鮮の屏風は元八面だが現在四面ずつ二組。蘭亭曲水図は王羲之の集いを江戸時代に想像したもの。フランスの肖像は現代の装いと狩猟女神の小道具を組み合わせた仮装的な絵で、本人の狩猟の証拠ではない。
- Met公式の作品PD、Open Access画像のCC0、現代の学芸員解説の著作権を個別に区別。原寸と表示JPEGの全バイトSHA256・サイズ・寸法・縮小RMS、真正な公式画像サムネイルの実見は[432〜434画像調査](artwork-research-evidence/met-432-434-2026-11-13.json)を参照。研究記録には今回未採用の既登録作品や他候補も含む。
- 再審査は同じAIによる別工程で、独立した人間・専門家・別モデルの検証ではない。先行431作品と過去の画像台帳部分は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-432.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==434,"final count mismatch")
    print("ALL PASS: 434 new total, existing 431 preserved",flush=True)
if __name__=="__main__":
    main()
