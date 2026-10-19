#!/usr/bin/env python3
"""Find new Met artwork candidates. Read-only research; DOES NOT register candidates."""
import concurrent.futures
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
api="https://collectionapi.metmuseum.org/public/collection/v1"
HEAD={"User-Agent":"KaigaData-CollectionResearch/0.4 (matumaruex/kaiga-data)","Accept":"application/json"}
queries=[
(11,"autumn"),(11,"winter"),(11,"snow"),(11,"storm"),(11,"sunrise"),(11,"night"),(11,"moonlight"),
(11,"garden"),(11,"flowers"),(11,"child"),(11,"mother"),(11,"family"),(11,"sisters"),(11,"letter"),
(11,"departure"),(11,"farewell"),(11,"mourning"),(11,"lamentation"),(11,"saint"),(11,"magdalen"),
(11,"joy"),(11,"dance"),(11,"music"),(11,"banquet"),(11,"festival"),(11,"traveler"),(11,"harvest"),
(11,"farm"),(11,"village"),(11,"bridge"),(11,"road"),(11,"river"),(11,"sea"),(11,"horse"),(11,"dog"),
(11,"sleep"),(11,"prayer"),(11,"self-portrait"),(11,"interior"),(11,"reading"),(11,"hope"),
(1,"landscape"),(1,"mother"),(1,"child"),(1,"evening"),(1,"river"),(1,"winter"),(1,"home"),
(1,"school"),(1,"portrait"),(1,"family"),(1,"war"),(1,"mountain"),(1,"harvest"),
(6,"mountain"),(6,"river"),(6,"lotus"),(6,"moon"),(6,"bird"),(6,"scholar"),(6,"autumn"),
(6,"snow"),(6,"friendship"),(6,"farewell"),(6,"Buddha"),(6,"pilgrimage"),(6,"plum"),
(14,"lovers"),(14,"king"),(14,"garden"),(14,"music"),(14,"battle"),(14,"prayer"),(14,"night"),
]
def get_json(url):
    err=None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=24) as r:return json.load(r)
        except Exception as e:
            err=e;time.sleep(1+attempt*2)
    raise err
def lookup(item):
    dept,q=item
    query=urllib.parse.urlencode({"hasImages":"true","departmentId":dept,"q":q})
    try:
        payload=get_json(f"https://collectionapi.metmuseum.org/public/collection/v1.1/search?{query}")
        return (item,(payload.get("objectIDs") or [])[:12])
    except Exception as exc:
        return (item,{"error":str(exc)[:150]})
def record(ident):
    try:
        x=get_json(f"{api}/objects/{ident}")
        return x
    except Exception:
        return None
def main():
    exclude={int(x["source"]["artwork_id"]) for x in json.loads((ROOT/"data/artworks.json").read_text("utf-8"))["artworks"] if x["id"].startswith("met-")}
    already=set()
    info=[]
    q_results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        found=list(pool.map(lookup,queries))
    oid=[]
    for query,ids in found:
        q_results.append({"department":query[0],"query":query[1],"hits":len(ids) if isinstance(ids,list) else ids})
        if isinstance(ids,list):
            for i in ids:
                if i not in already and i not in exclude:already.add(i);oid.append(i)
    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as pool:
        objs=list(pool.map(record,oid))
    for x in objs:
        if not x:continue
        typ=(x.get("classification") or "").lower()
        if not(x.get("isPublicDomain") is True and x.get("primaryImageSmall") and (typ=="paintings" or (not typ and x.get("objectName")=="Painting" and "oil on" in (x.get("medium") or "").lower()))):continue
        info.append({"id":x["objectID"],"title":x.get("title"),"artist":x.get("artistDisplayName") or "Unidentified artist","date":x.get("objectDate"),"accession":x.get("accessionNumber"),"department":x.get("department"),"culture":x.get("culture"),"objectName":x.get("objectName"),"classification":x.get("classification"),"medium":x.get("medium"),"url":x.get("objectURL"),"primaryImageSmall":x.get("primaryImageSmall")})
    path=ROOT/"artifacts"/"batch019-discovery.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"results":info,"queries":q_results,"sampled_api_objects":len(oid),"eligible":len(info)},ensure_ascii=False,indent=2)+"\n","utf-8")
    print("DISCOVERY",len(queries),"queries",len(oid),"unique looked up",len(info),"eligible",flush=True)
    for i,x in enumerate(info):
        print(f'CAND {i+1:03} {x["id"]} | {x["title"]} | {x["artist"]} | {x["department"]} | {x["date"]}',flush=True)
if __name__=="__main__":main()
