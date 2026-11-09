"""Compare native input/output weight SVD spaces; tolerance grid is descriptive only."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='4'
from pathlib import Path
import csv,json,time,datetime,hashlib
import numpy as np
from scipy import linalg
ROOT=Path(__file__).resolve().parents[1];CFG=json.load(open(ROOT/'config.json'));MAN=json.load(open(ROOT/'manifest.json'))
def read(n):return list(csv.DictReader(open(ROOT/'tables'/n)))
def write(n,rows):
 with open(ROOT/'tables'/n,'w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def js(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def dspace(a,b):
 c=np.clip(linalg.svdvals(a.T@b),0,1);ang=np.arccos(c)
 return dict(projection_distance=float(np.sqrt(np.mean(1-c*c))),angle_rms_deg=float(np.degrees(np.sqrt(np.mean(ang*ang)))),angle_max_deg=float(np.degrees(max(ang))))
def blockrank(a,b):
 for k in range(1,65):
  if min((a[k-1]-a[k])/a[k-1],(b[k-1]-b[k])/b[k-1])>=.05:return k
 return 0
def main():
 start=time.time();ts=CFG['checkpoint_tokens'];rows=[];spectra=[];summ={ (int(x['tokens']),x['module']):x for x in read('matrix_metrics.csv')}
 assert len(summ)==684
 for module in CFG['modules']:
  cached={t:dict(np.load(ROOT/'cache'/str(t)/(module+'.npz'))) for t in ts}
  for t in ts:
   for k,s in enumerate(cached[t]['singular_values'],1):spectra.append(dict(module=module,tokens=t,training_B=t/1e9,index=k,singular_value=float(s)))
  for kind,pairs in [('adjacent',list(zip(ts[:-1],ts[1:]))),('endpoint',[(t,ts[-1]) for t in ts])]:
   for t,u in pairs:
    a=cached[t];b=cached[u];gap=abs(t-u)/1e9;s=a['singular_values'];z=b['singular_values'];rel=float(abs(s[0]-z[0])/np.sqrt(s[0]*z[0]));eligible=min((s[0]-s[1])/s[0],(z[0]-z[1])/z[0])>=.05;block=blockrank(s,z)
    for side in ['input','output']:
     aa=a['V' if side=='input' else 'U'];bb=b['V' if side=='input' else 'U'];cross=aa.T@bb;cos=float(np.clip(abs(cross[0,0]),0,1));angle=float(np.degrees(np.arccos(cos)));c=np.clip(linalg.svdvals(cross[:64,:64]),0,1);angs=np.arccos(c);proj=float(np.sqrt(np.mean(1-c*c)))
     if t==u:angle=0.;proj=0.;angs=np.zeros_like(angs)
     identifiable=min((s[63]-s[64])/s[63],(z[63]-z[64])/z[63])>CFG['numerical_gap_floor']
     row=dict(module=module,side=side,comparison=kind,tokens=t,comparison_tokens=u,training_B=t/1e9,comparison_B=u/1e9,token_gap_B=gap,s1_source=float(s[0]),s1_target=float(z[0]),s1_relative_change_symmetric=rel,s1_relative_change_per_B=rel/gap if gap else None,pc1_angle_deg=angle if eligible else None,pc1_angle_raw_diagnostic_deg=angle,pc1_identifiable=bool(eligible),pc1_angle_per_B=angle/gap if gap and eligible else None,first_identifiable_block_rank=block,leading_block_distance=dspace(aa[:,:block],bb[:,:block])['projection_distance'] if block and not eligible else None,top64_projection_distance=proj,top64_distance_per_B=proj/gap if gap else None,top64_angle_rms_deg=float(np.degrees(np.sqrt(np.mean(angs*angs)))),top64_angle_max_deg=float(np.degrees(max(angs))),top64_numeric_identifiable=bool(identifiable),minimum_gap1_relative=float(min((s[0]-s[1])/s[0],(z[0]-z[1])/z[0])),minimum_gap64_relative=float(min((s[63]-s[64])/s[63],(z[63]-z[64])/z[63])))
     rows.append(row)
  print('MODULE_COMPARED',module,'elapsed',round(time.time()-start,1),flush=True);del cached
 write('pair_metrics.csv',rows);write('spectrum.csv',spectra)
 # Earliest terminal suffix of >=3observed intervals satisfying BOTH displacement and progress-normalized bounds.
 onset=[]
 for module in CFG['modules']:
  for side in ['input','output']:
   adj=sorted([r for r in rows if r['module']==module and r['side']==side and r['comparison']=='adjacent'],key=lambda r:r['tokens'])
   for metric,raw,rate,guard in [('s1','s1_relative_change_symmetric','s1_relative_change_per_B',None),('pc1_angle_deg','pc1_angle_deg','pc1_angle_per_B','pc1_identifiable'),('top64_projection_distance','top64_projection_distance','top64_distance_per_B','top64_numeric_identifiable')]:
    grid=CFG['stability_tolerances'][metric]
    for tol in grid['raw']:
     for tr in grid['per_B']:
      good=[bool(r[raw] is not None and r[raw]<=tol and r[rate]<=tr and (guard is None or r[guard])) for r in adj];earliest=None
      for i in range(len(good)-2):
       if all(good[i:]):earliest=i;break
      onset.append(dict(module=module,side=side,metric=metric,raw_tolerance=tol,per_B_tolerance=tr,onset_training_B=adj[earliest]['training_B'] if earliest is not None else None,consecutive_intervals=len(good)-earliest if earliest is not None else 0,last_interval_pass=good[-1],status='CONDITIONAL_WITHIN_WINDOW_TOLERANCE' if earliest is not None else 'NOT_ESTABLISHED',scientific_tolerance='AI_PROPOSAL_SENSITIVITY_ONLY'))
 write('tolerance_onsets.csv',onset)
 late=[r for r in rows if r['comparison']=='adjacent' and r['comparison_tokens']==ts[-1]];write('late_interval.csv',late)
 # Module/side robustness over all nine predeclared tolerance settings, no selected best grid.
 robust=[]
 for module in CFG['modules']:
  for side in ['input','output']:
   for metric in CFG['stability_tolerances']:
    a=[r for r in onset if r['module']==module and r['side']==side and r['metric']==metric];vals=[r['onset_training_B'] for r in a if r['onset_training_B'] is not None]
    robust.append(dict(module=module,side=side,metric=metric,grids_with_onset=len(vals),total_grids=len(a),earliest_conditional_onset=min(vals) if vals else None,latest_conditional_onset=max(vals) if vals else None,interpretation='ALL_GRID_PASS' if len(vals)==len(a) else 'THRESHOLD_DEPENDENT' if vals else 'NO_GRID_ONSET'))
 write('onset_sensitivity_summary.csv',robust)
 js(ROOT/'audit/comparison_complete.json',dict(status='PASS',module_states=len(summ),paired_rows=len(rows),spectrum_rows=len(spectra),tolerance_rows=len(onset),seconds=time.time()-start,new_forwards=0,scientific_acceptance='Unknown'))
if __name__=='__main__':main()
