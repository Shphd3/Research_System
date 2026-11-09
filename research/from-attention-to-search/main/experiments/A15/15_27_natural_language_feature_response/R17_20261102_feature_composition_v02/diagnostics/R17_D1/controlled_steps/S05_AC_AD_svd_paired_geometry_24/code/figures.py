from common import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.transforms import Bbox
import shutil
panel=rows(R/'data/panel.jsonl');D=np.load(R/'data/S04_frozen_activations.npz');parts=list(csv.DictReader(open(R/'results/difference_decomposition.csv')));pairs=list(csv.DictReader(open(R/'results/paired_differences_summary.csv')));means=list(csv.DictReader(open(R/'results/mean_difference_summary.csv')))
colors={'P':'#333333','cat':'#16856d','dog':'#bd641a','N':'#8a80a2'};markers={'P':'o','cat':'^','dog':'D','N':'s'}
def separate_labels(fig,ax,annotations,points):
 fig.canvas.draw();renderer=fig.canvas.get_renderer();placed=[];display=ax.transData.transform(points);unit=fig.dpi/72
 options=[(5,7),(5,-13),(-43,7),(-48,-13),(5,20),(-48,20),(5,-27),(-48,-27),(20,32),(-64,32),(20,-38),(-64,-38),(40,15),(-75,15)]
 for ann in annotations:
  anchor=ax.transData.transform(ann.xy);w,h,descent=renderer.get_text_width_height_descent(ann.get_text(),ann.get_fontproperties(),ismath=False);best=None
  for k,(dx,dy) in enumerate(options):
   box=Bbox.from_bounds(anchor[0]+dx*unit-2,anchor[1]+dy*unit-descent-2,w+4,h+4);overlap=sum(box.overlaps(b) for b in placed);covered=sum(box.contains(p[0],p[1]) for p in display);outside=int(not ax.bbox.contains(box.x0,box.y0) or not ax.bbox.contains(box.x1,box.y1));score=overlap*10000+covered*3000+outside*500+k
   if best is None or score<best[0]:best=(score,(dx,dy),box)
  ann.set_position(best[1]);placed.append(best[2])
if (R/'figures/ATTN_SAE_raw_z_projections.png').exists():
 old=R/'versions/figures_before_label_repair';old.mkdir(parents=True,exist_ok=False)
 for p in (R/'figures').glob('*.png'):shutil.copy2(p,old/p.name)
for site in SITES:
 for scale in SCALES:
  z=D[site+'__z'].astype(float);x=z if scale=='raw_z' else z*D[site+'__decoder_norm'];fig,axs=plt.subplots(2,2,figsize=(14,10));fig.subplots_adjust(left=.07,right=.98,bottom=.12,top=.84,hspace=.33,wspace=.24)
  for col,g in enumerate(['AC','AD']):
   fit=np.load(R/f'cache/{site}/{scale}/{g}.npz');pc=(x-fit['mean'])@fit['components'][:2].T;lo=pc.min(0);hi=pc.max(0);pad=np.maximum((hi-lo)*.18,1)
   for row,sp in enumerate(['exploration','heldout_check']):
    ax=axs[row,col];annotations=[];points=[]
    for fi in (range(3) if row==0 else range(3,6)):
     off=fi*4
     for ci,cond in enumerate(CONDS):
      px,py=pc[off+ci];points.append((px,py));ax.scatter(px,py,c=colors[cond],marker=markers[cond],s=43,alpha=.85,zorder=3);offset={'P':(3,5),'cat':(3,-10),'dog':(3,5),'N':(3,-10)}[cond];annotations.append(ax.annotate(f'F{fi+1:02d} {cond}',(px,py),xytext=offset,textcoords='offset points',fontsize=8,color=colors[cond],annotation_clip=False,arrowprops=dict(arrowstyle='-',color='#aaaaaa',lw=.35,alpha=.6)))
     for ci,cond in [(1,'cat'),(2,'dog')]:ax.annotate('',xy=pc[off+ci],xytext=pc[off],arrowprops=dict(arrowstyle='->',lw=1,color=colors[cond],alpha=.6))
    ax.set_xlim(lo[0]-pad[0],hi[0]+pad[0]);ax.set_ylim(lo[1]-pad[1],hi[1]+pad[1]);ax.axhline(0,color='#cccccc',lw=.6);ax.axvline(0,color='#cccccc',lw=.6);ax.set_xlabel(f'{g} PC1: own frozen exploration mean/basis');ax.set_ylabel(f'{g} PC2');ax.set_title(f'{g} basis | '+('F01-03 exploration' if row==0 else 'F04-06 check (no refit)'),fontsize=11);ax.grid(alpha=.12)
    separate_labels(fig,ax,annotations,points)
  handles=[Line2D([0],[0],marker=markers[c],color='none',markerfacecolor=colors[c],label=c,markersize=7) for c in CONDS];fig.legend(handles=handles,loc='lower center',ncol=4,frameon=False,bbox_to_anchor=(.5,.015));fig.suptitle(f'{site} | {scale} | all points projected on exploration-only SVD\nAC fit uses exploration P/cat only; AD uses same P/dog only; N never fitted\nArrows = actual paired changes. Panels have different means/axes; separation is not semantic proof.',fontsize=12,y=.975)
  fig.savefig(R/f'figures/{site}_{scale}_projections.png',dpi=145,bbox_inches='tight',pad_inches=.15);plt.close(fig)
 # Raw paired differences and disjoint per-family energy decomposition.
 pp=[p for p in pairs if p['site']==site and p['scale']=='raw_z'];mean=next(m for m in means if m['site']==site and m['scale']=='raw_z');fig,axs=plt.subplots(3,1,figsize=(13,11));fig.subplots_adjust(left=.08,right=.98,bottom=.12,top=.90,hspace=.5)
 xx=np.arange(6);cv=np.array([float(p['cat_dog_delta_signed_cosine']) for p in pp]);axs[0].bar(xx,cv,color=['#7694ad']*3+['#73ad91']*3);axs[0].set_ylim(-1,1);axs[0].axhline(0,color='black',lw=.8);axs[0].axhline(float(mean['exploration_cat_dog_signed_cosine']),color='#b94d48',ls='--',label='cos(discovery mean cat-P, mean dog-P)');axs[0].legend(fontsize=8,loc='lower left');axs[0].set_ylabel('Signed cosine');axs[0].set_title('Actual same-family cat-P vs dog-P: signed directions, not SVD-axis cosine')
 for j,v in enumerate(cv):axs[0].text(j,v+.04,f'{v:.3f}',ha='center',fontsize=9)
 axs[1].bar(xx-.17,[float(p['cat_delta_L2']) for p in pp],width=.34,label='cat-P',color=colors['cat']);axs[1].bar(xx+.17,[float(p['dog_delta_L2']) for p in pp],width=.34,label='dog-P',color=colors['dog']);axs[1].legend(fontsize=8);axs[1].set_ylabel('L2 in raw activation coordinates');axs[1].set_title('Full30000-coordinate difference length (not model-output effect)')
 for ax in axs[:2]:ax.set_xticks(xx,[f'F{i+1:02d} '+('E' if i<3 else 'H') for i in range(6)]);ax.axvline(2.5,color='black',ls=':',lw=1)
 xx=np.arange(12);bottom=np.zeros(12)
 for part,color in zip(PARTS,['#4e88a1','#d9ab49','#ad707b']):
  vv=np.array([float(next(p['squared_norm_share'] for p in parts if p['site']==site and p['scale']=='raw_z' and p['family']==f'F{fi+1:02d}' and p['fine']==fine and p['part']==part)) for fi in range(6) for fine in ['cat','dog']]);axs[2].bar(xx,vv,bottom=bottom,color=color,label=part);bottom+=vv
 axs[2].set_xticks(xx,[f'F{fi+1:02d}\n'+('C' if fine=='cat' else 'D') for fi in range(6) for fine in ['cat','dog']]);axs[2].set_ylim(0,1);axs[2].set_ylabel('Share of squared difference norm');axs[2].set_title('Per-pair disjoint parts: retained-member strength / new support / lost support');axs[2].axvline(5.5,color='black',ls=':');fig.legend(*axs[2].get_legend_handles_labels(),loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.015));fig.suptitle(f'{site} | raw paired changes and native Top32 decomposition\nE = exploration F01-03; H = check F04-06. Support turnover is not independent new semantics.',fontsize=12,y=.975)
 fig.savefig(R/f'figures/{site}_raw_paired_decomposition.png',dpi=145,bbox_inches='tight',pad_inches=.15);plt.close(fig)
dump(R/'evidence/figures_generated.json',dict(UTC=now(),figures=[dict(path=str(p.relative_to(R)),sha256=sha(p)) for p in sorted((R/'figures').glob('*.png'))],sources=['frozen S04 raw cache','cache/site/scale/AC.npz,AD.npz','results/paired_differences_summary.csv','results/difference_decomposition.csv'],new_fits=0,scientific_boundary='geometric description only'))
print('SIX_FIGURES_WRITTEN',flush=True)
