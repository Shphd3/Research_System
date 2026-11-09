from engine import *
import sys,time
site=sys.argv[1];tag=sys.argv[2];mode=sys.argv[3];long='--long' in sys.argv;output=R/'cache'/f'{site}__{tag}__{mode}{"__long" if long else ""}.npz';assert not output.exists();features=SEL[site]['features'];support=split_support(site,tag);n=support.shape[1];patterns=None
patfile=R/'data'/f'{site}__discovery_directions.npz'
if patfile.exists():patterns=np.load(patfile)['patterns']
realq,realhist,codes,_=joint(support,features,patterns)
if tag=='discovery' and mode=='position':
 codesi,counts=np.unique(codes,return_counts=True);patterns=codesi[np.lexsort((codesi,-counts))[:8]]
assert patterns is not None
jq,jh,jc,jp=joint(support,features,patterns);realJ,realI=kernels(support);realstats=pair_stats(realJ,realI);qnull=[];jnull=[];inull=[];curvenull=[];fullnull=[];histnull=[];patnull=[];qdocsum=np.zeros_like(jq);audits=[];snapshots={};burntrace=[];start=time.time();siteidx=SITES.index(site);tagidx=['discovery','heldout'].index(tag);modeidx=['position','position_token3'].index(mode);burn=500 if long else PLAN['burn_sweeps'];thin=50 if long else PLAN['thin_sweeps']
for chain in range(4):
 states=[]
 for d,ds in enumerate(DATASETS):
  for t in range(8):
   tokens=np.array([PANEL[i]['position_token_ids'][t] for i in INDEX[ds+'__'+tag]])
   labels=np.zeros(n,int) if mode=='position' else np.array([TOK.index(int(v))+1 if v in TOK else 0 for v in tokens])
   for label in sorted(set(labels)):
    rowsi=np.where(labels==label)[0];seed=PLAN['seed']+siteidx*1000000+tagidx*100000+modeidx*10000+chain*1000+d*100+t*5+int(label);obj=Sampler(support[d,rowsi,t],seed);states.append((d,t,int(label),rowsi,obj))
 # Diagnostic burn snapshots are NOT retained for null estimation.
 for step in [0,10,25,50,burn]:
  if step==0:prev=0
  for d,t,label,rr,obj in states:
   obj.advance(step-prev);a=obj.snapshot();burntrace.append(dict(chain=chain,dataset=DATASETS[d],quantile=t,token_class=label,sweep=step,retention=obj.retention[-1]))
  prev=step
 # Reset retention checks to post-burn only, while keeping total proposal counters.
 for *_,obj in states:obj.retention=[];obj.hashes=[];obj.checks=0
 for draw in range(64):
  current=support.copy()
  for d,t,label,rr,obj in states:obj.advance(thin);current[d,rr,t]=obj.snapshot()
  q,h,c,p=joint(current,features,patterns);js,ins=kernels(current);st,ist,cu,fu=pair_stats(js,ins);qnull.append(q.mean(1));qdocsum+=q;jnull.append(st);inull.append(ist);curvenull.append(cu);fullnull.append(fu);histnull.append(h);patnull.append(p)
  if draw in [0,63]:snapshots[f'chain{chain}_draw{draw}']=current
  if draw%32==0:print(site,tag,mode,'chain',chain,'draw',draw,'seconds',round(time.time()-start,2),flush=True)
 for d,t,label,rr,obj in states:
  audits.append(dict(site=site,split=tag,mode=mode,chain=chain,dataset=DATASETS[d],quantile=t,token_class=label,**obj.audit()));obj.close()
np.savez_compressed(output,qnull=np.array(qnull).reshape(4,64,3,276),Jnull=np.array(jnull).reshape(4,64,6),Inull=np.array(inull).reshape(4,64,6),curvature_null=np.array(curvenull).reshape(4,64,6),fullcross_null=np.array(fullnull).reshape(4,64,3),histnull=np.array(histnull).reshape(4,64,3,25),patnull=np.array(patnull).reshape(4,64,3,9),qdoc_null_mean=qdocsum/256,realq=jq,realhist=jh,realpat=jp,realJ=realJ,realI=realI,realstats=realstats[0],real_intersections=realstats[1],real_curvature=realstats[2],real_fullcross=realstats[3],patterns=patterns,features=np.array(features),pair_featureIDs=np.array([[features[i],features[j]] for i,j in PAIRS]))
np.savez_compressed(R/'cache'/f'{site}__{tag}__{mode}{"__long" if long else ""}__audit_snapshots.npz',**snapshots)
jsonl(R/'evidence'/f'{site}__{tag}__{mode}{"__long" if long else ""}__constraints.jsonl',audits);table(R/'tables'/f'{site}__{tag}__{mode}{"__long" if long else ""}__burn_trace.csv',burntrace)
dump(R/'evidence'/f'{site}__{tag}__{mode}{"__long" if long else ""}__complete.json',dict(UTC=now(),status='COMPLETED',seconds=time.time()-start,rows_per_source=n,null_panels=256,source_cache_sha256=sha(S08/'cache/activations.npz'),sampler_cpp_sha256=sha(R/'code/curveball.cpp'),output_sha256=sha(output)))
print('NULL_COMPLETE',str(output),'seconds',time.time()-start,flush=True)
