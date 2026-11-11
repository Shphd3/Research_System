from fu import *

def main():
 p=REPORT/'明早速报_追加_cn.md';s=p.read_text();s=s.replace('0.5B 和 10B 的读法一致。','0.5B 和 10B 的读法一致。');s=s.replace('最大、最小各 20 个 feature、频率、集中度、两模型掌握率及每个 3 段真实上下文均已输出。','最大、最小各 20 个 feature、频率、集中度、两模型掌握率及每个 3 段真实上下文均已输出。主参照下 MoE 领先的 20 个覆盖全部 8 个 A5 分组，其中 7 个位于组 4；19/20 的可学支撑主要属于“靠上下文”，Dense 领先的 20 个均属这一类。分类沿旧 DEV 拟合的当前 token→下一 token 条件概率，达到 0.5 算“认 token”；这是操作性分层，非语义标注。')
 s=s.replace('逐 feature 状态遗忘比例、两个参照、频段/A5 分组/认 token 或靠上下文汇总及变化最大 20 个 feature 的上下文已输出。','逐 feature 状态遗忘比例、两个参照、频段/A5 分组/认 token 或靠上下文汇总及变化最大 20 个 feature 的上下文已输出。共同遗忘的 3169 个中，3116 个（98.33%）按多数可学支撑归为“靠上下文”；组 4/5/7 分别有 1402/748/616 个，这是集合构成，不是已控制组大小的富集结论。')
 if not (F/'evidence/E_complete.json').exists():p.write_text(s);return
 main=pd.read_csv(F/'results/E_main_statistics.csv');rule=pd.read_csv(F/'results/E_precision_rule.csv').iloc[0];comp=pd.read_csv(F/'results/E_10B_precision_comparison.csv');pair=pd.read_csv(F/'results/E_stable_interference_pairs.csv');help=pd.read_csv(F/'results/E_strongest_stable_help_pairs.csv');old=main[main['mode']=='8_original'];lines=[]
 for r in comp.sort_values(['model','sequences','mode']).itertuples():lines.append(f'| {r.model} | '+{'8_original':'原 DEV 8','8_extended_control':'扩展 DEV 8','32_extended':'扩展 DEV 32'}[r.mode]+f' | {r.negative_pairs}/{r.valid_pairs}（{100*r.negative_pair_fraction:.2f}%） | {r.signal_to_total_norm_ratio_median:.4f} |')
 nodes=[]
 for t in sorted(old.tokens.unique()):
  vals=[]
  for m in ['MoE','Dense']:
   r=old[(old.tokens==t)&(old.model==m)].iloc[0];vals.append(f'{r.borrowing_difference:.3f} [{r.borrowing_ci_low:.3f}, {r.borrowing_ci_high:.3f}]')
  nodes.append(f'| {t/1e9:g}B | '+ ' | '.join(vals)+' |')
 flags={}
 for m in ['MoE','Dense']:
  z=old[old.model==m];flags[m]=', '.join(f'{r.tokens/1e9:g}B' for r in z.itertuples() if r.borrowing_ci_low>0)
 confirmed=int(pair.both_negative_32.sum()) if len(pair) else 0
 examples=[]
 for r in help.head(3).itertuples():examples.append(f'- 组对 {r.group_a}–{r.group_b}：{r.content_a}；对应 {r.content_b}。五时点×两模型最小 $T$={r.minimum_T_across_10:.3f}，共现 lift={r.cooccurrence_lift:.2f}。')
 e='''## E：什么时候互相帮助，10B 的干扰是否稳定

![帮助与干扰随训练变化](E_帮助与干扰随训练变化.png)

**一句话结论：10B 的干扰读数未通过精度稳定性检查；两模型的 32 序列版本都没有负组对。** 这满足预写“后期读到的干扰主要是估计噪声”的数值门槛。扩展样本的 8 序列对照也显著减少了负组对，因此能确认的是**原负号对抽样与批次组成敏感，未建立稳定干扰证据**；不能把全部变化单独归因于序列数量。

![10B 精度对照](E_10B精度检查.png)

| 模型主参数块 | 条件 | 负组对 / 有效组对 | 跨份信号 / 总范数² 中位数 |
| -- | -- | --: | --: |
'''+ '\n'.join(lines)+'''

原 8 序列版在 10B 的 MoE 有 2 个组自信号非正，Dense 主块没有；扩展 32 版两者 16 组均有正自信号，120 个组对全部可定义。所有无定义值保留为缺失，没有填成零。

用户已允许扩展独立 DEV。原 DEV 为 1024 条，32 序列版需 16组×4份×32=2048 条全局不复用序列；新增 1024 条来自原 validation 文件、位于旧 EVAL 完整文档边界之后。旧 8 序列逐份原样保留在相应 32 份中，额外 24 条固定随机分配；扩展 8 对照从同一 32 份中预先固定抽 8 条。新标签使用与原 DEV 相同的 FP32 teacher/SAE 路径，不重拟合分组。

**同组低频与高频是否更能互相帮助：** 下表为“同组低高 $T$ − 对应低频组与其他高频组的平均 $T$”，方括号是 R4 自助 95% 区间；每次固定原点有效组对集合，无定义重抽样不换一套组。

| 时点 | MoE expert 差值 [95%区间] | Dense FFN 差值 [95%区间] |
| -- | --: | --: |
'''+ '\n'.join(nodes)+f'''

MoE 的区间下界大于 0 的时点：{flags['MoE'] or '无'}；Dense：{flags['Dense'] or '无'}。点估计与区间需分别读取；没有通过区间的节点不能称为已确定“共现内容更互助”。全部同组/跨组均值、共现相关和有效 bootstrap 比例见 [E_main_statistics.csv](E_main_statistics.csv)。

**哪些组对稳定：** 原 8 序列版中，满足“3B/5B/10B 至少两个相同时点两模型都负”的候选共有 {len(pair)} 对，其中 {confirmed} 对在 10B 扩展 32 版仍同时为负。候选名单与每个节点原始值见 [E_stable_interference_pairs.csv](E_stable_interference_pairs.csv)，两模型各自至少两个负节点的较宽敏感性见 [E_interference_candidates.csv](E_interference_candidates.csv)。不能将原 8 版候选直接当作已确认稳定干扰。

五时点、两模型的 10 个 $T$ 全部有效且为正，按其中最小值排序的稳定帮助名单给出 {len(help)} 对，含每对内容例子、共现 lift、各节点数值及 32 版确认值：[E_strongest_stable_help_pairs.csv](E_strongest_stable_help_pairs.csv)。例如：

'''+ '\n'.join(examples)+'''

这些内容说明来自每个 A5 分组×频段中，旧 DEV 激活质量最高的两个 feature，另附每个 3 个高激活真实上下文；不是根据帮助系数挑选例子后给组命名。[代表 feature](E_group_representative_features.csv)与[96 段上下文](E_group_representative_contexts.csv)同包。

原始表还包括 [E_pair_signs_and_values.csv](E_pair_signs_and_values.csv)、[E_signal_norm_audit.csv](E_signal_norm_audit.csv)、[E_negative_set_overlap.csv](E_negative_set_overlap.csv)、[E_precision_rule.csv](E_precision_rule.csv)。未完成：无；所有指定节点和 10B 精度检查已完成。局部梯度结果不能替代真实训练干预。

'''
 start=s.index('## E：');end=s.index('## B：');s=s[:start]+e+s[end:];s=s.replace('A、B、C 和 M1–M7 已完成；任务 E 的 32 序列精度检查正在计算。','A–E 和 M1–M7 均已完成，所有可用节点均已实测。');s=s.replace('2026-11-11 凌晨持续更新。','2026-11-11 凌晨完成。');p.write_text(s)
 # Compact entry for a discussion with another AI.
 readme='''# 1111 学会遗忘追加分析

AI 分析；研究者判断 **Unknown**。本轮回答：MoE 领先的内容是否对应 router 集中、3B→5B 是否共同遗忘，以及后期梯度干扰是否稳定。只用本地 H100 MIG 3g.40GB 和 CPU；未训练或更新任何参数。

先读 [追加速报](明早速报_追加_cn.md)，再看图和表。

| 任务 | 一句话结论 | 规则套用 | 核心原始表 |
| -- | -- | -- | -- |
| A：多学会什么 | 掌握率优势与集中度相关很弱 | .5B/10B频段相关中位数小于.05，1B介于阈值之间；不支持偏向集中 feature | [A_correlations.csv](A_correlations.csv)、[A_extreme_features.csv](A_extreme_features.csv) |
| E：何时互助/干扰 | 10B扩展32版两模型负组对均为0，原负号未精度确认 | 两者小于5%；扩展8也变化，采样组成与精度作用不可完全分开 | [E_main_statistics.csv](E_main_statistics.csv)、[E_10B_precision_comparison.csv](E_10B_precision_comparison.csv) |
| B：共同遗忘 | 3B→5B共有3169个，Jaccard=.750、随机11.42倍、变化相关=.800 | 超过10倍及.5，符合共同因素读法；因素未识别 | [B_overlap_and_correlations.csv](B_overlap_and_correlations.csv)、[B_recovery.csv](B_recovery.csv) |
| C：最早差距 | 正式Dense无0–.5B内部状态，不能确定差距在哪段建立 | A0附近NLL差−.000974，通过.01描述性相容门槛 | [C_checkpoint_inventory.csv](C_checkpoint_inventory.csv)、[C_A0_baseline_check.csv](C_A0_baseline_check.csv) |
| D：组会图 | M1–M7均已提供中文PNG/PDF和逐图读法 | 指定臂和统一颜色；插值与示意坐标明确标注 | M1–M7及[M3_source.csv](M3_source.csv)、[M7_source.csv](M7_source.csv) |

**完成与缺失：** A/B/E 的所有指定计算已完成；C 新增了真实A0 200步的前向，Dense更早权重和A0 250/750/1250/1750逐位置数据缺失，未补造。不存在等待某个未完成训练的本轮节点。

**讨论用途（AI 建议）：** 目前最直接的区别是“MoE早期已建立的优势”与“原生集中度继续缓慢增长”没有表现为强逐feature对应；后期局部负号又对抽样敏感。若据此选新架构，仍需能够区分路由分工、总参数容量和优化历史的直接对照，不能只按集中度或小批次梯度符号定方案。

**文件：** protocol_cn.md、protocol_E_cn.md 保留跑前读法；protocol_deviations_cn.md 记录实际偏差；raw/ 含全部逐feature CSV；code/ 含本轮脚本和只读复用源；evidence/ 与 SOURCE_MANIFEST.json 提供输入和校验。为保持结果包小于20MB，raw/ 的 Markdown 是前20行阅读视图，完整 CSV 不删行、不降低精度；执行根保留完整 Markdown。

ZIP 中数值 CSV 使用标准 ZIP-LZMA 压缩，其他文件为常见 Deflate；Python `python -m zipfile -e 包名.zip 解压目录` 或7-Zip均可解压。包内不含模型权重、逐位置大数组、梯度投影或原始语料；它们的绝对路径与身份在证据中。

**共同边界：** 单种子；feature支撑重叠；文档区间只含评估抽样不含种子方差；掌握率以33B标尺为主，最晚Dense作敏感性；相关不是因果；$T$为原始梯度一步的局部量，非Adam长期训练效果。数据源在本机可核验，旧远端对话读取超时，未用聊天代替实验数值。
''';(REPORT/'README_cn.md').write_text(readme)

if __name__=='__main__':main()
