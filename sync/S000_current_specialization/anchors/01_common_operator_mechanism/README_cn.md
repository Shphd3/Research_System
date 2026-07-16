# 01 Common Operator Mechanism

这个文件夹是 01 common-operator 机制线。

先读一个入口即可：

```text
route_document_cn.md
```

只有在审计某个阶段时，再读对应 anchor：

```text
01_01_common_operator_identifiability_anchor.md
01_02_ground_truth_projector_recovery_anchor.md
01_03_gradient_common_vs_activation_common_anchor_cn.md
01_04_feedback_common_preservation_bridge_anchor.md
```

## 当前裁定

```text
common 不是一个通用 hidden-state 方向。
common 是一族由机制判据索引的算子。
```

当前结果链：

| Stage | Result |
|---|---|
| A01_01 identifiability | `criterion_winner_diversity = 4` |
| A01_03 gradient vs activation | `n_passed_mismatch_regimes = 4 / 4` |
| A01_04 controlled feedback bridge | `n_passed_main_feedback_regimes = 2 / 2`, `controls_ok = true` |
| A01_04 real-DCLM gate-logit bridge | `pass=false`, `mean_explain_valid=0.4230`, `mean_rescue_valid=0.1625` |

下一步决策：

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

## 文件

| 作用 | 路径 |
|---|---|
| 中文路线 | `route_document_cn.md` |
| 英文路线 | `route_document.md` |
| 可识别性 anchor | `01_01_common_operator_identifiability_anchor.md` |
| 恢复能力 anchor | `01_02_ground_truth_projector_recovery_anchor.md` |
| gradient-vs-activation anchor | `01_03_gradient_common_vs_activation_common_anchor.md` |
| feedback bridge anchor | `01_04_feedback_common_preservation_bridge_anchor.md` |

这个文件夹不能直接支持 common branch、residualized MoE 或 utility claim。
这些方法必须等真实 collapse 分解完成后再进入主线。
