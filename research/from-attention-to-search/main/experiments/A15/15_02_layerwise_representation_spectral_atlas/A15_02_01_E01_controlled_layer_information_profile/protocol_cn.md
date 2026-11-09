---
experiment_id: A15_02_01_E01_controlled_layer_information_profile
anchor_id: 15_02_01_controlled_layer_information_identity
status: approved_for_smoke_and_full
approved_by: user
approval_date: 2026-07-31
canonical_language: en
---

# Protocol：四层 MoE 的层 × 频带 × 信息画像

## 0. Approval And Decision

用户已明确授权构造数据、通过能力门、训练、封存测试、每个模型训练两遍并完成比较。实现必须先 smoke；full 只有在数据与工程 guards 全过后启动。

## 1. Decision Question

在能力有效的四层 MoE 中，同一相对 covariance 频带在不同层是否承载不同的粗条件、中间状态与组合结果信息？

## 2. Hypothesis And Rivals

- **H1：**组合目标在特定层—频带形成超过同维随机方向的一步状态或组合结果可读性。
- **R0：**所有同维随机投影都同样可读，旧 Pilot 的饱和问题复现。
- **R1：**组合结果只因更接近输出而随深度可读；一步控制模型出现同样趋势。
- **R2：**模型没有真正组合，只记住已见 \((a,b)\) 对。

## 3. Controlled Dataset

有限域为 \(\mathbb Z_{17}\)。每条样本包含查询类型、共享 shift token \(a\)、value token \(x\)、独立 context token、共享 shift token \(b\) 与 ROOT token。真值为

\[m=(x+a)\bmod17,\qquad y=(m+b)\bmod17.\]

八个 shift 值构成 \(8\times8\) 组合。final-query 训练留出一个八对完美匹配；每个原子在其余七对中出现。mid-query 覆盖全部组合，用作组成能力监督。

context ids 冻结为：train 0--15；validation 16--19；covariance calibration 20--23；probe fit 24--25；probe validation 26--27；sealed test 28--31。切分间不得重用 context id。

两个模型条件拥有相同输入：

| 条件 | mid query | final query |
| --- | --- | --- |
| one-step control | \(m\) | \(m\) |
| composition | \(m\) | \(y\) |

因此两条件仅在 final-query 功能目标上不同。

## 4. Dataset Gates

必须全部通过：split/context hash 独立；final holdout 是完美匹配；每个 \(a,b,x\) 在训练出现；每个 split 目标边际精确均衡；oracle accuracy=1；输入不含答案 token；打乱任一功能 token 后 oracle 降至机会附近；只含 token one-hot 加和项、没有交互项的线性捷径在未见 final pairs 上准确率不高于 0.20。

## 5. Model

四层 pre-norm causal Transformer-MoE：width 256、8 heads、每层 8 个 top-1 experts、expert MLP width 512、GELU、序列长度 6。Gate 直接接收 MoE norm 输出；selected softmax probability 乘在专家输出上，保留 Gate 学习路径。无 shared expert、无 capacity drop、`lambda_lb=0`。所有模型共享非梯度 load-free score bias；bias 不进入 \(W\) 的频谱指标。

模型在第 2 层 ROOT 处增加一个只用于训练能力约束的中间状态读出头，预测 \(m=(x+a)\bmod17\)；第 4 层仍预测各条件注册的最终目标。总训练损失为最终目标交叉熵加等权的第 2 层中间状态交叉熵。该头不接收留出组合答案，也不进入频谱画像主指标。

两个条件均训练 seeds 17 与 29，共四个独立模型；初始化、数据顺序和优化器在同 seed 条件间配对。

## 6. Preflight And Training

测试集封存。仅用 seed 1001 和 validation 选择固定训练档：

1. 2,000 steps，LR \(10^{-3}\)；
2. 3,500 steps，LR \(10^{-3}\)；
3. 5,000 steps，LR \(5\times10^{-4}\)。

选择第一个使两个条件都通过 validation capability 的档位；若全失败，停止并修订 Protocol，不查看 sealed test。正式训练使用 AdamW、betas (0.9,0.95)、weight decay 0.01、100-step warmup、cosine decay、global batch 512、gradient clip 1.0。模型选择只看 validation，取连续三个评估点通过的最早 checkpoint。

**2026-07-31 测试开启前修订：**首轮预检表明，原非梯度 load-free bias 的更新率 0.01、截断值 1.0 会从约 400 步起持续触及截断边界；即使能力接近通过，也不满足“bias 不饱和”的有效性门。测试集从未打开。保持数据、模型、优化器、能力阈值和训练档位不变，仅将所有条件共享的 bias 更新率冻结为 0.003、截断值冻结为 4.0。validation seed 1001 的同档 2,000-step 检查中，control 在 900 步通过，composition 在 1,400 步通过；composition 未见组合 accuracy=0.897、NLL=0.615、seen-unseen gap=0.103，recent max expert share=0.372，最大 bias=1.130，未饱和。修订后必须重新运行完整 preflight 和 8-GPU smoke，旧 smoke 只保留为实现证据，不授权 full。

**2026-07-31 能力修订：**修订后的第一轮四模型 full 在封存测试开启前被 capability gate 阻断：两个 control seeds 通过，但 composition seeds 17/29 的 validation unseen-pair accuracy 为 0.711/0.871、NLL 为 2.277/0.909。负载均有效，说明通用模型仍可记忆已见 pair，而没有跨 seeds 稳定形成可重组的两步计算。保持输入、留出组合、四层 MoE、正式 seeds、主指标和所有阈值不变；加入等权的第 2 层中间状态监督，并新增 layer-2 unseen-pair \(m\) accuracy \(\ge0.95\)、NLL \(\le0.20\) 的能力门。该修订只把概率树的已知中间变量作为训练约束，不暴露 \(y\) 的留出组合。修订后重新执行数据审计、单测、mini-run、独立 validation preflight、8-GPU smoke 和 full；旧 full 保留为 `insufficient_composition_capability`。

## 7. Capability Gates

两个条件、两个 seeds 均要求：mid-query unseen-pair accuracy \(\ge0.95\)、NLL \(\le0.20\)；control final-query accuracy \(\ge0.95\)、NLL \(\le0.20\)；composition final-query unseen-pair accuracy \(\ge0.80\)、NLL \(\le0.75\)，且 seen-unseen accuracy gap \(\le0.15\)。所有层 recent max expert share \(\le0.65\)、每个 expert 均被使用、bias 不饱和。测试只在 validation gate 冻结后打开一次。

此外，第 2 层中间状态头必须在 final-query unseen pairs 上达到 accuracy \(\ge0.95\)、NLL \(\le0.20\)；该门用于确认模型确实形成第一步状态，不作为“某个 covariance 频带特异”的证据。

## 8. Spectral Profile

对每个模型、每层 ROOT 位置的实际 Gate 输入，在 calibration split 上拟合均值和 covariance 基底。两个 calibration halves 的相应 projector overlap 必须超过 256 个同维随机对照 q95。

细带为八个连续 32 维带；粗带为 H=`F1`、M=`F2--F4`、T=`F5--F8`。所有 probe 标准化与超参数只由 fit/validation 学习。

## 9. Primary Metric

对 \(q\in\{a,m,y\}\)，用训练样本数 \(n\in\{32,64,128,256\}\) 的 ridge linear probe 测 sealed-test accuracy，并取四个规模的平均值 \(A_{\ell,B,q}\)。该量表示“用很少标注样本从该子空间学会读出变量的难易度”。

每个真实频带与 64 个同维 Haar 随机子空间比较：

\[S_{\ell,B,q}=A_{\ell,B,q}-Q_{0.95}(A_{\ell,R_{d_B},q}).\]

组合目标增量为 \(\Gamma=S^{compose}-S^{control}\)。同时报告完整表征上限、初始化画像和逐 seed 数值，不只给聚合结果。

## 10. Secondary Causal-Use Audit

在 sealed final-query 上，仅从某层 Gate logits 中删除一个真实频带的贡献，专家输入保持 native；测 answer NLL、route flip 与 margin 变化。同维随机子空间重复 64 次。该指标只回答 Router 是否使用该带，不能证明该带对训练有益。

## 11. Statistics

随机方向 q95 控制方向偶然性；组合对为重采样单位做 2,000 次 paired bootstrap。两 seeds 是复现要求，不伪装为大样本统计。一个 cell 只有在两个 seeds 的 \(S>0\) 且 pooled 95% lower bound \(>0\) 时才称特异；层间身份变化还要求差分 \(\Gamma\) 在两 seeds 同向。

## 12. Execution Contract

- 本地/当前容器：数据生成、单元测试、CPU/GPU mini-run、提交 dry-run。
- ACP：单节点 `5090-8-spot`，workspace `share-space`，AEC2 `computing-cluster-5090-01g`，spec `n12lp.nn.i10a.8`，quota `spot`。
- smoke：四条件—种子槽位各 8 steps，检查 8 GPU、DDP 分组、Gate 梯度、bias 无梯度、实际输入 replay、数据 hash、checkpoint/resume 与 analyzer closure。
- full：四个模型并行，先 capability 后 sealed test/profile；失败模型不得进入画像结论。

## 13. Pass / Fail / Insufficient

- **Pass：**四模型能力有效，且至少一个层—频带—信息 cell 在两 seeds 超过同维随机并显示组合相对控制的复现增量。
- **Fail：**能力有效，但没有 cell 通过；这否定注册任务中的固定 covariance 频带身份，不否定其他功能坐标。
- **Insufficient：**数据、能力、负载、基底、两 seed 或封存测试任一 guard 失败。

## 14. Claim Boundary And Deliverables

交付数据 manifest/hash、四个 checkpoint、能力表、完整 coarse/fine profile CSV、中心热图、随机对照、ablation 表、`summary.md`、`detailed.md` 和次日认识更新。即使 Pass，也不声称跨层频带路由改善 NLL/FLOP；该问题必须进入独立兼容性 Protocol。
