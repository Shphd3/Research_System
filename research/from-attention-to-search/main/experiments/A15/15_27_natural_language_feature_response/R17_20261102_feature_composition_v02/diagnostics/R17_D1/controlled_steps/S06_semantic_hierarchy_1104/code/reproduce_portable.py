"""Offline replay from text+sparse full activations; no model weights or full cache needed."""
from pathlib import Path
import json,csv,math,itertools,sys
import numpy as np
from scipy import sparse
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
pp=[json.loads(l) for l in open(root/'data/panel.jsonl')];ix={p['id']:i for i,p in enumerate(pp)};lk={(p['family'],p['wording'],p['label']):i for i,p in enumerate(pp)};sel=json.load(open(root/'results/selection.json'))['sites'];maxj=maxq=maxp=maxbeh=0.;n=0
for site in ['ATTN_SAE','MLPIN_SAE']:
 z=sparse.load_npz(root/f'data/{site}_all_z_csr.npz').toarray().astype(float);assert z.shape==(384,30000);assert (z>0).sum(1).min()==32==(z>0).sum(1).max()
 for r in csv.DictReader(open(root/'results/overlaps.csv')):
  if r['site']!=site:continue
  a=z[lk[(r['family'],r['wording'],r['a'])]]>0;b=z[lk[(r['family'],r['wording'],r['b'])]]>0;v=(a&b).sum()/(a|b).sum();maxj=max(maxj,abs(v-float(r['Jaccard'])));n+=1
 for r in csv.DictReader(open(root/'results/candidate_values.csv')):
  if r['site']!=site:continue
  ids=sel[site][r['domain']]['H2' if r['list']=='H2' else 'common'] if r['list'] in ['H2','H1_common'] else sel[site][r['domain']]['events'][r['list']]
  a=z[ix[r['id']]];den=math.sqrt(math.fsum(float(a[j])**2 for j in ids));v=0 if den==0 else a[int(r['feature_id'])]/den
  assert abs(float(r['fixed_list_L2'])-den)<1e-10
  if r['q']:maxq=max(maxq,abs(v-float(r['q'])))
 for r in csv.DictReader(open(root/'results/joint_patterns.csv')):
  if r['site']!=site:continue
  ids=sel[site][r['domain']]['H2'];a,b=r['pair'].split('->');x=z[[lk[(r['family'],r['wording'],l)] for l in [a,b]]][:,ids];den=np.linalg.norm(x,axis=1,keepdims=True);q=np.divide(x,den,out=np.zeros_like(x),where=den>0);direction=sel[site][r['domain']]['directions'][r['pair']]['unit'];v=float((q[1]-q[0])@direction);maxp=max(maxp,abs(v-float(r['projection'])))
for r in [json.loads(l) for l in open(root/'data/behavior_all.jsonl')]:
 for c in r['candidates']:maxbeh=max(maxbeh,abs(math.fsum(c['token_logprobs'])-c['total_logprob']))
assert max(maxj,maxq,maxp,maxbeh)<1e-9
print(json.dumps(dict(status='PASS',prefixes=len(pp),overlaps_replayed=n,max_Jaccard_error=maxj,max_q_error=maxq,max_joint_projection_error=maxp,max_token_score_sum_error=maxbeh)))
