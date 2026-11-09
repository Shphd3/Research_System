# Detailed: E14-P1 frozen coarse-path intervention

Status: COMPLETE / ELIGIBLE. Registered verdict: `COARSE_CORRECTION_SUPPORTED`.
Knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
[Protocol](protocol.md) · [Summary](summary.md).

## 1. Actual scope and training accounting

This experiment has no training stages, optimizer, learning rate, accumulation, or new checkpoint. All base, output-head, expert and Router parameters were frozen; optimizer updates are zero. Evaluation batch size is 8. Each seed executes five complete 512-example passes: A, C, B, D-shift-1 and D-shift-2. The latter two enumerate wrong children, with eligibility masks for parent sizes (3,3,2); D is their per-example eligible average, not another forward pass. Each pass scores 30,442 answer tokens. No new task-only model, gold Oracle, shuffled-label null or matched deletion was evaluated. A is the baseline, C the privileged pseudo-teacher reference, B the parent correction and D the wrong-child control.

Historical source training was **not staged** for this benchmark branch: only stage 2, 128 optimizer updates, microbatch 8 with accumulation 16. Both seed histories span epochs 0–3 and record 911,644 answer-target token exposures. Base and language head were frozen; shared, parent and leaf LoRA banks and Routers were nominal optimizer members, but the parent Router received no gradient. Objective: answer NLL plus child classification cross-entropy with unit weight. Nominal learning rates: LoRA 2e-4, Router 5e-4 with the historical schedule. Final update 128 is the selected checkpoint, without best-development selection; there is no earlier parent-training stage or stage handoff. Seven saved updates are 1,6,13,32,64,96,128. Current evaluation loads those final tensors unchanged. The separate M2D2 branch does have two stages and is not the treatment under audit.

## 2. Results and analysis

The complete condition table, contrast definitions, intervals and eligible figures are in [Summary](summary.md). Machine-readable sources: [condition table](tables/condition_nll.csv), [contrasts](tables/contrasts.csv), [task-stratified descriptive table](tables/source_nll.csv), [analysis result](tables/results.json).

Primary contrast A−B is 0.039619370 [0.033635655,0.046319138] for seed 17 and 0.021731576 [0.017851930,0.026396028] for seed 29. Both lower bounds exceed zero under the frozen rule. Residual B−C is 0.000708633 and 0.001398138; wrong-child D−C is 0.018794753 and 0.019650431. No equivalence threshold is introduced. Ratios are 0.982428268 and 0.939552293, conditional on this intervention order.

All condition comparisons pair sample IDs, sources and answer-token counts. Analysis uses float64 accumulation of stored per-example losses, including paired differences, avoiding float32 reduction noise. Historical replay compares original stored arrays exactly; float64 display aggregates differ from old float32 aggregates by less than 6e-8 nats/token. This does not change raw losses, evaluation, tolerance or verdict. Bootstrap: 2,000 paired-example draws, NumPy generator seed 20260906, percentile 95%; checkpoints are analyzed separately, not pooled as independent examples. Seed mean is descriptive. No population-of-training-seeds or multiple-testing-adjusted auxiliary claim.

## 3. Execution and immutable evidence

Worker: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention`.
Eligible full run: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/full`.
Analysis: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention/runs/reserved-20260906-p1-v2/analysis`.
Historical run: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z`.
Data: `/data/250010109/datasets/a15_e14_benchmark/processed.pt`.
Base: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.

ACP `pt-5xgwtcam`: SUCCEEDED; start 2026-09-06 09:24:08 UTC (17:24:08 Beijing). One reserved H100 80GB, one `n6ls.iu.i40.1` worker, original NGC 25.06 image. Smoke elapsed 17.825 seconds; full runner elapsed 42.315 seconds, excluding container startup and separate analysis. No automatic retries; 5,400-second process limit. Resource selection was explicitly authorized by the researcher.

Command: `RUN_STAMP=reserved-20260906-p1-v2 timeout 5400 bash <worker>/run_remote.sh`.
Analysis command: `python <worker>/analyze.py --run <eligible-full-run> --output <analysis-directory>`.
Runtime: Python 3.12.3, PyTorch 2.8.0a0+5228986c39.nv25.06, Transformers 4.53.3, NumPy 1.26.4; bf16 frozen base, historical attention implementation. Local analysis uses NumPy 1.24 with float64 accumulation.

[Execution metadata](tables/execution_metadata.json) owns exact source-code, data, pseudo-label and adapter SHA-256 digests and replay/freeze checks. All five evaluation source-code hashes were rechecked after completion. Base safetensors SHA-256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; config: `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`, verified against historical identity before execution.

Raw arrays, logs and checkpoints remain on the worker. Curated metadata, tables and figures only are copied here. No original training code/checkpoint was modified; no commit, push or external publication occurred.

## 4. Actual stage and architecture audit

This audit has no training stages or optimizer. Historical eight-task training used 128 updates, microbatch 8, accumulation 16 and only stage 2. The implementation `_route_loss` returns parent classification cross-entropy in stage 1 and only leaf cross-entropy in stage 2. Hard-pseudo training uses teacher parent/child indices with unit coefficients. Therefore parent logits influence neither the task forward nor the stage-2 auxiliary loss. A tiny backward check confirms absent parent gradients; a diagnostic added parent loss makes them nonzero.

Seven historical snapshots for each seed were compared with final adapter tensors. Parent weights/biases are identical at all seven points; leaf weight/bias changes are nonzero. This directly establishes no observed parent change from update 1 through 128. The code gradient path explains why no parent update is expected from initialization, but the stored-snapshot claim itself begins at update 1.

The original benchmark differs from M2D2: M2D2 actually runs stages 1 and 2, trains the parent in stage 1 and freezes it in stage 2. Do not apply the benchmark hard-pseudo defect to that separate two-stage result without a separate audit.

## 5. Input and target contracts

E14 Router: zero-indexed block 14 pre-forward hidden state, 1,024 dimensions, before same-block attention. E14 adapter input: 3,072-dimensional MLP down-projection input. E15 static audit: layer MLP pre-forward hidden state after attention and normalization. Benchmark teacher: attention-mask-weighted mean of final `hidden_states[-1]` over the full valid sequence, including later answer positions. Parent and leaf supervision are expanded from per-example pseudo assignments and scored on answer prediction positions. Deep current-token states remain causal; whole-window averages have a different information boundary.


## 6. Guards, failures and exclusions

Eligible run: 3/3 regression tests passed, including full outer-model parent forwarding and reset, parent-constrained child reselection, and uneven child-count enumeration. Both-seed smoke and full A/C replay have zero per-example loss error and exact route/source/count identity. All intervention paths are legal; B/C/D use supplied parents; C/D use supplied children. Model parameters have requires-grad disabled and adapter tensors compare exactly before/after. Full matrix is finite; every D average and its alternative counts were independently recomputed from saved arrays.

Excluded local runs: `smoke-v1` failed ONNX/protobuf import; pure-Python protobuf allowed subsequent import. `smoke-v2` batch 2 and `smoke-batch8` failed original A replay at absolute aggregate errors 0.003542423 and 0.007956505 under local PyTorch 2.3/Python 3.10. No local full matrix ran and tolerance remained 1e-4.

Excluded first reserved job `pt-a4qkvyya`, run `reserved-20260906-p1-v1`: original-runtime A/C smoke replay passed exactly but B parent guard failed. The intervention wrapper's base forward cleared the supplied parent. A regression test reproduced it; forwarding the argument through the base call fixed it. That job ended FAILED before replacement. Fresh directory `reserved-20260906-p1-v2` contains the only eligible full run. No failed outputs enter scientific aggregation.

## 7. Architecture evidence and visualization audit

[Architecture JSON](tables/architecture_audit.json), [weight audit](tables/architecture_weight_audit.csv), [gradient audit](tables/architecture_gradient_audit.csv). The gradient diagnostic uses the actual adapter and routing loss with a small squared-output surrogate to inspect task-gradient reachability; it is not a language-model training experiment. The added-parent-loss diagnostic only proves a gradient route exists.

| Figure | Question and computation | Aggregation and display | Allowed conclusion / limitation |
|---|---|---|---|
| `figures/path_intervention.png` | Does supplying the parent reduce answer loss? Stored per-example losses and token counts | Left: A/B/C/D token-weighted NLL by seed; right: paired differences with 95% intervals; nats/answer token | Frozen intervention benefit and wrong-child cost; no deployable training gain, equivalence, or semantic causal claim |
| `figures/architecture_weight_audit.png` | Did historical Router parameters change? Exact snapshot tensors | Max absolute update-1-to-final tensor difference; seed-colored parent/leaf weights and biases | Parent parameters unchanged at stored snapshots; no initialization snapshot or repaired-model performance claim |

Both rendered PNGs inspected: axes, legends, units and labels readable; values trace to tables; zero parent changes are represented on a zero-based axis. Fine differences are visible but their precise values and intervals must be read from the table. No curve smoothing or excluded-run data.

## 8. Boundary and next decision

Teacher is the original pseudo label, not gold Oracle. Full-sequence teacher context is privileged. These are previously examined internal task losses, not uncontaminated generalization scores. The intervention replaces parent identity and consequently downstream computation; its recovery fraction is not a unique decomposition of independent causal effects. No current-layer labels or causal-prefix teacher were tested. The architecture failure prevents attributing the original large deployment gap solely to final-layer semantic mismatch or early readout failure.

AI recommendation pending researcher judgment: step 2 first tests parent-only training with fixed experts and child Router, preserving labels and hook to isolate supervision repair. No step-2 training was started. Human result wording, Focus knowledge update and subsequent protocol are still pending; no delayed daily report is generated.
