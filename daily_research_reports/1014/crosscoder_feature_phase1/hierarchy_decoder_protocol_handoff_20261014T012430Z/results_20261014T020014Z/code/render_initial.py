"""Three separate visual questions; frozen selections, no scientific recomputation."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
import sys,json,csv,time,resource
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def rows(p):
 with Path(p).open() as f:return list(csv.DictReader(f))
def main(out):
 out=Path(out);start=time.monotonic();figdir=out/'figures';figdir.mkdir(exist_ok=True)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
 g=np.load(out/'derived_geometry.npz');p=g['p'];L=g['L'];h=g['h'][1];nodes=g['nodes'].tolist();layers=g['layers'];sel=json.loads((out/'selection_frozen_before_geometry.json').read_text());nr={int(r['feature']):r for r in rows(out/'graph1_nodes.csv')};er=rows(out/'graph1_edges.csv')
 def save(fig,name):
  for ext in ['png','pdf','svg']:fig.savefig(figdir/(name+'.'+ext),dpi=160,bbox_inches='tight')
  plt.close(fig)
 # Figure 1 panels use only graph depth on y, with edge-ID support lookup.
 for anchor,subset in sel['subsets'].items():
  group=defaultdict(list)
  for a in subset:group[int(h[a])].append(a)
  pos={}
  for depth,ids in group.items():
   xx=np.linspace(.04,.96,len(ids)) if len(ids)>1 else [.5]
   for a,x in zip(sorted(ids),xx):pos[a]=(float(x),depth)
  fig,ax=plt.subplots(figsize=(23,13));ax.set_xlim(-.02,1.02);ax.set_ylim(-.45,5.55);ax.set_yticks(range(6));ax.set_ylabel('Statistical graph hierarchy h (full V graph)');ax.set_xticks([]);ax.set_xlabel('Horizontal positions are layout only; arrows A -> more frequent u. Edge IDs refer to support table.')
  ax.grid(axis='y',color='#dddddd',zorder=0);ax.spines[['top','right','bottom']].set_visible(False)
  used=[r for r in er if int(r['A']) in subset]
  for j,row in enumerate(used):
   a,u=int(row['A']),int(row['u']);x1,y1=pos[a];x2,y2=pos[u];rad=((int(row['edge_id'])%5)-2)*.025
   patch=FancyArrowPatch((x1,y1-.12),(x2,y2+.13),arrowstyle='-|>',mutation_scale=11,linewidth=.9,color='#526b82',alpha=.65,connectionstyle=f'arc3,rad={rad}',zorder=1);ax.add_patch(patch)
   # Small IDs identify edges without mixing numerical support labels at crossings.
   frac=.32+.10*(int(row['edge_id'])%3);xx=x1+(x2-x1)*frac;yy=y1+(y2-y1)*frac
   ax.text(xx,yy,str(row['edge_id']),fontsize=7,color='#334c64',ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',alpha=.75,pad=.25),zorder=2)
  for a,(x,y) in pos.items():
   v=nr[a];text=f"ID {a} | h={h[a]}\nnV={int(v['n_V']):,} | pV={float(v['frequency_V']):.6g}"
   ax.text(x,y,text,ha='center',va='center',fontsize=9,bbox=dict(boxstyle='round,pad=.4',facecolor='#e5eef6' if str(a)!=anchor else '#cbdfee',edgecolor='#416781',linewidth=1.3),zorder=4)
  ax.set_title(f"Figure 1 | Anchor {anchor}: complete reachable subgraph ({len(subset)} nodes, {len(used)} edges)\nGlobal h is unchanged by display. Association, not causal / temporal / model-layer arrows.",pad=16)
  save(fig,f'figure1_anchor_{anchor}')
 # Figure 2 same 30 nodes, ordered solely by graph h then ID.
 order=sorted(nodes,key=lambda a:(h[a],a));mat=p[:,order].T
 fig,ax=plt.subplots(figsize=(16,13));im=ax.imshow(mat,aspect='auto',vmin=0,vmax=float(np.nanmax(mat)),cmap='viridis',interpolation='nearest');ax.set_xticks(range(14),layers);ax.set_yticks(range(len(order)),[f'ID {a} | h={h[a]}' for a in order]);ax.set_xlabel('Actual Qwen model block (one based)');ax.set_ylabel('Same nodes as Figure 1; sorted by h, then ID')
 for i in range(len(order)):
  for j in range(14):ax.text(j,i,f'{mat[i,j]:.3f}',ha='center',va='center',fontsize=7,color='black' if mat[i,j]>.6*np.nanmax(mat) else 'white')
 fig.colorbar(im,ax=ax,pad=.02,label='p: decoder magnitude share across 14 layers (unitless; row sum 1)');ax.set_title('Figure 2 | Cross-layer decoder magnitude distribution\nTRAIN-normalized coordinates; shared z cancels. L is an average position, not a whole-distribution shift.',pad=16);fig.tight_layout();save(fig,'figure2_decoder_distribution')
 # Figure 3 full Q; jitter source frozen in CSV, equal feature weights.
 rr=rows(out/'figure3_source.csv');xs=np.array([float(r['x_for_plot']) for r in rr]);ys=np.array([float(r['L']) for r in rr]);hh=np.array([int(r['h']) for r in rr]);ids=np.array([int(r['feature']) for r in rr]);result=json.loads((out/'results.json').read_text());rho=result['correlations']['V_train_normalized']['rho']
 fig,ax=plt.subplots(figsize=(12,8));ax.scatter(xs,ys,s=7,color='#346b91',alpha=.12,rasterized=True,label='One feature per point; horizontal jitter is display only')
 for depth in range(6):
  vals=ys[hh==depth];q=np.quantile(vals,[.25,.5,.75],method='linear');ax.text(depth,28.7,f'n={len(vals):,}',ha='center',fontsize=10)
  if depth<5:ax.errorbar(depth,q[1],yerr=np.array([[q[1]-q[0]],[q[2]-q[1]]]),fmt='o',color='#c95e2a',linewidth=2.5,capsize=6,label='Median and feature IQR (not confidence interval)' if depth==0 else None)
  else:
   for a in [937,3461]:
    k=np.flatnonzero(ids==a)[0];ax.scatter(xs[k],ys[k],s=65,facecolors='none',edgecolors='#a22c35',linewidths=1.6);ax.annotate(f'ID {a}',(xs[k],ys[k]),xytext=(8,12 if a==937 else -19),textcoords='offset points',fontsize=9)
 ax.set_xlim(-.4,5.45);ax.set_ylim(1.5,29.3);ax.set_xticks(range(6));ax.set_xlabel('Statistical graph hierarchy h (full V graph)');ax.set_ylabel('L: decoder magnitude-weighted average actual model block');ax.grid(alpha=.2);ax.set_title(f'Figure 3 | All {len(rr):,} qualified features; descriptive Spearman = {rho:.6f}\nL measures the average position only. Inspect p distributions; h=5 has only two nodes.',pad=16)
 ax.legend(loc='upper left',bbox_to_anchor=(0,-.14),frameon=False,fontsize=9);fig.subplots_adjust(bottom=.23);save(fig,'figure3_all_features')
 (out/'render_receipt.json').write_text(json.dumps({'status':'RENDERED_PENDING_VISUAL_REVIEW','seconds':time.monotonic()-start,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'figures':sorted(p.name for p in figdir.iterdir())},indent=2)+'\n');print('FIGURES_RENDERED',flush=True)
if __name__=='__main__':main(sys.argv[1])
