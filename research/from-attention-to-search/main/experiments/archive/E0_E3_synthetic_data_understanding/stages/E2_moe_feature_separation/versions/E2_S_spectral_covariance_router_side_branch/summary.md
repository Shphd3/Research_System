# Result Summary: E2-S Spectral Covariance Router Side Branch

## Observation

本支线的目的，是检验“全局 hidden covariance 的中后段谱子空间”能否作为无 LB router 输入，让 MoE 更自然地按人工 sequential feature 分 expert。

核心结果：不支持强假设。`midlate_25_90_raw_no_lb` 和 `midlate_25_90_whiten_no_lb` 都能保持 feature readback，但 routing alignment 明显弱于普通 full-hidden router，也弱于同维随机子空间对照。

| source | variant | readback | NMI | purity | load entropy | ablation drop |
|---|---|---:|---:|---:|---:|---:|
| none | `full_hidden_lb` | 0.948 | 0.809 | 0.945 | 1.386 | 0.457 |
| none | `full_hidden_no_lb` | 0.910 | 0.819 | 0.946 | 1.218 | 0.503 |
| trained_dense_cov | `midlate_25_90_raw_no_lb` | 0.948 | 0.429 | 0.691 | 1.306 | 0.515 |
| trained_dense_cov | `midlate_25_90_whiten_no_lb` | 0.946 | 0.443 | 0.688 | 1.317 | 0.519 |
| trained_dense_cov | `random_matched_42_no_lb` | 0.950 | 0.797 | 0.873 | 1.216 | 0.554 |
| random_init_cov | `midlate_25_90_raw_no_lb` | 0.940 | 0.546 | 0.754 | 1.270 | 0.326 |
| shuffled_dense_cov | `midlate_25_90_raw_no_lb` | 0.928 | 0.453 | 0.701 | 1.189 | 0.403 |

## Interpretation

第一，midlate projection 不是失败在 readback：四个 feature 仍能被预测，说明 expert path 没有坏掉。

第二，失败点在 routing alignment：中后段谱投影里的 feature 信息可线性读出，但 router 没有因此形成更强的 feature-aligned expert choice。

第三，同维随机子空间表现很强，说明当前结果不能说明“中后段谱方向”比一般低维投影更接近语义 routing 子空间。

## Limitation

`probe_accuracy=1.0` 在多个 source 和 projection 中都成立，说明这个 toy corpus 的 feature label 很容易线性读出；因此 probe 成功不能单独证明谱中后段有特殊语义价值。

`variant_summary_table.csv` 中少数聚合值与明细表不完全一致。本报告数字直接从 `routing_alignment_table.csv`、`readback_table.csv`、`ablation_delta_table.csv` 重新聚合。

## Key Figures

![Routing NMI by projection](figures/routing_nmi_by_projection.png)

![Routing matrix comparison](figures/routing_matrix_midlate_vs_full_lb_vs_random.png)

![Readback by projection](figures/readback_by_projection.png)

![Fisher ratio by projection](figures/fisher_ratio_by_projection.png)

![Covariance spectrum by source](figures/covariance_spectrum_by_source.png)

## Claim Update

可以说：在这个 all-trigram toy setting 中，改变 router 输入子空间会明显改变 routing 行为；但是 trained covariance 的中后段谱投影没有比普通 full-hidden router 或同维随机投影更稳定地对齐人工 feature。

不能说：谱中后段就是语义子空间；不能说去掉 top covariance directions 会自然带来更好的 feature routing；也不能把该负结果外推到真实语言语义。

## Decision

不更新主线 `current_mainline.md`。E2-S 作为负向支线结果保留：它削弱“无监督谱中后段投影可直接改善 MoE feature routing”的假设。

下一步若继续这条支线，应先改统计问题，而不是直接改 router：需要区分 global covariance、feature-conditioned covariance、以及 residualized covariance 哪一种统计量真正对应 feature relation。
