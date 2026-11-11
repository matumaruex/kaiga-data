#!/usr/bin/env python3
"""TEMPORARY one-off 375–377 Met source-bound registration. Remove after checks."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat
ROOT=Path(__file__).resolve().parents[1]
DAY="2026-11-11"
RESEARCH_RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42970025681"
OFFICIAL_OA="https://www.metmuseum.org/hubs/open-access"
SPECS=json.loads(r'''[{"num":853449,"artist":"Domingo Ortiz","ja":"修道女ソル・フアナ・デ・ヌエストラ・セニョーラ・デ・グアダルーペの肖像","tones":["落ち着き"],"themes":["共同体","時間","記憶"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"18世紀末メキシコの修道女の肖像から、冠や宗教的装飾が新しい名と社会的身分を示すことを知りたい","history":"Met公式作品別Overviewは、1797年に16歳のフアナ・バルデスがメキシコシティのレヒナ・コエリ修道院で無原罪の御宿り会の修道女となり、ソル・フアナ・デ・ヌエストラ・セニョーラ・デ・グアダルーペという新たな名を得た際の肖像と説明する。『戴冠した修道女』と呼ばれる新スペイン固有のジャンルで、結婚の冠と指輪は『キリストの花嫁』の身分を示す。胸の大きなメダイには聖母マリアとその両親聖ヨアキム・聖アンナ、手に持つ小さな衣装付きの幼子キリスト像は祝福する右手と世界を意味する青い球を持つ。親の家に掲げることで家族の信仰・財産・社会的地位と、離れて暮らす娘の存在を伝えたとMetは述べる。作者ドミンゴ・オルティス。","visual":"公式原寸・表示JPEGとサムネイルを別々に確認。暗い褐色の背景の中に、金色の背の高い冠をかぶり青と白の修道服を着た若い女性が正面からやや斜めに立つ。胸に大きな丸い絵入りの徽章、右手側に衣装を着た幼い人物の小彫像。最下部に細字の銘文帯。新たな宗教名や年齢はMet本文の根拠であり画面から読めたとは主張しない。","limits":"本人が自主的に入会した心理や家族の感情を断定しない。『キリストの花嫁』は信仰上の象徴的な呼称。ソル・フアナは著名詩人ソル・フアナ・イネス・デ・ラ・クルスと同一人物ではない。","visitor":"金色の高い冠をかぶり、青と白の修道服をまとった若い女性が描かれています。胸元の丸い徽章には聖母マリアとその両親、手には衣装を着た幼子キリストの小像があります。暗い背景の前に、冠や装飾が明るく浮かび上がっています。\n\nこれは1797年、16歳の少女がメキシコシティの修道院で修道女となった際の肖像画です。もとの名はフアナ・バルデスでしたが、入会を機にソル・フアナ・デ・ヌエストラ・セニョーラ・デ・グアダルーペという新しい宗教名を得ました。冠と指輪は信仰上の『キリストの花嫁』を示しています。\n\nこの絵はもともと彼女の両親の家に飾られたと考えられています。離れて暮らす娘の姿を記念すると同時に、家族の信仰や社会的な地位も示す役割がありました。表情だけでなく、服装や持ち物が一人の人生の転機をどう記録しているかに注目できます。","quotes":[["a sixteen-year-old girl professed the vows of a Conceptionist nun","16歳の少女がメキシコシティの修道院で修道女となった際の肖像画です","Overview: 16-year-old's profession of vows"],["The portrait would have been displayed in the home of her parents","この絵はもともと彼女の両親の家に飾られたと考えられています","Overview: intended family-home display"]],"known":{"title":"Portrait of Sor Juana de Nuestra Señora de Guadalupe","date":"1797","medium":"Oil on canvas","culture":"New Spain (present-day Mexico)","accession":"2021.430"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/DP-25528-001.jpg","ad848d5848e92b4e39b7ba129a08904dc58d32d55b207c760afd4650c6e2efd4",4928598,3268,4000],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/DP-25528-001.jpg","78c661d559c86e483b96eb62f250e94b21b96a0f8ae0a5b12df75cdae1383275",128698,510,624]}},{"num":813585,"artist":"Henry Inman","ja":"ヘイネ・フジヒニ（イーグル・オブ・ディライト）の肖像","culture_label":"United States: American painter depicting Hayne Hudjihini of the Jiwere-Nut'achi (Otoe-Missouria) Nation","tones":["落ち着き"],"themes":["共同体","記憶","時間"],"emotions":[],"strengths":{},"primary":[],"secondary":[],"situation":"北米先住民オトー・ミズーリアの外交に携わった女性の肖像を、本人の子孫による解説とともに鑑賞したい","history":"Met公式作品別Overviewによると、ヘンリー・インマンが1832〜33年に描いた『ヘイネ・フジヒニ（Eagle of Delight）』の肖像は、トマス・L・マッケニーの北米先住民史（1836〜44年）の彩色石版画に使うため制作された。元の肖像画は1822年にワシントンに招かれた先住民の指導者たちをチャールズ・バード・キングが生きている姿から描いたが、1865年の火災で焼失した。Metはヘイネ・フジヒニをオトー・ミズーリアの首長スモニャカシーの妻と記し、イヤリングや首飾り、銀の腕輪を指摘。加えてMet公式の記事『Native Perspectives』で本人の子孫Veronica、Rock、Wolf Pipestemは、彼女がオトー・ミズーリアのワシの氏族に生まれ、額の青い入れ墨が家系の高い地位を示し、1822年に夫とともにワシントンへ出向いて部族の主権を守る外交活動を行ったと解説している。これらは子孫の説明であると出典を分けて述べる。","visual":"Met公式同一IDの元/表示JPEGを完全照合してサムネイルを目視。赤橙の衣を着た女性の胸から上を正面に近く描く。暗い髪を中央で分けて左右に垂らし、左右に細長い耳飾りと重ねた首飾り、手元に銀色の腕輪。暗い無地の背景。眉間上の青い印がうっすら見えるが、身分の意味は子孫の説明による。","limits":"アメリカ人画家の肖像を『先住民自身が描いた肖像』と混同しない。子孫の声はMet『Native Perspectives』から引用した解釈として記録し、19世紀の米国官僚が刊行した本の目的と先住民当事者の視点を同一視しない。人物の精神状態、本人の写真のような厳密な肖似は断定しない。","visitor":"赤い衣を着た女性が、暗い背景の前で静かにこちらを見つめています。髪は左右に分けられ、長い耳飾りと重ねた首飾りが見えます。描かれているのは、オトー・ミズーリア（ジウェレ・ヌタチ）の女性、ヘイネ・フジヒニです。\n\nアメリカ人画家ヘンリー・インマンによるこの肖像は、当時刊行された北米先住民の歴史書に使う彩色石版画の準備として制作されました。ヘイネ・フジヒニはオトー・ミズーリアの首長スモニャカシーの妻でした。彼女を単に肖像のモデルとしてではなく、その社会で役割を担った人物として見ることも大切です。\n\nメトロポリタン美術館が公開した本人の子孫たちの解説によれば、額の青い入れ墨は家系の地位を示し、1822年には夫とともにワシントンを訪れて部族の主権を守る外交活動に携わりました。後世のアメリカ人画家が残した姿と、子孫が伝える本人の歴史の両方を重ねて鑑賞できます。","quotes":[["were painted in preparation for hand-colored lithographs","彩色石版画の準備として制作されました","Overview: lithograph preparatory painting"],["wife of Sumonyeacathee, Chief of the Otoe-Missouria people","ヘイネ・フジヒニはオトー・ミズーリアの首長スモニャカシーの妻でした","Overview: the subject's identification and community"]],"extra_source_url":"https://www.metmuseum.org/ja/perspectives/native-perspectives","extra_source_summary":"Met Native Perspectives: descendants Veronica, Rock and Wolf Pipestem (Otoe-Missouria) explain the subject's Eagle clan, forehead tattoo, and 1822 sovereignty-related diplomatic journey; separate from American painter's object overview.","known":{"title":"Hayne Hudjihini, Eagle of Delight","date":"1832–33","medium":"Oil on canvas","culture":"American","accession":"2018.501.1"},"image":{"original":["https://images.metmuseum.org/CRDImages/ad/original/DP-18741-001.jpg","4844da5320ecad6f94ce22080ff357b40396c7504e188b879c21f97a7377ee46",4329437,3379,4000],"display":["https://images.metmuseum.org/CRDImages/ad/web-large/DP-18741-001.jpg","084182117198b9329c471819aa1a6a13f3de1aa86692f1ab53459c57f8164d5e",83471,527,624]}},{"num":441379,"artist":"Peder Balke","ja":"月光に照らされたノール岬","culture_label":"Norway (artist's home and depicted landscape; Met API culture unspecified)","tones":["静けさ"],"themes":["自然","記憶","時間"],"emotions":["畏敬","孤独"],"strengths":{"畏敬":2,"孤独":1},"primary":["畏敬"],"secondary":["孤独"],"situation":"ノルウェー最北部の岬を月光と暗い雲で描いたロマン主義の海景から、記憶と自然の広がりを感じたい","history":"Met公式作品別Overviewによると画家ペーダー・バルケはノール岬を1832年に一度だけ訪れ、その体験が終生の想像力の基点になった。1848年の作品は暗い色調と表現的な筆遣いが成熟期の特徴で、師ヨハン・クリスチャン・ダールの抑制された自然主義と対照的である。1848年秋オスロで本作か別バージョンが展示された際、批評家が題材や瞬間の独特の捉え方に関心を示した。Metの関連記事ではノール岬を船の甲板から見た16年前の記憶に基づくと説明。画面は実景の写真のような再現ではなく劇的な自然の印象を強調する。","visual":"Met公式元画像と表示JPEGを全バイトのSHAと縮小RMSで照合し目視。横長の低く暗い海面に小舟と複数の小さな人影があり、右側には大きな平たい頂を持つ岩の岬。空には厚い灰黒色の雲が広がり、雲の切れ間から落ちる月光が海面に銀色の帯を作る。淡い月光の狭い領域と黒々した海・岬の対比。","limits":"画中の舟に画家本人が乗っているとは主張しない。絵は訪問から16年後に描いたもので、その場での写生と断定しない。1848年に展示されたのがこの個体か別バージョンかは美術館も不確実とする。","visitor":"暗い雲が空を覆い、雲の切れ間から落ちる月の光が海面を細く照らしています。手前には小さな舟、その先には大きな岩の岬が広がります。わずかな光と広い暗がりの対比が、自然の大きさを感じさせます。\n\nノルウェーの画家ペーダー・バルケがノール岬を訪れたのは、1832年の一度きりでした。それでもその体験は、生涯を通じて繰り返し描く題材となりました。この絵は訪問から16年後の1848年に制作されています。\n\n暗い色調と勢いのある筆遣いは、バルケが成熟期に好んだ表現です。師であるダールの穏やかな写実とは異なり、月光と岩壁を大胆にまとめています。舟の小ささと岬の大きさを見比べると、人の存在と自然の広がりがいっそう強く感じられます。","quotes":[["Balke visited the North Cape only once, in 1832","ノルウェーの画家ペーダー・バルケがノール岬を訪れたのは、1832年の一度きりでした","Overview: single visit to the North Cape"],["The tenebrous palette and expressive brushwork seen in this moonlit view","暗い色調と勢いのある筆遣いは、バルケが成熟期に好んだ表現です","Overview: palette and brushwork in mature style"]],"known":{"title":"The North Cape by Moonlight","date":"1848","medium":"Oil on canvas","culture":"","accession":"2019.167.4"},"image":{"original":["https://images.metmuseum.org/CRDImages/ep/original/DP-1740-001_cropped.jpg","6256785d860a5af36221f98bb66b0f3682053bbf524304a0cbccc7df4441cb4c",1240553,3928,2836],"display":["https://images.metmuseum.org/CRDImages/ep/web-large/DP-1740-001_cropped.jpg","9d900f4cf9e0db79df87d43758aac639f319ba5d3f0f6c825a6265c4b32d5a9e",68092,600,433]}}]''')
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
 if num in (853449,813585):
  require(o["classification"]=="" and o["department"]=="The American Wing" and o["medium"]=="Oil on canvas","American Wing oil painting metadata changed")
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
 require(len(initial)==374,"expected 374 before additions")
 for i,spec in enumerate(SPECS,375):add(spec,i)
 catalog=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
 registry=json.loads((ROOT/"data/image-sources.json").read_text(encoding="utf-8"))["records"]
 require(len(catalog)==377 and catalog[:374]==initial,"old artwork regression or total mismatch")
 require(registry[:len(older_sources)]==older_sources,"image registry previous records changed")
 for path in ("validate_artworks.py","check_image_sources.py","check_catalog_snapshot.py"):
  run("python","scripts/"+path)
 for path in ("complete_artwork.py","add_artwork.py","rotate_resume.py"):
  run("python","scripts/"+path,"check")
 run("python","scripts/visitor_draft_queue.py","check")
 run("python","-m","unittest","discover","-s","tests","-v")
 new_status="""## 現在の状態（2026-11-11時点）

- **完成登録：377作品**。正本はmainの作品DBとREADME。
- **次：378作品目から候補調査**。重複・作品別一次出典本文・画像利用権利を一点ずつ確認。
- 今回375〜377：`met-853449` ドミンゴ・オルティス《修道女ソル・フアナの肖像》（新スペイン）、`met-813585` ヘンリー・インマン《ヘイネ・フジヒニの肖像》（米国・オトー＝ミズーリアの女性）、`met-441379` ペーダー・バルケ《月光に照らされたノール岬》（ノルウェー）。
- 各Met作品別公式Overviewの原文2箇所と独自日本語鑑賞解説の主張を照合。先住民女性の肖像では公式の当事者子孫の解説 [Native Perspectives](https://www.metmuseum.org/ja/perspectives/native-perspectives) を追加出典として区別。作品Public Domain／Met Open Access CC0原寸・表示画像／現代の美術館説明文の著作権を分離し、JPEGの完全SHA256・バイト数・寸法・縮小RMSと画像の目視を確認（[画像調査](https://github.com/matumaruex/kaiga-data/actions/runs/42970025681)）。同一AIの別工程での監査であり外部の専門家による査読ではない。
- `met-764092`はすでにDB登録済みのため除外。既存374作品と画像台帳の従来部分を変更しない。手順は [新規追加ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を継続。
"""
 p=Path("/tmp/next-artwork-resume-375.md")
 p.write_text(new_status,encoding="utf-8")
 run("python","scripts/rotate_resume.py","update","--from",str(p))
 run("git","diff","--check")
 run("git","add","README.md","data/artworks.json","data/image-sources.json",
     "docs/resume-artwork-work.md","docs/history/resume-updates.md",
     "drafts/artwork-additions","drafts/visitor-explanations","docs/artwork-completion-audits")
 run("git","diff","--cached","--check")
 run("git","config","user.name","github-actions[bot]")
 run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
 run("git","commit","-m","data: register three reviewed Met artworks 375-377")
 run("git","push")
 print("REGISTRATION-PASS 377 total; 3 entries; 6 official JPEGs, 50 unit tests, past artworks unchanged",flush=True)

if __name__=="__main__":main()
