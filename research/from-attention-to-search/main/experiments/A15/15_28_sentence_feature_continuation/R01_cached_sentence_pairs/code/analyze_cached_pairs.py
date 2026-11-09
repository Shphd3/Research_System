from core import *
import pandas as pd
from datetime import datetime,timezone
import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)
def aggregate(k,base,match,out,counts):
 ids=np.flatnonzero(match[:,1]>0);ba=base[ids];ma=match[ids];y=out[ids];cnt=counts[ids];N=len(ids)
 np.savez_compressed(R/f'results/matched_{k}.npz',base_indices=ids,pairs=np.c_[ba[:,:2],ma[:,0]],values=y,counts=cnt)
 meta=pd.DataFrame(ba[:,2:],columns=['doc','sid','block','domain','distance','distance_bin','class','same_id']);meta['q']=np.arange(N);meta['tier']=ma[:,1];meta['narrow']=ma[:,2]
 cells=[];wrow=[];wcol=[];wval=[];blockdata=[];sentence_tables=[];document_tables=[];allreal=[]
 grouping=['domain','tier','class','same_id','distance_bin']
 for g in range(5):
  for m in range(1 if k=='SAE' else 7):
   ar=pd.DataFrame(base[:,[2,3,4,5,7,8,9]],columns=['doc','sid','block','domain','distance_bin','class','same_id']);ar['real']=out[:,g,m,0];ar=ar.dropna()
   if len(ar):
    ar=ar.groupby(['domain','class','same_id','distance_bin','block','doc','sid'],as_index=False).real.mean().groupby(['domain','class','same_id','distance_bin','block','doc'],as_index=False).real.mean().groupby(['domain','class','same_id','distance_bin','block'],as_index=False).real.mean().groupby(['domain','class','same_id','distance_bin'],as_index=False).real.mean();ar['dictionary']=k;ar['frequency']=GROUPS[g];ar['metric']=METRICS[m];allreal.append(ar)
   good=np.isfinite(y[:,g,m,:]).all(1);df=meta[good].copy();df['real']=y[good,g,m,0];df['control']=y[good,g,m,1];df['delta']=df.real-df.control
   for c in range(4):df[f'den{c}']=cnt[good,g,c]
   sens=df[(df.tier==1)&(df.narrow==1)].copy();sens['tier']=3;df=pd.concat([df,sens],ignore_index=True)
   if not len(df):continue
   sent=df.groupby(grouping+['block','doc','sid'],as_index=False).agg(real=('real','mean'),control=('control','mean'),delta=('delta','mean'),pairs=('q','size'))
   sent['dictionary']=k;sent['frequency']=GROUPS[g];sent['metric']=METRICS[m];sentence_tables.append(sent)
   doc=sent.groupby(grouping+['block','doc'],as_index=False)[['real','control','delta']].mean();doc['dictionary']=k;doc['frequency']=GROUPS[g];doc['metric']=METRICS[m];document_tables.append(doc)
   for key,dfc in df.groupby(grouping,sort=True):
    dom,tier,cl,eq,db=map(int,key);cid=len(cells)
    ss=dfc.groupby(['block','doc','sid'],as_index=False)[['real','control','delta']].mean();dd=ss.groupby(['block','doc'],as_index=False)[['real','control','delta']].mean();bb=dd.groupby('block')[['real','control','delta']].mean();nb=len(bb)
    # Exact equal pair/sentence/document/block weights on the observed eligible mask.
    ww=1/dfc.groupby(['block','doc','sid'])['q'].transform('size').to_numpy()
    ns=ss.groupby(['block','doc']).size();nd=dd.groupby('block').size()
    ww*=np.array([1/ns.loc[(int(b),int(d))]/nd.loc[int(b)]/nb for b,d in zip(dfc.block,dfc.doc)])
    assert abs(ww.sum()-1)<1e-9
    wrow.extend([cid]*len(dfc));wcol.extend((dfc.q.to_numpy()*35+g*7+m).tolist());wval.extend(ww.tolist())
    blockmat=np.full((30,3),np.nan);blockmat[bb.index.to_numpy()]=bb.to_numpy();blockdata.append(blockmat)
    cell=dict(cell=cid,dictionary=k,domain=['math','biology'][dom],domain_id=dom,tier=int(tier),pair_class=['lexical','whitespace','punctuation','other'][cl],class_id=cl,same_id=eq,distance=DIST[db],distance_bin=db,frequency=GROUPS[g],group=g,metric=METRICS[m],metric_id=m,real=float(bb.real.mean()),control=float(bb.control.mean()),delta=float(bb.delta.mean()),pairs=len(dfc),sentences=len(ss),documents=len(dd),blocks=nb,one_doc_blocks=int((nd==1).sum()),source_count_mean=float(dfc.den0.mean()),lost_real_mean=float(dfc.den1.mean()),lost_control_mean=float(dfc.den2.mean()),common_lost_mean=float(dfc.den3.mean()),primary=tier==1 and cl==0 and g<3 and m<3)
    cells.append(cell)
 W=sparse.csr_matrix((wval,(wrow,wcol)),shape=(len(cells),N*35));sparse.save_npz(R/f'results/weights_{k}.npz',W);np.save(R/f'results/blocks_{k}.npy',np.array(blockdata));dump(R/f'results/cells_{k}.json',cells)
 pd.concat(sentence_tables).to_csv(R/f'results/sentence_metrics_{k}.csv.gz',index=False);pd.concat(document_tables).to_csv(R/f'results/document_metrics_{k}.csv.gz',index=False);pd.concat(allreal).to_csv(R/f'results/unmatched_population_real_{k}.csv',index=False)
 assert np.allclose(W@np.nan_to_num((y[:,:,:,0]-y[:,:,:,1]).reshape(-1)),[c['delta'] for c in cells],atol=1e-12)
 print(k,'aggregate',N,'matched,',len(cells),'cells,',W.nnz,'weights',flush=True)

def bootstrap():
 rng=np.random.default_rng(20261030);boot=[rng.multinomial(30,np.repeat(1/30,30),size=5000) for _ in range(2)];np.savez_compressed(R/'results/bootstrap_counts.npz',math=boot[0],biology=boot[1]);records=[];qmax=np.zeros(5000)
 for k in ['SAE','CC']:
  cs=json.loads((R/f'results/cells_{k}.json').read_text());bv=np.load(R/f'results/blocks_{k}.npy')
  for c,b in zip(cs,bv):
   valid=np.isfinite(b[:,2]);n=valid.sum();bc=boot[c['domain_id']];den=bc@valid.astype(float);missing=int((den==0).sum());draw=bc@np.nan_to_num(b)/den[:,None]
   c['missing_bootstrap_draws']=missing;c['se']=float(np.std(b[valid,2],ddof=1)/np.sqrt(n)) if n>=2 else None;c['interval_available']=bool(missing==0 and n>=2 and c['se']>0)
   for z,nm in enumerate(['real','control','delta']):
    lo,hi=np.quantile(draw[:,z],[.025,.975]) if missing==0 and n>=2 else [np.nan,np.nan];c[nm+'_point_lo']=float(lo);c[nm+'_point_hi']=float(hi)
   if c['primary'] and c['interval_available']:qmax=np.maximum(qmax,np.abs((draw[:,2]-c['delta'])/c['se']))
   records.append(c)
 q=float(np.quantile(qmax,.95))
 for c in records:
  if c['primary'] and c['interval_available']:
   c['simultaneous_lo']=c['delta']-q*c['se'];c['simultaneous_hi']=c['delta']+q*c['se'];c['matched_verdict']='POSITIVE_MATCHED' if c['simultaneous_lo']>0 else ('NONPOSITIVE_MATCHED' if c['simultaneous_hi']<=0 else 'INSUFFICIENT_INTERVAL')
  else:c['simultaneous_lo']=None;c['simultaneous_hi']=None;c['matched_verdict']='INSUFFICIENT_INTERVAL' if c['primary'] else 'DIAGNOSTIC'
 dump(R/'results/cells_intervals.json',records)
 # Full predefined primary ledger retains absent cells.
 ledger=[]
 for dom in ['math','biology']:
  for k,m in [('SAE','identity'),('CC','identity'),('CC','forward'),('CC','reverse')]:
   for g in GROUPS[:3]:
    for db in range(7):
     for eq in range(2):
      found=[c for c in records if c['primary'] and c['domain']==dom and c['dictionary']==k and c['metric']==m and c['frequency']==g and c['distance_bin']==db and c['same_id']==eq]
      ledger.append(found[0] if found else dict(domain=dom,dictionary=k,metric=m,frequency=g,distance=DIST[db],same_id=eq,matched_verdict='UNAVAILABLE_NO_MATCH_OR_DENOMINATOR',pairs=0,blocks=0))
 assert len(ledger)==336;pd.DataFrame(ledger).to_csv(R/'results/primary_336.csv',index=False);pd.DataFrame(records).to_csv(R/'results/all_cells.csv',index=False)
 dump(R/'provenance/bootstrap.json',dict(draws=5000,simultaneous_max_abs_quantile=q,primary_family=336,estimable_primary=sum(c.get('interval_available',False) for c in ledger),all_cells=len(records)))

def main():
 synthetic();base=np.load(R/'data/base_pairs.npz')['pairs'];a,b=graph()
 freeze={'time':datetime.now(timezone.utc).isoformat(),'files':{str(p.relative_to(R)):sha(p) for p in list((R/'code').glob('*.py'))+[R/'config.json',R/'data/sentence_manifest.jsonl',R/'data/matches_SAE.npz',R/'data/matches_CC.npz']},'protocol_sha256':sha('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol.md'),'graph_sha256':sha(GRAPH)}
 assert not (R/'provenance/outcome_freeze.json').exists();dump(R/'provenance/outcome_freeze.json',freeze)
 for k in ['SAE','CC']:
  start=time.time();B,ptr,ids,g=load_data(k);mt=np.load(R/f'data/matches_{k}.npz')['matches'];pairs=np.c_[base[:,:2],mt[:,0]]
  fw,rv=coverage(B,ptr,ids,np.arange(len(B)),*adjacency(a,b)) if k=='CC' else (np.zeros((1,1),bool),np.zeros((1,1),bool))
  out,cnt=measure(B,ptr,ids,g,pairs,fw,rv,k=='CC');np.savez_compressed(R/f'results/pair_metrics_{k}.npz',values=out,counts=cnt)
  print(k,'measure secs',time.time()-start,flush=True);aggregate(k,base,mt,out,cnt);del B,fw,rv,out,cnt
 bootstrap();dump(R/'provenance/observed_completed.json',dict(time=datetime.now(timezone.utc).isoformat(),status='OBSERVED_AND_BOOTSTRAP_COMPLETE_NULLS_PENDING'))
if __name__=='__main__':main()
