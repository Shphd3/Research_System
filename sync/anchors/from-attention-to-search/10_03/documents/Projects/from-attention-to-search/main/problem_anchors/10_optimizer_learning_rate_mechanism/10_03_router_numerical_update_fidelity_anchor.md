派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_03_router_numerical_update_fidelity_anchor.md`。
[精确原始文件](../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_03_router_numerical_update_fidelity_anchor.md)；研究修改仍回到原件。

---

---
anchor_id: "10_03"
canonical_language: en
task_state: SOURCE_AUDIT_AND_CALIBRATION_COMPLETE
question_state: OPEN
design_state: AI_PROPOSAL_PENDING_RESEARCHER_REVIEW
result_state: NATURAL_REPLAY_NOT_RUN
---

# A10_03: Does Router numerical error change a finite learning update?

## 1. Problem Definition

**Decision question:** at one fixed MoE model and optimizer state, does changing only the numerical evaluation of the same differentiable Router objective change the finite one-step task-loss effect beyond the replay error floor?

The researcher requested a bounded numerical-research assessment and local Anchor placement on 2026-10-24. The question and proposed natural-data comparison below are **AI operationalization for review**, rather than a confirmed explanation of an existing failure. Source inspection and synthetic calibration are complete; the natural-token comparison is NOT RUN. No Focus is created or reset.

A10 concerns common directions and optimizer-dependent learning stability. This is an independent sibling of A10_01/A10_02: it asks whether the gradient entering that optimization analysis faithfully represents its objective. A05 owns top-1 collapse mechanisms; A16 owns load-control effects; A15_24_01 owns clipping and AdamW-history coupling. Their results are neither reinterpreted nor inherited as evidence of a numerical cause.

The useful outcome is a decision about whether this numerical explanation merits further investigation. A residual in the sum of logit gradients alone does not establish a meaningful learning effect.

## 2. Physical Priors

1. **Exact relation:** where the selected expert set is fixed, a loss depending only on softmax probabilities is invariant to adding the same scalar to every expert logit. Its logit gradients sum to zero. Top-K boundaries require separate treatment; a logit-dependent regularizer such as z-loss need not obey this relation.
2. **Verified numerical possibility:** mathematically equivalent softmax computations can produce different derivatives. The source calibration below establishes this possibility for one unnormalized top-1 path, with counterexamples for normalized paths.
3. **AI hypothesis:** such an error may survive gate normalization, output casting, other gradient paths, clipping and optimizer history sufficiently to change a finite task-loss effect on natural tokens. Whether it does is Unknown.

## 3. Falsifiable Hypotheses

**H-N, AI proposal:** a reproducible native-versus-stable numerical-gradient difference causes a finite one-step task-loss difference above the matched replay error floor, with the stable gradient closer to a qualified higher-precision reference.

**Rival:** the relevant states do not reach a sensitive regime, gate normalization cancels the discrepancy, or the discrepancy has negligible effect after the actual optimizer. Genuine task interference and common-feature learning remain alternatives. The diagnostic need not find the stable variant beneficial.

## 4. Mathematical Model

For one token, the Router maps its input \(h\in\mathbb R^d\) to expert scores \(z=Wh\), where \(W\in\mathbb R^{E\times d}\), and probabilities \(p=\operatorname{softmax}(z)\). Write \(g=\nabla_z L\), \(w_e=\bar w+\widetilde w_e\), with \(\bar w=E^{-1}\sum_e w_e\). The exact input gradient is

\[
\nabla_h L=\sum_e\widetilde w_e g_e+\bar w\sum_e g_e.
\]

For the shift-invariant component, \(\sum_e g_e=0\); a computed nonzero sum can therefore introduce a component along the **mean expert weight row**. This row mean is distinct from a common input feature or a CrossCoder feature. The relation identifies a possible error path, not its prevalence or a task consequence. AdamW can also produce a nonzero mean row update from exact zero-sum gradients because its coordinatewise states differ.

For the proposed finite comparison, let \(S\) contain the same parameters, optimizer moments/counters, clipping rule and learning rate. Let \(U(S,G)\) be the complete parameter increment from the full parameter gradient \(G\). The primary observable, in nat per valid prediction token, is

\[
D=L_{\mathrm{probe}}\!\left(\theta+U(S,G_{\mathrm{native}})\right)
 -L_{\mathrm{probe}}\!\left(\theta+U(S,G_{\mathrm{stable}})\right).
\]

Both losses use the same evaluation arithmetic and fixed probe tokens. Positive \(D\) favors the stable update on this local probe; negative \(D\) favors native. Neither sign establishes long-term training benefit. Update-vector differences and logit-gradient residuals explain the comparison but cannot replace it.

## 5. Computational Realization

**Completed scope audit.** Read the paper's full eight sections and the two local routing implementations. Reuse their routing expressions through AST extraction; adapt only the softmax computation for the stable and float64 references. No trainer, pretrained model, saved representation or dataset is reused in calibration. The [source/calibration record](../../research_notes/router_numerical_fidelity/20261024_scope_audit.md) retains exact provenance, the fixed case grid and the source-placement audit.

**Proposed bounded natural replay, NOT RUN.** First bind one actual executed source/config, exact checkpoint with optimizer state, one Router layer, source batch and disjoint probe batch. Inspect the real dtypes and margin distribution. At the same recorded upstream derivative, compare native, stable and higher-precision Router derivatives. Preserve the same selected experts and forward values when isolating the backward effect; report forward precision and near-tie selection effects separately. Propagate the derivative substitution through the complete gradient, then clone the same state \(S\) for each virtual update and evaluate \(D\). No original checkpoint is mutated.

Task, effective load-balance and any z-loss terms are differentiated separately before combining them. Apply zero-sum checks only to terms that are shift invariant. The natural checkpoint, layer, token selection, numerical error calibration and finite step remain proposed choices to freeze in a Protocol; this Anchor is not executable.

**Prior-art decision.** [Barron et al.](https://jonbarron.info/softmaxfix/) supply an adapted, objective-preserving stable arithmetic comparator. [Switch Transformers](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf) establish selective Router precision as an existing baseline. [ST-MoE §3.3–3.4](https://arxiv.org/html/2202.08906v2) motivate inspecting logit magnitude and z-loss; adding that loss changes the objective and is deferred. Subtracting the gradient mean is a diagnostic, not an equivalent numerical repair.

## 6. Minimal Falsification Tests

Use one natural frozen-state replay before considering retraining. The primary quantity is \(D\), accompanied by same-method replay/no-op comparisons under identical evaluation arithmetic.

- **Supports a local numerical effect:** the intervention changes only the intended derivative; stable agrees better with a qualified reference; and the finite difference exceeds the frozen replay uncertainty. Preserve either sign of \(D\).
- **Does not support further work in the tested scope:** numerical-gradient differences cancel or remain below the finite-effect error floor. Park this numerical explanation for that state.
- **Insufficient:** source/objective, inherited optimizer state, forward matching, reference quality, or measurement resolution is unresolved.

No numerical threshold or sample budget is approved yet. Freeze an independently calibrated error floor and the exact asset/split identities before natural execution; do not tune the criterion after observing \(D\). A tiny relative denominator or a large gradient residual cannot rescue an unresolved finite-effect comparison.

## 7. Current Evidence

The [bounded CPU calibration](../../research_notes/router_numerical_fidelity/20261024_scope_audit.md) used five predefined strict-order logit vectors, two source kernels, top-1/top-2 and three arithmetic variants: 60 rows, synthetic inputs only. Native unnormalized top-1 had mean relative logit-gradient error 0.316676 across this constructed grid; normalized top-2 had 6.6444e-8. The original normalized top-1 path had zero task gradient under every variant. These are implementation calibrations, not population estimates or evidence about the current model's training states.

The same record gives a constructed upstream-gradient/zero-moment AdamW example and its negative controls. It establishes a realizable numerical path worth testing and an important cancellation boundary. Natural margins, natural-gradient prevalence, inherited-state update effects, \(D\), expert-choice changes and long-term consequences are **NOT RUN / Unknown**.

## 8. Claim Boundary And Next Decision

The formal update is a bounded numerical rival and a falsifier. Existing A05/A15/A16/A17 scientific conclusions remain unchanged. Calibration does not establish a cause of Router collapse, meaningful cross-task interference, useful expert specialization, or benefit from replacing softmax.

**AI-suggested next decision:** retain or park this numerical explanation after one qualified natural frozen-state replay. Resume by binding the actual executed source and exact optimizer-bearing state, then freeze the small comparison in its Protocol. Broader precision sweeps and new training are deferred until a local finite effect warrants them.
