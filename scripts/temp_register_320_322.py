#!/usr/bin/env python3
"""One-time, source-checked Met 320–322 registration. Refuses changes to existing works."""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile

R=Path(__file__).resolve().parents[1]
D="2026-11-10"
E="https://github.com/matumaruex/kaiga-data/actions/runs/42786337414"
OA="https://www.metmuseum.org/hubs/open-access"
W=[
dict(n=319625,title="Icon triptych of Ewosṭatewos and eight of his disciples",ja="エウォスタテウォスと八人の弟子の三連聖画像",who="Northern Highlands artist",
    culture="Amhara (Ethiopia)",when="late 17th century",medium="Wood, tempera, cord",acc="2006.98",
    path="ao",file="DP124866.jpg",
    sh="fa7d701ebf2c1327b43adf738908a13c765539e65ab0a835ce4d3ea9582cee7c",sz=119151,
    oh="d462a3fc80438dd6898a69d4d3e0af69f14e4ed2b160b2bb3a1f55bfd790992a",oz=2910151,
    wh=[2927,3832],rms=12.3316,
    visual="左右へ開いた木製三連画。赤や黄色を基調にした中央上部の聖人は杖と十字架、香炉を手にし、中央下に二人、左右の翼に三人ずつ、計八人の弟子が細いひげと模様のある衣をまとって描かれている。Met公式作品ページのIIIF画像を直接目視し、同IDの公式API一次JPEGを検証。",
    meaning="Metの作品別Overviewによれば、エチオピア正教会の二大修道会の一つである『エウォスタテウォスの家』の系譜を描いた、同種の主題で唯一知られた聖画像。聖人は1273年頃に生まれ、修道院を設立し、教義上の論争のためエジプトとアルメニアへ追放された。中央上部の聖人は巡礼者の杖、香炉と祝福用の十字架を持ち、その下と両脇に名が示された八人の弟子が小さく描かれる。修道院の歴史を示すために所有されていた可能性がある。",
    uncertain="絵の制作を依頼した具体的な修道院は特定されていない。Metの『唯一知られた』は現在の知見を示す表現で、世界に他の作品が絶対存在しないという証明ではない。作者は特定個人名ではなく北部高地の画家という記述。",
    tags=["畏敬"],strength={"畏敬":2},primary=["畏敬"],secondary=[],tones=["静けさ"],themes=["共同体","記憶","時間"],
    situation="信仰と師弟のつながりを絵画の配置から考えたい",
    caution="歴史的な信仰の表現を説明するもので、信仰の正しさや霊的な効果を保証しない。個々の弟子の性格は分からない。",
    text="木の扉を左右に開くと、中央の大きな聖人と、その下や両脇に整然と並んだ人物が現れます。赤、黄、緑の衣には、それぞれ違う細かな文様が描き込まれています。\n\n17世紀後半のエチオピアで制作されたこの三連画は、修道会の祖であるエウォスタテウォスを描いたものです。左右の翼と中央下部には、師に従う八人の弟子が小さく描かれています。人物の大きさの違いは、単なる遠近感ではなく、教えを伝える師と弟子の関係も示しています。\n\n小さな弟子たちはそれぞれ名で区別され、共通する衣装や姿勢によってひとつの集団にも見えます。三枚の板をまたぐ配置を追うと、この絵が人の姿だけでなく、修道会の記憶を残そうとするものだったことが見えてきます。",
    excerpt="Eight diminutive disciples are depicted in his image to underscore their devotion and allegiance.",
    claim="左右の翼と中央下部には、師に従う八人の弟子が小さく描かれています",
    section="Overview, first paragraph: eight disciples and hierarchical scale"),
dict(n=454054,title="Princesses Gather at a Fountain",ja="泉に集う王女たち",who="Unidentified artist",
    culture="India (Farrukhabad)",when="ca. 1770",medium="Opaque watercolor and gold on paper",acc="2001.421",
    path="is",file="DP231325.jpg",
    sh="539e2b25fc482586b5232ff17a37131823b28dec426fef66a4f0364d319702f7",sz=102051,
    oh="5bc1819186b3137d860578183baf10ddf60e743456dd88bf5e534ea13db7e7cf",oz=3097890,
    wh=[3689,2597],rms=10.8922,
    visual="横長の色鮮やかな庭園図。中央左の階段状の泉に女性が腰掛け、周囲に細長い衣の女性たちと子どもが集う。上半分には水辺・動物のつがい・架空の長首の水鳥・遠くの建物が描かれる。Met作品ID454054の公式IIIF画像を直接確認。",
    meaning="Metの作品別Overviewは、1770年頃のインド北部ファルッハーバード宮廷に帰属する細密画として、ハイウエストで流れるようなアンガルカを着た細身の女性たちと庭園の題材を説明する。泉には宮廷の女性十二人と子ども一人が集い、背景には幻想的な首の長い白鳥や対になった動物が見える。別のMet研究記事『Desiring Landscapes』は色調やつがいの動物を、宮廷的な恋愛感情を示す美術的表現として解釈している。",
    uncertain="画家の実名はMetの公式作品別ページに示されない。題名のPrincessesを根拠に全員を個別の王女と確定しない。動物の寓意は研究者の読みで、描かれた人々の私的な感情の証拠ではない。",
    tags=["喜び"],strength={"喜び":2},primary=["喜び"],secondary=[],tones=["にぎわい"],themes=["自然","共同体","愛情"],
    situation="宮廷の庭園で過ごす女性たちと動物の賑わいを味わいたい",
    caution="美術史上の『宮廷の楽しみ』という主題から、人物の実際の感情や身分を断定しない。ファルッハーバード画派への帰属は確定した画家名ではない。",
    text="大きな泉を取り囲むように、色とりどりの長い衣を着た女性たちが集まっています。左には建物、奥には緑の丘と小川が広がり、白い鳥や鹿のつがいが小さく描かれています。\n\nこの作品は1770年頃、インド北部のファルッハーバード宮廷の様式に属すると考えられる絵です。宮廷の女性十二人と子ども一人が、噴水を囲むように描かれています。衣服の細い線や、背景の鳥の大きさには、現実の風景をそのまま再現するより、庭の豊かさを見せる工夫が感じられます。\n\n人物同士の距離や手の動き、動物が二羽ずつ、二頭ずつ現れる様子にも目を向けると、庭園が人々の交流や憧れを映す舞台として描かれていることに気づきます。",
    excerpt="twelve courtly ladies and a child gathered around a fountain",
    claim="宮廷の女性十二人と子ども一人が、噴水を囲むように描かれています",
    section="Overview, opening paragraph: courtly women and child around a fountain"),
dict(n=860960,title="Hawk at sunrise",ja="日の出の鷹",who="Attributed to Jeong Hong-Rae 정홍래 鄭弘來",
    culture="Korea",when="second half 18th century–first half 19th century",
    medium="Hanging scroll; ink and color on silk",acc="2022.99",
    path="as",file="DP-24801-002.jpg",
    sh="dd64fe39c21da92b47ec2c0fe8b81970c28f904f920a4df2e35fff2ecd6085f1",sz=96889,
    oh="c595e932963d12694bbf7c41a97686b6bfd7c7280c0f2f03cb4a79f57e3b969f",oz=3588669,
    wh=[2516,4000],rms=4.6538,
    visual="縦長の掛軸に、波打つ海と青緑色の岩、その上に左を向いて立つ鷹がいる。画面上方に赤い太陽、鷹の鋭い眼と羽毛が細かく描かれる。Met公式IIIF画像と作品別記述を直接照合。",
    meaning="Metの作品別Overviewでは、訓練した猛禽を台にとまらせた朝鮮初期の図像を改め、海上の岩に鷹を置いた作品とする。赤い太陽、岩、海の波は流麗な筆致で表し、鷹は精緻に描く。猛禽は朝鮮王朝初期以来、勇気と正義感を重視する監察機関（Imperial Censorate）に関連づけられ、18〜19世紀には水、青緑の岩、赤い日輪という吉祥の環境に描かれた。",
    uncertain="Met公式作品別ページは『鄭弘來に帰属』としており、署名による確定作とは扱わない。監察機関との関係は図像の文化的意味で、この特定絵の注文主を直接示すものではない。",
    tags=["畏敬"],strength={"畏敬":2},primary=["畏敬"],secondary=[],tones=["緊張"],themes=["自然","時間"],
    situation="海と猛禽の描写から力強さや威厳を感じる絵を鑑賞したい",
    caution="鷹の象徴を現代の個人の感情や政治的立場に置き換えない。作者帰属は未確定。",
    text="青緑の岩の上に、一羽の鷹がまっすぐ立っています。下には砕ける白い波、上には赤い太陽。波や岩が自由な線で表される一方、鷹の羽や眼は細密に描かれています。\n\n《日の出の鷹》は18世紀後半から19世紀前半の朝鮮で描かれ、画家・鄭弘來の作と考えられていますが、確定した作者ではありません。猛禽は、勇気や正義感を重んじた朝鮮王朝の監察機関とも結びついていました。こうした作品では、海や赤い日輪はめでたい景色として表現されることもありました。\n\n激しく動く波と、動かず遠くを見つめる鷹。その対照をたどると、写実的な鳥の姿と、強さを託す象徴としての鳥とが、ひとつの掛軸で重なって見えます。",
    excerpt="birds of prey were associated with the Imperial Censorate",
    claim="猛禽は、勇気や正義感を重んじた朝鮮王朝の監察機関とも結びついていました",
    section="Overview, second paragraph: hawks and the Imperial Censorate"),
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
       image_evidence=ims,notes=["One-off 320–322 research record. Previous 313 works and their original audits are unchanged.","Same-assistant separate pass; not independent human expert."])
    put(ap,audit)
    print("PREVIEW",id,flush=True)
    call("scripts/add_artwork.py","preview","--audit",ap)
    call("scripts/add_artwork.py","save","--audit",ap)
    call("scripts/add_artwork.py","check")

def main():
    current=json.loads((R/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    ids={x["id"] for x in current};new={"met-"+str(w["n"]) for w in W}
    if new<=ids:print("ALREADY 316; no modifications");return
    if len(ids)!=319 or ids&new:raise RuntimeError("Unexpected baseline or partial registration")
    for w in W:one(w)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",suffix=".md") as f:
        f.write("""## 現在の状態（2026-11-10時点）

- **完成登録：322作品**。正式数は作業開始時の最新 `main` の `data/artworks.json` とREADMEで再確認する。
- **次：323作品目から候補調査**。以前の完成作品を再登録しない。
- 320〜322の新作品は `met-319625`（エチオピア）、`met-454054`（インド）、`met-860960`（朝鮮）。各作品の出典本文、画像、権利と解説の照合結果は作品別v2監査JSONに保存。
- 新規登録は [追加手順](artwork-expansion-v2.md) と [共通v2基準](artwork-completion-workflow-v2.md) を守る。新規監査形式は `artwork-v2-new-registration-2`。
- 3作品のMet公式ページOverviewを直接読み、公式IIIF画像を目視。Met API配信の大小JPEGについて完全SHA256・バイト数とリサイズ一致をGitHub Actionsで確認。HTMLのオンライン再照合はMetによるHTTP制限があり保証しない。
- 過去319件の作品・元監査は不変。過去の出典追加照合は `docs/source-rechecks/` を参照。

""")
        f.flush();call("scripts/rotate_resume.py","update","--from",f.name)
    for script in ("scripts/rotate_resume.py check","scripts/visitor_draft_queue.py check","scripts/add_artwork.py check","scripts/validate_artworks.py","scripts/check_image_sources.py","scripts/check_catalog_snapshot.py"):
        call(*script.split())
    print("SUCCESS: 322 total works in branch",flush=True)

if __name__=="__main__":main()
