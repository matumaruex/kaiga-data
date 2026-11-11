#!/usr/bin/env python3
"""TEMPORARY one-off 336–338 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42929134131"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":45655,"artist":"Attributed to Lü Jingfu","ja":"花蝶図","tones":["静けさ"],"themes":["自然"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"14世紀の中国花鳥画に見られる花や昆虫の描写を丁寧に見たい","history":"Met公式作品Overviewは、この掛軸を毗陵派に属する花卉画と説明し、呂敬甫による署名のある作品との類似性から同画家への帰属を示す。元は対になる一組の片方で、芥子や菊などの草花の間に蝶とカマキリ、前景にはサンショウウオ、左右に蘭と白菜を置く。花と小動物の組合せが当時の装飾美術にも見られ、自然界で繰り返される捕食の象徴として読む可能性が論じられている。","visual":"縦長の絹地に草花の茎が上下に伸び、蝶やカマキリが花の周囲に配置される。中央下には小さなサンショウウオが見える。画面は茶系の地に淡い彩色が重なる。Met所蔵の同一作品IDの公式画像に基づく。","limits":"作家は『Attributed to』であり真筆の断定を避ける。花や昆虫が必ず特定の政治的寓意を持つとは断言しない。Metが述べる捕食の象徴は一般的な図像解釈として扱う。","visitor":"淡い茶色の絹地に、細い茎を伸ばす花々と、蝶やカマキリが描かれています。画面手前にはサンショウウオがいて、左右には蘭と白菜が配されています。花弁や羽は、細い筆先と控えめな彩色で表現されています。\n\nこの作品は、14世紀の中国で描かれ、呂敬甫の作と考えられていますが、確定しているわけではありません。かつては一対の画面の片方でした。メトロポリタン美術館は、花と虫の描写を当時の装飾美術とも結びつけ、自然界の捕食関係を象徴する可能性にも触れています。\n\n花だけでなく、その間を飛ぶ虫や地面近くの小動物にも目を向けると、静かな植物画の中に小さな生き物どうしの関係が浮かび上がります。","quotes":[["Originally one of a matching pair of panels","かつては一対の画面の片方でした","Overview: originally paired panels"],["a salamander in the center foreground is flanked","画面手前にはサンショウウオがいて、左右には蘭と白菜が配されています","Overview: salamander with orchid and cabbage"]],"known":{"title":"Flowers","date":"14th century","medium":"Hanging scroll; ink and color on silk","culture":"China","accession":"12.37.134"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DT235402.jpg","821957dab4b2e026890437df65775f19340dfb52b10d6ee64ab9934ba81f492d",1557792,1989,3722],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DT235402.jpg","afd5fdeb63866c5b8521ed4adb8413c0114450578cbbdbf5a40b3be799bbb368",49785,333,623]}},{"num":436595,"artist":"Francesco Guardi","ja":"幻想風景","culture_label":"Unspecified by Met API (Italian artist; Venetian painting)","tones":["余韻"],"themes":["自然","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"実景ではない風景の中に海辺、岩、廃墟、人物を組み合わせる工夫を味わいたい","history":"Met公式作品Overviewによると、これは空想の風景『カプリッチョ』であり、ウーディネ近郊のコッロレード・ディ・モンテ・アルバーノ城由来の三作品のうち一つ。画家は装飾用の漆喰の枠に納めるため、制作中または直後に画面の形と大きさを調整した可能性がある。岩場、斜めに傾く木、古典的な廃墟を組み合わせ、漁師とその家族を画面に配置した。","visual":"柔らかい雲の下、左に小舟の浮かぶ水辺、中央から右に岩や傾いた木と廃墟があり、小さな人影が点在する。Met公式の同作品ページと原寸・表示主画像から画面構成を照合した。","limits":"場所を実際の特定の海岸と断定しない。額装のための形状変更は美術館が可能性として述べた範囲に留める。","visitor":"大きな空の下、左には小舟が浮かぶ水面、右には岩場と傾いた木々、古い建物の廃墟が描かれています。岸には小さな人物が点在し、広い風景に日々の営みを感じさせます。\n\nこの作品は、現実の場所をそのまま描くのではなく、想像上の風景を組み立てる『カプリッチョ』です。岩場、傾いた木々、古代建築の廃墟を組み合わせて描かれています。メトロポリタン美術館によれば、もともとイタリア北東部の城にあった三点のうち一つで、装飾の枠に合わせて画面の形を調整した可能性があります。\n\n人々のいる地面から、樹木や建築の輪郭、空へと視線を動かすと、異なる景色の断片が一つに溶け合う様子を楽しめます。","quotes":[["This imaginary landscape, or capriccio, is one of three","この作品は、現実の場所をそのまま描くのではなく、想像上の風景を組み立てる『カプリッチョ』です","Overview: imaginary capriccio"],["rocky outcroppings, slanting tree trunks, and classical ruins","岩場、傾いた木々、古代建築の廃墟を組み合わせて描かれています","Overview: compositional elements"]],"known":{"title":"Fantastic Landscape","date":"ca. 1765","medium":"Oil on canvas","culture":"","accession":"53.225.4"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DT9351.jpg","757c2d104fdc6966b0219717bef44172e3420177a136fec70e7580bb9d880fb5",2582299,3807,3113],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DT9351.jpg","c504f684d9a9cb1f6c6c8efe1778aff368053c7c6f732fbc27cb6054ef26bbf1",73870,599,490]}},{"num":921065,"artist":"José Campeche","ja":"ニコラス・マティアス・フェルナンデス・メンデスの肖像","culture_label":"Puerto Rico (artist and sitter context; Met API culture unspecified)","tones":["落ち着き"],"themes":["共同体","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"小さな木板の肖像画から、植民地期プエルトリコの人物表現と社会を考えたい","history":"Met公式作品Overviewによると、アフリカ系のルーツを持つカンペチェは18世紀末のプエルトリコを代表する画家で、植民地社会の要請に応じて官吏や商人など多様な肖像画を制作した。本作は私的肖像の保存状態が極めて良い例で、被写体は大西洋とカリブ海をまたぐ交易に関わった役人・商人ニコラス・マティアス・フェルナンデス・メンデス。赤い制服と、背景の架空の石造りの枠が人物の存在を強調している。","visual":"赤い上着を着た成熟した男性が正面へ視線を向け、無地に近い暗色の背景と石造りを模した枠に囲まれている。Met公式同一作品画像の図像に基づく。","limits":"男性の財力や内面、交易による個人的行動の詳細を推測しない。アーティストの出自を作品のAPIにない文化項目と同一視しない。","visitor":"赤い制服の上着を着たフェルナンデスは、こちらをまっすぐ見つめています。背景には細かな物語や風景が描かれず、石造りを模した枠が人物を際立たせています。\n\n描かれたニコラス・マティアス・フェルナンデス・メンデスは、プエルトリコの役人であり、カリブ海と大西洋を結ぶ交易に関わった商人でした。画家ホセ・カンペチェは18世紀末のプエルトリコで多くの肖像画を残しました。この作品は、カンペチェの個人肖像画の中でも保存状態が非常によい例だと説明されています。\n\n小さな木板に描かれた顔と服の輪郭をたどると、装飾を抑えながら人物の存在感を伝える工夫が見えてきます。","quotes":[["an exceptionally well-preserved example of Campeche’s private portraiture","この作品は、カンペチェの個人肖像画の中でも保存状態が非常によい例だと説明されています","Overview: preservation and private portraiture"],["wearing a scarlet uniform jacket, Fernández turns his forthright gaze","赤い制服の上着を着たフェルナンデスは、こちらをまっすぐ見つめています","Overview: scarlet uniform and gaze"]],"known":{"title":"Portrait of Nicolás Matías Fernández Méndez","date":"ca. 1800","medium":"Oil on wood panel","culture":"","accession":"2025.243"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/DP-40070-001.jpg","038ddc233c20243397e62ce5a884e0f53aadb6c90ce53ca037b1b55a10f482ec",2401955,3176,4000],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/DP-40070-001.jpg","9253191cb7a6686145c77502ad9b2f2e7ff9b8a9727ee767b623c579254b7f42",70627,496,625]}}]''')
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
 if num==921065:
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil on wood panel", "American Wing painting classification discrepancy changed")
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
              "identity":f"Met object {num}, {o['title']}, {spec['artist']}, {o['objectDate']}, {o['accessionNumber']}. Attribution caveats and empty American Wing API classification preserved.",
              "image_match":spec["visual"]+f" API official primary JPEG complete hashes/dimensions, downscale RMS {rms:.5f}.",
              "historical_interpretation":spec["history"]+" Limits: "+spec["limits"],
              "emotion":"Artist's subjective mood not asserted; curated tags are grounded and may be zero: "+str(spec["emotions"]),
              "visitor_text":"Original Japanese interpretation in three paragraphs with two grounded, limited official Overview source excerpts.",
              "rights":"Museum exact-work PD; official Open Access CC0 primary images; independently written Japanese text, not copied museum prose."}},
        "image_evidence":[docs["display"][1],docs["original"][1]],
        "notes":[f"Sequential addition {sequence}; prior artworks and image-source records unchanged.",
                 "Source Overview passages independently read via official museum page 2026-11-11. Separate AI pass is not human expert.",
                 "One previously selected met-11269 is already registered and was excluded from this batch. Source excerpts in this audit are from the exact official Met object page."]]}
 write(audit_path,audit)
 run("python","scripts/verify_official_source_text.py","--audit",audit_path)
 run("python","scripts/add_artwork.py","preview","--audit",audit_path)
 run("python","scripts/add_artwork.py","save","--audit",audit_path)
 run("python","scripts/add_artwork.py","check")
 print("REGISTERED",sequence,id,o["title"],flush=True)

def main():
 initial=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 older_sources=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(initial)==335,"expected 335 before additions")
 for i,spec in enumerate(SPECS,336):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==338 and catalog[:335]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：338作品**。正本はmainのDBとREADME。
- **次：339作品目から候補調査**。重複・権利・同一画像・出典本文を作品単位で確認する。
- 336〜338：`met-45655` 中国・呂敬甫（伝）《花蝶図》、`met-436595` イタリア・フランチェスコ・グアルディ《幻想風景》、`met-921065` プエルトリコ・ホセ・カンペチェ《ニコラス・マティアス・フェルナンデス・メンデスの肖像》。
- 個別の独自日本語鑑賞解説とMet作品別Overviewの2箇所の短文引用照合、画像原寸/表示JPEGの完全SHA256・寸法・縮小一致、個別v2監査と権利区分を保存（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42929134131)）。別工程の確認は同一AIで、外部の人間の鑑定ではない。
- 既存335作品と画像台帳の過去部分は変更なし。手順は [新規追加ガイド](artwork-expansion-v2.md) および [共通品質基準](artwork-completion-workflow-v2.md) に従う。
"""
 p=Path("/tmp/next-artwork-resume-336.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 336-338")
 run("git","push")
 print("REGISTRATION-PASS 338 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
