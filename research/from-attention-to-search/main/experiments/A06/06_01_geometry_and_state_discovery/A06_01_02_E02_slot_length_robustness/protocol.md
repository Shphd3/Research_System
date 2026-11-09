# Protocol: A06_01_02_E02 Slot-Length Robustness Replay

## 0. Approval Snapshot

Approval status:
Approved by user on 2026-06-22. User requested `slot_token_len=2,4`, reproduction of the A06_01_01_E05-A06_01_03_E01 flow, and comparison of result / conclusion changes. The run keeps `slot_token_len=1` as the baseline.

Purpose:
Test whether the A06_01_01_E05-A06_01_03_E01 initialized router-geometry conclusions are robust to longer repeated slot spans.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question:
Do the A06_01_01_E05-A06_01_03_E01 conclusions remain stable when `slot_token_len` changes from `1` to `2` and `4`?

Anchor physical prior tested:
Longer slot spans may strengthen feature information at the routed slot position; if A06_01_03_E01 failed only because the one-token slot cue was too weak, label-free global controls may improve feature_NMI for longer slots.

Anchor core model term tested:
Compare raw score \(w_e^\top h\), common-centered score \(w_e^\top(h-c)\), residual / whitened score, oracle centroid score, and label-free controlled score \(w_e^\top\phi(h)\) across slot lengths.

Anchor falsifier:
If a label-free global control improves held-out feature_NMI by at least `+0.25` over baseline and closes at least `50%` of the oracle gap for `slot_token_len=2` or `4`, then A06_01_03_E01's negative result must be narrowed to the one-token slot boundary.

Experiment role:
Robustness / scaling check for the A06_01_01_E05-A06_01_03_E01 mechanism sequence.

Primary metric from anchor:
Held-out feature_NMI for A06_01_03_E01-style label-free controls, read together with load imbalance \(L\) and oracle-gap fraction.

Claim boundary from anchor:
Synthetic initialized hidden-state replay only; no training, real DCLM transfer, distributed slot-code claim, or expert utility claim.

Minimal setup:
Reuse the A06 synthetic generator and initialized Transformer-MoE replay. Run step-0 only. Set `slot_token_len in {1,2,4}`. Route at the last slot position, target immediately after the slot span.

Basic configuration:
Four uniform `(slot,target)` pair features, four experts, `seq_len=32`, random pair start, random background tokens independent of pair id, seeds `20260521..20260528`, depths `1,2,4`, readouts `post_ln` and `pre_ln_replay`, 4096 samples per pair for full.

Conditions to run:
A06_01_01_E05-style common/norm replay; A06_01_01_E06-style residual geometry replay; A06_01_02_E01-style oracle feature-centroid positive control; A06_01_03_E01-style label-free global common / residual controls.

Pass:
Current A06_01_03_E01 conclusion remains robust if no label-free global control passes the NMI gate at slot lengths `2` or `4`, while oracle centroid remains reachable.

Fail:
At least one label-free global control passes the NMI gate for long slots.

Insufficient:
Pair counts are not uniform, route position is wrong, target is not after slot span, calibration/evaluation split is unbalanced, label-free controls use `pair_id`, or oracle positive control fails due to implementation error.

Cannot claim:
Real DCLM behavior, trained routing stability, semantic specialization, distributed long slot codes, or failure of all label-free feature discovery methods.

Approval decision:
Approved and ready to run.

## 1. Anchor Alignment

Decision question:
Do the A06_01_01_E05-A06_01_03_E01 conclusions remain stable when slot length increases?

Physical prior tested:
Longer repeated slots may strengthen feature signal at the route position.

Core model term tested:
The score decompositions and controls from A06_01_01_E05-A06_01_03_E01, stratified by slot length.

Falsifier:
Long slots make simple label-free global controls recover the oracle feature partition.

Claim boundary:
Repeated-slot synthetic setting only.

## 2. Tested Hypotheses

H1:
Common-centering remains the main A06_01_01_E05-style load reduction across slot lengths.

H2:
Residual geometry remains after common-centering across slot lengths.

H3:
Oracle feature-centroid routing remains reachable across slot lengths.

H4:
Simple label-free global controls remain load controls rather than feature-specialization controls across slot lengths.

## 3. Rival Explanations

R1:
A06_01_03_E01 failed because the one-token slot signal was too weak.

Separated by:
`slot_token_len=2,4` A06_01_03_E01-style feature_NMI and oracle-gap fraction.

R2:
Longer slots only improve load, not feature routing.

Separated by:
feature_NMI versus load \(L\) and route heatmaps.

R3:
Any change is caused by position / target-placement artifacts rather than slot signal.

Separated by:
route-position audit, target-position audit, pair-start distribution, and pair count audit.

R4:
Oracle fails because the long-slot generator or extraction is wrong.

Separated by:
A06_01_02_E01-style oracle positive control and split audit.

## 4. Data / Model / Algorithm / Objective

Data:
Synthetic sequence length 32. Four pair ids. For each pair, `slot_token_len` copies of `SLOT_s` are placed at a random valid start, followed by `TARGET_s`. Background tokens are sampled independently from a disjoint background-token set.

Model:
Initialized Transformer-MoE replay, four experts, no training.

Algorithm:
Collect final-block router inputs at the last slot position. Run A06_01_01_E05-A06_01_03_E01-style score replays and controls.

Objective:
No training objective; this is a step-0 replay audit.

## 5. Conditions, Seeds, And Checkpoints

Full run:

- `slot_token_len in {1,2,4}`;
- seeds `20260521..20260528`;
- `num_layers in {1,2,4}`;
- `router_input_norm in {post_ln, pre_ln_replay}`;
- `samples_per_pair=4096`;
- `calibration_fraction=0.5`;
- step-0 only.

Smoke run:

- `slot_token_len in {1,4}`;
- seeds `20260521,20260522`;
- `num_layers=1`;
- `router_input_norm=post_ln`;
- `samples_per_pair=512`.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A06_01_01_E05 replay | H1 | common versus row norm | checks whether common dominance is stable | secondary | common remains main reduction | norm dominates | missing paired replay | `tables/a06_04_replay.csv` |
| A06_01_01_E06 residual | H2 | residual geometry after centering | checks whether residual geometry remains | secondary | centered residual load remains and controls reduce it | residual load vanishes | invalid whitening/isotropic control | `tables/a06_05_residual.csv` |
| A06_01_02_E01 oracle | H3 | oracle feature centroid | checks target reachability | guard / primary context | oracle NMI near 1 and load near 0 | oracle fails | split/leak issue | `tables/a06_06_oracle.csv` |
| A06_01_03_E01 label-free | H4 | label-free global controls | primary robustness test | primary | no label-free pass | long-slot label-free pass | label leakage | `tables/a06_07_label_free.csv` |
| audits | validity | generator / split / route position | protects the setting | guard | all pass | invalid construction | missing audit | `tables/*_audit.csv` |

## 6. Primary Metric

Primary metric:
Held-out feature_NMI for A06_01_03_E01-style label-free controls.

Why it decides:
The core claim at risk is whether simple label-free global controls fail because they do not discover feature partitions. Load \(L\) can improve without specialization, so feature_NMI decides the boundary.

Pass gate for a label-free control:

- feature_NMI improves by at least `+0.25` absolute over same-slot baseline raw router;
- oracle-gap fraction is at least `0.50`;
- label-free audit shows no pair-label use for control.

## 7. Secondary Metrics

- load imbalance \(L\);
- max load;
- active experts;
- load entropy;
- feature purity;
- dominant expert count;
- margin p05;
- oracle-gap fraction;
- route heatmap;
- removed variance fraction for projection;
- whitening effective rank and condition proxy.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
At `slot_token_len=1`, A06_01_02_E01 oracle feature centroid should reproduce feature_NMI near 1 and load near 0.

Known bad:
At `slot_token_len=1`, A06_01_03_E01 label-free controls should reproduce load-only improvement without passing the NMI gate.

Known confusing:
Repeated long slots may strengthen a repeated-token identity cue rather than a distributed slot code. This is acceptable for this robustness check but cannot be claimed as a distributed long-context slot result.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | Are pair counts and route positions valid? | generated batch metadata | uniform counts, valid start, last slot route | `tables/data_audit.csv` | detailed |
| split audit | Is calibration/eval balanced? | split counts | equal per pair | `tables/split_audit.csv` | detailed |
| replay audit | Were A06_01_01_E05-A06_01_03_E01 conditions computed for every slot length? | condition tables | complete grid | `tables/condition_audit.csv` | detailed |
| primary comparison | Does long slot change label-free NMI? | A06_01_03_E01-style table | gate pass/fail by slot length | `figures/a06_07_nmi_by_slot_len.png` | summary |
| load/NMI separation | Does load still separate from NMI? | load and oracle-gap table | load-only effect visible | `figures/a06_07_load_gap_by_slot_len.png` | summary |
| conclusion update | Does the story change? | all tables | stable / narrowed / ambiguous | `summary.md` | summary |

## 10. Algorithm Specification

input:
Base A06 synthetic config, slot lengths, seeds, layers, readouts, conditions.

parameters:
`slot_token_len`, `samples_per_pair`, `calibration_fraction`, `projection_rank`, `whitening_eps`.

intermediate variables:
hidden states \(h_i^{(l)}\), common means \(c^{(l)}\), residuals \(r_i^{(l)}\), covariance estimates, router scores, assignments, NMI, load, margin.

steps:

1. For each slot length, seed, and layer depth, generate a synthetic batch.
2. Extract router inputs at the last slot position for each readout.
3. Run A06_01_01_E05 common/norm replay.
4. Run A06_01_01_E06 residual geometry replay.
5. Split calibration/evaluation by pair id.
6. Run A06_01_02_E01 oracle centroid positive-control conditions.
7. Run A06_01_03_E01 label-free common / residual controls.
8. Aggregate by slot length, layer, readout, and condition.
9. Plot central comparisons.

outputs:
`summary.md`, `detailed.md`, tables, figures, run config.

debug artifacts:
data audit, split audit, projection audit, whitening audit, label-leakage audit, route heatmaps.

pass conditions:
No long-slot label-free condition passes the NMI gate while oracle remains reachable.

fail conditions:
Any long-slot label-free condition passes the NMI gate without label leakage.

failure reasons:
Short-slot artifact, route-position artifact, label leakage, invalid split, or changed geometry.

## 11. Success / Failure / Insufficient Evidence

Support robustness:
A06_01_01_E05-A06_01_03_E01 conclusions remain qualitatively stable for `slot_token_len=2,4`.

Weaken / narrow:
Long slots make label-free global controls recover feature_NMI.

Insufficient evidence:
Generator audit fails, oracle fails unexpectedly, or the full grid does not complete.

## 12. What This Cannot Claim

This protocol cannot claim:

- real DCLM behavior;
- training stability;
- semantic feature discovery;
- distributed multi-token slot codes;
- expert utility;
- failure of all label-free methods.

## 13. Review Notes And Protocol Changes

2026-06-22:
User approved `slot_token_len=2,4`, reproduction of A06_01_01_E05-A06_01_03_E01, and result/conclusion comparison. Baseline `slot_token_len=1` is retained for direct comparison.
