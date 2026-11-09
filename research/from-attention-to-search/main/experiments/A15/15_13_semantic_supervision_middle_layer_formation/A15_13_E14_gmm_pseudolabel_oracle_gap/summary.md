# Summary: A15_13_E14 Diagonal-GMM Pseudo-Label Oracle-Gap Audit

Primary Anchor: [A15_13_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md)
Frozen Protocol: [protocol.md](protocol.md)
Detailed evidence: [detailed.md](detailed.md)
Result status: `FULL_RUN_COMPLETE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Registered verdict: `B` — the offline semantic partition exists, but the learned causal Router does not convert it into task or efficiency gains.**

The gold-path Oracle confirms usable routing headroom. On the eight-task internal capability diagnostic, its mean answer-token negative log-likelihood was `0.794920`, versus `0.806323` for the matched hierarchical task-only model, and its macro score was `16.50%`, versus `15.82%`. Both seeds showed a positive macro-score difference (`+0.98` and `+0.39` percentage points).

The diagonal-GMM learned Router did not recover this value. Its mean NLL was `0.817358`, which was `0.011035` worse than task-only and `0.022438` above Oracle. Hard pseudo-path training made the deployed causal result worse: mean NLL `0.836757` and Oracle gap `0.041838`. It also enlarged rather than reduced the loss-curve-area gap to Oracle (`0.030683` versus `0.014159`).

The most useful causal localization is the forced-pseudo-path diagnostic. The hard-pseudo experts scored `0.836757` under their learned causal Router but `0.805028` when the frozen pseudo path was supplied externally, an improvement of `0.031729` nats per answer token. Thus the trained expert bank contains conditional capacity, but the online block-14 Router does not reproduce the offline whole-window assignment. This does not yet prove that the pseudo experts themselves are semantically matched, because a forced wrong-pseudo-path control was not registered.

## What Actually Ran

- `30/30` registered two-seed checkpoints were trained and hashed: five M2D2 conditions and ten eight-task conditions under seeds 17 and 29. Frozen Qwen3-0.6B-Base was evaluated separately.
- M2D2 was genuinely staged: stage one trained shared LoRA, coarse experts, and the coarse Router for two passes and 144 updates; stage two froze the coarse Router, kept coarse experts trainable, added fine experts and the fine Router, and ran two more passes and 144 updates.
- The eight-task continuation was intentionally not staged. Each condition ran four deterministic passes and 128 updates over the same `911,644` answer-token budget.
- Unified evaluation produced 21 benchmark model outputs, `10,752` per-item predictions, 165 likelihood/intervention arrays, eight analysis tables, and five audited figures. The completion audit has no errors.

## Complete Eight-Task Internal Capability Diagnostic

Scores are percentages. These are within-mixture diagnostics because official evaluation records may overlap the training mixture; they are not uncontaminated benchmark-generalization claims.

| Model | Seed | MMLU | MMLU-Pro | BBH | GSM8K | MATH | GPQA | HumanEval | MBPP | Average |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Frozen Base | fixed | 50.00 | 10.94 | 1.56 | 0.00 | 7.81 | 25.00 | 0.00 | 1.56 | 12.11 |
| Dense rank-24 LoRA | 17 | 51.56 | 15.62 | 6.25 | 0.00 | 14.06 | 23.44 | 0.00 | 1.56 | 14.06 |
| Dense rank-24 LoRA | 29 | 51.56 | 15.62 | 6.25 | 1.56 | 12.50 | 18.75 | 0.00 | 1.56 | 13.48 |
| Dense rank-24 LoRA | mean | 51.56 | 15.62 | 6.25 | 0.78 | 13.28 | 21.09 | 0.00 | 1.56 | 13.77 |
| Flat task-only | 17 | 51.56 | 14.06 | 6.25 | 0.00 | 9.38 | 21.88 | 0.00 | 1.56 | 13.09 |
| Flat task-only | 29 | 54.69 | 17.19 | 4.69 | 1.56 | 9.38 | 23.44 | 0.00 | 3.12 | 14.26 |
| Flat task-only | mean | 53.12 | 15.62 | 5.47 | 0.78 | 9.38 | 22.66 | 0.00 | 2.34 | 13.67 |
| Hierarchical task-only | 17 | 51.56 | 17.19 | 9.38 | 0.00 | 12.50 | 29.69 | 0.00 | 3.12 | 15.43 |
| Hierarchical task-only | 29 | 51.56 | 17.19 | 18.75 | 0.00 | 10.94 | 28.12 | 0.00 | 3.12 | 16.21 |
| Hierarchical task-only | mean | 51.56 | 17.19 | 14.06 | 0.00 | 11.72 | 28.91 | 0.00 | 3.12 | 15.82 |
| Frequency-matched random hierarchy | 17 | 54.69 | 14.06 | 7.81 | 1.56 | 14.06 | 18.75 | 0.00 | 1.56 | 14.06 |
| Frequency-matched random hierarchy | 29 | 51.56 | 17.19 | 14.06 | 0.00 | 12.50 | 26.56 | 0.00 | 3.12 | 15.62 |
| Frequency-matched random hierarchy | mean | 53.12 | 15.62 | 10.94 | 0.78 | 13.28 | 22.66 | 0.00 | 2.34 | 14.84 |
| Source-supervised hierarchy | 17 | 53.12 | 17.19 | 10.94 | 0.00 | 14.06 | 21.88 | 0.00 | 3.12 | 15.04 |
| Source-supervised hierarchy | 29 | 51.56 | 17.19 | 15.62 | 0.00 | 14.06 | 31.25 | 0.00 | 1.56 | 16.41 |
| Source-supervised hierarchy | mean | 52.34 | 17.19 | 13.28 | 0.00 | 14.06 | 26.56 | 0.00 | 2.34 | 15.72 |
| Diagonal-GMM learned Router | 17 | 51.56 | 14.06 | 9.38 | 1.56 | 9.38 | 23.44 | 0.00 | 3.12 | 14.06 |
| Diagonal-GMM learned Router | 29 | 50.00 | 15.62 | 14.06 | 0.00 | 12.50 | 32.81 | 0.00 | 3.12 | 16.02 |
| Diagonal-GMM learned Router | mean | 50.78 | 14.84 | 11.72 | 0.78 | 10.94 | 28.12 | 0.00 | 3.12 | 15.04 |
| Diagonal-GMM learned Router + load bias | 17 | 48.44 | 15.62 | 9.38 | 0.00 | 12.50 | 25.00 | 0.00 | 3.12 | 14.26 |
| Diagonal-GMM learned Router + load bias | 29 | 50.00 | 17.19 | 18.75 | 1.56 | 12.50 | 29.69 | 0.00 | 3.12 | 16.60 |
| Diagonal-GMM learned Router + load bias | mean | 49.22 | 16.41 | 14.06 | 0.78 | 12.50 | 27.34 | 0.00 | 3.12 | 15.43 |
| Diagonal-GMM hard-pseudo training | 17 | 50.00 | 14.06 | 7.81 | 0.00 | 10.94 | 20.31 | 0.00 | 3.12 | 13.28 |
| Diagonal-GMM hard-pseudo training | 29 | 51.56 | 17.19 | 9.38 | 1.56 | 14.06 | 26.56 | 0.00 | 3.12 | 15.43 |
| Diagonal-GMM hard-pseudo training | mean | 50.78 | 15.62 | 8.59 | 0.78 | 12.50 | 23.44 | 0.00 | 3.12 | 14.36 |
| Hard-pseudo training + load bias | 17 | 50.00 | 15.62 | 7.81 | 0.00 | 10.94 | 28.12 | 0.00 | 3.12 | 14.45 |
| Hard-pseudo training + load bias | 29 | 53.12 | 15.62 | 10.94 | 0.00 | 17.19 | 29.69 | 0.00 | 1.56 | 16.02 |
| Hard-pseudo training + load bias | mean | 51.56 | 15.62 | 9.38 | 0.00 | 14.06 | 28.91 | 0.00 | 2.34 | 15.23 |
| Gold-path Oracle | 17 | 51.56 | 15.62 | 23.44 | 0.00 | 12.50 | 23.44 | 0.00 | 4.69 | 16.41 |
| Gold-path Oracle | 29 | 51.56 | 17.19 | 21.88 | 0.00 | 12.50 | 25.00 | 0.00 | 4.69 | 16.60 |
| Gold-path Oracle | mean | 51.56 | 16.41 | 22.66 | 0.00 | 12.50 | 24.22 | 0.00 | 4.69 | **16.50** |

![Eight-task internal capability](figures/02_benchmark_average.png)

How to read: longer bars are better; black points are the two seeds and the red line is frozen Base. GMM models improve over Base on average but do not beat matched hierarchical task-only, while Oracle is best.

## Learning Efficiency And Oracle Gap

Negative log-likelihood, abbreviated NLL, is mean reference-answer surprise in nats per answer token; lower is better. Curve area is NLL integrated over seen answer tokens and normalized by the token budget; lower is faster learning.

| Condition | Final evaluation NLL | Curve area | Gap to Oracle NLL |
| --- | ---: | ---: | ---: |
| Hierarchical task-only | `0.806323` | `0.839792` | `0.011403` |
| Diagonal-GMM learned Router | `0.817358` | `0.848492` | `0.022438` |
| Diagonal-GMM learned + load bias | `0.817267` | `0.848477` | `0.022347` |
| Diagonal-GMM hard-pseudo training | `0.836757` | `0.865017` | `0.041838` |
| Hard-pseudo + load bias | `0.837340` | `0.865123` | `0.042420` |
| Gold-path Oracle | **`0.794920`** | **`0.834334`** | `0.000000` |

![Learning efficiency](figures/01_learning_efficiency.png)

How to read: lower is better. The hard-pseudo curve stays above the learned-GMM curve rather than moving toward the red Oracle curve.

![Oracle gaps](figures/03_oracle_gap.png)

How to read: shorter bars are better. Hard-pseudo training increases both the final-NLL and curve-area distance to Oracle in both seeds.

## Routing And Expert Function

The frozen offline GMM partition was source-related: evaluation leaf normalized mutual information was `0.5924` and parent normalized mutual information was `0.6012`. This confirms accessible source/task structure in final-layer whole-sequence means. It does not establish causal token routing.

For the requested comparison with the old direction-plus-radius labeler, the only eligible common evidence is the earlier frozen-state audit: M2D2 confirmation fine-domain NMI was `0.444` for direction plus radius and `0.524` for diagonal GMM. The old direction-plus-radius Router checkpoint uses a different adapter state schema and did not enter E14's unified evaluator. Its historical mean confirmation NLL was `2.881270`, while the newly trained E14 GMM learned route was `2.884899`; therefore E14 does **not** establish a task advantage for diagonal GMM. It establishes only a better offline partition under the earlier audit.

![Earlier offline cluster-method audit](../A15_13_E09_m2d2_baselines_last_layer_pseudolabel/figures/05_teacher_cluster_methods.png)

How to read: higher is better for offline fine-domain agreement. Diagonal GMM is the strongest labeler here, but this plot does not measure causal Router or language-model performance.

The deployed GMM Router was not stable across seeds. Its route/source NMI was `0.3709` in seed 17 and `0.3142` in seed 29, while task-only was `0.3753` and `0.0967`. Pseudo-leaf recovery was `0.1951` and `0.4468`; the frequency-only majority baseline was `0.2631`. Therefore one seed was below the trivial majority baseline and the Protocol's two-seed semantic gate failed.

![Route semantics](figures/05_route_semantics.png)

How to read: higher bars mean routes align more with true task source, but black seed points show substantial instability. This plot diagnoses routing only and cannot establish task gain.

Expert interventions report changed-minus-intact NLL. Positive values mean removing or replacing the selected expert hurts.

| Condition | Delete | Wrong leaf, same parent | Wrong expert, other parent |
| --- | ---: | ---: | ---: |
| Hierarchical task-only | `+0.024529` | `+0.023494` | `+0.051461` |
| Diagonal-GMM learned Router | `+0.014830` | `+0.011947` | `+0.040649` |
| Diagonal-GMM hard-pseudo training | `+0.011095` | `+0.007851` | **`-0.000828`** |
| Gold-path Oracle | `+0.029325` | `+0.024341` | `+0.049011` |

![Expert functional interventions](figures/04_expert_function.png)

How to read: higher positive bars indicate stronger non-interchangeable expert function. Learned GMM is weaker than task-only and Oracle; the hard-pseudo other-parent bar is below zero, so its deployed path fails the strongest functional test.

## Claim Boundary

**Can claim:** the gold forced route has task and efficiency value in this frozen-base, one-layer continuation setup; offline final-layer GMM clusters contain source/task information; hard pseudo-path experts perform substantially better when the same offline pseudo path is supplied at evaluation; the present causal Router and load-bias mechanism fail to convert that structure into stable task gain.

**Cannot claim:** that the GMM discovers semantic reasoning rather than source/topic regularity; that the result generalizes to uncontaminated benchmarks; that pseudo-label experts are semantically matched without a forced-wrong-pseudo control; that all causal Router designs fail; or that parameter geometry proves function.

## Next Decision Proposed For Human Confirmation

Do not expand the pseudo-label family yet. First test one localized handoff repair: keep the hard-pseudo-trained experts fixed, train a causal Router by matching the offline **prefix-conditioned** pseudo teacher, and include forced-correct-pseudo versus forced-wrong-pseudo paths. Continue only if both seeds reduce the `0.031729` forced-path deployment gap and increase selective expert-intervention cost without worsening task-only NLL.
