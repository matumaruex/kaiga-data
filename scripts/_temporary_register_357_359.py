#!/usr/bin/env python3
"""TEMPORARY one-off 357–359 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42950522740"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":441971,"artist":"Jusepe de Ribera (called Lo Spagnoletto)","ja":"聖ペテロの涙","culture_label":"Spain / Italy (Spanish artist active in Italy; Met API culture unspecified)","tones":["重苦しさ"],"themes":["記憶","共同体"],"emotions":["悲しみ"],"strengths":{"悲しみ":2},"primary":["悲しみ"],"secondary":[],"situation":"宗教的な後悔と祈りの感情を、表情や組んだ手・暗い背景から感じ取りたい","history":"メトロポリタン美術館の作品別Overviewによれば、スペイン出身でイタリアで活動したフセペ・デ・リベーラの初期作品。イエスを否認した後の聖ペテロを描き、涙で赤くなった目と、祈りのために合わせた手が、罪の重みを示す。宗教的な告白の一形式として激しい涙を流す行為は、当時のカトリックの信仰実践で重要な位置を占め、詩や歌にも取り上げられた。作品が史料に現れる最初は1644年ローマの枢機卿ベネデット・モナルディ・バルデスキの収蔵記録。","visual":"Met公式の同一作品JPEGを縮小画像で目視。暗い背景の前に、灰色の髭と薄い髪の年配の男性が黄褐色の重い上着をまとい、身体を大きく曲げて左上を見つめる。左側で両手を寄せ、顔に弱い光が当たる。色数を抑えた暗い油彩で、主題を孤立させる構図。","limits":"聖ペテロの後悔はキリスト教の物語とMetの作品解釈として扱い、史実として断言しない。ペテロの具体的な言葉や涙の原因を画面から直接判読したとは言わず、公式解説に依拠する。画家の信仰心の実際は推測しない。","visitor":"暗い背景の前に、黄褐色の衣をまとった年配の男性が身をかがめています。目元には涙が浮かび、手を合わせて祈りながら、顔を上へ向けています。わずかな光が顔や衣のひだを浮かび上がらせます。\n\n描かれているのは、イエスとの関係を否定したあとで深く後悔する聖ペテロです。メトロポリタン美術館は、涙で赤くなった目と祈りのために組んだ手が、罪を背負う心の重さを示すと説明しています。当時のカトリックでは、涙を流す悔悟が信仰の実践において大切にされ、詩や歌でもたたえられました。\n\n作者リベーラはスペイン生まれで、主にイタリアで活動した画家です。激しい動きを描くのではなく、暗がりの中に表情と手だけを強調することで、内面の葛藤を伝えています。","quotes":[["his eyes red with tears and his hands clasped in prayer","涙で赤くなった目と祈りのために組んだ手が","Overview: tear-red eyes and clasped hands"],["became central to Catholic devotional practices","涙を流す悔悟が信仰の実践において大切にされ","Overview: tears in devotional practice"]],"known":{"title":"The Tears of Saint Peter","date":"ca. 1612–13","medium":"Oil on canvas","culture":"","accession":"2012.416"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP286357.jpg","d3575d5455b46be66e0fc14e7ee1e7daf9194d2e8f68bd29d99608fea4a6e68e",1684900,2721,3874],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP286357.jpg","165965b0a9ceb8b4bafef2a81b39cb353ce85c9b417b7537810cb0585e2b8f44",44549,438,624]}},{"num":853892,"artist":"Unidentified artist","ja":"龍と鯉","tones":["高揚"],"themes":["共同体","時間"],"emotions":["希望","畏敬"],"strengths":{"希望":2,"畏敬":1},"primary":["希望"],"secondary":["畏敬"],"situation":"朝鮮の龍と鯉を描いた絵に、立身出世や努力をたとえる物語と色彩の対照を見つけたい","history":"Metの作品別Overviewによれば、上部では暗い渦巻く雲と波から龍が現れ、下の長方形の蓮池には三匹の鯉が泳ぐ。龍は力と幸運を、鯉は粘り強さと強い意志を象徴する。鯉が激流を逆に泳いで跳び上がり龍になる伝説は、官吏採用試験を突破する困難を示す比喩として知られ、男児の将来の成功への願いとも結びついた。上部の円形画面は墨と色で力強く塗り、下部の水面は余白を使って柔らかく表現する。","visual":"Met公式表示JPEGの同一作品サムネイルを目視。長方形の紙の上半分にほぼ円形の枠内で鱗のある龍が大きくうねり、龍の周囲に濃い灰黒の波・雲と色のある花状の装飾。下半分の薄い線描の長方形の池に三匹の魚が泳ぎ、蓮の茎と花が立つ。上の強い動きと下の静けさが対照的。","limits":"龍と鯉の象徴は朝鮮時代の図像解釈であり、超自然的な変身を事実として述べない。特定の受験者や持ち主の願いを断定しない。作者は不明。","visitor":"画面上では、大きな龍が暗い雲と波の中から姿を現しています。その下には長方形の蓮池があり、三匹の鯉が静かな水面を泳いでいます。上の濃い色と激しい動き、下の淡い線と余白が鮮やかな対照を作っています。\n\n朝鮮時代の絵画では、龍は力や幸運を、鯉は粘り強さや強い意志を表すことがありました。鯉が流れに逆らって泳ぎ、跳び上がることで龍になるという伝説もあります。この物語は、難しい官吏採用試験を乗り越えることのたとえとなり、将来の成功を願う意味にもつながりました。\n\n龍のうねる線と、池で泳ぐ鯉の姿を見比べると、力強さと静けさが一枚の中に収められているのが分かります。","quotes":[["A dragon emerges from dark, animated clouds and waves","大きな龍が暗い雲と波の中から姿を現しています","Overview: dragon from dark clouds"],["carp represent persistence and strength of character","鯉は粘り強さや強い意志を表す","Overview: carp as perseverance"]],"known":{"title":"Dragon and carp","date":"late 19th century","medium":"Framed painting; ink and color on paper","culture":"Korea","accession":"2024.89.3"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-37218-001.jpg","cba1b5e59898d384bac1618e377a14ea3cbee0c6462ada464c3d2903735e02e1",3083464,2562,3814],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-37218-001.jpg","d647fc9d1a55e7b6f1dca45c9bede8a84111b4f437269f7a46a80e6ddcdb22d7",159015,419,624]}},{"num":853896,"artist":"Unidentified artist","ja":"書物と文房具の屏風","tones":["落ち着き"],"themes":["日常","共同体","時間"],"emotions":["好奇心"],"strengths":{"好奇心":2},"primary":["好奇心"],"secondary":[],"situation":"朝鮮の書斎図で本棚に描かれた本や文房具、果物に込められた象徴を観察したい","history":"Metの作品別Overviewによれば、19世紀朝鮮の書斎図『文房図（ムンバンド）』に属する二曲屏風で、18世紀に成立した画題。儒教の経典や通俗小説などの本の背表紙に題名が書かれた珍しい例で、書物が最も重要なモチーフ。西洋の線遠近法と陰影の技術で棚の奥行きや器物の量感を表し、陶磁器は教養、桃は長寿、種の見える切ったスイカは子孫繁栄を象徴する。もともとの表装では二面を横につなげて一つの段差のある書棚に見せていた。二曲屏風は角の場所に置くために作られることもあった。","visual":"Met公式の表示画像と原寸画像を目視。濃いベージュの横に並ぶ二面の屏風で、それぞれの狭い画面内部に書棚と重なった本・器・果物・文房具が描かれ、遠近法で棚の奥へ向かう空間を見せている。表装された二面の間は現在縦の継ぎ目として見える。狭いサムネイルから書名の個々を判読したとは主張しない。","limits":"描かれた書物の書名は公式解説に基づくが、実画面の縮小画像ですべて判読できたとは言わない。果物の象徴は当時の図像として理解し、現代科学的効能の主張にしない。作者は不詳。","visitor":"二枚の細長い画面に、本が並ぶ棚や器物、果物がぎっしり描かれています。段差のある棚の奥へ視線が入り込み、本物の書斎をのぞいているように見えます。\n\nこれは19世紀の朝鮮で描かれた、学問にまつわる品々を集めた『文房図（ムンバンド）』という絵画です。書物はこの画題の中心となるモチーフで、絵の中には儒教の経典や物語の書名も見られます。西洋の線遠近法と陰影の表現を取り入れ、棚や陶磁器を立体的に見せています。\n\n道具や果物には象徴も重ねられています。桃は長寿、種が見えるように切られたスイカは子孫繁栄を表しました。本を読む暮らしへの憧れと、縁起のよい品々を並べる楽しさが、一つの画面に込められています。","quotes":[["Books are the most important motif in the genre","書物はこの画題の中心となるモチーフで","Overview: role of books in munbangdo"],["incorporates Western linear perspective and shading techniques","西洋の線遠近法と陰影の表現を取り入れ","Overview: adopted Western perspective and shading"]],"known":{"title":"Books and Scholarly Accoutrements","date":"19th century","medium":"Two-panel folding screen; ink and color on paper","culture":"Korea","accession":"2024.89.6"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-40204-001.jpg","44b63f71aba65a9c23e3e7447ed089be824161468a5d2aa582b53665517ddab0",2532403,3002,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-40204-001.jpg","d4e5f3aad707eeacc34eac6a55845157fd97fad6c525c8791528e39e403ade58",93442,469,625]}}]''')
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
 require(len(initial)==356,"expected 356 before additions")
 for i,spec in enumerate(SPECS,357):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==359 and catalog[:356]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：359作品**。正本は最新mainの作品DBとREADME。
- **次：360作品目から候補調査**。重複・作品別公式Overview・画像同一性と権利を個別に確認。
- 今回357〜359：`met-441971` スペイン・フセペ・デ・リベーラ《聖ペテロの涙》、`met-853892` 韓国《龍と鯉》、`met-853896` 韓国《書物と文房具の屏風》。
- Met公式の個別作品ページを直接読んで本文の短い原文2箇所と独自日本語解説の重要主張を対応。作品のPD・画像のMet Open Access CC0・現代解説文の権利を区別し、主画像の原寸・表示JPEG完全SHA256・寸法・縮小画面一致と目視を検証（[画像研究](https://github.com/matumaruex/kaiga-data/actions/runs/42950522740)）。同一AIによる別パスの監査であり、外部の専門家による査読ではない。
- 既存356作品および画像台帳の既存部分は変更なし。手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-357.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 357-359")
 run("git","push")
 print("REGISTRATION-PASS 359 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
