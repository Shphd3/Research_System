from engine import *
import pandas as pd
# Preserve original S08, freeze identity and complete document split.
original=json.load(open(R/'evidence/S08_original_hashes.json'))
for name,h in original.items():assert sha(S08/name)==h,name
for name,h in json.load(open(R/'evidence/protocol_freeze.json'))['hashes'].items():assert sha(name)==h
for name,h in json.load(open(R/'evidence/directions_freeze.json'))['hashes'].items():assert sha(name)==h
allindex=[i for ii in INDEX.values() for i in ii];assert len(allindex)==len(set(allindex))==771
for d in DATASETS:assert len(INDEX[d+'__discovery'])==128 and len(INDEX[d+'__heldout'])==129
seterrors=[];identityerrors=[];snapchecks=0;jointchecks=0
for site in SITES:
 for tag in ['discovery','heldout']:
  obs=split_support(site,tag);x=np.load(R/'cache'/f'{site}__{tag}__position.npz');snaps=np.load(R/'cache'/f'{site}__{tag}__position__audit_snapshots.npz');features=x['features'];n=obs.shape[1]
  for name in snaps.files:
   arr=snaps[name];assert arr.shape==obs.shape;assert np.all(np.diff(arr,axis=-1)>0)
   for d in range(3):
    for t in range(8):assert np.array_equal(np.bincount(arr[d,:,t].ravel(),minlength=30000),np.bincount(obs[d,:,t].ravel(),minlength=30000));snapchecks+=1
   chain=int(name.split('_')[0][5:]);draw=int(name.split('draw')[1]);q=np.zeros((3,276));pIDs=[(int(a),int(b)) for a,b in x['pair_featureIDs']]
   for d in range(3):
    sets=[set(row) for row in arr[d].reshape(-1,32)]
    for j,(a,b) in enumerate(pIDs):q[d,j]=sum(a in s and b in s for s in sets)/(n*8)
   assert np.max(np.abs(q-x['qnull'][chain,draw]))<1e-12;jointchecks+=1
  for d in range(3):
   counts=np.stack([np.bincount(obs[d,:,t].ravel(),minlength=30000) for t in range(8)]);exact=float(np.sum(counts*(counts-1),axis=1).mean()/(n*(n-1)));identityerrors.append(abs(exact-x['real_intersections'][d]));identityerrors.append(float(np.max(np.abs(x['Inull'][:,:,d]-exact))))
  # Independent direct Python sets on original heldout binary supports.
  rr=np.random.default_rng(77)
  flat=obs.reshape(3*n,8,32)
  for _ in range(50):
   a,b=rr.choice(3*n,2,False);vals=[]
   for t in range(8):
    aa=set(flat[a,t]);bb=set(flat[b,t]);vals.append(len(aa&bb)/len(aa|bb))
   seterrors.append(abs(np.mean(vals)-x['realJ'][a,b]))
assert max(identityerrors)<1e-12;assert max(seterrors)<1e-12
own=pd.read_csv(R/'tables/B_own_structure.csv');between=pd.read_csv(R/'tables/B_dataset_differences.csv')
for df in [own,between]:
 p=df[df['mode']=='position'];assert len(p)==6;v=p.p_null.to_numpy();o=np.argsort(v);adj=np.minimum(1,np.maximum.accumulate([(6-i)*v[j] for i,j in enumerate(o)]));assert np.allclose(p.Holm_p.to_numpy()[o],adj)
 for _,r in df.iterrows():
  site=r.site;mode=r['mode'];stem=f'{site}__heldout__{mode}';p=R/'cache'/f'{stem}__long.npz';p=p if p.exists() else R/'cache'/f'{stem}.npz';x=np.load(p);dirs=np.load(R/'data'/f'{site}__discovery_directions.npz');rr=x['realq'].mean(1)-x['qnull'].mean((0,1))
  if 'dataset' in r.index:
   d=DATASETS.index(r.dataset);truth=float(rr[d]@dirs['own'][d]);assert abs(truth-r.heldout_excess)<1e-12
  else:
   a=DATASETS.index(r.A);b=DATASETS.index(r.B);ab=DP.index((a,b));truth=float((rr[a]-rr[b])@dirs['between'][ab]);assert abs(truth-r.heldout_difference)<1e-12
# Unbiased discovery intersection is a different formula from plugin p^2, not E[J].
for site in SITES:
 b=np.load(R/'cache'/f'{site}__frequency_reference.npz');p=np.load(R/'data/discovery_marginals.npz')
 for j in range(6):
  a,c=(j,j) if j<3 else DP[j-3];theory=float(np.sum(p[site+'__'+DATASETS[a]]*p[site+'__'+DATASETS[c]],axis=1).mean());mc=b['Inull'][:,j];se=mc.std(ddof=1)/16;assert abs(mc.mean()-theory)<6*se+1e-9
out=dict(UTC=now(),status='PASS',original_S08_files_hashed=len(original),original_S08_changed=0,document_split_total=771,independent_set_checks=len(seterrors),max_J_error=max(seterrors),fixed_degree_snapshot_strata_checks=snapchecks,joint_snapshot_checks=jointchecks,max_fixed_intersection_identity_error=max(identityerrors),signed_projection_replays=len(own)+len(between),Holm_families=2,discovery_marginal_intersection_MC_checks=12,conditional_CI_boundary='fixed discovery directions and estimated null centers',code_sha256=sha(__file__))
dump(R/'evidence/independent_verification.json',out);print(json.dumps(out))
