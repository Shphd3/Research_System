# Understanding update: sharing changes the whole learning path

[中文](cognition_update_cn.md) · [Today's summary](daily_summary.md)

Research window: 2026-10-04 15:53:50–17:53:50 UTC. This is a derived stage synthesis for the original temporary question, not a question-closure report. Interpretations and suggestions are AI-authored; scientific confirmation remains Unknown. Execution is explicitly authorized. The bounded analyses and report are complete; GPU observations close at 17:48:35 UTC, with full training incomplete.

**This window makes two existing gaps more precise: matching gains remain within domains/categories, yet every original policy loses to common; out-of-fold FIT selection returns eleven of twelve policies to common. Separately, immediate help can reverse at a finite horizon under stable future learning.** Sharing must therefore be evaluated as a complete policy under specified information, optimizer, resources and horizon, rather than from present matchability alone.

This is not a claim to discover a new universal learning law. The additions are a more direct empirical localization of the current negative result, an explicit bridge and counterexample between immediate and later utility, and continued execution of the registered shared/private comparison. Sections 1–3 concern current selection; sections 4–6 connect it to learning; section 7 records actual completion.

## 1. The question is unchanged; three decision objects differ

The question remains: when should different inputs share parameter updates, and when should they use separately learned experts, to improve acquisition and retention under limited resources? The [Anchor](../1002/candidates/ntp_representation_update_channels/anchor.md) owns that question; the [Protocol](../1002/candidates/ntp_representation_update_channels/protocol.md) owns exact execution. The Anchor already separates current selection, later learning and optimizer boundaries. This window adds empirical localization and explicit derivations, without claiming those distinctions are newly discovered. The temporary location is retained, without a new Focus or scientific closure.

| Object | Actual comparison | What it can answer |
|---|---|---|
| Selection among existing computations | Fix a model and action bank, select from pre-target inputs, then read measured finite loss | Whether this selector beats a strong fixed action |
| Allocation of learning | Apply the same training data to common parameters or private copies and compare trajectories | Whether the specified finite-budget scheme improves acquisition and retention |
| Later effect of one update | Accept/reject an update from one state, then run the same future training rule | Whether that update still helps at a specified future horizon |

The first does not automatically answer the other two. Its failure does not refute separate learning; its success does not establish long-run sharing value. Possibility at later stages also cannot turn a negative current selector into a successful one.

## 2. New empirical localization: within-category matching does not offset leaving common

The original fixed-bank study freezes Dense, fresh S7 and SALL at 33B cumulative training tokens; 33B is a token coordinate, not parameter count. Source panels A/B each generate four domain updates and one common update. Predictors fit 512 FIT records and score 1024 DEV records at 16 positions each. The common action averages raw gradients before independent normalization; it is not an average of action losses.

Previously emphasized results showed all 92 cross-source pooled conditions beating random assignment at the same global action frequencies while losing to the FIT-fixed common action. This window verifies that **all 92 within-source pooled conditions also lose to common, with all original conditional 95% interval upper bounds below zero**. Within source means selecting and scoring actions from the same source bank while still evaluating DEV records. It does not mean reporting FIT training performance as DEV. [Original Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_summary.md), [switch audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/policy_switch_audit_cn.md).

Gain is common loss minus policy loss; positive is better. Values below are micro-nats/event. Ranges span registered conditions, not intervals or independent replications.

| Model | Same policy's in-FIT gain | Within-source DEV gain | FIT-positive / DEV-negative conditions |
|---|---:|---:|---:|
| Dense | +856.5 to +3122.2 | −431.5 to −102.2 | 28/28 |
| fresh S7 | +1432.9 to +5310.3 | −792.0 to −145.2 | 32/32 |
| SALL | +909.2 to +3348.0 | −437.7 to −109.8 | 32/32 |

Source transfer alone is therefore an insufficient explanation. The fitted policy's FIT gains do not carry to this same-source DEV panel. Different record composition, estimation error, selection-amplified error, function-class limitations and irreducible target variation remain rivals; this contrast does not uniquely identify overfitting.

This window also tests whether coarse receiving-label composition alone accounts for positive matching gain. For every frozen policy, preserve its action frequencies inside each receiving category and compute expected cost after randomizing choices within that category. The control allows different category preferences while removing within-category matching. Every whole-record bootstrap draw reestimates frequencies and costs.

**All 184 same/cross-source pooled conditions still beat category-matched random allocation, with positive conditional 95% lower bounds; all intervals against common remain negative.** Four-domain controls also retain positive gains. These are pooled weighted residuals, not claims of positivity in every individual category. Cross-source within-category ranges are:

| Model | Category-matched random cost minus policy cost, micro-nats/event | Positive intervals |
|---|---:|---:|
| Dense | +93.34 to +332.36 | 28/28 |
| fresh S7 | +186.51 to +670.21 | 32/32 |
| SALL | +124.05 to +391.36 | 32/32 |

For Dense/base/A→B/five actions, the +133.49-micro-nat global matching gain splits exactly into +40.15 from category composition and +93.34 within category; the latter interval is [+7.73,+173.81]. The same policy is −386.77 against common. Coarse domain/category composition cannot by itself explain these matching gains. Finer association remains without establishing net adoption value. [Group-decomposition Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary.md).

Let \(S\) denote leaving the common action and \(D\) the chosen action's additional measured loss. Since \(D=0\) without switching, exactly

\[
\mathbb E[D]=\Pr(S)\,\mathbb E[D\mid S].
\]

For Dense/base/A→A with five actions, the policy switches on about 75.46% of events. At those events it predicts a mean 1467-micro-nat saving but incurs about 352 micro-nats of additional loss. Approximately 49% of switches still help: errors are not universal, but the probability and magnitude of improvements fail to offset harms. Mean realized advantage on the switching subset is negative in all 184 same/cross-source pooled conditions. [All 184 rows](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/policy_switch_audit.csv).

An outcome-informed event oracle still has roughly 4764–8347 micro-nats of headroom, with a better measured action than common on about 89%–91% of events. This rules out pointwise common dominance in measured outcomes. The oracle reads post-target results, cannot be deployed, and does not show that pre-target inputs predict those differences.

The distinction has an exact expression. Let \(R_{\mathrm{fixed}}\) be the best fixed-action population risk, \(R_X\) the ideal minimum risk given pre-target information X, and \(R_{\mathrm{oracle}}\) the risk of selecting after reading outcomes. Then

\[
R_{\mathrm{fixed}}-R_{\mathrm{oracle}}
=(R_{\mathrm{fixed}}-R_X)+(R_X-R_{\mathrm{oracle}}).
\]

Both terms are nonnegative: ideal pre-target information value and additional outcome-informed advantage. Large total oracle headroom can coexist with zero first term. An exact loss-table example in this window has common conditionally best at every input, while a restricted policy beats its usage-matched random control and every realized event offers a better hindsight action. **Those positive signals therefore do not prove pre-target value over common; the example does not identify this mechanism in the real panel.** Finite DEV has not directly identified \(R_X\). [Derivation, example and exact arithmetic](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/decision_value_bridge.md).

The supported description is therefore: **post-outcome heterogeneity and within-category matching gains exist, but predictions are optimistic on the subsets where policies choose to switch.** Readable differences are not by themselves an adoption argument.

## 3. Out-of-fold selection mostly returns to common; reduced loss is not adaptive advantage

A registered, completed CPU diagnostic uses three models, the original base and full-input families, and banks A/B: twelve amplitude selections. Only the fixed five actions are included, without rejection; success proportions cannot be directly compared with the original 92 conditions spanning two action sets. Four-fold cross-fitting keeps whole FIT records together. Feature means/scales and output intercepts are rebuilt only on each training fold. With training-fold mean finite effect \(\mu_a\) and fitted prediction \(\widehat q_a\), score

\[
\widehat q_a^{(\alpha)}=\mu_a+\alpha(\widehat q_a-\mu_a),
\qquad\alpha\in\{0,0.1,0.25,0.5,1\}.
\]

Only out-of-fold FIT loss chooses \(\alpha\). Final DEV uses the original all-FIT prediction and means: alpha 0 returns to fixed common, and alpha 1 must exactly reproduce the old selector. OOF predictions come from smaller training folds and are not the original all-FIT predictions. The same selected amplitude is used for both same-source and cross-source DEV. When common has the uniquely best mean, shrinking the amplitude raises the local predicted advantage required to leave it. The check tests conservative use of the same prediction.

**Eleven of twelve selections choose \(\alpha=0\), the fixed common action; only SALL/base/bank A chooses \(\alpha=0.1\).** Frozen selections produce 24 pooled same/cross-source DEV evaluations. All improve over the original \(\alpha=1\) policy, with positive lower bounds of their paired conditional 95% intervals. Yet 22 simply return to common and the remaining two still have negative pooled gains against common.

| Model | Pooled gain over original policy, micro-nats/event | Gain over common |
|---|---:|---|
| Dense | +265.74 to +453.33 | All 8 are zero: common is selected |
| fresh S7 | +434.38 to +707.13 | All 8 are zero: common is selected |
| SALL | +283.38 to +464.68 | 6 zero; the other 2 are −6.23 and −19.72 |

The sole retained adaptive amplitude switches away from common on 2.53% of DEV events. Its A→A gain is −6.23 micro-nats, interval [−20.88,+9.06]; A→B is −19.72, interval [−35.49,−3.45]. FIT selection mostly removes switching. The complete grid is retained: 95 of 96 nonzero-amplitude pooled estimates are below common; one slightly positive \(\alpha=0.1\) estimate was not FIT-selected and is not used to select another policy.

This sharpens the interpretation: **whole-record out-of-fold checking mostly rejects the input-dependent component of these two estimators; their in-sample gains do not justify leaving the strong common action.** The result is limited to these features, samples, ridge fits and amplitude grid. It does not show that pre-target inputs lack information.

All 600 grid rows, 120 selected subgroup rows and 300 FIT cross-fitting rows are saved. Alpha 1 reproduces the original event choices; alpha 0 returns exactly to the original fixed action. [Result Summary](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary.md), [execution receipt](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json). DEV was already exposed and the selected OOF minimum itself is biased. Intervals do not refit or correct for multiplicity. Improvement does not uniquely identify repaired overfitting or long-run learning value.

## 4. Sharing changes gradient aggregation and optimizer computation

In the small-model comparison, C is the common FFN, \(E_d\) the known-domain-selected private FFN, and T the remaining shared trunk. `common_parallel` uses \(C(z)+E_d(z)\); `private_active` copies C's channels into every domain expert. Their initial functions match up to floating-point summation and active FFN widths match. The private model stores three additional C copies, adding 4,718,592 parameters. Its trunk T remains shared; it is not four independent models.

At a common initial state, with ordinary SGD and explicitly matched scale, tied C allows a source example to alter other domains through C. Untying copies removes that cross-domain channel. Whether its effect helps depends on receiving-loss sensitivity, not the structure's name.

Actual AdamW adds another distinction: shared gradients combine before squaring, whereas copies maintain separate second moments. For the same specified external gradient streams, fixed positive weights summing to one, zero initial moments, synchronized participation, and equal clocks and decay coefficients, the exact coordinatewise identity is

\[
v_{S,t}=\sum_d p_dv_{d,t}
-(1-\beta_2)\sum_{s=1}^{t}\beta_2^{t-s}
\sum_d p_d(g_{d,s}-\bar g_s)^2,
\quad\bar g_s=\sum_d p_dg_{d,s}.
\]

Here\(p_d\) are domain weights and \(v\) are second-moment exponential statistics. The conditional moments \(v_{d,t}\) are not actual private checkpoint moments whose gradients already include \(p_d\). This follows from mean square minus squared mean, without a random-independence assumption. The shared second moment is not the average conditional second moment. A smaller shared moment does not by itself mean a better estimate or update.

Actual mixed-phase private gradients additionally contain\(p_d=1/4\). Under ideal fixed-scaling Adam conditions that factor cancels between first/second-moment normalization, so it is not a quarter-sized parameter step. Global clipping, epsilon, different activity clocks and subsequent trajectory divergence further limit simple correspondence. [Derivation and CPU algebra checks](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/adam_and_readout_audit.md).

**Interpretation:** matched initialization removes the initial prediction gap, but does not separate aggregation, preconditioning, storage or update history. The six arms compare complete finite-budget schemes; one favorable endpoint cannot independently identify a common-representation mechanism.

## 5. Immediate help can reverse under stable future learning

Fix one model and state coordinate system; parameters of different architectures cannot simply be subtracted. Let \(s_t\) be complete training state, including parameters and optimizer moments. Hold future data/randomness fixed, write future updates\(s_{u+1}=U_u(s_u)\), and terminal risk\(R(s_N)\). On one smooth branch, the later effect of a current perturbation is

\[
\Delta R_N=\nabla R(s_N)^\top
D U_{N-1}\cdots D U_t\,\delta s
+O(\|\delta s\|^2).
\]

This chain rule says future learning reweights today's changes. AdamW moments belong to the state; parameter Hessians alone do not describe its transition derivative. Hard routing, clipping boundaries and changed skip counters further restrict the local formula. Finite branches require replay or remainder control. [Independent mathematical review](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/independent_theory_review.md); an established source for differentiation through training is [Maclaurin et al., 2015, §2](https://proceedings.mlr.press/v37/maclaurin15.pdf).

An exact example reverses the sign. Start two parameters at zero with old risk\(L_B(w)=\tfrac12(w_1+w_2-1)^2\). For source loss \(L_A(w)=\tfrac12[(w_1-2)^2+(w_2+1)^2]\), one gradient step at learning rate 0.1 produces\(\delta=(0.2,-0.1)\), reducing old risk from 0.5 to 0.405.

Both accept/reject branches then take the same learning-rate 1 gradient step on \(L_C(w)=\tfrac12(0.9w_1^2+0.1w_2^2)\). Here C labels the future task, independently of the common-FFN label in the previous section. Its update matrix is \(\operatorname{diag}(0.1,0.9)\): both directions contract, without negative curvature or coordinate overshoot. The accepted branch becomes \((0.02,-0.09)\), with old risk 0.57245; the rejected branch remains zero, with risk 0.5.

![Finite-horizon reversal under stable convex learning](figures/finite_reversal.png)

The green point is the accepted source update; the red point follows one identical future step. Future learning removes the helpful first coordinate faster and retains more of the harmful second coordinate. The right panel compares branches at the same horizon: immediate gap −0.095, then +0.07245. **This is an analytical squared-loss example, not an LM measurement.** Repeating the future update eventually sends both branches to zero, so the gap vanishes. The claim is finite-horizon, and reversal persists for arbitrarily small positive source steps. [Exportable PDF](figures/finite_reversal.pdf).

The example refutes automatic persistence of immediate positive transfer. It does not establish prevalence in language models. The missing evidence is now more concrete: how subsequent training preserves or changes a current effect, rather than another measurement of current gradient similarity alone.

A first-order guarantee is also precise. Write P for the product of future state-update derivatives, \(g_t\ne0\) for current old-risk sensitivity, and \(P^\top g_N\) for future old-risk sensitivity propagated back to the current state. **Every perturbation direction retains its linearized utility sign if and only if \(P^\top g_N=cg_t\) with \(c>0\).** Stable contraction alone does not ensure this alignment. The statement is linearized: finite steps require remainder control, while a restricted perturbation subspace or finite action bank does not require full-space collinearity. Current logs do not measure these complete-state sensitivities, so this does not identify reversal in the real models. [Proof and boundaries](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/future_sign_certificate.md).

Future sensitivity is also not a signal already available to a router. The expression fixes or retrospectively reads the future training process and terminal risk. When that future is unknown at decision time, a risk-neutral allocation rule would need expected later utility conditional on its allowed information. A retrospective identity does not supply that forecast. As with the outcome-informed oracle, an explainable effect is not automatically deployable decision information.

## 6. Read the complete acquisition–retention trajectory

The existing contract has 512 mixed updates followed by four 1024-update domain phases. Shared parameters participate in 4608 updates, each private expert in 1536. The globally declining LR sums over the four domain phases are 0.283852, 0.205944, 0.108722 and 0.042958, a first/last ratio 6.608. **This is not a 6.608-fold learning amount or parameter displacement.** Equal update counts do not imply equal learning opportunities; weak later acquisition cannot automatically be called insufficient capacity.

For one domain, denote DEV losses at mixed-end, just before/after its own phase, and final by\(L_M,L_-,L_+,L_F\). The registered matrix admits the exact reading

\[
L_M-L_F
=\underbrace{L_M-L_-}_{\text{transfer before own phase}}
+\underbrace{L_--L_+}_{\text{own-phase acquisition}}
-\underbrace{L_F-L_+}_{\text{later forgetting}}.
\]

A common model may help a domain before its own phase, leaving less additional own-phase gain while finishing better. Looking only at own-phase gain misses that possible value. No earlier transfer for the first phase and no later forgetting for the last are structural timing zeros, not capabilities.

C/T rollback exchanges modules between phase endpoints; expert swaps change domain–expert matching within the same final checkpoint. They measure finite effects of specified interventions, without reconstructing the optimization path. Endpoint optimizer states cannot recover unlogged conditional gradients or causal contributions. Read absolute loss, prior transfer, own acquisition, later retention and measured cost together. [What current logs can support](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/adam_and_readout_audit.md).

## 7. Window execution and boundaries

Both new bounded CPU diagnostics are complete. Their Summary/Detailed records preserve every condition, method, result and limit. Separate implementations recomputed 12,240 shrinkage values and about 4.78 million group-decomposition bootstrap values. Mathematical examples use exact arithmetic. Figure, table and compact-audit origins are recorded in the [selected evidence manifest](payload_manifest.json). These checks add no sample independence or researcher scientific approval.

Four-card RTX5090 Spot job `pt-scl8ek3y` actually started and passed hardware qualification. Seed1003 passed all 42 exact-resume state checks across six arms. Seed1004 failed the original FP32 combined tolerance at one of 524,288 initial hidden-feature entries, so overall qualification failed. The platform records termination at 17:14:49 UTC; no formal trajectory started.

Before another GPU observation, numerical qualification was explicitly amended to exact full parameter mapping, an independent genuine-FP64 forward at fixed 1e−10 tolerances, and correct finite native shapes. Original FP32 failure remains diagnostic and is not relabelled as passed. Production model/training arithmetic is unchanged. CPU positive/negative controls, an independent implementation reference and six-arm tiny integration passed. [Amendment and recovery certificate](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/initial_equivalence_recovery_20261004/execution_certificate.md).

**Window cutoff:** Recovery `pt-c44kwvx3`, submitted at 17:23:53, was still STARTING with a Pending worker and no runtime at the 17:48 cutoff. It was stopped at 17:48:22; the 17:48:35 verification reports SUSPENDED. All twelve formal trajectories have zero updates and no checkpoints. Amended exact GPU qualification remains NOT RUN, and none of the eighteen registered endpoint mechanism readouts was obtained. This window therefore cannot rank shared, private or serial training schemes. [Final status and provenance](evidence/final_window_status.json).

The current **AI understanding update** is that sharing should be judged by the cross-input update effects it creates and the acquisition/retention those effects leave after the actual optimization process. Present matching, estimation reliability, optimizer processing and future propagation are connected stages; a sign at one stage does not stand for the entire path.

Researcher judgment on practical utility thresholds, strongest mechanism, architecture adoption and closure remains Unknown. Exposed DEV, correlated conditions, limited samples and seed/order confounding remain explicit. Computational verification adds no independent experimental replication.

Delivery verification covers local links and mathematical source in 26 current documents, plus file/source hashes in both selected-evidence manifests. Root git-payload checks pass; navigation retains one pre-existing, unrelated untracked Diffusion literature entry. Source checks do not certify rendering or scientific correctness. [Delivery verification](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/second_window_20261004/delivery_verification.json).
