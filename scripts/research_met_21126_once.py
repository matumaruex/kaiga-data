#!/usr/bin/env python3
"""One-off evidence-backed generation for Met 21126; no arbitrary auto-selection."""
import copy
import datetime
import hashlib
import io
import json
from pathlib import Path
import urllib.request
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
ID = "met-21126"
DATE = "2026-11-10"
PAGE = "https://www.metmuseum.org/art/collection/search/21126"
PAIR = "https://www.metmuseum.org/art/collection/search/765285"
OA = "https://www.metmuseum.org/hubs/open-access"
API = "https://collectionapi.metmuseum.org/public/collection/v1/objects/21126"
COMMONS = "https://commons.wikimedia.org/wiki/File:Young_Husband-_First_Marketing_MET_DP355340.jpg"
REFERENCE_ID = "met-11122"
EXPECTED = {
    "web": {"sha256": "ec9e67c30cda9c3b3c54d643f61a41a4a3f78a21042c61c22e566a599c4a9fc5", "size": 94074, "width": 521, "height": 624},
    "original": {"sha256": "46f0b3ac82f6ad6240d5c2a93121090e95e4a6b9f2dc1b8fcc386bb918a73dcc", "size": 3223627, "width": 3229, "height": 3869},
}
HEADERS = {"User-Agent": "KaigaMuseumResearch/0.1 (source verification)", "Accept": "application/json,image/jpeg,*/*"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    return sha_bytes(path.read_bytes())


def download(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=90) as response:
        assert response.status == 200, response.status
        return response.read(14000000)


def validate_image(url, expected):
    contents = download(url)
    assert contents[:3] == b"\xff\xd8\xff", "not JPEG"
    assert len(contents) == expected["size"] and sha_bytes(contents) == expected["sha256"], "image bytes differ from original verification"
    im = Image.open(io.BytesIO(contents))
    im.verify()
    im = Image.open(io.BytesIO(contents))
    assert (im.width, im.height) == (expected["width"], expected["height"])
    return im


def main():
    works = read_json(ROOT / "data/artworks.json")["artworks"]
    recs = read_json(ROOT / "data/image-sources.json")["records"]
    assert len(works) == 300 and not any(r["id"] == ID for r in works) and not any(r["id"] == ID for r in recs)
    api = json.loads(download(API))
    assert api["objectID"] == 21126 and api["isPublicDomain"] is True
    assert api["title"] == "Young Husband: First Marketing"
    assert api["artistDisplayName"] == "Lilly Martin Spencer"
    assert api["artistEndDate"] == "1902" and api["objectDate"] == "1854"
    assert api["medium"] == "Oil on canvas" and api["accessionNumber"] == "2015.401"
    assert api["primaryImageSmall"] == "https://images.metmuseum.org/CRDImages/ad/web-large/DP355340.jpg"
    assert api["primaryImage"] == "https://images.metmuseum.org/CRDImages/ad/original/DP355340.jpg"
    web = validate_image(api["primaryImageSmall"], EXPECTED["web"])
    original = validate_image(api["primaryImage"], EXPECTED["original"])
    assert abs((web.width / web.height) - (original.width / original.height)) < 0.005
    thumb = original.convert("RGB").resize(web.size, Image.Resampling.LANCZOS)
    compare = ImageChops.difference(thumb, web.convert("RGB"))
    rms = sum(ImageStat.Stat(compare).rms) / 3
    assert rms < 40, f"web-large/original may not depict same picture: rms={rms}"
    print(f"Official JPEG full hashes verified (small and original); 521x624 vs 3229x3869; RMS={rms:.2f}")
    art = copy.deepcopy(next(a for a in works if a["id"] == REFERENCE_ID))
    registry = copy.deepcopy(next(a for a in recs if a["id"] == REFERENCE_ID))
    art.pop("completion", None)
    art["id"] = ID
    art["source"] = {
        "museum": "Metropolitan Museum of Art",
        "artwork_id": 21126,
        "artwork_url": PAGE,
        "api_url": API,
        "record_checked_on": DATE,
    }
    art["facts"] = {
        "title_original": "Young Husband: First Marketing",
        "title_ja_provisional": "若い夫、初めての買い物",
        "artist": "Lilly Martin Spencer",
        "creation_date_display": "1854",
        "type": "Painting",
        "is_public_domain_at_source": True,
        "culture": "United States",
        "accession_number": "2015.401",
    }
    high = {
        "url": api["primaryImage"],
        "sha256": EXPECTED["original"]["sha256"],
        "byte_length": EXPECTED["original"]["size"],
        "width": original.width,
        "height": original.height,
        "verification": "complete_jpeg_sha256_and_downscale_match",
        "source_identity_basis": "Met API primaryImage + same frame/dimensions and web-large pixel comparison",
        "last_full_sha_checked_on": DATE,
        "human_visual_checked": False,
    }
    art["image"] = {
        "image_id": ID + "-primary",
        "iiif_base": None,
        "iiif_reference_url": None,
        "display_url": api["primaryImageSmall"],
        "source_registry_id": ID,
        "local_path": f"/artworks/{ID}.jpg",
        "sha256": EXPECTED["web"]["sha256"],
        "byte_length": EXPECTED["web"]["size"],
        "live_image_checked": True,
        "live_check_scope": "Met API primaryImageSmall, exact JPEG bytes/SHA256; 2026-11-10 image correspondence compared to original and Commons Met DP355340 visual",
        "source_accession_number": "2015.401",
        "high_resolution": high,
    }
    art["curation"] = {
        "emotions": ["喜び"],
        "emotion_strengths": {"喜び": 2},
        "tones": ["にぎわい", "緊張"],
        "themes": ["日常", "他者との距離"],
        "evidence_url": PAGE,
        "search_profile": {
            "fitting_situations": [{
                "situation": "日々の小さな失敗を、他人の視線も含めたユーモアとして眺めたい",
                "reason": "買い物籠を持て余す夫と、傘の下の通行人を通じて、日常の不器用さを喜劇的に描いている。",
                "strength": 2,
            }],
            "selection_cautions": [
                "面白い失敗を扱うが、登場人物本人が喜んでいると決めない。喜びタグは鑑賞者への入口。",
                "Metの説明する19世紀の家事分担と世間体の問題を、作者本人の直接証言と混同しない。",
                "夫と妻を現代の価値観だけで評価せず、別作品との関係も所蔵館の解説の範囲にとどめる。",
            ],
            "review_status": "evidence_reviewed",
        },
        "meaning_basis": {
            "author_intent": {"status": "not_verified_for_this_work", "summary": None, "source_url": None},
            "scholarly_interpretation": {
                "summary": "Metは、買い物に不慣れな若い夫が食材を抱えて街路でよろめき、傍観者の視線にさらされる場面を、新婚の家事運営をめぐる当時の社会的な不安をユーモラスに示す風俗画と解説する。夫をモデルにした事実と、作者の個人的感情の推測は区別する。",
                "source_url": PAGE,
            },
            "creation_context": "米国で1854年に制作された油彩画。所蔵館はリリー・マーティン・スペンサー自身の夫がモデルであると説明する。同年の対作品《Young Wife: First Stew》では、夫が買った食材が妻の台所に移るとMetが記している。",
            "visual_clues": "黒い帽子と上着の男性が、卵や野菜の詰まった籠を抱え、手には食用の鳥をぶら下げて歩く。後方の傘の下の人物や道沿いの人々、濡れた石畳、階段が見える。",
            "uncertainty_note": "画中の若い夫の感情を断定しない。Metの解説は19世紀の家事と世間体の緊張を読み取るが、作者本人によるこの作品への直接的な制作意図の言葉までは確認できていない。",
        },
        "emotion_categories": {"primary": ["喜び"], "secondary": []},
    }
    art["review"] = {
        "facts_checked_against_museum_api": True,
        "source_public_domain_flag_checked": True,
        "visual_checked": False,
        "curatorial_reviewed_on": DATE,
        "curatorial_review_status": "provisional",
        "curatorial_review_note": "Met individual official explanation, companion painting, original and web JPEG hashes and imagery, Open Access policy reviewed; v2 completion audit separately bound. No independent human or different model reviewer.",
        "ai_content_review_status": "pending",
        "source_evidence_review_status": "pending",
        "image_subject_match_status": "pending",
    }
    visitor_text = (
        "雨に濡れた石畳を、黒い帽子の男性が食材でいっぱいの籠を抱えて進んでいます。"
        "籠からは卵や野菜がのぞき、片手には鳥がぶら下がっています。"
        "傘の下の通行人はその姿を面白がっているようです。"
        "目の前には階段。家まで無事に持ち帰るのも簡単ではなさそうです。\n\n"
        "この《若い夫、初めての買い物》を1854年に描いたリリー・マーティン・スペンサーは、"
        "自分の夫を買い物に苦戦する男性のモデルにしました。"
        "メトロポリタン美術館は、慣れない家事や人前での失敗を笑いに変えながら、"
        "新婚生活で家を切り盛りすることへの当時の不安を表した作品と説明しています。\n\n"
        "同じ年に描かれた対作品《Young Wife: First Stew》では、夫が持ち帰った食材が妻の台所に現れます。"
        "妻も料理に戸惑い、そばにいる手伝いの人物は不思議そうに見つめています。"
        "二枚の絵は、家事の分担にまつわるぎこちなさをそれぞれ別の場面から映し出します。"
        "登場人物が内心でどう感じたかまでは、画面だけで決めることはできません。"
    )
    visitor = {
        "language": "ja",
        "text": visitor_text,
        "source_urls": [PAGE, PAIR],
        "review": {
            "content_status": "verified",
            "source_status": "verified",
            "rights_status": "verified",
            "reviewed_on": DATE,
        },
    }
    art["visitor_explanation"] = visitor
    registry["id"] = ID
    registry["title"] = art["facts"]["title_original"]
    registry["official_artwork_url"] = PAGE
    registry["origin"] = "met_official_primary"
    registry["in_shared_catalog"] = True
    registry["verification"] = "met_primary_jpeg_http_verified"
    registry["image_source"] = {
        "type": "met_open_access",
        "official_image_page": PAGE,
        "license_label": "The Met Open Access / CC0 (work-level Public Domain, primary image)",
        "license_url": OA,
        "verified_download_url": api["primaryImageSmall"],
        "sha256": EXPECTED["web"]["sha256"],
        "byte_length": EXPECTED["web"]["size"],
        "last_http_sha_checked_on": DATE,
        "last_verification_evidence": "https://github.com/matumaruex/kaiga-data/actions/runs/42745645404",
        "license_review_status": "official_OA_confirmed_release_review_pending",
        "high_resolution": high,
    }
    registry["accession_number"] = "2015.401"

    draft_path = ROOT / f"drafts/visitor-explanations/{ID}.json"
    proposal_path = ROOT / f"drafts/artwork-additions/{ID}.json"
    audit_path = ROOT / f"docs/artwork-completion-audits/{ID}-{DATE}.json"
    save_json(draft_path, {
        "id": ID, "visitor_explanation": visitor,
        "evidence": [
            {
                "claim": "Met 21126はリリー・マーティン・スペンサーの1854年油彩《Young Husband: First Marketing》で、2015.401、PD。夫が買い物に失敗する日常の風俗画で、作者の夫がモデル。新婚夫婦と家事運営の社会的不安が読み取られている。",
                "source_url": PAGE,
                "source_location": "Met collection page, overview paragraphs and Artwork Details, Title/Artist/Date/Medium/Accession/PD",
                "checked_against_source": True,
            },
            {
                "claim": "同年1854年の対作品《Young Wife: First Stew》では、夫の買い物が妻の台所で料理に用いられ、妻が玉ねぎを剥き、手伝い人が見つめる。",
                "source_url": PAIR,
                "source_location": "Met companion work, introductory text, first paragraph under gallery number",
                "checked_against_source": True,
            },
        ],
    })
    save_json(proposal_path, {
        "schema_version": "artwork-addition-proposal-v1",
        "id": ID, "artwork": art, "image_record": registry,
    })
    evidence = [
        {
            "url": PAGE, "location": "Overview paragraphs and Artwork Details: title, artist, 1854, 2015.401, oil/canvas, public domain",
            "finding": "Specific Met object ID 21126, artist's spouse as sitter, comic public embarrassment, new-household social anxiety, public-domain indication",
            "checked_against_source": True,
        },
        {
            "url": PAIR, "location": "Overview paragraph: companion relationship and kitchen ingredients",
            "finding": "1854 companion work exists and depicts wife peeling onion and domestic awkwardness; not used as a registered image",
            "checked_against_source": True,
        },
        {
            "url": API, "location": "Met JSON object 21126 fields primaryImage/primaryImageSmall/isPublicDomain/accessionNumber",
            "finding": "Official object API confirms title, authorship, date, PD status, exact image URLs and accession",
            "checked_against_source": True,
        },
        {
            "url": OA, "location": "Open Access policy overview on CC0 and reuse of public-domain artwork images",
            "finding": "The Met makes qualifying PD artwork images available under CC0 for commercial and noncommercial reuse",
            "checked_against_source": True,
        },
        {
            "url": COMMONS, "location": "File summary / Met object accession 2015.401 / image DP355340 / thumbnail",
            "finding": "Independent public image page shows same Met painting ID and DP355340, matching the supplied web-large/original JPEG frame and subject",
            "checked_against_source": True,
        },
    ]
    observation = (
        "Met 21126 / DP355340 image: black hat and dark green coat on man, overloaded woven basket with "
        "eggs and greens, upside-down poultry on one side, laughing-looking person under umbrella on left, "
        "rain-wet stone roadway and steps at right. Compared Met object and Commons DP355340 picture. "
        "Original and web-large exact bytes verified by GitHub Actions; resized-image RMS under 40."
    )
    audit = {
        "schema_version": "artwork-v2-new-registration-1",
        "id": ID,
        "checked_on": DATE,
        "result": "PASS",
        "unresolved_material_issues": [],
        "candidate_path": str(proposal_path.relative_to(ROOT)),
        "candidate_sha256": file_sha(proposal_path),
        "draft_path": str(draft_path.relative_to(ROOT)),
        "draft_sha256": file_sha(draft_path),
        "baseline": {
            "artworks_sha256": file_sha(ROOT / "data/artworks.json"),
            "image_registry_sha256": file_sha(ROOT / "data/image-sources.json"),
        },
        "source_evidence": evidence,
        "rights": {
            "artwork": {
                "verified": True, "public_domain": True,
                "source_url": PAGE,
                "finding": "Met flags the specific 1854 painting as Public Domain and artist died in 1902. This refers to the artwork, not modern interpretive prose.",
            },
            "image": {
                "verified": True, "permitted_for_site_use": True,
                "source_url": OA,
                "finding": "Met Open Access / CC0 applies to the identified public-domain painting's official original and web-large primary JPEG; exact file hashes are recorded.",
            },
            "text": {
                "verified": True, "independent_japanese_prose": True,
                "source_url": PAGE,
                "finding": "Japanese visitor explanation was newly written and separately compared against cited museum interpretations; no passage or close translation of copyrighted explanatory prose reproduced. No legal guarantee implied.",
            },
        },
        "separate_pass_review": {
            "result": "PASS",
            "method": "Same assistant, second distinct review pass: independently re-opened Met 21126, Met 765285, Met Open Access and Commons DP355340, checked draft's identity, meaning, tag caution, visual claims and text against source locations. Image bytes/pixel resize verified by separate GitHub Actions run and this creation run.",
            "limitations": "No independent human or separate AI model; verified source image previews at reduced display resolution, while full source JPEGs received byte-level machine checks. A content review does not constitute individual legal advice.",
            "areas": ["identity", "image_match", "historical_interpretation", "emotion", "visitor_text", "rights"],
            "findings": {
                "identity": "Met objectID 21126 and accession 2015.401, not paired 765285; source API 21126 crosschecked.",
                "image_match": observation,
                "historical_interpretation": "Met work-specific essay frames shopping as domestic comedy in context of mid-19th-century expectations; pair essay confirms continuation but not author's private intent.",
                "emotion": "Primary 喜び strength2 is a viewer-facing entrance via the depicted humor; do not infer figures themselves are happy; no other unsupported tags.",
                "visitor_text": "Freely authored Japanese prose, factual scene and pair-work statements grounded in Met sources, avoids rhetorical forced reaction and unsupported inner feelings.",
                "rights": "Public-domain painting + separate CC0 JPEG image rights + independent prose, with distinct supporting sources.",
            },
        },
        "image_evidence": [
            {
                "kind": kind, "url": api["primaryImageSmall"] if kind == "display" else api["primaryImage"],
                "sha256": EXPECTED[kind]["sha256"],
                "byte_length": EXPECTED[kind]["size"],
                "download_status": 200,
                "full_bytes_sha256_checked": True,
                "image_subject_visually_compared": True,
                "observation": observation,
                "checked_on": DATE,
            }
            for kind in ("web", "original")
        ],
        "notes": [
            "Met API and exact JPEG download verified twice by distinct GitHub Actions runs; web/original image resize comparison checked in this run.",
            "Registered image pixels are not stored in the repository; the official URL and SHA256 are version-bound.",
            "No unrelated baseline records, semantics or legacy completion records should change."
        ],
    }
    audit["image_evidence"][0]["kind"] = "display"
    save_json(audit_path, audit)
    print("Prepared one candidate", ID, "draft", file_sha(draft_path), "proposal", file_sha(proposal_path))
    print("Unrelated artwork records are untouched until add_artwork.py save")


if __name__ == "__main__":
    main()
