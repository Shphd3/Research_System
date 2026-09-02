# A15_13_04: Does Coarse-to-Fine Semantic Routing Have Functional Value in Causal Language Modeling?

Thinking Card source: [15_13_04_m2d2_causal_lm_semantic_routing_thinking_card_cn.md](15_13_04_m2d2_causal_lm_semantic_routing_thinking_card_cn.md)

## 1. Problem Definition

The decision question is whether a coarse-to-fine natural-language domain partition reduces held-out next-token negative log-likelihood and creates non-interchangeable child-expert function when a frozen Qwen3-0.6B-Base is continued on M2D2-Wikipedia. This is the smallest correction to the preceding CLINC150 result: CLINC routing labels were also the 150-way task answer, whereas M2D2 domain labels choose or supervise a path but never specify the next token. The experiment is limited to one block-14 rank-eight LoRA hierarchy, three coarse and nine fine Wikipedia domains, and two-stage continued training. It does not test pretraining, larger models, label discovery, or open-domain deployment.

A Pass supports functional value for the registered Oracle semantic partition. A Fail rejects that value under this realization. An Insufficient result means the causal mask, data separation, matched controls, completion, or expert interventions do not support a verdict. Learned-Router recovery is a separate typed result and cannot substitute for the Oracle verdict.

## 2. Physical Priors

The human-confirmed prior is that documents in one fine natural-language domain share conditional token-prediction regularities beyond their common coarse domain. If this partition is functionally meaningful, routing their token updates to the same child expert should generalize better than equal-capacity arbitrary grouping or no fine split. This prior is false for the registered realization if correct grouping does not improve held-out token likelihood and expert interventions show that children are interchangeable.

## 3. Falsifiable Hypotheses

The primary hypothesis predicts that hard gold fine-domain routing beats both balanced random within-parent grouping and one common child per parent on confirmation token NLL, and that deleting or replacing the active child increases NLL. The strongest rival predicts that extra conditional capacity or balanced load, not semantics, explains any gain.

The learned-Router hypothesis predicts that gold route cross-entropy organizes token routes and recovers part of the hard-Oracle advantage over an architecture-identical next-token-only Router. Its strongest rival predicts semantic-looking routes without held-out likelihood or expert-function gain.

## 4. Mathematical Model

Each sequence has tokens $x_0,\ldots,x_{255}$. The first 64 tokens provide context only. The optimized language loss is

$$
L_{\mathrm{NTP}}=-\frac{1}{192}\sum_{j=64}^{255}\log p(x_j\mid x_{<j}).
$$

The Router acting on the logit that predicts $x_j$ reads only the block-14 state at position $j-1$, which is a causal function of $x_{<j}$. In the learned treatment, route cross-entropy over the same 192 prediction positions is added with unit weight. In the hard family, the document label chooses the expert with coefficient exactly one and shadow Router probabilities never enter the forward path.

The primary Oracle value is

$$
V_{\mathrm{oracle}}=\min\{\mathrm{NLL}_{\mathrm{random}}-\mathrm{NLL}_{\mathrm{semantic}},\ \mathrm{NLL}_{\mathrm{common}}-\mathrm{NLL}_{\mathrm{semantic}}\}.
$$

It is measured in natural-log units per target token. A positive value means semantic grouping beats both registered rivals; it cannot by itself establish a deployable Router.

## 5. Computational Realization

M2D2-Wikipedia supplies official train, validation, and test files for three coarse domains, each containing three fine domains. Empty lines are removed; natural text is tokenized without adding domain names; records from one fine domain and one official split are packed with an end-of-sequence separator into non-overlapping 256-token windows. A deterministic hash sampler selects 1,024 train, 256 development, and 512 untouched confirmation windows per fine domain after exact token-window deduplication across domains and splits.

All original Qwen weights and the tied language head remain frozen. Rank-eight shared, parent, and child LoRA residuals are added to the zero-indexed block-14 MLP output. Stage one trains the coarse path. Stage two freezes the coarse Router and parent experts, then trains three local child experts per parent. The learned family compares next-token-only fine routing with gold fine-route supervision and a balanced shuffled-label control. The hard family compares one common child, a balanced random child assignment, and the gold fine-domain child. Only the hard family uses unit-weight forced paths; its shadow Routers are diagnostic and detached.

## 6. Minimal Falsification Tests

The decisive comparison is hard semantic routing against both hard controls on equal-fine-domain confirmation token NLL. Pass requires both seed-level differences to be positive, a positive pooled 95% paired fine-domain bootstrap lower bound for $V_{\mathrm{oracle}}$, and positive NLL changes in both seeds for active-child deletion and within-parent wrong-child substitution. Fail means eligible evidence violates any of those requirements. Insufficient means a condition, seed, per-token array, causal-future-invariance test, hard-route isolation test, or intervention is missing.

Learned semantic routing receives a separate `PASS_LEARNED_RECOVERY` only if it lowers confirmation NLL versus the task-only Router in both seeds with a positive pooled lower bound, improves route-label agreement, and passes both child interventions. Route entropy, normalized mutual information, probes, nearest-neighbor scores, residual geometry, and gradient alignment are explanatory diagnostics and cannot rescue a failed value verdict.

## 7. Current Evidence

CLINC150 E06 found that hard fine-intent grouping beat balanced-random and common-child controls and produced positive child deletion and substitution effects. However, its fine route label was also the intent-classification target, so that result did not establish generative-task value.

The M2D2 hard-route audit now supplies that missing natural-language-modeling test. Gold coarse--fine grouping beat both hard controls in both seeds: the pooled worst-control confirmation-NLL advantage was `0.001506` natural-log units per target token with a 95% interval of `[0.001396, 0.001618]`. Active-child deletion increased NLL by `0.004691`, and within-parent wrong-child substitution increased it by `0.005355`. The typed verdict is `PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP`; seven of nine fine domains contributed positively, while Biology and Physical sciences remained negative. The complete evidence is recorded in the [E08 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E08_m2d2_hard_semantic_route_ntp/summary.md).

Learned semantic supervision improved route-label agreement but did not recover that value. Fine-route normalized mutual information rose from `0.00646` to `0.12059`, yet learned semantic routing was worse than task-only routing in both seeds by `0.001054` NLL on average; the typed verdict is `FAIL_NO_LEARNED_FUNCTION`. Child deletion and wrong-child substitution were nevertheless positive, so experts became non-interchangeable without yielding the registered task advantage. See the [E07 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E07_m2d2_learned_semantic_router_ntp/summary.md).

The final-layer whole-window direction-plus-radius pseudo-label condition beat the strongest newly trained simple baseline, flat task-only routing, by `0.001841` NLL with a 95% interval of `[0.001684, 0.002003]` and positive effects in both seeds. It remained descriptively `0.000903` NLL worse than the matched staged task-only hierarchy. Its route normalized mutual information was `0.237`, while active-child deletion and wrong-child substitution increased NLL by `0.000932` and `0.000485`. The typed verdict is `PASS_PSEUDO_METHOD`, bounded to the registered pseudo-label construction and simple-baseline family; see the [E09 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E09_m2d2_baselines_last_layer_pseudolabel/summary.md).

## 8. Claim Boundary And Next Decision

The evidence supports a bounded functional value for the registered gold M2D2 partition in one frozen Qwen3-0.6B block-14 LoRA hierarchy. It also supports that one final-layer pseudo-label construction can preserve task performance relative to newly trained simple baselines while increasing route interpretability. It does not show that the learned semantic Router recovers the gold-route value, that pseudo routing beats the matched staged task-only hierarchy, or that the signal reflects deep semantic reasoning rather than topical lexical regularity. Native-representation formation, general unsupervised label discovery, full-model training benefit, and deployment value remain unclaimed.

Exactly one next decision follows: without retraining, run the frozen learned-Router two-by-two forward-path decomposition that crosses predicted versus gold expert index with learned versus unit route coefficient. Completion requires the same held-out token arrays and expert interventions for all four cells and a direct attribution of the Oracle-recovery loss to routing-index errors, probability scaling, or both; only then may a new training method be selected.
