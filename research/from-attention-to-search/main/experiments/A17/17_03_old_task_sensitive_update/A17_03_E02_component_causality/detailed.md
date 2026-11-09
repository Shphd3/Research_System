# Detailed: A17_03_E02 component-causality evidence

[中文](detailed_cn.md) · [Summary](summary.md) · [Protocol](protocol.md) · [Artifact manifest](artifact_manifest.json)

Primary Anchor: [17_03_01](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/subanchors/17_03_01_component_causality_anchor.md). Frozen [Protocol](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/protocol_frozen.md), SHA256 `5a2d33e67b66ab9ce8d8c585309bdd955ef397b71e33c7e3f5d49adb5428f773`. Eligibility: **ELIGIBLE for registered finite interventions on exposed development data**. Interpretation is AI_PROPOSAL; researcher mechanism judgment, next decision and closure remain Unknown.

## 0. Quick recap

The question is whether deleting sensitive components or amplifying the remainder explains an immediate new-dev CE advantage. All 630 conditions qualify. Six case-mean deletion gains are negative and amplification gains positive: pooled −0.000353638/+0.000589189/+0.000235550 nat/answer. H1's deletion-benefit account is not supported for these means; finite intervention supports amplification compensating deletion costs. Four total gains are positive, two negative. The original additional long-run old-accuracy cost is not reproduced by this average immediate contrast. No complete 100-step mechanism is established.

## 1. Objects and measurements

| Object | Construction and purpose | Unit / boundary |
| --- | --- | --- |
| full | Mean source-20 CE gradient with original clipped-SGD coefficient | One parameter displacement, not a trajectory |
| in/out | Projection onto fixed rank-16 Q and its complement | Sensitivity is unsigned; components sum to full |
| out_norm | Complement amplified to full norm | Separates deletion from subsequent amplification |
| random_norm | Random rank-16 complement, norm matched | Removed gradient energy is not matched |
| access/selection | Exact answer-pair loss-component gradients with the common CE coefficient | selection is mathematical choice; cross-effects are possible |
| margin | Correct-answer logit minus opposite-rule-answer logit | Not full-vocabulary accuracy |
| b/h | Mean correct margins / prompt-averaged new-answer bias | m_new=b+h, m_old=b−h; output coordinates, not modules |
| Gdelete/Gamp | New CE(full)−CE(out), CE(out)−CE(out_norm) | nat/answer; positive favors the latter |

CE=access+selection and selection=softplus(−margin). Mean selection loss cannot be inferred from mean margin. Actual parameter interventions identify conditional effects; additive objectives do not establish independent mechanisms.

## 2. Anchor and decision point

The parent question concerns shared updates helping or harming predictive requirements. This round identifies the local deletion/amplification contrast and preserves E01's absence of ordinary CE forgetting. Whether to investigate reduced old-error repair later in the trajectory remains a researcher decision.

## 3. Freeze, conformance and deviations

| Registered item | Actual evidence | Eligibility |
| --- | --- | --- |
| Same state/source and per-cell restoration | Matrix/source20 equality and frozen versions/hashes pass | PASS |
| Six cases × three batches × seven directions × five scales | 630 complete cells, no replacement or exclusion | PASS |
| Smoke before separate Full | 140 Smoke cells and four independent replays precede Full | PASS |
| Data identity and test boundary | Frozen original train/dev; test unread | PASS; exposed dev |
| Primary scale 1 and both novelty panels | Every case/panel/batch retained; no scale selection | PASS |
| Analysis provenance | Rules frozen before measurement; script hash saved before formal aggregation; 1,296 scalars independently recomputed | PASS, maximum difference 1.11e−16 |
| Analysis accounting | Zero training updates; 504,000 dev and 12,600 source intervention readouts | PASS; other forwards are baseline/restoration |
| Post-hoc trajectory linkage | First-step audit and saved checkpoints 1/16/50/100 | BOUNDED context, not a changed primary estimand |

There were no retries, exclusions, threshold changes or additional conditions. The script's 1e−8 three-way sign label is a display convention, not a population-significance threshold. See [independent audit](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_engineering_audit.json).

## 4. Actual setup

Official 28-layer Qwen3-0.6B Base; only `model.layers.27.self_attn.o_proj.weight` [1024,2048] is varied. Native FP32, eval, SDPA, TF32 disabled. Visible FIRST/LAST prompts over three distinct words; one answer token. Dev contains 400 answers per rule, 200 each for unseen order and unseen combination. Ordered train/dev lists are disjoint. Seeds 29/43/71 each have both orders. Old states are E01 update100 after 2,000 old-rule answers.

The original new_order's first 60 records form three fixed batches of 20. Gradients use microbatch5 and denominator20; eta_eff=0.01·min(1,1/||g||), without momentum or decay. Seven independently applied directions and scales −0.1,0.1,0.25,1,4; primary scale1. Complement amplification factors range 1.188920–1.851537, mean1.461656 across 18 batches. Only out_norm/random_norm are norm matched; access/selection are not separately normalized.

Config SHA256 `3bb5337c5dad82beb7d51b9a1dd9c1507d0d8d789474ae8c7ef60d903201d1a5`. Ten model/tokenizer/data/six-old-state/subspace input assets are recorded in [artifact_manifest](artifact_manifest.json) and [freeze](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/freeze.json); all 43 frozen files rehashed successfully. No original state, basis or dataset was retrained or modified.

## 5. Metrics and registered rules

Positive Gdelete/Gamp supports the respective local CE benefit. Preserve both signed terms and their sum; no attribution fraction with a near-zero denominator. No invented all-six-favorable gate. Average batches within case, then weight seeds and orders equally; six cases are not six independent seeds. Accuracy is percentage points, while positive margin changes favor improvement and positive CE changes do not.

H2 records per-list Δh>Δb>0 without presenting its algebraic implication as empirical discovery. Secondary scales cannot rescue a primary claim. No population p-values or independent-confirmation intervals. Source first-order predictions use native gradients dotted with actual displacement; dev slopes use central finite differences at ±0.1 and are not analytical dev gradients.

## 6. Evidence lineage

| Claim | Raw-to-derived path | Observation / eligibility | Boundary |
| --- | --- | --- | --- |
| Deletion cost and amplification benefit | Cell records→rule/panel means→three-batch case means; [case table](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_case_effects.csv) | Six negative/six positive means; ELIGIBLE | Three seed blocks, not a theorem |
| Source and dev differ | Source20 readouts/actual-displacement derivatives; [source](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/source_analytic_first_order.csv), [dev](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv) | Full helps source more, out_norm helps dev more; ELIGIBLE | Not a generalization theorem |
| Different choice readers disagree | [Coordinates](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/paired_coordinates.csv), [transitions](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/accuracy_transitions.json) | Readers retained separately; ELIGIBLE | Mean margin does not determine mean softplus or argmax |
| Small-contrast approximation limits | Same-curve ±0.1 slopes versus larger scales; [curve contrasts](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/dev_component_curve_checks.csv) | Remainders retained; ELIGIBLE diagnostic | Extrapolation is not independent predictive confirmation |
| E01 first-step linkage | [First-step audit](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/first_step_bridge.json) | Twelve conditions, maximum difference1.1444e−5, accuracy disagreements0; BOUNDED | Only the actual first step |
| Later timing context | [Saved-trajectory recap](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/trajectory_recap/analysis_cn.md) and its manifests | Original steps1/16/50/100; BOUNDED | Post-hoc description, not later-component attribution |

## 7. Main results

### 7.1 Six cases and both panels

Each row averages three source batches within its case. CE uses nat/answer. Combined equally weights the two panels. The last column is out_norm minus full old accuracy, so positive values favor the restricted update. [Full case table](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_case_effects.csv)

| Case | Panel | Gdelete | Gamp | Gtotal | Old accuracy out_norm−full (pp) |
| --- | --- | --- | --- | --- | --- |
| s29_FIRST_to_LAST | combined | -0.000061336 | +0.000453617 | +0.000392281 | +0.500000 |
| s29_FIRST_to_LAST | order_new | -0.000085204 | +0.000428621 | +0.000343416 | +0.166667 |
| s29_FIRST_to_LAST | combination_new | -0.000037468 | +0.000478613 | +0.000441145 | +0.833333 |
| s29_LAST_to_FIRST | combined | -0.000165639 | +0.000878025 | +0.000712387 | -0.083333 |
| s29_LAST_to_FIRST | order_new | -0.000209191 | +0.000847834 | +0.000638643 | -0.166667 |
| s29_LAST_to_FIRST | combination_new | -0.000122086 | +0.000908217 | +0.000786131 | -0.000000 |
| s43_FIRST_to_LAST | combined | -0.000227828 | +0.000423685 | +0.000195857 | -0.333333 |
| s43_FIRST_to_LAST | order_new | -0.000293447 | +0.000401767 | +0.000108320 | -0.666667 |
| s43_FIRST_to_LAST | combination_new | -0.000162209 | +0.000445603 | +0.000283394 | -0.000000 |
| s43_LAST_to_FIRST | combined | -0.000832750 | +0.000632354 | -0.000200396 | +0.250000 |
| s43_LAST_to_FIRST | order_new | -0.000691293 | +0.000616224 | -0.000075069 | +0.500000 |
| s43_LAST_to_FIRST | combination_new | -0.000974207 | +0.000648484 | -0.000325723 | -0.000000 |
| s71_FIRST_to_LAST | combined | -0.000497517 | +0.000495217 | -0.000002300 | -0.000000 |
| s71_FIRST_to_LAST | order_new | -0.000600172 | +0.000502763 | -0.000097409 | -0.000000 |
| s71_FIRST_to_LAST | combination_new | -0.000394863 | +0.000487672 | +0.000092809 | -0.000000 |
| s71_LAST_to_FIRST | combined | -0.000336760 | +0.000652233 | +0.000315473 | +0.250000 |
| s71_LAST_to_FIRST | order_new | -0.000382297 | +0.000626834 | +0.000244538 | -0.000000 |
| s71_LAST_to_FIRST | combination_new | -0.000291223 | +0.000677632 | +0.000386408 | +0.500000 |

All six combined deletion gains are negative and amplification gains positive; total gains are four positive/two negative. The s71 FIRST→LAST total of −2.300e−6 results from near cancellation of approximately −4.975e−4 and +4.952e−4. Preserve the value without claiming robust superiority. Across18 source batches, deletion has2 positive/16 negative, amplification18 positive, and total12 positive/6 negative; batches are not independent seeds.

### 7.2 Order and novelty-panel summaries

[Complete order table](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_order_effects.csv)

| Order | Panel | New Gdelete | New Gamp | New Gtotal | Old CE full−out_norm |
| --- | --- | --- | --- | --- | --- |
| FIRST_to_LAST | order_new | -0.000326274 | +0.000444383 | +0.000118109 | +0.000104309 |
| FIRST_to_LAST | combination_new | -0.000198180 | +0.000470629 | +0.000272449 | +0.000348591 |
| FIRST_to_LAST | combined | -0.000262227 | +0.000457506 | +0.000195279 | +0.000226450 |
| LAST_to_FIRST | order_new | -0.000427594 | +0.000696964 | +0.000269370 | +0.000216421 |
| LAST_to_FIRST | combination_new | -0.000462505 | +0.000744777 | +0.000282272 | +0.000051584 |
| LAST_to_FIRST | combined | -0.000445049 | +0.000720871 | +0.000275821 | +0.000134003 |

Both panel/order means show deletion costs and amplification benefits. These novelty panels do not establish natural-corpus generalization.

### 7.3 Seven directions and old-selection costs

Equal-weight means across18 source updates, relative to each untouched old endpoint. Negative CE and positive margin changes are improvements. Objective-gradient directions have different norms and cannot be ranked as equal-budget methods. [Source rows](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv)

| Direction | Old ΔCE | New ΔCE | Old Δmargin | New Δmargin | Old Δaccuracy pp | New Δaccuracy pp |
| --- | --- | --- | --- | --- | --- | --- |
| full | -0.001137093 | -0.001678487 | +0.000903156 | +0.001761810 | -0.166667 | +0.013889 |
| in | -0.000234727 | -0.000370856 | +0.000131625 | +0.000189526 | -0.152778 | +0.000000 |
| out | -0.000914302 | -0.001324849 | +0.000771901 | +0.001571199 | -0.111111 | -0.027778 |
| out_norm | -0.001317320 | -0.001914037 | +0.001127607 | +0.002242881 | -0.069444 | -0.027778 |
| random_norm | -0.001137110 | -0.001678475 | +0.000903262 | +0.001761800 | -0.166667 | +0.013889 |
| access | -0.000893938 | -0.001051852 | +0.000895830 | +0.000980111 | +0.041667 | +0.000000 |
| selection | -0.000246437 | -0.000630086 | +0.000007795 | +0.000780986 | -0.055556 | +0.055556 |

Out_norm old accuracy exceeds full by0.097222 percentage points, failing to reproduce E01's additional long-run old-accuracy cost. Its old mean margin is higher by0.000183894/0.000265008 in the two orders, but old selection CE is worse by0.000027736/0.000146847. The nonlinear softplus(−m) weights sample-level margin changes differently; average margin is not average selection loss.

Across7,200 old record/update instances per direction, full loses27 correct answers and repairs15, out loses10 and repairs2, and out_norm loses11 and repairs6. All11 out_norm new errors predict the opposite-rule word; full has22 opposite-rule and5 middle-word errors. These are18 interventions over repeated lists, not independent accuracy trials. Do not pool them with E01's2,400 long-run instances.

### 7.4 Rule response and bias

Out_norm mean Δb=0.001685244 and Δh=0.000557637; full means are0.001332483 and0.000429327. In 6,812/7,200 out_norm list/update instances (94.61%), Δb>0; 3,117 have Δh>Δb>0 and old margin declines. Both margins improve in 1,037/7,200 (14.40%), versus 371/7,200 (5.15%) for full. Opposing per-list effects can cancel in averages; mean Δb>|mean Δh| does not imply per-list shared help. [Coordinates and quadrants](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/paired_coordinate_summary.json)

### 7.5 Source analytical derivatives and dev finite curves

Source remainder is measured ΔL minus gᵀΔW_actual. Report means and medians of ratios separately. [Source table](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/source_analytic_first_order.csv)

| Direction | Measured ΔCE | g·actual ΔW | Remainder | Median absolute remainder / absolute effect | Maximum |
| --- | --- | --- | --- | --- | --- |
| full | -0.013797487 | -0.013937400 | +0.000139912 | 0.995% | 1.413% |
| in | -0.007306296 | -0.007374657 | +0.000068361 | 0.925% | 1.363% |
| out | -0.006542337 | -0.006562743 | +0.000020406 | 0.302% | 0.465% |
| out_norm | -0.009466609 | -0.009509562 | +0.000042953 | 0.443% | 0.643% |
| access | -0.005165182 | -0.005207743 | +0.000042560 | 0.648% | 2.795% |
| selection | -0.008639408 | -0.008729664 | +0.000090255 | 0.966% | 1.597% |

Full source descent is larger, consistent with the steepest first-order descent property. Dev uses the same intervention's ±0.1 curve to extrapolate to scale1; the following is not analytical dev Taylor validation. [Small-contrast remainders](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/dev_component_curve_checks.csv)

| Contrast | Measured | Central extrapolation | Remainder | Median absolute remainder / absolute effect | Maximum |
| --- | --- | --- | --- | --- | --- |
| deletion | -0.000353638 | -0.000416187 | +0.000062549 | 16.950% | 415.038% |
| amplification | +0.000589189 | +0.000600395 | -0.000011206 | 1.728% | 5.344% |
| total | +0.000235550 | +0.000184208 | +0.000051343 | 16.661% | 80.863% |

A maximum deletion-contrast relative error of415.038% shows that a small contrast cannot always be explained by local extrapolation, even when the much larger loss change is well approximated. Actual finite contrasts govern the primary judgment.

### 7.6 Scales and interactions

[Four-corner interactions](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/four_corner_interactions.csv) and [finite contrasts](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/deletion_amplification_contrasts.csv), equally weighted across orders, seeds and sources.

| Scale | Gdelete | Gamp | Gtotal | Mean geometric interaction |
| --- | --- | --- | --- | --- |
| 0.25 | -0.000100299 | +0.000149402 | +0.000049102 | +0.000001398 |
| 1.0 | -0.000353638 | +0.000589189 | +0.000235550 | +0.000017218 |
| 4.0 | -0.000642529 | +0.002225570 | +0.001583041 | +0.000280840 |

Scales0.25/4 are registered diagnostics, not candidates for winner selection. Nonzero four-corner effects show failure of simple finite additivity, but very small effects also include FP32 corners whose actual displacements do not sum exactly, plus readout precision. Nonzero alone is not proof of model curvature. Actual source derivatives help inspect rounding; analytical dev gradients were not computed to eliminate all numerical interaction.

The secondary objective-component interaction is also computed from the same seven-direction readouts: I_obj=ΔCE(full)−ΔCE(access)−ΔCE(selection). At the primary scale, equal-order mean old/new dev values are +0.000003282/+0.000003451 nat. These finite effects do not imply independent objective gradients and do not replace the primary geometric interaction; numerical precision remains relevant. [All objective-direction readouts](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv)

## 8. Visualization boundary

The registered decision is readable from these tables and source records; no new figure is required. The meeting's black/gray/white endpoint figure is an E01 post-hoc explanation. The max-min candidate direction for the weaker of the two first-order improvements was not executed in E02 and cannot be presented as an effective tested method.

## 9. Stage evidence and failure decomposition

| Check | Observed maximum/status | Bound/meaning |
| --- | --- | --- |
| Original old baseline reproduction | 0 | ≤2e−5 |
| Source-gradient recomposition relative error | 3.177037e−6 | <2e−4 |
| Per-record CE decomposition absolute error | 1.158142e−6 | <2e−5 |
| Actual-step relative rounding | 0.002663046 | <0.01 |
| Sensitive-Q leakage | 4.746678e−6 | <0.002 |
| Random-R leakage | 3.506868e−6 | <0.002 |
| Source20 restoration/independent replay | Exact throughout | Engineering only |
| Frozen parameter hashes and versions | PASS | Only registered matrix changed |
| 43 frozen inputs,630 cells,1,296-scalar recomputation | PASS; maximum difference1.11e−16 | Integrity/arithmetic, not mechanism proof |

No data, implementation or engineering failure was found. H1 non-support is a scientific outcome. The leap from unsigned sensitivity to harmful new-task function is restricted; sensitivity estimation itself is not disproved. Long-run accuracy costs still need trajectory evidence.

## 10. Full round record

On2026-10-11 the round tested local deletion/amplification. Ten registered inputs and original old states were reused;43 files frozen. Smoke `pt-1gvachp3` on four reserved H100s completed140 cells and4 independent replays. Separate Full `pt-majgvu5m` started02:22:46Z, completed02:31:02Z and SUCCEEDED; all four workers exited0. No retry. Eighteen source batches×20 answers;630 cells×800 dev+20 source readouts. Total539,520 forward answers include baseline/restoration repetitions;360 gradient answers,216 objective backward calls,zero new training updates.

The result is six negative case-mean deletion gains and six positive amplification gains, with four positive/two negative totals. Source fitting and dev help differ; local old accuracy does not match the long-run additional deterioration. The insight is that old-sensitive components can help both old and new CE and that update-length redistribution must be tested separately. Next researcher decision remains Unknown; no additional trajectory or method is automatically launched.

## 11. Interpretation and trajectory linkage

AI_PROPOSAL: at these fixed initial states, average immediate new-CE advantage comes from amplification compensating the deletion cost, not removal of an already harmful new-learning component. Geometry and norm allocation jointly matter. Random codimension removal approximates ordinary updates but does not energy-match the sensitive removal.

The first batch matches E01's actual first-step conditions: across12 comparisons, common readouts differ by at most1.144409e−5 and accuracy indicators never disagree. Different FP32 operation ordering precludes claiming bitwise equivalence of the original restricted operation. Batches1/2 in E02 still start at the old endpoint; they are not actual E01 training steps2/3.

At saved E01 steps1/16/50/100, pooled ordinary-minus-restricted new CE is+0.00028500/+0.00417299/+0.01164035/+0.02156073. Five of six cases benefit at the first saved point; six by step16. This cannot locate first appearance between saved checkpoints or attribute later divergence to the initial fixed displacement. This post-hoc recap remains separate from E02's registered three-source average.

## 12. Claim boundary

Can claim: specified finite deletion/amplification effects, signed effects distinct from unsigned sensitivity, and measured output-coordinate/competitor consequences. Cannot claim: shared/unique modules, expert necessity, functional parameter separation, a universally optimal policy, natural-NTP conclusions, the complete100-step mechanism, or effectiveness of an unexecuted constructive candidate.

## 13. Next decision

Researcher decision: Unknown. AI suggestion: decide whether the next target should explain why old-error repair decreases later in the trajectory. If pursued, fix that predictive requirement and a discriminating comparison; additional CE gains cannot substitute for the answer. This record does not authorize or launch another run.

## 14. Artifact and asset manifest

[artifact_manifest.json](artifact_manifest.json) binds29 compact provenance references/hashes: two job receipts, complete-cell manifest, freeze, analysis/audits, first-step comparison and offline/trajectory records. Large payloads remain execution-side. [Analysis output manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/output_manifest.json) and [input/script manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/input_manifest.json) record actual sources and revisions; platform success is not substituted for payload verification.

Actually registered outputs: `representation_a17_03_component_causality_full_20261011t020424z` and `representation_a17_03_component_causality_smoke_20261011t020424z`. The [fresh strict access check](/data/250010109/Research_System/assets/checks/2026-10-11_a17_component_causality_outputs_0233.json) passes. No trained checkpoint was produced. `results.json` SHA256 `82c5770bf4193e568503ef2a4830e25002705845814464cfea225a57e5f7a532`.

## 15. Entry points

- [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/execution_certificate.md), [terminal platform state](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_platform_terminal.json), [engineering audit](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_engineering_audit.json).
- [Runner](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/source/run.py), [objective/displacement construction](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/source/components.py), [config](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/config.json), [aggregator](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/summarize.py).
- [Results](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/results.json), [input/script manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/input_manifest.json), [first-step audit](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/first_step_bridge.json).
- [Original endpoint explanation](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/analysis_cn.md), [saved-trajectory recap](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/trajectory_recap/analysis_cn.md).

Record self-review: frozen scope preserved; primary values trace to source tables and independent recomputation; eligibility, observations, derivations and AI interpretation are separated. Researcher scientific judgment was not filled by an agent.
