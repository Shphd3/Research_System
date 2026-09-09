# 0909 组会证据图表索引

本目录保存经过筛选的派生图表，不保存原始日志、激活或检查点。它是组会阅读附件，不是新的正式结果记录。新离线聚类实验尚未执行，未绘制任何预期结果图。

## 每项图表支持什么

| 报告位置 | 文件 | 计算／来源 | 允许结论及最近边界 |
|---|---|---|---|
| 表1 | [策略比较](/data/250010109/Research_System/daily_research_reports/0909/tables/strategy_comparison.csv) | 当前训练后验证的S1逐种子配对差值；三种子等权均值及负差值计数 | B优于A方向一致；B未稳定超过任务对照。不是生成能力结果 |
| 表2 | [专家功能覆盖](/data/250010109/Research_System/daily_research_reports/0909/tables/expert_function_coverage.csv) | S3每模型/种子仅取发现排序第0候选，检查两组优势异号、各95%区间不跨零、方向复现 | 各模型都存在局部专家功能差异；不同模型候选不同，不能比较分工强度 |
| 表3 | [自动动作](/data/250010109/Research_System/daily_research_reports/0909/tables/automatic_new_arrival_choices.csv) | S6只取GMM-B、两次真实新任务到达；U=更新旧专家，R=更新旧路由 | 六次选择旧容量；实际重放和初始化不完全匹配，只是该实现观察 |
| 图1 | [高层原子归属图](/data/250010109/Research_System/daily_research_reports/0909/figures/hierarchy_membership.png)／[计数](/data/250010109/Research_System/daily_research_reports/0909/tables/hierarchy_membership.csv) | 旧深度探索图的节点编号，与当前冻结八组映射逐个连接；按深度计数 | 当前并非叶节点专用；不证明这些原子经常激活或使用了连接 |
| 图2 | [历史语义覆盖](/data/250010109/Research_System/daily_research_reports/0909/figures/historical_semantic_coverage.png) | E18正式结果图片的逐字节副本；左图原定语义检验，右图附加事后联合条件 | 只有2/9细类获得原定确认；更强联合条件无交集。不替换原注册判定 |
| 备查表4 | [筛选口径计数](/data/250010109/Research_System/daily_research_reports/0909/tables/screening_position_counts.csv) | 同一发现缓存，首答案位置与全部缓存答案位置按组去重记录计数 | 支持不足直接受筛选位置影响；多位置组会重叠，不保证合格双组 |

## 来源与复现

全部绝对源路径、SHA256、变换说明、输出哈希和边界记录在[证据清单](/data/250010109/Research_System/daily_research_reports/0909/evidence_manifest.json)。

当前训练后验证源目录：[full-20260909T052900Z](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z)。历史语义图及表的所属结果：[E18 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E18_dataset_conditioned_sae_semantic_hierarchy/summary.md)。

导出脚本：[build_report_evidence.py](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/analysis_reports/20260909_meeting_attribution/build_report_evidence.py)。仅读取已有结果、生成精选表格、绘制编号计数图和复制历史图，不执行模型前向、拟合或训练。编号连接的上游脚本为同目录下的[audit_hierarchy_membership.py](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/analysis_reports/20260909_meeting_attribution/audit_hierarchy_membership.py)，筛选计数来源为同目录下的[build_figures.py](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/analysis_reports/20260909_meeting_attribution/build_figures.py)。不要为更新报告重新运行后者并将其中的loss图重新加入报告。

重新导出只需执行导出脚本，传入本日目录的绝对路径以及可用的思源/Noto中文字体绝对路径。字体是绘图依赖，不参与数据计算；当前临时字体路径不是长期资源保证。

## 审核结果

- 报告中的loss差值只以表格出现，不绘制微小差值对比图。
- 高层原子图是精确计数，不虚构误差条；专家功能表保留原记录级区间的判据。
- 当前训练、顺序适配观察、历史层级语义证据分开标注，不能互相替代。
- 报告用语仍是AI讨论稿；不修改人类拥有的Focus判断或正式协议。
- 新的两阶段实验结果文件不提前创建为空表，也不填入示例数值。
