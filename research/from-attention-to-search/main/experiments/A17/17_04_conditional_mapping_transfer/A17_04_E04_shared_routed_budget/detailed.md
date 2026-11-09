# Detailed: A17_04_E04 bounded qualification

Primary Anchor: [A17_04_02](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_02_shared_routed_budget_anchor.md).
Frozen Protocol: [registered copy](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md), SHA256 `ecdc6ef8fc04c7332198569ac58204f178bf2da86858594f7546ba696da9810b`.
Summary: [summary.md](summary.md).
Eligibility: ELIGIBLE engineering and BOUNDED single-seed acquisition; formal utility NOT_RUN。

## 0. Quick Recap

Purpose: qualify implementation and both mappings. Engineering PASS, learning qualification NOT_PASSED in all five arms. Do not infer separation utility. Next decision: which bounded qualification repair to adopt.

## 1. Definitions

| Object | Meaning / computation | Boundary |
|---|---|---|
| Shared base | Exact Base plus E03 acquired-old q/k/v/o; all frozen | Same in all arms |
| Shared increment | Factors active in both modes | Sharing permissions, not identified common semantics |
| Private increment | Factors active for one visible input mode | Known-mode allocation, not learned routing |
| Rule margin | log p(correct) − log p(opposite endpoint), nat | Mean can hide weak conditions |
| Qmin | Minimum accuracy of8 cells, each200 DEV answers | Qualification threshold95% |
| Candidate choice CE | −log[p(correct)/candidate mass] | Separates access from selection |

## 2. Anchor and decision

This prerequisite protects the parent sharing/separation decision from interpreting learning failure as architecture utility. Researcher scientific acceptance remains Unknown.

## 3. Conformance and deviations

| Contract | Actual | Status / scope |
|---|---|---|
| Three main plus2 rank controls |5 arms, seed29 |PASS for pilot;3-seed formal NOT_RUN |
| Main parameter counts |163,840 each |PASS |
| Active counts S/U/H |163,840/81,920/122,880 |PASS; deliberately unequal |
| Data exposure |Each pilot1200×20, old/new12,000 each |PASS |
| Compute |Main relative spread2.7229207703621487e-7 |PASS matrix FLOPs; no wall-time equality claim |
| Original freeze |Same original-parameter digest before/after every case |PASS, source byte hash and per-step versions |
| Resume |5 independent Smoke step1→2 replays |PASS; pilot240 continuation restores actual state, no uninterrupted241 reference |
| Backend |FP32 eager; parent used SDPA |Clarified before freeze, common new-arm setting |
| Pilot stopping |All fail240; all continue1200 |Matches bounded authorization |
| Mixed GPU check |5 synthetic nonzero-bank cases, zero optimizer steps |Supplemental engineering check, recorded separately; max difference5.43594e-5≤1e-4 |
| Formal utility/local interventions |Not submitted/not run |NOT_RUN, not silently replaced by pilot |

No rank/LR changes, retries, seed substitutions, outlier exclusions or TEST evaluation. The supplementary read-only check ran through ACP exec on the same reserved node; it did not change saved/training states.

## 4. Actual Setup

Frozen acquired-old Qwen3-0.6B, final-layer rank bank; all other parameters frozen.
Joint view:4800 TRAIN/1600 exposed DEV; mode partitions2400/800 each. Source labels: mode1甲FIRST乙LAST, mode2甲LAST乙FIRST. Both mode prefixes visible, target not supplied. Sampler: five lists × two commands × two modes; microbatch5, accumulation4, DP1; CE sum/20.
AdamW1e-4, betas(.9,.999), eps1e-8, decay0, global clip1, constant schedule, zero-B initialization/gain1. Same paired seed/order; rank masks S16all, U8old0–7/new8–15, H8shared0–7/old8–11/new12–15, controls real rank8/12 padded to16.
Milestones0/1/16/50/120/240/600/1200. Smoke8/arm. Pilot1200/arm. Source/config/view identities in [freeze.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/freeze.json), with exact old1200 member. Runtime: four H10080GB, PyTorch2.3.0a0+6ddf5cf85e.nv24.04/CUDA12.4, independent GPU lanes, TF32off, dropoutoff.

Independent exposure reconstruction: every pilot processed489,600 non-padding prefix tokens and500,410 padded token positions, in addition to its24,000 counted answer targets. All five totals and complete ordered record IDs match. Prefix/padding counts measure work and are not added to the answer-only target axis.

## 5. Metrics and rules

Full-vocabulary accuracy, answer CE, correct/opposite margin, candidate mass and candidate choice CE. Learning qualification is eight-cell minimum≥95%; formal utility additionally needs three seeds and its separate gain/non-regression guards, which are NOT_EVALUATED here.

## 6. Evidence Lineage

| Question | Criterion | Raw / independent evidence | Observation | Eligibility |
|---|---|---|---|---|
| Engineering |Budget/mask/freeze/exposure/replay |[Smoke verdict](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/smoke_verdict.json); per-case scope/guards/TB verification |5 PASS |ELIGIBLE engineering |
| Both rules learned |All8 cells≥95% |[Raw-record audit](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json) from40 pilot evaluations |Qmin45.5%–78.5% at1200 |BOUNDED acquisition |
| Identical exposure/order |20 targets/update,10 each |Independent metrics+record lookup |5 same1200-window orders and prefix/padding totals |ELIGIBLE matching |
| Actual saves |Saved weights/optimizer/counters |[Tensor audit](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_tensor_audit.json) after registration |55 states PASS |ELIGIBLE saves, not learning |
| Allocation utility |Qualified3-seed comparisons |No formal run |NOT_RUN |Cannot adjudicate |

## 7. Results

### 240 updates /4800 targets

| Arm | Old accuracy | New accuracy | Old CE | New CE | Old margin | New margin | Weakest cell |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fully shared16 | 89.625% | 45.375% | 0.339318 | 1.788583 | 2.524 | -0.637 | 1.00% |
| Private8/8 | 100.000% | 50.000% | 0.000702 | 1.765268 | 17.768 | -0.042 | 1.50% |
| Shared8 + private4/4 | 100.000% | 49.875% | 0.007010 | 1.620648 | 8.467 | -0.044 | 1.50% |
| Shared8 control | 90.375% | 42.500% | 0.355196 | 2.374215 | 2.982 | -1.172 | 0.00% |
| Shared12 control | 88.250% | 45.250% | 0.374472 | 1.958276 | 2.480 | -0.769 | 1.00% |


### 1200 updates /24000 targets

| Arm | Old accuracy | New accuracy | Old CE | New CE | Old margin | New margin | Weakest cell |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fully shared16 | 99.750% | 87.500% | 0.011851 | 0.332006 | 11.581 | 5.929 | 75.00% |
| Private8/8 | 100.000% | 84.375% | 0.000054 | 0.411580 | 21.647 | 2.918 | 71.50% |
| Shared8 + private4/4 | 100.000% | 89.750% | 0.000852 | 0.275144 | 15.131 | 5.006 | 78.50% |
| Shared8 control | 99.125% | 72.750% | 0.033712 | 0.649917 | 9.342 | 3.236 | 45.50% |
| Shared12 control | 99.500% | 84.375% | 0.017920 | 0.416978 | 11.091 | 4.732 | 69.00% |


### Separate unseen panels at1200

| Arm | Mode | Panel | Accuracy | CE | Rule margin | Candidate mass | Candidate choice CE |
|---|---|---|---:|---:|---:|---:|---:|
| Fully shared16 | old | order_new | 99.500% | 0.013964 | 11.703 | 99.977% | 0.013739 |
| Fully shared16 | old | combination_new | 100.000% | 0.009738 | 11.458 | 99.976% | 0.009492 |
| Fully shared16 | reversed | order_new | 86.500% | 0.319916 | 6.082 | 98.674% | 0.305415 |
| Fully shared16 | reversed | combination_new | 88.500% | 0.344096 | 5.775 | 99.248% | 0.336273 |
| Private8/8 | old | order_new | 100.000% | 0.000095 | 21.920 | 100.000% | 0.000095 |
| Private8/8 | old | combination_new | 100.000% | 0.000013 | 21.374 | 100.000% | 0.000012 |
| Private8/8 | reversed | order_new | 85.250% | 0.369947 | 2.979 | 97.219% | 0.339399 |
| Private8/8 | reversed | combination_new | 83.500% | 0.453213 | 2.857 | 97.446% | 0.426046 |
| Shared8 + private4/4 | old | order_new | 100.000% | 0.001088 | 15.371 | 99.998% | 0.001067 |
| Shared8 + private4/4 | old | combination_new | 100.000% | 0.000616 | 14.891 | 99.990% | 0.000516 |
| Shared8 + private4/4 | reversed | order_new | 92.250% | 0.225965 | 5.156 | 98.445% | 0.208485 |
| Shared8 + private4/4 | reversed | combination_new | 87.250% | 0.324322 | 4.855 | 98.817% | 0.311723 |
| Shared8 control | old | order_new | 98.500% | 0.040934 | 9.231 | 99.923% | 0.040156 |
| Shared8 control | old | combination_new | 99.750% | 0.026490 | 9.454 | 99.883% | 0.025278 |
| Shared8 control | reversed | order_new | 70.500% | 0.674809 | 3.323 | 94.483% | 0.612300 |
| Shared8 control | reversed | combination_new | 75.000% | 0.625024 | 3.150 | 95.116% | 0.571464 |
| Shared12 control | old | order_new | 99.250% | 0.022083 | 11.155 | 99.943% | 0.021512 |
| Shared12 control | old | combination_new | 99.750% | 0.013757 | 11.027 | 99.953% | 0.013281 |
| Shared12 control | reversed | order_new | 83.250% | 0.409357 | 4.873 | 98.191% | 0.389933 |
| Shared12 control | reversed | combination_new | 85.500% | 0.424600 | 4.591 | 98.654% | 0.410415 |

### Eight qualification cells at1200

| Arm | Cell | Accuracy |
|---|---|---:|
| S16 | old/甲/order_new | 99.50% |
| S16 | old/甲/combination_new | 100.00% |
| S16 | old/乙/order_new | 99.50% |
| S16 | old/乙/combination_new | 100.00% |
| S16 | reversed/甲/order_new | 98.00% |
| S16 | reversed/甲/combination_new | 98.50% |
| S16 | reversed/乙/order_new | 75.00% |
| S16 | reversed/乙/combination_new | 78.50% |
| U8 | old/甲/order_new | 100.00% |
| U8 | old/甲/combination_new | 100.00% |
| U8 | old/乙/order_new | 100.00% |
| U8 | old/乙/combination_new | 100.00% |
| U8 | reversed/甲/order_new | 94.00% |
| U8 | reversed/甲/combination_new | 95.50% |
| U8 | reversed/乙/order_new | 76.50% |
| U8 | reversed/乙/combination_new | 71.50% |
| H8 | old/甲/order_new | 100.00% |
| H8 | old/甲/combination_new | 100.00% |
| H8 | old/乙/order_new | 100.00% |
| H8 | old/乙/combination_new | 100.00% |
| H8 | reversed/甲/order_new | 96.50% |
| H8 | reversed/甲/combination_new | 96.00% |
| H8 | reversed/乙/order_new | 88.00% |
| H8 | reversed/乙/combination_new | 78.50% |
| S8 | old/甲/order_new | 97.50% |
| S8 | old/甲/combination_new | 100.00% |
| S8 | old/乙/order_new | 99.50% |
| S8 | old/乙/combination_new | 99.50% |
| S8 | reversed/甲/order_new | 95.50% |
| S8 | reversed/甲/combination_new | 97.00% |
| S8 | reversed/乙/order_new | 45.50% |
| S8 | reversed/乙/combination_new | 53.00% |
| S12 | old/甲/order_new | 99.50% |
| S12 | old/甲/combination_new | 100.00% |
| S12 | old/乙/order_new | 99.00% |
| S12 | old/乙/combination_new | 99.50% |
| S12 | reversed/甲/order_new | 97.50% |
| S12 | reversed/甲/combination_new | 98.50% |
| S12 | reversed/乙/order_new | 69.00% |
| S12 | reversed/乙/combination_new | 72.50% |

Each cell has200 answers. Each panel has400 per mode; combined mean equals equal panel weighting. All values are raw unsmoothed single-seed observations.

## 9. Stage failure decomposition

Engineering succeeds; operational learning qualification fails. Model/library failure, obvious mask/freeze errors and unequal exposure are not supported explanations. Rank capacity, factorized optimization/update scale and generalization remain unresolved. Only final mini-batch losses are available here as training-loss examples; no complete seen-TRAIN accuracy evaluation ran, so do not diagnose memorization as established.

## 10. Round record

1. Question: five-arm implementation and two-rule qualification.
2. Setup: same frozen old state, masks/rank allocation only, fixed optimizer.
3. TRAIN: joint view and exact equivalent mode partitions.
4. DEV: unseen order/combination exposed panels; no TEST truth.
5. Result: engineering PASS, acquisition NOT_PASSED; registered actual assets.
6. Boundary/next: no formal utility verdict; choose one bounded qualification repair.

## 11. Interpretation

Private routing protects parameter access, but protection alone does not solve new-rule acquisition. Hybrid performs best on mean new accuracy here yet is not qualified. The restricted factor family is a new learning configuration; parent full-matrix joint success does not qualify it automatically.

## 12. Claim boundary

Can report implemented masks/counts, matched supervised exposures, near-perfect old retention, partial new acquisition and failed95% floor. Cannot claim separation utility, unique/common semantic experts, learned routing, rank impossibility or natural-task generalization.

## 13. Next decision

Researcher decision: which bounded qualification repair to adopt. AI suggestion: keep data/code, test update-scale and rank separately. Formal remains held; no repair run was submitted.

## 14. Artifact manifest

[Machine-readable artifact manifest](artifact_manifest.json) binds sources, freeze, raw records, independent audits and actual registration. Two data-view IDs;10 output families containing55 real checkpoint members. [Strict actual output access](../../../../../../../assets/checks/2026-10-12_a17_e04_actual_checkpoints.json).
Saved states: `<run>/smoke/seed_29/<arm>/checkpoints/` and `<run>/pilot/seed_29/<arm>/checkpoints/`. Smoke saves0/1/8 (15 states); pilot saves0/1/16/50/120/240/600/1200 (40 states). External reference step2 files are replay artifacts, not extra checkpoint members. Five source-profile backward computations and one rolled-back isolation step are engineering overhead, excluded from pilot update exposure and separately bounded.

## 15. Execution sources

Job `pt-1rb3s2t0`, completed successfully2026-10-12T05:53:32Z. [Certificate](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/execution_certificate.md).
Runner: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/orchestrate.py`.
Worker: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/run_bank.py`; bank: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/bank.py`.
Config: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/config.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/config.json).
Registered body: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/registered_protocol.md).
Dataset: [/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1/manifest.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1/manifest.json).
Raw evals: `<run>/pilot/seed_29/<arm>/eval_<step>.json`; metrics: `metrics.jsonl`.
Independent record/profile verification: [independent_results.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/independent_results.json).
Additional mixed checks: [additional_mixed_gpu_checks.json](/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/runs/qualification_20261012T053102Z/additional_mixed_gpu_checks.json), producer `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/source/additional_mixed_checks.py`, independent of training source freeze.
Reproduce only under new authorization: source runtime then `python source/orchestrate.py --config <frozen_config> --run <NEW_ROOT>`; do not overwrite this completed run or treat this text as run approval.
