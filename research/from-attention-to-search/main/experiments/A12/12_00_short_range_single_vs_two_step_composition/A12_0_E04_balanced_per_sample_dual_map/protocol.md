# Protocol: A12_0_E04 Balanced Per-Sample Dual-Map Carrier

## 0. Approval Snapshot

- **Approval status:** the user approved the data construction and audit revision, then explicitly authorized Stage A on 2026-07-15. Stage A is complete; Stage B and every MTP run remain unauthorized.
- **Purpose:** replace E03's asymmetric direct-edge-versus-unique-chain carrier with a short paired carrier in which one-step and two-step examples share the exact same query and map contents.
- **Primary anchor:** [12_0 short-range single-step versus two-step composition](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
- **Anchor decision question:** after difficulty and the mastery threshold are frozen without MTP results, is MTP's standard-head learning-speed gain larger for two ordered map applications than for one?
- **Physical prior tested:** if the sample exposes two fresh local maps with balanced alias statistics, the only intended task difference is whether the answer requires one lookup or two ordered lookups.
- **Core model term:** future paired interaction \(\Gamma_d(\tau)\) in optimizer steps; E04 Stage A only determines whether this carrier and threshold are eligible.
- **Falsifier:** no formal scale can stably learn both task depths without an immediate ceiling, or a generator-aware query-hidden predictor reaches the frozen mastery threshold without the query.
- **Experiment role:** operationalization and capability-gate test.
- **Stage-A primary metric:** standard Next-1 head answer-accuracy trajectory on the fixed calibration set.
- **Future primary metric:** first optimizer step at which the same standard Next-1 head reaches a frozen threshold \(\tau\).
- **Minimal setup:** five active node aliases, two per-sample bijections, one fixed 31-token sequence, 2- and 4-layer formal models, NTP only, three seeds.
- **Pass:** every generator guard passes; at least one formal scale has both task depths and all three seeds at or above `0.95` throughout steps 19,000--20,000 without any task group reaching median sustained exact accuracy by step 2,000; an NTP-only threshold can be frozen.
- **Fail:** a shortcut guard passes above its allowed baseline, no scale/task/seed set passes capability, or every otherwise eligible group saturates too early.
- **Insufficient:** incomplete trajectories, implementation/protocol drift, missing artifacts, or infrastructure failure.
- **Cannot claim:** MTP benefit, causal use of the intermediate value \(B\), general composition, wall-clock efficiency, or transfer beyond this short synthetic carrier.
- **Approval decision:** Stage A NTP-only execution was authorized and completed. Stop after its result record; every MTP run requires a new explicit decision.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| active node set | the five node aliases used by one sample | \(S\subset\{N000,\ldots,N127\}\) with \(|S|=5\) | five aliases | keeps the sequence short while giving multiple lookup candidates | large-vocabulary reasoning |
| per-sample map | a fresh one-to-one mapping generated inside one example | bijections \(\pi_1:S\to S\) and \(\pi_2:S\to S\) | two maps | removes a fixed global truth table | use of a symbolic algorithm |
| task depth | number of ordered map applications needed for the answer | one-step: \(B=\pi_1(A)\); two-step: \(Y=\pi_2(\pi_1(A))\) | 1 or 2 | intended structural variable | prediction horizon |
| Next-1 target | the token immediately after the current position | \(q_1(h_t)\) predicts \(x_{t+1}\) | cross-entropy / accuracy | standard deployment head and common outcome surface | two-step task composition |
| Next-2 target | the token two positions after the current position | \(q_2(h_t)\) predicts \(x_{t+2}\) | cross-entropy / accuracy | adds earlier supervision, including the answer target at `DECIDE` | replacement of Next-1 |
| NTP objective | train only the standard Next-1 loss | \(L_{\mathrm{NTP}}=L_1\) | mean cross-entropy | baseline objective | absence of a second instantiated head |
| standard \(K=2\) MTP objective | retain Next-1 and add a second Next-2 head | \(L_{\mathrm{MTP}}=L_1+L_2\) with weight 1 | mean cross-entropy | intended future objective comparison | equal backward FLOPs or isolated answer-only supervision |
| standard-head answer accuracy | correctness of the common Next-1 head on the final answer | \(q_1(h_{\mathrm{SHARED}})\) top-1 equals the answer alias | fraction | decides task learning under both objectives | causal reliance on \(B\) |
| query-hidden predictor | must output an answer after seeing the maps and generator rules but not query \(A\) | enumerate generator-admissible queries under the observed maps and choose the highest-probability answer | accuracy | measures answer information leaked by generator constraints | whether the trained model uses the same shortcut |
| sustained exact | three consecutive evaluations with answer accuracy `1.0` | first step beginning such a three-checkpoint run | optimizer steps | detects an immediate ceiling | generalization beyond the generator |

**Critical distinction:** task depth and prediction horizon are independent. A one-step or two-step task may be trained with NTP or MTP. “Next-2” below always means an added horizon-two prediction target, not a two-step task and not a replacement for Next-1.

## 2. Anchor Alignment

- **Decision question:** can a short, fresh, statistically balanced carrier support a fair later comparison of NTP and standard \(K=2\) MTP on one versus two ordered map applications?
- **Physical prior tested:** identical per-sample maps and query tokens remove E03's query-free two-step topology shortcut and equalize the full-position token statistics outside the answer depth.
- **Core model term tested:** Stage A separately tests whether \(T_{d,c,\mathrm{NTP},s}(\tau)\) can be defined for each formal scale across both task depths and all three calibration seeds without a floor or immediate ceiling.
- **Falsifier:** the carrier remains shortcut-solvable, seed-unstable, unlearned, or too rapidly saturated.
- **Claim boundary:** passing Stage A supports only carrier eligibility. It does not adjudicate the MTP interaction.

## 3. Tested Hypothesis

**Stage-A hypothesis:** with both task depths sharing the same two local maps and query, 2- and 4-layer Transformers are qualified separately; at least one scale trained with full-position NTP can stably learn fresh one-step and two-step answers across seeds without any task group reaching median sustained exact accuracy by step 2,000.

**Future hypothesis, blocked:** after the carrier and threshold are frozen, standard \(K=2\) MTP reduces standard-head steps-to-threshold more for the two-step task than for the one-step task.

Stage A cannot support or weaken the future objective-interaction hypothesis. It only determines whether the comparison is valid to run.

## 4. Rival Explanations And Guards

1. **Alias or answer frequency:** a frequent active node predicts the answer. Guard by exact active-node occurrence balance and answer-balanced evaluation.
2. **Row position:** a fixed table row carries the answer. Guard by independent row permutations for both maps.
3. **Table position:** the first serialized table is always \(\pi_1\). Guard by random table-block order and explicit relation headers.
4. **Query omission:** table topology and generator rejection rules may narrow the answer without \(A\). Run and report a generator-aware query-hidden predictor; do not assume a fixed candidate-chance pass line. The carrier is ineligible if this predictor reaches the eventually frozen mastery threshold.
5. **Relation omission or wrong order:** the model ignores which map is first or second. Guard by map-header swaps, query-relation swaps, and rejection of instances where reverse composition equals the correct two-step answer.
6. **First-hop-only behavior:** the two-step model outputs \(B\) rather than \(Y\). Record the rate and probability mass assigned to \(B\) at the final answer position.
7. **Capacity floor:** 2 layers may not robustly implement row binding plus two lookups. Keep 2 and 4 layers as separate formal scales and do not average a failed scale into a passed scale.
8. **Immediate ceiling:** 4 layers may solve the carrier too early for a speed comparison. Apply the frozen non-saturation guard.
9. **General extra-loss or gradient-dose effect:** future MTP adds a full-position loss, not only answer supervision. A future interaction may remain structure-dependent but will not isolate an answer-only mechanism.

## 5. Data, Model, Algorithm, And Objective

### 5.1 Per-sample data algorithm

For each paired base instance:

1. Sample five distinct node aliases \(S\) from the 128-node vocabulary.
2. Sample distinct relation aliases \(r_1,r_2\) from the 16-relation vocabulary.
3. Sample a query alias \(A\in S\).
4. Sample independent random bijections \(\pi_1,\pi_2:S\to S\).
5. Compute \(B=\pi_1(A)\) and \(Y=\pi_2(B)\).
6. Reject and resample unless \(A\), \(B\), and \(Y\) are pairwise distinct.
7. Reject and resample if reverse composition \(\pi_1(\pi_2(A))\) equals \(Y\).
8. Independently shuffle the five key-value rows inside each map.
9. Randomly order the two table blocks; each block carries its relation header.
10. Create a paired one-step and two-step sequence from the exact same base instance and serialization randomness. Only `DEPTH` and the final answer differ.

Training instances are generated online. The Stage-A calibration set and the Stage-B final confirmation set each contain 8,192 fixed, base-instance-disjoint examples. For fixed evaluation sets, both one-step answer \(B\) and two-step answer \(Y\) must be exactly balanced over the 128 node aliases. The construction may schedule target aliases first and sample the remaining roles conditionally; it must not accept approximate balance. Stage A may inspect the calibration set, but the final confirmation set must remain sealed until the threshold, eligible scales, generator, and training settings are frozen.

The depth-free base fingerprint hashes \(A\), \(r_1\), \(r_2\), and the canonical content of \(\pi_1,\pi_2\). Paired task depths intentionally share this fingerprint. Online training, Stage-A calibration, and Stage-B final-confirmation base fingerprints must have zero overlap.

### 5.2 Fixed 31-token serialization

```text
[DEPTH_c, A, r1, r2,
 MAP, relation_header, key1, value1, ..., key5, value5,
 MAP, relation_header, key1, value1, ..., key5, value5,
 DECIDE, SHARED, ANSWER]
```

Length accounting:

\[
4 + (2+5\times2) + (2+5\times2) + 3 = 31.
\]

There is no emitted intermediate state. At `SHARED`, the standard Next-1 head predicts `ANSWER`. At `DECIDE`, the future Next-2 head predicts the same `ANSWER` two positions ahead.

### 5.3 Exact paired task targets

| Object | One-step task | Two-step task |
|---|---|---|
| input maps | identical \(\pi_1,\pi_2\) | identical \(\pi_1,\pi_2\) |
| query tokens | identical \(A,r_1,r_2\) | identical \(A,r_1,r_2\) |
| required computation | \(B=\pi_1(A)\) | \(B=\pi_1(A)\), then \(Y=\pi_2(B)\) |
| output token | \(B\) | \(Y\) |
| answer position | token 31 | token 31 |

Because each bijection contains every active alias exactly once as a key and once as a value, every active alias appears four times across the two tables. With pairwise-distinct \(A,B,Y\), the one-step and two-step sequences have the same alias-count multiset after the query and answer occurrences are included.

### 5.4 Concrete example

Let

```text
S = {N03, N17, N42, N58, N91}
r1 = R04
r2 = R11
A = N03
```

and

```text
R04: N03->N42, N17->N91, N42->N58, N58->N17, N91->N03
R11: N03->N58, N17->N03, N42->N91, N58->N42, N91->N17
```

Then \(B=N42\) and \(Y=N91\). The paired sequences share the same shuffled tables and query:

```text
DEPTH1 ... DECIDE SHARED N42
DEPTH2 ... DECIDE SHARED N91
```

### 5.5 Model family

| Layers | Width | Attention heads | FFN width | Dropout | Role |
|---:|---:|---:|---:|---:|---|
| 2 | 128 | 4 | 512 | 0 | formal small scale |
| 4 | 128 | 4 | 512 | 0 | formal large scale |

Use a decoder-only pre-LN Transformer trained from scratch with learned token and positional embeddings. Instantiate identical standard \(q_1\) and second \(q_2\) heads in every condition; tie \(q_1\) to the token embedding matrix and give \(q_2\) an independent vocabulary-projection matrix. Model structure and parameter count must be identical between NTP and MTP at a fixed scale; NTP instantiates \(q_2\) but does not include it in the loss.

A one-layer diagnostic is not part of the approved Stage-A matrix. It may be proposed later but cannot select the carrier or threshold.

### 5.6 Next-1 versus Next-2 objectives

The standard Next-1 loss is

\[
L_1=
\frac{1}{L-1}
\sum_{t=1}^{L-1}
\operatorname{CE}\left(q_1(h_t),x_{t+1}\right).
\]

The added Next-2 loss is

\[
L_2=
\frac{1}{L-2}
\sum_{t=1}^{L-2}
\operatorname{CE}\left(q_2(h_t),x_{t+2}\right).
\]

Objectives:

\[
L_{\mathrm{NTP}}=L_1,
\]

\[
L_{\mathrm{MTP}(K=2)}=L_1+L_2.
\]

| Current position | Next-1 target | Next-2 target |
|---|---|---|
| `DECIDE` | `SHARED` | `ANSWER` |
| `SHARED` | `ANSWER` | no in-range target |

Thus MTP retains the same standard answer loss at `SHARED` and adds a direct answer loss at the earlier `DECIDE` state. It also adds horizon-two supervision at all earlier valid positions, including map syntax and alias tokens. A future effect cannot automatically be attributed only to the answer target.

### 5.7 Training configuration

| Setting | Value |
|---|---:|
| objective in approved Stage A | NTP only |
| optimizer | AdamW |
| learning-rate schedule | \(10^{-3}\) to \(10^{-4}\) cosine |
| warmup | 200 steps |
| betas | \((0.9,0.95)\) |
| weight decay | 0.01 |
| gradient clipping | 1.0 |
| batch size | 512 examples |
| precision | FP32 |
| maximum steps | 20,000 |
| evaluation interval | 100 steps |
| final stability window | steps 19,000--20,000 |
| Stage-A calibration / Stage-B final confirmation | 8,192 fixed examples each, with disjoint base fingerprints |
| Stage-A seeds | 1201, 1202, 1203 |
| protected future seeds | 1301, 1302, 1303 |

These values were approved for Stage-A NTP-only execution on 2026-07-15. They do not authorize Stage B.

## 6. Conditions, Seeds, And Checkpoints

### 6.1 Executed Stage-A design surface

Stage A contains only:

\[
2\text{ scales}\times2\text{ task depths}\times3\text{ seeds}=12
\]

NTP trajectories. No MTP trajectory may be implemented or run in Stage A. Within one model scale and seed, the one-step and two-step runs share backbone/head initialization, base-instance order, and serialization randomness; only `DEPTH` and the final answer change.

| Item | Anchor clause tested | Rival explanation / model term | Why needed | Evidence role | Pass | Fail | Insufficient | Planned artifact |
|---|---|---|---|---|---|---|---|---|
| generator/oracle guards | fresh graph and query dependence | leakage or topology shortcut | validates the carrier | primary guard | exact guards pass and the query-hidden predictor remains below the frozen threshold | query-hidden predictor reaches the threshold or deterministic leakage exists | incomplete audit | generator audit table |
| 2-layer NTP, both depths, 3 seeds | small formal capability | capacity floor / seed instability | protects later speed interpretation | primary | every final window at this scale passes without early saturation | any seed at this scale fails or saturates early | incomplete run | learning curves and final table |
| 4-layer NTP, both depths, 3 seeds | large formal capability | capacity versus ceiling | checks robust learnability | primary | every final window at this scale passes without early saturation | any seed at this scale fails or saturates early | incomplete run | learning curves and final table |
| two-step first-hop error | ordered composition | outputting \(B\) instead of \(Y\) | localizes partial learning | secondary | declines as \(Y\) accuracy rises | persists after format learning | missing logits | error decomposition table |

### 6.2 NTP-only threshold freeze

If carrier capability passes, evaluate

\[
\tau\in\{0.80,0.90,0.95,0.99\}.
\]

First qualify 2 and 4 layers separately: a scale is eligible only if both task depths and all three seeds pass the final-window and non-saturation rules. At least one scale must qualify. Then choose the largest \(\tau\) such that every trajectory at every eligible scale reaches it by step 16,000, remains at or above it throughout the final window, each eligible-scale/task group has median first-hit step at least 2,000, and the generator-aware query-hidden predictor remains below it. Exact `1.0` is excluded from the primary threshold grid.

After Stage A, write the selected \(\tau\), eligible scales, generator hash, and complete freeze record, then stop for a second user decision.

### 6.3 Future Stage B, blocked

If separately approved, Stage B would compare NTP and standard \(K=2\) MTP on the frozen generator, threshold, eligible model scales, training settings, protected seeds, and sealed final-confirmation set. Within one scale and seed, the one-step/two-step and NTP/MTP conditions share backbone/head initialization and base-instance order. No Stage-B result may alter the carrier, threshold, scale set, seeds, or data.

## 7. Primary Metric

For Stage A, the deciding evidence is the complete calibration-set standard-head answer-accuracy trajectory. A scale passes capability only when every final-window checkpoint is at least `0.95` for both task depths and all three seeds; scales are adjudicated separately.

For a future approved objective comparison:

\[
T_{d,c,o,s}(\tau)=
\min\{t:\operatorname{Acc}^{q_1}_{d,c,o,s}(t)\ge\tau\},
\]

\[
G_{d,c,s}(\tau)=
T_{d,c,\mathrm{NTP},s}(\tau)-T_{d,c,\mathrm{MTP},s}(\tau),
\]

\[
\Gamma_{d,s}(\tau)=G_{d,2,s}(\tau)-G_{d,1,s}(\tau).
\]

Positive \(\Gamma\) means MTP's optimizer-step gain is larger on the two-step task. It does not prove that the network explicitly stores or causally uses \(B\).

Stage B is adjudicated separately at each eligible scale. All three protected seeds must have \(\Gamma_{d,s}(\tau)>0\) to support a stable positive interaction at that scale. Two positive and one non-positive seed is directionally unstable and insufficient. A non-positive median or larger one-step gain weakens \(H_1\). If any compared condition misses the frozen capability gate, interaction interpretation stops for that scale.

**False-positive cost:** admitting a shortcut-solvable, unlearned, or immediately saturated carrier can manufacture an objective interaction. **False-negative cost:** the strict all-seed gate may reject a real but unstable scale-local effect.

## 8. Secondary Metrics

- exact oracle accuracy and all corruption/removal guards;
- generator-aware query-hidden predictor accuracy, plus relation-swapped, table-header-hidden, frequency-only, and row-position baselines;
- final-answer probability and top-1 error rate for \(B\) versus \(Y\) on two-step examples;
- standard-format accuracy at `DECIDE`;
- full-position loss separated into grammar/header, key, value, and answer token classes;
- first-hit and three-consecutive-hit times for each threshold;
- examples, tokens, wall-clock time, and measured device utilization;
- seed-level curves, never only a seed mean.

No learned probe or hidden-state intervention is part of E04. Those remain downstream of a shared capability pass and belong to `12_03`.

## 9. Known Good, Known Bad, And Known Confusing Cases

### Known good

- A symbolic executor performs \(\pi_1(A)\) for one-step and \(\pi_2(\pi_1(A))\) for two-step with exact accuracy `1.0`.
- Swapping row order or table-block order leaves the oracle answer unchanged.
- Paired one-step and two-step examples have identical base fingerprints and identical serialized map/query tokens.

### Known bad

- Removing the \(A\mapsto B\) row from \(\pi_1\) makes both tasks unidentifiable.
- Removing the \(B\mapsto Y\) row from \(\pi_2\) makes only the two-step task unidentifiable.
- Replacing \(A\), swapping the relation order, or hiding headers requires reporting the corresponding controlled predictor accuracy; the query-hidden condition has no fixed candidate-chance pass line.
- Any accepted instance with \(A=B\), \(B=Y\), \(A=Y\), or reverse-composition equality violates the generator contract.

### Known confusing

- A model may learn table syntax and format while answer accuracy remains near the measured query-hidden prediction level.
- A two-step model may reliably output \(B\), showing first lookup without second lookup.
- A 4-layer model may learn correctly but too early for a useful steps-to-threshold comparison.
- A 2-layer model may be representationally capable but seed-unstable; Stage A records this as a capability failure rather than choosing the successful seed.

## 10. Stage-Level Profiling Plan And Possible Learning Path

The stages below are mechanistic hypotheses used to interpret behavioral errors. They are not established internal states and do not authorize probes.

| Stage | Possible learned operation | Behavioral evidence | Pass / fail / unclear rule | Handoff |
|---|---|---|---|---|
| grammar | recognize map headers, key-value alternation, `DECIDE`, and `SHARED` | format and token-class losses | format learned / not learned / mixed | row binding |
| row binding | bind each key to its adjacent value under the correct relation header | oracle corruptions and relation/header guards | required information affects output / ignored / unclear | first lookup |
| first lookup | retrieve \(B=\pi_1(A)\) | one-step accuracy and two-step \(B\) error | one-step learned / at chance / seed-unstable | second lookup |
| second lookup | use \(B\) as the key in \(\pi_2\) and retrieve \(Y\) | two-step \(Y\) accuracy versus \(B\) output rate | \(Y\) learned / first-hop-only / unclear | standard output |
| standard output | expose the selected alias to \(q_1\) at `SHARED` | common-head answer accuracy | stable / unstable / missing | capability decision |

A plausible depth allocation is: an early layer binds local key-value rows; a later layer retrieves \(B\); an additional layer uses \(B\) to retrieve \(Y\); a final layer stabilizes the answer for the standard head. This makes 2 layers a meaningful tight-capacity scale and 4 layers a more permissive scale, but it is not a theorem that one lookup consumes two layers or that two lookups require four.

## 11. Algorithm Specification

**Input:** base seed, split label, paired instance index, task depth, node/relation vocabularies, active-set size 5.

**Parameters:** 128 node aliases; 16 relation aliases; five active aliases; two bijections; sequence length 31; exact fixed-set answer balance.

**Intermediate variables:** \(S,r_1,r_2,A,\pi_1,\pi_2,B,Y\), row permutations, table-block permutation, depth-free base fingerprint.

**Procedure:**

1. Schedule or sample answer roles according to the split contract.
2. Construct a valid base instance under the distinctness and wrong-order rejection rules.
3. Serialize the two randomly ordered map blocks with shuffled rows.
4. Emit paired `DEPTH1`/answer-\(B\) and `DEPTH2`/answer-\(Y\) sequences.
5. Run the exact oracle, generator-aware query-hidden predictor, corruption, occurrence-count, balance, and fingerprint guards.
6. Reject the entire base pair if any guard fails.
7. Store fixed Stage-A calibration pairs and sealed Stage-B final-confirmation pairs; generate training pairs from a disjoint stream.

**Outputs:** paired tokens, \(A,B,Y\), both map tables, row/block permutations, fingerprint, guard results, and oracle/corruption predictions.

**Debug artifacts:** one human-readable paired example per split, occurrence-count table, baseline table, rejected-instance counts by reason, and split-overlap manifest.

**Pass conditions:** all exact guards satisfy the contract; query-hidden predictor accuracy is fully recorded and remains below the eventually frozen threshold; paired serialized inputs differ only at `DEPTH` and `ANSWER`.

**Fail conditions:** any shortcut exceeds its bound, any semantic corruption does not change identifiability as specified, occurrence multisets differ, or base fingerprints overlap across splits.

**Failure reasons:** generator bug, invalid balancing scheduler, relation/header leakage, row/block order leakage, reverse-order collision, split collision, or mismatched paired serialization.

## 12. Success, Failure, And Insufficient Evidence

### Stage-A success

- all generator guards pass;
- all 12 NTP trajectories complete;
- at least one formal scale has both task depths and all three seeds at or above `0.95` throughout the final window;
- no task group at an eligible scale has median sustained exact accuracy by step 2,000;
- at least one threshold in the frozen grid is eligible.

**Allowed conclusion:** this short balanced carrier, frozen threshold, and explicitly listed eligible scales qualify for a separately approved NTP/MTP confirmation; a failed scale cannot be averaged into the claim.

### Stage-A failure

- any generator shortcut or mismatch is present;
- no formal scale passes all required NTP capability conditions;
- every formal scale saturates too early;
- no threshold qualifies.

**Allowed conclusion:** this operationalization is not a valid carrier for the objective comparison. The result does not adjudicate MTP.

### Insufficient evidence

- incomplete or duplicated trajectories;
- seed, generator, model, or optimizer drift;
- missing curves, manifests, or guards;
- infrastructure failure.

## 13. What This Cannot Claim

Even after a future successful Stage B, E04 cannot by itself establish:

- that the network explicitly represents \(B\);
- that the standard head causally uses such a representation;
- that MTP is wall-clock or FLOP efficient;
- that the Next-2 answer target, rather than other full-position Next-2 targets or gradient dose, caused the effect;
- that more than two applications, longer contexts, natural language, code, or real pretrained models show the same behavior;
- that MTP is generally superior to NTP.

## 14. Review Notes And Protocol Changes

- **2026-07-15:** E04 created after the E03 carrier audit found an asymmetric query-free two-step topology shortcut and mismatched node-repetition statistics.
- **2026-07-15:** user approved the five-node, two-bijection, fixed-31-token data construction for Protocol documentation.
- **2026-07-15:** user removed a fixed candidate-chance query-hidden pass line and required an actual generator-aware query-hidden prediction; separated Stage-A calibration from Stage-B final confirmation; made 2/4-layer eligibility scale-local; required strict pairing across task depth and objective; and required all three protected-seed \(\Gamma\) values to be positive for stable support.
- E03 remains the evidence record for the rejected direct-edge-versus-unique-chain operationalization; E04 does not rewrite it post hoc.
- **2026-07-15:** the user explicitly authorized Stage A. Job `pt-9863fywz` completed all 12 NTP trajectories; no MTP condition was run. See [summary.md](summary.md) and [detailed.md](detailed.md).
- **2026-07-15 post-run audit:** the row-removal unidentifiability clauses in Sections 9 and 11 are false for a complete bijection: the fifth mapping value is recoverable from the other four rows. This approved design clause is preserved above as provenance and marked failed in the result records rather than silently rewritten.
- **Current authorization:** Stage A is closed. Stage B and all MTP runs are blocked because no scale passed capability and the row-removal guard failed.
