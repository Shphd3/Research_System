from common import *
import numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt,textwrap
from scipy import sparse
plt.rcParams.update({'font.size':11,'axes.titlesize':12,'figure.dpi':130,'savefig.dpi':160})
pp=rows(R/'data/panel.jsonl');index={p['id']:i for i,p in enumerate(pp)};sel=json.load(open(R/'results/selection.json'))['sites'];prov=[]
def csvrows(name):return list(csv.DictReader(open(R/f'results/{name}.csv')))
ov=csvrows('overlaps');jm=csvrows('joint_patterns');rm=csvrows('row_metrics');be=csvrows('behavior_summary');he=csvrows('hypothesis_statistics');fe=csvrows('family_effects');rr=csvrows('support_random_baselines');wc=csvrows('wording_controls')
def save(fig,name,sources,purpose):
 fig.savefig(R/'figures'/name,bbox_inches='tight');plt.close(fig);prov.append(dict(file=name,source_tables=sources,purpose=purpose,unit_of_independence='template family',allowed_claim='Frozen SAE coordinate association on constructed stimuli; human scientific acceptance Unknown'))
def heat(ax,x,ids,labels,title):
 im=ax.imshow(x,aspect='auto',cmap='YlGnBu',vmin=0);ax.set_xticks(range(len(ids)),['#'+str(i) for i in ids],rotation=35 if len(ids)>4 else 0,ha='right' if len(ids)>4 else 'center',fontsize=10);ax.set_yticks(range(3),labels);ax.set_title(title)
 for (i,j),v in np.ndenumerate(x):ax.text(j,i,f'{v:.3f}',ha='center',va='center',fontsize=10,color='white' if v>x.max()*.65 else 'black')
 plt.colorbar(im,ax=ax,shrink=.72)
for s in SITES:
 z=sparse.load_npz(R/f'data/{s}_all_z_csr.npz').toarray()
 for d,labels in DOMAINS.items():
  ps=[next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==c) for c in labels];ii=[index[p['id']] for p in ps];x=z[ii];ids=sel[s][d]['H2'];q=x[:,ids]/np.linalg.norm(x[:,ids],axis=1,keepdims=True)
  fig=plt.figure(figsize=(14,11));gs=fig.add_gridspec(3,2,height_ratios=[1.12,1.2,1.1],hspace=.4,wspace=.3)
  ax=fig.add_subplot(gs[0,:]);ax.axis('off');yy=.99
  for p in ps:
   text=p['label']+': '+p['prefix'].replace('\n',' / ')
   lines=textwrap.wrap(text,135);ax.text(0,yy,'\n'.join(lines),va='top',fontsize=11);yy-=.2+.05*(len(lines)-1)
  ax.set_title(f'{s}: complete F09 {d} family | heldout, explicit words | final colon ID25',loc='left',pad=16,fontweight='bold')
  ax=fig.add_subplot(gs[1,0]);shared=[];recruit=[];lost=[]
  for k in [1,2]:
   b=x[0]>0;c=x[k]>0;shared.append((b&c).sum());recruit.append((~b&c).sum());lost.append((b&~c).sum())
  ax.bar([0,1],shared,color='#519778',label='retained');ax.bar([0,1],recruit,bottom=shared,color='#e6ae46',label='recruited')
  for i in range(2):ax.text(i,33,f'{shared[i]} retained + {recruit[i]} in\n{lost[i]} lost',ha='center',fontsize=10)
  ax.set_ylim(0,40);ax.set_xticks([0,1],[labels[0]+' -> '+labels[k] for k in [1,2]]);ax.set_ylabel('Members / 32 active');ax.legend(loc='lower center',bbox_to_anchor=(.5,-.25),ncol=2,fontsize=9)
  ax.set_title('Membership changes (equal in/out is Top32 structure)')
  ax=fig.add_subplot(gs[1,1]);ax.axis('off');lines=[]
  for j,c in enumerate(labels):lines.append(f'{c}: all-z L2 = {np.linalg.norm(x[j]):.3f}; list L2 = {np.linalg.norm(x[j,ids]):.3f}')
  triple=np.flatnonzero((x>0).all(0));lines.append(f'Triple common: {len(triple)}/32 parent members')
  for j in [1,2]:
   new=np.flatnonzero((x[0]==0)&(x[j]>0));lines.append(labels[j]+' recruited IDs: '+', '.join(str(a) for a in new))
  ax.text(0,1,'\n\n'.join(textwrap.fill(t,64) for t in lines),va='top',fontsize=10)
  heat(fig.add_subplot(gs[2,0]),x[:,ids],ids,labels,'Raw z on discovery-fixed H2 members')
  heat(fig.add_subplot(gs[2,1]),q,ids,labels,'q = z / L2(z on this exact fixed list)')
  fig.text(.1,.025,'Each grid cell is one actual activation. Zero remains zero. Complete support, preactivation and texts are indexed in the casebook.',fontsize=10)
  save(fig,f'case_{d}_{s}.png',['active_values.csv','candidate_values.csv','overlaps.csv','row_metrics.csv'],'Inspect one complete family without averaging away its texts/member IDs/strengths.')

fig,axes=plt.subplots(2,2,figsize=(14,10),gridspec_kw={'hspace':.35,'wspace':.28})
for row,s in enumerate(SITES):
 ax=axes[row,0];groups=['parent-child','siblings','cross-domain'];values=[]
 for group in groups:
  vv=[]
  for f in [f'F{i:02d}' for i in range(9,17)]:
   tt=[r for r in ov if r['site']==s and r['family']==f and r['wording']=='explicit']
   if group=='cross-domain':v=[float(r['Jaccard']) for r in tt if r['relation']=='cross']
   elif group=='siblings':v=[float(r['Jaccard']) for r in tt if (r['a'],r['b']) in [('cat','dog'),('car','bicycle')]]
   else:v=[float(r['Jaccard']) for r in tt if r['relation']=='within' and (r['a'] in DOMAINS or r['b'] in DOMAINS)]
   vv.append(np.mean(v))
  values.append(vv)
 for i,v in enumerate(values):
  ax.scatter(i+np.linspace(-.09,.09,8),v,color=['#24889a','#dc8c3f','#8268a7'][i]);ax.plot([i-.15,i+.15],[np.mean(v)]*2,color='black',lw=2)
 for kind,style,col in [('uniform',':','gray'),('frequency_weighted','--','#9f403a')]:
  v=[float(r['Jaccard']) for r in rr if r['site']==s and r['baseline']==kind];ax.axhline(np.mean(v),ls=style,color=col,label=f'{kind} 32/30000 (512)')
 ax.set_xticks(range(3),groups);ax.set_ylabel('Jaccard = intersection / union');ax.set_title(s+' | one dot = family mean; n=8');ax.legend(fontsize=8)
 ax=axes[row,1]
 for j,d in enumerate(DOMAINS):
  t=[r for r in fe if r['site']==s and r['domain']==d and r['hypothesis']=='H2' and r['split']=='heldout' and r['wording']=='explicit']
  for k,r in enumerate(t):ax.scatter(j+(k-3.5)*.025,float(r['estimate']),marker='o' if r['eligible']=='True' else 'x',color=['#24889a','#dc8c3f'][j]);ax.annotate(r['family'],(j+(k-3.5)*.025,float(r['estimate'])),fontsize=7,xytext=(3,3),textcoords='offset points')
  h=next(r for r in he if r['site']==s and r['domain']==d and r['hypothesis']=='H2' and r['split']=='heldout' and r['wording']=='explicit')
  if h['estimate']:ax.errorbar(j,float(h['estimate']),yerr=[[float(h['estimate'])-float(h['ci_low'])],[float(h['ci_high'])-float(h['estimate'])]],color='black',fmt='_',capsize=5)
 ax.axhline(0,color='gray',ls='--');ax.set_xticks([0,1],['animal: dog-cat','vehicle: bicycle-car']);ax.set_ylabel('Joint q difference along frozen discovery direction');ax.set_title('H2: points and family-bootstrap 95% interval\nx = unequal-list support or fewer than 2 active members')
save(fig,'relations_and_joint_patterns.png',['overlaps.csv','support_random_baselines.csv','joint_patterns.csv','hypothesis_statistics.csv'],'Compare related/cross-domain membership and joint strength changes with full family variation.')

fig,axes=plt.subplots(2,2,figsize=(14,10),gridspec_kw={'hspace':.45,'wspace':.3})
for si,s in enumerate(SITES):
 for di,d in enumerate(DOMAINS):
  ax=axes[si,di]
  for j,w in enumerate(['explicit','synonym','property']):
   tt=[r for r in fe if r['site']==s and r['domain']==d and r['hypothesis']=='H2' and r['split']=='heldout' and r['wording']==w]
   for k,r in enumerate(tt):ax.scatter(j+(k-3.5)*.025,float(r['estimate']),color=['#24889a','#dc8c3f','#8268a7'][j],marker='o' if r['eligible']=='True' else 'x')
   h=next(r for r in he if r['site']==s and r['domain']==d and r['hypothesis']=='H2' and r['split']=='heldout' and r['wording']==w)
   vals=[r for r in be if r['split']=='heldout' and r['wording']==w and r['domain']==d and r['sibling_correct']!=''];cnt=','.join(r['sibling_correct'] for r in vals)
   ax.text(j,.98,f'eligible {h["eligible"]}/8\ncorrect {cnt} /8 each',ha='center',va='top',fontsize=9,transform=ax.get_xaxis_transform())
  ax.axhline(0,color='gray',ls='--');ax.set_xticks(range(3),['explicit words','synonyms','properties']);ax.set_ylabel('Joint q projection\n(frozen explicit-discovery direction)');ax.set_title(s+' | '+d);ax.margins(y=.28)
fig.text(.1,.025,'All 8 heldout families are shown in every condition. Crosses remain descriptive and cannot establish fixed-member strength replication.',fontsize=10)
save(fig,'wording_control_joint.png',['family_effects.csv','behavior_summary.csv','hypothesis_statistics.csv'],'Show whether frozen joint patterns persist, reverse or become ineligible under lexical changes.')

fig,axes=plt.subplots(1,2,figsize=(14,5))
for si,s in enumerate(SITES):
 ax=axes[si]
 for j,d in enumerate(DOMAINS):
  for k,w in enumerate(['synonym','property']):
   vv=[]
   for f in [f'F{i:02d}' for i in range(9,17)]:vv.append(np.mean([float(r['Jaccard']) for r in wc if r['site']==s and r['domain']==d and r['family']==f and r['to_wording']==w]))
   x=j*2+k;ax.scatter(x+np.linspace(-.1,.1,8),vv,color=['#24889a','#8268a7'][k]);ax.plot([x-.15,x+.15],[np.mean(vv)]*2,color='black')
 ax.set_xticks(range(4),['animal\nsynonym','animal\nproperty','vehicle\nsynonym','vehicle\nproperty']);ax.set_ylim(0,1);ax.set_title(s+' | same class, changed wording');ax.set_ylabel('Support Jaccard: explicit vs changed wording')
save(fig,'wording_control_support.png',['wording_controls.csv'],'Measure support changes with semantic intent retained; dots average three levels within each of8 families.')
dump(R/'evidence/figure_provenance.json',prov)
print('FIGURES',len(prov),flush=True)
