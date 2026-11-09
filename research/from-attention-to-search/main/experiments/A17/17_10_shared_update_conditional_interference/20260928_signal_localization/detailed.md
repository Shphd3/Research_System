# Detailed: posthoc localization of the shared-update task-signal effect

## Round 2026-09-28 — question and hypothesis

The [current Protocol](protocol.md) asks where the task-signal-related harmful contribution of an effective A update on B resides, what larger component offsets it, and whether SAE common atoms, major static variance directions, or a readable task-signal probe identify the relevant update path. This is an extension of the [registered 0927 result](../20260927_controlled/summary.md), not a new confirmation set. Every one of the 12 direction families had already been inspected. The original verdict `MODULATION_WITHOUT_NET_HARM` and researcher-pending scientific judgment are unchanged.

The native candidate explanation is that the within-nuisance-pair odd displacement \(t s\) is harmful under B's flipped rule but helpful under A and B's same rule. The stronger shared-space explanation predicts that the signed harm lies predominantly in a static common or task-readable space. Rivals are (a) common activation or raw leading energy dominated by background, (b) pooled PCs dominated by one group or variance without functional effect, and (c) a probe that decodes \(t\) but does not describe the actual update.

## Setup, controls, and authorization

On 2026-09-28 the researcher explicitly requested execution of the 0928 continuation plan. The Protocol approval snapshot and A–G ledger register that authorization for local CPU analysis of saved arrays, figures, and result records. No GPU, model loading, training, new directions, parameter isolation, or source-result rewrite occurred. The result remains `POST_HOC_EXPLORATORY`; approval to run is not scientific approval.

The immutable source root is `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z` (R). The checkpoint is S7 at exactly 33,000,000,000 training tokens, not a 33-billion-parameter model. The source state SHA256 is `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`. R's `registration.json` SHA256 is `ab201f81cdcfa9ff9b5be7e745d7125ffe4f7908df3d8727f1b479c8c397616c`; `measurement_complete.json` SHA256 is `e3ee791665dd7e3e80bdaae50891fb51fe2f7a68720a20650a4d1497bd102f26`.

The final execution directory is `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z` (E). Its [registration.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/registration.json) froze code, config, current Protocol, 48 structure cells, 12 SAE bases, 48 readout files, all 192 dynamic NPZ files, original registration/completion certificates, and the original bootstrap indices before new projection results. [bootstrap_registration.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/bootstrap_registration.json) and [secondary_registration.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/secondary_registration.json) froze later implementation-only stages and their inputs. Actual output is about 200 MiB, below the 2 GiB budget.

Each family uses four balanced structure cells: A/B × low/high \(\rho\), each 128 matched \(t=\pm1\) pairs. The independent source/target readout set uses 256 pairs per family/rho. Conditions cover \(\rho=0.1,0.8\), source repetitions 0–3, steps \(10^{-4},5\times10^{-5}\), and B same/flip, giving 192 saved update files. The source A readout is independent of the A batch that formed the update. Same/flip B have bit-identical saved \(a_0\) and \(\Delta a\); only the target rule differs. No cell, family, or extreme pair was dropped.

The spaces, fit without dynamic or B-loss information, are frozen SAE-full rank 32; raw SVD and pooled-centered PCA of the 1024-row four-cell native \(a\) matrix; PCA restricted to the SAE 32-dimensional span; four separate ridge probes (A/B × rho) orthogonalized to one family-level span; and three Gaussian random bases at each matching rank. Nested geometric ranks are 1, 2, 4, 8, 16 (primary 8), plus probe's own effective rank and matching controls. Ridge coefficient is \(10^{-3}\operatorname{tr}(X_c^\top X_c/n)/1024\), with no sweep. Probe shuffles flip exactly 64 of 128 structure-set pair labels per seed 17/29/43, keeping evaluation labels true. The paired bootstrap uses the exact saved 2000 family/repeat/target-pair/source-pair index tensors; fitted spaces are held fixed. Source A uses source-pair indices, B uses target-pair indices.

## Data qualification and measurement closure

[preflight.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/preflight.json) is `PASS`: all 48 structure cells and 192 dynamic files were read, original pairwise mean terms and \(I_1\) reproduced within \(10^{-11}\), same/flip \(a_0\) and \(\Delta a\) differences are exactly zero, maximum per-pair first-order closure error is \(2.69\times10^{-17}\), five-piece loss closure error \(2.78\times10^{-17}\), and B's saved SAE projection agrees to \(6.78\times10^{-19}\). All SAE bases meet \(\|Q_S^\top Q_S-I\|_\infty<10^{-8}\). The original A/source `C_S` field is a zero placeholder, so the A projection is calculated directly from saved \(e,\Delta a,Q_S\); only B saved `C_S` fields are used for reproduction.

The final signed, displacement, and sign-fraction tables each contain 24,192 unique family/rho/repeat/step/rule/method cells (12×2×4×2×3×42); their key sets match. All numeric cells are finite and the CSV-level five-piece closure error is below \(2.25\times10^{-16}\). There are 84 space/step interval records. No required condition is marked missing.

The signal split is \(b_i=(\Delta a_{i,+}+\Delta a_{i,-})/2\), \(s_i=(\Delta a_{i,+}-\Delta a_{i,-})/2\). Thus \(C_{sig}=E[e_{i,t}^{\top}(t s_i)]\) and \(C_{even}=E[e_{i,t}^{\top}b_i]\); for a span \(P=QQ^\top\), \(C_{P,sig}+C_{\perp,sig}=C_{sig}\) and \(C_{P,even}+C_{\perp,even}=C_{even}\). Finally \(I=C_{sig}+C_{even}+R\). The even term mixes background and nuisance-related displacement; it is **not** SAE common.

## Results: native task-signal effect and offset

All entries are nat per target; bracketed values are paired 95% conditional bootstrap intervals. The first-order signed term uses the saved target derivative; only \(I\) is the observed finite-step loss difference.

| Step | High-rho readout | \(C_{sig}\) | \(C_{even}+R\) | Observed \(I\) |
| --- | --- | ---: | ---: | ---: |
| \(10^{-4}\) | A | \(-1.03354\times10^{-4}\) [\(-1.04190,-1.02556\)] × \(10^{-4}\) | \(-0.00673855\) | \(-0.00684190\) |
| \(10^{-4}\) | B same | \(-8.27006\times10^{-5}\) [\(-8.3303,-8.2121\)] × \(10^{-5}\) | \(-0.00673597\) | \(-0.00681867\) |
| \(10^{-4}\) | B flip | \(+8.31259\times10^{-5}\) [\(8.2860,8.3411\)] × \(10^{-5}\) | \(-0.00674801\) [\(-0.00676326,-0.00673216\)] | \(-0.00666488\) [\(-0.00668001,-0.00664918\)] |
| \(5\times10^{-5}\) | A | \(-5.16768\times10^{-5}\) [\(-5.2095,-5.1278\)] × \(10^{-5}\) | \(-0.00341482\) | \(-0.00346649\) |
| \(5\times10^{-5}\) | B same | \(-4.13503\times10^{-5}\) [\(-4.1652,-4.1060\)] × \(10^{-5}\) | \(-0.00341353\) | \(-0.00345488\) |
| \(5\times10^{-5}\) | B flip | \(+4.15629\times10^{-5}\) [\(4.1430,4.1706\)] × \(10^{-5}\) | \(-0.00341955\) [\(-0.00342717,-0.00341163\)] | \(-0.00337798\) [\(-0.00338554,-0.00337013\)] |

For \(10^{-4}\), the original registered contrast \(M_I=+1.5205636\times10^{-4}\) has interval \([1.3617195,1.6721771]\times10^{-4}\). Its native components close as \(M_{sig}=+1.4510221\times10^{-4}\), CI \([1.4457701,1.4571421]\times10^{-4}\); \(M_{even}=+6.9846\times10^{-6}\), CI \([-8.7217,22.1864]\times10^{-6}\); and \(M_R=-3.0468\times10^{-8}\). At \(5\times10^{-5}\), the corresponding values are \(M_I=+7.6027980\times10^{-5}\), \(M_{sig}=+7.2551106\times10^{-5}\), \(M_{even}=+3.4923\times10^{-6}\), and \(M_R=-1.5432\times10^{-8}\). The native branch conditions in Protocol §15 hold at both steps. This says the known task-signal part changes sign and is offset by larger help on these viewed samples; it does not show that an isolated signal update would causally induce net B harm.

![Native terms and net outcome](../../../../../../../daily_research_reports/backup/2026/09/0928/figures/shared_update_signal_even_fourterm_net.png)

## Results: SAE, geometric spaces, probe, and random controls

High rho/B flip at \(10^{-4}\): the frozen SAE-full span yields \(C_{P,sig}=+2.67664\times10^{-6}\), \(C_{\perp,sig}=+8.04492\times10^{-5}\), \(C_{P,even}=-0.00022322\), \(C_{\perp,even}=-0.00670654\), and \(R=+0.00018175\). Their sum is the observed \(-0.00666488\). Thus the observed helpful even action is also mostly outside this static SAE common span. `C_P_sig` is about 3.22% of native \(C_{sig}\), a descriptive signed ratio only; it is not a causal explanation rate. The original 12/12 SAE task-signal reconstruction failures remain, and the independently recomputed structure-cell median error lies between 1.02 and 1.15 (all above the unchanged 0.5 guard).

The table reports \(C_{P,sig}\), the excess \(\delta_P\) over the mean of three same-rank random spaces, and \(D_P=C_{P,sig}-C_{\perp,sig}\), all in \(10^{-6}\) nat per target. Intervals are paired and conditional on fitted spaces. `delta` for a single random seed is an internal check against the three-seed mean, not an independent random-distribution test.

| Span | Rank | \(C_{P,sig}\) | \(\delta_P\) 95% CI | \(D_P\) 95% CI |
| --- | ---: | ---: | ---: | ---: |
| SAE-full | 32 | 2.677 | [−0.066, 0.305] | [−78.018, −77.539] |
| raw SVD | 8 | 0.805 | [0.017, 0.263] | [−81.741, −81.306] |
| centered PCA | 8 | 0.904 | [0.153, 0.319] | [−81.596, −81.060] |
| SAE-restricted PCA | 8 | 0.812 | [−0.026, 0.317] | [−81.823, −81.188] |
| probe span | 3 | 0.198 | [−0.123, 0.062] | [−82.901, −82.527] |

At half step all values halve approximately; raw SVD-8 and centered PCA-8 still have small positive same-rank excess intervals, while SAE-full, SAE-restricted PCA-8, and probe do not separate from their three random instances by this rule. Every listed \(D_P\) remains negative at both steps. Consequently, even the spaces with detectable same-rank excess capture only a small minority of the signed harm. Rank-curve values for k=1,2,4,8,16 and both steps are in [space_rank_curve.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/space_rank_curve.csv); no space or rank was selected using the loss.

![Candidate-space dynamic displacement and signed contribution](../../../../../../../daily_research_reports/backup/2026/09/0928/figures/shared_update_same_rank_capture_signed.png)

Effective numerical ranks are 17 for raw SVD, 16 for centered PCA and SAE-restricted PCA, and 3 for the probe span in each of 12 families. The prespecified 1e-4 sensitivity threshold gives the same ranks; all requested k≤16 are identifiable and each k boundary gap exceeds 1e-5 (raw SVD k=8 minimum gap 2.5e-5). This corrects the *interpretation* of the older PCA-32 control, whose implementation did not clip numerical rank, without changing its frozen result record. The SAE-full rank-32 comparison retains its own random-32 controls.

On high-rho independent B readouts, raw SVD-1 captures essentially 100% of mean energy but only 3.37% of centered variance and 3.43% of static task difference. Centered PCA-1 captures 77.17% of centered variance and 81.98% of task difference; centered PCA-8 captures 96.78% and 99.9995%. Yet centered PCA-8 captures only 1.0873% of the **actual update's task-signal displacement** energy; raw SVD-8 0.9680%, SAE-full 3.2210%, SAE-restricted PCA-8 0.9773%, and probe-3 0.2381%. The matching random-8 seed 17 captures 0.8252% of that displacement. Static A and B occupancy, per-axis distributions, and their min/max ratios are in [occupancy.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/occupancy.csv) and [occupancy_group_ratio.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/occupancy_group_ratio.csv). The mean A/B centered-variance min/max ratio for centered PCA-8 is 0.996; for SAE-full it is 0.829, with individual families down to 0.650. Pooled geometry is therefore reported with separate group occupation.

The true probe has balanced accuracy 1.000 with negligible MSE on within-group independent readouts at the same rho; matched-rho cross-group accuracy averages 0.875, MSE 0.434, predicted RMS 0.457. Pair-label shuffle controls average approximately 0.50 within group with near-zero prediction RMS; their cross-group mean is also near chance, though individual seeds vary. Probe rank is 3, not 4, under the frozen numerical threshold. The high decoding result only establishes accessible static \(t\), not that the model's actual update or its signed loss effect follows that readout. [probe_eval.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/probe_eval.csv) contains every train/test combination, MSE, and RMS.

![Static geometry and independent probe decoding](../../../../../../../daily_research_reports/backup/2026/09/0928/figures/shared_update_static_geometry_probe.png)

Per-condition, per-method projected signal/even energy capture is in [displacement_capture.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/displacement_capture.csv); four signed terms, \(R\), \(I_1\), and \(I\) in [signed_terms.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/signed_terms.csv). Per-logical-pair contributions remain in 12 `per_pair_terms_f*.npz` shards, and per-condition sign fractions in [signed_term_sign_fractions.csv](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/signed_term_sign_fractions.csv). For high-rho/B-flip at \(10^{-4}\), the task-signal signed term is positive and the even term negative across all 256 pairs, all repeats, and all 12 families for the example spaces SAE-full, centered PCA-8, and probe-3. This is a property of the constructed task, not an independent natural-domain replication.

## Split, deviations, and interpretation boundary

The structure/readout split prevents a fitted basis or probe from using its evaluation sample. It does **not** create untouched direction families: all 12 families and original results were viewed before this posthoc plan. The bootstrap intervals quantify conditional sampling variation with the fitted spaces fixed; they omit basis-refit, model, and external-data uncertainty. Three random bases do not estimate the full random-subspace distribution. Multiple spaces and ranks are descriptive, with no multiplicity-adjusted claim of a winning tool.

Two implementation deviations are logged in [failures.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/failures.json) and the Protocol §17 ledger. First, a prior immutable attempt `signal_localization_20260928T025000Z` stopped on the invalid A/source `C_S` placeholder check. Its source arrays were not changed. Second, the first bootstrap scalar loop was interrupted before interval output for speed; the registered vectorized stage used the identical saved index tensors. Three independently coded direct index-loop draws (including draw 0 and draw 1999) match its stored draw arrays within \(6.94\times10^{-18}\); [verification.json](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_20260928T025800Z/verification.json) also records \(P=0\), \(P=I\), and paired record-swap checks. No sample, method, rank, metric, or criterion was changed in either correction.

**Result branch:** the Protocol's native signal/offset sign conditions hold at both steps. The stronger “most harm is in SAE common” branch is unsupported; SAE-full's excess over the three random rank-32 spaces is unresolved, and \(D_P<0\). Raw SVD-8 and centered PCA-8 provide small conditional extra information relative to their three random rank-8 instances, but also have \(D_P<0\); this is not majority localization or evidence of causal necessity. Probe decoding succeeds as a readability control while its functional localization remains weak. The exact residual functional direction within the 1024-dimensional native space has not been identified by these static candidate spans. No new prospective prediction, isolation experiment, or single-atom intervention was run.

**Next researcher decision:** whether this now well-measured but largely unlocalized task-signal effect justifies designing a targeted representation intervention to test causal contribution. If not, stop the static-space localization line for this fixed construction; repeated analysis of these 12 families cannot supply a new confirmation set. Do not alter the existing Focus judgment or original verdict from this AI result record.

## Artifact map

| Artifact | Role |
| --- | --- |
| E/`registration.json`, `config.json`, `analyze_signal_localization.py` | frozen initial plan/code/input identity and FP64 projection computation |
| E/`preflight.json`, `baseline_reproduction.csv` | shape, pair, rule, source-mean, signed-closure qualification |
| E/`bases`, `basis_manifest.json`, `rank_audit.csv`, `probe_fit.json` | frozen candidate spaces, effective rank, supervised-fit provenance |
| E/`per_pair_terms_f*.npz`, `signed_terms.csv`, `signed_term_sign_fractions.csv` | draw-reconstructible per-pair and per-condition four-term signed measurements |
| E/`bootstrap_registration.json`, `bootstrap_signal_localization.py`, `bootstrap_selected.npz`, `intervals.json` | exact-index hierarchical bootstrap and conditional intervals |
| E/`secondary_registration.json`, `secondary_metrics.py`, `occupancy.csv`, `occupancy_group_ratio.csv`, `displacement_capture.csv`, `probe_eval.csv` | static/dynamic geometry, A/B balance, and independent decoding controls |
| E/`failures.json`, `projection_stage_status.json`, `manifest.json` | named resolved deviations and content hashes |
| [0928 figure sources](../../../../../../../daily_research_reports/backup/2026/09/0928/figures/SOURCES.md) | three date-local reading copies and execution-side origins/hashes |

