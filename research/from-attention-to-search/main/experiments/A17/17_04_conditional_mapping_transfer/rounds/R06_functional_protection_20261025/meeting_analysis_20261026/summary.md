# Maintaining learned behavior: supervision organization versus local constraints

Purpose: the advisor's reuse-and-differentiate intuition requires learned behavior to remain valid during new learning. This bounded A17 case asks whether parameter restrictions, first-order old-loss constraints and continued correct old supervision have equivalent effects. The task is visible-mode command-to-first/last mapping, with reversed mappings in mode two, not mathematical hierarchy or identified reusable subspaces.

All36existing runs completed240steps/8640new targets, fixed36new/36old slots and denominator72. Old active targets0/4/36 change both exposure and old-objective weight. All methods compute64old TRAIN probes; F/D use old labels even at0old replay. Three continuation orders share one acquired-old model, DEV exposed, TEST unopened.

| old_slots | method | old_accuracy_pct | new_accuracy_pct | old_ce_nats | new_ce_nats |
| --- | --- | --- | --- | --- | --- |
| 0 | U | 0.125 | 99.833 | 9.711 | 0.010 |
| 0 | S | 0.208 | 99.750 | 9.925 | 0.010 |
| 0 | F | 11.292 | 98.792 | 5.839 | 0.038 |
| 0 | D | 0.125 | 99.792 | 9.836 | 0.010 |
| 4 | U | 93.125 | 99.042 | 0.189 | 0.036 |
| 4 | S | 87.542 | 98.958 | 0.331 | 0.038 |
| 4 | F | 68.250 | 98.208 | 0.795 | 0.054 |
| 4 | D | 89.875 | 99.292 | 0.241 | 0.032 |
| 36 | U | 99.708 | 99.458 | 0.009 | 0.019 |
| 36 | S | 99.917 | 99.167 | 0.005 | 0.029 |
| 36 | F | 99.750 | 98.792 | 0.009 | 0.039 |
| 36 | D | 99.667 | 99.042 | 0.009 | 0.023 |

F-minus-U old gains+11.167,-24.875,+0.042pp are nonmonotonic; F1:9 is worse in every order. S1:1 has a small+0.208pp old change in everyorder, with-0.292pp new change, not the5pp operational utility threshold. At the second consecutive scheduled newaccuracy>=90% point, U/F1:9 both confirm at180steps yet old means88.167%/59.375%; zero-replay F confirms240/180/240 versus U180/180/180. No interpolation or endpoint reselection.

| method | old_slots | old_rule_correct_pct | new_rule_endpoint_pct | other_list_item_pct | other_output_or_invalid_pct | both_correct_pct | same_prediction_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U | 0 | 0.125 | 99.833 | 0.042 | 0.000 | 0.125 | 99.750 |
| F | 0 | 11.292 | 87.333 | 1.375 | 0.000 | 10.583 | 88.375 |
| U | 4 | 93.125 | 6.792 | 0.083 | 0.000 | 92.167 | 7.125 |
| F | 4 | 68.250 | 28.708 | 3.042 | 0.000 | 66.708 | 29.958 |

Old/new targets come from paired labels independently checked against generator rules, not inferred predictions. All targets differ, zero exclusions;800modepairs/run,400/panel. At acquisition start old100% but modes give sameanswer99.875%, so the parent had not already learned correct reversed-mode switching. Endpoints show behavioral rule confusion and its reduction with correct supervision, not old-circuit deletion or distinct internal mechanisms.

F measurement audit: same64probe records, same parameter start, CEmean64 and16microbatch, deterministic eval-child modules, actual post-filter FP32 displacement. The90checks have75projection triggers,15nontriggers,0nearzero-gradient guards;48raw-positive finaldots, maximum2.356e-7,0above inherited posthoc ideal-audit tolerance plus Cauchy parameter-copy rounding and conservativeFP64 reduction bounds.69actuallossincreases are raw signs; no saved repeated/no-op loss-noise calibration. Finite remainder is not identified curvature. U1:9also has16/30local increases but much better endpoint, so69/90is not a rootcause explanation. Full360checks and90Fpoints retain all inputs/tolerances/norms.

Nine existing endpoints U0/U1:9/F1:9 across3orders were read on locked64paired inputs (1152sequences total), on the already-existing collaboration H100MIG without a job/allocation or updates. Correctness-stratified sample is descriptive, not fullDEVestimate. At the final prefix token, q_proj input modegap is0.08188for all checkpoints by frozen-upstream construction; output o_proj modegap is nonzero even in U0, whose old/new endpoint-logit margins both favor newrule. F1:9outputgap exceeds U1:9in2/3orders while behavior is worse, so geometry magnitude is not a consistent functional explanation; no further metric scan. All1152argmax predictions match saved records, maxCEdifference3.815e-5.

AI bounded update: prioritize how input conditions maintain/organize correct function updates, retaining finite-step/probe-scope/optimizer-path explanations as rivals. This is not evidence for mandatory MoE, circuit deletion, natural-feature frequency laws or universal protection directions. Researcher acceptance/next experiment remain Unknown. Original training/source/Protocol/results unchanged; current posthoc analysis and finite readout are separate records.

[Chinese full report](summary_cn.md),[all seed/point appendix](appendix_cn.md),[figures/captions](figures_and_captions_cn.md),[coverage](coverage_cn.md).
