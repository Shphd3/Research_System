from common import *
import numpy as np,matplotlib,textwrap
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'figure.dpi':130,'savefig.dpi':160})
rr=rows(R/'results/conditions.jsonl');pp=rows(R/'data/panel.jsonl');idx={p['id']:p for p in pp};prov=[]
def find(p,s,d,arm,alpha=None,destination=None,group='common'):return next(r for r in rr if r['text_id']==p['id'] and r['site']==s and r['intervention_domain']==d and r['arm']==arm and (arm=='identity' or r['group']==group) and r['alpha']==alpha and r['destination']==destination)
def save(fig,name,sources,purpose):
 fig.savefig(R/'figures'/name,bbox_inches='tight');plt.close(fig);prov.append(dict(file=name,sources=sources,purpose=purpose,independence='8heldout template families; two child rows per family',claim='Local decoder-direction effect, not uniqueness or genuine concept conversion'))
for s in SITES:
 for d,ls in DOMAINS.items():
  p=next(p for p in pp if p['family']=='F09' and p['wording']=='explicit' and p['label']==ls[1]);dest=ls[2];a=find(p,s,d,'identity',0,group='none');b=find(p,s,d,'delete');c=find(p,s,d,'strength',.5,dest);sh=find(p,s,d,'strength_shuffle',.5,dest);recs=[a,b,c,sh]
  fig=plt.figure(figsize=(15,11));gs=fig.add_gridspec(3,2,height_ratios=[.5,1,1],hspace=.45,wspace=.32);ax=fig.add_subplot(gs[0,:]);ax.axis('off');ax.text(0,.9,'\n'.join(textwrap.wrap(p['prefix'].replace('\n',' / '),145)),va='top',fontsize=11);ax.set_title(s+' | '+d+' | F09 '+ls[1]+' | original vs residual-preserving edits',loc='left',fontweight='bold')
  ax=fig.add_subplot(gs[1,0]);x=np.array([b['old_z'],b['new_z'],c['new_z'],sh['new_z']]);im=ax.imshow(x,cmap='YlGnBu',aspect='auto');ax.set_xticks(range(len(b['feature_ids'])),['#'+str(t) for t in b['feature_ids']],rotation=35 if len(b['feature_ids'])>4 else 0,ha='right' if len(b['feature_ids'])>4 else 'center');ax.set_yticks(range(4),['original','delete common','opposite alpha=.5','shuffle, norm matched']);ax.set_title('Actual latent strengths z on fixed members')
  for (i,j),v in np.ndenumerate(x):ax.text(j,i,f'{v:.3f}',ha='center',va='center',fontsize=9,color='white' if v>x.max()*.65 else 'black')
  plt.colorbar(im,ax=ax,shrink=.75)
  ax=fig.add_subplot(gs[1,1]);pos=np.arange(4);colors=['#6d8c9e','#d98655','#4b9c81','#9f78af']
  for k,r in enumerate(recs):ax.bar(pos+(k-1.5)*.18,np.array(r['scores'])-a['baseline_scores'],width=.18,color=colors[k],label=['original','delete','opposite .5','shuffle'][k])
  ax.set_xticks(pos,[l+'.\nS0='+f'{a["baseline_scores"][j]:.3f}' for j,l in enumerate(a['candidate_order'])]);ax.set_ylabel('Change in complete log probability (nats)');ax.set_title('Complete score changes; native S0 listed below');ax.legend(fontsize=8,loc='lower left')
  ax=fig.add_subplot(gs[2,0]);ax.bar(np.arange(len(c['feature_ids']))-.18,np.array(c['new_z'])-c['old_z'],width=.36,label='opposite .5',color=colors[2]);ax.bar(np.arange(len(c['feature_ids']))+.18,np.array(sh['new_z'])-sh['old_z'],width=.36,label='shuffle matched',color=colors[3]);ax.set_xticks(range(len(c['feature_ids'])),['#'+str(t) for t in c['feature_ids']],rotation=35 if len(c['feature_ids'])>4 else 0);ax.set_ylabel('Raw latent change');ax.set_title(f'Group L2 {c["old_group_L2"]:.3f} -> {c["new_group_L2"]:.3f}\nInjected norm {c["delta_hidden_L2"]:.4f}, shuffle {sh["delta_hidden_L2"]:.4f}');ax.legend(fontsize=8)
  ax=fig.add_subplot(gs[2,1]);ax.axis('off');tabledata=[]
  for j,l in enumerate(a['candidate_order']):tabledata.append([l,f'{a["candidate_sequence_prob4"][j]:.3f}',f'{c["candidate_sequence_prob4"][j]:.3f}',a['candidate_vocab_ranks'][j],c['candidate_vocab_ranks'][j]])
  tt=ax.table(cellText=tabledata,colLabels=['candidate','p4 original','p4 opposite','rank original','rank opposite'],loc='center',cellLoc='center');tt.auto_set_font_size(False);tt.set_fontsize(9);tt.scale(1,1.8);ax.set_title('p4: normalized four complete sequences\nrank: first word among full151936token vocabulary')
  fig.text(.09,.012,'Feature IDs are dictionary-specific. Decoder linear delta is added to original hidden state, preserving original SAE residual. Full scores and ranks use different denominators.',fontsize=9)
  save(fig,f'case_{d}_{s}.png',['conditions.jsonl','top20.jsonl'],'Connect exact text and feature-strength changes to native candidate scores and word ranks.')

fig,axes=plt.subplots(2,2,figsize=(14,10),gridspec_kw={'hspace':.4,'wspace':.3})
for si,s in enumerate(SITES):
 for di,d in enumerate(DOMAINS):
  ax=axes[si,di]
  for j,arm in enumerate(['delete','delete_matched','norm_random_add']):
   vv=[]
   for f in [f'F{i:02d}' for i in range(9,17)]:
    t=[r for r in rr if r['site']==s and r['intervention_domain']==d and r['family']==f and r['wording']=='explicit' and r['label'] in DOMAINS[d][1:] and r['arm']==arm and r['group']=='common'];vv.append(np.mean([-r['correct_margin_change'] for r in t]))
   ax.scatter(j+np.linspace(-.08,.08,8),vv,color=['#d98655','#6d8c9e','#9f78af'][j]);ax.plot([j-.12,j+.12],[np.mean(vv)]*2,color='black',lw=2)
   for k,v in enumerate(vv):ax.annotate(f'{k+9:02d}',(j+(k-3.5)*.023,v),fontsize=7,xytext=(2,2),textcoords='offset points')
  ax.axhline(0,color='gray',ls='--');ax.set_xticks(range(3),['delete common','delete other\nclosest; unmatched','random positive add\nsame hidden norm']);ax.set_ylabel('Correct sibling-margin loss (nats)');ax.set_title(s+' | '+d+' |8family means')
save(fig,'deletion_family_controls.png',['conditions.jsonl','family_primary.csv','candidate_match_audit.csv'],'Distinguish local deletion effects from other deletions and equal-norm arbitrary-combination changes; mismatches explicit.')

fig,axes=plt.subplots(2,2,figsize=(14,10),gridspec_kw={'hspace':.35,'wspace':.3})
for si,s in enumerate(SITES):
 for di,d in enumerate(DOMAINS):
  ax=axes[si,di]
  for j,arm in enumerate(['strength','strength_shuffle','strength_own']):
   means=[]
   for a in [.25,.5,1.]:
    vv=[];eligible=[]
    for f in [f'F{i:02d}' for i in range(9,17)]:
     t=[r for r in rr if r['site']==s and r['intervention_domain']==d and r['family']==f and r['wording']=='explicit' and r['label'] in DOMAINS[d][1:] and r['arm']==arm and r['alpha']==a and r['destination']!=r['label']];vv.append(np.mean([-r['correct_margin_change'] for r in t]));eligible.append(all(r['support_preserved'] and r['active_before']>=2 and (arm=='strength' or r['norm_ratio'] is not None and .9<=r['norm_ratio']<=1.1) for r in t))
    means.append(np.mean(vv))
    for k,value in enumerate(vv):ax.scatter(a+(j-1)*.018+(k-3.5)*.002,value,s=20,alpha=.7,marker='o' if eligible[k] else 'x',color=['#4b9c81','#9f78af','#6d8c9e'][j])
   ax.plot([.25,.5,1.],means,color=['#4b9c81','#9f78af','#6d8c9e'][j],label=['opposite pattern','shuffled pattern, norm matched','own-side pattern, norm matched where feasible'][j])
  ax.axhline(0,color='gray',ls='--');ax.set_xlabel('Registered interpolation alpha');ax.set_ylabel('Correct sibling-margin loss (nats)');ax.set_title(s+' | '+d+' | x: support/norm ineligible');ax.legend(fontsize=7)
save(fig,'strength_family_dose_controls.png',['conditions.jsonl','control_quality.csv'],'Show full-family dose response and matched same-member controls, including contrary cases.')
dump(R/'evidence/figure_provenance.json',prov);print('S07_FIGURES',len(prov),flush=True)
