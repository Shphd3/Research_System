# Protocol: A12_0_E03 Per-Sample Relational Graph

## 0. Approval Snapshot

- **Approval status:** Stage A approved by the user on 2026-07-15 with three seeds per experiment and one four-GPU reserved remote job. Stage B remains unapproved and prohibited.
- **Purpose:** replace the fixed finite truth table with a per-example regenerated short relation graph while preserving the one-step/two-step comparison and standard full-position language-model objectives.
- **Primary anchor:** [12_0 short-range single-step versus two-step composition](/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md).
- **Anchor decision question:** after NTP alone freezes data difficulty and the mastery threshold, is MTP's reduction in standard-head steps-to-threshold larger for two-step than for matched one-step examples?
- **Physical prior tested:** per-example regeneration removes fixed-map memorization; matched layout makes the objective-by-composition interaction more informative than a raw NTP/MTP difference.
- **Core model term:** $\Gamma_{d,s}(\tau)$, the two-step-minus-one-step difference in MTP's standard-head optimizer-step gain.
- **Falsifier:** both tasks are learnable under both objectives, but $\Gamma$ is non-positive, seed-unstable, or no larger than the evaluation resolution.
- **Experiment role:** workload operationalization and capability-gated objective comparison.
- **Primary metric:** optimizer steps for the common $q_1$ head to reach one frozen fresh-test answer-accuracy threshold.
- **Minimal setup:** fresh graph per example; two core fact slots; matched distractors; identical sequence layout across task depths; 1/2/4-layer causal Transformers; full-position NTP versus standard two-head $K=2$ MTP.
- **Stage A:** implement generator guards and run **NTP only** for data-difficulty and threshold calibration.
- **Stage B:** formal NTP/MTP confirmation on untouched seeds, blocked until Stage A produces a freeze record and the user explicitly approves it.
- **Pass:** at an eligible scale, the paired confirmation interaction satisfies the frozen positive-stability rule.
- **Fail / weakened:** both tasks are learnable, but no reproducible positive interaction is present.
- **Insufficient:** generator guards fail, no NTP-only difficulty setting is both learnable and non-saturated, no threshold can be frozen without MTP, trajectories are incomplete, or the formal capability gate fails.
- **Cannot claim:** explicit formation or causal use of $B$, wall-clock/FLOP efficiency, benefits beyond two short relation steps, or natural-language/code transfer.
- **Approved action:** implement the generator and run Stage A NTP-only difficulty/threshold calibration on four remote GPUs. Formal comparison remains prohibited.

### 0.1 Stage-A execution record

- **Submitted:** 2026-07-15 03:20 UTC
- **ACP job:** `pt-1uo5irqm`
- **Run name:** `a12_0_e03_stage_a_20260715_0322`
- **Allocation:** one `n6ls.iu.i40.4` worker, four NVIDIA N6LS 80 GB GPUs, `reserved` quota
- **Approved matrix:** 36 NTP-only trajectories; three seeds per condition (`1201--1203`)
- **Result directory:** `active/synthetic_data_understanding/results/a12_0_e03_stage_a_ntp_calibration/a12_0_e03_stage_a_20260715_0322`
- **Current state:** submitted and starting; no MTP trajectory is present in this job

All Stage-A numerical values below are frozen for this run. Stage-B execution still requires a second approval after the freeze amendment.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| graph instance | one self-contained local relation system | query, relation facts, aliases, order, and answer generated together | one sequence | answer must be computed from the current sample | symbolic algorithm use |
| graph fingerprint | content hash before serialization order is applied | hash of task depth, aliased query, unordered edge multiset, and answer | 256-bit digest | audits train/eval independence | absence of all semantic similarity |
| core fact | a fact occupying one of the two controlled non-distractor slots | single-step: one answer fact plus one matched control; two-step: two necessary chain facts | two slots | fixes fact count | two necessary facts in a genuine one-step computation |
| matched distractor | irrelevant edge with relation-frequency and serialization matched across tasks | equal counts using $r_1$ and $r_2$, with no ambiguous path from the query source | facts | increases relation selection difficulty without changing the answer | perfect equality of abstract task difficulty |
| fresh-test accuracy | answer correctness on fixed evaluation instances never used for training | $q_1(h_{\mathrm{SHARED}})$ top-1 accuracy over 8,192 test graphs | fraction | measures generalization to new graph instances | use of $B$ |
| difficulty freeze | irreversible selection made from NTP-only calibration | distractor count, sequence length, eligible scales, threshold, budget, and seed lists | configuration record | prevents MTP-driven task selection | correctness of the later mechanism interpretation |
| first-hit step | first recorded evaluation with accuracy at least $\tau$ | $T_{d,c,o,s}(\tau)$ | optimizer steps | primary speed outcome | sustained mastery by itself |
| capability gate | stable learnability prerequisite | final-window accuracy at or above frozen $\tau$ for all required conditions | pass / fail | prevents floor effects | causal composition mechanism |

## 2. Anchor Alignment

- **Decision question:** is the MTP step advantage larger for two-step fresh-graph composition than for one-step fresh-graph lookup?
- **Physical prior tested:** removing a fixed global map forces dependence on current facts; matching answer distance and serialization controls the simplest distance account.
- **Core model term tested:** paired $\Gamma_{d,s}(\tau)$ on confirmation seeds.
- **Falsifier:** eligible conditions show no reproducible positive $\Gamma$.
- **Claim boundary:** a pass supports only a structure-dependent optimizer-step interaction on this generated distribution.

## 3. Tested Hypothesis

For a frozen generator and threshold, standard $K=2$ MTP reduces the number of optimizer steps needed by the common next-token head more on two-step graphs than on matched one-step graphs.

The experiment does not assume this hypothesis is true. NTP-only calibration establishes only an eligible workload and metric; it cannot support the objective comparison.

## 4. Rival Explanations

1. **General auxiliary-loss effect:** the second head improves optimization similarly for both task depths.
2. **Full-position token prediction:** MTP may benefit from predicting grammar, aliases, or fact tokens rather than the final composition.
3. **Gradient dose:** MTP adds a second full-position loss and more backward computation even when parameter count is matched.
4. **Residual difficulty mismatch:** two-step examples require a join and may have different token-occurrence statistics despite matched length and fact count.
5. **Capacity boundary:** one scale may be too small or another may saturate too quickly.
6. **Threshold artifact:** a threshold chosen from MTP curves could manufacture the interaction; the staged freeze forbids this.
7. **Instance leakage:** repeated graphs, imbalanced aliases, or answer-frequency skew could recreate a memorization shortcut.

## 5. Data, Model, Algorithm, And Objective

### 5.1 Shared vocabulary and sequence grammar

**Frozen for Stage A:**

- node alias pool: 128 tokens, `N000`--`N127`;
- relation alias pool: 16 tokens, `R00`--`R15`;
- grammar tokens shared by both tasks: `BOS`, `DEPTH1`, `DEPTH2`, `QUERY`, `FACT`, `SEP`, `DECIDE`, `SHARED`, `EOS`;
- choose distinct query relation aliases $r_1\ne r_2$ per example;
- answer alias $Y$ is uniform over the 128 node tokens; fixed evaluation sets are exactly answer-balanced.

Serialization:

```text
[BOS, DEPTH_c, QUERY, A, r1, r2, SEP,
 FACT, u1, rel1, v1, SEP,
 ...,
 FACT, uk, relk, vk, SEP,
 DECIDE, SHARED, ANSWER_Y, EOS]
```

At fixed distractor count $D$, both tasks contain $k=2+D$ facts and have length

$$
L=21+5D.
$$

The final answer is always two positions after `DECIDE`. No intermediate state is emitted before the answer.

### 5.2 Per-example graph generation

For every paired instance key, independently:

1. draw a task depth $c$ supplied by the condition;
2. draw distinct relation aliases $r_1,r_2$;
3. draw all latent node roles without replacement, then apply a fresh random permutation into the shared node-token pool;
4. create the two core fact slots:
   - one-step: $(A,r_1,Y)$ plus a disconnected matched control $(U,r_2,V)$;
   - two-step: $(A,r_1,B)$ plus $(B,r_2,Y)$;
5. create an even number $D$ of distractors, with exactly $D/2$ using $r_1$ and $D/2$ using $r_2$;
6. require distractor endpoints to be decoy nodes and reject any distractor that creates another valid answer path or makes the query ambiguous;
7. uniformly shuffle all $2+D$ fact blocks;
8. serialize the sequence and emit only `ANSWER_Y` as the answer token.

The one-step condition has only one causally necessary answer fact. Its second core slot is a matched control. This is required to keep composition depth equal to one; calling both facts necessary would redefine the task.

The paired instance key fixes $A$, $Y$, $r_1$, $r_2$, decoy aliases, distractor facts, and the fact-slot permutation before the one-step or two-step core edges are inserted. Thus task depths are paired on superficial randomness while differing in the required join. `ANSWER_Y` denotes the sampled node alias $Y$, not a fixed answer-class token.

### 5.3 Split independence and shortcut guards

- Training examples are generated online from a training-only counter-based random stream.
- Validation and test each contain 8,192 fixed graphs from disjoint random streams.
- Graph content fingerprints must have zero overlap across train, validation, and test; collisions are rejected during generation and counts are stored in the manifest.
- Node aliases, relation aliases, answer aliases, and fact positions must be distribution-matched across task depths.
- An oracle graph executor must recover every answer exactly.
- Query-only and alias-frequency baselines must remain at the $1/128$ answer-chance level; the empirical upper guard is `0.012` accuracy on 8,192 balanced examples.
- Removing the first core fact must destroy answer identifiability in both tasks; removing the second core fact must do so only for two-step examples. These are generator semantics guards, not model results.

### 5.4 Model family

**Frozen for Stage A:** decoder-only pre-LN Transformers trained from scratch:

| Layers | Width | Attention heads | FFN width | Dropout | Role |
|---:|---:|---:|---:|---:|---|
| 1 | 128 | 4 | 512 | 0 | diagnostic capacity floor only |
| 2 | 128 | 4 | 512 | 0 | formal small scale |
| 4 | 128 | 4 | 512 | 0 | formal large scale |

All vocabulary, embeddings, positional encoding, context length, heads, and optimizer settings are identical across task and objective conditions at a given scale.

For each paired seed, NTP and MTP use identical backbone/head initialization and the identical counter-indexed training graph stream. One-step and two-step conditions use the same paired instance keys. Only task core-edge construction or objective loss coefficient changes.

### 5.5 Full-position objectives

Both NTP and MTP instantiate the same $q_1$ and $q_2$ prediction heads. Boundary positions without a target are masked.

$$
L_{\mathrm{NTP}}
=
\frac{1}{L-1}\sum_{t=1}^{L-1}
\operatorname{CE}\left(q_1(h_t),x_{t+1}\right),
$$

$$
L_{\mathrm{MTP}}
=
L_{\mathrm{NTP}}
+
\frac{1}{L-2}\sum_{t=1}^{L-2}
\operatorname{CE}\left(q_2(h_t),x_{t+2}\right).
$$

The second-head weight is exactly 1. Under NTP, $q_2$ is instantiated but its loss coefficient is zero. This matches parameter count, not backward FLOPs. The primary unit is optimizer steps; wall-clock time, examples, tokens, and measured compute must be reported separately and cannot replace the primary claim.

### 5.6 Independent variables and controls

| Role | Variable | Values / contract | Interpretation |
|---|---|---|---|
| primary independent variable | composition depth | one-step, two-step | changes whether answering requires an ordered join through $B$ |
| primary independent variable | objective | NTP, MTP with $K=2$ and weight 1 | changes whether the horizon-two loss is optimized |
| robustness variable | model depth | 2 and 4 formal; 1 diagnostic | tests scale locality, not a composition-depth sweep |
| Stage-A calibration variable | distractor count | proposed $D\in\{2,4,6\}$ under NTP only | selects one workload difficulty before MTP exists |
| held fixed in Stage B | data | generator code/hash, node/relation pools, $D^*$, fact count, answer balance, split instances | prevents objective-dependent data selection |
| held fixed in Stage B | sequence | vocabulary, token count, fact count/order distribution, answer position, output format | controls visible layout and answer distance |
| held fixed in Stage B | model/training | architecture at a given scale, initialization within paired seed, optimizer, schedule, batch, steps, data order | leaves objective coefficient as the intended change |
| held fixed in Stage B | decision rule | $\tau$, first-hit definition, capability window, seeds, aggregation rule | prevents post-hoc metric selection |

## 6. Conditions, Seeds, And Checkpoints

### 6.1 Proposed fixed training settings

All values in this table are frozen for Stage A.

| Setting | Proposed value |
|---|---:|
| optimizer | AdamW |
| learning-rate schedule | $10^{-3}$ to $10^{-4}$ cosine decay |
| warmup | 200 steps |
| betas | $(0.9,0.95)$ |
| weight decay | 0.01 |
| gradient clipping | 1.0 |
| batch size | 512 examples |
| precision | FP32 |
| maximum steps | 20,000 |
| evaluation interval | 100 steps |
| final stability window | steps 19,000--20,000, 11 evaluations |
| validation/test examples | 8,192 each |

### 6.2 Stage A — NTP-only difficulty calibration

- distractor candidates: $D\in\{2,4,6\}$, corresponding to sequence lengths 31, 41, and 51;
- formal scales used for selection: 2 and 4 layers;
- task depths: one and two;
- objective: NTP only;
- calibration seeds: 1201, 1202, 1203;
- maximum trajectories: $3\times2\times2\times3=36$;
- after $D^*$ is selected, one-layer NTP may run on the frozen setting as a diagnostic only and cannot alter $D^*$ or $\tau$.

**Difficulty eligibility:** a candidate $D$ is learnable only if, for every formal scale, task depth, and calibration seed, every final-window test accuracy is at least `0.95`.

**Non-saturation guard:** “sustained exact” means three consecutive evaluations at accuracy `1.0`. For each formal-scale/task group, fewer than two of the three seeds may have reached sustained exact accuracy by step 2,000. A candidate is rejected as too easy if the median seed in any of the four groups is already saturated by that step.

**Selection rule:** choose the largest $D$ satisfying both rules. If none qualifies, stop and return to workload design without running MTP.

### 6.3 Threshold selection from NTP only

**Frozen Stage-A threshold grid:**

$$
\tau\in\{0.80,0.90,0.95,0.99\}.
$$

After selecting $D^*$, choose the largest $\tau$ such that:

1. every formal NTP calibration trajectory reaches it by step 16,000;
2. every final-window evaluation remains at or above it;
3. within every formal-scale/task group, the median first-hit step is at least 2,000.

Exact `1.0` is excluded because E02 showed that an exact-only threshold can isolate a last-error tail rather than broad learning. This remains a metric boundary, not an established result for the new workload.

If no candidate threshold qualifies, stop. Do not inspect or generate MTP results.

### 6.4 Freeze and second approval gate

After Stage A, amend this protocol with:

- selected $D^*$ and resulting sequence length;
- selected $\tau$ and first-hit definition;
- NTP capability evidence for each formal scale and task;
- eligible formal scales;
- frozen generator manifest hash;
- frozen model, optimizer, budget, evaluation interval, and seeds;
- confirmation that no MTP calibration result exists.

Then stop. Formal Stage B requires explicit user approval of this freeze amendment.

### 6.5 Stage B — formal confirmation, currently prohibited

If separately approved:

- formal scales: frozen eligible subset of 2 and 4 layers;
- task depths: one and two;
- objectives: NTP and MTP;
- untouched confirmation seeds: 1301--1303;
- conditions per eligible scale: $2\times2\times3=12$;
- same generator, graph distribution, threshold, model, optimizer, examples per step, and budget as frozen after Stage A;
- within each seed, NTP/MTP share initialization and data order; one-step/two-step conditions share paired instance keys;
- no difficulty, threshold, checkpoint, or seed change after any MTP result is visible.

**Formal capability gate:** a model scale is eligible only if every task/objective/confirmation-seed trajectory remains at or above the frozen $\tau$ at all 11 final-window evaluations. An ineligible scale receives no $T/G/\Gamma$ mechanism interpretation. If neither formal scale is eligible, stop the comparison entirely.

### 6.6 Condition justification

| Item | Anchor clause tested | Rival explanation / guard | Why needed | Evidence | Pass | Fail | Insufficient | Planned artifact |
|---|---|---|---|---|---|---|---|---|
| graph generator audit | no fixed-map shortcut | leakage / repeated instances | validates the workload | primary guard | all audits pass | any shortcut | incomplete manifest | generator audit table |
| NTP distractor ladder | learnable, nontrivial carrier | floor / ceiling | selects difficulty without MTP | stage-primary | one frozen $D^*$ | none qualifies | incomplete curves | NTP learning curves |
| 1-layer diagnostic | capacity floor | memorization/easy carrier | descriptive only | secondary | recorded | not applicable | failed run | diagnostic curve appendix |
| 2/4-layer confirmation | structure-dependent speed | scale boundary | formal comparison | primary | positive stable $\Gamma$ | no stable positive $\Gamma$ | capability failure | paired interaction figure |
| $q_2$ answer accuracy | added target is learned | broken MTP implementation | implementation guard | secondary | learned under MTP | not learned | incomplete | head-accuracy table |

### 6.7 Stop conditions

1. Stop before training if any generator validity, answer-balance, oracle, or split-overlap guard fails.
2. Stop before any MTP run if no $D$ passes NTP learnability and non-saturation, or if no $\tau$ passes the NTP-only threshold rule.
3. Stop automatically after Stage A and wait for the user's second approval, even when the freeze rule succeeds.
4. Run each approved calibration or confirmation trajectory to the full budget; do not early-stop on the primary threshold.
5. At formal analysis, stop objective/composition interpretation for every scale that fails the capability gate; stop the entire comparison if both formal scales fail.
6. Treat incomplete trajectories, protocol drift, or infrastructure failure as insufficient evidence; do not replace missing conditions or change seeds without a protocol revision and approval.

## 7. Primary Metric

For each model scale $d$, task depth $c$, objective $o$, and seed $s$:

$$
T_{d,c,o,s}(\tau)
=
\min\{t:\operatorname{Acc}^{q_1}_{d,c,o,s}(t)\ge\tau\}.
$$

Then compute

$$
G_{d,c,s}(\tau)
=
T_{d,c,\mathrm{NTP},s}(\tau)
-T_{d,c,\mathrm{MTP},s}(\tau),
$$

$$
\Gamma_{d,s}(\tau)
=
G_{d,2,s}(\tau)-G_{d,1,s}(\tau).
$$

Positive $G$ means MTP reaches the same standard-head accuracy sooner. Positive $\Gamma$ means that advantage is larger for two-step than for one-step examples.

**Frozen seed count; Stage-B rule pending second approval:** a formal scale supports a positive interaction when all three seeds have $\Gamma_{d,s}>0$ and the median $\Gamma_d$ is at least one evaluation interval (`100` steps). Both formal scales meeting the rule is cross-scale support; only one meeting it is scale-local evidence.

**False-positive cost:** claiming composition-specific usefulness from a threshold or difficulty selected using MTP would invalidate the comparison. **False-negative cost:** the strict capability and sign-stability rules may reject a real but small or scale-local effect.

## 8. Secondary Metrics

- final-window and complete-trajectory $q_1$ fresh-test answer accuracy;
- three-consecutive-evaluation sustained threshold time, reported as a robustness metric rather than replacing first-hit time;
- $q_2$ answer accuracy at `DECIDE` under MTP as an implementation guard;
- full-position $q_1$ and $q_2$ losses separated by token type: grammar, node alias, relation alias, and final answer;
- format-token accuracy;
- examples processed, tokens processed, wall-clock time, and measured device utilization;
- answer-frequency, alias-frequency, fact-position, and graph-overlap audits.

No intermediate-state probe or intervention is part of E03. Readability and causal use of $B$ remain separate `12_03` questions.

## 9. Known Good, Known Bad, And Known Confusing Cases

- **Known good generator case:** an oracle follows $(A,r_1,Y)$ for one-step and $(A,r_1,B),(B,r_2,Y)$ for two-step and returns the serialized answer exactly after arbitrary aliasing and fact shuffling.
- **Known bad generator case:** removing the first core fact makes both tasks underdetermined; removing the second makes only two-step underdetermined.
- **Known bad learner case:** query-only or alias-frequency prediction remains at answer chance; the empirical guard is accuracy at most `0.012` on the 8,192-example balanced set.
- **Known confusing case:** MTP may lower full-position loss by predicting syntax while leaving standard-head answer learning unchanged; token-type losses must expose this.
- **Known confusing case:** one-step can saturate earlier than two-step even under a valid design. This is not itself an MTP effect; only the within-seed difference-in-differences $\Gamma$ is decision-bearing.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| graph construction | is each graph valid and uniquely answerable? | latent graph plus oracle trace | exact / invalid / missing | sampled serialized graphs and oracle traces | split manifest |
| alias/order randomization | is there a stable lexical or position shortcut? | token/fact distributions | balanced / leaked / insufficient sample | frequency and position tables | generator audit |
| split construction | are graph instances independent? | fingerprints | zero overlap / overlap / incomplete | overlap report | frozen manifest hash |
| NTP difficulty calibration | is the workload learnable but non-saturated? | complete $q_1$ curves | one $D^*$ / none / incomplete | per-scale learning curves | freeze amendment |
| threshold freeze | can one threshold be selected without MTP? | NTP-only crossing table | one $\tau$ / none / ambiguous | threshold eligibility table | second approval gate |
| formal capability | can every compared condition reach $\tau$? | final-window curves | eligible per scale / ineligible / incomplete | capability table | interaction only if eligible |
| formal interaction | is $\Gamma$ positive and stable? | paired first-hit steps | support / weakened / mixed | seed-paired interaction plot | anchor update |

## 11. Algorithm Specification

### 11.1 Generator

**Input:** paired instance key, task depth, distractor count, split key, sample counter, shared vocabulary specification.

**Parameters:** node pool 128, relation pool 16, even $D$, fixed grammar, answer position.

**Intermediate variables:** latent roles $A,B,Y,U,V$ and decoy nodes; relation aliases $r_1,r_2$; core edge list; distractor list; fact permutation; graph fingerprint.

**Procedure:** sample paired aliases and distractors without replacement; construct the task-specific core edges; reject ambiguity; apply the paired fact-slot permutation; verify with oracle; check split fingerprint; serialize.

**Outputs:** token sequence, answer position, task depth, latent oracle trace, graph fingerprint, audit metadata.

**Pass conditions:** one oracle answer; matched length/count; balanced distributions; no split overlap.

**Failure reasons:** alias exhaustion, ambiguous path, duplicate graph, answer imbalance, serialization mismatch, oracle disagreement.

**Debug artifacts:** representative one-step/two-step samples, rejected samples by reason, oracle traces, balance tables, overlap table.

### 11.2 NTP-only calibration

**Input:** generator candidates $D\in\{2,4,6\}$, formal scales, NTP objective, calibration seeds.

**Procedure:** run every approved NTP trajectory to the full budget; apply the learnability and non-saturation rules; choose the largest eligible $D$; apply the threshold-grid rule; write the freeze amendment.

**Pass:** exactly one $D^*$ and one $\tau$ are selected by the deterministic rules.

**Fail:** no $D$ or no $\tau$ qualifies.

**Forbidden action:** running, inspecting, or using MTP results before the freeze amendment is approved.

### 11.3 Formal confirmation

**Input:** approved freeze amendment and untouched confirmation seeds.

**Procedure:** run the frozen NTP/MTP matrix; apply the capability gate per scale; compute paired $T$, $G$, and $\Gamma$ only at eligible scales; apply the preregistered sign/median rule.

**Pass:** positive stable interaction under the frozen rule.

**Fail:** eligible conditions show no positive stable interaction.

**Insufficient:** capability, protocol compliance, or execution failure.

## 12. Success, Failure, And Insufficient-Evidence Outcomes

| Outcome | Operational result | Allowed conclusion | Prohibited conclusion |
|---|---|---|---|
| generator guard fails | leakage, overlap, imbalance, ambiguity, or oracle failure | E03 workload implementation is invalid | MTP or composition prior is false |
| NTP calibration fails | no $D$ is both learnable and non-saturated, or no $\tau$ qualifies | current model/workload pairing is not eligible | NTP/MTP mechanism comparison |
| formal capability fails at a scale | any required task/objective/seed lacks stable final-window mastery | no speed or mechanism interpretation at that scale | treating non-reach as slow convergence |
| both scales support | both meet the three-of-three and median rule | fresh-graph composition depth modulates MTP's optimizer-step benefit under this setup | causal use of $B$, general MTP superiority, compute efficiency |
| one scale supports | one eligible scale meets the rule, the other does not | scale-local structure-dependent interaction | scale-invariant mechanism |
| both tasks speed up similarly | positive $G$ but $\Gamma\approx0$ | general extra-supervision/distance accounts remain more consistent | composition-specific advantage |
| no positive or negative interaction | eligible scales have zero, unstable, or negative $\Gamma$ | $H_1$ is weakened for this workload | MTP never helps any task |
| $q_2$ learns but $q_1$ does not accelerate | future target is directly learned without standard-head speed benefit | formation is not sufficient for the primary behavioral benefit | causal explanation of non-use |

## 13. What This Cannot Claim

E03 cannot establish:

- that MTP forms an explicit, linearly decodable, or causally used intermediate state $B$;
- that a positive interaction grows monotonically beyond two composition steps;
- that optimizer-step efficiency equals token, FLOP, energy, or wall-clock efficiency;
- that full-position MTP's benefit comes specifically from the answer-position loss rather than its other horizon-two targets;
- that one-step and two-step tasks have identical intrinsic difficulty merely because their visible layout is matched;
- transfer to natural language, code, long contexts, or branching computation trees.

## 14. Review Notes And Approval Checklist

This draft supersedes E02 only as the **next operationalization**. It does not rewrite E02's completed protocol or result.

The following Stage-A choices are now frozen by the 2026-07-15 approval:

- two core slots, with the second one-step slot explicitly treated as a matched control rather than a necessary fact;
- node pool 128 and relation pool 16;
- distractor ladder $D\in\{2,4,6\}$;
- 8,192 validation and 8,192 test instances;
- model sizes and optimizer settings in Sections 5--6;
- NTP learnability threshold `0.95`, per-scale/task median early-saturation boundary at step 2,000, and latest eligible crossing step 16,000;
- query-only / alias-frequency empirical guard `0.012` on the balanced test set;
- threshold grid $\{0.80,0.90,0.95,0.99\}$ with exact `1.0` excluded;
- calibration seeds 1201--1203 and untouched confirmation seeds 1301--1305;
- confirmation seed count: three, reserved as 1301--1303;
- proposed Stage-B support rule for second approval: all three $\Gamma$ values positive and median at least 100 steps.

**Current authorization:** implement and run Stage A only, using four remote GPUs and calibration seeds 1201--1203. Stop after the NTP-only freeze amendment; Stage B needs a second explicit approval.
