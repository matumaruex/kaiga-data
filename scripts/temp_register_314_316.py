#!/usr/bin/env python3
"""One-time, source-checked Met 314–316 registration. Refuses changes to existing works."""
from pathlib import Path
import hashlib, json, subprocess, sys, tempfile

R=Path(__file__).resolve().parents[1]
D="2026-11-10"
E="https://github.com/matumaruex/kaiga-data/actions/runs/42781149191"
OA="https://www.metmuseum.org/hubs/open-access"
W=[
dict(n=453283,title="Laila and Majnun",ja="ライラとマジュヌーン",who="Unidentified artist",
    culture="Iran (attributed to Shiraz)",when="mid-18th century",medium="Oil on canvas",acc="1987.355.1",
    path="is",file="DT5774.jpg",
    sh="452537d036cadaedc0887ffe9a886632198a28ab76378dc2b375a55c320ca4ff",sz=123184,
    oh="200a07fc06540886bfeee48b54d1f24405ea23b9f345aef760db92f245b21934",oz=3397322,
    wh=[3417,3655],rms=6.6572,
    visual="上辺がアーチ状の画面。赤い衣のライラと痩せたマジュヌーンが向かい合い、兎・鹿・獅子などの動物が周囲にいる。Met番号を表示するCommonsの該当画像を目視照合。",
    meaning="Metは、本作が恋物語を題材とする室内装飾用八点組の一枚で、上部が壁龕にはまる形であると説明する。マジュヌーンは結婚の申し出を拒絶された後に荒野に入り動物たちと暮らす姿として描かれる。ライラの衣装はザンド朝時代の服装に近い。",
    uncertain="Metの制作地表記はシーラーズへの帰属で、作家名は公式APIに記載がない。登場人物の感情を作者自身の経験と同一視しない。",
    tags=["未練","孤独"],strength={"未練":3,"孤独":1},primary=["未練"],secondary=["孤独"],tones=["余韻"],themes=["愛情","他者との距離","自然"],
    situation="叶わない恋の物語を絵画から考えたい",
    caution="恋の結末や人物の内心を画面だけから断定しない。制作地は帰属表記。",
    text="上辺が弓なりの画面で、赤い衣の女性と痩せ細った青年が向かい合っています。足元には兎や鹿、獅子などの動物が集まり、静かながらも不思議な賑わいがあります。\n\nこの絵は18世紀半ば、イランのシーラーズに由来すると考えられる油彩画で、恋物語を題材に室内を飾った八点組の一枚でした。ライラの父から結婚を認められなかったマジュヌーンは、人里を離れ、動物たちに囲まれて暮らす青年として描かれています。\n\n赤い衣と細い体、向かい合う姿とその間の空間。悲恋の物語を知ってから眺めると、動物の穏やかさとは対照的に、人間同士の距離が浮かび上がります。",
    excerpt="it was part of a series of eight works made to decorate a room",
    claim="恋物語を題材に室内を飾った八点組の一枚でした",
    section="Overview, first paragraph: eight-panel room decoration"),
dict(n=860959,title="Gathering of Government Officials",ja="官人たちの集まり",who="Unidentified artist",
    culture="Korea",when="16th century",medium="Hanging scroll; ink on silk",acc="2022.98",
    path="as",file="DP-24854-002.jpg",
    sh="99797a2b5c8a541f7f0b4c45f4c34e025cb6f312b317561bdded5adf89599e98",sz=104293,
    oh="3b60bbe44b28528f38e96a83c384a3384410e13c18b521c0d04f0d10e9088194",oz=4594593,
    wh=[3000,4000],rms=3.9811,
    visual="掛軸に霧のかかる山水、下方の岩に集まる小さな人物、川の舟と対岸の道や村。Met公式画像と同作品の細部表示を目視照合。",
    meaning="Metは、朝鮮王朝の官人たちの会合を記録した契会図（gyehoedo）であると説明する。人物が下方の岩上に小さく描かれる。停泊した舟から来た可能性のある人々、近づく二人の官人、漁師、遠方の塔も記述される。",
    uncertain="具体的な会合の日時、参加者の氏名、個々の人物の心理は公開情報から確定できない。",
    tags=[],strength={},primary=[],secondary=[],tones=["静けさ"],themes=["共同体","自然","記憶"],
    situation="人物と広い山水の関係を古い朝鮮絵画で鑑賞したい",
    caution="集まりが楽しげだったといった感情を捏造しない。会合の参加者や日時を確定しない。",
    text="水辺の向こうに山並みが重なり、遠い峰は霧の中に溶けていきます。川には舟が浮かび、画面の下方、岩の上に小さな人びとの集まりが見えます。\n\nこれは16世紀朝鮮の作品で、官人たちの会合を記録する「契会図（けいかいず）」という絵画の一例です。集まりが主題なのに、人物は景色に比べて驚くほど小さく描かれています。所蔵館は、舟で到着した人がいた可能性や、岩陰から近づく二人の官人にも目を向けています。\n\n会話の内容は分かりません。けれど、集った人びとが広い山水の中の一点として残されたことで、行事の記録と風景を味わう楽しみが同じ画面に収まっています。",
    excerpt="the figures are diminutively situated on an outcrop in the lower center",
    claim="集まりが主題なのに、人物は景色に比べて驚くほど小さく描かれています",
    section="Overview, first paragraph: diminutive officials on an outcrop"),
dict(n=853239,title="Triad of the Medicine Master Buddha Yakushi (Bhaisajya Buddha)",ja="薬師三尊図",who="Unidentified artist",
    culture="Japan",when="17th or 18th century",
    medium="Hanging scroll; ink, color, metallic paint, and kirikane (cut gold) on silk",acc="2021.396.3",
    path="as",file="DP-21707-002.jpg",
    sh="4639edebe0748009ace1325fbe8c8cdf7ede02c22d0b115556f6d556a1e71555",sz=91183,
    oh="1f4061d200ba987900a01365feac1c00a45c53dce8c6ebe0e04ac3d27a75a9a9",oz=3038446,
    wh=[2187,4000],rms=4.4001,
    visual="中央に大きな金色の薬師如来、その左右に二菩薩、上には天蓋と細かな文様。Met公式ページの作品画像を目視照合。",
    meaning="Metは日本で彫刻として知られやすい薬師三尊を描いた珍しい絵画と説明する。中央の薬師如来は脇侍の日光・月光菩薩より大きく、薬壺と恐れを払う印相を示す。金色の肌は中国由来の図像伝統との関連がある。",
    uncertain="作者、制作を依頼した人物と具体的な祈願目的は特定されていない。",
    tags=["畏敬"],strength={"畏敬":2},primary=["畏敬"],secondary=[],tones=["静けさ"],themes=["時間"],
    situation="仏画の三尊構成と装飾表現をじっくり見たい",
    caution="薬師という名から医療的な効果を保証しない。鑑賞者の信仰を推定しない。",
    text="淡い金色の肌で大きく座る薬師如来。その左右に日光菩薩と月光菩薩が立ち、二尊が掲げる日と月が画面の両側に配されています。\n\nこの《薬師三尊図》は、17〜18世紀の日本で描かれた掛軸です。薬師如来は片手に小さな薬壺を持ち、もう一方の手を恐れを払う印相にしています。メトロポリタン美術館によると、この三尊の姿は日本では彫刻としてよく知られ、絵画としては比較的珍しい題材です。\n\n中央の大きな姿と、脇侍の細やかな装身具。金を使った文様や上部の天蓋まで目を移すと、仏への信仰が色や大きさ、整った配置に表れていることを感じられます。",
    excerpt="He cradles a small medicine jar in one hand",
    claim="薬師如来は片手に小さな薬壺を持ち、もう一方の手を恐れを払う印相にしています",
    section="Overview, second sentence on the medicine jar"),
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
       image_evidence=ims,notes=["One-off 314–316 research record. Previous 313 works and their original audits are unchanged.","Same-assistant separate pass; not independent human expert."])
    put(ap,audit)
    print("PREVIEW",id,flush=True)
    call("scripts/add_artwork.py","preview","--audit",ap)
    call("scripts/add_artwork.py","save","--audit",ap)
    call("scripts/add_artwork.py","check")

def main():
    current=json.loads((R/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    ids={x["id"] for x in current};new={"met-"+str(w["n"]) for w in W}
    if new<=ids:print("ALREADY 316; no modifications");return
    if len(ids)!=313 or ids&new:raise RuntimeError("Unexpected baseline or partial registration")
    for w in W:one(w)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",suffix=".md") as f:
        f.write("""## 現在の状態（2026-11-10時点）

- **完成登録：316作品**。正式件数は最新mainのデータとREADMEで再確認する。
- **次：317作品目から候補調査**。過去の完成作品は再登録しない。
- 314〜316の3作品は met-453283、met-860959、met-853239。根拠は作品別監査JSONに保存。
- 新規登録は追加手順 (artwork-expansion-v2.md) と品質基準 (artwork-completion-workflow-v2.md) を守る。
- 3作品の公式作品別解説は2026-11-10に直接読んで照合。Met公式画像の原寸と表示用JPEGは全量SHAと縮小画像比較をGitHub Actionsで確認。
- 過去313件の監査は変更せず、既存の補足公式解説照合は source-rechecks に保持。

""")
        f.flush();call("scripts/rotate_resume.py","update","--from",f.name)
    for script in ("scripts/rotate_resume.py check","scripts/visitor_draft_queue.py check","scripts/add_artwork.py check","scripts/validate_artworks.py","scripts/check_image_sources.py","scripts/check_catalog_snapshot.py"):
        call(*script.split())
    print("SUCCESS: 316 total works in branch",flush=True)

if __name__=="__main__":main()
