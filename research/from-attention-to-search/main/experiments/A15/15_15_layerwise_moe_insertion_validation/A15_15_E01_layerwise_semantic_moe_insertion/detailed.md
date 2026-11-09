# Detailed Evidence: A15_15_E01 Layerwise Semantic MoE Insertion

## 1. Provenance And Status

- Anchor: [A15_15](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md)
- Frozen execution contract: [protocol.md](protocol.md)
- Eligible ACP job: `pt-lxue71oe`
- Ineligible pre-training attempt: `pt-owrlkt10`
- Worker root: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion`
- Eligible run root: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion/runs/full-20260904T011100Z`
- Resource: one ACP node, reserved quota, `4× NVIDIA H100 80GB`, worker spec `n6ls.iu.i40.4`
- Completion state: `FULL_RUN_COMPLETE`
- Result wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

The first ACP job passed its then-current 11 tests but stopped before any training checkpoint. The frozen-gradient audit had enumerated newly injected adapter parameters through `backbone.parameters()` and incorrectly called their expected gradients a frozen-base violation. The repair records original base-parameter identities before injection and audits only those parameters. A regression test first reproduced the failure; the repaired suite passed `12/12`. The replacement job restarted from update zero and passed the causal-prefix, frozen-base, forced-path, and unit-coefficient smoke guards.

## 2. Data And Fixed Objects

The layer comparison uses the balanced M2D2-Wikipedia `3×3` tensor at `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`, SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`. Each of nine parent-child cells has 1,024 training, 256 development, and 512 confirmation windows. Sequence length is 256; positions 0--63 are context and targets 64--255 contribute standard causal next-token cross-entropy.

The Flat Oracle uses the frozen E14 eight-source answer-only mixture and exact prior splits. Its 1,024 final predictions comprise 512 fixed evaluation items for each seed. Since the training mix contains the evaluation task families, the reported eight-task score is an internal ability diagnostic, not an uncontaminated benchmark-generalization estimate.

Qwen3-0.6B-Base and the language head are frozen. One zero-indexed Transformer block receives the LoRA mixture. Block 1 is the lowest-readability Transformer-block contrast from E15; block 9 is E15's descriptive first stable block for both coarse and conditional-fine readout. E15 itself remains formally unqualified because one confirmation shuffled-child cross-entropy guard missed by `0.000132` nat.

## 3. Architecture And Registered Conditions

At block 1 or block 9, every token activates one shared rank-8 LoRA, one of three parent rank-8 LoRAs, and one of nine child rank-8 LoRAs. The active rank is therefore 24. The six conditions per block and seed are:

| Code | Supervision/path | Child-Router input | Parent experts in stage 2 |
|---|---|---|---|
| `HIER_TASK_R0_F0` | next-token loss only; learned path | native block state | trainable |
| `HIER_ORACLE_R0_F0` | true labels force unit-coefficient path; shadow route loss | native block state | trainable |
| `SEM_R0_F0` | true-label route loss; learned path | native block state | trainable |
| `SEM_R1_F0` | true-label route loss; learned path | centered parent-Router row space removed | trainable |
| `SEM_R0_F1` | true-label route loss; learned path | native block state | frozen |
| `SEM_R1_F1` | true-label route loss; learned path | centered parent-Router row space removed | frozen |

The registered main learned arm is `SEM_R0_F0`. Flat Oracle uses eight rank-24 experts at block 14. The source label forces the expert index; expert output is multiplied by one, not by Router probability. A shadow Router receives route cross-entropy but cannot affect selection or scaling.

## 4. Actual Training Contract

| Stage | Trainable | Frozen | Passes / updates | Objective | Batch and optimizer | Handoff |
|---|---|---|---|---|---|---|
| M2D2 stage 1 | shared LoRA, parent experts, parent Router or Oracle shadow Router | Qwen, language head, child experts, child Router | 2 passes / 144 updates | target-token CE; plus unit-weight parent route CE for semantic/Oracle | microbatch 8, accumulation 16, effective batch 128; AdamW, LR `3e-4`, WD `0.01`, warmup 5, cosine, clip 1 | exact adapter, optimizer, scheduler, update, and RNG state |
| M2D2 stage 2 | shared LoRA, child experts, child Router; parent experts only for `F0` | Qwen, language head, parent Router; parent experts additionally for `F1` | 2 passes / updates 145--288 | target-token CE; plus unit-weight child route CE for semantic/Oracle | same optimizer lineage and batch contract | final checkpoint at update 288 |
| Flat Oracle | eight flat experts and shadow Router | Qwen and language head | 4 passes / 128 updates | answer-token CE plus eight-way shadow route CE | microbatch 8, accumulation 16, effective batch 128; LoRA LR `2e-4`, Router LR `5e-4`, WD `0.01`, warmup 5, cosine, clip 1 | final checkpoint; `911,644` seen answer tokens per seed |

The main task-only model freezes **only the parent Router** at the stage boundary; its parent experts remain trainable. The `F1` ablation freezes both the parent Router and the parent experts.

## 5. Completion Audit

| Required artifact | Expected | Observed |
|---|---:|---:|
| Stage-one checkpoints | 12 | 12 |
| Final layer-study checkpoints | 24 | 24 |
| Layer evaluation arrays | 96 | 96 |
| Flat Oracle checkpoints | 2 | 2 |
| Flat intervention arrays | 6 | 6 |
| Flat benchmark predictions | 1,024 | 1,024 |
| Frozen analysis tables | 5 | 5 |

The immutable checkpoint manifest contains 38 records: 12 stage-one, 24 layer-final, and 2 Flat Oracle checkpoints, each with a SHA-256 digest. The completion audit reports no errors. Six figures were rendered from frozen tables; the three explanatory additions changed no checkpoint, metric, or verdict rule, and the completion audit was rerun successfully.

## 6. Registered Primary Result

For layer \(\ell\), the primary learned-to-Oracle gap is

\[
G_\ell=N^L_\ell-N^O_\ell,
\]

and the selection interaction is

\[
I=G_1-G_9.
\]

Positive \(I\) favors block 9. Seeds are the independence unit.

| Seed | \(N^T_1\) | \(N^L_1\) | \(N^O_1\) | \(G_1\) | \(N^T_9\) | \(N^L_9\) | \(N^O_9\) | \(G_9\) | \(I\) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 17 | 2.867124 | 2.871190 | 2.869271 | 0.001919 | 2.877496 | 2.879535 | 2.878242 | 0.001294 | +0.000625 |
| 29 | 2.866413 | 2.870480 | 2.867970 | 0.002510 | 2.877162 | 2.881097 | 2.877677 | 0.003420 | -0.000911 |
| Mean | 2.866768 | 2.870835 | 2.868620 | 0.002214 | 2.877329 | 2.880316 | 2.877959 | 0.002357 | -0.000143 |

The two interaction signs disagree, so the frozen Pass rule fails and the registered verdict is `INSUFFICIENT`. In addition, task-only NLL is lower than Oracle NLL at both layers: by `0.001852` nat/token at block 1 and `0.000630` at block 9 in the two-seed means. Therefore these two insertion points do not expose a positive M2D2 Oracle task headroom under this exact budget.

## 7. Route Accessibility

| Block | Static coarse recovery | Static fine recovery | Learned coarse accuracy | Learned fine accuracy | Learned joint NMI |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.599087 | 0.662009 | 0.505211 | 0.392819 | 0.067675 |
| 9 | 1.000000 | 1.000000 | 0.686814 | 0.484551 | 0.205000 |

This is a consistent mechanism result: the high-readability block also makes the supervised causal Router more label-aligned. It does not rescue the primary task verdict because semantic agreement is not task improvement.

## 8. Expert Intervention Evidence

Mean confirmation NLL increases after deleting or replacing the selected fine expert are:

| Path | Block | Delete selected | Wrong fine 1 | Wrong fine 2 |
|---|---:|---:|---:|---:|
| Learned semantic | 1 | 0.000100 | 0.000105 | 0.000143 |
| Learned semantic | 9 | 0.000140 | 0.000077 | 0.000109 |
| Forced-gold Oracle | 1 | 0.000970 | 0.001829 | 0.001886 |
| Forced-gold Oracle | 9 | 0.000832 | 0.001015 | 0.001089 |

The learned effects are positive but very small, and block 9 is not larger on both wrong-expert tests. Oracle experts are more functionally non-interchangeable, but their effects are larger at block 1. This fails the block-9 functional guard for seed 29 and prevents a functional layer-selection claim.

## 9. Ablation Effects

All effects below are NLL changes relative to `SEM_R0_F0`; positive is worse.

| Block | Change | Seed 17 | Seed 29 | Mean |
|---:|---|---:|---:|---:|
| 1 | remove row space, parent trainable | -0.000038 | +0.000067 | +0.000015 |
| 1 | freeze parent experts, native input | +0.000928 | +0.000920 | +0.000924 |
| 9 | remove row space, parent trainable | +0.000001 | -0.000004 | -0.000001 |
| 9 | freeze parent experts, native input | +0.000948 | +0.000500 | +0.000724 |

Freezing parent experts has a consistent cost. Row-space removal is effectively zero at block 9 and changes sign at block 1. This reproduces the earlier implementation direction: freeze the parent Router only, continue training parent experts, and retain native child-Router input.

## 10. Flat Oracle Closure

| Model | Seed 17 NLL | Seed 29 NLL | Mean NLL | Mean internal score |
|---|---:|---:|---:|---:|
| Flat task-only | 0.828130 | 0.834529 | 0.831329 | 0.136719 |
| Flat Oracle | 0.827135 | 0.823666 | 0.825400 | 0.152344 |
| Hierarchical task-only | 0.807642 | 0.805004 | 0.806323 | 0.158203 |
| Hierarchical Oracle | 0.796570 | 0.793270 | 0.794920 | 0.165039 |

Flat Oracle improves its matched Flat baseline in both NLL seeds. Its mean shadow-route accuracy is `0.949740`; deletion and wrong-expert interventions increase NLL by `0.083083` and `0.052320`. Thus forced source routing creates real flat-expert dependence. Nevertheless, the hierarchical task-only model remains better than Flat Oracle on both mean NLL and the internal score, and hierarchical Oracle is the strongest upper reference.

## 11. Boundary, Verdict, And Next Decision

Direct result: block 9 improves semantic route accessibility but gives no reproducible reduction in the learned-to-Oracle NLL gap and no uniformly stronger expert function. Typed verdict: `INSUFFICIENT`.

Can claim:

- Flat Oracle is complete and improves over matched Flat task-only.
- Block 9 is more label-accessible to both static probes and the supervised causal Router.
- Freezing parent experts in stage 2 is harmful under both tested layers; row-space removal remains unsupported.

Cannot claim:

- static readability selects the best functional MoE layer;
- block 9 is a task-optimal or globally optimal insertion point;
- route-label agreement itself is expert utility or language-model gain;
- the two-layer, two-seed result defines a monotone depth rule.

One proposed next decision: keep static readability as candidate generation only, then require a cheap functional pilot. A follow-up should add one intermediate-readability layer and two fresh seeds before promoting or rejecting the filter more broadly.

## 12. Artifact Map

- Frozen tables: [`tables/`](tables)
- Audited figures: [`figures/`](figures)
- Worker checkpoint manifest: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion/runs/full-20260904T011100Z/checkpoint_manifest.json`
- Worker logs: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion/runs/full-20260904T011100Z/logs/`
- Worker evaluation arrays: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion/runs/full-20260904T011100Z/evaluations/`
- Worker Flat predictions: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion/runs/full-20260904T011100Z/flat_oracle/benchmark/`
