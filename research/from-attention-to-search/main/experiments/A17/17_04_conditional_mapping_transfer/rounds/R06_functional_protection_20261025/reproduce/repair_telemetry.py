"""Repair an axis-tag bug from immutable scalar logs, preserving original events."""
from pathlib import Path
import json,hashlib,datetime
from torch.utils.tensorboard import SummaryWriter
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert (ROOT/'terminal.json').exists(),'repair only after training terminal'
 receipts=[]
 for met in sorted((ROOT/'runs').glob('seed_*/old_*/*/metrics.jsonl')):
  case=met.parent;rows=[json.loads(s) for s in met.read_text().splitlines()]
  if not rows:continue
  original=case/'tensorboard';raw=case/'tensorboard_raw'
  assert original.is_dir() and not raw.exists(),'do not overwrite an earlier repair'
  rawhash={str(p.relative_to(case)):sha(p) for p in original.glob('events*')}
  original.rename(raw)
  tb=SummaryWriter(str(original))
  for m in rows:
   t=m['step'];n=m['counters']['valid_objective_targets']
   for tag,val in [('train_lm_loss',m['train_lm_loss']),('train_total_loss',m['objective']),('loss_component/new_raw',m['new_train_ce']),('loss_component/new_weighted',m['new_weighted']),('loss_component/old_active_raw',m['old_active_train_ce']),('loss_component/old_active_weighted',m['old_weighted'])]:
    tb.add_scalar('tokens/'+tag,val,n);tb.add_scalar('updates/'+tag,val,t)
   tb.add_scalar('updates/learning_rate',1e-4,t)
   for tag,val in [('tokens_seen',n),('effective_tokens_per_update',36+m['old_active_count']),('new_targets',m['counters']['new_targets']),('probe_label_accesses',m['counters']['old_probe_targets'])]:tb.add_scalar('progress/'+tag,val,t)
   tb.add_scalar('progress/optimizer_step',t,n)
   for tag in ['candidate_norm','actual_norm','g_dot_candidate','g_dot_actual','probe_loss','actual_C_energy_fraction','objective_grad_raw_norm']:tb.add_scalar('diagnostics/'+tag,m[tag],t)
  tb.close();ea=EventAccumulator(str(original),size_guidance={'scalars':0}).Reload();tags=ea.Tags()['scalars']
  for tag in tags:
   es=ea.Scalars(tag);assert len(es)==len(rows)
   assert all(a.step<b.step for a,b in zip(es,es[1:])),tag
   assert all(__import__('math').isfinite(e.value) for e in es)
  assert ea.Scalars('progress/optimizer_step')[-1].step==rows[-1]['counters']['valid_objective_targets']
  assert ea.Scalars('progress/optimizer_step')[-1].value==len(rows)
  for i,e in enumerate(ea.Scalars('tokens/train_lm_loss')):
   assert abs(e.value-rows[i]['train_lm_loss'])<=max(1e-7,abs(rows[i]['train_lm_loss'])*1e-6)
  rec={'case':str(case),'status':'PASS','steps':len(rows),'raw_event_SHA_before_move':rawhash,'immutable_metrics_sha256':sha(met),'canonical_events':'rebuilt from original step metrics, not a new training run','tag_axis_fix':'progress/optimizer_step only against valid targets; original erroneously emitted both update and token steps'}
  (case/'telemetry_verification.json').write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
 (ROOT/'provenance/telemetry_repair.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_original_event_files_preserved':True,'runs':receipts,'scientific_settings_changed':False},indent=2)+'\n')
 print(json.dumps({'status':'PASS','runs':len(receipts),'raw_events_preserved':True}))
if __name__=='__main__':main()
