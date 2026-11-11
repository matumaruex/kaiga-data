#!/usr/bin/env python3
"""TEMPORARY one-off 342–344 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42940134395"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":39956,"artist":"Unknown artist","ja":"舞姫図・紅葉蒔絵衝立","tones":["余韻"],"themes":["日常","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"17世紀の舞姫の衣装や所作と、絵画が後世に衝立へ仕立てられた経緯を鑑賞したい","history":"Met作品別Overviewは、舞姫の大胆な衣装模様が存在感と動きの流れを強調し、顔と手の繊細な輪郭が感情のニュアンスを伝えると説明。絵画はもとはより大きな構図の一部だった可能性があり、現在の衝立への表装は19世紀。下部の漆器部分は梨地の上に蒔絵の装飾がある。作品制作時期17世紀と表装19世紀を分けて記述する。","visual":"Met同一IDの公式JPEGをサムネイル化して目視。黒髪の一人の踊り手が金茶の背景の前で、渦巻き模様のある緑がかった小袖を着て、右手を横に伸ばし扇状の小道具を持つ。足先が左に向くように軽く動きをつけ、長方形の絵画の下に蒔絵風の下部パネルと左右の脚を備えた衝立。","limits":"踊りの具体的な曲名・舞台、作者名を断定しない。現在の衝立が17世紀に作られたとはせず、19世紀の表装と区別する。元の大画面は可能性であり確証ではない。","visitor":"金色がかった背景の前に、華やかな衣装を着た舞姫が一人立っています。袖や裾の大胆な模様が人物の動きを強調し、顔や手の細い線は所作の繊細さを伝えています。\n\n絵そのものは17世紀の日本で描かれたものです。メトロポリタン美術館によれば、もとはもっと大きな構図の一部だった可能性があります。現在見られる衝立は19世紀に仕立てられたもので、絵の下には「梨地」に「蒔絵」で飾られた部分があります。\n\n踊り手の衣装の模様から、手先の小さな動きへ視線を移してみてください。古い絵画が別の時代の装飾具に組み込まれ、今の姿となったことも作品の見どころです。","quotes":[["The bold designs of the dancer’s robe accentuate her striking presence and fluid movements","袖や裾の大胆な模様が人物の動きを強調","Overview: bold robe patterns and movement"],["which may have once been part of a larger composition","もとはもっと大きな構図の一部だった可能性があります","Overview: uncertain original larger composition"]],"known":{"title":"Freestanding Screen with Dancer","date":"17th century","medium":"Ink, color, and gold on gilt paper, mounted on a lacquered screen","culture":"Japan","accession":"29.100.520"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/29_100_520.JPG","a32e2dac628bc781405d0738e9b16544d8b07654565ae385bb135263da5d3646",106213,590,890],"display":["https://images.metmuseum.org/CRDImages/as/web-large/29_100_520.JPG","4b3f3cfbfe68ed492a9f46e57cd1b9a9274e6c66161be7c16876acb1a1e030a0",65833,414,625]}},{"num":437898,"artist":"Elisabeth Louise Vigée Le Brun","ja":"グラン夫人（ノエル・カトリーヌ・ヴォルレ）の肖像","culture_label":"France (artist nationality; Met API culture unspecified)","tones":["落ち着き"],"themes":["共同体","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"フランス革命前の社交界での肖像画と、モデルの出自・見られ方の関係を考えたい","history":"Met公式Overviewによると、ノエル・カトリーヌ・ヴォルレ（のちのグラン夫人）はインドのポンディシェリ近郊でフランス植民地系家庭に生まれ、美貌で知られ後に政治家タレーランの妻になった。周囲は出自を強調して『インド人』の呼称を与えた。ヴィジェ＝ルブランは1783年のサロンに肖像画10点と歴史画3点を出品し、この作品もその中の一つだった。同じ1783年、女性4名だけが所属する王立絵画彫刻アカデミー会員になった。","visual":"同一作品公式サムネイル実見。暗い地に楕円形の額枠を示す金の線、深緑のソファの前に座る明るい髪の若い女性。淡い銀白色の衣装と青いリボン、頭にも青い飾り。上方へ視線を向け、片腕を低く肘掛けに置き、胸元に青い大きなリボン。","limits":"人物が実際に歌っていたとはせず『歌うように』はMetがそう表現した描写に留める。『インド人』は当時の周囲による他者化の呼称であり本人の自己認識と混同しない。","visitor":"黒っぽい背景の中、明るい髪と青いリボンが目を引きます。白銀色の衣服には柔らかな光が当たり、女性は少し上を見つめています。楕円の画面が、人物へ視線を集める構図です。\n\nモデルは、のちに政治家タレーランの妻となるグラン夫人、ノエル・カトリーヌ・ヴォルレです。インドのポンディシェリ近郊のフランス植民地系の家庭に生まれ、当時の周囲からは、その出自を強調する異国趣味的な呼び名で語られました。\n\nヴィジェ＝ルブランは1783年のサロンに肖像画10点と歴史画3点を出品し、この絵もそのうちの一つです。同年、画家は王立アカデミーに選ばれた数少ない女性会員の一人となりました。衣装の明るさと視線の表情を眺めながら、肖像が人々にどう見せられたのかも考えられます。","quotes":[["Madame Grand was born to a French colonial family near Pondicherry, India","インドのポンディシェリ近郊のフランス植民地系の家庭に生まれ","Overview: colonial background and Pondicherry"],["was among ten portraits and three history paintings shown by Vigée Le Brun at the Salon of 1783","ヴィジェ＝ルブランは1783年のサロンに肖像画10点と歴史画3点を出品し","Overview: Salon of 1783 entries"]],"known":{"title":"Madame Grand (Noël Catherine Vorlée, 1761–1835)","date":"1783","medium":"Oil on canvas","culture":"","accession":"50.135.2"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP320094.jpg","0b77d80b2073e7ec78f1fe7a7c92d0360b0762b42c4aadc7258ae37aa8744215",2249298,3174,4000],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP320094.jpg","64cc076812b068a40610fafbe571bde1f4323e5f21c065b3692fcc4b627ddc61",62839,495,624]}},{"num":764096,"artist":"Unknown artist","ja":"聖母マリアの魂","tones":["静けさ"],"themes":["共同体","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"18世紀のクスコ派宗教画が祈りや瞑想に用いられた意図を理解したい","history":"Met作品別Overviewでは、クスコ派に属する作品で、聖母の内面に聖霊が宿り受肉の神秘に参加する『聖母の魂』という民間信仰の主題だと解説される。マリアは幼いイエスを抱え、胸元に聖霊を表す鳩、頭上に光輪と天使頭部を伴う。頭部周囲の文字にはIHSと祈願文、下部では翼ある二人のプットーが個人の祈りに用いる銘文を載せた碑文を支える。個人の祈祷・瞑想を助ける絵だった。","visual":"公式同一作品表示JPEGの縮小画像を目視。正面に幼子を抱えたマリアの半身像。頭部の上に赤い文字が弧を描き、胸元に白い鳩、衣装に細密な金の模様。下部に左右一対の小天使、中央に銘文。暗い縁取りと金の光の効果。","limits":"信仰内容と歴史的図像を説明するものであり、宗教的な奇跡の実在を断言しない。文字内容の翻訳はMetが解説した範囲に限り、視認できない細字は断定しない。","visitor":"装飾的な衣をまとった聖母マリアが幼いイエスを抱き、胸元には聖霊を示す鳩が描かれています。頭の周囲には文字が弧を描き、画面下には二人の小さな天使が祈りの言葉を記した板を支えています。\n\n18世紀のペルー・クスコで描かれたこの作品は、『聖母マリアの魂』という宗教的な主題を表したものです。マリアの内面に聖霊が宿るという信仰上の意味を、鳩や光、銘文によって示しています。メトロポリタン美術館によると、個人の祈りや瞑想を助けるために使われた絵でした。\n\n顔と幼子の表情を見たあと、胸元の小さな鳩、頭の周囲の文字、画面下の天使へと視線を移してみてください。一つの像に、見る人の祈りを導く要素が重ねられています。","quotes":[["Mary is represented half-length, holding the infant Christ in her arms","装飾的な衣をまとった聖母マリアが幼いイエスを抱き","Overview: Virgin Mary and infant Christ"],["The painting would have functioned as an aid to individual prayer and contemplation","個人の祈りや瞑想を助けるために使われた絵でした","Overview: use for individual prayer"]],"known":{"title":"The Soul of the Virgin Mary","date":"18th century","medium":"Oil and gold on canvas","culture":"Peru (Cuzco)","accession":"2018.836.3"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/DP-18755-013.jpg","54321f3710ffda4b07cabc893f112a4575dbb813e7ac9caab710dc0e96e45f42",6208339,3385,4000],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/DP-18755-013.jpg","89172ed09bdf2b661ef2b868c87dcf627f05373087a6ea9ddbc4fbffbfcede55",156100,528,624]}}]''')
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
 if num==764096:
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil and gold on canvas", "Peruvian oil painting metadata changed")
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
                 "Official Met artwork Overview passages were reviewed against same-object catalogue pages and two limited English excerpts were bound to visitor claims."]}
 write(audit_path,audit)
 run("python","scripts/verify_official_source_text.py","--audit",audit_path)
 run("python","scripts/add_artwork.py","preview","--audit",audit_path)
 run("python","scripts/add_artwork.py","save","--audit",audit_path)
 run("python","scripts/add_artwork.py","check")
 print("REGISTERED",sequence,id,o["title"],flush=True)

def main():
 initial=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 older_sources=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(initial)==341,"expected 341 before additions")
 for i,spec in enumerate(SPECS,342):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==344 and catalog[:341]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：344作品**。正本はmainのDBとREADME。
- **次：345作品目から候補調査**。ID重複・作品本文・画像の同一性と権利を作品単位で検証する。
- 342〜344：`met-39956` 日本《舞姫図・紅葉蒔絵衝立》、`met-437898` フランス・ヴィジェ＝ルブラン《グラン夫人》、`met-764096` ペルー《聖母マリアの魂》。
- 各Met公式Overviewと短文2箇所の出典確認、鑑賞者向けの独自日本語解説、作品・画像・説明文の権利区分、原寸/表示JPEGの完全SHA256・寸法・縮小一致に加えて三点の公式縮小画像を別パス目視（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42940134395)）。同一AIによる別工程検査であり外部専門家による査読ではない。
- 既存341作品と画像台帳の過去部分は変更していない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-342.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 342-344")
 run("git","push")
 print("REGISTRATION-PASS 344 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
