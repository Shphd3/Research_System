# 01 Common Operator Mechanism Closure Report

## From "Common Direction" To Mechanism-Indexed Common Operators

## Abstract

This line asks one narrow question: when we say a mixture-of-experts router or
expert has a "common" component, what object are we actually estimating?

What we established:

```text
Common is not one universal hidden-state direction.
Common is an operator family indexed by the mechanism being tested.
```

What the experiments show:

```text
Controlled regimes support mechanism-conditioned estimators:
activation principal component analysis (activation PCA), group mean, gradient
intersection, and feedback drift each win when the criterion matches the
mechanism.
The real-DCLM text-training bridge shows that gate-logit drift reproduces the
A06 proxy-route collapse, but a simple low-rank gate-logit common does not
explain or rescue that collapse.
```

What we do next:

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

The next experiment must decide whether the real collapse is caused mainly by
gate-weight drift, hidden-state drift, or their interaction.

Reading path: Sections 1-5 explain the mechanism and the mathematical reason a
common branch is not identifiable by loss alone. Sections 6-9 explain the
controlled evidence, the real negative result, and the next decision. Section
10 and the appendix provide the audit trail.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters here | What it cannot prove |
|---|---|---|---|---|
| mixture-of-experts (MoE) | Architecture where a router sends each token state to one or more experts. | In this line, the router computes scores $z=Wh$ from hidden state $h$ and gate weights $W$. | The common question is about what the router or experts learn repeatedly across groups. | MoE routing alone does not prove expert specialization or utility. |
| common component | Structure shared across groups, tokens, or training updates under a specified criterion. | It may be an activation direction, mean offset, gradient direction, or checkpoint drift. | The whole line asks which object should be called common. | It is not automatically removable, harmful, or universal. |
| common operator / projector $P$ | Linear map used to select, remove, or replay a candidate common subspace. | Residualization uses $(I-P)h$; feedback replay uses $P\Delta h$. | It makes the common claim testable. | A good $P$ for one criterion need not work for another criterion. |
| residual component | What remains after the candidate common part is removed. | $(I-P)h$ for static hidden states or $(I-P)\Delta h$ for drift. | It tests whether the removed part carries the targeted mechanism. | Residual does not mean "unique" unless the criterion proves that. |
| activation principal component analysis (activation PCA) | Finds high-variance hidden-state directions. | Top eigenvectors of hidden-state covariance. | It is the natural baseline for "common direction." | High variance does not imply shared function or redundant gradient. |
| gradient intersection | Finds directions shared by gradients across groups. | A candidate subspace is scored by how much it reduces pairwise group-gradient cosine after removal. | It estimates optimization-common in controlled mismatch regimes. | It does not identify real feedback drift or expert utility. |
| feedback drift | Training-time change that may overwrite routing. | $\Delta h=h_t-h_0$ for hidden states or $\Delta z=z_t-z_0$ for gate logits. | It connects common estimation to early-training preservation failure. | Aggregate drift alone cannot separate gate-weight drift from hidden-state drift. |
| gate logit | Router score before top-1 selection. | $z_t=W_t h_t$. | The real-DCLM bridge tests whether logit drift reproduces route collapse. | Logit evidence does not by itself identify hidden-state causality. |
| proxy-route normalized mutual information (proxy-route NMI) | Agreement between proxy labels and top-1 expert assignments. | NMI ranges from 0 to 1; higher means assignments match the proxy partition better. | It is the preservation metric for A06/A01_04 real-DCLM bridge. | It does not prove semantic experts or language-model utility. |
| explain fraction | Fraction of full route collapse reproduced by a candidate drift. | Example: NMI drop under feedback-only replay divided by full NMI drop. | It tests whether the candidate common component is sufficient to reproduce collapse. | A high value is not specific if random subspaces also explain collapse. |
| rescue fraction | Fraction of route collapse removed by deleting a candidate drift. | Compare residual-only NMI with full-drift NMI relative to step-0 NMI. | It tests whether removing the candidate component restores routing. | It does not guarantee loss-neutral training or expert utility. |
| real-DCLM bridge | Real-text audit that replays recovered router logits from the DCLM-bin setup. | Uses a 6-layer Qwen3-MoE toy model, raw-center router, seeds 0/1/2, layers 3/4/5, checkpoints 0/5/10. | It checks whether controlled feedback conclusions survive real training artifacts. | It does not test every layer, scale, dataset, or intervention. |
| low rank | A small-dimensional subspace used as a compact common explanation. | The real bridge first tests rank-1 logit drift and then sweeps higher ranks. | Low-rank success would make a simple projector target plausible. | Higher-rank reconstruction can be nonspecific because random subspaces also improve. |

## 1. Motivation

The project repeatedly observed that common components can dominate
specialization:

- common offsets can become expert-specific router biases;
- common logits can collapse top-1 routing;
- early training can erase a step-0 proxy route;
- common/rare gradient overlap can interfere with specialization.

A tempting shortcut is to call the top hidden-state singular direction, batch
mean, sequence mean, or route-logit contrast "the common direction." That
shortcut is unsafe. The same word "common" can refer to different objects:
high activation variance, shared prediction function, redundant gradient
updates, or training feedback drift.

The purpose of the 01 line is to make this ambiguity explicit before designing
a common branch, residualized router, or unique-expert input split.

## 2. What Must Be Distinguished

There are four objects that are easily confused.

| Name | Concrete meaning | Typical estimator | Failure if confused |
|---|---|---|---|
| activation common | high-variance shared activation structure | activation PCA | can select high-variance unique or nuisance directions |
| functional common | component needed for shared prediction | loss after masking $Ph$ | can be useful and should not always be removed |
| optimization common | component producing redundant cross-group updates | gradient intersection | may be invisible in activation covariance |
| feedback common | checkpoint-to-checkpoint drift that overwrites routing | drift replay/removal | can be dynamic, not visible in static step-0 geometry |

This distinction is the core lesson borrowed from the advisor-style documents:
define the confused concepts first, prove a clean baseline or impossibility,
then test the mechanism under controlled and real conditions.

## 3. Clean Impossibility Result

Let a model output be the sum of a shared branch and a routed branch:

$$
F_g(h)=S(h)+R_g(h).
$$

For any function $\Delta(c)$ of the shared component $c$, define:

$$
S'(h)=S(h)+\Delta(c),\qquad R'_g(h)=R_g(h)-\Delta(c).
$$

Then:

$$
S'(h)+R'_g(h)=S(h)+R_g(h)=F_g(h).
$$

Therefore a loss that only sees $F_g(h)$ cannot identify whether the function
$\Delta(c)$ belongs to the shared branch or the routed branch.

This is the first anchor of the story. Adding a common branch does not
guarantee that the common branch learns common, and it does not guarantee that
unique experts stop learning common. A mechanism criterion is required.

## 4. Mechanism Model

Use the hidden-state decomposition:

$$
h=c+u_g+\epsilon,
$$

where $c$ is shared structure, $u_g$ is group-specific structure, and
$\epsilon$ is unmodeled structure. A candidate operator $P$ is only meaningful
relative to a criterion.

Three static criteria are:

$$
\operatorname{Var}_g(\mathbb{E}[Ph\mid g])
\quad\text{for cross-group stability,}
$$

$$
\Delta L_c(P)=L_c((I-P)h)-L_c(h)
\quad\text{for shared-prediction causality,}
$$

and

$$
\Delta C(P)=
\mathbb{E}_{g\neq g'}\cos(G_g,G_{g'})
-
\mathbb{E}_{g\neq g'}\cos(G_g^r(P),G_{g'}^r(P))
$$

for gradient redundancy, where

$$
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g].
$$

The dynamic criterion is feedback replay/removal. If
$\Delta h=h_t-h_0$, a feedback projector $P_{\mathrm{fb}}$ is relevant only if
replaying $P_{\mathrm{fb}}\Delta h$ reproduces collapse and removing it
rescues routing.

## 5. Propositions And Proofs

### Proposition 1: Activation And Gradient Common Can Diverge

Let $a,b$ be orthonormal. Let $z_a,z_b$ be uncorrelated unit-variance scalars,
and let $\epsilon$ be isotropic noise with smaller variance than both signal
terms. Define:

$$
h=s_a a z_a+s_b b z_b+\epsilon,\qquad s_b^2>s_a^2.
$$

Then the activation covariance has larger eigenvalue in direction $b$ than in
direction $a$, so the top activation PCA direction is $b$.

Now assume group gradients share input direction $a$:

$$
G_g=q_ga^\top+E_g,
$$

where the perturbation $E_g$ has no shared right-singular direction larger than
the $a$ term. The shared gradient right direction is then $a$. Since
$a\perp b$, activation PCA and gradient intersection select different
projectors. Therefore activation variance is not a sufficient definition of
optimization common.

### Proposition 2: Real Gate-Logit Drift Mixes Three Mechanisms

For gate logits $z_t=W_th_t$:

$$
z_t-z_0=W_th_t-W_0h_0.
$$

Adding and subtracting terms gives:

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

So an aggregate logit-drift experiment cannot by itself tell whether collapse
comes from gate-weight drift, hidden-state drift, or interaction.

## 6. Controlled Evidence

The controlled experiments build the story step by step.

**A01_01: identifiability.** With known $P_c^*$ synthetic hidden states, four
estimator families win under different regimes:

```text
criterion_winner_diversity = 4
```

This weakens the single-estimator theory.

**A01_03: optimization common.** In activation-gradient mismatch regimes,
gradient intersection beats activation PCA on gradient-overlap reduction:

```text
n_passed_mismatch_regimes = 4 / 4
```

This supports gradient intersection as the current estimator for
optimization-common.

**A01_04 controlled feedback bridge.** In feedback regimes, feedback-only
replay reproduces proxy-route collapse, and feedback removal rescues routing:

```text
n_passed_main_feedback_regimes = 2 / 2
controls_ok = true
```

This shows that feedback-common collapse is a valid controlled mechanism.

## 7. Real Evidence And Negative Result

The bounded real-DCLM bridge reused the A06 raw-center proxy setup. It captured
gate logits for seeds 0/1/2, layers 3/4/5, and checkpoints 0/5/10.

Full logit drift reproduces the observed A06 collapse:

```text
step0 NMI = 0.7549
step5 full NMI = 0.0410
step10 full NMI = 0.0131
```

But the low-rank feedback-logit bridge fails:

```text
pass = false
mean_explain_valid = 0.4230
mean_rescue_valid = 0.1625
mean_random_explain_valid = 0.3355
```

Higher ranks reconstruct more collapse, but random subspaces also improve.
Therefore high-rank reconstruction is not specific evidence for a low-rank
common mechanism.

## 8. Reconciliation And Refined Theory

The controlled and real results are not contradictory.

Controlled experiments show:

```text
If the relevant common mechanism is isolated, the matching estimator can find
or replay it.
```

The real gate-logit experiment shows:

```text
In real DCLM, aggregate gate-logit collapse is not explained by one simple
rank-1 logit-common direction.
```

The refined theory is:

```text
Common must be indexed by mechanism and layer/state role.
Real preservation failure likely mixes gate-weight drift, hidden-state drift,
and expert-feedback effects.
```

This is why a residualized MoE method is premature. We do not yet know which
real term should be residualized.

## 9. Next Experiment

The next test should compute route NMI under three replay states:

$$
z_{\mathrm{gate}}=z_0+(W_t-W_0)h_0,
$$

$$
z_{\mathrm{hidden}}=z_0+W_0(h_t-h_0),
$$

$$
z_{\mathrm{interaction}}=z_0+(W_t-W_0)(h_t-h_0).
$$

Decision rule:

| Dominant collapse term | Interpretation | Next action |
|---|---|---|
| $(W_t-W_0)h_0$ | gate weights drift away from proxy partition | gate-update or router-loss intervention |
| $W_0(h_t-h_0)$ | hidden states are pushed by training feedback | hidden feedback-common estimator |
| interaction / cancellation | collapse is coupled and not projector-simple | build finer feedback model before methods |

## 10. Source Map And Audit Tables

This closure does not introduce new measurements. It reorganizes the already
recorded A01 evidence into one line-level mechanism story.

### 10.1 Source Map

| Object | Source |
|---|---|
| Route document | `../route_document.md` |
| Chinese route document | `../route_document_cn.md` |
| A01_01 identifiability | `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md`; `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/detailed.md` |
| A01_03 activation/gradient mismatch | `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md`; `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/detailed.md` |
| A01_04 controlled feedback bridge | `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md`; `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/detailed.md` |
| A01_04 real-DCLM logit bridge | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md`; `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/detailed.md` |

### 10.2 Experiment Logic Chain

| Step | Question | Evidence | Decision unlocked |
|---|---|---|---|
| A01_01 | Is "common" one estimator or criterion-dependent? | Four estimator families win in different controlled regimes. | Treat common as mechanism-indexed. |
| A01_03 | If activation and gradient criteria conflict, which estimates optimization-common? | Gradient intersection wins all four mismatch regimes. | Use gradient intersection for optimization-common audits; keep activation PCA as a rival. |
| A01_04 controlled | Can feedback-common be causally replayed and removed in a controlled router? | Feedback-only replay collapses proxy routes; residual-only removal rescues them. | Feedback-common is a valid controlled mechanism. |
| A01_04 real-DCLM | Does a simple low-rank gate-logit common explain the real A06 collapse? | Full logit drift reproduces collapse, but rank-1 explain/rescue fails and random controls are close. | Decompose real drift into gate-weight, hidden-state, and interaction terms before method construction. |

### 10.3 Measured Results

| Experiment | Primary metric | Observed result | What it decides | What it cannot decide |
|---|---|---:|---|---|
| A01_01 | `criterion_winner_diversity`: number of distinct non-random estimator families that win primary criteria. | 4 | A universal common estimator is not supported in controlled regimes. | Real-DCLM common, layer choice, or utility. |
| A01_03 | `gradient_overlap_reduction_advantage`: $\Delta C(P_{\mathrm{grad}})-\Delta C(P_{\mathrm{act}})$. | 4 / 4 mismatch regimes pass. | Optimization-common is better estimated by gradient intersection than activation PCA in controlled mismatch settings. | Real feedback causality or preservation rescue. |
| A01_04 controlled | `proxy_nmi_drop_explained_by_feedback_common`: fraction of full proxy-route NMI drop reproduced by feedback-only drift. | 2 / 2 main feedback regimes pass; controls ok. | Feedback replay/removal is a valid controlled preservation mechanism. | Real-DCLM hidden drift or loss-neutral intervention. |
| A01_04 real-DCLM | Real bridge pass rule: rank-1 explain/rescue must specifically explain and rescue full collapse. | `pass=false`; mean explain 0.4230; mean rescue 0.1625. | Low-rank gate-logit common is insufficient as the main real explanation. | Whether hidden-state drift or gate-weight drift is dominant. |

### 10.4 Proof / Assumption / Empirical Ledger

| Statement | Type | Status | Boundary |
|---|---|---|---|
| Loss on a shared+routed sum cannot assign a function component uniquely to the shared or routed branch. | Proven from the algebra in Section 3. | Supported. | It is an identifiability result, not a statement that common branches never help. |
| Activation PCA and gradient common can select orthogonal projectors. | Proven by construction in Proposition 1. | Supported; A01_03 adds controlled evidence. | It assumes the stated covariance and gradient structure. |
| Aggregate gate-logit drift mixes gate-weight drift, hidden-state drift, and their interaction. | Proven by algebraic decomposition in Proposition 2. | Supported. | It does not say which term dominates in the real run. |
| Feedback common can overwrite routing. | Controlled empirical proposition. | Supported in A01_04 controlled. | Not yet established for real-DCLM hidden-state drift. |
| Low-rank real gate-logit common explains A06 collapse. | Empirical proposition. | Weakened by A01_04 real-DCLM. | Higher-rank reconstruction is nonspecific because random subspaces also improve. |
| Real hidden-state feedback common explains A06 collapse. | Open empirical proposition. | Unresolved. | Requires the next gate-weight/hidden-state decomposition. |
| Residualized MoE or a common branch should be built now. | Method proposal. | Not supported as the next mainline step. | It can be revisited after the real drift source is isolated. |

## 11. Claim Boundary

Can claim:

- controlled common estimation is mechanism-conditioned;
- gradient intersection is the current controlled estimator for
  optimization-common;
- feedback replay/removal is a valid controlled preservation mechanism;
- real gate-logit drift reproduces A06 collapse;
- low-rank gate-logit common is insufficient as the main real explanation.

Cannot claim:

- real hidden-state feedback common is identified;
- gate-weight drift and hidden-state drift are separated;
- common branch or residualized MoE improves language-model loss or rare-token
  utility;
- one layer-global common projector is enough;
- proxy-route NMI proves semantic expert utility.

Current working assumption:

```text
The real preservation failure is a coupled training-feedback problem. The next
valid move is decomposition, not method construction.
```

## Appendix: Data / Model / Parameters / Scripts

| Experiment | Data / model / objective | Parameters and checkpoints | Runner and result path | Primary metric |
|---|---|---|---|---|
| A01_01 | Synthetic hidden states with known $P_c^*$; criteria test subspace recovery, shared-loss sensitivity, and gradient-overlap reduction. | dim 16; common rank 2; unique rank 2; 6 groups; 600 samples/group; seeds 0-9. | `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/scripts/run_common_operator_full_run.py`; result dir `../../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/`; config `tables/run_config.json`. | `criterion_winner_diversity` |
| A01_03 | Synthetic activation/gradient mismatch states; objective is to separate activation variance from optimization redundancy. | dim 32; common/functional/unique/nuisance ranks 2; 6 groups; 500 samples/group; seeds 0-19. | `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/scripts/run_gradient_vs_activation_full_run.py`; result dir `../../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/`; config `tables/run_config.json`. | `gradient_overlap_reduction_advantage` |
| A01_04 controlled | Synthetic proxy router with feedback and residual drift; objective is replay/removal causality for proxy-route collapse. | dim 32; 8 experts; 600 samples/group; feedback rank 1; seeds 0-19. | `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/scripts/run_feedback_bridge_controlled_full_run.py`; result dir `../../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/`; config `tables/run_config.json`. | `proxy_nmi_drop_explained_by_feedback_common` |
| A01_04 real-DCLM | DCLM-bin real-text setup; 6-layer Qwen3-MoE toy model; raw-center router; recovered gate-logit artifacts from next-token training. | seeds 0/1/2; layers 3/4/5; checkpoints 0/5/10; 65,536 eval tokens/layer; lr 0.0003; batch 2. | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/scripts/run_real_dclm_feedback_logit_bridge.py`; rank sweep `scripts/reanalyze_real_feedback_logit_artifacts.py`; result dir `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/`. | real bridge pass rule |

Key real-DCLM artifacts:

| Artifact | Path |
|---|---|
| source manifest | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/config/source_manifest.json` |
| run config | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/config/run_config.json` |
| per-cell bridge scores | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_scores.csv` |
| bridge summary JSON | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_bridge_summary.json` |
| rank sweep | `../../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/runs/real_dclm_logit_bridge_20260629_full01/tables/real_feedback_logit_rank_sweep_summary.csv` |
