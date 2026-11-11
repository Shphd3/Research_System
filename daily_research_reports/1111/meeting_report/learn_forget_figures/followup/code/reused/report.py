from lf_common import *
import shutil,zipfile,re
def preview(name,query=None,cols=None):
 p=R/f'results/{name}.csv'
 if not p.exists():return '待测。'
 d=pd.read_csv(p)
 if query is not None:d=d.query(query)
 if cols is not None:d=d[cols]
 return d.to_markdown(index=False,floatfmt='.6g')
def main():
 inv=json.load(open(R/'evidence/checkpoint_inventory.json')) if (R/'evidence/checkpoint_inventory.json').exists() else [];actual=[]
 for p in sorted((R/'evidence').glob('forward_*.json')):
  z=json.load(open(p))
  if 'row' in z:actual.append(dict(model=z['row']['model'],tokens=z['row']['tokens'],NLL=z['NLL']))
 headline='；'.join(f'{a} '+','.join(f'{z["tokens"]/1e9:g}B' for z in actual if z['model']==a) for a in ['Dense','MoE']) if actual else '前向进行中，尚无完整检查点落盘'
 local=datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
 t=f'''# 学会／遗忘四张图：明早速报

AI分析；研究者判断 Unknown。更新时间：{local.isoformat()}（北京时间）。

实际已测检查点：{headline}。

“激活相同”核对：Dense总／激活参数281431040；MoE总507988992、常规激活281496576，多65536个router参数（约0.0233%）；Dense FFN3072等于两个1536专家的矩阵宽度预算。AdamW、3e−4、β=(0.9,0.95)、ε1e−8、wd0.1、1000步warmup后constant、seed17、数据manifest与前10B历史样本顺序对齐；物理卡数与微批不同。总容量不相同。

$L_D-L_M$（nat，正值表示MoE更低）：

{preview('baseline_NLL_document_CI')}

## 图4：已有十臂数据

![固定分发关系](图4a_NLL与集中度.png)

![切换与恢复](图4b_切换与恢复.png)

![遗忘账本](图4c_十臂遗忘.png)

一句话结论：A9d的切换冲击比A9小，A8等新臂偏离固定分发三点关系，集中度本身不足以解释所有loss差。

读法套用：A2/A1/A5三点拟合，其余点只报告竖直残差；切换1000点为零更新，后续各250步按实际A0聚合差。遗忘计数保留真实区间，A0为500步，A4/A1-deep为1000步，不能伪装为250步等条件比较。

{preview('fig4_fixed_fit_residuals',"band=='overall'",['arm','NLL','M','vertical_residual_nat'])}

未完成部分：本图无新增前向依赖；旧1250／1750等逐位置缺口未重建，聚合差和真实账本已有。

## 图1：学得快还是忘得少

'''
 if (R/'evidence/fig1_complete.json').exists():
  t+='![MoE33B参照](图1_MoE33B.png)\n\n'
  if (R/'results/图1_Dense_latest_available.png').exists():t+='![真正最晚Dense参照](图1_Dense_latest_available.png)\n\n'
  t+='一句话结论：在MoE33B标尺下，10B时MoE掌握率高3.56个百分点，约98.7%的增长差来自新学会，低频占比高的位置也主要来自学得快；真正最晚Dense34.076B标尺仍给同样方向。\n\n可学位置是参照模型loss≤ln2的位置；当前loss≤ln2记会、≥2ln2记不会，中间沿用此前状态。掌握率K是可学位置中会的比例。图中下排新学会和忘掉是对K变化的贡献；初始掌握率差另列。文档bootstrap配对重抽样2000次，恒等式误差≤1.2e−16。\n\n读法套用（10B终点）：\n\n'+preview('fig1_gap_decomposition',"tokens==10000000000",['reference','stratum','K_MoE_minus_Dense','gap_ci95_low','gap_ci95_high','cumulative_new_learned_difference','cumulative_less_forgotten','rule_result'])+'\n\nAI分析：能靠DEV bigram识别当前token的位置是例外，差距主要来自忘得少；需要上下文的位置与低频高占比位置主要来自新学会差。以Dense自己10B终点会的位置作额外参照会偏向Dense，结果反向，图1_Dense_latest10B是保留的附加诊断，不能替代真正最晚34.076B敏感性。参照选择会改变可学内容的组成。\n\n关键数：'+str(json.load(open(R/'evidence/fig1_complete.json')))+'\n\n未完成部分：无；以稀疏保存检查点观测，区间内部短暂学会／遗忘不可见。\n'
 else:t+='进行中。已存在0／0.5／1／3／5／10B真实成对状态和33B参照；正在按token升序逐个前向，完成一个落盘一个。统计及绘图代码已就绪。\n'
 t+='\n## 图3：重叠feature下的可达集中度\n\n'
 if (R/'evidence/fig3_complete.json').exists():
  z=json.load(open(R/'evidence/fig3_complete.json'));t+='![启发式可达曲线](图3_集中度可达曲线.png)\n\n一句话结论：等权目标EVAL集中度中位数为'+f"{z['equal_EVAL_M']:.6f}"+'；lambda1的指定更新存在无低频位置的负载障碍。\n\n读法套用：'+z['rule_result']+'；表中的lambda1高频下降比例'+f"{z['high_frequency_drop_lambda1_vs0']:.4%}"+'来自不满足负载约束的诊断点，不用它判定取舍或同时集中。\n\n'+preview('fig3_frontier')+'\n\n'+preview('fig3_overlap_summary')+'\n\n'+preview('fig3_feasibility_diagnostic')+'\n\nAI分析：47.52%的DEV位置没有低频feature。lambda1更新把其他feature的表项全部置零后，这些位置得到相同分数，单一bias与确定性Top2使它们选择同一对expert，负载比至少1.9008；这是规定更新映射的障碍，不表示原优化问题无可行解，初始二值A5仍可行。高频／背景位置需要保留可区分的分发信息。\n\n边界：仅DEV求解与选起点，EVAL报告；EVAL负载超过1.2的点明确不满足测试端同一负载约束。真实最优不低于DEV启发式找到的可行目标值；EVAL数值为泛化读数，非已证明最优。4只在全局负载完全均匀时是严格上限，例如u=(.05,.05,.15,.15,.15,.15,.15,.15)、某原子q=(.5,.5,0,0,0,0,0,0)满足负载比1.2却给M=10。\n\n未完成部分：所有6目标×4起点×30轮均实际测试；lambda1未得到满足约束的更新端点，取舍判据不成立。没有把失败解换成新训练。\n'
 else:t+='CPU优化进行中：6个目标、各4起点、30轮，DEV选择最优可行解，之后在EVAL报告。原始进度在fig3_optimization_history。\n'
 t+='\n## 图2：局部帮助与冲突\n\n'
 if (R/'evidence/fig2_complete.json').exists():
  t+='![只读梯度](图2_局部帮助与冲突.png)\n\n![共现与帮助](图2_共现与帮助.png)\n\n一句话结论：单序列估计的冲突率对批量很敏感，更有信号的8序列结果支持部分同组低频向高频借力，尚不能按共现无条件判断该共享或隔离哪些内容。\n\n'+preview('fig2_rules',cols=['model','tokens','block','negative_pair_fraction','borrowing_difference','borrowing_ci_low','borrowing_ci_high','cooccurrence_spearman','insufficient_groups'])+'\n\n读法：负组对<5%、同组低高借力差区间全大于0、共现秩相关≥0.3分别按预写规则套用；信号非正组不填T。4份bootstrap排除同一原份的自内积；同一批次重复抽样不会被当作独立交叉份。\n\n未完成部分：'+('无，已完成16组。' if len(json.load(open(R/'evidence/fig2_complete.json'))['groups'])==16 else '按90分钟预写规则完成最大两组×低高频4组，其余12组待测。')+'\n'
  if (R/'precision8/evidence/fig2_complete.json').exists():
   t+='\n### 一次预先说明的批量精度敏感性\n\n![8序列每份](precision8/图2_局部帮助与冲突.png)\n\n'+preview('precision8/fig2_rules',cols=['model','tokens','block','negative_pair_fraction','borrowing_difference','borrowing_ci_low','borrowing_ci_high','cooccurrence_spearman','insufficient_groups'])+'\n\n保留原1序列/份结果；因若干组跨份自信号非正，补做一次8序列/份，仍R4，16组×4份共512条DEV序列全局不复用。批量大小可明显改变负组对占比，应先区分估计噪声与稳定冲突，不能选更好看的结果替代原表。T的交叉份归一化可超过1，不能当普通余弦；正值只对应当前点原始梯度下降方向的局部帮助，未模拟Adam或真实训练。\n\nAI分析：8序列下，MoE expert的负组对占比1B为2.5%、10B为14.29%，Dense FFN为1.67%／10.83%；未显示MoE全局冲突更少。MoE expert同组低高借力均值差分别0.2020（区间0.1019–0.4782）和0.1541（0.0411–0.6328）；与共现的秩相关0.3775／0.29697，只有1B达到0.3阈值。逐组上1B的A5组0、1、3、4、7支持借力，10B仅组4支持、组1和2信号不足，其余分不出；这些是本地读数，尚不足以决定永久隔离或合并。\n\n既有投影梯度的精度诊断显示：MoE expert跨份信号／总范数中位数，从单序列约0.00166升至8序列的0.02699（1B）；10B为0.00142／0.01158。接近收敛时局部平均方向相对批次波动更难估计，是小批次冲突符号不稳定的候选原因，而非“没有帮助”的证据。原表fig2_signal_to_noise。\n'
  if (R/'results/fig2_borrowing_by_A5_group.csv').exists():t+='\n每个A5分组的低高借力差与区间另见fig2_borrowing_by_A5_group.csv/md；投影范数校准见fig2_projection_norm_calibration.csv/md。\n'
 else:t+='等待固定评估前向完成后在同一MIG执行，节点为1B和10B；已准备16组×4独立序列批及参数块CountSketch只读梯度代码。先计时，若超过90分钟则按原规则缩至4组。\n'
 t+='''
## 共同边界与文件

单种子；会／不会以33B MoE为主标尺，Dense最晚10B为敏感性。图2是某时刻局部一阶量，不等于训练中真实帮助／伤害；只测DEV少量独立序列批且用固定随机投影，近零符号有估计误差。图3仅优化离线分发表，不更新任何模型；坐标是teacher feature。图1的Dense／MoE差还包含总容量、硬件历史及检查点之间未观测的变化。

执行和证据目录：`/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/`。所有表有CSV／Markdown，图有PNG／PDF；旧实验未修改。实际缺失／失败以evidence及coverage表为准。
'''
 # Dollar style explicitly requested.
 t='\n'.join(re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)',lambda m:' $'+m[1]+'$ ',line) for line in t.split('\n'))
 (REPORT/'明早速报_cn.md').write_text(t)
 for p in (R/'results').rglob('*'):
  if p.is_file():
   dest=REPORT/p.relative_to(R/'results');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 shutil.copy2(R/'protocol_cn.md',REPORT/'protocol_cn.md');shutil.copy2(R/'protocol_original_cn.md',REPORT/'protocol_original_cn.md')
 if (R/'protocol_deviations_cn.md').exists():shutil.copy2(R/'protocol_deviations_cn.md',REPORT/'protocol_deviations_cn.md')
if __name__=='__main__':main()
