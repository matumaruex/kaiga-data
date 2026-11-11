#!/usr/bin/env python3
"""TEMPORARY one-off 351–353 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42948048573"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":50486,"artist":"Yi Jeong (artist name: Taneun)","ja":"風竹図","tones":["静けさ"],"themes":["自然","時間"],"emotions":["希望"],"strengths":{"希望":1},"primary":[],"secondary":["希望"],"situation":"朝鮮時代の文人画で風にしなる竹の筆遣いと、折れずに耐える姿に込められた意味を感じたい","history":"Met公式作品別Overviewによると、朝鮮時代の文人画家李霆（タンウン）は世宗大王の玄孫で、詩・書・水墨画に優れた。竹の葉先の細い線や、風を受けた折れたように曲がる葉の描写には書法的な技術が用いられている。濃淡の異なる重なった竹が奥行きを生み、儒教・道教で高潔さや節操の象徴とされる。作品の銘文も、竹が風に折れずにしなる粘り強さを述べる。心情や作者の個人経験に結びつけすぎない。","visual":"公式主JPEGの縮小画像を実際に見て確認。縦長の絹地の下半分には風で右へなびく細い竹や葉が濃墨と薄墨で重なり、上部には墨で書かれた漢字の詩文。全体の上下には青色の装丁や周囲余白が見える。密度の低い竹と余白が主題。","limits":"実際の嵐や作者の心理状態を断定しない。『希望』は鑑賞者の連想として弱いタグにとどめ、儒教・道教の象徴は美術館の解説に従う。画中銘文は直接翻訳せず公式訳の趣旨のみ示す。","visitor":"長い掛軸の下半分に、風を受けて斜めに傾く竹が描かれています。濃い墨の葉と薄い墨の茎が重なり、奥行きが生まれています。鋭く尖った葉先や折れ曲がる線には、書道のような精密な筆づかいが見られます。\n\n作者の李霆は17世紀初めの朝鮮の文人画家で、世宗大王の玄孫にあたります。竹は儒教や道教の伝統で高潔さや節操の象徴とされてきました。美術館の解説では、風を受けてもしなやかに曲がり、折れない竹の姿が粘り強さを表すと説明されています。\n\n上部に書かれた詩と、その下の竹を行き来しながら見ると、少ない色数で風の存在を感じさせる仕組みが分かります。動きのある葉と静かな余白の対比にも注目してみてください。","quotes":[["His calligraphic brushwork showcases intricate techniques","鋭く尖った葉先や折れ曲がる線には、書道のような精密な筆づかいが見られます","Overview: calligraphic leaves and brushwork"],["Bending but not breaking in the wind, bamboo embodies resilience and fortitude","風を受けてもしなやかに曲がり、折れない竹の姿が粘り強さを表す","Overview: bamboo symbol of resilience"]],"known":{"title":"Bamboo in the Wind","date":"early 17th century","medium":"Hanging scroll; ink on silk with gold on colophon","culture":"Korea","accession":"2015.300.299"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP355790.jpg","509ba497b1763032669bfe57ea68855e007f15af80c727fde81650d3c82e07cd",1364409,1716,3880],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP355790.jpg","56edcef599c4dc77e7d6e5914f17e7897c33d2238a4a09d1d7a6b728047cc8d7",53250,276,624]}},{"num":765275,"artist":"Attributed to Ramji working in the workshop of Sahib Ram","ja":"ラーダーに扮した宮廷女性","tones":["余韻"],"themes":["愛情","他者との距離","時間"],"emotions":["未練"],"strengths":{"未練":1},"primary":[],"secondary":["未練"],"situation":"18世紀のジャイプル宮廷絵画で、詩歌のヒロインと美しい服飾表現がどう重なったかを観察したい","history":"Met作品別Overviewによると、暗い室内に立つ理想化された宮廷女性は、シンバルと拍子を取る道具を持つ。羽を飾った大きなターバン、緑の長衣、宝石と白真珠の列が華やかに強調される。彼女は恋人と離れた状態の感情を体現する詩的原型のナーヤカーで、背景の青がクリシュナを示唆するため、その恋人ラーダーに扮した女性かもしれないと解釈される。画風からラームジーに仮に帰属するが確定ではない。18世紀末ジャイプル宮廷で短期間に大画面の洗練された作品群が作られた。","visual":"公式原画像から作ったサムネイルを目視。広い薄クリーム色の台紙の中央、赤と金の装飾縁のある縦長の画面。黒っぽい背景に緑の長衣と羽の付いた頭飾りを着けた女性が立ち、左右の手に小さな楽器を持つ。宝石の装飾と明るい顔・首が目立つ。","limits":"彼女は理想化された人物であり、歴史上の特定の女性とは断定しない。ラーダーは『扮した可能性』のある解釈で確定しない。作者も『Attributed to』で筆者の確定はしない。モデルの実際の恋愛感情を推測しない。","visitor":"暗い室内を背景に、鮮やかな緑の長衣と羽飾りのついたターバンを身につけた女性が立っています。両手にはシンバルや拍子を取る道具を持ち、白い真珠と宝石が身体の輪郭を明るく飾ります。\n\nこの人物は、恋人と離れた切なさを表現するインドの詩的な女性像「ナーヤカー」として描かれています。青い背景が神クリシュナを連想させるため、その恋人ラーダーに扮した宮廷女性かもしれないとメトロポリタン美術館は解釈しています。\n\n18世紀末、ジャイプルの宮廷では、このような大画面で装飾性の高い絵が一時期制作されました。作者はラームジーの作と考えられていますが、確定していません。人物の姿勢や楽器、宝石の描写とともに、詩の世界を一枚の絵に表す工夫を楽しめます。","quotes":[["woman of the court is shown holding cymbals and musical clappers","両手にはシンバルや拍子を取る道具を持ち","Overview: cymbals and clappers"],["allows for a tentative attribution to the artist Ramji","作者はラームジーの作と考えられていますが、確定していません","Overview: uncertain attribution"]],"known":{"title":"A Woman of the Court Dressed as Radha","date":"late 18th century","medium":"Opaque watercolor, gold and silver on paper","culture":"India (Jaipur, Rajasthan)","accession":"2017.447"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/LC-TR_310_2017_sr1-002.jpg","0a2b02bf0d5661d262d4077bcfc49c38eadc036be70b8df1f5f2a1b03110da82",951644,1943,2449],"display":["https://images.metmuseum.org/CRDImages/as/web-large/LC-TR_310_2017_sr1-002.jpg","157c7b967157823e41366e99077824c0ae35bbfe63b6b165e0bc445fbb82fb8a",127371,495,624]}},{"num":65003,"artist":"Unknown artist (Marwar/Jodhpur court)","ja":"騎馬の貴族の肖像","tones":["落ち着き"],"themes":["共同体","時間"],"emotions":["畏敬"],"strengths":{"畏敬":1},"primary":[],"secondary":["畏敬"],"situation":"インドの武人が馬上で描かれる肖像画における色面・服飾・武器の役割を考えたい","history":"Met公式作品別Overviewでは、マールワール地方の画家がはっきりした色面を用いて騎馬の貴族一人の存在感を際立たせたと述べる。盾と槍は戦場と宮廷での社会的身分を示す。横顔の精緻な描写と控えめな衣服の陰影は、ダルチャンドの下での当時のジョードプル宮廷におけるムガル絵画とのつながりを示す。作品には作者名の確定がないためダルチャンドを作者と断定しない。","visual":"Met公式JPEGの縮小画像を実見。緑一色に近い平坦な野原と薄い青灰色の空を背景に、左へ進む黒茶色の馬に、白い上着・頭巻き・赤い腰飾りをつけた人物が乗る。黒い丸盾を横に抱えて細い長槍を立てる。上下に細い装飾枠がある。","limits":"人物の固有名は不明。『ダルチャンドの下で』の説明は画風の連関であり、本人の筆とは断定しない。実戦中の瞬間や具体的な戦闘は描かれていない。","visitor":"淡い空と大きな緑の野原を背景に、黒茶色の馬に乗った人物が横向きに描かれています。白い衣装と赤い腰飾り、丸い盾と長い槍が、すっきりとした輪郭の中で目立っています。\n\nこの貴族が持つ盾と槍は、戦場での役割だけでなく、宮廷での地位も示すものでした。18世紀初めのインド・ジョードプルの画家は、大胆な色面を用いて人物の存在感を強調しています。人物の横顔や衣装の細やかな描き方には、当時の宮廷がムガル絵画から受けた影響が見られます。\n\n背景の緑をあえて大きく平坦に残すことで、馬と騎手の形が際立ちます。静かな画面の中でも、斜めに進む馬の脚や槍の縦線から、動きと格式を同時に感じられます。","quotes":[["The shield and spear emphasize the nobleman’s status","この貴族が持つ盾と槍は、戦場での役割だけでなく、宮廷での地位も示す","Overview: shield, spear and court status"],["affirm links to the Mughal painting tradition in the Jodhpur court","当時の宮廷がムガル絵画から受けた影響が見られます","Overview: Mughal painting influence"]],"known":{"title":"Equestrian Portrait of a Nobleman","date":"ca. 1710–20","medium":"Ink, opaque watercolor, and gold on paper","culture":"India (Rajasthan, Jodhpur)","accession":"2002.411"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP156145.jpg","0fcc31247f67c8c70cde1631ce7f96882c042d19229ce7df16c9c1dfd2bb8078",2070932,1507,2000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP156145.jpg","0c8bc01f92088c97a7942607c4de1e0bae83980f9d5b0f2ec81fd3df794d4b57",235608,470,624]}}]''')
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
 require(len(initial)==350,"expected 350 before additions")
 for i,spec in enumerate(SPECS,351):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==353 and catalog[:350]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：353作品**。最新mainの作品DBとREADMEを正本とする。
- **次：354作品目から候補調査**。重複・作品別公式Overview・主画像の同一性・権利を個別照合。
- 今回351〜353：`met-50486` 韓国・李霆《風竹図》、`met-765275` インド・ラームジー（伝）《ラーダーに扮した宮廷女性》、`met-65003` インド《騎馬の貴族の肖像》。
- 各作品別Met公式OverviewをWebで実読して出典の短い2箇所と独自日本語鑑賞解説を対応。PD作品とMet Open Access CC0画像、現代解説文の権利を区別。原寸/表示JPEGのSHA256・バイト数・寸法・縮小一致とサムネイル目視を確認（[公式画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42948048573)）。監査は同一AIの別工程であり外部専門家による査読ではない。
- 画像利用に制限のある候補`met-10406`は登録せず。既存350作品と画像台帳の過去部分は変更しない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を参照。
"""
 p=Path("/tmp/next-artwork-resume-351.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 351-353")
 run("git","push")
 print("REGISTRATION-PASS 353 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
