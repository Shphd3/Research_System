# A06_02_04_E01 Result Summary: Representation-Router-Optimizer Co-Dynamics

## Conclusion

On this controlled one-layer Transformer plus weighted top-1 MoE surface, the failure path is optimizer-conditioned.

1. **Under AdamW, router-row motion is necessary for early matched-margin crossing.** Joint training crossed in 78 of 192 non-common feature-seed cells (40.625%). Freezing the router removed all 78 events; freezing the representation removed none.
2. **Representation training is mainly corrective, not the initial damage source.** Every jointly trained AdamW cell that crossed returned to positive margin. In the paired router-only condition, 62 of those 78 re-entry events disappeared, giving a representation freeze-necessity fraction of 79.49% for re-entry.
3. **AdamW changes the event regime, not merely the final routing state.** At the same nominal learning rate, joint AdamW crossed 39.58 percentage points more often than joint SGD and crossed at median step 7 rather than step 516. Both optimizers nevertheless ended near fully specialized under joint training.

Therefore the next mechanism question is not whether a better static initialization exists. It is whether AdamW's coordinate-wise router preconditioning creates the early boundary pressure. That mechanism must be isolated before proposing a new router update.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it decides | Cannot prove |
| --- | --- | --- | --- | --- |
| Matched margin | Router-logit lead of the intended expert over a competitor | \(m_{f,a,b}=(w_a-w_b)^\top\mu_f\) | A nonpositive value means the initialized feature-expert binding has crossed a boundary | Expert usefulness on real text |
| First crossing | First update at which a matched margin becomes nonpositive | \(T_{cross}=\min\{t:m_f(t)\le0\}\) | Detects temporary or persistent binding failure | Irreversibility |
| Positive re-entry | First later update at which the crossed margin becomes positive again | \(T_{re}=\min\{t>T_{cross}:m_f(t)>0\}\) | Detects correction after failure | Recovery of downstream utility |
| Freeze-necessity fraction | Fraction of joint-training events removed by freezing one trainable path | \(N_k(E)=\Pr(E_{joint}=1,E_{freeze(k)}=0\mid E_{joint}=1)\) | Localizes a necessary path under paired seeds | Sufficiency or universality |
| Margin p05 | Fifth percentile of matched margins over non-common feature-seed cells | empirical 5th percentile, in router-logit units | Shows low-tail binding stability | Average routing quality |

The primary decision unit is one of features 1--3 under one seed. Each biased regime has \(32\times3=96\) units; the combined critical set has 192.

## Exact Setup

- Data: batches of 32 complete sequences, each with 33 repeated tokens and 32 next-token losses. `biased_s8` has 8 feature sequences and 24 class-0 background sequences; `biased_s4` has 4 feature sequences and 28 class-0 background sequences.
- Model: one causal attention layer, residual plus layer normalization, four weighted top-1 experts, no positional embedding.
- Utility control: fixed function-matched experts and fixed readout; expert \(f\) is useful for feature \(f\) at initialization.
- Interventions: router-only, representation-only, and joint training under plain SGD and AdamW.
- Run: 32 seeds, 1,000 updates, learning rate 0.002, four GPUs, full-position language-model loss.

## Primary Evidence

### Event And Freeze Results

| Optimizer / condition | Crossing rate | Median crossing step | Re-entry given crossing | Final margin p05 | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| Joint SGD | 1.04% | 516 | 50.0% across the two events | 0.072--0.086 | Too few joint events for path classification |
| Router-only SGD | 100% | 23.5--26.5 | 0--1.04% | -1.64 to -1.54 | Router updates alone destroy non-common bindings |
| Representation-only SGD | 0% | -- | -- | 0.368--0.371 | Representation motion alone stays safe |
| Joint AdamW | 40.625% | 7 | 100% | 0.136--0.138 | Early transient crossing followed by full correction |
| Router-only AdamW | 100% | 8 | 19.79--40.63% | -1.58 to -1.30 | Router motion reproduces crossing but usually not correction |
| Representation-only AdamW | 0% | -- | -- | 0.386--0.387 | Representation motion alone stays safe |

The combined AdamW freeze profile is:

| Event | Joint event cells | Freeze representation | Freeze router | Both single paths miss |
| --- | ---: | ---: | ---: | ---: |
| First crossing | 78 / 192 | 0.0% necessary | 100% necessary | 0.0% |
| Positive re-entry | 78 / 192 | 79.49% necessary | 100% event-level necessity | 79.49% |

For re-entry, the freeze-router number is not an isolated recovery-path estimate: representation-only cells never cross, so they cannot re-enter. The informative recovery contrast is joint versus router-only. It shows that allowing representation learning restores 62 of the 78 joint re-entry events that router updates alone do not reproduce.

### Figure 1: Margin Trajectories

![Matched-margin trajectories](figures/margin_trajectories.png)

**Question:** Which trainable path moves the low-tail matched margin across zero?

**How to read:** The horizontal zero line is the routing boundary. Each curve is the non-common-feature margin p05 across 32 seeds.

**Observed result:** Router-only training drives the margin deeply negative under both optimizers. Representation-only training remains positive. Joint SGD remains mostly positive; joint AdamW crosses early and then returns positive.

**Take-home:** Router-row motion is the damage channel, while trainable representation dynamics counteract it under joint training.

**Limitation:** The plot identifies trajectory shape, not the AdamW submechanism that accelerates the crossing.

### Figure 2: Crossing And Re-entry Rates

![Crossing and re-entry rates](figures/event_rates.png)

**Question:** Are the trajectory differences reproducible at the feature-seed event level?

**How to read:** Orange is the fraction that ever crosses; green is the fraction of crossed cells that later re-enters.

**Observed result:** Joint AdamW crosses in about 40% of non-common cells and all recover. Router-only conditions cross in every cell, but recovery is rare or partial. Representation-only conditions never cross.

**Take-home:** Final route quality hides a large optimizer-dependent transient event regime.

**Limitation:** A re-entry event requires a preceding crossing; it cannot identify recovery causality in a condition that never crosses.

### Figure 3: Causal Freeze Necessity Under AdamW

![AdamW freeze necessity](figures/paired_freeze_necessity.png)

**Question:** Which path is removed when the joint AdamW event disappears?

**How to read:** A value above the dashed 0.75 threshold satisfies the registered necessity rule. Only AdamW is shown because joint SGD did not reach the 0.25 event-rate prerequisite.

**Observed result:** Freezing the router removes every crossing. Freezing the representation does not remove crossing but removes 79.49% of joint re-entry events.

**Take-home:** Damage and correction use different parts of the trainable system.

**Limitation:** The re-entry statistic does not separate representation correction from an interaction with the already-moving router.

## Validity And Guards

- All 32 seeds and 2,048 feature-condition event rows completed.
- Exact finite-step margin decomposition maximum error: \(8.32\times10^{-7}\).
- Signal-plus-background raw-gradient closure maximum error: \(4.77\times10^{-7}\).
- Signal-only and task-solved orthogonal-background guards remained finally specialized with margin p05 above 1.75 under AdamW.
- Both AdamW guards had a 7.29% low-rate transient crossing, and every such cell immediately re-entered. This is below the registered 25% failure threshold but prevents a claim that AdamW transients require biased background in every seed.

## Hypothesis Update

| Hypothesis | Verdict | Evidence boundary |
| --- | --- | --- |
| Router or representation motion is necessary for crossing | **Supported for router motion under AdamW** | Joint AdamW event rate 40.625%; \(N_{router}(cross)=1\) and \(N_{representation}(cross)=0\) |
| Recovery uses the same path as crossing | **Weakened** | Router-only reproduces all crossings but misses 79.49% of joint re-entries |
| Optimizer changes the event regime | **Supported** | Crossing-rate gap 39.58 points; median event-time ratio 73.71 |
| SGD crossing-path classification | **Insufficient** | Joint SGD crosses only 2 of 192 cells |

## Claim Boundary

The experiment establishes a causal path classification only for fixed-utility experts, synthetic repeated-token full-LM data, one trainable attention layer, and the tested learning rate. It does not establish natural-language feature specialization, learned-expert co-adaptation, downstream interference reduction, or an MTP benefit. It also does not yet show whether AdamW's effect comes from coordinate-wise second moments, first-moment accumulation, weight decay, or effective step magnitude.

## Next Decision

Test whether **coordinate-wise second-moment normalization in the router optimizer** is necessary for the early AdamW crossing, while holding the representation optimizer and actual router-update norm under explicit controls. The decisive comparison is joint AdamW versus an isotropized-second-moment router update and a norm-matched SGD-router hybrid.

