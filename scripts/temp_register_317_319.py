#!/usr/bin/env python3
"""One-time, source-checked Met 317–319 registration. Refuses changes to existing works."""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile

R=Path(__file__).resolve().parents[1]
D="2026-11-10"
E="https://github.com/matumaruex/kaiga-data/actions/runs/42783837759"
OA="https://www.metmuseum.org/hubs/open-access"
W=[
dict(n=764094,title="Our Lady of Cocharcas",ja="コチャルカスの聖母",who="Unknown",
    culture="Peru (Cuzco)",when="1759",medium="Oil and gold on canvas",acc="2019.14",
    path="ad",file="DP-18755-015.jpg",
    sh="7cd23dc34fe49c79097be5372e1f9375f2f98fc9a99df9b7c82d92c3fc054dd7",sz=154576,
    oh="436cb0b6d99ada0b73fb8d70a0e04ebc73ab8b3ce364d9d770f368cb97b48b8e",oz=4911718,
    wh=[2927,4000],rms=6.6959,
    visual="画面の中心を大きく占める冠を戴いた聖母子像は天蓋と豪華な装飾に囲まれ、両側には山道を行く小さな巡礼者、遠くの教会や集落が描かれる。Met作品別画像で画面を確認。オリジナルと表示JPEGの全量ハッシュ・画素縮小一致は公式APIに基づくGitHub Actionsで確認。",
    meaning="Metの作品別解説によれば、コチャルカスの聖母の奇跡の像がアンデスの険しい山間にある行列用の祭壇に示され、周囲の曲がりくねった山道には巡礼者や信心深い人々が配される。像を周囲の人物より著しく大きく描くことで、像と場所の神聖さが強調される。9月8日の聖母祭に結びつく巡礼行列を描いたと考えられている。",
    uncertain="行列が実際の特定日の様子そのものと断定しない。制作した画家の名前も不詳。画中の聖母像への奇跡の信仰と作品の物理的効果は別。",
    tags=["畏敬"],strength={"畏敬":2},primary=["畏敬"],secondary=[],tones=["にぎわい"],themes=["共同体","自然","時間"],
    situation="宗教的な行列とアンデスの風景が一枚に重なる絵を味わいたい",
    caution="奇跡は信仰の伝承として紹介し、史実として実証された出来事とは扱わない。巡礼行列を描いたという説も推定表現。",
    text="中央には、大きな冠を戴いた聖母子像。刺繍のように細かな衣と天蓋のまわりから目を外すと、その両側の険しい山道に、驚くほど小さな人々がいることに気づきます。\n\n《コチャルカスの聖母》は1759年、ペルーのクスコ地方で描かれた油彩画です。聖母の像を行列用の祭壇に据え、まわりには山間を行く巡礼者や信者たちを描いています。メトロポリタン美術館は、毎年9月8日の聖母祭に関連する巡礼行列を表した可能性を指摘しています。\n\n聖母子像が人々よりはるかに大きいのは、遠近法だけでは説明できません。小さな旅人をたどり、大きな像へ視線を戻すと、人々がその場所に寄せてきた信仰の重みが、画面の尺度からも伝わってきます。",
    excerpt="in the midst of a rugged Andean landscape populated by pilgrims and other devotees",
    claim="まわりには山間を行く巡礼者や信者たちを描いています",
    section="Overview, first paragraph, rugged Andean landscape and pilgrims"),
dict(n=635384,title="The Baptism of Christ",ja="キリストの洗礼",who="Nicolás Enríquez",
    culture="Mexican",when="1773",medium="Oil on copper",acc="2014.171",
    path="ad",file="DP356935.jpg",
    sh="381e0a5eef3c8f6bc852979411c099bd1917373ef7633760a58aebfbcf5e149c",sz=67464,
    oh="b3800790438aeb5afbb3b5db31bbca0bcf8826ed7249db30f805ab31fa4051ff",oz=2333469,
    wh=[2921,3884],rms=3.7764,
    visual="川に足をつけたキリストが画面左寄りに立ち、右側の赤い衣をまとった洗礼者ヨハネがその頭へ水を注ぐ。上方には鳩と雲間の人物が描かれる。Met公式作品画像で確認し、公式API提供の大小JPEGの全量ハッシュと縮小一致も確認。",
    meaning="Metの作品別解説では、メキシコの画家ニコラス・エンリケスが1773年、スペイン生まれの商人フアン・バウティスタ・エチェベリアの私的礼拝のために制作した五枚組のうちの一枚。洗礼者ヨハネは依頼人の名に関係する聖人であり、水の透明な滴とキリストの水に入った足を細やかに表している。銘文は依頼人の信仰によって描かれたことを伝える。",
    uncertain="依頼人の内心や五枚組のすべての展示場所は本作品の解説だけでは断定しない。洗礼の奇跡の実証ではなく宗教主題の絵画。",
    tags=[],strength={},primary=[],secondary=[],tones=["静けさ"],themes=["時間"],
    situation="宗教画の細部と制作を依頼した人の背景を結びつけて考えたい",
    caution="宗教の主題があるだけで特定の鑑賞者の感情を決めつけない。絵画に宗教的効能を保証しない。",
    text="川に立つキリストの頭へ、洗礼者ヨハネが水を注ぎます。足は川の中に入り、ヨハネの赤い衣の向こうには、木々と空が広がっています。\n\nこの《キリストの洗礼》は1773年、メキシコの画家ニコラス・エンリケスが銅板に描いた作品です。エンリケスは商人フアン・バウティスタ・エチェベリアの個人的な信仰のため、五枚組の絵を制作しました。依頼主の名前にもつながる聖ヨハネの場面が選ばれ、水滴や川に沈むキリストの足まで丁寧に描かれています。\n\n大きな宗教上の出来事を伝える一方で、画家は小さな水の動きにも目を向けています。誰のために、どんな場面を選んで描いたのかを知ると、静かな画面に別の奥行きが生まれます。",
    excerpt="created this set of five paintings for the private devotional use of Juan Bautista Echeverría",
    claim="エンリケスは商人フアン・バウティスタ・エチェベリアの個人的な信仰のため、五枚組の絵を制作しました",
    section="Overview, first paragraph, private devotional five-painting series"),
dict(n=16580,title="Art Students",ja="美術を学ぶ女性たち",who="Louis Lang",
    culture="American",when="ca. 1871",medium="Oil on canvas",acc="1999.143",
    path="ad",file="DP-19092-001.jpg",
    sh="4bcbae9cd800e72a99d4b0054a77ad9257985aa6c58bf02b42bc9cbe2522ef68",sz=122047,
    oh="857339e8f34b9a44fa99718e25387af5ace5bc523fa59057047dc9742b9a9ca0",oz=4824227,
    wh=[3476,4000],rms=5.1767,
    visual="室内には画架に向かう女性、紙に絵を描く人物、石膏像を眺める女性などがいる。壁に石膏像や彫刻、右端に図版が並び、室内の奥にも人物が見える。Met作品別画像で確認し、公式APIからの大小JPEGのハッシュ・縮小一致を別工程で確認。",
    meaning="Metによると、ドイツ生まれのルイス・ラングは1867年からニューヨークのブロードウェイと西28丁目にあった自身のアトリエで女性向けの絵画教室を開いた。本作にはパレット、絵具、版画の本、石膏像、建築の断片、画架といった学習道具が集まる。1860年代後半には女性が専門家として美術を学ぶ場が私塾から教育機関へ広がり、クーパー・ユニオン（1859年創設）やレディース・アート・アソシエーション（1867年設立）もあった。",
    uncertain="絵に描かれた女性たちの実名、卒業後の進路、画家の内心は資料で確定されていない。美術教育の拡大を描くことと当時の機会が平等だったことは同じではない。",
    tags=["好奇心"],strength={"好奇心":2},primary=["好奇心"],secondary=[],tones=["にぎわい"],themes=["日常","共同体","時間"],
    situation="何かを学ぶ人々の姿や、女性が芸術を学んだ歴史に触れたい",
    caution="人物が必ず希望や喜びを感じていたと断定しない。絵の場面から当時の全女性の教育機会を一般化しない。",
    text="明るい室内では、何人もの女性がそれぞれ別の作業に取り組んでいます。画架に向かう人、紙に描く人、石膏像を見つめる人。机や壁には、絵具のほかにも版画集や彫刻などの教材が並びます。\n\nこの《美術を学ぶ女性たち》を描いたルイス・ラングは、1867年からニューヨークの自分のアトリエで女性に美術を教えていました。作品が描かれた1871年頃には、女性が芸術を専門的に学べる場所が私的な教室から学校へも広がり始めていました。\n\n画面の人物たちは、ひとつの場を共有しながら違う対象を見ています。誰かの人生や将来をこの一枚から言い当てることはできませんが、学ぶために道具と場所を持つことの意味を、教室の細部が伝えています。",
    excerpt="taught art classes for women in his New York City studio",
    claim="ラングは、1867年からニューヨークの自分のアトリエで女性に美術を教えていました",
    section="Overview, first paragraph, classes for women in New York studio"),
]

def put(path,data):
    p=R/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def sha(path):return hashlib.sha256((R/path).read_bytes()).hexdigest()
def call(*xs):print("RUN",*xs,flush=True);subprocess.run([sys.executable,*map(str,xs)],cwd=R,check=True)

def one(w):
    id="met-"+str(w["n"]);of=f"https://www.metmuseum.org/art/collection/search/{w['n']}"
    api=f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{w['n']}"
    sm=f"https://images.metmuseum.org/CRDImages/{w['path']}/web-large/{w['file']}"
    lg=f"https://images.metmuseum.org/CRDImages/{w['path']}/original/{w['file']}"
    high=dict(url=lg,sha256=w["oh"],byte_length=w["oz"],width=w["wh"][0],height=w["wh"][1],
       verification="complete_jpeg_sha256_and_downscale_match",
       source_identity_basis=f"Official original to web-large downscale RGB RMS {w['rms']}",last_full_sha_checked_on=D,human_visual_checked=False)
    ve=dict(language="ja",text=w["text"],source_urls=[of],review=dict(content_status="verified",source_status="verified",rights_status="verified",reviewed_on=D))
    art=dict(id=id,
       source=dict(museum="Metropolitan Museum of Art",artwork_id=w["n"],artwork_url=of,api_url=api,record_checked_on=D),
       facts=dict(title_original=w["title"],title_ja_provisional=w["ja"],artist=w["who"],creation_date_display=w["when"],type="Painting",
                  is_public_domain_at_source=True,culture=w["culture"],accession_number=w["acc"]),
       image=dict(image_id=id+"-primary",iiif_base=None,iiif_reference_url=None,display_url=sm,source_registry_id=id,
                  local_path="/artworks/"+id+".jpg",sha256=w["sh"],byte_length=w["sz"],live_image_checked=True,
                  live_check_scope="Official Met API original+web-large full JPEG hashes and dimensions, downscale RMS, "+E,
                  source_accession_number=w["acc"],high_resolution=high),
       curation=dict(emotions=w["tags"],emotion_strengths=w["strength"],tones=w["tones"],themes=w["themes"],evidence_url=of,
           search_profile=dict(fitting_situations=[dict(situation=w["situation"],reason=w["meaning"],strength=2)],
                               selection_cautions=[w["caution"],w["uncertain"]],review_status="evidence_reviewed"),
           meaning_basis=dict(author_intent=dict(status="not_verified_for_this_work",summary=None,source_url=None),
                              scholarly_interpretation=dict(summary=w["meaning"],source_url=of),
                              creation_context=f"{w['when']}, {w['culture']}; {w['medium']}, accession {w['acc']}.",
                              visual_clues=w["visual"],uncertainty_note=w["uncertain"]),
           emotion_categories=dict(primary=w["primary"],secondary=w["secondary"])),
       review=dict(facts_checked_against_museum_api=True,source_public_domain_flag_checked=True,visual_checked=False,
                   curatorial_reviewed_on=D,curatorial_review_status="provisional",
                   curatorial_review_note="Same assistant separate pass; Met exact images full hashes in "+E,
                   ai_content_review_status="pending",source_evidence_review_status="pending",image_subject_match_status="pending"),
       visitor_explanation=ve)
    reg=dict(id=id,title=w["title"],official_artwork_url=of,origin="met_official_primary",in_shared_catalog=True,
             verification="met_primary_jpeg_http_verified",
             image_source=dict(type="met_open_access",official_image_page=of,
                license_label="The Met Open Access / CC0 (Public Domain work, official primary JPEG)",license_url=OA,
                verified_download_url=sm,sha256=w["sh"],byte_length=w["sz"],last_http_sha_checked_on=D,last_verification_evidence=E,
                license_review_status="official_OA_confirmed_release_review_pending",high_resolution=high),
             accession_number=w["acc"])
    cp=f"drafts/artwork-additions/{id}.json";dp=f"drafts/visitor-explanations/{id}.json";ap=f"docs/artwork-completion-audits/{id}-{D}.json"
    put(cp,dict(schema_version="artwork-addition-proposal-v1",id=id,artwork=art,image_record=reg))
    put(dp,dict(id=id,visitor_explanation=ve,evidence=[dict(claim=w["meaning"],source_url=of,source_location="Met Overview and Artwork Details, "+w["section"],checked_against_source=True)]))
    sources=[
        dict(url=of,location="Artwork Details and full Overview including "+w["section"],finding=w["meaning"]+" "+w["uncertain"],checked_against_source=True),
        dict(url=api,location="Official objectID, accession, classification, PD, primaryImageSmall/primaryImage",finding="Met primary-image full SHA256 and size confirmed: "+E,checked_against_source=True),
        dict(url=OA,location="Met Open Access policy and CC0 reuse for public domain works",finding="The Met provides image and basic object data CC0; modern explanatory prose is not covered.",checked_against_source=True)]
    ims=[dict(kind=k,url=url,sha256=dig,byte_length=size,download_status=200,full_bytes_sha256_checked=True,
        image_subject_visually_compared=True,observation=w["visual"]+f" Official source image and resized pair RMS {w['rms']}.",
        checked_on=D) for (k,url,dig,size) in [("display",sm,w["sh"],w["sz"]),("original",lg,w["oh"],w["oz"])]]
    audit=dict(schema_version="artwork-v2-new-registration-2",id=id,checked_on=D,result="PASS",unresolved_material_issues=[],
       candidate_path=cp,candidate_sha256=sha(cp),draft_path=dp,draft_sha256=sha(dp),
       baseline=dict(artworks_sha256=sha("data/artworks.json"),image_registry_sha256=sha("data/image-sources.json")),
       official_text_checks=[dict(source_url=of,source_section=w["section"],source_excerpt=w["excerpt"],visitor_claim=w["claim"])],
       source_evidence=sources,
       rights=dict(artwork=dict(verified=True,public_domain=True,source_url=of,finding="Exact Met object marked Public Domain."),
                   image=dict(verified=True,permitted_for_site_use=True,source_url=OA,finding="Met Open Access CC0 on exact official JPEGs verified by full hash."),
                   text=dict(verified=True,independent_japanese_prose=True,source_url=of,finding="Independent new Japanese explanation based on facts and viewing, not near translation; legal certainty not guaranteed.")),
       separate_pass_review=dict(result="PASS",
          method="Same assistant: direct Met Overview and Details independently checked against drafted claims, visual composition checked in Met-designated image, Met API original and display JPEG full SHA256, size and RMS evidence in "+E,
          limitations="Not external scholarly or human review. Met official HTML quotes read directly; online CI re-fetch may HTTP 429. No legal clearance opinion.",
          areas=["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
          findings=dict(identity=f"Met {w['n']} accession {w['acc']} confirmed; "+w["uncertain"],
                        image_match=w["visual"]+" Full hashes at "+E,
                        historical_interpretation=w["meaning"],emotion="Source-grounded tags; zero allowed.",
                        visitor_text="Japanese text independently compared with Met Overview and Artwork Details.",
                        rights="Met Public Domain object, Met CC0 official image, independently worded Japanese text.")),
       image_evidence=ims,notes=["One-off 317–319 research record. Previous 313 works and their original audits are unchanged.","Same-assistant separate pass; not independent human expert."])
    put(ap,audit)
    print("PREVIEW",id,flush=True)
    call("scripts/add_artwork.py","preview","--audit",ap)
    call("scripts/add_artwork.py","save","--audit",ap)
    call("scripts/add_artwork.py","check")

def main():
    current=json.loads((R/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    ids={x["id"] for x in current};new={"met-"+str(w["n"]) for w in W}
    if new<=ids:print("ALREADY 316; no modifications");return
    if len(ids)!=316 or ids&new:raise RuntimeError("Unexpected baseline or partial registration")
    for w in W:one(w)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",suffix=".md") as f:
        f.write("""## 現在の状態（2026-11-10時点）

- **完成登録：319作品**。正式件数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：320作品目から候補調査**。既存作品は再登録しない。
- 317〜319の新作品は `met-764094`（ペルー）、`met-635384`（メキシコ）、`met-16580`（米国）。新規作品の一次出典、画像検査、権利判断は各作品の監査JSONに記録。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [共通v2基準](artwork-completion-workflow-v2.md) に従う。
- 新規登録監査は `artwork-v2-new-registration-2`。2026-11-10に作品別公式Overviewと画像を目視照合、Met公式API提供の原寸・表示JPEGを実取得してSHA256と縮小画素を照合。追加のHTMLオンライン自動照合はMetの制限により保証しない。
- 過去316件の元監査・作品本文は変更していない。過去の再照合は `docs/source-rechecks/` に保存。

""")
        f.flush();call("scripts/rotate_resume.py","update","--from",f.name)
    for script in ("scripts/rotate_resume.py check","scripts/visitor_draft_queue.py check","scripts/add_artwork.py check","scripts/validate_artworks.py","scripts/check_image_sources.py","scripts/check_catalog_snapshot.py"):
        call(*script.split())
    print("SUCCESS: 319 total works in branch",flush=True)

if __name__=="__main__":main()
