# Purpose Card: E4.3 Simple Unsupervised Center Control

## 1. Purpose / Main Reason

E4 uniform 和 Zipf 结果显示 C7d/C7e 最接近可用 routing reference，但它们使用了 oracle-selected feature-prefix positions 做 center initialization。真实语言中没有这种人工 feature-prefix label，因此本实验做一个最小无监督对照。

核心问题：

```text
不用 feature label / feature-prefix positions，只从全 corpus 随机 token positions 做 KMeans 初始化 centers，
C7d/C7e 的效果是否还能保留？
```

## 2. Mainline Position

本实验仍属于 E4 Oracle-MoE router reference 线。它不推进 Reverse Index，只检查 C7d/C7e 的强结果有多依赖 oracle center initialization。

## 3. Known Narrative / Premise

已知结果：

- C7d/C7e 在 uniform shortcut controls 和 Zipf long-tail 上表现最好；
- 但 C7d/C7e 的 center 初始化来自 feature-prefix representations；
- 这使它们更像 synthetic routing reference，而不是真实可直接使用的方法。

## 4. Experiment Purpose

只跑 uniform `unique_uniform`，只新增两个 variants：

- U1: random-position KMeans init + C7d loss；
- U2: random-position KMeans init + C7e performance loss。

O1/O2 使用已有 C7d/C7e oracle-init 结果作 reference，不重跑。

## 5. Hypothesis And Sub-Hypotheses

主假设：

```text
H4.3: 如果 C7d/C7e 的效果主要来自 prototype loss / utility loss 本身，
那么无监督 random-position KMeans center init 也应接近 oracle-init reference。
```

子假设：

- H4.3a: 若 U1/U2 接近 O1/O2，则 oracle feature-prefix init 不是必要条件。
- H4.3b: 若 U1/U2 readback 好但 NMI 明显下降，则任务可学，但 feature-aligned routing 依赖 oracle init。
- H4.3c: 若 U2 selected-best 高但 NMI 低，则 utility routing 可行，但不是 feature-level one-feature-one-expert。
- H4.3d: 若 U1/U2 expert collapse，则 random-position KMeans 不足以稳定 allocation。

## 6. Experiment Object

数据：

```text
dataset = unique_uniform
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
counts = 3900 / 3900 / 3900 / 3900
vocab_size = 1000
```

模型：

```text
1-layer Transformer + Oracle-MoE
gate_input = raw attention_output
expert_input = original hidden / residual
router_type = trainable_center
num_experts = 4
```

## 7. Experiment Paradigm

初始化：

1. warmup 一个 raw-attention linear Oracle-MoE；
2. 从全 corpus 随机 token positions 采样 raw `attention_output`；
3. 用 100000 个随机位置做 KMeans，$K=4$；
4. 用 KMeans centers 初始化 trainable centers；
5. 继续训练 U1/U2。

U2 的 performance loss 需要 all-expert forced forward，额外 expert forward 约为 `num_experts=4`。

## 8. Expected Outcomes And Hypothesis Update Logic

- U1/U2 接近 O1/O2：无监督 random-position KMeans 已能替代 oracle feature-prefix init。
- U1/U2 readback 高但 NMI 低：C7d/C7e 的 feature routing 主要依赖 oracle feature-prefix init。
- U2 selected-best 高但 NMI 低：performance loss 学到 utility routing，但不是 feature identity routing。
- U1/U2 collapse：random-position KMeans center init 不足以稳定 expert allocation。

## 9. What This Can Prove

它能判断：C7d/C7e 的强结果是否依赖 oracle-selected feature-prefix center initialization。

## 10. What This Cannot Prove

不能证明真实语言无监督 routing 可行；也不能证明更复杂的无监督 center selection 不可行。本实验只测试最简单 random-position KMeans。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
