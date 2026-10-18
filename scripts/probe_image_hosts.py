#!/usr/bin/env python3
"""各美術館の公開サンプル画像の配信状況を軽く確認する（2件のみ）。"""
import urllib.error
import urllib.request

SAMPLES = {
    "Cleveland Museum of Art": "https://openaccess-cdn.clevelandart.org/1998.78.14/1998.78.14_web.jpg",
    "Metropolitan Museum of Art": "https://images.metmuseum.org/CRDImages/ep/web-large/DT1567.jpg",
}
success = []
for name, url in SAMPLES.items():
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "KaigaData-ImageSource-Check/0.1", "Accept": "image/jpeg"})
        with urllib.request.urlopen(request, timeout=20) as response:
            data = response.read(2048)
            mime = response.headers.get("Content-Type", "")
            if response.status != 200 or not data.startswith(bytes((0xFF, 0xD8, 0xFF))) or "image/jpeg" not in mime.lower():
                raise ValueError("応答は画像JPEGとして確認できなかった")
            print(f"PASS: {name} HTTP={response.status} MIME={mime}")
            success.append(name)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"FAIL: {name}: {type(exc).__name__}: {str(exc)[:130]}")
print(f"SUCCESS: {len(success)}/{len(SAMPLES)}")
if not success:
    raise SystemExit("すべての代替画像ホストにアクセスできない")
