# Experiment Card: E2-S Spectral Covariance Router Side Branch

## 1. Purpose / Main Reason

本支线检验一个谱空间直觉：全局 hidden covariance 的 top directions 可能包含 cone effect 和高频干扰；去掉 top directions 后的 middle-to-late subspace，可能更接近人工 sequential feature 的“语义”差异。我们要判断这个子空间是否能作为 MoE router 输入，让 expert choice 更按 feature 路由。

## 2. Mainline Position

E2.1/E2.2 已经说明：feature representation 在 router input 中可分，但 learned router 不自然按 feature direction 干净切分。本支线接在这个问题之后，专门测试“换一个无监督谱投影输入”是否能改善 router 的切分依据。

## 3. Known Narrative / Premise

已知前提：

- all-trigram synthetic data 是干净的；
- dense Transformer 能读回 `[A,B]->C` feature；
- MoE 能形成 feature-expert alignment，但不是 clean one-feature-one-expert；
- 之前粗糙的 spectral midband routing 在 R1 retrieval 里没有形成可靠正结果。

因此这次必须先检查 $\mu$ 与 covariance 统计是否可靠，再判断中后段子空间是否有 routing value。

## 4. Experiment Purpose

本实验要区分两个失败来源：

1. 效果不好，是不是因为全局 covariance / $\mu$ 统计量本身没有捕捉 feature structure；
2. 如果统计量可靠，中后段投影是否真的比 full hidden、top-only、tail-only、random subspace 更利于 feature-aligned routing。

## 5. Hypothesis And Sub-Hypotheses

核心假设 H-S：

```text
全局 covariance 去掉 top directions 后的 middle-to-late subspace 更保留 feature-level relation；即使不加 LB loss，用该投影作为 router 输入也能让 expert choice 更对齐人工 sequential features。
```

细化假设：

- H-S1: global $\mu$ 与 covariance 统计稳定，trained dense hidden covariance 比 random-init / shuffled covariance 更能保留 feature structure。
- H-S2: middle-to-late band 的 feature separability 高于 top-only、tail-only、random matched subspace。
- H-S3: 无 LB 的 middle-to-late router 在 readback 不下降时，routing NMI / purity / ablation delta 接近或优于 `full_hidden_lb`。
- H-S4: 若 projection probe 可分但 spectral router 不对齐，则问题不在统计量，而在 NTP router objective 没自然使用这些方向。
- H-S5: 若 spectral router collapse，则说明没有 LB 时谱投影不足以维持可用 expert allocation。

## 6. Experiment Object

数据对象固定为非层级 all-trigram corpus：

```text
ABC: [1,2] -> 22, count 10000
DEF: [3,4] -> 23, count 5000
GHI: [6,7] -> 20, count 500
JKL: [8,9] -> 21, count 100
```

模型对象是 1-layer causal Transformer + 4-expert top-1 MoE FFN。

## 7. Experiment Paradigm

先从 dense hidden states 估计 global $\mu$ 与 covariance，再构造多个 router-input projections。Spectral variants 只改变 router 输入，expert FFN 仍接收原始 hidden state。

关键对照：

- `full_hidden_lb`: 普通 router + LB loss；
- `full_hidden_no_lb`: 普通 router，无 LB；
- spectral projection routers: 全部无 LB；
- random matched subspace: 同维度随机投影对照。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 middle-to-late no-LB router 接近或超过 `full_hidden_lb`，并超过 `full_hidden_no_lb` / random subspace，则支持谱中后段投影具有独立 routing value。

如果 middle-to-late probe 可分但 routing 不改善，则说明 feature 信息在投影中存在，但 router objective 没自然使用。

如果 middle-to-late probe 本身不优于 random/shuffled covariance，则说明当前 global covariance 中后段不是可靠 feature statistic。

如果只有 `full_hidden_lb` 表现稳定，则说明当前 feature routing 主要依赖普通 hidden + LB，而不是无监督谱投影。

## 9. What This Can Prove

它可以检验 controlled all-trigram setting 下，global hidden covariance 的 middle-to-late subspace 是否有 feature routing value。

## 10. What This Cannot Prove

它不能证明真实语言语义位于 covariance 中后段；不能证明 spectral direction 等于 semantic mechanism；也不能证明 MoE router 可直接作为真实 KV retrieval index。

## 11. Result

Full run completed. Middle-to-late spectral routers kept feature readback high, but did not improve feature-aligned routing over ordinary full-hidden routers or same-dimensional random projection.

## 12. Conclusion

H-S is not supported in this toy setting. The projection contains feature information, but the learned router does not turn this middle-to-late covariance subspace into better expert specialization.

## 13. Next Step

Do not update the mainline claim. If this side branch continues, test better-defined statistics such as feature-conditioned covariance or residualized covariance, rather than treating global covariance midlate bands as semantic by default.
