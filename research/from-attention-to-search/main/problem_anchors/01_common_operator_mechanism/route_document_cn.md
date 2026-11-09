# 路线文档：01 Common Operator Mechanism

## 当前路线决策

01 线现在不应该进入方法构造。

当前结论：

```text
受控 common estimation 是机制条件化的；
真实低秩 gate-logit common 不充分。
```

下一步路线决策：

```text
把真实 logit collapse 分解为 gate-weight drift、hidden-state drift 和交互项。
```

## 四阶段

| Stage | Anchor | 决策 | 证据 | 状态 |
|---|---|---|---|---|
| 1. 可识别性 | `01_01`, `01_02` | common 是单一 estimator，还是机制索引？ | A01_01: `criterion_winner_diversity=4` | 已完成 |
| 2. optimization-common estimator | `01_03` | optimization common 更接近 activation covariance 还是 gradient covariance？ | A01_03: `n_passed_mismatch_regimes=4/4` | 已完成 |
| 3. feedback bridge | `01_04` | feedback-common replay/removal 能否解释 preservation collapse？ | A01_04 controlled: `2/2`, controls ok；real gate-logit: `pass=false` | 受控支持；真实低秩 logit 削弱 |
| 4. 方法前真实分解 | next anchor | 真实 collapse 来自哪一项？ | 待分解 \(z_t-z_0\) | 下一步 |

## 源文件

| 作用 | 路径 |
|---|---|
| A01_01 summary | `../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md` |
| A01_03 summary | `../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md` |
| A01_04 controlled summary | `../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md` |
| A01_04 real-DCLM summary | `../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md` |

## Stop Rule

在测量真实 collapse 分解前，不从这条线启动 common branch、residualized MoE
或 anti-feedback method protocol：

\[
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
\]
