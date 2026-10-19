from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':10})
manifest=json.load(open(ROOT/'provenance/figures_manifest.json'))
def out(fig,name,src,q):
 for ext in ['png','svg','pdf']:
  pp=ROOT/'figures'/f'{name}.{ext}';fig.savefig(pp,dpi=170,bbox_inches='tight');manifest.append(dict(path=str(pp),sha256=sha(pp),source=src,question=q))
 plt.close(fig)
rows=list(csv.DictReader(open(ROOT/'tables/group_to_actual_expert.csv')));names=[f'{g}_S{s}' for g in ['T','R11'] for s in range(4)];fig,axs=plt.subplots(2,4,figsize=(20,9),sharex=True,sharey=True)
for ax,n in zip(axs.ravel(),names):
 a=np.zeros((8,8))
 for r in rows:
  if r['split']=='eval' and r['condition']==n:a[int(r['feature_list_group']),int(r['actual_expert'])]=float(r['fraction'])*100
 im=ax.imshow(a,vmin=0,vmax=100,cmap='Blues',aspect='auto');ax.set(title=n,xlabel='Actual expert ID',ylabel='Original list group ID',xticks=range(8),yticks=range(8))
 for i in range(8):
  for j in range(8):ax.text(j,i,f'{a[i,j]:.0f}',ha='center',va='center',fontsize=7,color='white' if a[i,j]>55 else '#333')
fig.suptitle('13 | Feature-group hits -> actual expert | % of each group\'s hit events; tokens may hit multiple groups');fig.subplots_adjust(right=.9,hspace=.3,wspace=.2);fig.colorbar(im,cax=fig.add_axes([.93,.2,.015,.6]),label='% of feature-hit events in this list group');out(fig,'figure13_group_to_actual_expert','tables/group_to_actual_expert.csv','Does list membership become actual arrival?')
names=names+[n+f'_seed{s}' for n in ['Learned','LearnedLB'] for s in [11,22]];fig,axs=plt.subplots(3,4,figsize=(21,14));pool=stats()['pool'];grid=np.geomspace(1e-5,1,300)
for ax,n in zip(axs.ravel(),names):
 d=np.load(ROOT/'metrics/exposure'/f'eval_{n}.npz');empty=[]
 for e in range(8):
  if d['N_e'][e]==0:empty.append(e);continue
  values=np.sort(d['q'][pool,e]);cdf=np.searchsorted(values,grid,side='right')/len(pool);ax.plot(grid,cdf,label=f'e{e}',color=plt.get_cmap('tab10')(e))
 ax.set(title=n+(' | empty e='+','.join(map(str,empty)) if empty else ''),xscale='log',xlim=(1e-5,1),ylim=(0,1.01),xlabel='Within-expert frequency q (positive log axis)',ylabel='Fraction of all 9,615 features with q <= x');ax.grid(alpha=.15);ax.legend(ncol=4,fontsize=7)
fig.suptitle('14 | Actual exposure-frequency distributions | zeros included in CDF intercept; empty experts are NA');fig.tight_layout();out(fig,'figure14_expert_frequency_distributions','metrics/exposure/eval_*.npz','Compare all actual feature frequencies, retaining zero exposure and empty experts')
write_json(ROOT/'provenance/figures_manifest.json',manifest)
