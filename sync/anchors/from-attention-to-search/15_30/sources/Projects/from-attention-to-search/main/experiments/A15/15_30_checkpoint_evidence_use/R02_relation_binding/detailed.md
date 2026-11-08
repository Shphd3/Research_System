# R02 complete evidence and execution record

[Summary](summary.md) states the bounded result; scientific judgment remains Unknown.24R01-exposed families, six templates, no independent confirmation. The tables retain every actual state/gap, candidates versus greedy generation, world margins and binding response. Headers in the aligned tables identify model, actual billions of tokens, anchor gap, paired success/24, Wilson95%, lexical-candidate success,Δand its family interval, positiveΔfamilies and OTHER prompts/48.

| 模型 | B token | 锚点gap | 候选成对 /24 [95%Wilson] | 生成成对 /24 [95%Wilson] | 候选首词 /24 | 翻转响应Δ nat [家族区间] | Δ>0家族 /24 | OTHER提示 /48 |
|---|---|---|---|---|---|---|---|---|
| Baseline | 3.0 | 16 | 9 [0.212, 0.573] | 9 [0.212, 0.573] | 11 | 1.144 [0.672, 1.624] | 18 | 9 |
| Baseline | 3.0 | 1024 | 7 [0.149, 0.492] | 11 [0.279, 0.649] | 9 | 1.646 [0.979, 2.378] | 21 | 16 |
| Dense | 3.0 | 16 | 5 [0.092, 0.405] | 3 [0.043, 0.310] | 4 | 0.481 [0.194, 0.787] | 17 | 14 |
| Dense | 3.0 | 1024 | 3 [0.043, 0.310] | 2 [0.023, 0.258] | 4 | 0.918 [0.508, 1.391] | 21 | 22 |
| Baseline | 15.0 | 16 | 4 [0.067, 0.359] | 3 [0.043, 0.310] | 3 | 0.685 [0.423, 0.951] | 20 | 0 |
| Baseline | 15.0 | 1024 | 7 [0.149, 0.492] | 5 [0.092, 0.405] | 6 | 1.552 [1.222, 1.911] | 24 | 2 |
| Dense | 15.0 | 16 | 5 [0.092, 0.405] | 3 [0.043, 0.310] | 4 | 0.335 [0.052, 0.637] | 17 | 7 |
| Dense | 15.0 | 1024 | 7 [0.149, 0.492] | 5 [0.092, 0.405] | 5 | 2.072 [1.220, 2.951] | 19 | 5 |
| Baseline | 17.0 | 16 | 3 [0.043, 0.310] | 4 [0.067, 0.359] | 2 | 0.478 [0.238, 0.719] | 19 | 7 |
| Baseline | 17.0 | 1024 | 6 [0.120, 0.449] | 7 [0.149, 0.492] | 6 | 1.824 [1.206, 2.460] | 22 | 4 |
| Dense | 17.0 | 16 | 1 [0.007, 0.202] | 1 [0.007, 0.202] | 1 | 0.127 [-0.137, 0.401] | 14 | 11 |
| Dense | 17.0 | 1024 | 3 [0.043, 0.310] | 3 [0.043, 0.310] | 3 | 1.037 [0.568, 1.527] | 17 | 9 |

## Within-family near-minus-far effects

Rate differences are proportions; margin/Δdifferences are nats.10000family paired bootstrap draws, seed20261105; six-template cluster sensitivity is separate. Neither estimates training-seed uncertainty. Raw per-family and template/type tables remain execution-side.

| 模型 | B token | 指标 | 近减远 | 95%家族区间 | 95%六模板聚类敏感性 |
|---|---|---|---|---|---|
| Baseline | 3.0 | candidate_paired | 0.083 | [-0.083,0.250] | [-0.083,0.292] |
| Baseline | 3.0 | generation_paired | -0.083 | [-0.250,0.083] | [-0.375,0.125] |
| Baseline | 3.0 | mean_margin | -0.251 | [-0.423,-0.096] | [-0.501,-0.025] |
| Baseline | 3.0 | binding_delta | -0.502 | [-0.846,-0.191] | [-1.002,-0.050] |
| Dense | 3.0 | candidate_paired | 0.083 | [-0.125,0.292] | [0.000,0.250] |
| Dense | 3.0 | generation_paired | 0.042 | [-0.125,0.208] | [-0.208,0.250] |
| Dense | 3.0 | mean_margin | -0.218 | [-0.393,-0.079] | [-0.486,-0.006] |
| Dense | 3.0 | binding_delta | -0.436 | [-0.787,-0.158] | [-0.971,-0.011] |
| Baseline | 15.0 | candidate_paired | -0.125 | [-0.375,0.125] | [-0.458,0.250] |
| Baseline | 15.0 | generation_paired | -0.083 | [-0.292,0.125] | [-0.333,0.167] |
| Baseline | 15.0 | mean_margin | -0.434 | [-0.635,-0.234] | [-0.671,-0.135] |
| Baseline | 15.0 | binding_delta | -0.867 | [-1.270,-0.468] | [-1.341,-0.270] |
| Dense | 15.0 | candidate_paired | -0.083 | [-0.208,0.000] | [-0.167,0.000] |
| Dense | 15.0 | generation_paired | -0.083 | [-0.208,0.000] | [-0.167,0.000] |
| Dense | 15.0 | mean_margin | -0.868 | [-1.212,-0.530] | [-1.422,-0.294] |
| Dense | 15.0 | binding_delta | -1.736 | [-2.424,-1.060] | [-2.845,-0.587] |
| Baseline | 17.0 | candidate_paired | -0.125 | [-0.333,0.083] | [-0.500,0.125] |
| Baseline | 17.0 | generation_paired | -0.125 | [-0.375,0.125] | [-0.500,0.167] |
| Baseline | 17.0 | mean_margin | -0.673 | [-0.948,-0.407] | [-1.208,-0.211] |
| Baseline | 17.0 | binding_delta | -1.346 | [-1.897,-0.813] | [-2.417,-0.423] |
| Dense | 17.0 | candidate_paired | -0.083 | [-0.250,0.083] | [-0.375,0.125] |
| Dense | 17.0 | generation_paired | -0.083 | [-0.250,0.083] | [-0.375,0.125] |
| Dense | 17.0 | mean_margin | -0.455 | [-0.623,-0.304] | [-0.759,-0.203] |
| Dense | 17.0 | binding_delta | -0.910 | [-1.247,-0.609] | [-1.518,-0.407] |

## Same-model FP32 R01 reference

The576old prefixes are rescored only inR02while each actual model is loaded; no original score or input is overwritten. Every new-vs-old condition has14–22old-pass/new-fail families. Competitor/filler/target-gap differences remain, so this is not identification of the old strategy.

| 模型 | B token | 锚点gap | R01 FP32成对 /24 | R02 FP32成对 /24 | 旧对新错家族 | 旧减新成功率 [家族区间] |
|---|---|---|---|---|---|---|
| Baseline | 3.0 | 16 | 24 | 9 | 15 | 0.625 [0.417,0.792] |
| Baseline | 3.0 | 1024 | 23 | 7 | 16 | 0.667 [0.458,0.833] |
| Dense | 3.0 | 16 | 20 | 5 | 15 | 0.625 [0.417,0.792] |
| Dense | 3.0 | 1024 | 19 | 3 | 16 | 0.667 [0.458,0.833] |
| Baseline | 15.0 | 16 | 21 | 4 | 17 | 0.708 [0.500,0.875] |
| Baseline | 15.0 | 1024 | 23 | 7 | 16 | 0.667 [0.458,0.833] |
| Dense | 15.0 | 16 | 23 | 5 | 18 | 0.750 [0.583,0.917] |
| Dense | 15.0 | 1024 | 21 | 7 | 14 | 0.583 [0.375,0.792] |
| Baseline | 17.0 | 16 | 22 | 3 | 19 | 0.792 [0.625,0.958] |
| Baseline | 17.0 | 1024 | 21 | 6 | 15 | 0.625 [0.417,0.833] |
| Dense | 17.0 | 16 | 23 | 1 | 22 | 0.917 [0.792,1.000] |
| Dense | 17.0 | 1024 | 19 | 3 | 16 | 0.667 [0.458,0.833] |

## Setup, guards, provenance and cost

All six states pass fresh fullSHA/native strict-load/parameter count and actual tokens_seen/optimizer_step checks:3/15/17B,11446/57224/64854steps. Dense total/active281431040; ordinary MoE total507988992, conventional active281496576. One seed17trajectory each, unequal capacity/hardware/realized compute; six points precede the22.018691584Bhistorical order divergence. The old training-order audit is sourced, not rerun. All37old raw-score files are freshly hashed and replayed; other31weights are not reloaded here.

Frozen input words/labels/positions and exact protocol precede first new behavior. Two worlds differ only at the two entity-token positions; all value positions/bags/query/length/filler are identical. Target-value gaps differ from the final-listed-value anchor; see[definitions](definitions.md). Native FP32 forward/head/logsoftmax, TF32off, weights and MoE load bias frozen. Primary candidates are word+period,2tokens each. Greedy first lexical word after an optional initial article is a separate metric; OTHER is never deleted. No80percent screening or task/threshold amendment.

Smoke:two3Bmodels×24engineering prefixes, all numerical/label/parser/context gates passed. CE calibration maximum~8.11e-6nat and prefix hidden max~6.80e-6against5e-4tolerance.308direct lexical-start generation scores align with candidate first-token probabilities, max~1.69e-5nat. R01 all noncache bytes and file set are unchanged. Original weights retain file identity/mtime; loaded parameters/bias are unchanged, zero updates.

Full stage275.63s plus smoke71.48s; loading/hash187.76s, peak2.797GiB. Main candidate/generation/old-reference physical positions are1,329,408/1,734,032/1,329,408;1375generated tokens. No KV cache reuse, no new resource/job. Smoke calibration extra forwards and CPU/report overhead are not in these main counters; billing Unknown. All576binding and576bridge prefixes complete, with48engineering prefixes. Existing H100MIG3g.40gb, not full-H100-equivalent billing.

Coverage: main complete DONE_EXPLORATORY; smoke/data/numerical/byte guards DONE_VALID engineering only. Independent new families, paraphrase transfer, seed replication, multihop composition, full-checkpoint expansion, feature analysis and new training NOT RUN. Another Base-student knowledge-learning startup gate is NOT ASSESSED. Actual weak near performance and OTHER/failure cases remain, with researcher expansion decision pending.

[Assets/data](assets_and_data.md) · [Cases](cases.md) · [Reproduction](reproduce.md) · [Artifact manifest](artifact_manifest.json) · [Verification](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/verification.json).
