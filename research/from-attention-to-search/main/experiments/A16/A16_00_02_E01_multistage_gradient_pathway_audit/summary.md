---
experiment_id: A16_00_02_E01_multistage_gradient_pathway_audit
status: complete
scientific_verdict: fail_global_centering_mediation_with_early_stage_relief
last_updated: 2026-08-09
---

# Final Result Summary

## Direct conclusion

The strict hypothesis failed: running-centering did not consistently reduce the immediate held-out language cost of a differentiable Switch load-balancing (LB) objective across both seeds and all registered early, middle, and late states. It also did not consistently reduce LM/LB opposition in the Router-source and Gate pathways or within-expert update conflict.

A narrower stage-specific result is established. At about 50M tokens, one effective LB shadow update increased WoS NLL by 0.000845/0.000617 nat/token in Vanilla, while the Centered effects were indistinguishable from zero. The paired Centered mediation effects were +0.000839/+0.000630 and both document-level intervals were above zero. Centering therefore removed a reproducible early LB cost, but this advantage did not persist uniformly.

## Primary outcome

The immediate LB cost is the WoS NLL difference after one exact-state LM+LB versus LM-only AdamW shadow update. The Centered mediation is \(M=\Delta NLL_{LB}^{Vanilla}-\Delta NLL_{LB}^{Centered}\).

| Seed | \(M\) at 50M | \(M\) at 6B | \(M\) at 10B | Three-stage median and 95% interval | Verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| 17 | +0.000839 | -0.001466 | +0.000242 | +0.000242 [-0.001474, +0.000961] | Fail |
| 29 | +0.000630 | -0.000685 | +0.002152 | +0.000630 [+0.000376, +0.000938] | Pass |

Both seeds were required to pass, so the registered outcome verdict is **Fail**, not Insufficient.

![Centered mediation](figures/figure2_centering_mediation.png)

## Mechanism verdicts

- **Shared Router pathways: Fail.** Centering made both Router-source and Gate LM/LB cosines less opposed at 50M, but the gains became negative at 6B and 10B.
- **Within-expert conflict: Fail.** The token-weighted negative cosine mass was nearly zero in Vanilla and about \(4.0\times10^{-4}\) to \(5.5\times10^{-4}\) in Centered at 6B/10B. This does not show healthier Vanilla experts: collapsed routing can mechanically make the few retained expert groups homogeneous. It only falsifies the registered lower-conflict prediction.
- **Hard-load response.** The LB shadow step reduced Vanilla's mean maximum expert share by roughly 0.74--1.49 percentage points, versus about -0.18 to +0.02 points in Centered. LB had less hard-load leverage once routing was already balanced.

## Validity and boundary

All 12 arm--seed--stage cells passed the checkpoint, optimizer, paired-batch, WoS, shadow-state, direct-derivative, and artifact guards. All four formal 8x5090 jobs succeeded.

The source 30B runs recorded `lambda_LB=0.01`, but re-entrant activation checkpointing detached the nested LB tensor from the backward graph. These checkpoints were not trained under an effective LB gradient. A16 is therefore a counterfactual one-step audit at frozen states, not a measurement of LB's original long-run trajectory effect.

The result does not establish that centering's long-run benefit comes from globally lower LB conflict, that lower within-expert negative cosine is necessarily healthier, or that one-step effects predict 30B efficiency.

## Next decision

Compare **Centered + dynamic expert bias**, **Centered + truly differentiable LB**, and **Centered without additional load control**. This directly tests whether non-gradient hard-load control can preserve usable expert load without paying the stage-dependent differentiable-LB cost.

