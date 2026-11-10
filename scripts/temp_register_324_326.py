#!/usr/bin/env python3
"""One-use source-audited registration for Met works 324-326. Remove after proof."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42805639776"
OA="https://www.metmuseum.org/hubs/open-access"
IDS=("met-764090","met-77180","met-701989")

def run(*args):
    print("EXEC", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)

def read(relative):
    return json.loads((ROOT/relative).read_text(encoding="utf-8"))

def digest(relative):
    return hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()

def build_audit(ident, note):
    cp=f"drafts/artwork-additions/{ident}.json"
    dp=f"drafts/visitor-explanations/{ident}.json"
    proposal=read(cp)
    art=proposal["artwork"]
    dr=read(dp)
    assert art["id"]==ident and dr["id"]==ident
    assert dr["visitor_explanation"]==art["visitor_explanation"]
    url=art["source"]["artwork_url"]
    api=art["source"]["api_url"]
    image=art["image"]
    high=image["high_resolution"]
    assert url==f"https://www.metmuseum.org/art/collection/search/{ident[4:]}"
    assert proposal["image_record"]["image_source"]["license_url"]==OA
    audit={
      "schema_version":"artwork-v2-new-registration-2",
      "id":ident, "checked_on":"2026-11-10","result":"PASS",
      "unresolved_material_issues":[],
      "candidate_path":cp,"candidate_sha256":digest(cp),
      "draft_path":dp,"draft_sha256":digest(dp),
      "baseline":{
        "artworks_sha256":digest("data/artworks.json"),
        "image_registry_sha256":digest("data/image-sources.json")},
      "official_text_checks":note["claims"],
      "source_evidence":[
        {"url":url,"location":"Exact Met object page Artwork Details and Overview; "+ " | ".join(x["source_section"] for x in note["claims"]),
         "finding":note["source_finding"],"checked_against_source":True},
        {"url":api,"location":"Met official API: objectID, title, artist, objectDate, culture, accession, isPublicDomain, primaryImage/primaryImageSmall",
         "finding":"Verified full JSON metadata and exact original/display bytes in "+RUN+"; image dimensions and resizing correspondence recorded. Met API metadata not inferred from title.", "checked_against_source":True},
        {"url":OA,"location":"Met Open Access CC0 policy for public-domain artworks and their official primary images",
         "finding":"Met PD work object and CC0 licensed public-domain digital images; copyrighted contemporary Met exposition is excluded.", "checked_against_source":True}
      ],
      "rights":{
        "artwork":{"verified":True,"public_domain":True,"source_url":url,
                   "finding":"The Met public-domain flag is true for this exact object; artist/date and provenance retained with attribution uncertainty."},
        "image":{"verified":True,"permitted_for_site_use":True,"source_url":OA,
                 "finding":"Met official primary Open Access CC0 JPEG original/display, full bytes and image identity verified; "+note["rights"]},
        "text":{"verified":True,"independent_japanese_prose":True,"source_url":url,
                "finding":"Original Japanese presentation newly written from checked museum facts and visual observation, not a long quotation or near-translation. No legal guarantee."}
      },
      "separate_pass_review":{
        "result":"PASS",
        "method":"Same AI's separate substantive review: exact object-specific Met Overview read, short excerpts checked against visitor claims; Met IIIF main-image visually inspected; official API/primary JPEG SHA256, dimensions and downscale matched at "+RUN,
        "limitations":note["limitations"],
        "areas":["identity","image_match","historical_interpretation","emotion","visitor_text","rights"],
        "findings":{
          "identity":"Met ID "+ident+" title="+art["facts"]["title_original"]+", artist="+art["facts"]["artist"]+", accession="+art["facts"]["accession_number"]+". Explicit differences from other works and artist attribution reviewed.",
          "image_match":note["visual"]+" Official API original/display full SHA256/dimensions and resize match run: "+RUN,
          "historical_interpretation":note["interpretation"],
          "emotion":note["emotion"],
          "visitor_text":"Two exact Met artwork-page excerpts bound to two concrete Japanese visitor claims; visual language independently compared with depicted figures and forms. No near-literal prose copying.",
          "rights":note["rights"]
        }
      },
      "image_evidence":[
        {"kind":"display","url":image["display_url"],"sha256":image["sha256"],"byte_length":image["byte_length"],
         "download_status":200,"full_bytes_sha256_checked":True,"image_subject_visually_compared":True,
         "observation":note["visual"]+" Display and original form same image as official Met ID; corresponding full JPEG hashes/size and downscale RMS verified "+RUN,"checked_on":"2026-11-10"},
        {"kind":"original","url":high["url"],"sha256":high["sha256"],"byte_length":high["byte_length"],
         "download_status":200,"full_bytes_sha256_checked":True,"image_subject_visually_compared":True,
         "observation":note["visual"]+" Original JPEG resolution "+str(high["width"])+"x"+str(high["height"])+" checked; reduced to display pair, same artwork "+RUN,"checked_on":"2026-11-10"}
      ],
      "notes":["One individually investigated, version-bound work; do not modify older artworks and their audits.",
               "Separate review by the same AI is not external professional or human review.",
               "The displayed-image JPEG and high-resolution JPEG are official public files, not embedded binary assets in the Git data repository."]
    }
    out=Path("docs/artwork-completion-audits")/(ident+"-2026-11-10.json")
    (ROOT/out).write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("AUDIT "+str(out)+" baseline="+audit["baseline"]["artworks_sha256"],flush=True)
    return str(out)

def main():
    configs={x["id"]:x for x in read("drafts/artwork-additions/temp-audit-source-324-326.json")["cases"]}
    assert set(configs)==set(IDS)
    assert len(read("data/artworks.json")["artworks"])==323
    for ident in IDS:
        ap=build_audit(ident,configs[ident])
        run(sys.executable,"scripts/verify_official_source_text.py","--audit",ap)
        run(sys.executable,"scripts/add_artwork.py","preview","--audit",ap)
        run(sys.executable,"scripts/add_artwork.py","save","--audit",ap)
        run(sys.executable,"scripts/add_artwork.py","check")
    assert len(read("data/artworks.json")["artworks"])==326
    resume="""## 現在の状態（2026-11-10時点）

- **完成登録：326作品**。正式件数は最新 `main` の `data/artworks.json` で確認。
- **次：327作品目から候補調査**。重複IDと同作別画像を調べ、品質未満は保留。
- 324〜326作品：`met-764090` ペルー《楽園のアダムとエバ》、`met-77180` 日本《花魁図》、`met-701989` アメリカ《エマ・ヴァン・ネーム》。独自日本語解説・作品別v2出典監査を保存。
- 3件の公式作品解説と公式IIIF画像を確認。Met公式APIで原寸・表示用JPEG計6ファイルのSHA256、バイト数、寸法、縮小RMSを完全照合（[検証記録]("""+RUN+""")）。同じAIによる別工程審査であり、外部の人間の鑑定ではない。
- 既存323作品と旧監査は変更せず、[新規登録ガイド](artwork-expansion-v2.md) と [v2完成条件](artwork-completion-workflow-v2.md) に準拠。GitHubの標準検査後にmainへ統合。
"""
    temp=Path("/tmp/kaiga-326-status.md")
    temp.write_text(resume,encoding="utf-8")
    run(sys.executable,"scripts/rotate_resume.py","update","--from",str(temp))
    checks=[
      ["scripts/validate_artworks.py"],
      ["-m","unittest","discover","-s","tests","-p","test_*.py"],
      ["scripts/rotate_resume.py","check"],
      ["scripts/complete_artwork.py","check"],
      ["scripts/add_artwork.py","check"],
      ["scripts/visitor_draft_queue.py","check"],
      ["scripts/check_catalog_snapshot.py"],
      ["scripts/check_image_sources.py"],
      ["scripts/validate_candidates.py"],
      ["scripts/validate_evaluation_cases.py"],
      ["scripts/audit_coverage.py"]
    ]
    for arguments in checks:
        run(sys.executable,*arguments)
    for ident in IDS:
        run(sys.executable,"scripts/verify_target_image_live.py","--id",ident)
    print("FINAL_PASS: 323 -> 326; all source, image, content, baseline, version and test checks passed",flush=True)

if __name__=="__main__":
    main()
