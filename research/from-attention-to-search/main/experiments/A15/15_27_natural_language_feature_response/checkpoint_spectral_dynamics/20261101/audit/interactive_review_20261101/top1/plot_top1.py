"""User-requested leading singular-value curve from frozen tables; no refit/forward."""
from pathlib import Path
import csv,json,hashlib,datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path('/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics')
OUT=Path(__file__).resolve().parent
CAN=Path('/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(n):return list(csv.DictReader(open(ROOT/'analysis'/n)))
rows=[r for r in read('spectrum.csv') if r['index']=='1'];assert len(rows)==12
N=32768;summary=[]
for r in rows:
 s=float(r['singular_value']);lam=float(r['eigenvalue']);assert np.isclose(s*s/(N-1),lam,rtol=1e-12)
 cached=np.load(ROOT/'analysis/stats'/f"{r['tokens']}_layer7.npz")
 assert np.isclose(float(cached['singular_values'][0]),s,rtol=1e-12)
 summary.append({k:r[k] for k in ['tokens','training_B','singular_value','eigenvalue','normalized_eigenvalue']})
with open(OUT/'top1_values.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
dirs=[]
for r in read('isolated_vector_diagnostics.csv'):
 if r['index']!='1':continue
 assert r['eligible']=='True'
 a=np.load(ROOT/'analysis/stats'/f"{r['tokens']}_layer7.npz")['basis'][:,0]
 b=np.load(ROOT/'analysis/stats'/f"{r['comparison_tokens']}_layer7.npz")['basis'][:,0]
 cos=float(np.clip(abs(a@b),0,1));assert abs(cos-float(r['absolute_cosine']))<1e-12
 dirs.append(dict(comparison=r['comparison'],tokens=r['tokens'],comparison_tokens=r['comparison_tokens'],token_gap_B=abs(int(r['comparison_tokens'])-int(r['tokens']))/1e9,absolute_cosine=cos,sign_invariant_angle_deg=float(np.degrees(np.arccos(cos))),source_relative_gap=float(r['source_relative_gap']),target_relative_gap=float(r['target_relative_gap'])))
with open(OUT/'top1_direction_checks.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(dirs[0]));w.writeheader();w.writerows(dirs)
sens=[]
for t in [500000000,3000000000,17000000000,33000000000]:
 angles=[]
 for rep in range(8):
  a=np.load(ROOT/'analysis/splitstats'/f'{t}_{rep}_0.npz')['basis'][:,0];b=np.load(ROOT/'analysis/splitstats'/f'{t}_{rep}_1.npz')['basis'][:,0]
  angles.append(float(np.degrees(np.arccos(np.clip(abs(a@b),0,1)))))
 q=np.quantile(angles,[.025,.5,.975]);sens.append(dict(tokens=t,lower=float(q[0]),median=float(q[1]),upper=float(q[2]),unit='degrees',meaning='8 fixed 512/512 record half-splits; descriptive range, not population confidence interval'))
(OUT/'top1_sampling_sensitivity.json').write_text(json.dumps(sens,indent=2)+'\n')
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,4.8));x=np.array([float(r['training_B']) for r in rows]);y=np.array([float(r['singular_value']) for r in rows])
ax.plot(x,y,'o-',color='#315b92',lw=1.8,ms=5)
for t,offset in [(.5,(5,9)),(10.,(-15,12)),(15.,(-9,-22)),(31.,(-55,-23)),(33.,(-42,12))]:
 i=np.flatnonzero(x==t)[0];ax.annotate(f'{y[i]:,.0f}',(x[i],y[i]),xytext=offset,textcoords='offset points',fontsize=10)
ax.set(xlabel='Cumulative valid training tokens (B)',ylabel='Largest singular value of centered X: s1',xlim=(-.3,34.5),ylim=(0,31000),title='Dense final residual-post: leading singular-value magnitude')
ax.set_xticks([.5,5,10,15,20,25,30,33]);ax.grid(alpha=.2)
fig.text(.11,.01,'N = 32,768 fixed positions from 1,024 reference records; own mean at each checkpoint.\n12 measured states; lines are reading aids, not measurements of missing states. No error bars.',fontsize=8.5)
fig.tight_layout(rect=(0,.08,1,1));fig.savefig(OUT/'figure_top1_singular_value.png',dpi=180);fig.savefig(OUT/'figure_top1_singular_value.pdf');plt.close(fig)
manifest=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request='User asks x=training tokens,y=largest singular value; separate direction tracking from magnitude.',run='pt-0o94658v',effective_version='Frozen run; A01/A02/A03 preserved. Added cache-only plot; no changes to original protocol or results.',model='native Dense,281431040 parameters,8 blocks,hidden1024',tensor='final_raw_h: final block residual-post,before model.norm',rows=12,N=N,documents=1024,positions_per_document=32,formula='X=reference activations minus own checkpoint reference mean; s1=sqrt((N-1)*lambda1)',source_hashes={n:sha(ROOT/'analysis'/n) for n in ['spectrum.csv','isolated_vector_diagnostics.csv','checkpoint_statistics.csv']},code_sha256=sha(__file__),new_forwards=0,new_fits=0,error_bars='none; separately derived half-split direction ranges are descriptive,not population CIs',checks='All 12 s1 match stored statistical NPZ and s1^2/(N-1)=lambda1; all first-direction cosines independently match stored bases; no row filtering other than direction index1.')
(OUT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
dest=CAN/'audit/interactive_review_20261101/top1';dest.mkdir(exist_ok=True)
import shutil
for p in OUT.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name)
print(json.dumps({'figure':str(dest/'figure_top1_singular_value.png'),'s1_change_31_33_percent':(y[-1]/y[-2]-1)*100,'first_direction_angle_31_33_deg':dirs[10]['sign_invariant_angle_deg'],'source_singular_value_rows':len(rows),'min_gap':min(z['source_relative_gap'] for z in dirs)},ensure_ascii=False))
