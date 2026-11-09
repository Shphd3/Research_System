# Tulu answer-only SFT replication

All20 condition/seed models completed504updates/256644 valid answer targets each on one4-H100 Reserved node (job pt-ihan2rw2). Three read-only agents audited supervision, mixture assets and comparison logic; every cached label/position was checked. This is frozen-Base final-residual expert adaptation, not full-model SFT.

Purpose: test whether the routing/learning discrepancy persists after moving from DCLM next-token prediction to instruction-answer SFT, and whether group calibration helps against original-score and size-matched random controls. The rival is that distribution/task changes alone are insufficient and finite-data optimization/generalization remains limiting.

Model: frozen Qwen3-0.6B Base, joint14-layer/F16384 CrossCoder and original norm/head. Eight full1024-wide SwiGLU experts are added after block28 residual-post and before final RMSNorm; top1,25165824 trainable expert parameters; learned-router references add8192. Keep original T/R11 lists and reference-low964; estimate only calibration and branch scale on new TRAIN.

Data: pinned Tulu-v2 mixture revision6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752;1024TRAIN/128DEV/256EVAL first-turn pairs,85548/10340/22446 answer targets. Normalized-prompt hash isolation; prompt≤256, answer8–256tokens with EOS, no answer truncation. Only answer/EOS targets; prompt/padding excluded. Ten TRAIN source tags, includingCoT andCodeAlpaca; no separately added GSM8K. Near-duplicate and Base-pretraining contamination Unknown.

At the fixed epoch3 endpoint,20/20 models have higher overall NLL and20/20 higher reference-low macro NLL than frozen Base (1.242698/1.218116). Some overall curves improve at epoch1 then rebound; do not select that epoch post hoc. S1 fails the joint practical comparison against S0 and R11-S1. Exact paired deltas and descriptive dialogue-bootstrap intervals are in tables/paired_comparisons.csv; all conditions, including negative extensions, are retained.

Calibration still changes reception without establishing learning benefit. 960/964 reference-low features are EVAL-estimable; missing support stays NA. Old-reference frequency is not automatically SFT rarity or knowledge difficulty. Dataset, format, mask, calibration and exposure budget change jointly, so this does not uniquely identify DCLM or format novelty as the old cause. Answer NLL is not generation accuracy, capacity or phi-grouping utility.

AI interpretation: replacing data with this SFT subset is not a sufficient repair; finite-data over-updating is compatible with observed curves but not uniquely identified. One suggested next check is a common DEV-selected budget, frozen before a new problem-isolated holdout comparison ofT_S0/T_S1/R11_S1. It was NOT RUN. Human scientific judgment remains Unknown.

[Full Chinese record](detailed_cn.md) · [Protocol](protocol.md) · [All endpoints](tables/all_condition_results.csv).
