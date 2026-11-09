from common import *
import pandas as pd,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'figure.dpi':160,'savefig.dpi':180,'axes.spines.top':False,'axes.spines.right':False})
df=pd.read_csv(R/'tables/overlap_summary.csv');pairs=[('Magicoder','GSM8K'),('Magicoder','MMLU'),('GSM8K','MMLU')];colors=['#2166ac','#1b9e77','#d95f02'];fig,axes=plt.subplots(1,2,figsize=(12,5.5),sharey=True)
for ax,site in zip(axes,SITES):
 sub=df[(df.site==site)&(df['mode']=='main')]
 for p,(A,B) in enumerate(pairs):
  r=sub[(sub.A==A)&(sub.B==B)].iloc[0]
  for k,(name,color) in enumerate(zip(['within_A','within_B','cross'],colors)):
   x=p+(k-1)*.22;y=r[name];ax.errorbar(x,y,yerr=[[y-r[name+'_lo']],[r[name+'_hi']-y]],fmt='o',color=color,capsize=4,markersize=7,label=['Within A','Within B','Across A / B'][k] if p==0 else None)
 ax.set_xticks(range(3),['A=Magicoder\nB=GSM8K','A=Magicoder\nB=MMLU','A=GSM8K\nB=MMLU']);ax.set_title(site.replace('_',' ')+' | native Top32 / 30,000');ax.grid(axis='y',alpha=.2);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(loc='upper right',fontsize=9)
axes[0].set_ylabel('Mean support Jaccard = intersection / union');fig.suptitle('Within-source vs across-source SAE member overlap',fontsize=15,y=.99);fig.text(.5,.02,'257 documents / source; 8 aligned quantile positions / document; 32,896 unique document pairs / group.\n95% document-bootstrap intervals (1,999 resamples). Pair counts are not independent sample sizes.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.1,1,.94]);fig.savefig(R/'figures/01_main_overlap.png');fig.savefig(R/'figures/01_main_overlap.pdf');plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(14,8),sharey=False);modes=['main','length_matched','fixed32','fixed16','same_token'];labels=['Main: 8 quantiles','Full-length bins','32-token prefix','16-token prefix','Same literal token'];cc=['#333333','#7570b3','#e6ab02','#1b9e77','#e7298a']
for z,site in enumerate(SITES):
 for j,(A,B) in enumerate(pairs):
  ax=axes[z,j];ss=df[(df.site==site)&(df.A==A)&(df.B==B)];yl=[]
  for y,(mode,label,col) in enumerate(zip(modes,labels,cc)):
   r=ss[ss['mode']==mode].iloc[0];v=r.pooled_minus_cross;ax.errorbar(v,y,xerr=[[v-r.pooled_minus_cross_lo],[r.pooled_minus_cross_hi-v]],fmt='o',color=col,capsize=3);yl.append(label+' | N='+str(int(r.N_A)))
  ax.axvline(0,color='black',lw=.7);ax.set_yticks(range(5),yl,fontsize=9);ax.invert_yaxis();ax.xaxis.set_major_formatter(PercentFormatter(1));ax.set_title(site.replace('_',' ')+'\n'+A+' / '+B);ax.grid(axis='x',alpha=.2);ax.set_xlabel('Average(within A, within B) - across (pp)')
fig.suptitle('Controls narrow the claim; each comparison keeps its own document uncertainty',fontsize=14);fig.text(.5,.012,'95% document bootstrap; controls exploratory. Same-token comparisons have missing eligible pairs (see CSV).\nFull-length matching N=11 for Magicoder / GSM8K is weak; fixed prefixes match observed context, not complete question length.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.065,1,.95]);fig.savefig(R/'figures/02_controls.png');fig.savefig(R/'figures/02_controls.pdf');plt.close(fig)
panel=rows(R/'data/panel.jsonl');fig,axes=plt.subplots(1,2,figsize=(11,4.5));datas=[[p['full_token_count'] for p in panel if p['dataset']==d] for d in DATASETS];axes[0].boxplot(datas,labels=DATASETS,showfliers=False);axes[0].set_ylabel('Full question token count');axes[0].axhline(128,color='gray',ls='--',label='Visible-prefix cap:128');axes[0].legend(fontsize=8)
x=np.arange(3);fmt=pd.read_csv(R/'data/basic_format.csv')
for k,col in enumerate(['code_fence','with_newline','with_question_mark']):
 vals=[float(fmt[fmt.dataset==d].iloc[0][col])/257 for d in DATASETS];axes[1].bar(x+(k-1)*.22,vals,width=.22,label=col.replace('_',' '),color=colors[k])
axes[1].set_xticks(x,DATASETS);axes[1].yaxis.set_major_formatter(PercentFormatter(1));axes[1].set_ylabel('Fraction of 257 sampled questions');axes[1].legend(fontsize=8);fig.suptitle('Observed source differences: length and formatting');fig.tight_layout();fig.savefig(R/'figures/03_format_and_length.png');plt.close(fig)
# Representative case fixed before activations: SHA-first documents, first sampled position.
ex=rows(R/'tables/deterministic_examples.jsonl');ee=[r for r in ex if r['site']=='ATTN_SAE' and r['quantile_index']==0 and r['A_id'].startswith('Magicoder') and r['B_id'].startswith('GSM8K')][0]
if ee['shared_ids']:
 fig,ax=plt.subplots(figsize=(10,4));xx=np.arange(len(ee['shared_ids']));ax.bar(xx-.18,ee['A_shared_values'],.36,label=ee['A_id'],color=colors[0]);ax.bar(xx+.18,ee['B_shared_values'],.36,label=ee['B_id'],color=colors[1]);ax.set_xticks(xx,['#'+str(i) for i in ee['shared_ids']],rotation=45);ax.set_ylabel('Native SAE activation (raw scale)');ax.set_title('Separate amplitude supplement: shared ATTN coordinates\nJaccard='+str(round(ee['Jaccard'],4))+'; intersection='+str(ee['intersection'])+', union='+str(ee['union']));ax.legend(fontsize=8);fig.tight_layout();fig.savefig(R/'figures/04_shared_amplitude_example.png');plt.close(fig)
print('FIGURES_COMPLETE')
