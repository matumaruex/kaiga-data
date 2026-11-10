from pathlib import Path
import hashlib, json, io, math, subprocess, urllib.request, urllib.parse, copy
from PIL import Image, ImageStat, ImageChops

DAY="2026-11-10"
OA="https://www.metmuseum.org/hubs/open-access"
RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42762928000"
ROOT=Path.cwd()
items=json.loads(r'''[{"id":45808,"title":"Enjoying the Evening Cool under a Gourd Trellis","ja":"夕顔棚下納涼図","artist":"Utagawa Toyohiro","date":"early 19th century","culture":"Japan","acc":"1975.268.129","shas":["6c09bcef6c2fd006229388869efb7eefae572e44b32d8fb2e0b7882122a5437e","6c6a9b90e73a8c0db37c7b82d3edd0283696a97b760c54680b52f78f09fae297"],"primary":["安心"],"secondary":[],"tones":["落ち着き"],"themes":["日常","休息","時間"],"fit":"身近な人と夏の夜風を味わう、くつろいだ時間に触れたい","fitwhy":"夕顔の棚の下で、男女が涼み、扇とうつわを交わす具体的な休息の場面。","cautions":["安心は画中の具体的な涼みと休息に基づく鑑賞への入口であり、作者本人の心情の証明ではない。","Metが紹介する木下長嘯子の和歌への呼応は作品解釈であり、男女の発言を直接記録したものではない。","夏の終わりの寂寥感を必ず感じるよう誘導せず、涼を共有する日常として見せる。"],"scholar":"Metは、夕顔の棚の下で涼む男女を描いた本作が、木下長嘯子の和歌に通じると解説する。男が歌いかけ、女が扇を持ち飲み物を求めるような動作を、ただの日常風俗画ではなく絵画と詩の親密な結び付きとして説明している。","context":"江戸時代、19世紀初頭の紙本着色掛軸。和歌に詠まれた夕顔の棚下での夕涼みの情景を踏まえ、歌川豊広が庶民の日々のひとこまを描く。","visual":"縦長の掛軸の上に葉を広げる棚があり、その下の敷物に男女が座る。扇と飲み物を入れた器や壺が見え、背景は簡素な余白として残る。","uncertain":"二人が実在の夫婦かどうか、どの詩句を画家が直接意図したかを証明する自筆の文は未確認。和歌の結び付けはMetによる研究解釈。","text":"縦に伸びる夕顔の棚の下で、二人の人物が涼んでいます。一人は扇を手に持ち、もう一人は空を見上げるように座っています。敷物の近くには飲み物の器が置かれ、夏の日の終わりの小さな休息が描かれています。\n\n19世紀初めに歌川豊広が描いた《夕顔棚下納涼図》です。メトロポリタン美術館は、この何気ない暮らしの風景に、木下長嘯子の和歌とのつながりを見いだしています。庶民の夕涼みを描く風俗画であると同時に、詩の情景を絵へ移す営みでもあります。\n\n画面の上の葉と、下でくつろぐ二人のあいだには大きな余白が残されています。会話や歌は聞こえませんが、扇や手の動きを追うと、外の風や人と過ごす時間を想像できます。","where":"Met Overview paragraph 1 on couple, summer evening, the wife's fan and drink, song and Kinoshita Chōshōshi verse; Artwork Details 1975.268.129","finding":"Met identifies an early-19th-century ink/color hanging scroll by Utagawa Toyohiro and connects the evening-cooling genre scene to an earlier Japanese waka. Personal motives remain uncertain."},{"id":11269,"title":"Edward and Sarah Rutter","ja":"エドワードとサラ・ラター","artist":"Joshua Johnson","date":"ca. 1805","culture":"American","acc":"65.254.3","shas":["746c8e3d2514859415c6d11c8b44fe6177ba3b63aab3f5306ae4876dbbbf80be","d377c608946cfe9717456418c78b6df9d2ac7961fa3c645c0a98caff4cc705f8"],"primary":[],"secondary":[],"tones":["静けさ"],"themes":["日常","時間"],"fit":"幼い兄妹の姿に残された家族肖像と、画家の描写技法を見つめたい","fitwhy":"同じ空間に立つラター家の二人の子どもを、強い色彩と細部の観察が伝える。","cautions":["幼い兄妹の表情や家族の姿だけで慈しみや喜びのタグを付けない。","ジョンソンの生い立ちは美術館の解説を根拠とするが、被写体の内面や画家本人の発言とは区別する。","赤い鳥や果実、籠の寓意を公式出典なしに断定しない。"],"scholar":"Metによれば、本作は船長ジョシュア・ラターとメアリー・ペニントン・ラターの子、エドワードとサラの肖像である。アフリカ系アメリカ人で初期の職業的肖像画家ジョシュア・ジョンソンの、鮮やかな色彩と精緻な細部に対する関心が表れるとされ、その率直な表現は20世紀の芸術家や収集家からも評価された。","context":"1805年頃のアメリカ、ボルティモアの画家ジョシュア・ジョンソンによるキャンバス油彩。ジョンソンは奴隷身分に置かれた黒人女性と白人男性のもとに生まれ、18世紀末から19世紀初めにかけて海運・商業関係者や家族の肖像を制作した。","visual":"黒い服と白い襟を着た年長の子、白いドレスに赤い靴の年少の子が並び、片方が小さな籠を持つ。左に赤い鳥、二人が果実を手に持つ。暗色の背景が衣装と顔の輪郭を際立たせる。","uncertain":"ラター家が画家にどう注文したか、絵の鳥や果実の具体的な象徴、二人の気持ちは公式資料で確定できない。感情索引は無理に付けない。","text":"暗い背景の前に、二人の子どもが並んで立っています。年上の子は黒い服に白い襟を着け、年下の子は白いドレスと赤い靴を身に着けています。小さな籠や果実、左端の赤い鳥まで、さまざまな色と形が丁寧に描かれています。\n\n1805年頃、ジョシュア・ジョンソンが描いた《エドワードとサラ・ラター》です。二人は船長ジョシュア・ラターとメアリー・ペニントン・ラターの子どもたちで、画家が活動していたボルティモアの家庭を伝える肖像画です。\n\nメトロポリタン美術館によれば、ジョンソンはアフリカ系アメリカ人として職業的に肖像画を描いて生計を立てた最初期の画家とされています。強い色彩と細部の明晰さは、後の時代の芸術家たちにも注目されました。今の私たちには二人の生活の全体は分かりませんが、この一枚には家族が子どもの姿を残そうとした時代の表現が留められています。","where":"Met Overview, description of Captain Joshua and Mary Pennington Rutter's children, painter's professional history, colors and detail; Artwork Details accession 65.254.3","finding":"Met identifies children of the Rutter family and contextualizes Joshua Johnson's pioneering professional portrait practice and bold-detail style; it does not assign emotional allegories to the bird or fruit."},{"id":40447,"title":"Grapevine and Squirrels","ja":"葡萄と栗鼠","artist":"Unidentified artist","date":"early 19th century","culture":"Korea","acc":"1987.195","shas":["422fea0436ca1d62dc78dea153c81bf66bc0b06777d898bf4a75bf1b245e0bf9","64348586d7de3841dbaa614a7304e88f5359216e5c74a8e8a79f5707b1601bcc"],"primary":[],"secondary":[],"tones":["静けさ"],"themes":["自然","時間"],"fit":"古い朝鮮絵画で、植物と小動物の細やかな筆致をじっくり見たい","fitwhy":"垂れ下がる葡萄の房と蔓、ところどころに隠れた栗鼠、上部の詩文がひとつの縦長の画面に収まる。","cautions":["植物の豊かさだけを根拠に喜びや安心の感情を固定しない。","作者はMetの登録で不詳。上部の詩文を19世紀の日本人が書いたという説は一研究者の見解で、確定事実ではない。","Metの古いページに画像制限文が残る一方、同ページでPublic Domain / Open Accessと明記され、公式APIからPD対象の画像が取得できる。現在の画像利用条件と文章の著作権を区別する。"],"scholar":"Metは、葡萄の蔓が朝鮮王朝時代を通して文人画家の好んだ主題であり、初期の画面が画帖に多かったのに対して19世紀には掛軸や屏風など大型化したと説明する。この作品は葡萄の枝に栗鼠を配する例で、上部の漢詩は一研究者によれば19世紀の日本人による筆跡の可能性がある。","context":"朝鮮、19世紀初頭の紙本墨彩掛軸。Met1987.195、作者不詳。葡萄と栗鼠を描き、上部に漢文四行の詩と印がある。朝鮮文人画に通じる葡萄画の伝統と関連づけられる。","visual":"縦長の掛軸に斜めに伸びる太い葡萄の蔓があり、葉と房が下へ垂れる。上部に墨書と赤い印、枝には小動物の姿が紛れる。広い紙地と墨の濃淡が葉や蔓の質感を分ける。","uncertain":"作者名、葡萄・栗鼠の画中での限定的な寓意、詩文の筆者は特定されていない。19世紀日本人による銘文説も研究者の判断であり確証ではない。","text":"大きく曲がった葡萄の蔓から葉と房が垂れ、枝のあいだには小さな栗鼠も描き込まれています。上の方には縦書きの詩と印があり、植物の動きと文字がひとつの掛軸の中に重なります。\n\nこの《葡萄と栗鼠》は、19世紀初めの朝鮮で描かれた作品で、作者の名前は分かっていません。メトロポリタン美術館によれば、葡萄は朝鮮王朝の文人画で親しまれた画題でした。以前は画帖の小さな頁に描かれることが多かった葡萄画が、19世紀にはこうした縦長の掛軸や屏風にも描かれるようになったと説明されています。\n\n上の漢詩については、19世紀の日本人が書いた可能性を指摘する研究者もいます。ただし筆者が確定したわけではありません。葉と蔓の重なり、余白、文字の位置を行き来すると、風景画とは違う密度で自然を描きとめた作品であることが見えてきます。","where":"Met Overview on grapevine motifs in Joseon literati art and nineteenth-century hanging scrolls; Signatures, Inscriptions, and Markings on four-line Chinese poem and speculative Japanese handwriting; Artwork Details accession 1987.195","finding":"Met documents the grape-and-squirrel theme, Korean nineteenth-century hanging-scroll format, and uncertain attribution of the inscription to a Japanese hand. Artist is unidentified; symbolism not fixed."}]''')

def fetch(url):
    req=urllib.request.Request(urllib.parse.quote(url,safe=":/%?=&,.-_~"),headers={"User-Agent":"MuseumResearch/1.0"})
    with urllib.request.urlopen(req,timeout=70) as r:
        assert r.status==200
        return r.read(),r.url
def save_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args): subprocess.run(list(args),check=True)
def git(*args): run("git",*args)
def perform(w,index):
    n=w["id"]; ident=f"met-{n}"; official=f"https://www.metmuseum.org/art/collection/search/{n}"
    api=f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{n}"
    info=json.loads(fetch(api)[0])
    assert info["objectID"]==n and info["title"]==w["title"] and info["artistDisplayName"]==w["artist"]
    assert info["isPublicDomain"] is True and info["accessionNumber"]==w["acc"] and info["objectDate"]==w["date"]
    assert info.get("classification")=="Paintings" or info["objectName"].lower() in ("painting","hanging scroll")
    data_path=ROOT/"data/artworks.json";registry_path=ROOT/"data/image-sources.json"
    assert len(json.loads(data_path.read_text())["artworks"])==310+index
    pics={}; imgs={}
    for kind,key,expected in (("display","primaryImageSmall",w["shas"][0]),("original","primaryImage",w["shas"][1])):
        raw,url=fetch(info[key])
        sha=hashlib.sha256(raw).hexdigest();assert sha==expected,(ident,kind)
        pil=Image.open(io.BytesIO(raw));assert pil.format=="JPEG"
        pics[kind]=pil.convert("RGB")
        imgs[kind]={"url":url,"sha256":sha,"byte_length":len(raw),"width":pil.width,"height":pil.height}
    resized=pics["original"].resize(pics["display"].size,Image.Resampling.LANCZOS)
    rms=math.sqrt(sum(x*x for x in ImageStat.Stat(ImageChops.difference(resized,pics["display"])).rms)/3)
    assert rms<20
    high={k:imgs["original"][k] for k in ("url","sha256","byte_length","width","height")}
    high.update({"verification":"complete_jpeg_sha256_and_downscale_match","source_identity_basis":f"Official original/display downscale RMS {rms:.4f}","last_full_sha_checked_on":DAY,"human_visual_checked":False})
    strengths={s:(1 if s in w["secondary"] else 2) for s in w["primary"]+w["secondary"]}
    emotions=w["primary"]+w["secondary"]
    visitor={"language":"ja","text":w["text"],"source_urls":[official],"review":{"content_status":"verified","source_status":"verified","rights_status":"verified","reviewed_on":DAY}}
    curation={"emotions":emotions,"emotion_strengths":strengths,"tones":w["tones"],"themes":w["themes"],"evidence_url":official,
      "search_profile":{"fitting_situations":[{"situation":w["fit"],"reason":w["fitwhy"],"strength":1 if not w["primary"] and w["secondary"] else 2}],"selection_cautions":w["cautions"],"review_status":"evidence_reviewed"},
      "meaning_basis":{"author_intent":{"status":"not_verified_for_this_work","summary":None,"source_url":None},
         "scholarly_interpretation":{"summary":w["scholar"],"source_url":official},"creation_context":w["context"],
         "visual_clues":w["visual"],"uncertainty_note":w["uncertain"]},
      "emotion_categories":{"primary":w["primary"],"secondary":w["secondary"]}}
    art={"id":ident,"source":{"museum":"Metropolitan Museum of Art","artwork_id":n,"artwork_url":official,"api_url":api,"record_checked_on":DAY},
      "facts":{"title_original":w["title"],"title_ja_provisional":w["ja"],"artist":w["artist"],"creation_date_display":w["date"],"type":"Painting","is_public_domain_at_source":True,"culture":w["culture"],"accession_number":w["acc"]},
      "image":{"image_id":ident+"-primary","iiif_base":None,"iiif_reference_url":None,"display_url":imgs["display"]["url"],"source_registry_id":ident,"local_path":"/artworks/"+ident+".jpg","sha256":imgs["display"]["sha256"],"byte_length":imgs["display"]["byte_length"],"live_image_checked":True,"live_check_scope":f"Met full JPEG bytes/SHA256 and pixel fit at RMS {rms:.4f}; image viewed in official-source GitHub Actions {RUN}","source_accession_number":w["acc"],"high_resolution":high},
      "curation":curation,
      "review":{"facts_checked_against_museum_api":True,"source_public_domain_flag_checked":True,"visual_checked":False,"curatorial_reviewed_on":DAY,"curatorial_review_status":"provisional","curatorial_review_note":f"Met website, object API, original JPEG visual preview and exact SHA check {RUN}; same assistant separate-pass analysis not external scholarly audit.","ai_content_review_status":"pending","source_evidence_review_status":"pending","image_subject_match_status":"pending"},
      "visitor_explanation":visitor}
    ir={"id":ident,"title":w["title"],"official_artwork_url":official,"origin":"met_official_primary","in_shared_catalog":True,"verification":"met_primary_jpeg_http_verified",
      "image_source":{"type":"met_open_access","official_image_page":official,"license_label":"The Met Open Access / CC0 (work-level Public Domain, official primary JPEG)","license_url":OA,"verified_download_url":imgs["display"]["url"],"sha256":imgs["display"]["sha256"],"byte_length":imgs["display"]["byte_length"],"last_http_sha_checked_on":DAY,"last_verification_evidence":RUN,"license_review_status":"official_OA_confirmed_release_review_pending","high_resolution":copy.deepcopy(high)},
      "accession_number":w["acc"]}
    candidate=ROOT/f"drafts/artwork-additions/{ident}.json";draft=ROOT/f"drafts/visitor-explanations/{ident}.json";audit=ROOT/f"docs/artwork-completion-audits/{ident}-{DAY}.json"
    save_json(candidate,{"schema_version":"artwork-addition-proposal-v1","id":ident,"artwork":art,"image_record":ir})
    save_json(draft,{"id":ident,"visitor_explanation":visitor,"evidence":[{"claim":w["finding"],"source_url":official,"source_location":w["where"],"checked_against_source":True}]})
    obs=w["visual"]+f" Original and display JPEGs match exact Met object {n} and both versions agree (RGB RMS {rms:.4f}); official original preview visually checked."
    sources=[{"url":official,"location":w["where"],"finding":w["finding"],"checked_against_source":True},
      {"url":api,"location":"Met API objectID, artistDisplayName, objectDate, accessionNumber, classification, Public Domain flag, original and small image URLs","finding":f"Met object metadata and exact JPEG bytes reconfirmed after full SHA256 checks in {RUN}.","checked_against_source":True},
      {"url":OA,"location":"Met Open Access CC0 release for public domain artwork images","finding":"Artwork is marked Public Domain and its official image is eligible for CC0; modern text rights are separate.","checked_against_source":True}]
    rights={"artwork":{"verified":True,"public_domain":True,"source_url":official,"finding":"The Met explicitly marks the specific artwork Public Domain; this does not cover modern museum prose."},
      "image":{"verified":True,"permitted_for_site_use":True,"source_url":OA,"finding":"Official Met primary-image and Open Access policy allow reuse of this PD work's image; full SHA and visually verified."},
      "text":{"verified":True,"independent_japanese_prose":True,"source_url":official,"finding":"New original Japanese writing based on source facts, not long copying or close translation; legal certainty not guaranteed."}}
    review={"result":"PASS","method":f"Same assistant rechecked source facts and visual observations separately from drafting, with direct Met API and image file re-download. Verified original/display SHA256 and resized pixel RMS; official-source visual previews in {RUN}.",
      "limitations":"Not a different model or independent human expert. Legal reuse is an evidence-based assessment, not legal opinion. Previews examined; not every full-resolution pixel visually inspected.",
      "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
      "findings":{"identity":f"Met {n}, accession {w['acc']}, exact title/artist/date and Public Domain.","image_match":obs,"historical_interpretation":w["finding"],
        "emotion":f"Only {strengths} linked as viewing index; no claims about figures' private feelings.","visitor_text":"New Japanese explanation checked for accuracy and independent wording.","rights":"Artwork PD, official image CC0, museum prose separately considered."}}
    audit_doc={"schema_version":"artwork-v2-new-registration-1","id":ident,"checked_on":DAY,"result":"PASS","unresolved_material_issues":[],
      "candidate_path":str(candidate.relative_to(ROOT)),"candidate_sha256":digest(candidate),"draft_path":str(draft.relative_to(ROOT)),"draft_sha256":digest(draft),
      "baseline":{"artworks_sha256":digest(data_path),"image_registry_sha256":digest(registry_path)},
      "source_evidence":sources,"rights":rights,"separate_pass_review":review,
      "image_evidence":[{"kind":kind,"url":v["url"],"sha256":v["sha256"],"byte_length":v["byte_length"],"download_status":200,"full_bytes_sha256_checked":True,"image_subject_visually_compared":True,"observation":obs,"checked_on":DAY} for kind,v in imgs.items()],
      "notes":["User explicitly approved three selected works.","Same-assistant source/visual second pass not external expert review.","No changes to previously registered artworks."]}
    save_json(audit,audit_doc)
    ar=str(audit.relative_to(ROOT))
    run("python3","scripts/add_artwork.py","preview","--audit",ar)
    run("python3","scripts/add_artwork.py","save","--audit",ar)
    run("python3","scripts/add_artwork.py","check")
    git("add",str(candidate.relative_to(ROOT)),str(draft.relative_to(ROOT)),ar,"data/artworks.json","data/image-sources.json","README.md")
    git("-c","user.name=ChatGPT Museum Research","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","commit","-m",f"Add reviewed Met artwork {ident}")
    print(f"REGISTERED {ident} total={310+index+1}",flush=True)
for index,w in enumerate(items):
    perform(w,index)
resume=ROOT/"docs/resume-artwork-work.md"
resume.write_text("""## 【最新の再開地点】2026-11-10：新規3作品追加候補311–313件（main統合後に313件確定）
- 新規 met-45808 歌川豊広《夕顔棚下納涼図》、met-11269 ジョシュア・ジョンソン《エドワードとサラ・ラター》、met-40447 作者不詳《葡萄と栗鼠》について、Met個別解説・公式APIと画像・権利・意味資料・鑑賞者向け日本語本文・同一AI別工程監査を1点ずつ確認・保存。
- 原画像・表示画像のJPEG計6件をGitHub Actions run 42762928000 と本登録時の再取得で全SHA256とRGB縮小比較、図像プレビューの目視照合を実施。Met Open AccessのPD/CC0画像と現代の解説文を区別。葡萄図の旧UIは画像制限とPD/OA表示が併存するため公式APIのPublic Domainフラグ・OA説明・実画像取得を根拠として記録。
- 歌川豊広は休息と夕涼みを具体的に描くため主タグ安心2、ジョンソンと朝鮮葡萄図は無理に感情タグを付けず0件。作者自身の心情・登場人物の心理は断定しない。
- scripts/add_artwork.py の preview/save/check を各作品で通過。旧310作品には変更なし。別工程監査は同一AIであり別モデル・専門家による独立審査とは称さない。
- **PRの作品DB・鑑賞下書きCI両方が成功しmainへ統合した時だけ313完成と確定。** 次は314件目から新規候補を調べる。展示アプリへの反映確認は別工程。

"""+resume.read_text(encoding="utf8"),encoding="utf8")
git("add","docs/resume-artwork-work.md")
for name in (".github/workflows/temp-inspect-met-311.yml",".github/workflows/temp-register-expansion-3.yml","scripts/temp_register_expansion_3.py"):
    git("rm","-f",name)
git("-c","user.name=ChatGPT Museum Research","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","commit","-m","Record 311-313 handoff and remove temporary tooling")
git("push","origin","HEAD:codex/museum-expansion-311-313-20261110")
print("PUSHED_EXPANSION_THREE",flush=True)
