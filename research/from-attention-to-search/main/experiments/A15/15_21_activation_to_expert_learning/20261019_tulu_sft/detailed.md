# Tulu answer-only SFT replication

All20 condition/seed models completed504updates/256644 valid answer targets each on one4-H100 Reserved node (job pt-ihan2rw2). Three read-only agents audited supervision, mixture assets and comparison logic; every cached label/position was checked. This is frozen-Base final-residual expert adaptation, not full-model SFT.

Purpose: test whether the routing/learning discrepancy persists after moving from DCLM next-token prediction to instruction-answer SFT, and whether group calibration helps against original-score and size-matched random controls. The rival is that distribution/task changes alone are insufficient and finite-data optimization/generalization remains limiting.

Model: frozen Qwen3-0.6B Base, joint14-layer/F16384 CrossCoder and original norm/head. Eight full1024-wide SwiGLU experts are added after block28 residual-post and before final RMSNorm; top1,25165824 trainable expert parameters; learned-router references add8192. Keep original T/R11 lists and reference-low964; estimate only calibration and branch scale on new TRAIN.

Data: pinned Tulu-v2 mixture revision6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752;1024TRAIN/128DEV/256EVAL first-turn pairs,85548/10340/22446 answer targets. Normalized-prompt hash isolation; prompt≤256, answer8–256tokens with EOS, no answer truncation. Only answer/EOS targets; prompt/padding excluded. Ten TRAIN source tags, includingCoT andCodeAlpaca; no separately added GSM8K. Near-duplicate and Base-pretraining contamination Unknown.

At the fixed epoch3 endpoint,20/20 models have higher overall NLL and20/20 higher reference-low macro NLL than frozen Base (1.242698/1.218116). Some overall curves improve at epoch1 then rebound; do not select that epoch post hoc. S1 fails the joint practical comparison against S0 and R11-S1. Exact paired deltas and descriptive dialogue-bootstrap intervals are in tables/paired_comparisons.csv; all conditions, including negative extensions, are retained.

Calibration still changes reception without establishing learning benefit. 960/964 reference-low features are EVAL-estimable; missing support stays NA. Old-reference frequency is not automatically SFT rarity or knowledge difficulty. Dataset, format, mask, calibration and exposure budget change jointly, so this does not uniquely identify DCLM or format novelty as the old cause. Answer NLL is not generation accuracy, capacity or phi-grouping utility.

AI interpretation: replacing data with this SFT subset is not a sufficient repair; finite-data over-updating is compatible with observed curves but not uniquely identified. One suggested next check is a common DEV-selected budget, frozen before a new problem-isolated holdout comparison ofT_S0/T_S1/R11_S1. It was NOT RUN. Human scientific judgment remains Unknown.

[Full Chinese record](detailed_cn.md) · [Protocol](protocol.md) · [All endpoints](tables/all_condition_results.csv).

## Reproducibility ledger

Execution root:/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z. Active remote pipeline wall:345.096s; CPU analysis:18.529s, not kernel time. Every model uses3epochs,batch512,micro128,tail44,AdamW3e-4/(.9,.95)/eps1e-8/wd.01,26-update warmup,cosine to.1,clip1. Seeds11/22 share expert initialization and data permutations across conditions. Save stable epoch0/1/2/3 complete training states and64-update recovery states. All20 actual TensorBoard streams pass finite task/total-loss and monotonic valid-target checks ending at256644. Reference-low macro averages per-feature losses before averaging features; overlapping hit positions are not independent knowledge samples.

Source hashes and exact split/filter counts:evidence/manifest.json. Native/cached first-batch logits/NLL error0 on all three splits. All labels and positions pass CPU verification; zero-branch equivalence, expert/router gradients,small-fit and exact next-update replay pass. Parent stale deadline/priority fields and the old smoke-ETA field are explicitly non-operative; see metadata_interpretation.json,without mutating frozen config. Actual outputs/IDs:artifact_manifest.json.

Four figures separate paired fixed-routing learning,learned references,routing reception and source-tag breakdown. Full endpoint/curve/paired/source/dialogue/member/per-feature tables are retained; q/count/load matrices and resumable states stay execution-side. All raw failures and old DCLM results are preserved. No new target-adaptation,spectral grid,full-model tuning,commit or push occurred. Detailed source-level evidence and three-agent audit are in detailed_cn.md/reasoning_audit_cn.md.
