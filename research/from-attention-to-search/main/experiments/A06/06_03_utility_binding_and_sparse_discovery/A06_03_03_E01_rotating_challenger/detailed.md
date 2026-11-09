# A06_03_03_E01 Bounded-Challenger Router: Detailed Record

## Decision

H3, coverage-only sufficiency, is supported. Full-loss bounded pair routing
corrects every rank-2 cell and 125 of 128 rank-4 cells. Semantic task masking
improves time and regret but is not necessary for high eventual correction.

## Setup

A06_03_03_E01 exactly reconstructs A06_03_02_E02's 200-step learned specialists and installed
rank-2/rank-4 routers. Experts and representation are frozen. Router-only SGD
uses learning rate `0.001` for 300 updates. The full run has 32 seeds and four
tasks per seed. ACP job `pt-169humfr` succeeded on four H100 GPUs.

For selected expert \(r\), the schedule cycles through a seed-specific permutation
of the other three expert IDs. At step \(t\), candidate set \(C_t=\{r,c_t\}\) and

\[
\tilde p_e=\frac{\exp(s_e)}{\sum_{j\in C_t}\exp(s_j)},
\qquad
z=\sum_{e\in C_t}\tilde p_eE_e(h).
\]

The static schedule has zero deviation from uniform three-phase coverage. Its
realized inclusion conditioned on remaining wrong is descriptive because route
correction censors that state at different schedule phases.

## Validity Audit

| Guard | Result | Status |
| --- | ---: | --- |
| completed seeds | 32 | pass |
| specialist utility gap | `8.894682` | pass |
| generalist absolute gap | `0.004236` | pass |
| minimum rank accuracy | `1.0` | pass |
| minimum adjacent gap p05 | `0.472443` | pass |
| maximum initial load spread | `0` | pass |
| static challenger schedule error | `0` | pass |
| generalist arbitrary identity | `0/128` | pass |
| rank-2/rank-4 soft positive control | `128/128`, `128/128` | pass |

## Complete Results

| Condition | Correction | Median capped time | Median regret | Final task loss | Final useful probability |
| --- | ---: | ---: | ---: | ---: | ---: |
| rank-2 full top-1 | 0.0000 | 301.0 | 1.0133 | 6.3844 | 0.2188 |
| rank-2 task top-1 | 0.3281 | 301.0 | 0.9915 | 5.7087 | 0.3037 |
| rank-2 full pair | 1.0000 | 59.0 | 0.2305 | 0.2493 | 0.4568 |
| rank-2 task pair | 1.0000 | 36.0 | 0.1539 | 0.2031 | 0.4751 |
| rank-2 task soft | 1.0000 | 19.0 | 0.1149 | 0.0566 | 0.6508 |
| rank-4 full top-1 | 0.0000 | 301.0 | 1.0132 | 6.3817 | 0.0877 |
| rank-4 task top-1 | 0.0000 | 301.0 | 0.9917 | 6.1095 | 0.1077 |
| rank-4 full pair | 0.9766 | 192.5 | 0.6810 | 0.8304 | 0.3581 |
| rank-4 task pair | 1.0000 | 118.5 | 0.4582 | 0.5051 | 0.4015 |
| rank-4 task soft | 1.0000 | 69.0 | 0.1961 | 0.0744 | 0.6189 |
| generalist rank-4 task pair | 0.0000 | 301.0 | 1.0009 | 0.9377 | 0.1016 |

The rank-4 correction-rate factorial interaction is `0.0234375`, with
seed-clustered 95% confidence interval `[0,0.0546875]`. The lower bound is not
positive. Hence task credit improves efficiency but is not required for the
correction-rate threshold.

## Visualization Results

### Factorial Correction

![Factorial correction rates](figures/factorial_correction_rates.png)

- Question: which factor is necessary for sustained identity correction?
- Reading: each bar is the fraction of 128 cells reaching five-step top-1
  accuracy at least 0.95.
- Result: pair branches are near-perfect; top-1 branches are not.
- Boundary: this compares one-versus-two expert forward, not equal total FLOPs.

### Rank-4 Dynamics

![Rank-4 discovery trajectory](figures/rank4_discovery_trajectory.png)

- Question: does the challenger cause a real top-1 identity crossing from the
  lowest installed rank?
- Reading: median useful-expert softmax probability under ordinary router scores.
- Result: full-pair rises to `0.3581`, task-pair to `0.4015`; selected-only stays
  near `0.1`. Task-soft reaches `0.6189` fastest.
- Boundary: probability growth does not yet establish retained specialization
  after joint expert/representation training resumes.

## Theory Update

A06_03_02_E02's additive source model was local to selected-only top-1:

\[
P_{full}^{top1}=\tfrac12P_{task}^{top1}+\tfrac12P_{bg}^{top1}<0.
\]

A06_03_03_E01 shows that changing candidate coverage changes the forward function and
therefore the gradient field; pair pressure is not obtained by merely adding a
coverage constant to the old top-1 pressure. The useful expert's output enters
the pair loss whenever auditioned, creating a direct counterfactual comparison.
Repeated auditions accumulate sufficient evidence even under full-LM background.

The more accurate controlled model is

\[
\mathbb E[\Delta m_{u,r}]
=\rho\,P_{audition}+(1-\rho)P_{selected},
\]

where \(\rho\) is challenger duty cycle. A06_03_03_E01 tests \(\rho=1\). Production value
depends on the minimum \(\rho\) that preserves positive cumulative drift and
crossing probability.

## Claim Boundary

Supported: bounded counterfactual expert evaluation is sufficient for learned
identity discovery in this four-expert controlled task; task-position credit
accelerates but is not necessary at full audition duty cycle.

Not supported: sparse-duty sufficiency, joint end-to-end training, pretrained
LLM semantics, many-expert scaling, communication cost, MTP prioritization, or
downstream utility per activated FLOP.

## Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/protocol.md`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_42_bounded_challenger_semantic_credit_router.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_42_bounded_challenger_semantic_credit_router.json`
- Raw result: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_42_bounded_challenger_semantic_credit_router/a06_42_full_4gpu_20260711_01/`
- Job: `pt-169humfr`, `SUCCEEDED`
- Curated figures: `figures/factorial_correction_rates.png`, `figures/rank4_discovery_trajectory.png`
- Curated table: `tables/condition_summary.csv`
