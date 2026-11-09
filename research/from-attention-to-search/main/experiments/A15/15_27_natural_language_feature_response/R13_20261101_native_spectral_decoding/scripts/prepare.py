import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,hashlib,shutil,re,datetime,unicodedata
import numpy as np
from tokenizers import Tokenizer
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parents[1];B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response');E=B/P.name;R=B/'R11_three_domain_replication_20261030/qualified_three_domain_A02';R12=B/'R12_spectral_semantic_granularity_20261031';M=Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for z in iter(lambda:f.read(8<<20),b''):h.update(z)
 return h.hexdigest()
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines() if l]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert not (E/'freeze.json').exists(),'frozen; do not resample'
tok=Tokenizer.from_file(str(M/'tokenizer.json'));vocab=151936
D={x['seq_id']:x for x in rows(R/'data/documents.jsonl')};S=[x for x in rows(R12/'data/selected_metadata.jsonl') if x['panel']=='the' and x['split']=='heldout'];assert len(S)==37
named=['R11_A02_'+n for n in ['282','292','262','297','090']]
rng=np.random.default_rng(20261101)
ordinary=[str(rng.choice(sorted(x['seq_id'] for x in S if x['domain']==d and x['seq_id'] not in named))) for d in ['math','biology']]
cache={};out=[];targetaudit=[]
# Only cache-end case requires source recovery. Reproduce pinned collector cleaning without fetching.
def successor(r):
 raw=Path(r['raw_path']).read_text();assert hashlib.sha256(raw.encode()).hexdigest()==r['raw_sha256'];s=BeautifulSoup(raw,'html.parser');body=s.find('article');assert body
 for n in body.select('script,style,form,nav,header,footer,.byjus-pagination,.post-tags,.comment-list,.comments-area'):n.decompose()
 for n in list(body.select('table')):
  if re.search('table of contents',n.get_text(' ',strip=True),re.I):n.decompose()
 t=body.get_text('\n',strip=True);assert hashlib.sha256(t.encode()).hexdigest()==r['source_text_sha256'];enc=tok.encode(t[r['char_start']:r['char_start']+6000],add_special_tokens=False);assert enc.ids[:192]==r['token_ids'];assert len(enc.ids)>192
 targetaudit.append({'seq_id':r['seq_id'],'raw_path':r['raw_path'],'raw_sha256':r['raw_sha256'],'source_text_sha256':r['source_text_sha256'],'first192_exact':True,'target_id':enc.ids[192],'target_fragment':tok.decode([enc.ids[192]],skip_special_tokens=False),'following_source_preview':t[r['char_end']:r['char_end']+120]})
 return enc.ids[192]
def add(r,t,panel):
 if r['seq_id'] not in cache:cache[r['seq_id']]=np.load(R/'forward/H'/(r['seq_id']+'.npz'))
 a=cache[r['seq_id']];assert np.array_equal(a['token_ids'],r['token_ids']);y=r['token_ids'][t+1] if t<191 else successor(r)
 row={k:r.get(k) for k in ['seq_id','domain','topic','split','document_family','platform_family','source_stratum','genre','url','raw_path','raw_sha256']};row.update(panel=panel,position=int(t),input_id=int(r['token_ids'][t]),target_id=int(y),input_fragment=tok.decode([r['token_ids'][t]],skip_special_tokens=False),target_fragment=tok.decode([y],skip_special_tokens=False),visible_prefix=tok.decode(r['token_ids'][:t+1],skip_special_tokens=False),future_description=tok.decode(r['token_ids'][t+1:],skip_special_tokens=False),fixed_example=r['seq_id'] in named+ordinary and panel=='the',position_uid=f"{panel}:{r['seq_id']}:{t}",h_source=str(R/'forward/H'/(r['seq_id']+'.npz')))
 out.append((row,a['h27'][t].astype(np.float64)))
for s in S:add(D[s['seq_id']],s['position'],'the')
positions={x['seq_id']:x['position'] for x in S}
for r in sorted(D.values(),key=lambda x:x['seq_id']):
 if r['split']!='heldout' or r['seq_id'] in named:continue
 pool=[t for t in range(32,191) if t!=positions.get(r['seq_id'])]
 for t in sorted(rng.choice(pool,4,replace=False)):add(r,int(t),'natural')
assert len(out)==737 and len({x[0]['seq_id'] for x in out if x[0]['panel']=='natural'})==175
# R04 discovery fitting documents are training side, not H. Check independent document families.
old=rows(B/'R04_domain_usage_20261027/data/documents.jsonl');trainfamilies={x.get('document_family',x.get('document_group')) for x in old if x['split']=='discovery'}
assert not trainfamilies.intersection(x[0]['document_family'] for x in out)
H=np.stack([h for r,h in out]);assert np.isfinite(H).all();np.save(E/'data/h.npy',H)
(E/'data/positions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r,h in out))
base=np.load(R12/'analysis/bases.npz');V=base['V'];mu=base['mean'];ev=base['eigenvalues'];assert V.shape==(1024,1024) and ev[-1]>0
orth=float(abs(V.T@V-np.eye(1024)).max());assert orth<1e-10
bands={'identity':np.empty((1024,0)),'mean_only':np.empty((1024,0))}
for k in [1,4,16,64,128,256,512,768,1024]:bands[f'k{k}']=V[:,:k]
for n in ['middle','tail','head_middle','head_tail','random1031','random1032','random1033']:bands[n]=V@base[n]
for seed in [1034,1035,1036]:
 if seed==1034:Q=V@base['head_random'];assert np.max(abs(Q[:,:64]-V[:,:64]))<1e-12
 else:
  g=np.random.default_rng(seed).normal(size=(1024,64));g-=V[:,:64]@(V[:,:64].T@g);q=np.linalg.qr(g,mode='reduced')[0];Q=np.column_stack([V[:,:64],q])
 assert abs(Q.T@Q-np.eye(128)).max()<1e-10
 bands[f'head_random{seed}']=Q
np.savez(E/'data/bases.npz',V=V,mean=mu,eigenvalues=ev,**bands)
cond=[]
for name,Q in bands.items():
 if name=='identity':rv=1.;dim=1024;hp=H
 else:
  dim=Q.shape[1];rv=float(np.sum(ev[:,None]*(V.T@Q)**2)/ev.sum());hp=mu+(H-mu)@Q@Q.T
 err=float(abs(hp-H).max()) if name=='k1024' else None
 if err is not None:assert err<1e-8
 cond.append({'condition':name,'dimensions':dim,'reference_variance_fraction':rv,'projection_formula':'identity h' if name=='identity' else 'mu+Q Q^T(h-mu)','identity_error_fp64':err})
# Independent TRAIN slice; preserve incomplete inherited raw tokenization provenance.
f=Path('/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin');a=np.fromfile(f,dtype='<u4',count=4194304);assert len(a)==4194304 and a.max()<vocab
counts=np.bincount(a,minlength=vocab);tj=json.loads((M/'tokenizer.json').read_text());valid=np.zeros(vocab,bool);valid[list(tok.get_vocab().values())]=True;special=[x['id'] for x in tj['added_tokens'] if x.get('special')];valid[special]=False
order=sorted(np.flatnonzero(valid),key=lambda i:(-counts[i],int(i)));groups=np.full(vocab,-1,np.int8);n=len(order)
for j,(lo,hi) in enumerate([(0,.01),(.01,.1),(.1,.5),(.5,1)]):groups[np.array(order[int(lo*n):int(hi*n)])]=j
freq=(counts+.5)/(counts[valid].sum()+.5*valid.sum());logfreq=np.log(freq);logfreq[~valid]=0
format_mask=np.zeros(vocab,bool)
for i in np.flatnonzero(valid):
 text=tok.decode([int(i)],skip_special_tokens=False);format_mask[i]=bool(text) and all(c.isspace() or unicodedata.category(c).startswith('P') for c in text)
np.savez(E/'data/frequency.npz',counts=counts,valid=valid,group=groups,logfreq=logfreq,format_mask=format_mask)
frequency={'asset_id':'dclm_token_bins_global01','source':str(f),'offset_tokens':0,'n_tokens':len(a),'selected_bytes_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'dtype':'uint32 little endian','alpha':.5,'nonlexical_or_padding_ids':np.flatnonzero(~valid).tolist(),'lexical_ids':int(valid.sum()),'observed_lexical_ids':int(np.sum((counts>0)&valid)),'reference_tokens_special':int(counts[~valid].sum()),'decode_pilot':tok.decode(a[:128].tolist(),skip_special_tokens=False),'top20':[[int(i),tok.decode([int(i)],skip_special_tokens=False),int(counts[i])] for i in order[:20]],'raw_tokenizer_provenance':'Inherited Qwen3 training declaration; original bin generation revision Unknown'}
spectrum={'n_fit_positions':9600,'n_fit_documents':60,'fit_split':'R04 discovery','mean_centering':'one pooled TRAIN mean; raw residual model units; no RMS normalization','effective_rank_entropy':float(np.exp(-np.sum((ev/ev.sum())*np.log(ev/ev.sum())))),'numerical_rank':int(np.sum(ev>ev[0]*np.finfo(float).eps*1024)),'min_eigenvalue':float(ev[-1]),'max_eigenvalue':float(ev[0]),'orthogonality_max_abs':orth,'adjacent_relative_gaps_lt_1pct':int(np.sum((ev[:-1]-ev[1:])/ev[:-1]<.01)),'eigengaps':{str(k):float((ev[k-1]-ev[k])/ev[k-1]) for k in [1,4,16,64,128,256,480,512,544,768,960]},'reuse_independent_replication':False,'all_PC_identity_max_abs':float(abs(mu+(H-mu)@V@V.T-H).max())}
manifest=json.loads((E/'manifest.json').read_text());manifest.update(status='CPU_AUDIT_COMPLETE_PANEL_FROZEN',model_dir=str(M),R12=str(R12),cache_root=str(R),measurement='block27 residual-post BEFORE final model.norm; apply native norm then tied lm_head',panels={'the':{'documents':37,'positions':37,'exposed':True},'natural':{'documents':175,'positions':700,'exposed_parent_docs':True,'new_positions_unselected_by_output':True}},fixed_examples=named+ordinary,target_recovery=targetaudit,spectrum=spectrum,frequency_reference=frequency,conditions=cond,resource={'profile':'5090-2-spot','reason':'Existing registered minimum RTX5090 profile is2 cards; only device0 used for this small analysis. No unverified single-card spec is invented.','max_concurrent_gpus':2},asset_ids=['model_qwen3_0p6b_base_official_a5','tokenizer_qwen3_0p6b_base_official_a5','analysis_a15_27_05_r12_spectral_semantic_granularity_20261031','representation_a15_27_r11_A02_h_native_jointz_h27_20261030','analysis_a15_27_04_r10_domain_member_atlas_20261030','dclm_token_bins_global01'])
files=[M/'model.safetensors',M/'config.json',M/'tokenizer.json',M/'tokenizer_config.json',R12/'config.json',R12/'analysis/bases.npz',R12/'data/selected_metadata.jsonl',R/'data/documents.jsonl',R/'scripts/run_native_cc.py',E/'data/positions.jsonl',E/'data/h.npy',E/'data/bases.npz',E/'data/frequency.npz']
manifest['input_sha256']={str(f):sha(f) for f in files};assert manifest['input_sha256'][str(M/'model.safetensors')]=='cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba'
for b in [P,E]:dump(b/'manifest.json',manifest)
dump(E/'audit/01_scientific_identification.json',{'question':'native output recovery vs variance rank','rivals':['mean bias','rank or energy recovery','the lexical restriction','normalization angle','frequency proxy not semantics'],'changed':'projected block27 vector only','fixed':'weights,head,norm,prefix,targets,mean,basis','mechanism_conclusion':'not identified'})
dump(E/'audit/02_data_statistics.json',{'positions':len(out),'primary_documents':37,'supplemental_documents':175,'independent_PCA_document_families':True,'H_previously_exposed':True,'next_target_recovered':targetaudit,'frequency_sample_frozen_before_outputs':True,'bootstrap_unit':'document','no_output_selection':True})
print(json.dumps({'prepared_positions':len(out),'showcases':manifest['fixed_examples'],'spectrum':spectrum,'frequency_top10':frequency['top20'][:10]},ensure_ascii=False,indent=2))
