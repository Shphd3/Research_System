# R05: distillation and frozen student-atom routing

AI analysis; researcher judgment Unknown. All three new arms completed. A8 trains for 2000 updates from the shared initialization. A9 and A9d fork the complete native A0 state at update 1000 and add 1000 updates, replacing all eight layers or only layers 4–7. NLL is held-out negative log likelihood in nat, with lower values indicating better predictions. M measures actual hard Top-2 concentration in the same external teacher-atom coordinates; layers are averaged per atom before taking the atom median.

| arm     |      NLL |   M_median |
|:--------|---------:|-----------:|
| A5      | 4.039119 |   1.344968 |
| A0      | 4.083142 |   1.010460 |
| A1-deep | 4.085093 |   0.870829 |
| A9d     | 4.098041 |   1.026740 |
| A8      | 4.102006 |   1.113494 |
| A9      | 4.124848 |   0.967771 |
| A4      | 4.129442 |   0.810892 |
| A1      | 4.157604 |   0.585752 |
| A6      | 4.174997 |   0.924780 |
| A2      | 4.286028 |   0.256799 |

| pair   |   difference |   ci95_low |   ci95_high |
|:-------|-------------:|-----------:|------------:|
| A8-A0  |     0.018864 |   0.017118 |    0.020535 |
| A8-A5  |     0.062888 |   0.059057 |    0.066572 |
| A8-A4  |    -0.027435 |  -0.029164 |   -0.025726 |
| A9-A0  |     0.041705 |   0.039531 |    0.043695 |
| A9d-A0 |     0.014899 |   0.013455 |    0.016281 |
| A9-A9d |     0.026807 |   0.025567 |    0.028002 |

**None of the new arms beats native A0 at update 2000. A9d is better than A9 by 0.026807 nat, with a paired document interval [0.025567, 0.028002] for A9 minus A9d.** Frozen decisions are: P5 supported, P6 weakened, P7 insufficient because recovery is ongoing for both arms, P8 supported for both, and P9 supported. The last 250-update NLL drops, 0.085077 and 0.085756, exceed the preregistered 0.0817 threshold; this is why P7 is not classified as weakened.

Concentration changes relative to A0 are +10.20% for A8, −4.22% for A9 and +1.61% for A9d. The exact symmetric decomposition into conditional expert-slot distribution q and global load u is algebraic, not causal. Rounded mean M changes are approximately +0.139898 = +0.127172 +0.012726 for A8; −0.013685 = −0.038592 +0.024907 for A9; and +0.027357 = +0.024964 +0.002394 for A9d. These mean contributions do not decompose a difference of medians. The q term includes bias effects, and M ignores gate amplitudes.

Fixed-weight switching increases NLL by 1.105043 nat for A9 and 0.277600 for A9d. Atom-level Spearman correlations between route change and immediate loss increase are 0.487058 and 0.536567. Highest-quartile shock medians, 1.425312 and 0.411769, exceed lowest-quartile medians, 0.888983 and 0.203920. These meet P8, while gate changes, bias reset and routing changes remain joint interventions. A9 minus A9d estimates the conditional effect of adding early-layer interventions, rather than an additive independent layer contribution. Frozen dictionaries also drift: for example, A9 layer-0 normalized reconstruction error rises from 0.028965 to 0.278293, and A9d layer-4 error rises from 0.151707 to 0.458784.

The final interval's learned / forgotten / net-forgotten counts are 23765 / 240 / 456 for A8, 24291 / 164 / 293 for A9, and 24101 / 182 / 404 for A9d, among 29995 eligible atoms. Counts use at least 50 occurrences, BH q<0.05 and an absolute mean paired change of at least 0.01 nat. A8 history starts at update 250; self-routing histories start at the damaged post-switch update-1000 snapshot. From the common native update-1000 reference to each endpoint, learned / forgotten counts are 29125 / 226 for A9, 29262 / 205 for A9d, and 29281 / 212 for A0. Recovery below the old native-1000 level was observed for 29871 / 29915 atoms by update 2000, leaving 124 / 80 right-censored. Recovering an old baseline does not imply outperforming native update 2000. Atom tests remain descriptive because supports overlap and document dependence remains. A8 t50 has median 750, correlation −0.276977 with log frequency and −0.068577 with endpoint M; t50 is relative to improvement over updates 250–2000, rather than semantic knowledge acquisition.

AI interpretation: hard switching disrupts existing expert–input adaptation, especially when early layers are replaced. Training repairs much of this damage without overtaking native continuation. Gate 0.5, bias reset and dictionary drift remain credible competing explanations. An AI proposal, NOT RUN, is a fixed-weight late-layer selection-by-gate control before deciding the next main-model architecture. Architecture choice and new training remain for researcher discussion.

Only seed 17 was run. The 2000 paired resamples of 1871 documents measure evaluation sampling, not seed variance. A8 ran on four H100 GPUs; A9 and A9d ran on four RTX 5090 Reserved GPUs. Microbatch 16 with accumulation 2 changed to microbatch 8 with accumulation 4, preserving 262144 valid tokens per update and sample order. Read-only evaluation of identical native weights on the 5090 runtime changes aggregate NLL by +6.335e−6 / +3.396e−6 nat at updates 1000 / 2000. Minimum per-layer hard-set agreement is 99.5795% / 99.6124%; the 99th percentile of absolute position-loss changes is 0.0625 nat, so pointwise equivalence is not established. No native 5090 continuation was run, and hardware effects on training trajectories remain unresolved. The frozen primary baseline is unchanged. Evaluation uses FP32 weights with BF16 autocast and FP16 position-loss storage, rather than exclusively FP32 operators. Historical teacher BF16/FP32 Top-32 index overlap of 98.96% and exact-set agreement of 70.59% were not remeasured.

The diluted positive hint control remains below the 0.02 sensitivity threshold after four epochs (0.003803), while the full-hint control gives 1.016478. Detection power at the 0.04-nat scale therefore remains unestablished. The early A0@500 host's A5 hint gain is 0.000114, classified as not detected under the frozen rule, rather than an information upper bound. Five historical checkpoint-pair comparisons, or 55 overall and frequency-band intervals, remain BLOCKED because A0 position arrays and weights at 1250 / 1750 and A4 arrays and weights at 1500 were not retained. Aggregate curves and all primary endpoints are available. Missing intervals were neither imputed nor recovered by retraining old arms.

All requested tables, figures, recovery analyses, optional descriptive time-rescaling regressions, source identities and cost records are linked from the Chinese Detailed record. Job pt-kmzxmmyf SUCCEEDED and released its allocation. Each self-routing arm took about 77 minutes including initialization, evaluation and saving. The conservative total allocation across earlier H100 attempts and the 5090 run is 23.660797 GPU-hours, excluding queue time and counting MIG separately. Retained checkpoint families, dictionaries and actual evaluation caches are registered. The archive excludes model weights and position arrays. Researcher judgment remains Unknown.


## Complete tables and evidence lineage

| claim                       | criterion          | raw                                                       | producer                                                  | eligibility         | limit                                                  |
|:----------------------------|:-------------------|:----------------------------------------------------------|:----------------------------------------------------------|:--------------------|:-------------------------------------------------------|
| A8 manipulation andbenefit  | P5/P6              | B_M_medians.csv;A_bootstrap_differences.csv               | analysis/finalize.py                                      | bounded as recorded | M is external geometry;single seed                     |
| Selfbenefit andearlylayers  | P7/P9              | A_learning.csv;A_bootstrap_differences.csv                | analysis/finalize.py                                      | bounded as recorded | 1000newupdates;crosshardware native training reference |
| Switch association          | P8                 | D_switch_correlations.csv;D_switch_quartiles.csv          | analysis/finalize.py                                      | bounded as recorded | Gate,bias,groupchoices jointlychange                   |
| Concentration decomposition | descriptive        | F_concentration_bands.csv;F_concentration_layers.csv      | analysis/final_supplement.py                              | bounded as recorded | Exact algebra,not independent intervention             |
| Learning/forgetting         | R04fixedthresholds | C_ledger_by_bin.csv;F_matched_learning.csv                | analysis/finalize.py;analysis/final_supplement.py         | bounded as recorded | Overlapping atoms;post-switch history differs          |
| Retainedstates              | execution          | evidence/saved_A8.json;saved_A9.json;saved_A9d.json       | analysis/finalize_records.py                              | bounded as recorded | Fullstate versusBF16 snapshots separated               |
| Runtimecontrol              | secondary          | runtime_forward_difference.csv;runtime_sensitivity_CI.csv | analysis/forward_reference_5090.py;runtime_sensitivity.py | bounded as recorded | Forwardonly;no native5090training                      |

| prediction   | result               |    value |   ci95_low |   ci95_high |   last250_drop | researcher_judgment   |
|:-------------|:---------------------|---------:|-----------:|------------:|---------------:|:----------------------|
| P5           | 支持                 | 1.113494 | nan        |  nan        |     nan        | Unknown               |
| P6           | 削弱                 | 0.018864 |   0.017118 |    0.020535 |     nan        | Unknown               |
| P7_A9        | 不足（恢复尚未完成） | 0.041705 | nan        |  nan        |       0.085077 | Unknown               |
| P7_A9d       | 不足（恢复尚未完成） | 0.014899 | nan        |  nan        |       0.085756 | Unknown               |
| P8_A9        | 支持                 | 0.487058 | nan        |  nan        |     nan        | Unknown               |
| P8_A9d       | 支持                 | 0.536567 | nan        |  nan        |     nan        | Unknown               |
| P9           | 支持                 | 0.026807 |   0.025567 |    0.028002 |     nan        | Unknown               |

| arm   |   from_step |   to_step | band    |   atoms |   learned |   forgotten |   net_forgotten |   mean_delta |   chi_mean |
|:------|------------:|----------:|:--------|--------:|----------:|------------:|----------------:|-------------:|-----------:|
| A8    |         250 |       500 | overall |   29995 |     29992 |           1 |               0 |    -1.050166 |   0.729559 |
| A8    |         500 |       750 | overall |   29995 |     29953 |           4 |               0 |    -0.622071 |   0.474145 |
| A8    |         750 |      1000 | overall |   29995 |     29877 |          19 |               9 |    -0.618506 |   0.404590 |
| A8    |        1000 |      1250 | overall |   29995 |     29576 |          65 |              41 |    -0.351583 |   0.341512 |
| A8    |        1250 |      1500 | overall |   29995 |     23396 |        1896 |            1385 |    -0.129569 |   0.327854 |
| A8    |        1500 |      1750 | overall |   29995 |     25560 |         199 |             619 |    -0.130893 |   0.311820 |
| A8    |        1750 |      2000 | overall |   29995 |     23765 |         240 |             456 |    -0.102464 |   0.282660 |
| A9    |        1000 |      1250 | overall |   29995 |     29993 |           0 |               0 |    -1.466133 |   0.521705 |
| A9    |        1250 |      1500 | overall |   29995 |     26777 |         711 |             453 |    -0.186422 |   0.385308 |
| A9    |        1500 |      1750 | overall |   29995 |     24635 |         431 |             454 |    -0.122231 |   0.398969 |
| A9    |        1750 |      2000 | overall |   29995 |     24291 |         164 |             293 |    -0.104499 |   0.410058 |
| A9d   |        1000 |      1250 | overall |   29995 |     29945 |          18 |              14 |    -0.614735 |   0.324249 |
| A9d   |        1250 |      1500 | overall |   29995 |     25640 |        1014 |             685 |    -0.162653 |   0.313956 |
| A9d   |        1500 |      1750 | overall |   29995 |     24496 |         384 |             558 |    -0.118459 |   0.311944 |
| A9d   |        1750 |      2000 | overall |   29995 |     24101 |         182 |             404 |    -0.104710 |   0.311043 |

| arm   | band    |   rho_swap_delta_chi |   rho_recovery_delta |   rho_recovery_chi |   rho_final_delta |   rho_final_delta_logM |   recovered |   unrecovered |
|:------|:--------|---------------------:|---------------------:|-------------------:|------------------:|-----------------------:|------------:|--------------:|
| A9    | overall |             0.487058 |            -0.031842 |          -0.070803 |          0.273698 |               0.018028 |       29871 |           124 |
| A9d   | overall |             0.536567 |            -0.018461 |          -0.037503 |          0.251904 |              -0.045155 |       29915 |            80 |

| arm   | start_UTC                        | end_UTC                          |   wall_seconds |   measured_step_seconds |   updates |   last_step | status   |
|:------|:---------------------------------|:---------------------------------|---------------:|------------------------:|----------:|------------:|:---------|
| A8    | 2026-11-10T06:10:34.071565+00:00 | 2026-11-10T08:15:27.986112+00:00 |    7493.914547 |             5664.940863 |      2000 |        2000 | complete |
| A9    | 2026-11-10T11:53:33.194270+00:00 | 2026-11-10T13:11:00.646713+00:00 |    4647.452443 |             2878.804145 |      1000 |        2000 | complete |
| A9d   | 2026-11-10T13:11:22.599362+00:00 | 2026-11-10T14:28:40.902733+00:00 |    4638.303371 |             2862.337123 |      1000 |        2000 | complete |

| pair   |   step | status                 |   aggregate_NLL_difference | reason                                                                    | missing_positions                                                                                                   |
|:-------|-------:|:-----------------------|---------------------------:|:--------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|
| A8-A4  |   1500 | 区间未完成；聚合差已知 |                  -0.008070 | 旧对照逐位置数据缺失，且该步权重未保存；仅有聚合NLL不足以计算文档配对区间 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A4/step001500.npz |
| A9-A0  |   1250 | 区间未完成；聚合差已知 |                   0.081043 | 旧对照逐位置数据缺失，且该步权重未保存；仅有聚合NLL不足以计算文档配对区间 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A0/step001250.npz |
| A9-A0  |   1750 | 区间未完成；聚合差已知 |                   0.045078 | 旧对照逐位置数据缺失，且该步权重未保存；仅有聚合NLL不足以计算文档配对区间 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A0/step001750.npz |
| A9d-A0 |   1250 | 区间未完成；聚合差已知 |                   0.034293 | 旧对照逐位置数据缺失，且该步权重未保存；仅有聚合NLL不足以计算文档配对区间 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A0/step001250.npz |
| A9d-A0 |   1750 | 区间未完成；聚合差已知 |                   0.018951 | 旧对照逐位置数据缺失，且该步权重未保存；仅有聚合NLL不足以计算文档配对区间 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A0/step001750.npz |

| item      | question                                                    | status           | evidence                                                                             | missing_dependency                                                                                             | bounded_reading                                                            |
|:----------|:------------------------------------------------------------|:-----------------|:-------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|
| TRAIN_A8  | A8 2000 updates; native router with atom-score distillation | DONE_VALID       | runs/A8/completion.json                                                              |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| TRAIN_A9  | A9 full-state fork1000 and1000 new updates                  | DONE_VALID       | runs/A9/completion.json                                                              |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| TRAIN_A9d | A9d same fork and1000 new updates                           | DONE_VALID       | runs/A9d/completion.json                                                             |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| A1        | NLL curves and10frequency bands                             | DONE_VALID       | A_learning.csv;A_frequency.png;F_loss_detailed.png                                   |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| A3        | A8 gain-inheritance ratio overall/bands                     | DONE_VALID       | A8_inheritance.csv                                                                   |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| A4        | Train50/EVAL step lead with censoring                       | DONE_VALID       | A_step_lead.csv;A_training_CE50.csv                                                  |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| B5        | Every retained checkpoint/layer hardM plusEVAL denominator  | DONE_VALID       | B_M_medians.csv;B_layer_distribution.csv;per_atom/M_*                                |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| B6        | A8 agreement versus frozen linear-probe benchmark           | DONE_VALID       | B_A8_vs_linear_probe.csv                                                             |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| B7        | Flips,load,bias,effective pairs,bias selection changes      | DONE_VALID       | B_combinations_flips.csv;B_layer_distribution.csv                                    |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| B8        | Dictionary reconstruction drift                             | DONE_VALID       | B_layer_distribution.csv;B_dictionary_drift_load.png                                 |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| C9        | Adjacent learned/forgotten/net-forgotten all10bands         | DONE_VALID       | C_ledger_by_bin.csv;F_learning_forgetting.png                                        |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| C10       | A8 t50 andfrequency/M correlations                          | DONE_VALID       | C_A8_t50.csv;per_atom/A8_t50.csv                                                     |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| D11       | Fixed-weight switch shock anddocument intervals             | DONE_VALID       | D_switch_bootstrap.csv                                                               |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| D12       | Route-change versusshock;quartiles and10bands               | DONE_VALID       | D_switch_correlations.csv;D_switch_quartiles.csv                                     |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| D13       | Per-atom recovery grid,censoring,correlations               | DONE_VALID       | per_atom/swap_A9.csv;per_atom/swap_A9d.csv;F_recovery_distribution.csv               |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| D14       | Final gap correlates withswitchshock andlogMchange          | DONE_VALID       | D_switch_correlations.csv                                                            |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| HINT      | Positive andearly probes;frozen4epoch fallback completed    | DONE_VALID       | hint_supplement.csv                                                                  |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| ASSETS    | Actual retained checkpoints,dictionaries,evaluation caches  | DONE_VALID       | evidence/saved_A*.json;analysis_output_manifest.json                                 |                                                                                                                | AI analysis; scientific judgment Unknown                                   |
| A2        | Paired document bootstrap allrequestedpairs/checkpoints     | BLOCKED          | A_bootstrap_differences.csv;A_missing_comparisons.csv                                | 5 historical checkpoint-pair combinations / 55 overall+band intervals; no saved old weights or position arrays | Available comparisons DONE_VALID; do not impute missing intervals          |
| E         | Optional per-atom time rescaling                            | DONE_EXPLORATORY | E_atom_time_rescaling.csv                                                            |                                                                                                                | Descriptive regression;censoring visible;not independent atom replications |
| F         | Requested finalq/u decomposition andmatchedlearning         | DONE_EXPLORATORY | F_concentration_bands.csv;F_concentration_layers.csv;F_matched_learning.csv          |                                                                                                                | Exact algebraic attribution;not causal mediation                           |
| RUNTIME   | Same5090 native forward sensitivity                         | DONE_EXPLORATORY | runtime_forward_difference.csv;runtime_sensitivity_CI.csv;runtime_sensitivity_P8.csv |                                                                                                                | No native5090 continuation training;frozen primary baseline retained       |

Source manifests and source identity: evidence/final_sources.json, actual_arm_configs_sources.json, source_release_qualified_A8, saved_A*.json and analysis_output_manifest.json. Original frozen prompt SHA256b577ed19ce503fdaa0415e54891faf3f958f470ab7278a77f20a8b9ae76adb30;5090resource migration is the documented amendment. Earlier startup and fork/shutdown failures are execution-only and charged in cost; full details remain in the Chinese Detailed and immutable receipts.
