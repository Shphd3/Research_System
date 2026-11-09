"""Independent reaggregation of every main number from raw per-position arrays."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='2'
from pathlib import Path
import json,hashlib,numpy as np,pandas as pd
E=Path(__file__).resolve().parents[1]
def rows(p):return [json.loads(l) for l in Path(p).read_text().splitlines() if l]
def main():
 R=rows(E/'data/prefixes.jsonl');positions=rows(E/'data/positions.jsonl');conditions=json.load(open(E/'data/conditions.json'));cfg=json.load(open(E/'config.json'));F=pd.read_csv(E/'analysis/family_metrics.csv');S=pd.read_csv(E/'analysis/summary.csv');C=pd.read_csv(E/'analysis/primary_feature_contrasts.csv');errors=[];expected={};full_cache={};counts={};maxerr=0.
 for c in conditions['unique']:
  name=c['condition'];A=np.load(E/'analysis'/f'condition_{name}.npz');lp=A['logp'];
  for k in A.files:
   if not np.isfinite(A[k]).all():errors.append(['NONFINITE',name,k])
  if (A['first_diagnostics'][:,1]<-1e-5).any():errors.append(['NEGATIVE_KL',name,float(A['first_diagnostics'][:,1].min())])
  if (A['first_diagnostics'][:,2]<0).any():errors.append(['NEGATIVE_ENTROPY',name])
  raw={};perfamily={};counters={}
  for r in R:
   if r['split']!='evaluation':continue
   ans={}
   for j,k in enumerate(['U','V','A','B']):
    a=r['candidate_map'][k];ix=np.array(a['position_indices']);cols=np.zeros(len(ix),int);cols[0]=j;ans[k]=float(np.sum(lp[ix,cols],dtype=np.float64))
   raw[r['prefix_id']]={'r':ans['A']-ans['B'],'upper':ans['U']-ans['V']}
  for fid in sorted({r['family_id'] for r in R if r['split']=='evaluation'}):
   domain=fid.rsplit('_',1)[0];m=[]
   for p in [0,1]:
    z={k:raw[f'{fid}_p{p}_{k}'] for k in ['broad','A','B']};m.append({'J':(z['A']['r']-z['B']['r'])/2,'gA':z['A']['r']-z['broad']['r'],'gB':z['broad']['r']-z['B']['r'],'specific_correct':(int(z['A']['r']>0)+int(z['B']['r']<0))/2,'upper_correct':sum(int(z[k]['upper']>0) for k in z)/3,'both_correct':int(z['A']['r']>0 and z['B']['r']<0)})
   mf={k:np.mean([x[k] for x in m]) for k in m[0]};perfamily[fid]=mf
   row=F[(F.condition==name)&(F.family_id==fid)].iloc[0]
   for k,v in mf.items():
    err=abs(row[k]-v);maxerr=max(maxerr,err)
    if err>1e-9:errors.append([name,fid,k,v,float(row[k])])
  expected[name]=perfamily
  for d in ['biology','mathematics','physics','overall_equal_domains']:
   ids=[f for f in perfamily if d=='overall_equal_domains' or f.startswith(d+'_')];row=S[(S.condition==name)&(S.domain==d)].iloc[0]
   for k in ['J','gA','gB','specific_correct','upper_correct','both_correct']:
    v=np.mean([perfamily[f][k] for f in ids]);err=abs(row[k]-v);maxerr=max(maxerr,err)
    if err>1e-9:errors.append([name,d,k,v,float(row[k])])
   for score,den,countcol in [('specific_correct',4,'specific_correct_count'),('upper_correct',6,'upper_correct_count'),('both_correct',2,'both_correct_count')]:
    count=int(np.rint(sum(perfamily[f][score]*den for f in ids)))
    if row[countcol]!=count:errors.append(['COUNT',name,d,countcol,count,float(row[countcol])])
 # Primary contrasts and intervals reconstructed without using all_paired_contrasts.csv.
 draws=np.load(E/'analysis/bootstrap_family_draws.npz');full=expected['full']
 for _,r in C.iterrows():
  g=r['group'];target=expected['feature_delete_'+g];controls=[f'feature_delete_random_{g}_{seed}' if r.control_type=='same_count' else f'feature_normmatch_{g}_{seed}' for seed in cfg['random_seeds']];ds=['biology','mathematics','physics'] if r.domain=='overall_equal_domains' else [r.domain];means=[];boots=[]
  for d in ds:
   ids=sorted(f for f in full if f.startswith(d+'_'));excess=np.array([np.mean([expected[c][f]['J'] for c in controls])-target[f]['J'] for f in ids]);means.append(excess.mean());boots.append(excess[draws[d]].mean(1))
  b=np.mean(boots,0);want={'excess_J_loss':np.mean(means),'low95':np.quantile(b,.025),'high95':np.quantile(b,.975),'low_simultaneous6':np.quantile(b,.05/12),'high_simultaneous6':np.quantile(b,1-.05/12)}
  for k,v in want.items():
   err=abs(r[k]-v);maxerr=max(maxerr,err)
   if err>1e-8:errors.append(['PRIMARY',g,r.domain,r.control_type,k,v,float(r[k])])
 # Boundaries and no-op checks tied to input data, not filename claims.
 w=np.load(E/'data/wanted_token_ids.npy');boundary_ok=True
 for r in R:
  pre=r['prefix_token_ids']
  for j,k in enumerate(['U','V','A','B']):
   a=r['candidate_map'][k]
   for ai,ix in enumerate(a['position_indices']):
    p=positions[ix];boundary_ok &= (p['model_position']==len(pre)-1+ai and p['visible_token_ids']==pre+a['token_ids'][:ai] and w[ix,j if ai==0 else 0]==a['token_ids'][ai])
 groups=json.load(open(E/'data/feature_groups.json'));main_groups=[groups[g] for g in ['low','middle','high','zero_reference','insufficient_positive']];all_ids=sum(main_groups,[]);groups_ok=(len(all_ids)==16384 and len(set(all_ids))==16384)
 for g in ['low','middle','high']:
  for seed in cfg['random_seeds']:
   n=groups[f'random_{g}_{seed}'];groups_ok &= (len(n)==len(groups[g]) and len(set(n))==len(n) and not(set(n)&set(groups[g])))
 B=np.load(E/'data/bases.npz');orth_errors={}
 for seed in cfg['random_seeds']:
  Q=B[f'random_{seed}'];R0=B[f'orthogonal_{seed}'];orth_errors[str(seed)]=float(max(abs(Q.T@Q-np.eye(1024)).max(),abs(R0.T@R0-np.eye(1008)).max(),abs(B['V'][:,:16].T@R0).max()))
 smoke=json.load(open(E/'audit/03_implementation_numerics.json'));initial=json.load(open(E/'audit/freeze_initial.json'));effective=json.load(open(E/'freeze.json'));freeze_ok=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in effective['sha256'].items())
 checks={'no_reaggregation_errors':not errors,'boundary_shift_mask_indices':bool(boundary_ok),'frequency_groups_and_matched_controls':bool(groups_ok),'random_basis_ranks_and_orthogonality':max(orth_errors.values())<1e-10,'new_smoke_pass':bool(smoke['pass']),'effective_frozen_inputs_unchanged':freeze_ok,'all_PC_bit_exact':bool(np.array_equal(np.load(E/'analysis/condition_full.npz')['logp'],np.load(E/'analysis/condition_keep_head1024.npz')['logp']))}
 out={'pass':all(checks.values()),'checks':checks,'max_main_value_absolute_error':maxerr,'reaggregated_conditions':len(expected),'reaggregated_evaluation_families_per_condition':36,'reaggregated_primary_rows':len(C),'errors':errors,'random_orthogonality_max':orth_errors,'initial_protocol_preserved':initial['protocol_sha256']==hashlib.sha256((E/'protocol.md').read_bytes()).hexdigest()}
 (E/'audit/independent_reaggregation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['pass']
if __name__=='__main__':main()
