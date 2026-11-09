from pathlib import Path
import json,re,hashlib,collections,io,math
from urllib.parse import urlsplit,unquote
import zstandard as zstd,numpy as np
from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];OLD=E.parent;SRC=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/data/formal_dclm_1b_unique_v3/raw_compressed_cache/494fa3d37bd9b5f68b1171b1c2352f39691af7fabed89cb1377f37589cc8cc75.jsonl.zst');SEED=110203
sha=lambda b:hashlib.sha256(b).hexdigest()
T=Tokenizer.from_file('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json')
terms={'mathematics':r'\b(?:theorem|lemma|algebra|algebraic|calculus|integral|derivative|polynomial|topology|topological|equation|matrix|matrices|vector|geometry|geometric|manifold|integer|prime|proof|axiom|mathematical|mathematician|isomorphism|cohomology|arithmetic|eigenvalue|function|functions|differential)\b','biology':r'\b(?:cell|cells|cellular|protein|proteins|gene|genes|genetic|genome|genomic|dna|rna|enzyme|enzymes|bacteria|bacterial|organism|organisms|evolution|ecology|species|chromosome|neuron|neurons|biological|biology|tissue|mitochondria|membrane|molecular|mutation)\b','physics':r'\b(?:photon|photons|electron|electrons|quantum|relativity|relativistic|magnetic|electromagnetic|gravitational|gravity|thermodynamics|thermodynamic|momentum|velocity|acceleration|wavelength|frequency|wave|waves|electric|electricity|voltage|current|particle|particles|proton|neutron|physics|physicist|oscillation|energy|force|forces|pressure|mass)\b'}
# Known analyzed texts and reference lines are excluded; merely scanned candidates cannot enter validation.
old_lines=set();old_hash=set();old_groups=set();oldtext=[];exposed_candidates=set()
for name in ['R04_domain_usage_20261027/data/documents.jsonl','R04_domain_usage_20261027/data/reference.jsonl','R12_spectral_semantic_granularity_20261031/data/selected_metadata.jsonl']:
 for l in (OLD/name).read_text().splitlines():
  d=json.loads(l);line=d.get('source_line');
  if line is not None:old_lines.add(int(line))
  old_hash.update(str(d[k]) for k in ['source_text_sha256','text_sha256'] if k in d)
  if d.get('document_group'):old_groups.add(d['document_group'])
  oldtext.append(d)
for name in ['document_source_candidates.jsonl','biology_qa_source_pool.jsonl','reference_source_pool.jsonl']:
 for l in (OLD/'R04_domain_usage_20261027'/name).read_text().splitlines():
  d=json.loads(l)
  if 'source_line' in d:exposed_candidates.add(int(d['source_line']))
pools={k:[] for k in list(terms)+['general']};counts=collections.Counter();filt=collections.Counter();scanned=0
with SRC.open('rb') as raw,zstd.ZstdDecompressor().stream_reader(raw) as rd:
 for i,l in enumerate(io.TextIOWrapper(rd)):
  scanned=i+1;d=json.loads(l);text=d.get('text','');url=d.get('url','');u=urlsplit(url);host=(u.hostname or '').lower();group=host+unquote(u.path).rstrip('/')
  if group in old_groups:filt['old_analyzed']+=1;continue
  if len(text)<900 or d.get('language_id_whole_page_fasttext',{}).get('en',0)<.85:filt['short_or_low_en']+=1;continue
  scan=text[:6500].lower();hits={k:len(set(re.findall(v,scan))) for k,v in terms.items()};order=sorted(hits,key=hits.get,reverse=True);top=order[0]
  domain=top if hits[top]>=4 and hits[top]>=hits[order[1]]+2 else 'general'
  if domain=='general' and max(hits.values())>=3:filt['mixed_domain']+=1;continue
  if domain=='general' and len(re.findall(r'\b(?:the|is|was|were|and|that|with|from)\b',scan))<15:filt['not_prose']+=1;continue
  counts[domain]+=1;rank=sha(f'{SEED}:{group}:{i}'.encode());x={'source_line':i,'url':url,'host':host,'document_group':group,'domain':domain,'term_distinct_counts':hits,'text':text,'source_text_sha256':sha(text.encode()),'warc_record_id':d.get('metadata',{}).get('WARC-Record-ID'),'prior_candidate_exposure':False,'rank':rank}
  pools[domain].append(x)
  if len(pools[domain])>1200:pools[domain]=sorted(pools[domain],key=lambda x:x['rank'])[:800]
# Full contiguous prefix, no hand-selected content start or outcome screening.
selected=[];seen_group=set();shingles=[];accepted=collections.Counter();hosts=collections.Counter();rejected=[]
def sh(ids):return set(tuple(ids[i:i+5]) for i in range(len(ids)-4))
for dom in pools:
 for x in sorted(pools[dom],key=lambda x:x['rank']):
  if accepted[dom]>=150:break
  if x['document_group'] in seen_group or hosts[(dom,x['host'])]>=40:continue
  en=T.encode(x['text'],add_special_tokens=False)
  if len(en.ids)<256:continue
  n=min(512,len(en.ids));end=en.offsets[n-1][1];prefix=x['text'][:end];ids=T.encode(prefix,add_special_tokens=False).ids
  while ids!=en.ids[:n] and n>256:
   n-=1;end=en.offsets[n-1][1];prefix=x['text'][:end];ids=T.encode(prefix,add_special_tokens=False).ids
  if ids!=en.ids[:n]:continue
  ss=sh(ids);duplicate=False
  for prev in shingles:
   inter=len(ss&prev)
   if inter/max(len(ss|prev),1)>=.8:duplicate=True;break
  if duplicate:rejected.append({'source_line':x['source_line'],'reason':'exact_token5_Jaccard>=.8'});continue
  # Old 192/256-token windows are also excluded by containment, not only Jaccard.
  for old in oldtext:
   oi=old.get('token_ids',[])
   if len(oi)<32:continue
   os=sh(oi);inter=len(ss&os)
   if inter/max(min(len(ss),len(os)),1)>=.8:duplicate=True;break
  if duplicate:rejected.append({'source_line':x['source_line'],'reason':'old_window_shingle_containment>=.8'});continue
  x={k:v for k,v in x.items() if k!='text'};x.update({'doc_id':f'R15_{dom}_{accepted[dom]:03d}','prefix':prefix,'token_ids':ids,'source_token_count':len(en.ids),'window_tokens':n,'char_start':0,'char_end':end,'source_asset_id':'dclm_crosscoder_selected_raw_1b_candidates_20261013','source_file':str(SRC),'possible_A22_training_exposure':True,'domain_annotation':'deterministic source-cohort keyword screen;not semantic gold label','genre_annotation':'general prose screen only;not blinded expository/narrative annotation'})
  selected.append(x);seen_group.add(x['document_group']);shingles.append(ss);hosts[(dom,x['host'])]+=1;accepted[dom]+=1
# 75/37/38 and75/38/37 alternating yields300/150/150 when all quotas exist.
for k,dom in enumerate(pools):
 aa=sorted([x for x in selected if x['domain']==dom],key=lambda x:x['rank']);disc=math.floor(len(aa)*.5);dev=math.floor((len(aa)-disc)/2)+(k%2)
 fresh=[x for x in aa if not x['prior_candidate_exposure']];old=[x for x in aa if x['prior_candidate_exposure']];nv=len(aa)-disc-dev
 if len(fresh)<nv:
  print('DATA_GATE',dom,'selected',len(aa),'fresh',len(fresh),'required_validation',nv,'all_candidates',dict(counts),flush=True)
  raise RuntimeError(('insufficient unviewed validation documents',dom,len(fresh),nv))
 validation=fresh[-nv:];others=[x for x in aa if x not in validation]
 for x in others[:disc]:x['split']='discovery'
 for x in others[disc:]:x['split']='development'
 for x in validation:x['split']='validation'
# Sample32 positions per sequence quartile, at most128, exclude final position lacking observed successor.
positions=[]
for di,x in enumerate(selected):
 ids=x['token_ids'];enc=T.encode(x['prefix'],add_special_tokens=False);rng=np.random.default_rng(int(x['rank'][:12],16));ix=[]
 for bin in np.array_split(np.arange(len(ids)-1),4):ix.extend(sorted(rng.choice(bin,min(32,len(bin)),replace=False).tolist()))
 x['positions']=ix;x['row_start']=len(positions)
 for p in ix:
  off=enc.offsets[p][1];vis=T.decode(ids[:p+1],skip_special_tokens=False);piece=T.decode([ids[p]],skip_special_tokens=False);cat='number' if re.fullmatch(r'\s*\d+\s*',piece) else 'punctuation' if re.fullmatch(r'\s*[^\w\s]+\s*',piece,re.U) else 'word' if re.search('[A-Za-z]',piece) else 'format' if not piece.strip() else 'other'
  positions.append({'row':len(positions),'doc_index':di,'doc_id':x['doc_id'],'split':x['split'],'domain':x['domain'],'source_family':x['host'],'document_group':x['document_group'],'source_line':x['source_line'],'position':p,'position_quartile':min(3,4*p//len(ids)),'visible_tokens':p+1,'window_tokens':len(ids),'token_id':ids[p],'token_fragment':piece,'token_category':cat,'next_token_id':ids[p+1],'special_token':ids[p]>=151643,'visible_prefix':vis,'visible_token_ids_reference':{'doc_id':x['doc_id'],'slice_stop':p+1},'partial_unicode_decode': '\ufffd' in vis,'causal_boundary':'ends at current token;no future used for phenomenon labels'})
(E/'data/documents.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in selected));(E/'data/positions.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in positions))
report={'scanned_records':scanned,'candidate_domain_counts':dict(counts),'filter_counts':dict(filt),'selected_documents':len(selected),'selected_domain_counts':dict(accepted),'split_counts':dict(collections.Counter(x['split'] for x in selected)),'domain_split_counts':{dom:dict(collections.Counter(x['split'] for x in selected if x['domain']==dom)) for dom in pools},'source_host_counts':dict(collections.Counter(x['host'] for x in selected)),'old_analyzed_lines_excluded':len(old_lines),'known_candidate_pool_lines':len(exposed_candidates),'validation_prior_candidate_exposure':sum(x['prior_candidate_exposure'] for x in selected if x['split']=='validation'),'near_duplicate_rejections':rejected,'positions':len(positions),'source':str(SRC),'source_sha256':sha(SRC.read_bytes()),'length_by_domain':{dom:{'window_min':min(x['window_tokens'] for x in selected if x['domain']==dom),'window_max':max(x['window_tokens'] for x in selected if x['domain']==dom),'source_token_median':float(np.median([x['source_token_count'] for x in selected if x['domain']==dom]))} for dom in pools}}
(E/'audit/data_preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['source_host_counts','near_duplicate_rejections']},ensure_ascii=False,indent=2),flush=True)
