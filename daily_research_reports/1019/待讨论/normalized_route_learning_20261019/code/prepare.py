from common import *
import importlib.util,argparse

def run():
 t=time.time();(ROOT/'cache').mkdir(exist_ok=True);(ROOT/'routes').mkdir(exist_ok=True)
 g=json.load(open(OLD/'cache/grouping.json'));pool=np.array(g['support_pool']);L=np.array(g['low_ids']);high=np.array(g['high_ids']);top=np.array(json.load(open(PREV/'metrics/core/T10.json'))['feature_ids']);own=np.load(PREV/'metrics/core/owners.npz')
 c=loadcache('train');z=csr(c);x=csr(c,True);n=np.bincount(c['feature_ids'].numpy(),minlength=FCOUNT);p=n/len(c['target']);weights=np.zeros(FCOUNT)
 for row in csv.DictReader(open(OLD/'tables/feature_members.csv')):weights[int(row['feature_id'])]=float(row['sum14_decoder_l2_norm']);assert abs(p[int(row['feature_id'])]-float(row['train_p']))<1e-12
 sumz=np.asarray(z.astype(np.float64).sum(0)).ravel();m=np.divide(sumz*weights,n,out=np.zeros(FCOUNT),where=n>0);pm=p*m
 fm=np.median(m[pool][m[pool]>0])*1e-6;fpm=np.median(pm[pool][pm[pool]>0])*1e-6
 invm=np.divide(1,np.maximum(m,fm),out=np.zeros_like(m),where=m>0);invpm=np.divide(1,np.maximum(pm,fpm),out=np.zeros_like(pm),where=pm>0)
 scale_sum=0.
 for a in range(0,len(c['target']),4096):scale_sum+=float(c['hidden'][a:a+4096].double().square().sum())
 scale=math.sqrt(scale_sum/(len(c['target'])*D));np.savez(ROOT/'cache/train_stats.npz',p=p,m=m,pm=pm,weights=weights,pool=pool,low=L,high=high,top10=top,scale=scale,invm=invm,invpm=invpm)
 modspec=importlib.util.spec_from_file_location('legacy_prepare',OLD/'code/prepare_cache.py');mod=importlib.util.module_from_spec(modspec);modspec.loader.exec_module(mod)
 denom=dict(m_floor=fm,pm_floor=fpm,m_zero=int((m[pool]==0).sum()),pm_zero=int((pm[pool]==0).sum()),m_floor_triggers=int(((m[pool]>0)&(m[pool]<fm)).sum()),pm_floor_triggers=int(((pm[pool]>0)&(pm[pool]<fpm)).sum()),positive_reference='original9615 reliable pool; shared by T/R11',groups={})
 memberrows=[];sourcerec=json.load(open(OLD/'provenance/cache_preparation_receipt.json'));mu={};summ=[]
 for group in ['T','R11']:
  labels=own[group];sizes=np.bincount(labels[labels>=0],minlength=8);assert sizes.tolist()==[1257,1347,1506,1629,1824,1189,523,330]
  s0=mod.score_matrix(z.astype(np.float64),labels,sizes,weights);mu[group]=s0.astype(np.float64).mean(0);floor=np.median(mu[group][mu[group]>0])*1e-6
  identity=np.array([(p[labels==e]*m[labels==e]).sum()/sizes[e] for e in range(8)])
  assert np.allclose(mu[group],identity,rtol=1e-7,atol=1e-12)
  denom['groups'][group]=dict(mu=mu[group].tolist(),floor=floor,zero=int((mu[group]==0).sum()),floor_triggers=int(((mu[group]>0)&(mu[group]<floor)).sum()),identity_max_abs=float(abs(identity-mu[group]).max()),sizes=sizes.tolist())
  for i in pool:memberrows.append(dict(grouping=group,feature_id=i,p=p[i],m=m[i],p_m=pm[i],weight_sum14=weights[i],owner=labels[i],is_low=int(i in L),is_top10=int(i in top)))
 for split in ['train','eval']:
  c=loadcache(split);z=csr(c).astype(np.float64);source=sourcerec['inputs']['sources'][0 if split=='train' else 1]['sha256']
  # Full next-token alignment, labels may never be read as route input.
  sourcepath=sourcerec['inputs']['sources'][0 if split=='train' else 1]['path'];tokens=np.memmap(sourcepath,dtype=np.uint32,mode='r');pos=c['position_id'].numpy();assert np.array_equal(tokens[pos+1].astype(np.int64),c['target'].numpy());assert (pos%1024<1023).all()
  for group in ['T','R11']:
   labels=own[group];sizes=np.bincount(labels[labels>=0],minlength=8)
   for s in range(4):
    s0=mod.score_matrix(z,labels,sizes,weights*(invm if s==2 else invpm if s==3 else 1))
    if s==1:
     floor=denom['groups'][group]['floor'];s0=np.divide(s0,np.maximum(mu[group],floor),out=np.zeros_like(s0),where=mu[group]>0)
    assert np.isfinite(s0).all() and (s0>=0).all();r,tie=mod.fixed_route(s0,c,CFG['tie_seed'],source);name=f'{group}_S{s}';np.savez_compressed(ROOT/'routes'/f'{split}_{name}.npz',score=s0,route=r)
    if s==0:
     prev=np.load(PREV/'routes'/f'{split}_{group}.npz');assert np.array_equal(r,prev['route']),'S0 route mismatch'
    ep=ROOT/'metrics/exposure'/f'{split}_{name}.json'
    ss=json.load(open(ep)) if ep.exists() else exposure(split,r,name,labels);ss.update(tie);summ.append(ss)
 csvwrite(ROOT/'tables/group_members.csv',memberrows);write_json(ROOT/'provenance/denominators.json',denom);write_json(ROOT/'metrics/routing_summary.json',summ)
 # Register target and probe before any training results.
 c=loadcache('train');x=csr(c,True).tocsc();chosen=None
 for threshold in [256,200]:
  for i in sorted(L):
   hits=x.indices[x.indptr[i]:x.indptr[i+1]];contexts=len(np.unique(c['block_id'][hits].numpy()))
   if len(hits)>=threshold and contexts>=20:chosen=dict(feature_id=int(i),TRAIN_hits=len(hits),TRAIN_contexts=contexts,threshold=threshold);break
  if chosen:break
 write_json(ROOT/'config/target.json',chosen or dict(status='NOT RUN',reason='no TRAIN eligible target'))
 e=loadcache('eval');rng0=np.random.default_rng(20261019);blocks=e['block_id'].numpy();sample=[]
 for b in sorted(np.unique(blocks)):
  ix=np.flatnonzero(blocks==b);sample.extend(rng0.permutation(ix).tolist())
 # Round-robin contexts, then cap; preserve equal context opportunity.
 by=[rng0.permutation(np.flatnonzero(blocks==b)) for b in sorted(np.unique(blocks))];general=np.array([a[j] for j in range(max(map(len,by))) for a in by if len(a)>j][:1024]);low=np.flatnonzero(e['mask_low'].numpy());extra=rng0.choice(low,min(512,len(low)),replace=False);probe=np.unique(np.r_[general,extra]);np.save(ROOT/'config/probe.npy',probe)
 write_json(ROOT/'provenance/preparation_receipt.json',dict(status='COMPLETE',seconds=time.time()-t,scale=scale,source_labels='all TRAIN/EVAL targets equal source[position+1], no cross-context label',S0_routes_reproduce_previous=True,train_only=True,probe_N=len(probe),target=chosen,precision='FP64 sparse accumulation rounded FP32, exact saved FP32 argmax',no_model_inference=True))
 print('PREPARATION COMPLETE',time.time()-t,flush=True)
if __name__=='__main__':run()
