from core import *
import pandas as pd
from datetime import datetime,timezone

def main():
 tok=dict(np.load(R/'data/tokens.npz'));base=np.load(R/'data/base_pairs.npz')['pairs'];blocks=json.loads((R/'data/document_blocks.json').read_text());partner={a:b for v in blocks for a,b in [v['docs'],v['docs'][::-1]]};checks={}
 assert np.all(tok['sid'][base[:,0]]==tok['sid'][base[:,1]]) and np.all(tok['pos'][base[:,1]]-tok['pos'][base[:,0]]==base[:,6]);assert np.all(base[:,6]>0)
 checks['all_pairs_within_frozen_sentence_and_correct_distance']=len(base)
 for k in ['SAE','CC']:
  mt=np.load(R/f'data/matches_{k}.npz');match=mt['matches'];l0=mt['l0'];ok=match[:,1]>0;ii=base[ok,0];jj=base[ok,1];cc=match[ok,0]
  assert all(tok['doc'][c]==partner[tok['doc'][j]] for j,c in zip(jj,cc));assert np.all(tok['doc'][jj]!=tok['doc'][cc]);assert np.all(tok['domain'][jj]==tok['domain'][cc]);assert np.all(tok['decile'][jj]==tok['decile'][cc]) and np.all(tok['quartile'][jj]==tok['quartile'][cc]);assert np.all((l0[cc]>=.8*l0[jj])&(l0[cc]<=1.25*l0[jj]))
  t1=match[ok,1]==1;t2=~t1;assert np.all(tok['id'][jj[t1]]==tok['id'][cc[t1]]);assert np.all(tok['class'][jj[t2]]==tok['class'][cc[t2]]);assert np.array_equal(tok['id'][ii]==tok['id'][jj],tok['id'][ii]==tok['id'][cc]);checks[k+'_fixed_match_contract']=int(ok.sum())
  B,ptr,ids,g=load_data(k);pv=np.load(R/f'results/pair_metrics_{k}.npz')['values'];a,b=graph();E=set(zip(a.tolist(),b.tolist()));rng=np.random.default_rng(99);choice=rng.choice(len(base),32,replace=False);n=0
  for q in choice:
   i,j=base[q,:2];c=match[q,0]
   for freq in range(5):
    src={int(f) for f in ids[ptr[i]:ptr[i+1]] if freq==4 or g[f]==freq};targets=[set(ids[ptr[t]:ptr[t+1]].tolist()) if t>=0 else None for t in [j,c]]
    for m in range(1 if k=='SAE' else 7):
     for cond,target in enumerate(targets):
      if target is None:expected=np.nan
      else:
       den=src if m in [0,3,4] else ((src-targets[0]-targets[1]) if m>=5 and targets[1] is not None else (set() if m>=5 else src-target));rev=m in [2,4,6]
       numerator=sum((f in target) if m==0 else any(((h,f) if rev else (f,h)) in E for h in target) for f in den);expected=numerator/len(den) if den else np.nan
      assert np.isclose(pv[q,freq,m,cond],expected,equal_nan=True,atol=1e-14),(k,q,freq,m,cond,pv[q,freq,m,cond],expected)
      n+=1
  checks[k+'_direct_set_numeric_comparisons']=n
  del B,pv
 freeze=json.loads((R/'provenance/outcome_freeze.json').read_text());changed=[p for p,h in freeze['files'].items() if sha(R/p)!=h];checks['frozen_core_files_unchanged']=not changed;assert not changed,changed
 ledger=pd.read_csv(R/'results/primary_336.csv');assert len(ledger)==336;checks['primary_family_preserved']=336
 dump(R/'provenance/results_audit.json',dict(time=datetime.now(timezone.utc).isoformat(),status='PASS',processing_agent='Codex /root separate direct-set verification',checks=checks,not_independent_agent=True));print(checks)
if __name__=='__main__':main()
