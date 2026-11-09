# A11_03_02_E01 Detailed Evidence Record

## 0. Quick Recap

Purpose: test whether informative K=2 MTP makes the ordinary next-token head
causally depend on layer-2 `U03` K/V more strongly than a matched shared-aux
condition.

Hypothesis: at least `4/5` seeds and the five-seed mean satisfy
\(\Gamma_{info}\ge0.10\) after all guards pass.

Experiment: train NTP, shared-aux, and informative-MTP from paired
initializations; select a common capability checkpoint; patch real model-local
same-branch and different-branch source K/V; evaluate all ordered branch pairs
on a sealed confirmation split.

Conclusion: **fail**. All guards passed, but
\(\bar\Gamma_{info}=0.01675\) and `0/5` seeds reached `0.10`.

Evidence: [primary table](tables/causal_use_by_seed.csv),
[capability table](tables/capability_match.csv),
[patch guards](tables/patch_controls.csv), and
[central figure](figures/kv_causal_use_main.png).

## 1. Execution Record

| Field | Value |
|---|---|
| ACP job | `pt-pz6zjzzn` |
| ACP state | `SUCCEEDED` |
| submitted | `2026-07-15T15:58:51Z` |
| completed | `2026-07-15T15:59:58Z` |
| resource | one `n6ls.iu.i40.4` worker, four N6LS-80GB GPUs |
| run name | `a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605` |
| seeds | `971, 972, 973, 974, 975` |
| trajectories | 15: three conditions for each seed |
| config | `active/synthetic_data_understanding/configs/a11_03_02_e01_model_local_kv_causal_use.json` |
| runner | `active/synthetic_data_understanding/scripts/run_a11_03_02_e01_model_local_kv_causal_use.py` |
| submitter | `active/synthetic_data_understanding/scripts/submit_a11_03_02_e01_model_local_kv_causal_use_4gpu_acp.sh` |

Raw result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_03_02_e01_model_local_kv_causal_use/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605
```

Raw log directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605
```

Reproduction command:

```bash
A11_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605 \
bash active/synthetic_data_understanding/scripts/submit_a11_03_02_e01_model_local_kv_causal_use_4gpu_acp.sh
```

## 2. Protocol Compliance

| Contract item | Observed | Verdict |
|---|---|---|
| three registered conditions | NTP, shared-aux, informative-MTP | pass |
| standard full-vocabulary CE | all active heads | pass |
| model | two layers, width 64, one attention head, FFN 256 | pass |
| data | 4096/256/1024 nuisance configurations, four branches each | pass |
| split isolation | zero permutation-hash overlap | pass |
| seeds | 971–975 | pass |
| common checkpoint | one shared step per seed, no post-hoc independent selection | pass |
| intervention | model-local layer-2 `U03` joint K/V | pass |
| primary metric | \(\Gamma_{info}\) only | pass |
| threshold | `0.10`, frozen | pass |
| confirmation | read only after checkpoint and intervention contract were frozen | pass |

No K-only, V-only, Q, layer, horizon, or long-range sweep was run.

## 3. Capability Evidence

| Seed | selected step | shared/info q1 CE gap | all q1 accuracy | shared q2 `U03` | info q2 `U03` |
|---:|---:|---:|---:|---:|---:|
| 971 | 500 | 0.000128 | 1.0 | 1.0 | 1.0 |
| 972 | 500 | 0.000096 | 1.0 | 1.0 | 1.0 |
| 973 | 900 | 0.007056 | 1.0 | 1.0 | 1.0 |
| 974 | 600 | 0.004578 | 1.0 | 1.0 | 1.0 |
| 975 | 700 | 0.003587 | 1.0 | 1.0 | 1.0 |

The standard-head comparison is capability-matched under the frozen rule. NTP
auxiliary-head accuracy is irrelevant because its second head is inactive.

## 4. Intervention Guards

Across all 15 model instances:

- maximum double-precision full-versus-incremental replay error: `2.36e-14`;
- maximum self-patch logit error: `0`;
- same-branch answer-change rate: `0`;
- positive-control donor-answer switch rate: `1.0`;
- clean answer accuracy: `1.0`;
- branch-pair coverage: 12 ordered pairs, 1,024 examples per pair.

The positive control being perfect across all donor examples also verifies that
the output interface and donor labels can express both directions of every
unordered branch pair. The one-sided primary effect in seed 972 is therefore a
learned-channel result, not an incapable patch interface.

## 5. Primary Result

| Seed | \(C_{NTP}\) | \(C_{shared}\) | \(C_{info}\) | \(\Gamma_{info}\) | threshold pass |
|---:|---:|---:|---:|---:|---:|
| 971 | 0 | 0 | 0 | 0 | no |
| 972 | 0 | 0 | 0.083740 | 0.083740 | no |
| 973 | 0 | 0 | 0 | 0 | no |
| 974 | 0 | 0 | 0 | 0 | no |
| 975 | 0 | 0 | 0 | 0 | no |

Mean \(\Gamma_{info}=0.016748\). Passing seeds: `0/5`. The frozen decision JSON
therefore returns `fail` with reason
`registered_information_content_increment_failed`.

Seed 972 is strongly anisotropic. For informative-MTP, receiver branch 3 with
donor branch 1 switched in `1024/1024` examples, while the reverse direction
switched in `5/1024`; all other ordered pairs were zero. This isolated event is
below the seed threshold and absent in the other four seeds.

## 6. Secondary Results

The informative-MTP minus shared-aux donor-margin changes were:

| Seed | margin increment |
|---:|---:|
| 971 | 0.01025 |
| 972 | 2.44658 |
| 973 | -0.00406 |
| 974 | 0.10554 |
| 975 | 0.24083 |

Four seeds are positive and the mean is `0.55983`, but the mean is dominated by
seed 972. This suggests a candidate weak or redundant influence on the ordinary
head's logits. It was not preregistered as a second pass criterion and cannot
override the failed switch-based hypothesis.

Gradient diagnostics also show why averaged loss is not realized gradient
matching. Shared-aux component-gradient cosines were `0.863–0.923`, whereas
informative-MTP cosines were `0.087–0.265`. This is an observation about the
training treatment, not evidence that gradient geometry caused the downstream
behavior.

## 7. Visualization Audit

![Model-local K/V causal-use result](figures/kv_causal_use_main.png)

- Question: does informative-MTP increase strong K/V causal use beyond
  shared-aux?
- Metric and unit: \(C_o\) and \(\Gamma_{info}\), probability difference.
- Source: all confirmation examples and all 12 ordered branch pairs, aggregated
  within seed.
- Reading: the left panel compares condition-level \(C_o\); the right panel
  compares \(\Gamma_{info}\) with zero and `0.10` reference lines.
- Observed result: four seeds are zero; seed 972 is `0.08374`.
- Allowed conclusion: the registered strong, stable increment failed.
- Limitation: the plot does not adjudicate margin-only, redundant, K-only,
  V-only, or Q-mediated effects.

The rendered figure was manually inspected. Labels, seed ordering, legend, and
threshold lines agree with the central table.

## 8. Evidence Classification

Direct result: all technical and capability guards pass; the primary threshold
passes in `0/5` seeds and the mean is `0.01675`.

Interpretation: informative future supervision can alter source-to-output
margins, but does not reliably make this `U03` K/V interface an independently
answer-controlling channel.

Rejected claim: informative K=2 MTP produces a seed-stable strong behavioral
causal-use increment over matched shared-aux at this interface.

Cannot claim: the ordinary head never uses MTP-formed information; MTP is
generally ineffective; or another source position, layer, K/V component, or
receiver policy cannot carry the information.

Exactly one next decision: choose between a preregistered weak-margin audit and
closing this interface in favor of a task where the early state is structurally
necessary. Do not start either without a new decision.
