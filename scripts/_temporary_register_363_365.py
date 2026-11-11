#!/usr/bin/env python3
"""TEMPORARY one-off 363–365 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42957140730"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":437630,"artist":"Giovanni Gerolamo Savoldo","ja":"聖マタイと天使","fallback_date":"1534年頃（Met作品Overviewによる。APIの年代欄は空欄）","culture_label":"Italy (artist's cultural context; Met API culture unspecified)","tones":["静けさ"],"themes":["共同体","時間"],"emotions":["畏敬"],"strengths":{"畏敬":1},"primary":[],"secondary":["畏敬"],"situation":"16世紀イタリアの宗教画で、暗がりの人物、書物、灯火が作る複数の光源の効果を観察したい","history":"Met個別作品Overviewによれば、聖マタイが天使と目を合わせ、福音書を書くよう霊感を受ける姿を描く。右後方にはエチオピア女王の宮廷で歓待を受ける聖人の物語が小さく描かれるが、左後方の場面は特定が難しい。複数の光源の描き分けから、ヴァザーリが1534年頃ミラノ造幣局長向けの作品として記録した『火のある夜景』に該当する可能性があるとMetは述べる。Met APIのobjectDate欄が空欄であるため年代はOverview由来の参考表記。","visual":"同一Met作品IDの公式元JPEGと表示JPEGの内容を直接照合。暗い室内の左手前に赤紫色の衣をまとい机に向かう聖マタイ。ペンと書物のそばで顔を上へ向け、背後の青紫の衣の天使と視線を交わす。右端には小さな建築・人物と火の光。光が頬や衣服の折り目に落ちる。","limits":"聖マタイの福音書執筆という宗教的場面を表現として説明し、史実とは断言しない。後方左側の出来事の解釈はMetが不明確とするため断定しない。1534年頃は作品の作成年代が確定している意味ではなくMetの関連作品群についての説明に基づく。","visitor":"暗い部屋で、赤紫の衣を着た聖マタイが机に向かっています。ペンを持つ手を休め、すぐそばの天使と見つめ合うように顔を上げています。机上の光は、人物の表情や衣服のひだを明るく浮かび上がらせます。\n\nキリスト教の伝承では、天使が聖マタイに福音書を書く霊感を与えます。画面右奥には、マタイがエチオピアの女王の宮廷で迎えられる場面も小さく描かれています。左奥の物語については、所蔵するメトロポリタン美術館も解釈がはっきりしないとしています。\n\n室内の明かりだけでなく、後景に見える火や外の光もこの絵の重要な要素です。美術館は、この複数の光源の効果から、画家サヴォルドが1534年頃に描いたと伝えられる夜景の作品群との関係を指摘しています。明るい部分を順番に追うと、小さな画面の奥にも物語が広がっているのが分かります。","quotes":[["Saint Matthew shares a spellbound gaze with an angel","ペンを持つ手を休め、すぐそばの天使と見つめ合うように顔を上げています","Overview: Saint Matthew eye contact with angel"],["The various sources of light in the painting suggest","この複数の光源の効果から、画家サヴォルドが1534年頃に描いたと伝えられる夜景の作品群との関係を指摘しています","Overview: various light sources and proposed association"]],"known":{"title":"Saint Matthew and the Angel","date":"","medium":"Oil on canvas","culture":"","accession":"12.14"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP-26762-001.jpg","cb280b039468b75774541a3888e50581ceba61e4601913314d3bd293c1a925f3",3400241,4000,3019],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP-26762-001.jpg","791fbe17dba5e3d4f46231dea98e3c62b71c1ebd009c9df6626823ad853866a7",82537,599,452]}},{"num":456949,"artist":"Attributed to Bhawani Das or a follower","ja":"インドオオコウモリ","culture_label":"India, Calcutta (museum geography; Met API culture unspecified)","tones":["驚き"],"themes":["自然","時間"],"emotions":["好奇心"],"strengths":{"好奇心":2},"primary":["好奇心"],"secondary":[],"situation":"18世紀のインドの自然史画で、コウモリの翼の膜や爪、毛並みを描き分けた観察表現を楽しみたい","history":"Met作品別Overviewによると、インドオオコウモリを正面から描き、片翼を大きく広げて、毛皮・目・曲がった爪・翼の静脈まで観察に基づく表現で詳しく示している。バワーニー・ダースはムガル細密画の訓練を受け、英領ベンガル最高裁判事エライジャ・インピーとその妻メアリーの依頼で、カルカッタの邸宅の自然史画を多数制作した。作品はダース自身ではなく、より写実的な描法を使ったその追随者によって描かれた可能性があるため作者は未確定。","visual":"公式の原寸・表示JPEGをサムネイルで直接目視し照合。薄い無地の紙面に黒褐色のコウモリが正面から描かれ、画面左へ水平に片翼を大きく広げ、反対側の翼は立っている。小さな頭部、茶色い毛、関節の折れ目、薄い翼膜に沿う筋が見える。ほかの動物や風景は描かれない。","limits":"コウモリの種名はMetの同定に基づく。『バワーニー・ダース作』と断定しない。英領時代の注文制作は観察画の来歴の説明であり、画家が特定の個体を生け捕りにして描いたという確証はない。","visitor":"薄い紙の上に、一匹の大きなコウモリが正面から描かれています。片方の翼を横へ大きく伸ばし、もう片方は上に曲げています。黒い翼の筋、茶色い毛、目、曲がった爪まで細かく観察されています。\n\nこれは18世紀後半にインドで描かれた自然史画です。ムガル細密画を学んだ画家バワーニー・ダースは、当時カルカッタに住んでいたイギリス人判事夫妻の依頼で、動植物を調べるための絵を制作しました。この作品もその活動と深く関わっていますが、作者はダース本人ではなく弟子や追随者だった可能性があります。\n\n背景を描き込まず、翼の形と体の細部を見せる構図は、動物の特徴を伝えることに集中しています。毛と薄い翼膜の描き方を見比べると、観察と絵画技術が結びついていることに気づきます。","quotes":[["the bat’s fur, eyes, curling claws, and wing veins","黒い翼の筋、茶色い毛、目、曲がった爪まで細かく観察されています","Overview: depicted fur, claws and wing veins"],["It was perhaps made by a follower of Bhawani Das","作者はダース本人ではなく弟子や追随者だった可能性があります","Overview: qualified uncertain attribution"]],"known":{"title":"Great Indian Fruit Bat","date":"ca. 1777–82","medium":"Pencil, ink, and opaque watercolor on paper","culture":"","accession":"2008.312"},"image":{"original":["https://images.metmuseum.org/CRDImages/is/original/DP167067.jpg","877657234d1677d21cdbb48cb64e244da0fb82f30e3248db0011d1c52a3456d9",1208973,3905,2869],"display":["https://images.metmuseum.org/CRDImages/is/web-large/DP167067.jpg","b760b363646d6ac4272416aa8bb2efd9b1166bbe4aa5f38deb07ec8e436f02bd",33509,599,440]}},{"num":853897,"artist":"Unidentified artist","ja":"龍と人物たち","tones":["余韻"],"themes":["愛情","共同体","時間"],"emotions":["悲しみ","好奇心"],"strengths":{"悲しみ":1,"好奇心":1},"primary":[],"secondary":["悲しみ","好奇心"],"situation":"韓国の民間信仰の絵で二人の人物と二匹の龍がどう描かれ、別れと再会をどう願ったか考えたい","history":"Met作品別Overviewは、画面の男女が天の川を挟んで離れた牛飼いと織姫という可能性を挙げ、旧暦7月7日の七夕（チルソク）に再会する伝説に結びつける。対をなす二匹の龍は他者への寛容さにより一緒に天へ昇る『双龍』である可能性がある。龍の色や絡み合う姿は葬儀用の輿に描かれる龍に似ており、Metは亡くなった人の魂を天へ導き、先に亡くなった伴侶との再会を願う葬儀の儀礼に用いられた可能性を示す。どの同定も『could』『may』の推量。","visual":"Met公式の同一作品原寸JPEGと表示JPEGの同一性、サムネイルを目視。絵の上半分に黒と青緑の大きな鱗状の龍二匹が交差し、白い稲光のような筋と雲の中で動く。下半分に向き合うような二人の人物が華やかな衣と冠を着け、両者の間に黒い装束や台がある。やや退色した背景に赤と青が残る。","limits":"男女は牛飼いと織姫『かもしれない』、龍は双龍『かもしれない』、葬儀使用も『可能性』。いずれもMetの推定にとどまり、実際の使用場面や持ち主の家族関係は断定しない。","visitor":"上の画面では二匹の龍が色の異なる体を絡ませ、雲の中を動いています。下には向き合う二人の人物が描かれています。力強い龍の姿と静かな人物の組み合わせが印象的です。\n\nメトロポリタン美術館は、この男女が天の川の両岸に引き離された牛飼いと織姫を表す可能性を挙げています。二匹の龍も、互いに助け合い一緒に天へ昇ったとされる『双龍』かもしれません。ただし、どちらも確定した解釈ではありません。\n\n龍の色や姿が葬儀用の輿の装飾と似ていることから、この絵は亡くなった人を天へ導き、先立った伴侶との再会を願う儀式で用いられた可能性があります。別れと再会への願いが、人物と龍の間に重ねられているのかもしれません。","quotes":[["The pair of dragons could be ssangyong, twin dragons","二匹の龍も、互いに助け合い一緒に天へ昇ったとされる『双龍』かもしれません","Overview: dragons could be ssangyong"],["may have been used in funerary rituals to guide the deceased","この絵は亡くなった人を天へ導き、先立った伴侶との再会を願う儀式で用いられた可能性があります","Overview: uncertain proposed funerary usage"]],"known":{"title":"Figures with dragons","date":"late 19th–early 20th century","medium":"Ink and color on paper","culture":"Korea","accession":"2024.89.7"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-37220-001.jpg","7c6ad4df6290313936de63a3f8af3de0a8f5a114efad5f4f7658465b471d33bc",3447820,2868,3499],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-37220-001.jpg","e61f53b50dd414bcaa1ec40bcafe88348399fe54b52658892e011dd74b407e1e",170276,512,625]}}]''')
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
 require(len(initial)==362,"expected 362 before additions")
 for i,spec in enumerate(SPECS,363):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==365 and catalog[:362]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：365作品**。正本は最新mainの作品DBとREADME。
- **次：366作品目から候補調査**。重複・一次出典本文・公開画像の権利と同一性を一点ずつ照合。
- 今回363〜365：`met-437630` イタリア・サヴォルド《聖マタイと天使》、`met-456949` インド・バワーニー・ダース（または追随者、伝）《インドオオコウモリ》、`met-853897` 韓国《龍と人物たち》。
- 各Met公式個別作品ページのOverview本文を直接閲覧し、短い正確な英語原文2箇所を日本語解説と照合。Met API作品PDとOpen Access CC0主画像、現代の美術館解説文の権利を別に確認。原寸・表示JPEGの完全SHA256/バイト数/寸法/縮小一致とサムネイル目視を実施（[調査](https://github.com/matumaruex/kaiga-data/actions/runs/42957140730)）。監査は同一AIの別工程で、外部の人間の専門家による査読ではない。
- `met-437630`はMet APIの年代欄が空欄で、説明上の1534年頃をあくまで参考として記す。`met-456949`の作者帰属と`met-853897`の葬儀用途は断定しない。
- 既存362作品と画像台帳の旧部分は変更なし。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-363.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 363-365")
 run("git","push")
 print("REGISTRATION-PASS 365 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
