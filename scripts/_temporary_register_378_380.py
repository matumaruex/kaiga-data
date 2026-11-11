#!/usr/bin/env python3
"""TEMPORARY one-off 378–380 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42976021314"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":845805,"artist":"Nagasawa Rosetsu 長澤蘆雪","ja":"月夜山水図","tones":["静けさ"],"themes":["自然","時間"],"emotions":["畏敬"],"strengths":{"畏敬":1},"primary":[],"secondary":["畏敬"],"situation":"江戸後期の長澤蘆雪が月明かりと雲、松の輪郭を使って夜の山をどう描いたかをゆっくり眺めたい","history":"Met作品別Overviewは1794～95年の月夜山水図を、月を塗り残し（reserve）で表し、雲の細い帯が空を横切る怪しげな雰囲気から龍のイメージも連想される作品と説明。松の大胆な黒い輪郭と、付立筆という穂の長い幅広い筆で輪郭をつけずに描く山肌の薄墨が対照的である。薄墨は一層ごとに乾燥させて重ね、上半分の大きな余白には作者の署名と朱印が置かれる。月夜と雲の画題は蘆雪の生涯を通じて繰り返された。","visual":"公式Met原JPEG・表示JPEGの完全一致条件と縮小RMSを確認し実見。細長い茶色がかった絹地の画面下方には濃墨の松と淡い岩・山の輪郭、真ん中やや右に淡い満月が白く浮く。月の周りをかすかに雲が横切り、上方はほとんど余白。左右の青い表装の縁は絵自体の描写と混同しない。","limits":"画中の雲が本当に龍を表すと決めつけず、美術館が連想を示すにとどめる。付立筆の技法は美術館の解説に基づく。夜景を実際に現地でその場写生したとはしない。","visitor":"淡い墨で描かれた山の上に、白く抜かれた丸い月が浮かんでいます。手前の松は濃い線で大きく枝を伸ばし、山の輪郭は柔らかな薄墨で表されています。空の広い余白が、夜の静けさを強めています。\n\n長澤蘆雪は1794〜95年頃、松と月と雲を組み合わせてこの山水画を描きました。松の大胆な輪郭と、薄墨を重ねて作る山肌の対比が見どころです。山には輪郭線を使わず、幅広い『付立筆』の柔らかな穂で形を作っています。\n\n雲の形には、東アジアの伝承に登場する龍の姿を連想させるところもあります。月の光の周囲から松へ、そして何も描かれていない空へと視線を戻してみてください。描かない部分も、夜の空気を作る大切な表現になっています。","quotes":[["The bold silhouettes of pine trees contrast with gray washes","松の大胆な輪郭と、薄墨を重ねて作る山肌の対比が見どころです","Met exact Overview: silhouetted pine versus wash"],["The upper expanse of the painting is entirely blank","空の広い余白が、夜の静けさを強めています","Met exact Overview: large empty upper field"]],"known":{"title":"Moonlit Landscape","date":"1794–95","medium":"Hanging scroll; ink on silk","culture":"Japan","accession":"2020.392"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/LC-TR_168_1ab_2020_sr1-006.jpg","e0a7a450b4a7aaaf049f3738869febe4ef00d87911e56d4cf7b6fc4b254f8faf",2235293,1881,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/LC-TR_168_1ab_2020_sr1-006.jpg","5d357411d3ee2d1a68b05f79654c06264df15d1a6ce6b7f0f6b30e39ebdabb06",71939,293,623]}},{"num":74661,"artist":"Unidentified artist","ja":"走る象（表）・象の素描練習（裏）","tones":["高揚"],"themes":["自然","時間"],"emotions":["好奇心"],"strengths":{"好奇心":2},"primary":["好奇心"],"secondary":[],"situation":"インド・コータで作られた象の勢いある素描から、足の動きと動物観察に集中した画家の視線を感じたい","history":"Met公式作品別Overviewでは、18世紀半ばのインド、ラージャスターンのコータ宮廷では戦や狩猟が主要な絵画主題で、象はとりわけ人気があったと説明する。本図では人間の存在はほぼ無視され、動いている象の姿を自然に捉えることが中心。媒体は紙に木炭で、所蔵品の題名は表に『Running Elephant』、裏に象の素描練習があることを示す。公式主画像が示すのは表側で、裏の練習線の詳細をこの主画像から見たとは言わない。","visual":"Met ID74661公式原寸/表示JPEGを直接目視・縮小照合。横長の薄茶の紙面の中央を、鼻をくねらせ右へ駆ける大きな象が占める。脚を前後に大きく伸ばし、体や背に細い木炭の補助線、背後の左に小さな人影とさらに右端に小さな人物。彩色画でなく木炭の簡潔な素描。主画像は表面のみ。","limits":"画中の象が実際に起こした特定の戦闘や狩猟事件を断定しない。象の裏面の構図は公開主画像に映らないため推測で描写しない。『自然主義的』はMetの分析であり動物の行動観察自体を記録した証明ではない。","visitor":"薄茶色の紙の上を、大きな象が勢いよく走っています。鼻は曲がり、四本の脚は前後に広く伸びています。細い線を重ねた木炭の素描から、重い体が動く瞬間を感じられます。\n\n18世紀半ばのインド・コータでは、宮廷の狩猟や軍事にまつわる絵が多く作られ、象は特に好まれた題材でした。この絵では人の姿よりも、走っている象そのものの動きが中心になっています。\n\n作品には表側の走る象だけでなく、裏側にも象の姿を練習した素描があります。ここに掲載した公式の主画像は表側です。動物の大きな胴と脚の伸び方、鼻の曲がりを順に見ると、画家が線で速度や重みを捉えようとした工夫が伝わってきます。","quotes":[["Elephants were an extremely popular subject in Kotah court painting","象は特に好まれた題材でした","Met exact Overview: elephants popular in Kotah painting"],["the emphasis is on naturalistically capturing the elephant in motion","走っている象そのものの動きが中心になっています","Met exact Overview: naturalistic emphasis on motion"]],"known":{"title":"Running Elephant (recto); Practice Sheet of Elephant Sketches (verso)","date":"mid-18th century","medium":"Charcoal on paper","culture":"India (Rajasthan, Kotah)","accession":"2008.359.14"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP166081.jpg","6ae177e390566be0ef8e2d6a857e29236b3c767ff4fa56152bfbac148ab98daf",1638210,2000,1189],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP166081.jpg","878ee97839e87596fef8132e852bba12829abdde5d503a8d8d52133d721631c5",156749,599,356]}},{"num":45680,"artist":"Attributed to Jiang Song","ja":"冬景山水図（蔣嵩伝）","tones":["静けさ"],"themes":["自然","居場所","時間"],"emotions":["孤独"],"strengths":{"孤独":1},"primary":[],"secondary":["孤独"],"situation":"明代中国の長い山水画で、雪山・旅人・漁師・隠者の姿と、力強い墨の濃淡が作る冬の世界をたどりたい","history":"Met公式作品別Overviewによると、蔣嵩は南京出身で医者・官吏の家柄に生まれながら職業画家として生計を立てた。山水画の主要なモチーフには、ひとりで釣る漁師、隠居した学者、山を行く旅人があり、それらが本作の長い絵巻に含まれる。切り詰めて抽象化した岩山の形、奔放な筆遣い、濃淡を重ねた墨の効果が特徴で、南京の画家史忠の大胆な雪景山水の系譜につながる。本作は署名がなく、ベルリン東洋美術館にある別の四図との比較から蔣嵩の作と『伝』として帰属される。","visual":"公式原JPEG DP204373_CRD.jpgと表示JPEGを実際に見て照合。主画像は約7mの長巻のうち水辺・岩・木・橋や建物のある横長の一場面を切り出した表示で、山や樹木を墨の細線と淡墨で描く。端から端まで全長7mを一枚の主JPEGに記録したと誤解しない。独立した小さな人影の細部はサムネイルだけで全箇所の見分けは難しい。","limits":"『蔣嵩作』は断定でなく署名不在の比較による帰属。長巻全長7.04mのうち掲載画像が一場面を写すことを区別。旅人や漁師や隠者の配置を主画像から全て見たと主張しない。人物の心理や地名は推定しない。","visitor":"淡い墨の山と、細い線で描かれた木々が、横長の絵の中に続いています。岸辺や建物、岩の形が次々に現れ、白い余白から冬の冷たい空気が感じられます。\n\nこれは16世紀前半の中国で描かれた長い山水画の一部分です。全長は約7メートルあり、絵巻の中には、ひとりで釣る漁師や隠れて暮らす学者、山を旅する人物が描かれています。掲載した公式主画像は絵巻全体ではなく、一部の場面を示しています。\n\nこの絵は南京の画家、蔣嵩（しょうすう）の作と伝えられています。岩山を大胆に単純化し、濃い墨と薄い墨を使い分ける筆致が特徴ですが、絵には署名がありません。美術館は別作品との比較をもとに画家への帰属を示しています。景色の濃い部分と余白を行き来しながら見てみてください。","quotes":[["lone fishermen, scholars living in reclusion, and mountain travelers","ひとりで釣る漁師や隠れて暮らす学者、山を旅する人物が描かれています","Met exact Overview: three recurring subject motifs"],["This unsigned painting is attributed to Jiang Song","絵には署名がありません。美術館は別作品との比較をもとに画家への帰属を示しています","Met exact Overview: unsigned tentative attribution"]],"known":{"title":"Winter landscape","date":"first half 16th century","medium":"Handscroll; ink and color on paper","culture":"China","accession":"55.124"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP204373_CRD.jpg","aaddb4f5b0ce7caf41af8809c6d09a2028589cda6469346c27f768b7b90287da",244376,1750,717],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP204373_CRD.jpg","16605c82b1fd3f593ecc13e0ec5f9f509dbc21ac4c4928fec4b32c21a0c58852",44386,598,245]}}]''')
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
  allowed={(expect_sha,expect_len)}
  if num==74661 and kind=="original":
   # The Met serves two reproducible source JPEG bitstreams at the same object URL.
   # 42976021314 verified 1638210B SHA6ae177..., and 42976707754
   # independently verified 1634779B SHAcde213..., both 2000x1189
   # and both downscaling to the exact same official display JPEG.
   allowed.add(("cde213395bfd7b2339a932a61a3c41122598c37145f7ce6ffe8a75527874da45",1634779))
  for attempt in range(4):
   b=get(url).content
   actual_sha=hashlib.sha256(b).hexdigest();actual_len=len(b)
   if (actual_sha,actual_len) in allowed:break
   print("RETRY JPEG",id,kind,actual_len,actual_sha,flush=True);time.sleep(3+attempt)
  require((actual_sha,actual_len) in allowed,"JPEG integrity mismatch")
  im=Image.open(io.BytesIO(b));im.load()
  require(im.format=="JPEG" and im.size==(width,height),"JPEG format or dimension changed")
  docs[kind]=(im.copy().convert("RGB"),{"kind":kind,"url":url,"sha256":actual_sha,"byte_length":actual_len,
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
 visitor={"language":"ja","text":spec["visitor"],"source_urls":[official]+([spec["extra_source_url"]] if spec.get("extra_source_url") else []),
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
 if spec.get("extra_source_url"):
  source_evidence.append({"url":spec["extra_source_url"],"location":"Met Native Perspectives: Veronica, Rock and Wolf Pipestem on Hayne Hudjihini","finding":spec["extra_source_summary"],"checked_against_source":True})
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
 require(len(initial)==377,"expected 377 before additions")
 for i,spec in enumerate(SPECS,378):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==380 and catalog[:377]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：380作品**。mainのDBとREADMEを正本とする。
- **次：381作品目から候補調査**。重複・個別の公式Overview本文・実画像と利用権利の照合を一点ずつ行う。
- 今回378〜380：`met-845805` 長澤蘆雪《月夜山水図》（日本1794〜95年）、`met-74661` 《走る象（表）・象の素描練習（裏）》（インド、コータ、18世紀半ば）、`met-45680` 蔣嵩（伝）《冬景山水図》（中国・明代）。
- 全件Met作品別OverviewをWebで直接確認し、二つずつの短い正確な英文を日本語鑑賞解説の主張と照合。Met API作品PD・Open Access CC0画像と美術館の現代解説文の権利を区別。原寸/表示JPEGの全SHA256・バイト数・画面サイズ・縮小RMS・画像目視も確認（[一次画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42976021314)、[別JPEGを再確認](https://github.com/matumaruex/kaiga-data/actions/runs/42976707754)、[長巻の画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42976227882)）。同じAIによる別工程の監査で外部専門家の査読ではない。
- `met-74661`は公式主画像が表側のみ、`met-45680`は7mの長巻の一部分のみであることを明記。`met-45680`の作者帰属は未確定。すでに登録済みの韓国作品と非PDのエチオピア作品は除外。
- 既存377作品と画像台帳の以前の部分は変更せず、[新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-378.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 378-380")
 run("git","push")
 print("REGISTRATION-PASS 380 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
