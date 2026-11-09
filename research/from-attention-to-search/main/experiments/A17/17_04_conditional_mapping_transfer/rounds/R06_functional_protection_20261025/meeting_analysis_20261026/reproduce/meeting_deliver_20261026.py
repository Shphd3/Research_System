from pathlib import Path
import json,csv,hashlib,datetime,shutil,math,collections,zipfile,re
E=Path(__file__).resolve().parents[1];O=E/'analysis/meeting_20261026';S=Path('/data/250010109/Research_System');OWN=json.load(open(E/'provenance/ownership.json'));R=Path(OWN['round']);D=R/'meeting_analysis_20261026';D.mkdir(exist_ok=True);T=D/'tables';T.mkdir(exist_ok=True);F=D/'figures';F.mkdir(exist_ok=True);P=D/'reproduce';P.mkdir(exist_ok=True)
def read(p):return json.loads(Path(p).read_text())
def rs(n):return list(csv.DictReader(open(O/'tables'/n)))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def table(rows,cols):
 def fmt(v):
  if v is None:return 'MISSING'
  if isinstance(v,float):return f'{v:.3f}'
  return str(v)
 return '\n'.join(['| '+' | '.join(n for k,n in cols)+' |','| '+' | '.join('---' for _ in cols)+' |']+['| '+' | '.join(fmt(r.get(k,'MISSING')) for k,n in cols)+' |' for r in rows])
def typed(rows):
 out=[]
 for r in rows:
  a={}
  for k,v in r.items():
   try:a[k]=float(v) if any(z in v for z in ['.','e','E']) else int(v)
   except (ValueError,TypeError):a[k]=v
  out.append(a)
 return out

def main():
 now=datetime.datetime.now(datetime.timezone.utc);assert now.timestamp()<datetime.datetime(2026,10,26,1,40,tzinfo=datetime.timezone.utc).timestamp(),'analysis cutoff reached; only existing outputs may be curated'
 result=read(O/'results.json');rep=read(O/'provenance/representation_receipt.json');assert rep['status']=='PASS' and rep['checkpoint_count']==9 and rep['sequence_forwards']==1152
 endpoints=typed(rs('01_endpoints_36.csv'));means=typed(rs('01_method_means_12.csv'));contr=typed(rs('01_all_vs_U_seed_27.csv'));cm=typed(rs('01_all_vs_U_means_9.csv'));behavior=typed(rs('02_rule_mode_endpoint_seed12.csv'));bm=typed(rs('02_rule_mode_endpoint_mean4.csv'));ng=typed(rs('03_finite_check_summary_12.csv'));numeric=typed(rs('03_F_finite_checks_90.csv'));op=typed(rs('01_operating90_36.csv'));reps=typed(rs('04_representation_summary_9.csv'))
 assert len(endpoints)==36 and len(behavior)==12 and len(numeric)==90 and result['F_raw_loss_increases']==69 and result['F_final_positive_beyond_tolerance']==0
 # Curated tables only; raw105600pair rows remain execution-side.
 selected=[p for p in (O/'tables').glob('*.csv') if p.name!='02_rule_mode_pairs_105600.csv']
 for p in selected:shutil.copy2(p,T/p.name)
 for p in (O/'figures').glob('*'):shutil.copy2(p,F/p.name)
 for name in ['meeting_analysis_20261026.py','meeting_mode_readout_20261026.py','meeting_plot3_refine.py','meeting_deliver_20261026.py']:shutil.copy2(E/'ops'/name,P/name)
 for p in (O/'provenance').glob('*.json'):shutil.copy2(p,P/p.name)
 shutil.copy2(O/'real_paired_examples.json',D/'real_paired_examples.json')
 # Source audit names actual lines; add inherited deterministic/eval lines.
 src=read(O/'provenance/03_measurement_object_audit.json');src['inherited_source_locations']={}
 for p in [E/'source/retention_r05_v1.py',Path('/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/source/carriers.py')]:
  lines=p.read_text().splitlines();src['inherited_source_locations'][str(p)]={'sha256':sha(p),'lines':[{'line':i+1,'source':line.strip()} for i,line in enumerate(lines) if any(t in line for t in ['torch.use_deterministic_algorithms','allow_tf32 = False','.eval().requires_grad_','class CachedAnswerLM','F.cross_entropy'])]}
 write(P/'03_measurement_object_audit.json',src)
 # Full facts and all required negative results.
 summary='''# 已学行为怎样继续有效：监督组织与局部约束的区别

**判断：在固定新题学习机会下，正确旧监督对本轮功能保持的作用最明确；参数方向限制和局部旧损失一阶约束没有同等作用。** 本轮失败主要表现为旧模式采用新规则，而非广泛不能输出列表词；F的局部条件在数值容差内落实，但仍不足以保证有限步及长期行为。以下机制更新为AI有界判断，研究者的科研接受与总问题关闭未被替代。

原直觉是复用已学计算，让新增区别继续学习。本轮只检验其中的前提：旧行为在什么学习安排下继续有效。任务是有明确模式标记的两套可兼容列表规则：模式一甲取首、乙取尾，模式二反转；不是数学知识层级形成实验，也未识别可复用计算子空间。Qwen3-0.6B Base只更新最后一层查询/键/值/输出四张注意力矩阵，三个续训顺序共用一个已学旧规则的起点。

## 1. 旧监督改变了什么

每步固定36新题、36旧输入槽，旧有效目标为0/4/36，训练损失统一除72。旧新监督比分别0:1、1:9、1:1。全部36条轨迹都完成240步、8640次新答案曝光，新平均损失系数始终36/72=0.5。旧目标曝光分别0/960/8640；每个方法每步另读64旧TRAIN探针，F/D用这些旧标签。监督档同时改变旧目标次数和总损失权重，不能叫纯频率或自然feature频率实验。

U为普通AdamW实际位移；S衰减初始完整权重每矩阵Top-16秩一系数的位移，保留R05原1200步调度前240步；F投影掉当前旧TRAIN探针损失的一阶有害分量；D在自身状态只缩小候选位移长度、保持方向。全部方法用相同数据顺序、探针规则和新项系数。

'''
 summary+=table(means,[('old_slots','有效旧槽/36'),('method','方法'),('old_accuracy_pct','旧准确率 %'),('new_accuracy_pct','新准确率 %'),('old_ce_nats','旧CE'),('new_ce_nats','新CE')])+'\n\n'
 summary+='交叉熵（Cross Entropy，CE）是正确答案概率的负自然对数，单位nat/答案，越低越好。表为三个续训顺序等权平均；旧/新DEV各800题、四格各200；全词表151936输出取最大值；DEV已暴露，本轮TEST未读取。逐种子准确率与损失完整列在[附录](appendix_cn.md)。\n\n'
 summary+=table(cm,[('old_slots','旧槽'),('comparison','相对U'),('old_accuracy_pct','旧差 pp'),('new_accuracy_pct','新差 pp'),('old_ce_nats','旧CE差'),('new_ce_nats','新CE差'),('old_positive_seeds','旧正向种子数'),('old_negative_seeds','旧负向种子数')])+'\n\n'
 summary+='**观察。** U旧表现随旧监督从0.125%升至93.125%、99.708%，新表现均约99%；因为新题曝光与新loss系数相同，可排除“仅因减少新题曝光”这一解释。F−U旧收益为+11.167、−24.875、+0.042个百分点，三个种子均不是监督越少优势越大的单调序列。1:9档F−U旧差逐种子为−30、−9.625、−35个百分点，旧CE也全部更差。S在1:1档旧准确率三种子均略高于U，均差仅+0.208个百分点，且新均差−0.292；这限制“所有设置下S均无差别”的说法，但未达到5个百分点的预定实用门槛。\n\n'
 summary+='**同等新学习标准。** 使用原先冻结的“连续两次计划评价新平均准确率≥90%”的第二点，不插值、不改240主终点。0槽U三种子均在180步确认，F在240/180/240步确认，说明F有学习成本；1:9档U与F均在180步确认，此时旧准确率平均88.167%与59.375%，F仍明显较差，不能只用未达到同一达标标准解释终点差异。该标准是相同门槛，不是精确匹配的新准确率；完整损失、曝光和计算秒见附录。\n\n'
 summary+='## 2. 失败是怎样的输出错误\n\n同一续训顺序、列表和口令配对，只改变模式标记。反事实新答案来自配对数据标签，并用原生成器FIRST/LAST规则复核，不从预测猜规则。旧题互斥分为旧规则正确、新规则端点、另一列表项、其他/无效输出；同目标样本单列并排除规则混淆。实际三词各异，全部目标不同，排除0题。\n\n'
 summary+=table(bm,[('method','方法'),('old_slots','旧槽'),('old_rule_correct_pct','旧答对 %'),('new_rule_endpoint_pct','旧答新规则 %'),('other_list_item_pct','其他列表项 %'),('other_output_or_invalid_pct','列表外/无效 %'),('both_correct_pct','模式成对均正确 %'),('same_prediction_pct','两模式同答 %')])+'\n\n'
 summary+='**观察。** U零旧目标有99.833%旧题回答新规则端点、两模式同答99.750%；U1:9的新规则端点错误仅6.792%，两模式均正确92.167%。F零旧目标和F1:9的同类错误分别87.333%与28.708%。四条件所有种子列表外/无效词编号均为0；其余错误主要是中间词。每种子U1:9相对U0都减少新规则混淆，F1:9相对U1:9均混淆更多；面板和口令分项完整保留。\n\n'
 summary+='这里的规则混淆是输出行为描述。成功与失败主要是同类错误程度不同，不足以宣称内部机制不同或旧电路被删除。模型只输出单个词编号，没有自由格式生成；“无效格式”不能被独立测试，只能查非法词编号，本轮为0。\n\n'
 summary+='**已有时间点。** 起点旧准确率100%，但两模式99.875%同答；模型尚未掌握新模式的反转条件规则，不能说它原先已会按模式正确切换。U0终点从大多同答旧端点变为大多同答新端点。U1:9在64/120/240步旧准确率31.042/53.292/93.125%，两模式均正确11.250/49.583/92.167%；F1:9同点分别旧41.208/19.458/68.250%、成对均正确10.500/13.500/66.708%。这些保存点显示U后续建立更好的模式对应，不能插补未保存步骤或直接认定因果环节。\n\n'
 summary+='## 3. F到底约束了什么\n\n令g是当前64条旧TRAIN探针的平均答案损失梯度，d是裁剪训练梯度后Adam提出的参数位移。F在g·d>0且||g||²>1e−24时用dF=d−g(g·d)/||g||²，否则保留d。源代码确认：前后损失与梯度用同一order[probe]、同一64条题、同一分母64和探针微批16，参数起点相同；网络子模块保持eval，FP32且启用确定性算法。内积记录的是最后FP32写回之后的actual=p_after−p_before；不是未经修改的Adam提案。Adam矩状态保留，训练裁剪在提出d之前，过滤之后没有额外裁剪或衰减。\n\n'
 summary+='**数值观察。** 90个固定F检查点，75次触发投影，15次本来不需投影；近零梯度触发0次。最终实际内积原始正值48次，最大约2.356e−7，但没有一次超过原有事后理想位移审计容差加FP32写回误差的上界。因而不能说实数意义下最终内积恒≤0；更准确是“未发现超出当前数值容差的约束违背”。本轮没有事后扩大训练阈值。\n\n'
 summary+='容差为tau0=max(1e−10,|g·d|×1e−5)，沿用既有事后数值审计而非伪称事前冻结的科学门槛；写回误差上界为||g||·||actual−desired||，再加保守FP64内积求和误差。原始符号、每点容差、位移范数与余项均在[90点表](tables/03_F_finite_checks_90.csv)，全360点对照另列。没有保存同状态无操作/重复loss的噪声标定；梯度前向与no_grad前向可能选择不同内核，所以细小正值不称统计显著。\n\n'
 summary+=table([r for r in ng if r['method']=='F'],[('old_slots','旧槽'),('checks','检查数'),('projection_trigger_n','投影次数'),('raw_positive_final_dot_n','实际内积原始正值'),('positive_final_dot_beyond_tolerance_n','超容差正值'),('raw_actual_loss_increase_n','实际loss原始上升'),('mean_actual_loss_change','平均实际变化'),('max_actual_loss_change','最大实际变化')])+'\n\n'
 summary+='**判断边界。** 参数写回舍入不足以解释记录中的较大有限步差额，但当前数据不能把余项唯一归于曲率。局部一阶条件没有构成真实有限步loss或240步行为保证；69/90只是固定检查步的原始上升计数，不是所有更新的比例，也不能单独解释1:9下F为何弱于U。U1:9同样有16/30次检查loss上升，却有更好的终点。随步更换探针，不能把每步探针loss连成同一批题的持久loss曲线；尚未保存“当前探针总体保持但整DEV下降”的完整对齐证据，故不把探针代表性不足说成已证实原因。\n\n'
 summary+='## 4. 有限模式表征读出\n\n在查看表征结果前锁定64对DEV输入，先覆盖九个条件已有正确/错误情况，再按固定哈希在两个面板×两口令各取16对；这是事后按正确性分层的诊断样本，不代表完整DEV总体。读取三个种子的U0、U1:9、F1:9共9个终点，每模型128序列，合计1152序列；没有训练、其他任务或额外资源申请。检查位置为答案生成前最后一个前缀token，测末层q_proj归一化输入与o_proj原始输出。每个模型内部比较模式一/二差异，并计算logit(旧正确词)−logit(新规则词)；两目标均已验证单token。\n\n'
 summary+=table(reps,[('seed','种子'),('method','方法'),('old_slots','旧槽'),('input_mode_gap_ratio','输入模式差/基准'),('output_mode_gap_ratio','输出模式差/基准'),('old_mode_old_minus_new_logit','旧模式旧−新logit'),('new_mode_old_minus_new_logit','新模式旧−新logit')])+'\n\n'
 summary+='输入模式差异比在全部模型相同，约0.08188，因为上游和输入归一化被冻结；这只说明模式标记在所测输入留下可测差别，不证明模型已经正确利用。U0的输出模式差异仍非零（0.0703—0.0893），但旧/新输入的答案优势都指向新规则；U1:9在旧模式转为正优势、新模式保持负优势。F1:9的输出模式差异比在种子29/71反而大于U1:9，旧表现却更差，所以“模式表示差得更大就更会切换规则”没有稳定对应；不继续扫描几何指标。全部样本预测与原评价逐项相同，CE最大误差3.815e−5，小于沿用的2e−4复放容差。\n\n'
 summary+='## 5. 从观察到下一项决定\n\n**观测事实：** 固定新曝光和新项系数，直接旧监督显著改善旧行为；失败主要是旧模式回答新规则；局部一阶约束在数值范围落实却不保证有限步或长期保持；所测模式差异存在但大小不决定规则正确使用。\n\n**与结果相容的解释：** 正确旧监督帮助维持/形成模式与规则的对应；局部平均梯度约束未充分维护这种输入条件下的功能关系。这里“维持/形成”刻意同时保留，因为旧起点未学会新模式反转。\n\n**待验证假设：** F可能改变了后续有利的学习路径，64探针与4条旧目标可能存在抽样冲突，有限步曲率与Adam状态也可能参与；本轮未分别识别，不能写成根因。\n\n**AI建议：** 下一步主问题应优先指向“正确的输入条件怎样持续组织功能更新”，局部约束的有效范围是必须保留的竞争诊断；新增支持来自模式配对错误及有限模式读出，而不只是U准确率更高。暂不把保护方向搜寻或新MoE作为必然下一步。本轮不提出额外自动运行；研究者后续选择仍Unknown。\n\n[一页组会主稿](../../../../../../../../../../daily_research_reports/1026/meeting_report/meeting_brief_A17_R06_functional_protection_cn.md)（便携副本若链接不可用，以同包meeting_brief_cn.md为准） · [完整附录](appendix_cn.md) · [三图与四句图注](figures_and_captions_cn.md) · [执行/未执行清单](coverage_cn.md)。\n'
 # Use verified absolute main link instead of speculative relative navigation.
 brief=S/'daily_research_reports/1026/meeting_report/meeting_brief_A17_R06_functional_protection_cn.md'
 summary=summary.replace('../../../../../../../../../../daily_research_reports/1026/meeting_report/meeting_brief_A17_R06_functional_protection_cn.md',str(brief))
 (D/'summary_cn.md').write_text(summary)
 # Full appendix: every run, contrasts, same-standard points and all seeds panels.
 app='# 必要附录：任务、逐种子数值与判据核验\n\n'
 app+='## A. 任务与监督\n\n输入“模式：一。口令：甲。列表：黄 红 鸟。答案：”目标黄；同列表模式二口令甲目标鸟。乙则相反。原DEV两面板分别检验新排列/新无序组合；每面板×口令×模式200题。共享参数在可见模式下可以表达两套规则，没有标签矛盾。模型Qwen3-0.6B Base，末层Q/K/V/O6291456参数，FP32AdamW1e−4，初始空矩状态；所有条件同一旧终点。旧/新全词表准确率与CE分开，不合成总分。\n\n'
 app+='## B. 四方法×三档×三顺序的240步终点\n\n'+table(endpoints,[('seed','续训顺序'),('old_slots','旧有效槽'),('method','方法'),('new_targets','新曝光'),('old_accuracy_pct','旧 %'),('new_accuracy_pct','新 %'),('old_ce_nats','旧CE'),('new_ce_nats','新CE')])+'\n\n'
 app+='## C. 每个种子的保护方法减U\n\n差值准确率单位为百分点，CE单位nat/答案；正旧准确率差表示相对保留更多。\n\n'+table(contr,[('seed','顺序'),('old_slots','旧槽'),('comparison','方法−U'),('old_accuracy_pct','旧差 pp'),('new_accuracy_pct','新差 pp'),('old_ce_nats','旧CE差'),('new_ce_nats','新CE差')])+'\n\n'
 app+='## D. 相同新学习门槛的次要比较\n\n固定连续两次计划评价新平均准确率≥90%，使用第二次读数，不插值。所有36条均达到；步骤相同不表示新准确率精确相同。更新计算秒来自逐步记录，排除DEV评价、存盘与首次U工程恢复检查；0槽F的部分顺序确认更晚。\n\n'+table(op,[('seed','顺序'),('old_slots','旧槽'),('method','方法'),('step','确认步'),('new_targets','新曝光'),('old_accuracy_pct','旧 %'),('new_accuracy_pct','新 %'),('old_ce_nats','旧CE'),('new_ce_nats','新CE'),('probe_gradient_labels','探针梯度标签'),('update_compute_seconds','更新计算秒')])+'\n\n'
 app+='## E. 终点模式配对逐种子结果\n\n每行800对；旧题分母800，两个面板各400。旧新同目标排除0题。所有其他输出/非法词编号0；并非测试自由文本格式。\n\n'+table(behavior,[('seed','顺序'),('method','方法'),('old_slots','旧槽'),('old_rule_correct_n','旧正确数'),('new_rule_endpoint_n','旧答新规则数'),('other_list_item_n','其余列表项数'),('other_output_or_invalid_n','其他输出数'),('both_correct_pct','两模式均对 %'),('same_prediction_pct','两模式同答 %')])+'\n\n'
 app+='完整面板/口令分项与11个保存点见tables/02_rule_mode_stats_all.csv，互斥计数之和均等于原分母。105600条模式配对行保留在执行侧analysis/meeting_20261026/tables/02_rule_mode_pairs_105600.csv，避免把重复评价当独立样本。\n\n'
 app+='## F. 90个F检查点逐点数值\n\n实际内积是最终权重写回后位移；tau包括旧审计理想位移容差、Cauchy写回误差上界与保守FP64求和误差。它是事后数值审计，不是新的科学显著性阈值。完整精度的三个内积、g²、候选/理想/实际范数、前后loss、余项和容差全部在CSV；下表用科学记数保留小量。没有同状态重复loss噪声标定，微小正值不称显著。\n\n'
 cols=[('seed','顺序'),('old_slots','旧槽'),('step','步'),('g_dot_before','保护前g·d'),('g_dot_ideal_after','理想后'),('g_dot_final_actual','实际后'),('final_actual_tolerance','容差'),('actual_displacement_norm','实际位移范数'),('actual_loss_change','实际Δloss'),('finite_remainder','余项')]
 small=[]
 for r in numeric:small.append({k:(f'{r[k]:.6e}' if k not in ['seed','old_slots','step'] else r[k]) for k,n in cols})
 app+=table(small,cols)+'\n\n'
 app+='## G. 局部代表性与不能裁定的内容\n\n每步探针重新采样，不能把不同步探针loss当作同批样本的长期保持曲线。虽然有单步loss下降而终点旧准确率很低的实例，这不足以断定是探针代表性而非有限步与路径造成。没有梯度冲突分解、曲率单独操纵、Adam矩匹配长程反事实，也没有内部电路删除/完整性的证据。\n\n'
 app+='## H. 有限模式读出与真实样例\n\n'+table(reps,[('seed','顺序'),('method','方法'),('old_slots','旧槽'),('sample_pairs','配对数'),('old_accuracy_pct','抽样旧 %'),('new_accuracy_pct','抽样新 %'),('input_mode_gap_ratio','输入差比'),('output_mode_gap_ratio','输出差比'),('old_mode_old_minus_new_logit','旧模式答案优势'),('new_mode_old_minus_new_logit','新模式答案优势')])+'\n\n'
 app+='输入/输出差比是同模型内两模式向量差的长度，除以两原向量平方长度平均的平方根；不是跨模型知识距离。答案优势为旧正确端点logit减新规则端点logit，同一输入两答案的log概率差与此相同。正值偏旧端点，负值偏新端点。该正确/错误分层抽样不是完整DEV性能估计，图1/图2始终使用全DEV。锁定文件和9权重身份、1152序列回执见reproduce/。\n\n'
 examples=read(O/'real_paired_examples.json')
 for ex in examples:
  a=ex['pair_conditions'];app+='### '+ex['label']+'，顺序'+str(a[0]['seed'])+'\n\n'
  app+='事后按该类别最小record_id选取的真实例子，只用于说明。输入列表与口令相同，只改变模式。\n\n'
  app+=table(a,[('method','方法'),('old_slots','旧槽'),('old_prefix','旧模式输入'),('old_target_word','旧正确'),('old_prediction_word','旧预测'),('new_target_word','新正确'),('new_prediction_word','新预测')])+'\n\n'
 app+='## I. 推理复核\n\n1. 事实：同新曝光与同新loss系数成立，U随旧监督改善；不能说纯频率，因为旧目标权重也变。\n2. 事实：错误主要是相反规则端点，同答比例高；允许命名条件规则混淆，不推出电路删除。\n3. 数值：当前容差内实际内积无明显违背，loss仍升；允许说一阶条件不足，不唯一识别曲率。\n4. 表征：非零模式差异不等于正确使用，F差异更大也可更差；停止用几何大小解释机制，不追加扫描。\n5. 决定：AI建议优先条件功能维护，局部保护范围仍为竞争诊断；科研接受与下一项实验由研究者决定。\n'
 (D/'appendix_cn.md').write_text(app)
 # Each figure has exactly four narrative sentences, external to image.
 notes='''# 三张主图与四句说明

## 图1：旧监督与更新方式

![旧监督与更新方式](figures/figure1_supervision_methods.png)

问题：新题曝光与新损失系数相同时，旧监督和更新方式怎样改变旧新表现？
观察：U旧准确率随监督从0.125%升到93.125%和99.708%，F相对U的旧收益依次+11.167、−24.875、+0.042个百分点，新准确率总体约99%。
判断更新：正确旧监督组织有明确作用，而当前F只在零旧重放目标档有有限相对收益，未形成单调频率规律。
边界：这是共享同一旧模型的三个续训顺序均值，旧监督次数和目标权重同时改变，不能外推为自然feature频率规律。

## 图2：旧规则错误与模式切换

![规则混淆](figures/figure2_rule_confusion.png)

问题：失败主要是不能输出列表词，还是在旧模式选择了新规则？
观察：U0有99.833%旧题选择新规则端点，U1:9降至6.792%，F1:9仍为28.708%，四条件列表外输出均为0。
判断更新：输出证据支持具体的条件规则混淆描述，正确旧监督显著改善模式与答案的对应。
边界：每条件每顺序800对、旧新同目标排除0题，右侧成对均正确与两模式同答是两个独立统计，不能由此证明内部旧计算被删除或不同条件采用不同电路。

## 图3：局部预测与有限步结果

![一阶预测与实际loss](figures/figure3_first_order_finite_loss.png)

问题：F对最终实际位移的一阶约束是否落实，落实后是否保证旧探针损失不升？
观察：左图保留全部90个F检查点且实际loss原始上升69次，右图的48个原始正内积均远低于各自数值容差。
判断更新：没有发现超出当前数值审计范围的约束违背，但局部一阶条件不足以保证有限步loss或长期旧行为。
边界：横纵轴分别是最终实际一阶预测与同批探针真实损失差，单位nat/答案，容差是事后审计且缺少重复loss噪声标定，差额不能唯一归因于曲率。
'''
 (D/'figures_and_captions_cn.md').write_text(notes)
 # One-page main speaking report, five paragraphs and minimal numerical table.
 # Preserve the previous user-owned working draft rather than deleting it.
 if brief.exists():
  target=O/'provenance/meeting_brief_before_0900_analysis_cn.md'
  if not target.exists():shutil.copy2(brief,target)
 maintext='''# 已学行为怎样继续有效：监督组织与局部保护

**会议问题。** 我们希望复用已学计算，让新增区别继续学习；关键前提是旧行为怎样在后续更新中继续有效。本轮的有界判断是：持续提供正确旧监督，比当前参数限制或局部旧loss不增的一阶约束，更稳定地维持了旧新规则的正确使用。

**已有证据。** A17是带模式标记的两套可兼容三词列表规则：模式一甲取首、乙取尾，模式二反转。共享参数混训可以共存，纯新续训会丢失旧行为；原Top-16保护未解决该问题。我们尚未找到可复用计算子空间，本轮也不是数学知识层级形成实验。

**本轮唯一问题。** 固定每步36条新题、损失分母72及240步，共8640次新曝光，改变旧有效监督0/4/36条，比较普通U、Top-16衰减S、旧损失梯度投影F及仅缩步长D。36条轨迹全部完成，三个顺序共用一个旧模型；全部方法另读64条旧TRAIN探针，F/D使用这些标签，因此0:1仅指训练目标没有旧重放项。

**结果如何更新判断。** U旧／新准确率随旧新监督0:1、1:9、1:1分别为0.125%／99.833%、93.125%／99.042%、99.708%／99.458%；F为11.292%／98.792%、68.250%／98.208%、99.750%／98.792%。F在零旧目标档有有限收益，1:9档三个顺序却全部弱于U，且同达90%新学习门槛时仍较差；没有单调频率规律。新增逐题证据表明，U0主要把旧题答成新规则（99.833%），U1:9降至6.792%，F1:9仍28.708%，列表外输出均为0。90个F检查点中实际最终内积没有超数值容差的违背，但69次实际探针loss上升；9个终点的有限读出还显示模式差异存在，却不保证模型正确使用，且差异更大不一定表现更好。

**边界与下一步。** 观测支持“旧监督组织与局部保护并不等价”，并把失败具体化为条件规则混淆；它不能说明旧电路删除或必须分专家。旧监督次数同时改变旧目标权重，局部有限步误差、探针代表性与学习路径尚未分离。**AI建议优先研究输入条件怎样持续组织正确功能更新，同时把局部约束有效范围作为竞争诊断；暂不继续追逐大奇异方向或直接扩展MoE。** 支持该选择的新证据是模式配对错误、同批有限步核验及模式差异不等于正确使用，而不只是平均准确率改善。

'''
 maintext+='[三张主图及逐图四句说明]('+str(D/'figures_and_captions_cn.md')+') · [完整结果解读]('+str(D/'summary_cn.md')+') · [逐种子、损失、90点与真实例子附录]('+str(D/'appendix_cn.md')+') · [执行/未执行清单]('+str(D/'coverage_cn.md')+')\n'
 brief.write_text(maintext)
 # English canonical analysis record with all decisive data; tables carry full precision.
 en='''# Maintaining learned behavior: supervision organization versus local constraints

Purpose: the advisor's reuse-and-differentiate intuition requires learned behavior to remain valid during new learning. This bounded A17 case asks whether parameter restrictions, first-order old-loss constraints and continued correct old supervision have equivalent effects. The task is visible-mode command-to-first/last mapping, with reversed mappings in mode two, not mathematical hierarchy or identified reusable subspaces.

All36existing runs completed240steps/8640new targets, fixed36new/36old slots and denominator72. Old active targets0/4/36 change both exposure and old-objective weight. All methods compute64old TRAIN probes; F/D use old labels even at0old replay. Three continuation orders share one acquired-old model, DEV exposed, TEST unopened.

'''
 en+=table(means,[(k,k) for k in ['old_slots','method','old_accuracy_pct','new_accuracy_pct','old_ce_nats','new_ce_nats']])+'\n\n'
 en+='F-minus-U old gains+11.167,-24.875,+0.042pp are nonmonotonic; F1:9 is worse in every order. S1:1 has a small+0.208pp old change in everyorder, with-0.292pp new change, not the5pp operational utility threshold. At the second consecutive scheduled newaccuracy>=90% point, U/F1:9 both confirm at180steps yet old means88.167%/59.375%; zero-replay F confirms240/180/240 versus U180/180/180. No interpolation or endpoint reselection.\n\n'
 en+=table(bm,[(k,k) for k in ['method','old_slots','old_rule_correct_pct','new_rule_endpoint_pct','other_list_item_pct','other_output_or_invalid_pct','both_correct_pct','same_prediction_pct']])+'\n\n'
 en+='Old/new targets come from paired labels independently checked against generator rules, not inferred predictions. All targets differ, zero exclusions;800modepairs/run,400/panel. At acquisition start old100% but modes give sameanswer99.875%, so the parent had not already learned correct reversed-mode switching. Endpoints show behavioral rule confusion and its reduction with correct supervision, not old-circuit deletion or distinct internal mechanisms.\n\n'
 en+='F measurement audit: same64probe records, same parameter start, CEmean64 and16microbatch, deterministic eval-child modules, actual post-filter FP32 displacement. The90checks have75projection triggers,15nontriggers,0nearzero-gradient guards;48raw-positive finaldots, maximum2.356e-7,0above inherited posthoc ideal-audit tolerance plus Cauchy parameter-copy rounding and conservativeFP64 reduction bounds.69actuallossincreases are raw signs; no saved repeated/no-op loss-noise calibration. Finite remainder is not identified curvature. U1:9also has16/30local increases but much better endpoint, so69/90is not a rootcause explanation. Full360checks and90Fpoints retain all inputs/tolerances/norms.\n\n'
 en+='Nine existing endpoints U0/U1:9/F1:9 across3orders were read on locked64paired inputs (1152sequences total), on the already-existing collaboration H100MIG without a job/allocation or updates. Correctness-stratified sample is descriptive, not fullDEVestimate. At the final prefix token, q_proj input modegap is0.08188for all checkpoints by frozen-upstream construction; output o_proj modegap is nonzero even in U0, whose old/new endpoint-logit margins both favor newrule. F1:9outputgap exceeds U1:9in2/3orders while behavior is worse, so geometry magnitude is not a consistent functional explanation; no further metric scan. All1152argmax predictions match saved records, maxCEdifference3.815e-5.\n\n'
 en+='AI bounded update: prioritize how input conditions maintain/organize correct function updates, retaining finite-step/probe-scope/optimizer-path explanations as rivals. This is not evidence for mandatory MoE, circuit deletion, natural-feature frequency laws or universal protection directions. Researcher acceptance/next experiment remain Unknown. Original training/source/Protocol/results unchanged; current posthoc analysis and finite readout are separate records.\n\n[Chinese full report](summary_cn.md),[all seed/point appendix](appendix_cn.md),[figures/captions](figures_and_captions_cn.md),[coverage](coverage_cn.md).\n'
 (D/'summary.md').write_text(en)
 coverage='''# 执行与未执行清单

| 项目 | 状态 | 实际范围与边界 |
|---|---|---|
| 监督频率主分析 | DONE_EXPLORATORY | 36终点、396保存点评价、F/S/D−U逐种子27配对差、全部90%门槛点；无新训练 |
| 规则/模式配对 | DONE_EXPLORATORY | 四重点条件×3顺序×11保存点，105600模式对记录；互斥错误、面板/口令、真实例子、排除0题 |
| F一阶/有限步 | DONE_EXPLORATORY | 全8640步标量复用，360有限检查含90F；最终实际位移内积、容差、范数、loss差额、近零/无投影分开 |
| 小型模式读出 | DONE_EXPLORATORY | 9已有终点，先锁64对，1152序列，现有协作H100MIG，无优化器更新 |
| 图与数据来源 | DONE_VALID | 三图PNG/SVG/PDF、每图CSV与hash；图外四句说明；均值非独立模型统计 |
| 探针loss噪声标定 | NOT_SAVED / NOT_RUN | 原日志无同状态重复/no-op校准；本轮不补造；微小正值不称显著 |
| 旧TRAIN整体逐点评价 | NOT_RUN | 每步不同探针不能代替完整旧TRAIN保持曲线 |
| 曲率、抽样冲突、Adam路径因果分解 | NOT_RUN | 无专门操纵，不归为已定位根因 |
| 参数保护/新算法搜索 | NOT_RUN | 不训练、不调参、不新增方法 |
| SAE/CrossCoder/TEST/MoE | NOT_RUN | 本轮完全不执行、不读取TEST |
| 外部任务/付费资源申请 | NOT_RUN | 未创建Work/Codex/ACP任务，无资源扩额 |
| 09:40后分析扩展 | NOT_RUN | 本轮提前完成并停止追加分析；完成时刻见回执 |
| Git发布/科研状态关闭 | NOT_RUN | 本轮只本地交付；不代替科研判断 |

原整库导航仍有7项既存未跟踪入口，本轮没有修复无关实验；范围内来源、链接和图表独立核验。原R06四小时交付窗口偏差保留在旧记录，本次10月26日组会材料有自己的09:40/10:00时限，不能用本次按时交付改写旧记录。
'''
 (D/'coverage_cn.md').write_text(coverage)
 # figure provenance + explicit four-sentence contract.
 sources=read(O/'provenance/source_manifest.json');pv={'created_utc':now.isoformat(),'plots':{n:{'csv':'tables/'+data,'source':'existing savedDEV per-item evaluations or stepmetrics','aggregation':agg,'axis':axes,'max_claim':claim} for n,data,agg,axes,claim in [
 ('figure1_supervision_methods','figure1_data.csv','equal-weight3continuation-order means; one acquired-old parent','x categorical old:new objective labelratio; yold/new accuracypercent0..100','supervision organization vs current update rules at fixednewexposure'),
 ('figure2_rule_confusion','figure2_data.csv','equal-weight3orders; each800pairedquestions,0same-targetexclusions','left exclusive oldanswer percentages; right paired bothcorrect and sameanswer percentages','behavioral conditionalruleconfusion only'),
 ('figure3_first_order_finite_loss','figure3_data.csv','all90Ffixedcheckpoints,noaveraging; rightsubset48rawpositives explicitly labelled','left actualfinalgdotdisplacement vsactualprobeΔCE(nat/answer); rightprediction/tolerance','finite-step mismatch given current numericalaudit; no identifiedcurvature')
 ]},'original_evaluation_identity':'all151936vocabargmax; same800permode200percell','TEST_opened':False,'independence':'oneparent,3continuationorders; repeatedquestionsnotindependentreplicates','source_manifest':sources,'new_forward_receipt':rep,'files':{str(p.relative_to(D)):sha(p) for p in [*F.glob('*'),*T.glob('figure*_data.csv')]}}
 write(D/'figure_provenance.json',pv)
 (P/'README_cn.md').write_text('# 分析复现\n\nmeeting_analysis_20261026.py只读原36条轨迹、原DEV和生成器源文本，生成统计与图；meeting_plot3_refine.py对固定90F点作一次可读性调整。meeting_mode_readout_20261026.py在sampling_lock.json锁定样本上读取9权重，已执行1152序列；复现需要原登记资产和既有依赖环境，不因交付自动再运行。meeting_deliver_20261026.py将结果整理到现有R06的本分析附录。\n\nanalysis_plan.json、source_manifest.json、03_measurement_object_audit.json及representation_receipt.json保留对象、容差与边界。原始逐条大表/输入向量仍在执行侧，不放入Git轻量报告。没有权重、原始TEST或新训练产物。\n')
 # One speaking entry already linked from day index; no new competing report/Focus.
 profile=S/'sync/anchors/profiles.json';x=read(profile);entry=next(z for z in x['entries'] if z['project']=='from-attention-to-search' and z['anchor_id']=='17_04_R06')
 for p in [D/'summary.md',D/'summary_cn.md',D/'appendix_cn.md',D/'figures_and_captions_cn.md',D/'coverage_cn.md']:
  rel=str(p.relative_to(S))
  if rel not in entry['sources']:entry['sources'].append(rel)
 write(profile,x)
 (D/'README.md').write_text('# A17 R06 meeting analysis,26Oct2026\n\n[Summary](summary.md) / [中文](summary_cn.md) · [逐种子与测量附录](appendix_cn.md) · [三图](figures_and_captions_cn.md) · [覆盖清单](coverage_cn.md) · [来源](figure_provenance.json)。\n\nDerived posthoc analysis of the existing36trajectories plus one bounded9checkpoint frozen readout, no new training. Scientific owners/primaryendpoints unchanged; old four-hour delivery deviation remains recorded.\n')
 write(O/'provenance/delivery_paths.json',{'owner':str(D),'brief':str(brief),'created_utc':now.isoformat(),'new_training_updates':0,'new_checkpoint_forward_sequences':1152,'new_checkpoints_read':9,'target_BJT':'2026-10-26 10:00','analysis_cutoff_BJT':'2026-10-26 09:40'})
 print(json.dumps({'owner':str(D),'brief':str(brief),'curated_tables':len(selected),'new_forward_sequences':1152,'new_training':0},ensure_ascii=False))
if __name__=='__main__':main()
