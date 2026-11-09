from engine import *
import pandas as pd
assert not (R/'data/candidates.json').exists()
selected={}
for site in SITES:
 p,z,cache=load_stage('discovery',site);ix=per_condition(p);main=np.array([i for i,x in enumerate(p) if x['condition'].startswith('main')]);families=sorted({x['family'] for x in p});rms=np.sqrt(np.mean(z[main].astype(float)**2,axis=0));scores=np.zeros(30000);jointcount=np.zeros(30000,int);anycount=jointcount.copy()
 ds=[]
 for fam in families:
  ff=[i for i in main if p[i]['family']==fam];jointcount+=(z[ff]>0).all(0);anycount+=(z[ff]>0).any(0)
  for co in CONDS[:3]:
   aa=next(i for i in ff if p[i]['condition']==co and p[i]['gold']=='A');bb=next(i for i in ff if p[i]['condition']==co and p[i]['gold']=='B');ds.append(z[aa]-z[bb])
 response=np.sqrt(np.mean(np.array(ds,dtype=float)**2,axis=0));scores=np.divide(response,rms,out=np.zeros_like(response),where=rms>0)
 eligible=np.where((jointcount>=8)&(rms>0))[0];order=sorted(eligible,key=lambda f:(-jointcount[f],-scores[f],int(f)));Cids=[int(x) for x in order[:6]]
 eligibleR=[f for f in np.where((anycount>=6)&(rms>0))[0] if f not in Cids];Rids=[int(x) for x in sorted(eligibleR,key=lambda f:(-scores[f],int(f)))[:6]];features=Cids+Rids;assert len(features)>=2
 freq=pd.read_csv(R/f'data/{site}_reference_frequency.csv');selection=[]
 for f in features:selection.append(dict(site=site,atom=f,role='common' if f in Cids else 'responsive',common_families=int(jointcount[f]),any_main_families=int(anycount[f]),discovery_RMS=float(rms[f]),content_response_score=float(scores[f]),reference_group=str(freq.iloc[f]['group']),reference_frequency=float(freq.iloc[f]['frequency'])))
 table(R/f'tables/{site}_candidate_selection.csv',selection)
 selected[site]=dict(C=Cids,C3=Cids[:3],responsive=Rids,U=features,scale=[float(rms[f]) for f in features],selection=selection,insufficient_common=len(Cids)<3)
 print(site,'C',Cids,'R',Rids,flush=True)
dump(R/'data/candidates.json',dict(UTC=now(),rule='Protocol6; discovery only; no heldout response accessed',sites=selected))
# Nulls and discovery pair directions are fixed before opening new heldout feature data.
for si,site in enumerate(SITES):
 p,z,cache=load_stage('discovery',site);sel=selected[site];features=sel['U'];scale=np.array(sel['scale']);br,ar,pairs,ix=moments(p,z,features,scale);ids=cache[site+'__indices'];values=cache[site+'__values'];assert np.all(np.count_nonzero(values,axis=1)==32)
 binary,audits,snaps=run_binary(ids,p,features,2026110419+si*100000)
 amplitude=run_amplitude(z,p,features,scale,2026110419+si*100000+50000)
 np.savez_compressed(R/f'cache/{site}_discovery_null.npz',binary=binary,amplitude=amplitude,real_binary=br,real_amplitude=ar,pairs=pairs,features=np.array(features),scale=scale,**snaps)
 jsonl(R/f'evidence/{site}_discovery_degree_constraints.jsonl',audits)
 spec={}
 for kind,real,null in [('binary',br,binary),('amplitude',ar,amplitude)]:
  center=null.mean((0,1));res=real.mean(1)-center;sd=null.std((0,1));support=np.zeros(len(pairs),int)
  for co,rr in ix.items():
   for j,(a,b) in enumerate(pairs):
    fams={p[i]['family'] for i in rr if z[i,features[a]]>0 and z[i,features[b]]>0};support[j]=max(support[j],len(fams))
  eligible=[j for j in range(len(pairs)) if support[j]>=4 and np.count_nonzero(sd[:,j]>1e-10)>=2]
  ranked=sorted(eligible,key=lambda j:(-abs(float(res[:,j].mean())),features[pairs[j,0]],features[pairs[j,1]]))[:4]
  v=res[:,ranked];norm=float(np.linalg.norm(v));weights=v/norm if norm>1e-12 else v*0
  score=np.sum((null[:,:, :,ranked]-center[:,ranked])*weights,axis=(2,3)) if ranked else np.zeros((4,64));mix=mixing(score)
  if kind=='binary' and ranked and not mix['adequate'] and not mix['degenerate']:
   long,aa,ss=run_binary(ids,p,features,2026110419+si*100000,burn=500,thin=50);np.savez_compressed(R/f'cache/{site}_discovery_binary_long.npz',binary=long,**ss);jsonl(R/f'evidence/{site}_discovery_degree_constraints_long.jsonl',aa)
   # Pair list remains fixed; direction is calibrated from the predeclared longer discovery reference.
   center=long.mean((0,1));v=real.mean(1)[:,ranked]-center[:,ranked];norm=float(np.linalg.norm(v));weights=v/norm if norm>1e-12 else v*0;score=np.sum((long[:,:,:,ranked]-center[:,ranked])*weights,axis=(2,3));mix=mixing(score)
  spec[kind]=dict(pair_indices=[int(j) for j in ranked],pair_ids=[[features[pairs[j,0]],features[pairs[j,1]]] for j in ranked],weights=weights.tolist(),discovery_residual=(real.mean(1)[:,ranked]-center[:,ranked]).tolist(),coactive_family_support=[int(support[j]) for j in ranked],discovery_mixing=mix,eligible=bool(ranked and norm>1e-12 and (kind=='amplitude' or mix['adequate'])),status='FROZEN' if ranked and norm>1e-12 else 'INSUFFICIENT_PAIR_SUPPORT')
 dump(R/f'data/{site}_joint_directions.json',dict(UTC=now(),site=site,features=features,kinds=spec))
files=[R/'data/candidates.json',*[R/f'data/{site}_joint_directions.json' for site in SITES]]
dump(R/'evidence/candidates_and_joint_frozen.json',dict(UTC=now(),source='discovery sparse responses only',hashes={str(f):sha(f) for f in files},heldout_feature_reads=0))
print('CANDIDATES_AND_JOINT_FROZEN',flush=True)
