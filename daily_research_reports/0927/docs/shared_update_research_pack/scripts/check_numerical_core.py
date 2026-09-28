"""Test reductions, exact parameter-to-representation link, and span closure.
The toy downstream below is NOT S7 and is NOT a trained SAE.
"""
from pathlib import Path
import json,sys
import numpy as np
import torch
from controlled_data import Geometry,generate
from mechanism_core import source_gradient,normalized_delta,measure

torch.set_num_threads(2)
torch.manual_seed(927)
dtype=torch.float64
c0=np.zeros(64);c0[0]=3
Q=np.zeros((64,16));Q[1:17]=np.eye(16)
g=Geometry(c0,Q,.3)
A=generate(g,21001,.8,20,0,16,'A')
B=generate(g,21001,.8,40,0,20,'B')
W=torch.randn((8,64),dtype=dtype)*.025
b=torch.zeros(8,dtype=dtype)
C=lambda x:torch.as_tensor(x,dtype=dtype)
y=lambda x:torch.as_tensor(x,dtype=torch.long)
def tail(a):
    score=a[:,0]+.1*torch.tanh(a[:,1])
    return torch.stack((-score,score),dim=-1)
G=source_gradient(W,b,C(A['c']),y(A['y_same']),tail,7)
G2=source_gradient(W,b,C(A['c']),y(A['y_same']),tail,32)
assert torch.allclose(G,G2,rtol=1e-10,atol=1e-12)
dW=normalized_delta(W,G,1e-4)
QS=torch.eye(8,dtype=dtype)[:,:3]
z=measure(W,b,C(B['c']),y(B['y_same']),torch.zeros_like(W),tail,QS,9)
assert np.array_equal(z['baseline'],z['after']) and np.max(np.abs(z['da']))==0
results=[]
for label in ('y_same','y_flip'):
    r=measure(W,b,C(B['c']),y(B[label]),dW,tail,QS,9)
    assert np.allclose(r['C_S']+r['C_perp'],r['I1'],rtol=1e-12,atol=1e-14)
    assert np.allclose(r['da'],B['c']@dW.numpy().T,rtol=1e-12,atol=1e-12)
    results.append({'rule':label,'mean_I':float(r['I'].mean()),'mean_I1':float(r['I1'].mean()),
                    'closure_error':abs(float(r['I1'].mean())-float(r['I1_from_gradient']))})
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('checks/numerical_core.json')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'status':'PASS','scope':'TOY_KERNEL_TEST_NOT_S7',
    'microbatch_reduction':'PASS','zero_update':'PASS','span_closure':'PASS',
    'torch_version':torch.__version__,'records':results},indent=2)+'\n')
print('PASS: numerical core checks; no S7 model or SAE was used.')
