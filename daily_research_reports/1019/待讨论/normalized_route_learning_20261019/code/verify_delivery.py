from common import *
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def main():
 t=time.monotonic();rows=[];sources=[];step_rows=[];exposure_rows=[];members=[]
 for co in CFG['conditions']:
  for seed in CFG['seeds']:
   pp=ROOT/f'training/{co["id"]}/seed{seed}';cc=json.load(open(pp/'complete.json'));last=torch.load(pp/'epoch3.pt',map_location='cpu',mmap=True,weights_only=False);zero=torch.load(pp/'epoch0.pt',map_location='cpu',mmap=True,weights_only=False);expected=[o.tolist() for o in (lambda gen:[gen.permutation(CFG['train_N']) for _ in range(3)])(np.random.default_rng(seed))];assert zero['orders']==expected and last['orders']==expected
   assert last['step']==768 and last['seen']==392136 and last['epoch']==3;assert len(last['optimizer']['state'])>0;assert 'rng' in last and 'cuda' in last['rng'];assert last['config_sha']==sha(ROOT/'config/frozen.json')
   ea=EventAccumulator(str(pp/'tensorboard'),size_guidance={'scalars':0});ea.Reload();tags=ea.Tags()['scalars'];ev=ea.Scalars('tokens/train_lm_loss');assert len(ev)==768 and ev[-1].step==392136;assert ea.Scalars('progress/optimizer_step')[-1].step==392136
   if co['router']=='learned':assert len(ea.Scalars('tokens/loss_component/load_balance_raw'))==768 and len(ea.Scalars('tokens/loss_component/load_balance_weighted'))==768
   else:assert 'tokens/loss_component/load_balance_raw' not in tags
   for e in range(8):exposure_rows.append(dict(condition=co['id'],seed=seed,expert=e,cumulative_supervised_positions=cc['expert_exposures'][e],steps_with_non_None_task_gradient=cc['expert_updates'][e],definition='expert got task gradients; does not equate all exposure or nonzero gradients across matrices'))
   for line in (pp/'steps.jsonl').read_text().splitlines():
    rr=json.loads(line);step_rows.append({**dict(condition=co['id'],seed=seed),**{k:rr[k] for k in ['step','epoch','seen','N','lr','nll','total','lb_raw','lb_weighted','grad_norm','seconds']}})
   assert sum(x['N'] for x in step_rows if x['condition']==co['id'] and x['seed']==seed)==392136
   base=np.load(ROOT/'smoke/baseline_eval.npz')['nll'];probe=np.load(ROOT/f'functional/{co["id"]}/seed{seed}/probe.npz');baseerr=float(abs(base[probe['rows']]-probe['base_nll']).max());assert baseerr<1e-5
   rows.append(dict(condition=co['id'],seed=seed,saved_state_counters='PASS',orders_exact_PCG64='PASS',optimizer_RNG_present='PASS',TensorBoard_768_token_axis='PASS',frozen_base_probe_max_NLL_difference=baseerr,peak_GPU_bytes=cc['gpu_peak_allocated_bytes'],peak_RSS_bytes=cc['rss_peak_bytes']))
   for ep in range(4):
    fp=pp/f'epoch{ep}.pt';members.append(dict(condition=co['id'],seed=seed,epoch=ep,path=str(fp),bytes=fp.stat().st_size,step=ep*256,seen=ep*130712,sha256=sha(fp) if ep==3 else 'NOT_COMPUTED',hash_policy='fresh selected-final full-file hash; milestone bytes/access only'))
 # Verify original selected activations and real D28 amplitudes after every train condition.
 ck=torch.load(json.load(open(OLD/'provenance/cache_preparation_receipt.json'))['inputs']['crosscoder_checkpoint'],map_location='cpu',mmap=True,weights_only=False);d28=ck['crosscoder']['decoder'][-1].norm(dim=-1).numpy();frozen=[]
 for split in ['train','eval']:
  dat=np.load(ROOT/'cache'/f'profile_{split}.npz');actual=csr(loadcache(split))[dat['rows']][:,dat['feature_ids']].toarray();assert np.array_equal(actual,dat['z']);assert np.array_equal(actual*d28[dat['feature_ids']],dat['c']);frozen.append(dict(split=split,original_window_z_after_training_exact=True,original_window_c28_after_training_exact=True))
 csvwrite(ROOT/'tables/training_steps.csv',step_rows);csvwrite(ROOT/'tables/expert_training_exposures.csv',exposure_rows);write_json(ROOT/'provenance/checkpoint_members.json',members);write_json(ROOT/'provenance/final_verification.json',dict(status='PASS',seconds=time.monotonic()-t,main_models=rows,original_z_c=frozen,full_steps_rows=len(step_rows),main_exposures=sum(r['N'] for r in step_rows),selected_final_hashes='fresh full-file SHA256',individual_formal_resume_continuations='NOT RUN; separate smoke next-update replay exact'))
 # Current exact source identity, no repository-wide diff or unrelated project mutation.
 for fp in sorted((ROOT/'code').glob('*')):
  if fp.is_file():sources.append(dict(path=str(fp),bytes=fp.stat().st_size,sha256=sha(fp)))
 write_json(ROOT/'provenance/source_manifest.json',sources);print('FINAL VERIFICATION PASS',len(rows),time.monotonic()-t,flush=True)
if __name__=='__main__':main()
