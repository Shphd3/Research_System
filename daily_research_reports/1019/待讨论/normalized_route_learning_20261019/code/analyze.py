from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':10})
FIGS=[]
def figsave(fig,name,source,question):
 (ROOT/'figures').mkdir(exist_ok=True)
 for ext in ['png','svg','pdf']:
  path=ROOT/'figures'/f'{name}.{ext}';fig.savefig(path,dpi=170,bbox_inches='tight');FIGS.append(dict(path=str(path),sha256=sha(path),source=source,question=question))
 plt.close(fig)
def bootstrap(c,nll,weights,block_ids,features):
 x=csr(c,True)[:,features];b=c['block_id'].numpy();bi=np.searchsorted(block_ids,b);C=sparse.csr_matrix((np.ones(len(b)),(bi,np.arange(len(b)))),shape=(len(block_ids),len(b)));counts=(C@x).toarray();sums=(C@x.multiply(nll[:,None])).toarray();den=weights@counts;num=weights@sums;means=np.divide(num,den,out=np.full_like(num,np.nan),where=den>0);macro=np.nanmean(means,axis=1);tot=weights@np.bincount(bi,weights=nll);nn=weights@np.bincount(bi);return macro,tot/nn,np.isfinite(means).sum(1)
def run():
 t0=time.monotonic();curves=[];ends=[];nlls={};boot={};c=loadcache('eval');L=c['low_ids'].numpy();bids=np.unique(c['block_id'].numpy());rg=np.random.default_rng(20261019);weights=rg.multinomial(len(bids),np.repeat(1/len(bids),len(bids)),1000);np.save(ROOT/'config/bootstrap_context_multiplicities.npy',weights)
 for co in CFG['conditions']:
  name=co['id']
  for seed in CFG['seeds']:
   out=ROOT/f'training/{name}/seed{seed}';complete=(out/'complete.json').exists()
   for ep in range(4):
    pp=out/f'metrics_epoch{ep}.json'
    if pp.exists():curves.append(json.load(open(pp)))
   if complete:
    met=json.load(open(out/'metrics_epoch3.json'));met.update(status='COMPLETE',alias=co['alias'],initial_overall=json.load(open(out/'metrics_epoch0.json'))['overall'],initial_M_L=json.load(open(out/'metrics_epoch0.json'))['M_L']);ends.append(met);nll=np.load(out/'eval_epoch3.npz')['nll'];nlls[name,seed]=nll;boot[name,seed]=bootstrap(c,nll,weights,bids,L)
   else:ends.append(dict(condition=name,seed=seed,status='PARTIAL' if out.exists() else 'NOT RUN',alias=co['alias']))
 csvwrite(ROOT/'tables/training_metrics.csv',curves)
 # Make rectangular full-condition endpoint table.
 keys=sorted(set().union(*(row.keys() for row in ends)));csvwrite(ROOT/'tables/all_condition_results.csv',[{k:row.get(k) for k in keys} for row in ends]);lookup={(x['condition'],x['seed']):x for x in ends}
 comps=[('T_S1','T_S0','primary calibration B-A'),('T_S1','R11_S1','primary organization B-C')]
 for group in ['T','R11']:
  comps.extend((f'{group}_S{s}',f'{group}_S0','same list calibration') for s in [1,2,3]);comps.append((f'{group}_S3',f'{group}_S2','additional frequency weighting'))
 comps.extend((f'T_S{s}',f'R11_S{s}','same score organization') for s in range(4));comps.append(('LearnedLB','Learned','specific .01 balance coefficient'))
 comps=list(dict.fromkeys(comps));paired=[]
 for a,b,role in comps:
  for seed in CFG['seeds']:
   if (a,seed) not in nlls or (b,seed) not in nlls:paired.append(dict(A=a,B=b,seed=seed,role=role,status='MISSING',delta_M_L=None,delta_overall=None,ML_CI_low=None,ML_CI_high=None,overall_CI_low=None,overall_CI_high=None,practice_gate=None,bootstrap_min_estimable=None));continue
   da=lookup[a,seed]['M_L']-lookup[b,seed]['M_L'];dd=lookup[a,seed]['overall']-lookup[b,seed]['overall'];bs=boot[a,seed][0]-boot[b,seed][0];bo=boot[a,seed][1]-boot[b,seed][1];paired.append(dict(A=a,B=b,seed=seed,role=role,status='COMPLETE',delta_M_L=da,delta_overall=dd,ML_CI_low=np.quantile(bs,.025),ML_CI_high=np.quantile(bs,.975),overall_CI_low=np.quantile(bo,.025),overall_CI_high=np.quantile(bo,.975),practice_gate=bool(da<=-.01 and dd<=.01),bootstrap_min_estimable=int(min(boot[a,seed][2].min(),boot[b,seed][2].min()))))
 csvwrite(ROOT/'tables/paired_outcomes.csv',paired)
 # Per feature and per frequency band retain original TRAIN-defined populations.
 feature_rows=[];bandrows=[];p=stats()['p'];pool=stats()['pool'];edges=np.quantile(p[pool],np.linspace(0,1,6));x=csr(c,True)
 for (name,seed),nll in nlls.items():
  _,f,counts=metrics(nll,c)
  for i in pool:feature_rows.append(dict(condition=name,seed=seed,feature_id=i,TRAIN_p=p[i],is_low=int(i in L),EVAL_hits=int(counts[i]),NLL=f[i] if np.isfinite(f[i]) else None))
  for j in range(5):
   ids=pool[(p[pool]>=edges[j])&(p[pool]<(edges[j+1]) if j<4 else p[pool]<=edges[j+1])];union=np.asarray(x[:,ids].sum(1)).ravel()>0;bandrows.append(dict(condition=name,seed=seed,TRAIN_frequency_band=j,lower=edges[j],upper=edges[j+1],feature_N=len(ids),EVAL_position_N=int(union.sum()),position_NLL=float(nll[union].mean()) if union.any() else None,feature_macro_NLL=float(np.nanmean(f[ids]))))
 csvwrite(ROOT/'tables/per_feature_learning.csv',feature_rows);csvwrite(ROOT/'tables/frequency_band_learning.csv',bandrows)
 # Figure 1: same-grid activation and actual last-layer amplitude; p separate from either.
 if all((ROOT/'cache'/f'profile_{s}.npz').exists() for s in ['train','eval']):
  dat={s:np.load(ROOT/'cache'/f'profile_{s}.npz') for s in ['train','eval']};win={w['split']:w for w in json.load(open(ROOT/'texts/fixed_windows.json'))};maxz=max(np.log1p(d['z']).max() for d in dat.values());maxc=max(np.log1p(d['c']).max() for d in dat.values());fig,axs=plt.subplots(2,3,figsize=(23,12),gridspec_kw={'width_ratios':[2,7,7]})
  for rr,s in enumerate(['train','eval']):
   d=dat[s];ids=d['feature_ids'];axs[rr,0].barh(range(len(ids)),d['p'],color='#477db3');axs[rr,0].set(yticks=range(len(ids)),yticklabels=ids,xscale='log',xlabel='TRAIN hit frequency p (log axis)',title=f'{s.upper()} | {len(ids)} displayed features');axs[rr,0].invert_yaxis()
   for cc,key,mx,title in [(1,'z',maxz,'Shared 14-layer activation z'),(2,'c',maxc,'Layer28 decoder amplitude c')]:
    im=axs[rr,cc].imshow(np.log1p(d[key]).T,aspect='auto',vmin=0,vmax=mx,cmap='magma',interpolation='nearest');axs[rr,cc].set(yticks=range(len(ids)),yticklabels=ids,xticks=range(0,64,4),xticklabels=[f'{k}:{win[s]["raw_tokens"][k][:10]}' for k in range(0,64,4)],xlabel='Window token index : raw token piece',title=title+' | log(1+value)');axs[rr,cc].tick_params(axis='x',rotation=60,labelsize=7);fig.colorbar(im,ax=axs[rr,cc],fraction=.025,label='log1p(z), dictionary activation units' if key=='z' else 'log1p(c), TRAIN normalized residual units')
  fig.suptitle('1 | Fixed source-ordered 64-token windows: frequency, activation and contribution are separate quantities');fig.tight_layout();figsave(fig,'figure1_fixed_activation_profiles','cache/profile_train.npz; cache/profile_eval.npz; texts/fixed_windows.json','Are low features absent or merely competing with larger contributions?')
  rows=list(csv.DictReader(open(ROOT/'tables/conditional_amplitudes.csv')));fig,axs=plt.subplots(1,3,figsize=(16,5))
  for ax,q in zip(axs,['z','c28','a_route']):
   rr=[r for r in rows if r['quantity']==q];bp=[]
   for r in rr:bp.append(dict(label=r['split']+' '+r['group'],med=float(r['median']),q1=float(r['q25']),q3=float(r['q75']),whislo=float(r['q25']),whishi=float(r['q75'])))
   ax.bxp(bp,showfliers=False);ax.set(yscale='log',ylabel=q+' positive-event amplitude (log axis)',title=q+' | median and IQR');ax.tick_params(axis='x',rotation=30)
  fig.suptitle('2 | Conditional positive-event amplitudes | pooled events, not equal-feature distributions');fig.tight_layout();figsave(fig,'figure2_conditional_amplitudes','tables/conditional_amplitudes.csv','Compare conditional amplitudes separately from frequency and sample count')
  rank=list(csv.DictReader(open(ROOT/'tables/low_window_rankings.csv')))
  for s in ['train','eval']:
   ids=[int(i) for i in dat[s]['feature_ids'] if int(i) in set(L)];fig,axs=plt.subplots(2,4,figsize=(20,8));
   for ax,i in zip(axs.ravel(),ids):
    rr=[r for r in rank if r['split']==s and int(r['feature_id'])==i];vals=[float(r['c28']) for r in rr];ax.plot(range(1,65),vals);ax.scatter(range(1,6),vals[:5],color='#d66a43');ax.set(title=f'Feature {i} | TRAIN p={p[i]:.4g}',xlabel='Contribution rank in fixed window',ylabel='Layer28 c (TRAIN normalized residual units)')
   for ax in list(axs.ravel())[len(ids):]:ax.axis('off')
   fig.suptitle(f'3 | {s.upper()}: low-feature contribution ranks | top5 text fragments in source table');fig.tight_layout();figsave(fig,f'figure3_{s}_low_position_ranks','tables/low_window_rankings.csv','Which actual positions supply the displayed low-feature contribution?')
  for s in ['train','eval']:
   fig,axs=plt.subplots(2,4,figsize=(23,8));
   for row,group in enumerate(['T','R11']):
    for sc in range(4):
     d=np.load(ROOT/'routes'/f'{s}_{group}_S{sc}.npz');ix=dat[s]['rows'];im=axs[row,sc].imshow(np.log1p(d['score'][ix].T),aspect='auto',cmap='viridis');axs[row,sc].scatter(range(64),d['route'][ix],s=8,color='white',label='selected expert');axs[row,sc].set(title=f'{group} S{sc} | log(1+score)',xlabel='Same fixed token index',ylabel='Expert ID',yticks=range(8));fig.colorbar(im,ax=axs[row,sc],fraction=.03)
   fig.suptitle(f'4 | {s.upper()}: same inputs, four separate scoring rules | scales differ by definition');fig.tight_layout();figsave(fig,f'figure4_{s}_same_text_scores','tables/fixed_text_score_contributors.csv; routes/*.npz','Does calibrated competition change the selected expert on the same text?')
 # All fixed scores: loads, owner reception, every L target zero statistic.
 summ=[x for x in json.load(open(ROOT/'metrics/routing_summary.json')) if x['split']=='eval'];names=[x['condition'] for x in summ];fig,axs=plt.subplots(1,3,figsize=(19,7));a=np.array([x['load'] for x in summ])/len(c['target'])*100;im=axs[0].imshow(a,aspect='auto',vmin=0,vmax=100,cmap='Blues');axs[0].set(yticks=range(8),yticklabels=names,xticks=range(8),xlabel='Expert ID',title='Actual load (% EVAL positions)');fig.colorbar(im,ax=axs[0],fraction=.04)
 axs[1].barh(names,[100*x['low_receive_macro'] for x in summ]);axs[1].set(xlabel='Feature-macro assigned reception (%)',title='Each low feature: owner hits / all its hits');axs[2].barh(names,[x['low_zero_receive'] for x in summ]);axs[2].set(xlabel='Number of fixed 964 low features',title='Zero assigned reception');fig.suptitle('5 | Receiving targets and balancing expert loads are different outcomes');fig.tight_layout();figsave(fig,'figure5_dispatch_outcomes','metrics/routing_summary.json','Which calibration changes actual target reception, and with what load?')
 # Actual frequency profiles include Top10 unassigned atoms.
 poolord=pool[np.argsort(-p[pool],kind='stable')];fig,axs=plt.subplots(8,1,figsize=(16,18),sharex=True)
 for ax,co in zip(axs,summ):
  d=np.load(ROOT/'metrics/exposure'/f'eval_{co["condition"]}.npz');im=ax.imshow(d['q'][poolord].T,aspect='auto',vmin=0,vmax=1,cmap='magma');ax.set(ylabel=co['condition'],yticks=[0,7]);
 axs[-1].set_xlabel('All 9,615 reliable features ordered by original TRAIN p (including Top10)');fig.suptitle('6 | Actual within-expert frequency q | empty expert rows are NA');fig.subplots_adjust(right=.89,hspace=.2);fig.colorbar(im,cax=fig.add_axes([.92,.3,.015,.4]),label='q = feature hits / actual expert inputs');figsave(fig,'figure6_actual_frequency_profiles','metrics/exposure/eval_*.npz','Did same-frequency lists become same-frequency actual input?')
 # Curves: main fixed comparison, references separately, extensions all shown.
 for group,ns in [('primary',['T_S0','T_S1','R11_S1']),('learned_references',['Learned','LearnedLB']),('expanded_fixed',[f'{g}_S{s}' for g in ['T','R11'] for s in range(4)])]:
  fig,axs=plt.subplots(1,2,figsize=(15,5));
  for ni,n in enumerate(ns):
   for seed in [11,22]:
    rr=sorted([x for x in curves if x['condition']==n and x['seed']==seed],key=lambda x:x['epoch'])
    if not rr:continue
    for ax,met in zip(axs,['overall','M_L']):ax.plot([x['seen'] for x in rr],[x[met] for x in rr],marker='o',ls='-' if seed==11 else '--',color=plt.get_cmap('tab10')(ni),label=f'{n} seed{seed}');ax.set(xlabel='Cumulative valid prediction positions',ylabel='NLL (nat/token)',title=met);ax.grid(alpha=.15)
  axs[1].legend(fontsize=8,bbox_to_anchor=(1.02,1),loc='upper left');fig.suptitle(f'7 | {group} | epoch3 endpoint fixed before training');fig.tight_layout();figsave(fig,'figure7_'+group+'_learning_curves','tables/training_metrics.csv','Does a routing change improve held-out learning, rather than only reception?')
 primary=[x for x in paired if x['role'].startswith('primary') and x['status']=='COMPLETE'];fig,axs=plt.subplots(1,2,figsize=(14,5))
 for ax,key,lo,hi in [(axs[0],'delta_M_L','ML_CI_low','ML_CI_high'),(axs[1],'delta_overall','overall_CI_low','overall_CI_high')]:
  if primary:
   vals=np.array([r[key] for r in primary]);ax.hlines(range(len(primary)),[r[lo] for r in primary],[r[hi] for r in primary]);ax.plot(vals,range(len(primary)),'o');ax.set(yticks=range(len(primary)),yticklabels=[f'{r["A"]} - {r["B"]} / seed{r["seed"]}' for r in primary]);ax.axvline(0,color='#777');ax.axvline(-.01 if key=='delta_M_L' else .01,color='#b66b44',ls='--')
  ax.set(xlabel='NLL difference (nat/token); negative is better',title=key+' | paired context bootstrap 95% interval')
 fig.suptitle('8 | Registered primary paired comparisons | EVAL-context description; document independence unknown');fig.tight_layout();figsave(fig,'figure8_primary_paired_differences','tables/paired_outcomes.csv','Do primary comparisons meet the predeclared .01 practical threshold?')
 # Functional: all arms/seeds retained in sources, primary seed11 figure plus all table.
 probes=[];spectral=[]
 for co in CFG['conditions']:
  for seed in CFG['seeds']:
   pp=ROOT/f'functional/{co["id"]}/seed{seed}'
   if (pp/'expert_probe.csv').exists():probes.extend(list(csv.DictReader(open(pp/'expert_probe.csv'))))
   if (pp/'spectra.csv').exists():spectral.extend(list(csv.DictReader(open(pp/'spectra.csv'))))
 csvwrite(ROOT/'tables/expert_probe.csv',probes);csvwrite(ROOT/'tables/parameter_response_spectra.csv',spectral)
 if probes:
  fig,axs=plt.subplots(1,2,figsize=(15,6));ns=['T_S0','T_S1','R11_S1'];aa=np.array([[float(next(r for r in probes if r['condition']==n and int(r['seed'])==11 and int(r['expert'])==e)['force_NLL']) for e in range(8)] for n in ns]);im=axs[0].imshow(aa,aspect='auto',cmap='viridis');axs[0].set(yticks=range(3),yticklabels=ns,xticks=range(8),xlabel='Forced expert ID (gate1)',title='Same probe inputs: absolute forced NLL');fig.colorbar(im,ax=axs[0]);
  for n in ns:
   rr=sorted([r for r in probes if r['condition']==n and int(r['seed'])==11],key=lambda r:int(r['expert']));axs[1].plot(range(8),[float(r['swap_preserve_natural_gate_delta']) for r in rr],marker='o',label=n)
  axs[1].set(xlabel='Replacement expert ID',ylabel='NLL replacement - natural (nat/token)',title='Preserve original natural gate multiplier');axs[1].axhline(0,color='#777');axs[1].legend();fig.suptitle('9 | Same-input expert probes | seed11 primary arms; IDs across strategies are not functional matches');fig.tight_layout();figsave(fig,'figure9_same_input_expert_probes','tables/expert_probe.csv; functional/*/probe.npz','Do experts produce different outputs/losses on identical inputs?')
 # Target held-out update.
 targets=[]
 for e in range(8):
  pp=ROOT/f'target/adapt/expert{e}/new_input_assignment.csv'
  if pp.exists():targets.extend(list(csv.DictReader(open(pp))))
 csvwrite(ROOT/'tables/new_input_assignment.csv',targets)
 if targets:
  finals=[r for r in targets if int(r['step'])==32];safe=sorted([r for r in finals if float(r['B_old_cost'])<=.01],key=lambda r:(float(r['C_absolute_NLL']),int(r['expert'])));write_json(ROOT/'target/oracle_ranking.json',dict(safe_absolute_NLL_experts=[int(r['expert']) for r in safe],gain_ranking_experts=[int(r['expert']) for r in sorted(finals,key=lambda r:(-float(r['gain_before_minus_after']),int(r['expert'])))],retrospective_oracle=True))
  fig,axs=plt.subplots(1,2,figsize=(14,5));rec=json.load(open(ROOT/'target/recommendations.json'))
  for r in finals:
   e=int(r['expert']);gain=float(r['gain_before_minus_after']);cost=float(r['B_old_cost']);axs[0].scatter(gain,cost);axs[0].annotate(str(e),(gain,cost),xytext=(4,4),textcoords='offset points');rr=sorted([q for q in targets if int(q['expert'])==e],key=lambda q:int(q['step']));axs[1].plot([int(q['step']) for q in rr],[float(q['C_absolute_NLL']) for q in rr],marker='o',label=f'expert{e}')
  axs[0].axhline(.01,ls='--',color='#b65b42');axs[0].set(xlabel='C_eval improvement: before - after (nat/token)',ylabel='B_eval old cost: after - before (nat/token)',title='All 8 matched adaptations | 32 steps');axs[1].set(xlabel='Matched target updates',ylabel='Absolute C_eval NLL (nat/token)',title='Starting difficulty and final performance both shown');axs[1].legend(ncol=2,fontsize=8,bbox_to_anchor=(1,1));fig.suptitle(f'10 | Target feature {rec["target_feature"]} | recommendations list/route/prediction={rec["list_recommendation"]}/{rec["actual_route_recommendation"]}/{rec["current_prediction_recommendation"]}');fig.tight_layout();figsave(fig,'figure10_target_assignment','tables/new_input_assignment.csv; target/recommendations.json','Does pre-update attribution predict safe adaptation with low absolute target NLL?')
 if spectral:
  fig,axs=plt.subplots(3,3,figsize=(17,13));
  for cc,nm in enumerate(['gate','up','down']):
   for n in ['T_S0','T_S1','R11_S1']:
    for rr,version in enumerate(['initial','final','delta']):
     rows=[r for r in spectral if r['condition']==n and r['seed']=='11' and r['matrix']==f'W_{nm}' and r['version']==version];vals=[np.array(r['top16_singular_values'].split(';'),float) for r in rows]
     if vals:axs[rr,cc].plot(range(1,17),np.median(vals,axis=0),label=n)
     axs[rr,cc].set(title=f'W_{nm} {version} | median over 8 experts',xlabel='Singular index',ylabel='Absolute singular value')
  axs[0,2].legend();fig.suptitle('11 | Parameter spectra are auxiliary geometry, not capacity or function evidence');fig.tight_layout();figsave(fig,'figure11_parameter_spectra','tables/parameter_response_spectra.csv; functional/*/full_spectra.npz','Separate original weight geometry from parameter changes')

 if spectral:
  ns=[co['id'] for co in CFG['conditions']];fig,axs=plt.subplots(1,3,figsize=(20,6))
  for ci,n in enumerate(ns):
   vals=[];energy=[];norm=[]
   for seed in [11,22]:
    pp=ROOT/f'functional/{n}/seed{seed}/full_spectra.npz'
    if not pp.exists():continue
    d=np.load(pp)
    for e in range(8):
     ev=d[f'e{e}_response_centered_covariance_eigenvalues'];vals.append(ev[:16]);energy.append(ev.sum());norm.append(ev[:16]/ev.sum() if ev.sum()>0 else np.full(16,np.nan))
   if vals:
    axs[0].plot(range(1,17),np.median(vals,axis=0),label=n);axs[1].plot(range(1,17),np.nanmedian(norm,axis=0),label=n);axs[2].scatter(np.full(len(energy),ci),energy,s=14,alpha=.6)
  axs[0].set(xlabel='Covariance eigenvalue index',ylabel='Absolute eigenvalue',title='Median over experts/seeds; same probe')
  axs[1].set(xlabel='Covariance eigenvalue index',ylabel='Eigenvalue / FULL trace',title='Shape separate from total amplitude')
  axs[2].set(xticks=range(len(ns)),xticklabels=ns,ylabel='Centered response covariance trace',title='All expert energies, no ID matching');axs[2].tick_params(axis='x',rotation=60);axs[0].legend(fontsize=7)
  fig.suptitle('12 | Response spectra: centered across fixed input rows, uniform weights | no capacity inference');fig.tight_layout();figsave(fig,'figure12_response_spectra','functional/*/seed*/full_spectra.npz','Separate response amplitude, shape and functional evidence')
 write_json(ROOT/'provenance/figures_manifest.json',FIGS);write_json(ROOT/'provenance/analysis_receipt.json',dict(status='COMPLETE',seconds=time.monotonic()-t0,endpoints=sum(x['status']=='COMPLETE' for x in ends),all_planned=20,paired_rows=len(paired),figures=len(FIGS)//3,bootstrap=1000,bootstrap_unit='EVAL original context block',document_independence='UNKNOWN'))
if __name__=='__main__':run()
