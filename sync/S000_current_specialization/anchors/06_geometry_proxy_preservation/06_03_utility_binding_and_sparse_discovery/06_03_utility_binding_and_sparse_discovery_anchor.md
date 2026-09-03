# A06_03 Utility Binding And Sparse Discovery

Status: completed parent anchor in the controlled four-expert bridge.


## 1. Complete Problem

**Decision question:** Can training create distinct expert functions and can a
sparse Router discover and exploit them with bounded counterfactual feedback?

### Terminology / Definitions

| Term | Plain meaning | Computation | Cannot prove |
|---|---|---|---|
| Specialist | Expert with a held-out condition-specific loss advantage | forced-expert loss matrix | Natural semantics |
| Selected-path blindness | Unselected experts do not expose their own output quality | wrong-rank top-1 correction failure | Failure of every sparse estimator |
| Challenger | One additional nonselected expert evaluated with the incumbent | pairwise forced loss | Systems efficiency |
| Tail-safe certificate | Stop only when weak utility samples favor the incumbent | lower quantile or lower-tail mean | Joint-training theorem |

## 2. Physical Priors

1. Conditional exposure, not expert name or load, creates function.
2. Counterfactual utility and confidence in an already correct route are
   different objects.
3. Reweighting observed gradients cannot create missing expert comparisons.
4. Discovery cost should be reduced only after weak conditions have corrected.

## 3. Falsifiable Hypotheses

**H1: conditional function formation.** Correct exposure does not create
held-out specialist utility beyond load-matched shuffle. Rejected.

**H2: utility-confidence equivalence.** Larger expert-identity utility implies
larger margin growth for an already correct top-1 route. Rejected.

**H3: selected-only discovery.** Native weighted top-1 recovers a useful expert
from rank 2 or rank 4. Rejected on the learned bridge.

**H4: bounded coverage.** One rotating challenger is sufficient for correction,
and a lower-tail certificate can stop it without losing weak routes. Supported
within the frozen four-expert system.

## 4. Core Mathematical Model

Held-out specialist utility is

$$
G_f^{cf}=\min_{b\ne f}
\left[L_{f,b}^{cf}-L_{f,f}^{cf}\right].
$$

Selected-only top-1 observes $\ell(E_r(h),y)$ but not
$\ell(E_e(h),y)$ for $e\ne r$. A challenger $c_t$ supplies

$$
\widehat A_{r,c_t}
=\ell(E_{r_t}(h),y)-\ell(E_{c_t}(h),y).
$$

For recent pairwise samples $U$, phase-switch candidates are

$$
\overline U,
\qquad q_{0.10}(U),
\qquad
\operatorname{LCVaR}_{0.10}(U)
=\mathbb E[U\mid U\le q_{0.10}(U)].
$$

## 5. Evidence Chain

1. Correct exposure creates positive held-out utility in 128/128 task-seed
   cells. The paired correct-minus-shuffle median is 8.892 nats per task token,
   with 95% confidence interval $[8.694,9.142]$, while both route NMIs are 1.0.
2. Specialists retain lower task loss after Router release, even though their
   confidence margin grows slightly less than the generalist control.
3. Native selected-only top-1 corrects 0/128 cells at both useful-expert ranks
   2 and 4; a soft mixture corrects 128/128.
4. Task and background credit coexist, so source reweighting does not repair
   the missing expert comparison.
5. One rotating challenger corrects 128/128 rank-2 cells and 125/128 rank-4
   cells, with complete correction on task-only pairs.
6. Mean utility stops prematurely in 24/128 cells. The 10th percentile and
   lower-tail mean retain 128/128 corrections with zero premature stops while
   saving about 51% and 43% of challenger evaluations.

### Subanchor Registry

| Subanchor | Local decision | Experiment group |
|---|---|---|
| [`A06_03_01`](subanchors/06_03_01_trainable_expert_utility_binding_anchor.md) | Conditional exposure creates expert utility before Router release. | [`E01`--`E02`](/Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery) |
| [`A06_03_02`](subanchors/06_03_02_selected_path_blindness_anchor.md) | Selected-only top-1 feedback can fail to reveal a better unselected expert. | [`E01`--`E02`](/Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery) |
| [`A06_03_03`](subanchors/06_03_03_bounded_challenger_discovery_anchor.md) | One rotating challenger supplies the missing local comparison. | [`E01`](/Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger) |
| [`A06_03_04`](subanchors/06_03_04_tail_safe_phase_switch_anchor.md) | Lower-tail evidence, not mean utility, decides when exploration may stop. | [`E01`--`E03`](/Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery) |

## 6. Minimal Adjudication Contract

Functional Router tests must jointly report held-out forced-expert utility,
native task loss, sustained useful-expert correction, cumulative route regret,
expert evaluations, premature stops, and weak-condition retention. Route NMI
cannot replace any of these functional metrics.

## 7. Current Verdict

**Supported:** conditional exposure can create specialist functions;
selected-only top-1 has a controlled counterfactual-information blind basin;
one challenger plus a lower-tail switch repairs that basin in the frozen
four-expert bridge.

**Rejected:** route purity proves function, utility magnitude calibrates
correct-route confidence growth, or source reweighting alone solves discovery.

## 8. Claim Boundary And Next Decision

**Cannot claim:** natural semantic experts, joint pretrained-LLM stability,
many-expert scaling, or realized systems savings.

**Next decision:** establish whether a real unfiltered workload contains stable
expert-function headroom worth routing (`A06_04`).
