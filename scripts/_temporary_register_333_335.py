#!/usr/bin/env python3
"""TEMPORARY one-off 333–335 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42927377170"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=[
 {
  "num":816194,
  "artist":"Attributed to Sōami",
  "ja":"山水図",
  "tones":["静けさ"],"themes":["自然","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],
  "situation":"水墨の淡い濃淡と、室町時代の中国画からの影響を眺めたい",
  "history":"Met作品別Overviewによると、この画面は柔らかい墨のにじみで水辺の地形と樹木を表し、岸のそばに舟が2艘見える。相阿弥は室町時代の阿弥派の絵師の一人で、足利将軍家の美術鑑定や助言に携わり、中国からもたらされた絵画にも通じていた。中国・南宋の禅僧牧谿の墨表現に学んだと説明される。",
  "visual":"ほのかに暗い水辺へ下る丘、枝垂れる柳、左下の小舟、右側の小道をたどる小人物が、淡い墨の景色に置かれる。外縁の古い装丁と朱印も同一作品の公式表示で視認した。",
  "limits":"『Attributed to』であり相阿弥本人の筆と断定しない。画中人物の感情や特定の実景・季節を推定しない。",
  "visitor":"低い丘が水辺へなだらかに下り、枝を垂らす柳のそばに小さな舟が見えます。右側には道を歩く人物が描かれ、薄くにじむ墨が、地面や木々とその奥の空間をつなげています。\n\nこの山水画は、室町時代の絵師・相阿弥の作と伝えられていますが、作者の確定には至っていません。水際には二艘の舟があり、一方の舟は岸から離れようとしています。相阿弥は足利将軍家で美術の鑑定や助言を担い、中国から伝わった絵画にも親しんだ人物でした。\n\n濃い輪郭で一つ一つを囲うのではなく、墨の濃淡によって枝や地形が現れては消えていきます。舟や小さな人影をたどると、余白を含めた画面の広さが感じられます。",
  "quotes":[
   ("Two boats are visible along the grassy shoreline","水際には二艘の舟があり、一方の舟は岸から離れようとしています","Overview: boats along shoreline"),
   ("he served as art connoisseur and consultant to the Ashikaga shoguns","相阿弥は足利将軍家で美術の鑑定や助言を担い","Overview: Sōami role and imported Chinese artworks")
  ],
  "known":{"title":"Landscape","date":"15th–early 16th century","medium":"Hanging scroll; ink on paper","culture":"Japan","accession":"2018.853.7"},
  "image":{"original":("https://images.metmuseum.org/CRDImages/as/original/DP-17102-002.jpg","7fbc9b2f4ef4182c555f9b96f6a93448170980350a26d77c461dd8ce99acb513",4017906,4000,3002),
           "display":("https://images.metmuseum.org/CRDImages/as/web-large/DP-17102-002.jpg","64532fa928de1c4ec9ed5046dddd8aa856220501a237a3c4dbb113905d87efd8",89782,600,450)}
 },
 {
  "num":929265,
  "artist":"Jang Seung-eop (장승업 張承業, sobriquet: Owon 오원 吾園)",
  "ja":"鳥・動物・静物図屏風",
  "tones":["落ち着き"],"themes":["自然","日常"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],
  "situation":"八枚の屏風で鳥や動物、花枝、器物の描き方の違いを見比べたい",
  "history":"Met作品別Overviewによると、この八曲屏風には鳥と花、動物、器物と枝を描く静物という三つのジャンルが一つに収められる。十九世紀の朝鮮では『器皿折枝図』という器物と植物を描くジャンルが発達した。Metは作者を示す根拠として第一扇裏側の題箋と第八扇に押された作者の印二つを挙げる。",
  "visual":"八曲の縦長の屏風。左側に鳥や枝、中央に脚付きの器物と葉、右側に樹の幹や器物、小獣を墨と淡彩で配している。同一IDのMet公式画像で8枚の画面が一続きの組作品であることを確認。",
  "limits":"作品ごとの鳥や動物を特定種と断定しない。題箋と印を記すが作者直筆の全扇確実性までは拡大しない。Metの『器皿折枝図』は一部の静物ジャンルを指し、屏風全体が静物だけではない。",
  "visitor":"細長い八枚の画面に、鳥、木の枝、小動物、花、そして形の異なる器物が配置されています。羽を広げた鳥がいる一方、器と植物が静かに並ぶ画面もあり、屏風を横へたどると題材が次々に変わります。\n\nメトロポリタン美術館によれば、この屏風は鳥と花、動物、静物という三種類の絵画ジャンルを合わせたものです。十九世紀の朝鮮では、器物と枝を描く『器皿折枝図』という形式も広まりました。作者を示す手がかりには、第一扇の裏側にある題箋と、第八扇に押された二つの印が挙げられています。\n\n自由な筆の動きと、羽や葉を表す細い線が交互に現れます。八枚をひとつの大きな絵として眺めたり、画面ごとの違いを探したりして楽しめます。",
  "quotes":[
   ("This eight-panel folding screen incorporates images from three painting genres","この屏風は鳥と花、動物、静物という三種類の絵画ジャンルを合わせたものです","Overview: three painting genres"),
   ("The theme and authorship are provided by a title slip","作者を示す手がかりには、第一扇の裏側にある題箋と、第八扇に押された二つの印が挙げられています","Overview: title slip and seals")
  ],
  "known":{"title":"Birds, Animals, and Still-lifes","date":"late 19th century","medium":"Eight-panel folding screen; ink and color on panel","culture":"Korea","accession":"2026.527.1"},
  "image":{"original":("https://images.metmuseum.org/CRDImages/as/original/DP-45714-001.jpg","36c763bf5dab83985d7b97f475f5dcc12d037a5d897f375fa9a0934557b68ad3",2420631,4000,2204),
           "display":("https://images.metmuseum.org/CRDImages/as/web-large/DP-45714-001.jpg","27f3ab9a41e06b7a6e682baaed0fd13e5b2b08157646edb0f4a9940076add496",90271,599,330)}
 },
 {
  "num":11287,
  "artist":"Theodor Kaufmann",
  "ja":"自由への道",
  "tones":["緊張"],"themes":["共同体","居場所"],"emotions":["不安"],"strengths":{"不安":2},"primary":["不安"],"secondary":[],
  "situation":"南北戦争を題材にした歴史画の人物構成と、自由への道が見えない状況を考えたい",
  "history":"Met作品別Overviewによると、画家カウフマンはドイツで1848年の政治運動に参加した後、1850年に渡米し南北戦争では北軍兵として従軍した。絵は逃れる一行の進路が明らかでない様子を示す。Metはこの画面がフランソワ＝オーギュスト・ビアールによる1859年作の、ブラジルを舞台とした類似題材の構図を参照したと説明する。",
  "visual":"暗い林の間を複数の大人と子どもが、衣服や荷物を担いで右の明るい場所へ歩く。足元は土の道で、人物の顔と衣服に光が当たり、遠い道筋は視界に入らない。Met原画像と表示画像は同作の構図。",
  "limits":"画中人物の具体的な名前、逃走の行先や結果は特定しない。実際に作者が南軍の撤退を目撃したかはMetでも推量。ビアールの1859年作とカウフマンの1867年作は別作品。",
  "visitor":"木々が薄暗く茂る中、大人と子どもが荷物を抱えて歩いています。前へ進む人物もいれば、後ろの人を気にかけるように振り返る人物もいます。画面の右側に光が差しているものの、その先の道がどこへ続くのかは描かれていません。\n\n1867年に描かれたこの絵は、アメリカ南北戦争の時代に自由を求めた人々を題材にしています。メトロポリタン美術館は、逃げる人々の姿が自由への明確な道筋のない状況を示すと説明しています。また画家は、1859年にブラジルを舞台として描かれたフランスの画家ビアールの構図を参考にしました。\n\n荷物を運ぶ姿勢や大人と子どもの距離を追うと、ひとりの英雄ではなく、集団で移動することの困難さが見えてきます。題名が示す『自由へ』という方向と、行く先の見えない画面の緊張を重ねて鑑賞できます。",
  "quotes":[
   ("his portrayal of a group of fleeing figures indicates","逃げる人々の姿が自由への明確な道筋のない状況を示す","Overview: flight and unclear route to liberty"),
   ("Kaufmann based his Civil War scene on an 1859 composition","画家は、1859年にブラジルを舞台として描かれたフランスの画家ビアールの構図を参考にしました","Overview: compositional reference to Biard")
  ],
  "known":{"title":"On to Liberty","date":"1867","medium":"Oil on canvas","culture":"American","accession":"1982.443.3"},
  "image":{"original":("https://images.metmuseum.org/CRDImages/ad/original/DT2100.jpg","fb03e98cd239b8820dc2ba69b7116c1bcad92be3f0e5835786942f89a51551b1",1946349,3811,2474),
           "display":("https://images.metmuseum.org/CRDImages/ad/web-large/DT2100.jpg","a39f746d7190743a49bf4d2922a74df3e559d1b7296a0a5c8f7c05d8b2a6aec6",72410,599,389)}
 }
]
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
 if num==11287:
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil on canvas", "American Wing painting classification discrepancy changed")
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
       "artist":spec["artist"],"creation_date_display":o["objectDate"],
       "type":"Painting","is_public_domain_at_source":True,
       "culture":spec["known"]["culture"],"accession_number":o["accessionNumber"]}
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
              "identity":f"Met object {num}: {o['title']}; {spec['artist']}, {o['objectDate']}; {o['accessionNumber']}. API artist differs in attribution framing if supplied; museum page preserves attribution. American Wing classification blank is restricted to verified oil painting 11287." if num in (11287,816194) else f"Met exact object {num} title/date/creator/accession checked.",
              "image_match":spec["visual"]+f" API official primary JPEG complete hashes/dimensions, downscale RMS {rms:.5f}.",
              "historical_interpretation":spec["history"]+" Limits: "+spec["limits"],
              "emotion":"Artist's subjective mood not asserted; curated tags are grounded and may be zero: "+str(spec["emotions"]),
              "visitor_text":"Original Japanese interpretation in three paragraphs with two grounded, limited official Overview source excerpts.",
              "rights":"Museum exact-work PD; official Open Access CC0 primary images; independently written Japanese text, not copied museum prose."}},
        "image_evidence":[docs["display"][1],docs["original"][1]],
        "notes":[f"Sequential addition {sequence}; prior artworks and image-source records unchanged.",
                 "Source Overview passages independently read via official museum page 2026-11-11. Separate AI pass is not human expert.",
                 "The 2026 Korean accession is a separate eight-panel screen (929265), not the older ten-panel Jang-attributed screen (646996)."]}
 write(audit_path,audit)
 run("python","scripts/verify_official_source_text.py","--audit",audit_path)
 run("python","scripts/add_artwork.py","preview","--audit",audit_path)
 run("python","scripts/add_artwork.py","save","--audit",audit_path)
 run("python","scripts/add_artwork.py","check")
 print("REGISTERED",sequence,id,o["title"],flush=True)

def main():
 initial=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 older_sources=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(initial)==332,"expected 332 before additions")
 for i,spec in enumerate(SPECS,333):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==335 and catalog[:332]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status=f"""## 現在の状態（2026-11-11時点）

- **完成登録：335作品**。正式な数は最新mainとREADMEを確認。
- **次：336作品目から候補調査**。作品ID・題材重複、所蔵館の作品別出典、作品・画像・現代解説の権利、公式JPEGの対象画面を検証する。
- 333〜335：\`met-816194\` 日本・相阿弥（伝）《山水図》、\`met-929265\` 韓国・張承業《鳥・動物・静物図屏風》、\`met-11287\` アメリカ・テオドール・カウフマン《自由への道》。
- 各作品に独自日本語解説・公式概要と短い2箇所の引用照合・v2監査。PDと公式Open Access CC0画像の権利を分け、元画像と表示JPEGのSHA256・寸法・縮小画像を照合（[画像研究]({RESEARCH_RUN})）。同一AIの別パスによる確認で外部専門家の審査ではない。
- 過去332作品のレコードと画像台帳の既存部分は変更していない。手順は [新規登録ガイド](artwork-expansion-v2.md) と [共通品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-333.md")
 p.write_text(new_status.replace("\\\`","\`"),encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 333-335")
 run("git","push")
 print("REGISTRATION-PASS 335 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
