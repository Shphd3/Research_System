派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/detailed.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/detailed.md)；研究修改仍回到原件。

---

# Detailed A15_24_03：Direction intervention under frequency conditioning: full evidence and credibility

[Summary](summary.md) · [Protocol](protocol.md) · [Artifact manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/artifact_manifest.json)

**Execution complete; primary frequency inference insufficient.**11pairs/9dialogues, opposite seed signs and intervals crossing zero. This neither accepts stable association nor demonstrates its absence. Valid finite effects are separate from inadequate frequency interpretation.

## Objects and actual procedure

Reuse original T_F seeds11/22 step168 and initialization. Only E0 up has1,048,576 temporarily editable entries. Other23 expert matrices,scale and frozen head remain fixed. Full1024-dimensional final hidden inputs are retained; two experts contribute.5 each. SwiGLU gate/up product passes down into a residual and frozen RMS/head yields actual next-token NLL. No new training,gradient or optimizer.

Roll back25%/50% of net displacement D along existing TRAIN PCA16. D is neither full W nor replayed history. Eight random Gaussian-QR bases use seed20261024+31r, shared across models; actual edit norms match PCA. FP64 projections,FP32 parameters/forwards,TF32off. All conditions evaluate the same693 E0 positions,micro64; restore original models.

## Data,events and matching

Original TRAIN85548positions/1024dialogues,DEV10340/128;693affected positions across109dialogues. Stored frequency exactly equals TRAIN positive counts/85548,not DEV redefinition. B1/B2/B3/B4 have417/2808/6761/1097supported features and908/7195/97021/132768events. These237892events are not independent losses. B1/B4 cover the same693 positions; B2 covers690,B3 covers693.

Primary pairs use different positions with identical dialogue,current-token and other routed expert. Five covariates:log(z×decoder norm),log decoder norm,log hidden RMS,mean inherited two-seed baseline NLL,position/input length. Contribution is an amplitude proxy,not raw z,controlled together with decoder norm. Original data/dev.jsonl block/position/target aligns current and next tokens.

Scale by combined B1+B4 event SD; per-coordinate caliper.5. Greedy global squared-distance matching with deterministic position/feature ties; each position at most once. Frequency is not matched away and feature identity is not randomized. Same-dialogue context/semantics can differ. High-side positions can also contain other low features; labels do not define pure inputs.

Covariate preflight used existing baseline but no new intervened losses.86 repeated within-dialogue/token/route groups contain218positions;285 candidate event edges yield11 position pairs/9dialogues. A cross-dialogue same-source/token/route diagnostic with disjoint dialogues has one pair and does not replace primary.

| Covariate | SMD(low−high) | Eligibility bound |
|---|---:|---:|
| log_contribution | +0.071780 | ±0.1 |
| log_decoder_norm | -0.106611 | ±0.1 |
| log_hidden_RMS | +0.028225 | ±0.1 |
| baseline_NLL | +0.025068 | ±0.1 |
| relative_position | +0.151256 | ±0.1 |

Two SMDs fail. Every pair is within.5SD,but local proximity does not ensure aggregate balance. The20pairs/10dialogues gate is an AI operational rule frozen after covariate preflight but before new effects,not a power analysis or independent preregistration. Insufficiency was known at freeze.

## Matched and band results

T is low-minus-high PCA loss change minus mean8random equivalent contrast. Positive=greater low-side excess harm. Raw/random contrasts remain explicit.50%primary,25%secondary;unit nat.

| Seed | Rollback | PCA low−high | Mean random low−high | Excess T | Conditional95% interval |
|---|---:|---:|---:|---:|---|
| 11 | 0.25 | -0.000482746 | +0.000015154 | -0.000497900 | [-0.002294919, +0.001350924] |
| 11 | 0.5 | -0.000960490 | +0.000034976 | -0.000995466 | [-0.004580875, +0.002690475] |
| 22 | 0.25 | +0.001991024 | +0.000045373 | +0.001945651 | [-0.005056263, +0.008899924] |
| 22 | 0.5 | +0.004019452 | +0.000088292 | +0.003931161 | [-0.010033855, +0.017777335] |

5000dialogue bootstrap draws retain all pairs within a resampled dialogue.95%intervals are conditional on fixed models,bases,matches; they do not include model-seed/random-basis population uncertainty. Nine dialogues are inadequate for robust inference and both seeds share evaluation data.

Leave-one-random-out50% T ranges[−.001102,−.000909] for11,[+.003687,+.004119] for22. Within-model sign stability does not repair opposite seed signs/support. Cross-dialogue single-pair values remain in results.json without interval inference.

The following four-band feature macros use the same693affected-position scope: average loss difference within each supported feature,then equally across features. They are unmatched,overlapping and dependent. They neither isolate feature deletion nor dilute with unaffected full-DEV positions.

| Seed | Rollback | Band | Supported features | Events | PCA macro loss delta | Mean8random macro delta |
|---|---:|---|---:|---:|---:|---:|
| 11 | 0.25 | B1 | 417 | 908 | +0.000215328 | -0.000024426 |
| 11 | 0.25 | B2 | 2808 | 7195 | -0.000037329 | -0.000049490 |
| 11 | 0.25 | B3 | 6761 | 97021 | +0.000186966 | -0.000030346 |
| 11 | 0.25 | B4 | 1097 | 132768 | +0.000386079 | -0.000025828 |
| 11 | 0.5 | B1 | 417 | 908 | +0.000569578 | -0.000046804 |
| 11 | 0.5 | B2 | 2808 | 7195 | +0.000059176 | -0.000096782 |
| 11 | 0.5 | B3 | 6761 | 97021 | +0.000494969 | -0.000058667 |
| 11 | 0.5 | B4 | 1097 | 132768 | +0.000903841 | -0.000049712 |
| 22 | 0.25 | B1 | 417 | 908 | +0.000849884 | +0.000047897 |
| 22 | 0.25 | B2 | 2808 | 7195 | +0.000338863 | -0.000005252 |
| 22 | 0.25 | B3 | 6761 | 97021 | +0.000084810 | -0.000014830 |
| 22 | 0.25 | B4 | 1097 | 132768 | +0.000124562 | -0.000018858 |
| 22 | 0.5 | B1 | 417 | 908 | +0.001917561 | +0.000098028 |
| 22 | 0.5 | B2 | 2808 | 7195 | +0.000849839 | -0.000008774 |
| 22 | 0.5 | B3 | 6761 | 97021 | +0.000342540 | -0.000027668 |
| 22 | 0.5 | B4 | 1097 | 132768 | +0.000448963 | -0.000035049 |

## All40 readouts

PCA=candidate rollback,R0–R7=fixed random bases,suffix0p25/0p5=rollback fraction. Each starts from original W. This table weights693 positions equally,unlike feature macros. Every readout is DONE_VALID; frequency inference remains INSUFFICIENT.

| Seed/condition | Mean NLL on693 positions | Baseline delta | Actual parameter-edit norm | Relative norm mismatch |
|---|---:|---:|---:|---:|
| 11/baseline | 0.944763399 | +0.000000000 | 0.000000000 | 0 |
| 11/exact_noop | 0.944763399 | +0.000000000 | 0.000000000 | 0 |
| 11/PCA_0p25 | 0.944962060 | +0.000198661 | 0.252217789 | 0 |
| 11/R0_0p25 | 0.944724797 | -0.000038602 | 0.252217790 | 3.92e-09 |
| 11/R1_0p25 | 0.944698596 | -0.000064804 | 0.252217790 | 5e-09 |
| 11/R2_0p25 | 0.944645436 | -0.000117963 | 0.252217791 | 7.5e-09 |
| 11/R3_0p25 | 0.944863975 | +0.000100576 | 0.252217789 | 2.96e-09 |
| 11/R4_0p25 | 0.944743414 | -0.000019985 | 0.252217791 | 8.37e-09 |
| 11/R5_0p25 | 0.944626078 | -0.000137321 | 0.252217789 | 1.01e-09 |
| 11/R6_0p25 | 0.944786146 | +0.000022747 | 0.252217790 | 3.29e-09 |
| 11/R7_0p25 | 0.944722282 | -0.000041117 | 0.252217790 | 5.95e-09 |
| 11/PCA_0p5 | 0.945291155 | +0.000527756 | 0.504435581 | 0 |
| 11/R0_0p5 | 0.944687770 | -0.000075629 | 0.504435580 | 1.95e-09 |
| 11/R1_0p5 | 0.944636430 | -0.000126969 | 0.504435580 | 1.24e-09 |
| 11/R2_0p5 | 0.944530695 | -0.000232704 | 0.504435580 | 1.08e-09 |
| 11/R3_0p5 | 0.944966447 | +0.000203048 | 0.504435579 | 3.04e-09 |
| 11/R4_0p5 | 0.944725156 | -0.000038243 | 0.504435579 | 3.28e-09 |
| 11/R5_0p5 | 0.944491821 | -0.000271578 | 0.504435580 | 2.06e-09 |
| 11/R6_0p5 | 0.944809954 | +0.000046555 | 0.504435578 | 4.73e-09 |
| 11/R7_0p5 | 0.944681576 | -0.000081823 | 0.504435578 | 5.2e-09 |
| 22/baseline | 0.947763094 | +0.000000000 | 0.000000000 | 0 |
| 22/exact_noop | 0.947763094 | +0.000000000 | 0.000000000 | 0 |
| 22/PCA_0p25 | 0.947798454 | +0.000035360 | 0.241657130 | 0 |
| 22/R0_0p25 | 0.947721742 | -0.000041352 | 0.241657128 | 5e-09 |
| 22/R1_0p25 | 0.947741422 | -0.000021672 | 0.241657128 | 5.34e-09 |
| 22/R2_0p25 | 0.947806167 | +0.000043073 | 0.241657128 | 6.07e-09 |
| 22/R3_0p25 | 0.947803832 | +0.000040738 | 0.241657128 | 5.23e-09 |
| 22/R4_0p25 | 0.947703071 | -0.000060023 | 0.241657128 | 4.3e-09 |
| 22/R5_0p25 | 0.947691821 | -0.000071273 | 0.241657129 | 1.34e-09 |
| 22/R6_0p25 | 0.947716450 | -0.000046644 | 0.241657128 | 6.82e-09 |
| 22/R7_0p25 | 0.947717651 | -0.000045443 | 0.241657130 | 2.76e-09 |
| 22/PCA_0p5 | 0.948023427 | +0.000260333 | 0.483314257 | 0 |
| 22/R0_0p5 | 0.947682114 | -0.000080980 | 0.483314257 | 1.77e-10 |
| 22/R1_0p5 | 0.947722269 | -0.000040825 | 0.483314258 | 1.1e-09 |
| 22/R2_0p5 | 0.947853179 | +0.000090085 | 0.483314258 | 1.94e-09 |
| 22/R3_0p5 | 0.947846494 | +0.000083400 | 0.483314257 | 5.1e-10 |
| 22/R4_0p5 | 0.947646710 | -0.000116384 | 0.483314258 | 1.97e-09 |
| 22/R5_0p5 | 0.947623881 | -0.000139213 | 0.483314257 | 3.84e-10 |
| 22/R6_0p5 | 0.947673255 | -0.000089839 | 0.483314257 | 1.19e-09 |
| 22/R7_0p5 | 0.947672846 | -0.000090248 | 0.483314258 | 2.3e-09 |

## A real pair and its limits

The first pair by prespecified distance order,not effect selection:dialogue110,current-tokenID15,other expert2; low position9218/feature1497,high position9217/feature13076. Frequencies4/85548 and5369/85548. Seed11,50%:PCA deltas−.000065497/+.000059265;mean random−.000005557/+.000003942;paired excess−.000115264nat. One position improves while the other worsens,showing average damage is not uniform.

Positions differ and high side also contains low features; this is not isolated contributions of1497/13076. All48 seed/dose/pair records are in paired_effects.csv;44,332feature rows in feature_effects.csv. Same-position band copies necessarily yield zero difference,an identity rather than a frequency null.

## Credibility,deviations and verification

| Check | Observation | Scope |
|---|---|---|
| Four original tensor digests |Match original receipts |Exact model identity |
|FP32 replay/no-op |Maxerror0; elementwise equal |Same-environment consistency |
|Freeze/restore |Other tensors/head unchanged;full digest restored |Only intended matrix edited |
|8random bases/rank/norm |Rank16,orthonormal;norm mismatch<8.4e-9 |Equal parameter size,not equal functional size |
|Independent CPU aggregation |40readouts,pairs,intervals,44332feature rows;maxerror0 |Aggregation,not mechanism |
|Budget |70.110s; GPU 0.995GiB; CPU RSS 2.687GiB;about11.3MiBoutput |Below900s/12GiB/1GiB |
|Primary qualification |11pairs/9dialogues,2SMDfailures |Association inference insufficient |

The GPU worker succeeded once with no missing arms. Metadata preflight and CPU verification repaired repeated compressed-npz decompression by loading arrays once; own slow CPU attempts were stopped,old source/log/repair records retained. No scientific setting,pair or GPU outcome changed. Independent verification does not call worker metric functions. Frozen Protocol/GPU source remain unchanged. No new trained checkpoint,hidden representation or dictionary cache was created.

Three distinct audit rounds by the same Codex /root,not independent reviewers:scientific identification BOUNDED;data/statistics INSUFFICIENT_PRIMARY;implementation/numerics PASS. Full [verification.json](../../../../../../../../UNAVAILABLE.md) and [audits.json](../../../../../../../../UNAVAILABLE.md).

## Evidence lineage and reproduction

| Quantity | Raw material | Computation/scope |
|---|---|---|
|Frequency labels |groups.npz andTRAIN positive counts |Original fixed bands rechecked |
|Match eligibility |event_covariates,matched_pairs,preflight |No new effect selection;failures retained |
|Finite predictive effects |693positions×20conditions per seed |Actual fixed-input/target forwards |
|PrimaryT/interval |Position NLL,11fixedpairs |PCA−8random,thenlow−high;9dialoguebootstrap |
|Band macros |Feature occurrence positions |Unmatched,not independent tasks |
|Measurement eligibility |No-op,hashes,freeze,norms,verification |Implementation,not scientific acceptance |

- [Machine contract](../../../../../../../../UNAVAILABLE.md)
- [Freeze identity](../../../../../../../../UNAVAILABLE.md)
- [Actual GPU program](../../../../../../../../UNAVAILABLE.md)
- [Matching implementation](../../../../../../../../UNAVAILABLE.md)
- [All paired effects](../../../../../../../../UNAVAILABLE.md)
- [All feature effects](../../../../../../../../UNAVAILABLE.md)
- [Seed11position NLL](../../../../../../../../UNAVAILABLE.md)
- [Seed22position NLL](../../../../../../../../UNAVAILABLE.md)
- [All structured results](../../../../../../../../UNAVAILABLE.md)
- [Independent verifier](../../../../../../../../UNAVAILABLE.md)
- [Pre-run asset access](../../../../../../../../UNAVAILABLE.md)
- [I/O repairs](../../../../../../../../UNAVAILABLE.md)
- [Local run log](../../../../../../../../UNAVAILABLE.md)

Protocol retains the six input asset IDs and current strict-access snapshot. Payloads remain execution-side. Run `python verify.py` for verification; `python -u worker.py` reruns interventions and was not repeated for display. Frozen design bytes remain in frozen_documents;current Anchor only appends a factual result link. Complete digests/sizes are in artifact_manifest.json.

Scientific judgment/next decision Unknown pending researcher review of implementation and credibility. No move to forgetting,new architecture or long training.
