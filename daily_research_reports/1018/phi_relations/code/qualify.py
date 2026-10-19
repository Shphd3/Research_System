#!/usr/bin/env python3
"""Small counterexamples and direct enumeration qualify conditional statistics."""
import importlib.util
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('analysis',ROOT/'analyze.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def aggregate(A,b,s,B,S):
    c=np.zeros((B,S,A.shape[1]));n=np.zeros((B,S));np.add.at(c,(b,s),A);np.add.at(n,(b,s),1)
    K=A.sum(1);num=np.bincount(b,weights=K*(K-1),minlength=B)
    return c,n,num
def run():
    # Relation entirely due to a binary observed condition.
    B=4;A=np.tile(np.array([[0.,0.],[1.,1.]]),(B,1));b=np.repeat(np.arange(B),2);s=np.tile([0,1],B)
    c,n,q=aggregate(A,b,s,B,2);v=a.conditional_stats(np.ones(B),c,n,q,2)
    assert np.allclose(v[:6],[.5,.25,.5,.25,0,.25])
    assert np.allclose(v[[6,7,8,9,10]],[.25,.5,.25,0,.25])
    condition_example=v.copy()
    # Nonuniform real counts; brute ordered feature pairs and cross-block positions.
    rng=np.random.default_rng(7);b=np.repeat(np.arange(4),7);s=np.tile([0,0,0,1,1,1,1],4)
    A=(rng.uniform(size=(28,3))<np.array([.2,.5,.8])).astype(float)
    c,n,q=aggregate(A,b,s,4,2);v=a.conditional_stats(np.ones(4),c,n,q,3)
    manual=0.
    for cell in (0,1):
        ii=np.flatnonzero(s==cell);summed=0.;pairs=0
        for x in ii:
            for y in ii:
                if b[x]==b[y]:continue
                summed+=sum(A[x,i]*A[y,j] for i in range(3) for j in range(3) if i!=j);pairs+=1
        manual+=len(ii)/len(A)*summed/pairs/6
    assert abs(v[7]-manual)<1e-13,(v[7],manual)
    result={'status':'PASS','observed_condition_counterexample':dict(zip(a.METRICS,condition_example.tolist())),
            'explicit_cross_block_enumeration_error':abs(v[7]-manual),
            'checks':['condition-only dependence removed as expected','ordered pair denominator matches direct enumeration','cross-block uses counts and excludes within-block position pairs'],
            'scientific_validation':False}
    a.dump(a.OUT/'estimator_qualification.json',result);print('ESTIMATOR_QUALIFICATION_PASS')
if __name__=='__main__':run()
