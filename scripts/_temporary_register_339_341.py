#!/usr/bin/env python3
"""TEMPORARY one-off 339–341 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42932375742"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":65417,"artist":"Unknown artist","ja":"南蛮屏風（ヨーロッパ人の来航）","tones":["余韻"],"themes":["共同体","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"近世日本の屏風に描かれたヨーロッパ人の来航と、史実・想像が混ざる描写を見比べたい","history":"Met公式作品Overviewは、日本の港にヨーロッパ人が来航する南蛮屏風の一双と説明する。左隻には帆を下ろして港へ入る大型の帆船、右隻には船長・乗員の行列と、教会付近で出迎える宣教師たちが描かれる。黒衣のイエズス会士のほか茶衣のフランシスコ会士である可能性がある人物も描かれるが、右隻の中国風の衣装の女性三人は美術館が『完全に想像上の存在』と明言している。鑑賞順は右から左。主表示画像は一双全体ではなくMetの指定した主画像一枚。","visual":"金雲で場面を区切った横長の六曲屏風一隻を主画像として確認した。建物、通りを歩く人々、樹木、色鮮やかな衣服が細かく描かれている。作品は左右一双であり、主画像だけを両隻全体の画像だとは説明しない。","limits":"『南蛮』は歴史的な屏風分類の名称として使い、現代の人々の呼称として使わない。女性三人はMetが想像上の存在と述べる一方、すべての人物を個々に史実と断定しない。主画像は一双の片隻とし、もう片方の詳細は作品別Overviewに従う。","visitor":"金色の雲の間から、建物や通りを行く人々が見えます。小さな人物の衣服や動きが丁寧に描き分けられ、港町のにぎわいが画面に広がっています。\n\nこれは17世紀初めの日本で制作された、ヨーロッパ人の来航を描く「南蛮屏風」と呼ばれる一双の屏風です。左隻には帆を下ろして港に入る大型船、右隻には船長や船員の行列、教会付近で迎える宣教師たちが描かれています。左右の屏風は、右から左へと鑑賞する構成です。\n\n美術館の解説では、右隻に現れる中国風の衣服を着た三人の女性は、実際の来航を再現したのではなく、想像で加えられた人物とされています。細部を追うと、当時の交流を伝える場面と、絵画としての華やかな演出が同居していることが分かります。","quotes":[["This pair of folding screens is characteristic of Nanban byōbu","これは17世紀初めの日本で制作された、ヨーロッパ人の来航を描く「南蛮屏風」と呼ばれる一双の屏風です","Overview: object type, depicted arrival"],["The left screen depicts carracks arriving at a port with sails lowered","左隻には帆を下ろして港に入る大型船","Overview: left screen ships"]],"known":{"title":"Arrival of the Europeans","date":"first quarter 17th century","medium":"Pair of six-panel folding screens; ink, color, gold, and gold leaf on paper","culture":"Japan","accession":"2015.300.109.1, .2"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP368004.jpg","1b8232a98626ea2ce6151d47ae07c64cf70b5b35b040d9c8f25ebb9a15c4f36b",1827873,3961,1723],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP368004.jpg","d9686368aeaf9838499f985ec778b8909432fb4abd84dec6076a8944eeaf306d",67164,598,260]}},{"num":437920,"artist":"Jacob Vosmaer","ja":"花瓶に生けた花","culture_label":"Netherlands (Delft artist; Met API culture unspecified)","tones":["静けさ"],"themes":["自然","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"暗い背景に浮かび上がる花と、後世に切り詰められた静物画の構図を見つめたい","history":"Met公式Overviewによれば、デルフトの画家ヤコプ・フォスマールは花の静物画を早くから専門にした画家の一人で、当時の花の絵には、画家自身が実物を見ず図鑑でのみ知る珍しい植物も描かれた。Metはこの板絵が1870年より前に左右を切り詰め、上部を約9インチ切除され、画面上部のクラウン・インペリアル（ユリ科の花）が途中で切れていると説明する。制作年は『probably 1613』で確定年ではない。","visual":"暗い背景を背に大きな金属製の水差し形の花器に赤、桃色、青、黄、白の花々が挿される。石のような台の上に落ちた花弁と小さなトカゲ状の生き物が見える。公式同一作品IDの原画像と表示JPEGで主題と寸法を照合。","limits":"制作年は『おそらく1613年』とする。個々の花を確証なくすべて品種同定しない。画面上端の切断は制作時ではなく1870年以前の後世の変更として説明する。","visitor":"暗い背景から、赤や桃色、青、黄色の花々が浮かび上がっています。大きな水差し形の花器を中心に茎が曲線を描き、花弁には細かい光と影が重ねられています。足元には落ちた花の一部も見えます。\n\nこの絵を描いたヤコプ・フォスマールは、17世紀初めのオランダで花の静物画を早くから専門にした画家の一人です。当時は、珍しい花を実物ではなく植物図鑑で知り、描くこともありました。制作年は、おそらく1613年とされています。\n\n現在の画面は制作当初の大きさではありません。メトロポリタン美術館によれば、1870年より前に板絵の左右と上部が切り詰められ、上端に描かれた花の一部が失われています。残る花の密集した姿を見ながら、かつての画面の広がりを想像することもできます。","quotes":[["which often depict rare specimens known to the artists solely from illustrated books","当時は、珍しい花を実物ではなく植物図鑑で知り、描くこともありました","Overview: rare botanical specimens from books"],["At some time before 1870 this panel was trimmed on the sides and cut down","1870年より前に板絵の左右と上部が切り詰められ","Overview: later cropping"]],"known":{"title":"A Vase with Flowers","date":"probably 1613","medium":"Oil on wood","culture":"","accession":"71.5"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP145940.jpg","1398f9e6565a7fe0fa78008ebc040a6e958b44e3bbbd3af684081fe4573f46f6",1918695,2764,3721],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP145940.jpg","8a580c3a39258d2a28c0e94854fb2581d9380ca9a40f9b94a25f54b9ea311016",88678,464,625]}},{"num":850685,"artist":"Unknown artist (Thanjavur School)","ja":"大臣を伴うマハラジャ・セルフォージー2世","tones":["落ち着き"],"themes":["共同体","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"19世紀初めの南インドの王侯肖像におけるインドとヨーロッパの表現の重なりを見たい","history":"Met公式Overviewによると、これは1800年頃のタンジャーヴール派の大型肖像画で、インド南部タンジャーヴールを治めたセルフォージー2世と大臣を描く。王は宮廷のような室内で正面を見据え、欧州の18世紀後半の肖像画の慣習に学び、金縁と房飾りのついた厚い幕が人物を囲む。金箔を施した左右の小机にはバラ水の瓶と置時計が描かれ、デンマーク出身の宣教師から教育を受け、東インド会社の監督下で統治した王の世界を示すと美術館は述べる。別バージョンが知られ、1800年の贈り物としてウェールズのポウイス城にある。","visual":"大型の肖像画の主図は左側に華やかな衣装で杖を持って立つ王、右側に白い服とターバンの大臣。上から青い大きなカーテンと金の縁が垂れ、左右に金色の小机、右に置時計。Metが選んだ主画像と原寸の同一性を確認。","limits":"大臣の身分や来歴をMet記載以上に特定しない。別バージョンの現所在は所蔵館説明に基づく。欧州様式の取り入れ方から王の個人的な価値観を推測しない。","visitor":"華やかな衣装を着た王が左側に立ち、白い衣服の大臣が右にいます。天井から下がる深い青の幕と金色の縁飾りが、二人を舞台のように囲んでいます。\n\n描かれているのは、南インドのタンジャーヴールを治めたセルフォージー2世とその大臣です。1800年頃のこの肖像画には、18世紀後半のヨーロッパの肖像画に見られる室内表現が取り入れられています。左右に置かれた金色の小机には、バラ水の瓶と置時計が描かれています。\n\nメトロポリタン美術館は、こうした品々を、デンマーク人宣教師から教育を受け、東インド会社の監督下で統治した王の立場に結びつけています。インドの王侯肖像とヨーロッパの演出が同じ画面に重なる様子に注目できます。","quotes":[["The setting draws directly on European conventions, with heavy drapery","18世紀後半のヨーロッパの肖像画に見られる室内表現が取り入れられています","Overview: European compositional conventions"],["Gilded side-tables, one displaying a rosewater bottle and the other a mantle clock","左右に置かれた金色の小机には、バラ水の瓶と置時計が描かれています","Overview: rosewater bottle and clock"]],"known":{"title":"Maharaja Serfoji II accompanied by his Minister","date":"ca. 1800","medium":"Opaque watercolor with raised gold on paper","culture":"India, Thanjavur, Tamil Nadu","accession":"2021.81a, b"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-22860-001.jpg","e5439207dedc504834d0ad578dc97fba35930c9389a8ce95fd31e1976ee1751c",6057900,2568,3544],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-22860-001.jpg","816a94ce122c20352842ed08cd9d90cee32352b701b1a833bfea5ff609b6dbe0",326835,452,624]}}]''')
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
                 "Source Overview passages independently read via official museum page 2026-11-11. Separate AI pass is not human expert.",
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
 require(len(initial)==338,"expected 338 before additions")
 for i,spec in enumerate(SPECS,339):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==341 and catalog[:338]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：341作品**。正本はmainのDBとREADME。
- **次：342作品目から候補調査**。出典本文・画像完全性・著作権・重複を作品ごとに調査する。
- 339〜341：`met-65417` 日本《南蛮屏風（ヨーロッパ人の来航）》、`met-437920` オランダ・ヤコプ・フォスマール《花瓶に生けた花》、`met-850685` インド《大臣を伴うマハラジャ・セルフォージー2世》。
- Met各作品ページのOverview原文と解説内容の短文2箇所照合、作品・画像・説明文の権利別の確認、原寸/表示主画像の完全SHA256・寸法・縮小画像照合、個別v2監査・日本語鑑賞解説を保存（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42932375742)）。同一AIによる別工程の検証で、外部専門家の審査ではない。
- 既存338作品と画像台帳の過去部分は変更していない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-339.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 339-341")
 run("git","push")
 print("REGISTRATION-PASS 341 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
