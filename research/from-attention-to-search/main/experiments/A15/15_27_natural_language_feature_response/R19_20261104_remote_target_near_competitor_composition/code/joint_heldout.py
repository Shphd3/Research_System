from engine import *
from stats_utils import boot_interval,holm,cluster_interval
spec=json.load(open(R/'data/candidates.json'))['sites'];records=[];pairs_rows=[]
for si,site in enumerate(SITES):
 p,z,cache=load_stage('heldout',site);sel=spec[site];features=sel['U'];scale=np.array(sel['scale']);directions=json.load(open(R/f'data/{site}_joint_directions.json'))['kinds'];br,ar,pairs,ix=moments(p,z,features,scale);ids=cache[site+'__indices'];assert np.all(np.count_nonzero(cache[site+'__values'],axis=1)==32)
 binary,audit,snaps=run_binary(ids,p,features,2026110419+si*100000+10000);amplitude=run_amplitude(z,p,features,scale,2026110419+si*100000+60000)
 jsonl(R/f'evidence/{site}_heldout_degree_constraints.jsonl',audit);saved=dict(binary=binary,amplitude=amplitude,real_binary=br,real_amplitude=ar,pairs=pairs,features=np.array(features),scale=scale,**snaps)
 families=sorted({x['family'] for x in p});templates=[next(x['template'] for x in p if x['family']==f) for f in families]
 for kind,real,null in [('binary',br,binary),('amplitude',ar,amplitude)]:
  frozen=directions[kind];jj=frozen['pair_indices'];weights=np.array(frozen['weights']);center=null.mean((0,1));fallback=False
  if not jj:
   records.append(dict(site=site,kind=kind,selected_pairs=0,pair_ids=[],families=12,score=None,lo=None,hi=None,p=1.,eligible=False,mixing=dict(degenerate=True,adequate=False),verdict='INSUFFICIENT_PAIR_SUPPORT'));continue
  traces=np.sum((null[:,:,:,jj]-center[:,jj])*weights,axis=(2,3));mix=mixing(traces)
  if kind=='binary' and not mix['adequate'] and not mix['degenerate']:
   null,au,ss=run_binary(ids,p,features,2026110419+si*100000+10000,burn=500,thin=50);center=null.mean((0,1));traces=np.sum((null[:,:,:,jj]-center[:,jj])*weights,axis=(2,3));mix=mixing(traces);fallback=True;saved['binary_long']=null;jsonl(R/f'evidence/{site}_heldout_degree_constraints_long.jsonl',au)
  observed=float(np.sum((real.mean(1)[:,jj]-center[:,jj])*weights));rowcon=[]
  for f in families:
   percond=np.array([real[k,[j for j,i in enumerate(rr) if p[i]['family']==f]][:,jj].mean(0) for k,rr in enumerate(ix.values())]);rowcon.append(float(np.sum((percond-center[:,jj])*weights)))
  assert abs(np.mean(rowcon)-observed)<1e-10
  lo,hi=boot_interval(rowcon);cl,ch=cluster_interval(rowcon,templates);pval=float((1+np.count_nonzero(traces>=observed-1e-14))/257);eligible=bool(frozen['eligible'] and (kind=='amplitude' or mix['adequate']))
  if not eligible:pval=1.
  records.append(dict(site=site,kind=kind,selected_pairs=len(jj),pair_ids=frozen['pair_ids'],families=12,score=observed,lo=lo,hi=hi,template_lo=cl,template_hi=ch,p=pval,eligible=eligible,mixing=mix,fallback=fallback,discovery_mixing=frozen['discovery_mixing'],family_contributions=dict(zip(families,rowcon)),MC_draws=256,MCSE_upper=float(np.sqrt(.25/256))))
  saved[kind+'_decision_trace']=traces;saved[kind+'_family_contributions']=np.array(rowcon)
  for k,co in enumerate(CONDS):
   for j in jj:
    rowsi=ix[co];fa,fb=[features[n] for n in pairs[j]];pa=float(np.mean(z[rowsi,fa]>0));pb=float(np.mean(z[rowsi,fb]>0));coact=float(np.mean((z[rowsi,fa]>0)&(z[rowsi,fb]>0)))
    pairs_rows.append(dict(site=site,kind=kind,condition=co,atom_a=fa,atom_b=fb,rows=len(rowsi),families=12,active_A=pa,active_B=pb,coactive=coact,coactive_minus_pApB=coact-pa*pb,mean_raw_A=float(np.mean(z[rowsi,fa])),mean_raw_B=float(np.mean(z[rowsi,fb])),real_joint=float(real.mean(1)[k,j]),own_null_mean=float(center[k,j]),residual=float(real.mean(1)[k,j]-center[k,j]),discovery_weight=float(weights[k,jj.index(j)])))
 np.savez_compressed(R/f'cache/{site}_heldout_null.npz',**saved)
adj=holm([x['p'] for x in records])
for x,a in zip(records,adj):
 x['holm_p']=a
 if not x['eligible']:x['verdict']='INSUFFICIENT'
 elif x['lo']>0 and a<=.05:x['verdict']='SUPPORT_IN_THIS_PANEL'
 elif x['hi']<0:x['verdict']='NOT_SUPPORTED'
 else:x['verdict']='INSUFFICIENT'
dump(R/'results/joint_hypotheses.json',records);table(R/'tables/joint_pair_values.csv',pairs_rows);print('JOINT',json.dumps(records,ensure_ascii=False),flush=True)
