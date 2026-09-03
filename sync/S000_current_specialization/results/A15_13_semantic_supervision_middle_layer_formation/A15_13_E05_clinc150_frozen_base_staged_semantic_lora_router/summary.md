# A15_13_E05 Result Summary

```text
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
machine_verdict: INSUFFICIENT_ORACLE
completion: 32/32 final condition-by-seed runs complete
data: CLINC150, 15,000 train / 2,997 development / 4,498 confirmation after deduplication
model: frozen Qwen3-0.6B-Base with block-14 shared, parent, and child LoRA residuals
seeds: 17, 29
```

## Conclusion First

Semantic supervision made the Router semantic and the parent experts functionally non-interchangeable, but this experiment did not establish that it made the effective middle-layer representation more separable by fine intent.

The gold hierarchical condition improved the registered domain-local linear-probe macro F1 over the architecture-identical task-only hierarchy by `+0.289` and `+0.093` percentage points in the two seeds. The pooled effect was `+0.191`, but its 95% intent-stratified bootstrap interval was `[-0.0003, +0.3866]`. Because the lower bound crossed zero, the Oracle denominator was inadmissible under the frozen Protocol. The spherical-cluster condition was also positive in both seeds (`+0.039`, `+0.093`; pooled `+0.066`, 95% interval `[-0.0490, +0.1860]`), but Oracle recovery cannot be promoted when the Oracle gate fails.

The result therefore does not support the claim that the current staged hierarchy improves fine-intent separability. It does support a narrower observation: semantic route labels prevent task-only route collapse and create small but reproducible parent-expert task utility.

## Focus Question And Direct Answer

**Question.** Can semantics already present in a frozen Qwen3-0.6B-Base seed a coarse Router and parent experts, after which a fixed coarse Router supports fine routing and a more semantically separable effective representation?

**Direct answer.** The first clause is supported at the routing/function level. The second clause is not established at the representation level. The current child experts contribute too little residual signal, while the frozen representation is already close to the ceiling of the registered linear probe.

## Decisive Evidence

| Condition, mean over two seeds | Intent task macro F1 (%) | Domain-local probe macro F1 (%) | Coarse route NMI | Largest coarse load | Parent selective utility |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dense rank-24 LoRA | 91.35 | 89.65 | n/a | n/a | n/a |
| Hierarchical task-only | 91.20 | 89.49 | 0.027 | 0.972 | n/a |
| Gold staged hierarchy | 90.63 | 89.68 | 0.517 | 0.120 | 0.00533 |
| Spherical-cluster staged hierarchy | 90.79 | 89.56 | 0.287 | 0.160 | 0.00303 |

`NMI` is normalized mutual information with the held-out gold domain; it is an evaluation-only semantic-alignment score. `Largest coarse load` is the fraction routed to the most-used parent. `Parent selective utility` is the extra confirmation loss caused by deleting the matched parent expert relative to deleting non-matched parents; it is an eligibility diagnostic, not the headline endpoint.

- Task-only hierarchical routing collapsed: largest-parent load was `1.000` and `0.943`, with coarse NMI `0.000` and `0.054`.
- Gold routing was balanced and semantic: largest load `0.124` and `0.115`, coarse NMI `0.531` and `0.502`, and matched coarse macro F1 `0.729` and `0.712`.
- Spherical clustering recovered partial route semantics: largest load `0.156` and `0.164`, coarse NMI `0.290` and `0.284`, and matched coarse macro F1 `0.377` and `0.376`.
- The parent functional gate passed for both gold and spherical supervision. Gold pooled selectivity was `0.00533` with 95% interval `[0.00447, 0.00619]`; spherical selectivity was `0.00303` with `[0.00198, 0.00409]`.
- The spherical hierarchy preserved the registered task guard: it lost `0.765` and `0.348` task-F1 points relative to Dense LoRA, both within the one-point limit.

![Primary probe effect](figures/primary_probe_effect.png)

![Coarse route semantics](figures/coarse_route_semantics.png)

## Why Representation Improvement Was Not Established

The frozen Base already reached `89.95%` with the registered domain-local linear readout and `64.81%` intent 5-nearest-neighbor accuracy. Across the main conditions, the effective-state linear readout remained about `89.8%--90.0%`, and 5-nearest-neighbor accuracy remained about `64.5%--64.8%`. Gold-intent covariance statistics were also essentially unchanged: the Base X-MoE collapse statistic was `524.56`, effective rank `187.10`, fifth-percentile centroid margin `-0.1108`, and top-10 eigenvalue mass `0.2865`; the main trained conditions stayed within tiny numerical neighborhoods of those values.

The residual decomposition supplies a mechanism diagnosis. Mean shared-residual norm was about `4.6--4.8`, whereas the gold child residual was only `0.024--0.027` and the spherical child residual `0.061--0.063`. Their mean principal angles to the corresponding child-Router row space were about `83--84` degrees. Thus the Router learned semantic decisions, but those directions were not strongly written into the child residual that defines the effective representation.

The frequency-matched shuffled hierarchy further limits the claim: it was balanced but non-semantic (coarse NMI about `0.02`) and nevertheless showed probe increases of roughly `+0.25` and `+0.29` points over task-only. This descriptive control is consistent with generic fixed partitioning or optimization effects explaining small probe shifts.

## Freeze By Coarse-Removal Ablation

Mean probe changes relative to hierarchical task-only were small:

| Label | Parent experts trainable, native | Trainable, coarse-removed | Frozen, native | Frozen, coarse-removed |
| --- | ---: | ---: | ---: | ---: |
| Gold | +0.27 | +0.24 | +0.15 | +0.20 |
| Spherical cluster | +0.11 | +0.01 | +0.02 | +0.07 |

No cell had a registered confidence interval. Descriptively, the predicted `freeze parent experts + remove coarse row space` cell was not best. Keeping parent experts trainable and giving the child Router the native representation was numerically strongest. This rejects neither staged learning nor all forms of coarse-information removal; it only fails to support the present linear row-space removal and strict parent-expert freeze.

![Two-by-two ablation](figures/ablation_2x2_probe.png)

## Data Judgment

CLINC150 was adequate for checking whether natural-language semantics can organize routing: all post-trained task systems reached about `90%--92%` confirmation macro F1, and gold supervision produced semantic, balanced, functional parent routing. It was not decisive for representation shaping because the registered fine-intent linear readout was already near `90%` before training and the child residual carried little signal.

This is not the earlier failure mode in which a small model cannot learn the task. The present bottleneck is the combination of a saturated representation endpoint and an objective that sends semantic cross entropy only into Router parameters. The frozen Base can therefore support semantic selection without being forced to encode that semantic distinction in the added child residual.

## Claim Boundary

This result establishes neither improved natural-language representation separability nor superiority of the hierarchical method over Dense or flat training. It does not validate the current coarse-removal operation, dynamic online labels, token-level routing, open-domain semantic discovery, generative-task benefit, or transfer to MASSIVE. The X-MoE statistic is a diagnostic of within-versus-between scatter; unchanged values do not prove absence of every useful geometric change.

## Candidate Next Decision

Run one English MASSIVE mechanism audit before returning to synthetic data. Use its natural hierarchy of scenario to intent and its slot spans as a non-saturated token-level fine-semantic endpoint. Require the gold Oracle to improve slot/span representation metrics and require the child-residual-to-shared-residual ratio to become non-negligible. If the MASSIVE Oracle still fails, or child residuals remain negligible, stop scaling natural data and use controlled synthetic sequences to diagnose the objective and gradient path from the bottom up.

This next decision is an AI proposal awaiting the researcher's closed-book result, cannot-claim boundary, and decision confirmation.

## Evidence

- [Protocol](protocol.md)
- [Detailed evidence record](detailed.md)
- Raw run root: `/data/250010109/MoE_Router/experiments/20260831_a15_13_e05_clinc150_frozen_base_staged_semantic_lora_router/runs/full-e05-full-20260831T171638Z`
