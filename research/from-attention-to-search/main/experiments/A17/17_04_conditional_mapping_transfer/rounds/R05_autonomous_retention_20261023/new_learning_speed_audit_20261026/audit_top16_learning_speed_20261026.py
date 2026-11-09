"""Supplementary existing-results audit: no training, inference, TEST or checkpoint load."""
from pathlib import Path
import json,csv,hashlib,math,statistics,datetime
E=Path(__file__).resolve().parents[1];O=E/'analysis/A_top16_new_learning_audit_20261026';O.mkdir(exist_ok=True)
S=Path('/data/250010109/Research_System');R=S/'Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023';D=R/'new_learning_speed_audit_20261026';D.mkdir(exist_ok=True)
E6=Path('/data/250010109/MoE_Router/experiments/20261025_a17_functional_protection');R6=S/'Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025'
SEEDS=[29,43,71];ARMS=['U','UL','US','TC','TS','RS','LS'];POINTS=[0,1,16,50,120,240,600,1200]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def dump(name,rs):
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rs[0]));w.writeheader();w.writerows(rs)
def table(rs,cols):
 def fmt(x):return f'{x:.6f}' if isinstance(x,float) else str(x)
 return '\n'.join(['| '+' | '.join(n for k,n in cols)+' |','| '+' | '.join('---' for _ in cols)+' |']+['| '+' | '.join(fmt(r.get(k,'MISSING')) for k,n in cols)+' |' for r in rs])
def main():
 sources=[];curves=[];thresholds=[];endpoints=[];timing=[];eq=[]
 rules={'original_new_four_cells95':lambda r:r['new_min_cell_pct']>=95,
        'posthoc_new_mean90':lambda r:r['new_accuracy_pct']>=90,
        'posthoc_new_mean95':lambda r:r['new_accuracy_pct']>=95,
        'posthoc_new_mean99':lambda r:r['new_accuracy_pct']>=99,
        'posthoc_new_mean99p5':lambda r:r['new_accuracy_pct']>=99.5}
 for seed in SEEDS:
  order_ref=None
  for arm in ARMS:
   case=E/'runs/A'/f'seed_{seed}'/arm
   ms=[json.loads(s) for s in (case/'metrics.jsonl').read_text().splitlines()];completion=read(case/'completion.json');assert len(ms)==1200 and completion['new_answers']==24000 and completion['old_answers']==0
   order=[x['batch_record_ids'] for x in ms]
   if order_ref is None:order_ref=order
   assert order==order_ref
   assert all(x['valid_answers']==20 and x['new_valid_answers']==20 and x['old_valid_answers']==0 and x['step']==i+1 for i,x in enumerate(ms))
   sums=[0.]
   for m in ms:sums.append(sums[-1]+m['update_compute_seconds'])
   rr=[]
   for step in POINTS:
    p=case/f'eval_{step:05}.json';a=read(p);sources.append({'path':str(p),'sha256':sha(p)})
    records=a['records'];n=[r for r in records if r['mode']==2];old=[r for r in records if r['mode']==1];assert len(n)==len(old)==800
    cells={k:v for k,v in a['qualification_cells'].items() if k.startswith('mode2/')};assert len(cells)==4
    acc=sum(r['correct'] for r in n)/8;ce=sum(r['ce'] for r in n)/800
    assert math.isclose(acc,a['aggregates']['mode2/both/combined']['correct']*100,abs_tol=1e-10)
    row={'seed':seed,'arm':arm,'step':step,'new_targets':20*step,'new_accuracy_pct':acc,'new_ce_nats':ce,'new_min_cell_pct':100*min(cells.values()),'old_accuracy_pct':sum(r['correct'] for r in old)/8,'update_compute_seconds_to_point':sums[step]}
    rr.append(row);curves.append(row)
    if step==1200:endpoints.append(row)
   for name,fn in rules.items():
    hit=next((i for i,r in enumerate(rr) if fn(r)),None);twice=next((i for i in range(1,len(rr)) if fn(rr[i-1]) and fn(rr[i])),None)
    row={'seed':seed,'arm':arm,'criterion':name,'first_saved_step':rr[hit]['step'] if hit is not None else 'NOT_REACHED','first_saved_new_targets':rr[hit]['new_targets'] if hit is not None else 'NOT_REACHED','previous_saved_step':rr[hit-1]['step'] if hit is not None and hit>0 else None,'second_consecutive_saved_step':rr[twice]['step'] if twice is not None else 'NOT_REACHED','first_hit_update_compute_seconds':rr[hit]['update_compute_seconds_to_point'] if hit is not None else None,'first_hit_new_accuracy_pct':rr[hit]['new_accuracy_pct'] if hit is not None else None,'first_hit_new_ce':rr[hit]['new_ce_nats'] if hit is not None else None};thresholds.append(row)
   timing.append({'seed':seed,'arm':arm,'steps':1200,'new_targets':24000,'recorded_update_seconds':sums[-1],'recorded_total_elapsed_seconds':completion['elapsed_seconds'],'timing_boundary':'descriptive original-job timings; concurrent workers/GPU load, startup/eval/IO differ; not controlled end-to-end speed benchmark'})
   sources.extend([{'path':str(case/p),'sha256':sha(case/p)} for p in ['metrics.jsonl','completion.json']])
 ix={(r['seed'],r['arm']):r for r in endpoints};tx={(r['seed'],r['arm'],r['criterion']):r for r in thresholds}
 primary=[];means=[];contrasts=[]
 for seed in SEEDS:
  for arm in ['U','TC','TS']:
   r=ix[seed,arm];a=tx[seed,arm,'original_new_four_cells95']
   primary.append({**r,'first_original_qualified_step':a['first_saved_step'],'first_original_qualified_new_targets':a['first_saved_new_targets'],'second_original_qualified_step':a['second_consecutive_saved_step']})
  for arm in ['TC','TS']:
   r=ix[seed,arm];u=ix[seed,'U'];contrasts.append({'seed':seed,'arm_minus_U':arm+'-U','new_accuracy_difference_pp':r['new_accuracy_pct']-u['new_accuracy_pct'],'new_CE_difference':r['new_ce_nats']-u['new_ce_nats'],'original_qualified_step_difference':tx[seed,arm,'original_new_four_cells95']['first_saved_step']-tx[seed,'U','original_new_four_cells95']['first_saved_step']})
 for arm in ARMS:
  rs=[r for r in endpoints if r['arm']==arm];means.append({'arm':arm,'new_accuracy_mean_pct':statistics.mean(r['new_accuracy_pct'] for r in rs),'new_CE_mean_nats':statistics.mean(r['new_ce_nats'] for r in rs),'old_accuracy_mean_pct':statistics.mean(r['old_accuracy_pct'] for r in rs),'qualified_orders':sum(r['new_min_cell_pct']>=95 for r in rs),'original_qualified_first_steps_29_43_71':' / '.join(str(tx[s,arm,'original_new_four_cells95']['first_saved_step']) for s in SEEDS)})
 # R06 is a distinct batch/objective/probe design: supporting check only, not pooled.
 r6=[]
 for seed in SEEDS:
  for k in [0,4,36]:
   for m in ['U','S']:
    case=E6/'runs'/f'seed_{seed}'/f'old_{k:02}'/m;ev=[]
    for step in [0,1,2,4,8,16,32,64,120,180,240]:
     a=read(case/f'eval_{step:06}.json');gg=a['aggregates'];cells=[v['accuracy'] for key,v in gg.items() if key.startswith('mode2/') and '/both/' not in key and not key.endswith('/combined')]
     ev.append({'step':step,'accuracy':gg['mode2/both/combined']['accuracy']*100,'CE':gg['mode2/both/combined']['ce'],'mincell':min(cells)*100})
    hit=next((i for i,x in enumerate(ev) if x['mincell']>=95),None)
    twice=next((i for i in range(1,len(ev)) if ev[i-1]['accuracy']>=90 and ev[i]['accuracy']>=90),None)
    r6.append({'seed':seed,'old_slots':k,'method':m,'endpoint_steps':240,'new_targets':8640,'new_accuracy_pct':ev[-1]['accuracy'],'new_CE_nats':ev[-1]['CE'],'first_fourcell95_step':ev[hit]['step'] if hit is not None else 'NOT_REACHED','second_consecutive_mean90_step':ev[twice]['step'] if twice is not None else 'NOT_REACHED'})
 for name,rs in [('R05_primary_U_TC_TS_9.csv',primary),('R05_endpoint_all_methods_7.csv',means),('R05_paired_endpoint_6.csv',contrasts),('R05_saved_curves_168.csv',curves),('R05_thresholds_all_105.csv',thresholds),('R05_recorded_timing_21.csv',timing),('R06_separate_U_S_18.csv',r6)]:dump(name,rs)
 # Existing audit coverage: verify original published first-qualification numbers.
 assert [tx[s,'U','original_new_four_cells95']['first_saved_step'] for s in SEEDS]==[120,240,1200]
 assert all(tx[s,'TS','original_new_four_cells95']['first_saved_step']==tx[s,'U','original_new_four_cells95']['first_saved_step'] for s in SEEDS)
 verify={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'existing_audit':'R05 a_stage_audit_cn section3 already reports endpoint and first new four-cell95 qualification for all7methods; this audit independently recalculates from per-item outputs and adds90/95/99/99.5sensitivity, consecutive checks, descriptive time and separateR06check','original_qualified_rule':'all4new command×panel cells>=95%; qualified_both not used because it includesold cells','question_count_each':800,'all21paired_orders_equal':True,'same20newtargets_per_step':True,'primary_endpoint':1200,'same_acquired_old_model':True,'additional_criteria':'posthoc descriptive only, not original preregistered endpoints','sparse_eval_limit':'eightoriginal points; step2posthoc audit results wereallbelownewqualification and earlyhighaccuracy thresholds; no unmeasured crossingtime inferred','TEST_opened':False,'new_forward':False,'training':False,'sources':sources,'config_sha256':sha(E/'configs/frozen_v1.json'),'script_sha256':sha(__file__)}
 write(O/'verification.json',verify)
 en='# R05 Top-16 protection: new learning outcome and speed audit\n\n**New-task learning succeeds, but reliable acceleration is not established.** This audit recalculates all original168DEVreadings from per-item records, retains1200asprimaryendpoint, and never trains or readsTEST. ExistingA-stageaudit already covered newendpoints and firstfour-cell95qualification; addedthresholds are descriptive, posthoc sensitivity only.\n\n'
 en+='Actual intervention attenuates16pairedinitialfull-Wrank-onecoefficients perQ/K/V/Omatrix (64total); complementarydisplacement keeps ordinaryscale. TC uses0.1constant; TS usesR05cosine0.1to0.01over1200steps. They filter actualAdamdisplacement without separateoptimizers or establishedsharedfunction. Eachseed sharesoneoldmodel and exactlymatched20newanswers/update,24000atendpoint.\n\n'+table(means,[(k,k) for k in means[0]])+'\n\n'+table(primary,[(k,k) for k in ['seed','arm','new_accuracy_pct','new_ce_nats','first_original_qualified_step','first_original_qualified_new_targets','second_original_qualified_step']])+'\n\n'
 en+='Underoriginalall4newcells>=95%, U/TC/TSfirstsavedhits are120/240/1200fororders29/43/71, with2400/4800/24000newtargets. Sameobservedfirsthitdoesnotproveexactcrossingtimesequalbetweencheckpoints. SomehigherthresholdcasesfavorTC, othersfavorUorTS; all are retained inCSV and cannotreplaceoriginalcriterion. Recordedcomputetimingsarejob-loadconfounded andnotaconfirmedwallclockspeedupbenchmark. R06U/Sisreportedseparatelybecausebatch/denominator/probes/budgetdiffer.\n\n[Chinese](summary_cn.md) · [Allthresholds](R05_thresholds_all_105.csv) · [R06separatecheck](R06_separate_U_S_18.csv) · [Verification](verification.json).\n'
 cn='# Top-16保护：新任务最终效果与学习速度审计\n\n**结论：新任务最终能够学会；现有证据没有建立稳定的新学习加速。** 原A阶段审计已经检查新任务终点及首次四格95%达标，本次从逐题输出独立复算，并补充多门槛、连续达标、原记录计算耗时和R06分开核对。没有新增训练、模型前向或TEST读取。\n\n'
 cn+='## 实际干预对象\n\n每张末层Q/K/V/O矩阵取旧任务后完整权重的前16个配对奇异秩一系数（四矩阵共64系数）；TC把这些系数对应的Adam位移乘0.1，TS用0.1→0.01调度，其余补空间位移不衰减。实际没有两套独立优化器；“缓慢更新”指实际Adam位移的衰减，不是已确认共同计算，也不保护整个16维左右输入输出子空间。\n\n'
 cn+='## 最终新任务效果（保留原1200步终点）\n\n'+table(means,[('arm','方法'),('new_accuracy_mean_pct','新准确率均值 %'),('new_CE_mean_nats','新CE均值'),('old_accuracy_mean_pct','旧准确率均值 %'),('qualified_orders','新四格达标/3'),('original_qualified_first_steps_29_43_71','首次达标步29/43/71')])+'\n\n'
 cn+='CE为正确答案概率的负自然对数，单位nat/答案，越低越好。每条轨迹新DEV800题、四格各200，全词表最大值评价。U新准确率99.541667%，TC/TS均99.500000%；TS新CE略低于U，但并非所有顺序均更低，不能据此宣称稳定优势。三个顺序共享一个旧模型，均值不是独立模型总体估计。\n\n'
 cn+='## 是否更快达到高准确率\n\n优先沿用原门槛：新任务两口令×两面板四格各≥95%，不是只看平均95%。各方法同20新答案/步，因此步数与新样本曝光等价。\n\n'+table(primary,[('seed','续训顺序'),('arm','方法'),('new_accuracy_pct','终点新 %'),('new_ce_nats','终点新CE'),('first_original_qualified_step','首次四格95%步'),('first_original_qualified_new_targets','当时新曝光'),('second_original_qualified_step','连续两点评价确认步')])+'\n\n'
 cn+='U、TC、TS在三个顺序的首次已保存达标点完全相同：120、240、1200步；对应2400、4800、24000次新答案曝光。连续达标确认也没有为Top-16建立稳定提前：顺序71只有最后保存点达标，无法确认后续第二点，不写成未学会。原评价点稀疏，不能据此说真实跨越阈值的瞬间完全相同，也不能插值编造未测步骤。\n\n'
 cn+='补充门槛为平均90%、95%、99%、99.5%，均属事后描述，所有单次/连续两次读数原样保留；只在某个顺序、某个门槛更早不叫稳定加速。原日志记录计算秒，但不同作业并发负载、启动、评价和存盘不同，因此不把总耗时直接归因于方法；计算秒明细单列，仅作工程描述。\n\n'
 cn+='## R06另列，不混合数值\n\n最新R06将batch/旧监督/统一分母/探针与总步数改为另一设置。其U与S在三个旧监督档、三个续训顺序的“连续两次新平均≥90%”均在180步确认，没有观察到S提前；四格95%的读数及终点新CE完整保留在独立表，不与原1200步实验混成均值。\n\n'+table(r6,[('seed','顺序'),('old_slots','旧槽'),('method','方法'),('new_accuracy_pct','240步新 %'),('new_CE_nats','新CE'),('first_fourcell95_step','首次四格95%'),('second_consecutive_mean90_step','连续两次90%确认')])+'\n\n'
 cn+='## 可以怎样汇报\n\n“降低初始Top-16秩一系数的更新速度，没有妨碍最终学会新规则，但也没有在原定达标标准下表现出更快的新任务学习；同时未保住旧能力。”这限定于当前旧模型、任务、四矩阵、秩与优化设置，不能推出所有保护方法都无法加速。\n\n[所有保存点](R05_saved_curves_168.csv) · [全部补充门槛](R05_thresholds_all_105.csv) · [逐方法配对终点差](R05_paired_endpoint_6.csv) · [原记录时间](R05_recorded_timing_21.csv) · [复算与来源](verification.json)。\n'
 for name,text in [('summary.md',en),('summary_cn.md',cn)]: (O/name).write_text(text)
 import shutil
 for p in O.iterdir():
  if p.is_file():shutil.copy2(p,D/p.name)
 shutil.copy2(__file__,D/'audit_top16_learning_speed_20261026.py')
 print(json.dumps({'means':means,'primary':primary,'audit_dir':str(D)},ensure_ascii=False))
if __name__=='__main__':main()
