# R02 执行契约：一步更新均值项／噪声项分解（MIG 先导）

[Summary](summary_cn.md) · [Detailed](detailed_cn.md)

状态：**按研究者上传 prompt 授权执行，已完成**。本页记录实际执行时冻结的契约，不另立科学设计；问题与假设的来源是研究者 2026-11-08 上传的《执行 Prompt：长尾学习的信噪比机制——MIG 先导实验与 11/9 组会汇报》，原字节存于执行侧 `evidence/authorizing_prompt_20261108.md`（SHA256 `f4b40ca4…de57`）。

## 1. 授权范围

- 授权：任务 A（MIG 资产与测速）、任务 B（本轮）、任务 C（CPU，见 A15_27 S18）、任务 D（只写配置）与 11/9 汇报。GPU 总时长上限 3 小时。
- 未授权：4×H100、训练、续训、改动模型／SAE／load bias、commit/push、新建 Focus。

## 2. 冻结的设置（执行前写入文件并记录哈希）

| 项 | 冻结值 | 冻结文件 |
|---|---|---|
| 模型 | `20261031_dense_order_aligned_moe_baseline` 33B milestone，state SHA256 `3e392157…c795` | — |
| SAE | `20261104_moe_gate_input_sae_33b/runs/formal/sae_full_final.pt`，接口 blocks.7.norm2 输出 | — |
| 数据 | S14 `reference_general.jsonl` 中 body_index=127 的 5589 篇；正文前 128 token；目标位置 32–126 | — |
| 文档划分 | 13-token 共有片段并查集归组；组按 `sha256(seed:最小id)` 排序；DEV .35 / GRAD .35 / EVAL .30；seed 2026110809 | `data/split.json`（在任何损失前） |
| expert | DEV 上 Top-2 负载份额最接近 0.25 的 block-7 expert | `data/groups_frozen.json` |
| 聚类 | DEV expert-e token 的 Top32 二值矩阵，df≥20，TF-IDF、L2 → TruncatedSVD(32, seed 0) → L2 → KMeans(K=8, seed 0, n_init 10)；GRAD/EVAL 用同一变换取最近质心 | 同上 |
| 资格 | DEV≥1024、GRAD≥4096、EVAL≥1024 token | 同上 |
| 选簇 | Y＝合格簇中 DEV 支持最大者；X＝与 Y 质心余弦最低的合格簇；其余合格簇作次要 A→B，全部报告 | 同上 |
| 损失 | 被路由到 expert e 的目标位置的下一 token CE，其余位置屏蔽；float64 尾部（block-7 残差＋其他 expert 贡献＋w·E_e(x) → 末层 RMSNorm → 共享嵌入） | `code/common.py` |
| 更新 | 单步纯 SGD，无动量、无权重衰减；每分支后从快照恢复并 `torch.equal` 核验 | — |
| ḡ | 池内随机置换后 M=⌊池/128⌋（≥32）个互不重叠 128-token minibatch 的平均 | `data/probe_plan_frozen.json` |
| 噪声分支 | n∈{32,64,128}，主比较 R=32、次要 R=16，每次无放回独立抽样 | 同上 |
| η 网格 | η_hi＝DEV 预检（n0、8 次抽样）跨组单 batch 平均 ΔL_B ≥0.01 nat 的最小 2 的幂；网格 η_hi·2^k，k=−6..1 → {1/32,…,4} | 同上（看 EVAL 前） |
| 判据 | 见 Summary 第 3 节；斜率窗口 [1.6,2.4] 与 [−1.4,−0.6] 为执行前补写的“约为 2 / −1”操作化 | 同上 |

## 3. 修订（Amendments）

- **A01（事后，看过主表后）：**加入 (i) 均值投影 g_eval·ḡ 的标准误（由各次抽样投影的方差推得）；(ii) 控制变量估计 E[ΔL(−ηĝ)] ＝ mean_r(ΔL_r − lin_r) + lin_mean；(iii) η\* 推导值。代码 `code/analyze_supplement.py`，输出 `results/probe_supplement_A01.json`。不替代预先估计量，不改判据。

## 4. 未运行

反方向 B→A 已运行（用簇 7 的 GRAD 梯度测 A 的 EVAL）。大 R（≈1000）直接观测 η\*、匹配损失与 gate 的簇对：NOT RUN。
