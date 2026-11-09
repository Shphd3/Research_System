"""FP64 covariance, spectrum, sample-relation and subspace estimators."""
import numpy as np
from scipy import linalg

def moments(h):
 h=np.asarray(h,dtype=np.float64).reshape(-1,h.shape[-1]);mu=h.mean(0);x=h-mu;n=len(x);c=x.T@x/(n-1)
 w,v=linalg.eigh(c,check_finite=True,driver='evd');w=w[::-1].copy();v=v[:,::-1].copy()
 if w[-1]<-max(w[0],1)*1e-10:raise ValueError('NON_PSD')
 w=np.maximum(w,0);p=w/w.sum()
 err=np.linalg.norm(c@v-v*w,ord='fro')/np.linalg.norm(c,ord='fro');ortho=np.linalg.norm(v.T@v-np.eye(len(w)),ord='fro')
 assert err<1e-8 and ortho<1e-8 and abs(w.sum()-np.trace(c))/np.trace(c)<1e-8
 return dict(mean=mu,cov=c,eigenvalues=w,singular_values=np.sqrt(w*(n-1)),basis=v,p=p,n=n,rank=int(np.sum(w>w[0]*1e-10)),effective_rank=float(np.exp(-np.sum(p[p>0]*np.log(p[p>0])))),eigen_residual=err,orthogonality_error=ortho)

def spectral(w,z):
 p=w/w.sum();q=z/z.sum();a=np.linalg.norm(w-z)
 return dict(absolute_spectrum_l2=float(a),relative_absolute_spectrum_l2=float(a/np.sqrt(np.linalg.norm(w)*np.linalg.norm(z))),normalized_spectrum_TV=float(np.abs(p-q).sum()/2),trace_ratio=float(w.sum()/z.sum()),absolute_trace_difference=float(abs(w.sum()-z.sum())))

def subspace(u,v):
 cos=np.clip(linalg.svdvals(u.T@v),0,1);angles=np.arccos(cos);k=u.shape[1]
 return dict(projection_distance=float(np.linalg.norm(u-v@(v.T@u),'fro')/np.sqrt(k)),angle_rms_deg=float(np.rad2deg(np.sqrt(np.mean(angles**2)))),angle_max_deg=float(np.rad2deg(max(angles)))),angles

def alignment(x,y):
 cross=x.T@y;u,_,vt=linalg.svd(cross,full_matrices=False,check_finite=True);sign=np.linalg.slogdet(u@vt)[0]
 if sign<0:u[:,-1]*=-1
 r=u@vt
 assert np.linalg.norm(r.T@r-np.eye(r.shape[1]))<1e-8
 return r

def cka(x,y):
 # Evaluation-only centering defines a statistic, not a fitted transfer map.
 x=x-x.mean(0);y=y-y.mean(0)
 return float(np.linalg.norm(x.T@y,'fro')**2/(np.linalg.norm(x.T@x,'fro')*np.linalg.norm(y.T@y,'fro')))

def stream_cka(x,y,chunk=2048):
 # Sufficient statistics avoid N-by-N Gram; correct each sum by outer means.
 n=len(x);d=x.shape[1];sx=np.zeros(d);sy=np.zeros(d);xx=np.zeros((d,d));yy=xx.copy();xy=xx.copy()
 for i in range(0,n,chunk):
  a=np.asarray(x[i:i+chunk],np.float64);b=np.asarray(y[i:i+chunk],np.float64);sx+=a.sum(0);sy+=b.sum(0);xx+=a.T@a;yy+=b.T@b;xy+=a.T@b
 xx-=np.outer(sx,sx)/n;yy-=np.outer(sy,sy)/n;xy-=np.outer(sx,sy)/n
 return float(np.linalg.norm(xy,'fro')**2/(np.linalg.norm(xx,'fro')*np.linalg.norm(yy,'fro')))
