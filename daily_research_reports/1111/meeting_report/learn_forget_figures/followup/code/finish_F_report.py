from fu import *

def main():
 assert (F/'evidence/F_direction_validation_complete.json').exists();S=pd.read_csv(F/'results/F_layer_summary.csv');D=pd.read_csv(F/'results/F_statistics.csv');rules=pd.read_csv(F/'results/F_prediction_rules.csv');cv=pd.read_csv(F/'results/F_total_covariance_decomposition.csv');reliability=pd.read_csv(F/'results/F_direction_heldout_validation.csv');features=pd.read_csv(F/'results/F_subspace_features.csv');dense=D[(D.arm=='Dense')&(D.condition=='global')];own=S[(S.view=='own')&(S.condition=='actual')];common=S[(S.arm=='A0')&(S.condition=='actual')];n1=int(rules[rules.view=='own'].joint_order.sum());n2=int(rules[rules.view=='common_A0'].joint_order.sum());rawrankok=0;rows=[]
 for l in range(8):
  z={a:own[(own.arm==a)&(own.layer==l)].iloc[0] for a in ['A0','A5','A2']};rawrankok+=bool(z['A5'].effective_rank_median<z['A0'].effective_rank_median<z['A2'].effective_rank_median)
  rows.append(dict(layer=l,Dense_global_effective_rank=float(dense[dense.layer==l].effective_rank.iloc[0]),**{a+'_conditional_rank_median':float(r.effective_rank_median) for a,r in z.items()},**{a+'_rank_ratio':float(r.rank_ratio_to_global_median) for a,r in z.items()},**{a+'_low64_amplification':float(r.low_variance_amplification_64_median) for a,r in z.items()}))
 summary=pd.DataFrame(rows);table(summary,'F_meeting_key_values');l=7;con=common[common.layer==l].set_index('route');low=D[(D.condition=='actual')&(D.view=='own')&(D.layer==l)];b=[]
 for a in ['A0','A5','A2']:
  z=low[low.arm==a];g=D[(D.arm==a)&(D.layer==l)&(D.condition=='global')].iloc[0];b.append(dict(arm=a,global_low64_variance_fraction=g.low_variance_fraction_64,conditional_low64_variance_fraction_median=z.low_variance_fraction_64.median(),conditional_low64_amplification_median=z.low_variance_amplification_64.median(),conditional_low64_second_moment_amplification_median=z.low_second_moment_amplification_64.median(),shuffled_feature_direction_amplification_median=z.null_variance_amplification_64.median()))
 bt=pd.DataFrame(b);table(bt,'F_layer7_variance_breakdown');counter=rules[~rules.joint_order];table(counter,'F_counterexample_layers');rangelow=(float(reliability.heldout_energy_ratio.min()),float(reliability.heldout_energy_ratio.max()));subcounts=features.groupby('bin').size();form='支持预写的完整顺序' if n1==8 and n2==8 else '未在所有层复现预写的完整顺序，不能把该谱预测写成已证实机制';p=REPORT/'明早速报_追加_cn.md';text=p.read_text();start=text.index('## F：');text=text[:start]
 f='''## F：FFN 输入条件协方差谱

![条件协方差谱](F_条件协方差谱.png)

**一句话结论：'''+form+f'''。** “A5 条件有效秩 / 自身全局秩低于原生，原生低于 A2，且 A5 的低频方向方差放大最高”的联合顺序，在各自训练表征中满足 **{n1}/8 层**，在固定 A0 表征、只更换统计切片标签时满足 **{n2}/8 层**。直接按原始条件有效秩排序 A5<原生<A2，满足 **{rawrankok}/8 层**。完整逐层判定与反例在 [F_prediction_rules.csv](F_prediction_rules.csv)、[F_counterexample_layers.csv](F_counterexample_layers.csv)。

**先区分两个读法：** 归一化谱越平，熵有效秩越高；低秩表示总方差集中在较少方向。原预测“最平、秩最低”不能由同一个熵秩数字同时支持。这里同时给完整谱、熵秩、参与秩、90%方差维数与头尾占比，不改变观察后的定义。

每个臂使用8层 FFN 的 norm2 输出，DEV/EVAL各128条固定完整序列（各262144位置）。Dense 为真实0.5B、1908步；A0/A5/A2为2000步、0.524288B，不对模型或谱插值。Top-2每个expert各计一次；逐expert均值分别扣除后算条件协方差。全部前向回放与既有EVAL逐位置缓存吻合，三个MoE臂Top2集合核验通过；隐藏缓存float16舍入均方占比约4.3e−8，统计与分解用float64。

| 层 | Dense全局有效秩 | 原生A0条件秩 | A5条件秩 | A2条件秩 |
| -- | --: | --: | --: | --: |
'''
 for r in summary.itertuples():f+=f'| {r.layer} | {r.Dense_global_effective_rank:.1f} | {r.A0_conditional_rank_median:.1f} | {r.A5_conditional_rank_median:.1f} | {r.A2_conditional_rank_median:.1f} |\n'
 f+='''
条件值为8个expert的中位数。Dense与三个MoE模型的权重不同，表中绝对差混合了架构、分发和表征适应；以下共同表征控制更接近“分发如何改变每个expert接收的方向”。

![有效秩与低频方向](F_有效秩与低频方向放大.png)

第7层共同A0表征的对照：

| 仅用于统计切片的分发 | 条件/全局有效秩 | 低频64维方差占比放大 |
| -- | --: | --: |
'''
 for a in ['A0','A5','A2']:f+=f'| {a} | {con.loc[a,"rank_ratio_to_global_median"]:.4f} | {con.loc[a,"low_variance_amplification_64_median"]:.4f} |\n'
 f+='''
这里没有换模型前向或gate，只在同一批A0输入向量上按三种已存分发分组。每套标签还在位置之间打乱一次，保留每层Top2集合和负载分布，用来检查条件样本数造成的谱差。A2相对自身全局与Dense全局的归一化谱L1距离均在 [F_layer_summary.csv](F_layer_summary.csv)，不能把“随机分组不改变其自身分布”混同于“不同权重模型的协方差完全相同”。

**低频方向的定义和拆解：** 先在每个模型本层的DEV坐标里，求隐藏状态与bin0–2 feature正激活标签的交叉协方差，取前64个可线性读出的方向；再在EVAL测占总方差的比例。只纳入DEV所抽位置里出现至少20次的原子，bin0–2保留数量为 '''+', '.join(f'bin{j}={int(subcounts.get(j,0))}' for j in range(3))+'''。32/128维敏感性与高频/打乱标签方向均已同样保存，不直接跨坐标使用teacher decoder。

| 第7层，各臂自己的表征 | 全局低频方向占比 | expert内占比中位数 | 内部方差放大 | 关于全局均值的二阶矩放大 | 打乱feature方向放大 |
| -- | --: | --: | --: | --: | --: |
'''
 for r in bt.itertuples():f+=f'| {r.arm} | {r.global_low64_variance_fraction:.4f} | {r.conditional_low64_variance_fraction_median:.4f} | {r.conditional_low64_amplification_median:.4f} | {r.conditional_low64_second_moment_amplification_median:.4f} | {r.shuffled_feature_direction_amplification_median:.4f} |\n'
 f+=f'''
expert内方差与expert均值差是两件事。总协方差按Top2混合权重精确拆成“expert内”与“均值间”，相对恒等误差最大 {cv.covariance_trace_identity_relative_error.max():.2g}，见 [F_total_covariance_decomposition.csv](F_total_covariance_decomposition.csv)。低频子空间在EVAL捕获的feature交叉协方差能量相对DEV打乱标签子空间的比值范围为 {rangelow[0]:.3f}–{rangelow[1]:.3f}，详 [F_direction_heldout_validation.csv](F_direction_heldout_validation.csv)；噪声方向相近的情况不能当作低频专属放大证据。

**判读与下一步（AI 分析）：** {form}。这些测量直接描述expert接收到的表征谱；即使局部顺序吻合，训练因果仍需要固定初始化/预算并改变分发的对照。此处不凭几何谱宣布学习机制或选择新架构；研究者判断仍为Unknown。

原始表：[F_meeting_key_values.csv](F_meeting_key_values.csv)、[F_statistics.csv](F_statistics.csv)、[完整1024维谱](raw/F_eigenvalues.csv)、[方向原子列表](F_subspace_features.csv)、[第7层方差拆解](F_layer7_variance_breakdown.csv)。未完成：无；四臂、8层、实际/打乱标签、共同A0表征、三种子空间维数和留出方向核验均完成。
''';p.write_text(text+f)
 read=REPORT/'README_cn.md';s=read.read_text();s=s.replace('A/B/E 的所有指定计算已完成','A/B/E/F 的所有指定计算已完成');s=s.replace('| C：最早差距 |',f'| F：条件协方差谱 | 完整秩/低频联合顺序：各自表征{n1}/8层，共同A0表征{n2}/8层 | 谱平坦与低秩分开读，完整结果与反例保留 | [F_meeting_key_values.csv](F_meeting_key_values.csv)、[F_layer_summary.csv](F_layer_summary.csv) |\n| C：最早差距 |');s=s.replace('protocol_cn.md、protocol_E_cn.md','protocol_cn.md、protocol_E_cn.md、protocol_F_cn.md');read.write_text(s)
 dump(F/'evidence/all_analysis_complete.json',dict(tasks=['A','B','C','D','E','F'],F_joint_order_layers_own=n1,F_joint_order_layers_common=n2,F_rank_original_order_layers=rawrankok,missing_historical_Dense_early=True,training_updates=0))
if __name__=='__main__':main()
