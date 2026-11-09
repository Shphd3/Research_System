"""A01: finish literal rotation-only constraint on existing caches, no forwards."""
import os
os.environ['OPENBLAS_NUM_THREADS']='4';os.environ['OMP_NUM_THREADS']='4'
from pathlib import Path
import time,json,hashlib,shutil,subprocess,sys,datetime
ROOT=Path(__file__).resolve().parents[1]
while not (ROOT/'analysis/completion.json').exists():
 if (ROOT/'analysis/failure.json').exists():raise RuntimeError('Initial pipeline failed;inspect before correction')
 time.sleep(5)
# Current process starts only after the original pipeline has released all outputs.
p=ROOT/'scripts/metrics.py';before=hashlib.sha256(p.read_bytes()).hexdigest();s=p.read_text();s=s.replace('r=u@vt\n assert',"sign=np.linalg.slogdet(u@vt)[0]\n if sign<0:u[:,-1]*=-1\n r=u@vt\n assert")
assert s!=p.read_text();p.write_text(s)
p2=ROOT/'scripts/calibrate.py';s=p2.read_text().replace('y=x@q',"q[:,-1]*=np.linalg.slogdet(q)[0];y=x@q");p2.write_text(s)
subprocess.run([sys.executable,str(p2)],check=True)
import numpy as np
import analyze
old=[];archive=ROOT/'audit/superseded_reflection_alignment';archive.mkdir(exist_ok=True)
for f in (ROOT/'analysis/alignments').glob('*.npz'):
 r=np.load(f)['R'];sign=np.linalg.slogdet(r)[0]
 if sign<0:
  stem=f.stem;tt,uu,layer=stem.split('_');jp=ROOT/'analysis/pairs'/f'{stem}.json';o=json.load(open(jp));old.append((int(tt),int(uu),int(layer[5:]),o))
  shutil.copy2(jp,archive/jp.name);shutil.copy2(f,archive/f.name);jp.unlink()
deltas=[]
for t,u,l,o in old:
 n=analyze.pair_metrics(t,u,l)
 rawkeys=['absolute_spectrum_l2','relative_absolute_spectrum_l2','normalized_spectrum_TV','mean_drift','raw_eval_relative_residual','cka'];rawdiff={k:abs(n['metrics'][k]-o['metrics'][k]) for k in rawkeys}
 assert all(v<=1e-10*max(1,abs(o['metrics'][k])) for k,v in rawdiff.items()),rawdiff
 deltas.append(dict(tokens=t,comparison_tokens=u,layer=l,old_aligned_eval_residual=o['metrics']['aligned_eval_relative_residual'],new_aligned_eval_residual=n['metrics']['aligned_eval_relative_residual'],raw_metric_absolute_differences=rawdiff))
analyze.make_pairs()
from plot import geometry_figures
geometry_figures()
checks=[]
for f in (ROOT/'analysis/alignments').glob('*.npz'):
 r=np.load(f)['R'];sg,lg=np.linalg.slogdet(r);err=np.linalg.norm(r.T@r-np.eye(1024));assert sg==1 and abs(lg)<1e-8 and err<1e-8
 checks.append(dict(file=f.name,determinant_sign=float(sg),log_absolute_determinant=float(lg),orthogonality_error=float(err)))
a=dict(status='PASS_PROPER_ROTATIONS_ONLY',amendment='A01',ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),corrected_pairs=len(old),all_unique_alignment_matrices=len(checks),deltas=deltas,determinant_checks=checks,language_model_updates=0,new_forwards=0,new_GPU_allocations=0,compute='CPU cached recomputation;no new parameter/split/threshold selection',old_metrics_code_sha256=before,current_source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'scripts/metrics.py',ROOT/'scripts/calibrate.py',Path(__file__)]})
(ROOT/'audit/rotation_only_correction.json').write_text(json.dumps(a,indent=2)+'\n')
c=json.load(open(ROOT/'analysis/completion.json'));c['amendment_A01']='COMPLETE_SO(d)_det+1';c['corrected_at']=a['ended_at'];c['all_unique_alignments_proper_rotations']=len(checks);(ROOT/'analysis/completion.json').write_text(json.dumps(c,indent=2)+'\n')
print('A01_COMPLETE',len(old),'negative-det pairs corrected;',len(checks),'proper rotations verified',flush=True)
