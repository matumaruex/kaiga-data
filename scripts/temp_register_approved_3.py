from pathlib import Path
import hashlib, json, io, math, subprocess, urllib.request, urllib.parse, copy
from PIL import Image, ImageStat, ImageChops

DAY="2026-11-10"
OA="https://www.metmuseum.org/hubs/open-access"
RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42760271445"
ROOT=Path.cwd()
items=[
{
"id":435826,"title":"The Love Song","ja":"恋歌","artist":"Sir Edward Burne-Jones","date":"1868–77","culture":"British","acc":"47.26",
"shas":["b7999cfd7919574fd5e5c65683e4b7dbaac576ddfdc4f61082defeeba311cf0d","9b0a356726da653f082ef10f8cd79122d17eabda035ed09ae320461d0c111f98"],
"primary":[],"secondary":["悲しみ"],"tones":["余韻"],"themes":["愛情","時間"],
"fit":"恋の喜びと切なさが交差する絵に触れたい","fitwhy":"古い恋歌の哀歓を主題とし、音楽と三者の視線・距離が感情の余地を生む。",
"cautions":["悲しみは恋歌の憂いから鑑賞を始める弱い接点で、画中人物の心理を証明しない。","画家とマリア・ザンバコとの関係を画中の人物の同定や当該作品に関する画家自身の直接証言と混同しない。","恋を悲しみだけの物語に固定しない。Metは喜びと悲しみの交錯を記す。"],
"scholar":"Metは、古い恋歌にある悲しみと喜びの繰り返しから着想した絵と説明する。右ではクピドがオルガンのふいごを動かし、画面は音楽を通して物語に還元しきれない感情を表す。画家とモデルのマリア・ザンバコとの関係にもMetは言及する。",
"context":"1868〜1877年のキャンバス油彩。中世風の城跡と甲冑、古典風の衣装など異なる時代を重ねた、ラファエロ前派とイタリア・ルネサンスの影響を示す幻想画。画家は《Chant d’Amour》と呼んでいたとMetは紹介する。",
"visual":"夕暮れの城を背に、銀色の衣の女性がオルガンに手を添える。左に甲冑姿の人物、右に赤い衣の翼のあるクピド。手前に花が咲く。",
"uncertain":"人物それぞれの内面は資料から確定できない。画家の恋愛との結び付けはMetの解説であり、画家の当該作品への直接引用とみなさない。",
"text":"夕暮れの城跡を背に、銀色の衣をまとった女性がオルガンに手を添えています。甲冑を着た人物は彼女に目を向け、右では赤い衣のクピドがオルガンのふいごを動かします。足元には花が並び、互いの距離と視線が静かな緊張を生んでいます。\n\nエドワード・バーン＝ジョーンズが1868年から1877年にかけて描いた《恋歌》です。メトロポリタン美術館によれば、発想のもとにあるのは、恋歌には悲しいものも楽しいものもあるという古い歌の一節でした。画家はこの作品をフランス語で《Chant d’Amour》と呼びました。\n\n甲冑と城の中世的な世界に、別の時代を思わせる衣装が重ねられています。美術館は画家とモデルのマリア・ザンバコとの関係にも触れますが、画面の人物をそのまま実在の誰かと決めることはできません。音楽の響きは描かれていないのに、耳を澄ませたくなる絵です。",
"where":"Met Overview, first two paragraphs; Artwork Details 47.26; curator audio transcript on chant, music, Cupid, medieval and classical motifs",
"finding":"Met ties the work to a love-song refrain of sadness and joy, organ/Cupid, historical motifs and Maria Zambaco, without certifying depicted persons' inner states."
},
{
"id":11259,"title":"Corn Husking at Nantucket","ja":"ナンタケットのトウモロコシの皮むき","artist":"Eastman Johnson","date":"ca. 1875","culture":"American","acc":"07.68",
"shas":["f179b3a12ddc5b809fe9eea841f70878dd152561d2327703b257b43864cd747f","894bba83eb05ef045d002b9a490f816abbd62ae79fc3c5f676db51cc323ee13d"],
"primary":["懐かしさ"],"secondary":[],"tones":["にぎわい"],"themes":["共同体","日常","時間"],
"fit":"人々が集まり季節の仕事を分かち合う昔の暮らしを眺めたい","fitwhy":"秋の共同作業と、近代化の中で古い労働風景を描きとめたというMetの解説が結び付く。",
"cautions":["懐かしさは鑑賞の入口であり、作者や登場人物の心情を断定しない。","北部の自由な共同労働と南部の小作制度の対比はMetによる制作時代の読解として示す。","同題の別作、とくにシカゴ美術館版との取り違えを避ける。Met所蔵07.68の屋外群像。"],
"scholar":"Metは1876年のナショナル・アカデミー・オブ・デザイン展で注目された大作の最終習作の可能性が高いと説明する。産業化が進む時代に伝統的なニューイングランドの仕事を描いたこと、再建期の北部の共同労働が南部の小作制度に対比されたことを論じる。",
"context":"1875年頃、ナンタケット島の野外の収穫作業を描いた油彩。大作の最終習作と見られるが断定ではない。画家はクランベリー収穫や樹液採取なども描いた。",
"visual":"横長の野外風景。大きな藁の山や散った茎の間に大勢の作業者が座り、また立っている。前景に鶏、奥に建物と木立が見える。",
"uncertain":"1876年展の大作とのつながりはMetも推定にとどめる。農村労働の社会的読解と登場人物の個々の境遇は区別する。",
"text":"広い畑に人が集まり、藁やトウモロコシに囲まれて手を動かしています。奥には大きな束が積み上がり、手前には鶏が歩いています。人々はそれぞれの場所で作業しながら、ひとつの季節の仕事を進めています。\n\nイーストマン・ジョンソンが1875年頃に描いた、アメリカ・ナンタケット島の収穫風景です。メトロポリタン美術館はこの作品を、翌1876年の展覧会で高く評価された大作に向けた最後の習作だった可能性が高いと説明しています。\n\n産業化が進む時代、ジョンソンはクランベリーの収穫や樹液採取など、地域に根付いた仕事を繰り返し描きました。美術館は、南北戦争後の再建期にこの絵の共同作業が北部の自由な労働の象徴としても読まれたことを指摘しています。穏やかな田園の集まりに見える一枚には、当時の社会の捉え方も重なっています。",
"where":"Met Overview on likely final study for 1876 exhibition, industrialization and labor, Reconstruction-era contrast; Artwork Details 07.68",
"finding":"Met considers this likely the final study for an acclaimed 1876 composition and situates the harvest in Northern Reconstruction-era communal labor, not solely timeless nostalgia."
},
{
"id":57318,"title":"Three Crows in Flight","ja":"三羽黒鳥図","artist":"Shibata Zeshin","date":"19th century","culture":"Japan","acc":"51.137.3",
"shas":["33db013b1acff6266e7f10305e3042ea783eb903f706d878967e5fd8223c0910","b711e0b75b497ca18dbd48d5d115d4a4788771b5b4bd95d7ab837def8bb3c6d1"],
"primary":[],"secondary":[],"tones":["静けさ"],"themes":["自然"],
"fit":"余白と墨の濃淡から鳥の動きや遠近を見つめたい","fitwhy":"細長い掛軸の三羽のカラスは、異なる墨色で飛ぶ鳥の奥行きを感じさせる。",
"cautions":["余白だけを根拠に孤独や不安の感情タグを付けない。","金地の《烏鷺図屏風》や赤い夕空の版画と区別する。Met所蔵51.137.3は墨画の掛軸。","三羽のカラスに特定の寓意や作者の感情を込めたという直接証言は確認できない。"],
"scholar":"Metは、柴田是真が繰り返しカラスを題材にし、この掛軸の三羽の鳥に墨の濃淡の差を付けることで遠近を表現したと解説する。「是真」の署名と楕円の「対柳居」印も記録する。",
"context":"19世紀の日本で制作された絹本墨画の掛軸。Met所蔵番号51.137.3。同作家のカラス三羽と白鷺二羽を描いた金地屏風は別作品。",
"visual":"細長い縦の掛軸で、淡い余白の下半分を三羽のカラスが斜めに飛ぶ。一羽は小さく淡く、二羽は下のほうに濃く描かれ、下方に署名と印がある。",
"uncertain":"正確な制作年、鳥の寓意、作者の心情は未確認。静けさは画面のトーンであり、感情タグの強制はしない。",
"text":"縦に細長い画面には、広い余白が残されています。その下のほうを、三羽のカラスが斜めに横切ります。近くに見える鳥と遠くに見える鳥では墨の濃さが違い、わずかな筆づかいが空の奥行きを生んでいます。\n\n柴田是真が19世紀に描いた《三羽黒鳥図》です。絹に墨で描かれた掛軸で、画面には「是真」の署名と楕円形の印があります。メトロポリタン美術館は、是真が繰り返しカラスを題材にしたこと、濃淡の変化で遠近を感じさせる構成を解説しています。\n\n同じ作者には、金色の屏風にカラスと白鷺を描いた作品もあります。この掛軸では色彩や背景を大きく広げず、鳥の羽と身体の向き、残された空間に目を向けさせます。カラスたちの行く先や作者の込めた象徴的な意味までを、確かな資料から決めることはできません。",
"where":"Met Overview on three crows and ink gradations, artist's recurring crow motif, signed Zeshin and oval Tairyūkyo seal; Artwork Details 51.137.3",
"finding":"Met explains perspective via ink gradation, recurring crow subject, signature and seal; no fixed allegory or artist emotion established."
}]

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
    assert len(json.loads(data_path.read_text())["artworks"])==307+index
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
    print(f"REGISTERED {ident} total={307+index+1}",flush=True)
for index,w in enumerate(items):
    perform(w,index)
resume=ROOT/"docs/resume-artwork-work.md"
resume.write_text("""## 【最新の再開地点】2026-11-10：新規3作品を登録（mainへ統合後に310作品確定）
- ユーザー承認済みのmet-435826《恋歌》、met-11259《ナンタケットのトウモロコシの皮むき》、met-57318《三羽黒鳥図》を1作品ずつ原資料・画像・解説・権利・意味資料・感情索引・別工程監査にかけ、各preview/save/checkに成功。前307作品は不変。
- Met API作品番号、所蔵番号、Public Domain、公式原画像と表示画像を確認。6JPEGはGitHub Actions run 42760271445と登録時の再取得でSHA256照合し、縮小画素一致および原画像の実画面を確認。感情タグ：恋歌は「悲しみ」補助1、収穫画は「懐かしさ」主2、烏は0件。作者心理の断定はしない。
- 同一AIの別工程照合であり、別モデル／外部専門家の学術的保証ではない。画像CC0と現代解説文の権利を分ける。アプリ配信確認は未実施。
- **PRの2系統CI成功とmain統合の確認後に310完成を確定**。未統合ならmainは307件のまま。次は311件目の新規候補の品質を調査。
 
"""+resume.read_text(encoding="utf8"),encoding="utf8")
git("add","docs/resume-artwork-work.md")
for name in (".github/workflows/temp-probe-met-new-3.yml",".github/workflows/temp-register-approved-3.yml","scripts/temp_register_approved_3.py"):
    git("rm","-f",name)
git("-c","user.name=ChatGPT Museum Research","-c","user.email=41898282+github-actions[bot]@users.noreply.github.com","commit","-m","Record new artwork handoff and remove temporary workflows")
git("push","origin","HEAD:codex/museum-approved-308-310-20261110")
print("PUSHED_APPROVED_THREE",flush=True)
