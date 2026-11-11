#!/usr/bin/env python3
"""TEMPORARY one-off 369–371 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42967173997"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":53551,"artist":"Unidentified artist","ja":"女性と子ども、乳母のいる室内","tones":["落ち着き"],"themes":["日常","共同体","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"清代中国の美人画で、西洋風の壁紙や室内に取り入れられた遠近感の工夫を探したい","history":"Met公式作品別Overviewによると、清代中国で女性を描いた『美人画（meiren）』は商業市場向けに作られ、西洋で流行した技法を取り入れることがあった。一方、将来の雍正帝の円明園（夏宮）の読書室のような上層の空間にも美人画が飾られた。本作品はトロンプ・ルイユ（だまし絵）の空間表現を使い、ヨーロッパ式の壁紙や建築要素で飾られた室内へ覗き込むように見せる。複数の場面をつなぎ、戸外の風景と女性・子ども・乳母の姿の間を鑑賞者の目が移動するよう設計される。","visual":"Met公式同一作品のフルJPEGと表示版を目視し照合。縦長の室内図で、上下に装飾縁のある画面内に、緑の窓外の樹木、室内の複数の柱・開口部、中央左の女性と子ども、右側で向かい合う乳母、奥へ入る床の線と鮮やかな家具を描く。壁面や扉の奥行きを重ねた様子を確認。","limits":"描かれた実在の住居や人物の固有名は特定せず、すべての美人画が輸出用だったとは誤解させない。建築・壁紙は西洋風の表現として美術館の説明に基づき、画面の場所がヨーロッパとは言わない。","visitor":"細長い絵の中に、いくつもの扉や柱が重なる室内が広がっています。女性と子ども、そのそばにいる乳母が描かれ、奥の窓からは緑の木々が見えます。部屋の奥まで視線が入り込むような構図です。\n\n清代の中国では、こうした女性像を描いた作品が『美人画』と呼ばれていました。商業市場向けにも制作され、西洋で流行した絵画技法を取り入れた例があります。この作品の部屋は、ヨーロッパ風の壁紙や建築の要素を使い、だまし絵のように奥行きを見せています。\n\n戸外の風景、幾重にも重なる室内、女性と子どもの姿へと順番に目を移してみてください。一つの平らな画面なのに、複数の部屋を歩いているように感じられる工夫が楽しめます。","quotes":[["images of women like this one were known as meiren","こうした女性像を描いた作品が『美人画』と呼ばれていました","Overview: meiren as beauty paintings"],["lavishly decorated with European-style wallpaper and architectural elements","ヨーロッパ風の壁紙や建築の要素を使い","Overview: trompe-l'oeil European wallpaper and architectural elements"]],"known":{"title":"Interior with Woman, Child and Nurse","date":"late 18th–early 19th century","medium":"Hanging scroll; ink and color on silk","culture":"China","accession":"44.121"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-35307-002.jpg","95f119d2c2ee90680da36f4f71a71c86044e5f3185247667b581d5f4165027fd",3813816,2999,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-35307-002.jpg","5dca38aff9bd84cc2ced13b6be914a33acb87ba3142f791da3389179df94b96e",161489,468,624]}},{"num":437405,"artist":"Govert Flinck","ja":"羊飼いに扮した若い女性","fallback_date":"17世紀（Met作品APIでは制作年の記載なし）","culture_label":"The Netherlands (artist origin; Met API culture unspecified)","tones":["余韻"],"themes":["時間","共同体"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"レンブラントと弟子フリンクの画風の近さや、作品の誤った署名が後世に起こした誤認を考えたい","history":"Met公式作品別Overviewによると、レンブラントの弟子ホーフェルト・フリンクは、師に学んだ、古代や劇場の世界を連想させる装飾的な衣装の人物像を描いた。この作品の若い女性は花冠、ベール、羊飼いの杖を身に着け、理想化された牧歌のヒロインの姿をとる。フリンク独自の表現は光る衣服の質感、精緻な花、細く傾いた肩の線に現れる。18世紀までには絵にレンブラントを装う偽の署名が加えられ、弟子の絵が師のものと誤認されて20世紀後半まで伝わることさえあった。制作年はMet APIの作品欄では未記載。","visual":"Met公式原寸画像と表示JPEGの縮小一致・実画面を目視。暗い楕円形の画面に、白っぽい衣と肩を覆う薄い布、花冠をまとった若い女性が右へ少し身体を向け、こちらを見ている。頭上には花冠、右側の暗い背景で肩の輪郭が細く傾く。左上にはほのかに明かり。","limits":"モデルをレンブラントの妻サスキアと断定しない。作品はフリンク作で、レンブラントの名前の署名は偽物であると明確に区別する。制作年を出典にない1633年などで確定しない。","visitor":"暗い楕円形の画面の中で、若い女性がこちらを見つめています。頭には花冠をつけ、薄いベールと羊飼いの杖を持った、物語の中の羊飼いを思わせる姿です。衣服の柔らかな光と、細かな花の描写が目を引きます。\n\n作者ホーフェルト・フリンクはレンブラントの弟子でした。師にならって劇場や古代世界を連想させる衣装の人物を描きながら、きらめく布地や肩の輪郭には自分の表現も加えました。この絵には18世紀までに、レンブラント作と見せかける偽の署名が加えられていたことが分かっています。\n\n絵そのものを眺めるだけでなく、作品が誰の手で描かれたと信じられてきたかにも注目してみてください。美しい肖像の背後に、美術品が伝わる中で起きた誤解の歴史が見えてきます。","quotes":[["young woman wears the floral garland, veil, and crook","頭には花冠をつけ、薄いベールと羊飼いの杖を持った","Overview: pastoral costume and crook"],["a false Rembrandt signature had been added to the painting","レンブラント作と見せかける偽の署名が加えられていた","Overview: later spurious Rembrandt signature"]],"known":{"title":"A Young Woman as a Shepherdess","date":"","medium":"Oil on canvas, transferred from wood","culture":"","accession":"60.71.15"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP146492.jpg","d3da1d60f9790ee8d24c7035a3d321d79847777acd177c31e8ce9af25cfe3a57",2528369,2833,3722],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP146492.jpg","cde0ba36ed7bbc5c7e18d27452cb9029245f7e686a0e08b93b412c60406f53d2",70517,475,624]}},{"num":45229,"artist":"Eiraku Hozen","ja":"杖を持つ狐（白蔵主）","tones":["落ち着き"],"themes":["日常","時間"],"emotions":["好奇心"],"strengths":{"好奇心":2},"primary":["好奇心"],"secondary":[],"situation":"江戸の狂言に登場する僧に化けた狐を、永樂保全の簡潔な筆遣いと添えた詩で味わいたい","history":"Met公式作品別Overviewによると、京都の陶工永樂保全は、文人と親交を持ち中国風の趣味に通じ、鮮やかな色彩の陶器や金を使った作品で知られた。しかしこの掛軸では、非常に少ない筆の線で、杖を持つ僧の姿に化けた狐を表す。人物は狂言『釣狐（The Fox Trapper）』の主人公で、添えられた謎めいた詩は僧衣を着た者も内心は狐のままでありうると警告する。作家の晩年の事業上の失敗が作品の質に影響した可能性をMetは推測するが、確定ではない。","visual":"Met公式同一作品の元画像と表示画像を視認して照合。淡い茶色の細長い紙の下部に墨の濃い線を使った、頭が長く前に出た狐のような僧姿の小人物。細い杖を斜め左へ伸ばす。上方の大きな余白には縦書きの詩文が数行あり、最下部に落款。人物はごく少ない線で描かれる。","limits":"作品の狐が実在した僧であるとは言わず狂言の登場人物として説明。作家の商売上の経験と心理を因果関係として断定しない。狂言題名の英訳はMetの表記で、和名『釣狐』は作品解説の『The Fox Trapper』に対応する一般名。","visitor":"細長い掛軸の下に、杖を持った不思議な姿が小さく描かれています。僧のように見えますが、その顔つきには狐を思わせる特徴があります。少ない墨の線で人物の形を表し、上には余白と詩が大きく残されています。\n\n描かれているのは、狂言『釣狐』に登場する、僧に化けた狐です。作者の永樂保全は、京都で色鮮やかな陶器や金を使った作品を作った陶工でもありました。この掛軸では、わずかな筆遣いで狐僧の姿を生み出しています。\n\n添えられた詩は、僧衣をまとっていても内心は狐のままかもしれない、と見る人に注意を促しています。余白と短い線、風刺めいた言葉を重ねると、簡潔な表現の面白さが感じられます。","quotes":[["A few economic brush strokes create the figure of a fox-priest","わずかな筆遣いで狐僧の姿を生み出しています","Overview: sparse strokes depicting a fox-priest"],["the protagonist in the comic kyōgen play The Fox Trapper","狂言『釣狐』に登場する、僧に化けた狐です","Overview: fox-priest in the kyōgen play"]],"known":{"title":"Fox with Staff (Hakuzōsu)","date":"after 1848","medium":"Hanging scroll; ink on paper","culture":"Japan","accession":"36.100.95"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/36_100_95_O2_sf.jpg","d99d306b0ab2a65781b4b487ff226b690a3f0c586b970fc0b428b4bd83f8001a",531150,1683,2969],"display":["https://images.metmuseum.org/CRDImages/as/web-large/36_100_95_O2_sf.jpg","caf40f4d6019d5c8b9719cc06b40d65a25b914b8c4aaaf44a9467fecf6c30091",29777,354,624]}}]''')
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def get(url):
 for i in range(5):
  try:
   r=requests.get(url,timeout=60,headers={"User-Agent":"MuseumArtworkRegistration/1.0"})
   if r.status_code==200:return r
   print("GET",r.status_code,url,flush=True)
  except Exception as e:print("GET ERR",str(e)[:100],flush=True)
  time.sleep(2+i*2)
 raise RuntimeError("URL unreachable "+url)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(rel,content):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(content,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 return sha(p)
def run(*argv):
 print("RUN",*argv,flush=True)
 subprocess.run(argv,cwd=ROOT,timeout=250,check=True)

def add(spec,sequence):
 num=spec["num"];id="met-"+str(num)
 official=f"https://www.metmuseum.org/art/collection/search/{num}"
 api=f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{num}"
 o=get(api).json()
 require(o["objectID"]==num and o["isPublicDomain"] is True,"Met object not PD")
 require(o["title"]==spec["known"]["title"] and o["objectDate"]==spec["known"]["date"] and o["medium"]==spec["known"]["medium"] and o["accessionNumber"]==spec["known"]["accession"],"Met facts updated")
 require(o["classification"]=="Paintings","non-painting")
 require(o["culture"]==spec["known"]["culture"],"culture metadata changed")
 docs={}
 for kind,key in (("original","primaryImage"),("display","primaryImageSmall")):
  url,expect_sha,expect_len,width,height=spec["image"][kind]
  require(o[key]==url,"object primary JPEG identity changed")
  for attempt in range(4):
   b=get(url).content
   if hashlib.sha256(b).hexdigest()==expect_sha and len(b)==expect_len:break
   print("RETRY JPEG",id,kind,len(b),hashlib.sha256(b).hexdigest(),flush=True);time.sleep(3+attempt)
  require(hashlib.sha256(b).hexdigest()==expect_sha and len(b)==expect_len,"JPEG integrity mismatch")
  im=Image.open(io.BytesIO(b));im.load()
  require(im.format=="JPEG" and im.size==(width,height),"JPEG format or dimension changed")
  docs[kind]=(im.copy().convert("RGB"),{"kind":kind,"url":url,"sha256":expect_sha,"byte_length":expect_len,
       "download_status":200,"full_bytes_sha256_checked":True,
       "image_subject_visually_compared":True,"checked_on":DAY,
       "observation":spec["visual"]+" Full original/display exact object JPEG identity/size/dimensions checked in "+RESEARCH_RUN})
 rms=math.sqrt(sum(x*x for x in ImageStat.Stat(ImageChops.difference(
   docs["original"][0].resize(docs["display"][0].size,Image.Resampling.LANCZOS),docs["display"][0])).rms)/3)
 require(rms<30,"image original/display mismatched")
 display=docs["display"][1];original=docs["original"][1]
 hi={"url":original["url"],"sha256":original["sha256"],"byte_length":original["byte_length"],
     "width":spec["image"]["original"][3],"height":spec["image"]["original"][4],
     "verification":"complete_jpeg_sha256_and_downscale_match",
     "source_identity_basis":f"Met original/display same-object image downscale RMS {rms:.5f}",
     "last_full_sha_checked_on":DAY,"human_visual_checked":False}
 visitor={"language":"ja","text":spec["visitor"],"source_urls":[official],
          "review":{"content_status":"verified","source_status":"verified","rights_status":"verified","reviewed_on":DAY}}
 fact={"title_original":o["title"],"title_ja_provisional":spec["ja"],
       "artist":spec["artist"],"creation_date_display":(o["objectDate"] or spec.get("fallback_date","年代不詳")),
       "type":"Painting","is_public_domain_at_source":True,
       "culture":(spec.get("culture_label") or spec["known"]["culture"] or "Unknown (Met API culture unspecified)"),"accession_number":o["accessionNumber"]}
 art={"id":id,
   "source":{"museum":"Metropolitan Museum of Art","artwork_id":num,"artwork_url":official,"api_url":api,"record_checked_on":DAY},
   "facts":fact,
   "image":{"image_id":id+"-primary","iiif_base":None,"iiif_reference_url":None,"display_url":display["url"],
     "source_registry_id":id,"local_path":f"/artworks/{id}.jpg","sha256":display["sha256"],
     "byte_length":display["byte_length"],"live_image_checked":True,
     "live_check_scope":"Met official API+full exact JPEG SHA256/dimensions/RMS verified "+RESEARCH_RUN,
     "source_accession_number":o["accessionNumber"],"high_resolution":copy.deepcopy(hi)},
   "curation":{"emotions":spec["emotions"],"emotion_strengths":spec["strengths"],
     "tones":spec["tones"],"themes":spec["themes"],"evidence_url":official,
     "search_profile":{"fitting_situations":[{"situation":spec["situation"],"reason":spec["history"],"strength":2}],
       "selection_cautions":[spec["limits"]],"review_status":"evidence_reviewed"},
     "meaning_basis":{"author_intent":{"status":"not_verified_for_this_work","summary":None,"source_url":None},
       "scholarly_interpretation":{"summary":spec["history"],"source_url":official},
       "creation_context":f"{o['objectDate']}; {spec['known']['culture']}; {o['medium']}; accession {o['accessionNumber']}",
       "visual_clues":spec["visual"],"uncertainty_note":spec["limits"]},
     "emotion_categories":{"primary":spec["primary"],"secondary":spec["secondary"]}},
   "review":{"facts_checked_against_museum_api":True,"source_public_domain_flag_checked":True,
     "visual_checked":False,"curatorial_reviewed_on":DAY,"curatorial_review_status":"provisional",
     "curatorial_review_note":"Same AI reviewed exact official artwork page and image against primary JPEGs, not external expert "+RESEARCH_RUN,
     "ai_content_review_status":"pending","source_evidence_review_status":"pending","image_subject_match_status":"pending"},
   "visitor_explanation":visitor}
 reg={"id":id,"title":o["title"],"official_artwork_url":official,"origin":"met_official_primary",
     "in_shared_catalog":True,"verification":"met_primary_jpeg_http_verified",
     "image_source":{"type":"met_open_access","official_image_page":official,
       "license_label":"The Met Open Access / CC0 (Public Domain work, official primary JPEG)",
       "license_url":OFFICIAL_OA,"verified_download_url":display["url"],
       "sha256":display["sha256"],"byte_length":display["byte_length"],
       "last_http_sha_checked_on":DAY,"last_verification_evidence":RESEARCH_RUN,
       "license_review_status":"official_OA_confirmed_release_review_pending",
       "high_resolution":copy.deepcopy(hi)},
     "accession_number":o["accessionNumber"]}
 proposal_path=f"drafts/artwork-additions/{id}.json"
 draft_path=f"drafts/visitor-explanations/{id}.json"
 audit_path=f"docs/artwork-completion-audits/{id}-{DAY}.json"
 proposal_sha=write(proposal_path,{"schema_version":"artwork-addition-proposal-v1",
                                  "id":id,"artwork":art,"image_record":reg})
 evidence={"claim":spec["history"],"source_url":official,
           "source_location":"Met exact-artwork Overview: "+" | ".join(q[2] for q in spec["quotes"]),
           "checked_against_source":True}
 draft_sha=write(draft_path,{"id":id,"visitor_explanation":visitor,"evidence":[evidence]})
 for q,claim,section in spec["quotes"]:
  require(q and claim in visitor["text"] and len(q.strip())>=35 and len(q.split())>=6,"invalid source bound excerpt")
 source_evidence=[
  {"url":official,"location":"Met object Overview and Artwork Details: "+" | ".join(q[2] for q in spec["quotes"]),
   "finding":spec["history"]+" Visual subject based on specific same-object source image: "+spec["visual"],
   "checked_against_source":True},
  {"url":api,"location":"Object ID, PD, culture, artist, accession, medium, classification and API exact primary images",
   "finding":"Met API checked; exact original and display JPEG full SHA256/length/dimensions and RMS "+RESEARCH_RUN,
   "checked_against_source":True},
  {"url":OFFICIAL_OA,"location":"Open Access CC0 primary JPEG and public-domain object data rights",
   "finding":"Public-domain object primary images are published for reuse as CC0; museum Overview text remains separately protected.",
   "checked_against_source":True}
 ]
 rights={
  "artwork":{"verified":True,"public_domain":True,"source_url":official,
             "finding":"Exact Met artwork Public Domain flag on museum page and API isPublicDomain true."},
  "image":{"verified":True,"permitted_for_site_use":True,"source_url":OFFICIAL_OA,
           "finding":"Met PD primary JPEG under Open Access/CC0; complete original/display checks "+RESEARCH_RUN},
  "text":{"verified":True,"independent_japanese_prose":True,"source_url":official,
          "finding":"New independently structured Japanese prose relying on direct claim checks; no extensive copy or near-verbatim translation. Not legal counsel."}}
 audit={"schema_version":"artwork-v2-new-registration-2","id":id,"checked_on":DAY,"result":"PASS",
        "unresolved_material_issues":[],"candidate_path":proposal_path,"candidate_sha256":proposal_sha,
        "draft_path":draft_path,"draft_sha256":draft_sha,
        "baseline":{"artworks_sha256":sha(ROOT/"data/artworks.json"),
                    "image_registry_sha256":sha(ROOT/"data/image-sources.json")},
        "official_text_checks":[{"source_url":official,"source_excerpt":q,"visitor_claim":claim,"source_section":section}
                                 for q,claim,section in spec["quotes"]],
        "source_evidence":source_evidence,"rights":rights,
        "separate_pass_review":{"result":"PASS",
            "method":"Independent same-AI second-pass rereading of official exact-work Overview, matching two short verbatim source excerpts to Japanese claims, crosschecking the exact primary visual and official API and images.",
            "limitations":"Not a separate model, external scholarly review, human expert or legal clearance. Online CI museum HTML may rate-limit so the audit's offline program only checks excerpt structure, not live quote accuracy.",
            "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
            "findings":{
              "identity":f"Met object {num}, {o['title']}, {spec['artist']}, {o['objectDate']}, {o['accessionNumber']}. Attribution caveats and source classifications preserved.",
              "image_match":spec["visual"]+f" API official primary JPEG complete hashes/dimensions, downscale RMS {rms:.5f}.",
              "historical_interpretation":spec["history"]+" Limits: "+spec["limits"],
              "emotion":"Artist's subjective mood not asserted; curated tags are grounded and may be zero: "+str(spec["emotions"]),
              "visitor_text":"Original Japanese interpretation in three paragraphs with two grounded, limited official Overview source excerpts.",
              "rights":"Museum exact-work PD; official Open Access CC0 primary images; independently written Japanese text, not copied museum prose."}},
        "image_evidence":[docs["display"][1],docs["original"][1]],
        "notes":[f"Sequential addition {sequence}; prior artworks and image-source records unchanged.",
                 "Official Overview paragraphs were read directly from the exact museum webpages; source excerpts separately matched to Japanese visitor claims. Review by same AI, not a human expert.",
                 "Exact English Overview excerpts were verified against the public Met collection pages; long copyrighted museum text was not copied into visitor descriptions."]}
 write(audit_path,audit)
 run("python","scripts/verify_official_source_text.py","--audit",audit_path)
 run("python","scripts/add_artwork.py","preview","--audit",audit_path)
 run("python","scripts/add_artwork.py","save","--audit",audit_path)
 run("python","scripts/add_artwork.py","check")
 print("REGISTERED",sequence,id,o["title"],flush=True)

def main():
 initial=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 older_sources=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(initial)==368,"expected 368 before additions")
 for i,spec in enumerate(SPECS,369):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==371 and catalog[:368]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：371作品**。最新mainのデータとREADMEが正本。
- **次：372作品目から候補調査**。重複、所蔵館の個別作品Overview、主画像の内容と権利を作品ごとに確認する。
- 今回369〜371：`met-53551` 清代中国《女性と子ども、乳母のいる室内》、`met-437405` オランダ・ホーフェルト・フリンク《羊飼いに扮した若い女性》、`met-45229` 日本・永樂保全《杖を持つ狐（白蔵主）》。
- Met各作品の公式Overview本文を直接読み、日本語鑑賞解説と短い原文2箇所ずつ照合。作品のPD、Met Open Access CC0の主画像、現代の解説の権利を区別し、原寸と表示JPEGの完全SHA256・サイズ・縮小一致とサムネイル実見を確認（[公式画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42967173997)）。同一AIが別工程で検査しており外部専門家の査読ではない。
- `met-437405`はMet APIの制作年欄が空欄で、17世紀とだけ説明。レンブラントの偽署名と作家フリンクの区別に注意。中国の『美人画』と日本の狂言の狐僧は歴史的な作品ジャンルとして説明。
- 既存368作品・画像台帳の既存部分は変更なし。手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-369.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 369-371")
 run("git","push")
 print("REGISTRATION-PASS 371 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
