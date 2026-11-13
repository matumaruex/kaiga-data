#!/usr/bin/env python3
"""One-off source-reviewed registration for #405-407. Runs only on the temporary work branch."""
import copy
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATE="2026-11-13"
EVIDENCE="docs/artwork-research-evidence/met-405-407-2026-11-13.json"
RESEARCH_URL="https://github.com/matumaruex/kaiga-data/blob/codex/artworks-405-407-20261113/"+EVIDENCE
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
  "39581": {
    "number": 405,
    "japanese": "滝を眺める中国の文人",
    "artist": "Follower of Soga Shōhaku",
    "culture": "Japan (Edo period)",
    "situation": "大胆な筆づかいで描かれた滝と絶壁の風景で、小さな人影と自然の大きさを見比べたい",
    "meaning": "Metの作品別Overviewは、巨大な山水の中に占める人の小ささを主題とし、左の崖の文人が滝を眺め、右の危うい橋を旅人が渡って寺を目指す構図と説明する。滝の飛沫は龍のように人の上に弧を描き、山並みや枯れ木は穏やかな自然より不穏な自然の強さを強調する。蕭白の奇抜さを模倣した作だが、仕上がりの硬さなどからMetは曽我蕭白本人ではなくその追随者による作とする。Met APIのartistDisplayNameがSoga Shōhakuとなるのに対し公式の個別作品ページの表示はFollower of Soga Shōhakuなので、後者と学芸員による説明を優先する。",
    "visual": "Met APIの原寸・表示JPEGの全バイトハッシュと縮小RMSを調査し、公式主画像サムネイルを視認。金茶色の横長二曲屏風。左寄りに深い落下の滝と向き合う極小の人物が見え、奥には濃淡の山や木、右に木と高所の屋根のある建物がある。巨大な滝の白いしぶきが弧を描く。細部の人物名などは画像だけでは分からない。",
    "caution": "作者は曽我蕭白本人とは断定しない。Met APIとウェブページの帰属表示の差を監査に明記し、所蔵館の個別解説による追随者への帰属を採用。人物の危険や感情は研究者の読みであって当事者の記録ではない。",
    "emotions": [
      "不安"
    ],
    "tones": [
      "緊張",
      "静けさ"
    ],
    "themes": [
      "自然",
      "他者との距離"
    ],
    "text": "画面いっぱいにそびえる山と断崖の中では、人の姿は驚くほど小さく描かれています。左の崖際では文人が遠くの滝を眺め、右側では旅人が細い橋を渡っています。大きく弧を描く滝の飛沫に注目すると、静かな風景の中に不思議な緊張感も感じられます。\n\n江戸時代の絵画《滝を眺める中国の文人》です。曽我蕭白の奇抜な山水画を思わせますが、メトロポリタン美術館は構図や筆づかいの硬さなどから、制作は蕭白本人ではなく、彼の画風を受け継いだ画家によると考えています。従来の美しい山水の趣を借りながらも、この絵では人間が自然の広がりに圧倒されるように描かれています。\n\n右側の人物は、霧の中に続く寺を目指しているようにも見えます。ただし、画中の物語を細部まで断定することはできません。二曲屏風を右から左へ眺め、細い道や滝のしぶきが作る動きを追うと、画面の大きな空間が違って見えてきます。",
    "checks": [
      [
        "a gentleman sits contemplating a distant waterfall",
        "左の崖際では文人が遠くの滝を眺め、右側では旅人が細い橋を渡っています。",
        "Exact Met object Overview: scholar and waterfall on left"
      ],
      [
        "it is safe to assume that this work was created by a follower",
        "制作は蕭白本人ではなく、彼の画風を受け継いだ画家によると考えています。",
        "Exact Met object Overview: attributed to follower, not Soga himself"
      ]
    ]
  },
  "309529": {
    "number": 407,
    "japanese": "聖ゲオルギウスと玉座の聖母子の携帯イコン",
    "artist": "Northern or Central Highlands artist",
    "culture": "Ethiopia (Ethiopian Orthodox Christianity)",
    "situation": "エチオピアの小さな二面の携帯用聖画を開いて、聖母子と竜退治の二つの図像が並ぶ意味を見たい",
    "meaning": "Met作品別Overviewによれば、木製の開閉式小箱の内部に二面の聖画を持ち、上部の穴を利用して首から下げられる個人用イコン。中央の玉座の聖母子を天使たちが囲み、隣の面には白馬に乗った聖ゲオルギウスが槍で竜を倒す場面が描かれる。エチオピア正教の伝統における守護や祈りと結びついた図像で、ヨーロッパのマリア像からの図像的影響を独自の様式へと変えている。Metは制作を18世紀としている一方、木箱は古くても彩色の一部が20世紀に塗り直された可能性に触れる。この推定は確定年代ではなく再制作の断定は避ける。",
    "visual": "Met公式API主画像を原寸/表示とも実取得し、サムネイルで確認。灰色の展示背景に木の小箱が左右に開かれ、左の絵は白馬の聖ゲオルギウスが槍を構える赤青緑の彩色図、右は青い衣の聖母子が玉座に座り、その両側に色鮮やかな天使がいる。上部の吊り下げ用飾りと蝶番、傷んだ彩色の細部も見える。",
    "caution": "作品は木板に描かれた二面の聖画を持つ携帯具で、平面の一枚絵や油彩キャンバスではない。Metの作品年代は18世紀だが20世紀の再彩色の可能性がある。竜退治は宗教伝承であり史実ではない。公開画像に写るのは開いた状態の二面である。",
    "emotions": [
      "畏敬"
    ],
    "tones": [
      "落ち着き"
    ],
    "themes": [
      "共同体",
      "時間"
    ],
    "text": "小さな木の扉を開くと、左右に異なる聖画が現れます。左には白馬に乗り槍を構える聖ゲオルギウス。右には玉座に座る聖母子が描かれています。小さな画面ながら、鮮やかな青や赤、緑が人物の姿をはっきりと伝えています。\n\nこれはエチオピア正教の信仰に用いられた小さな携帯用聖画です。首から下げて持ち歩く個人用のイコンとして使える造りです。隣の扉には、聖ゲオルギウスが竜を倒す場面が描かれています。聖母子の図像にはヨーロッパから伝わった表現の影響も見られますが、天使たちの姿や衣服はエチオピア独自の絵画の伝統に沿って描き直されています。\n\n所蔵館はこの作品を18世紀のものとしていますが、絵の具や表現を調べた結果、後の20世紀に塗り直された部分がある可能性も指摘しています。すべてが制作当初の状態で残っているとは限りません。持ち運べる大きさと絵の組み合わせを見比べると、身近な祈りの道具としての姿が浮かびます。",
    "checks": [
      [
        "allowed it to be used as a portable personal icon",
        "首から下げて持ち歩く個人用のイコンとして使える造りです。",
        "Exact Met object Overview: wearable portable devotional icon"
      ],
      [
        "St. George slaying the dragon is represented on the adjacent panel",
        "隣の扉には、聖ゲオルギウスが竜を倒す場面が描かれています。",
        "Exact Met object Overview: St George scene on adjacent painted panel"
      ]
    ]
  },
  "845160": {
    "number": 406,
    "japanese": "木陰で煎茶を淹れる",
    "artist": "Aoki Mokubei",
    "culture": "Japan (Edo period)",
    "situation": "江戸後期の文人たちが山中の木陰で煎茶を楽しむ、のびやかな交流の風景を見たい",
    "meaning": "Met作品別Overviewは、京都で陶工・画家として活動した青木木米の1820年代の絵で、文人たちが中国風の煎茶を楽しむ山中の集まりを描くという。若い従者は陶製のかまどで湯を沸かしている。風景は中国を愛好した日本の都市知識人の文化を示す。山に誰が参加したか、個々の正確な身元、実際にあった会合であることは資料上未確認。",
    "visual": "Met公式主画像の原寸と表示JPEGを取得し同一作品を視認。縦長の掛軸画面に険しい山岳と高木が墨と淡彩で描かれ、下半分に小さな人物たち、山石の間に茶を飲む集まりらしい小空間がある。掛軸の上と下の表装は絵の一部ではない。人物の個人名は識別できない。",
    "caution": "青木木米は絵画だけでなく陶工であった事実と、画中の従者の陶製かまどを区別する。茶会を特定の実在の会合や人物と断定しない。煎茶の様式はMetの中国風という説明に従う。",
    "emotions": [
      "安心"
    ],
    "tones": [
      "落ち着き",
      "静けさ"
    ],
    "themes": [
      "休息",
      "共同体",
      "自然"
    ],
    "text": "大きな山や木々の下に、小さな人物たちが集まっています。石のかげにある人の姿を探しながら見ていくと、雄大な景色の中に、ほっと一息つくための場所が見つかります。\n\n1820年代、京都の陶工で画家でもあった青木木米が描いた山水画です。木陰には、文人たちが集まって煎茶を楽しむ場面が描かれています。当時の日本の知識人にとって、中国の文化や文芸を愛好することは暮らしの楽しみのひとつでもありました。\n\n若い従者は、陶製のかまどで湯を沸かしています。高い山や豊かな木々に比べると、茶を用意する人々は小さな存在です。それでも彼らのいる場所を見つけると、風景がただの山の眺めではなく、人と人が時間を分け合う場として立ち上がってきます。",
    "checks": [
      [
        "a group of literati gather to partake of sencha",
        "木陰には、文人たちが集まって煎茶を楽しむ場面が描かれています。",
        "Exact Met object Overview: literati gathered for sencha"
      ],
      [
        "A young servant tends to the ceramic stove",
        "若い従者は、陶製のかまどで湯を沸かしています。",
        "Exact Met object Overview: tea kettle heated by servant"
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
          "Met 39581 web art-page and Overview identify artist as a follower of Soga Shōhaku, contrary to simplified API artistDisplayName; Met 309529 notes possible twentieth-century repainting and its medium is two painted wooden panels, not canvas."]}
    audit_path="docs/artwork-completion-audits/"+ident+"-"+DATE+".json"
    dump(audit_path,audit)
    run(sys.executable,"scripts/verify_official_source_text.py","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","preview","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","save","--audit",audit_path)
    run(sys.executable,"scripts/add_artwork.py","check")
    print("COMPLETED ARTWORK",number,ident,api["title"],flush=True)

def main():
    check(len(load("data/artworks.json")["artworks"])==404,"main must have exactly 404 artworks")
    research=load(EVIDENCE)
    works={x["id"]:x for x in research["works"] if x["id"] in SPEC}
    check(set(works)==set(SPEC),"research IDs mismatch")
    for ident,spec in sorted(SPEC.items(),key=lambda x:x[1]["number"]):
        baseline={"artworks_sha256":sha("data/artworks.json"),"image_registry_sha256":sha("data/image-sources.json")}
        prepare(works[ident],spec,baseline)
    state="""## 現在の状態（2026-11-13時点）

- **完成登録：407作品**。mainに統合後、DBとREADMEが正本になる。
- **次：408作品目から候補調査**。重複・Metの個別Overview原文・JPEG画像・著作権を個別に照合し、収録地域や主題の多様性も維持する。
- 今回405〜407：`met-39581`《滝を眺める中国の文人》（江戸後期、日本、蕭白の追随者）、`met-845160` 青木木米《木陰で煎茶を淹れる》（1820年代、日本）、`met-309529`《聖ゲオルギウスと玉座の聖母子の携帯イコン》（18世紀とされる、エチオピア）。
- 39581のMet API作者表示は曽我蕭白だが個別作品ページと学芸員解説は明確に『蕭白の追随者』とし、後者を優先。309529は二面の木製携帯聖画であり、20世紀の塗り直しの可能性も記録。作品別Overviewを直接読み、各二箇所の英文抜粋を日本語本文の対応主張と照合した。
- 作品そのもののPD、Met公式画像のCC0、現代の美術館本文の権利を分け、原寸・表示JPEGの全SHA256・バイト数・実寸と縮小RMS、公式画像から得たサムネイルの実見を[405〜407画像研究](artwork-research-evidence/met-405-407-2026-11-13.json)に記録。研究したが今回未登録の49079も研究記録に残した。
- 同じAIの別工程による監査であって独立した人間・外部学芸員の査読ではない。既存404作品と画像台帳の過去記録は変更しない。
"""
    temp=ROOT/"tmp-artwork-resume-405.md"
    temp.write_text(state,encoding="utf-8")
    try:run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    finally:temp.unlink(missing_ok=True)
    run(sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py")
    for script in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py","visitor_draft_queue.py","add_artwork.py"):
        if script=="visitor_draft_queue.py":run(sys.executable,"scripts/"+script,"check")
        elif script=="add_artwork.py":run(sys.executable,"scripts/"+script,"check")
        else:run(sys.executable,"scripts/"+script)
    check(len(load("data/artworks.json")["artworks"])==407,"final count mismatch")
    print("ALL PASS: 407 new total, existing 404 preserved",flush=True)
if __name__=="__main__":
    main()
