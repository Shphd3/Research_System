from engine import *
from scipy.stats import chisquare
import collections
# Enumerated small fixed-degree state space, independent of research activations.
patterns=list(itertools.combinations(range(4),2));space=[]
for rs in itertools.product(patterns,repeat=4):
 a=np.array(rs,np.int32)
 if np.all(np.bincount(a.ravel(),minlength=4)==2):space.append(tuple(a.ravel()))
a=np.array(space[0],np.int32).reshape(4,2);h=LIB.create_chain(a.ctypes.data_as(ct.POINTER(ct.c_int32)),4,2,839124);LIB.advance_chain(h,1000);out=np.zeros_like(a);counts=collections.Counter()
for _ in range(20000):
 LIB.advance_chain(h,5);LIB.copy_rows(h,out.ctypes.data_as(ct.POINTER(ct.c_int32)));assert np.all(np.diff(out,axis=1)>0);assert np.all(np.bincount(out.ravel(),minlength=4)==2);counts[tuple(out.ravel())]+=1
LIB.free_chain(h);cv=np.array([counts[t] for t in space]);test=chisquare(cv);assert len(counts)==len(space);assert test.pvalue>1e-4
p=np.tile(np.arange(32,dtype=np.int32),(4,1));obj=Sampler(p,8);obj.advance(100);z=obj.snapshot();assert np.array_equal(z,p);locked=obj.audit();assert locked['locked_edge_fraction']==1;obj.close()
dump(R/'evidence/sampler_calibration.json',dict(UTC=now(),status='PASS',enumerated_states=len(space),sampled_states=len(counts),draws=20000,chi_square=float(test.statistic),p=float(test.pvalue),note='Numerical implementation calibration only; does not prove research-chain mixing',fully_locked_matrix=locked,cpp_sha256=sha(R/'code/curveball.cpp')))
print('CALIBRATION_PASS',len(space),test)
