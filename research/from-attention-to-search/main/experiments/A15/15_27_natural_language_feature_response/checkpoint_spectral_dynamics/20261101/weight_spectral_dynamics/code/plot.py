"""All-module weight dynamics panels from frozen measured CSVs; no case selection."""
from pathlib import Path
import json,csv,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];CFG=json.load(open(ROOT/'config.json'))
def read(n):return list(csv.DictReader(open(ROOT/'tables'/n)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def label(m):return 'tied embed/output' if m=='embed.weight' else m.replace('blocks.','B').replace('.weight','').replace('attn.','')
def main():
 rows=read('pair_metrics.csv');ts=CFG['checkpoint_tokens'];mods=CFG['modules'];labels=[label(m) for m in mods];manifest={}
 # Dense row order preserves every module; no averaging or selected examples.
 plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
 def heat_figure(name,metrics,title):
  fig,ax=plt.subplots(1,len(metrics),figsize=(4.5*len(metrics)+1,15),squeeze=False);ax=ax[0]
  for j,(metric,side,text,vmax,cmap) in enumerate(metrics):
   values=np.full((len(mods),len(ts)-1),np.nan)
   for i,m in enumerate(mods):
    for k,(t,u) in enumerate(zip(ts[:-1],ts[1:])):
     r=next(r for r in rows if r['module']==m and r['side']==side and r['comparison']=='adjacent' and int(r['tokens'])==t)
     v=r[metric];values[i,k]=float(v) if v else np.nan
     if metric.startswith('top64') and r['top64_numeric_identifiable']!='True':values[i,k]=np.nan
   cm=plt.colormaps[cmap].copy();cm.set_bad('#bcbcbc')
   if metric=='s1_relative_change_symmetric':
    values*=100;vmax=max(vmax,float(np.nanmax(values)))
   img=ax[j].imshow(values,aspect='auto',interpolation='nearest',cmap=cm,vmin=0,vmax=vmax)
   ax[j].set_title(text,pad=10);ax[j].set_xticks(range(11),[f'{t/1e9:g}' for t in ts[1:]],rotation=65,ha='right');ax[j].set_xlabel('Interval right endpoint (training B)')
   ax[j].set_yticks(range(len(mods)),labels if j==0 else ['']*len(mods),fontsize=8)
   for y in np.arange(.5,len(mods),7):ax[j].axhline(y,color='white',lw=.7,alpha=.8)
   fig.colorbar(img,ax=ax[j],fraction=.03,pad=.02)
  fig.suptitle(title,fontsize=14,y=.994)
  mask_note=('Gray = first direction is not isolated under the frozen 5% singular-gap guard.' if name=='figure1_weight_top1' else 'Gray = the 64/65 cutoff is numerically unresolved; weak gaps remain in the source table.')
  fig.text(.02,.015,'Every cell is a measured adjacent interval; gaps differ (0.5 to 8.9813 training B). Read rates in the source table.\n'+mask_note+' No sampling error bars.\n57 native 2D weights x 12 checkpoints; raw W[out,in], no centering. Tied embedding/output counted once.',fontsize=8)
  fig.tight_layout(rect=(0,.065,1,.98));fig.savefig(ROOT/'figures'/f'{name}.png',dpi=180);fig.savefig(ROOT/'figures'/f'{name}.pdf');plt.close(fig)
  manifest[name]=dict(question=title,sources={'pair_metrics.csv':sha(ROOT/'tables/pair_metrics.csv')},rows='all57modules,no selected examples',columns='11actual adjacent intervals;right endpoint labels,see token_gap_B',metrics=[dict(column=m,side=s,meaning=t,color_range=[0,v]) for m,s,t,v,c in metrics],uncertainty='No text-samplingCI;full saved matrices,numerical guards and single-run boundary')
 heat_figure('figure1_weight_top1',[('s1_relative_change_symmetric','input','Largest singular-value change (%)',30,'viridis'),('pc1_angle_deg','input','First input direction angle (degrees)',90,'magma'),('pc1_angle_deg','output','First output direction angle (degrees)',90,'magma')],'Dense weights: magnitude and first-direction changes are different')
 heat_figure('figure2_weight_top64',[('top64_projection_distance','input','Top64 input-space distance',1,'viridis'),('top64_projection_distance','output','Top64 output-space distance',1,'viridis')],'Dense weights: leading64 subspace changes in native coordinates')
 # Optional magnitude view, all blocks retained rather than a chosen attractive curve.
 mm=read('matrix_metrics.csv');fig,axs=plt.subplots(2,4,figsize=(15,7));groups=['embed','attn.q','attn.k','attn.v','attn.o','gate','up','down'];cm=plt.colormaps['viridis']
 for ax,group in zip(axs.flat,groups):
  selected=[m for m in mods if (m=='embed.weight' if group=='embed' else f'.{group}.weight' in m)]
  for i,m in enumerate(selected):
   data=sorted([r for r in mm if r['module']==m],key=lambda r:int(r['tokens']));ax.plot([float(r['training_B']) for r in data],[float(r['s1']) for r in data],'o-',ms=2,lw=1,color=cm(i/7) if len(selected)>1 else '#315b92',label=label(m))
  ax.set(title=group,xlabel='Training B',ylabel='Largest singular value of native W');ax.grid(alpha=.15)
  if len(selected)>1:ax.legend(fontsize=6,ncol=2)
 fig.suptitle('Largest weight singular value: every native module, uncentered',fontsize=14);fig.tight_layout(rect=(0,.04,1,.96));fig.text(.01,.008,'12 measured checkpoints; connecting lines are not missing measurements. Exact per-module values in matrix_metrics.csv. No sampling error bars.',fontsize=8);fig.savefig(ROOT/'figures/figureS_weight_s1_curves.png',dpi=180);fig.savefig(ROOT/'figures/figureS_weight_s1_curves.pdf');plt.close(fig)
 manifest['figureS_weight_s1_curves']=dict(source_sha256=sha(ROOT/'tables/matrix_metrics.csv'),scope='all57modules across8type panels;colors distinguish block,not statistical replicates',x='actual cumulative trainingB',y='s1 uncentered native weight,each panel independent scale')
 (ROOT/'figures/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('FIGURES_COMPLETE',flush=True)
if __name__=='__main__':main()
