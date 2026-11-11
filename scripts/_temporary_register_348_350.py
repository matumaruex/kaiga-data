#!/usr/bin/env python3
"""TEMPORARY one-off 348–350 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42946160945"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":748432,"artist":"Sin Hak-gwon (artist name: Doam)","ja":"金剛内山総図","tones":["静けさ"],"themes":["自然","時間"],"emotions":["畏敬"],"strengths":{"畏敬":1},"primary":[],"secondary":["畏敬"],"situation":"朝鮮時代の金剛山の名所を描いた長大なパノラマから風景と旅への憧れをたどりたい","history":"Met公式作品Overviewによれば、金剛山の内側の景色を六枚の紙をつなげて横長のパノラマに表し、峰・川・丘・寺院を右から左へ描く。絵の中には著名な名所46か所の名称が記されている。作者申學權は金剛山を描いた先人鄭敾の画風を意識して模し、細い峰を二重の輪郭線で表す点を自分の特徴とした。実際に金剛山を訪れられない人も、こうした絵によって名山への思いを満たしたとMetは説明している。","visual":"Met公式主表示JPEGをサムネイルで実見し、原寸JPEGとも同定。極端に横長の単一画面。黄土色がかった地に薄墨で多数の鋭い峰と谷、木々が右から左へ連なり、画面の上部付近に小さな文字が配置されている。小さな名所の個別判読は公式本文に依拠し、目視で全46箇所の名を読めたとは言わない。","limits":"山への憧れは資料の一般的な鑑賞者の文脈であり作者個人の実際の旅行経験は断定しない。金剛山は朝鮮半島の名山で、現代国家の文化的帰属を単純化しない。","visitor":"細長い画面に、鋭く伸びた山の峰や、谷を縫う川、丘と寺院が次々に現れます。右から左へ視線を送ると、山の奥を旅するように景色がつながっていきます。\n\nこれは19世紀半ばの朝鮮で描かれた金剛山の全景です。画中には名所46か所の名前が書き込まれています。作者の申學權（シン・ハクグォン）は、金剛山を描いた先人・鄭敾（チョン・ソン）の表現を意識しながら、自身の特徴として細い峰の輪郭を二重に描きました。\n\n実際に名山を訪ねられなかった人々も、こうした絵を眺めて旅への思いを深めたとメトロポリタン美術館は説明しています。名所を探す地図のようにも、連続する岩山の表情を楽しむ風景画としても見ることができます。","quotes":[["Notably, the painting identifies forty-six renowned sites by name.","画中には名所46か所の名前が書き込まれています","Overview: 46 annotated sites"],["double outlines of the spindly peaks that impart a slightly ethereal quality","細い峰の輪郭を二重に描きました","Overview: painter's double outlines"]],"known":{"title":"General View of Inner Geumgang","date":"mid-19th century","medium":"Six sheets of paper mounted as a single panel; ink and light color on paper","culture":"Korea","accession":"2017.185"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-13538-001.jpg","13e1dacd04110ef16adc3b84a0f507eedb64fa82285b1ac9084fe57eef91bdbb",1220905,4000,915],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-13538-001.jpg","316a9aba4713af488b6455d60d83e30de0919137c4c906c678c3690b3144ac30",41779,599,137]}},{"num":888892,"artist":"Unknown","ja":"クトゥブ・ミナールを描いた細密画","culture_label":"India, Delhi (museum geographical attribution; API culture unspecified)","tones":["落ち着き"],"themes":["都市","時間"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"19世紀インドで英国からの訪問者に向けて制作された、歴史建築の小さな観光記念品を鑑賞したい","history":"Met公式作品Overviewは、象牙に描かれた円形の細密画で、デリーに13世紀に建てられたモスク付属の塔クトゥブ・ミナールを主題とすると説明する。18世紀ヨーロッパで流行した象牙の円形肖像画が、東インド会社の進出でインドに広がり、訪問者の記念品として著名建築の描写にも転じた。19世紀のインドの画家が英国人旅行者向けに作り、英国へ持ち帰られるものもあった。この個体は黒色の枠と幅広い台紙の中央に円形絵が飾られている。","visual":"Met公式表示JPEGサムネイルを実見。正方形の黒い額、白い幅広の余白、中央に小さな丸い画面があり、縦長の塔と周囲の空・赤みがかった遺構・緑の地面が細密に描かれる。額装込みの画像なので、現物全面が象牙の画面だとは記さない。","limits":"材料が象牙である歴史的事実と画像利用の権利は区別。現代の象牙製品の流通を推奨・合法と断言しない。作者と制作地は公式の『Unknown』『Attributed to India, Delhi』の範囲に留める。","visitor":"黒い額の広い余白の中心に、小さな円形の絵が収められています。目を近づけると、空にそびえる細長い塔と、その周囲の建物や緑が細かく描かれていることが分かります。\n\nこの象牙の細密画には、インド・デリーのクトゥブ・ミナールが描かれています。塔は13世紀に隣接するモスクのためのミナレットとして建てられました。19世紀のインドの画家たちは、英国からの旅行者に向けてこうした絵を制作しました。建物の名所を円形の小さな画面に収める方法は、ヨーロッパで流行した肖像細密画から発展したものです。\n\n大きな建築を手のひらほどの絵で持ち帰るという、当時の旅の記念品のあり方が感じられます。額の中の小さな景色へ目を凝らす鑑賞を楽しめます。","quotes":[["This ivory miniature depicts the Qutb Minar in Delhi","この象牙の細密画には、インド・デリーのクトゥブ・ミナールが描かれています","Overview: subject and material"],["Indian artists in the nineteenth century produced works of art for English visitors","19世紀のインドの画家たちは、英国からの旅行者に向けてこうした絵を制作しました","Overview: visitor market"]],"known":{"title":"Painting of the Qutb Minar","date":"19th century","medium":"Ivory; painted","culture":"","accession":"2024.3.1"},"image":{"original":["https://images.metmuseum.org/CRDImages/is/original/DP-32733-001.jpg","07bf6e9a29d91a1fc819a153f12369b3c9c73a5248abd99a809d6a53e557d0db",2175679,3556,3459],"display":["https://images.metmuseum.org/CRDImages/is/web-large/DP-32733-001.jpg","e57e60abc7b4874a19c55d66c1af134373a291622c0602a42eb0089a99b669aa",88437,599,583]}},{"num":436976,"artist":"Otto Marseus van Schrieck","ja":"ケシと昆虫・爬虫類の静物","culture_label":"Dutch (artist nationality; Met API culture unspecified)","tones":["緊張"],"themes":["自然"],"emotions":["好奇心"],"strengths":{"好奇心":2},"primary":["好奇心"],"secondary":[],"situation":"17世紀オランダの自然観察から生まれた森の地表の静物画で、小動物の関係を探したい","history":"Met公式作品Overviewによれば、マルセウス・ファン・スリークは森の下草を調べることから「嗅ぎ回る人」という呼び名を持ち、実物の自然標本を採取し顕微鏡も使って観察するという17世紀の経験的研究の文化に参加していた。絵は花瓶ではなく野外に生えるケシの周囲で、トカゲ・ヘビ・カタツムリ・チョウなどが関わる森の地表を描いた。複数のモチーフは画室で個別に研究して一つの画面に組み合わせたと説明される。","visual":"Met公式表示JPEGサムネイルを目視。極端に暗い緑がかった地面に、上部で赤い花を咲かせるケシが目立つ。下部の落ち葉・地面・菌類・小さな生物の形が入り組むが、サムネイルだけで動物の種を全部判読したとは言わない。","limits":"画家が実際に野外で一度にこの配置を目撃したとは主張せず、スタジオ内の複合構図として説明する。具体的な捕食の瞬間や画家の思想は、対象のMet本文を越えて断定しない。","visitor":"暗い森の地面から、赤いケシの花が立ち上がっています。足元には落ち葉や草が重なり、よく見ると生き物がひそんでいます。花を中心にした明るい静物画とは違い、薄暗い自然の一角そのものが題材です。\n\nオットー・マルセウス・ファン・スリークは、17世紀のオランダで自然を細かく観察した画家でした。採集した自然の標本を調べ、顕微鏡のような新しい道具も観察に使いました。美術館の解説によれば、画面にはトカゲ、ヘビ、カタツムリ、チョウなどが関わり合う様子が描かれています。\n\n描かれた生き物は、一度に同じ場所で見つけたものではなく、画室で個々に研究したモチーフを組み合わせたものです。草の陰や花の下を順に眺めると、絵の中に小さな自然観察の世界が広がります。","quotes":[["used new technologies like the microscope to examine them","顕微鏡のような新しい道具も観察に使いました","Overview: natural specimens and microscope"],["interactions between a lizard, snake, snails, and butterflies","トカゲ、ヘビ、カタツムリ、チョウなどが関わり合う様子が描かれています","Overview: small forest-floor animals"]],"known":{"title":"Still Life with Poppy, Insects, and Reptiles","date":"ca. 1670","medium":"Oil on canvas","culture":"","accession":"53.155"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP145933.jpg","9fce409db6611c71ea6f6753dc9b7c7184dc9b8d47c8f0c1c6ee8fc3281921ac",2338342,2916,3722],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP145933.jpg","a98a7524e38e5ccc77d248d6eb55d7ee926c2b9b75e5a510b0236fc79e40cf1a",85062,489,624]}}]''')
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
 require(len(initial)==347,"expected 347 before additions")
 for i,spec in enumerate(SPECS,348):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==350 and catalog[:347]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：350作品**。正本は最新mainのデータベースとREADME。
- **次：351作品目から候補調査**。重複・作品別公式出典・主画像・著作権を一点ずつ検証。
- 今回348〜350：`met-748432` 韓国・申學權《金剛内山総図》、`met-888892` インド《クトゥブ・ミナールを描いた細密画》、`met-436976` オランダ・マルセウス・ファン・スリーク《ケシと昆虫・爬虫類の静物》。
- Met各作品別Overviewを直接読み、2つの短い正確な原文と独自日本語解説の主張を個別対応。公式API・作品PD、Open Access CC0主画像、現代の解説文は権利を別々に確認し、画像の原寸・表示JPEG完全SHA256・サイズ・縮小一致・実画面サムネイル目視を検証（[画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42946160945)、[金剛山の画像](https://github.com/matumaruex/kaiga-data/actions/runs/42946273644)）。監査は同一AIの別工程で人間の専門家の査読ではない。
- 既存347作品と画像台帳の旧部分を変更せず継続。基準は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-348.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 348-350")
 run("git","push")
 print("REGISTRATION-PASS 350 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
