#!/usr/bin/env python3
"""Batch006 research, read-only. Verify AIC identity/PD painting and Commons JPEG image."""
import argparse,hashlib,json,re,time,urllib.parse,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
H={"User-Agent":"KaigaMuseumResearch/0.1 GitHub matumaruex/kaiga-data","Accept":"application/json,image/jpeg,*/*"}
def get(u):
 for k in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25) as r:
    if r.status!=200:raise ValueError(str(r.status))
    return r.read(7500000)
  except urllib.error.HTTPError as e:
   if k==2 or e.code not in (429,502,503,504):raise
   time.sleep(3*(k+1))
def api(q):
 return json.loads(get("https://api.artic.edu/api/v1/artworks/search?"+urllib.parse.urlencode({"q":q,"fields":"id,title,artist_title,date_display,artwork_type_title,is_public_domain,image_id,main_reference_number","limit":60})))["data"]
def commons(q):
 return json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"format":"json",**q})))
def norm(s):return re.sub(r"[^a-z0-9]+","",str(s).casefold())
def main():
 p=argparse.ArgumentParser();p.add_argument("--online",action="store_true");p.add_argument("--output",default="artifacts/batch006-research.json");a=p.parse_args()
 works=json.loads((ROOT/"data/candidates-batch-006.json").read_text(encoding="utf-8"))["works"]
 live={x["id"] for x in json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]}
 vocab=set(json.loads((ROOT/"data/emotions.json").read_text(encoding="utf-8"))["emotions"])
 for w in works:
  tags=w["emotion_categories"];alltags=tags["primary"]+tags["secondary"]
  assert 1<=len(tags["primary"])<=2 and len(tags["secondary"])<=2
  assert len(set(alltags))==len(alltags) and set(alltags)<=vocab
  assert w["meaning_basis"]["scholarly_interpretation"]["source_url"].startswith("https://")
 print("STRUCTURE OK "+str(len(works)),flush=True)
 if not a.online:return
 out=[]
 for i,w in enumerate(works,1):
  k=w["candidate_title"];expected=w["expected_accession_number"];rec={"candidate_title":k,"expected_accession_number":expected,"official_ok":False,"image_ok":False}
  try:
   results=api(k)
   matches=[x for x in results if norm(x.get("title"))==norm(k) and w["expected_artist"].split()[-1].casefold() in str(x.get("artist_title")).casefold()]
   if expected:matches=[x for x in matches if x.get("main_reference_number")==expected]
   if len(matches)!=1: raise ValueError("no unique painting: "+str([(x.get("id"),x.get("title"),x.get("artist_title"),x.get("main_reference_number")) for x in results[:6]]))
   x=matches[0]
   if x.get("artwork_type_title")!="Painting" or x.get("is_public_domain") is not True:raise ValueError("not public domain painting")
   if not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",x.get("image_id") or ""):raise ValueError("no image UUID")
   if "aic-"+str(x["id"]) in live:raise ValueError("already curated")
   rec.update(official_ok=True,official=x)
   print(f"[{i}/{len(works)}] AIC OK {k} => {x['id']} ACC={x.get('main_reference_number')}",flush=True)
  except Exception as e:
   rec["official_error"]=str(e)[:300]
   print(f"[{i}/{len(works)}] AIC PENDING {k}: {str(e)[:220]}",flush=True)
  if rec["official_ok"]:
   try:
    acc=rec["official"]["main_reference_number"]
    results=commons({"action":"query","list":"search","srnamespace":"6","srsearch":acc+" Art Institute of Chicago","srlimit":"20"}).get("query",{}).get("search",[])
    can=[v["title"] for v in results if acc in v["title"] and v["title"].lower().endswith((".jpg",".jpeg"))]
    if not can:
     results=commons({"action":"query","list":"search","srnamespace":"6","srsearch":acc,"srlimit":"30"}).get("query",{}).get("search",[])
     can=[v["title"] for v in results if acc in v["title"] and v["title"].lower().endswith((".jpg",".jpeg"))]
    if len(can)!=1:raise ValueError("unique accession image not found: "+str(can[:5]))
    title=can[0]
    z=commons({"action":"query","prop":"imageinfo","titles":title,"iiprop":"url|mime|extmetadata","iiurlwidth":"960"})
    info=next(iter(z["query"]["pages"].values()))["imageinfo"][0]
    if info.get("mime")!="image/jpeg":raise ValueError("not JPEG")
    license=info.get("extmetadata",{}).get("LicenseShortName",{}).get("value","")
    if not any(t in license.lower() for t in ["public domain","cc0","pd-old"]):raise ValueError("license not PD: "+license)
    u=info.get("thumburl") or info["url"];body=get(u)
    if body[:3]!=bytes((255,216,255)) or len(body)<1000:raise ValueError("JPEG signature")
    rec.update(image_ok=True,image={"file_title":title,"commons_page":"https://commons.wikimedia.org/wiki/"+urllib.parse.quote(title.replace(" ","_"),safe=":/()'"),"verified_download_url":u,"sha256":hashlib.sha256(body).hexdigest(),"byte_length":len(body),"license_label":license})
    print(f"[{i}/{len(works)}] IMAGE OK {k} {len(body)} B SHA256={rec['image']['sha256']} URL={u}",flush=True)
   except Exception as e:
    rec["image_error"]=str(e)[:240];print(f"[{i}/{len(works)}] IMAGE PENDING {k}: {str(e)[:240]}",flush=True)
  out.append(rec);time.sleep(0.5)
 target=ROOT/a.output;target.parent.mkdir(parents=True,exist_ok=True)
 summ={"checked":len(out),"official_passed":sum(x["official_ok"] for x in out),"image_passed":sum(x["image_ok"] for x in out),"both_passed":sum(x["official_ok"] and x["image_ok"] for x in out),"results":out}
 target.write_text(json.dumps(summ,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(f"SUMMARY API {summ['official_passed']}/{len(out)} IMAGE {summ['image_passed']}/{len(out)} BOTH {summ['both_passed']}/{len(out)}",flush=True)
if __name__=="__main__":main()
