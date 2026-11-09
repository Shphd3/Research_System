from common import *
import itertools
def interval(v,seed=SEED,n=8192):
 v=np.asarray(v,float);v=v[np.isfinite(v)]
 if not len(v):return [None,None]
 rng=np.random.default_rng(seed);a=v[rng.integers(0,len(v),(n,len(v)))].mean(1);return list(map(float,np.quantile(a,[.025,.975])))
def sign_p(v):
 v=np.asarray(v,float);v=v[np.isfinite(v)]
 if not len(v):return 1.
 signs=np.array(list(itertools.product([-1.,1.],repeat=len(v))));return float(np.mean(signs@v>=sum(v)-1e-12))
def holm(p):
 order=np.argsort(p);out=np.zeros(len(p));old=0.
 for rank,i in enumerate(order):old=max(old,(len(p)-rank)*p[i]);out[i]=min(1.,old)
 return out.tolist()
def summarize(df,field,log=False,seed=SEED):
 q=df.groupby('family',sort=True)[field].mean().dropna();v=q.to_numpy();lo,hi=interval(v,seed);groups=df[['family','template']].drop_duplicates().set_index('family');template=[np.mean([x for f,x in q.items() if groups.loc[f,'template']==t]) for t in sorted(set(groups.loc[q.index,'template']))];tl,th=interval(template,seed)
 if log:return dict(families=len(v),value=float(np.exp(np.mean(v))),lo=float(np.exp(lo)),hi=float(np.exp(hi)),template_lo=float(np.exp(tl)),template_hi=float(np.exp(th)))
 return dict(families=len(v),value=float(np.mean(v)),lo=lo,hi=hi,template_lo=tl,template_hi=th)
