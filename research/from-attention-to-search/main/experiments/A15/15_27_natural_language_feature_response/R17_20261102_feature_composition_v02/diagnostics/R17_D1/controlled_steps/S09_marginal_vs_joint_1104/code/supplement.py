from engine import *
import pandas as pd
# Descriptive intersection distribution on pre-fixed audit snapshots, not a new test.
records=[]
def dist(a):
 n=a.shape[1];wt=np.triu_indices(n,1);r=np.repeat(np.arange(n),(n-1)//2);c=(r+np.tile(np.arange(1,(n-1)//2+1),n))%n;out=np.zeros((6,33),int)
 for t in range(8):
  b=binary(a[:,:,t].reshape(3*n,32));x=(b@b.T).toarray().astype(int)
  for j in range(6):
   d,e=(j,j) if j<3 else DP[j-3];ii,jj=wt if j<3 else (r,c);out[j]+=np.bincount(x[ii+d*n,jj+e*n],minlength=33)
 return out
for site in SITES:
 obs=split_support(site,'heldout');real=dist(obs);sn=np.load(R/'cache'/f'{site}__heldout__position__audit_snapshots.npz');null=np.array([dist(sn[k]) for k in sn.files]);assert real.sum(1).min()==8256*8
 for j in range(6):
  label='within_'+DATASETS[j] if j<3 else DATASETS[DP[j-3][0]]+'/'+DATASETS[DP[j-3][1]]
  for k in range(33):records.append(dict(site=site,comparison=label,intersection=k,real_position_pairs=int(real[j,k]),position_pairs_denominator=8256*8,real_fraction=float(real[j,k]/(8256*8)),audit_null_fraction=float(null[:,j,k].mean()/(8256*8)),audit_null_draws=8))
table(R/'tables/A_intersection_distributions_audit.csv',records)
a=pd.read_csv(R/'tables/A_overlap_references.csv');a['real_minus_fixed32_CI_lo']=a.real_CI_lo-a.heldout_fixed32_margin_J;a['real_minus_fixed32_CI_hi']=a.real_CI_hi-a.heldout_fixed32_margin_J;a['Bernoulli_gap_reproduction_ratio']=np.where(a.comparison=='pooled_gap',a.discovery_Bernoulli_J/a.real_J,np.nan);a['fixed32_gap_reproduction_ratio']=np.where(a.comparison=='pooled_gap',a.heldout_fixed32_margin_J/a.real_J,np.nan);a.to_csv(R/'tables/A_overlap_references.csv',index=False)
# Concrete selected-pair case, retaining original text, token and native magnitudes.
site='ATTN_SAE';x=np.load(R/'data'/f'{site}__discovery_directions.npz');j=int(x['selected_pair_indices'][0]);f,g=map(int,np.load(R/'cache'/f'{site}__heldout__position.npz')['pair_featureIDs'][j]);ac=np.load(S08/'cache/activations.npz');ii=ac[site+'__indices'];vv=ac[site+'__values'];cases=[]
for d in DATASETS:
 hit=[]
 for ix in INDEX[d+'__heldout']:
  for t in range(8):
   ids=ii[ix,t];value=vv[ix,t];di={int(k):float(v) for k,v in zip(ids,value)}
   if f in di and g in di:hit.append(dict(site=site,dataset=d,id=PANEL[ix]['id'],text=PANEL[ix]['text'],quantile=t,position=PANEL[ix]['positions'][t],token_id=PANEL[ix]['position_token_ids'][t],token=PANEL[ix]['position_decoded'][t],feature_i=f,feature_j=g,z_i=di[f],z_j=di[g],selection='First heldout coactive example in frozen discovery order, no primary selection from this case'))
  if hit:break
 if hit:cases.append(hit[0])
jsonl(R/'tables/concrete_pair_cases.jsonl',cases)
# Explicit within-source exceptions to the global projection pattern, posthoc description.
docs=rows(R/'tables/heldout_document_scores.jsonl');worst=[]
for site in SITES:
 for d in DATASETS:
  ds=[q for q in docs if q['site']==site and q['dataset']==d and q['mode']=='position'];lo=min(ds,key=lambda x:x['own_excess_projection']);lo.update(selection='POSTHOC minimum heldout document score, no new test',negative_documents=sum(x['own_excess_projection']<0 for x in ds),total_documents=len(ds));worst.append(lo)
jsonl(R/'tables/posthoc_document_counterexamples.jsonl',worst)
print('SUPPLEMENTS_COMPLETE',len(records),len(cases))
