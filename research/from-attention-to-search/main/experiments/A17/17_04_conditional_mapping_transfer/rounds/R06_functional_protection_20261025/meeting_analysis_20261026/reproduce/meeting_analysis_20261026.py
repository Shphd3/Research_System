"""Read-only analysis of36existing runs; no model import, training or TEST."""
from pathlib import Path
import json,csv,hashlib,math,datetime,statistics,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
E=Path(__file__).resolve().parents[1];O=E/'analysis/meeting_20261026';T=O/'tables';G=O/'figures';V=O/'provenance'
C=json.load(open(E/'config/frozen.json'));CONDITIONS=[('U',0),('F',0),('U',4),('F',4)];SEEDS=[29,43,71];METHODS=['U','S','F','D'];K=[0,4,36]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False,default=lambda z:z.item() if isinstance(z,np.generic) else str(z))+'\n')
def dump(name,rows):
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (T/name).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def table(rows,cols):
 def fmt(v):return f'{v:.3f}' if isinstance(v,float) else str(v)
 return '\n'.join(['| '+' | '.join(n for k,n in cols)+' |','| '+' | '.join('---' for _ in cols)+' |']+['| '+' | '.join(fmt(r.get(k,'MISSING')) for k,n in cols)+' |' for r in rows])
def source(path):
 p=Path(path);return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
def load_eval(p):
 a=read(p)
 if 'records' not in a:
  b=read(a['shared_source']);assert b['aggregates']==a['aggregates'];a['records']=b['records']
 return a

def main():
 sources=[];endpoints=[];contrast=[];countercheck=[];metrics={};evals={};curves=[];operating=[];checks=[]
 devpath=Path(C['data'])/'dev.jsonl';assert sha(devpath)==C['data_file_sha256']['dev.jsonl'];sources.append(source(devpath))
 dev=[json.loads(x) for x in devpath.read_text().splitlines()];meta={r['record_id']:r for r in dev if r['world'] in ['old','reversed']};wordids=dict(zip(C['answer_words'],C['answer_ids']));idwords={v:k for k,v in wordids.items()}
 for r in meta.values():
  want=r['first_id'] if ((r['command']=='甲') != (r['world']=='reversed')) else r['last_id']
  assert r['target_id']==want and len({r['first_id'],r['middle_id'],r['last_id']})==3
 sources+=list(map(source,[E/'config/frozen.json',E/'source/engine.py',Path(C['data']).parents[1]/'source/generate.py']))
 for s in SEEDS:
  for k in K:
   for m in METHODS:
    case=E/'runs'/f'seed_{s}'/f'old_{k:02}'/m;ident={'seed':s,'old_slots':k,'method':m};comp=read(case/'completion.json');assert comp['status']=='DONE_EXPLORATORY' and comp['steps']==240
    ms=[json.loads(x) for x in (case/'metrics.jsonl').read_text().splitlines()];metrics[s,k,m]=ms;assert len(ms)==240
    sources.extend(map(source,[case/'metrics.jsonl',case/'completion.json',case/'scope.json']))
    scope=read(case/'scope.json');countercheck.append({**ident,'new_targets':comp['counters']['new_targets'],'old_active_targets':comp['counters']['old_active_targets'],'old_probe_gradient_targets':comp['counters']['old_probe_targets'],'old_probe_diagnostic_targets':640,'new_per_record_loss_coefficient':1/72,'new_mean_loss_coefficient':.5,'denominator':72,'orders_sha256':scope['orders_sha256']})
    for t,x in enumerate(ms,1):
     assert x['step']==t and x['counters']['new_targets']==36*t and x['counters']['old_active_targets']==k*t
     assert abs(x['new_weighted']-.5*x['new_train_ce'])<1e-6
     assert abs(x['old_weighted']-x['old_active_train_ce']*k/72)<1e-6
    for step in C['eval_steps']:
     path=case/f'eval_{step:06}.json';a=load_eval(path);evals[s,k,m,step]=a;sources.append(source(path))
     rr=a['records'];assert len(rr)==1600
     row={**ident,'step':step,'new_targets':36*step}
     for mode,label in [(1,'old'),(2,'new')]:
      r=[z for z in rr if z['mode']==mode];assert len(r)==800
      acc=sum(z['correct'] for z in r)/8;ce=sum(z['ce'] for z in r)/800
      assert math.isclose(acc,100*a['aggregates'][f'mode{mode}/both/combined']['accuracy'],abs_tol=1e-10)
      assert math.isclose(ce,a['aggregates'][f'mode{mode}/both/combined']['ce'],abs_tol=1e-10)
      row[label+'_accuracy_pct']=acc;row[label+'_ce_nats']=ce
     curves.append(row)
     if step==240:endpoints.append(row)
    ev=[r for r in curves if r['seed']==s and r['old_slots']==k and r['method']==m]
    for x,y in zip(ev,ev[1:]):
     if x['new_accuracy_pct']>=90 and y['new_accuracy_pct']>=90:
      operating.append({**y,'first_of_confirming_pair_step':x['step'],'criterion':'second of consecutive scheduled new accuracy>=90%; no interpolation','status':'REACHED','probe_gradient_labels':64*y['step'],'old_objective_labels':k*y['step'],'update_compute_seconds':sum(z['update_seconds'] for z in ms[:y['step']])});break
    else:operating.append({**ident,'status':'NOT_REACHED'})
 ix={(r['seed'],r['old_slots'],r['method']):r for r in endpoints}
 for s in SEEDS:
  for k in K:
   for m in ['F','S','D']:
    a=ix[s,k,m];b=ix[s,k,'U'];contrast.append({'seed':s,'old_slots':k,'comparison':m+'-U',**{n:a[n]-b[n] for n in ['old_accuracy_pct','new_accuracy_pct','old_ce_nats','new_ce_nats']}})
 for s in SEEDS:assert len({r['orders_sha256'] for r in countercheck if r['seed']==s})==1
 means=[];contrmean=[]
 for k in K:
  for m in METHODS:
   rs=[ix[s,k,m] for s in SEEDS];means.append({'old_slots':k,'method':m,**{q:statistics.mean(r[q] for r in rs) for q in ['old_accuracy_pct','new_accuracy_pct','old_ce_nats','new_ce_nats']}})
  for m in ['F','S','D']:
   rs=[r for r in contrast if r['old_slots']==k and r['comparison']==m+'-U'];contrmean.append({'old_slots':k,'comparison':m+'-U',**{q:statistics.mean(r[q] for r in rs) for q in ['old_accuracy_pct','new_accuracy_pct','old_ce_nats','new_ce_nats']},'old_positive_seeds':sum(r['old_accuracy_pct']>0 for r in rs),'old_negative_seeds':sum(r['old_accuracy_pct']<0 for r in rs)})
 dump('01_endpoints_36.csv',endpoints);dump('01_method_means_12.csv',means);dump('01_all_vs_U_seed_27.csv',contrast);dump('01_all_vs_U_means_9.csv',contrmean);dump('01_exposure_36.csv',countercheck);dump('01_curves_396.csv',curves);dump('01_operating90_36.csv',operating)
 # Analysis2: exclusive rule-choice errors and explicit paired mode behaviors.
 individual=[];behavior=[];samplecandidates=[]
 for s in SEEDS:
  for m,k in CONDITIONS:
   for step in C['eval_steps']:
    a=evals[s,k,m,step];groups={}
    for z in a['records']:groups.setdefault((z['list_id'],z['command']),{})[z['mode']]=z
    assert len(groups)==800 and all(set(x)=={1,2} for x in groups.values())
    items=[]
    for key,pair in sorted(groups.items()):
     old,new=pair[1],pair[2];om=meta[old['record_id']];nm=meta[new['record_id']]
     assert om['list_id']==nm['list_id'] and om['words']==nm['words'] and om['command']==nm['command']
     assert old['target_id']==om['target_id'] and new['target_id']==nm['target_id']
     samegold=old['target_id']==new['target_id'];pred=old['prediction_id'];valid=isinstance(pred,int) and 0<=pred<151936
     if samegold:category='same_target_excluded'
     elif pred==old['target_id']:category='old_rule_correct'
     elif pred==new['target_id']:category='new_rule_endpoint'
     elif pred in [om['first_id'],om['middle_id'],om['last_id']]:category='other_list_item'
     else:category='other_output_or_invalid'
     d={'seed':s,'method':m,'old_slots':k,'step':step,'panel':old['panel'],'command':old['command'],'list_id':old['list_id'],'record_id':old['record_id'],'same_target_excluded':samegold,'category':category,'old_correct':old['correct'],'new_correct':new['correct'],'both_correct':int(old['correct'] and new['correct']),'same_prediction':int(pred==new['prediction_id']),'old_selects_new_rule':int(not samegold and pred==new['target_id']),'old_prediction_id':pred,'new_prediction_id':new['prediction_id'],'old_target_id':old['target_id'],'new_target_id':new['target_id'],'old_ce':old['ce'],'new_ce':new['ce'],'other_output_valid_single_token':valid}
     items.append(d);individual.append(d)
     if step==240:samplecandidates.append({**d,'old_prefix':om['prefix'],'new_prefix':nm['prefix'],'old_target_word':idwords.get(old['target_id'],str(old['target_id'])),'new_target_word':idwords.get(new['target_id'],str(new['target_id'])),'old_prediction_word':idwords.get(pred,str(pred)),'new_prediction_word':idwords.get(new['prediction_id'],str(new['prediction_id']))})
    for panel in ['combined','order_new','combination_new']:
     for cmd in ['both','甲','乙']:
      rs=[r for r in items if (panel=='combined' or r['panel']==panel) and (cmd=='both' or r['command']==cmd)];n=len(rs);ex=sum(r['same_target_excluded'] for r in rs);eligible=n-ex
      counts=collections.Counter(r['category'] for r in rs)
      assert sum(counts.values())==n
      behavior.append({'seed':s,'method':m,'old_slots':k,'step':step,'panel':panel,'command':cmd,'pair_n':n,'same_target_excluded_n':ex,'rule_confusion_denominator':eligible,
       **{q+'_n':counts[q] for q in ['old_rule_correct','new_rule_endpoint','other_list_item','other_output_or_invalid']},
       **{q+'_pct':100*counts[q]/eligible if eligible else None for q in ['old_rule_correct','new_rule_endpoint','other_list_item','other_output_or_invalid']},
       'both_correct_n':sum(r['both_correct'] for r in rs),'both_correct_pct':100*sum(r['both_correct'] for r in rs)/n,'same_prediction_n':sum(r['same_prediction'] for r in rs),'same_prediction_pct':100*sum(r['same_prediction'] for r in rs)/n,
       'old_selects_new_rule_pct':100*sum(r['old_selects_new_rule'] for r in rs)/eligible if eligible else None,
       'invalid_token_ID_n':sum(not r['other_output_valid_single_token'] for r in rs),'format_boundary':'single argmax token; no free-form syntax to assess'})
 endpointbehavior=[r for r in behavior if r['step']==240 and r['panel']=='combined' and r['command']=='both'];bmeans=[]
 for m,k in CONDITIONS:
  rs=[r for r in endpointbehavior if r['method']==m and r['old_slots']==k]
  bmeans.append({'method':m,'old_slots':k,'n_orders':3,'old_questions_each':800,'same_target_excluded_total':sum(r['same_target_excluded_n'] for r in rs),**{q:statistics.mean(r[q] for r in rs) for q in ['old_rule_correct_pct','new_rule_endpoint_pct','other_list_item_pct','other_output_or_invalid_pct','both_correct_pct','same_prediction_pct']}})
 dump('02_rule_mode_stats_all.csv',behavior);dump('02_rule_mode_endpoint_seed12.csv',endpointbehavior);dump('02_rule_mode_endpoint_mean4.csv',bmeans)
 # Per-item output records remain execution-side, not indiscriminately copied to Git.
 dump('02_rule_mode_pairs_105600.csv',individual)
 # Fixed illustrative examples: lowest record_id within each requested category/seed,
 # with a matched U4 comparison. Selection is posthoc illustration, not inference.
 samples=[]
 for s in SEEDS:
  f0=[r for r in samplecandidates if r['seed']==s and r['method']=='U' and r['old_slots']==0 and r['category']=='new_rule_endpoint' and r['new_correct']]
  f4=[r for r in samplecandidates if r['seed']==s and r['method']=='F' and r['old_slots']==4 and r['category']=='new_rule_endpoint' and r['new_correct']]
  for label,rs in [('U0_wrong_to_new',f0),('F4_wrong_to_new',f4)]:
   if rs:
    a=sorted(rs,key=lambda r:r['record_id'])[0]
    matches=[r for r in samplecandidates if r['seed']==s and r['record_id']==a['record_id']]
    samples.append({'selection':'posthoc lowest record_id in observed category; illustrative only','label':label,'pair_conditions':matches})
 write(O/'real_paired_examples.json',samples)
 # Analysis3: ideal vs final FP32 displacement. Audit tolerance is descriptive.
 numerics=[];ngroups=[];fp64eps=np.finfo(np.float64).eps;numel=6291456
 gamma=(numel*fp64eps)/(1-numel*fp64eps)
 for s in SEEDS:
  for k in K:
   for m in METHODS:
    for x in metrics[s,k,m]:
     if 'probe_loss_change' not in x:continue
     tau0=max(1e-10,abs(x['g_dot_candidate'])*1e-5)
     roundbound=math.sqrt(x['probe_g2'])*x['filter_roundoff_norm']
     reductionbound=gamma*math.sqrt(x['probe_g2'])*x['actual_norm'];tau=tau0+roundbound+reductionbound
     delta=x['probe_loss_change'];pred=x['g_dot_actual'];rem=x['first_order_remainder']
     assert math.isclose(delta,x['probe_loss_after']-x['probe_loss_before'],abs_tol=1e-14)
     assert math.isclose(rem,delta-pred,abs_tol=1e-14)
     assert abs(x['g_dot_actual']-x['g_dot_desired'])<=roundbound+reductionbound+1e-12
     if m=='F':assert x['g_dot_desired']<=tau0
     numerics.append({'seed':s,'old_slots':k,'method':m,'step':x['step'],'g2':x['probe_g2'],'gradient_floor_trigger':x['gradient_floor'],'projection_trigger':x['projection_needed'],
       'g_dot_before':x['g_dot_candidate'],'g_dot_ideal_after':x['g_dot_desired'],'g_dot_final_actual':pred,'ideal_audit_tolerance':tau0,'roundoff_Cauchy_bound':roundbound,'fp64_reduction_bound':reductionbound,'final_actual_tolerance':tau,
       'ideal_nonpositive_within_tolerance':x['g_dot_desired']<=tau0,'final_raw_positive':pred>0,'final_positive_beyond_tolerance':pred>tau,'candidate_displacement_norm':x['candidate_norm'],'ideal_displacement_norm':x['desired_norm'],'actual_displacement_norm':x['actual_norm'],'roundoff_displacement_norm':x['filter_roundoff_norm'],
       'probe_loss_before':x['probe_loss_before'],'probe_loss_after':x['probe_loss_after'],'actual_loss_change':delta,'raw_loss_increase':delta>0,'finite_remainder':rem,'remainder_larger_than_prediction_tolerance':rem>tau,'loss_precision_calibration':'NOT_SAVED no repeated/no-op empirical loss-noise calibration; raw signs not significance tests'})
 for m in METHODS:
  for k in K:
   rs=[r for r in numerics if r['method']==m and r['old_slots']==k]
   ngroups.append({'method':m,'old_slots':k,'checks':len(rs),'raw_actual_loss_increase_n':sum(r['raw_loss_increase'] for r in rs),'raw_positive_final_dot_n':sum(r['final_raw_positive'] for r in rs),'positive_final_dot_beyond_tolerance_n':sum(r['final_positive_beyond_tolerance'] for r in rs),'projection_trigger_n':sum(r['projection_trigger'] for r in rs),'gradient_floor_n':sum(r['gradient_floor_trigger'] for r in rs),
     'mean_actual_loss_change':statistics.mean(r['actual_loss_change'] for r in rs),'median_actual_loss_change':statistics.median(r['actual_loss_change'] for r in rs),'max_actual_loss_change':max(r['actual_loss_change'] for r in rs),'max_actual_dot':max(r['g_dot_final_actual'] for r in rs),'max_final_tolerance':max(r['final_actual_tolerance'] for r in rs),
     'max_remainder':max(r['finite_remainder'] for r in rs),'positive_remainder_beyond_prediction_tolerance_n':sum(r['remainder_larger_than_prediction_tolerance'] for r in rs)})
 dump('03_all_finite_checks_360.csv',numerics);dump('03_F_finite_checks_90.csv',[r for r in numerics if r['method']=='F']);dump('03_finite_check_summary_12.csv',ngroups)
 nonfinite=[]
 for s in SEEDS:
  for k in K:
   ms=metrics[s,k,'F'];nonfinite.append({'seed':s,'old_slots':k,'all_steps':240,'projection_trigger_steps':sum(x['projection_needed'] for x in ms),'gradient_floor_steps':sum(x['gradient_floor'] for x in ms),'zero_candidate_steps':sum(x['zero_candidate'] for x in ms),'final_dot_positive_beyond_roundoff_tolerance_steps':sum(x['g_dot_actual']>max(1e-10,abs(x['g_dot_candidate'])*1e-5)+math.sqrt(x['probe_g2'])*x['filter_roundoff_norm']+gamma*math.sqrt(x['probe_g2'])*x['actual_norm'] for x in ms),
      'probe_pre_loss_first':ms[0]['probe_loss'],'probe_pre_loss_last':ms[-1]['probe_loss'],'probe_comparison_boundary':'different sampled batches at different steps, NOT one persistent loss trajectory'})
 dump('03_F_all_step_constraint_summary_9.csv',nonfinite)
 # Three main plots with independent units; narrative belongs in external captions.
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
 color={'U':'#333333','S':'#0072B2','F':'#D55E00','D':'#009E73'};marker={'U':'o','S':'s','F':'^','D':'D'}
 def savefig(fig,name):
  for ext in ['png','svg','pdf']:fig.savefig(G/(name+'.'+ext),dpi=280,bbox_inches='tight')
  plt.close(fig)
 fig,axs=plt.subplots(1,2,figsize=(9,3.5))
 for ax,task in zip(axs,['old','new']):
  for m in METHODS:
   rr=[next(r for r in means if r['method']==m and r['old_slots']==k) for k in K]
   ax.plot(range(3),[r[task+'_accuracy_pct'] for r in rr],label=m,color=color[m],marker=marker[m],ms=6)
  ax.set_xticks(range(3),['0:1','1:9','1:1']);ax.set_ylim(-1,101);ax.set_xlabel('Old:new objective supervision ratio');ax.set_ylabel(('Old A' if task=='old' else 'New B')+' accuracy (%)');ax.grid(alpha=.18)
 axs[1].legend(ncol=4,loc='lower center',frameon=False);fig.tight_layout();savefig(fig,'figure1_supervision_methods')
 fig,axs=plt.subplots(1,2,figsize=(10,3.9));xs=np.arange(4);labels=['U 0:1','F 0:1','U 1:9','F 1:9'];base=np.zeros(4)
 cats=['old_rule_correct_pct','new_rule_endpoint_pct','other_list_item_pct','other_output_or_invalid_pct'];cl=['#009E73','#D55E00','#E69F00','#777777'];names=['Old rule correct','New-rule endpoint','Other list item','Other/invalid token']
 for cat,col,lab in zip(cats,cl,names):
  vals=[r[cat] for r in bmeans];axs[0].bar(xs,vals,bottom=base,color=col,label=lab);base+=vals
 axs[0].set_xticks(xs,labels);axs[0].set_ylim(0,101);axs[0].set_ylabel('Old-mode answers (%)');axs[0].legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.14),ncol=2,frameon=False)
 for off,key,col,lab in [(-.19,'both_correct_pct','#0072B2','Both modes correct'),(.19,'same_prediction_pct','#CC79A7','Same answer across modes')]:axs[1].bar(xs+off,[r[key] for r in bmeans],width=.36,color=col,label=lab)
 axs[1].set_xticks(xs,labels);axs[1].set_ylim(0,101);axs[1].set_ylabel('Matched mode pairs (%)');axs[1].legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.14),frameon=False)
 for ax in axs:ax.grid(axis='y',alpha=.15)
 fig.tight_layout();savefig(fig,'figure2_rule_confusion')
 fig,axs=plt.subplots(1,2,figsize=(9,3.6));fs=[r for r in numerics if r['method']=='F'];kcols={0:'#D55E00',4:'#0072B2',36:'#009E73'}
 for k in K:
  rr=[r for r in fs if r['old_slots']==k];axs[0].scatter([r['g_dot_final_actual'] for r in rr],[r['actual_loss_change'] for r in rr],s=23,color=kcols[k],alpha=.7,label=f'Old slots {k}')
 axs[0].set_xscale('symlog',linthresh=1e-8);axs[0].set_yscale('symlog',linthresh=1e-4);axs[0].axhline(0,color='grey',lw=.7);axs[0].axvline(0,color='grey',lw=.7);axs[0].set_xlabel('Final first-order prediction (nat/answer)');axs[0].set_ylabel('Actual old-probe loss change (nat/answer)');axs[0].legend(fontsize=8,frameon=False)
 # Explicit comparison to rounding-aware tolerances separates raw tiny positives.
 ratio=[r['g_dot_final_actual']/r['final_actual_tolerance'] for r in fs]
 axs[1].scatter(range(1,91),ratio,s=18,c=[kcols[r['old_slots']] for r in fs]);axs[1].axhline(0,color='grey',lw=.7);axs[1].axhline(1,color='black',ls='--',lw=.9);axs[1].set_ylim(min(-1.2,min(ratio)*1.05),1.2);axs[1].set_yscale('symlog',linthresh=1);axs[1].set_xlabel('Saved F check index (seed, ratio, step order)');axs[1].set_ylabel('Final prediction / numerical tolerance')
 for ax in axs:ax.grid(alpha=.15)
 fig.tight_layout();savefig(fig,'figure3_first_order_finite_loss')
 dump('figure1_data.csv',means);dump('figure2_data.csv',bmeans);dump('figure3_data.csv',fs)
 # Source audit records exact object equality; do not claim an empirical noise experiment.
 engine=(E/'source/engine.py').read_text();source_audit={'same_probe_records':'take_grad(...order[probe]) and probe_loss(...order[probe]) within same update; frozen orders identify64records','same_loss':'both return sum answer CE /64, probe_microbatch16; before from gradient pass, after from no_grad pass','same_parameter_start':'g and before loss computed before objective backward/Adam; backward/clip do not change parameters; initial parameter clones immediately before opt.step','final_displacement':'actual=p-before after post-Adam filter and FP32copy; dot and loss after that final copy; no further optimizer clipping/weight decay after this','deterministic_mode':'QwenCarrier.eval().requires_grad_(False), selectedweights requires_grad True, CachedAnswerLM uses the eval child layers; no .train() call; r05.configure deterministic algorithms, FP32 noTF32','precision_limit':'gradient pass and no_grad pass may use different backend kernels; empirical same-state no-op/repeat loss noise NOT SAVED; available rounding bounds quantify parameter-copy contribution only','source_sha256':sha(E/'source/engine.py'),'source_locations':{needle:i+1 for i,line in enumerate(engine.splitlines()) for needle in ['def take_grad','def probe_loss','def update','d=[p-w','actual=[p-w','g_dot_actual','after=probe_loss'] if needle in line}}
 write(V/'03_measurement_object_audit.json',source_audit)
 # Save source-derived facts and numerical outcomes before deciding an optional forward.
 summary={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed_runs':36,'same_new_targets_each':8640,'new_coefficient':.5,'all_versus_U_means':contrmean,'behavior_endpoint_means':bmeans,'behavior_endpoint_seeds':endpointbehavior,'F_finite_checks':90,'F_raw_loss_increases':sum(r['raw_loss_increase'] for r in fs),'F_final_positive_beyond_tolerance':sum(r['final_positive_beyond_tolerance'] for r in fs),'F_raw_positive_final_dots':sum(r['final_raw_positive'] for r in fs),'numeric_summary':ngroups,'same_target_excluded':sum(r['same_target_excluded_n'] for r in endpointbehavior),'TEST_opened':False,'new_forward_sequences':0,'new_training_updates':0}
 write(O/'results.json',summary);write(V/'source_manifest.json',{'files':sources,'analysis_script':source(__file__),'raw_results_not_modified':True})
 print(json.dumps({k:summary[k] for k in ['completed_runs','behavior_endpoint_means','F_raw_loss_increases','F_raw_positive_final_dots','F_final_positive_beyond_tolerance']},ensure_ascii=False,default=lambda z:z.item() if isinstance(z,np.generic) else str(z)))
if __name__=='__main__':main()
