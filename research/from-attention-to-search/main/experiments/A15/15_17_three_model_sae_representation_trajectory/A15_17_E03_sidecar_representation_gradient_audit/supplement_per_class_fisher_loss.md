# Post-hoc Supplement: Per-Class Fisher, Representation Surfaces, Loss Scale, And Coefficient Implications

Parent result: [summary.md](summary.md)  
Chinese companion: [supplement_per_class_fisher_loss_cn.md](supplement_per_class_fisher_loss_cn.md)  
Status: `POST_HOC_EXPLORATORY`; read-only analysis of qualified caches and immutable training ledgers; no new GPU job and zero optimizer updates.

## Measurement definition

For class \(c\), let \(\mu_c\) be its report-set mean and let \(\bar{\mu}\) be the unweighted mean of all class means:

\[
B_c=\lVert\mu_c-\bar{\mu}\rVert_2^2,
\qquad
W_c=\mathbb{E}_{x\in c}\lVert x-\mu_c\rVert_2^2,
\qquad
F_c=\frac{B_c}{W_c}.
\]

The existing class-balanced global Fisher ratio is reconstructed as

\[
F=\frac{\operatorname{mean}_c B_c}{\operatorname{mean}_c W_c},
\]

not as the mean of (F_c). Every recomputed global value matches the qualified E03 aggregate table within numerical tolerance.

The two internal surfaces are the raw Attention output passed to the SAE encoder and the SAE reconstruction. S7, S37, and SALL all use the raw Attention output as SAE encoder input. The reconstruction is not fed back into the native LM forward path.

## Direct observations

At 3B in raw coordinates, the reconstruction/global-Attention Fisher ratios are:

| Model | Dataset | Layer-wise reconstruction / Attention Fisher |
| --- | --- | --- |
| S7 | P / N | L7 `0.895 / 1.081` |
| S37 | P | L3 `1.138`, L7 `0.848` |
| S37 | N | L3 `1.168`, L7 `0.967` |
| SALL | P | range `0.941–1.416` across layers |
| SALL | N | range `0.915–1.342` across layers |

The direction is therefore layer- and dataset-dependent. Reconstruction sometimes raises and sometimes lowers Fisher; it is not a monotonic denoiser.

![Global Fisher retention](figures/global_fisher_reconstruction_to_attention_ratio.png)

Per-class trajectories preserve the same mixed structure. At 3B, the reconstruction/Attention class-Fisher ratio ranges from `0.884–0.918` for S7-P, `0.995–1.173` for S7-N, `0.783–1.198` for S37-P, `0.922–1.302` for S37-N, `0.688–1.623` for SALL-P, and `0.834–1.529` for SALL-N. These are descriptive class contributions, not independent experimental replicates.

- [S7 P](figures/per_class_fisher_s7_p.png) / [S7 N](figures/per_class_fisher_s7_n.png)
- [S37 P](figures/per_class_fisher_s37_p.png) / [S37 N](figures/per_class_fisher_s37_n.png)
- [SALL P](figures/per_class_fisher_sall_p.png) / [SALL N](figures/per_class_fisher_sall_n.png)

At 3B, trailing-128-update medians are:

| Model | LM loss | Weighted reconstruction | Weighted AuxK | Total regularization / LM |
| --- | ---: | ---: | ---: | ---: |
| S7 | 3.459 | 0.161 | 0.031 | 0.0555 |
| S37 | 3.443 | 0.184 | 0.031 | 0.0624 |
| SALL | 3.436 | 0.188 | 0.031 | 0.0633 |

![Training loss scales](figures/training_loss_scale_trajectories.png)

The scalar regularization contribution is only about 5.6–6.3% of LM loss at 3B, yet support-only local reconstruction/LM gradient ratios span `0.099–0.763` for S7, `0.153–1.564` for S37, and `0.012–0.073` for SALL across the registered checkpoints and layers. Similar scalar loss ratios therefore do not imply similar optimization influence.

![Local gradient coefficient sensitivity](figures/local_gradient_coefficient_sensitivity.png)

## Coefficient implication

Changing the reconstruction coefficient from \(\lambda\) to \(\lambda'\) scales the reconstruction gradient norm by \(\lambda'/\lambda\) at a fixed model state and leaves its direction unchanged. The later [dimension-matched random-null audit](fisher_gradient_reliability.md) found 43/44 checkpoint-layer groups compatible with independent random directions in 262,144 dimensions and none unusually closer to exact orthogonality. The valid description is therefore near-zero local cosine, not learned special orthogonality. A large near-zero-cosine component can still change update length and interact with curvature, so matching scalar loss values is not a valid coefficient rule.

`AI proposal pending researcher confirmation`:

1. Keep the layer reduction as a mean, not a sum, and keep AuxK at `1/32` for the first controlled pilot.
2. For a topology-matched conservative Smoke, use one common reconstruction coefficient (lambda_{rec}=0.1), not topology-specific coefficients. Under fixed-state linear scaling, the largest observed local support ratio would be about `0.156` rather than `1.564`.
3. Before a full training comparison, measure the summed reconstruction gradient in shared parameter space. Escalate to `0.3` only if the total parameter-gradient ratio is below `0.05`; reduce to `0.03` if it exceeds `0.25` or shows stable opposition. These thresholds are proposed safety/trust-region gates, not established scientific optima.

Do not increase SALL's coefficient merely because each layer is small after the exact `1/8` averaging: the eight terms can align, cancel, or act on different shared parameter groups.

## Evidence and boundary

Primary tables: [per-class Fisher](tables/per_class_fisher_metrics.csv), [global Fisher reconstruction check](tables/global_fisher_recomputed.csv), [loss scales](tables/loss_scale_metrics.csv), and [local gradient summary](tables/local_gradient_scale_summary.csv).

Can claim: exact per-class decomposition of the qualified Fisher computation; both internal surfaces on P and N; arithmetic loss-scale comparison; fixed-state local coefficient sensitivity.

Cannot claim: the reconstruction is used by the native LM forward; a larger Fisher ratio is better; scalar loss ratio determines update strength; `0.1` is optimal; local activation gradients equal summed parameter gradients; or any causal performance effect.
