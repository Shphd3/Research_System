# 01 Common Operator Mechanism

This folder contains the 01 common-operator mechanism line.

Read only one entry first:

```text
closure/01_common_operator_mechanism_closure_report.md
```

Use the route document only when deciding the next stage:

```text
route_document.md
```

## Current Verdict

```text
Common is not one universal hidden-state direction.
It is a mechanism-indexed operator family.
```

Current result chain:

| Stage | Result |
|---|---|
| A01_01 identifiability | `criterion_winner_diversity = 4` |
| A01_03 gradient vs activation | `n_passed_mismatch_regimes = 4 / 4` |
| A01_04 controlled feedback bridge | `n_passed_main_feedback_regimes = 2 / 2`, `controls_ok = true` |
| A01_04 real-DCLM gate-logit bridge | `pass=false`, `mean_explain_valid=0.4230`, `mean_rescue_valid=0.1625` |

Next decision:

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

## Files

| Role | Path |
|---|---|
| full-story synthesis | `closure/01_common_operator_mechanism_closure_report.md` |
| Chinese full-story synthesis | `closure/01_common_operator_mechanism_closure_report_cn.md` |
| route | `route_document.md` |
| Chinese route | `route_document_cn.md` |
| identifiability anchor | `01_01_common_operator_identifiability_anchor.md` |
| recovery anchor | `01_02_ground_truth_projector_recovery_anchor.md` |
| gradient-vs-activation anchor | `01_03_gradient_common_vs_activation_common_anchor.md` |
| feedback bridge anchor | `01_04_feedback_common_preservation_bridge_anchor.md` |

Do not treat this folder as a method claim. It does not support common-branch,
residualized MoE, or utility claims until the real collapse decomposition is
resolved.
