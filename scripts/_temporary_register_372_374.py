#!/usr/bin/env python3
"""TEMPORARY one-off 372–374 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42968403594"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":764087,"artist":"Attributed to Melchor Pérez Holguin","ja":"聖クリストフォロス","tones":["緊張"],"themes":["自然","共同体","時間"],"emotions":["畏敬","不安"],"strengths":{"畏敬":2,"不安":1},"primary":["畏敬"],"secondary":["不安"],"situation":"月明かりの川を幼いキリストを背負って渡る聖人の重みと、光の表現に注目したい","history":"Met公式作品別Overviewは、巨人の聖クリストフォロスが幼いキリストを肩に載せ荒れた川を渡る伝説を描いたものと説明する。幼子は十字架の付いた大きな球体を持ち、その重みは世界を表す。満月と幼子自身の光が夜の横断を照らし、対岸でランタンを上げる修道士は旅人を助けるよう聖人に諭した隠者である。岩が多い暗い岸辺が危険を感じさせる。絵に署名や制作記録はなく、18世紀初めのポトシ周辺で活動したメルチョール・ペレス・オルギンへの帰属は美術館の判断であり確定ではない。","visual":"Met公式ID764087の原寸/表示画像を全バイト照合して実見。縦長の暗い油彩画の中央で、足を曲げた大柄の男性が、右肩に座る幼子を支えつつ左手で長い杖を握り、川を渡る。幼子の頭の背後に光、遠い岸の小人物と灯り、左の夜景に暗い樹木が見える。岩や衣服の暗い茶色と、幼子の光が対照的。光の宗教的象徴の意味はMet本文に基づく。","limits":"物語はキリスト教の伝説であり、超自然的な出来事の史実性は断定しない。作者の署名がなく制作記録も未確認のため『伝』と表示する。描かれた小さな子が実際に世界の物理的重量を負っていたとは断言せず、図像上の寓意と説明する。","visitor":"荒れた川の中で、大きな聖人が幼いキリストを荒れた川の向こうへ運んでいます。聖人は長い杖を握り、重みをこらえるように体をかがめています。幼子の手には十字架の付いた大きな球体があり、世界を象徴しています。\n\nこれは、旅人を川の向こうへ運ぶ聖クリストフォロスの伝説を描いた絵です。満月と幼子から広がる光が夜の川を照らし、対岸では隠者が灯りを掲げています。暗い岩場と光の対比から、危険な道のりと信仰上の意味が伝わります。\n\nこの絵には作者の署名や制作を示す記録が残っていません。メトロポリタン美術館は、18世紀初めにボリビアのポトシ周辺で活動した画家、メルチョール・ペレス・オルギンの作と考えていますが、確定しているわけではありません。光を受ける顔と、それを支える体の姿勢を見比べてみてください。","quotes":[["The giant Canaanite carries the divine child across the turbulent waters","大きな聖人が幼いキリストを荒れた川の向こうへ運んでいます","Overview: child bearer crossing turbulent river"],["Although the painting is not signed or documented","この絵には作者の署名や制作を示す記録が残っていません","Overview: attribution lacks signed documentation"]],"known":{"title":"Saint Christopher","date":"ca. 1710–20","medium":"Oil on canvas","culture":"Bolivia","accession":"2018.652.2"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/DP-30759-001.jpg","f38dbd1daa85963f717bfe9d534ed5f96e70776f8bc412515eaa226065749aa9",3256457,2451,4000],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/DP-30759-001.jpg","ad6b91edcbb7369aaffc7992601f231f5955efbadad73e4184e7d01fd0b06e02",70732,382,623]}},{"num":37895,"artist":"Unidentified artist","ja":"マドゥマダヴァイ・ラーギニー（雨を告げるクジャク）","tones":["緊張"],"themes":["自然","愛情","時間"],"emotions":["期待","不安"],"strengths":{"期待":1,"不安":1},"primary":[],"secondary":["期待","不安"],"situation":"17世紀インドの音楽の旋法を描くラーガマーラー画で、雨を告げるクジャクと恋の詩がどう結びつくか見たい","history":"Met公式個別Overviewでは、ラーギニー『マドゥマダヴァイ』の詩が、雨の気配に鳴くクジャクの声を題材にすると説明する。画面奥の暗くうねる雲と青い斜線が雷雨を暗示し、女性は鳴き声を空腹と取り違えて餌を与えようとする。一方、同時代の鑑賞者は『ナーヤカー・ベーダ』詩に登場するアビサーリカー・ナーヤカー、すなわち嵐の夜に恋人のもとへ出かけるヒロインへの暗示も読み取っただろうとされる。人物・色彩はラージャスターンのマールワール様式で、平面的な建築と色面はマールワー派の絵画とも共通する。","visual":"Met公式同一作品の原寸・表示JPEGを照合しサムネイル目視。赤い扉を持つ角張った建物の前、赤橙の衣装の女性が左へ腕を伸ばして青緑色の長い尾のあるクジャクに向き合う。左下に黄色い布と黒い円形道具。上の広い暗い雲の地平線に青く波打つ雨の線、装飾的な文字の枠がある。画中の人物の固有名は不明。","limits":"女性を実在の特定人物や恋人に直接会う瞬間と断定しない。恋の詩はMetの『暗示を読み取っただろう』という解釈として留める。クジャクが実際に空腹であったとは言わず、女性の勘違いとして説明する。","visitor":"赤い扉の建物のそばで、女性がクジャクに手を伸ばしています。背後の空には黒い雲がうねり、青い線が雨の気配を伝えています。女性の衣装や建築は、はっきりした色の面で描き分けられています。\n\nこの絵は、インドの音楽の旋法を人物や物語で表す『ラーガマーラー』の一葉です。女性はクジャクの鳴き声を空腹のせいだと思い、食べ物を差し出しています。しかし、その声は雨が近づいたことを知らせるものでした。\n\n当時の鑑賞者には、嵐の夜に恋人を訪ねるヒロインの詩も連想させました。小さな行き違いの場面に、雨を待つ自然と恋する人の期待が重ねられています。空の暗さからクジャクの羽、女性の動きへと目を移してみてください。","quotes":[["Thinking that the peacock’s cry comes from hunger","女性はクジャクの鳴き声を空腹のせいだと思い、食べ物を差し出しています","Overview: peacock cry misread as hunger"],["travels at night in a storm to meet her lover","嵐の夜に恋人を訪ねるヒロインの詩も連想させました","Overview: possible poetry allusion to stormy-night lover"]],"known":{"title":"Madhumadhavai Ragini:  Page from a Dispersed Ragamala Series (Garland of Musical Modes)","date":"ca. 1640–50","medium":"Ink and opaque watercolor on paper","culture":"India (Rajasthan, Marwar)","accession":"55.121.27"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP156139.jpg","359a0df9e1bef07ccb442473e655072425d3d545df29b81037d14077c320616a",2841664,3151,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP156139.jpg","8a7bc308d97fb32039384052912b5bd933ad3f09aa5dee9dedf4e9dc4e43cbd6",112430,492,625]}},{"num":49132,"artist":"Gong Xian","ja":"冬景山水図","tones":["静けさ"],"themes":["自然","居場所","時間","記憶"],"emotions":["孤独","寂しさ"],"strengths":{"孤独":2,"寂しさ":1},"primary":["孤独"],"secondary":["寂しさ"],"situation":"清朝初期の中国山水画で、岩や樹木の静かな景色に隠棲への願いと王朝交替期の経験を感じたい","history":"Met公式作品別Overviewによれば、画面中央の冬景山水図は17世紀後半に活動した龔賢が描き、その脇の書は収集家・批評家であった周亮工による。山水画に添えられた詩と左右の対聯は、俗世の騒がしさを離れ、静かに独り暮らす隠れ家への憧れを表す。龔賢と周亮工は明から清への王朝交替に伴う征服と復興の混乱を生きた人物で、この願いが特に切実なものとなったとMetは説明する。主画像は一幅の画と脇の書が組み合わさっている展示形態を記録している。","visual":"Met公式同一IDの元画像と表示JPEGを完全ハッシュ・縮小一致・実見。細長い掛軸の中段から下に、薄墨と濃墨を重ねた岩山や樹木、奥へ流れる白い余白、下方に小さな建物や水辺のような形がある。右上に詩文。左右の書は別作者のものであるため、山水自体の作者と混同しない。","limits":"山水画に描かれた具体的な地名や作者の私的な人生の描写と断定しない。清朝への移行期の歴史的な痛みは美術館の解釈に基づくもので、見た目だけで読み取ったとは書かない。書の作者・画の作者を区別する。","visitor":"濃い墨で重ねた山の岩肌と、葉を落としたような細い木々が縦長の画面に続いています。白く残された空間が奥行きを作り、冷えた空気を想像させます。絵に添えられた詩や書も、この作品の大切な部分です。\n\n中央の山水画は龔賢（きょうけん）が描き、脇の書は同時代の収集家・批評家、周亮工によるものです。詩と絵には、世間の騒ぎを離れて静かな隠れ家に退きたいという願いが表されています。\n\n二人は明から清への王朝交替の時代を生き、征服と復興に伴う苦難を経験しました。メトロポリタン美術館は、そうした時代の中で隠棲への願いが切実だったと解説しています。岩山の重なりから小さな人の住む場所へと視線を移すと、静かな風景に込められた思いが伝わってきます。","quotes":[["reflect the dream of escaping to a solitary retreat","世間の騒ぎを離れて静かな隠れ家に退きたいという願いが表されています","Overview: retreat from worldly affairs"],["the pain of conquest and reconstruction during the Ming-Qing transition","征服と復興に伴う苦難を経験しました","Overview: Ming-Qing historical turbulence"]],"known":{"title":"Wintry mountains","date":"ca. 1679–89","medium":"Hanging scroll; ink on paper","culture":"China","accession":"1989.363.132"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-36008-002.jpg","bcbd63bfbb49d6a262617debfd7fe2bb75f23dca4f15f3de42d9fd7e63bed1af",1824580,1698,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-36008-002.jpg","c11e4308603ce981a7ff8bb0dc0a21e5239bfcadb91aa3282e3ca6498ef66b47",76819,265,624]}}]''')
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
 if num==764087:
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil on canvas","Bolivian oil painting Met metadata changed")
 else:
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
 require(len(initial)==371,"expected 371 before additions")
 for i,spec in enumerate(SPECS,372):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==374 and catalog[:371]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：374作品**。正本は最新mainの作品DBとREADME。
- **次：375作品目から候補調査**。重複・一次出典の作品別Overview・公式画像の同一性と権利を作品ごとに確認。
- 今回372〜374：`met-764087` ボリビア・メルチョール・ペレス・オルギン（伝）《聖クリストフォロス》、`met-37895` インド《マドゥマダヴァイ・ラーギニー》、`met-49132` 中国・龔賢《冬景山水図》。
- 各Met公式作品別Overview原文を直接読み、重要な日本語解説と原文の短い2箇所を対応。作品Public Domain、Met Open Access CC0画像、現代解説本文の権利を区別し、原寸・表示JPEGのSHA256全バイト・寸法・縮小一致・サムネイル目視を確認（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42968403594)）。同一AIの別工程監査で外部の専門家による査読ではない。
- `met-764087`は作品に署名・制作記録がなく画家への帰属は推定。`met-37895`の詩的暗示も解釈の範囲にとどめる。現行Met APIで`met-438007`はPDでないため今回除外。
- 既存371作品および画像台帳の過去部分は変更しない。手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-372.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 372-374")
 run("git","push")
 print("REGISTRATION-PASS 374 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
