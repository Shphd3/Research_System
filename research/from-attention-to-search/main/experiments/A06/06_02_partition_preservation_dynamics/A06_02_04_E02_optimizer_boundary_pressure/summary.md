# A06_02_04_E02 Result Summary: Optimizer-Preconditioned Router Boundary Pressure

## Conclusion

AdamW's coordinate-wise router second moment is **not necessary** for early matched-margin crossing on the controlled trainable bridge.

1. Replacing coordinate-wise \(\hat v_t\) with one scalar while exactly matching the full-AdamW router-update norm reproduced 75 of 78 reference early-crossing cells (96.15%) and increased the combined early-cross rate from 40.625% to 52.08%.
2. Replacing the full AdamW direction with the current raw-gradient direction at the same update norm reproduced 69 of 78 reference cells (88.46%) and produced a similar 43.75% event rate. AdamW-specific moment direction is therefore not required for the event.
3. The immediate remaining variable is actual router-update scale. During the first 50 steps, full AdamW, scalar-second-moment, and raw-gradient norm-matched updates were 9.48--9.83 times larger in norm than nominal-SGD router updates. Nominal SGD reproduced none of the 78 reference events and reduced cumulative negative router pressure by 86.69%.

Direction still matters for the transient shape: the scalar-second-moment condition crosses more deeply and recovers later, while the current raw-gradient direction recovers fastest. The next decision is therefore a controlled router-update norm threshold, not a claim that optimizer direction is irrelevant.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it decides | Cannot prove |
| --- | --- | --- | --- | --- |
| Early crossing | Matched margin becomes nonpositive by step 50 | \(C_i=\mathbf1[T_{cross,i}\le50]\) | Captures the A06_02_04_E01 AdamW event regime | Permanent failure |
| Scalar second moment | One router-wide denominator replaces coordinate-wise AdamW \(\hat v_t\) | preserve \(\hat m_t\) direction, then match full-update norm | Removes coordinate-wise preconditioning | Removes optimizer history |
| Raw-gradient norm match | Current \(-g_t\) direction with full-AdamW update norm | \(-\|\Delta W^{full}\|g/\|g\|\) | Tests whether AdamW-specific direction is required | Norm alone without task direction |
| Reproduction fraction | Full-AdamW early events also present under intervention | \(R_q=\Pr(C^q=1\mid C^{full}=1)\) | Tests necessity of a removed component | Universal sufficiency |
| Negative router pressure | Router update projected against the current matched boundary | \([-\langle\Delta w_a-\Delta w_b,\mu_f\rangle]_+\) | Links update to margin consumption | Representation correction |

The primary population contains features 1--3 across 32 seeds and two biased-background regimes: \(3\times32\times2=192\) cells.

## Exact Setup

- Data/model/initialization: identical to A06_02_04_E01; full-sequence LM loss, no positional embedding, one causal attention layer, four fixed function-matched experts, initial margin p05 0.5.
- Representation: standard AdamW in every condition.
- Router conditions: full AdamW; scalar second moment with norm match; raw-gradient direction with norm match; nominal SGD at learning rate 0.002.
- Run: 32 seeds, 1,000 updates, four GPUs, two biased-background regimes and two guards.
- Early horizon: first 50 updates.

## Primary Evidence

| Router update | Early-cross rate | Reference events reproduced | Median crossing | Median re-entry | Final margin p05 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full AdamW | 40.625% | 78 / 78 | 7 | 16.5--19.5 | 0.136--0.138 |
| Scalar second moment, norm matched | 52.08% | 75 / 78 | 5 | 22 | 0.075--0.078 |
| Raw gradient, norm matched | 43.75% | 69 / 78 | 5 | 6--7 | 0.298--0.327 |
| Nominal SGD | 0% | 0 / 78 | -- | -- | 0.372--0.374 |

Every crossed cell in the first three conditions eventually re-entered and every critical condition ended with route NMI 1.0. The experiment therefore identifies transient boundary fragility, not final specialization collapse.

### Figure 1: Early Crossing

![Early crossing rates](figures/early_cross_rates.png)

**Question:** Does removing coordinate-wise second-moment anisotropy or AdamW-specific direction remove early crossing?

**How to read:** Each bar is the fraction of non-common feature-seed cells crossing by step 50. The dashed line is the 0.25 reference-event prerequisite.

**Observed result:** Scalar-second-moment and raw-gradient norm-matched updates both retain frequent crossing. Nominal SGD removes it.

**Take-home:** Coordinate-wise second moments and AdamW-specific direction are not necessary; the large actual update scale remains the common factor.

**Limitation:** Nominal SGD changes update norm, so this figure does not identify a critical norm threshold.

### Figure 2: Margin Trajectories

![Margin trajectories](figures/margin_trajectories.png)

**Question:** How do same-norm directions change damage depth and recovery time?

**How to read:** The horizontal zero line is the matched routing boundary; curves are non-common-feature margin p05.

**Observed result:** Scalar-second-moment updates create the deepest and longest negative excursion. Raw-gradient norm-matched updates cross briefly and recover fastest. Nominal SGD remains positive.

**Take-home:** Scale controls whether crossing is reachable, while direction changes transient severity and correction speed.

**Limitation:** The trajectories diverge after the first intervention, so later direction comparisons are state-dependent.

### Figure 3: Boundary Pressure

![Cumulative negative router pressure](figures/boundary_pressure.png)

**Question:** Does the safe nominal-SGD condition reduce router movement against the matched boundary?

**How to read:** The population is the 78 cells that crossed under full AdamW. The bar is mean cumulative negative router projection through step 50.

**Observed result:** Nominal SGD reduces negative pressure from 0.5283 to 0.0703, an 86.69% reduction, and reproduces no reference events. Scalar second moment increases pressure by 36.92%; raw norm match reduces it by 25.68% but still reproduces 88.46% of events.

**Take-home:** Boundary pressure distinguishes the safe scale reference, but the step-50 cumulative value does not fully explain crossing/recovery under same-norm directions.

**Limitation:** Summing through step 50 includes post-crossing correction and competitor changes.

## Actual Update Scale

| Horizon | Full AdamW / nominal SGD | Scalar second moment / nominal SGD | Raw norm match / nominal SGD |
| ---: | ---: | ---: | ---: |
| first 10 steps | 6.65x | 6.65x | 6.61x |
| first 50 steps | 9.73x | 9.83x | 9.48x |

These are means of the actual router-update Frobenius norm over both critical regimes and 32 seeds. The scale contrast is measured, but no causal scale threshold has yet been estimated.

## Validity And Guards

- Completed: 32/32 seeds, 2,048 event rows, 28,672 trajectory rows, and 114,688 update-pressure rows.
- Manual full-AdamW versus PyTorch AdamW maximum parameter error: \(9.54\times10^{-7}\).
- Maximum scalar/raw norm-match relative error: \(2.30\times10^{-7}\).
- Maximum guard early-cross rate: 11.46%, below the registered 25% threshold.
- All guards ended with positive margins and route NMI 1.0.

## Hypothesis Update

| Hypothesis | Verdict | Evidence |
| --- | --- | --- |
| Coordinate-wise second moment is necessary | **Rejected** | Scalar-\(v\) removal is only 3.85%; reproduction is 96.15% |
| AdamW-specific direction is necessary | **Rejected** | Raw-gradient norm match reproduces 88.46% with a similar event rate |
| First-moment direction is sufficient but raw gradient is not | **Rejected** | Raw-gradient reproduction is high, not below 25% |
| Negative boundary pressure mediates the scale contrast | **Supported with boundary** | Nominal SGD reduces pressure 86.69% and removes crossing; same-norm recovery timing remains direction-dependent |

## Claim Boundary

The run shows that AdamW-specific coordinate and moment directions are not necessary for early crossing on this fixed-utility synthetic bridge. It does not prove that update norm alone determines every event, because task-gradient direction remains present and no controlled norm multiplier sweep has been run. It also does not establish natural-language specialization, learned-expert behavior, downstream utility, MTP benefit, or a deployable Router.

## Next Decision

Hold the router direction to the current raw gradient and sweep only a small set of update-norm multipliers relative to the full-AdamW candidate. Test whether crossing follows a margin-budget threshold before representation correction acts. The next method family is adaptive router step control only if this scale law is supported while LM progress remains intact.
