#!/usr/bin/env python3
"""現在の美術館公式APIと画像配信のHTTP到達性を19作品について点検する。
画像の肉眼確認・アプリ表示・法的な利用可否の最終判断とは別。
候補を本登録へ自動昇格させず、レビュー用の結果JSONだけ保存する。
"""
import argparse
import datetime
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.artic.edu/api/v1/artworks/"
IIIF = "https://www.artic.edu/iiif/2"
FIELDS = "id,title,artist_title,artist_display,date_display,is_public_domain,artwork_type_title,image_id"
IMAGE_RE = re.compile(r"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
HEADERS = {"User-Agent": "KaigaData-Curation/0.2 (low-volume public-collection verification)", "Accept": "application/json"}
TIMEOUT = 20


def request_json(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.load(response)


def request_image(url):
    request = urllib.request.Request(url, headers={"User-Agent": HEADERS["User-Agent"], "Accept": "image/jpeg"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        content_type = response.headers.get("Content-Type", "")
        payload = response.read(3_000_000)
        if "image/jpeg" not in content_type.lower():
            raise ValueError("Content-TypeがJPEGではない: " + content_type)
        if len(payload) < 512 or not payload.startswith(b"\\xff\\xd8\\xff"):
            raise ValueError("JPEG画像の実データを確認できない")
        return {"content_type": content_type, "bytes_read": len(payload), "http_status": response.status}


def describe_exception(exc):
    if isinstance(exc, urllib.error.HTTPError):
        return "HTTP " + str(exc.code)
    return type(exc).__name__ + ": " + str(exc)[:130]


def verify_record(art, kind):
    art_id = int(art["source"]["artwork_id"])
    result = {
        "id": art["id"], "kind": kind, "metadata_ok": False, "image_http_ok": False,
        "official_title": None, "official_image_id": None, "official_image_url": None,
        "image_http": None, "problems": [], "warnings": []
    }
    url = API + str(art_id) + "?" + urllib.parse.urlencode({"fields": FIELDS})
    try:
        official = request_json(url)["data"]
        result["official_title"] = official.get("title")
        result["official_image_id"] = official.get("image_id")
        if official.get("id") != art_id:
            result["problems"].append("公式APIの作品IDが不一致")
        expected_title = art["facts"]["title_original"] if kind == "registered" else art["facts_from_museum_sample"]["title"]
        expected_artist = art["facts"]["artist"] if kind == "registered" else art["facts_from_museum_sample"]["artist"]
        if (official.get("title") or "").strip() != expected_title.strip():
            result["problems"].append("保存済みの作品名と現在の公式名が不一致")
        if official.get("artist_title") != expected_artist and expected_artist not in (official.get("artist_display") or ""):
            result["problems"].append("作者が保存済みの情報と一致しない")
        if (official.get("artwork_type_title") or "").lower() != "painting":
            result["problems"].append("公式分類がPaintingではない")
        if official.get("is_public_domain") is not True:
            result["problems"].append("現在の公式APIでPDと確認できない")
        iid = official.get("image_id") or ""
        if not IMAGE_RE.fullmatch(iid):
            result["problems"].append("公式画像IDがない、または形式が違う")
        if not official.get("date_display"):
            result["problems"].append("公式APIに制作年代の表示がない")
        if kind == "registered" and art["image"]["image_id"] != iid:
            result["problems"].append("登録された画像IDが現在の公式画像IDと違う")
        if kind == "candidate":
            historical = art.get("archived_api_metadata") or {}
            if historical.get("image_id_candidate") != iid:
                result["warnings"].append("過去の複製と現在の公式画像IDが違う（公式を優先して再審査）")
        if result["problems"]:
            return result
        result["metadata_ok"] = True
        result["official_image_url"] = f"{IIIF}/{iid}/full/843,/0/default.jpg"
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
        result["problems"].append("公式APIの取得失敗: " + describe_exception(exc))
        return result

    # 表示用と同じ公式IIIFサーバーで、軽量な画像を実際にダウンロードする。
    # 取得できたことと絵の内容・画像の権利・ブラウザ表示は別。
    thumb_url = f"{IIIF}/{result['official_image_id']}/full/400,/0/default.jpg"
    try:
        result["image_http"] = request_image(thumb_url)
        result["image_http_ok"] = True
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        result["problems"].append("公式IIIF画像の取得失敗: " + describe_exception(exc))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/live-artwork-check.json")
    parser.add_argument("--require-all", action="store_true")
    args = parser.parse_args()

    registered = json.loads((ROOT / "data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    candidates = json.loads((ROOT / "data/candidates-batch-002.json").read_text(encoding="utf-8"))["works"]
    results = []
    for index, (kind, art) in enumerate(
        [("registered", x) for x in registered] + [("candidate", x) for x in candidates], start=1
    ):
        item = verify_record(art, kind)
        results.append(item)
        status = "OK" if item["metadata_ok"] and item["image_http_ok"] else "PENDING"
        print(f"[{index}/{len(registered) + len(candidates)}] {status} {art['id']} | {item['official_title']} | image_id={item['official_image_id']}", flush=True)
        for issue in item["problems"]:
            print("  ISSUE:", issue, flush=True)
        for warning in item["warnings"]:
            print("  NOTE:", warning, flush=True)
        time.sleep(0.8)

    report = {
        "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "checks": "current_official_AIC_API_and_IIIF_JPEG_HTTP",
        "limitations": [
            "画像の内容を人間が見て検証したわけではない",
            "実際のアプリ上の画像表示は未検証",
            "公式PDフラグの確認は使用権全般についての法的保証ではない",
            "解釈や感情の妥当性はこのテストの対象外"
        ],
        "registered_count": len(registered),
        "candidate_count": len(candidates),
        "metadata_ok_count": sum(x["metadata_ok"] for x in results),
        "image_http_ok_count": sum(x["image_http_ok"] for x in results),
        "results": results
    }
    target = ROOT / args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(f"SUMMARY: metadata={report['metadata_ok_count']}/{len(results)}, IIIF_JPEG_HTTP={report['image_http_ok_count']}/{len(results)}", flush=True)
    print("Saved:", target.relative_to(ROOT), flush=True)
    if args.require_all and report["image_http_ok_count"] != len(results):
        raise SystemExit("公式APIまたは画像HTTPの確認に未完了作品があるため、オンラインチェックを不合格とする")


if __name__ == "__main__":
    main()
