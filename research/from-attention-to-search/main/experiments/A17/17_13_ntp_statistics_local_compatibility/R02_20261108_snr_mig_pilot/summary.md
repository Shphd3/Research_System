# R02 Result: Mean and Noise Terms of a One-Step Update (33B MoE, last-layer single expert, MIG pilot)

[中文](summary_cn.md) · [Detailed (CN)](detailed_cn.md) · [Execution contract (CN)](protocol_cn.md) · [H2 pending config (CN)](h2_4xh100_config_NOT_RUN_cn.md) · [Memory diagnostic design (CN)](memory_diagnostic_design_NOT_RUN_cn.md)

Executed 2026-11-08 on a local H100 MIG 3g.40gb, about 10.4 GPU-minutes. No training; model, SAE and load bias unchanged. Researcher scientific judgment: **Unknown**. Interpretations are AI analysis. Placement under A17_13 is an AI choice pending researcher confirmation.

## Answer

**The noise term behaves as predicted.** After one SGD step on group A, the extra harm to held-out group B from minibatch noise grows as η² and falls roughly as 1/n. Past the crossing point it quickly dominates the mean term (about 17× at n = 32, η = 1/4; about 9× at n = 128, η = 1/2). The cross-group mean help on the primary pair cannot be distinguished from zero (z = 1.28). The help-to-harm crossing η\* and its rightward shift with n are therefore supported only by derivation and a post-hoc control-variate estimator; they were not observed directly on the preregistered grid. Verdict (AI): noise part supported, crossing part insufficient; the "direction conflict is the main cause" branch did not occur.

## Model

Only block-7 expert 7's FFN moves; routes and load bias stay native. With minibatch size n, mean gradient ḡ_A, per-token covariance Σ_A, and B's held-out gradient g_B and Hessian H_B:

E[ΔL_B] ≈ −η g_B·ḡ_A + (η²/2) tr(H_B Σ_A)/n + (η²/2) ḡ_Aᵀ H_B ḡ_A.

The first term (transfer or conflict) is linear in η. The second (noise) always harms and scales as η²/n. If the first term helps, η\* = 2 g_B·ḡ_A / (tr(HΣ)/n + ḡᵀHḡ) ∝ n when the noise term dominates.

## Key results

- Controls: zero update gives ΔL = 0 exactly; repeated evaluation is bitwise identical; every branch restores exactly; float64 tail vs native fp32 token CE differs by ≤3.1e-5 nat.
- Noise-term slope in log η: 1.95–2.35 across 12 primary cells. Slope in log n: −0.77 to −1.39 for η = 1/16–2. Estimated trΣ is constant across n (A ≈ 41, B′ ≈ 210).
- Per-minibatch SNR |ḡ|²/(trΣ/n) is 0.004–0.024. A's 5,376-token mean gradient sits at its own noise floor (|ḡ_A|² = 0.0074 vs trΣ/5376 ≈ 0.0077).
- Mean projections on EVAL: same group B′→B 2.73e-3 (z = 5.2); primary cross A→B 5.67e-5 (z = 1.28). All six cross pairs help in first order (3 with z > 2); none harms. On DEV the primary cross mean term was harmful, consistent with a noise-floor sign.
- η\*: derived 0.018 / 0.036 / 0.057 for n = 32/64/128 (cross) and 0.016 / 0.022 / 0.048 (same). Control-variate crossings: 0.042 (n = 64) and 0.075 (n = 128) for the cross pair.
- The prediction "cross-group noise share is higher" was not observed: noise-to-help ratios and η\* are similar for cross and same groups. The same-group tokens have higher loss and gate weight, which enlarges signal and noise together.

## Boundary

One checkpoint, one expert, one layer, a single SGD step. A and B are unmatched in initial loss (1.59 vs 4.30) and gate weight (0.20 vs 0.49). The clusters are SAE co-activation clusters, not long-tail features. A direct η\* observation with R ≈ 1000 is NOT RUN.

## Next (AI suggestion)

The researcher decides whether to accept the bounded "noise dominates, no significant conflict" reading. If accepted, the pending 4×H100 H2 comparison tests whether concentrating one signal into a new expert raises the usable learning rate.
