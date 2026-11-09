"""Run in an extracted result packet: python code/offline_replay.py.

Reads literal sparse observations, raw candidate scores and conditional-null traces.
Requires numpy/scipy only. Does not load a model or execute any inference.
"""
from pathlib import Path
import json,math,itertools,hashlib
import numpy as np
from stats_utils import cosine,corr_audit,sign_p,boot_interval,holm
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def rows(p):return [json.loads(s) for s in (R/p).read_text().splitlines() if s.strip()]
SITES=['ATTN_SAE','MLPIN_SAE'];CONDS=['main16','main64','main128','nearN','nearA','nearB']
panel=rows('data/panel.jsonl');lookup={p['id']:p for p in panel};spec=read('data/candidates.json')['sites'];behavior={p['id']:p for split in ['smoke','discovery','heldout'] for p in rows(f'results/behavior_{split}.jsonl')};zall={};checks=0
def equal(a,b,tol=1e-8):
 global checks
 if a is None or b is None:assert a is b,(a,b)
 else:assert abs(float(a)-float(b))<tol,(a,b,tol)
 checks+=1
for p in behavior.values():
 for c in p['candidates']:equal(math.fsum(c['token_logprobs']),c['total_logprob'],1e-12)
 equal(p['candidates'][0]['total_logprob']-p['candidates'][1]['total_logprob'],p['A_minus_B'])
 equal(p['A_minus_B']*(1 if p['gold']=='A' else -1),p['correct_margin'])
for site in SITES:
 zall[site]={}
 for split in ['discovery','heldout']:
  a=np.load(R/f'cache/{split}.npz')
  for i,pid in enumerate(a['ids']):
   ids=a[site+'__indices'][i];v=a[site+'__values'][i];assert len(set(ids))==32 and np.all(v>0);zall[site][str(pid)]={int(f):float(x) for f,x in zip(ids,v)}
for m in rows('results/membership_pairs.jsonl'):
 x=zall[m['site']][m['left']];y=zall[m['site']][m['right']];sx=set(x);sy=set(y);assert sorted(sx&sy)==m['shared_ids'] and sorted(sy-sx)==m['entered_ids'] and sorted(sx-sy)==m['exited_ids'];equal(len(sx&sy)/len(sx|sy),m['Jaccard'])
computed=[];geometry={}
for si,site in enumerate(SITES):
 fs=sorted({p['family'] for p in panel if p['split']=='heldout'});ids=spec[site]['C'];gg=[]
 for f in fs:
  z={co:{g:np.array([zall[site][f'{f}_{co}_{g}'].get(i,0.) for i in ids]) for g in 'AB'} for co in CONDS};q={co:{g:v/np.linalg.norm(v) for g,v in dd.items()} for co,dd in z.items()};d0=q['nearN']['A']-q['nearN']['B'];ta=q['nearA']['A']-q['nearA']['B'];tb=q['nearB']['A']-q['nearB']['B'];T=(ta+tb)/2;N=(q['nearA']['A']-q['nearB']['A']+q['nearA']['B']-q['nearB']['B'])/2;opp=q['nearB']['A']-q['nearA']['B'];assert np.max(abs(opp-(T-N)))<1e-12
  ca=cosine(ta,d0);cb=cosine(tb,d0);c=cosine(q['main16']['A']-q['main16']['B'],q['main128']['A']-q['main128']['B']);e1=all(np.all(z[co][g]>0) for co in ['nearN','nearA','nearB'] for g in 'AB');e2=all(np.all(z[co][g]>0) for co in ['main16','main128'] for g in 'AB');loss=1-float(opp@d0/(d0@d0));margin=lambda co,g:behavior[f'{f}_{co}_{g}']['correct_margin'];bl=(margin('nearN','A')+margin('nearN','B')-margin('nearB','A')-margin('nearA','B'))/2
  gg.append(dict(f=f,template=lookup[f'{f}_main16_A']['template'],H1=(ca+cb)/2 if ca is not None and cb is not None else None,H2=c,e1=bool(e1 and ca is not None and cb is not None),e2=bool(e2 and c is not None),loss=loss,bl=bl));geometry[(site,f)]=gg[-1]
 for h,e in [('H1','e1'),('H2','e2')]:
  q=[g for g in gg if g[e]];v=[g[h] for g in q];computed.append(dict(site=site,hypothesis=h,N=len(q),mean=float(np.mean(v)) if v else None,CI=boot_interval(v,2026110419+si),p=sign_p(v) if len(q)>=8 else 1.))
 q=[g for g in gg if g['e1']];a=corr_audit([g['loss'] for g in q],[g['bl'] for g in q],[g['template'] for g in q],2026110419+si);computed.append(dict(site=site,hypothesis='H3',N=len(q),mean=a['rho'],CI=[a['lo'],a['hi']],p=a['p'] if len(q)>=8 else 1.))
for x,adj,y in zip(computed,holm([x['p'] for x in computed]),read('results/primary_hypotheses.json')):
 assert (x['site'],x['hypothesis'],x['N'])==(y['site'],y['hypothesis'],y['N']);equal(x['mean'],y['mean']);equal(adj,y['holm_p']);equal(x['CI'][0],y['lo']);equal(x['CI'][1],y['hi'])
joint=[]
for site in SITES:
 a=np.load(R/f'cache/{site}_heldout_null.npz');features=list(map(int,a['features']));scale=a['scale'];pairs=list(itertools.combinations(range(len(features)),2));directions=read(f'data/{site}_joint_directions.json')['kinds'];pp=[p for p in panel if p['split']=='heldout'];v=np.array([[zall[site][p['id']].get(f,0.) for f in features] for p in pp]);b=v>0
 for kind in ['binary','amplitude']:
  frozen=directions[kind];jj=frozen['pair_indices']
  if not jj:continue
  w=np.array(frozen['weights']);arr=b if kind=='binary' else v/scale;real=np.array([np.array([arr[[i for i,p in enumerate(pp) if p['condition']==co],k]*arr[[i for i,p in enumerate(pp) if p['condition']==co],l] for k,l in pairs],float).T for co in CONDS]);null=a['binary_long'] if kind=='binary' and 'binary_long' in a else a[kind];center=null.mean((0,1));score=float(np.sum((real.mean(1)[:,jj]-center[:,jj])*w));trace=np.sum((null[:,:,:,jj]-center[:,jj])*w,axis=(2,3));expected=next(x for x in read('results/joint_hypotheses.json') if x['site']==site and x['kind']==kind);equal(score,expected['score'],1e-7);equal(np.max(abs(trace-a[kind+'_decision_trace'])),0,1e-7);pv=(1+sum(trace.ravel()>=score-1e-14))/257 if expected['eligible'] else 1.;equal(pv,expected['p']);joint.append(dict(site=site,kind=kind,score=score,p=pv))
for x,p in zip(joint,holm([x['p'] for x in joint])):equal(p,next(y for y in read('results/joint_hypotheses.json') if y['site']==x['site'] and y['kind']==x['kind'])['holm_p'])
receipt=dict(status='PASS',checks=checks,prefixes=len(panel),membership_pairs=len(rows('results/membership_pairs.jsonl')),primary=computed,joint=joint,method='Independent sparse reconstruction and all raw score sums; primary CI/p and joint projection replay without weights.')
(R/'offline_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
