# Route Document: 01 Common Operator Mechanism

## Current Route Decision

The 01 line should not move to method construction yet.

Current conclusion:

```text
controlled common estimation is mechanism-conditioned;
real low-rank gate-logit common is not sufficient.
```

Next route decision:

```text
decompose real logit collapse into gate-weight drift, hidden-state drift,
and interaction.
```

## Four Stages

| Stage | Anchor | Decision | Evidence | Status |
|---|---|---|---|---|
| 1. Identifiability | `01_01`, `01_02` | Is common one estimator or mechanism-indexed? | A01_01: `criterion_winner_diversity=4` | complete |
| 2. Optimization-common estimator | `01_03` | Is optimization common better captured by activation covariance or gradient covariance? | A01_03: `n_passed_mismatch_regimes=4/4` | complete |
| 3. Feedback bridge | `01_04` | Can feedback-common replay/removal explain preservation collapse? | A01_04 controlled: `2/2`, controls ok; real gate-logit: `pass=false` | controlled supported; real low-rank logit weakened |
| 4. Real decomposition before methods | next anchor | Which term causes real collapse? | pending decomposition of \(z_t-z_0\) | next |

## Source Artifacts

| Role | Path |
|---|---|
| A01_01 summary | `../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md` |
| A01_03 summary | `../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md` |
| A01_04 controlled summary | `../../experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md` |
| A01_04 real-DCLM summary | `../../experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md` |

## Stop Rule

Do not start common branch, residualized MoE, or anti-feedback method protocols
from this line until the real collapse decomposition is measured:

\[
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
\]
