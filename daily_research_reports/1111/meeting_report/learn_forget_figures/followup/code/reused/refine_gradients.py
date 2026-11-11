"""Per-A5-group borrowing intervals from saved projections; no new model work."""
from gradients import raw_T
from lf_common import *
from threadpoolctl import threadpool_limits
def main():
 rows=[];norms=[]
 for case,folder,prefix in [('registered1seq',R,''),('precision8seq',R/'precision8','precision8/')]:
  scope=json.load(open(folder/'evidence/fig2_complete.json'))['groups'];co=pd.read_csv(R/f'results/{prefix}fig2_transfer_coefficients.csv');rng=np.random.default_rng(20261111);weights=rng.multinomial(4,np.full(4,.25),size=2000)
  for p in sorted((folder/'gradient').glob('*_sketch.npy')):
   kind,token,block,_=p.stem.split('_');t=int(token);G=np.load(p);K=len(scope);flat=G.reshape(K*4,-1).astype(np.float64);gram=(flat@flat.T).reshape(K,4,K,4);T,sig=raw_T(gram);cache={}
   for w in weights:
    key=tuple(w)
    if key not in cache:cache[key]=raw_T(gram,w)[0]
   for i,g in enumerate(scope):
    if g%2:continue
    same=scope.index(g+1);others=[j for j,h in enumerate(scope) if h%2 and h!=g+1 and np.isfinite(T[i,j])];point_ok=bool(np.isfinite(T[i,same]) and others);v=[]
    for w in weights:
     B=cache[tuple(w)];v.append(B[i,same]-B[i,others].mean() if point_ok and np.isfinite(B[i,same]) and np.isfinite(B[i,others]).all() else np.nan)
    v=np.asarray(v);good=np.isfinite(v);ci=np.quantile(v[good],[.025,.975]) if good.any() else [np.nan,np.nan];difference=float(T[i,same]-T[i,others].mean()) if point_ok else np.nan
    rows.append(dict(case=case,model=kind,tokens=t,block=block,A5_group=g//2,T_same_low_high=float(T[i,same]),mean_T_other_high=float(T[i,others].mean()) if others else np.nan,difference=difference,ci95_low=ci[0],ci95_high=ci[1],fixed_other_groups=len(others),valid_bootstrap_fraction=float(good.mean()),rule_result='信号不足' if not point_ok else '低频从共现高频借力' if ci[0]>0 else '分不出'))
   audit=pd.read_csv(R/f'results/{prefix}fig2_norm_audit_{kind}_{t}.csv');z=audit[audit.block==block];ratio=z.projected_norm_squared/z.exact_gradient_norm_squared;norms.append(dict(case=case,model=kind,tokens=t,block=block,min_sketch_to_exact_norm2=float(ratio.min()),max_sketch_to_exact_norm2=float(ratio.max()),mean_sketch_to_exact_norm2=float(ratio.mean())))
 table(pd.DataFrame(rows),'fig2_borrowing_by_A5_group','Each group separately; fixed original-point validother-highgroups retained across bootstrap. If any required signal invalid in a resample, that resample is missing. This is a precision-sensitive local readout,not a long-term architecture verdict.')
 table(pd.DataFrame(norms),'fig2_projection_norm_calibration','Exactgradientnorm2 versus CountSketchnorm2; normagreement does not certify everynear-zero cross-group innerproduct sign.')
 dump(R/'evidence/gradient_refinement_complete.json',dict(rows=len(rows),cases=2,readout_only=True,additional_backward_passes=0))
if __name__=='__main__':
 with threadpool_limits(limits=4):main()
