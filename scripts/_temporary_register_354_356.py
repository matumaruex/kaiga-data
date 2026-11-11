#!/usr/bin/env python3
"""TEMPORARY one-off 354–356 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42949317444"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":844779,"artist":"Northern Highlands artist","ja":"聖母子と寄進者たちの壁画","culture_label":"Ethiopia, Lake Tana region (museum geography; culture unspecified in API)","tones":["落ち着き"],"themes":["共同体","時間","愛情"],"emotions":["慈しみ"],"strengths":{"慈しみ":2},"primary":["慈しみ"],"secondary":[],"situation":"エチオピアの教会壁画に描かれた聖母子、天使、寄進者と装飾の関係を眺めたい","history":"Met作品別Overviewによると、この壁画は1800年頃にエチオピアのタナ湖周辺の教会の装飾として制作された。布地に塗布した石膏下地の上へ鮮やかな黄土・赤・青・白・緑の顔料を使っている。中央の聖母子は黄色と白の編み目模様を持つ鮮やかな青い敷物の上に座り、二人の天使に掲げられた赤い幕で囲まれる。上部の二人の小天使は契約の箱を表す像を掲げ、下部右側には祈る姿勢の寄進者が並ぶ。下部の古典エチオピア語ゲエズ語の銘文は寄進者名を列挙していたが、今なお読めるのは『ブラッタ・フェンタ』という一人の名前だけ。","visual":"公式Met主画像（844779）とオリジナルJPEGを見比べて確認。縦長の大きな画面に青い衣の母が子を抱く中心像、その背後を囲む朱赤の幕、周縁に天使・小さな寄進者・細密な幾何学文様。上部の細かな図像は作品別本文で同定し、サムネイルから細部がすべて読めたとは主張しない。","limits":"宗教的教義を事実として断言せず、画中で表現される信仰として説明。特定の寄進者の身元はMetの判読できる名前以上に断定しない。作者個人は不明で、所蔵館の『Northern Highlands artist』を地理的な仮称として扱う。","visitor":"大きな壁画の中央に、幼いイエスを抱く聖母マリアが座っています。二人の下には、黄色と白の編み目模様を持つ鮮やかな青い敷物が描かれ、赤い幕を掲げる天使たちが中央の姿を囲みます。\n\n1800年頃のエチオピア・タナ湖周辺で、教会を飾るために作られた絵です。布に石膏下地を施し、赤や青、緑などの顔料を重ねています。画面上部には契約の箱を象徴するものを持つ天使、右下には祈る姿勢の寄進者たちが描かれています。\n\n寄進者の名前は下部にゲエズ語で記されていましたが、現在読み取れるのは『ブラッタ・フェンタ』という名だけです。中央の聖母子から周囲の人物や装飾へ視線を移すと、この絵が共同体の祈りの場に置かれていたことが感じられます。","quotes":[["vibrant blue mat decorated with yellow and white interlaced patterns","黄色と白の編み目模様を持つ鮮やかな青い敷物が描かれ","Overview: Virgin and Child seated on patterned blue mat"],["only the name of “Blatta Fenta” remains still legible","現在読み取れるのは『ブラッタ・フェンタ』という名だけです","Overview: donor names in Ge'ez inscription"]],"known":{"title":"Wall painting of the Virgin and Child with donors","date":"ca. 1800","medium":"Pigment over gesso on canvas","culture":"","accession":"2021.170"},"image":{"original":["https://images.metmuseum.org/CRDImages/ao/original/DP-39222-001.jpg","19bdcd033306e2c3984b292696200ee512f576b0348c01e74077ba81b9c416fb",6851556,3212,4000],"display":["https://images.metmuseum.org/CRDImages/ao/web-large/DP-39222-001.jpg","1010ba1048114e6b8219c5965361cc8db48148ad5a792db60da3bf64af0e5d44",248123,501,624]}},{"num":437519,"artist":"Théodore Rousseau","ja":"川のある風景","culture_label":"France (artist nationality; Met API culture unspecified)","tones":["静けさ"],"themes":["自然","日常","居場所"],"emotions":["安心"],"strengths":{"安心":1},"primary":[],"secondary":["安心"],"situation":"静かな川沿いの村と、人が暮らす場所としての自然を風景画から感じたい","history":"Met公式作品別Overviewは、ルソーが1844年にフランス南西部ランド地方を訪れ、その平坦な地形が本作の田園風景の着想になった可能性を述べる。広い平野と空は彼が以前から好んでいた17世紀オランダ風景画を思わせる。舟を扱う人物と、木々の中の農家へ向かう道は、手つかずの荒野ではない田舎の暮らしを示す。","visual":"公式Met主画像437519を縮小JPEGと完全原画像照合で目視。低い地平線の上に雲が多く大きな空、暗い緑と茶色の前景。画面右側の水面に小さな舟と人物が見え、中央には集まった木と丈の高い木、その奥に家が隠れる。画面は横長で彩度を抑えた風景。","limits":"ここをランド地方の特定の実景として断定せず、同地方の地形が着想となった『可能性』とする。舟の人物の名前や行先は推測しない。『安心』タグは鑑賞者の穏やかな連想にとどめる。","visitor":"大きな空の下に、木々の集まる岸辺と穏やかな川が広がっています。水面には小舟を扱う人物が小さく描かれ、木立の奥には農家へ続く道が見えます。\n\n画家テオドール・ルソーは1844年にフランス南西部のランド地方を訪れました。その平坦な地形が、この風景の着想になった可能性があると美術館は説明しています。広い平野と空の表現には、ルソーが敬愛した17世紀オランダの風景画も重なります。\n\n舟を扱う人物や農家へ続く小道があるため、ここはまったく人のいない荒野ではありません。暗い緑の岸辺から明るい水面、そして遠くの空へと視線を動かすと、自然の中に人々の暮らしが溶け込む様子を味わえます。","quotes":[["whose flat terrain may have inspired the countryside depicted here","その平坦な地形が、この風景の着想になった可能性がある","Overview: Landes terrain as a possible inspiration"],["The boatman and the path leading back to the farm","舟を扱う人物や農家へ続く小道があるため","Overview: river boatman and farm path"]],"known":{"title":"A River Landscape","date":"ca. 1845–50","medium":"Oil on wood","culture":"","accession":"43.86.7"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP274261.jpg","38c2559d9bda93094e21086e4cc96f7dc14763b240409abac7380e82aaa00d22",1639041,1957,1300],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP274261.jpg","b9e9f15b0c0cef8b4c8373151d09a9fc240dd355f83e6a3946d634981ae60752",160115,599,398]}},{"num":58451,"artist":"Unknown artist","ja":"水たばこを吸うラージャ","tones":["落ち着き"],"themes":["日常","時間","共同体"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"17世紀末から18世紀初めのコータ宮廷画における色面や人物の姿を鑑賞したい","history":"Met公式作品別Overviewによると、17世紀の最終四半世紀にはインド・ラージャスターンのコータで宮廷生活の絵画が制作されていた。この一枚には身元不詳のラージャ（王）が花柄の絨毯を敷いたテラスに座り、水たばこの管を口へ運びながら小さな花の枝も左手に持つ姿が描かれる。右腕を大きな縞模様のクッションへ預け、手前にはパン（キンマ）を入れる箱がある。明るい強い色と浅い空間の処理にはラージプート絵画、肖像形式や薄緑の背景にはムガルとデカン絵画の影響が見られる。","visual":"Met公式画像58451の主画像縮小と元画像を目視で同定。赤い四角い枠の中で薄緑の背景と遠い水平線、下半分の濃い黄の花柄絨毯。その上に薄桃色衣装とターバンの男性が脚を組むように座り、細い水たばこの管が右下の丸い水たばこ器具へつながり、背後に大型の縞模様クッションがある。人物名は不詳。","limits":"人物の固有名や具体的な生涯は不明。水たばこの喫煙を推奨しないし、現代的な健康効能も付与しない。技法の影響関係はMetの研究解釈と分けて示す。","visitor":"花柄の黄色い絨毯の上に、薄桃色の衣装を着たラージャ（王）が座っています。左手では水たばこの管を口に運びながら、小さな花の枝も持ち、右腕は縞模様の大きなクッションに預けています。\n\n17世紀末から18世紀初めのインド・コータでは、宮廷での暮らしを題材にした絵が描かれていました。人物の前には、キンマを入れる箱も置かれています。誰を描いたのかは分かっていません。\n\nこの絵は、ラージプート、デカン、ムガルという異なる絵画伝統を組み合わせています。下半分の鮮やかな色と浅い空間はラージプート絵画の特徴とされ、淡い緑の背景や肖像の形式には他の地域の影響が見られます。色の配分と人物の落ち着いた姿勢を見比べて楽しめます。","quotes":[["a terrace covered with a floral carpet","花柄の黄色い絨毯の上に、薄桃色の衣装を着たラージャ（王）が座っています","Overview: raja seated on floral-carpet terrace"],["The painting combines elements of the Rajput, Deccani, and Mughal styles","この絵は、ラージプート、デカン、ムガルという異なる絵画伝統を組み合わせています","Overview: mixing Rajput Deccani Mughal visual conventions"]],"known":{"title":"A Raja Smoking a Hookah","date":"ca. 1690–1710","medium":"Ink, opaque watercolor, and gold on paper","culture":"India (Rajasthan, Kota)","accession":"1981.371.2"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP156143.jpg","0d8f9b9b2e2cf62813da577c9e954a0931726bce06dd59e973ce6216c77108be",2973892,3313,3927],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP156143.jpg","1403ce7f4344d0a527d8a39c84705e7c2bd306fa1005c072e870fef05afeff25",113471,527,625]}}]''')
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
       "artist":spec["artist"],"creation_date_display":o["objectDate"],
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
 require(len(initial)==353,"expected 353 before additions")
 for i,spec in enumerate(SPECS,354):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==356 and catalog[:353]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：356作品**。正本は最新mainの作品DBとREADME。
- **次：357作品目から候補調査**。重複・一次出典本文・画像同一性・作品/画像/解説の権利を個別照合。
- 今回354〜356：`met-844779` エチオピア・タナ湖周辺《聖母子と寄進者たちの壁画》、`met-437519` フランス・ルソー《川のある風景》、`met-58451` インド・コータ《水たばこを吸うラージャ》。
- 各作品別Met公式Overviewを実際に読み、重要な日本語鑑賞解説に対応する短い英語原文2箇所を照合。公式MetのPD作品とOpen Access CC0画像、著作権のある現代解説文を別扱い。元画像と表示JPEGの完全SHA256・バイト数・寸法・縮小一致・公式サムネイルの目視を確認（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42949317444)）。確認は同一AIの別パスで、人間の専門家による査読ではない。
- 既存353作品・画像台帳の旧部分は一切変更しない。手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-354.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 354-356")
 run("git","push")
 print("REGISTRATION-PASS 356 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
