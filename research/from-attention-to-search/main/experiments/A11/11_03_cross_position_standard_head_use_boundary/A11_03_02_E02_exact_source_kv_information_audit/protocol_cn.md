# Protocol：A11_03_02_E02 精确源 K/V 信息形成与 MTP 特异性审计

## 0. 审批快照

**批准状态：** 研究者已批准远程四卡 GPU 执行。  
**目的：** 判断 informative-MTP 的精确第二层 `U03` 源 K/V 是否形成可跨 nuisance 泛化的 branch 信息，以及该信息是否强于 matched shared-aux。  
**主要 Anchor：** [11_03_02 标准主头因果使用](../../../../problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor_cn.md)。  
**Anchor 决策关系：** 为既有 K/V 因果补丁负结果补齐源信息形成守卫，定位失败发生在精确 K/V 形成之前还是之后。  
**检验的物理先验：** 若信息性未来目标特异增强精确源 K/V 的 branch 表征，则固定复杂度的 held-out 线性读出在 informative-MTP 上应比 shared-aux 获得更低的 branch 预测交叉熵。  
**核心模型项：**

\[
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}.
\]

**主要证伪结果：** informative-MTP 的精确 K/V 绝对可读，但 \(\Gamma_{\mathrm{read}}\) 没有跨种子稳定为正。  
**实验角色：** 根因审计；不是方法构造、结构比较或重新检验主头使用。  
**唯一主要指标：** held-out 线性 probe 的 informative-MTP 相对 shared-aux 交叉熵改善，单位为 nat/样本。  
**最小设置：** 原 A11 数据、模型、五个配对种子和共同能力检查点；不改变训练目标或模型结构。  
**基本配置：** calibration 为 256 个 nuisance、1,024 条序列；confirmation 为 1,024 个 nuisance、4,096 条序列；精确特征为 \([K_{2,T};V_{2,T}]\in\mathbb R^{128}\)。  
**条件：** NTP、shared-aux、informative-MTP；主比较仅 informative-MTP 对 shared-aux，NTP 为次要系统基线。  
**重要实现边界：** 原正式运行没有保存模型 checkpoint。必须在 GPU 上按原种子、数据清单、批次顺序和代码合同重放训练，并先通过结果复现守卫；这属于 same-contract replay，不得写成读取原 checkpoint。  
**通过：** source-formation guard 通过；至少 `4/5` 个种子的 \(\Gamma_{\mathrm{read},s}>0\)，且配对分层 bootstrap 的五种子均值 95% 区间下界大于 `0`。  
**失败：** source-formation guard 通过；至少 `4/5` 个种子的 \(\Gamma_{\mathrm{read},s}\le0\)，且均值 95% 区间上界不大于 `0`。  
**证据不足：** replay 守卫失败、source-formation guard 失败、种子方向混合、置信区间跨 `0`，或结果只集中在单一种子/单一 branch 对。  
**不能声称：** 标准主头使用、完全零使用、K/V 含有全部 branch 信息、MTP 普遍优于 NTP、共享词表能够修复问题或真实任务收益。  
**审批决定：** 已批准；允许实现并在远程四卡 GPU 上执行 same-contract replay，不允许本地或 CPU smoke。

## 1. 术语与定义

| 术语 | 通俗含义 | 具体对象或计算 | 单位或公式 | 决策作用 | 不能证明 |
|---|---|---|---|---|---|
| 精确源 K/V | 既有补丁真正替换的注意力记忆 | 第二层 `U03` 的 \([K_{2,T};V_{2,T}]\) | 128 维向量 | 检查被干预对象是否含 branch 信号 | 下游是否使用 |
| held-out 线性可读性 | 简单线性分类器能否在未见 nuisance 上预测 branch | calibration 拟合、confirmation 冻结评估 | accuracy、CE | 检查稳定线性信号 | 任意非线性信息 |
| source-formation guard | informative-MTP 的精确 K/V 是否绝对可读 | confirmation accuracy 的 nuisance-bootstrap 下界 | 概率；随机为 `0.25` | 允许讨论形成后的失败 | MTP 特异性 |
| \(\Gamma_{\mathrm{read}}\) | informative-MTP 相对 shared-aux 的线性可读性增量 | \(\operatorname{CE}_{shared}-\operatorname{CE}_{info}\) | nat/样本 | 唯一主要指标 | 标准主头使用 |
| Fisher 分离比 | branch 间中心差异相对 branch 内 nuisance 波动 | \(\operatorname{tr}(S_B)/(\operatorname{tr}(S_W)+\epsilon)\) | 无量纲 | 诊断几何是否稳定 | 因果使用 |
| same-contract replay | 用相同代码合同重建原训练状态 | 相同种子、数据、批次和停止规则 | 布尔守卫 | 原 checkpoint 缺失时恢复分析对象 | 与原权重逐 bit 相同 |

## 2. Anchor 对齐

**决策问题：** informative-MTP 是否在 matched shared-aux 之外增强精确源 K/V 中可泛化的 branch 信息？  
**物理先验：** 若未来信息目标改变了被干预源表示，固定读出复杂度下的 held-out branch CE 应下降。  
**核心模型项：** \(\Gamma_{\mathrm{read}}\)。  
**主要证伪条件：** informative-MTP 的精确 K/V 可读，但相对 shared-aux 没有稳定 CE 改善。  
**结论边界：** 只定位既有两层、K=2、四分支 A11 中第二层 `U03` 联合 K/V 的源信息形成。

## 3. 待检验假设

主要假设：

\[
\Gamma_{\mathrm{read},s}>0
\]

在至少 `4/5` 个配对种子成立，并且均值的配对分层 bootstrap 95% 区间完全高于 `0`。

这只表示 informative-MTP 使精确 K/V 中的 branch 标签更容易被固定线性读出，不表示标准主头采用相同读出方向。

## 4. 最强替代解释

1. **晚形成：** branch 信息主要在第二层注意力与 MLP 后进入最终隐藏状态，因此 \(q_2(h_T^{final})\) 正确而精确 K/V 不可读。
2. **普通路径共同形成：** 三个条件均通过 `BR_z`、第一层或残差路径形成同等 K/V 信息，因此绝对可读但 \(\Gamma_{\mathrm{read}}\approx0\)。
3. **replay 状态不等价：** 原 checkpoint 未保存，重放没有恢复原共同能力状态；此时只能判证据不足。
4. **弱或冗余使用：** 这是原行为结果的剩余解释，本实验不能裁决。

## 5. 数据、模型与分析对象

- 复用原 `manifest_seed=20260715` 和 train/calibration/confirmation 划分；
- 复用种子 `971–975`；
- 复用 NTP、shared-aux、informative-MTP 模型与目标；
- 目标共同检查点依次为 `500, 500, 900, 600, 700`；
- 模型 replay 与 K/V 提取使用 GPU；
- 每个模型、种子和条件独立训练 probe，不跨模型传递 probe；
- confirmation 不参与标准化、正则强度或停止条件选择。

## 6. 条件、守卫与证据角色

| 项目 | 检验对象/替代解释 | 为什么需要 | 证据角色 | 通过 | 失败/不足 |
|---|---|---|---|---|---|
| replay 复现 | replay 状态不等价 | 原 checkpoint 未保存 | 必要守卫 | 检查点、能力和原 K/V 补丁结果复现 | 否则不足 |
| informative-MTP 绝对 probe | 晚形成 | 确认精确 K/V 是否已有信号 | formation guard | held-out 下界高于 `0.25`，至少 4/5 | 否则不能定位到形成后 |
| informative 对 shared-aux | MTP 特异增强 | 排除辅助头/损失结构 | 主要证据 | \(\Gamma_{\mathrm{read}}\) 稳定为正 | 稳定非正则失败；混合则不足 |
| NTP | 系统基线 | 描述普通 NTP 路径 | 次要证据 | 不参与主要通过 | 不改变主要判定 |
| label shuffle | probe 泄漏 | 防止 nuisance/实现泄漏 | 技术守卫 | confirmation accuracy 不高于 `0.30` | 否则不足 |
| 四类 recall 覆盖 | 单一 branch 对异常 | 检查 seed 972 式集中 | formation guard | informative-MTP 的四类 recall 均高于 `0.25`，至少 4/5 | 否则不足 |
| Fisher 与六对中心距离 | 单一 branch 对异常 | 描述几何是否集中 | 次要诊断 | 报告完整分布 | 不单独改变主要判定 |

## 7. 主要指标

对每个种子 \(s\) 和条件 \(o\)，只在 calibration 上拟合固定 L2 正则的四分类线性 probe：

\[
q_{o,s}(z\mid x)
=
\operatorname{softmax}(W_{o,s}x+b_{o,s}),
\]

\[
\min_{W,b}
-
\frac{1}{N_{cal}}
\sum_i\log q_{o,s}(z_i\mid x_i)
+
\frac{\lambda}{2}\|W\|_F^2,
\qquad
\lambda=10^{-3}.
\]

标准化参数只由 calibration 计算：

\[
x_i
=
\frac{S_i-\mu_{cal}}
{\max(\sigma_{cal},10^{-8})}.
\]

冻结 probe 后，在 confirmation 上计算：

\[
\operatorname{CE}_{o,s}
=
-
\frac{1}{N_{conf}}
\sum_i\log q_{o,s}(z_i\mid x_i).
\]

唯一主要指标：

\[
\boxed{
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}
}
\]

- \(\Gamma_{\mathrm{read}}>0\)：informative-MTP 的精确 K/V 更容易线性读出 branch；
- \(\Gamma_{\mathrm{read}}=0\)：没有观察到信息目标特异增强；
- \(\Gamma_{\mathrm{read}}<0\)：shared-aux 的精确 K/V 反而更容易读出。

选择 CE 而不是仅用 accuracy，是因为四分类 accuracy 可能同时饱和到 `1.0`；CE 仍能反映正确类别概率 margin。它也不能被解释为标准主头的 CE 或因果使用。

## 8. 次要指标

1. confirmation macro accuracy 与四类 recall；
2. 线性可解码信息下界：

   \[
   I_{\mathrm{lin},o,s}
   =
   \log 4-\operatorname{CE}_{o,s};
   \]

3. Fisher 分离比：

   \[
   F_{o,s}
   =
   \frac{
   \frac14\sum_z\|\mu_z-\mu\|_2^2
   }{
   \frac1N\sum_i\|x_i-\mu_{z_i}\|_2^2+\epsilon
   };
   \]

4. 六个无序 branch 对的标准化中心距离；
5. confusion matrix；
6. NTP 相对 shared-aux 与 informative-MTP 的描述性差异。

## 9. 已知好、坏与易混淆案例

- **已知好：** 最终隐藏状态由已训练 \(q_2\) 线性读出 branch，准确率为 `1.0`；
- **已知坏：** 打乱 calibration branch 标签后，confirmation 读出应接近 `0.25`；
- **易混淆：** seed 972 的原 K/V 补丁只在一个替换方向显著；任何只由 `3↔1` 驱动的分离都不算稳定机制。

## 10. 阶段审计

| 阶段 | 本地问题 | 通过 | 不通过后的含义 |
|---|---|---|---|
| replay | 是否恢复原共同能力状态 | 原检查点和行为统计复现 | 证据不足，不能读取新指标 |
| extraction | 是否读取精确第二层 `U03` K/V | tensor 位置、形状和自检一致 | 实现错误 |
| absolute formation | informative-MTP K/V 是否可读 | 至少 4/5 高于 chance | 不能说信息已进入精确 K/V |
| specificity | 是否强于 shared-aux | \(\Gamma_{\mathrm{read}}\) 通过 | 决定 MTP 特异增强 |
| geometry | 是否跨 pair 稳定 | 非单 seed/单 pair 驱动 | 否则证据不足 |

## 11. 算法实现合同

```text
input:
  原配置、manifest_seed、5 个种子、3 个条件、原共同检查点

replay:
  按原初始化和批次顺序在 GPU 上重放
  检查 selected step、q1/q2 能力、原 K/V 补丁 C 值

extract:
  对 calibration 和 confirmation 前向
  读取 k2[:, U03, :] 与 v2[:, U03, :]
  沿最后一维拼接成 [N, 128]

fit:
  calibration-only 均值/标准差
  零初始化四分类线性 probe
  float64、固定 L2、固定优化收敛条件

evaluate:
  冻结 probe
  计算 confirmation CE、accuracy、recall、confusion
  计算 Fisher 比与六对中心距离

uncertainty:
  以 nuisance ID 为整组单位重采样
  每次同时保留该 nuisance 的四个 branch
  shared-aux 与 informative-MTP 使用同一重采样索引
  外层按配对 seed 重采样，报告均值 95% 区间

outputs:
  replay_guard.csv
  probe_by_condition_seed.csv
  probe_confusion.csv
  fisher_by_condition_seed.csv
  pairwise_centroid_distance.csv
  bootstrap_gamma_read.csv
  source_kv_information_audit.png
```

## 12. 通过、失败与证据不足

**通过 MTP 特异增强：**

- replay、数据、probe 与 label-shuffle 守卫全部通过；
- informative-MTP absolute formation guard 在至少 `4/5` 种子通过；
- 上述通过种子的 informative-MTP 四类 recall 均高于 `0.25`；
- \(\Gamma_{\mathrm{read},s}>0\) 在至少 `4/5` 种子成立；
- 五种子均值的配对分层 bootstrap 95% 区间下界大于 `0`；
- Fisher 与六对中心距离只作几何诊断，不作为第二主要判据。

**失败 MTP 特异增强：**

- 所有必要守卫和 absolute formation guard 通过；
- \(\Gamma_{\mathrm{read},s}\le0\) 在至少 `4/5` 种子成立；
- 均值 95% 区间上界不大于 `0`。

**证据不足：** 其余情况。

## 13. 不能声称

- 可读性等于标准主头使用；
- probe 的方向等于 receiver query 或标准输出头方向；
- 接近随机等于 K/V 没有任何非线性 branch 信息；
- 更高分离度来自 attention 而不是 embedding、第一层、残差或直接 `BR_z` 路径；
- MTP 在其他层、位置、跨度、任务或模型结构上具有同样效果。

## 14. 审核记录

- 本 Protocol 只补齐原实验遗漏的 source-information audit；
- 原正式运行未保存 checkpoint，因此不能执行“直接读取现有 checkpoint”的原计划；
- 研究者已授权远程四卡 GPU 实现与执行；不运行本地或 CPU smoke。
