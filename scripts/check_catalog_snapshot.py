#!/usr/bin/env python3
"""Guard the verified 2026-10-20 300-work museum catalog snapshot.

Fail closed on partial artwork/registry updates, accidental held-work
promotion, unexpected removals, stale README headline, or mislabeled painter
attribution. Bump EXPECTED_* deliberately when approving a catalog expansion.
This static audit does NOT claim human approval or live source availability.
"""
from collections import Counter
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARTWORKS = 300
EXPECTED_IMAGES = 301
EXPECTED_MET = 249
EXPECTED_AIC = 51
EXPECTED_HIGH_RES = 246
EXPECTED_HELD_IMAGES = {"aic-4575"}
CANONICAL_ARTISTS = {
    "Auguste Renoir": "Pierre-Auguste Renoir",
    "Pierre-Auguste Renoir": "Pierre-Auguste Renoir",
    "Edouard Manet": "Édouard Manet",
    "Édouard Manet": "Édouard Manet",
    "Paul Cezanne": "Paul Cézanne",
    "Paul Cézanne": "Paul Cézanne",
    "Rembrandt van Rijn": "Rembrandt van Rijn",
    "Domenico Theotokópoulos, called El Greco": "El Greco",
    "El Greco": "El Greco",
}
KNOWN_UNCERTAIN_ATTRIBUTIONS = {
    "met-437412": "Style of Rembrandt (Rembrandt van Rijn)",
    "met-57280": "School of Katsushika Hokusai",
}
SHA = re.compile(r"^[a-f0-9]{64}$")
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main():
    data = read("data/artworks.json")
    registry = read("data/image-sources.json")
    vocabulary = read("data/emotions.json")
    works = data["artworks"]
    entries = registry["records"]
    errors = []
    def require(condition, detail):
        if not condition:
            errors.append(detail)
    ids = [a["id"] for a in works]
    recids = [a["id"] for a in entries]
    require(len(works) == EXPECTED_ARTWORKS, f"Expected {EXPECTED_ARTWORKS} works, got {len(works)}")
    require(len(entries) == EXPECTED_IMAGES, f"Expected {EXPECTED_IMAGES} source records, got {len(entries)}")
    require(len(ids) == len(set(ids)), "Duplicate artwork IDs")
    require(len(recids) == len(set(recids)), "Duplicate image source IDs")
    require(Counter(k.split("-")[0] for k in ids) == {"aic": EXPECTED_AIC, "met": EXPECTED_MET}, "Museum totals differ")
    require(set(recids) - set(ids) == EXPECTED_HELD_IMAGES, "Orphaned image records changed")
    require(all(k in recids for k in ids), "Artworks missing image registry")
    byid = {r["id"]: r["image_source"] for r in entries}
    highcount = 0
    canonicalcount = 0
    for a in works:
        ident = a["id"]
        facts = a["facts"]
        image = a["image"]
        r = byid.get(ident)
        if r is None:
            continue
        for key in ("sha256", "byte_length"):
            require(image.get(key) == r.get(key), f"{ident}: historical image {key} mismatch")
        require(image["display_url"] in [r.get("verified_download_url"), r.get("download_url")],
                f"{ident}: registered image URL mismatched")
        require(SHA.fullmatch(image.get("sha256", "")) is not None, f"{ident}: invalid image sha")
        require(isinstance(image.get("byte_length"), int) and image["byte_length"] > 1000, f"{ident}: image byte length")
        require(image.get("live_image_checked") is True, f"{ident}: image validation flag")
        require(facts["is_public_domain_at_source"] is True, f"{ident}: not public domain at source")
        require(facts["type"] == "Painting", f"{ident}: non-Painting artwork")
        require(facts.get("artist") not in (None, ""), f"{ident}: blank artist")
        require(facts.get("title_original") not in (None, ""), f"{ident}: blank title")
        expected = CANONICAL_ARTISTS.get(facts["artist"])
        if expected is not None:
            require(facts.get("artist_canonical") == expected, f"{ident}: known spelling alias missing")
        if "artist_canonical" in facts:
            canonicalcount += 1
        if ident in KNOWN_UNCERTAIN_ATTRIBUTIONS:
            require(facts["artist"] == KNOWN_UNCERTAIN_ATTRIBUTIONS[ident],
                    f"{ident}: official School/Style attribution changed")
            require("artist_canonical" not in facts, f"{ident}: School/Style wrongly treated as direct author")
        high = image.get("high_resolution")
        highsource = r.get("high_resolution")
        require((high is None) == (highsource is None), f"{ident}: high resolution pairing mismatch")
        if high is not None and highsource is not None:
            highcount += 1
            for k in ("url", "sha256", "byte_length", "width", "height", "verification"):
                require(high.get(k) == highsource.get(k), f"{ident}: high resolution {k} mismatch")
            require(high["verification"] == "complete_jpeg_sha256_and_downscale_match",
                    f"{ident}: unverified high resolution promoted")
            require(high.get("human_visual_checked") is False,
                    f"{ident}: false claim of human visual approval")
        c = a["curation"]
        primary = c["emotion_categories"]["primary"]
        secondary = c["emotion_categories"]["secondary"]
        tags = primary + secondary
        require(len(primary) <= 2 and len(secondary) <= 2, f"{ident}: tag overflow")
        require(len(tags) == len(set(tags)) and set(tags) == set(c["emotions"]), f"{ident}: tag/index difference")
        require(all(t in vocabulary["emotions"] for t in tags), f"{ident}: invalid emotion")
        require(all(c["emotion_strengths"].get(t) in (2, 3) for t in primary), f"{ident}: primary strength wrong")
        require(all(c["emotion_strengths"].get(t) == 1 for t in secondary), f"{ident}: secondary strength wrong")
        require(bool(c["search_profile"]["summary_for_ai"]), f"{ident}: missing AI summary")
    require(highcount == EXPECTED_HIGH_RES, f"Expected {EXPECTED_HIGH_RES} high-res source records, got {highcount}")
    require(canonicalcount == 21, f"Expected 21 canonical artist records, got {canonicalcount}")
    for n in range(16, 23):
        batch = read(f"data/candidates-batch-{n:03}.json")
        for candidate in batch["works"]:
            ident = candidate["candidate_id"]
            status = candidate.get("registration_status", "")
            if status == "registered_provisional":
                require(ident in ids, f"Batch {n}: registered artwork missing: {ident}")
            elif status.startswith("held_"):
                require(ident not in ids, f"Batch {n}: held artwork was promoted without review: {ident}")
            else:
                require(False, f"Batch {n}: unexpected status {ident} = {status}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("**試験登録：300作品**" in readme[:1800], "README current 300 work summary is stale")
    require("画像台帳は**301件**" in readme[:1800], "README 301 source image summary is stale")
    if errors:
        print("FAIL: snapshot integrity", len(errors))
        for e in errors:
            print("-", e)
        raise SystemExit(1)
    print(f"PASS: {len(works)} artworks, {len(entries)} source records, {highcount} high-res, "
          f"{canonicalcount} canonical artist records, candidate batches 016-022 aligned.")
    print("Human visual inspection, curatorial correctness and live-host availability are NOT verified by this test.")

if __name__ == "__main__":
    main()
