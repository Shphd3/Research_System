# A11_03_02_E02 Detailed Evidence Record

## 0. Quick Recap

Purpose: determine whether exact layer-2 `U03`
\([K_{2,T};V_{2,T}]\) contains held-out branch information and whether
informative-MTP strengthens that information beyond matched shared-aux.

Registered primary metric:

\[
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}.
\]

Formal verdict: **insufficient** because the registered label-shuffle guard
failed.

Direct bounded result: exact K/V was perfectly linearly branch-readable under
NTP, shared-aux, and informative-MTP in all five seeds, while
\(\bar\Gamma_{\mathrm{read}}=-0.002299\) with a 95% bootstrap interval of
`[-0.004502, -0.000173]`.

## 1. Execution Record

| Field | Value |
|---|---|
| ACP job | `pt-rqtb6bw0` |
| ACP state | `SUCCEEDED` |
| submitted | `2026-07-16T14:58:08Z` |
| execution | `2026-07-16T15:01:41Z` to `2026-07-16T15:02:42Z` |
| resource | one `n6ls.iu.i40.4` worker, four observed NVIDIA H100 80GB GPUs |
| run name | `a11_03_02_e02_exact_source_kv_information_audit_4gpu_20260716_1500` |
| seeds | `971, 972, 973, 974, 975` |
| trajectories | 15: three conditions for each seed |
| config | `active/synthetic_data_understanding/configs/a11_03_02_e02_exact_source_kv_information_audit.json` |
| runner | `active/synthetic_data_understanding/scripts/run_a11_03_02_e02_exact_source_kv_information_audit.py` |
| submitter | `active/synthetic_data_understanding/scripts/submit_a11_03_02_e02_exact_source_kv_information_audit_4gpu_acp.sh` |

Raw result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_03_02_e02_exact_source_kv_information_audit/a11_03_02_e02_exact_source_kv_information_audit_4gpu_20260716_1500
```

Raw log directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_03_02_e02_exact_source_kv_information_audit_4gpu_20260716_1500
```

The original E01 run did not save checkpoints. E02 therefore used the
registered same-contract GPU replay and did not claim to read the old weights.

## 2. Protocol Compliance

| Contract item | Observed | Verdict |
|---|---|---|
| execution surface | remote four-GPU ACP job; no local/CPU model smoke | pass |
| conditions | NTP, shared-aux, informative-MTP | pass |
| data | 4096/256/1024 train/calibration/confirmation nuisances | pass |
| split isolation | zero permutation-hash overlap | pass |
| seeds | 971–975 | pass |
| checkpoint replay | steps `500, 500, 900, 600, 700` | pass |
| E01 behavior replay | all registered switch and margin values reproduced | pass |
| source object | layer-2 `U03` joint K/V, 128 dimensions | pass |
| probe fitting | calibration-only standardization and fixed L2 probe | pass |
| confirmation isolation | no confirmation tuning | pass |
| source-formation guard | `5/5` informative-MTP seeds pass | pass |
| class coverage | all four recalls equal `1.0` | pass |
| label-shuffle guard | three of 15 runs exceed `0.30` | **fail** |

No K-only, V-only, source-Q, receiver-Q, layer, horizon, architecture, or
shared-unembedding sweep was run.

## 3. Replay And Data Guards

All 15 models reproduced the original E01 selected step exactly. The replayed
controlled switch effects and donor-margin changes equal the reference values
recorded in the configuration. Across all models:

- ordinary-head answer accuracy was `1.0`;
- active shared-aux and informative-MTP `U03` target accuracy was `1.0`;
- maximum full-versus-incremental cache error was below `2.36e-14`;
- self-patch error was `0`;
- same-branch answer-change rate was `0`;
- final-hidden-state positive-control switch rate was `1.0`.

The train, calibration, and confirmation sets were balanced across four
branches and had no nuisance-permutation hash overlap.

Sources: [replay table](tables/replay_guard.csv) and
[data table](tables/data_guard.csv).

## 4. Absolute Source Formation

For each seed and condition, a separate four-class linear probe was fitted on
1,024 calibration sequences and frozen before evaluation on 4,096 confirmation
sequences.

| Condition | Mean confirmation CE | Accuracy range | Recall range |
|---|---:|---:|---:|
| NTP | 0.000486 | 1.0–1.0 | 1.0–1.0 |
| shared-aux | 0.000528 | 1.0–1.0 | 1.0–1.0 |
| informative-MTP | 0.002827 | 1.0–1.0 | 1.0–1.0 |

Thus exact layer-2 `U03` K/V contains a stable linearly decodable branch label
under every objective. The human prior that branch information should be
present in K/V is supported in this bounded linear sense.

The result does not support MTP-specific source formation: NTP and shared-aux
already reach perfect branch decoding. Because the input begins with explicit
`BR_z` and every later position can attend it under the standard causal mask,
generic source formation is an expected surviving explanation.

Sources: [probe table](tables/probe_by_condition_seed.csv) and
[formation guard](tables/source_formation_by_seed.csv).

## 5. Registered Primary Result

| Seed | shared-aux CE | informative-MTP CE | \(\Gamma_{\mathrm{read}}\) |
|---:|---:|---:|---:|
| 971 | 0.0010209 | 0.0056748 | -0.0046539 |
| 972 | 0.0002403 | 0.0011652 | -0.0009249 |
| 973 | 0.0003397 | 0.0004371 | -0.0000974 |
| 974 | 0.0006880 | 0.0066374 | -0.0059493 |
| 975 | 0.0003513 | 0.0002223 | 0.0001291 |

Mean:

\[
\bar\Gamma_{\mathrm{read}}=-0.0022993.
\]

The paired nuisance-within-seed and paired-seed bootstrap 95% interval was

\[
[-0.0045019,-0.0001735].
\]

The direction was nonpositive in `4/5` seeds. Under the main metric alone this
would meet the registered failure direction. The complete decision contract,
however, also required the label-shuffle guard. Its failure forces the formal
`insufficient` verdict.

The CE values are all very close to zero and every probe has accuracy `1.0`.
Therefore the small negative CE difference is a probe-margin result at a
saturated boundary. It cannot be interpreted as loss of the two-bit branch
label or general representation degradation.

Source: [paired primary table](tables/gamma_read_by_seed.csv).

## 6. Secondary Geometry

| Seed | Fisher shared-aux | Fisher informative-MTP | ratio info/shared | within-dispersion ratio | between-dispersion ratio |
|---:|---:|---:|---:|---:|---:|
| 971 | 2.543 | 42.975 | 16.90 | 0.080 | 1.348 |
| 972 | 41.686 | 409.574 | 9.83 | 0.104 | 1.022 |
| 973 | 8.648 | 89.182 | 10.31 | 0.107 | 1.103 |
| 974 | 7.209 | 20.990 | 2.91 | 0.373 | 1.085 |
| 975 | 49.612 | 2458.015 | 49.55 | 0.021 | 1.021 |

Informative-MTP had a larger Fisher ratio in every seed. Most of the gain came
from contracting variation among different nuisance permutations within the
same branch. Pairwise centroid distances were mixed, so the result is better
described as nuisance compaction and relative geometric organization than as
uniformly larger pairwise distances.

This secondary result is stable enough to update the mechanism hypothesis:
MTP may alter how the shared trunk organizes already-readable branch
information. It cannot be promoted to proof of extra information, downstream
readout, standard-head use, or task benefit.

Source: [Fisher table](tables/fisher_by_condition_seed.csv). Full pairwise
centroid distances remain in the raw result directory.

## 7. Label-Shuffle Guard Audit

The registered guard required all shuffled-label confirmation accuracies to be
at most `0.30`. Observed across 15 probes:

- mean accuracy: `0.2209`;
- range: `0.0837–0.3357`;
- values above `0.30`: `3/15`;
- mean CE: `1.4427`;
- four-class chance CE: \(\log 4=1.3863\).

The maximum-accuracy rule was not well calibrated for a representation that
already forms four nearly deterministic clusters. A single global random
shuffle gives each true cluster small random calibration-label imbalances; the
probe can map a cluster to the accidentally most frequent random label, and a
chance alignment with the original class then moves confirmation accuracy in
large cluster-sized increments. Taking the maximum over 15 such fits further
inflates the probability of exceeding `0.30`.

This pattern is more consistent with a guard-design problem than with broad
train-confirmation leakage, because mean shuffled accuracy is below chance and
mean CE is worse than chance. That is a post-result diagnosis, not a
preregistered pass. A future protocol should use repeated shuffles and a
distributional CE criterion, but E02 remains formally insufficient.

One non-decision diagnostic field also needs correction before code reuse:
`probe_final_objective` stores the value returned by the first LBFGS closure,
not a recomputed post-optimization objective. It therefore appears as
`1.386294` even though the fitted parameters used for confirmation are the
optimized parameters. This field was not used by any metric, guard, interval,
or verdict, so it does not change the result above.

## 8. Combined Causal Reading With E01

E01 and E02 answer different links:

| Causal link | Evidence | Current reading |
|---|---|---|
| exact source K/V contains branch signal | E02 held-out probes | yes, under all three objectives |
| informative-MTP adds probe-readable branch information | E02 \(\Gamma_{\mathrm{read}}\) | not supported; controls are saturated |
| informative-MTP reorganizes branch/nuisance geometry | E02 Fisher diagnostic | candidate support, secondary only |
| ordinary head strongly uses the source more under informative-MTP | E01 K/V patch | registered strong increment failed |

The new evidence rejects the simplest absolute-formation explanation for E01:
the patched object is not linearly branch-empty. It does not establish the
stronger story “MTP-specific information formed but the ordinary head ignored
it,” because MTP-specific readable information was not identified.

The remaining task confounds are direct access from the answer position to
`BR_z`, redundant source paths, saturated answer margins, and a receiver policy
that was not forced to rely on `U03`.

## 9. Visualization Audit

![Exact source-K/V readability audit](figures/source_kv_information_audit.png)

- Question: does informative-MTP lower held-out branch-probe CE relative to
  shared-aux?
- Metric and unit: confirmation CE and
  \(\Gamma_{\mathrm{read}}=\mathrm{CE}_{shared}-\mathrm{CE}_{info}\),
  nat/example.
- Source: 4,096 confirmation sequences per seed and condition; paired
  nuisance and seed bootstrap.
- Reading: the left panel shows per-condition CE; the right shows paired
  \(\Gamma_{\mathrm{read}}\) and zero.
- Allowed conclusion: no positive registered CE improvement is observed.
- Limitation: the plot does not show the failed shuffle guard, causal use, or
  the secondary Fisher compaction.

The rendered artifact was inspected. Seed ordering, condition labels, metric
sign, and confidence-interval annotation agree with the tables. The title is
close to the right boundary but the numerical interval remains readable.

## 10. Evidence Classification And Next Decision

Direct result: exact source K/V is perfectly branch-readable for all objectives;
the registered CE increment is negative in `4/5` seeds; the shuffle guard
fails.

Interpretation: the current A11 construction makes branch identity generically
available, while informative future supervision appears to compact nuisance
geometry without producing a registered readability or strong-use increment.

Cannot claim: informative-MTP adds no information of any kind; the ordinary
head never uses MTP-related information; Fisher compaction causes behavior;
shared unembedding would repair the effect; or the result transfers to
long-range, natural-language, composition, or MoE settings.

Exactly one next decision: validate a `relay-required` carrier with no direct
answer bypass and a non-saturated shared-aux baseline before any new
objective comparison. Do not run a K/V/Q/layer or shared-unembedding sweep on
the current bypass-open task.
