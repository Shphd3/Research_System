# Result Summary: E2-S Uniform Frequency Control

## Observation

本次控制实验已经跑完。目的很直接：把 E2-S 的四个 planted feature 从长尾频率 `10000/5000/500/100` 改成均匀频率 `3900/3900/3900/3900`，检查之前 spectral covariance router 的负结果是不是因为低频 feature 被长尾分布淹没。

数据仍是 all-trigram v1000：

| feature | relation | target count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 3900 |
| DEF | `[3,4] -> 23` | 3900 |
| GHI | `[6,7] -> 20` | 3900 |
| JKL | `[8,9] -> 21` | 3900 |

核心结果：均匀频率后，所有模型几乎都能稳定 readback；routing alignment 有所提高，但并不能支持“trained covariance 的中后段谱投影天然更语义、更适合 routing”。

| source | variant | readback | NMI | purity | load entropy | ablation drop |
|---|---|---:|---:|---:|---:|---:|
| none | `full_hidden_lb` | 0.994 | 0.645 | 0.608 | 1.386 | 0.433 |
| none | `full_hidden_no_lb` | 0.995 | 0.637 | 0.645 | 1.249 | 0.467 |
| trained_dense_cov | `midlate_25_90_raw_no_lb` | 0.997 | 0.661 | 0.651 | 1.206 | 0.580 |
| trained_dense_cov | `midlate_25_90_whiten_no_lb` | 0.997 | 0.688 | 0.649 | 1.214 | 0.676 |
| trained_dense_cov | `random_matched_42_no_lb` | 0.996 | 0.641 | 0.641 | 1.025 | 0.615 |
| random_init_cov | `midlate_25_90_raw_no_lb` | 0.996 | 0.562 | 0.565 | 1.247 | 0.496 |
| shuffled_dense_cov | `midlate_25_90_raw_no_lb` | 0.997 | 0.705 | 0.699 | 1.164 | 0.678 |
| shuffled_dense_cov | `midlate_25_90_whiten_no_lb` | 0.996 | 0.724 | 0.728 | 1.171 | 0.567 |

## Interpretation

第一，均匀频率确实让四个 feature 都变得容易学：所有主要变体的 readback probability 都约为 `0.994-0.997`。这说明 long-tail 设置里的低频困难不是模型容量问题，而是频率结构本身带来的诊断压力。

第二，trained midlate spectral router 在均匀频率下不再明显弱于 full-hidden router：`midlate_25_90_whiten_no_lb` 的 NMI 为 `0.688`，高于 `full_hidden_lb` 的 `0.645`。这说明频率均匀化会让 spectral router 的 feature alignment 变好。

第三，这个改善不是干净的谱语义证据，因为 shuffled covariance control 也达到甚至超过 trained covariance：`shuffled_dense_cov` raw/whiten 的 NMI 为 `0.705/0.724`。如果打乱顺序后的 covariance 也能给出强 routing alignment，就不能把结果解释成“trained dense hidden 的中后段谱子空间捕捉了 sequential semantics”。

## Limitation

`probe_accuracy=1.0` 在所有主要 projection 中都成立，说明这个 toy setting 中 feature label 太容易线性读出。它只能说明投影中存在 feature 信息，不能说明该投影是更好的 routing 统计量。

此外，本实验使用均匀 feature 频率，降低了原始长尾问题难度。因此它更像是 sanity/control，不应替代长尾设定下的主判断。

## Key Figures

![Routing NMI by projection](figures/routing_nmi_by_projection.png)

![Routing matrix comparison](figures/routing_matrix_midlate_vs_full_lb_vs_random.png)

![Readback by projection](figures/readback_by_projection.png)

![Expert load by projection](figures/expert_load_by_projection.png)

![Covariance spectrum by source](figures/covariance_spectrum_by_source.png)

## Claim Update

可以说：当四个人工 sequential features 频率均匀时，spectral midlate router 的 feature alignment 明显好于长尾设置，并且 readback 几乎完美。

不能说：trained covariance 的中后段谱子空间就是语义 routing 子空间。原因是 random/shuffled covariance controls 也能达到类似或更强的 routing alignment。

## Decision

No mainline update today. 这次结果说明“长尾频率确实影响 E2-S 表现”，但没有推翻 E2-S 的主结论：当前 global covariance midlate projection 还不是一个可靠、可归因的 feature routing 统计量。

下一步如果继续 spectral router 支线，应该转向更严格的统计量：feature-conditioned covariance、去 token shortcut 后的 residual covariance，或 shared-target/shared-prefix control 下的 covariance。
