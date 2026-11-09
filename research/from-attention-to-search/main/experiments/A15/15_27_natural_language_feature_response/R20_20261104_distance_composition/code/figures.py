from load_data import *
from stats import *
import pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10})
pair=pd.read_csv(R/'tables/baseline_pair_metrics.csv');fact=pd.read_csv(R/'tables/baseline_fact_contrasts.csv');fm=pd.read_csv(R/'tables/baseline_fact_metrics.csv');freq=pd.read_csv(R/'tables/baseline_frequency_pairs.csv');ms=pd.read_csv(R/'tables/baseline_member_values.csv');primary=json.load(open(R/'results/primary_hypotheses.json'));selection=json.load(open(R/'results/case_selection.json'));colors={'ATTN_SAE':'#267ba3','MLPIN_SAE':'#c85a38'};groupcolors=['#cd873f','#5893bb','#64a275','#999999','#d6d6d6'];manifest=[]
def save(fig,name,question,sources,limit):
 fig.savefig(R/'figures'/name,dpi=170,bbox_inches='tight');plt.close(fig);manifest.append(dict(file=name,sha256=sha(R/'figures'/name),question=question,sources=sources,unit='whole family; facts averaged inside family',limit=limit))
def ratio_curve(df,field):
 val=df.groupby('family')[field].mean();lo,hi=interval(val);return float(np.exp(val.mean())),float(np.exp(lo)),float(np.exp(hi))
# The meeting figure isolates member retention from contrast magnitude.
fig,ax=plt.subplots(1,2,figsize=(11,4.2),layout='constrained')
for si,site in enumerate(SITES):
 q=pair[(pair.site==site)&(pair.split=='heldout')];vals=[32.];low=[32.];high=[32.]
 for d in [64,128]:
  v=q[(q.distance_left==16)&(q.distance_right==d)].groupby('family').shared.mean();a,b=interval(v,SEED+si);vals.append(v.mean());low.append(a);high.append(b)
 ax[0].errorbar(DISTS,vals,yerr=[np.array(vals)-low,np.array(high)-vals],marker='o',capsize=4,color=colors[site],label=site)
 ff=fact[(fact.site==site)&(fact.split=='heldout')&(fact.view=='native')];vals=[1.];low=[1.];high=[1.]
 for d in [64,128]:
  v=ff[(ff.distance_left==16)&(ff.distance_right==d)].log_relative_ratio;a,b=interval(v,SEED+si);vals.append(np.exp(v.mean()));low.append(np.exp(a));high.append(np.exp(b))
 ax[1].errorbar(DISTS,vals,yerr=[np.array(vals)-low,np.array(high)-vals],marker='o',capsize=4,color=colors[site],label=site)
ax[0].axhline(28.8,color='gray',ls=':',label='90% retained (operational H1)');ax[0].set(title='Members change',xlabel='Actual token gap d',ylabel='Common with d16, out of 32',ylim=(20,33));ax[1].axhspan(.8,1.25,color='#eeeeee',label='Registered tolerance [0.8, 1.25]');ax[1].axhline(1,color='gray',ls='--');ax[1].set(title='Fact contrast does not uniformly shrink',xlabel='Actual token gap d',ylabel='Relative fact separation / value at d16',ylim=(.65,1.5))
for a in ax:a.set_xticks(DISTS);a.grid(alpha=.2);a.legend(fontsize=8,loc='lower left')
fig.suptitle('R19 reanalysis | 12 heldout families | full native Top32 codes',fontsize=13);fig.text(.02,-.04,'Points: family means (left) or geometric ratios (right); intervals: 95% whole-family bootstrap.\nRelative separation = norm(A-B) / RMS(norm(A),norm(B)); it is an observable, not causal information use.',fontsize=9)
save(fig,'main_distance.png','Does turnover imply weaker within-family fact contrast?',['tables/baseline_pair_metrics.csv','tables/baseline_fact_contrasts.csv'],'Distance also changes fact absolute position/filler order; controls reported separately.')
fig,axes=plt.subplots(2,3,figsize=(14,8),layout='constrained')
for row,site in enumerate(SITES):
 q=pair[(pair.site==site)&(pair.split=='heldout')]
 for col,(metric,label) in enumerate([('log_full_norm_ratio','Whole-code raw norm ratio'),('log_common_norm_ratio','Common-member raw norm ratio'),('cosine_common','Common-member direction cosine')]):
  for k,(lo,hi) in enumerate(PAIRS):
   v=q[(q.distance_left==lo)&(q.distance_right==hi)].groupby('family')[metric].mean();data=np.exp(v) if col<2 else v;axes[row,col].scatter(k+np.linspace(-.09,.09,len(data)),data,s=24,color=colors[site],alpha=.7);value=np.exp(v.mean()) if col<2 else v.mean();axes[row,col].plot([k-.2,k+.2],[value]*2,color='black',lw=2)
  axes[row,col].axhline(1,color='gray',ls='--');axes[row,col].set(xticks=range(3),xticklabels=[f'{lo} to {hi}' for lo,hi in PAIRS],ylabel=label,title=site+'; n=12 families');axes[row,col].grid(alpha=.15)
save(fig,'strength_audit.png','Separate amplitude changes from common-member relative arrangement.',['tables/baseline_pair_metrics.csv'],'High common-vector cosine is dominated by common positive coordinates; it does not imply unchanged A-B contrast.')
fig,axes=plt.subplots(2,3,figsize=(14,8),layout='constrained')
for row,site in enumerate(SITES):
 for col,field in enumerate(['log_raw_ratio','log_relative_ratio']):
  for view,color in [('native',colors[site]),('pre_relu','#6e9964'),('hidden','#8c79a5')]:
   q=fact[(fact.site==site)&(fact.split=='heldout')&(fact.view==view)];vals=[1.]
   for d in [64,128]:vals.append(float(np.exp(q[(q.distance_left==16)&(q.distance_right==d)][field].mean())))
   axes[row,col].plot(DISTS,vals,marker='o',label={'native':'native Top32','pre_relu':'preTopK ReLU','hidden':'hook input h'}[view],color=color)
  axes[row,col].axhline(1,color='gray',ls='--');axes[row,col].set(xticks=DISTS,xlabel='Actual gap d',ylabel='Ratio to d16',title=site+(' | raw A-B norm' if col==0 else ' | scale-normalized separation'));axes[row,col].legend(fontsize=8)
 q=fact[(fact.site==site)&(fact.split=='heldout')&(fact.distance_left==16)&(fact.distance_right==128)];native=q[q.view=='native'].set_index('family');six=q[q.view=='six'].set_index('family');axes[row,2].scatter(six.unit_contrast_cosine,native.unit_contrast_cosine,color=colors[site]);axes[row,2].plot([0,1],[0,1],ls='--',color='gray')
 for fam in native.index:axes[row,2].annotate(fam,(six.loc[fam,'unit_contrast_cosine'],native.loc[fam,'unit_contrast_cosine']),fontsize=7,xytext=(3,3),textcoords='offset points')
 axes[row,2].set(xlabel='Fixed-six contrast cosine (zeros retained)',ylabel='Full-code contrast cosine',title=site+' | n=12, all families')
save(fig,'fact_contrast_audit.png','What do normalization, truncation and selected members hide?',['tables/baseline_fact_contrasts.csv'],'Rectified preTopK is diagnostic; it is not an alternative trained SAE code or intervention.')
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
for row,site in enumerate(SITES):
 for col,stat in enumerate(['entered','exited']):
  bottom=np.zeros(3)
  for group,color in zip(GROUPS,groupcolors):
   means=[]
   for lo,hi in PAIRS:
    q=freq[(freq.site==site)&(freq.split=='heldout')&(freq.group==group)&(freq.distance_left==lo)&(freq.distance_right==hi)];means.append(q.groupby('family')[stat].mean().mean())
   axes[row,col].bar(range(3),means,bottom=bottom,color=color,label=group);bottom+=means
  axes[row,col].set(xticks=range(3),xticklabels=[f'{a} to {b}' for a,b in PAIRS],ylabel='Mean members per paired fact',title=site+' | '+stat+' | 12 families');axes[row,col].legend(fontsize=8)
save(fig,'frequency_turnover.png','Which fixed reference groups enter or exit at each distance pair?',['tables/baseline_frequency_pairs.csv'],'In=out totals follow Top32; category composition and opportunities are the measured objects.')
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
for row,site in enumerate(SITES):
 q=freq[(freq.site==site)&(freq.split=='heldout')&(freq.distance_left==16)&(freq.distance_right==128)]
 for k,group in enumerate(GROUPS):
  qq=q[q.group==group]
  for offset,field,color,label in [(-.13,'reference_entry_excess','#9e9e9e','natural-frequency opportunity'),(.13,'task_entry_excess',colors[site],'discovery-task opportunity')]:
   vv=qq.groupby('family')[field].mean();lo,hi=interval(vv);axes[row,0].errorbar(k+offset,vv.mean(),yerr=[[vv.mean()-lo],[hi-vv.mean()]],fmt='o',capsize=3,color=color,label=label if k==0 else None)
  vv=qq.groupby('family').rank_matched_exit_excess.mean();lo,hi=interval(vv);axes[row,1].errorbar(k,vv.mean(),yerr=[[vv.mean()-lo],[hi-vv.mean()]],fmt='o',capsize=4,color=colors[site])
 for col in range(2):axes[row,col].axhline(0,color='gray',ls='--');axes[row,col].set(xticks=range(5),xticklabels=['high','middle','low','ref-insuff.','ref-zero'],ylabel='Observed minus conditional expected members',title=site+(' | entrants' if col==0 else ' | rank-matched exits'));axes[row,col].grid(alpha=.15)
 axes[row,0].legend(fontsize=8)
save(fig,'frequency_opportunities.png','Do group counts differ after accounting for opportunities?',['tables/baseline_frequency_pairs.csv','cache/*_opportunity_weights.npz'],'512 conditional draws; whole-family intervals. Reference-zero expectation is uncalibrated, not infinite enrichment. No semantic or causal ranking.')
fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
for row,site in enumerate(SITES):
 q=ms[(ms.site==site)&(ms.split=='heldout')&(ms.distance_left==16)&(ms.distance_right==128)&(ms.status!='common')];axes[row,0].hist(q.active_value_over_cutoff,bins=np.geomspace(1,max(q.active_value_over_cutoff.max(),1.1),24),color=colors[site],alpha=.7);axes[row,0].axvline(1.25,color='gray',ls='--');axes[row,0].set(xlabel='Selected activation / local Top32 cutoff',ylabel='Turnover instances (descriptive pooled)',title=site+f' | {len(q)} instances; 12 families')
 q=fact[(fact.site==site)&(fact.split=='heldout')&(fact.distance_left==16)&(fact.distance_right==128)];native=q[q.view=='native'].set_index('family');pre=q[q.view=='pre_relu'].set_index('family');axes[row,1].scatter(native.raw_contrast_cosine,pre.raw_contrast_cosine,color=colors[site]);axes[row,1].plot([0,1],[0,1],ls='--',color='gray')
 for fam in native.index:axes[row,1].annotate(fam,(native.loc[fam,'raw_contrast_cosine'],pre.loc[fam,'raw_contrast_cosine']),fontsize=7,xytext=(3,3),textcoords='offset points')
 axes[row,1].set(xlabel='PostTop32 A-B direction cosine',ylabel='Rectified preTopK A-B direction cosine',title=site+' | truncation sensitivity')
save(fig,'threshold_audit.png','How much turnover sits near truncation, and how does truncation affect direction?',['tables/baseline_member_values.csv','tables/baseline_fact_contrasts.csv'],'BelowTop32 does not imply zero encoder response; preTopK codes are diagnostic, not decoder-trained alternatives.')
if (R/'tables/control_effect_differences.csv').exists():
 controls=pd.read_csv(R/'tables/controls_fact_contrasts.csv');diff=pd.read_csv(R/'tables/control_effect_differences.csv');fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained');frames=['baseline','reverse','content','fixed_e']
 for col,site in enumerate(SITES):
  for k,frame in enumerate(frames):
   dd=fact if frame=='baseline' else controls;q=dd[(dd.site==site)&(dd.frame==frame)&(dd.split=='heldout')&(dd.view=='native')&(dd.distance_left==16)&(dd.distance_right==128)];v=q.log_relative_ratio;lo,hi=interval(v);value=np.exp(v.mean());axes[col].errorbar(k,value,yerr=[[value-np.exp(lo)],[np.exp(hi)-value]],fmt='o',capsize=5,color=colors[site]);axes[col].text(k,np.exp(hi)+.02,f'n={len(q)}',ha='center',fontsize=8)
  axes[col].axhspan(.8,1.25,color='#eee');axes[col].axhline(1,color='gray',ls='--');axes[col].set(xticks=range(4),xticklabels=['original','reverse\nweather','office\nfiller','fixed e190'],ylabel='Relative fact-separation ratio,128 / 16',title=site);axes[col].grid(alpha=.15)
 fig.text(.02,-.03,'All plotted conditions use the same 12 families. The +64 position-ID control is paired separately on 6 families; see position_id_shift_audit.csv.',fontsize=9)
 save(fig,'controls.png','Does the magnitude pattern survive the declared filler and position controls?',['tables/controls_fact_contrasts.csv','tables/control_effect_differences.csv'],'Fixed-e also changes answer position/length; pos64 changes encoding IDs only, not visible context. Descriptive, no fresh-template confirmation.')
data={site:load_site(site,False)[0] for site in SITES};b=behavior(False)
for case in selection['families']:
 fam=case['family'];fig,axes=plt.subplots(1,3,figsize=(14,6),gridspec_kw={'width_ratios':[2,2,1]},layout='constrained');ids=[cid('baseline',fam,d,g) for d in DISTS for g in 'AB']
 for k,site in enumerate(SITES):
  atoms=SPEC[site]['C'];a=np.array([data[site][pid]['z'][atoms] for pid in ids]);sd=a.std(0);colorsz=np.divide(a-a.mean(0),sd,out=np.zeros_like(a),where=sd>1e-12);axes[k].imshow(colorsz,cmap='RdBu_r',vmin=-2.5,vmax=2.5,aspect='auto');ref=pd.read_csv(R/f'data/{site}_reference_frequency.csv').set_index('atom')
  axes[k].set(yticks=range(6),yticklabels=[f'd{d} target {g}' for d in DISTS for g in 'AB'],xticks=range(6),xticklabels=[f'#{f}\n{ref.loc[f,"group"]}' for f in atoms],title=site+' | old fixed six')
  axes[k].tick_params(axis='x',rotation=35,labelsize=8)
  for i in range(6):
   for j in range(6):axes[k].text(j,i,f'{a[i,j]:.3g}',ha='center',va='center',fontsize=8,color='white' if abs(colorsz[i,j])>1.3 else 'black')
 margins=[b[pid]['correct_margin'] for pid in ids];axes[2].barh(range(6),margins,color='#4c8a9b');axes[2].invert_yaxis();axes[2].set(yticks=range(6),yticklabels=['']*6,xlabel='Correct-candidate full margin (nat)',title='Same native model')
 fig.suptitle(f'{fam} | {case["role"]} | every original family remains in the data');fig.text(.02,-.04,'Cell numbers are raw z. Colors standardize each feature for display only. Zero is an actual postTop32 zero.\nFixed-six panel is illustrative; all-member turnover and full-code fact contrasts are in the casebook.',fontsize=9)
 save(fig,'case_'+fam+'.png','Literal original case: '+case['reason'],['cache/*_old_main.npz','results/case_selection.json','results/behavior_old.jsonl'],'These six IDs do not represent the full dictionary; full union and counterexamples are retained.')
dump(R/'figures/provenance.json',dict(UTC=now(),local_time=local_now(),figures=manifest));print('FIGURES',len(manifest))
