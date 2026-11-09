"""python code/offline_replay.py in the extracted packet; NumPy only, no model."""
from common import *
from stats import *
import math
panel={p['id']:p for p in rows(R/'data/panel.jsonl')};spec=json.load(open(R/'data/R19_candidates.json'))['sites'];checks=0;all_data={}
def close(a,b,tol=1e-8):
 global checks
 assert abs(float(a)-float(b))<tol,(a,b);checks+=1
b=rows(R/'results/behavior_old.jsonl')+[json.load(open(f)) for f in (R/'results/new_rows').glob('*.json')]
for p in b:
 for c in p['candidates']:close(math.fsum(c['token_logprobs']),c['total_logprob'],1e-12)
 close((p['candidates'][0]['total_logprob']-p['candidates'][1]['total_logprob'])*(1 if p['gold']=='A' else -1),p['correct_margin'])
for site in SITES:
 data={}
 with np.load(R/f'cache/{site}_old_main.npz') as a:
  for i,pid in enumerate(a['ids']):
   z=np.zeros(30000);z[a['indices'][i]]=a['values'][i];data[str(pid)]=dict(z=z)
 if (R/'cache/new_all.npz').exists():
  with np.load(R/'cache/new_all.npz') as a:
   ids=a['ids'];ii=a[site+'__indices'];vv=a[site+'__values']
   for i,pid in enumerate(ids):
    z=np.zeros(30000);z[ii[i]]=vv[i];data[str(pid)]=dict(z=z)
 else:
  for p in panel.values():
   if p['provenance']!='NEW_FORWARD':continue
   with np.load(R/f'cache/new_rows/{p["id"]}.npz') as a:
    z=np.zeros(30000);z[a[site+'__indices'][0]]=a[site+'__values'][0];data[p['id']]=dict(z=z)
 all_data[site]=data
 for stage in ['baseline','controls']:
  for row in csv.DictReader(open(R/f'tables/{stage}_pair_metrics.csv')):
   if row['site']!=site:continue
   x=data[row['left_id']]['z'];y=data[row['right_id']]['z'];sx=set(np.flatnonzero(x));sy=set(np.flatnonzero(y));close(len(sx&sy),row['shared']);close(len(sy-sx),row['entered']);close(len(sx-sy),row['exited']);close(len(sx&sy)/len(sx|sy),row['Jaccard']);close(np.linalg.norm(y)/np.linalg.norm(x),math.exp(float(row['log_full_norm_ratio'])))
computed=[]
for si,site in enumerate(SITES):
 data=all_data[site];famset=json.load(open(R/'config.json'))['primary_heldout'];ret=[];contrast=[]
 for fam in famset:
  ret.append(np.mean([len(set(np.flatnonzero(data[cid('baseline',fam,16,g)]['z']))&set(np.flatnonzero(data[cid('baseline',fam,128,g)]['z'])))/32 for g in 'AB']))
  def sep(d):
   x=data[cid('baseline',fam,d,'A')]['z'];y=data[cid('baseline',fam,d,'B')]['z'];return np.linalg.norm(x-y)/np.sqrt((x@x+y@y)/2)
  contrast.append(np.log(sep(128)/sep(16)))
 ret=np.array(ret);v=np.array(contrast);bound=np.log(1.25);rl,rh=interval(ret,SEED+si);lo,hi=interval(v,SEED+si)
 computed.extend([dict(site=site,hypothesis='H1',value=float(ret.mean()),lo=rl,hi=rh,p=sign_p(ret-.9)),dict(site=site,hypothesis='H2',value=float(np.exp(v.mean())),lo=float(np.exp(lo)),hi=float(np.exp(hi)),p=max(sign_p(v+bound),sign_p(bound-v))),dict(site=site,hypothesis='H3',value=float(np.exp(v.mean())),lo=float(np.exp(lo)),hi=float(np.exp(hi)),p=sign_p(-v-bound))])
for x,p,y in zip(computed,holm([x['p'] for x in computed]),json.load(open(R/'results/primary_hypotheses.json'))):
 assert (x['site'],x['hypothesis'])==(y['site'],y['hypothesis'])
 for field in ['value','lo','hi','p']:close(x[field],y[field])
 close(p,y['holm_p'])
receipt=dict(status='PASS',checks=checks,actual_text_rows=len(panel),score_rows=len(b),primary=computed,scope='All raw score sums, all paired membership/norm changes, primary whole-code effect/interval/p/Holm from sparse observations. No weights,network or LM forwards.')
dump(R/'offline_replay_receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2))
