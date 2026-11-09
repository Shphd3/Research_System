from engine import *
import pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'figure.dpi':150,'savefig.dpi':180,'axes.spines.top':False,'axes.spines.right':False})
a=pd.read_csv(R/'tables/A_overlap_references.csv');own=pd.read_csv(R/'tables/B_own_structure.csv');between=pd.read_csv(R/'tables/B_dataset_differences.csv');pairs=list(itertools.combinations(DATASETS,2));colors=['#2166ac','#e6ab02','#1b9e77']
fig,axes=plt.subplots(2,3,figsize=(14,8),sharey='row')
for z,s in enumerate(SITES):
 for col,(A,B) in enumerate(pairs):
  ax=axes[z,col];ss=a[(a.site==s)&(a.A==A)&(a.B==B)]
  for j,comp in enumerate(['within_A','within_B','cross']):
   r=ss[ss.comparison==comp].iloc[0]
   for k,(name,label) in enumerate([('real_J','Real heldout'),('discovery_Bernoulli_J','Discovery freq: free row count'),('heldout_fixed32_margin_J','Heldout freq + exact32')]):
    value=r[name];err=np.array([[value-r.real_CI_lo],[r.real_CI_hi-value]]) if k==0 else [[1.96*r.Bernoulli_MCSE],[1.96*r.Bernoulli_MCSE]] if k==1 else [[1.96*r.fixed32_null_SD/16],[1.96*r.fixed32_null_SD/16]]
    ax.errorbar(j+(k-1)*.2,value,yerr=err,fmt=['o','^','s'][k],color=colors[k],capsize=3,label=label if j==0 else None)
  ax.set_xticks(range(3),['Within A','Within B','Cross A/B']);ax.set_title(s.replace('_',' ')+'\nA='+A+' / B='+B);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='y',alpha=.15)
  if col==0:ax.set_ylabel('Mean support Jaccard')
  if z==0 and col==1:pass
handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.95),ncol=3,fontsize=9)
fig.suptitle('A | Marginal references reproduce most of the within-minus-cross overlap gap',fontsize=14,y=.99);fig.text(.5,.012,'128 discovery + 129 heldout documents / source; 8 original positions; 8,256 distinct pairs / group.\nReal: 95% document-bootstrap CI. Reference bars: Monte Carlo mean uncertainty, not document CIs. Exact32 uses heldout counts (descriptive).',ha='center',fontsize=9);fig.tight_layout(rect=[0,.085,1,.91]);fig.savefig(R/'figures/01_overlap_vs_frequency.png');fig.savefig(R/'figures/01_overlap_vs_frequency.pdf');plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(13,8.5))
for z,s in enumerate(SITES):
 for col,kind in enumerate(['own','between']):
  ax=axes[z,col];df=own if kind=='own' else between;sub=df[(df.site==s)&(df['mode']=='position')];labels=[]
  for j,(_,r) in enumerate(sub.iterrows()):
   label=r.dataset if kind=='own' else r.A+'/'+r.B;labels.append(label);value=r.heldout_excess if kind=='own' else r.heldout_difference;disc=r.discovery_excess_projection if kind=='own' else r.discovery_excess_difference
   mode='position';nfile=np.load(R/'cache'/f'{s}__heldout__{mode}.npz');dirs=np.load(R/'data'/f'{s}__discovery_directions.npz');q=nfile['qnull'];mean=q.mean((0,1))
   if kind=='own':d=DATASETS.index(r.dataset);null=np.einsum('csp,p->cs',q[:,:,d]-mean[d],dirs['own'][d]);expl=own[(own.site==s)&(own.dataset==r.dataset)&(own['mode']=='position_token3')].iloc[0];ev=expl.heldout_excess
   else:ab=DP.index((DATASETS.index(r.A),DATASETS.index(r.B)));d,e=DP[ab];null=np.einsum('csp,p->cs',q[:,:,d]-mean[d]-(q[:,:,e]-mean[e]),dirs['between'][ab]);expl=between[(between.site==s)&(between.A==r.A)&(between.B==r.B)&(between['mode']=='position_token3')].iloc[0];ev=expl.heldout_difference
   lo,hi=np.quantile(null,[.025,.975]);ax.errorbar(j-.23,0,yerr=[[-lo],[hi]],fmt='_',color='gray',elinewidth=5,capsize=5,label='Degree-null 95% range' if j==0 else None);ax.plot(j-.08,disc,'^',color='#7570b3',label='Discovery fitted excess' if j==0 else None);ax.errorbar(j+.08,value,yerr=[[value-r.doc_CI_lo],[r.doc_CI_hi-value]],fmt='o',color=colors[0],capsize=4,label='Heldout + doc 95% CI' if j==0 else None);ax.errorbar(j+.24,ev,yerr=[[ev-expl.doc_CI_lo],[expl.doc_CI_hi-ev]],fmt='s',color=colors[2],capsize=3,label='Heldout token-strata (exploratory)' if j==0 else None)
  ax.axhline(0,color='gray',lw=.7);ax.set_xticks(range(3),labels,fontsize=9);ax.set_title(s.replace('_',' ')+' | '+('Own-source residual pattern' if kind=='own' else 'Between-source residual contrast'));ax.set_ylabel('Pair-coactivation excess projection');ax.grid(axis='y',alpha=.15)
  if z==0 and col==0:pass
handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.95),ncol=2,fontsize=9)
fig.suptitle('B | Joint statistics exceed exact row32 / feature-count nulls and replicate in heldout documents',fontsize=13,y=.99);fig.text(.5,.012,'Each score uses all 276 pairs of 24 discovery-fixed members, mean over 8 positions/document; frozen unit-length discovery weights.\nDiscovery points are fitted, not validation. Null range is algorithmic, not extra documents. CIs condition on discovery direction / estimated null center.\nToken control preserves three frequent current-token IDs or OTHER; it does not match independent formatting.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.10,1,.90]);fig.savefig(R/'figures/02_joint_null_and_holdout.png');fig.savefig(R/'figures/02_joint_null_and_holdout.pdf');plt.close(fig)
h=pd.read_csv(R/'tables/B_member_count_distribution.csv');fig,axes=plt.subplots(2,3,figsize=(13,7),sharey='row')
for z,s in enumerate(SITES):
 for j,d in enumerate(DATASETS):
  ax=axes[z,j];q=h[(h.site==s)&(h.dataset==d)&(h['mode']=='position')];xx=q.active_candidate_members.to_numpy();ax.plot(xx,q.heldout_real,'o-',ms=3,color=colors[0],label='Heldout real');ax.plot(xx,q.heldout_null,'-',color='gray',label='Exact32 / frequency null');ax.fill_between(xx,q.null_lo.to_numpy(),q.null_hi.to_numpy(),color='gray',alpha=.2);ax.set_title(s.replace('_',' ')+' | '+d);ax.set_xlabel('Number of active members among fixed 24');ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='y',alpha=.15)
  if j==0:ax.set_ylabel('Fraction of 1032 heldout positions')
  if z==0 and j==2:ax.legend(fontsize=8)
fig.suptitle('Supplement | Distribution of multiple-member coactivation counts');fig.text(.5,.012,'129 documents × 8 positions; counts are descriptive, shaded bands are conditional-null 95% ranges, not independent-token CIs.\nEvery complete native row still has 32 members; the candidate 24 subset count is allowed to vary.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.09,1,.94]);fig.savefig(R/'figures/03_candidate_member_count_distribution.png');plt.close(fig)
print('FIGURES_COMPLETE')
