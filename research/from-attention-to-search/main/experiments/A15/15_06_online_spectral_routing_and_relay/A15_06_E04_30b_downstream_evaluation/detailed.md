---
experiment_id: A15_06_E04_30b_downstream_evaluation
status: complete
scientific_verdict: fail_broad_transfer_with_task_specific_local_hmt_gains
last_updated: 2026-08-09
---

# A15_06_E04 detailed evidence ledger

## 1. Registered question

Do the six immutable seed-17 30B models differ on the eight requested
zero-shot downstream benchmarks, and do task results agree with or qualify the
held-out-DCLM NLL ordering?

## 2. Model endpoints

All arms are four-layer H768, eight-sparse-plus-one-shared-expert, top-1 DCLM
MoEs evaluated at optimizer step 38,147 = 30,000,021,504 tokens.  The six model
SHA-256 values are frozen in the approved [Protocol](protocol.md) and worker
preflight record.  The exact checkpoint directories are
`/data/250010109/MoE_Router/outputs/online_spectral_router_training/osrt-30b-<arm>-s17/checkpoints/checkpoint-38147/`.

## 3. Evaluation contract

- Evaluator: lm-eval 0.4.12; Transformers 4.53.3.
- Tokenizer: `/data/share/Qwen3-0.6B-Base`.
- Maximum context: 1,024 tokens; zero-shot; no chat template; no added BOS.
- Random, NumPy, Torch, and few-shot seeds: 42.
- Suite SHA-256: `81cf7e1b4b9874e8053d5a9215ccad3dd0667938c7f02e638c402a4521761307`.
- Task versions: ARC-C 1, ARC-E 1, HellaSwag 1, LAMBADA_OPENAI 1,
  PIQA 1, RACE 3, Social IQA 0, WinoGrande 1.
- Samples: 1,172 / 2,376 / 10,042 / 5,153 / 1,838 / 1,045 /
  1,954 / 1,267 in the order above.
- Primary task metrics: normalized accuracy for ARC-C, ARC-E, HellaSwag,
  PIQA; ordinary accuracy for LAMBADA, RACE, SIQA, WinoGrande.

## 4. Remote execution ledger

| Attempt | Job ID | State | Reading |
| --- | --- | --- | --- |
| Initial | `pt-qjq52j6l` | stopped before model load | Cluster-side pyarrow download made no progress; no benchmark evidence |
| Frozen-runtime retry | `pt-axk78fi3` | `SUCCEEDED` | Six Router guards and all six-by-eight raw results written |

The retry staged a deterministic Python 3.12 evaluation layer on shared
storage before submission.  It did not change any checkpoint, task, prompt,
metric, or Router behavior.

## 5. Router evaluation guards

All six guards have status `pass`.  For every layer, native Gate logits replay
with maximum error 0 and top-1 winner agreement 1.0.  Vanilla uses no running
center; all other arms use the saved center.  Local and Relay projected layers
are initialized, nested-basis residuals are below \(7.58\times10^{-4}\), and
removing the projection changes a nonzero fraction of routes.  Relay source
replay error is 0 for both Relay arms.  Router buffers hash identically before
and after full evaluation.

This guard proves that the trained Router variant was active and immutable
during scoring.  It does not prove that its routes were useful.

## 6. Full task evidence

The complete task matrix and evaluator standard errors are in
[task_scores.csv](tables/task_scores.csv).  Figure 1 is the primary reading
surface.

![Task accuracy heatmap](figures/figure1_task_accuracy_heatmap.png)

No non-Centered arm meets the registered breadth rule.  Local-HMT is higher
than Centered on six tasks, ties one, and is lower on one, but only two task
intervals are confidently positive.  The typed broad-transfer verdict is
therefore `fail`, while the ARC-Easy and LAMBADA gains remain valid
task-specific observations.

## 7. Paired item-level inference

Samples are aligned by `(doc_id, doc_hash)`.  For each task, treatment-minus-
reference correctness is bootstrapped 10,000 times.  Full results are in
[paired_vs_centered.csv](tables/paired_vs_centered.csv) and
[mechanism_contrasts.csv](tables/mechanism_contrasts.csv).

![Paired differences versus Centered](figures/figure2_paired_delta_vs_centered.png)

![Registered architecture contrasts](figures/figure4_mechanism_contrasts.png)

Decision-bearing readings:

1. Centered exceeds Vanilla with positive paired intervals on HellaSwag
   (+1.50 points), LAMBADA (+1.65), and PIQA (+3.05).
2. Local-HMT exceeds Centered on ARC-Easy (+1.98) and LAMBADA (+1.30), but no
   other task interval excludes zero.
3. Local-HMT versus Local-Random has no task interval excluding zero; covariance
   rank identity is not certified downstream.
4. Relay-HMT is below Local-HMT on ARC-Easy (-3.20) and LAMBADA (-1.55), with
   no reliable positive task.
5. Relay-HMT versus Relay-Random has no reliable positive task and is lower on
   ARC-Easy (-1.56).

## 8. DCLM-to-downstream comparison

| Arm | 30B DCLM NLL | Max expert share | Mean normalized route entropy | Downstream macro |
| --- | ---: | ---: | ---: | ---: |
| Vanilla-Full | 3.493947 | 0.9979 | 0.3310 | 36.19% |
| Centered-Full | 3.395985 | 0.2927 | 0.9407 | 37.33% |
| Local-HMT | **3.391913** | 0.2427 | 0.9632 | **37.84%** |
| Local-Random | 3.396798 | 0.2264 | 0.9566 | 37.22% |
| Relay-HMT | 3.407530 | 0.3303 | 0.9376 | 37.21% |
| Relay-Random | 3.408655 | 0.3526 | 0.9222 | 36.94% |

![DCLM NLL versus downstream navigation score](figures/figure3_dclm_vs_downstream.png)

The endpoint ordering is qualitatively aligned, especially for collapsed
Vanilla and Local-HMT.  This is a six-point descriptive association, not a
causal or population correlation.

## 9. Source-model LB status

The training configs and logs record `lambda_LB=0.01`.  The A16 shadow-engine
audit subsequently showed that re-entrant activation checkpointing detached
the nested LB auxiliary tensor from the recomputed backward graph: nominal
LM-only and LM+LB branches produced tensor-identical updates until the shadow
engine disabled checkpointing.  Therefore all six source trajectories had LB
telemetry but no effective LB parameter update.  This does not invalidate the
six endpoint models or this evaluation, but it forbids attributing any score
or load difference to LB regularization.

## 10. Plot contracts and visual audit

- **Figure 1:** question: absolute task performance; metric: percentage
  accuracy; rows: arms; columns: tasks; limitation: no uncertainty and macro
  is not a primary score.
- **Figure 2:** question: which arms differ from Centered; metric: paired
  accuracy points; star: paired 95% interval excludes zero; limitation: one
  seed and multiple tasks.
- **Figure 3:** question: whether DCLM and downstream orderings broadly agree;
  axes: DCLM NLL and navigation-only macro accuracy; limitation: six
  non-independent architecture points.
- **Figure 4:** question: which registered architectural change drives a task
  difference; metric: treatment-minus-reference paired accuracy points;
  limitation: task effects do not identify internal expert mechanism.

All four PNGs were opened and visually inspected at native resolution on
2026-08-09.  Axis labels, units, arm/task labels, signs, stars, and color bars
are legible; the Figure 3 label offsets were adjusted after the first visual
audit.

## 11. Artifact map and claim boundary

- Curated tables: `tables/task_scores.csv`, `paired_vs_centered.csv`,
  `mechanism_contrasts.csv`, `breadth_verdict.csv`, `endpoint_dclm.csv`.
- Curated figures: `figures/figure1...figure4...png`.
- Raw 90-MB-per-arm lm-eval JSON, Router guards, environment records, and logs
  remain under
  `/data/250010109/MoE_Router/outputs/online_spectral_router_training/downstream_30b_e04/`.
- Worker implementation and analysis scripts remain under
  `/data/250010109/MoE_Router/experiments/20260809_a15_06_30b_downstream_eval/`.

This experiment supports only task-specific seed-17 30B readings.  It does not
establish universal transfer, covariance-band semantics, Relay utility at
other scale, or expert specialization as the mediator.  The next A15 decision
remains a functional, expert-utility-aligned coordinate test before further
matched training.

