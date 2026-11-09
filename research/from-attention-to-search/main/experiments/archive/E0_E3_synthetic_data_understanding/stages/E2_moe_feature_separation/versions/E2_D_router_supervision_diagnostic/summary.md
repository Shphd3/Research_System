# Result Summary: E2-D Router Supervision Diagnostic

## Purpose And Hypothesis

目的：在均匀频率 synthetic data 上，直接给 router 真实 feature label，检查当前 MoE/router/expert/评估链路是否能形成 clean specialization。

核心假设 H-D：如果明确监督 router，当前 tiny MoE 应能把 ABC/DEF/GHI/JKL 固定路由到 expert 0/1/2/3，并保持 feature readback。

## Observation

E2-D full run 已完成。结果是 strong pass：只要加入 router feature auxiliary loss，router 迅速形成固定对角路由；`λ=0.1/1.0/5.0` 的 fixed-label router accuracy、NMI、ARI 全部达到 `1.0`。

| variant | router acc | router CE | NMI | ARI | readback | ablation drop | load entropy |
|---|---:|---:|---:|---:|---:|---:|---:|
| `moe_top1_no_lb` | 0.5100 | 1.2815 | 0.6369 | 0.4902 | 0.9951 | 0.4669 | 1.2493 |
| `moe_top1_lb` | 0.2829 | 1.3815 | 0.6452 | 0.5192 | 0.9945 | 0.4328 | 1.3859 |
| `router_aux_lam_0_1` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9964 | 0.9587 | 1.2397 |
| `router_aux_lam_1_0` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9962 | 0.9700 | 1.2617 |
| `router_aux_lam_5_0` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9963 | 0.9668 | 1.2320 |

固定对角 routing matrix：

| feature | aux result |
|---|---|
| ABC | expert 0 with probability 1.0 |
| DEF | expert 1 with probability 1.0 |
| GHI | expert 2 with probability 1.0 |
| JKL | expert 3 with probability 1.0 |

## Interpretation

这说明当前实现链路没有明显 bug：feature prefix-end 位置、feature id mapping、router logits、aux loss 梯度、evaluation routing 位置是对齐的。

更重要的是，它把 E2 的核心问题缩窄了：MoE 不是“不能”形成 clean specialization；而是在自然 NTP 目标下没有足够压力必须形成 one-feature-one-expert。

ablation drop 从 baseline 的约 `0.43-0.47` 提升到 `0.96-0.97`，说明被监督选中的 dominant expert 对对应 feature prediction 有强因果贡献，不只是 router 表面分配。

## Limitation

这不说明真实语言可以获得 feature label，也不说明真实 MoE 会自然形成语义专家。它只证明：在 controlled synthetic setting 中，如果给 router 明确 feature 信号，当前 tiny MoE 可以形成 clean specialization。

## Key Figures

![Routing matrix by lambda](figures/routing_matrix_by_lambda.png)

![Router feature accuracy by lambda](figures/router_feature_accuracy_by_lambda.png)

![Feature readback by lambda](figures/feature_readback_by_lambda.png)

![Ablation delta by lambda](figures/ablation_delta_by_lambda.png)

![Training loss and router auxiliary loss](figures/ntp_loss_and_router_aux_loss.png)

## Claim Update

可以说：在 synthetic feature label 可用时，当前 MoE 实现可以被明确监督成 clean feature-expert specialization；因此此前自然 MoE 不 clean 不是因为模型或代码完全做不到，而更可能是 NTP objective / specialization pressure 不足。

不能说：真实语言中的 semantic feature 可以这样监督；也不能说自然 MoE 会自动按语义分 expert。

## Decision

更新 E2 局部解释：`representation separability != natural router specialization` 仍成立；E2-D 进一步说明 `explicit feature supervision -> clean router specialization` 成立。下一步若继续 E2 主线，应研究自然 router objective 为什么不使用 feature direction，而不是继续怀疑实现链路。
