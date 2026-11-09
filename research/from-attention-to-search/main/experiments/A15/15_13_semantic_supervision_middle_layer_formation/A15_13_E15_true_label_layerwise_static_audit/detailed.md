# Detailed Record: A15_13_E15 Gold-label layerwise static audit

Result status: `FULL_RUN_COMPLETE`; knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`
Registered typed verdict: `UNQUALIFIED_SHUFFLE_CONTROL`

## 1. Provenance And Completion

- Worker surface: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit`
- SCO ACP job: `om-kqsc3ncy`
- Platform outcome: `SUCCEEDED`, one replica, zero retries.
- Resource: workspace `share-space`; AEC2 cluster `share-cluster`; SPOT quota; worker spec `n6ls.iu.i40.1`; one NVIDIA H100 80GB HBM3 GPU; 22 vCPU; 240 GiB host memory.
- Image: `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`
- Startup command: `cd /data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit; E15_EXPECTED_GPUS=1 bash scripts/run_remote.sh`
- Runtime: Python `3.12.3`; PyTorch `2.8.0a0+5228986c39.nv25.06`; CUDA `12.9`; Transformers `4.53.3`; NumPy `1.26.4`.
- Remote smoke: `8/8` current regression tests after the verdict repair; the actual pre-run remote smoke executed the then-current `7/7` suite and returned `SMOKE_STATUS=PASS`.
- Full run: three train passes, `768` optimizer updates, complete development evaluation, frozen selector marker, one confirmation evaluation, 2,000 stratified window bootstrap replicates per split, seven audited figures, and five curated tables.
- No 5090, reserved-quota, multi-GPU, SAE, LoRA, language-model update, or expert-training path entered the evidence.

Important hashes:

| Artifact | SHA-256 |
|---|---|
| Full probe checkpoint | `4cfbb8b24f1866e5cae93853262cc3fea1a805ee38834946f48fc012e550c4f3` |
| Development JSON | `89280fd279ef23723dbfccdb4700316367a11e7c5c0c9c5f512b5433b4c4dbc3` |
| Confirmation JSON | `aea8d70ccd295422fe93fd61c686f8fabfcca76b41593d9afe52a8f0f271dba2` |
| Development per-window arrays | `38b7a91449ef5342378b34b538cb28c53309085fde9efdd3c44cb567d3a0cf3b` |
| Confirmation per-window arrays | `844ba556a79e3da39e899f826bd36c419ec09a6b316be2613645e8783aa6f5ba` |
| Frozen development selector | `c2884a91725da1531f90345223a7b74ade3de62a65e6fa620a7698a0d14d19cf` |
| Corrected verdict | `35c369aee29124307a78b9cdbf39b5fdabec9638f73a6bb2fd49f9c1b2946848` |
| Verdict repair record | `736c1ac039d50f8213ca24b30ba6f40f9f141850836606f3c4dcaa5e7880bc6d` |

## 2. Frozen Data, Model, And Tensor

The dataset was `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`, SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`. It contains three parent domains and three child domains inside each parent. Every child contributes 1,024 train, 256 development, and 512 confirmation windows. Every window has 256 tokens. Representation positions 63--254 correspond to next-token targets 64--255. Domain names were never added to inputs, and no token from one window crossed a split.

The model was `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, Hugging Face revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd`. `model.safetensors` SHA-256 was `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; `config.json` SHA-256 was `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`. Before/after hashes agree.

For each zero-indexed block 0--27, a forward pre-hook captured the first input to `decoder_layer.mlp`. The smoke tensor was `[28,2,192,1024]`: 28 layers, two windows, 192 current-token positions, hidden width 1,024. No prefix average, window average, layer output, cross-layer center, or coarse-direction subtraction was evaluated.

## 3. What Was Trained

Training was **not staged**. One stage fitted mutually independent probe families together in a single streaming base-model pass:

| Item | Actual execution |
|---|---|
| Trainable objects | `6,353,788` probe parameters: real and shuffled affine heads, five smaller nested-budget affine sets, fixed-width nonlinear heads, and three leave-one-child-out parent heads |
| Frozen objects | all `596,049,920` Qwen3 parameters and the language head; `0` trainable base parameters |
| Passes and updates | 3 deterministic passes; 256 balanced updates per pass; `768` updates total |
| Batch and accumulation | 36 windows per update, four per parent-child cell; no gradient accumulation |
| Objective | sum of each independent head's three-way classification cross-entropy; because parameter sets do not overlap, the sum only shares the frozen representation pass |
| Learning rates | affine heads `1e-3`; nonlinear heads `3e-4`; AdamW weight decay `1e-4`; no scheduler or early stopping |
| Checkpoint rule | final optimizer update only; SPOT resume state atomically replaced after every update |
| Handoff | evaluate development; write code/checkpoint/development/subset hashes and `(9,9)` candidates; then evaluate confirmation exactly once |

The run used initialization/order seed `170903`, bootstrap seed `170904`, label-shuffle seed `170905`, and nested-budget seed `170906`. Nested per-cell counts were exactly `10, 51, 102, 256, 512, 1024`, and every smaller subset was contained in every larger one. Each leave-one-child-out fold trained on 6,144 windows and excluded the same local child index from all three parents.

## 4. Metrics And Selector

For every layer, token classification cross-entropy was averaged first inside each window. Window values were averaged inside each of the nine parent-child cells, and the nine cell means were then averaged equally. Accuracy used the same order. The margin was true-class logit minus strongest wrong-class logit; its reported 5th percentile is over balanced held-out windows.

With random three-way CE \(\log3\), recovery was

\[
R_\ell=\frac{\log3-\mathrm{CE}_\ell}{\log3-\min_m\mathrm{CE}_m}.
\]

The selector was the earliest block whose own and next two recovery values were all at least `0.95`. Development froze this rule before confirmation. The bootstrap resampled complete windows with replacement inside all nine cells, retaining every selected window's 192 positions.

## 5. Primary Results

### 5.1 First stable layers

| Split | Task | Block | Recovery at blocks 9, 10, 11 | Bootstrap selection rate | 95% interval |
|---|---|---:|---|---:|---|
| Development | Parent | `9` | `1.000000, 0.986399, 0.966900` | `1.000` | `[9,9]` |
| Development | Conditional child | `9` | `1.000000, 0.995349, 0.970083` | `1.000` | `[9,9]` |
| Confirmation | Parent | `9` | `1.000000, 0.988717, 0.966612` | `1.000` | `[9,9]` |
| Confirmation | Conditional child | `9` | `1.000000, 0.994273, 0.968259` | `1.000` | `[9,9]` |

Both splits therefore have descriptive layer gap `0`, bootstrap median and 95% interval `[0,0]`, both-candidate-defined rate `1.000`, and \(P(\ell_f-\ell_c\geq2)=0.000\).

### 5.2 Block-9 held-out performance

| Split | Task | CE | Balanced accuracy | Margin 5th percentile |
|---|---|---:|---:|---:|
| Development | Parent | `0.471644` | `0.819519` | `-0.457606` |
| Development | Conditional child | `0.378842` | `0.857976` | `-0.520469` |
| Confirmation | Parent | `0.482906` | `0.812298` | `-0.582999` |
| Confirmation | Conditional child | `0.363137` | `0.864030` | `-0.266432` |

![Primary layerwise recovery](figures/01_primary_linear_recovery.png)

How to read: both tasks cross the same registered three-block window at block 9; this is descriptive evidence against a coarse-before-fine depth gap.

## 6. Nonlinear, Sample, Position, And Abstraction Audits

The fixed `1024 → 32 → 3` GELU heads also select block `9` for both tasks and splits. Block-9 linear-minus-nonlinear CE gaps were parent `+0.013149/+0.011629` and conditional child `-0.000588/+0.000090` on development/confirmation. No nonlinear-only earlier candidate exists.

At block 9, the smallest nested budget recovering 95% of the full-data gain was 25% for parent and 50% for child on both splits. The child candidate is sample-fragile; the parent candidate is not sample-fragile under the registered `>25%` threshold.

Every one of the early 63--126, middle 127--190, and late 191--254 position bins selects block `9` for parent and conditional child on both splits. Neither candidate is position-fragile.

Leave-one-child-out parent readout selects no stable layer in any of the three folds or their mean. Mean block-9 CE was `1.280881` on development and `1.312866` on confirmation; the best mean was still `1.193947/1.226787` at block 6, worse than random `1.098612`. Parent readability is child-identity-fragile.

![Sample efficiency](figures/03_sample_efficiency.png)

How to read: the child readout requires the 50% row at block 9 to recover nearly all of its full-data improvement, whereas the parent readout reaches that criterion at 25%.

![Position robustness](figures/05_position_robustness.png)

How to read: all three position-bin curves cross the stability threshold together at block 9; the onset is not a late-token-only artifact.

![Leave-one-child-out](figures/06_leave_one_child_out.png)

How to read: the held-out-child CE curves remain worse than random even though the standard readout is strong, so the parent signal does not transfer to unseen children in this audit.

## 7. Readout Geometry

At block 9, parent Fisher eigenvalue sums were `2.082556` on development and `2.013094` on confirmation. Mean conditional-child sums were `4.477566` and `4.541372`. The trained weight subspaces are the same across evaluation splits; their parent-versus-child normalized overlaps were `0.040516`, `0.079681`, and `0.068373`. Corresponding principal-angle pairs were `[73.47°,89.58°]`, `[71.97°,75.40°]`, and `[68.96°,84.91°]`. Pairwise child-head overlaps were `0.047132`, `0.023603`, and `0.026275`.

These values diagnose compact held-out class separation and near-orthogonal fitted decision directions. They do not estimate LoRA rank, establish causal use, or require different insertion depths.

![Fisher and subspace audit](figures/04_fisher_and_subspace.png)

How to read: both task families have their strongest discriminant peak around block 9--10, while the parent/child fitted row spaces have low overlap; strength and direction differ, but onset depth does not.

## 8. Shuffled-Label Qualification

The Protocol required both tasks on both splits to have across-layer median shuffled accuracy in `[0.28,0.39]`, median shuffled CE within `0.05` nat of \(\log3\), and no stable shuffled onset.

| Split | Task | Median accuracy | Median CE | \(\mathrm{CE}-\log3\) | Shuffled onset | Result |
|---|---|---:|---:|---:|---|---|
| Development | Parent | `0.298621` | `1.132845` | `+0.034232` | none | pass |
| Development | Conditional child | `0.316059` | `1.148097` | `+0.049485` | none | pass |
| Confirmation | Parent | `0.297037` | `1.133857` | `+0.035245` | none | pass |
| Confirmation | Conditional child | `0.313740` | `1.148744` | `+0.050132` | none | **fail** |

The confirmation conditional-child value is `0.000132` above the allowed upper edge `1.148612`. This is numerically tiny and does not resemble positive shuffled-label decoding: accuracy is close to one third and no stable layer exists. It is nevertheless a pre-registered hard qualification miss, so the evidence cannot receive the otherwise descriptive `NO_STAGGERED_LAYER_SUPPORT` verdict.

![Shuffle qualification](figures/07_shuffle_control.png)

How to read: confirmation fails only the median-CE edge, shown in the lower-right panel; the accuracy and stable-onset guards pass.

## 9. Failure, Warning, And Repair Ledger

No attempt or negative control was deleted.

| Item | Outcome | Cause or observation | Treatment |
|---|---|---|---|
| Old job `om-kpp7frgn` | stopped, zero replicas, no evidence | earlier 4×5090 request was superseded by the user's one-H100-SPOT instruction | preserved as historical submission log; excluded from evidence |
| Job `om-kqsc3ncy` | succeeded | one H100 SPOT, zero retries | canonical execution |
| CuBLAS warnings | warning only | runtime did not set `CUBLAS_WORKSPACE_CONFIG`, so GPU operations are not promised bitwise deterministic despite deterministic-algorithm warnings | no rerun or seed change; recorded as a reproducibility limitation |
| Initial verdict derivation | incorrectly wrote `NO_STAGGERED_LAYER_SUPPORT` | the support branch checked null qualification, but other scientific branches omitted the same prerequisite | regression test added first; derived verdict corrected to `UNQUALIFIED_SHUFFLE_CONTROL`; raw development, confirmation, per-window arrays, checkpoint, and confirmation pass were not changed or rerun |
| Leave-one-child-out figure | visually unstable recovery scale | recovery denominator was small while CE stayed above random | figure changed to raw CE with random baseline; raw analysis unchanged |
| Shuffle figure | accuracy alone hid the CE-edge failure | the decisive guard also depends on CE | figure changed to show both registered quantities and split pass/fail; raw analysis unchanged |

The execution code hash frozen before confirmation is `29a9b2c895158a5ab5e6526aa741868ebfc278782058c43af42f7f8b94e304e0`. The repaired verdict-derivation code hash is `34a626f4dfbd4e1e8aeb8342eefd7811754ceb5f9849dc4b724015ac640bd3d5`. `verdict_derivation_repair.json` records all four unchanged raw-artifact hashes and `confirmation_reexecuted=false`.

## 10. Verdict And Claim Boundary

### Registered verdict

`UNQUALIFIED_SHUFFLE_CONTROL`.

### Descriptive observation beneath the guard

The fixed run estimates `(\ell_c,\ell_f)=(9,9)` on both splits, with `[9,9]` intervals and zero probability of a two-block fine delay. It also finds block 9 position-robust, the child readout sample-fragile, and the parent readout child-identity-fragile.

### Can claim

1. The exact current-token MLP-input tensor contains strong trainable real-label information around block 9 under this fixed readout and seed.
2. No coarse-before-fine delay appears in either raw split or any of 2,000 bootstrap samples.
3. The ordinary parent readout does not generalize to unseen child identities, and conditional-child readout needs more data than parent readout.
4. The complete experiment fails its pre-registered confirmation null-control qualification by `0.000132` nat.

### Cannot claim

1. A qualified block `(9,9)` insertion recommendation.
2. That an online Router can reproduce the readout.
3. That any block's LoRA experts acquire distinct function.
4. Any next-token likelihood, capability, or efficiency gain.
5. That low probe-direction overlap implies different optimal LoRA ranks or depths.

### One proposed next decision, awaiting human confirmation

Decide whether to authorize one fresh-seed replication of the same frozen static audit to adjudicate the null-control edge miss. Unless that run passes the unchanged qualification gates and reproduces `(9,9)`, do not begin the matched-budget Oracle LoRA test.

## 11. Artifact Map

- Worker code: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/scripts/`
- Smoke and full logs: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/logs/`
- Reloadable heads and resume state: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/checkpoints/`
- Raw JSON and per-window arrays: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/artifacts/`
- Worker figures and tables: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/figures/` and `/data/250010109/MoE_Router/experiments/20260903_a15_13_e15_true_label_layerwise_static_audit/tables/`
- Canonical curated tables: [tables](tables)
- Canonical figures: [primary recovery](figures/01_primary_linear_recovery.png), [linear versus nonlinear](figures/02_linear_vs_nonlinear.png), [sample efficiency](figures/03_sample_efficiency.png), [geometry](figures/04_fisher_and_subspace.png), [position robustness](figures/05_position_robustness.png), [leave-one-child-out](figures/06_leave_one_child_out.png), and [shuffle qualification](figures/07_shuffle_control.png)
