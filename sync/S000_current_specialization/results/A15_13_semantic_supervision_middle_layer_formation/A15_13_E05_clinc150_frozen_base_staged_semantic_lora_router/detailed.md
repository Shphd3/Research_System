# A15_13_E05 Detailed Evidence Record

```text
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
machine_verdict: INSUFFICIENT_ORACLE
evidence_opened: 2026-08-31
full_run_root: /data/250010109/MoE_Router/experiments/20260831_a15_13_e05_clinc150_frozen_base_staged_semantic_lora_router/runs/full-e05-full-20260831T171638Z
canonical_record: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/
```

## 1. Question, Registered Decision Rule, And Completion

The registered question was whether frozen-base natural-language semantics can train a coarse Router and parent LoRA experts, then support fixed-parent fine routing with a more separable effective representation. The primary endpoint was domain-local fine-intent linear-probe macro F1, evaluated by the gold hierarchy's effect over task-only and the spherical-cluster recovery of that effect.

Pass required an admissible positive Oracle interval, positive spherical effects in both seeds with a positive pooled lower bound, task preservation, and positive parent selective utility. The full matrix had to finish even if an earlier gate failed.

Completion audit returned:

```json
{"complete": true, "missing": [], "smoke": false}
```

The full artifact tree contains 12 stage-one checkpoints, 32 final condition-by-seed directories, two seeds, four parent-utility arrays, one aggregate, one extended representation audit, one fine functional audit, and six generated figures. `BASE_FROZEN` was evaluated without optimization as specified.

## 2. Data And Model

The local official CLINC150 snapshot supplied 15,000 training, 3,000 development, and 4,500 confirmation utterances. Train-priority exact normalized-text deduplication removed three development and two confirmation rows, leaving `15,000 / 2,997 / 4,498`. It contains 150 intents nested evenly under ten domains. No label string was rendered in the model input, and clustering used training representations only.

The original Qwen3-0.6B-Base parameters remained frozen. A trainable 150-way task head and shared/parent/child low-rank residuals were added at zero-indexed block 14. Stage one trained the coarse Router and parent experts for two epochs. Stage two fixed the coarse Router, added child Routers and experts, and trained for two more epochs. Dense and flat controls used four epochs. Each trained example contributed a 150-way intent cross entropy; semantic route cross entropy updated only Router parameters.

## 3. Execution Ledger

| Job | Role | Outcome |
| --- | --- | --- |
| `pt-jtr051b5` | reserved four-H100 smoke | completed |
| `pt-ipyrra1g` | first resumable full run | completed 12 stage-one and 24 final runs, then suspended after flat pseudo-label dtype failure |
| `pt-5ueee3w7` | regression-tested continuation | completed the remaining final runs and four utility arrays; full completion audit passed |
| `pt-qhl55aor`, `pt-96zomcq7` | first analysis attempts | exposed missing analysis-directory creation |
| `pt-a17pcesk` | corrected parallel analysis | completed aggregate, bootstrap, representation audit, functional diagnostics, and figures |
| `pt-le90locj` | first post-analysis | exposed invalid 150-way-flat versus 10-way-hierarchical load comparison |
| `pt-bf27nzku` | corrected post-analysis | completed the separated analysis |

All jobs used one reserved `n6ls.iu.i40.4` node exposing four H100 80GB devices. Full runs were condition-parallel, not a data-parallel change to a condition.

The complete deviation ledger is in Protocol Section 18. The most consequential limitation is that the Router used the uncentered block input, while the frozen Protocol described a train-mean-centered input. All conditions share the actual input, but the result applies only to that actual variant.

## 4. Registered Primary Endpoint

| Comparison | Seed 17 effect | Seed 29 effect | Pooled mean | 95% intent-stratified bootstrap interval |
| --- | ---: | ---: | ---: | ---: |
| Gold hierarchy minus task-only hierarchy | +0.2887 | +0.0934 | +0.1911 | [-0.0003, +0.3866] |
| Spherical hierarchy minus task-only hierarchy | +0.0388 | +0.0928 | +0.0658 | [-0.0490, +0.1860] |

Units are macro-F1 percentage points. Both contrasts were positive in both seeds, but both pooled intervals crossed zero. The registered machine verdict is therefore `INSUFFICIENT_ORACLE`. Oracle recovery values are mechanically computable but ineligible: spherical `0.540`, Gaussian `2.054`, and directional-mixture `1.232`. Values above one are unstable because the inadmissible Oracle denominator is tiny; they are not evidence that a pseudo method beat an established upper bound.

## 5. Condition Results

### Seed 17

| Condition | Task macro F1 (%) | Probe macro F1 (%) | Coarse NMI | Largest parent load |
| --- | ---: | ---: | ---: | ---: |
| Dense rank-24 | 91.454 | 89.668 | n/a | n/a |
| Flat task-only | 92.350 | 89.539 | 0.000 | 1.000 |
| Hierarchical task-only | 91.175 | 89.465 | 0.000 | 1.000 |
| Shuffled hierarchy | 90.348 | 89.714 | 0.023 | 0.134 |
| Gold hierarchy | 90.591 | 89.757 | 0.531 | 0.124 |
| Spherical hierarchy | 90.688 | 89.509 | 0.290 | 0.156 |
| Gaussian hierarchy | 90.772 | 89.601 | 0.194 | 0.514 |
| Directional-mixture hierarchy | 90.587 | 89.653 | 0.294 | 0.241 |

### Seed 29

| Condition | Task macro F1 (%) | Probe macro F1 (%) | Coarse NMI | Largest parent load |
| --- | ---: | ---: | ---: | ---: |
| Dense rank-24 | 91.249 | 89.638 | n/a | n/a |
| Flat task-only | 92.124 | 89.454 | 0.038 | 0.932 |
| Hierarchical task-only | 91.219 | 89.514 | 0.054 | 0.943 |
| Shuffled hierarchy | 90.510 | 89.805 | 0.021 | 0.133 |
| Gold hierarchy | 90.675 | 89.612 | 0.502 | 0.115 |
| Spherical hierarchy | 90.901 | 89.605 | 0.284 | 0.164 |
| Gaussian hierarchy | 91.036 | 89.872 | 0.190 | 0.508 |
| Directional-mixture hierarchy | 91.036 | 89.693 | 0.311 | 0.230 |

Flat task-only was the strongest task baseline, averaging `92.24%`. No hierarchical semantic condition improved task accuracy. Task accuracy was not the primary endpoint, but this prevents a product-performance claim.

## 6. Semantic Entrance And Routing

Before training, spherical clustering of frozen Base representations reached confirmation coarse NMI `0.290`, adjusted Rand index `0.182`, matched macro F1 `0.367`, and largest load `0.147`. Its 150-leaf assignment reached intent NMI `0.622` and matched macro F1 `0.317`. The directional mixture gave slightly higher coarse NMI `0.313` and matched macro F1 `0.385`; the diagonal Gaussian mixture was imbalanced, with largest coarse load `0.440` and NMI `0.190`.

After route training, task-only parent routing collapsed. Gold and pseudo supervision prevented collapse and preserved partial semantic agreement. A balanced load by itself was insufficient: the shuffled hierarchy had largest load near `0.13` but NMI near `0.02`.

The fine route also carried partial semantics. Gold leaf routing had NMI `0.691/0.690` and matched macro F1 `0.518/0.514`; spherical leaf routing had NMI `0.613/0.613` and matched macro F1 `0.296/0.303`.

## 7. Functional Evidence

The registered parent selective-utility gate passed:

| Label source | Seed means | Pooled mean loss increase | 95% interval |
| --- | --- | ---: | ---: |
| Gold | 0.00520, 0.00545 | 0.00533 | [0.00447, 0.00619] |
| Spherical cluster | 0.00321, 0.00286 | 0.00303 | [0.00198, 0.00409] |

This establishes that deleting the semantically matched parent hurts slightly more than deleting non-matched parents on average. It does not establish a task advantage, and two of ten spherical matched experts had negative selectivity in each seed.

Supporting child diagnostics were positive on average but smaller and heterogeneous. Gold active-child deletion increased loss by `0.00068/0.00023`; wrong-child substitution increased it by `0.00054/0.00057`. Spherical active-child deletion increased loss by `0.00187/0.00241`; wrong-child substitution increased it by `0.00192/0.00257`. Many per-intent effects were negative, so these results show weak aggregate influence rather than uniformly specialized child experts.

## 8. Representation Audit

### 8.1 Effective-state metrics

| Object | Intent 5-nearest-neighbor accuracy | Fifth-percentile margin | Effective rank | X-MoE collapse statistic | Top-10 eigenvalue mass |
| --- | ---: | ---: | ---: | ---: | ---: |
| Frozen Base | 64.807% | -0.11075 | 187.10 | 524.56 | 0.28650 |
| Dense, seed 17 | 64.7% range | -0.11053 | 187.21 | 524.54 | 0.28639 |
| Main gold/spherical/task conditions | 64.5%--64.8% | about -0.111 | about 187 | about 524 | about 0.286 |

The X-MoE statistic is $\operatorname{Tr}(\Sigma_W\Sigma_B^\dagger)$: within-class scatter measured against between-class scatter. Larger values indicate more collapse under that label partition. Here it was computed both for route partitions and for gold intents; only the latter is comparable in this table. The nearly unchanged values do not support improved gold-intent geometry.

The fixed Base readout scored `89.946%` on Base states. On effective states from the main conditions, both that frozen readout and a retrained readout stayed around `89.8%--90.0%`. Thus the residuals did not introduce a substantial new linearly accessible fine-intent signal.

### 8.2 Residual magnitudes

| Condition | Shared residual mean L2 | Parent residual mean L2 | Child residual mean L2 |
| --- | ---: | ---: | ---: |
| Task-only hierarchy, seeds 17/29 | 4.40 / 4.15 | 1.41 / 1.56 | 1.10 / 0.92 |
| Gold hierarchy, seeds 17/29 | 4.84 / 4.63 | 0.522 / 0.529 | 0.027 / 0.024 |
| Spherical hierarchy, seeds 17/29 | 4.82 / 4.56 | 0.619 / 0.665 | 0.061 / 0.063 |

Semantic routing spread samples across experts, but each child expert received less task gradient and produced a residual two orders of magnitude smaller than the shared residual. The total residual norm remained about `5.1--5.3`, roughly 9% of the Base block-state norm near `58.7`; most of that change was shared rather than fine-semantic.

Mean principal angles were about `84--85` degrees between total residual directions and the parent Router row space, and about `83--84` degrees between child residual directions and child Router row spaces. The learned routing decision boundaries were therefore almost orthogonal to the directions written by the low-rank residuals.

## 9. Complete Two-By-Two Ablation

The coarse Router was fixed in every stage-two cell. `F0/F1` denotes parent experts trainable/frozen, and `R0/R1` denotes native/coarse-row-space-removed child-Router input.

| Label source | F0_R0 | F0_R1 | F1_R0 | F1_R1 |
| --- | ---: | ---: | ---: | ---: |
| Gold mean probe F1 | 89.763 | 89.724 | 89.642 | 89.685 |
| Gold delta from task-only | +0.27 | +0.24 | +0.15 | +0.20 |
| Spherical mean probe F1 | 89.601 | 89.497 | 89.512 | 89.557 |
| Spherical delta from task-only | +0.11 | +0.01 | +0.02 | +0.07 |

The registered intuition cell `F1_R1` was not numerically best. The result instead favors, descriptively, keeping parent experts trainable and reading the native representation. Because cell-wise uncertainty was not registered and the Oracle primary gate failed, this is a mechanism diagnosis only.

## 10. Data And Objective Diagnosis

Four observations separate rival explanations:

1. The task is learnable: confirmation task macro F1 reached `90%--92%` and training macro F1 reached about `99%`. This is not a general small-model inability to learn CLINC150.
2. Frozen Base already exposes the fine intents strongly to a linear readout. The registered probe therefore has little headroom.
3. Route cross entropy stops at Router parameters. It can make routing semantic without directly shaping either the frozen Base or the expert residual directions.
4. The shared residual dominates while the semantically split child residual is tiny. The effective state is consequently almost unchanged by the component that should carry fine semantic specialization.

CLINC150 is therefore a valid semantic-routing benchmark but an underpowered representation-shaping benchmark for this particular endpoint and objective.

## 11. MASSIVE Extension Requirements

The proposed next experiment should start with the official English `en-US` partition, not all languages at once. [MASSIVE 1.0](https://aclanthology.org/2023.acl-long.235/) supplies 51 languages, 18 scenarios, 60 intents, and 55 slot types; the [official repository](https://github.com/alexa/massive) documents the released data and later language extension. Preserve the natural hierarchy as scenario to intent and treat slots as token-level fine semantics rather than forcing sequence and token labels into one target.

Minimum contract:

1. Use official train/development/test partitions and raw utterances. Never include scenario, intent, or slot-name strings in inputs.
2. Train a joint intent-classification and BIO slot-tagging task. Use one sequence-level parent Router for scenario; audit an intent-level child Router and a separate token-level slot Router or slot-conditioned child mechanism.
3. Fit pseudo labels only from frozen-Base training states. Compare task-only hierarchy, gold Oracle, spherical/directional pseudo labels, flat routing, and Dense LoRA. Re-run the full freeze-by-removal matrix only after the gold Oracle clears its gate.
4. Make held-out slot span F1 and a token-level slot representation probe the non-saturated fine-semantic endpoints. Report rare-slot and worst-scenario performance, route entropy/NMI/adjusted Rand/matched F1, parent and child deletion, and the child-residual-to-shared-residual norm ratio.
5. Require the gold Oracle to improve the registered slot endpoint with a positive paired interval. If it does not, or if the child/shared residual ratio remains negligible, stop natural-data scaling and return to controlled synthetic sequences to isolate the objective and gradient path. If it works and pseudo labels recover a positive fraction, expand to multilingual transfer with language held out or explicitly stratified.

This extension is not yet an approved Protocol and must not inherit the current positive routing observation as proof of representation improvement.

## 12. Artifact Map And Integrity

### Canonical figures

- `figures/primary_probe_effect.png`
- `figures/coarse_route_semantics.png`
- `figures/routing_entropy.png`
- `figures/ablation_2x2_probe.png`
- `figures/representation_knn.png`

### Raw decision-bearing artifacts

- `analysis/aggregate.json`, SHA-256 `a450a7f09e48571c8b382d5e410bb490fabb767a0ffb26c88db0fd999c0948dd`
- `analysis/extended_representation.json`, SHA-256 `6978302e91bcd81da6953c379341450ad736a95de11d09e78c019cc30e0fe191`
- `analysis/fine_functional_diagnostics.json`, SHA-256 `32684e913effe29e15c1c90533e40ee7a1e8626aeed116479ee45a72572d11fa`
- `completion_audit.json`
- `prepared/data_manifest.json`, `prepared/cluster_audit.json`, `prepared/route_labels.npz`
- `final/seed_{17,29}/<condition>/evaluation.npz`, `task_metrics.json`, `selection.json`, and checkpoints
- main gold/spherical `parent_utility.npz` files for both seeds

All raw paths are relative to the full run root in the document header. The worker directory is not version-controlled, so source hashes captured after execution are not presented as immutable pre-run provenance.

## 13. Result Boundary And Pending Human Step

The direct registered result is `INSUFFICIENT_ORACLE`. The strongest bounded interpretation is that semantic supervision organizes routing and creates small parent-expert selectivity, while the current training path does not establish fine-semantic representation shaping. The researcher must now provide or approve the closed-book five-part account—question, direct result, updated judgment, cannot claim, and one next decision—before the Focus, Anchor, or delayed daily report can be finalized.
