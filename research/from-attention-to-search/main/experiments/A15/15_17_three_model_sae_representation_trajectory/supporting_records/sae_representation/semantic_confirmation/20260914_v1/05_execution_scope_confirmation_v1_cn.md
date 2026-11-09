# Analysis2 冻结面板两臂表征分析：执行范围

日期：2026-09-14  
状态：研究者已在当前对话明确确认数据 family 全部保留、同意分析规划，并要求立即完成绘图和报告。本文只冻结本次只读分析范围，不替代项目 Anchor 或正式 Protocol，不拥有最终科学判断。

## 目的与边界

用已冻结的 360 句、72 family 面板，比较普通稠密模型与 SAE-mediated 模型在共同训练词元点的最后一层 MLP 前表征，并检查线上 SAE 的命题复用、领域激活和重构质量。分析不创建优化器、不更新模型、不修改 checkpoint、不停止或启动训练。

本轮结果资格为 `BOUNDED_DESCRIPTIVE_COMPARISON_PENDING_RESEARCHER_JUDGMENT`：可以给出固定数据上的估计、区间和图，但单 seed、两臂参数量差异及缺少等参数消融限制了强因果归因。

## 固定输入

- 数据：`/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/data/panel_frozen_v1.jsonl`
- 数据 SHA-256：`7aaf0ec96fdae2f2eecc4a011cd03539d6dc2268d3198203fcd6e3344781bf61`
- 事实 triplet SHA-256：`b22730719d00fc7c8b3308d6381b1693c0b86c3c1c82cdd3b3f5318b884402cf`
- 主比较词元点：0.5B、1B、3B、5B；0B 只作初始化资格检查和附录。
- 读取位置：原句后统一换行，读取最后一个有效 token 在最后块 `norm2` 后、最后 MLP 前的向量。
- 两臂使用同一文本、tokenizer、顺序、读取位置和 family 划分。

## 固定分析

1. 在原始 1024 维空间计算粗领域、细领域和同命题关系的正例相似度、反例相似度及差值；按 family 做配对 bootstrap 区间。
2. 对线上 SAE 计算激活集合 Jaccard、幅度加权 Jaccard、同命题重合 \(S^+\)、异命题重合 \(S^-\) 和选择性差值 \(G=S^+-S^-\)；并列重构误差、正激活数、固定面板覆盖与激活频率。
3. 在 fit family 上为每个粗领域选择 6 个相对其他领域更强的 feature，在独立 confirmation family 上显示其领域富集；每个 checkpoint 独立选择，feature 编号不解释为跨时期稳定语义身份。
4. 联合两臂四个主 checkpoint 的 confirmation 表征，无标签拟合 PCA、UMAP 和 t-SNE。降维图仅作描述；原空间关系量和 family-disjoint 线性读出用于检查信息是否存在于二维主轴之外。
5. 对两个模型在 0.5B、1B、3B、5B 的原始表示趋势逐点作 token-aligned 对照；两臂差使用相同 family 的配对区间。

## 资源与完成条件

- 执行环境：`5090-2-spot`，镜像 `shphd-lite-0911`；研究者在 2026-09-14 当前对话中明确改为两卡 RTX 5090 SPOT，并自行停止先前仍在排队的 H100 Smoke，AI 不操作该 H100 作业。
- UMAP 依赖安装到本实验独立目录，不修改基础镜像。
- 本轮原计划先执行 20 句、两模型 H100 Smoke，但该作业仍在排队时，研究者明确要求改为两卡 RTX 5090 SPOT 并直接提交完整分析。直接 full 的工程门槛复用：analysis1 已在相同 5090 运行层成功加载 SAE checkpoint；普通基线已在相同运行层训练并保存 checkpoint；本轮 1,440 点 PCA/UMAP/t-SNE 与完整合成后处理矩阵测试均通过。不得把这些写成“本轮 H100 Smoke PASS”。
- 完成要求：终止回执 exit 0，`optimizer_updates=0`，十个 cache 齐全，三种降维图、领域激活图、关系/重叠/质量/读出/两臂差图及来源表齐全。
- 最终解释和机制判断由研究者审核；本轮不更新 Anchor 或 Focus 的科学结论。
