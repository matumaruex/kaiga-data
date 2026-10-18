#!/usr/bin/env python3
"""第5群：所蔵番号を鍵としてシカゴ美術館APIとCommons画像を個別照合する。"""
import argparse, hashlib, json, re, time
import urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HEADERS={"User-Agent":"KaigaMuseumResearch/0.1 (collection provenance research; GitHub: matumaruex/kaiga-data)","Accept":"application/json,image/jpeg,*/*"}
def get(url):
    req=urllib.request.Request(url,headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=28) as response:
                if response.status!=200: raise ValueError("HTTP "+str(response.status))
                raw=response.read(7500000)
                if len(raw)>=7500000: raise ValueError("too large")
                return raw
        except urllib.error.HTTPError as e:
            if e.code not in (429,502,503,504) or attempt==2:raise
            time.sleep([3,7][attempt])
def api(endpoint,params):
    q=urllib.parse.urlencode(params)
    return json.loads(get("https://api.artic.edu/api/v1/"+endpoint+"?"+q))
def commons(params):
    return json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"format":"json",**params})))
def norm(v):return re.sub(r"[^a-z0-9]+","",str(v).casefold())
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--online",action="store_true")
    p.add_argument("--require-all",action="store_true")
    p.add_argument("--output",default="artifacts/batch005-research.json")
    p.add_argument("--only-accessions",default="",help="comma-separated subset for online retry")
    args=p.parse_args()
    works=json.loads((ROOT/"data/candidates-batch-005.json").read_text(encoding="utf-8"))["works"]
    existing=json.loads((ROOT/"data/artworks.json").read_text(encoding="utf-8"))["artworks"]
    vocab=set(json.loads((ROOT/"data/emotions.json").read_text(encoding="utf-8"))["emotions"])
    seen=set()
    for a in works:
        accession=a["accession_number"]
        assert re.fullmatch(r"[0-9]{4}[.][0-9]+",accession)
        assert accession not in seen
        seen.add(accession)
        assert len(a["emotion_categories"]["primary"]) in (1,2)
        assert len(a["emotion_categories"]["secondary"])<=2
        alltags=a["emotion_categories"]["primary"]+a["emotion_categories"]["secondary"]
        assert len(set(alltags))==len(alltags) and set(alltags)<=vocab
        assert a["source_catalogue_url"].startswith("https://")
    print(f"FORMAT OK {len(works)} research candidates, no automatic exhibition promotion",flush=True)
    if not args.online:return
    out=[]
    selected={x.strip() for x in args.only_accessions.split(",") if x.strip()}
    for index,a in enumerate(works,1):
        if selected and a["accession_number"] not in selected: continue
        x={"accession":a["accession_number"],"title_expected":a["expected_title"],"official_ok":False,"commons_ok":False}
        accession=a["accession_number"]
        try:
            matches=api("artworks/search",{"q":a["expected_title"],"fields":"id,title,artist_title,date_display,artwork_type_title,is_public_domain,image_id,main_reference_number","limit":50}).get("data",[])
            options=[m for m in matches if str(m.get("main_reference_number"))==accession]
            if len(options)!=1:
                # Search is relevance-ranked; try reference number directly.
                r=api("artworks/search",{"q":accession,"fields":"id,title,artist_title,date_display,artwork_type_title,is_public_domain,image_id,main_reference_number","limit":50}).get("data",[])
                options=[m for m in r if str(m.get("main_reference_number"))==accession]
            if len(options)!=1:raise ValueError(f"expected exactly one accession match; got {len(options)}; title candidates="+str([(m.get("id"),m.get("title"),m.get("main_reference_number")) for m in matches[:4]]))
            obj=options[0]
            if obj.get("is_public_domain") is not True or obj.get("artwork_type_title")!="Painting":raise ValueError("not PD painting")
            if not norm(a["expected_artist"].split()[-1]) in norm(obj.get("artist_title")):raise ValueError("artist mismatch")
            if not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",obj.get("image_id") or ""):raise ValueError("missing image ID")
            x["official_ok"]=True
            x["official"]={k:obj.get(k) for k in ("id","title","artist_title","date_display","artwork_type_title","is_public_domain","image_id","main_reference_number")}
            print(f"[{index}/{len(works)}] AIC OK accession={accession} id={obj['id']} title={obj['title']} artist={obj['artist_title']}",flush=True)
        except Exception as e:
            x["official_error"]=type(e).__name__+": "+str(e)[:240]
            print(f"[{index}/{len(works)}] AIC PENDING {accession}: {x['official_error']}",flush=True)
        try:
            explicit=a.get("manual_commons_file_title")
            if explicit:
                title=explicit
            else:
                results=commons({"action":"query","list":"search","srnamespace":"6","srsearch":accession+" Art Institute of Chicago","srlimit":"15"}).get("query",{}).get("search",[])
                good=[y for y in results if accession in y.get("title","") and "Art Institute of Chicago" in y.get("title","").replace("_"," ") and y.get("title","").endswith((".jpg",".jpeg",".JPG"))]
                if not good:
                    results=commons({"action":"query","list":"search","srnamespace":"6","srsearch":accession,"srlimit":"20"}).get("query",{}).get("search",[])
                    good=[y for y in results if accession in y.get("title","") and y.get("title","").lower().endswith((".jpg",".jpeg"))]
                if len(good)!=1:raise ValueError("Commons accession matches "+str([z["title"] for z in good[:8]]))
                title=good[0]["title"]
            pages=commons({"action":"query","prop":"imageinfo","titles":title,"iiprop":"url|size|mime|extmetadata","iiurlwidth":"960"})["query"]["pages"]
            page=next(iter(pages.values()))
            info=page["imageinfo"][0]
            if info["mime"]!="image/jpeg":raise ValueError("image is not jpeg")
            lic=info.get("extmetadata",{}).get("LicenseShortName",{}).get("value","")
            if "public domain" not in lic.lower() and lic.lower() not in ("cc0","pd-old"):raise ValueError("license not clearly public domain: "+lic)
            url=info.get("thumburl") or info["url"]
            raw=get(url)
            if len(raw)<1000 or raw[:3]!=bytes((255,216,255)):raise ValueError("jpeg signature invalid")
            if a["expected_artist"].split()[-1].casefold() not in urllib.parse.unquote(title).casefold() and not a.get("manual_commons_accession_verified_by"):raise ValueError("artist not in Commons file title")
            x["commons_ok"]=True
            x["image"]={"file_title":title,"commons_page":"https://commons.wikimedia.org/wiki/"+urllib.parse.quote(title.replace(" ","_"),safe=":/()'"),"verified_download_url":url,"sha256":hashlib.sha256(raw).hexdigest(),"byte_length":len(raw),"license_label":lic}
            print(f"[{index}/{len(works)}] IMAGE OK accession={accession} {title} SHA256={x['image']['sha256']} {len(raw)}B",flush=True)
        except Exception as e:
            x["image_error"]=type(e).__name__+": "+str(e)[:240]
            print(f"[{index}/{len(works)}] IMAGE PENDING {accession}: {x['image_error']}",flush=True)
        out.append(x);time.sleep(1)
    result={"date":"2026-10-18","checked":len(out),"official_passed":sum(x["official_ok"] for x in out),"images_passed":sum(x["commons_ok"] for x in out),"both_passed":sum(x["official_ok"] and x["commons_ok"] for x in out),"results":out}
    output=ROOT/args.output
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+chr(10),encoding="utf-8")
    print(f"SUMMARY: API {result['official_passed']}/{len(out)} CommonsJPEG {result['images_passed']}/{len(out)} BOTH {result['both_passed']}/{len(out)}",flush=True)
    if args.require_all and result["both_passed"]!=len(out):raise SystemExit(1)
if __name__=="__main__":main()
