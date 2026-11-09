from pathlib import Path
import csv,json,math,statistics,hashlib,datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis';OUT.mkdir(exist_ok=True)
CFG=json.loads((ROOT/'config/frozen.json').read_text());OWN=json.loads((ROOT/'provenance/ownership.json').read_text());R=Path(OWN['round'])
LABEL={'U':'Ordinary U','S':'Top-16 S','F':'Functional F','D':'Norm control D'}
COLORS={'U':'#333333','S':'#0072B2','F':'#D55E00','D':'#009E73'}
def read(p):return json.loads(p.read_text())
def csvwrite(name,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def table(rows,columns):
    lines=['| '+' | '.join(n for k,n in columns)+' |','| '+' | '.join('---' for _ in columns)+' |']
    for r in rows:
        def fmt(k):
            v=r.get(k,'MISSING')
            if isinstance(v,float):return f'{v:.3f}'
            return str(v)
        lines.append('| '+' | '.join(fmt(k) for k,n in columns)+' |')
    return '\n'.join(lines)
def point(a):
    old=a['aggregates']['mode1/both/combined'];new=a['aggregates']['mode2/both/combined']
    return {'old_accuracy_pct':100*old['accuracy'],'new_accuracy_pct':100*new['accuracy'],'old_ce':old['ce'],'new_ce':new['ce']}

def main():
    endpoints=[];curves=[];thresholds=[];diag=[];allmetrics={};evaluations={};coverage=[];verification=[];cellrows=[];finite_rows=[]
    terminal_coverage={(r['seed'],r['old_nonzero'],r['method']):r for r in read(ROOT/'terminal.json')['coverage']}
    orders_payload=read(ROOT/'provenance/orders.json')['seeds']
    lengths=[len(json.loads(x)['input_ids']) for x in (Path(CFG['data'])/'train.jsonl').read_text().splitlines() if json.loads(x)['world'] in ('old','reversed')]
    for seed in CFG['seeds']:
      for k in CFG['old_slots_nonzero']:
       for method in CFG['methods']:
        case=ROOT/'runs'/f'seed_{seed}'/f'old_{k:02}'/method
        ident={'seed':seed,'old_nonzero':k,'method':method};evaluations[(seed,k,method)]=ev=[]
        completion=read(case/'completion.json') if (case/'completion.json').exists() else terminal_coverage.get((seed,k,method),{'status':'NOT_COMPLETED','steps':None})
        coverage.append({**ident,'status':completion['status'],'steps':completion.get('steps')})
        for p in sorted(case.glob('eval_*.json')):
            a=read(p)
            for cell,v in a['aggregates'].items():cellrows.append({**ident,'step':a['step'],'cell':cell,'n':v['n'],'accuracy_pct':100*v['accuracy'],'ce':v['ce']})
            row={**ident,'step':a['step'],'new_targets':36*a['step'],**point(a),'elapsed_seconds':a['elapsed_seconds']}
            for name,value in row.items():
                if isinstance(value,float):assert math.isfinite(value),(case,name)
            curves.append(row);ev.append(row)
            if 'records' in a:
                rr=a['records'];assert len(rr)==1600
                for mode,label in [(1,'old'),(2,'new')]:
                    rs=[r for r in rr if r['mode']==mode];assert len(rs)==800
                    assert abs(sum(r['correct'] for r in rs)/8-row[label+'_accuracy_pct'])<1e-10
                    assert abs(sum(r['ce'] for r in rs)/800-row[label+'_ce'])<1e-10
                    cells={}
                    for r in rs:cells.setdefault((r['panel'],r['command']),[]).append(r)
                    assert sorted(map(len,cells.values()))==[200]*4
                verification.append(str(p))
        if ev and ev[-1]['step']==240 and completion['status']=='DONE_EXPLORATORY':endpoints.append({**ev[-1],'status':completion['status']})
        else:endpoints.append({**ident,'status':completion['status'],'step':completion.get('steps')})
        mets=[json.loads(s) for s in (case/'metrics.jsonl').read_text().splitlines()] if (case/'metrics.jsonl').exists() else []
        allmetrics[(seed,k,method)]=mets
        assert all(m['step']==i+1 for i,m in enumerate(mets))
        for m in mets:
            if 'probe_loss_change' in m:finite_rows.append({**ident,**{key:m[key] for key in ['step','probe_loss_before','probe_loss_after','probe_loss_change','g_dot_candidate','g_dot_desired','g_dot_actual','first_order_remainder','candidate_norm','functional_norm','actual_norm','actual_C_energy_fraction']}})
            t=m['step'];c=m['counters']
            assert c['new_targets']==36*t and c['old_active_targets']==k*t and c['old_probe_targets']==64*t
            assert c['valid_objective_targets']==(36+k)*t and c['all_input_slots']==72*t
            assert abs(m['objective']-(m['new_weighted']+m['old_weighted']))<1e-6
            assert all(math.isfinite(m[n]) for n in ['objective','probe_g2','candidate_norm','actual_norm','g_dot_candidate','g_dot_actual'])
        if mets:
            measured=[m for m in mets if 'probe_loss_change' in m]
            needed=[m for m in mets if m['projection_needed']]
            diag.append({**ident,'steps':len(mets),'projection_needed_steps':len(needed),'floor_triggers':sum(m['gradient_floor'] for m in mets),'clip_steps':sum(m['clip_triggered'] for m in mets),
                'mean_candidate_norm':statistics.mean(m['candidate_norm'] for m in mets),'mean_actual_norm':statistics.mean(m['actual_norm'] for m in mets),
                'sum_actual_step_norms':sum(m['actual_norm'] for m in mets),'sum_actual_step_norm_squared':sum(m['actual_norm']**2 for m in mets),
                'mean_C_energy_fraction_pct':100*statistics.mean(m['actual_C_energy_fraction'] for m in mets),
                'sum_C_step_squared_fraction_pct':100*sum(m['actual_C_norm']**2 for m in mets)/sum(m['actual_norm']**2 for m in mets),
                'probe_measured_steps':len(measured),'probe_loss_increase_steps':sum(m['probe_loss_change']>0 for m in measured),
                'mean_measured_probe_loss_change':statistics.mean(m['probe_loss_change'] for m in measured) if measured else None,
                'mean_measured_remainder':statistics.mean(m['first_order_remainder'] for m in measured) if measured else None,
                'gradient_compute_seconds':sum(m['times']['probe_grad_seconds'] for m in mets),
                'probe_diagnostic_forward_seconds':sum(m['times'].get('probe_after_forward_seconds',0) for m in mets),'probe_diagnostic_label_uses':64*len(measured),'probe_total_label_uses':64*(len(mets)+len(measured)),'probe_gradient_input_tokens':mets[-1]['counters']['old_probe_input_tokens'],'probe_diagnostic_input_tokens':sum(sum(lengths[i] for i in orders_payload[str(seed)][m['step']-1]['probe']) for m in measured),
                'update_compute_seconds':sum(m['update_seconds'] for m in mets),'new_targets':mets[-1]['counters']['new_targets'],'old_active_targets':mets[-1]['counters']['old_active_targets'],'probe_label_accesses':mets[-1]['counters']['old_probe_targets'],
                'note':'step norm sums / squared sums; NOT endpoint net displacement'})
        op=None
        for a,b in zip(ev,ev[1:]):
            if a['new_accuracy_pct']>=90 and b['new_accuracy_pct']>=90:
                op={**b,'first_pair_reading_step':a['step'],'confirmed_step':b['step'],'status':'REACHED','old_active_targets':k*b['step'],'probe_label_accesses':64*b['step'],'probe_diagnostic_label_uses':64*sum('probe_loss_change' in m for m in mets[:b['step']]),'probe_total_label_uses':64*(b['step']+sum('probe_loss_change' in m for m in mets[:b['step']])),
                    'update_compute_seconds':sum(m['update_seconds'] for m in mets[:b['step']]),
                    'timing_note':'seed29 k0 U elapsed includes once-only external replay; use update_compute_seconds for update cost'};break
        thresholds.append(op or {**ident,'status':'NOT_REACHED' if completion['status']=='DONE_EXPLORATORY' else 'MISSING_OR_PARTIAL','confirmed_step':None})
    csvwrite('probe_finite_diagnostics_360.csv',finite_rows);csvwrite('DEV_cells_all_readings.csv',cellrows);csvwrite('endpoints_36.csv',endpoints);csvwrite('curves.csv',curves);csvwrite('learning90_operating_points.csv',thresholds);csvwrite('diagnostic_overview.csv',diag);csvwrite('coverage.csv',coverage)
    ix={(r['seed'],r['old_nonzero'],r['method']):r for r in endpoints};contrasts=[];aggregate=[];decisions=[]
    for k in CFG['old_slots_nonzero']:
        for method in CFG['methods']:
            rs=[ix[(s,k,method)] for s in CFG['seeds'] if 'old_accuracy_pct' in ix[(s,k,method)]]
            if rs:
                aggregate.append({'old_nonzero':k,'method':method,'completed_seeds':len(rs),**{a:statistics.mean(r[a] for r in rs) for a in ['old_accuracy_pct','new_accuracy_pct','old_ce','new_ce']},
                    'old_min_pct':min(r['old_accuracy_pct'] for r in rs),'old_max_pct':max(r['old_accuracy_pct'] for r in rs),
                    'new_min_pct':min(r['new_accuracy_pct'] for r in rs),'new_max_pct':max(r['new_accuracy_pct'] for r in rs)})
        for comparator in ['U','S','D']:
            rs=[]
            for seed in CFG['seeds']:
                a=ix[(seed,k,'F')];b=ix[(seed,k,comparator)]
                if 'old_accuracy_pct' not in a or 'old_accuracy_pct' not in b:continue
                r={'seed':seed,'old_nonzero':k,'comparison':'F-'+comparator,'old_difference_pp':a['old_accuracy_pct']-b['old_accuracy_pct'],'new_difference_pp':a['new_accuracy_pct']-b['new_accuracy_pct'],'old_ce_difference':a['old_ce']-b['old_ce'],'new_ce_difference':a['new_ce']-b['new_ce']};contrasts.append(r);rs.append(r)
            decisions.append({'old_nonzero':k,'comparison':'F-'+comparator,'paired_seeds':len(rs),'old_mean_difference_pp':statistics.mean(r['old_difference_pp'] for r in rs) if rs else None,
                'new_mean_difference_pp':statistics.mean(r['new_difference_pp'] for r in rs) if rs else None,'old_all_positive':len(rs)==3 and all(r['old_difference_pp']>0 for r in rs),
                'new_each_within_5pp':len(rs)==3 and all(r['new_difference_pp']>=-5 for r in rs),
                'operational_rule_pass':len(rs)==3 and statistics.mean(r['old_difference_pp'] for r in rs)>=5 and all(r['old_difference_pp']>0 and r['new_difference_pp']>=-5 for r in rs)})
    trends=[]
    for seed in CFG['seeds']:
        rs=[r for r in contrasts if r['seed']==seed and r['comparison']=='F-U'];ds={r['old_nonzero']:r['old_difference_pp'] for r in rs}
        trends.append({'seed':seed,**{f'F_minus_U_old_pp_k{k}':ds.get(k) for k in [0,4,36]},'advantage_larger_when_old_sparser':len(ds)==3 and ds[0]>ds[4]>ds[36]})
    csvwrite('method_means_12.csv',aggregate);csvwrite('paired_contrasts_27.csv',contrasts);csvwrite('operational_decisions.csv',decisions);csvwrite('frequency_relative_gains.csv',trends)
    writeout={'evaluations_recomputed':len(verification),'all_per_item_accuracy_denominators_800':True,'all_cells_200':True,'full_vocabulary_argmax_source':'engine.evaluate logits.argmax(-1), no candidate restriction',
       'all_loss_objective_counters_checked':True,'uncertainty':'continuation-order values/ranges conditional on one old model; no model-population confidence interval','complete_runs':sum(r['status']=='DONE_EXPLORATORY' for r in coverage),'expected_runs':36,
       'step240_new_targets_per_complete_run':8640,'probe_gradient_label_uses_per_complete_run':15360,'probe_diagnostic_label_uses_per_complete_run':640,'probe_total_label_uses_per_complete_run':16000,'TEST_opened':False,'decisions':decisions,'trends':trends}
    (OUT/'verification.json').write_text(json.dumps(writeout,indent=2)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
    for metric,name in [('accuracy_pct','accuracy'),('ce','answer_loss')]:
        fig,axes=plt.subplots(2,3,figsize=(12,6.4),sharex=True)
        for c,k in enumerate([0,4,36]):
            for row,task in enumerate(['old','new']):
                ax=axes[row,c]
                for method in CFG['methods']:
                    vals=[];xs=[]
                    for step in CFG['eval_steps']:
                        rr=[r for r in curves if r['old_nonzero']==k and r['method']==method and r['step']==step]
                        if len(rr)!=3:continue
                        xs.append(step*36);vals.append([r[f'{task}_{metric}'] for r in rr])
                    if vals:
                        vs=np.asarray(vals);ax.plot(xs,vs.mean(1),label=LABEL[method],color=COLORS[method],marker={'U':'o','S':'s','F':'^','D':'D'}[method],markersize=3)
                        ax.fill_between(xs,vs.min(1),vs.max(1),color=COLORS[method],alpha=.10)
                ax.set_ylabel(('Old A' if task=='old' else 'New B')+(' accuracy (%)' if metric=='accuracy_pct' else ' CE (nat/answer)'))
                if row==0:ax.set_title(f'Old objective slots: {k}/36')
                else:ax.set_xlabel('Cumulative new answer targets')
                if metric=='accuracy_pct':ax.set_ylim(-1,101)
                ax.grid(alpha=.18)
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=4,frameon=False)
        fig.tight_layout(rect=[0,0,1,.95])
        for ext in ['png','svg','pdf']:fig.savefig(OUT/f'{name}_curves.{ext}',dpi=260,bbox_inches='tight')
        plt.close(fig)
    for seed in CFG['seeds']:
        fig,axes=plt.subplots(2,3,figsize=(12,6),sharex=True,sharey=True)
        for c,k in enumerate([0,4,36]):
            for row,task in enumerate(['old','new']):
                ax=axes[row,c]
                for method in CFG['methods']:
                    rr=[r for r in curves if r['seed']==seed and r['old_nonzero']==k and r['method']==method]
                    ax.plot([r['new_targets'] for r in rr],[r[f'{task}_accuracy_pct'] for r in rr],label=method,color=COLORS[method],marker='o',ms=3)
                ax.set_ylim(-1,101);ax.grid(alpha=.15);ax.set_ylabel(task+' accuracy (%)')
                if row==0:ax.set_title(f'Order {seed}; old slots {k}')
                else:ax.set_xlabel('New answer targets')
        fig.legend(*axes[0,0].get_legend_handles_labels(),loc='upper center',ncol=4,frameon=False);fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(OUT/f'order_{seed}_accuracy.png',dpi=220);plt.close(fig)
    cols=[('old_nonzero','旧有效槽'),('method','方法'),('completed_seeds','完成顺序数'),('old_accuracy_pct','旧准确率 %'),('new_accuracy_pct','新准确率 %'),('old_ce','旧CE'),('new_ce','新CE')]
    text='# R06：固定新任务曝光的保护方法与监督配比\n\n'
    text+='三条阅读路径：①行为与因素对照，看各档F相对U/S/D的旧新表现；②表示与层间组织，本轮未新增此类测量；③功能干预与测量质量，看实际Adam位移、探针损失与数值核验。\n\n'
    text+='本轮目的：在新任务曝光不变时，区分功能方向选择、整体减速和旧监督本身的作用。全部条件共用同一个合格旧模型；每步36新答案、36旧输入槽，旧有效监督0/4/36，统一分母72。四方法均另读64条旧TRAIN探针，F/D用其标签约束位移。TEST本轮未读取。\n\n'
    text+=f'已完成 {writeout["complete_runs"]}/36 条240步轨迹。每条完整轨迹8640次新答案曝光，旧有效曝光0/960/8640，另有15360次旧探针梯度标签使用，以及10个检查步共640次更新后诊断标签复用，合计16000次探针标签使用。主结果保持240步；下表按三个续训顺序等权平均，若未齐全则明确显示完成数。答案损失用交叉熵（Cross Entropy，CE），即正确答案概率的负自然对数，单位nat/答案，越低越好；表内保留三位小数，完整精度在CSV。\n\n'+table(aggregate,cols)+'\n\n'
    text+='U=普通更新；S=原Top-16系数衰减；F=避免旧TRAIN探针损失一阶预测上升的位移投影；D=保留原位移方向、在自身轨迹上匹配F候选长度。S保留原1200步调度，只运行前240步，因此与R05终点强度不是同一阶段。\n\n'
    text+='## 冻结判据与配对比较\n\n'+table(decisions,[('old_nonzero','旧有效槽'),('comparison','比较'),('paired_seeds','配对数'),('old_mean_difference_pp','平均旧差 pp'),('new_mean_difference_pp','平均新差 pp'),('old_all_positive','旧改善均为正'),('new_each_within_5pp','各顺序新下降≤5pp'),('operational_rule_pass','操作性门槛')])+'\n\n'
    text+='操作性门槛要求旧改善平均至少5个百分点、三顺序均为正、各顺序新下降不超过5个百分点。对S/D的同门槛读数是补充比较，主要预定判据是F−U；不称为统计证明。\n\n'
    text+='## 旧监督减少时的相对收益\n\n'+table(trends,[('seed','续训顺序'),('F_minus_U_old_pp_k0','0槽 F−U pp'),('F_minus_U_old_pp_k4','4槽 F−U pp'),('F_minus_U_old_pp_k36','36槽 F−U pp'),('advantage_larger_when_old_sparser','随监督减少严格增大')])+'\n\n'
    text+='## 固定新学习水平与成本\n\n'+table(thresholds,[('seed','顺序'),('old_nonzero','旧槽'),('method','方法'),('status','90%状态'),('confirmed_step','连续两点评价确认步'),('old_accuracy_pct','确认时旧 %'),('new_accuracy_pct','确认时新 %'),('new_targets','新曝光'),('probe_label_accesses','探针梯度标签'),('probe_diagnostic_label_uses','探针诊断标签'),('update_compute_seconds','更新计算秒')])+'\n\n'
    text+='连续两次新平均准确率≥90%的第二个评价点为预定次要读数；未达到的保留。更新计算秒为各步测量之和，排除DEV评价、存盘和一次性外进程恢复检查；首次U运行的总耗时含工程检查，不能直接作为方法速度差。探针梯度与更新后诊断的标签使用、输入token和计算开销在diagnostic_overview.csv中分列；运行时old_probe_targets计数专指梯度探针，诊断复用按固定检查步另行补计。\n\n'
    text+='## 观察、解释与边界\n\n'
    for d in decisions:
        if d['comparison']=='F-U':text+=f'- 旧槽{d["old_nonzero"]}：F−U旧准确率均差{d["old_mean_difference_pp"]}pp，新均差{d["new_mean_difference_pp"]}pp；预定操作性判据={d["operational_rule_pass"]}。\n'
    text+='\n这些是冻结规则的计算结果；AI解释需同时看D与新学习资格。F即使满足局部一阶约束，也可能因有限步余项或探针泛化而遗忘。旧频率同时改变旧目标总权重，不是纯频率实验；三个顺序共用旧模型，不能外推到独立模型总体。没有新增MoE、路由或自然语言任务，加法证据未混入。研究者机制接受与主问题关闭仍Unknown。\n\n'
    text+='完整证据：[逐顺序终点](tables/endpoints_36.csv)、[全部曲线](tables/curves.csv)、[局部诊断](tables/diagnostic_overview.csv)、[核验](tables/verification.json)、[执行细节](detailed_cn.md)。\n'
    text+='\n## 曲线与读取方式\n\n![固定新曝光下的旧新准确率](figures/accuracy_curves.png)\n\n横轴是累计新答案曝光，纵轴分别是旧/新准确率（%）；每列对应一个旧监督档。线为三个续训顺序等权平均，色带只表示三者最小到最大值，不是置信区间；保存点之间连线辅助阅读，没有平滑。\n\n[旧新答案损失曲线](figures/answer_loss_curves.png)的纵轴为每答案自然对数损失，越低越好；[顺序29](figures/order_29_accuracy.png)、[顺序43](figures/order_43_accuracy.png)、[顺序71](figures/order_71_accuracy.png)保留逐顺序曲线。\n'
    (R/'summary_cn.md').write_text(text)
    # Data-first English companion; no new scientific verdict is inferred.
    en='# R06: Fixed-new-exposure functional protection\n\n'
    en+=f'{writeout["complete_runs"]}/36 step240 runs completed. All conditions share one acquired-old Qwen3-0.6B Base and update the same final Q/K/V/O matrices. Per update:36new answers,36old input slots with k=0/4/36 active, denominator72, plus64labelled old TRAIN probes for ALL methods. F/D use those labels even at k=0. TEST was not opened.\n\n'
    en+=table(aggregate,[(k,k) for k in ['old_nonzero','method','completed_seeds','old_accuracy_pct','new_accuracy_pct','old_ce','new_ce']])+'\n\n'
    en+='U uses actual Adam displacement; S uses R05 paired Top16 coefficient attenuation on the original1200-step schedule; F projects harmful old-probe first-order displacement; D keeps its own candidate direction and matches its own F-candidate norm. Fresh AdamW lr1e-4. Means/ranges describe three continuation orders conditional on one old model.\n\n'
    en+=table(decisions,[(k,k) for k in ['old_nonzero','comparison','old_mean_difference_pp','new_mean_difference_pp','operational_rule_pass']])+'\n\n'
    en+='Primary endpoints stay240steps/8640new targets. The second consecutive scheduled new accuracy>=90% reading is secondary and missing readings remain explicit. Operational rule: F-U mean old>=5pp, every old difference positive, every new difference>=-5pp. Compare D before direction attribution. Replay changes both old label count and objective weight. No universal model/feature/routing/architecture conclusion. Researcher scientific judgment/closure remain Unknown. See Chinese Summary, Detailed and CSVs for every order, loss, cost, negative result and numerical receipt.\n'
    en+='\n![Accuracy at fixed new exposure](figures/accuracy_curves.png)\n\nCurves: equal-weight3continuation orders; shading=min-to-max, notCI. Independent y axes for old/new behavior; no smoothing. [Answer CE curves](figures/answer_loss_curves.png). [All order endpoints](tables/endpoints_36.csv), [all readings](tables/curves.csv), [paired contrasts](tables/paired_contrasts_27.csv), [90percent operating points](tables/learning90_operating_points.csv), [frequency relative gains](tables/frequency_relative_gains.csv), [diagnostics](tables/diagnostic_overview.csv), [Detailed](detailed.md).\n'
    (R/'summary.md').write_text(en)
    tables=R/'tables';tables.mkdir(exist_ok=True)
    import shutil
    for p in OUT.glob('*.csv'):shutil.copy2(p,tables/p.name)
    shutil.copy2(OUT/'verification.json',tables/'verification.json')
    figs=R/'figures';figs.mkdir(exist_ok=True)
    for p in OUT.glob('*_curves.*'):shutil.copy2(p,figs/p.name)
    for p in OUT.glob('order_*_accuracy.png'):shutil.copy2(p,figs/p.name)
    (R/'coverage.md').write_text('# Full requested coverage\n\n'+table(coverage,[(k,k) for k in ['seed','old_nonzero','method','status','steps']])+'\n')
    print(json.dumps({'complete':writeout['complete_runs'],'decisions':decisions,'summary':str(R/'summary_cn.md')},ensure_ascii=False))
if __name__=='__main__':main()
