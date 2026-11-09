"""R10-v1: offline natural/shared-z member atlas. Never imports a model runtime."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,csv,hashlib,datetime,collections,argparse,shutil
import numpy as np
from scipy import sparse,linalg,stats
from tokenizers import Tokenizer

B=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=B/'R10_domain_member_atlas_20261030');args=parser.parse_args()
O=args.output;O.mkdir(parents=True,exist_ok=True)
if not (O/'config.json').exists():shutil.copy2(B/'R10_domain_member_atlas_20261030/config.json',O/'config.json')
A=O/'analysis';T=O/'tables'
for p in [A,T,O/'figures',O/'appendix']:p.mkdir(exist_ok=True)
C=json.loads((O/'config.json').read_text());rng=np.random.default_rng(C['seed']);F=16384
R4=B/'R04_domain_usage_20261027';S=R4/'domain_discriminability_spectrum_20261028';H=S/'real_spectrum_A01'
sources=set();checks={}
def track(p):sources.add(str(p));return p
def load(p):return np.load(track(p),allow_pickle=False)
def js(p):return json.loads(track(p).read_text())
def lines(p):return [json.loads(x) for x in track(p).read_text().splitlines()]
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def scalar(x):return x.item() if isinstance(x,np.generic) else x
def table(name,rows):
 rows=list(rows)
 if not rows:return
 with (T/name).open('w',newline='') as fp:
  w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows([{k:scalar(v) for k,v in r.items()} for r in rows])
def log(s):print(s,flush=True)
def mult(n):return rng.multinomial(n,np.full(n,1/n),size=C['bootstrap_reps'])/n
def bands(x):return x.reshape(*x.shape[:-1],16,64).sum(-1)
def auc(m,b):return ((m[:,None,:]>b[None,:,:])+0.5*(m[:,None,:]==b[None,:,:])).mean((0,1))
def ci(x):return np.quantile(x,[.025,.975],axis=0)

docs=lines(R4/'data/documents.jsonl');D=len(docs)
labels=np.array([r['label'] for r in docs]);splits=np.array([r['split'] for r in docs])
ix={s:np.flatnonzero(splits==s) for s in ['discovery','development','heldout']}
checks['document_groups_unique']=len({r['document_group'] for r in docs})==D
assert checks['document_groups_unique']
agg=load(R4/'forward/documents_CC.npz');order=[list(agg['seq_id']).index(r['seq_id']) for r in docs]
counts=agg['counts'][order];responses=agg['sum_z'][order]/agg['n_positions'][order,None]
trm=ix['discovery'][labels[ix['discovery']]==1];trb=ix['discovery'][labels[ix['discovery']]==0]
sm=(counts[trm]>0).sum(0);sb=(counts[trb]>0).sum(0)
support=(sm>=5)|(sb>=5);raw=auc(responses[trm],responses[trb]);direction=np.sign(raw-.5).astype(int)
oriented=np.maximum(raw,1-raw);rank=np.lexsort((np.arange(F),-np.abs(raw-.5)))
ranked={g:rank[support[rank]&(direction[rank]==sign)] for g,sign in [('math',1),('biology',-1)]}
sets={}
for g in ranked:
 sets['main_'+g]=ranked[g][oriented[ranked[g]]>=.75]
 for threshold in [.70,.80]:sets[f'auc{threshold:.2f}_'+g]=ranked[g][oriented[ranked[g]]>=threshold]
 for k in [16,64,128]:sets[f'top{k}_'+g]=ranked[g][:k]
main=np.r_[sets['main_math'],sets['main_biology']];selected=np.zeros(F,bool);selected[main]=True
freeze={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'config_sha256':hashlib.sha256((O/'config.json').read_bytes()).hexdigest(),'discovery_only':True,'universe':F,'positive_any_discovery':int(((sm+sb)>0).sum()),'support_qualified':int(support.sum()),'rejected_no_discovery_activation':int(((sm+sb)==0).sum()),'rejected_positive_but_under5_each':int((~support&((sm+sb)>0)).sum()),'eligible_auc_ties':int((support&(direction==0)).sum()),'sets':{k:v.tolist() for k,v in sets.items()},'rank_all_eligible':rank[support[rank]].tolist()}
if (O/'freeze.json').exists():
 existing=json.loads((O/'freeze.json').read_text());assert existing['config_sha256']==freeze['config_sha256'] and existing['sets']==freeze['sets'],'Frozen membership changed; refuse'
else:dump(O/'freeze.json',freeze)
log(f"FREEZE support={support.sum()} main math={len(sets['main_math'])} bio={len(sets['main_biology'])}; before heldout analysis")
np.savez_compressed(A/'discovery_metrics.npz',raw_auc=raw,oriented_auc=oriented,direction=direction,support=support,support_math=sm,support_biology=sb,document_response=responses)

ref=load(R4/'forward/reference_CC.npz');hits=ref['counts'].sum(0);refN=int(ref['n_positions'].sum());rate=hits/refN
freq=np.searchsorted(C['frequency']['original_cuts'],rate,side='left');freq[hits<20]=3
logfreq=np.searchsorted(C['frequency']['log_cuts'],rate,side='left');logfreq[hits<20]=3
freqrows=[]
for name,ids in {'eligible_pool':np.flatnonzero(support),**sets}.items():
 for rule,freqx in [('original',freq),('log_width',logfreq)]:
  valid=int((freqx[ids]<3).sum())
  for k,lab in enumerate(['low','middle','high','insufficient']):
   n=int((freqx[ids]==k).sum());freqrows.append(dict(selection=name,rule=rule,frequency=lab,count=n,plotted_denominator=valid,all_members=len(ids),proportion=n/valid if k<3 and valid else ''))
table('frequency_counts.csv',freqrows)

# Heldout does not affect membership. Intervals resample whole documents, not tokens.
aucs={};cis={};reps={};bootweights={}
for split in ['development','heldout']:
 mi=ix[split][labels[ix[split]]==1];bi=ix[split][labels[ix[split]]==0]
 a=auc(responses[mi],responses[bi]);aucs[split]=a
 if split=='heldout':
  wm,wb=mult(len(mi)),mult(len(bi));bootweights={'math':wm,'biology':wb}
  weights=(wm[:,:,None]*wb[:,None,:]).reshape(C['bootstrap_reps'],-1)
  low=np.full(F,np.nan);high=low.copy()
  for chunk in np.array_split(main,max(1,int(np.ceil(len(main)/512)))):
   pair=(responses[mi,None,:][:,:,chunk]>responses[None,bi,:][:,:,chunk]).astype(np.float64)
   pair+=.5*(responses[mi,None,:][:,:,chunk]==responses[None,bi,:][:,:,chunk])
   sample=weights@pair.reshape(-1,len(chunk));sample=np.where(direction[chunk]>0,sample,1-sample)
   low[chunk],high[chunk]=ci(sample)
  cis[split]=(low,high);reps[split]=selected&(low>.5)
np.savez_compressed(A/'heldout_document_bootstrap_weights.npz',**bootweights)
log(f"Heldout exploratory support math={reps['heldout'][sets['main_math']].sum()} bio={reps['heldout'][sets['main_biology']].sum()}")

# Full native position cache; preserve zeros in a sparse matrix.
indptr=[0];allids=[];allz=[];token=[]
for r in docs:
 a=load(R4/'forward/documents'/f"{r['seq_id']}.npz");assert np.array_equal(a['token_ids'],r['token_ids'])
 p=a['CC_ptr'];lo,hi=int(p[32]),int(p[192]);allids.append(a['CC_ids'][lo:hi].astype(np.int32));allz.append(a['CC_z'][lo:hi]);indptr.extend((p[33:193]-lo+indptr[-1]).tolist());token.extend(r['token_ids'][32:192])
Z=sparse.csr_matrix((np.concatenate(allz),np.concatenate(allids),np.array(indptr)),shape=(D*160,F));Z.sort_indices();token=np.array(token,dtype=np.int32)
docindex=np.repeat(np.arange(D),160);positions=np.tile(np.arange(32,192),D)
calc=np.stack([np.asarray(Z[d*160:(d+1)*160].sum(0)).ravel()/160 for d in range(D)])
checks['aggregate_vs_sparse_z_max_error']=float(abs(calc-responses).max());assert np.allclose(calc,responses,rtol=2e-6,atol=1e-7)
sparse.save_npz(A/'native_positions_csr.npz',Z);np.savez_compressed(A/'position_keys.npz',token_id=token,document_index=docindex,position=positions)

# Audit the existing common corpus PCA against actual raw h, never claim independence.
basis=load(H/'analysis/CC_common_basis.npz');V=basis['PC_columns'];lam=basis['eigenvalues'];mu=basis['mean']
fitH=[]
for j in ix['discovery']:
 a=load(H/'raw_documents'/f"{docs[j]['seq_id']}.npz");assert np.array_equal(a['token_ids'],docs[j]['token_ids']);fitH.append(a['CC_h'][32:192])
fitH=np.concatenate(fitH).astype(np.float64);center=fitH.mean(0);X=fitH-center;cov=X.T@X/(len(X)-1)
checks['pca_source_ids_exact']=set(basis['fit_seq_ids'])=={docs[j]['seq_id'] for j in ix['discovery']}
checks['pca_mean_max_error']=float(abs(center-mu).max());checks['pca_orthogonality_max_error']=float(abs(V.T@V-np.eye(1024)).max())
checks['pca_eigen_relative_residual']=float(np.linalg.norm(cov@V-V*lam)/np.linalg.norm(cov))
checks['pca_trace_error']=float(abs(np.trace(cov)-lam.sum())/np.trace(cov))
assert checks['pca_source_ids_exact'] and checks['pca_mean_max_error']<1e-8 and checks['pca_eigen_relative_residual']<1e-10
rankP=int((lam>basis['rank_tolerance']).sum());del fitH,X,cov
dec=load(B/'R09_domain_difference_decomposition_20261029/analysis/decoder_and_scale.npz');decoder=dec['decoder_model_scale'];norm=np.linalg.norm(decoder,axis=1);nz=norm>0
unit=np.divide(decoder,norm[:,None],out=np.zeros_like(decoder),where=nz[:,None]);coef=unit@V;power=coef**2;band=bands(power)
checks['full_decoder_projection_sum_max_error']=float(abs(power[nz].sum(1)-1).max());assert checks['full_decoder_projection_sum_max_error']<1e-10
checks['zero_decoder_main']=int((~nz[main]).sum())
np.savez_compressed(A/'common_spectrum.npz',PC_columns=V,mean=mu,eigenvalues=lam,effective_rank=rankP,source_basis_sha256=hashlib.sha256((H/'analysis/CC_common_basis.npz').read_bytes()).hexdigest())
np.savez_compressed(A/'all_decoder_projection.npz',per_pc=power,per_band=band,decoder_norm_model=norm,zero_norm=~nz)
log(f"Common PCA rank={rankP}; audited identical R04/R07 basis; full projection error={checks['full_decoder_projection_sum_max_error']:.2g}")

# Exact conditional background from the whole eligible dictionary, includes selected.
bgpool=np.flatnonzero(support&nz);stratum=freq*10+((sm+sb)//10)
draw={g:np.empty((1000,len(sets['main_'+g])),np.int32) for g in ranked};stratarows=[]
for st in np.unique(stratum[main]):
 pool=bgpool[stratum[bgpool]==st];loc={g:np.flatnonzero(stratum[sets['main_'+g]]==st) for g in ranked}
 nm,nb=len(loc['math']),len(loc['biology']);assert len(pool)>=nm+nb
 for i in range(1000):
  picked=rng.choice(pool,nm+nb,replace=False)
  draw['math'][i,loc['math']]=picked[:nm];draw['biology'][i,loc['biology']]=picked[nm:]
 stratarows.append(dict(stratum=int(st),frequency=['low','middle','high','insufficient'][int(st//10)],support_total_min=int(st%10*10),pool=len(pool),math=nm,biology=nb))
table('matched_strata.csv',stratarows)
bg={}
for g in ranked:
 ids=draw[g];row=np.repeat(np.arange(1000),ids.shape[1]);weights=sparse.csr_matrix((np.full(ids.size,1/ids.shape[1]),(row,ids.ravel())),shape=(1000,F))
 bg[g]=weights@power
 np.savez_compressed(A/f'{g}_matched_background.npz',feature_ids=ids,mean_per_pc=bg[g],selected_inclusion_fraction=selected[ids].mean(1))
q={g:power[sets['main_'+g]].mean(0) for g in ranked};overlap=float(np.minimum(q['math'],q['biology']).sum());overlapband=float(np.minimum(bands(q['math']),bands(q['biology'])).sum())
ovbg=np.minimum(bg['math'],bg['biology']).sum(1);ovbbg=np.minimum(bands(bg['math']),bands(bg['biology'])).sum(1)
segment={g:q[g][1:64].sum() for g in ranked}
ovseg=float(np.minimum(q['math'][1:64]/segment['math'],q['biology'][1:64]/segment['biology']).sum())
seg_bg=np.minimum(bg['math'][:,1:64]/bg['math'][:,1:64].sum(1,keepdims=True),bg['biology'][:,1:64]/bg['biology'][:,1:64].sum(1,keepdims=True)).sum(1)
geometry={'rank':rankP,'reuse_R04_R07_identical_basis':True,'independent_reference_status':'MISSING: R07 is same corpus, R08 target-only PCA is ineligible as replacement','overlap_pc':overlap,'overlap_band':overlapband,'overlap_pc_bg95':ci(ovbg).tolist(),'overlap_band_bg95':ci(ovbbg).tolist(),'PC2_64_overlap_renormalized':ovseg,'PC2_64_bg95':ci(seg_bg).tolist(),'groups':{}}
for g in ranked:
 ids=sets['main_'+g];tri=np.column_stack([power[ids,0],power[ids,1:64].sum(1),power[ids,64:].sum(1)])
 geometry['groups'][g]={'n':len(ids),'head_mean':float(band[ids,0].mean()),'head_median':float(np.median(band[ids,0])),'PC1_mean':float(power[ids,0].mean()),'PC2_64_mean':float(segment[g]),'head_background95':ci(bands(bg[g])[:,0]).tolist(),'PC1_background95':ci(bg[g][:,0]).tolist(),'PC2_64_background95':ci(bg[g][:,1:64].sum(1)).tolist(),'background_selected_inclusion_mean':float(selected[draw[g]].mean())}
idsm,idsb=sets['main_math'],sets['main_biology'];cos=abs(unit[idsm]@unit[idsb].T)
np.savez_compressed(A/'cross_group_absolute_cosine.npz',math_ids=idsm,biology_ids=idsb,absolute_cosine=cos)
qm=linalg.orth(unit[idsm].T);qb=linalg.orth(unit[idsb].T);principal=linalg.svdvals(qm.T@qb);subtrace=float((principal**2).sum())
geometry['actual_subspace']={'math_rank':qm.shape[1],'biology_rank':qb.shape[1],'trace_overlap':subtrace,'trace_over_min_rank':subtrace/min(qm.shape[1],qb.shape[1]),'pair_abs_cosine_mean':float(cos.mean()),'pair_abs_cosine_max':float(cos.max()),'interpretation':'dimension-dependent subspace overlap; not spectral-distribution overlap or semantic equivalence'}
np.savez_compressed(A/'actual_decoder_subspace.npz',principal_cosine=principal,math_rank=qm.shape[1],biology_rank=qb.shape[1])
dump(A/'geometry.json',geometry)
table('member_spectrum.csv',(dict(feature_id=int(f),domain_bias=g,**{f'band{i+1}':float(band[f,i]) for i in range(16)},PC1=float(power[f,0]),PC2_64=float(power[f,1:64].sum()),PC65_plus=float(power[f,64:].sum())) for g in ranked for f in sets['main_'+g]))
table('group_pc_spectrum.csv',(dict(PC=j+1,math=float(q['math'][j]),biology=float(q['biology'][j]),common=float(min(q['math'][j],q['biology'][j]))) for j in range(1024)))

# Group reconstruction: sum coefficient vectors before squaring, not a sum of member energies.
contrib=[];coefaudit=[]
for g in ranked:
 ids=sets['main_'+g];scaledcoef=coef[ids]*norm[ids,None]
 energies=[];wrong=[]
 for j in ix['heldout']:
  z=Z[j*160:(j+1)*160,ids];vpc=z@scaledcoef;energies.append(bands((vpc**2).mean(0)));wrong.append(bands(np.asarray(z.power(2).mean(0)).ravel()@(scaledcoef**2)))
  if len(coefaudit)<2:
   direct=(z[:3]@decoder[ids])@V;coefaudit.append(float(abs(direct-vpc[:3]).max()))
 energies=np.array(energies);wrong=np.array(wrong)
 for dom,lab in [('math',1),('biology',0)]:
  choose=labels[ix['heldout']]==lab;energy=energies[choose].mean(0);total=energy.sum();frac=energy/total if total>1e-12 else np.full(16,np.nan);wc=wrong[choose].mean(0)
  for k in range(16):contrib.append(dict(member_group=g,input_domain=dom,documents=int(choose.sum()),members=len(ids),band=k+1,mean_squared_projection=float(energy[k]),total_mean_squared_norm=float(total),fraction=float(frac[k]),incorrect_member_energy_sum=float(wc[k])))
table('group_reconstruction_energy.csv',contrib);checks['contribution_direct_vs_PC_max_error']=max(coefaudit)
log(f"Geometry overlap PC={overlap:.4f}, bands={overlapband:.4f}; reconstruction cross terms retained")

# Real token counts in this panel. Member high thresholds fit only on discovery positives.
vocabcounts=collections.Counter(token.tolist());types=np.array(sorted(vocabcounts));typecounts=np.array([vocabcounts[int(t)] for t in types]);cuts=np.quantile(typecounts,[1/3,2/3],method='higher').astype(int)
tbin={int(t):int(np.searchsorted(cuts,n,side='left')) for t,n in zip(types,typecounts)};eventbin=np.array([tbin[int(t)] for t in token]);baseline=np.bincount(eventbin,minlength=3)/len(token)
tok=Tokenizer.from_file(str(track(Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json'))))
vocabmeta=js(Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer_config.json'));specialids={int(x['id']) for x in js(Path('/data/250010109/model_cache/Qwen3-0.6B-Base-official/tokenizer.json'))['added_tokens'] if x.get('special')}
tdiscovery=np.isin(docindex,ix['discovery']);theld=np.isin(docindex,ix['heldout']);csc=Z.tocsc();threshold=np.full(F,np.nan);tokenresults={};tokenrows=[];examples=[];eventrows=[]
for g in ranked:
 for rr,f in enumerate(sets['main_'+g]):
  lo,hi=csc.indptr[f:f+2];rows=csc.indices[lo:hi];vals=csc.data[lo:hi];train=tdiscovery[rows];positive=vals[train];threshold[f]=np.quantile(positive,.9) if len(positive)>=20 else np.nan
  activeh=theld[rows]&(vals>threshold[f]);hr=rows[activeh];hv=vals[activeh];nh=len(hr);nd=len(np.unique(docindex[hr]));usable=len(positive)>=20 and nh>=5 and nd>=2
  proportions=np.bincount(eventbin[hr],minlength=3)/nh if nh else np.full(3,np.nan)
  tcounts=np.array([vocabcounts[int(t)] for t in token[hr]]) if nh else np.array([])
  tm=float(np.median(tcounts)) if nh else np.nan
  row=dict(feature_id=int(f),domain_bias=g,discovery_rank=rr+1,discovery_positive_events=len(positive),positive_z_p90=float(threshold[f]) if np.isfinite(threshold[f]) else '',heldout_high_events=nh,heldout_high_documents=nd,usable=bool(usable),distinct_high_token_ids=len(set(token[hr])),token_count_median=tm if nh else '',token_count_p10=float(np.quantile(tcounts,.1)) if nh else '',token_count_p90=float(np.quantile(tcounts,.9)) if nh else '',math_high_events=int((labels[docindex[hr]]==1).sum()),biology_high_events=int((labels[docindex[hr]]==0).sum()),low=float(proportions[0]) if nh else '',middle=float(proportions[1]) if nh else '',high=float(proportions[2]) if nh else '')
  tokenrows.append(row);tokenresults[int(f)]=row
  for t,n in collections.Counter(token[hr].tolist()).items():eventrows.append(dict(feature_id=int(f),token_id=t,high_event_count=n,panel_token_count=vocabcounts[t],token_frequency_bin=['low','middle','high'][tbin[t]]))
  if rr<3:
   useddocs=set()
   # Up to two high examples/member, one/document; low example shares exact token ID.
   for ei in np.argsort(-hv):
    pos=int(hr[ei]);dj=int(docindex[pos]);tid=int(token[pos]);zv=float(hv[ei])
    if dj in useddocs:continue
    useddocs.add(dj)
    candidates=np.flatnonzero((token==tid)&(docindex!=dj));localz=np.asarray(Z[candidates,f].toarray()).ravel()
    lowpos=int(candidates[np.argmin(localz)]) if len(candidates) else None
    def rec(kind,p,z):
     j=int(docindex[p]);pt=int(positions[p]);r=docs[j];return dict(feature_id=int(f),domain_bias=g,rank=rr+1,kind=kind,seq_id=r['seq_id'],split=r['split'],domain=r['domain'],token_id=int(token[p]),token_string=tok.decode([int(token[p])],skip_special_tokens=False),position=pt,z=float(z),threshold=float(threshold[f]),panel_token_count=vocabcounts[int(token[p])],already_read_prefix=tok.decode(r['token_ids'][:pt],skip_special_tokens=False))
    examples.append(rec('high',pos,zv))
    if lowpos is not None:examples.append(rec('same_token_low',lowpos,float(localz.min())))
    if len(useddocs)>=2:break
  high_counts=collections.Counter(token[hr].tolist());row['top1_high_token_share']=max(high_counts.values())/nh if nh else '';row['top5_high_token_share']=sum(sorted(high_counts.values(),reverse=True)[:5])/nh if nh else ''
  # All-member compact example appendix: highest heldout event and a same-ID low contrast.
  if nh:
   ei=int(np.argmax(hv));p=int(hr[ei]);j=int(docindex[p]);pt=int(positions[p]);tid=int(token[p]);can=np.flatnonzero((token==tid)&(docindex!=j));lz=np.asarray(Z[can,f].toarray()).ravel();lp=int(can[np.argmin(lz)]) if len(can) else None
   row['example_high_token_id']=tid;row['example_high_token']=tok.decode([tid],skip_special_tokens=False);row['example_high_seq_id']=docs[j]['seq_id'];row['example_high_position']=pt;row['example_high_z']=float(hv[ei]);row['example_prefix']=tok.decode(docs[j]['token_ids'][:pt],skip_special_tokens=False);row['same_token_low_z']=float(lz.min()) if lp is not None else '';row['same_token_low_seq_id']=docs[int(docindex[lp])]['seq_id'] if lp is not None else '';row['same_token_low_position']=int(positions[lp]) if lp is not None else '';row['same_token_low_prefix']=tok.decode(docs[int(docindex[lp])]['token_ids'][:int(positions[lp])],skip_special_tokens=False) if lp is not None else ''
  else:
   for k in ['example_high_token_id','example_high_token','example_high_seq_id','example_high_position','example_high_z','example_prefix','same_token_low_z','same_token_low_seq_id','same_token_low_position','same_token_low_prefix']:row[k]=''
  ordinary_candidates=np.flatnonzero(theld[rows])
  if len(ordinary_candidates):
   oi=ordinary_candidates[np.argsort(vals[ordinary_candidates])[len(ordinary_candidates)//2]];op=int(rows[oi]);oj=int(docindex[op]);ot=int(positions[op]);row.update(ordinary_token_id=int(token[op]),ordinary_token=tok.decode([int(token[op])],skip_special_tokens=False),ordinary_z=float(vals[oi]),ordinary_seq_id=docs[oj]['seq_id'],ordinary_position=ot,ordinary_prefix=tok.decode(docs[oj]['token_ids'][:ot],skip_special_tokens=False))
  else:
   for k in ['ordinary_token_id','ordinary_token','ordinary_z','ordinary_seq_id','ordinary_position','ordinary_prefix']:row[k]=''
table('token_member_summary.csv',tokenrows);table('high_response_token_counts.csv',eventrows);table('real_token_examples.csv',examples)
math_token_counts=collections.Counter(token[labels[docindex]==1].tolist());bio_token_counts=collections.Counter(token[labels[docindex]==0].tolist())
table('panel_token_counts.csv',(dict(token_id=int(t),token_string=tok.decode([int(t)],skip_special_tokens=False),count=int(n),math_count=math_token_counts[int(t)],biology_count=bio_token_counts[int(t)],per_domain_denominator=9600,frequency_bin=['low','middle','high'][tbin[int(t)]],special=bool(t in specialids)) for t,n in zip(types,typecounts)))
tokensummary={'panel_positions':len(token),'panel_documents':D,'frequency_count_cuts':cuts.tolist(),'type_counts':[int((np.array(list(tbin.values()))==i).sum()) for i in range(3)],'position_counts':np.bincount(eventbin,minlength=3).tolist(),'baseline':baseline.tolist(),'special_positions':sum(vocabcounts.get(t,0) for t in specialids),'groups':{}}
for g in ranked:
 good=[r for r in tokenrows if r['domain_bias']==g and r['usable']];props=np.array([[r[k] for k in ['low','middle','high']] for r in good]);fids=np.array([r['feature_id'] for r in good]);tm=np.array([r['token_count_median'] for r in good]);valid=(rate[fids]>0)&(tm>0)
 rho=stats.spearmanr(rate[fids[valid]],tm[valid]).statistic if valid.sum()>2 else np.nan
 tokensummary['groups'][g]={'main_members':len(sets['main_'+g]),'usable':len(good),'excluded_insufficient':len(sets['main_'+g])-len(good),'member_mean_token_bins':props.mean(0).tolist() if len(good) else None,'member_median_token_bins':np.median(props,axis=0).tolist() if len(good) else None,'spearman_feature_rate_vs_panel_token_count':float(rho) if np.isfinite(rho) else None,'scatter_nonzero_reference_members':int(valid.sum())}
dump(A/'tokens.json',tokensummary);np.savez_compressed(A/'token_thresholds.npz',positive_z_p90=threshold)
log(f"Token bins count thresholds={cuts.tolist()}; usable={[tokensummary['groups'][g]['usable'] for g in ranked]}")

# Paired context/target-plus-suffix effects. Family bootstrap carries all conditions together.
panel=lines(B/'R07_fixed_target_domain_spectrum_20261029/data/panel.jsonl');target=load(B/'R08_within_mixed_subspaces_20261029/forward/target_readings.npz');tz=target['z'];tidlist=list(target['seq_ids']);pr={r['seq_id']:r for r in panel}
contextrows=[];familyrows=[];contextflags={};contextarrays={};prefixchecks=[];targetids={}
for split in ['discovery','development','heldout']:
 families=sorted({r['family'] for r in panel if r['split']==split});arr=np.empty((len(families),2,2,2,len(main)),np.float64)
 for fi,fam in enumerate(families):
  for di,dom in enumerate(['math','biology']):
   for w in [0,1]:
    for e in [0,1]:
     sid=f'{fam}_{dom}_W{w}_E{e}';r=pr[sid];arr[fi,di,w,e]=tz[tidlist.index(sid),main];targetids.setdefault(e,set()).add(r['target_token_id'])
    r0,r1=pr[f'{fam}_{dom}_W{w}_E0'],pr[f'{fam}_{dom}_W{w}_E1'];prefixchecks.append(r0['core_text']==r1['core_text'])
 # arrays indexed families, domain, wording, ending, feature
 delta=arr[:,0]-arr[:,1];active=(arr>0).any((1,2,3));wgt=mult(len(families));deltaending=delta.mean(1)
 endingCI=ci(wgt@deltaending.reshape(len(families),-1)).reshape(2,2,len(main));suffix=(arr[:,:,:,1]-arr[:,:,:,0]).mean((1,2));interaction=(delta[:,: ,1]-delta[:,:,0]).mean(1)
 sci=ci(wgt@suffix);ici=ci(wgt@interaction);contextarrays[split]=dict(arr=arr,delta=delta,endingCI=endingCI,active=active,suffix=suffix,suffixCI=sci,interaction=interaction,interactionCI=ici,families=families)
 np.savez_compressed(A/f'context_{split}.npz',feature_ids=main,activation=arr,families=np.array(families),bootstrap_family_weights=wgt)
 for ki,f in enumerate(main):
  for w in [0,1]:
   for e in [0,1]:
    vals=delta[:,w,e,ki];cc=ci(wgt@vals)
    contextrows.append(dict(feature_id=int(f),domain_bias='math' if direction[f]>0 else 'biology',split=split,wording=w,ending=e,target_word='example' if e==0 else 'explanation',target_token_id=3110 if e==0 else 16148,math_mean_z=float(arr[:,0,w,e,ki].mean()),biology_mean_z=float(arr[:,1,w,e,ki].mean()),math_minus_biology=float(vals.mean()),CI_low=float(cc[0]),CI_high=float(cc[1]),active_family_count=int((arr[:,:,w,e,ki]>0).any(1).sum()),families=len(families)))
    for fi,fam in enumerate(families):familyrows.append(dict(feature_id=int(f),split=split,family=fam,wording=w,ending=e,math_z=float(arr[fi,0,w,e,ki]),biology_z=float(arr[fi,1,w,e,ki]),delta=float(vals[fi])))
dd,hh=contextarrays['discovery'],contextarrays['heldout'];categoryrows=[]
for k,f in enumerate(main):
 adequate=dd['active'][:,k].sum()>=3 and hh['active'][:,k].sum()>=3
 ctx=[]
 for e in [0,1]:
  means=np.r_[dd['delta'][:,:,e,k].mean(0),hh['delta'][:,:,e,k].mean(0)];same=(np.all(means>0) or np.all(means<0))
  ciok=all(v['endingCI'][0,e,k]*v['endingCI'][1,e,k]>0 for v in [dd,hh]);supportok=all((v['arr'][:,:,:,e,k]>0).any((1,2)).sum()>=3 for v in [dd,hh]);ctx.append(bool(same and ciok and supportok))
 def recurring(key):
  m0=dd[key][:,k].mean();m1=hh[key][:,k].mean();return bool(adequate and m0*m1>0 and dd[key+'CI'][0,k]*dd[key+'CI'][1,k]>0 and hh[key+'CI'][0,k]*hh[key+'CI'][1,k]>0)
 suffixok=recurring('suffix');intok=recurring('interaction');ctxok=any(ctx)
 cat='both_or_interaction' if (ctxok and suffixok) or intok else 'context_response' if ctxok else 'target_suffix_sensitive' if suffixok else 'insufficient'
 row=dict(feature_id=int(f),domain_bias='math' if direction[f]>0 else 'biology',context_example=ctx[0],context_explanation=ctx[1],context_any=ctxok,context_both=all(ctx),target_suffix_recurrent=suffixok,interaction_recurrent=intok,category=cat,discovery_active_families=int(dd['active'][:,k].sum()),heldout_active_families=int(hh['active'][:,k].sum()),all_fixed_target_zero=bool(not any(contextarrays[s]['active'][:,k].any() for s in contextarrays)),context_direction_agrees_natural=bool(ctxok and all(np.sign(hh['delta'][:,:,e,k].mean())==direction[f] for e in [0,1] if ctx[e])),heldout_suffix_effect=float(hh['suffix'][:,k].mean()),heldout_suffix_CI_low=float(hh['suffixCI'][0,k]),heldout_suffix_CI_high=float(hh['suffixCI'][1,k]),heldout_interaction=float(hh['interaction'][:,k].mean()),heldout_interaction_CI_low=float(hh['interactionCI'][0,k]),heldout_interaction_CI_high=float(hh['interactionCI'][1,k]))
 categoryrows.append(row);contextflags[int(f)]=row
table('context_effects.csv',contextrows);table('context_family_pairs.csv',familyrows);table('context_categories.csv',categoryrows)
contextsummary={'target_ids':{str(k):sorted(v) for k,v in targetids.items()},'ending_core_same_all':all(prefixchecks),'pure_identity_test':'MISSING / NOT RUN','groups':{}}
for g in ranked:
 rows=[r for r in categoryrows if r['domain_bias']==g];contextsummary['groups'][g]={k:sum(r[k] for r in rows) for k in ['context_any','context_both','target_suffix_recurrent','interaction_recurrent','all_fixed_target_zero']};contextsummary['groups'][g]['categories']=dict(collections.Counter(r['category'] for r in rows));contextsummary['groups'][g]['main_members']=len(rows)
dump(A/'context.json',contextsummary)

# Old/new mapping keeps every definition separate.
old=js(S/'analysis/candidate_freeze.json')['dictionaries']['CC']['groups'];oldsets={k:np.array(v if isinstance(v,list) else v.get('feature_ids',v.get('ids',[])),int) for k,v in old.items()}
r9=js(B/'R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json')
for k,v in r9['domain_candidates'].items():oldsets['R09_'+k+'64']=np.array(v,int)
for k,v in r9['top32_by_ending'].items():oldsets['R09_contribution_top32_ending'+k]=np.array(v,int)
oldsets['R09_union141']=np.array(r9['all_candidates'],int)
with track(B/'R09_domain_difference_decomposition_20261029/tables/domain_candidate_replication.csv').open() as fp:rr=list(csv.DictReader(fp))
oldsets['R09_recurrent36']=np.array([int(r['feature_id']) for r in rr if r['cross_condition_replication'].lower()=='true'],int)
oldmeeting=js(B/'meeting_five_20261030/freeze.json')
for g in ['math','biology']:
 v=oldmeeting.get('groups',{}).get(g,oldmeeting.get('sets',{}).get(g,[]))
 if isinstance(v,dict):v=v.get('feature_ids',v.get('ids',[]))
 if not v:v=oldmeeting.get(g,[])
 if isinstance(v,list) and v:oldsets['previous_meeting_'+g+'16']=np.array(v,int)
table('old_new_list_mapping.csv',(dict(feature_id=f,main=bool(selected[f]),domain_bias='math' if direction[f]>0 else 'biology' if direction[f]<0 else 'tie',**{k:bool(f in ids) for k,ids in {**sets,**oldsets}.items()}) for f in range(F)))
table('old_list_intersections.csv',(dict(old_definition=k,old_count=len(v),new_main_math=len(set(v)&set(idsm)),new_main_biology=len(set(v)&set(idsb))) for k,v in oldsets.items()))

master=[]
for g in ranked:
 for ranki,f in enumerate(sets['main_'+g]):
  tr=tokenresults[int(f)];ct=contextflags[int(f)];low,high=cis['heldout']
  master.append(dict(feature_id=int(f),dictionary='A22_999997440_09b432e98dd7',domain_bias=g,discovery_rank=ranki+1,discovery_raw_auc=float(raw[f]),discovery_oriented_auc=float(oriented[f]),development_raw_auc=float(aucs['development'][f]),heldout_raw_auc=float(aucs['heldout'][f]),heldout_oriented_auc=float(aucs['heldout'][f] if direction[f]>0 else 1-aucs['heldout'][f]),heldout_CI_low=float(low[f]),heldout_CI_high=float(high[f]),heldout_direction_agrees=bool(np.sign(aucs['heldout'][f]-.5)==direction[f]),heldout_interval_support=bool(reps['heldout'][f]),discovery_math_active_docs=int(sm[f]),discovery_biology_active_docs=int(sb[f]),heldout_math_active_docs=int((counts[ix['heldout'][labels[ix['heldout']]==1],f]>0).sum()),heldout_biology_active_docs=int((counts[ix['heldout'][labels[ix['heldout']]==0],f]>0).sum()),DCLM_hits=int(hits[f]),DCLM_denominator=refN,DCLM_feature_occurrence=float(rate[f]),frequency_original=['low','middle','high','insufficient'][freq[f]],frequency_log=['low','middle','high','insufficient'][logfreq[f]],decoder_status='OK' if nz[f] else 'ZERO_NORM',spectrum_full_sum=float(power[f].sum()),token_threshold=tr['positive_z_p90'],token_high_events=tr['heldout_high_events'],token_high_documents=tr['heldout_high_documents'],token_status='OK' if tr['usable'] else 'INSUFFICIENT',context_status=ct['category'],context_active_heldout_families=ct['heldout_active_families'],pure_identity_B='NOT_RUN',new_model_forwards=0))
table('master_members.csv',master)
table('all_dictionary_screen.csv',(dict(feature_id=f,support_qualified=bool(support[f]),discovery_math_active_docs=int(sm[f]),discovery_biology_active_docs=int(sb[f]),discovery_raw_auc=float(raw[f]),discovery_oriented_auc=float(oriented[f]),domain_bias='math' if direction[f]>0 else 'biology' if direction[f]<0 else 'tie',main=bool(selected[f]),DCLM_feature_occurrence=float(rate[f]),frequency=['low','middle','high','insufficient'][freq[f]],exclusion_reason='' if support[f] else 'no_positive_discovery' if sm[f]+sb[f]==0 else 'under5_documents_in_both_domains') for f in range(F)))
table('flow_counts.csv',[dict(stage='dictionary',math='',biology='',total=F),dict(stage='active_discovery',math='',biology='',total=freeze['positive_any_discovery']),dict(stage='support_eligible',math=int((support&(direction>0)).sum()),biology=int((support&(direction<0)).sum()),total=int(support.sum())),dict(stage='main_AUC075',math=len(idsm),biology=len(idsb),total=len(main)),dict(stage='heldout_exploratory_CI_support',math=int(reps['heldout'][idsm].sum()),biology=int(reps['heldout'][idsb].sum()),total=int(reps['heldout'].sum()))])

# Sensitivity uses same frozen spectrum and counts; never changes main.
sens=[]
for prefix in ['main','auc0.70','auc0.80','top16','top64','top128']:
 qm2=power[sets[prefix+'_math']].mean(0);qb2=power[sets[prefix+'_biology']].mean(0)
 for g in ranked:
  ids=sets[prefix+'_'+g];valid=ids[freq[ids]<3]
  sens.append(dict(selection=prefix,domain_bias=g,members=len(ids),frequency_valid=len(valid),low_share=float((freq[valid]==0).mean()),middle_share=float((freq[valid]==1).mean()),high_share=float((freq[valid]==2).mean()),head_mean=float(band[ids,0].mean()),head_median=float(np.median(band[ids,0])),PC1_mean=float(power[ids,0].mean()),PC2_64_mean=float(power[ids,1:64].sum(1).mean()),overlap_pc=float(np.minimum(qm2,qb2).sum()),overlap_band=float(np.minimum(bands(qm2),bands(qb2)).sum())))
table('sensitivity_summary.csv',sens)
results={'flow':{k:freeze[k] for k in ['universe','positive_any_discovery','support_qualified','rejected_no_discovery_activation','rejected_positive_but_under5_each','eligible_auc_ties']},'main_sizes':{g:len(sets['main_'+g]) for g in ranked},'heldout_interval_supported':{g:int(reps['heldout'][sets['main_'+g]].sum()) for g in ranked},'reference_positions':refN,'zero_norm_all':int((~nz).sum()),'new_forwards':0,'training_updates':0,'geometry':geometry,'tokens':tokensummary,'context':contextsummary,'scientific_acceptance':'Unknown'}
dump(A/'results.json',results);dump(A/'numerical_checks.json',checks)
manifest=[]
for p in sorted(sources):
 p=Path(p);manifest.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
dump(O/'source_manifest.json',{'files':manifest,'new_model_forwards':0,'old_outputs_written':0})
log(json.dumps({'main':results['main_sizes'],'context':contextsummary['groups'],'checks':checks},indent=2))
