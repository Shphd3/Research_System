from native import *
import time
assert_freeze();torch.set_num_threads(2);torch.set_num_interop_threads(1);start=time.monotonic();pp=[p for p in rows(R/'data/panel.jsonl') if p['provenance']=='R19_REUSE'];cfg=json.load(open(R/'config.json'));saes=load_saes();source={stage:np.load(OLD/f'cache/{stage}.npz') for stage in ['discovery','heldout']};indices={stage:{str(pid):i for i,pid in enumerate(a['ids'])} for stage,a in source.items()}
dump(R/'evidence/old_encode_started.json',dict(UTC=now(),local_time=local_now(),rows=len(pp),pid=__import__('os').getpid(),LM_forwards=0,code_sha256=sha(__file__)))
for site,sae in saes.items():
 col={};maxerr=0
 for p in pp:
  stage=p['split'];a=source[stage];i=indices[stage][p['id']];x=torch.tensor(a[site+'__h'][i:i+1]);v=encode_one(sae,x);orig=dict(zip(a[site+'__indices'][i],a[site+'__values'][i]));got=dict(zip(v['indices'][0],v['values'][0]));assert set(orig)==set(got);err=max(abs(float(orig[k])-float(got[k])) for k in orig);maxerr=max(maxerr,err);assert err==0
  for k,x in v.items():col.setdefault(k,[]).append(x)
 payload={k:np.concatenate(v) for k,v in col.items()};payload['ids']=np.array([p['id'] for p in pp]);payload['decoder_norm']=sae.decoder.weight.detach().norm(dim=0).numpy();np.savez_compressed(R/f'cache/{site}_old_main.npz',**payload)
 print(site,'old exact error',maxerr,'preReLU positive',np.count_nonzero(payload['pre_relu']), 'seconds',round(time.monotonic()-start,1),flush=True)
behavior=[x for stage in ['discovery','heldout'] for x in rows(OLD/f'results/behavior_{stage}.jsonl') if x['condition'].startswith('main')];assert len(behavior)==144;jsonl(R/'results/behavior_old.jsonl',behavior)
dump(R/'evidence/old_encode_complete.json',dict(UTC=now(),status='PASS',old_prefixes=144,LM_forwards=0,SAE_reencodings=288,exact_native_Top32=True,seconds=time.monotonic()-start,weight_updates=0,cache_hashes={site:sha(R/f'cache/{site}_old_main.npz') for site in SITES}))
