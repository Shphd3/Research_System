# A5 balanced h-input training: result summary

[Protocol A5.6–A5.9](../protocol.md) · [Detailed evidence and timing proposal](detailed.md)
Run: `full-20260908T111248Z`; job `pt-j131dsb1` SUCCEEDED.
Execution: 15/15 conditions × 512 updates, 15 full internal-test evaluations, 30 pairwise comparisons, six SAE/GMM interventions.
Interpretation: requested AI analysis; human scientific judgment and Focus transition remain unconfirmed. This is a separate result from old E20; do not mix their tables.

## 1. Purpose

Test whether SAE-derived routing provides stable answer-prediction benefit beyond random grouping and ordinary task-learned routing under the approved shared h-input architecture and loss-free selection bias.

## 2. Hypothesis

SAE should outperform matched random grouping in all three seeds; stronger method advantage also requires outperforming task-only routing. The rival is that ordinary task optimization, not the SAE partition, provides the useful routing.

## 3. Analysis method

- Fixed final update 512; answer-token-weighted internal-test negative log likelihood (NLL), lower is better. Three seeds 17/29/43 share paired sample schedules.
- Average the three seed-level values equally; sample SD is descriptive, not a confidence interval or pooled-seed hypothesis test.
- Use registered within-seed paired record-bootstrap comparisons, preserving seed reversals. Test loss and generated-answer benchmark accuracy are different endpoints.

### Training objectives and regularization coefficients

This experiment has two distinct optimization stages. Before MoE training, the fixed-teacher SAE, random-feature and GMM Routers minimize teacher-target KL plus ridge regularization,
\[
\mathcal L_{\mathrm{Router}}=
\frac{1}{|V|}\sum_{t\in V}D_{KL}(q_t\Vert p_t)
+\frac{\lambda_W}{2}\lVert W\rVert_F^2.
\]
Only the Router weight matrix \(W\) is penalized; the development-selected SAE values for seeds 17/29/43 were respectively `0`, `0`, and `0.001`. SAE feature grouping itself is a fixed spectral clustering operation, not a feature-separation regularization loss.

During the subsequent 512-update MoE adapter/expert training, every condition uses
\[
\mathcal L_{\mathrm{MoE}}=1\cdot\mathcal L_{\mathrm{answer\ CE}}+0\cdot R.
\]
Thus this stage has training-loss coefficient **1**, no explicit regularization term, and regularization-loss coefficient **0**. Separately, AdamW applies decoupled weight decay `0.01` to shared/expert adapter parameters; the task-only Router uses weight decay `0.0`. No auxiliary or load-balancing loss is added. The count-based balancing-bias update rate `0.001` is not a loss coefficient. See the [stage-by-stage formulas and all seed-specific coefficients](detailed.md#training-objectives-and-regularization-by-stage).

## 4. Conclusion

**Task-only routing has the lowest mean test loss (0.696579). SAE does not show stable superiority over the random control.** Its mean test loss is 0.734016 versus random 0.735215, but seed 43 favors random by 0.003481 nats/token, with a paired interval wholly favoring random. GMM (0.716802) also outperforms SAE in every seed.

| Condition | Train last 32 steps mean ± SD | Final development mean ± SD | Final test mean ± SD |
|---|---|---|---|
| C1 sae | 0.738629 ± 0.006551 | 0.743663 ± 0.000578 | 0.734016 ± 0.000526 |
| C2 random_features | 0.740085 ± 0.003115 | 0.745295 ± 0.004319 | 0.735215 ± 0.004531 |
| C3 gmm | 0.721069 ± 0.006706 | 0.726445 ± 0.002236 | 0.716802 ± 0.002218 |
| C4 task_only | 0.700752 ± 0.007100 | 0.706973 ± 0.000916 | 0.696579 ± 0.000782 |
| C5 dense_shared_r16 | 0.743415 ± 0.005932 | 0.748476 ± 0.000948 | 0.738619 ± 0.000927 |

Source: [condition means](tables/condition_means.csv), derived from the authenticated per-record test sums and per-seed training records in [verification](/data/250010109/MoE_Router/reports/a5_20260908/verification.json). Training column is the token-weighted last 32 updates, not a full training-set reevaluation. Development has 8,480 records; internal test has 8,481.

![Loss curves](figures/loss_curves.png)

How to read: left is the changing training-batch objective in non-overlapping 32-update windows; right evaluates the same full development set at five checkpoints. Lines average three seeds and shading is one sample SD. C4's advantage is present on both surfaces, not just a final noisy training batch. Fluctuating training batches cannot diagnose overfitting on their own.

![Fixed final test loss](figures/test_nll.png)

How to read: each dot is one seed; black marks mean ± sample SD. C2's seed 43 is lower than all C1 values, so the small C1–C2 mean gap cannot be called stable.

### Claim boundary

The direct result is lack of demonstrated cross-seed stable SAE advantage in this setting, not proof that all SAE routing is ineffective. Positive SAE/GMM route-intervention effects show dependence on the trained assignment under that intervention, not uniquely semantic expert specialization. Internal holdouts are not clean official benchmarks.

Protocol section 10 has a label ambiguity: a nonpositive random contrast maps to `NO_STABLE_STRUCTURE_GAIN`, while another sentence maps any seed reversal to `INSUFFICIENT`; the Anchor likewise treats reversal as insufficient evidence. No automatic label promotion is made. Both readings reject a stable favorable SAE claim.

### Next-step analysis — AI proposal, not execution approval

Measure whether the loss ranking transfers to generated-answer accuracy using one shared frozen evaluation contract. First benchmark throughput for 20–30 minutes, then screen Base plus all five conditions at prechosen seed 17 on a fixed stratified subset. Target 2–4 hours on four H100 GPUs **only if a qualified common larger batch achieves sufficient throughput**; retain a 4-hour screen budget and do not silently truncate generation. If projected runtime exceeds budget, return the scope choice before a long run. Partial screening cannot replace full benchmark scores or cross-seed confirmation.
