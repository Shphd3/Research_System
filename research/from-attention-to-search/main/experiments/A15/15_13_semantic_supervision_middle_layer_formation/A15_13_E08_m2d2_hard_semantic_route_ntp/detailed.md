# Detailed: A15_13_E08 M2D2 Hard Semantic Route Next-Token Prediction

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

Purpose: test whether the true 3-by-3 M2D2 partition itself has causal language-modeling value after removing Router prediction and probability scaling.  
Direct result: semantic grouping beats random and no fine split and passes deletion and wrong-child interventions.  
Verdict: `PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP`.  
Boundary: the gain is positive in seven of nine fine domains and requires gold metadata.

## 1. Actual Setup And Training Audit

Data, target mask, frozen Base, block-14 LoRA capacity, optimizer, seeds, and checkpoints match E07. Hard routing differs in exactly two ways: the gold or control assignment directly selects the expert, and selected expert output has coefficient `1.0`. Detached shadow Routers receive route cross-entropy but cannot affect expert selection, expert scaling, language logits through their values, or non-shadow gradients.

Stage one trains shared LoRA and hard gold-parent experts for two passes (`144` updates) while learning a diagnostic coarse shadow Router. Stage two freezes the parent experts and coarse shadow Router, restarts AdamW, and trains shared LoRA and child banks for two passes (`144` updates). Common, random, and semantic arms have identical stage-one tensors and child initialization per seed; the parent tensors remain byte-identical after stage two.

Microbatch is 8, accumulation 16, effective batch 128. AdamW learning rate is `3e-4`, weight decay `0.01`, clipping `1.0`, with five-update warmup and cosine decay. Update 144 is selected by rule, never by development or confirmation performance.

## 2. Conformance And Eligibility

| Guard | Actual evidence | Status | Eligibility impact |
| --- | --- | --- | --- |
| Full condition matrix | 3 arms × 2 seeds, all update 144 | Pass | none |
| Data balance | 1,024/256/512 per each of 9 fine domains | Pass | none |
| Split duplicates | zero exact token-window duplicates | Pass | none |
| Future access | prefix Router max error `0.0` after suffix change | Pass | none |
| Hard coefficient | synthetic identity test invariant to shadow logits | Pass | none |
| Shadow isolation | no Router-state or expert gradient from shadow loss | Pass | none |
| Matched start/freeze | child init and final parent tensors equal by tensor audit | Pass | none |
| Finite confirmation | all 38 NLL arrays finite | Pass | none |
| Runtime correction | trusted-cache `weights_only=False`, first smoke pre-training | Recorded `C001` | none |
| Full job | `pt-i9fis3c8`, `SUCCEEDED`, about 23 minutes wall time | Pass | none |

## 3. Primary Results

| Condition | Meaning | NLL seed 17 | NLL seed 29 | Mean NLL | Perplexity |
| --- | --- | ---: | ---: | ---: | ---: |
| Frozen Base | no continued training | — | — | `2.969889` | `19.4898` |
| Hard common | one fine child per coarse domain | `2.879200` | `2.878953` | `2.879077` | `17.7978` |
| Hard random | balanced arbitrary child per sequence | `2.880279` | `2.879964` | `2.880121` | `17.8164` |
| Hard semantic | true fine-domain child | `2.877732` | `2.877409` | `2.877571` | `17.7711` |

Semantic minus controls is evaluated in the positive-advantage direction:

- Random minus semantic: `+0.002551 [0.002440, 0.002664]`.
- Common minus semantic: `+0.001506 [0.001395, 0.001615]`.
- Registered worse-control minimum: `+0.001506 [0.001396, 0.001618]`; seed values `+0.001468`, `+0.001544`.
- Active-child deletion cost: `+0.004691 [0.004559, 0.004825]`.
- Mean wrong-child substitution cost: `+0.005355 [0.005205, 0.005504]`.

The 95% intervals use 10,000 paired bootstrap draws, resampling windows within each fine domain and weighting all nine domains and two seeds equally.

## 4. Evidence Lineage

| Claim or decision | Criterion | Raw artifact | Aggregation | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Semantic partition value | beat random and common in both seeds, pooled lower bound positive | intact per-window NLL arrays | equal domain/seed, paired bootstrap, minimum statistic | `+0.001506 [0.001396,0.001618]` | Eligible | Pass | average over domains |
| Child necessity | deletion cost positive | delete/intact arrays | same pairing/bootstrap | `+0.004691 [0.004559,0.004825]` | Eligible | Pass | necessity not selectivity alone |
| Child non-interchangeability | wrong-child cost positive | wrong1/wrong2/intact arrays | mean wrong path, paired bootstrap | `+0.005355 [0.005205,0.005504]` | Eligible | Pass | gold path required |
| Domain robustness | direction by fine domain | same intact arrays | mean across two seeds within domain | positive `7/9`; Biology and Physical sciences negative | Registered secondary | Mixed boundary | not multiplicity-controlled |
| Representation readability | semantic effective state exceeds random modestly | development/confirmation representations | fixed probe | effective probe about `0.929` versus `0.923` | Diagnostic | Positive small | hard child residual contains route code |

## 5. Visual Evidence

### The Oracle value and function gates all pass

![Decision-bearing contrasts](figures/decisive_contrasts.png)

How to read: the semantic-versus-random, semantic-versus-common, deletion, and wrong-child points are all above zero with narrow intervals. This is direct task and intervention evidence, not route appearance.

### The gain is not universal across domains

![Per-domain robustness](figures/per_domain_robustness.png)

How to read: both hard semantic contrasts are positive in seven domains but negative in Biology and Physical sciences; the learned semantic contrast is negative in all nine.

### Representation analysis is supporting evidence only

![Representation probe](figures/representation_probe.png)

How to read: the hard semantic effective representation is more linearly readable than the learned conditions, but most native readability was already present and the Base was frozen. The perfect hard child-residual probe reflects gold route-conditioned residuals and cannot establish improved native geometry.

## 6. Position And Domain Diagnostics

The hard random-minus-semantic advantage remains positive from early to late targets: approximately `+0.002850`, `+0.002594`, and `+0.002422` over target bins 64--95, 96--159, and 160--255. The common-minus-semantic advantage is similarly stable near `+0.00149`, `+0.00155`, and `+0.00148`. The result is therefore not produced only by one short sequence region.

The two negative fine domains are replicated across both seeds and both controls:

- Biology: random-minus-semantic about `-0.000574`, common-minus-semantic `-0.001444` after seed averaging.
- Physical sciences: random-minus-semantic about `-0.000850`, common-minus-semantic `-0.001875`.

This suggests the registered hierarchy is useful on average but over-partitions at least some science text. It does not invalidate the primary equal-domain estimand, but it prevents a universal semantic-routing claim.

## 7. Interpretation And Failure Decomposition

The Oracle Pass establishes that the old CLINC result was not solely a classification-answer code: on a standard next-token objective, correct semantic grouping still creates a small but stable held-out benefit and larger child intervention costs. The stronger wrong-child cost than deletion cost is consistent with genuinely different child functions, because substituting another trained child is worse than removing the child residual.

However, E07 shows that current learned routing does not recover this value. The joint evidence narrows the bottleneck: the partition has headroom, and learned children matter, but the learned forward policy is suboptimal. Route prediction is only moderately semantic—fine-route F1 about `0.564`, NMI about `0.121`—and expert outputs are probability-scaled. These two mechanisms remain confounded.

## 8. Claim Boundary And Next Decision

Can claim: the supplied M2D2 fine-domain partition has functional continued-training value under one frozen Qwen3-0.6B, one block, two-stage LoRA realization.

Cannot claim: learned recovery, benefit for all domains, deep compositional semantics, native Base reshaping, larger-model transfer, or deployable routing without metadata.

Next decision: on the frozen learned-semantic checkpoints, cross predicted/gold expert index with learned/unit coefficient. If gold index alone recovers the Oracle direction, route prediction is primary; if unit coefficient is required, attenuation is primary; if neither recovers it, child training under predicted routes is the remaining bottleneck.

## 9. Artifact Manifest

| Artifact | Purpose | Identity | Complete | Claim eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| Full run root | raw checkpoints, arrays, logs | `/data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing/runs/full-20260901T174147Z` | yes | yes | 38 evaluation files |
| ACP receipt | remote execution | job `pt-i9fis3c8`, `SUCCEEDED` | yes | yes | reserved four H100 |
| Dataset | frozen input tensors | SHA `8cd04d99...51a8` | yes | yes | exact manifest adjacent |
| Aggregate | primary estimates and diagnostics | SHA `e3d7deaf...354b9` | yes | yes | analysis revision in run code hash |
| Completion audit | completeness/causality | SHA `35886070...5d2e` | yes | yes | `complete: true` |
| Figures | human reading path | local `figures/` | yes | as labeled | per-domain figure generated after primary analysis |

Worker: `/data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing`  
Reproduction entry: `MODE=full DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1 bash submit_h100_4_reserved.sh`
