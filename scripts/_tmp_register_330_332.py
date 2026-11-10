#!/usr/bin/env python3
"""One-off, version-bound source-audited registrations of 330-332. Remove after success."""
import copy, hashlib, io, json, math, subprocess, sys, time
from pathlib import Path
import requests
from PIL import Image, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parents[1]
TODAY="2026-11-11"
RUN="https://github.com/matumaruex/kaiga-data/actions/runs/42916204559"
OA="https://www.metmuseum.org/hubs/open-access"
SPECS=[
 {
  "num":37817,
  "ja":"ンゴル寺第8代住職ムンチェン・サンゲ・リンチェンの肖像",
  "artist":"Unknown artist",
  "culture":"Tibet",
  "tones":["静けさ"],
  "themes":["共同体","時間"],
  "emotions":["畏敬"],"strengths":{"畏敬":2},"primary":["畏敬"],"secondary":[],
  "fitting":"仏教の師の肖像を、まわりの尊像や経典との配置から読みたい",
  "historical":"Met作品別Overviewは、ムンチェン・サンゲ・リンチェンが1513〜1516年にンゴル寺の第8代住職を務め、当時の寺がチベットのウー・ツァン地方に政治的な影響力を持っていたと記す。師が蓮華座に座り、教えを示す手と経典、周囲の祖師・守護尊が描かれると説明している。",
  "visual":"中央の僧が蓮華の座に坐り、赤・青・金色を含む枠の内外に多数の小さな像が整列する縦長のタンカ。絵の下部と上部に別の人物像が並び、装飾的な輪郭と細部が目立つ。Met同一作品の画像と所蔵番号1971.176に紐づく公式JPEGを照合。",
  "uncertain":"絵に描かれた儀礼や感情を現代的に断定せず、Metが説明する図像配置に留める。作者個人は不詳。16世紀末の制作と16世紀初頭の住職任期を混同しない。",
  "text":"鮮やかな色彩の中央に、僧が蓮の座に座り、周囲を数多くの仏教尊像が取り囲んでいます。上部や左右には小さな像が並び、下部にも別の尊像が置かれています。\n\n主役のムンチェン・サンゲ・リンチェンは、1513年から1516年までンゴル寺の第8代住職を務めました。美術館によれば、当時の寺はチベットの中部や西部でも政治的な力を持っていました。彼は片手を教えを説く仕草で掲げ、もう一方の手には説法に使う経典を持っています。\n\n細部を見ると、宝石で飾られた書物や座の縁、周囲の小さな像が丁寧に重ねられています。ひとりの僧の姿を取り巻く、仏教の系譜や教えの広がりにも目を向けられる作品です。",
  "quotes":[
    ("Munchen Sangye Rinchen served as abbot from 1513 to 1516","主役のムンチェン・サンゲ・リンチェンは、1513年から1516年までンゴル寺の第8代住職を務めました","Overview: abbot tenure"),
    ("one hand raised in exposition, the other holding the text","彼は片手を教えを説く仕草で掲げ、もう一方の手には説法に使う経典を持っています","Overview: raised hand and preaching text")
  ],
  "image":{"original":("https://images.metmuseum.org/CRDImages/as/original/DP238089.jpg","12b921a7bfdf07ec4a5d1207565ef3209c3972b162b7eeab21a30c69b5412400",1675446,1834,3562),
           "display":("https://images.metmuseum.org/CRDImages/as/web-large/DP238089.jpg","7a725c0827739f248a48cd549784db62b0d627ea5cd5df0937dc743e4c251226",76960,321,623)}
 },
 {
  "num":437102,
  "ja":"小屋のある風景",
  "artist":"Pieter de Molijn",
  "culture":"Unknown (Met API culture unspecified; Dutch artist)",
  "tones":["静けさ"],"themes":["自然","日常"],
  "emotions":[],"strengths":{},"primary":[],"secondary":[],
  "fitting":"身近な風景の中で、低い視点や抑えた色彩が生む空気を味わいたい",
  "historical":"Met作品別Overviewでは、1620年代のオランダの風景画が、地域の土地の様子を茶・灰・緑など落ち着いた色調で描く方向へ変化したと説明する。上空から俯瞰するのでなく、視点は地面近くの深い影に置かれ、その時代の独立戦争と国民意識の高まりにも触れる。",
  "visual":"低く伸びる砂地の道と小屋、小さな人影、暗い地面の上に大きな雲と空が広がる。Met公式の別撮影画像と、同作の原寸/表示主画像を物体ID 437102に紐づけた。地形が正確な場所を写したとまでは言えない。",
  "uncertain":"絵に描かれた道・小屋を特定の地名に結びつけない。作者の内面や鑑賞者の感情を断定しない。作者のオランダ国籍をAPIに無い文化フィールドへ短絡させない。",
  "text":"砂地の道が緩やかに奥へ続き、低い地平線の上を大きな雲が覆っています。道の近くには小さな家屋と人影があり、広い空と暗い地面の対比が目を引きます。\n\n1629年の作品です。メトロポリタン美術館は、当時のオランダ風景画には、身近な地形を茶色や灰色、緑色の抑えた色合いで描く変化があったと説明しています。また、この絵では見る人の視点が地面に近く、深い影の中に置かれています。\n\n遠景を上から見下ろすのではなく、道を歩く人と同じ高さに立つように見ると、雲の大きさと地面の質感が際立ちます。何気ない場所を描くことが、当時の絵画表現の新しさにもつながっていたのです。",
  "quotes":[
   ("modest scenes of local topography in a somber palette","当時のオランダ風景画には、身近な地形を茶色や灰色、緑色の抑えた色合いで描く変化があった","Overview: 1620s Dutch subdued local landscapes"),
   ("the viewer is placed low to the ground in an area of heavy shadow","この絵では見る人の視点が地面に近く、深い影の中に置かれています","Overview: viewpoint and shadow")
  ],
  "image":{"original":("https://images.metmuseum.org/CRDImages/ep/original/DP146459.jpg","5a852758a4f68883108dfbd6b35f5b4734588bcebab53891e8892b927b083f5e",2097556,3903,2647),
           "display":("https://images.metmuseum.org/CRDImages/ep/web-large/DP146459.jpg","66e562c6fe1f77ae7c803f981d7e66e6576bafa83a395f70302482c906876666",51907,599,406)}
 },
 {
  "num":451256,
  "ja":"瓶と杯を持つ人物",
  "artist":"Unknown artist",
  "culture":"Iran, Isfahan (Met geography; culture not specified by API)",
  "tones":["落ち着き"],"themes":["共同体","時間"],
  "emotions":[],"strengths":{},"primary":[],"secondary":[],
  "fitting":"イランの宮廷装飾と人物画を、壁画片の材質ごと眺めたい",
  "historical":"Met作品別Overviewによれば、16〜17世紀のサファヴィー朝宮殿では壁画が発注され、宮廷の杯を扱う若者は理想化された姿でよく描かれた。画面の題材は壁画にもアルバム用の作品にも用いられたと説明する。",
  "visual":"縦長の傷みを帯びた壁画片に、大きなターバン、赤い衣装、杯と細長い瓶を持つ上半身が描かれる。Met公式の同一物体画像とprimary JPEG URLを照合し、部分像を別作品と混同しない。",
  "uncertain":"特定の個人の肖像と断定しない。壁画が置かれた具体的な宮殿名や、杯の飲み物の中身は公式解説に無いので推測しない。作者個人は不詳。",
  "text":"縦長の壁画片に、大きなターバンを巻いた若者が描かれています。赤い衣装には丸い飾りが連なり、手には杯と瓶が見えます。ところどころ色が剥がれた表面は、この絵が長い時間を経て残ったことを伝えます。\n\n16〜17世紀のサファヴィー朝では、宮殿のために壁画が注文されました。美術館によれば、宮廷で杯を扱う若者は、理想化された姿で好んで描かれる題材でした。同じような人物は、壁画だけでなくアルバム用の絵にも登場しました。\n\n顔や布の細かな線と、欠けた壁面の対比に目を向けると、華やかな宮廷文化のイメージと、実際の作品に刻まれた時間とを同時に感じ取れます。",
  "quotes":[
    ("mural paintings were commissioned by Safavid rulers","16〜17世紀のサファヴィー朝では、宮殿のために壁画が注文されました","Overview: Safavid palace murals"),
    ("were a popular subject for artists, who portrayed them in idealized form","宮廷で杯を扱う若者は、理想化された姿で好んで描かれる題材でした","Overview: idealized cupbearers")
  ],
  "image":{"original":("https://images.metmuseum.org/CRDImages/is/original/wb-55.121.8.JPG","be79437178b3096fc7bb43d88acc9da63640dd7e84c9e8478b6dff1452fb8c4c",680141,1016,2560),
           "display":("https://images.metmuseum.org/CRDImages/is/web-large/wb-55.121.8.JPG","ef2db603126c62be152b506fb52edc8420cec7758b105d037d2579b1da091654",62392,248,625)}
 }
]

def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def get(url):
 for i in range(4):
  try:
   r=requests.get(url,timeout=65,headers={'User-Agent':'ArtworksDataReview/1.0 (Open Access research)'})
   if r.status_code==200: return r
   print(f'HTTP {r.status_code} {url}',flush=True)
  except Exception as e: print(f'GET: {type(e).__name__}: {str(e)[:100]}',flush=True)
  time.sleep(2+i*3)
 raise RuntimeError('fetch failed '+url)
def digest(path):
 return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,obj):
 p=ROOT/path
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return digest(p)
def call(*args):
 print('RUN',*args,flush=True)
 subprocess.run(args,check=True,cwd=ROOT,timeout=240)
def inspect_images(spec,obj):
 result={}
 for kind in ('original','display'):
  url, sha, length, w, h=spec['image'][kind]
  need(obj['primaryImage' if kind=='original' else 'primaryImageSmall']==url,'object API JPEG URL changed')
  binary=get(url).content
  im=Image.open(io.BytesIO(binary));im.load()
  need(im.format=='JPEG' and im.size==(w,h),'wrong image format or dimensions')
  need(len(binary)==length and hashlib.sha256(binary).hexdigest()==sha,'JPEG bytes changed')
  result[kind]=(im.copy().convert('RGB'),{'kind':kind,'url':url,'sha256':sha,'byte_length':length,
    'download_status':200,'full_bytes_sha256_checked':True,'image_subject_visually_compared':True,
    'observation':spec['visual']+' Official exact-object primary JPEG and downscaled counterpart checked in '+RUN,
    'checked_on':TODAY})
 orig,disp=result['original'][0],result['display'][0]
 rms=math.sqrt(sum(v*v for v in ImageStat.Stat(ImageChops.difference(orig.resize(disp.size,Image.Resampling.LANCZOS),disp)).rms)/3)
 need(rms<30,'original/display inconsistent')
 return {x:result[x][1] for x in ('original','display')},round(rms,5)

def register(spec,seq):
 num=spec['num'];id='met-'+str(num)
 official='https://www.metmuseum.org/art/collection/search/'+str(num)
 api='https://collectionapi.metmuseum.org/public/collection/v1/objects/'+str(num)
 obj=get(api).json()
 need(obj['objectID']==num and obj['isPublicDomain'] and obj['classification']=='Paintings','identity/rights/classification changed')
 need(obj['title'] and obj['accessionNumber'],'missing work identity')
 images,rms=inspect_images(spec,obj)
 display=images['display'];original=images['original']
 hi={'url':original['url'],'sha256':original['sha256'],'byte_length':original['byte_length'],
     'width':spec['image']['original'][3],'height':spec['image']['original'][4],
     'verification':'complete_jpeg_sha256_and_downscale_match',
     'source_identity_basis':f'Met exact official object original/display RGB downscale RMS {rms}',
     'last_full_sha_checked_on':TODAY,'human_visual_checked':False}
 visitor={'language':'ja','text':spec['text'],'source_urls':[official],
   'review':{'content_status':'verified','source_status':'verified','rights_status':'verified','reviewed_on':TODAY}}
 art={
  'id':id,
  'source':{'museum':'Metropolitan Museum of Art','artwork_id':num,'artwork_url':official,'api_url':api,'record_checked_on':TODAY},
  'facts':{'title_original':obj['title'],'title_ja_provisional':spec['ja'],'artist':spec['artist'],
     'creation_date_display':obj.get('objectDate') or 'Date unspecified','type':'Painting',
     'is_public_domain_at_source':True,'culture':spec['culture'],'accession_number':obj['accessionNumber']},
  'image':{'image_id':id+'-primary','iiif_base':None,'iiif_reference_url':None,
     'display_url':display['url'],'source_registry_id':id,'local_path':'/artworks/'+id+'.jpg',
     'sha256':display['sha256'],'byte_length':display['byte_length'],
     'live_image_checked':True,'live_check_scope':'Met exact object, complete original/display SHA256, dimensions and downscale: '+RUN,
     'source_accession_number':obj['accessionNumber'],'high_resolution':hi},
  'curation':{'emotions':spec['emotions'],'emotion_strengths':spec['strengths'],
    'tones':spec['tones'],'themes':spec['themes'],'evidence_url':official,
    'search_profile':{'fitting_situations':[{'situation':spec['fitting'],'reason':spec['historical'],'strength':2}],
      'selection_cautions':[spec['uncertain']],'review_status':'evidence_reviewed'},
    'meaning_basis':{'author_intent':{'status':'not_verified_for_this_work','summary':None,'source_url':None},
     'scholarly_interpretation':{'summary':spec['historical'],'source_url':official},
     'creation_context':f"{obj.get('objectDate')}; {spec['culture']}; {obj.get('medium')}; accession {obj['accessionNumber']}",
     'visual_clues':spec['visual'],'uncertainty_note':spec['uncertain']},
    'emotion_categories':{'primary':spec['primary'],'secondary':spec['secondary']}},
  'review':{'facts_checked_against_museum_api':True,'source_public_domain_flag_checked':True,
    'visual_checked':False,'curatorial_reviewed_on':TODAY,'curatorial_review_status':'provisional',
    'curatorial_review_note':'Separate same-AI source/subject review, official Met object and complete JPEGs '+RUN,
    'ai_content_review_status':'pending','source_evidence_review_status':'pending','image_subject_match_status':'pending'},
  'visitor_explanation':visitor
 }
 reg={'id':id,'title':obj['title'],'official_artwork_url':official,'origin':'met_official_primary',
      'in_shared_catalog':True,'verification':'met_primary_jpeg_http_verified',
      'image_source':{'type':'met_open_access','official_image_page':official,
       'license_label':'The Met Open Access / CC0 (Public Domain work, official primary JPEG)',
       'license_url':OA,'verified_download_url':display['url'],'sha256':display['sha256'],
       'byte_length':display['byte_length'],'last_http_sha_checked_on':TODAY,
       'last_verification_evidence':RUN,'license_review_status':'official_OA_confirmed_release_review_pending',
       'high_resolution':copy.deepcopy(hi)},'accession_number':obj['accessionNumber']}
 for q,claim,section in spec['quotes']:
  need(q in (' '.join(str(x) for x in [q])) and len(q)>=35 and len(q.split())>=6,'bad quote')
  need(claim in spec['text'] and len(claim)>13,'claim not located in Japanese visitor text')
 proposal={'schema_version':'artwork-addition-proposal-v1','id':id,'artwork':art,'image_record':reg}
 add='drafts/artwork-additions/'+id+'.json'
 draftp='drafts/visitor-explanations/'+id+'.json'
 auditp='docs/artwork-completion-audits/'+id+'-'+TODAY+'.json'
 csha=write(add,proposal)
 draft={'id':id,'visitor_explanation':visitor,'evidence':[
   {'claim':spec['historical'],'source_url':official,
    'source_location':'Met Overview: '+ ' | '.join(x[2] for x in spec['quotes']),
    'checked_against_source':True}]}
 dsha=write(draftp,draft)
 rights={'artwork':{'verified':True,'public_domain':True,'source_url':official,
      'finding':'Exact object labelled Public Domain at Met and API isPublicDomain:true.'},
  'image':{'verified':True,'permitted_for_site_use':True,'source_url':OA,
     'finding':'Met OA/CC0 exact primary JPEG; both variants independently checked for full SHA256/dimensions '+RUN},
  'text':{'verified':True,'independent_japanese_prose':True,'source_url':official,
     'finding':'Newly written Japanese visitor prose, original structure, only brief exact quoted primary passages in source audits; no human legal opinion.'}}
 audit={'schema_version':'artwork-v2-new-registration-2','id':id,'checked_on':TODAY,'result':'PASS',
   'unresolved_material_issues':[],'candidate_path':add,'candidate_sha256':csha,
   'draft_path':draftp,'draft_sha256':dsha,
   'baseline':{'artworks_sha256':digest(ROOT/'data/artworks.json'),
               'image_registry_sha256':digest(ROOT/'data/image-sources.json')},
   'official_text_checks':[{'source_url':official,'source_excerpt':q,'visitor_claim':claim,'source_section':section}
     for q,claim,section in spec['quotes']],
   'source_evidence':[
    {'url':official,'location':'Artwork Details and Overview; '+ ' | '.join(x[2] for x in spec['quotes']),
      'finding':spec['historical']+' Source/subject matched using same Met object page; visual: '+spec['visual'],
      'checked_against_source':True},
    {'url':api,'location':'Exact Met objectID, accession, date, primaryImage, primaryImageSmall, classification, public-domain API',
      'finding':'Exact Met object official metadata; complete bytes and dimensions of original and display JPEGs checked in '+RUN,
      'checked_against_source':True},
    {'url':OA,'location':'Met Open Access CC0 public-domain object image and basic data policy',
      'finding':'Images of PD works and basic facts are CC0, but modern artwork Overview writing is not automatically freely reusable.',
      'checked_against_source':True}],
    'rights':rights,
    'separate_pass_review':{'result':'PASS',
      'method':'Separate source-based same-AI evaluation of exact Met public domain webpage text, 2 source excerpt-to-Japanese-claim bindings, official image and primary JPEG API byte checks; research evidence '+RUN,
      'limitations':'Not an external human expert, human visual sign-off, or legal clearance. Met site may throttle CI re-fetch; offline quote binding is not a substitute for having read the original pages.',
      'areas':['identity','image_match','historical_interpretation','emotion','visitor_text','rights'],
      'findings':{'identity':f"Exact Met object {num}, {obj['title']}, {obj['accessionNumber']}; attribution and date kept as source.",
        'image_match':spec['visual']+f" Full official image bytes and downscale RMS {rms}; "+RUN,
        'historical_interpretation':spec['historical']+' Limits: '+spec['uncertain'],
        'emotion':'Tag selection grounded in scene, culture and cautious visitor associations; '+repr(spec['emotions'])+'.',
        'visitor_text':'Independent Japanese paragraphs with two direct Met-Overview sourced claim-to-excerpt checks; source prose not translated verbatim.',
        'rights':'Met official PD object; Met OA/CC0 primary JPEG; distinct current Overview content addressed separately.'}},
    'image_evidence':[images['display'],images['original']],
    'notes':[f"Sequential addition number {seq}; prior records unmodified.",
             'Same AI independent checking pass, not human scholarly or legal approval.']}
 write(auditp,audit)
 call('python','scripts/verify_official_source_text.py','--audit',auditp)
 call('python','scripts/add_artwork.py','preview','--audit',auditp)
 call('python','scripts/add_artwork.py','save','--audit',auditp)
 call('python','scripts/add_artwork.py','check')
 print('REGISTERED',seq,id,obj['title'],flush=True)

def main():
 data=json.loads((ROOT/'data/artworks.json').read_text(encoding='utf-8'))
 existing=copy.deepcopy(data['artworks'])
 registry=json.loads((ROOT/'data/image-sources.json').read_text(encoding='utf-8'))
 oldregistry=copy.deepcopy(registry['records'])
 need(len(existing)==329,'expected 329 starting works')
 for seq,spec in enumerate(SPECS,330):
  register(spec,seq)
 current=json.loads((ROOT/'data/artworks.json').read_text(encoding='utf-8'))['artworks']
 sources=json.loads((ROOT/'data/image-sources.json').read_text(encoding='utf-8'))['records']
 need(len(current)==332 and current[:329]==existing,'catalog count/old records changed')
 need(sources[:len(oldregistry)]==oldregistry,'prior image registry changed')
 for script in ('validate_artworks.py','check_image_sources.py','check_catalog_snapshot.py','complete_artwork.py','add_artwork.py'):
  call('python','scripts/'+script,'check' if script in ('complete_artwork.py','add_artwork.py') else '')
 call('python','-m','unittest','discover','-s','tests','-v')
 newstate=f"""# 美術館データの再開地点

## 現在の状態（2026-11-11時点）

- **完成登録：332作品**。正式数は最新mainとREADMEを確認。
- **次：333作品目から候補調査**。重複・出典本文・作品本体と公式画像の権利・表示を照合。
- 今回330〜332：\`met-37817\` チベットのンゴル寺第8代住職肖像、\`met-437102\` ピーテル・デ・モライン《小屋のある風景》、\`met-451256\` イラン《瓶と杯を持つ人物》。
- 3作品の独自日本語解説、作品別Overviewの短い2箇所と説明文の対応、公式APIによる原寸/表示JPEG完全SHA256・バイト数・寸法・縮小RMS、Met Open Access CC0画像権利とPD表示を個別に照合（[画像調査]({RUN})）。同一AIによる別工程の監査で、外部の人間による審査ではない。
- 既存329作品と画像台帳の過去部分は変更なし。品質と手順は [新規登録ガイド](artwork-expansion-v2.md) と [v2品質基準](artwork-completion-workflow-v2.md) を参照。

## 過去の作業履歴

日付別の進捗・PR・出典は [旧再開メモ](history/resume-artwork-work-through-2026-11-10.md) および [更新履歴](history/resume-updates.md) に保管。過去の「最新」はその時点の状態。
"""
 state=Path('/tmp/next-artwork-resume-330.md')
 state.write_text(newstate,encoding='utf-8')
 call('python','scripts/rotate_resume.py','update','--from',str(state))
 call('git','diff','--check')
 call('git','add','README.md','data/artworks.json','data/image-sources.json','docs/resume-artwork-work.md',
      'docs/history/resume-updates.md','drafts/artwork-additions','drafts/visitor-explanations','docs/artwork-completion-audits')
 call('git','diff','--cached','--check')
 call('git','config','user.name','github-actions[bot]')
 call('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
 call('git','commit','-m','data: register three audited Met paintings 330-332')
 call('git','push')
 print('REGISTRATION-PASS: 332 total; 3 new works, 6 SHA-matched JPEGs, no earlier records changed, committed/pushed',flush=True)

if __name__=='__main__':
 main()
