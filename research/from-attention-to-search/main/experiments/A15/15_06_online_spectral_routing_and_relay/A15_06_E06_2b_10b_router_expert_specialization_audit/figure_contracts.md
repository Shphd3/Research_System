# A15_06_E06 Figure Contracts

## Figure 1 — Router functional-quality trajectory

- **Question:** do the five Router architectures become better at choosing the
  counterfactually useful expert from 2B to 10B?
- **Source:** `document_metrics.csv` from all 15 eligible checkpoint tasks.
- **Top metric:** mean expert-choice regret, nat/token, equally averaged across
  four layers; lower is better.
- **Bottom metric:** mean within-token Spearman correlation between eight
  Router logits and negative forced-expert NLL; higher is better.
- **Axes/legend:** x is cumulative training tokens (2B, 5B, 10B); y retains
  each metric's native unit; one color per arm.
- **Aggregation:** document first, then equal document average; uncertainty is
  a document bootstrap 95% interval.
- **Allowed conclusion:** architecture-specific maturation of frozen expert
  choice.
- **Limitation:** the line is one seed and does not establish causal mediation
  of language-model NLL.

## Figure 2 — 10B expert-specialization ladder

- **Question:** where does each arm sit on the progression from parameter
  differentiation to different same-input functions and decision relevance?
- **Source:** `specialization_ladder.csv`, 10B rows.
- **Panels and units:** mean input-parameter subspace overlap at rank 8
  (dimensionless, lower means less shared geometry); same-input linear CKA
  (0--1, lower means less shared output geometry); forced-expert NLL standard
  deviation (nat/token, higher means experts are less interchangeable); Router
  score--utility Spearman correlation (dimensionless, higher means the Router
  uses utility ordering).
- **Axes/legend:** x is layer 1--4; y is the panel metric; one color per arm.
- **Allowed conclusion:** whether geometric, representational, functional, and
  utilization evidence align.
- **Limitation:** no panel alone is a specialization certificate.

## Figure 3 — Decisive matched covariance-identity comparisons

- **Question:** at 10B, does HMT beat its matched random control?
- **Source:** `primary_comparisons.csv`.
- **Metrics:** HMT-minus-random expert-choice regret (nat/token; negative is
  favorable) and HMT-minus-random score--utility Spearman (dimensionless;
  positive is favorable).
- **Axes:** x is paired effect with zero reference line; y is Local and Relay;
  points are estimates and horizontal bars are paired-document 95% intervals.
- **Allowed conclusion:** registered Local or Relay covariance-specific frozen
  functional support.
- **Limitation:** one seed and immediate counterfactual utility only.

## Figure 4 — Confidence and oracle-identity guards

- **Question:** is Router confidence calibrated to choice quality, and is swap
  cost caused by token-varying oracle experts rather than one global winner?
- **Source:** `specialization_ladder.csv`, 10B rows.
- **Metrics:** Pearson correlation between Router margin and regret (negative
  is desired); largest oracle expert share (0.125 is uniform, 1.0 is one global
  oracle).
- **Axes/legend:** x is layer; y retains the panel metric; one color per arm.
- **Allowed conclusion:** whether margin has decision meaning and whether
  counterfactual utility is token conditional.
- **Limitation:** oracle diversity does not prove semantic specialization.

## Rendered-Artifact Audit — 2026-08-10

All four PNGs were opened at rendered resolution after the eligible full run.

| Figure | Source present | Axes / legend / sign checked | Observed result | Contract state |
| --- | --- | --- | --- | --- |
| 1 | `document_metrics.csv` | yes | regret remains substantial; score--utility generally rises toward 10B without consistent HMT--Random separation | PASS |
| 2 | `specialization_ladder.csv` | yes | common parameter geometry coexists with low same-input CKA and meaningful swap cost; HMT utilization is not superior | PASS |
| 3 | `primary_comparisons.csv` | yes | all four 95% intervals cross zero; no registered path passes | PASS |
| 4 | `specialization_ladder.csv` | yes | oracle identity is diverse, while margin--regret calibration is mostly in the undesired positive direction | PASS |

No plotted panel is used to strengthen the typed verdict beyond its registered
source table. Figure 3 is the decisive figure; Figures 1, 2, and 4 are
mechanism diagnostics.
