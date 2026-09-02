# A15_13_03: Do Fine Intents Align with Functional Task Gradients?

Thinking Card source: [15_13_03_semantic_gradient_functional_alignment_thinking_card_cn.md](15_13_03_semantic_gradient_functional_alignment_thinking_card_cn.md)

## 1. Problem Definition

The decision question is whether CLINC150 fine intents correspond to distinct task-update requirements and whether assigning one hard-routed child LoRA expert to each intent improves held-out task loss and selective child-expert utility over matched random and unsplit controls. This is the smallest unresolved clause after E05: semantic supervision organized routing and induced parent selectivity, but did not establish fine-expert representation or task gain. The frozen Qwen3-0.6B-Base is not retrained, semantic-label discovery is out of scope, and gold routes are diagnostic rather than deployable.

## 2. Physical Priors

The human-confirmed prior is that semantic partitioning is functionally valuable only when examples within a semantic group demand more compatible task updates than examples across groups. A label partition that merely encodes the classification target, without improving held-out optimization or selective expert interventions over balanced random grouping, is not sufficient evidence for semantic expert value.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that gold fine-intent grouping produces a positive held-out task-loss advantage over both a balanced random within-domain partition and an unsplit within-domain child, while matched child deletion is selectively harmful. The strongest rival predicts that cross-entropy makes same-label gradients appear similar but arbitrary partitioning or a shared path achieves the same held-out result. A second rival is optimization bypass: semantic gradient structure exists, but shared LoRA and the task head absorb the update before child experts form function.

## 4. Mathematical Model

For example $i$, let $g_i=\partial \ell_i/\partial z_i$ be the task-cross-entropy gradient with respect to the child-residual output interface $z_i$ at the stage-two entry checkpoint. The local alignment diagnostic is

$$
\Delta_{\mathrm{align}}
=
\mathbb E[\cos(g_i,g_j)\mid f_i=f_j,d_i=d_j]
-
\mathbb E[\cos(g_i,g_j)\mid f_i\ne f_j,d_i=d_j],
$$

where $f_i$ is the fine intent and $d_i$ its domain. Alignment is a mechanism diagnostic, not the value endpoint. The primary value quantity is the worst-control confirmation-loss advantage

$$
V_{\mathrm{task}}=
\min\{\bar\ell_{\mathrm{random}}-\bar\ell_{\mathrm{semantic}},
       \bar\ell_{\mathrm{common}}-\bar\ell_{\mathrm{semantic}}\},
$$

in natural-log units per confirmation example. It is positive only when semantic splitting beats both matched rivals.

## 5. Computational Realization

CLINC150 supplies 15,000 training, 2,997 development, and 4,498 untouched confirmation utterances after the verified E05 deduplication. The task remains 150-way sequence-level intent prediction. A frozen Qwen3-0.6B-Base receives rank-eight shared, parent, and child LoRA residuals at zero-indexed block 14, for active rank 24 in the split conditions.

Stage one uses the gold domain to select one of ten parent experts with unit weight. Stage two freezes the parent path and compares: one common child per domain, a deterministic balanced random child assignment within domain, and one gold-intent child per intent. Hard-routed parent and child outputs always have weight one. Shadow Routers read detached native block input, predict gold domain or intent for diagnostic semantic metrics, and neither select nor scale experts nor send route-loss gradients into model or expert states.

## 6. Minimal Falsification Tests

The decisive test is the semantic split against the random and common controls at the fixed final update. Pass requires positive seed-level task-loss differences against both controls and a positive 95% intent-stratified bootstrap lower bound for $V_{\mathrm{task}}$, together with two positive child-function gates: deleting the active child and replacing it with a wrong within-domain child must each increase loss in both seeds with a positive pooled lower bound. Fail means the complete eligible comparison is non-positive against either control or either functional gate fails. Insufficient means a required condition, seed, gradient null, confirmation loss, or intervention artifact is missing or the implementation allows Router probabilities or gradients to affect expert computation.

Gradient alignment, norm-matched one-step development gain, module gradient/update shares, macro F1, worst-intent performance, residual magnitude, and shadow-route semantics explain the outcome but cannot rescue a failed primary value test. If alignment and one-step gain are present while realized child utility is absent, a pre-registered child-responsibility intervention freezes shared LoRA, parent experts, Routers, and task head and trains only child experts.

## 7. Current Evidence

E05 completed 32 final conditions across two seeds. Gold and spherical supervision prevented route collapse and produced positive parent selective utility, but the gold fine-intent probe effect was only +0.191 F1 points with a 95% interval crossing zero, and no hierarchical semantic condition improved task F1. Gold child residuals were only 0.52%--0.56% of the shared residual. This establishes the need for the present gradient and responsibility audit but does not establish its outcome. The complete predecessor evidence is recorded in the linked [E05 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/summary.md).

E06 then completed the registered hard-route audit across two seeds. Gold semantic grouping beat both the balanced-random and common-child controls in both seeds. The pooled worst-control confirmation cross-entropy advantage was `0.03126` natural-log units per example with a 95% interval of `[0.02928, 0.03335]`. Active-child deletion increased loss by `0.05092` `[0.04883, 0.05304]`, and wrong-child substitution increased loss by `0.05230` `[0.05015, 0.05444]`; both effects were positive in both seeds. The typed verdict is `PASS_SEMANTIC_FUNCTIONAL_VALUE`. Gradient alignment was strongly positive, but the norm-matched one-step semantic update did not beat both controls, so that local proxy does not explain the realized multi-step gain. Full evidence and the one-step deviation boundary are recorded in the [E06 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/summary.md) and [Detailed record](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/detailed.md).

## 8. Claim Boundary And Next Decision

A Pass would support only that supervised fine-intent partitioning provides functional post-training value on hard-routed CLINC150 under one frozen-base, one-layer LoRA realization. It would not establish self-discovered labels, deployable learned routing, better pretraining geometry, open-domain semantics, or generative-task benefit. A Fail would stop treating CLINC150 fine intents as sufficient evidence for semantic expert value under this objective. An optimization-bypass outcome would support only a responsibility-allocation diagnosis.

The evidence supports the hard-route value branch rather than the optimization-responsibility branch. Pending the researcher's confirmation of this wording and boundary, the sole next decision is whether to open a learned-Router recovery experiment that measures how much of the established Oracle gain survives predicted routing without retraining the frozen Base.
