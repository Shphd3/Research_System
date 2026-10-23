派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/summary.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/summary.md)；研究修改仍回到原件。

---

# R05 facts: Candidate retention, residual allocation and expert bridges

1. Validity and fairness.
2. Learning and retention utility.
3. Mechanism and extrapolation boundaries.

Status: `EXECUTION_COMPLETE`. Endpoint aggregate snapshot: 2026-10-22T17:26:38.014649+00:00. Researcher scientific acceptance and closure are `Unknown`. This page reports actual R05 outputs only. Read the separate [AI preliminary interpretation](ai_interpretation.md) and [stage cards](judgment_cards.md) after the facts. The [round Anchor](../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/anchor.md) and [Protocol](protocol.md) own the model and frozen comparisons.

All165 tasks, 70/70 initial and19/19 R2 formal endpoints are complete:85 training trajectories and4 zero-update references. A/TS old accuracy is0/0/.5%, new100/99.875/98.625%; C dynamic is0% old/99.875% new. R2 ordinary full FFN reaches82.375% new with51% weakest cell, while its TRAIN accuracy is96.708%; all five D arms miss95% qualification. All eight natural-continuation endpoints have higher NLL than their own initial models. All four historical A15_24 replays match10340 positions exactly. A17 evidence conditions on one acquired parent, exposed DEV and a short budget. The four A15_24 checkpoint interventions have their separate historical identities. Scientific acceptance remains Unknown.

Ordinary qualification, all A/B orders and all C/D/E/F registered endpoints are saved, totaling86000 optimizer updates and1720000 prediction targets. Every complete list-mode readout has800 answers: two400-answer panels and200 answers per command/panel cell. Accuracy is full-vocabulary argmax, not a prediction renormalized within the three candidate words.

## Purpose and actual computation

The question is whether preserving selected parts of an acquired model helps old retention while it learns a reversed conditional rule, whether remaining updates benefit from mode allocation, and whether actual experts and routers can use the resulting structure. A candidate direction is a parameter selector, not an established common function.

The exact Qwen3-0.6B Base starts from E03's acquired AdamW1200 four-weight adapter. A/B/C modify final-attention Q/K/V/O, comprising6,291,456 native matrix elements; all other parameters freeze. An input has a visible mode, neutral command and three different words; its target is one answer token. Old mode selects first/last by command; new mode swaps the choice. Visible modes permit joint coexistence.

A fixes top16, tail16 or random16 orthogonal matrix atoms at initialization. It computes one actual Adam candidate displacement and attenuates its selected-direction part; raw-gradient scaling is not substituted. A sees new-mode labels only. B uses the same fixed selector with joint labels and shared/separate residuals under normal/protected candidate movement. Complete private residual copies add total capacity; row controls match total effective degrees while changing each mode's available space. These are separate matching conventions.

## Stage0: qualification and ordinary references

For4800 TRAIN and1600 DEV records, native/attention-cache logits differ by maximum0 and every argmax matches. The ordinary three-update Smoke and an external process replay of step1→2 match weights, Adam state, RNG, counters, data order and projectors exactly. A/TS and B/SP three-update Smokes have zero no-op error and exact external next-step replay. The FFN interface is separately checked: maximum logits errors0.0000314713 TRAIN and0.0000286102 DEV, with all argmax values equal. These qualify measurements/implementation, not method utility.

Ordinary A/U reaches100% new accuracy at1200; joint B/Full reaches99.625% old and99.750% new, with every relevant cell at least95%. The ordinary comparisons are reachable. A has only new labels; B receives ten old and ten new answers per update. Raw A/B scores do not compare architectures under matched supervision.

## A: frozen-endpoint observations

Every arm has1200 updates/24000 new answers and no old replay. U is ordinary; UL scales all movement by.1; US schedules all movement .1→.01; TC scales top-direction movement by.1; TS schedules top, RS random and LS tail movement while their complements retain the ordinary update. The qualification column covers the four new-mode cells.

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate |
|---|---:|---:|---:|---:|---:|---|
| LS | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| RS | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| TC | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| TS | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| U | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| UL | 29 | 1200 | 0.125% | 99.250% | 98.000% | PASS |
| US | 29 | 1200 | 1.500% | 98.125% | 96.000% | PASS |
| LS | 43 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| RS | 43 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| TC | 43 | 1200 | 0.125% | 99.875% | 99.500% | PASS |
| TS | 43 | 1200 | 0.000% | 99.875% | 99.500% | PASS |
| U | 43 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| UL | 43 | 1200 | 0.000% | 99.125% | 98.000% | PASS |
| US | 43 | 1200 | 0.875% | 98.250% | 95.500% | PASS |
| LS | 71 | 1200 | 2.375% | 98.500% | 96.000% | PASS |
| RS | 71 | 1200 | 1.125% | 98.125% | 94.500% | FAIL |
| TC | 71 | 1200 | 0.000% | 98.625% | 96.500% | PASS |
| TS | 71 | 1200 | 0.500% | 98.625% | 96.500% | PASS |
| U | 71 | 1200 | 0.875% | 98.625% | 95.500% | PASS |
| UL | 71 | 1200 | 0.875% | 97.750% | 94.000% | FAIL |
| US | 71 | 1200 | 4.500% | 93.375% | 85.500% | FAIL |

Here pp means percentage points. TS old accuracy across the three orders is0%,0%,0.500%; new accuracy is100%,99.875%,98.625%, with every TS new-cell gate passed. A qualifies18/21 arms: order71 UL/US/RS weakest new cells are94%/85.5%/94.5%, below95%. None of the three orders meets the registered conjunction of at least5pp TS old gain over every primary control and at most1pp new loss. Order71 US retains4.5% old but reaches only93.375% new; that retention alone is not qualified utility. All six contrasts per order follow; TC additionally isolates scheduling. The2000-draw unordered-group bootstrap is paired and panel-stratified, conditional on this parent/order rather than independent-model variation. Contrasts with failed controls remain descriptive.

| Order | TS minus control | Old accuracy delta pp [95% group interval] | New accuracy delta pp | Control acquisition |
|---|---|---:|---:|---|
| 29 | U | +0.000 [+0.000, +0.000] | +0.000 | PASS |
| 29 | UL | -0.125 [-0.375, +0.000] | +0.750 | PASS |
| 29 | US | -1.500 [-2.375, -0.750] | +1.875 | PASS |
| 29 | RS | +0.000 [+0.000, +0.000] | +0.000 | PASS |
| 29 | LS | +0.000 [+0.000, +0.000] | +0.000 | PASS |
| 29 | TC | +0.000 [+0.000, +0.000] | +0.000 | PASS |
| 43 | U | +0.000 [+0.000, +0.000] | -0.125 | PASS |
| 43 | UL | +0.000 [+0.000, +0.000] | +0.750 | PASS |
| 43 | US | -0.875 [-1.625, -0.250] | +1.625 | PASS |
| 43 | RS | +0.000 [+0.000, +0.000] | -0.125 | PASS |
| 43 | LS | +0.000 [+0.000, +0.000] | -0.125 | PASS |
| 43 | TC | -0.125 [-0.375, +0.000] | +0.000 | PASS |
| 71 | U | -0.375 [-1.125, +0.375] | +0.000 | PASS |
| 71 | UL | -0.375 [-1.125, +0.375] | +0.875 | FAIL |
| 71 | US | -4.000 [-5.500, -2.625] | +5.250 | FAIL |
| 71 | RS | -0.625 [-1.500, +0.128] | +0.500 | FAIL |
| 71 | LS | -1.875 [-3.125, -0.750] | +0.125 | PASS |
| 71 | TC | +0.500 [+0.125, +1.000] | +0.000 | PASS |

## B and subsequent coverage

Full is ordinary full-matrix joint training. SN/SP share full-complement residuals with normal/protected candidates; DN/DP use complete private residuals. SRN/SRP share both row spaces; RN/RP assign the two row spaces to modes. N/P mean normal/protected, not mode identity. Each complete arm has24000 total answers,12000/mode, and an eight-cell qualification test.

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate |
|---|---:|---:|---:|---:|---:|---|
| DN | 29 | 1200 | 100.000% | 100.000% | 100.000% | PASS |
| DP | 29 | 1200 | 100.000% | 100.000% | 100.000% | PASS |
| Full | 29 | 1200 | 99.625% | 99.750% | 99.500% | PASS |
| RN | 29 | 1200 | 100.000% | 99.875% | 99.500% | PASS |
| RP | 29 | 1200 | 100.000% | 99.250% | 98.000% | PASS |
| SN | 29 | 1200 | 99.750% | 99.375% | 98.500% | PASS |
| SP | 29 | 1200 | 98.250% | 98.625% | 95.500% | PASS |
| SRN | 29 | 1200 | 99.750% | 99.375% | 99.000% | PASS |
| SRP | 29 | 1200 | 100.000% | 99.875% | 99.500% | PASS |
| DN | 43 | 1200 | 100.000% | 99.875% | 99.500% | PASS |
| DP | 43 | 1200 | 100.000% | 98.625% | 98.000% | PASS |
| Full | 43 | 1200 | 99.375% | 100.000% | 98.000% | PASS |
| RN | 43 | 1200 | 100.000% | 97.750% | 93.000% | FAIL |
| RP | 43 | 1200 | 100.000% | 97.500% | 92.500% | FAIL |
| SN | 43 | 1200 | 99.750% | 99.500% | 99.000% | PASS |
| SP | 43 | 1200 | 100.000% | 99.250% | 97.500% | PASS |
| SRN | 43 | 1200 | 100.000% | 99.750% | 99.000% | PASS |
| SRP | 43 | 1200 | 100.000% | 100.000% | 100.000% | PASS |
| DN | 71 | 1200 | 100.000% | 100.000% | 100.000% | PASS |
| DP | 71 | 1200 | 100.000% | 100.000% | 100.000% | PASS |
| Full | 71 | 1200 | 99.750% | 98.250% | 95.000% | PASS |
| RN | 71 | 1200 | 100.000% | 95.000% | 85.500% | FAIL |
| RP | 71 | 1200 | 100.000% | 92.000% | 74.000% | FAIL |
| SN | 71 | 1200 | 99.250% | 95.000% | 85.500% | FAIL |
| SP | 71 | 1200 | 99.375% | 93.125% | 82.500% | FAIL |
| SRN | 71 | 1200 | 99.750% | 95.500% | 86.000% | FAIL |
| SRP | 71 | 1200 | 99.625% | 96.250% | 88.500% | FAIL |

Utility uses the weaker-mode mean, min(old accuracy,new accuracy), while qualification separately checks all eight cells. Positive differences favor the left arm; no post-outcome effect threshold is added. Failed row-arm prerequisites leave descriptive differences only.

| Order | Contrast | Weaker-mode mean difference(pp) | Both-arm qualification |
|---|---|---:|---|
| 29 | DP−SP | +1.750 | PASS |
| 29 | DN−SN | +0.625 | PASS |
| 29 | SP−SN | -1.125 | PASS |
| 29 | DP−DN | +0.000 | PASS |
| 29 | RN−SRN | +0.500 | PASS |
| 29 | RP−SRP | -0.625 | PASS |
| 29 | (DP−DN)−(SP−SN) | +1.125 | PASS |
| 43 | DP−SP | -0.625 | PASS |
| 43 | DN−SN | +0.375 | PASS |
| 43 | SP−SN | -0.250 | PASS |
| 43 | DP−DN | -1.250 | PASS |
| 43 | RN−SRN | -2.000 | FAIL prerequisite |
| 43 | RP−SRP | -2.500 | FAIL prerequisite |
| 43 | (DP−DN)−(SP−SN) | -1.000 | PASS |
| 71 | DP−SP | +6.875 | FAIL prerequisite |
| 71 | DN−SN | +5.000 | FAIL prerequisite |
| 71 | SP−SN | -1.875 | FAIL prerequisite |
| 71 | DP−DN | +0.000 | PASS |
| 71 | RN−SRN | -0.500 | FAIL prerequisite |
| 71 | RP−SRP | -4.250 | FAIL prerequisite |
| 71 | (DP−DN)−(SP−SN) | +1.875 | FAIL prerequisite |

The next table separates measured engineering checks, execution, learning qualification and AI judgments. Checks cover their named family/version, with missing scope in the audits. A/B stage FAIL includes some failed controls rather than every arm; E FAIL is the expert prerequisite. Mechanism judgments remain on the separate AI page.

| Stage | Implementation evidence | Execution | Learning qualification | AI hypothesis judgment |
|---|---|---|---|---|
| 0 | cache/ordinary external replay; CHECKED_WITH_BOUNDARIES | COMPLETE | PASS | separate AI page; researcher acceptance Unknown |
| A | actual-Adam CPU boundaries; no-op/external replay; CHECKED_WITH_BOUNDARIES | COMPLETE (21/21) | MIXED 18/21; TS 3/3 PASS | separate AI page; researcher acceptance Unknown |
| B | row Gram/DOF; no-op/external replay; CHECKED_WITH_BOUNDARIES | COMPLETE (27/27) | MIXED 19/27 PASS | separate AI page; researcher acceptance Unknown |
| C | 400/800 weight/logit conservation; no dedicated C replay; CHECKED_WITH_BOUNDARIES | COMPLETE (3/3) | PASS | separate AI page; researcher acceptance Unknown |
| D | FFN cache/representative external replay; CHECKED_WITH_BOUNDARIES | COMPLETE (5/5) | FAIL | separate AI page; researcher acceptance Unknown |
| E | fixed/joint representative external replay; CHECKED_WITH_BOUNDARIES | COMPLETE (10/10) | expert prerequisite: FAIL | separate AI page; researcher acceptance Unknown |
| F | natural cache/dense external replay; CHECKED_WITH_BOUNDARIES | COMPLETE (4/4) | NOT_APPLICABLE | separate AI page; researcher acceptance Unknown |

All registered C/D/E/F endpoints remain in their respective stage directories. C uses no DEV direction selection. D separately qualifies the FFN carrier. E distinguishes fixed experts from joint learning and discloses full-input versus16-dimensional router capacity. F requires natural text rather than another synthetic seed. Its saved split has128 training and64 validation documents,127 prediction positions/document and disjoint text/window hashes; Base pretraining exposure remains unknown.



## Saved C/D/E/F endpoints

All registered endpoints appear here. D/E natural readouts measure collateral list-training behavior, not extra natural training. Since natural text has no mode label, known-mode D and E-oracle use an equal-probability predictive mixture, while learned routers use their actual selections; these inference rules differ. Failed D learning qualification is not an architecture/router-mechanism verdict. The95% list gate does not apply to natural NTP. F NLL is separate, while its list accuracies describe retained behavior.

### C

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate |
|---|---:|---:|---:|---:|---:|---|
| dynamic | 29 | 1200 | 0.000% | 99.875% | 99.500% | PASS |
| fixed | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |
| sham | 29 | 1200 | 0.000% | 100.000% | 100.000% | PASS |

### D

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate | Natural NLL |
|---|---:|---:|---:|---:|---:|---|---:|
| multi_normal | 29 | 1200 | 100.000% | 74.000% | 59.000% | FAIL | 2.696469 |
| multi_protected | 29 | 1200 | 100.000% | 74.000% | 59.000% | FAIL | 2.696100 |
| ordinary | 29 | 1200 | 100.000% | 74.125% | 59.000% | FAIL | 2.704869 |
| single_normal | 29 | 1200 | 85.500% | 43.250% | 26.000% | FAIL | 2.952694 |
| single_protected | 29 | 1200 | 85.500% | 43.250% | 26.000% | FAIL | 2.953398 |

### E

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate | Natural NLL |
|---|---:|---:|---:|---:|---:|---|---:|
| full/fixed | 29 | 600 | 99.625% | 71.250% | 56.500% | FAIL | 2.863950 |
| full/joint | 29 | 600 | 99.375% | 77.125% | 54.500% | FAIL | 2.777812 |
| oracle/fixed | 29 | 0 | 100.000% | 74.000% | 59.000% | FAIL | 2.696469 |
| oracle/joint | 29 | 600 | 100.000% | 79.625% | 58.000% | FAIL | 2.690085 |
| random/fixed | 29 | 0 | 57.125% | 39.000% | 30.000% | FAIL | 2.911503 |
| random/joint | 29 | 600 | 81.875% | 32.250% | 18.000% | FAIL | 2.973537 |
| random_summary/fixed | 29 | 600 | 16.250% | 72.625% | 14.000% | FAIL | 3.140316 |
| random_summary/joint | 29 | 600 | 81.125% | 43.000% | 21.000% | FAIL | 3.172406 |
| summary/fixed | 29 | 600 | 98.250% | 7.375% | 4.500% | FAIL | 3.170452 |
| summary/joint | 29 | 600 | 84.125% | 45.375% | 21.000% | FAIL | 3.187713 |

### F

| Condition | Order | Updates | Old accuracy | New accuracy | Weakest eligible cell | Learning gate |
|---|---:|---:|---:|---:|---:|---|
| dense_normal | 29 | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE |
| dense_protected | 29 | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE |
| ordinary2 | 29 | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE |
| shared2_protected | 29 | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE |


Real C reselection does change the selected geometry. Project the16 orthonormal current matrix atoms into the initial16-atom span and average squared projection norms. This overlap is0–1;1 means identical subspaces, not functional retention. Checkpoint600 contains the400-update switch and1200 the800-update switch.

| Saved update | Q overlap | K overlap | V overlap | O overlap |
|---|---:|---:|---:|---:|
| 600 | 0.761678 | 0.953217 | 0.648963 | 0.694163 |
| 1200 | 0.635394 | 0.843589 | 0.420907 | 0.460163 |

Switching preserves weight bytes and gives logits error0. Geometry changes without endpoint old-retention improvement do not identify common-function change. [Source](../../../../../../../../../UNAVAILABLE.md).
| Condition | Order | Validation positions | Initial NLL | Endpoint NLL | Endpoint−initial |
|---|---:|---:|---:|---:|---:|
| dense_normal | 29 | 8128 | 2.619969 | 2.631744 | +0.011775 |
| dense_protected | 29 | 8128 | 2.619969 | 2.630957 | +0.010988 |
| ordinary2 | 29 | 8128 | 2.619969 | 2.657658 | +0.037689 |
| shared2_protected | 29 | 8128 | 2.619969 | 2.656988 | +0.037019 |



## One qualification repair R2: Separate from R1

R1 trains only down projections and all five D arms fail. The [full-FFN repair](protocol_ffn_repair_v2.md) was registered at2026-10-22 16:41:48 UTC before its outcomes: train native gate/up/down with independently fixed top16 projectors; full-router input becomes x1024 with a64-unit hidden layer common to every router, while candidate/random summaries remain16-dimensional. All affected D/E/F controls rerun; A/B/C stay unchanged. Parameterization and capacity change, so no particular extra matrix is identified as necessary.

R2 identity is R05_FFN_qualification_repair_V2 under `runs/repair_full_ffn`. Initial D/E/F remain R1 failures/diagnostics; endpoints are never pooled or selected for appearance.

| R2 stage | Execution | Learning qualification |
|---|---|---|
| D | COMPLETE | FAIL |
| E | COMPLETE | FAIL |
| F | COMPLETE | NOT_APPLICABLE |

### R2 D

| Condition | Updates | Old accuracy | New accuracy | Weakest cell | Qualification | Natural NLL |
|---|---:|---:|---:|---:|---|---:|
| multi_normal | 1200 | 100.000% | 83.125% | 54.000% | FAIL | 2.710800 |
| multi_protected | 1200 | 100.000% | 84.500% | 58.000% | FAIL | 2.707394 |
| ordinary | 1200 | 100.000% | 82.375% | 51.000% | FAIL | 2.621951 |
| single_normal | 1200 | 96.000% | 77.875% | 46.500% | FAIL | 2.776462 |
| single_protected | 1200 | 97.125% | 78.000% | 45.000% | FAIL | 2.778127 |

### R2 E

| Condition | Updates | Old accuracy | New accuracy | Weakest cell | Qualification | Natural NLL |
|---|---:|---:|---:|---:|---|---:|
| full/fixed | 600 | 99.625% | 29.750% | 15.000% | FAIL | 2.739514 |
| full/joint | 600 | 98.375% | 84.250% | 52.000% | FAIL | 2.718541 |
| oracle/fixed | 0 | 100.000% | 83.125% | 54.000% | FAIL | 2.710800 |
| oracle/joint | 600 | 100.000% | 83.875% | 53.500% | FAIL | 2.760454 |
| random/fixed | 0 | 52.000% | 43.000% | 27.500% | FAIL | 2.747239 |
| random/joint | 600 | 93.375% | 65.125% | 37.000% | FAIL | 2.737204 |
| random_summary/fixed | 600 | 26.500% | 76.000% | 12.000% | FAIL | 2.746046 |
| random_summary/joint | 600 | 96.500% | 79.250% | 47.000% | FAIL | 2.792758 |
| summary/fixed | 600 | 100.000% | 0.000% | 0.000% | FAIL | 2.741471 |
| summary/joint | 600 | 97.750% | 82.125% | 52.500% | FAIL | 2.869599 |

### R2 F

| Condition | Updates | Old accuracy | New accuracy | Weakest cell | Qualification | Natural NLL |
|---|---:|---:|---:|---:|---|---:|
| dense_normal | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE | 2.685319 |
| dense_protected | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE | 2.685412 |
| ordinary2 | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE | 2.692302 |
| shared2_protected | 400 | 100.000% | 0.000% | N/A | NOT_APPLICABLE | 2.732653 |

A completed R2 endpoint below95% remains acquisition failure; E is then an unqualified-expert diagnostic. The zero-update single-expert natural-readout IndexError is preserved and repaired separately, not counted as failed learning. All endpoints are complete, with no second scientific configuration repair.


## F: Matched historical A15_24 functional replay

All four T_F/T_H seed11/22 models replay10340 DEV positions on H10080 exactly against saved actual-route and Base NLL; all errors are0. The old technical blocker is resolved and old failures are preserved. Expert a is the non-high-frequency expert called by both F/H; b is F’s original partner and c is H’s forced high-frequency partner. If F already selected the high group,b=c. Base remains present, each expert coefficient is.5 and all six branches use fixed weights. B1 means positions with at least one originally lowest-frequency feature active, not an equal-feature macro metric.

Each table reports the within-condition equal mean of two saved seeds in nat/prediction position. Negative differences favor the stated addition/replacement. Brackets are95% example intervals from2000 paired whole-dialogue draws(seed20261023); models are fixed, so these are not model-population intervals.

### all_B1_1701: 1701 positions, 124 dialogues

| Intervention | T_F fixed-seed mean [95% interval] | T_H fixed-seed mean [95% interval] |
|---|---:|---:|
| Add high-frequency c given a | +0.000687 [-0.004132, +0.005126] | +0.000804 [-0.004373, +0.005450] |
| Add original partner b given a | +0.002038 [-0.002783, +0.006464] | +0.001128 [-0.003805, +0.005874] |
| Replace b with c | -0.001351 [-0.004328, +0.001693] | -0.000324 [-0.003948, +0.003102] |
| High half c alone vs Base | -0.004270 [-0.009327, +0.000429] | -0.004528 [-0.009884, +0.000429] |
| a/c NLL interaction | +0.004957 [+0.003182, +0.006608] | +0.005331 [+0.003616, +0.007123] |

### true_replacement_1015: 1015 positions, 107 dialogues

| Intervention | T_F fixed-seed mean [95% interval] | T_H fixed-seed mean [95% interval] |
|---|---:|---:|
| Add high-frequency c given a | +0.000016 [-0.005484, +0.005269] | +0.001355 [-0.004390, +0.006679] |
| Add original partner b given a | +0.002280 [-0.002096, +0.006061] | +0.001898 [-0.002755, +0.006306] |
| Replace b with c | -0.002264 [-0.007851, +0.002843] | -0.000543 [-0.006652, +0.005591] |
| High half c alone vs Base | -0.002459 [-0.007889, +0.002626] | -0.002135 [-0.007734, +0.003043] |
| a/c NLL interaction | +0.002475 [+0.000149, +0.004841] | +0.003490 [+0.001159, +0.005499] |

Interaction is L(Base+.5a+.5c)−L(Base+.5a)−L(Base+.5c)+L(Base). A positive value means combined loss is higher than summing the individual loss changes: instantaneous NLL non-additivity, not automatically training interference. Per-seed values and array/receipt hashes are in the[separate summary](../../../../../../../../../UNAVAILABLE.md).


## F: Paired natural continuation and native-attention readouts

The64 validation documents each have127 targets,8128 positions total. Mean CE per document receives2000 paired document draws(seed20261023); equal document lengths make the document and position means identical. Intervals describe document uncertainty at fixed endpoints, not model-seed variation. Natural continuation and collateral natural readout of list-trained attention are separate experiments.

| R1 natural-continuation endpoint contrast | NLL delta nat/target [95% document interval] |
|---|---:|
| dense_protected_minus_dense_normal | -0.000786862 [-0.001044237, -0.000556584] |
| shared2_protected_minus_ordinary2 | -0.000670356 [-0.009293992, +0.008466520] |
| ordinary2_minus_dense_normal | +0.025914411 [+0.018487367, +0.033259061] |

Absolute reference: R1 dense starts near NLL2.619969 and ends near2.631; R2 starts near2.619969 and its first dense endpoint is near2.685. A negative protected-minus-normal difference means relatively less deterioration, not absolute natural held-out improvement versus parent.

All seven order29 list-trained A endpoints receive native full-attention natural readout without extra natural training. Every arm lowers NLL relative to the same acquired-old parent; this shared improvement cannot identify selector specificity. Direct TS-minus-control comparisons follow; positive means higher TS natural NLL.

| Control | TS−control NLL delta [95% document interval] |
|---|---:|
| U | +0.002007700 [+0.001442511, +0.002574058] |
| UL | -0.001768056 [-0.004144360, +0.000569133] |
| US | +0.001049039 [-0.001484547, +0.003530288] |
| TC | +0.000766132 [+0.000416887, +0.001151944] |
| RS | +0.000896914 [+0.000414960, +0.001401087] |
| LS | +0.002292947 [+0.001456193, +0.003161938] |

Source:[paired natural comparisons](../../../../../../../../../UNAVAILABLE.md), including every source file and every A-versus-parent contrast. R1/R2 remain separate; small document-panel differences do not establish broad practical benefit.


## A/B: Finite functional interventions and local limits

At the same A/TS order29 update1200 state, restore a component to its initial value, amplify its actual training displacement, or use a random perturbation matching that component norm. Each readout has800 old/new answers. C denotes the initial top16 projector; R is its complement.

| Intervention | Actual parameter perturbation norm | Old accuracy | New accuracy | Old CE change | New CE change |
|---|---:|---:|---:|---:|---:|
| endpoint | 0.000000000 | 0.000% | 100.000% | +0.000000000 | +0.000000000 |
| restore_C | 0.004188625 | 0.000% | 100.000% | -0.000608559 | -0.000000009 |
| amplify_C | 0.004188625 | 0.000% | 100.000% | +0.000602595 | +0.000000003 |
| restore_R | 4.964333223 | 100.000% | 0.000% | -16.006771445 | +16.038188113 |
| amplify_R | 4.964333222 | 3.250% | 92.250% | +7.324592764 | +0.432563313 |
| random_C | 0.004188623 | 0.000% | 100.000% | -0.000006921 | +0.000000010 |
| random_R | 4.964333429 | 0.000% | 100.000% | -0.106634738 | +0.000001961 |

Restoring R reinstates the old rule and removes the new rule; restoring C does not recover old accuracy. Restoring C undoes its actual drift rather than deleting initial C, so it cannot prove C functionally unimportant. C/R perturbation norms are about.00419/4.964, differing roughly1185-fold, so these are not equal-amplitude causal contrasts. Norm-matched random R does not restore old accuracy, establishing conditional direction sensitivity, not unique trajectory mediation or task-private semantics.

A separate local probe starts at the shared acquired-old state:20 TRAIN answers from one mode propose one Adam displacement, then800 opposite-mode DEV answers are read. Positive opposite-mode CE change is immediate harm. Candidate/complement/random directions are rescaled to that source mode’s measured full-update Frobenius norm.

| Source→recipient mode | Full | Candidate norm matched | Complement norm matched | Random norm matched | Full actual norm |
|---|---:|---:|---:|---:|---:|
| 1→2 | +0.443761723 | -0.002574007 | +0.443890111 | -0.002664036 | 0.158178863 |
| 2→1 | +0.000059342 | +0.000021280 | +0.000058713 | +0.000010681 | 0.235236840 |

Candidate matching amplifies its native component about71.84-fold(source1)/62.70-fold(source2). This tests direction sensitivity at equal total amplitude, not an equally large contribution in actual training. One-state local effects do not explain1200-update forgetting uniquely. Sources:[component restoration](../../../../../../../../../UNAVAILABLE.md),[finite update](../../../../../../../../../UNAVAILABLE.md).


## R2: Observed TRAIN fitting versus DEV generalization

At the prescribed1200-update ordinary and multi_normal states, reread all4800 TRAIN records with full-vocabulary argmax and CE, without training. Each old TRAIN panel has2400 records at100%; new TRAIN values follow. All four mode/command TRAIN cells reach95%, while the weakest new DEV cells remain51%/54%. This establishes an observed TRAIN-to-DEV gap, not perfect fitting, absent input information or a uniquely identified capacity/optimization cause.

| R2 condition | New TRAIN accuracy | New TRAIN CE | New DEV accuracy | Weakest new DEV cell |
|---|---:|---:|---:|---:|
| ordinary | 96.708% | 0.100911 | 82.375% | 51.000% |
| multi_normal | 96.208% | 0.134037 | 83.125% | 54.000% |

The saved panel localization identifies the weakest cell as乙-command/unseen-order,200 DEV answers each: ordinary51%/CE2.285740, multi_normal54%/CE2.444560. Other new DEV cells are ordinary90.5%/94.5%/93.5%, multi92%/93%/93.5%. TRAIN has1200 answers/command and only panel=train; novelty-matched TRAIN panel readouts are Unknown. Source:`analysis/ffn_generalization_panels.json`.

Sources: execution-root`runs/repair_full_ffn/D/seed_29/{ordinary,multi_normal}/train_endpoint_readout.json` and environment receipts. The earlier CPU20-answer-pool diagnostic covers R1 only and does not replace this R2 full-vocabulary result.


## F: Absolute change from each same-start parent

All four R1 and four R2 endpoint-minus-initial NLL differences are positive, with64-document paired2000-bootstrap intervals above0. A negative contrast against another method therefore means less deterioration only.

| Round | Condition | Endpoint−initial NLL [95% document interval] |
|---|---|---:|
| R1 | dense_normal | +0.011775 [+0.001091, +0.022125] |
| R1 | dense_protected | +0.010988 [+0.000304, +0.021154] |
| R1 | ordinary2 | +0.037689 [+0.025292, +0.049548] |
| R1 | shared2_protected | +0.037019 [+0.027494, +0.046475] |
| R2 | dense_normal | +0.065349 [+0.051041, +0.080027] |
| R2 | dense_protected | +0.065442 [+0.051103, +0.080126] |
| R2 | ordinary2 | +0.072333 [+0.057829, +0.087562] |
| R2 | shared2_protected | +0.112684 [+0.096399, +0.128775] |

The[absolute-change audit](../../../../../../../../../UNAVAILABLE.md) verifies alignment of all8128 document/position/target tuples. R1/R2 stay separate; intervals condition on fixed endpoints and64 documents rather than model seeds.


## E: Selection versus an exactly matched-load diagnostic

For six prespecified learned endpoints, freeze that endpoint’s experts and reassign records by a fixed record-id hash permutation, exactly preserving the learned two-expert DEV counts, without modes or targets. This is one prespecified permutation per endpoint rather than an independently trained random router. Accuracy pools1600 old/new answers; positive random-minus-learned CE favors learned selection.

| Round | Input/phase | Expert0/1 calls | Learned accuracy | Same-load permutation accuracy | CE random−learned |
|---|---|---:|---:|---:|---:|
| R1 | full/fixed | 823/777 | 85.438% | 48.250% | +4.932683 |
| R1 | full/joint | 798/802 | 88.250% | 47.125% | +5.334761 |
| R1 | summary/fixed | 1498/102 | 52.812% | 50.688% | +0.234082 |
| R1 | summary/joint | 289/1311 | 64.750% | 62.000% | +0.437187 |
| R1 | random_summary/fixed | 58/1542 | 44.438% | 43.125% | +0.139261 |
| R1 | random_summary/joint | 275/1325 | 62.062% | 57.250% | +0.417627 |
| R2 | full/fixed | 1315/285 | 64.688% | 50.125% | +2.145973 |
| R2 | full/joint | 784/816 | 91.312% | 48.125% | +4.363900 |
| R2 | summary/fixed | 1600/0 | 50.000% | 50.000% | +0.000000 |
| R2 | summary/joint | 0/1600 | 89.938% | 89.938% | +0.000000 |
| R2 | random_summary/fixed | 266/1334 | 51.250% | 43.000% | +0.983156 |
| R2 | random_summary/joint | 0/1600 | 87.875% | 87.875% | +0.000000 |

R2 candidate-summary fixed routes every record to expert0, whereas its joint endpoint and random-summary joint route every record to expert1. Joint accuracy gains therefore do not establish learned mode allocation: the experts themselves adapt. Full-input joint nearly separates modes (expert0 old784/new0, expert1 old16/new800) and beats the same-load permutation by43.1875pp accuracy. This is actual allocation utility conditional on those endpoint experts; it does not repair failed expert qualification or prove absent rule information in the summary. Sources: each E endpoint’s`router_load_control.json`; full costs/routes remain execution-side and in Detailed.

## Evidence and limits

The [factual JSON](../../../../../../../../../UNAVAILABLE.md) links each case's actual endpoint, completion, scope, saved-state manifests and queue identity. The [three audits](audits.md) state engineering/statistical eligibility. Per-answer records remain execution-side under `runs/<stage>/seed_<seed>/<arm>/eval_XXXXX.json`; E additionally separates fixed/joint phases. Final registration covers105 formal/engineering checkpoint families and686 actual states; the scientific-case count remains89. Receipt`audit/registration_receipt_20261022T174400242571Z.json` is REGISTERED_ACCESS_PASS; the[audits](audits.md) distinguish full-hash/CPU checks from strict access scope.

One R2 F/dense_protected source-identity boundary remains: its task freeze is pre-fix c49, while the environment stores the patched40eb disk-file hash, which cannot identify imported bytecode. Loaded source version is Unknown. The two sources differ only in a two-line single-expert oracle-natural-readout guard; this F case uses the string-valued none route and never enters that branch. Source comparison therefore bounds executed training/function equivalence without treating a disk hash as import proof. See the final fairness audit.

All list results share one acquired model and exposed DEV. Order variation is not independent old-model replication. Orthogonality does not establish functional independence. List-task findings do not causally explain natural-language semantics or historical A15_24 frequency routing. Missing, failed, blocked and unsaved items remain explicit. Execution of0/A–F and the sole R2 repair is complete; researcher scientific acceptance and question closure remain Unknown.
