# Protocol: A06_02_04_E01 Representation-Router-Optimizer Co-Dynamics

## 0. Approval Snapshot

**Approval status:** approved by the user's standing instruction to continue the specialization line with a definite anchor and execute the next full run.

**Purpose:** identify which trainable path is necessary for matched-margin first crossing and later re-entry under a neural full-sequence LM bridge.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_04_representation_router_optimizer_codynamics_anchor.md`

**Anchor decision question:** Does crossing/re-entry require router-row motion, representation motion, their joint coupling, or AdamW-conditioned transmission?

**Anchor physical prior tested:** $m_{f,a,b}(t)=(w_a(t)-w_b(t))^\top\mu_f(t)$ is jointly controlled by router and representation motion; optimizer preconditioning can change actual boundary-projected updates.

**Anchor core model term tested:** paired removal of $\Delta w$, $\Delta\mu$, or neither, with SGD/AdamW comparison.

**Anchor falsifier:** a claimed necessary path remains dispensable under paired freezing, or the full-joint reference never enters a decision-bearing event regime.

**Experiment role:** root-cause audit.

**Primary metric from anchor:** paired freeze-necessity fraction $N_k(E)$ for first crossing and conditional re-entry.

**Claim boundary from anchor:** controlled synthetic neural bridge with fixed experts/readout; no natural-language, MTP, learned-expert, downstream-utility, or router-method claim.

**Minimal setup:** a batch of 32 complete sequences with 32 next-token losses per sequence; four uniform features; one causal attention layer; four fixed function-matched experts; weighted top-1 routing; full-position cross-entropy.

**Basic configuration:** 32 seeds, 1,000 updates, four GPUs, exact event tracking each step, detailed diagnostics at 0/1/2/5/10/20/40/80/160/320/500/750/1000.

**Conditions to run:** critical class-0-biased background at 8/32 and 4/32 signal sequences under router-only, representation-only, and joint training for both SGD and AdamW; signal-only and solved orthogonal-background guards under joint SGD and joint AdamW.

**Pass:** at least one joint condition crosses in at least 25% of non-common feature-seed cells, and paired freezing or optimizer intervention yields a pre-registered necessary-path classification.

**Fail:** a proposed path is not necessary under the paired event rule, or solved-orthogonal/signal-only guards reproduce the biased-background failure.

**Insufficient:** step-0 routing/utility guard fails, fewer than 32 seeds complete, or no joint condition reaches the event regime.

**Cannot claim:** a deployable router, natural-language specialization, MTP benefit, or functional interference reduction.

**Approval decision:** proceed through smoke and remote four-GPU full run. Any smoke-driven implementation correction must be recorded before the full run and cannot change the decision question or primary metric.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Signal sequence | A full sequence whose every next-token target carries feature class $f$ | 33 repeated $F_f$ tokens, 32 losses | one of 32 batch sequences | Supplies matched expert utility | Natural-language feature |
| Biased common background | Full common-state sequence with class-0 next-token targets | 33 repeated $C_0$ tokens | batch sequences | Creates systematic expert-0 pressure | Real-text common operator |
| Solved orthogonal background | Full repeated-token sequences whose input/readout direction is orthogonal to the feature-router subspace and already predicted at step 0 | repeated neutral token $N$ | batch sequences | Holds background count fixed without persistent route pressure | Common-geometry control |
| Router-only | Representation frozen; router trainable | only $W$ requires gradients | condition | Isolates row motion | Full joint dynamics |
| Representation-only | Router frozen; upstream embedding/attention/norm trainable | only representation parameters require gradients | condition | Isolates center motion | Full joint dynamics |
| Joint | Representation and router train together | both parameter groups train | condition | Allows coupling | Expert learning |
| First crossing | First nonpositive matched margin | $T_{cross}$ | optimizer step | Failure event | Irreversibility |
| Re-entry | First positive margin after crossing | $T_{re}$ | optimizer step | Recovery event | Utility |
| Freeze-necessity fraction | Joint event disappears under a paired freeze | $N_k(E)$ | fraction | Primary causal statistic | General necessity outside this setup |
| Event-time ratio | Relative median crossing or re-entry time | $\operatorname{median}T_A/\operatorname{median}T_B$ | ratio | Optimizer time-scale effect | Cause of the ratio by itself |
| Margin p05 | Fifth percentile matched margin over feature-seed cells | low-tail router-logit gap | logit difference | Protects against averages hiding damaged features | Expert utility |
| Source gradient | Raw gradient from signal or background loss positions, weighted as in total loss | $g=g^{signal}+g^{background}$ | parameter gradient | Secondary mechanism evidence | AdamW-additive update attribution |

## 2. Anchor Alignment

**Decision question:** which trainable path is necessary for crossing and re-entry?

**Physical prior tested:** row and representation motion jointly determine margin; optimizer history can alter directional transmission.

**Core model term tested:** remove $\Delta w$ or $\Delta\mu$ by freezing, then compare with joint training.

**Falsifier:** an event remains unchanged when its claimed necessary path is frozen.

**Claim boundary:** fixed expert utility and synthetic token classes only.

## 3. Tested Hypotheses

For event $E$ and frozen path $k$:

$$
N_k(E)=\Pr(E_{joint}=1,E_{freeze(k)}=0\mid E_{joint}=1).
$$

1. **Crossing localization:** within each optimizer regime, label a path necessary only when the joint event rate is at least 0.25 and $N_k(cross)\ge0.75$.
2. **Recovery localization:** apply the same rule to re-entry among cells crossed in joint training.
3. **Optimizer regime change:** retain optimizer transmission when the paired event-rate gap is at least 0.25 or median event-time ratio is at least 2.

No event in joint training is an insufficient regime, not a negative causal result.

## 4. Rival Explanations

- Router-row motion alone causes all crossings and recoveries.
- Representation motion alone causes all crossings and recoveries.
- Neither path alone is sufficient; only joint feedback creates the event.
- AdamW, rather than the raw gradient, changes the effective boundary direction.
- Background count, rather than class-biased boundary pressure, explains the event.
- Step-0 expert utility or router binding is invalid, making later trajectories uninterpretable.

## 5. Data / Model / Algorithm / Objective

### 5.1 Data

Each training batch contains 32 complete sequences. Every sequence has 33 repeated tokens and 32 supervised next-token positions. Signal sequences are uniform over $f\in\{0,1,2,3\}$.

- `signal_only_s32`: 32 signal sequences, eight per feature; every sequence is 33 copies of $F_f$.
- `biased_s8`: eight signal sequences, two per feature, plus 24 sequences of repeated $C_0$.
- `biased_s4`: four signal sequences, one per feature, plus 28 sequences of repeated $C_0$.
- `solved_orthogonal_s4`: four signal sequences, one per feature, plus 28 repeated neutral-token sequences whose input/readout direction is orthogonal to feature class directions and already solved at step 0.

All class-biased common input ids share one trainable embedding parameter. The solved-background guard uses a separate router-orthogonal embedding/readout direction. There is no positional embedding. Every sequence uses the full 32-position LM loss; the signal fraction is controlled by sequence count, not by masking within a mixed sequence.

### 5.2 Model

- Input representation: feature-specific trainable embeddings plus one shared trainable common embedding.
- One causal multi-head self-attention layer, residual addition, and layer normalization.
- Router input: $h=\operatorname{LN}(X+A)$.
- Router: four linear rows, temperature 1.0, weighted top-1 dispatch.
- Experts: four fixed affine experts equivalent to expert-specific output vectors $\beta u_e$.
- Readout: fixed feature-class directions $u_f$ plus fixed token-type directions, so expert $e$ is locally useful for both $F_e$ and $C_e$ targets.
- Output: $y=h+p_r\beta u_r$, followed by the fixed readout.

Dimensions: $d=64$, four attention heads, four experts, expert strength $\beta=4$.

### 5.3 Initialization

For each seed, all conditions share one base model state. Router rows are initialized from step-0 signal-position feature centers and centered across experts. A single scalar rescales the rows so the step-0 low-tail matched margin equals 0.5. The fixed identity map $a(f)=f$ is used throughout.

Step-0 validity requires:

- every feature center selects expert $f$;
- every signal-position matched margin is positive;
- forcing expert $f$ gives lower signal loss than forcing any competitor for target $F_f$.

### 5.4 Objective And Source Partition

The training objective is the mean cross-entropy over all 32 next-token positions.

$$
L=\frac1{32}\sum_{t=1}^{32}\ell_t=L_{signal}+L_{background}.
$$

Signal and background raw gradients are computed with their original $1/32$ weighting so they add to the total raw gradient up to numerical tolerance.

### 5.5 Optimizers

- SGD: learning rate 0.002, no momentum, no weight decay.
- AdamW: learning rate 0.002, $\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$, weight decay $10^{-4}$.
- No gradient clipping in the primary run; non-finite values make a cell invalid.

The smoke may lower the common nominal learning rate only if non-finite values occur or the first five steps violate the step-0 validity contract. Such a change must apply to both optimizers and be recorded before full execution.

## 6. Conditions, Seeds, And Checkpoints

### 6.1 Condition Matrix

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `biased_s8/router_sgd` | row-only crossing/recovery | $\Delta w$ | single-path intervention | primary | reproduces joint event | does not | no joint event | event table |
| `biased_s8/repr_sgd` | representation-only crossing/recovery | $\Delta\mu$ | single-path intervention | primary | reproduces joint event | does not | no joint event | event table |
| `biased_s8/joint_sgd` | joint reference | row-center coupling | defines paired reference | primary | event regime | no event | event rate <0.25 | trajectory |
| `biased_s8/router_adamw`, `repr_adamw`, `joint_adamw` | optimizer-conditioned path | preconditioned row/center update | localizes AdamW events, not only their existence | primary | paired necessity resolved | unresolved | no joint event | event table |
| same six on `biased_s4` | signal/background ratio | stronger biased background | robustness near second threshold | primary | consistent localization | contradictory | invalid step0 | event table |
| `signal_only_s32/joint_{sgd,adamw}` | no-background guard | base dynamics | rejects generic instability | guard | safe | widespread crossing | non-finite | guard table |
| `solved_orthogonal_s4/joint_{sgd,adamw}` | equal-count solved-background guard | background count without route pressure | rejects count-only failure | guard | safe | same failure | step-0 unsolved | guard table |

### 6.2 Seeds And Execution

- Full seeds: 0--31.
- Four GPU shards: eight seeds per GPU.
- Updates: 1,000.
- Event metrics: evaluated every update.
- Detailed diagnostic checkpoints: 0, 1, 2, 5, 10, 20, 40, 80, 160, 320, 500, 750, 1000.
- Full result is valid only when every seed, data regime, and required training condition completes.

## 7. Primary Metric

The primary metric is the paired freeze-necessity profile:

$$
N_k(E)=\frac{\sum_i\mathbf1[E_i^{joint}=1\land E_i^{freeze(k)}=0]}{\sum_i\mathbf1[E_i^{joint}=1]}.
$$

The unit $i$ is one feature-seed cell. Feature 0 is reported separately because class-0-biased background may help it while harming features 1--3. The primary decision uses features 1--3.

This metric decides necessity on the tested surface. It does not prove that the path is sufficient or universal.

## 8. Secondary Metrics

- first-cross and re-entry step distributions;
- final positive-margin rate and final matched-route rate;
- final and trajectory margin p05;
- signal-position feature-route normalized mutual information;
- full-position LM loss and next-token accuracy by signal/background target type;
- exact row/representation/cross finite-step margin closure;
- $X/A/Q/h$ feature-center and common-center motion;
- raw signal/background router-gradient boundary projections;
- actual SGD/AdamW update boundary projection;
- Adam first and second moments for router rows.

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** step-0 identity routing and matched fixed-expert utility.

**Known bad:** an invalid expert/readout mapping can create clean geometry with wrong functional identity.

**Known confusing:** high route NMI can survive an expert-label permutation; first crossing can occur before full recovery; exact decomposition closure is not causal evidence; feature 0 can improve while features 1--3 fail.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| construction | Are signal/common counts exact? | token/target audit | exact 32-position partition | data audit table | detailed |
| step 0 | Are routing and utility matched? | forced-expert loss and margins | all guards pass | validity table | stop on fail |
| smoke | Is implementation finite and event logging complete? | one seed, 50 steps | all conditions produce expected files | smoke log | full submit |
| full trajectory | Do joint references cross/re-enter? | per-step event table | event rate criterion | trajectory table | causal analysis |
| attribution | Do row/center/cross and source gradients close? | checkpoint diagnostics | tolerance $10^{-5}$ | closure table | guard only |
| visualization | Which path changes the event? | paired event summary | direct mapping to anchor | central figures | summary |

## 11. Algorithm Specification

**Input:** seed, data regime, trainability condition, optimizer, 1,000 updates.

**Steps:**

1. Create fixed orthogonal class and type readout directions.
2. Initialize the shared neural base state for the seed.
3. Generate the 32-sequence batch for each data regime with exact signal/background counts.
4. Compute signal-position feature centers and initialize router rows to identity binding with margin p05 0.5.
5. Clone this exact state across all conditions.
6. Apply parameter freezing and optimizer selection.
7. Train on all 32 next-token losses.
8. At every step, evaluate pairwise matched margins on the fixed four-feature evaluation set and record crossing/re-entry.
9. At diagnostic checkpoints, record source centers, source gradients, actual updates, optimizer moments, LM metrics, and finite-step closure.
10. Aggregate paired feature-seed events across four GPU shards.

**Outputs:** raw per-step trajectories in the experiment workspace; curated event table, condition summary, closure table, central figures, `summary.md`, and `detailed.md` in the project experiment folder.

## 12. Success / Failure / Insufficient Evidence

**Supported path:** joint event rate $\ge0.25$ and paired necessity $\ge0.75$ for the named path, with guards passing.

**Coupling supported:** joint training produces the event while both single-path conditions fail to reproduce it in at least 0.75 of joint-event cells.

**Optimizer effect supported:** event-rate gap $\ge0.25$ or event-time ratio $\ge2$ under joint training, with signal-only and solved-orthogonal-background guards passing.

**Weakened:** single-path and joint profiles are similar, or AdamW and SGD profiles are close.

**Insufficient:** no joint event, failed step-0 guard, incomplete seeds, non-finite cells, or guard condition reproduces the same failure.

## 13. What This Cannot Claim

The run cannot claim natural-language MoE specialization, a useful downstream partition, learned expert utility, universal optimizer behavior, MTP routing benefit, or that a new router architecture is warranted before the causal path is localized.

## 14. Review Notes And Protocol Changes

- The anchor and protocol implement the next decision already stated in the canonical A06 story and the dated specialization meeting brief.
- The fixed affine experts intentionally preserve a known utility map. Trainable expert symmetry breaking is deferred so it cannot confound the representation-router causal audit.
- Smoke revision 1: the original within-sequence signal/common construction failed the balanced-background guard because causal attention carried the feature prefix into later common positions. The full protocol now mixes separate complete signal and common sequences in one batch, preserving full-sequence LM loss while making common input geometry identical across target classes.
- Smoke revision 2: the shared nominal learning rate was reduced from 0.01 to 0.002 because AdamW at 0.01 caused transient crossings in the signal-only guard. The new value matches the existing long-train neural bridge scale and is applied to both optimizers before the full run.
- Pilot revision 3: class-balanced targets on identical common inputs form an irreducible prediction conflict and produced persistent routing rotation. That condition is not a valid no-pressure guard in the trainable bridge. It is replaced by an equal-count, step-0-solved background in a router-orthogonal input/readout subspace. The earlier frozen common-balanced evidence remains valid for its own model.
- Pilot revision 4: router-only AdamW and representation-only AdamW were added because the pilot showed an optimizer-conditioned event regime. Without these freezes, the experiment could detect an AdamW/SGD difference but could not localize the path under AdamW.
- Alignment note: after revision 4 and before the full run, the same registered 0.25 event-rate and 0.75 necessity thresholds apply independently inside each optimizer regime. SGD remains the original reference; AdamW is classified only because its paired freeze matrix was added before full execution.
