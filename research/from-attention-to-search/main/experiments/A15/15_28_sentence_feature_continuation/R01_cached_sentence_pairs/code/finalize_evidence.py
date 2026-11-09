from core import *
import pandas as pd
from datetime import datetime,timezone
cs=json.loads((R/'results/cells_intervals.json').read_text());nullrows=[];cache={};observed_weighted={}
for k in ['SAE','CC']:
 y=np.load(R/f'results/matched_{k}.npz')['values'];W=sparse.load_npz(R/f'results/weights_{k}.npz');observed_weighted[k]=W@np.nan_to_num((y[:,:,:,0]-y[:,:,:,1]).reshape(-1))
for k in ['SAE','CC']:
 for dom in (0,1):
  prefix=f'incidence_{k}_{dom}';x=dict(np.load(R/f'results/nulls/{prefix}_{k}_{dom}.npz'));diag=json.loads((R/f'results/nulls/{prefix}_diagnostics.json').read_text());cache[('incidence',k,dom)]=(x,diag,{int(c):i for i,c in enumerate(x['cell_ids'])})
for dom in (0,1):
 x=dict(np.load(R/f'results/nulls/graph_CC_{dom}.npz'));diag=json.loads((R/'results/nulls/graph_diagnostics.json').read_text());cache[('graph','CC',dom)]=(x,diag,{int(c):i for i,c in enumerate(x['cell_ids'])})
for c in cs:
 for kind in ['incidence','graph']:
  if kind=='graph' and (c['dictionary']!='CC' or c['metric_id']==0):continue
  x,diag,lookup=cache[(kind,c['dictionary'],c['domain_id'])];ii=lookup[c['cell']];vv=x['values'][:,ii,2];bad=int((~np.isfinite(vv)).sum());status='AVAILABLE' if bad==0 else 'UNAVAILABLE_RANDOM_DENOMINATOR'
  if diag['flags']:status='MIXING_UNQUALIFIED'+(';' + status if bad else '')
  lo,hi=np.quantile(vv,[.025,.975]) if bad==0 else [np.nan,np.nan];obs=float(observed_weighted[c['dictionary']][c['cell']]);assert abs(obs-c['delta'])<1e-12;exceeds=bool(status=='AVAILABLE' and obs>hi);c['observed_delta_same_weight_operator']=obs
  c[kind+'_status']=status;c[kind+'_q025']=float(lo);c[kind+'_q975']=float(hi);c[kind+'_exceeds']=exceeds;c[kind+'_invalid_draws']=bad
  nullrows.append(dict(dictionary=c['dictionary'],cell=c['cell'],domain=c['domain'],tier=c['tier'],pair_class=c['pair_class'],same_id=c['same_id'],frequency=c['frequency'],metric=c['metric'],distance=c['distance'],kind=kind,observed_delta=obs,q025=lo,q975=hi,status=status,invalid_draws=bad,draws=len(vv),exceeds=exceeds,max_invalid_pairs=int(x['invalid'][:,ii].max())))
 c['qualified_positive_excess']=bool(c['primary'] and c['matched_verdict']=='POSITIVE_MATCHED' and c['incidence_exceeds'] and (c['metric_id']==0 or c.get('graph_exceeds',False)))
 c['interpretation']='Bounded coordinate recurrence' if c['qualified_positive_excess'] and c['metric_id']==0 else ('Condition-specific lost-set association; inspect common-source guard before replacement interpretation' if c['qualified_positive_excess'] else 'See matched verdict and null availability separately')
ledger=pd.read_csv(R/'results/primary_336.csv').to_dict('records');bykey={(c['domain'],c['dictionary'],c['metric'],c['frequency'],c['distance'],c['same_id']):c for c in cs if c['primary']}
ledger=[bykey.get((c['domain'],c['dictionary'],c['metric'],c['frequency'],str(c['distance']),c['same_id']),c) for c in ledger]
pd.DataFrame(cs).to_csv(R/'results/all_cells_final.csv',index=False);pd.DataFrame(ledger).to_csv(R/'results/primary_336_final.csv',index=False);pd.DataFrame(nullrows).to_csv(R/'results/null_cell_summary.csv',index=False)
summary=dict(completed_at=datetime.now(timezone.utc).isoformat(),primary_cells=336,matched_positive=sum(c.get('matched_verdict')=='POSITIVE_MATCHED' for c in ledger),qualified_H1=sum(c.get('qualified_positive_excess',False) and c['metric']=='identity' for c in ledger),qualified_H2=sum(c.get('qualified_positive_excess',False) and c['metric'] in ['forward','reverse'] for c in ledger),null_jobs=5,draws_each=398,all_actual_draws=1990,claim_boundary='Exploratory exposed documents; conditional matches cover a small function-word-heavy subset; no causal transfer or semantic hierarchy; SAE H2 incompatible.',human_judgment='Unknown')
dump(R/'results/result_summary.json',summary);print(json.dumps(summary,indent=2))
