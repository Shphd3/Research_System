import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
from pathlib import Path
import numpy as np,json
from metrics import moments,spectral,subspace,alignment,cka,stream_cka
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(1101);x=rng.normal(size=(512,16))*np.geomspace(4,.2,16);q=np.linalg.qr(rng.normal(size=(16,16)))[0];y=x@q
s=moments(x);t=moments(y);d= subspace(s['basis'][:,:4],t['basis'][:,:4])[0]['projection_distance'];r=alignment(x-x.mean(0),y-y.mean(0))
checks=dict(identity_CKA=abs(cka(x,x)-1),identity_subspace=subspace(s['basis'][:,:4],s['basis'][:,:4])[0]['projection_distance'],rotation_spectrum=np.linalg.norm(s['eigenvalues']-t['eigenvalues']),rotation_CKA=abs(cka(x,y)-1),rotation_raw_direction=d,rotation_aligned_residual=np.linalg.norm(x@r-y)/np.linalg.norm(y),scale_trace_ratio=moments(2*x)['eigenvalues'].sum()/s['eigenvalues'].sum(),scale_CKA=abs(cka(x,2*x)-1),permuted_CKA=cka(x,y[rng.permutation(len(y))]),stream_CKA_error=abs(cka(x,y)-stream_cka(x,y,70)),sv_lambda_error=np.max(abs(s['singular_values']**2/511-s['eigenvalues'])))
assert all(checks[k]<1e-8 for k in ['identity_CKA','rotation_spectrum','rotation_CKA','rotation_aligned_residual','scale_CKA','stream_CKA_error','sv_lambda_error'])
assert checks['identity_subspace']<1e-8 and d>.1 and checks['permuted_CKA']<.5 and abs(checks['scale_trace_ratio']-4)<1e-8
out=dict(status='PASS',checks=checks,note='FP64projection distance evaluated by equivalent orthogonal residual to avoid cancellation;all matrix identities1e-8;not a scientific effect tolerance')
(ROOT/'audit/calibration.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
