"""Independent post-run shape, digest, pair and singular residual audit; no new fits."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='4'
from pathlib import Path
import json,csv,hashlib,time
import numpy as np,torch
from scipy import linalg
r=Path(__file__).resolve().parents[1];cfg=json.load(open(r/'config.json'));man=json.load(open(r/'manifest.json'))
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(n):return list(csv.DictReader(open(r/'tables'/n)))
checks={};freeze=json.load(open(r/'freeze.json'));assert all(sha(Path(p))==h for p,h in freeze['files'].items());checks['initial_freeze']='PASS'
for n in ['comparison','plot']:
 f=json.load(open(r/'audit'/f'{n}_freeze.json'));key='code_sha256' if n=='comparison' else 'sha256';name='compare.py' if n=='comparison' else 'plot.py';assert sha(r/'scripts'/name)==f[key]
checks['comparison_plot_frozen_code']='PASS'
rows=read('matrix_metrics.csv');assert len(rows)==684;ids={(int(x['tokens']),x['module']) for x in rows};assert len(ids)==684
shape={'attn.q':(2048,1024),'attn.k':(1024,1024),'attn.v':(1024,1024),'attn.o':(1024,2048),'gate':(3072,1024),'up':(3072,1024),'down':(1024,3072)}
cache=[];ranks=[]
for row in rows:
 expected=(151936,1024) if row['module']=='embed.weight' else shape[row['module'].split('.',2)[2].removesuffix('.weight')]
 assert (int(row['rows']),int(row['cols']))==expected
 p=Path(row['cache']);m=json.load(open(p.with_suffix('.json')));assert sha(p)==m['npz_sha256'];d=np.load(p);s=d['singular_values'];assert len(s)==1024
 assert np.isclose(float(row['s1']),s[0],rtol=1e-12);assert np.isclose(float(row['total_squared_singular_energy']),sum(s*s),rtol=1e-12)
 ranks.append(dict(module=row['module'],tokens=row['tokens'],numerical_rank=int(sum(s>s[0]*1e-10))))
 cache.append(dict(module=row['module'],tokens=int(row['tokens']),path=str(p),sha256=m['npz_sha256'],key=m['key']))
checks['all684_cache_hashes_shapes_and_scalars']='PASS';assert len(read('excluded_tensors.csv'))==396;checks['396_one_dimensional_gains_excluded']='PASS'
# Reconstruct late pair overlaps independently for every module and both sides.
pairs=read('pair_metrics.csv');assert len(pairs)==57*23*2
late=[x for x in pairs if x['comparison']=='adjacent' and x['tokens']=='31000000000'];maxerr=0.
for m in cfg['modules']:
 a=np.load(r/'cache/31000000000'/(m+'.npz'));b=np.load(r/'cache/33000000000'/(m+'.npz'))
 for side,field in [('input','V'),('output','U')]:
  x=next(z for z in late if z['module']==m and z['side']==side);u=a[field][:,:64];v=b[field][:,:64]
  # Orthogonal-residual formulation avoids using the stored SVD-of-overlap formula.
  cross=v.T@u;dist=float(np.sqrt(max(0.,1.-np.sum(cross*cross)/64)))
  err=abs(dist-float(x['top64_projection_distance']));maxerr=max(maxerr,err);assert err<1e-7
  angle=float(np.degrees(np.arccos(np.clip(abs(a[field][:,0]@b[field][:,0]),0,1))));assert abs(angle-float(x['pc1_angle_raw_diagnostic_deg']))<1e-8
checks['114_late_projection_formula_max_error']=maxerr
# Verify actual singular equations Wv=s*u and W^Tu=s*v on one real late Q matrix.
row=man['checkpoints'][-1];st=torch.load(row['state_path'],map_location='cpu',weights_only=False,mmap=True);key='blocks.7.attn.q.weight';w=st['model'][key].numpy().astype(np.float64);d=np.load(r/'cache'/str(row['tokens'])/(key+'.npz'));u=d['U'];v=d['V'];s=d['singular_values'][:65]
e1=float(np.linalg.norm(w@v-u*s)/np.linalg.norm(w));e2=float(np.linalg.norm(w.T@u-v*s)/np.linalg.norm(w));assert max(e1,e2)<1e-8;checks['late_real_Q_singular_equation_residuals']=[e1,e2]
# Re-evaluate every reported conditional onset from raw pair tables.
onsets=read('tolerance_onsets.csv');assert len(onsets)==57*2*3*9
keys={'s1':('s1_relative_change_symmetric','s1_relative_change_per_B',None),'pc1_angle_deg':('pc1_angle_deg','pc1_angle_per_B','pc1_identifiable'),'top64_projection_distance':('top64_projection_distance','top64_distance_per_B','top64_numeric_identifiable')}
for x in onsets:
 a=sorted([z for z in pairs if z['module']==x['module'] and z['side']==x['side'] and z['comparison']=='adjacent'],key=lambda z:int(z['tokens']));raw,rate,guard=keys[x['metric']];passed=[bool(z[raw] and float(z[raw])<=float(x['raw_tolerance']) and float(z[rate])<=float(x['per_B_tolerance']) and (guard is None or z[guard]=='True')) for z in a];candidates=[i for i in range(9) if all(passed[i:])];wanted=a[candidates[0]]['training_B'] if candidates else ''
 assert (x['onset_training_B']==wanted) or (x['onset_training_B'] and wanted and float(x['onset_training_B'])==float(wanted)),x
checks['3078_conditional_onsets_recomputed']='PASS'
with open(r/'tables/numerical_ranks.csv','w') as f:
 wr=csv.DictWriter(f,fieldnames=list(ranks[0]));wr.writeheader();wr.writerows(ranks)
(r/'cache_index.json').write_text(json.dumps(cache,indent=2)+'\n')
payload_bytes=sum(p.stat().st_size for p in (r/'cache').glob('*/*.npz'));assert payload_bytes<cfg['max_output_gib']*1024**3
checks['basis_payload_bytes']=payload_bytes;checks['no_new_gpu_or_forward']=True
(r/'audit/independent_verification.json').write_text(json.dumps(dict(status='PASS_BOUNDED_AUDIT',checks=checks,scope='all hashes/shapes/scalars;all late pair overlaps;one real late singular-equation check;all conditional onset rows',unverified='Not independent direct SVD for all684;not independent pretraining replicates or future training'),indent=2)+'\n')
print(json.dumps(checks),flush=True)
