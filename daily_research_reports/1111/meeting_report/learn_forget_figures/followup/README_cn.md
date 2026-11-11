# 1111 学会遗忘追加分析

AI 分析；研究者判断 **Unknown**。本轮回答：MoE 领先的内容是否对应 router 集中、3B→5B 是否共同遗忘，后期梯度干扰是否稳定，以及条件协方差谱能否解释分发差异。只用本地 H100 MIG 3g.40GB 和 CPU；未训练或更新任何参数。运行成本见 [execution_cost.csv](execution_cost.csv)。

先读 [追加速报](明早速报_追加_cn.md)，再看图和表。

| 任务 | 一句话结论 | 规则套用 | 核心原始表 |
| -- | -- | -- | -- |
| A：多学会什么 | 掌握率优势与集中度相关很弱 | .5B/10B频段相关中位数小于.05，1B介于阈值之间；不支持偏向集中 feature | [A_correlations.csv](A_correlations.csv)、[A_extreme_features.csv](A_extreme_features.csv) |
| E：何时互助/干扰 | 10B扩展32版两模型负组对均为0，原负号未精度确认 | 两者小于5%；扩展8也变化，采样组成与精度作用不可完全分开 | [E_main_statistics.csv](E_main_statistics.csv)、[E_10B_precision_comparison.csv](E_10B_precision_comparison.csv) |
| B：共同遗忘 | 3B→5B共有3169个，Jaccard=.750、随机11.42倍、变化相关=.800 | 超过10倍及.5，符合共同因素读法；因素未识别 | [B_overlap_and_correlations.csv](B_overlap_and_correlations.csv)、[B_recovery.csv](B_recovery.csv) |
| F：条件协方差谱 | 完整秩/低频联合顺序：各自表征2/8层，共同A0表征0/8层 | 谱平坦与低秩分开读，完整结果与反例保留 | [F_meeting_key_values.csv](F_meeting_key_values.csv)、[F_layer_summary.csv](F_layer_summary.csv) |
| C：最早差距 | 正式Dense无0–.5B内部状态，不能确定差距在哪段建立 | A0附近NLL差−.000974，通过.01描述性相容门槛 | [C_checkpoint_inventory.csv](C_checkpoint_inventory.csv)、[C_A0_baseline_check.csv](C_A0_baseline_check.csv) |
| D：组会图 | M1–M7均已提供中文PNG/PDF和逐图读法 | 指定臂和统一颜色；插值与示意坐标明确标注 | M1–M7及[M3_source.csv](M3_source.csv)、[M7_source.csv](M7_source.csv) |

**完成与缺失：** A/B/E/F 的所有指定计算已完成；C 新增了真实A0 200步的前向，Dense更早权重和A0 250/750/1250/1750逐位置数据缺失，未补造。不存在等待某个未完成训练的本轮节点。

**讨论用途（AI 建议）：** 目前最直接的区别是“MoE早期已建立的优势”与“原生集中度继续缓慢增长”没有表现为强逐feature对应；后期局部负号又对抽样敏感。若据此选新架构，仍需能够区分路由分工、总参数容量和优化历史的直接对照，不能只按集中度或小批次梯度符号定方案。

**文件：** protocol_cn.md、protocol_E_cn.md、protocol_F_cn.md 保留跑前读法；protocol_deviations_cn.md 记录实际偏差；raw/ 含全部逐feature CSV；code/ 含本轮脚本和只读复用源；evidence/ 与 SOURCE_MANIFEST.json 提供输入和校验。为保持结果包小于20MB，raw/ 的 Markdown 是前20行阅读视图，完整 CSV 不删行、不降低精度；F 的四份逐臂底表合并为 F_statistics.csv，保留全部原列和行。执行根保留完整 Markdown 与逐臂底表。

ZIP 使用标准 ZIP-LZMA 压缩；Python `python -m zipfile -e 包名.zip 解压目录` 或7-Zip均可解压。包内不含模型权重、逐位置大数组、梯度投影或原始语料；它们的绝对路径与身份在证据中。

**共同边界：** 单种子；feature支撑重叠；文档区间只含评估抽样不含种子方差；掌握率以33B标尺为主，最晚Dense作敏感性；相关不是因果；$T$为原始梯度一步的局部量，非Adam长期训练效果。数据源在本机可核验，旧远端对话读取超时，未用聊天代替实验数值。
