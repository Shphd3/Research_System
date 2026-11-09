from pathlib import Path
import json,hashlib,shutil
import numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);O=Path(c['parent_round']);v=json.load(open(E/'audit/validation.json'));oldall=[json.loads(l) for l in (O/'analysis/raw_outputs.jsonl').read_text().splitlines()];old={r['index']:r for r in oldall if r['condition']=='identity'};base={}
for line in (E/'analysis/raw_outputs.jsonl').open():
 r=json.loads(line)
 if r['condition']=='identity':base[r['index']]=r
stable=[];setdiff=[];nll=[];groupchanges=json.load(open(E/'analysis/tie_policy.json'))['legacy_group_changes']
for i,r in base.items():
 oo=old[i];mx=oo['top20'][0]['probability'];tie={t['id'] for t in oo['top20'] if t['probability']==mx};assert len(tie)<20
 if min(tie)!=r['top1_id']:stable.append({'index':i,'old_stable':min(tie),'current_stable':r['top1_id']})
 nt={t['id'] for t in r['top10'] if t['probability']==r['top10'][0]['probability']}
 if tie!=nt:setdiff.append(i)
 nll.append(abs(r['NLL']-oo['NLL']))
assert not stable and not setdiff and max(nll)<1e-6,(stable,setdiff,max(nll))
# All actual target states, not a source-name assumption.
hold=np.load(O/'data/fresh_h.npy');err=0.;nn=0
for p in (E/'data/eval_targets').glob('*.npz'):
 a=np.load(p);err=max(err,float(abs(a['h'][27]-hold[a['indices']]).max()));nn+=len(a['indices'])
assert nn==737 and err==0
s=pd.read_csv(E/'analysis/summary_metrics.csv');z=s[(s.condition=='identity')&(s.metric=='top1_agreement')];assert (z['mean']==1).all()
a=pd.read_csv(E/'analysis/position_metrics.csv');assert len(a)==249843
# Both scopes share last-layer native output metrics at everyposition/condition.
z=a[(a.layer==28)&(a.readout=='continuation')];aa=z[z.scope=='all_prefix'].set_index(['index','condition']).sort_index();bb=z[z.scope=='target_only'].set_index(['index','condition']).sort_index();fields=['NLL','KL_full','top1_id','target_probability','full_top1_probability'];assert np.array_equal(aa[fields].values,bb[fields].values)
freeze=json.load(open(E/'freeze.json'));bad=[]
for p,h in freeze['sha256'].items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:bad.append(p)
assert not bad
v['serialized_topk_order_differences']=v['baseline_top1_differences'];v['baseline_top1_differences']=stable;v.update(tie_policy='probability desc,ID asc',max_tie_count_observed=7,identity_all737_target_h_max_abs_vs_R13=err,identity_all737_NLL_max_abs_vs_R13=max(nll),max_tie_sets_vs_R13_equal=True,category_membership_changes=groupchanges,identity_top1_preservation_exactly1=True,last_layer_both_scopes_exact=True,all_source_freeze_hashes_unchanged=True)
(E/'audit/validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');shutil.copy2(E/'audit/validation.json',P/'audit/validation.json');shutil.copy2(E/'analysis/tie_policy.json',P/'provenance/tie_policy.json');shutil.copy2(E/'audit/03_numerics_smoke.json',P/'audit/03_numerics_smoke.json')
print(json.dumps({k:v[k] for k in ['pass','raw_records','identity_all737_target_h_max_abs_vs_R13','identity_all737_NLL_max_abs_vs_R13','category_membership_changes','legacy_max_NLL_diff','legacy_top1_differences','last_layer_both_scopes_exact']},indent=2))
