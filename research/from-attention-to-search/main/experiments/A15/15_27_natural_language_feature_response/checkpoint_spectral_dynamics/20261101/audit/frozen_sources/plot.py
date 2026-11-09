"""Static scientific figures from frozen numeric tables, with actual token axes."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis';FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.spines.right':False,'axes.spines.top':False,'figure.dpi':140})
COL={'head':'#cf4f35','middle':'#15976f','tail':'#7856ad','top16':'#ab3a25','top64':'#db8740','top128':'#5c9675','top256':'#487ca6'}
def finish(fig,name,caption,sources):
 fig.tight_layout(rect=(0,0.02,1,.97));fig.text(.01,.002,caption,fontsize=8);fig.savefig(FIG/f'{name}.png',bbox_inches='tight');fig.savefig(FIG/f'{name}.pdf',bbox_inches='tight');plt.close(fig)
 p=FIG/'figure_manifest.json';m=json.load(open(p)) if p.exists() else {};m[name]=dict(caption=caption,sources={x:hashlib.sha256((OUT/x).read_bytes()).hexdigest() for x in sources},independence='documents/record groups,not checkpoint replicates',boundary='single Dense trajectory; descriptive sampling ranges;33Bnot known convergence');p.write_text(json.dumps(m,indent=2)+'\n')
def geometry_figures():
 s=pd.read_csv(OUT/'checkpoint_statistics.csv');s=s[s.layer==7];spec=pd.read_csv(OUT/'spectrum.csv');pairs=pd.read_csv(OUT/'pair_metrics.csv');sub=pd.read_csv(OUT/'subspace_distances.csv');sam=pd.read_csv(OUT/'sampling_reference_summary.csv');T=s.training_B.to_numpy();cm=plt.colormaps['viridis'];norm=plt.Normalize(.5,33)
 f,ax=plt.subplots(2,3,figsize=(15,8));f.suptitle('Dense final residual-post: variance scale and allocation (0.5B–33B training tokens)')
 for t,a in spec.groupby('training_B'):
  ax[0,0].plot(a['index'],a.eigenvalue,color=cm(norm(t)),lw=1.0);ax[0,1].plot(a['index'],a.normalized_eigenvalue,color=cm(norm(t)),lw=1.0)
 for a,y in [(ax[0,0],'Covariance eigenvalue (absolute variance)'),(ax[0,1],'Eigenvalue / own total variance')]:a.set(xscale='log',yscale='log',xlabel='Own sorted direction index',ylabel=y)
 cb=f.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cm),ax=ax[0,:2].tolist(),fraction=.025,pad=.03);cb.set_label('Cumulative valid training tokens (B)')
 ax[0,2].plot(T,s.trace,'o-',color='#315b92');ax[0,2].set(xlabel='Cumulative valid training tokens (B)',ylabel='Total variance: trace(C)')
 ax[1,0].plot(T,s.effective_rank,'o-',color='#15976f');ax[1,0].set(xlabel='Cumulative valid training tokens (B)',ylabel='Effective rank: exp(spectral entropy)')
 for k,label,style in [('adjacent','Adjacent interval, at right endpoint','o-'),('endpoint','Distance to33B','s--')]:
  a=pairs[pairs.comparison==k];xx=a.comparison_B if k=='adjacent' else a.training_B
  ax[1,1].plot(xx,a.absolute_spectrum_l2,style,label=label);ax[1,2].plot(xx,a.normalized_spectrum_TV,style,label=label)
 ax[1,1].set(xlabel='Cumulative valid training tokens (B)',ylabel='Absolute spectrum L2 distance (variance units)');ax[1,2].set(xlabel='Cumulative valid training tokens (B)',ylabel='Normalized spectrum total variation distance')
 for a in ax[1,1:]:a.legend(fontsize=8)
 finish(f,'figure1_spectra_scale_shape','Each checkpoint uses its own reference mean; 32768 positions from1024reference records. Missing saved weights produce real gaps; no interpolation as measurements.',['checkpoint_statistics.csv','spectrum.csv','pair_metrics.csv'])
 # A distinct rate and sampling-reference view, no unregistered convergence label.
 f,ax=plt.subplots(2,2,figsize=(12,7));f.suptitle('Dense spectrum change: actual token gaps, means and sampling sensitivity')
 a=pairs[pairs.comparison=='adjacent'];ax[0,0].plot(a.comparison_B,a.absolute_spectrum_l2_per_B,'o-');ax[0,0].set(ylabel='Absolute spectrum L2 / training B')
 ax[0,1].plot(a.comparison_B,a.normalized_spectrum_TV_per_B,'o-');ax[0,1].set(ylabel='Normalized spectrum TV / training B')
 ax[1,0].plot(T,s.mean_norm,'o-',label='Mean vector norm');a=pairs[pairs.comparison=='endpoint'];ax[1,0].plot(a.training_B,a.mean_drift,'s--',label='Mean drift to33B');ax[1,0].set(ylabel='Hidden-vector units');ax[1,0].legend(fontsize=8)
 ax[1,1].bar(np.arange(1,len(T)),np.diff(T),color='#6b89a0');ax[1,1].set(xlabel='Chronological interval index',ylabel='Actual gap (training B)')
 for a in ax.flat:
  if a!=ax[1,1]:a.set_xlabel('Cumulative valid training tokens (B)')
 finish(f,'figure1b_rates_mean_gaps','Rates divide by actual token gaps; mean drift and centered covariance are separate. No onset time is estimated.',['checkpoint_statistics.csv','pair_metrics.csv'])
 f,ax=plt.subplots(2,2,figsize=(13,8));f.suptitle('Dense original-coordinate subspaces: adjacent and endpoint drift')
 for row,kind in enumerate(['adjacent','endpoint']):
  for col,names in enumerate([['head','middle','tail'],['top16','top64','top128','top256']]):
   for name in names:
    a=sub[(sub.comparison==kind)&(sub.coordinates=='raw')&(sub.band==name)];xx=a.comparison_B if kind=='adjacent' else a.training_B;ax[row,col].plot(xx,a.projection_distance,'o-',label=name,color=COL[name])
    if kind=='adjacent':
     b=sam[sam.metric==name];ax[row,col].errorbar(b.training_B,b['median'],yerr=[b['median']-b.lower,b.upper-b['median']],fmt='x',color=COL[name],alpha=.5,capsize=3)
   ax[row,col].set(xlabel='Cumulative valid training tokens (B)',ylabel='Normalized projection distance',ylim=(-.02,1.02),title=('Adjacent intervals (right endpoint)' if kind=='adjacent' else 'Distance to33B'));ax[row,col].legend(fontsize=8,ncol=2)
 finish(f,'figure2_subspace_drift','Lines:paired checkpoint changes. Crosses/ranges:within-checkpoint8fixedhalf-splits, descriptive2.5–97.5%range. Bands own-sorted; near-degenerate boundaries may be unresolved.',['subspace_distances.csv','sampling_reference_summary.csv'])
 f,ax=plt.subplots(2,3,figsize=(15,8));f.suptitle('Dense: original coordinates, orthogonal alignment and paired sample relations')
 for row,kind in enumerate(['adjacent','endpoint']):
  a=pairs[pairs.comparison==kind];xx=a.comparison_B if kind=='adjacent' else a.training_B
  ax[row,0].plot(xx,a.raw_eval_relative_residual,'o-',label='Raw residual');ax[row,0].plot(xx,a.aligned_eval_relative_residual,'s-',label='After reference-only Procrustes');ax[row,0].set(ylabel='Evaluation residual / target centered norm');ax[row,0].legend(fontsize=8)
  ax[row,1].plot(xx,a.cka,'o-',color='#315b92');ax[row,1].set(ylabel='Centered linear CKA on paired evaluation',ylim=(0,1.02))
  for coord,style in [('raw','o-'),('aligned','s--')]:
   b=sub[(sub.comparison==kind)&(sub.band=='top64')&(sub.coordinates==coord)];bx=b.comparison_B if kind=='adjacent' else b.training_B;ax[row,2].plot(bx,b.projection_distance,style,label=coord)
  ax[row,2].set(ylabel='Top64 projection distance');ax[row,2].legend(fontsize=8)
  for z in ax[row,:]:z.set_xlabel('Cumulative valid training tokens (B)');z.set_title('Adjacent' if kind=='adjacent' else 'To33B endpoint')
 finish(f,'figure3_rotation_and_relations','Procrustes fits only reference documents and no scale. Alignment deliberately removes rotation; raw drift retains its independent meaning. CKA is rotation and scale invariant.',['pair_metrics.csv','subspace_distances.csv'])
 # Cumulative variance and fixed endpoint projections have different eigenbases.
 f,ax=plt.subplots(1,2,figsize=(12,4));f.suptitle('Own ordered spectrum versus fixed33B direction coordinates')
 p=pd.read_csv(OUT/'fixed_endpoint_projected_variance.csv')
 for t in [.5,17,33]:
  a=spec[spec.training_B==t];ax[0].plot(a['index'],a.cumulative_fraction,label=f'{t:g}B');b=p[p.training_B==t];ax[1].plot(b.endpoint_direction,b.fraction_of_own_trace,label=f'{t:g}B')
 ax[0].set(xlabel='Own ordered eigenvalue index',ylabel='Cumulative explained variance',xscale='log');ax[1].set(xlabel='Fixed33B direction index',ylabel='Projected variance / current trace',xscale='log',yscale='log')
 for a in ax:a.legend()
 finish(f,'figure1c_fixed_basis','Right panel is variance projected into fixed33B directions; it is not the early checkpoint eigenvalue spectrum.',['spectrum.csv','fixed_endpoint_projected_variance.csv'])

def semantic_figure():
 r=pd.read_csv(OUT/'readout_metrics.csv');c=pd.read_csv(OUT/'increment_contrasts.csv');f,ax=plt.subplots(2,3,figsize=(15,8));f.suptitle('Dense linear readability on the exact R12 common-the panel: three sampled times')
 for col,task in enumerate(['coarse','math_fine','bio_fine']):
  for name in ['head','middle','tail','full']:
   a=r[(r.task==task)&(r.basis=='own')&(r.subspace==name)];color=COL.get(name,'#333333');ax[0,col].errorbar(a.training_B,a.balanced_accuracy,yerr=[a.balanced_accuracy-a.lower,a.upper-a.balanced_accuracy],fmt='o-',color=color,label=name,capsize=3)
  ax[0,col].axhline(.5,color='#888',ls=':');ax[0,col].set(title=task,ylabel='Heldout balanced accuracy',ylim=(-.03,1.03));ax[0,col].legend(fontsize=8,ncol=2)
  for plus,color in [('head_middle',COL['middle']),('head_tail',COL['tail'])]:
   for basis,style in [('own','o-'),('fixed33B','s--')]:
    a=c[(c.task==task)&(c.control=='head128')&(c.addition==plus)&(c.basis==basis)];ax[1,col].errorbar(a.training_B,a.difference,yerr=[a.difference-a.lower,a.upper-a.difference],fmt=style,color=color,label=f'{plus}, {basis}',capsize=3)
  ax[1,col].axhline(0,color='#888',ls=':');ax[1,col].set(ylabel='Increment versus128Dhead (balanced accuracy)');ax[1,col].legend(fontsize=7)
  for z in ax[:,col]:z.set_xlabel('Cumulative valid training tokens (B)');z.set_xticks([.5,17,33])
 finish(f,'figure4_semantic_timing','Each checkpoint refits matched classifiers; error bars:2000pairedstratifiedheldoutresamples. Only three times measured; exposed small panel limits timing/increment conclusions.',['readout_metrics.csv','increment_contrasts.csv'])
