# Purpose Card: E4 Raw-Attention Dingyi-Style Oracle Init

## 1. Purpose / Main Reason

本实验修正旧 E4 的一个实现边界：旧 E4 的 router 原始输入是 `attention_output`，但算 logits 前经过了 `LayerNorm`。本轮把 C0-C6 全部改成 raw `attention_output` 直接进入 router；同时新增 C7，完全按 Dingyi 的 oracle-init prototype router 流程做可比实现。

核心问题：

```text
在真正 raw attention-output routing 下，
我们原有 C0-C6 结论是否保持？
Dingyi-style oracle initialized prototype router 是否比随机 prototype 更能形成 feature-aligned expert routing？
```

## 2. Mainline Position

这仍属于 router failure mode 诊断线。前序结果显示：

- feature representation 可分，不等于 natural router 会按 feature 分 expert；
- C5/C6 clean inhibition 能增强 expert 功能排他性，但旧结果处在 `LN(attention_output)` router-space；
- Dingyi 的 oracle-init 结果提示：如果先用已有表示空间中的 feature clusters 初始化 expert centers，router 可能更容易形成稳定分区。

## 3. Known Narrative / Premise

Dingyi 方法的关键不是给 feature label 做 supervised router CE，而是：

1. 先训练一个 warmup 模型；
2. 在 feature-prefix 位置收集 router 输入表示；
3. 用 KMeans 得到 feature-space centers；
4. 用这些 centers 初始化 prototype router；
5. 继续 NTP 训练，观察这些 centers 是否能保持 feature-aligned routing。

## 4. Experiment Purpose

本轮回答三个局部问题：

1. C0-C6 在 raw `attention_output` router setting 下是否复现旧 E4-LN 的主要结论；
2. raw `attention_output` 中是否存在足够干净的 feature cluster，可用于 oracle center 初始化；
3. oracle-initialized prototype router 是否比 random prototype 更接近 clean feature-expert assignment，同时保持 readback 和 expert utility。

## 5. Hypothesis And Sub-Hypotheses

主假设：

```text
H-C7: 如果 raw attention_output 已经包含可聚类的 feature context 信息，
那么用该空间的 KMeans centers 初始化 prototype router，
会比随机 prototype 更稳定地形成 feature-aligned routing。
```

细化假设：

- H-C7a: warmup raw attention-output 的 feature-prefix 表示可以被 KMeans 聚成较高 purity / NMI 的 clusters。
- H-C7b: frozen oracle centers 能把这些 clusters 直接转成 routing prior。
- H-C7c: trainable oracle-init centers 在 NTP 训练中不会被完全冲散。
- H-C7d: Dingyi-style attraction / score-margin inhibition / homeostasis 可以改善 collapse 或 sharpen centers，但不一定改善 expert utility。
- H-C7e: performance-gated feedback 可能改善 router 选中 best expert 的比例，但可能牺牲 feature purity。

## 6. Experiment Object

数据仍为 `unique_uniform` synthetic trigram：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

模型仍为 1-layer Transformer + Oracle-MoE：

```text
gate_input   = raw attention_output
expert_input = original hidden / residual
```

## 7. Experiment Paradigm

对比 C0-C6 raw-attn 与 C7 系列：

- C0-C6: 我们原来的 C-series router / inhibition 设计，但全部使用 raw `attention_output`；
- C7a: Dingyi random prototype；
- C7b: Dingyi frozen oracle router；
- C7c: Dingyi oracle-init trainable router；
- C7d: Dingyi oracle-init + attraction / score-margin inhibition / homeostasis；
- C7e: Dingyi oracle-init + performance-gated feedback。

## 8. Expected Outcomes And Hypothesis Update Logic

- 若 C7b/C7c 明显优于 C7a：支持 oracle center 初始化有效，问题不只是 prototype 形式。
- 若 C7d 优于 C7c：支持 Dingyi-style inhibition/homeostasis 能稳定 feature basins。
- 若 C7e selected-best 提升但 NMI 下降：说明功能反馈有用，但会把 feature clusters 合并。
- 若 warmup KMeans 本身 purity 低：不能说 oracle-init 无效，只能说 raw attention-output 统计量不够干净。
- 若 C7b/C7c 也不优于 C7a：说明 raw attention-output 的 oracle centers 没有转成稳定 routing prior。

## 9. What This Can Prove

可以证明或反驳：

```text
raw attention-output feature clusters 是否能作为 prototype router 初始化信号。
```

## 10. What This Cannot Prove

不能证明：

- 真实语言中有同样的 feature labels；
- natural MoE 会自己发现这些 centers；
- one-feature-one-expert 已经足够进入 Reverse Index；
- Dingyi-style score-margin inhibition 等同于 C5/C6 expert-level clean inhibition。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
