# Result Summary: linear_ffn_frequency_anisotropy

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

Story: 先不用 MoE / hierarchy，检验最小线性机制：频率不均衡是否足以让 FFN 矩阵学出 head-dominant anisotropy。

## 0. Closure Summary

目的：

验证导师建议的最小 toy：在 $x=k_c+k_{u_i}+\epsilon,\ y=v_c+v_{u_i}$ 中，Zipf 频率是否会让线性 FFN $W$ 优先学习高频 unique feature，并形成更尖的 singular spectrum；inverse-frequency reweight 是否能压回这个偏置。

假设 / 问题：

当前最小假设不是 “H-MoE works”，而是：组合 feature 中的频率不均衡会让 FFN 优先强化 common / head feature，形成 anisotropic direction；这可能解释 router 为什么容易被 common/token/frequency component 主导。

结论：

结果支持 “频率不均衡会造成 head-feature 优先学习和矩阵 anisotropy”，也支持 “normalized inverse-frequency reweight 可以消除这个偏置”。0529 subspace audit 修正了 top-1 版本的边界：Zipf-normal 的 top-1 direction 主要对齐 head unique feature，不是 common；但 common mode 在 top-32 input/output subspace 中被强覆盖。因此更准确的结论是：Zipf 下 $W$ 的高能子空间同时服务 common mode 和 head unique feature，tail feature 被推到更分散、更低能的方向。

SVD side audit：

runner 中 `LinearFFN.forward()` 是 `return x @ self.W`，不是 `nn.Linear(x)` / `F.linear(x, weight)` / `x @ W.T`。因此若 `U, S, Vh = torch.linalg.svd(W)`，则

$$
xW = xU\Sigma V^T.
$$

本实验 input/key side 应看 `U[:,0]`，output/value side 应看 `Vh.T[:,0]`。这个 convention 和报告中的 alignment 计算一致。

关键证据：

| Step | Condition | Top Energy | Effective Rank | Tail/Head Full MSE | Head Key Align | Head Value Align |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 100 | uniform_normal | 0.0247 | 141.3 | 1.00 | 0.020 | 0.016 |
| 100 | zipf_normal | **0.0380** | **111.1** | **8.04** | **0.100** | **0.156** |
| 100 | zipf_reweight | 0.0315 | 143.3 | 1.03 | 0.020 | 0.013 |
| 1000 | uniform_normal | 0.0174 | 142.9 | 1.04 | 0.036 | 0.092 |
| 1000 | zipf_normal | **0.0316** | **108.6** | **32.32** | **0.099** | **0.177** |
| 1000 | zipf_reweight | 0.0174 | 142.5 | 1.05 | 0.035 | 0.085 |
| 5000 | uniform_normal | 0.0175 | 142.9 | 1.02 | 0.036 | 0.094 |
| 5000 | zipf_normal | **0.0314** | **108.9** | **33.12** | **0.095** | **0.171** |
| 5000 | zipf_reweight | 0.0174 | 142.6 | 1.06 | 0.036 | 0.093 |

Subspace evidence at step 1000, r=32:

| Side | Condition | Common Coverage | Head Coverage | Tail Coverage | Common Weighted | Head Weighted | Tail Weighted |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| key | uniform_normal | 0.004 | 0.079 | 0.075 | 0.008 | 0.158 | 0.150 |
| key | zipf_normal | **0.978** | **0.454** | 0.079 | **0.989** | **0.614** | 0.100 |
| key | zipf_reweight | 0.007 | 0.080 | 0.080 | 0.012 | 0.157 | 0.155 |
| value | uniform_normal | 0.003 | 0.351 | 0.338 | 0.006 | 0.731 | 0.701 |
| value | zipf_normal | **0.984** | **0.795** | 0.139 | **0.994** | **1.177** | 0.178 |
| value | zipf_reweight | 0.005 | 0.345 | 0.335 | 0.010 | 0.698 | 0.674 |

结论边界：

这是线性 MSE toy，不是 NTP Transformer，也不是 router 实验。它证明频率足以在最小 setting 里制造 head/tail 学习差异和 $W$ 的谱偏置，并且 common mode 可以进入高能 top-r 子空间；它不能直接证明 MoE router 的 common dominance，因为 router 读的是 hidden state 和 routing logits，不是这个线性 $W$ 本身。

下一步决策：

先暂停继续加 hierarchy。若要回到 MoE，应把新假设写成：router failure 可能来自 common / 高频 component 的表示优势；下一步要在 router 输入上区分 common dominance 与 head-frequency dominance，而不是笼统说 H-MoE 会解决。

## Key Figures

![Core trajectory](figures/trajectory_core_metrics.png)

支持：Zipf-normal 的谱更尖、effective rank 更低、tail/head error 持续升高；reweight 基本回到 uniform。

![Seed trajectory](figures/tail_head_error_by_seed.png)

支持：head-tail 差异不是单 seed 偶然，而是在不同 seeds 中稳定出现。

![Singular spectrum](figures/singular_spectrum_selected_steps.png)

支持：Zipf-normal 的 singular spectrum 更尖；reweight spectrum 接近 uniform。

![Feature error by rank](figures/feature_error_by_rank_step1000.png)

支持：Zipf-normal 在高频 rank 处 error 低，在 tail rank 处 error 高；reweight 消除了这个频率梯度。

![Key subspace coverage](figures/subspace_coverage_key.png)

支持：只看 top-1 会漏掉 common；Zipf-normal 的 common key mode 在 top-32 子空间被强覆盖，head key 比 tail key 更早进入高能子空间。

![Value subspace coverage](figures/subspace_coverage_value.png)

支持：输出侧同样显示 common value 和 head value 进入 top-r 子空间，tail value coverage 明显滞后。

![Common alignment heatmap](figures/common_singular_alignment_heatmap.png)

支持：common mode 与 top-i singular vectors 的关系不是 top-1，而是集中出现在后续 top-r directions。

![Sigma weighted common alignment heatmap](figures/common_singular_alignment_sigma_weighted_heatmap.png)

支持：加上 $\sigma_i$ 权重后，common mode 仍在 Zipf-normal 的高能子空间中可见。

## Claim Update

Supported:

- 频率不均衡会让线性 FFN 先学 head feature，tail feature 被压住。
- Zipf-normal 的 $W$ 更 anisotropic：top energy 更高、effective rank 更低。
- normalized inverse-frequency reweight 能把 head/tail error 和 spectrum 拉回 uniform 附近。
- Top-r subspace analysis 显示，Zipf-normal 中 common mode 虽然不是 top-1，但进入了 top-32 高能子空间；head unique feature 比 tail feature 更早、更强地进入高能子空间。

Weakened:

- “只看 top-1 singular direction 就能判断 feature dominance” 被削弱。top-1 会漏掉 common mode，并低估 head feature 的低维子空间结构。

Still unclear:

- 真实 NTP hidden state 中，router 被 common component 主导还是被 head/frequency component 主导，需要回到 router 输入做 factor attribution。

## What Cannot Be Claimed

不能说 H-MoE 已经被支持。

不能说 MoE router 的失败已经由这个 toy 完全解释。

不能说 common-residual 一定有效；这个实验只说明 reweight 能在最小线性 setting 中消除 frequency-induced anisotropy。

## Next Decision

下一步如果回到 MoE，优先做一个 router-factor attribution：把 common component、B identity、head-frequency unique component 分开，看 routing logits 到底绑定哪一个。
