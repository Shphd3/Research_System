"""Known-formula/data unit tests. NOT a new empirical mechanism result."""
from pathlib import Path
import json, sys
import numpy as np
from controlled_data import Geometry, signed_qr, generate, directions, witness

out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('checks/calibration.json')
out.parent.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(927)
c0=np.zeros(64); c0[0]=3.0
Q=np.zeros((64,16)); Q[1:17]=np.eye(16)
g=Geometry(c0,Q,0.3)
rows=[]
for rho in (0.0,0.1,0.8):
    va,vb,_=directions(g,21001,rho)
    for s in (-1,1):
        wstar=(va+s*vb)/(1+s*rho)
        assert abs(wstar@va-1)<1e-12 and abs(wstar@vb-s)<1e-12
        for eta in (0.1,0.05):
            actual=0.5*(eta*(va@vb)-s)**2-0.5
            expected=-eta*rho*s+0.5*eta**2*rho**2
            assert abs(actual-expected)<1e-12
            rows.append(dict(rho=rho,rule=s,eta=eta,I=actual,formula=expected))
A=generate(g,21001,.8,40,0,10,'A')
B=generate(g,21001,.8,40,0,10,'B')
BL=generate(g,21001,.1,40,0,10,'B')
assert np.all(A['y_same']==1-A['y_flip'])
assert np.max(np.abs(np.linalg.norm(B['c'],axis=1)-np.linalg.norm(BL['c'],axis=1)))<1e-5
# Constructive certificate through a hypothetical downstream with two endpoints.
ap=np.array([2.,.1]); am=np.array([-2.,-.1]); bias=np.array([.1,-.2])
for rho in (.1,.8):
    for s in (-1,1):
        W=witness(g,21001,rho,s,ap,am,bias)
        for group in ('A','B'):
            data=generate(g,21001,rho,30,0,32,group)
            signs=data['t']*(1 if group=='A' else s)
            expected=np.where((signs>0)[:,None],ap,am)
            assert np.max(np.abs(data['c']@W.T+bias-expected))<1e-5
try:
    directions(g,21001,1.0)
    raise AssertionError('rho=1 was not rejected')
except ValueError: pass
receipt={'status':'PASS','scope':'DATA_AND_ANALYTIC_UNIT_TEST_ONLY',
         's7_experiment':'NOT_RUN','analytic_cases':rows,
         'shared_solution_certificate':'PASS','matched_input_norms':'PASS',
         'numpy_version':np.__version__}
out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print('PASS: analytic/data unit checks; no S7 experiment ran.')
