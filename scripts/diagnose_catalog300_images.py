#!/usr/bin/env python3
"""Diagnose transient or changed source images after catalog-300 audit; read-only."""
import hashlib,json,time,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
db=json.loads((ROOT/"data/image-sources.json").read_text("utf-8"))
ids=["aic-81551","met-670902","met-823663"]
HEAD={"User-Agent":"KaigaData-SourceImageDiagnosis/0.7 (github.com/matumaruex/kaiga-data)","Accept":"image/jpeg"}
def once(url):
  for n in range(3):
    try:
      with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=30) as response:
        raw=response.read(6_000_000)
        return {"ok":response.status==200,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"mime":response.headers.get("Content-Type"),"jpeg":raw[:3]==bytes((255,216,255)) and raw[-2:]==bytes((255,217))}
    except urllib.error.HTTPError as e:
      if e.code not in (429,500,502,503,504) or n==2:return {"ok":False,"error":"HTTP "+str(e.code)}
      time.sleep(5*(n+1))
    except Exception as e:
      return {"ok":False,"error":type(e).__name__+": "+str(e)[:130]}
out=[]
for rid in ids:
 rec=next(x for x in db["records"] if x["id"]==rid)
 src=rec["image_source"]
 print("CHECKING",rid,flush=True)
 samples=[once(src["verified_download_url"])]
 if rid.startswith("met-"):time.sleep(3);samples.append(once(src["verified_download_url"]))
 out.append({"id":rid,"expected_sha256":src["sha256"],"expected_bytes":src["byte_length"],"samples":samples})
 print(json.dumps(out[-1],ensure_ascii=False),flush=True)
output=ROOT/"artifacts"/"diagnostic-300-images.json";output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps({"checked":len(out),"results":out},ensure_ascii=False,indent=2)+"\n","utf-8")
print("DIAGNOSTIC_300_END",flush=True)
