"""Independent raw-array/aggregation and context checks after completion."""
from pathlib import Path
import json,sys,hashlib,shutil
import numpy as np,pandas as pd
sys.path.insert(0,'/data/250010109/dependency_packages/hf_transformers_qwen3');from tokenizers import Tokenizer
E=Path(__file__).resolve().parents[1];c=json.load(open(E/'manifest.json'));P=Path(c['project_dir']);R=Path(c['parent_round']);rr=[json.loads(s) for s in (E/'data/positions.jsonl').read_text().splitlines()];docs={d['seq_id']:d for d in [json.loads(s) for s in (E/'data/evaluation_documents.jsonl').read_text().splitlines()]};tok=Tokenizer.from_file(str(Path(c['model_dir'])/'tokenizer.json'));V=json.load(open(E/'audit/analysis_validation.json'));prefix=0
for r in rr:
 ids=docs[r['seq_id']]['token_ids'];t=r['position'];assert ids[t]==r['input_id'];assert tok.decode(ids[:t+1],skip_special_tokens=False)==r['visible_prefix'];prefix+=1
 if t<191:assert ids[t+1]==r['target_id']
 else:assert r['seq_id']=='R11_A02_090' and r['target_id']==34259
stats={};nllerr=0.;underflow=0;ties=0;native=[];energyerr=0.
for original in (E/'analysis/chunks').glob('*.npz'):
 p=E/'analysis/batch1_repair_chunks'/original.name if (E/'analysis/batch1_repair_chunks'/original.name).exists() else original
 z=np.load(p);a=z['ints'];f=z['floats'];assert (a[:,4]==z['top10_ids'][:,0]).all();assert (z['top10_probs'][:,:-1]>=z['top10_probs'][:,1:]).all();ties=max(ties,int(a[:,6].max()));mask=f[:,3]>=np.finfo(np.float32).tiny;underflow+=int((~mask).sum());nllerr=max(nllerr,float(abs(-np.log(f[mask,3].astype(float))-f[mask,5]).max()))
 n=len(np.unique(a[:,0]));grid=f[n:].reshape(28,34,2,n,-1);ee=float(abs(grid[:,:16,:,:,8].sum(1)-1).max());energyerr=max(energyerr,ee);assert ee<1e-5;assert np.array_equal(grid[:,:16,:,:,8],grid[:,16:32,:,:,8]);assert (grid[:,32,:,:,8]==0).all() and (grid[:,33,:,:,8]==1).all()
 last=a[:,1]==28;codes=a[last,2];scopes=a[last,3]
 for code in range(34):
  i=np.where(last&(a[:,2]==code)&(a[:,3]==0))[0];j=np.where(last&(a[:,2]==code)&(a[:,3]==1))[0];assert np.array_equal(a[i,0],a[j,0]);assert np.array_equal(f[i][:,list(range(9))+[10,11,12,16,17]],f[j][:,list(range(9))+[10,11,12,16,17]]);assert np.array_equal(z['top10_ids'][i],z['top10_ids'][j])
 # Independent selected cells: average first inside each document, using raw arrays.
 for l in [1,14,25,28]:
  for code in [0,1,7,15,16,17,23,31,32,33]:
   for scope in [0,1]:
    q=(a[:,1]==l)&(a[:,2]==code)&(a[:,3]==scope)&np.array([rr[i]['panel']=='natural' for i in a[:,0]])
    if q.any():stats.setdefault((l,code,scope),[]).append(float(f[q,0].mean()))
S=pd.read_csv(E/'analysis/summary_metrics.csv');S=S[(S.panel=='natural')&(S.group=='ALL')];err=0.
for (l,code,scope),vals in stats.items():
 name=f'add_b{code:02d}' if code<16 else f'no_b{code-16:02d}' if code<32 else ['zero','full_centered'][code-32];row=S[(S.layer==l)&(S.condition==name)&(S.scope==['all_prefix','target_only'][scope])].iloc[0];err=max(err,abs(np.mean(vals)-row.top1_agreement))
assert err<1e-7,err
frozen=json.load(open(E/'freeze.json'))['sha256'];assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in frozen.items())
V.update(all737_visible_prefixes_and_shifts_verified=prefix,top10_matches_native_argmax=True,max_probability_tie_count=ties,NLL_probability_consistency_error=nllerr,subnormal_or_zero_probability_rows=underflow,all16_band_energy_sum_max_error=energyerr,mean_modes_share_identical_band_energy=True,independent_selected_reaggregation_error=err,last_layer_scope_metrics_candidates_exact=True,execution_freeze_unchanged=True)
assert nllerr<1e-4
(E/'audit/validation.json').write_text(json.dumps(V,indent=2)+'\n');shutil.copy2(E/'audit/validation.json',P/'audit/validation.json');print(json.dumps(V),flush=True)
