from common import *
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
pp=rows(R/'data/panel.jsonl');g=np.load(R/'data/pair_graphs.npz');ks=np.load(R/'cache/document_kernels.npz');df=pd.read_csv(R/'tables/overlap_summary.csv');allrows=[];counts=[];counter=[]
for _,r in df[df['mode']=='main'].iterrows():
 key=r.A+'__'+r.B+'__main';a=g[key+'__A'];b=g[key+'__B'];w=g[key+'__within_ij'];c=g[key+'__cross_ij'];k=ks[r.site+'__main'];n=len(a);cm=np.zeros((n,n));cm[c[:,0],c[:,1]]=1
 for ds,own,other,cmat in [(r.A,a,b,cm),(r.B,b,a,cm.T)]:
  ownk=k[np.ix_(own,own)];wi=(ownk.sum(1)-np.diag(ownk))/(n-1);cr=(k[np.ix_(own,other)]*cmat).sum(1)/cmat.sum(1);adv=wi-cr
  for q,i in enumerate(own):allrows.append(dict(site=r.site,pair=r.A+'/'+r.B,dataset=ds,id=pp[i]['id'],within_neighbor_mean=float(wi[q]),cross_neighbor_mean=float(cr[q]),within_minus_cross=float(adv[q]),within_neighbors=n-1,cross_neighbors=(n-1)//2))
  counts.append(dict(site=r.site,pair=r.A+'/'+r.B,dataset=ds,N=n,negative_documents=int((adv<0).sum()),zero_documents=int((adv==0).sum()),min_advantage=float(adv.min()),median_advantage=float(np.median(adv))))
  q=int(np.argmin(adv));i=own[q];counter.append(dict(site=r.site,pair=r.A+'/'+r.B,dataset=ds,id=pp[i]['id'],text=pp[i]['text'],within_neighbor_mean=float(wi[q]),cross_neighbor_mean=float(cr[q]),within_minus_cross=float(adv[q]),selection='POSTHOC descriptive most negative document; no new confirmatory test or refitting'))
table(R/'tables/per_document_neighbors.csv',allrows);table(R/'tables/per_document_counts.csv',counts);jsonl(R/'tables/posthoc_counterexamples.jsonl',counter)
fig,axes=plt.subplots(1,2,figsize=(13,5.5),sharey=False);pr=np.random.default_rng(20261106);rr=pd.DataFrame(allrows);palette=['#2166ac','#1b9e77']
for ax,s in zip(axes,SITES):
 for j,(A,B) in enumerate([('Magicoder','GSM8K'),('Magicoder','MMLU'),('GSM8K','MMLU')]):
  for z,ds in enumerate([A,B]):
   vals=rr[(rr.site==s)&(rr.pair==A+'/'+B)&(rr.dataset==ds)].within_minus_cross.to_numpy();xx=j+(z-.5)*.24;ax.scatter(xx+pr.uniform(-.045,.045,len(vals)),vals,s=5,alpha=.28,color=palette[z],label=['A documents','B documents'][z] if j==0 else None);ax.plot([xx-.065,xx+.065],[np.mean(vals)]*2,color='black',lw=2)
 ax.axhline(0,color='black',ls='--',lw=.7);ax.set_title(s.replace('_',' '));ax.set_xticks(range(3),['Magicoder / GSM8K','Magicoder / MMLU','GSM8K / MMLU'],fontsize=9);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.legend(fontsize=9)
axes[0].set_ylabel('Document mean(within neighbors) - mean(cross neighbors)');fig.suptitle('Positive group means coexist with individual counterexamples');fig.text(.5,.015,'257 documents / source; within 256 neighbors, cross 128 neighbors on the frozen main graph.\nPoints are dependent descriptive document values, not independent tests; black ticks are means.',ha='center',fontsize=10);fig.tight_layout(rect=[0,.09,1,.94]);fig.savefig(R/'figures/05_document_counterexamples.png',dpi=180);plt.close(fig)
print(pd.DataFrame(counts).to_string(index=False))
