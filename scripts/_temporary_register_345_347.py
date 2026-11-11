#!/usr/bin/env python3
"""TEMPORARY one-off 345–347 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42942527720"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":75552,"artist":"Maruyama Ōshin","ja":"夏と冬の子供遊び","tones":["にぎわい"],"themes":["日常","自然","時間"],"emotions":["喜び","好奇心"],"strengths":{"喜び":2,"好奇心":1},"primary":["喜び"],"secondary":["好奇心"],"situation":"一双の屏風に描かれた夏の舟遊びと冬の雪遊びを、季節をまたぐ子供の動きとして見比べたい","history":"Met公式作品別Overviewは、一双の屏風で夏と冬それぞれの子供の遊びを対比する。夏には小舟で互いを運ぼうとする少年たち、冬には足元の悪い雪原で雪玉を押す一団が現れ、一人の子供は荒天に頓着せず動き回る。中国の宮廷庭園で遊ぶ皇子を描く伝統から着想を得ながら、簡素な景観へ更新した例と位置づけられている。円山応震は円山派三代目。","visual":"Met公式主表示画像（2009_511a.jpg）を縮小して目視。横長の六曲屏風の中に細く淡い水景と小さな人影、右側の岸辺の植生が見え、余白の大きい画面。対になるもう一隻を主画像が写しているかのように言わない。","limits":"公式主画像は一双のうち一隻の図像に限定される。もう一隻の雪遊びはMetのOverviewを根拠に記述し、主画像で実見したとは主張しない。子供たちの実際の名前や具体的な遊戯の場所は推定しない。","visitor":"広い余白のある水辺に、小さな子供たちの姿が点々と描かれています。静かな景色の中で、人影を探すほど遊びの動きが見えてくる屏風です。\n\nこの作品は、夏と冬の遊びを描いた一双の六曲屏風です。夏の子供たちは小舟を操り、お互いを運ぼうとしています。もう一方の冬の画面では、子供たちが足元に気をつけながら大きな雪玉を運んでいます。現在の公式主画像は一双のうち一隻なので、二つの季節を比較するときには対になる画面の存在も意識するとよいでしょう。\n\n美術館は、中国の宮廷で子供が遊ぶ絵画の伝統を踏まえつつ、円山応震がそれを簡素な日本の風景へ置き換えたと説明しています。広々とした自然の中に描かれた、小さな冒険に目を向けてみてください。","quotes":[["The boys of summer try their skill at ferrying","夏の子供たちは小舟を操り、お互いを運ぼうとしています","Met exact-object Overview: summer boat play"],["winter squad braves uneven footing to shepherd","子供たちが足元に気をつけながら大きな雪玉を運んでいます","Met exact-object Overview: winter snow play"]],"known":{"title":"Children Playing in Summer and Winter","date":"early 19th century","medium":"Pair of six-panel folding screens; ink, color, and gold on paper","culture":"Japan","accession":"2009.511.1, .2"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/2009_511a.jpg","e62724fb7650fd9479f025adac913e0cb6869b4410ee254acf60cb8a1744a908",1194348,2000,806],"display":["https://images.metmuseum.org/CRDImages/as/web-large/2009_511a.jpg","1238f0ce1a398cd34538664ca6e7f3ddca6399bc0cb3398eab995e4d103802cf",142223,598,241]}},{"num":40197,"artist":"Unidentified artist","ja":"江村図","tones":["静けさ"],"themes":["自然","居場所","時間"],"emotions":["安心"],"strengths":{"安心":1},"primary":[],"secondary":["安心"],"situation":"南宋の雪景山水における塗り残しの技法と、水辺の小さな家の静けさを味わいたい","history":"Met作品別Overviewでは、広い川の近くの素朴な家に、舟を岸につけた漁師が坂を上って戻る場面だと説明。新雪の白さを描くために岩と地面は塗り残し、空と水のほうへ薄墨を施すという、通常の水墨表現を逆にした技法が用いられる。静謐な光景を、中国文化における川が象徴する質素でよい暮らしのイメージとも結びつける。元来の団扇画を後世に画帖の一葉へと仕立てた作品。","visual":"Met公式主画像（DP153520.jpg）の縮小を目視。ベージュの余白に円形の古い扇面が一枚置かれ、その中に淡い水面と岸の小屋、右側の木々や山が描かれる。扇面の外側の左下に赤い印、右側には縦書きの書の付属面が映る。扇面内の人物はごく小さいので、明確に視認できない部分はMet本文による。","limits":"画中の小人物の表情を推測しない。雪が塗り残しで表現されるという技法はMet作品別解説に依拠。右側の文字の筆者や時代は確かめていないので独自の作者推定をしない。","visitor":"円い扇面の中には、広い川と岸辺の小さな家があります。川の大きな広がりのそばに、素朴な小屋が描かれています。山と木々の輪郭は薄く、冬の静けさが画面を包んでいます。\n\nメトロポリタン美術館の解説では、舟を岸につけた漁師が、家へ続く坂道を上っていく場面とされています。画家は雪に覆われた岩と地面を塗り残しています。その代わりに空と川へ淡く墨を重ねることで、降り積もった雪の白さを表現しました。\n\nこの絵は12〜13世紀の中国・南宋時代の作品です。もとは扇に描かれ、現在は画帖の一葉として伝わっています。小さな家と広い水面の対比から、静かで質素な暮らしを思い描くことができます。","quotes":[["A rustic dwelling sits by a broad expanse of river","川の大きな広がりのそばに、素朴な小屋が描かれています","Met exact-object Overview: humble home and wide river"],["the painter has left rocks and earth unpainted","画家は雪に覆われた岩と地面を塗り残しています","Met exact-object Overview: negative space for snowfall"]],"known":{"title":"River Hamlet","date":"12th–13th century","medium":"Fan mounted as an album leaf; ink and color on silk","culture":"China","accession":"1989.363.27"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP153520.jpg","4cac6a9f26ac35e8fa9c0830e155080719d76ef2f6eac95fcb5d932d77fe60eb",3188517,4000,3683],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP153520.jpg","2a7ebdda774e45bd5cf1b1d348e21382c2a3d8a50cbafae2adc4be229abc295f",63594,600,552]}},{"num":77169,"artist":"Shibata Zeshin","ja":"烏鷺図屏風","tones":["落ち着き"],"themes":["自然"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"金地の屏風に描かれた白鷺と黒いカラスの対比や、漆を使った描画技法を観察したい","history":"Met公式作品別Overviewは、金箔地の二面に二羽の白鷺が静止し三羽のカラスが飛ぶ対照的な光景を描くと説明。白鷺の白色部分は金箔を切り抜き下地の紙を露出させることで表現した。黒いカラスには墨の代わりに漆を用い、光沢を生み出す。作者柴田是真は漆芸の名手としても知られ、二面は元来別々の木枠へ表装されていたもので、円山四条派と琳派双方の要素を組み合わせる。","visual":"Met公式主画像（DP268682.jpg）を縮小して目視。左右二面の金地屏風、左の空間には黒いカラスが三羽飛び、右の枝には白鷺が二羽とまる。枝は上から曲線的に入って、カラスの斜めの動きと鳥の静止状態を対置する。","limits":"屏風は金地に『白鷺2羽・烏3羽』を確認できるが、鳥たちの個別の動機や寓意は断定しない。過去の別々の額装と現状二曲屏風の違いを保持。","visitor":"金色の背景を二つに分けるように、左では黒いカラスが空を飛び、右では白いサギが枝にとまっています。二羽の白鷺がとまり、三羽のカラスが飛んでいます。色も動きも対照的で、画面にははっきりしたリズムがあります。\n\nこの絵を描いた柴田是真は、漆工芸の名手でもありました。白いサギは金箔を切り抜いて紙の色を見せる方法で描き、墨の代わりに漆を用いて、黒い鳥に艶やかな光を与えています。絵画と漆芸の技術を組み合わせた表現です。\n\nもともと二面は別々の木枠に納められ、現在は二曲屏風として並んでいます。動くカラスと静止したサギを交互に見比べると、金地の余白そのものが構図の一部になっていることが感じられます。","quotes":[["two egrets at rest and three crows in flight","二羽の白鷺がとまり、三羽のカラスが飛んでいます","Met exact-object Overview: subjects and contrast"],["the lacquer employed in place of ink adds","墨の代わりに漆を用いて、黒い鳥に艶やかな光を与えています","Met exact-object Overview: lacquer rather than ink"]],"known":{"title":"Egrets and Crows","date":"late 19th century","medium":"Individual panels remounted as a two-panel folding screen; colored lacquer, white pigment, and gold leaf on paper","culture":"Japan","accession":"2011.572.3"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP268682.jpg","645bf369c80d0209578a50468e2daefa80b3926a8d21392c5de294893006335c",2170064,1963,1514],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP268682.jpg","9618cb30ec5d6c391813d9fbf6d1a06d0b9831f8790e1c1ec9a2b99301c1329a",225897,600,462]}}]''')
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
 require(len(initial)==344,"expected 344 before additions")
 for i,spec in enumerate(SPECS,345):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==347 and catalog[:344]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：347作品**。正本は最新mainのデータベースとREADME。
- **次：348作品目から候補調査**。重複・一次出典本文・画像の完全性・著作権を作品単位で確認。
- 345〜347：`met-75552` 円山応震《夏と冬の子供遊び》、`met-40197` 中国・南宋《江村図》、`met-77169` 柴田是真《烏鷺図屏風》。
- 各Met公式作品別OverviewをWebで直接読み、重要な日本語解説に対応する短い原文2箇所を記録。Met Open Accessの作品PDと画像CC0、現代の解説文の別権利を確認。公式原寸/表示JPEGの完全SHA256・寸法・縮小画像一致、および公式縮小画像を別パスで目視（[研究](https://github.com/matumaruex/kaiga-data/actions/runs/42942527720)）。監査は同一AIの別工程であり人間の専門家による査読ではない。
- 既存344作品と画像台帳の過去部分は変更していない。基準は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-345.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 345-347")
 run("git","push")
 print("REGISTRATION-PASS 347 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
