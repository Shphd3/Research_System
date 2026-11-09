"""CPU ideal-vector BF16 rounding diagnostic, not a new model forward."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1];R=Path(json.load(open(E/'manifest.json'))['parent_round']);rr=[json.loads(s) for s in (E/'data/positions.jsonl').read_text().splitlines()];h=np.zeros((28,737,1024),np.float32)
for p in (R/'data/eval_targets').glob('*.npz'):
 z=np.load(p);h[:,z['indices']]=z['h']
inds=[i for i,r in enumerate(rr) if r['panel']=='natural']
def bf16(x):
 a=np.asarray(x,dtype=np.float32).copy();b=a.view(np.uint32);return ((b+np.uint32(0x7fff)+((b>>16)&1))&np.uint32(0xffff0000)).view(np.float32)
out=[]
for l in range(28):
 b=np.load(R/'data/bases'/f'layer{l+1:02d}.npz');mu=b['mean'].astype(np.float32);v=b['V'].astype(np.float32);a=h[l,inds]-mu;coeff=a@v
 for band in range(16):
  vv=v[:,band*64:(band+1)*64];z=coeff[:,band*64:(band+1)*64]@vv.T;zn=np.linalg.norm(z,axis=1).clip(1e-20);delta=bf16(mu+z)-bf16(mu);no=bf16(z);out.append({'layer':l+1,'band':band,'add_mean_increment_rounding_relative_error':float(np.mean(np.linalg.norm(delta-z,axis=1)/zn)),'no_mean_rounding_relative_error':float(np.mean(np.linalg.norm(no-z,axis=1)/zn)),'coordinates_with_zero_increment_fraction':float(np.mean(delta==0)),'mode':'CPU_FP32_projection_BF16_rounding_not_native_replay'})
pd.DataFrame(out).to_csv(E/'analysis/CPU_rounding_diagnostic.csv',index=False);print(pd.DataFrame(out).query('layer in [1,14,25,28] and band in [0,7,15]').to_string(index=False))
