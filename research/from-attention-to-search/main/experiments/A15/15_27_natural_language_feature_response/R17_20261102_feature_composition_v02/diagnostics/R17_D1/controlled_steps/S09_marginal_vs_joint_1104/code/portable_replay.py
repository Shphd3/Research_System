from pathlib import Path
import json,numpy as np,pandas as pd,itertools
R=Path(__file__).resolve().parents[1];pp=[json.loads(l) for l in open(R/'inputs/data/panel.jsonl')];ac=np.load(R/'inputs/cache/activations.npz');index=json.load(open(R/'data/split_indices.json'));DATASETS=['Magicoder','GSM8K','MMLU'];SITES=['ATTN_SAE','MLPIN_SAE'];DP=list(itertools.combinations(range(3),2));AA=pd.read_csv(R/'tables/A_overlap_references.csv');OO=pd.read_csv(R/'tables/B_own_structure.csv');DD=pd.read_csv(R/'tables/B_dataset_differences.csv');errors=[];n=129;within=list(itertools.combinations(range(n),2));cross=[(i,(i+off)%n) for i in range(n) for off in range(1,65)]
for site in SITES:
 ii=ac[site+'__indices'];vv=ac[site+'__values'];dirs=np.load(R/'data'/f'{site}__discovery_directions.npz');features=dirs['features'];pairIDs=list(itertools.combinations(features,2));supports=[];q=np.zeros((3,129,276))
 for d,ds in enumerate(DATASETS):
  rowsi=index[ds+'__heldout'];supports.append([[{int(f) for f,v in zip(ii[i,t],vv[i,t]) if v>0} for t in range(8)] for i in rowsi])
  for a,sets in enumerate(supports[-1]):
   for j,(f,g) in enumerate(pairIDs):q[d,a,j]=sum(int(f) in s and int(g) in s for s in sets)/8
 for mode in ['position','position_token3']:
  x=np.load(R/'cache'/f'{site}__heldout__{mode}.npz');nullmean=x['qnull'].mean((0,1));real=q.mean(1)
  for d,ds in enumerate(DATASETS):
   truth=float((real[d]-nullmean[d])@dirs['own'][d]);row=OO[(OO.site==site)&(OO.dataset==ds)&(OO['mode']==mode)].iloc[0];errors.append(abs(truth-row.heldout_excess))
  for j,(a,b) in enumerate(DP):
   truth=float((real[a]-nullmean[a]-(real[b]-nullmean[b]))@dirs['between'][j]);row=DD[(DD.site==site)&(DD.A==DATASETS[a])&(DD.B==DATASETS[b])&(DD['mode']==mode)].iloc[0];errors.append(abs(truth-row.heldout_difference))
 actual=np.zeros(6)
 for j in range(6):
  a,b=(j,j) if j<3 else DP[j-3];edges=within if j<3 else cross;v=[]
  for i,k in edges:
   v.append(sum(len(s&t)/len(s|t) for s,t in zip(supports[a][i],supports[b][k]))/8)
  actual[j]=np.mean(v)
 null=np.load(R/'cache'/f'{site}__heldout__position.npz')['Jnull'].mean((0,1));freq=np.load(R/'cache'/f'{site}__frequency_reference.npz')['Jnull'].mean(0)
 for j,(a,b) in enumerate(DP):
  rows=AA[(AA.site==site)&(AA.A==DATASETS[a])&(AA.B==DATASETS[b])]
  for comp,k in [('within_A',a),('within_B',b),('cross',3+j)]:
   r=rows[rows.comparison==comp].iloc[0];errors.extend([abs(actual[k]-r.real_J),abs(null[k]-r.heldout_fixed32_margin_J),abs(freq[k]-r.discovery_Bernoulli_J)])
assert max(errors)<1e-12
print(json.dumps(dict(status='PASS',point_value_replays=len(errors),max_error=max(errors),requires_model=False,requires_original_execution_path=False,requires_compiled_sampler=False)))
