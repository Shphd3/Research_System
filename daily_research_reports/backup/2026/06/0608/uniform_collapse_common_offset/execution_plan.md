# Execution Plan: A05_03_uniform_collapse_common_offset

Anchor:

`05_03_uniform_collapse_common_offset_anchor.md`

Approved protocol:

`protocol_for_approval.md`

## 1. Run Goal

Decision question:

```text
Under verified uniform data and verified random router initialization, is collapse mainly initiated by the hidden common component through an expert-specific common offset in the linear gate?
If yes, can removing or controlling that offset reduce collapse while preserving target learning?
```

This experiment executes P0-P3 from the protocol:

1. P0: audit closure / baseline freezing.
2. P1: common-source perturbation, including repeated vs distributed / complex slot code.
3. P2: multi-seed common-score audit.
4. P3: logit-level common-offset cancellation before routing.

## 2. Data / Construction

Base setting:

```text
seq_len = 32
num_slots = 4
B tokens = 256
target = Y(slot, B)
feature grid = exact (slot, B) with fixed nuisance variants
```

Slot-code patterns:

```text
S0 repeated: [A,A,A,A,A]-style repeated cue.
S1 distributed_complex: [p,q,r,t,u]-style non-repeated code.
```

The complex slot code is not a new research direction. It is a construction
control for the same 05_03 question: does common-offset collapse depend on the
repeated-slot-token shortcut?

## 3. Can This Experiment Answer The Question?

| Protocol | Pre-run self-question | Answer |
|---|---|---|
| P0 | Can existing audit artifacts justify moving beyond bug explanations? | Yes, if all required 0607 audit tables exist and show slot uniformity, random bias-free R-router init, step-0 common component, and residual routing load reduction. |
| P1 | Can construction perturbations identify whether `c` is tied to position/template or repeated slot code? | Yes for step-0 source diagnosis. It cannot by itself prove training causality. |
| P2 | Can `w_e^T c` predict dominant expert across seeds and slot patterns? | Yes for early routing. Final-dominant evidence is limited by the training runs available in P3. |
| P3 | Can logit-level cancellation test whether common offset is causal for collapse? | Yes if training runs complete and target accuracy is preserved. If only CPU-shortened runs complete, it is mechanism evidence, not a full 4-card final claim. |

## 4. Implementation Contract

Use a new local script:

```text
scripts/run_a05_03_common_offset_experiments.py
```

The script must:

1. import the original H0605a model/config code;
2. reproduce training model creation semantics: seed, audit model, real model;
3. generate balanced feature grids for repeated and distributed slot-code patterns;
4. compute feature centroids at the routed B position;
5. compute common direction $c$, common scores $w_e^T c$, full-hidden load, residual load, and source alignment;
6. train baseline and logit-cancellation variants with expert input unchanged;
7. write CSV tables and PNG figures into this experiment folder.

## 5. Conditions

P1/P2 step-0 diagnostics:

```text
slot_pattern in {repeated, distributed_complex}
router_metric in {dot_product, cosine}
seeds = 20260521, 20260522, 20260523
diagnostic variants:
  full_hidden
  residual_mean_subtracted
  subtract_position_embedding_from_router_input
```

P3 training intervention:

```text
slot_pattern in {repeated, distributed_complex}
router_metric = dot_product first
intervention in {baseline_full_hidden, logit_common_offset_cancel}
seeds = 20260521, 20260522, 20260523
```

Reason for dot-product first:

The anchor's core offset is exactly $w_e^T c$ for dot-product routing. Cosine
routing has an analogous direction score but is not the first causal test.

## 6. Metrics And Artifacts

Primary metrics:

| Metric | Question |
|---|---|
| `step0_max_load` | Does the common offset already concentrate routing before training? |
| `residual_max_load` | Does removing feature-centroid mean reduce concentration? |
| `common_score_argmax_agrees_step0` | Does `argmax_e w_e^T c` predict the dominant expert? |
| `common_score_margin` | Does the common-score gap explain concentration strength? |
| `max_load_by_step` | Does logit cancellation reduce early/final load? |
| `target_accuracy` | Does the intervention preserve task learning? |
| `collapse_rate` | Does the intervention reduce hard collapse across seeds? |

Figures:

```text
figures/p1_common_source_by_pattern.png
figures/p2_common_score_prediction.png
figures/p3_training_load_accuracy.png
figures/p3_route_heatmap_by_condition.png
```

Tables:

```text
tables/p0_audit_closure.csv
tables/p1_step0_common_source.csv
tables/p2_common_score_prediction.csv
tables/p3_training_metrics_by_step.csv
tables/p3_summary_by_condition.csv
tables/run_manifest.json
```

## 7. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
|---|---|---|---|---|---|
| P0 audit closure | Are bug explanations weak enough? | 0607 audit tables exist | all required tables present | `p0_audit_closure.csv` | P1/P2/P3 allowed |
| data generation | Are slot patterns balanced? | feature-grid counts | every `(slot,B)` has equal variants | data count rows | step0 diagnostics trusted |
| initialization | Are R routers random and bias-free? | router stats | bias absent, row hashes recorded | init rows | P2 trusted |
| P1 | Does pattern/source change `c` and load? | common/source table | source/load changes reported | P1 figure | mechanism source updated |
| P2 | Does common score predict dominant expert? | argmax agreement table | agreement > random baseline supports | P2 figure | causal intervention justified |
| P3 | Does cancellation reduce collapse without hurting accuracy? | load/accuracy over steps | lower load + preserved accuracy supports | P3 figures | next decision |

## 8. Pass / Fail Criteria

Supported:

```text
P1: common source perturbation changes common_ratio / source alignment / step0 load.
P2: common-score argmax predicts step0 dominant expert above 25% random baseline.
P3: logit cancellation lowers early/final max_load or collapse rate while preserving target accuracy.
```

Weakened:

```text
common-score argmax does not predict dominant expert;
or cancellation leaves early/final load unchanged.
```

Redirected:

```text
cancellation balances load but target accuracy drops;
or repeated pattern improves but distributed_complex does not, requiring a narrower pattern-specific claim;
or short local runs are inconclusive, requiring ACP full run.
```

## 9. Result Location

Project-local result record:

```text
Projects/from-attention-to-search/main/experiments/A05/A05_03_uniform_collapse_common_offset/
```

Code workspace output:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a05_03_uniform_collapse_common_offset/
```

## 10. Execution Boundary

The local environment reports CUDA unavailable. Therefore:

```text
step-0 P1/P2 diagnostics can be complete locally;
P3 training can run locally as a CPU mechanism run;
full 4-card training should be queued separately if CPU runtime prevents completing all protocol steps at full length.
```

The final report must state which of these actually completed.
