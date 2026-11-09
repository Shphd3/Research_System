from common import *
import numpy as np
from scipy.sparse import csr_matrix
import itertools,time
start=__import__('time').time();plan=json.load(open(R/'frozen_plan.json'));panel=rows(R/'data/panel.jsonl');ids=[p['id'] for p in panel];lookup={x:i for i,x in enumerate(ids)};Nall=len(ids);controls=json.load(open(R/'data/control_selections.json'));lex=json.load(open(R/'data/lexical_control_tokens.json'));rng=np.random.default_rng(plan['seed']);cache=np.load(R/'cache/activations.npz');assert list(cache['ids'])==ids
ordered=lambda ii:np.array(sorted(ii,key=lambda i:hashlib.sha256(('S08'+ids[i]).encode()).hexdigest()),dtype=int)
groups={d:ordered([i for i,p in enumerate(panel) if p['dataset']==d]) for d in DATASETS}
results=[];amplitude=[];diagnostics=[];resamples={};pairpayload={};kernelpayload={};alltokenids=np.array([p['position_token_ids'] for p in panel]);alllex=sorted({q['token_id'] for v in lex.values() for q in v});examples=[]

def incidence(ind,val):
 rr=np.repeat(np.arange(len(ind)),ind.shape[1]);use=val.ravel()>0
 b=csr_matrix((np.ones(use.sum(),dtype=np.float64),(rr[use],ind.ravel()[use])),shape=(len(ind),30000));s=csr_matrix((val.ravel()[use].astype(float),(rr[use],ind.ravel()[use])),shape=b.shape);return b,s

def jmatrix(ind,val,withamp=False):
 b,s=incidence(ind,val);inter=(b@b.T).toarray();count=np.asarray(b.sum(axis=1)).ravel();union=count[:,None]+count[None,:]-inter;j=np.divide(inter,union,out=np.zeros_like(inter),where=union>0)
 if not withamp:return j
 s2=s.copy();s2.data**=2;part=(s2@b.T).toarray();squared=np.maximum(part+part.T-2*(s@s.T).toarray(),0);amp=np.sqrt(np.divide(squared,inter,out=np.full_like(inter,np.nan),where=inter>0));return j,amp

def masks(n):
 w=np.triu(np.ones((n,n)),1);c=np.zeros((n,n));i=np.arange(n)
 for off in range(1,(n-1)//2+1):c[i,(i+off)%n]=1
 assert w.sum()==c.sum()==n*(n-1)//2;return w,c

def stats(k,a,b,w,c,ba=None,bb=None):
 aa=k[np.ix_(a,a)];bbk=k[np.ix_(b,b)];ab=k[np.ix_(a,b)];kk=[aa,bbk,ab];mm=[w,w,c];vals=[]
 if ba is None:
  for q,m in zip(kk,mm):valid=np.isfinite(q);vals.append(float(np.sum(np.nan_to_num(q)*m)/np.sum(valid*m)))
 else:
  for q,m,x,y in zip(kk,mm,[ba,bb,ba],[ba,bb,bb]):
   valid=np.isfinite(q);num=np.einsum('bi,bi->b',x@(np.nan_to_num(q)*m),y);den=np.einsum('bi,bi->b',x@(valid*m),y);vals.append(np.divide(num,den,out=np.full_like(num,np.nan),where=den>0))
 av,bv,cv=vals;return np.array([av,bv,cv,av-cv,bv-cv,(av+bv)/2-cv])

for site in SITES:
 ind=cache[site+'__indices'];val=cache[site+'__values'];jall=[];amps=[]
 for t in range(10):
  j,amp=jmatrix(ind[:,t],val[:,t],True);jall.append(j);amps.append(amp)
 kmain=np.mean(jall[:8],axis=0);amain=np.nanmean(amps[:8],axis=0);kernelpayload[site+'__main']=kmain;kernelpayload[site+'__amplitude_main']=amain;kernelpayload[site+'__fixed32']=jall[8];kernelpayload[site+'__fixed16']=jall[9]
 lexical={}
 for tok in alllex:
  di,pi=np.where(alltokenids==tok)
  j=jmatrix(ind[di,pi],val[di,pi]);su=np.zeros((Nall,Nall));co=np.zeros_like(su);aa=np.repeat(di,len(di));bb=np.tile(di,len(di));np.add.at(su,(aa,bb),j.ravel());np.add.at(co,(aa,bb),1);lexical[tok]=(su,co)
 for d,gg in groups.items():
  act=cache[site+'__active_count'][gg,:8];z=cache[site+'__z_L2'][gg,:8];h=cache[site+'__h_L2'][gg,:8];err=cache[site+'__relative_reconstruction_error'][gg,:8];dn=cache[site+'__decoder_norm'];diagnostics.append(dict(site=site,dataset=d,N=len(gg),positions_per_doc=8,active_min=int(act.min()),active_max=int(act.max()),active_mean=float(act.mean()),z_L2_mean=float(z.mean()),z_L2_doc_SD=float(z.mean(1).std(ddof=1)),h_L2_mean=float(h.mean()),relative_reconstruction_error_mean=float(err.mean()),relative_reconstruction_error_p95=float(np.quantile(err,.95)),decoder_norm_min=float(dn.min()),decoder_norm_max=float(dn.max())))
 for A,B in itertools.combinations(DATASETS,2):
  for mode in ['main','length_matched','fixed32','fixed16','same_token']:
   a,b=groups[A],groups[B];k=kmain;strata=None
   if mode in ['length_matched','fixed32']:
    sel=next(v for v in controls if v['A']==A and v['B']==B and v['mode']==mode);a=ordered([lookup[x] for x in sel['A_ids']]);b=ordered([lookup[x] for x in sel['B_ids']]);strata=sel['strata'] if mode=='length_matched' else None
   if mode in ['fixed32','fixed16']:k=jall[8 if mode=='fixed32' else 9]
   if mode=='same_token':
    ts=[q['token_id'] for q in lex[A+'__'+B]];su=sum(lexical[t][0] for t in ts);co=sum(lexical[t][1] for t in ts);k=np.divide(su,co,out=np.full_like(su,np.nan),where=co>0);kernelpayload[site+'__same_token__'+A+'__'+B]=k
   n=len(a);assert len(b)==n and n%2==1;w,c=masks(n);m=int(w.sum());key=site+'__'+A+'__'+B+'__'+mode
   pairkey=A+'__'+B+'__'+mode
   if site==SITES[0]:pairpayload[pairkey+'__A']=a;pairpayload[pairkey+'__B']=b;pairpayload[pairkey+'__within_ij']=np.argwhere(w).astype(np.int16);pairpayload[pairkey+'__cross_ij']=np.argwhere(c).astype(np.int16)
   point=stats(k,a,b,w,c);seed=plan['seed']+int(hashlib.sha256((A+B+mode).encode()).hexdigest()[:6],16);rr=np.random.default_rng(seed);ba=rr.multinomial(n,np.full(n,1/n),size=1999).astype(float);bb=rr.multinomial(n,np.full(n,1/n),size=1999).astype(float);boots=stats(k,a,b,w,c,ba,bb);lo,hi=np.nanquantile(boots,[.025,.975],axis=1);resamples[key+'__bootstrap']=boots
   pv=None
   if mode!='same_token':
    pool=ordered(np.r_[a,b]);null=[];pr=np.random.default_rng(seed+1)
    if strata:
     bins=np.array([16,32,48,64,96,128,192,256,512,1024,2048,1e9]);stratum=np.searchsorted(bins,[panel[i]['full_token_count'] for i in pool],side='right')-1;stratum_sets=[np.where(stratum==v)[0] for v in np.unique(stratum)]
     for ss in stratum_sets:assert len(ss)%2==0
    for rep in range(999):
     if strata:
      pa=np.concatenate([pr.permutation(ss)[:len(ss)//2] for ss in stratum_sets]);mask=np.ones(len(pool),bool);mask[pa]=False;qa=ordered(pool[pa]);qb=ordered(pool[mask])
     else:
      perm=pr.permutation(len(pool));qa=ordered(pool[perm[:n]]);qb=ordered(pool[perm[n:]])
     null.append(stats(k,qa,qb,w,c)[-1])
    null=np.array(null);pv=float((1+np.sum(null>=point[-1]))/1000);resamples[key+'__permutation']=null
   row=dict(site=site,A=A,B=B,mode=mode,N_A=n,N_B=n,positions_per_doc=8 if mode in ['main','length_matched','same_token'] else 1,nominal_pairs_each=m,seed=seed,bootstrap_reps=1999,permutations=999 if pv is not None else 0,p_pooled_one_sided=pv,holm_primary=None)
   for j,label in enumerate(['within_A','within_B','cross','A_minus_cross','B_minus_cross','pooled_minus_cross']):row[label]=float(point[j]);row[label+'_lo']=float(lo[j]);row[label+'_hi']=float(hi[j])
   for label,aa,bb,mask in [('within_A',a,a,w),('within_B',b,b,w),('cross',a,b,c)]:
    kk=k[np.ix_(aa,bb)];valid=np.isfinite(kk)&(mask>0);row[label+'_actual_pairs']=int(valid.sum());row[label+'_effective_docs_left']=int(valid.any(1).sum());row[label+'_effective_docs_right']=int(valid.any(0).sum())
   results.append(row)
   if mode=='main':
    am=stats(amain,a,b,w,c);coverage={label+'_valid_position_pairs':int(np.isfinite(np.array(amps[:8])[:,aa[:,None],bb[None,:]])[:,mask>0].sum()) for label,aa,bb,mask in [('within_A',a,a,w),('within_B',b,b,w),('cross',a,b,c)]};amplitude.append(dict(site=site,A=A,B=B,N=n,positions=8,nominal_pairs_each=m,**coverage,definition='Common-coordinate raw activation RMS difference; per-position denominator=intersection count, then mean over eligible8positions. Separate from Jaccard.',within_A=float(am[0]),within_B=float(am[1]),cross=float(am[2]),pooled_minus_cross=float(am[-1])))
   print(site,A,B,mode,'N',n,'J',np.round(point[:3],6),'diff',round(point[-1],6),'CI',np.round([lo[-1],hi[-1]],6),'p',pv,'seconds',round(time.time()-start,1),flush=True)
 # Deterministic example pair from first two fixed SHA document IDs, not selected for outcome.
 for A,B in [(d,d) for d in DATASETS]+list(itertools.combinations(DATASETS,2)):
  aa=groups[A][0];bb=groups[B][1 if A==B else 0]
  for pos in [0,7]:
   ia={int(i):float(v) for i,v in zip(ind[aa,pos],val[aa,pos]) if v>0};ib={int(i):float(v) for i,v in zip(ind[bb,pos],val[bb,pos]) if v>0};shared=sorted(ia.keys()&ib.keys());examples.append(dict(site=site,A_id=ids[aa],B_id=ids[bb],quantile_index=pos,A_position=panel[aa]['positions'][pos],B_position=panel[bb]['positions'][pos],A_token=panel[aa]['position_decoded'][pos],B_token=panel[bb]['position_decoded'][pos],A_text=panel[aa]['text'],B_text=panel[bb]['text'],intersection=len(shared),union=len(ia.keys()|ib.keys()),Jaccard=len(shared)/len(ia.keys()|ib.keys()),shared_ids=shared,A_shared_values=[ia[i] for i in shared],B_shared_values=[ib[i] for i in shared],A_only=sorted(ia.keys()-ib.keys()),B_only=sorted(ib.keys()-ia.keys())))
primary=[i for i,r in enumerate(results) if r['mode']=='main'];ps=np.array([results[i]['p_pooled_one_sided'] for i in primary]);order=np.argsort(ps);adj=np.maximum.accumulate([(len(ps)-j)*ps[i] for j,i in enumerate(order)])
for j,i in enumerate(order):results[primary[i]]['holm_primary']=float(min(1,adj[j]))
for r in results:
 r['status']=('BOTH_WITHIN_HIGHER' if r['A_minus_cross_lo']>0 and r['B_minus_cross_lo']>0 and (r['holm_primary'] or r['p_pooled_one_sided'] or 0)<=.05 else 'MIXED_OR_INCONCLUSIVE');r['inference_scope']='primary Holm6' if r['mode']=='main' else 'exploratory; no primary rescue'
table(R/'tables/overlap_summary.csv',results);table(R/'tables/amplitude_supplement.csv',amplitude);table(R/'tables/SAE_diagnostics.csv',diagnostics);jsonl(R/'tables/deterministic_examples.jsonl',examples);np.savez_compressed(R/'cache/document_kernels.npz',**kernelpayload);np.savez_compressed(R/'tables/document_resamples.npz',**resamples);np.savez_compressed(R/'data/pair_graphs.npz',ids=np.array(ids),**pairpayload)
dump(R/'evidence/analysis_complete.json',dict(UTC=now(),status='COMPLETED',seconds=time.time()-start,rows=len(results),primary_tests=len(primary),code_sha256=sha(__file__),activation_sha256=sha(R/'cache/activations.npz')))
