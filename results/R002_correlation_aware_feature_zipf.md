# R002 Correlation-Aware Feature-Zipf Routing 实验报告

## 结论摘要

本实验没有支持“显式 feature-correlation routing 能带来稳定改进”。

在 correlated Feature-Zipf synthetic 数据上，correlation-aware z-gate 使用真实相关矩阵 `C` 后，tail Leaf NMI 比 feature-only z-gate 略高 `+0.0094`，但没有达到预设阈值 `+0.03`；Function Cos 反而低 `-0.0159`，并且只在 `1/3` seeds 上同时形成优势。更关键的是，正确 `C` 没有超过 shuffled `C` control。

因此，当前结果不应更新为“feature correlation 是下一阶段主线已验证方向”。它更像是一个负结果：仅把 `[z ; C z ; z * C z]` 喂给 router，还不能证明相关结构提供了超过 `z` 本身的有效信息。

## 与主线的关系

主线问题是：如果 hidden representations 由 common / group / unique sparse features 组合而成，MoE expert/path 是否能抓到 feature structure，并形成机制分工。

E001 Feature-Zipf 已经说明：

1. Hierarchical MoE 没有比 Flat MoE 更稳定地按 sparse atoms 分工；
2. expert 是否依赖 group / unique atoms，主要取决于这些 features 是否真的对应不同计算；
3. Hierarchical 的优势主要体现在函数结构更接近真实分层机制，而不是路由更清晰。

0508 组会后的新问题是：真实 features 可能不是独立的，而是存在语义/功能相关性。E002 就是在 E001 的基础上加一个最小检验：如果 common / group / unique features 存在相关结构，那么显式使用 feature-correlation matrix 的 router 是否能更好恢复 tail routing 和真实函数机制。

## 实验设计

数据仍然使用 Feature-Zipf synthetic，但加入相关结构：

- `rho=0.8`：在 group+unique 样本中，unique feature 有 80% 概率来自同一个 coarse block；
- 数据规模：train=20000，valid=5000，test=5000；
- seeds：`[0, 1, 2]`；
- 输出函数：variable-A / additive，即 common、group、unique feature 对应不同计算项；
- 相关矩阵 `C`：由训练集 feature co-activation 估计 positive PMI，保留每行 top-16 并归一化；
- shuffled control：随机打乱 `C` 的 feature index，用来检查 gain 是否真的来自正确相关结构。

比较模型：

| 编号 | 模型 | 含义 |
|---|---|---|
| M1 | Flat middle spectral + common | E001 中 feature-division 最强的 flat baseline |
| M2 | Hierarchical conditional_input | E001 中函数恢复最强的 learned hierarchical baseline |
| M3 | Hierarchical feature-only z-gate | 诊断模型，router 直接看真实 sparse activation `z` |
| M4 | Hierarchical correlation-aware z-gate | 诊断模型，router 看 `[z ; C z ; z * C z]` |
| Control | M4 with shuffled `C` | 检查正确相关结构是否必要 |

注意：M3/M4 是 diagnostic upper-bound 类型模型，不是可部署模型，因为 router 能直接看到真实 `z`。M4 router 参数量比 M3 更大，但 expert 参数量相同；如果 M4 仍不能稳定超过 M3，则更不应声称 correlation-aware routing 已被支持。

## 预设判据

只有同时满足以下条件，才认为 H2 被弱支持：

1. M4 在 tail Leaf NMI 上至少 `2/3` seeds 超过 M3；
2. M4 在 Function Cos 上至少 `2/3` seeds 超过 M3；
3. M4 平均 tail Leaf NMI 至少高 `+0.03`；
4. M4 平均 Function Cos 至少高 `+0.02`；
5. M4 test loss 不能比 M3 差超过 `2%`；
6. 正确 `C` 必须超过 shuffled `C` control。

## 主要结果

| Model | Loss ↓ | Tail Leaf NMI ↑ | Function Cos ↑ | True-feature diversity ↑ | Top feature overlap ↓ | Group+Unique ablation Δ ↑ |
|---|---:|---:|---:|---:|---:|---:|
| Flat middle spectral + common | 0.000167 | 0.3539 | 0.7791 | 0.0610 | 0.6598 | 0.000251 |
| Hier conditional_input | 0.000165 | 0.3401 | 0.8015 | 0.0440 | 0.7026 | 0.000254 |
| Hier feature-only z-gate | 0.000139 | 0.3814 | 0.8108 | 0.0832 | 0.6698 | 0.000276 |
| Hier corr-aware z-gate, correct C | 0.000141 | 0.3909 | 0.7949 | 0.0966 | 0.6343 | 0.000275 |
| Hier corr-aware z-gate, shuffled C | 0.000138 | 0.3910 | 0.8106 | 0.1069 | 0.5848 | 0.000278 |

说明：这里的 diversity / overlap 基于 synthetic 的真实 feature activation，而不是 sparse dictionary 学出来的 atom。因此它更适合作为 E002 内部诊断指标，不能直接和真实 DCLM 的 sparse dictionary 指标混用。

## 判据检查

| 判据 | 结果 | 是否通过 |
|---|---:|---|
| M4 correct C 在 Tail Leaf NMI 上胜过 M3 的 seeds 数 | 1/3 | 否 |
| M4 correct C 在 Function Cos 上胜过 M3 的 seeds 数 | 1/3 | 否 |
| 平均 Tail Leaf NMI delta, M4 correct C - M3 | +0.0094 | 否 |
| 平均 Function Cos delta, M4 correct C - M3 | -0.0159 | 否 |
| 平均 test loss relative delta, M4 correct C - M3 | +0.98% | 是 |
| correct C - shuffled C, Tail Leaf NMI | -0.0002 | 否 |
| correct C - shuffled C, Function Cos | -0.0156 | 否 |

最终判断：`H2 weakly supported = false`。

## 结果解释

M4 correct C 的 tail Leaf NMI 从 M3 的 `0.3814` 提到 `0.3909`，但提升很小，且跨 seed 不稳定。Function Cos 从 `0.8108` 降到 `0.7949`，说明它没有更好恢复真实函数机制。

shuffled C control 是最关键的负证据：shuffled C 的 Tail Leaf NMI `0.3910`、Function Cos `0.8106`，都不弱于 correct C。这说明 M4 的变化不能归因于正确 feature-correlation structure；更可能来自 router 输入维度扩大、训练噪声、或 z-gate 本身已经包含了可用相关信息。

Flat middle spectral 和 learned Hier conditional_input 在这个 correlated synthetic 上延续了 E001 的基本关系：Hier conditional_input 的 Function Cos 较高，Flat middle spectral 的 learned routing 不显示明显优势。真正强的是直接看真实 `z` 的 diagnostic z-gate，但这不等价于实际 hidden router 已经能发现这些 features。

## 对主线的更新

1. **Claim J 保持 unsupported。** 当前 relation-aware 设计 `[z ; C z ; z*Cz]` 没有通过最小实验，不应作为主线正结果写入。

2. **Claim D 不增强。** 本实验不能说明 Hierarchical MoE 比 Flat MoE 更会按 sparse features 分工；它只说明给 router 真实 `z` 会明显改善部分诊断指标。

3. **E001 主线结论基本不变。** Hierarchical 的主要优势仍然是函数结构恢复略强，而不是路由分工更清晰。

4. **下一步不应直接扩展 relation-aware 架构。** 更合理的下一步是先解释为什么 feature-only `z` 或 middle spectral routing 已经吃掉了相关性信号；如果继续做 correlation，需要换一个更有必要性的构造，例如只给不完整/有噪声的 `z`，检查 `Cz` 是否能补全缺失 feature 信息。

## 能说明什么 / 不能说明什么

能说明：

- 在当前 correlated Feature-Zipf synthetic 设定下，显式 correlation feature 没有稳定超过 feature-only z-gate；
- 正确 `C` 没有超过 shuffled `C`，所以不能把结果解释为利用了真实 feature correlation；
- M3/M4 这类 z-gate 诊断模型明显强于 learned hidden router，说明“看到真实 feature activation”本身很有帮助。

不能说明：

- 不能说明真实语言 hidden states 中不存在 feature correlation；
- 不能说明所有 correlation-aware routing 都无效；
- 不能说明 continual learning 或遗忘问题会因此改善；
- 不能把 z-gate 的改善等同于 learned MoE 在真实 hidden space 中自动发现了机制结构。

## 产物位置

- 结果目录：`results/e002_correlation_aware_feature_zipf/`
- 汇总表：`results/e002_correlation_aware_feature_zipf/summary_by_model.csv`
- seed 明细：`results/e002_correlation_aware_feature_zipf/all_seed_summary.csv`
- 判据 JSON：`results/e002_correlation_aware_feature_zipf/decision_summary.json`
- 运行日志：`logs/e002_cuda0_seeds_0_2.log`, `logs/e002_cuda1_seed_1.log`
