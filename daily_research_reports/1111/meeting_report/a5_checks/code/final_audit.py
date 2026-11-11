from common import *
import pandas as pd,zipfile,os

def main():
 frozen=json.load(open(R/'evidence/protocol_freeze.json'));assert sha(R/'protocol_frozen_cn.md')==frozen['sha256']
 # Actual coverage is explicit: optional tests must not be silently marked complete.
 expected={'1':'check1_hint_probes','2':'check2_step_lead','3':'check3_document_bootstrap','4':'check4_score_bias','5':'check5_layer_gates','6a':'check6a_readability','6b':'check6b_bootstrap_atoms'};coverage=[]
 for k,name in expected.items():
  p=R/f'results/{name}.csv';df=pd.read_csv(p) if p.exists() else None;coverage.append(dict(check=k,status='COMPLETE' if df is not None else 'NOT_RUN',rows=len(df) if df is not None else 0,file=str(p),researcher_judgment='Unknown'))
 d=pd.DataFrame(coverage);table(d,'coverage')
 a=pd.read_csv(R/'results/check1_hint_probes.csv');assert len(a)==88 and set(a.host)=={'A0','A1'} and a.delta_hint.notna().all()
 assert np.allclose(a.shuffled_probe_nll-a.real_probe_nll,a.delta_hint,atol=1e-12)
 b=pd.read_csv(R/'results/check3_document_bootstrap.csv');assert len(b)==99 and (b.bootstrap_samples==2000).all() and (b.ci95_low<=b.ci95_high).all()
 if (R/'evidence/check6a_complete.json').exists():
  sixa=pd.read_csv(R/'results/check6a_readability.csv');assert len(sixa)==24
  assert ((sixa.exact_set_accuracy>=0)&(sixa.exact_set_accuracy<=1)).all()
 if (R/'evidence/check6b_complete.json').exists():
  sixb=pd.read_csv(R/'results/check6b_bootstrap_atoms.csv');assert len(sixb)==6
  assert ((sixb.updates==10000)|(sixb.training_seconds>=1800)).all()
  assert (sixb.training_seconds<1810).all()
  assert np.isfinite(sixb[['Mbar_median','normalized_reconstruction_error','dead_atom_fraction']].to_numpy()).all()
 counts=[]
 for p in sorted((R/'probes').glob('*_metrics.csv')):
  x=pd.read_csv(p);assert np.isfinite(x.loss).all();expected_updates=768 if ('linear' in p.name or 'mlp_topk64' in p.name) else 512;assert len(x)==expected_updates,(p,len(x));counts.append(dict(file=str(p),updates=len(x)))
 # Frozen input arrays remain byte-identical; archival outside this task is not attributed to this task.
 inp=json.load(open(R/'evidence/gate_accepted.json'))['rows'];input_checks=[]
 for q in inp:
  p=Path(q['file']);assert p.exists() and sha(p)==q['sha256'];input_checks.append(dict(path=str(p),same_sha256=True))
 files=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted((R/'results').rglob('*')) if p.is_file()]
 totalgpu={}
 for line in (R/'evidence/events.jsonl').read_text().splitlines():
  x=json.loads(line);totalgpu[x['check']]=x['gpu_seconds']
 source=[dict(path=str(p),sha256=sha(p)) for p in sorted((R/'code').glob('*.py'))]
 small=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for dr in ['probes','dictionaries'] for p in sorted((R/dr).glob('*.pt'))]
 dump(R/'evidence/final_audit.json',dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),frozen_protocol_unchanged=True,coverage=coverage,probe_metric_files=counts,unmodified_R04_position_inputs=input_checks,analysis_files=files,source_versions=source,small_model_outputs=small,gpu_process_wall_seconds=totalgpu,resource_boundary='single local MIG; no main-model training or H100 allocations',scientific_judgment='Unknown'))
 register('analysis_a5_gain_checks_20261110','A5增益来源检查统计与小探针结果',[R/'evidence/final_audit.json']+[R/f'results/{n}.csv' for n in expected.values() if (R/f'results/{n}.csv').exists()],dict(parent='analysis_r04_atom_ledger_seven_20261109',protocol_sha256=frozen['sha256'],gpu='MIG H10040GB',main_models_frozen=True,scientific_judgment='Unknown'))
 if small:register('analysis_a5_gain_checks_small_probes_dictionaries_20261110','A5来源检查小探针及student稀疏字典',[Path(x['path']) for x in small]+[R/'evidence/final_audit.json'],dict(main_models_updated=False,small_model_manifest=str(R/'evidence/final_audit.json'),protocol_sha256=frozen['sha256'],judgment='Unknown'))
 print('AUDIT_PASS',len(files),len(small),flush=True)
if __name__=='__main__':main()
