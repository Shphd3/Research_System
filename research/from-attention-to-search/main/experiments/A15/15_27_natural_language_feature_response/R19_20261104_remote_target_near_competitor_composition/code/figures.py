from common import *
import numpy as np,pandas as pd
from stats_utils import boot_interval
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
plt.rcParams.update({'font.size':10})
geo=pd.read_csv(R/'tables/family_geometry.csv');mem=pd.read_csv(R/'tables/membership_summary.csv');freq=pd.read_csv(R/'tables/frequency_coverage.csv');change=pd.read_csv(R/'tables/frequency_pair_changes.csv');primary=json.load(open(R/'results/primary_hypotheses.json'));joint=json.load(open(R/'results/joint_hypotheses.json'));spec=json.load(open(R/'data/candidates.json'))['sites'];beh={x['id']:x for stage in ['discovery','heldout'] for x in rows(R/f'results/behavior_{stage}.jsonl')};panel={x['id']:x for x in rows(R/'data/panel.jsonl')}
colors={'high':'#cb7a31','middle':'#568bba','low':'#6caa79','insufficient':'#999999','zero':'#d2d2d2'};manifest=[]
def save(fig,name,question,sources):
 fig.savefig(R/'figures'/name,dpi=170,bbox_inches='tight');plt.close(fig);manifest.append(dict(file=name,question=question,sources=sources,sha256=sha(R/'figures'/name),unit='family; sparse sites separate',limit='observational constructed-text result; no activation intervention'))
for site in SITES:
 g=geo[(geo.site==site)&(geo.split=='heldout')];m=mem[(mem.site==site)&(mem.split=='heldout')];fig,ax=plt.subplots(2,2,figsize=(13,9),layout='constrained')
 conditions=[('content','main128','Target A vs B'),('distance','16_to_128','Same target 16 to 128'),('competition','neutral_to_opposite','Neutral to opposite')]
 for k,(kind,role,label) in enumerate(conditions):
  r=m[(m.kind==kind)&(m.role==role)].iloc[0];ax[0,0].errorbar([k],[r.mean_Jaccard],yerr=[[r.mean_Jaccard-r.lo],[r.hi-r.mean_Jaccard]],fmt='o',capsize=5,color='#28668c');ax[0,0].annotate(f"shared {r.mean_shared:.1f}\nin/out {r.mean_entered:.1f}/{r.mean_exited:.1f}",(k,r.mean_Jaccard),xytext=(0,12),textcoords='offset points',ha='center',fontsize=9)
 ax[0,0].set(xticks=range(3),xticklabels=[x[2] for x in conditions],ylim=(0,1.12),ylabel='Mean binary Jaccard;95% family interval',title='All 12 heldout families: membership')
 for k,(hyp,field,label) in enumerate([('H1','relative_target_alignment','Fixed-near target contrast'),('H2','relative_near_far_cosine','Near/far fact contrast')]):
  q=g[g[hyp+'_eligible']];values=q[field].to_numpy();jitter=np.linspace(-.09,.09,len(q));ax[0,1].scatter(k+jitter,values,s=32,color='#497ea1',alpha=.8)
  if len(values):ax[0,1].plot([k-.15,k+.15],[np.mean(values)]*2,color='black',lw=2)
  ax[0,1].text(k,-1.12,f'n={len(q)}/12',ha='center',fontsize=9)
 ax[0,1].axhline(0,color='gray',lw=.8);ax[0,1].set(xticks=[0,1],xticklabels=['H1 target across near words','H2 main 16 vs 128'],ylim=(-1.2,1.12),ylabel='Cosine of fixed-list relative differences',title='Fixed C list; strict common-member support')
 q=g[g.H3_eligible];cc=np.where(q.opposite_paired==1,'#3b789e','#c14946');ax[1,0].scatter(q.relative_target_projection,q.relative_near_projection,c=cc,s=55)
 if len(q):
  mn=min(q.relative_target_projection.min(),q.relative_near_projection.min(),0);mx=max(q.relative_target_projection.max(),q.relative_near_projection.max(),1);ax[1,0].plot([mn,mx],[mn,mx],ls='--',color='gray',label='T=N: opposite diagonal projection 0')
  if max(abs(mn),abs(mx))>8:ax[1,0].set_xscale('symlog',linthresh=1);ax[1,0].set_yscale('symlog',linthresh=1)
 for _,r in q.iterrows():ax[1,0].annotate(r.family,(r.relative_target_projection,r.relative_near_projection),fontsize=7,xytext=(3,3),textcoords='offset points')
 ax[1,0].set(xlabel='T projection / neutral target contrast',ylabel='N projection / neutral target contrast',title='Matched 128: target effect and nearby-word effect');ax[1,0].legend(fontsize=8)
 ax[1,1].scatter(q.relative_pattern_loss,q.behavior_loss,c=cc,s=55)
 for _,r in q.iterrows():ax[1,1].annotate(r.family,(r.relative_pattern_loss,r.behavior_loss),fontsize=7,xytext=(3,3),textcoords='offset points')
 h=next(x for x in primary if x['site']==site and x['hypothesis']=='H3');rho=h['mean'];ax[1,1].axhline(0,color='gray',lw=.8);ax[1,1].axvline(0,color='gray',lw=.8)
 ax[1,1].set(xlabel='Pattern loss:1 minus opposite projection retention',ylabel='Correct-candidate margin loss (nat)',title=f"Behavior association;n={len(q)},rho={rho:.3f}" if rho is not None else f'Behavior association;strict n={len(q)} insufficient')
 if len(q) and np.max(np.abs(q.relative_pattern_loss))>8:ax[1,1].set_xscale('symlog',linthresh=1)
 for a in ax.ravel():a.grid(alpha=.15)
 fig.suptitle(site+' | no feature IDs matched across dictionaries',fontsize=14)
 fig.text(.02,-.02,'C IDs: '+str(spec[site]['C'])+'; red=opposite pair fails;blue=both correct.\nMain distance changes fact position/filler order. Matched competition changes only the near item. Geometry omits only explicitly ineligible rows.',fontsize=9)
 save(fig,site+'_membership_geometry.png','How do reused members and within-family contrast geometry relate to target/distance/competition?',['tables/membership_summary.csv','tables/family_geometry.csv','results/primary_hypotheses.json'])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for row,site in enumerate(SITES):
 f=freq[(freq.site==site)&(freq.split=='heldout')].set_index('group').loc[GROUPS];labels=['high','middle','low','ref-insufficient','ref-zero'];x=np.arange(5);cols=[colors[g] for g in GROUPS]
 axes[row,0].bar(x,f.observed_members,color=cols)
 for i,(_,r) in enumerate(f.iterrows()):axes[row,0].text(i,r.observed_members,f'{int(r.observed_members)}/{int(r.reference_members)}',ha='center',va='bottom',fontsize=8)
 axes[row,0].set(xticks=x,xticklabels=labels,ylabel='Unique observed members',title=site+'; observed / reference group size');axes[row,0].tick_params(axis='x',rotation=25)
 axes[row,1].bar(x,f.active_instances,color=cols);axes[row,1].set_ylim(0,f.active_instances.max()*1.22)
 for i,(_,r) in enumerate(f.iterrows()):axes[row,1].text(i,r.active_instances,f"{int(r.families)}/12 families\n{int(r.positions)}/144 positions",ha='center',va='bottom',fontsize=7.5)
 axes[row,1].set(xticks=x,xticklabels=labels,ylabel='Positive activation instances',title='Family and position coverage (heldout)');axes[row,1].tick_params(axis='x',rotation=25)
 bars=[('content','main128','Fact A/B'),('distance','16_to_128','Distance'),('competition','neutral_to_opposite','Competition')];bottom=np.zeros(3)
 for group in GROUPS:
  values=[]
  for kind,role,_ in bars:
   d=change[(change.site==site)&(change.split=='heldout')&(change.kind==kind)&(change.role==role)];tot=d.abs_decoder_weighted_change.sum();values.append(100*d[d.group==group].abs_decoder_weighted_change.sum()/tot if tot else 0)
  axes[row,2].bar(range(3),values,bottom=bottom,color=colors[group],label=group);bottom+=values
 axes[row,2].set(xticks=range(3),xticklabels=[x[2] for x in bars],ylim=(0,105),ylabel='Share of absolute decoder-weighted atom change (%)',title='All changed atoms; cancellation not represented')
 axes[row,2].legend(fontsize=7,loc='lower right')
save(fig,'frequency_participation.png','Which old reference frequency groups participate and with what actual support?',['tables/frequency_coverage.csv','tables/frequency_pair_changes.csv','data/*_reference_bins.json'])
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
for i,site in enumerate(SITES):
 cache=np.load(R/f'cache/{site}_heldout_null.npz')
 for j,kind in enumerate(['binary','amplitude']):
  a=axes[i,j];v=next(x for x in joint if x['site']==site and x['kind']==kind)
  if v['selected_pairs']==0:a.text(.5,.5,'INSUFFICIENT\nNo discovery pair meeting\nsupport and variable-margin rules',ha='center',va='center',transform=a.transAxes)
  else:
   tr=cache[kind+'_decision_trace'].ravel();a.hist(tr,bins=22,color='#b4c9d8',label='Conditional null,256 draws');a.axvline(v['score'],color='#b94441',lw=2,label='Observed heldout score');a.legend(fontsize=8,loc='upper right');a.text(.02,.95,'4 frozen pairs; family n=12\nHolm p='+f"{v['holm_p']:.4f}"+'; '+v['verdict']+'\nFamily CI=['+f"{v['lo']:.3f}, {v['hi']:.3f}"+']',transform=a.transAxes,va='top',fontsize=8,bbox=dict(facecolor='white',alpha=.8,edgecolor='none'))
  a.set(title=site+' / '+kind,xlabel='Projection of joint excess on frozen discovery direction',ylabel='Null draws')
save(fig,'joint_marginal_controls.png','Does discovery-fixed joint structure replicate beyond occurrence/positive-value marginals?',['results/joint_hypotheses.json','cache/*_heldout_null.npz'])
selection=[]
for site in SITES:
 g=geo[(geo.site==site)&(geo.split=='heldout')];case='F23';base=g[g.family==case].iloc[0];eligible=g[g.H3_eligible]
 counter='F28' if site=='ATTN_SAE' else 'F11'
 selection.append(dict(site=site,primary=case,counter=counter,rule='F23 fixed pre-inference. After reading all families: report all failures F23/F27/F28; first strict successful family with nonpositive opposite projection is MLP F11. Attention F28 is the first other strict failed family with larger retained projection. Presentation-only correction is logged; primary selection/tests unchanged.',primary_strict=bool(base.H3_eligible)))
 data=np.load(R/'cache/heldout.npz');by={pid:i for i,pid in enumerate(data['ids'])};ids=spec[site]['C'];rr=[f'{case}_{co}_{gold}' for co in CONDS for gold in 'AB'];raw=np.zeros((12,len(ids)))
 for i,pid in enumerate(rr):
  k=by[pid];dd=dict(zip(data[site+'__indices'][k],data[site+'__values'][k]));raw[i]=[float(dd.get(f,0)) for f in ids]
 means=raw.mean(0);sd=raw.std(0);color=np.divide(raw-means,sd,out=np.zeros_like(raw),where=sd>1e-9)
 fig,(a,b)=plt.subplots(1,2,figsize=(12,9),gridspec_kw={'width_ratios':[2.6,1]},layout='constrained');im=a.imshow(color,cmap='RdBu_r',vmin=-2.5,vmax=2.5,aspect='auto');freqmap=pd.read_csv(R/f'data/{site}_reference_frequency.csv').set_index('atom')['group'].to_dict();a.set_xticks(range(len(ids)),[f'#{x}\n{freqmap[x]}' for x in ids],fontsize=9);labs=[f'{co} | target {gold}' for co in CONDS for gold in 'AB'];a.set_yticks(range(12),labs);a.axhline(5.5,color='black',lw=2)
 for i in range(12):
  for j in range(len(ids)):a.text(j,i,f'{raw[i,j]:.4g}',ha='center',va='center',fontsize=8,color='white' if abs(color[i,j])>1.3 else 'black')
 fig.colorbar(im,ax=a,shrink=.6,label='Within-feature display z-score; cell numerals are raw z')
 margins=np.array([beh[pid]['correct_margin'] for pid in rr]);b.barh(range(12),margins,color=np.where(margins>0,'#4e86a6','#bf4e46'));b.set_ylim(11.5,-.5);b.set_yticks(range(12),['']*12);b.axvline(0,color='black',lw=.8);b.axhline(5.5,color='black',lw=2);b.set_xlabel('Correct minus incorrect full score (nat)')
 for i,v in enumerate(margins):b.text(v,i,f'{v:.3f}',ha='left' if v>0 else 'right',va='center',fontsize=8)
 fig.suptitle(site+' | F23 battery / magnet | p319, token ":"',fontsize=14);fig.text(.02,-.035,'Top six rows: legacy distance panel; bottom six: matched128factorial. The separator marks a changed text frame.\nMatched nearN=unidentified object; nearA=battery; nearB=magnet. Full actual prefixes and both candidate scores are in casebook_cn.md.',fontsize=9)
 save(fig,site+'_F23_case.png','How do at least three literal member IDs and raw strengths change in the prespecified complete example?',['cache/heldout.npz','data/panel_portable.jsonl','results/behavior_heldout.jsonl','data/candidates.json'])
dump(R/'results/case_selection.json',selection);dump(R/'figures/provenance.json',dict(UTC=now(),figures=manifest));print('FIGURES',len(manifest))
