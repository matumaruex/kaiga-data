#!/usr/bin/env python3
"""Read-only batch 021 discovery: selected themes across painting departments.
Search official 2026 v1.1 API, then inspect IDs against /v1/objects.
Never register artworks or infer artist emotion."""
import concurrent.futures, json, urllib.request, urllib.parse, urllib.error, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
API="https://collectionapi.metmuseum.org/public/collection"
HEAD={"User-Agent":"KaigaDataArtResearch/0.6 (github.com/matumaruex/kaiga-data)", "Accept":"application/json"}
SEARCH=[
(11,"grief"),(11,"mourning"),(11,"death"),(11,"shipwreck"),(11,"storm"),(11,"parting"),(11,"old age"),
(11,"tenderness"),(11,"family"),(11,"wedding"),(11,"birth"),(11,"sleeping"),(11,"music"),(11,"dance"),
(11,"moonlight"),(11,"sunset"),(11,"winter"),(11,"harvest"),(11,"night"),(11,"prayer"),
(1,"Civil War"),(1,"Native American"),(1,"homestead"),(1,"children"),(1,"river"),(1,"mountains"),(1,"sunset"),(1,"family"),
(6,"solitude"),(6,"travelers"),(6,"poetry"),(6,"moon"),(6,"waterfall"),(6,"spring"),(6,"Buddha"),(6,"mother"),(6,"tiger"),(6,"festival"),(6,"autumn"),(6,"funeral"),
(14,"love"),(14,"poetry"),(14,"king"),(14,"battle"),(14,"lovers"),(14,"night"),(14,"garden"),(14,"horse")]
def load(url,limit=1_300_000):
  for tries in range(4):
    try:
      req=urllib.request.Request(url,headers=HEAD)
      with urllib.request.urlopen(req,timeout=22) as r:
        body=r.read(limit+1)
        if len(body)>limit:raise ValueError("large response")
        return json.loads(body)
    except Exception as e:
      if tries==3:raise
      time.sleep(1+tries)
def query(pair):
  department,q=pair
  params=urllib.parse.urlencode({"hasImages":"true","departmentId":department,"q":q,"limit":35})
  try:
    data=load(API+"/v1.1/search?"+params)
    return (department,q, (data.get("objectIDs") or [])[:30],None)
  except Exception as e:
    return (department,q,[],str(e)[:100])
def get_obj(id):
  try: return load(API+"/v1/objects/"+str(id))
  except Exception:return None
def main():
  previous=json.loads((ROOT/"data/artworks.json").read_text("utf-8"))["artworks"]
  exclude={int(a["source"]["artwork_id"]) for a in previous if a["id"].startswith("met-")}
  for f in (ROOT/"data").glob("candidates-batch-*.json"):
    try:
      exclude.update(int(w["museum_object_id"]) for w in json.loads(f.read_text("utf-8")).get("works",[]) if w.get("museum_object_id"))
    except Exception: pass
  with concurrent.futures.ThreadPoolExecutor(max_workers=9) as pool: queries=list(pool.map(query,SEARCH))
  objectids=[]; seen=set()
  for d,q,ids,e in queries:
    for id in ids:
      if id not in seen and id not in exclude:
        seen.add(id);objectids.append(id)
  with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: obj=list(pool.map(get_obj,objectids))
  res=[]
  for x in obj:
    if not x or x.get("isPublicDomain") is not True or not x.get("primaryImageSmall"):continue
    klass=(x.get("classification") or "").lower()
    if klass not in ("painting","paintings"):continue
    res.append({"id":x["objectID"],"title":x.get("title"),"artist":x.get("artistDisplayName") or "Unidentified artist",
      "date":x.get("objectDate"),"medium":x.get("medium"),"objectName":x.get("objectName"),
      "accession":x.get("accessionNumber"),"department":x.get("department"),"culture":x.get("culture"),
      "url":x.get("objectURL"),"image":x.get("primaryImageSmall"),"tags":x.get("tags")})
  report={"queries":[{"department":d,"query":q,"returned":len(ids),"error":e} for d,q,ids,e in queries],
  "objectIDs_considered":len(objectids),"eligible":len(res),"results":res}
  out=ROOT/"artifacts"/"batch021-discovery.json";out.parent.mkdir(exist_ok=True)
  out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n","utf-8")
  print("DISCOVERY_021",len(queries),"queries",len(objectids),"objects",len(res),"eligible",flush=True)
  for x in res:print("CAND",x["id"],json.dumps([x["title"],x["artist"],x["date"],x["department"]],ensure_ascii=False),flush=True)
  for a in report["queries"]:
    if a["error"]:print("QUERY_ERROR",a,flush=True)
if __name__=="__main__":main()
