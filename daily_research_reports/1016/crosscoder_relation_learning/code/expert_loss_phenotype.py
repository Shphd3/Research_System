#!/usr/bin/env python3
"""CPU-only expert decomposition of saved C baseline/final prediction losses.

Use the fixed R1.8 cohort and precomputed feature-equal position weights.
No model forward, training, sample/cohort change, or new intervention occurs.
"""
from pathlib import Path
import argparse
import csv
import datetime
import hashlib
import json
import numpy as np
import torch

DEFAULT=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z')


def main(root):
    root=Path(root)
    cached=torch.load(root/'data_eval512/eval.pt',map_location='cpu',mmap=True,weights_only=False)
    prepared=torch.load(root/'response_decomposition/precomputed.pt',map_location='cpu',mmap=True,weights_only=False)
    N=int(prepared['eval_positions'])
    assert N==len(cached['target'])==523136
    assert prepared['min_eval_support']==20
    assert len(prepared['eligible_features']['low'])==3737
    assert len(prepared['eligible_features']['high'])==3916
    weights={'overall':np.full(N,1/N,dtype=np.float64),
             **{k:v.numpy() for k,v in prepared['weights'].items()}}
    for w in weights.values():assert w.shape==(N,) and abs(w.sum()-1)<1e-12
    rows=[];summaries=[];max_error=0.;max_metric_error=0.
    for seed in [20261016,20261017,20261018]:
        for arm in ['R','F','N']:
            folder=root/f'learning/seed_{seed}/{arm}'
            baseline=np.load(folder/'eval_losses_00000.npy',mmap_mode='r').astype(np.float64)
            final=np.load(folder/'eval_losses_06120.npy',mmap_mode='r').astype(np.float64)
            assert baseline.shape==final.shape==(N,)
            change=final-baseline
            route=cached['routes'][arm].numpy()
            old=json.loads((folder/'eval_00000.json').read_text())
            end=json.loads((folder/'eval_06120.json').read_text())
            for metric,w in weights.items():
                name='overall' if metric=='overall' else metric+'_loss'
                baseline_metric=float(w@baseline)
                final_metric=float(w@final)
                damage=float(w@change)
                metric_error=max(abs(baseline_metric-old[name]),abs(final_metric-end[name]))
                assert metric_error<1e-10,(seed,arm,metric,metric_error)
                max_metric_error=max(max_metric_error,metric_error)
                selected=[]
                for expert in range(4):
                    keep=route==expert
                    mass=float(w[keep].sum())
                    baseline_sum=float(w[keep]@baseline[keep])
                    final_sum=float(w[keep]@final[keep])
                    contribution=float(w[keep]@change[keep])
                    row={'seed':seed,'arm':arm,'expert':expert,'metric':metric,
                         'eval_token_count':int(keep.sum()),'eval_token_fraction':float(keep.mean()),
                         'metric_weight_mass':mass,'baseline_mean':baseline_sum/mass,
                         'final_mean':final_sum/mass,'mean_change':contribution/mass,
                         'contribution_change':contribution,
                         'share_of_total_metric_change':contribution/damage}
                    rows.append(row);selected.append(row)
                contribution_sum=sum(r['contribution_change'] for r in selected)
                error=abs(contribution_sum-(end[name]-old[name]))
                assert error<1e-10,(seed,arm,metric,error)
                max_error=max(max_error,error)
                largest=max(selected,key=lambda x:x['contribution_change'])
                summaries.append({'seed':seed,'arm':arm,'metric':metric,
                    'baseline':baseline_metric,'final':final_metric,'total_change':damage,
                    'expert_contribution_sum':contribution_sum,'saved_metric_sum_error':error,
                    'positive_mean_change_experts':sum(r['mean_change']>0 for r in selected),
                    'minimum_expert_mean_change':min(r['mean_change'] for r in selected),
                    'maximum_expert_mean_change':max(r['mean_change'] for r in selected),
                    'largest_contribution_expert':largest['expert'],
                    'largest_contribution_share':largest['share_of_total_metric_change'],
                    'largest_contribution_expert_weight_mass':largest['metric_weight_mass']})
    out=root/'analysis_outputs';out.mkdir(exist_ok=True)
    with (out/'expert_loss_changes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    overview={}
    for metric in weights:
        rr=[r for r in rows if r['metric']==metric]
        ss=[s for s in summaries if s['metric']==metric]
        overview[metric]={'arm_seed_expert_cells':len(rr),
                         'positive_expert_mean_change_cells':sum(r['mean_change']>0 for r in rr),
                         'expert_mean_change_range':[min(r['mean_change'] for r in rr),max(r['mean_change'] for r in rr)],
                         'largest_expert_contribution_share_range':[min(s['largest_contribution_share'] for s in ss),max(s['largest_contribution_share'] for s in ss)],
                         'total_metric_change_range':[min(s['total_change'] for s in ss),max(s['total_change'] for s in ss)]}
    result={'status':'PASS','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'no_new_forward_or_training':True,'no_cohort_change':True,'eval_positions':N,
            'weights':'overall uniform token weight1/N; low/high fixed feature-equal main-metric weights from response_decomposition/precomputed.pt',
            'decomposition':'metric damage=sum_e sum_{t:route(t)=e} w_t*(L_final(t)-L_zero(t)); expert means divide by expert weight mass',
            'sign':'positive means higher prediction loss / damage',
            'maximum_expert_contribution_sum_error_vs_saved_metric_damage':max_error,
            'maximum_weighted_loss_error_vs_saved_metrics':max_metric_error,
            'overview':overview,'arm_seed_metric_summaries':summaries,'expert_rows':rows,
            'source_files':{'script':str(Path(__file__).resolve()),
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'eval_cache':str(root/'data_eval512/eval.pt'),
                'weights':str(root/'response_decomposition/precomputed.pt'),
                'loss_array_pattern':str(root/'learning/seed_*/ARM/eval_losses_{00000,06120}.npy')},
            'boundary':'descriptive fixed-evaluation expert partition; expert labels across arms need not correspond; condition means and population contributions differ; not a new causal intervention or root-cause identification'}
    (out/'expert_loss_changes.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'max_sum_error':max_error,'max_metric_error':max_metric_error,'overview':overview},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=DEFAULT);a=p.parse_args();main(a.root)
