from pathlib import Path
import json,csv,hashlib,math,statistics,datetime,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
E=Path(__file__).resolve().parents[1];O=E/'analysis/local_dynamics_20261026';V=O/'provenance';OWN=json.load(open(V/'ownership.json'));R=Path(OWN['round']);A=Path(OWN['anchor']);S=Path('/data/250010109/Research_System')
def read(p):return json.loads(Path(p).read_text())
def rows(n):return list(csv.DictReader(open(O/'tables'/n)))
def num(x):
 if x in ['',None]:return None
 if x in ['True','False']:return x=='True'
 try:return float(x)
 except:return x
def typed(rs):return [{k:num(v) for k,v in r.items()} for r in rs]
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def dump(n,rs):
 keys=list(dict.fromkeys(k for r in rs for k in r))
 with (O/'tables'/n).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rs)
def table(rs,cols):
 def f(x):return f'{x:.6f}' if isinstance(x,float) else str(x)
 return '\n'.join(['| '+' | '.join(v for k,v in cols)+' |','| '+' | '.join('---' for _ in cols)+' |']+['| '+' | '.join(f(r.get(k,'MISSING')) for k,v in cols)+' |' for r in rs])
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 rec=read(O/'receipt.json');assert rec['status']=='PASS' and rec['sequence_forwards']==11424
 losses=typed(rows('candidate_group_losses_138.csv'));dirs=typed(rows('candidate_directions_54.csv'));noise=typed(rows('noop_noise_18.csv'));curves=typed(rows('trajectory_alignment_132.csv'));ss=read(O/'state_summary.json')
 ix={(int(r['seed']),r['origin'],r['condition'],r['alpha'],r['group']):r for r in losses};di={(int(r['seed']),r['origin'],r['condition'],r['alpha']):r for r in dirs}
 comparisons=[];interactions=[];history=[];mainrows=[];scaling=[];branches=[]
 for seed in [29,43,71]:
  for origin in ['U','F']:
   for cond in ['d0','d4','F0','F4','D4']:
    a={'seed':seed,'origin':origin,'candidate':cond,'F_active':di[seed,origin,cond,1.]['F_active']}
    for group in ['probe','new','independent_old']:
     v=ix[seed,origin,cond,1.,group];a[group+'_baseline_CE']=v['before_CE'];a[group+'_delta_CE']=v['CE_change'];a[group+'_margin_change']=v['margin_change']
    mainrows.append(a)
   for tr,ct in [('F0','d0'),('F4','d4'),('D4','d4'),('F4','D4'),('d4','d0')]:
    for group in ['probe','new','independent_old']:
     t=ix[seed,origin,tr,1.,group];c=ix[seed,origin,ct,1.,group];delta=t['CE_change']-c['CE_change'];tol=2*max(t['noise_tau'],c['noise_tau'])
     comparisons.append({'seed':seed,'origin':origin,'comparison':tr+'-'+ct,'group':group,'treatment_delta_CE':t['CE_change'],'control_delta_CE':c['CE_change'],'paired_CE_difference':delta,'paired_noise_tolerance':tol,'direction':'worse' if delta>tol else 'better' if delta<-tol else 'noise_or_equal','treatment_margin_change':t['margin_change'],'control_margin_change':c['margin_change'],'paired_margin_change':t['margin_change']-c['margin_change']})
   for group in ['probe','new','independent_old']:
    a=ix[seed,origin,'F4',1.,group]['CE_change']-ix[seed,origin,'d4',1.,group]['CE_change'];b=ix[seed,origin,'F0',1.,group]['CE_change']-ix[seed,origin,'d0',1.,group]['CE_change']
    interactions.append({'seed':seed,'origin':origin,'group':group,'F_effect_with4':a,'F_effect_with0':b,'same_state_interaction_4_minus0':a-b,'warning':'samehistorical1:9state, currentbatch0vs4; NOTsameas0:1historyendpointinteraction'})
   for cond in ['d4','F4']:
    rems=[]
    for alpha in [1.,.5,.25]:
     r=ix[seed,origin,cond,alpha,'probe'];rems.append(abs(r['finite_remainder']));scaling.append({'seed':seed,'origin':origin,'candidate':cond,'alpha':alpha,'probe_delta_CE':r['CE_change'],'probe_first_order':r['first_order_prediction'],'probe_finite_remainder':r['finite_remainder'],'abs_remainder':abs(r['finite_remainder']),'remainder_over_alpha_squared':r['finite_remainder']/alpha**2,'independent_old_delta_CE':ix[seed,origin,cond,alpha,'independent_old']['CE_change'],'probe_noise_tolerance':r['noise_tau']})
    branches.append({'branch':'finite_remainder_scale','seed':seed,'origin':origin,'candidate':cond,'abs_remainder_decreases_1_half_quarter':rems[0]>rems[1]>rems[2]})
  for group in ['probe','new','independent_old']:
   f=ix[seed,'F','d4',1.,group];u=ix[seed,'U','d4',1.,group];history.append({'seed':seed,'group':group,'U_origin_before_CE':u['before_CE'],'F_origin_before_CE':f['before_CE'],'U_origin_d4_delta':u['CE_change'],'F_origin_d4_delta':f['CE_change'],'F_minus_U_origin_delta':f['CE_change']-u['CE_change'],'precision_tolerance':2*max(f['noise_tau'],u['noise_tau']),'scope':'differentthetaANDAdamhistory, notisolatedcausalcomponent'})
 dump('main_candidates_30.csv',mainrows);dump('paired_functional_comparisons_90.csv',comparisons);dump('same_state_old_target_interactions_18.csv',interactions);dump('origin_state_comparison_9.csv',history);dump('finite_scaling_36.csv',scaling);dump('scale_remainder_monotonicity_12.csv',branches)
 # Independent row/count/branch invariants, no additional forwards.
 assert len(losses)==138 and len(dirs)==54 and len(noise)==18
 for r in losses:assert math.isclose(r['after_CE']-r['before_CE'],r['CE_change'],abs_tol=1e-12)
 assert all(r['noop_span']==0 for r in noise)
 f4compar=[r for r in comparisons if r['comparison']=='F4-d4'];f4old=[r for r in f4compar if r['group']=='independent_old'];f4new=[r for r in f4compar if r['group']=='new']
 assert sum(r['direction']=='worse' for r in f4old)==0
 assert all(di[s,'U','F4',1.]['actual_removed_component_norm']==0 for s in [29,43,71])
 noise_max=max(r['noise_tolerance'] for r in noise)
 fixed={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_original_inputs_unchanged':read(V/'original_asset_immutability.json'),'same_state_branches_all_independent':True,'sequences':rec['sequence_forwards'],'rows':{'loss':len(losses),'direction':len(dirs),'noise':len(noise)},'F4_vs_d4_independent_old':{v:sum(r['direction']==v for r in f4old) for v in ['better','worse','noise_or_equal']},'F4_vs_d4_new':{v:sum(r['direction']==v for r in f4new) for v in ['better','worse','noise_or_equal']},'baseline_noop_spans_all_zero':True,'max_noise_tau':noise_max,'gradient_cosines':[{'seed':r['seed'],'origin':r['origin'],'cosine':r['g4_probe_cosine']} for r in ss],'all_scaling_abs_remainders_decrease':all(r['abs_remainder_decreases_1_half_quarter'] for r in branches),'historical_source_step121_candidate_norm_errors':[float(r['candidate_norm_abs_error']) for r in rows('source_step121_replay_6.csv')],'full_trajectory_causation_established':False,'parameter_and_moment_causes_separated':False}
 write(V/'analysis_verification.json',fixed)
 # Exactly two figures, no causal storytelling inside plots.
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
 colors={'U':'#333333','F':'#D55E00'}
 fig,axs=plt.subplots(2,2,figsize=(9.2,6.5),sharex=True)
 for col,k in enumerate([0,4]):
  for method in ['U','F']:
   rr=sorted(set(r['step'] for r in curves));acc=[];ce=[];newce=[]
   for step in rr:
    x=[r for r in curves if r['old_slots']==k and r['method']==method and r['step']==step]
    acc.append([r['old_accuracy_pct'] for r in x]);ce.append([r['old_CE'] for r in x]);newce.append([r['new_CE'] for r in x])
   for row,values in [(0,acc),(1,ce)]:
    vv=np.array(values);axs[row,col].plot(rr,vv.mean(1),color=colors[method],marker='o' if method=='U' else '^',ms=4,label=method);axs[row,col].fill_between(rr,vv.min(1),vv.max(1),color=colors[method],alpha=.10)
  axs[0,col].set_title('Old:new objective labels '+('0:1' if k==0 else '1:9'));axs[0,col].set_ylim(0,101);axs[0,col].set_ylabel('Old DEV accuracy (%)');axs[1,col].set_ylabel('Old DEV CE (nat/answer)');axs[1,col].set_xlabel('Optimizer step (36 new targets/step)')
  for row in [0,1]:axs[row,col].axvline(120,ls='--',c='#0072B2',alpha=.7);axs[row,col].grid(alpha=.16)
 axs[0,0].legend(frameon=False,ncol=2);fig.tight_layout()
 for ext in ['png','svg','pdf']:fig.savefig(O/'figures'/('figure1_trajectory.'+ext),dpi=270,bbox_inches='tight')
 plt.close(fig)
 fig,axs=plt.subplots(1,3,figsize=(12.2,4.0),sharex=True)
 groups=['probe','independent_old','new'];names={'probe':'Old TRAIN probe','independent_old':'Independent old DEV','new':'New TRAIN batch'};co={'d4':'#777777','F4':'#D55E00','D4':'#009E73'};xx=np.arange(6)
 for ax,group in zip(axs,groups):
  for offset,con in [(-.24,'d4'),(0.,'F4'),(.24,'D4')]:
   vals=[ix[s,o,con,1.,group]['CE_change'] for s,o in [(29,'U'),(29,'F'),(43,'U'),(43,'F'),(71,'U'),(71,'F')]];ax.bar(xx+offset,vals,width=.22,color=co[con],label=con)
  ax.axhline(0,c='black',lw=.7);ax.set_xticks(xx,['29\nU','29\nF','43\nU','43\nF','71\nU','71\nF']);ax.set_title(names[group]);ax.set_ylabel('One-step CE change (nat/answer)');ax.set_xlabel('Seed / state origin at step 120');ax.grid(axis='y',alpha=.15)
 fig.legend(*axs[0].get_legend_handles_labels(),ncol=3,frameon=False,fontsize=10,loc='upper center');fig.tight_layout(rect=[0,0,1,.91])
 for ext in ['png','svg','pdf']:fig.savefig(O/'figures'/('figure2_same_state.'+ext),dpi=270,bbox_inches='tight')
 plt.close(fig)
 # Detailed bilingual canonical result. Original rounds/meeting materials stay intact.
 maincols=[('seed','顺序'),('origin','120步起点来源'),('candidate','候选'),('probe_delta_CE','旧探针ΔCE'),('independent_old_delta_CE','独立旧ΔCE'),('new_delta_CE','新题ΔCE')]
 detail='''# F的当步作用与历史路径：固定六状态诊断

**核心判断：在预先固定的六个第120步状态，没有发现F4比普通联合更新d4更伤旧任务；在两个实际触发投影的状态，F4反而改善旧损失，并减慢当步新学习。历史状态差异的解释优先级上升，但参数历史和Adam历史尚未分离。** 这是局部诊断，不能由此解释全部240步终点。

## 1. 为什么做这轮

0:1中F优于U、1:9中F弱于U是不同历史轨迹的终点事实，不等于同状态加入4旧题后F变有害。我们固定三个顺序的U1:9和F1:9第120步，共六状态，保留完整Adam状态，比较相同下一批36新/4旧/64旧探针的当步作用。独立旧DEV64条在查看新结果前按固定哈希、面板×口令各16条锁定，不参与梯度、投影或目标选择。

## 2. 实际操作与资格

全部六状态完整，无回退。d0/d4独立恢复同一θ/Adam/RNG，按原72输入槽、分母72、微批12、全局裁剪1、AdamW1e−4直接形成候选，不把单独Adam位移相加。F0/F4是对对应提案施加原F；D4只匹配自身F4长度。每个候选独立写回FP32，评价后恢复原权重与Adam；没有串行累积，没有保存训练终点。新/旧探针/独立旧真实损失和答案优势分别记录；全部目标为单token，全词表答案评价。

共11424次序列前向，小于12000上限，12次临时Adam提案只发生在内存模型副本，完整续训更新0、候选检查点保存0、TEST读取0、新资源/任务0。重复无操作评价在全部18个状态×样本组中逐题相同，标量跨度均0；结合梯度前向差与预定精度下限，最大τ为4.7731e−8 nat/答案，局部比较用2τ判断数值可分辨性，不称统计显著。

## 3. 同状态的五主候选

表中ΔCE=更新后减更新前，单位nat/答案；负值改善。旧探针64、新题36、独立旧DEV64。各起点基线不同，不能直接把不同起点的Δ当同状态因果对比。

'''+table(mainrows,maincols)+'\n\n'
 detail+='## 4. 竞争解释的逐项更新\n\n'
 detail+='**A：当前不支持“F4比d4更伤独立旧功能”。** 六状态中独立旧损失F4相对d4为2改善、0恶化、4完全相同；三个U起点F4都不触发、等于d4，F起点43也不触发。F起点71的F4让探针略降、独立旧仍上升0.041265，说明局部保护范围不能等同独立旧保持；但它仍好于d4的+0.085813，不符合A所要求的“比d4更差”。该范围不一致仅是一个局部状态，不能推广为稳定根因。\n\n'
 detail+='**B：有限步余项确实存在并随缩放减小，但没有复现F4比d4更差的探针模式。** d4/F4的绝对余项在六状态、两候选全部随1→1/2→1/4减小。最清楚的反例是U起点71：F4=d4，最终g·d≈−0.003927，旧探针实际ΔCE=+0.000754；半步变−0.000800、四分之一步−0.000694。这支持局部一阶/有限步差异参与，且差额超过本次精度标定；但不是F额外投影造成，因为该状态根本未投影，也未证明有限步误差单独导致长期1:9劣势。\n\n'
 detail+='**C：目前最值得提高优先级。** 在三个U起点，普通d4使独立旧CE分别变化−0.043870、−0.072463、−0.004588；在对应F起点为+0.107916、−0.036755、+0.085813。每个种子的F历史起点都更不利，远超噪声；F4在当前步并不更差，却无法由一个普通当步更新抹去已形成的状态差异。它支持优先研究历史状态束，不区分当前θ与Adam矩各自贡献，也不定位历史上哪一步造成差别。\n\n'
 detail+='**D：在实际触发的两个状态，单纯缩步不能复现方向作用。** F起点29，独立旧ΔCE的d4/F4/D4为+0.107916/−0.026341/+0.107423；起点71为+0.085813/+0.041265/+0.085579。F4与D4差别超过噪声，D4非常接近d4；其余四状态F4未触发，与D4/d4相同，不能把这些无操作点当作方向无效的反证。两个活跃状态的当步新CE降幅同时变小，仍是局部旧新取舍，不是容量释放。\n\n'
 detail+='**E：当前未建立“加入旧目标让投影删掉联合学习有益分量”。** 所有六状态加入旧4后，普通d4在独立旧诊断上均优于对应d0；F起点29/71投影删除比例约9.715%/7.284%，删除分量与4旧题梯度内积为正，删除后反而更改善该旧梯度的一阶预测。所有六状态g4与g64余弦均为正（0.165—0.772），没有复现这两批旧梯度相反的模式；正夹角本身仍不能证明Adam功能效用。F4确实削弱两个状态的新题改善，但没有使旧功能比d4更差，因此只可描述当步权衡，不说删除了“有益联合分量”。本轮没有另做当步旧4完整后验目标值，不能宣布联合目标净收益。\n\n'
 detail+='**F：长期根因仍证据不足。** 当前只有固定120步、每来源每顺序一批，独立旧诊断64题且已暴露DEV；非零损失差远超重复噪声，但样本/时点总体不确定性未估计。不能扫描更多checkpoint、批次、超参数补故事，也不能由两状态活跃作用定义普遍机制。\n\n'
 detail+='## 5. 轨迹事实与局部证据怎样接上\n\n原日志对齐132个评价点、2880个逐步记录，保留0:1/1:9的U/F旧新CE、准确率、规则混淆、投影触发与理想删除比。旧准确率开始下降、U1:9恢复和U/F在120步分离都可见；其中删除比由日志g·d和||g||推导，只是理想投影量，非历史实际删除向量实测。整条轨迹未保存全词表端点logit优势，标记NOT_SAVED；本轮六状态的功能评价补充答案优势，但不补造历史曲线。\n\n'
 detail+='不同起点的基线CE已经不同。相同d4操作在F历史起点更不利，与当前投影仍可保护旧题并不矛盾：当前一步可能在补救已有劣势，而轨迹终点仍更差。这个区分削弱“终点差证明投影当步害旧”的推理，但没有证明历史一定是唯一原因。\n\n'
 detail+='## 6. 唯一后续实验建议（不启动）\n\n**在同样六个120步状态做配对的Adam矩交换单步诊断：固定各自θ，分别使用本来源与另一来源的Adam矩，保留同一批次、d4/F4与独立旧诊断。** 若固定θ后效应随矩交换明显改变，则提高Adam历史贡献解释；若主要跟θ走，则提高参数历史贡献解释；若有交互则报告交互。交换产生的是人工状态，只能定位局部贡献，仍不能解释完整240步。本轮不自动执行。\n\n[完整逐种子附录](appendix_cn.md) · [两图与说明](figures_cn.md) · [配置与采样](reproduce/plan.json) · [原资产未改动](reproduce/original_asset_immutability.json)。\n'
 # Detailed appendix full perstate norm/dot/scale/noise.
 appendix='# 完整局部诊断附录\n\n'
 appendix+='## 起点基线与Adam提案\n\n'
 for r0 in ss:
  appendix+=f"- 顺序{r0['seed']}，{r0['origin']}历史：g4/g64余弦{r0['g4_probe_cosine']:.6f}；d0裁剪前梯度范数{r0['proposal0']['raw_gradient_norm']:.6f}，d4为{r0['proposal4']['raw_gradient_norm']:.6f}；Adam提案及前后矩hash在state_summary.json，原有source121提案数值误差见CSV。\n"
 appendix+='\n## 全部功能配对差\n\n负差表示前一个候选更改善损失；同一θ/原Adam/RNG下比较，误差标定不代表统计置信区间。\n\n'+table(comparisons,[('seed','顺序'),('origin','来源'),('comparison','候选差'),('group','评价组'),('paired_CE_difference','ΔCE差'),('paired_noise_tolerance','2τ'),('direction','数值可分方向'),('paired_margin_change','答案优势变化差')])+'\n\n'
 appendix+='## 同状态加入旧目标的交互\n\n交互=(F4−d4)−(F0−d0)，局部同状态变化，不是0:1历史与1:9历史终点的交互。\n\n'+table(interactions,[(k,k) for k in interactions[0]])+'\n\n'
 appendix+='## 完整方向测量\n\nrawg4是4个有效旧题平均梯度，rawg64是64旧TRAIN探针平均梯度；梯度夹角不等于Adam位移作用。各候选actual包含最终FP32写回，removed=对应原Adam缩放位移−实际位移。\n\n'+table(dirs,[('seed','顺序'),('origin','来源'),('condition','候选'),('alpha','缩放'),('actual_displacement_norm','实际位移长度'),('actual_removed_component_norm','实际删除长度'),('removed_fraction','删除比'),('actual_probe_gradient_dot','g64·actual'),('actual_old4_gradient_dot','g4·actual'),('deleted_probe_gradient_dot','g64·removed'),('deleted_old4_gradient_dot','g4·removed'),('g4_probe_cosine','g4/g64余弦')])+'\n\n'
 appendix+='## 缩放回放\n\n1/2、1/4只缩放固定提案，不重算Adam、不重新裁剪、不寻优学习率；按计划省略缩放新题读出，只测旧探针/独立旧组。\n\n'+table(scaling,[('seed','顺序'),('origin','来源'),('candidate','候选'),('alpha','比例'),('probe_delta_CE','探针ΔCE'),('probe_first_order','探针一阶'),('probe_finite_remainder','有限余项'),('remainder_over_alpha_squared','余项/α²'),('independent_old_delta_CE','独立旧ΔCE')])+'\n\n'
 appendix+='## 无操作重复与噪声\n\n两次同状态前向全部逐题相同。τ=max(无操作span,预定1e−8×(1+|基线CE|),探针梯度前向和no_grad前向的CE差)。后者只适用探针，不将原作业GPU与当前环境的差用来放大τ；原121步复放误差另外保留。\n\n'+table(noise,[('seed','顺序'),('origin','来源'),('group','组'),('noop_CE_1','基线CE'),('noop_span','重复差'),('grad_forward_no_grad_gap','梯度/评测差'),('noise_tolerance','τ')])+'\n\n'
 appendix+='## 轨迹读取范围与缺失\n\ntrajectory_alignment_132.csv保留全部旧/新CE与准确率，trajectory_step_logs_2880.csv保留训练逐步探针、触发和理想删除比。不同步探针不同，不能按这些均值组成固定样本loss路径。整条轨迹答案logit优势未保存，当前只在六状态实际测量，未反推。无追加续训、无额外检查点、无TEST。\n'
 # English canonical summary aligned with the measured result.
 en='''# Local F effects versus origin-state history

Purpose: explain the R06 zero-replay versus1:9endpoint pattern by separating localcounterfactuals from differenttraining histories. Sixpreselected U1:9/F1:9step120states retain completeAdam120/RNG and identicalnext36new/4old/64probe batches. IndependentoldDEV64was fixedhash16perpanel×command before outcomes. Original72slotdenominator,clip1,AdamWlr1e-4andFP32writeback reproduced;2independentAdamproposals/state and deterministicF0/F4/D4transformations, everybranchrestored. No continuation, no candidate checkpoints, noTEST/resourceallocation.11424/12000sequenceforwards.

**Finding: no state shows F4 harming independentoldloss relative to d4.** Uorigin all3andForigin43do not triggerF4, hence exactd4=F4=D4. Forigin29/71triggerF4 and improve botholdprobeandindependentoldloss relative to d4 while reducing the newlossimprovement. D4staysclosetod4, so those2activecaseshave direction-specificlocaleffect beyondshrinkage, notcapacityrelease.

'''+table(mainrows,[(k,k) for k in ['seed','origin','candidate','probe_delta_CE','independent_old_delta_CE','new_delta_CE']])+'\n\n'
 en+='Ordinaryd4 independentoldΔCEfromUorigins=-.043870,-.072463,-.004588;fromForigins=+.107916,-.036755,+.085813. EachForiginislessfavorable than correspondingUorigin, raisingjointstate/historypriority, withoutseparatingparametersfromAdammoments. F4Forigin71keepsprobeCEslightlylowerbutindependentoldCErises+.041265, stillbetterthand4+.085813; scopegapexistslocallybutbranchA(strictF4worsethand4)notmet.\n\n'
 en+='Finiteabsolute remaindersshrinkwith1,.5,.25inall12state×candidatecases. Uorigin71hasnegativefirstorder−.003927butpositiveactualprobechange+.000754;halfstepturnsnegative. F4=d4there, so thisdoesnotshowprojection-specificharm. BranchB(worseF4thand4probe)notobserved. Allg4/g64cosinespositive(.165–.772);no rawopposite-gradientpattern. Removedg4dotspositive in2activeF4cases, so no evidencehereforremovinganold-beneficialcomponent. Newlearningcostremains.\n\n'
 en+='Two no-op evaluations giveexactper-itemagreement atall18state×groups;maximumprecisionτ4.7731e−8nat/answer;comparisonuses2τ, notstatisticalCI.6checkpointbefore/afterSHAidentical, modelnon-targetbytesunchanged. Oldtrajectorylosses/accuracy/confusionandprojectionlogsareassociational; fulltrajectoryendpointlogitmarginsNOT_SAVED. Fixed6stateones-stepcannotexplain240stependpointsorsweepstate/batchpopulations.\n\n'
 en+='Only proposedfollowup(notrun): pairedAdam-momentexchange atfixedoriginaltheta andsamebatch, comparingnative/cross-originmoments with d4/F4 andindependentoldloss. Effectfollowingmomentsraisesmoment-historycontribution; effectfollowingtheta raisesparameterhistory; artificialhybridstatesstilllocal.\n\n[Chineseone-page/fullrecord](summary_cn.md),[completeappendix](appendix_cn.md),[figures](figures_cn.md),[plan](reproduce/plan.json).\n'
 onepage='''# F为何在1:9较差：先分开当步作用与历史

**结论。** 当前固定六状态没有复现“加入旧目标后，F当步删掉了有利于旧功能的更新”；更值得优先研究的是已经积累的参数/Adam历史，不能从终点输赢直接推出投影当步有害。

**怎么检验。** 三个续训顺序各取U1:9和F1:9的第120步，完整恢复Adam；用相同下一批36新/4旧与64旧探针，对比d0、d4、F0、F4、D4。另用先锁定的64旧DEV作独立诊断，不参与投影。缩放1、1/2、1/4只回放同一位移。总计11424次序列前向，原资产未改，未续训、未保存候选终点、未读TEST。

**已经排除什么。** 在这六状态中，F4相对d4的独立旧损失为2改善、4完全相同、0恶化；三个U来源均未触发F4，F来源43也未触发。不能把该时点解释为“4旧题使投影突然伤旧”，也未见4旧题与64探针梯度相反。无操作重复逐题相同，观察到的非零差别超过本轮精度标定；不是由一个极小正值下结论。

**目前更支持什么。** 同样的普通d4在U来源下，对独立旧CE的改变为−0.0439、−0.0725、−0.0046；在F来源下为+0.1079、−0.0368、+0.0858，三个顺序均更不利，历史状态差异的解释优先级上升。实际触发F4的两个F来源状态中，方向投影改善旧损失但减慢新学习，单纯缩步D4未复现，说明局部方向作用存在。所有缩放的绝对有限步余项均减小；这是有限步偏差参与的证据，不是长期根因证明。

**仍不能区分什么。** 参数与Adam矩各自的历史贡献未分离；120步一批不能解释240步整条轨迹，也不能排除其他时点存在局部冲突。F来源71还出现探针略改善而独立旧损失上升，提示保护范围有限，但它仍比d4更好。本轮唯一后续建议是：固定现有θ，交换同种子U/F的Adam矩做同批单步对照，分辨效应主要跟随θ还是矩；只是建议，不自动执行。
'''
 (R/'summary_cn.md').write_text(detail);(R/'summary.md').write_text(en);(R/'appendix_cn.md').write_text(appendix);(R/'one_page_cn.md').write_text(onepage)
 notes='''# 两张图与解释

## 图1：不同轨迹的学习过程

![原轨迹](figures/figure1_trajectory.png)

问题：旧行为何时下降、恢复，以及U/F何时分离？
观察：原1:9轨迹中U在中后期恢复旧表现，而F的120步状态和最终表现更差。
判断更新：固定120步可以检查已分离历史下的当步作用，不能把曲线相关直接称为投影造成当步有害。
边界：线为共用一个旧模型的三续训顺序均值，色带为最小到最大值而非置信区间，虚线120是事前指定局部诊断点。

## 图2：同状态单步反事实

![同状态候选](figures/figure2_same_state.png)

问题：恢复同一θ和Adam后，F4相对普通d4及幅度控制D4怎样影响旧新损失？
观察：三个U来源和F来源43三候选相同，F来源29/71的F4改善旧损失但新损失下降较少，D4更接近d4。
判断更新：当前当步对照没有支持F4伤旧，历史状态束差异应优先分解，两个活跃状态也显示局部方向作用超过单纯缩步。
边界：每个柱是一个固定状态和固定批次的真实CE变化，单位nat/答案且负值改善，不是独立模型统计，也不能解释240步长期结果。
'''
 (R/'figures_cn.md').write_text(notes)
 # Copy compact reproducible evidence; per-itemdata is small but stays execution-side.
 outtab=R/'tables';outtab.mkdir(exist_ok=True);outfig=R/'figures';outfig.mkdir(exist_ok=True);repro=R/'reproduce';repro.mkdir(exist_ok=True)
 for p in (O/'tables').glob('*.csv'):
  if p.name not in ['per_item_losses.csv','trajectory_step_logs_2880.csv']:shutil.copy2(p,outtab/p.name)
 for p in (O/'figures').glob('*'):shutil.copy2(p,outfig/p.name)
 for p in V.glob('*.json'):shutil.copy2(p,repro/p.name)
 for name in ['local_dynamics_20261026.py','local_dynamics_summarize_20261026.py']:shutil.copy2(E/'ops'/name,repro/name)
 shutil.copy2(O/'receipt.json',repro/'execution_receipt.json');shutil.copy2(O/'state_summary.json',repro/'state_summary.json')
 write(R/'coverage.json',{'log_alignment':'DONE','six_states_with_fullAdam':'DONE','five_main_candidates_each':'DONE','scale1_half_quarter_oldgroups':'DONE','scaled_newloss':'NOT_RUN_BY_PLAN_budget','same_state_noop':'DONE','independent_old_sampling':'DONE','source_assets_before_afterSHA':'PASS','new_continuation_training':0,'candidate_checkpoint_exports':0,'forward_sequences':11424,'forward_budget':12000,'TEST':'NOT_READ','extra_resources_or_jobs':0,'fulltrajectorylogitadvantages':'NOT_SAVED','causaltheta_versus_Adam_history':'NOT_RUN suggestedonly','furtherstate_orhyperparamsearch':'NOT_RUN'})
 write(R/'figure_provenance.json',{'figure1_source':'tables/trajectory_alignment_132.csv','figure1_aggregation':'3continuationordermean,minmaxband;oneoldparent','figure2_source':'tables/main_candidates_30.csv','figure2_aggregation':'eachactualstate, noaveraging','max_claim':'localcounterfactualeffects,anddifferent-statehistorybundlesnotseparatedcomponents','script_sha256':sha(__file__),'no_causal_titles':True})
 (R/'reproduce/README_cn.md').write_text('# 复现入口\n\nlocal_dynamics_20261026.py复用原source/engine.py与retention_r05_v1.py的模型、Adam、梯度与投影。plan.json锁定六权重路径、下一批记录与独立旧DEV64条；freeze.json封存运行前源码/配置/协议。原资产SHA前后见original_asset_immutability.json；source_step121_replay_6.csv复放原下一步提案作数值检查。\n\n当前结果已完成，不自动重复运行。完整逐题loss与2880逐步日志仍在执行侧analysis/local_dynamics_20261026/tables，轻量CSV与源码回执在本目录。没有新训练终点权重。实际前向11424序列，剩余576不继续使用。\n')
 # Three completed internal audit outcomes, explicit numerical scope.
 with (R/'internal_audits.md').open('a') as f:f.write('\n## 完成核验\n\n同状态5主分支+4缩放分支均独立恢复，六状态各1904序列。六原状态完整Adam且120步无回退，原资产前后SHA相同，非目标参数字节未改。18组重复无操作逐题相同；数据/功能/数值三项PASS。当前结果没有支持E或B的特定有害F4模式，C优先级提高但θ/Adam不可分；不追加检查点寻找支持。\n')
 # Canonical source pointers, no historical source mutation.
 print(json.dumps({'status':'PASS','summary':str(R/'summary_cn.md'),'onepage':str(R/'one_page_cn.md'),'F4independent_old':fixed['F4_vs_d4_independent_old'],'history_differences':history,'noise_max':noise_max},ensure_ascii=False))
if __name__=='__main__':main()
