"""Presentation-only repair: generous margins, short titles and unobstructed legends."""
from common import *
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
panel=rows(R/'data/panel.jsonl');sel=json.load(open(R/'results/selection.json'))['sites']
old=R/'versions/figures_before_layout_repair';assert not old.exists();old.mkdir(parents=True)
before={}
for p in (R/'figures').glob('*.png'):before[p.name]=sha(p);shutil.copy2(p,old/p.name)
def norm(x):
 d=np.linalg.norm(x,axis=1,keepdims=True);return np.divide(x,d,out=np.full_like(x,np.nan),where=d>0)
for site in SITES:
 z=np.concatenate([np.load(R/f'cache/{sp}.npz')[site+'__z'] for sp in ['exploration','heldout_check']]).astype(float);dn=np.load(R/'cache/exploration.npz')[site+'__decoder_norm'];u=z*dn
 for group,ids in [('H1_common',sel[site]['H1_common']),('H2_joint',sel[site]['H2'])]:
  fig,axs=plt.subplots(2,2,figsize=(17,17));fig.subplots_adjust(left=.09,right=.96,bottom=.055,top=.90,hspace=.15,wspace=.29)
  for ax,m,title in zip(axs.flat,[z[:,ids],u[:,ids],norm(z[:,ids]),norm(u[:,ids])],['Raw activation z','Weighted u = z * decoder norm','Relative raw z / L2(z_selected)','Relative weighted u / L2(u_selected)']):
   cm=plt.get_cmap('viridis').copy();cm.set_bad('#bdbdbd');im=ax.imshow(np.ma.masked_invalid(m),aspect='auto',cmap=cm,vmin=0);fig.colorbar(im,ax=ax,shrink=.7,fraction=.04,pad=.035)
   ax.set_xticks(range(len(ids)),ids,fontsize=10);ax.set_yticks(range(24),[f'{p["family"]} {p["condition"]} '+('E' if p['split']=='exploration' else 'H') for p in panel],fontsize=9);ax.set_xlabel('Atom ID in this dictionary only');ax.set_title(title,fontsize=11);ax.axhline(11.5,color='red',lw=2)
   for j in range(24):
    for k in range(len(ids)):ax.text(k,j,'NA' if not np.isfinite(m[j,k]) else f'{m[j,k]:.2f}',ha='center',va='center',fontsize=8,color='white' if m[j,k]<np.nanmax(m)*.55 else 'black')
  fig.suptitle(f'{site}: {group}\nE = exploration F01-03; H = heldout check F04-06\nFixed candidates. P/cat/dog suffix: animal; N suffix: object. Gray = undefined norm.',fontsize=13,y=.975)
  fig.savefig(R/f'figures/{site}_{group}.png',dpi=125,bbox_inches='tight',pad_inches=.2);plt.close(fig)
 tt=list(csv.DictReader(open(R/f'results/{site}/transitions.csv')));fig,axs=plt.subplots(1,2,figsize=(13,5),sharey=True)
 for ax,c in zip(axs,['cat','dog']):
  t=[x for x in tt if x['source']=='P' and x['destination']==c];bottom=np.zeros(6)
  for key,label,col in [('retained','P members retained','#3c8c76'),('zero_to_positive','zero P -> positive fine','#e1a540')]:
   v=np.array([int(x[key]) for x in t]);ax.bar(range(6),v,bottom=bottom,label=label,color=col);bottom+=v
   for j,n in enumerate(v):ax.text(j,bottom[j]-n/2,str(n),ha='center',va='center')
  for j,x in enumerate(t):ax.text(j,33,f'lost {x["positive_to_zero"]}',ha='center',fontsize=9)
  ax.set_xticks(range(6),[f'F{i+1:02d}\n'+('E' if i<3 else 'H') for i in range(6)]);ax.set_ylim(0,36);ax.axvline(2.5,color='red',ls='--');ax.set_title(f'P -> {c}');ax.set_ylabel('Active members (native Top32)')
 fig.legend(*axs[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,-.02),ncol=2,frameon=False);fig.suptitle(f'{site}: membership counts (not added functional information)');fig.tight_layout(rect=(0,.05,1,.95));fig.savefig(R/f'figures/{site}_H1_transitions.png',dpi=145,bbox_inches='tight',pad_inches=.15);plt.close(fig)
dump(R/'evidence/visual_layout_repair.json',dict(UTC=now(),reason='Inspection: heatmap margins/titles and bar legend needed clearer separation. Layout only; no data, selection, rule or score change.',original_figure_SHA256=before,current_figure_SHA256={p.name:sha(p) for p in (R/'figures').glob('*.png')},selection_SHA256=sha(R/'results/selection.json'),originals_retained=str(old)))
