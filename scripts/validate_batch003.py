#!/usr/bin/env python3
"""第3群の候補：形式・既存画像・（オプションで）現行シカゴ公式APIの照合。
APIに接続できない場合は確認成功とみなさず、レポートに理由を残す。
"""
import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("--online", action="store_true")
    arg.add_argument("--require-all", action="store_true")
    args = arg.parse_args()
    candidates = json.loads((ROOT / "data/candidates-batch-003.json").read_text(encoding="utf-8"))["works"]
    live = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    vocab = json.loads((ROOT / "data/emotions.json").read_text(encoding="utf-8"))
    images = json.loads((ROOT / "data/image-sources.json").read_text(encoding="utf-8"))["records"]
    old = {x["id"] for x in live}
    registry = {x["id"]: x for x in images}
    seen, problems = set(), []
    for art in candidates:
        id_ = art["id"]
        source = art["source"]
        if id_ in seen or id_ in old or id_ != "aic-" + str(source["artwork_id"]):
            problems.append(id_ + ": duplicated or invalid ID")
        seen.add(id_)
        image = registry.get(id_)
        if image is None:
            problems.append(id_ + ": no image registry record")
        elif image["image_source"]["sha256"] != art["image"]["sha256_verified"]:
            problems.append(id_ + ": image digest disagrees with registry")
        if art["source"]["official_metadata_status"] != "pending_recheck_2026_10_18":
            problems.append(id_ + ": metadata must remain pending before online check")
        if art["review"]["status"] != "candidate_meaning_drafted_metadata_live_check_pending":
            problems.append(id_ + ": invalid candidate status")
        if art["review"]["human_approved"] is not False:
            problems.append(id_ + ": falsely marked approved")
        tags = art["emotion_categories"]
        if not 1 <= len(tags["primary"]) <= 2 or len(tags["secondary"]) > 2:
            problems.append(id_ + ": tag limits")
        if len(set(tags["primary"] + tags["secondary"])) != len(tags["primary"] + tags["secondary"]):
            problems.append(id_ + ": duplicate tag")
        if any(tag not in vocab["emotions"] for tag in tags["primary"] + tags["secondary"]):
            problems.append(id_ + ": unknown emotion tag")
        meaning = art["meaning_basis"]
        a = meaning["author_intent"]
        if a["status"] == "not_verified_for_this_work":
            if a["summary"] is not None or a["source_url"] is not None:
                problems.append(id_ + ": unsupported author statement")
        elif a["status"] not in ("related_motif_or_series", "related_artistic_program") or not a["source_url"]:
            problems.append(id_ + ": invalid author statement status")
        if not meaning["scholarly_interpretation"]["source_url"].startswith("https://"):
            problems.append(id_ + ": no scholarly URL")
    if problems:
        print("FORMAT ERROR: " + "; ".join(problems))
        raise SystemExit(1)
    print(f"STRUCTURE OK: {len(candidates)} candidates; existing verified image sources matched. No exhibition promotion.", flush=True)
    if not args.online:
        return
    records=[]
    for art in candidates:
        src=art["source"]
        id_=src["artwork_id"]
        report={"id":art["id"],"success":False}
        try:
            url=f"https://api.artic.edu/api/v1/artworks/{id_}?fields=id,title,artist_title,date_display,artwork_type_title,image_id,is_public_domain"
            req=urllib.request.Request(url,headers={"User-Agent":"KaigaMuseumResearch/0.1 (source verification; GitHub matumaruex/kaiga-data)","Accept":"application/json"})
            with urllib.request.urlopen(req,timeout=24) as r:
                j=json.load(r)["data"]
            assert j.get("id")==id_, "wrong artwork ID"
            assert j.get("title")==art["facts_provisional"]["title"], "title mismatch"
            assert str(j.get("artwork_type_title","")).lower()=="painting", "not a painting"
            assert j.get("is_public_domain") is True, "not PD in official API"
            assert re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",j.get("image_id") or ""), "missing image UUID"
            report.update(success=True,title=j["title"],artist=j.get("artist_title"),date=j.get("date_display"),image_id=j["image_id"],public_domain=True)
            print(f"OK {id_}: {j['title']} | {j.get('artist_title')} | {j.get('date_display')}",flush=True)
        except (urllib.error.URLError,TimeoutError,ValueError,KeyError,AssertionError) as e:
            report["error"]=str(e)[:180]
            print(f"NOT VERIFIED {id_}: {e}",flush=True)
        records.append(report)
    result={"checked":len(records),"passed":sum(x["success"] for x in records),"results":records}
    out=ROOT/"artifacts"/"batch003-api-check.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("SUMMARY: {}/{} API verified".format(result["passed"],result["checked"]),flush=True)
    if args.require_all and result["passed"]!=len(records):
        raise SystemExit(1)
if __name__=="__main__":
    main()
