from core import *
import pandas as pd
from collections import Counter
from urllib.parse import urlsplit
base=np.load(R/'data/base_pairs.npz')['pairs'];tok=np.load(R/'data/tokens.npz');out={};tables=[]
for k in ['SAE','CC']:
 m=np.load(R/f'data/matches_{k}.npz');mt=m['matches'];l0=m['l0'];rows=[]
 for dom in (0,1):
  for cl in range(4):
   for eq in range(2):
    for db in range(7):
     q=np.flatnonzero((base[:,5]==dom)&(base[:,8]==cl)&(base[:,9]==eq)&(base[:,7]==db));sel=q[mt[q,1]==1];t2=q[mt[q,1]==2]
     if not len(q):continue
     rows.append(dict(dictionary=k,domain=['math','biology'][dom],pair_class=['lexical','whitespace','punctuation','other'][cl],same_id=eq,distance=DIST[db],eligible=len(q),T1=len(sel),T1_fraction=len(sel)/len(q),T2=len(t2),narrow=int(mt[sel,2].sum()),no_match=int((mt[q,1]<0).sum()),global_no_ID=int((mt[q,3]==0).sum()),partner_no_ID_with_global=int(((mt[q,3]==1)&(mt[q,4]==0)).sum()),matched_source_l0=float(l0[base[sel,0]].mean()) if len(sel) else None,matched_real_target_l0=float(l0[base[sel,1]].mean()) if len(sel) else None,matched_control_l0=float(l0[mt[sel,0]].mean()) if len(sel) else None,matched_numeric_pairs=int(((tok['numeric'][base[sel,0]]+tok['numeric'][base[sel,1]])>0).sum())))
 tables.extend(rows)
 sel=np.flatnonzero((mt[:,1]==1)&(base[:,8]==0)&(base[:,9]==0));counts=Counter(tok['id'][base[sel,1]].tolist());surface={int(tok['id'][r]):DOCS[tok['doc'][r]]['token_surfaces'][tok['pos'][r]] for r in base[sel,1]}
 out[k]=dict(lexical_different_pairs=len(sel),eligible_lexical_different=int(((base[:,8]==0)&(base[:,9]==0)).sum()),unique_real_targets=len(set(base[sel,1].tolist())),unique_control_targets=len(set(mt[sel,0].tolist())),target_id_pair_counts=[dict(token_id=tid,surface=surface[tid],pairs=n) for tid,n in counts.most_common()],max_control_reuse=max(Counter(mt[sel,0].tolist()).values()),genre_source_counts=dict(Counter(DOCS[d]['genre'] for d in base[sel,2])),host_source_counts=dict(Counter(DOCS[d]['host'] for d in base[sel,2])))
pd.DataFrame(tables).to_csv(R/'results/matching_coverage.csv',index=False);dump(R/'results/lexical_support.json',out)
# Case organization is descriptive: no semantic labels assigned to coordinates.
cs=json.loads((R/'results/selected_cases.json').read_text());org=[]
for c in cs:
 s=SENTS[c['sid']];x=np.load(SRC/'forward/documents'/f'{s["seq_id"]}.npz')
 for k in ['SAE','CC']:
  ptr=x[k+'_ptr'];ids=x[k+'_ids'];z=x[k+'_z'];freq=Counter(int(f) for p in s['positions'] for f in ids[ptr[p]:ptr[p+1]]);n=len(s['positions'])
  org.append(dict(case=c['name'],sid=s['sid'],dictionary=k,tokens=n,union=len(freq),only_one_position=sum(v==1 for v in freq.values()),multiple_positions=sum(v>1 for v in freq.values()),every_position=sum(v==n for v in freq.values()),every_position_ids=sorted(f for f,v in freq.items() if v==n)))
dump(R/'results/case_organization.json',org)
# Exact common-lost forward differences: saved pair outputs, no new match or threshold.
v=np.load(R/'results/matched_CC.npz');ba=base[v['base_indices']];mt=np.load(R/'data/matches_CC.npz')['matches'][v['base_indices']];y=v['values'];good=(mt[:,1]==1)&(ba[:,8]==0)&(ba[:,9]==0);common=y[good,:,5,0]-y[good,:,5,1];allf=y[good,:,3,0]-y[good,:,3,1]
dump(R/'results/composition_diagnostic.json',dict(T1_lexical_different_pairs=int(good.sum()),finite_common_values=int(np.isfinite(common).sum()),max_abs_common_forward=float(np.nanmax(np.abs(common))),max_abs_all_source_forward=float(np.nanmax(np.abs(allf))),positive_lost_cells='See primary_336.csv; condition-specific denominators must not be read as stable-source replacement.'))
print(json.dumps({'lexical_support':{k:{n:v for n,v in t.items() if n in ['lexical_different_pairs','eligible_lexical_different','unique_real_targets','unique_control_targets','max_control_reuse']} for k,t in out.items()},'organization':org},ensure_ascii=False,indent=2))
