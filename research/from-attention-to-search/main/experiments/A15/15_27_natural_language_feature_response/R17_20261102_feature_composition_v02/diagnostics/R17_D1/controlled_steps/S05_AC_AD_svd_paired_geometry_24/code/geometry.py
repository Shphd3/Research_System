import numpy as np
def fit_svd(x):
 mean=x.mean(axis=0);centered=x-mean;U,s,V=np.linalg.svd(centered,full_matrices=False)
 for j in range(len(s)):
  pivot=int(np.argmax(abs(V[j])))
  if V[j,pivot]<0:V[j]*=-1;U[:,j]*=-1
 tol=max(x.shape)*np.finfo(np.float64).eps*s[0] if len(s) else 0
 return dict(mean=mean,centered=centered,singular_values=s,components=V,rank=int((s>tol).sum()),rank_tol=tol,U=U)
def signed_cos(a,b,tol):
 n=np.linalg.norm(a)*np.linalg.norm(b)
 return None if np.linalg.norm(a)<=tol or np.linalg.norm(b)<=tol else float(np.clip(a@b/n,-1,1))
def compare(a,b,k):
 if a['rank']<k or b['rank']<k:return dict(valid=False,abs_cosine=None,normalized_overlap=None,angles_degrees=None)
 A=a['components'][:k];B=b['components'][:k];sv=np.clip(np.linalg.svd(A@B.T,compute_uv=False),0,1)
 return dict(valid=True,abs_cosine=float(abs(A[0]@B[0])) if k==1 else None,normalized_overlap=float(np.sum((A@B.T)**2)/k),angles_degrees=np.degrees(np.arccos(sv)).tolist())
def decompose(parent,fine):
 a=parent>0;b=fine>0;delta=fine-parent
 masks=[a&b,(~a)&b,a&(~b)]
 return delta,np.stack([np.where(m,delta,0) for m in masks]),masks
