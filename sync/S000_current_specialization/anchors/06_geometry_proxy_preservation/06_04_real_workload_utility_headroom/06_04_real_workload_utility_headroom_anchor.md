# A06_04 Real-Workload Expert-Utility Headroom

Status: active parent anchor; protocol not yet approved.

Thinking Card source: [06_04_real_workload_utility_headroom_thinking_card.md](06_04_real_workload_utility_headroom_thinking_card.md)

## 1. Complete Problem

**Decision question:** Does an unfiltered repository-code workload contain
split-stable expert-function heterogeneity that the native Router fails to
capture?

### Terminology / Definitions

| Term | Plain meaning | Concrete computation | Cannot prove |
|---|---|---|---|
| Workload stratum $z$ | A registered code condition used only for evaluation | language, API family, dependency type | Correct expert label |
| Forced-expert loss | Loss when one MoE layer is forced through expert $e$ | $L_{z,l,e}^{cf}$ | Deployable intervention |
| Oracle headroom | Native loss minus split-stable forced-expert oracle loss | $G_{oracle,l}$ | Learnable Router capture |
| Split stability | Useful-expert identity repeats from calibration to test | agreement and held-out gap | Causal semantics |

## 2. Physical Priors

1. A semantic Router has no target if experts are conditionally
   interchangeable.
2. Human strata may organize evaluation but may not define the correct expert.
3. Expert selection and evaluation must use different data splits.
4. The primary sample must not be prefiltered by observed utility or MTP
   semantic latency.

## 3. Falsifiable Hypotheses

**H1:** calibration-selected useful-expert identities repeat on held-out data
and yield positive oracle headroom.

**H2:** the headroom survives load-matched, token-identity, local-only, length,
and frequency controls.

If either fails, semantic Router design stops on this workload.

## 4. Core Mathematical Model

Choose on calibration data

$$
a_l(z)=\arg\min_e L_{z,l,e}^{cf,cal}.
$$

Evaluate on held-out data

$$
G_{oracle,l}
=L_{native,l}
-\sum_z p(z)L_{z,l,a_l(z)}^{cf,test},
$$

with within-stratum guard

$$
G_{z,l}
=\min_{b\ne a_l(z)}
\left[L_{z,l,b}^{cf,test}-L_{z,l,a_l(z)}^{cf,test}\right].
$$

## 5. Computational Realization

Freeze a pretrained open MoE, select candidate layers before observing utility,
force each candidate expert on the same held-out positions, and compare the
calibration-selected oracle with native routing, load-matched random routing,
and matched shortcut controls.

## 6. Minimal Falsification Test

The anchor passes only if the confidence interval for held-out oracle headroom
is positive, useful-expert identity is split stable, and the advantage survives
all registered controls on an unfiltered repository-code sample.

## 7. Current Evidence

No experiment has been run for this anchor. `A06_00`--`A06_03` establish
controlled definitions and mechanisms only; they do not establish real
workload expert heterogeneity.

## 8. Claim Boundary And Next Decision

**Supported now:** this is the minimum workload gate required before designing
an LLM-scale semantic Router.

**Not supported now:** positive repository-code headroom, a deployable Router,
natural expert semantics, or downstream efficiency.

**Next decision:** approve or reject a minimal protocol that measures held-out
functional headroom before any new gating architecture is introduced.
