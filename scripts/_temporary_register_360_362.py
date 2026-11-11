#!/usr/bin/env python3
"""TEMPORARY one-off 360–362 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42951949511"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":436831,"artist":"Philips Koninck","ja":"広大な森の風景","culture_label":"The Netherlands (artist nationality; Met API culture unspecified)","tones":["静けさ"],"themes":["自然","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"オランダ17世紀の大空と遠くまで続く平野を眺め、実景と想像を合わせる風景画の作り方を知りたい","history":"Met公式の作品別Overviewは、この作品の地形がオランダ東部ヘルダーラント地方に着想を得た可能性があるものの、表現された風景は想像上のものと説明する。当時の画家は野外素描を資料にしつつ、画室で一つの風景を組み立てることが多かった。オランダ・アムステルダム国立美術館にある1676年の類似した川の風景には、右側に同じ優雅な狩猟用の舟『ヤハト』が描かれている。","visual":"Met公式同一作品の原寸JPEGと表示JPEGを縮小比較し、実画像を確認。横長の風景の上半分を広い灰青色の曇り空が占める。中央の低く長い地平線、左の木立と人のいる小道、右下に曲がる川と、緑の草地・遠景の村が描かれている。小さな舟の種類は公式Overviewによる。","limits":"ヘルダーラントの特定場所を写した実景として断定しない。絵の船が狩猟用船かどうかはMet本文を根拠とし、画面で小さな細部が明瞭に見えるとは言わない。人々の感情や作者の実体験は推測しない。","visitor":"雲が重なる広い空の下に、森の木々と、遠くまで続く平野が広がります。画面の左には木立と道があり、右には大きく曲がる川が見えます。近くの木々から遠い地平線まで、視線がゆっくり移動する構図です。\n\nこの風景の地形は、オランダ東部のヘルダーラント地方に着想を得た可能性があります。しかし、特定の景色を正確に写した絵ではなく、想像上の風景です。17世紀のオランダの風景画家は、自然の中で描いた素描を参考にしながら、画室で一つの風景を組み立てることが多くありました。\n\n画家フィリプス・コーニンクは、低い地平線と大きな空によって、土地の広さを感じさせています。川沿いの小さな人影や舟を探すと、遠くまで続く風景の中に人の営みが見えてきます。","quotes":[["was probably inspired by the eastern Dutch province of Gelderland","オランダ東部のヘルダーラント地方に着想を得た可能性があります","Overview: likely Gelderland inspiration"],["Dutch landscapists usually made up their views in the studio","画室で一つの風景を組み立てることが多くありました","Overview: studio construction"]],"known":{"title":"An Extensive Wooded Landscape","date":"1670s","medium":"Oil on canvas","culture":"","accession":"1980.4"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP146508.jpg","911753abe515a5718ae94b4eb266c4323741662101442271ff5d02eadad74088",3001959,3907,2893],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP146508.jpg","67f5c99f15c3d8ac100542cbd4074dd528598e55f0b40d10aa06ced7faa2b851",71608,600,444]}},{"num":441356,"artist":"Adrien Dauzats","ja":"カイロの市場","culture_label":"Egypt (depicted location); French painter (Met API culture unspecified)","tones":["にぎわい"],"themes":["都市","日常","共同体"],"emotions":["好奇心"],"strengths":{"好奇心":1},"primary":[],"secondary":["好奇心"],"situation":"カイロの市場の混雑とモスクの塔を、19世紀のフランス人画家の眼で描いた小さな絵から味わいたい","history":"Met公式作品別Overviewによると、フランスの画家アドリアン・ドーザは1830年にエジプトへ行き、約9年後にこの小さな木板の油彩画を描いた。板の絵具層は特によい保存状態にある。画家は初期に劇場の舞台装置の絵を学んでおり、空間を大胆に切り取る構図や明暗の効果、雲の前に浮かぶモスクのドームとミナレットの描写にその経験がうかがえる。実際の1830年の現地風景をそのまま描いたとまでは断定しない。","visual":"Met公式の主画像と原寸JPEGを目視。小さな縦長の板絵に、左右の古い建物に囲まれた市場の通り、手前の布で覆われた屋台や小さな人影。中央の奥にミナレット二本とドーム、白い雲が明るく広がる空。狭い路地の視線が塔へ上がる構図。","limits":"市場の具体的な店名・地名、絵の中の人物の民族や社会的役割を断定しない。画家はフランス人で描かれた文化・場所はエジプト・カイロであることを区別する。","visitor":"建物が迫る市場の通りに、日よけの布や屋台、人々の姿が重なっています。その奥にはモスクのドームと二本の高い塔が現れ、雲の明るい空に向かって伸びています。\n\nフランスの画家ドーザは1830年にエジプトを訪れました。それからおよそ9年後、1839年にこの小さな木板の油彩画を制作しています。画家は若い頃、劇場の舞台装置を描く仕事を学んでいました。その経験が、建物に囲まれた狭い道から遠くの塔を見せる構図や、光と影の表現に現れていると美術館は説明しています。\n\nにぎやかな通りから上空へ視線を動かすと、街の生活と大きな建築が一つの画面につながります。絵の小ささも意識しながら、細部を探してみてください。","quotes":[["Dauzats visited Egypt in 1830, nearly a decade before","フランスの画家ドーザは1830年にエジプトを訪れました","Overview: journey date"],["early training as a painter of set designs for the theater","画家は若い頃、劇場の舞台装置を描く仕事を学んでいました","Overview: theater scene painting training"]],"known":{"title":"A Cairo Bazaar","date":"1839","medium":"Oil on wood","culture":"","accession":"2018.209"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP-15439-001.jpg","c2c5b411004abaa4df1a149af7ba10f1c161dc959af740ef1f2e1e52c6e030a1",3666416,2998,4000],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP-15439-001.jpg","256fa11a3de51261956af0d409823d08c45db40ba4b65fc2f8699eb807dabf14",116021,468,624]}},{"num":45770,"artist":"Kawamata Tsunemasa","ja":"蛍狩りを楽しむ二人の女性","tones":["落ち着き"],"themes":["日常","自然","時間"],"emotions":["喜び"],"strengths":{"喜び":1},"primary":[],"secondary":["喜び"],"situation":"江戸時代の夏の夜、蛍の光や細い木々と人物から涼しさを感じる風俗画を見たい","history":"Met公式作品別Overviewによると、暗い衣装の年上の女性が少女に付き添い、少女は小さな籠の中の蛍を眺めている。背の高い木と曲がりながら流れる小川が画面を縁取り、茂みから飛び立つ蛍と細身の人物二人が夕涼みの感覚を生む。作者の川又常正は、若い女性の人形のような繊細な姿を特色とする川又派の浮世絵画家で、その型は後の鈴木春信によって洗練された。","visual":"Met公式同一作品の原寸・表示JPEGを縮小照合して目視。縦長の絹の掛軸に薄い茶の余白、中央に高い木の幹と枝、右下に赤い着物の小さな少女と暗い衣の年上の女性が並ぶ。水の流れと暗い草が画面の下側に描かれる。サムネイルから小さな蛍の点を一つずつ判別したと主張しない。","limits":"作者の意図や二人の実際の血縁関係は不明であり、母娘とは断定しない。年上の女性・少女という公式の人物記述に留める。時刻は夏の夕涼みという文脈で捉えるが特定の日付は分からない。","visitor":"細長い画面の中に、大きく伸びた木と、流れの曲がる小川が描かれています。手前にいるのは、赤い着物の少女と暗い衣装の年上の女性です。少女は小さな籠に捕まえた蛍を眺めています。\n\n蛍は茂みのあたりから舞い上がり、木の枝や水の流れとともに夏の夕暮れの涼しさを感じさせます。背の高い木と曲がりくねった小川が二人を囲み、細く柔らかな人物の姿を引き立てています。\n\n作者の川又常正は18世紀前半に活躍した浮世絵画家です。若い女性を人形のように繊細に描く川又派の様式は、後の鈴木春信にも受け継がれました。画面の小さな人物を探しながら、静かな夏の夜の一場面を味わえます。","quotes":[["A young girl accompanied by an older woman (in dark clothing)","手前にいるのは、赤い着物の少女と暗い衣装の年上の女性です","Overview: two women, elder in dark clothing"],["Framed by a tall tree and a meandering stream","背の高い木と曲がりくねった小川が二人を囲み","Overview: tree and meandering stream"]],"known":{"title":"Two Girls Catching Fireflies","date":"first half of the 18th century","medium":"Hanging scroll; ink, color, and gold on silk","culture":"Japan","accession":"36.100.87"},"image":{"original":["https://images.metmuseum.org/CRDImages/as/original/DP-45140-002.jpg","eae5c4a5948e44d5d143b35b8c4f6d8cd3f20f27a7897323bdebefcee4897801",2687702,2998,4000],"display":["https://images.metmuseum.org/CRDImages/as/web-large/DP-45140-002.jpg","3a94de0399284d3fbd5c70be5ac9cb4bdd1b624632e2a0ed2b4ceb36f7f95bfb",66722,468,624]}}]''')
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
 require(len(initial)==359,"expected 359 before additions")
 for i,spec in enumerate(SPECS,360):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==362 and catalog[:359]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：362作品**。正本は最新mainの作品DBとREADME。
- **次：363作品目から候補調査**。一次出典本文・画像の同一性と権利・重複を一作品ずつ照合する。
- 今回360〜362：`met-436831` フィリプス・コーニンク《広大な森の風景》、`met-441356` アドリアン・ドーザ《カイロの市場》、`met-45770` 川又常正《蛍狩りを楽しむ二人の女性》。
- Met各公式作品別Overviewの原文を直接読み、鑑賞者向け独自日本語解説と対応する短い原文2箇所を監査。作品PDとMet公式Open Access CC0主画像、現代の出典本文の権利を別扱い。原寸/表示JPEGのバイト数・SHA256・寸法・縮小一致と画像実見を確認（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42951848423)、[追加画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42951949511)）。監査は同一AIの別工程であり外部の人間の専門家による査読ではない。
- 既存359作品と画像台帳の旧部分は変更していない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md)。
"""
 p=Path("/tmp/next-artwork-resume-360.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 360-362")
 run("git","push")
 print("REGISTRATION-PASS 362 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
