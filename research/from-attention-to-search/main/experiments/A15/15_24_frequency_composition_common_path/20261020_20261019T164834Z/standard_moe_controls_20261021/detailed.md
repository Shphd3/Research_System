# Detailed: ordinary top-2 MoE controls

Execution completed for both arms and seeds. Scientific judgment remains `Unknown`. DEV was an exposed review panel. The full factual setup and limits are in [execution amendment 02](execution_amendment_02.md); original frozen records are unchanged.

| Condition | Seed | DEV overall NLL | Low feature macro | High feature macro |
|---|---:|---:|---:|---:|
| BASE |  | 1.248870 | 1.065837 | 1.217222 |
| MoE | 11 | 1.224911 | 1.056263 | 1.190839 |
| MoE | 22 | 1.225059 | 1.052710 | 1.190093 |
| MoE_LB | 11 | 1.226917 | 1.055016 | 1.192933 |
| MoE_LB | 22 | 1.225167 | 1.053284 | 1.190347 |
| T_F | 11 | 1.225300 | 1.053913 | 1.191097 |
| T_F | 22 | 1.226973 | 1.058728 | 1.192929 |
| T_H | 11 | 1.226156 | 1.053761 | 1.192061 |
| T_H | 22 | 1.228120 | 1.060859 | 1.194056 |
| R_F | 11 | 1.226192 | 1.054147 | 1.192694 |
| R_F | 22 | 1.228200 | 1.052640 | 1.193988 |
| R_H | 11 | 1.226764 | 1.054188 | 1.192971 |
| R_H | 22 | 1.227197 | 1.049655 | 1.192722 |

Each endpoint reached update 168 and 85,548 valid answer targets. All checkpoints and same-index per-position/per-feature arrays remain execution-side. The shared Smoke verified the actual saved state followed by an exact next-update replay, finite TensorBoard tags and answer-only target counts. Formal endpoint continuation was NOT_CHECKED. No checkpoint or hyperparameter selection was performed.

Lower NLL is descriptively better. The new learned-router models differ from old fixed routes in mixture weighting and 8,192 router parameters. This control cannot isolate feature information or establish a scientific mechanism. See [artifact manifest](artifact_manifest.json) for job, runtime, arrays, actually registered saved checkpoint IDs and current strict-access evidence.

## Saved-result audit on 2026-10-22

All four models passed the saved-artifact and source audit. Final tensor digests, all saved evaluation milestones and DEV per-position/per-feature metrics were independently recalculated. Answer-target alignment, paired expert initialization, 168 updates with 85,548 targets, load-balancing terms and learning-rate records were checked. No error requiring retraining was found within this scope. No new native forward was performed; this does not repair the separate frozen-residual diagnostic's replay-gate failure.

Two-seed mean overall DEV NLL is 1.224985 for MoE and 1.226042 for MoE_LB. On the same 1,701 positions activating at least one B1 low-frequency feature, the means are 1.054318 and 1.055211. T_F/T_H overall means are 1.226137/1.227138 and low-position means are 1.061886/1.062758. Position means use a different denominator from the feature-equal macro means above. MoE_LB improves training fit and load balance, but does not outperform ordinary MoE on this DEV panel. Two descriptive seeds do not establish a general ranking.

The actual producer was `pt-0hi8ldns` on 4 H100 Reserved GPUs. The canceled, unstarted `pt-50sa30mo` was moved from producer metadata into submission history, and the stale status page was refreshed. Original receipts were preserved. See the [saved-artifact audit](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261022_review/controls_audit.json) and [provenance correction](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261022_review/producer_metadata_correction.json).
