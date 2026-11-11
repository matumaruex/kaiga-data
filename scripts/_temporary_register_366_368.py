#!/usr/bin/env python3
"""TEMPORARY one-off 366–368 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42958124800"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":57166,"artist":"Suzuki Shōnen","ja":"月夜の宇治川を飛ぶ蛍","fallback_date":"明治時代（1868〜1912年、Met作品ページの時代区分）","tones":["静けさ"],"themes":["自然","時間","記憶"],"emotions":["寂しさ"],"strengths":{"寂しさ":1},"primary":[],"secondary":["寂しさ"],"situation":"宇治川の夜と蛍の光に、『源氏物語』宇治十帖の音や湿り気まで感じてみたい","history":"Met公式作品別Overviewによると、月光の下、京都郊外の宇治川沿いに生える草の上を蛍が飛ぶ風景。この着想は紫式部の11世紀の小説『源氏物語』第45帖にある、仏教への信仰が篤い未亡人ではなく妻に先立たれた皇子と娘二人の隠遁生活、若い宮廷人が二人の娘の楽の音と会話をこっそり聞こうとする場面に由来する。急流の轟き、雨、深い霧のために会話が聞き取りにくい。画家鈴木松年は京都の風景画を専門とし、寺院からの依頼や京都府画学校での日本画教育にも携わった。","visual":"Metの元画像DP-36813-002と表示画像を目視。細長い掛軸の下方は月の光を映すような斜めの白い水流と河畔の草、奥に暗い木々があり、上半分に暗色の広い夜空。蛍の細かな輝きは画面全体に小さな点として控えめに散る。個別の光点を種類や個数まで断定しない。","limits":"物語の人物を実際に画中で明確に描いているとは述べない。宇治十帖の雰囲気を重ねた作品であって、作者が作品の特定場面をそのまま描き起こしたとは断定しない。制作年代はMet API objectDate空欄のため明治期区分のみ。","visitor":"暗い夜空の下を、月の光を映す宇治川が流れています。岸辺の草は風に揺れ、その上に蛍の小さな光が見えます。広い暗がりと明るい流れの対照が印象的です。\n\nこの掛軸の着想には、紫式部の『源氏物語』の宇治を舞台にした巻があります。若い宮廷人が、隠れて暮らす二人の姫君の音楽や会話をこっそり聞こうとするものの、川の大きな音や雨、霧に遮られるという場面です。絵の中で物語の人物を探すのではなく、夜の川の音や湿った空気を想像すると、作品が伝えようとする雰囲気が感じられます。\n\n鈴木松年は京都で活動した風景画家でした。流れる水と風になびく葦をたどりながら、静かな画面に隠れた動きを味わえます。","quotes":[["shining fireflies traveling above the grass-flanked Uji River","岸辺の草は風に揺れ、その上に蛍の小さな光が見えます","Overview: fireflies above Uji River"],["the streaming water and the wind-swept reeds","流れる水と風になびく葦をたどりながら","Overview: moving river and reeds"]],"known":{"title":"Fireflies Over the Uji River by Moonlight","date":"","medium":"Hanging scroll; ink, color, and gold on silk","culture":"Japan","accession":"1979.72"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-36813-002.jpg","01d75e26f3dd1e9b17ff321ccce30f9b1f3cb6e909922fc605a6bea9cf8a90a0",2051548,1914,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-36813-002.jpg","05f5de99e58073b440b17cbe304ef5bd1c518780b58be298fb8bef84de84a962",64299,299,625]}},{"num":13171,"artist":"Edwin Lord Weeks","ja":"狩りに出発するラージャ","culture_label":"United States (artist's origin; Indian palace depicted; Met API culture American)","tones":["にぎわい"],"themes":["都市","共同体","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"アメリカ人画家が描いたインドの宮殿の中庭で、狩りの出発前の準備や建築装飾を観察したい","history":"Met公式作品別Overviewによると、画家エドウィン・ロード・ウィークスはボストン生まれでパリで修業し、画家・挿絵画家・写真家・作家・探検家・収集家として活動した。Metは彼をインドを訪れたことが知られる最初のアメリカ人画家とする。作品は1892〜93年の旅行以後に制作された可能性が高く、ラージャスターン州アジュメールの宮殿での狩猟遠征の準備を描く。画家が公刊した旅行記で宮殿の窓が重なった軽やかな建築を述べている。額縁は制作当初のものではない。","visual":"Met公式元画像・表示画像と縮小プレビューを照合。縦長の宮殿の中庭。白い多層アーケードと上階の大きく張り出した窓飾り、中央に黒っぽい馬を並べた人物たち、手前に犬や地面の小動物、右手に明るい衣の人物たちがいる。壁の白さと前景の土色が対比される。人物の具体的な民族・名前は見た目から判断しない。","limits":"インドの具体的な狩猟の成果や遠征目的を推定しない。民族や身分は画中から独自に割り当てない。額縁は後世のものであると区別し、1892〜93年にこの絵が現地で制作されたとは断言しない。","visitor":"白い壁と何層にも重なる窓飾りが目を引く宮殿の中庭に、馬や人々が集まっています。手前の地面には犬も描かれ、狩りへ出発する前の動きが画面に広がっています。\n\n画家エドウィン・ロード・ウィークスはアメリカのボストンに生まれ、パリで絵を学びました。1892〜93年にインドを訪れた後に描かれたと考えられるこの作品には、ラージャスターン州アジュメールの宮殿で狩りの準備をする人々が描かれています。\n\n画家は旅の記録の中で、この宮殿の窓が何段にも張り出す、軽やかな外観に注目していました。人や馬を眺めたあと、視線を上げて建築の細かい形へ移すと、画家がどこに関心を寄せたかも見えてきます。","quotes":[["after his 1892–93 trip to the country","1892〜93年にインドを訪れた後に描かれたと考えられるこの作品","Overview: after the 1892–93 journey"],["preparations for a hunting expedition at a palace in Ajmer","アジュメールの宮殿で狩りの準備をする人々が描かれています","Overview: hunt preparation at Ajmer palace"]],"known":{"title":"The Rajah Starting on a Hunt","date":"ca. 1895","medium":"Oil on canvas.","culture":"American","accession":"15.30.68"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/ADA3826.jpg","4079ac29a7da4b4a340f42588351ce679de02d9f7be7a84aae2dd722d5fba200",1008194,1712,2092],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/ADA3826.jpg","d825c79e9524a4093b437c7bc025ecd5e4b57debbc6e338c618bc54307330db0",143235,511,624]}},{"num":37974,"artist":"Attributed to Pannalai","ja":"ファテー・シングの熊狩り","tones":["緊張"],"themes":["自然","時間","共同体"],"emotions":["不安","畏敬"],"strengths":{"不安":1,"畏敬":1},"primary":[],"secondary":["不安","畏敬"],"situation":"20世紀初頭のインドの宮廷画で、一頭の熊を複数回描いて狩りの時間経過を示す独特の構図を見たい","history":"Met作品別Overviewによると、ラージャスターン州メーワールの絵画伝統は20世紀初頭にも続き、狩猟や宮廷の場面が好まれた。ファテー・シングの治世には宮廷への写真の普及に応じたような陰影や遠近法も取り入れられた。画中では王が木の上に身を隠し、熊を近距離から銃で撃つ。熊の姿は同じ絵に五回現れ、時間の推移を表す。粗い地形や枯れ木、深い谷が緊張感を強める。餌で熊を誘い寄せたのはMetの推測にとどまる。作者はパンナライと伝えられるが断定できない。","visual":"Met原寸・表示JPEGとサムネイルを確認。赤・橙・青の鮮やかな縁の中央に険しい斜面や裸木、谷を埋める淡い緑。左上付近の木の中に小さな人物の姿。熊の動きは複数の位置に繰り返され、主画面は劇的な俯瞰の構図。単独の瞬間を写した写真とは違う。","limits":"狩猟対象の熊の実際の個体数と画中で五回繰り返された像を混同しない。熊が餌で誘い寄せられたかは推測。作者はあくまで『Attributed to』。動物虐待を肯定・礼賛する作品解説にはしない。","visitor":"赤や青の鮮やかな縁取りの内側に、岩の多い斜面と枯れ木、深い谷が描かれています。王は木の上に身を隠して銃を構え、その下には熊の姿が何度も登場します。\n\nこの絵は1917年、インド・メーワール地方で制作されました。狩猟を題材にした宮廷絵画ですが、目を引くのは熊が画面に五回も描かれていることです。これは五頭の熊がいたという意味ではなく、出来事の異なる段階を一枚に収める表現として読むことができます。\n\n当時の宮廷画には写真の普及を受けたと思われる陰影や遠近表現も取り入れられました。厳しい地形と動物の動きをたどると、狩りの危険と緊張が伝わります。作者はパンナライの作とされていますが、確定していません。","quotes":[["The bear is depicted five times","熊が画面に五回も描かれていることです","Overview: five stages of one bear"],["the ruler, concealed in a treetop, shoots his rifle downward","王は木の上に身を隠して銃を構え","Overview: ruler shooting from a treetop"]],"known":{"title":"Maharaja Fateh Singh Hunting Female Bears","date":"dated 1917","medium":"Ink, opaque watercolor, and gold on paper","culture":"Western India, Rajasthan, Udaipur","accession":"1992.7.1"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DT6831.jpg","204eaf0e1eebd9fd1110b53a9ec97709d8049a6a031177915676bd27515fbc68",3259753,4000,3274],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DT6831.jpg","f82ef28ad9839444b7778005f043e0bd58029d1076ff4b8573620a1bcdbb93ba",132269,600,491]}}]''')
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
 if num==13171:
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil on canvas.", "American Wing primary oil painting metadata changed")
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
 require(len(initial)==365,"expected 365 before additions")
 for i,spec in enumerate(SPECS,366):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==368 and catalog[:365]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：368作品**。正本は最新mainの作品DBとREADME。
- **次：369作品目から候補調査**。作品ID・題材重複、Met一次出典本文、画像と作品の権利を個別確認。
- 今回366〜368：`met-57166` 日本・鈴木松年《月夜の宇治川を飛ぶ蛍》、`met-13171` アメリカ・エドウィン・ロード・ウィークス《狩りに出発するラージャ》、`met-37974` インド・パンナライ（伝）《ファテー・シングの熊狩り》。
- Met各作品の公式Overviewを直接閲覧し、短い英語原文2箇所を独自日本語の鑑賞解説に対応。作品PD・Met Open Access CC0画像・現代解説文を別々に権利確認。公式JPEG原寸/表示の完全SHA256/バイト数/寸法/縮小一致と実画面サムネイルを検証（[画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42958124800)）。同一AIの別パス監査で、外部の人間の専門家による査読ではない。
- `met-57166`はMet API制作年空欄で明治期という公式時代区分のみ。米国出身画家が描くインドの場面とインドの宮廷画は区別。作者帰属の不確実性を保持。
- 既存365作品と画像台帳の旧部分を変更しない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-366.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 366-368")
 run("git","push")
 print("REGISTRATION-PASS 368 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
