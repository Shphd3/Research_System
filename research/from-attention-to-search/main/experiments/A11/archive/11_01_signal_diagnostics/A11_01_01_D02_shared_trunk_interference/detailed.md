# Detailed Record: A11_02 Two-Token Shared-Trunk Signal / Interference

Status: `decision_only` and `all_positions_lm_control` completed locally on 2026-07-07. This record is the evidence ledger for A11_02. It does not include curriculum or K>2.

## 1. Purpose And Decision

This experiment tests whether second-token loss $L_2$ in a minimal K=2 Transformer is useful branch signal, redundant/local signal, noisy signal, or useful but difficult to optimize through shared parameters.

The main decision after the `decision_only` run:

`two_token_signal_class = useful branch signal with shared-trunk acquisition instability`.

The reason is precise: `A_clean` improves branch metrics over NTP and over `C_noisy`, but the shared-trunk condition has persistent failed seeds even after a 12000-step diagnostic. $L_1$ is solved, so the current evidence does not support the stronger claim that $L_2$ damages next-token learning in this setup.

The main decision after the `all_positions_lm_control` run:

`two_token_signal_class = useful branch signal under LM-style all-position control, with shared-gradient conflict but no observed L1 performance damage`.

The reason is that all-position `A_clean` shared trunk reaches head-2 accuracy, branch-swap preference, and branch-probe accuracy of `1.00`, while `C_noisy` head-2 stays near $1/16$ chance. Shared embedding and attention gradients remain strongly negative between $L_1$ and $L_2$, but $Y_1$ accuracy remains `1.00`.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| MTP | multi-token prediction | one prefix state predicts more than one future token | objective family | parent objective under study | universal improvement over NTP |
| `decision_only` | train only at the final prefix state | losses computed at `prediction_site` before $Y_1$ | objective scope | matches the theory object $h_T\to(Y_1,Y_2)$ | ordinary LM-style training |
| `A_clean` | useful branch target | $Y_1=U,\;Y_2=S_B$ | data regime | tests branch-specific $L_2$ signal | general MTP usefulness |
| `B_redundant` | locally/redundantly predictable target | $Y_1=S_B,\;Y_2=R(S_B)=T_B$ | data regime | separates redundant target learning from long-horizon signal | zero optimization impact |
| `C_noisy` | branch-independent noisy target | $Y_1=U,\;Y_2=Z,\;Z\perp B$ | data regime | detects arbitrary/noisy auxiliary effects | all noise forms |
| NTP | next-token prediction baseline | true one-head model, $L_1$ only | model condition | baseline without $L_2$ | inability to encode branch in all settings |
| shared trunk | same representation path for both losses | embedding + attention + MLP | parameter path | place where $g_1$ and $g_2$ can conflict | all architectures |
| separate expert | horizon-specific MLP/expert paths | shared embedding and attention; separate experts and heads | model condition | localizes MLP/expert conflict | fair capacity-matched superiority |
| branch probe | linear branch readout from hidden states | frozen linear classifier $h\to B$ | accuracy / CE | representation diagnostic | head usability without guards |
| branch swap | change only the branch token and test head-2 target | swap success / logit margin | rate / margin | causal guard | all shortcut exclusion |
| $c_s$ | gradient cosine | $\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | scalar | local conflict diagnostic | causal proof by itself |
| $r$ | relative gradient size | $\|g_2\|/\|g_1\|$ | ratio | detects domination risk | direction usefulness |
| $\rho$ | $L_1$ direction preservation under combined update | $\langle g_1+\lambda g_2,g_1\rangle/\|g_1\|^2$ | scalar | flags weakening of $L_1$ update | stable when $\|g_1\|$ is tiny |

## 3. Protocol Compliance Audit

| Protocol item | Status | Evidence |
| --- | --- | --- |
| K=2 only | passed | runner supports only two heads / two targets |
| no curriculum | passed | no staged horizon schedule |
| `decision_only` first | passed | `OBJECTIVE_SCOPES=("decision_only",)` in runner |
| three data regimes A/B/C | passed | all 3 regimes run in main matrix |
| three model conditions | passed | NTP, shared trunk, separate expert |
| two init modes | passed | `random` and `identical_branch` |
| five seeds | passed | seeds 971 to 975 |
| NTP true one-head | passed | `ntp_baseline` creates `SharedTrunkModel(..., two_heads=False)` |
| branch probes at multiple positions | passed | `probe_by_position.csv` contains four positions |
| gradient profiling by parameter group | passed | `gradient_profile.csv` and summary table |
| all-position LM control | passed locally | `objective_scope=all_positions_lm_control` run completed and aggregated |
| fully separated control | not run | parked in protocol |

## 4. Implementation Audit

Code workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Key files:

```text
active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json
active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py
active/synthetic_data_understanding/scripts/submit_a11_02_two_token_shared_trunk_signal_interference_4gpu.sh
```

Implementation facts checked from the runner:

- `C_noisy` uses fresh iid draws from a fixed noise-token set through `targets_for_branch(..., rng.choice(vocab.noise_ids))`.
- NTP is a true one-head model; `out.q2_logits` is `None`, so no $L_2$ loss is created.
- `decision_only` losses are computed only from final-position logits: `h_t = h_seq[:, -1, :]`.
- Gradient profiling computes $g_1$ and $g_2$ using `torch.autograd.grad`, then clears gradients before the normal training update.
- Branch-probe training uses detached hidden states and does not update the main model.
- Separate expert shares embedding and attention but separates horizon-specific experts and heads. Its primary branch probe is the horizon-2 stream, so C-noisy probe must be interpreted cautiously.

Known implementation boundary:

- The current runner supports both `decision_only` and `all_positions_lm_control`.
- Separate expert has more parameters than shared trunk. It is a localization diagnostic, not a fair method comparison.

## 5. Runs

### 5.1 Smoke And Main Run

Smoke checks:

- Python compilation passed.
- Small single-condition smoke passed.
- Small full-matrix smoke passed for A/B/C, all model conditions, and both init modes.

Main local run:

```bash
RUN_NAME="a11_02_decision_only_local2gpu_20260707_0411"
CONFIG="active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json"
for SHARD in 0 1; do
  CUDA_VISIBLE_DEVICES=${SHARD} python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
    --config "$CONFIG" \
    --run-name "$RUN_NAME" \
    --device cuda \
    --num-shards 2 \
    --shard-index "$SHARD"
done
python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
  --config "$CONFIG" \
  --run-name "$RUN_NAME" \
  --aggregate-only \
  --num-shards 2 \
  --device cpu
```

Main result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_decision_only_local2gpu_20260707_0411
```

### 5.2 Remote ACP Status

Remote 4-GPU ACP job was submitted:

```text
job id: pt-tydhqbgx
display name: a11-two-token-shared-trunk
workspace: share-space
worker spec: n6ls.iu.i40.4
state at last check: FAILED
```

The remote job produced partial shard logs but did not complete aggregation. No Python traceback was found in the shard logs. The completed evidence in this report comes from the local 2-GPU run and the local 12000-step completion diagnostic.

### 5.3 Completion Diagnostic

Purpose: test whether the 4000-step shared-trunk failures were only an insufficient-training-budget artifact.

Command:

```bash
RUN_NAME="a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545"
CONFIG="active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json"
for SHARD in 0 1; do
  CUDA_VISIBLE_DEVICES=${SHARD} python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
    --config "$CONFIG" \
    --run-name "$RUN_NAME" \
    --device cuda \
    --num-shards 2 \
    --shard-index "$SHARD" \
    --data-regimes A_clean \
    --model-conditions shared_trunk_two_token \
    --training-steps 12000
done
python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
  --config "$CONFIG" \
  --run-name "$RUN_NAME" \
  --aggregate-only \
  --num-shards 2 \
  --device cpu
```

Result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545
```

### 5.4 All-Position Control Run

Purpose: test whether the decision-site conclusion survives a more language-model-like objective where losses are computed at all valid positions.

Local full run:

```bash
RUN_NAME="a11_02_all_positions_lm_control_local2_20260707_0815"
CONFIG="active/synthetic_data_understanding/configs/a11_02_two_token_shared_trunk_signal_interference.json"
for SHARD in 0 1; do
  CUDA_VISIBLE_DEVICES=${SHARD} python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
    --config "$CONFIG" \
    --run-name "$RUN_NAME" \
    --objective-scope all_positions_lm_control \
    --device cuda \
    --num-shards 2 \
    --shard-index "$SHARD"
done
python active/synthetic_data_understanding/scripts/run_a11_02_two_token_shared_trunk_signal_interference.py \
  --config "$CONFIG" \
  --run-name "$RUN_NAME" \
  --objective-scope all_positions_lm_control \
  --aggregate-only \
  --num-shards 2 \
  --device cpu
```

Result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_all_positions_lm_control_local2_20260707_0815
```

Remote ACP status:

```text
job id: pt-3qu9lxh9
display name: a11-two-token-allpos
quota type: SPOT
state at last check: STARTING with worker replicas 0
```

The remote job is not an evidence source. The submit scripts now default to `reserved` for future ACP submissions.

## 6. Data Construction Audit

Source table:

```text
tables/decision_only_sample_table.csv
```

Data rules:

| Regime | $Y_1$ | $Y_2$ | Intended information relation |
| --- | --- | --- | --- |
| `A_clean` | shared token `Y_SHARED` | branch token `S_b` | $I(B;Y_2\mid Y_1)>0$ |
| `B_redundant` | branch token `S_b` | mapped token `T_b` | $I(B;Y_2\mid Y_1)=0$ because $Y_2=R(Y_1)$ |
| `C_noisy` | shared token `Y_SHARED` | iid noise token `Z_i` | $Y_2\perp B$ |

The important distinction is that `B_redundant` can be branch-specific marginally, but it is not new branch information after $Y_1$ is known.

## 7. Central Evidence Tables

Curated tables are stored in:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/tables
```

Central files:

| File | Role |
| --- | --- |
| `decision_only_core_metrics.csv` | compact condition-level means and min/max |
| `decision_only_refinement_metrics.csv` | first primary scalar |
| `decision_only_a_clean_gradient_selected.csv` | selected A-clean shared-gradient diagnostics |
| `decision_only_completion_a_clean_shared_trunk_12000_per_seed.csv` | completion diagnostic per seed |
| `decision_only_sample_table.csv` | data-construction sample table |
| `all_positions_core_metrics.csv` | compact all-position condition-level means |
| `all_positions_gradient_selected.csv` | selected all-position shared-gradient diagnostics |
| `all_positions_hypothesis_status.csv` | all-position hypothesis decision table |

### 7.1 Primary Scalar

| Init mode | A gain over NTP | C gain over NTP | A-vs-C gain |
| --- | ---: | ---: | ---: |
| `identical_branch` | 0.40 | 0.15 | 0.25 |
| `random` | 0.60 | 0.10 | 0.50 |

Interpretation: `A_clean` gives more branch representation gain than `C_noisy`, so $L_2$ is not merely arbitrary noise. However, nonzero C probe gain means branch probe alone is not sufficient.

### 7.2 A-Clean Main Comparison

| Condition | Init | $Y_1$ acc | head-2 acc | probe | swap | $L_1$ loss | $L_2$ loss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ntp_baseline` | identical | 1.00 | NA | 0.25 | NA | 1.76e-06 | NA |
| `shared_trunk_two_token` | identical | 1.00 | 0.65 | 0.65 | 0.65 | 3.54e-06 | 0.624 |
| `shared_attention_separate_expert` | identical | 1.00 | 1.00 | 1.00 | 1.00 | 1.43e-06 | 1.09e-05 |
| `ntp_baseline` | random | 1.00 | NA | 0.30 | NA | 1.81e-06 | NA |
| `shared_trunk_two_token` | random | 1.00 | 0.90 | 0.90 | 0.90 | 4.14e-06 | 0.165 |
| `shared_attention_separate_expert` | random | 1.00 | 0.90 | 0.90 | 0.90 | 1.24e-06 | 0.139 |

Observation: $L_1$ is solved in every A-clean condition. The failure mode is incomplete $Y_2$ branch learning, not next-token collapse.

### 7.3 B-Redundant Control

| Condition | Init | $Y_1$ acc | head-2 acc | probe | swap | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `ntp_baseline` | identical | 0.75 | NA | 0.75 | NA | branch-specific $Y_1$ partly learned |
| `ntp_baseline` | random | 1.00 | NA | 1.00 | NA | branch-specific $Y_1$ fully learned |
| `shared_trunk_two_token` | both | 1.00 | 1.00 | 1.00 | 1.00 | redundant/local continuation is easy |
| `shared_attention_separate_expert` | identical | 0.80 | 0.80 | 0.80 | 0.80 | optimization less stable |
| `shared_attention_separate_expert` | random | 0.95 | 0.95 | 0.95 | 0.95 | mostly solved |

Interpretation: B confirms that high head-2 accuracy is not enough to claim long-horizon branch signal. Here $Y_2$ is determined by $Y_1$.

### 7.4 C-Noisy Control

| Condition | Init | $Y_1$ acc | head-2 acc | probe | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| `ntp_baseline` | identical | 1.00 | NA | 0.25 | branch-blind baseline |
| `ntp_baseline` | random | 1.00 | NA | 0.30 | weak random branch leakage |
| `shared_trunk_two_token` | both | 1.00 | 0.071 | 0.40 | head-2 remains near noise chance |
| `shared_attention_separate_expert` | identical | 1.00 | 0.066 | 0.80 | probe can be high despite useless target |
| `shared_attention_separate_expert` | random | 1.00 | 0.066 | 0.95 | probe-only metric is invalid |

Interpretation: C validates head-2 as a noise guard but weakens branch-probe-only decision rules.

### 7.5 Completion Diagnostic

| Seed | Init | head-2 | probe | swap | $L_2$ loss |
| ---: | --- | ---: | ---: | ---: | ---: |
| 971 | random | 1.00 | 1.00 | 1.00 | 0 |
| 972 | random | 1.00 | 1.00 | 1.00 | 2.98e-08 |
| 973 | random | 0.50 | 0.50 | 0.50 | 0.824 |
| 974 | random | 1.00 | 1.00 | 1.00 | 0 |
| 975 | random | 1.00 | 1.00 | 1.00 | 2.98e-08 |
| 971 | identical | 0.75 | 0.75 | 0.75 | 0.347 |
| 972 | identical | 1.00 | 1.00 | 1.00 | 2.98e-08 |
| 973 | identical | 0.25 | 0.25 | 0.25 | 1.386 |
| 974 | identical | 1.00 | 1.00 | 1.00 | 0 |
| 975 | identical | 0.25 | 0.25 | 0.25 | 1.386 |

Interpretation: persistent failed seeds remain at 12000 steps. The shared-trunk instability is not explained by the original 4000-step budget alone.

### 7.6 Gradient Diagnostics

Selected A-clean gradient means:

| Condition | Init | Group | $c_s$ | $r$ | $\rho$ |
| --- | --- | --- | ---: | ---: | ---: |
| shared trunk | random | embedding | -0.765 | 11.90 | 0.171 |
| shared trunk | random | shared attention | -0.744 | 15.19 | 0.247 |
| shared trunk | random | shared MLP | -0.436 | 9.88 | 0.471 |
| shared trunk | identical | embedding | -0.488 | 85.76 | 4.34 |
| shared trunk | identical | shared attention | -0.432 | 87.94 | 4.28 |
| shared trunk | identical | shared MLP | -0.235 | 47.48 | 1.51 |
| separate expert | random | embedding | -0.448 | 145.64 | 5.80 |
| separate expert | random | shared attention | -0.261 | 249.35 | -2.07 |
| separate expert | identical | embedding | -0.091 | 54.02 | 4.19 |
| separate expert | identical | shared attention | -0.110 | 55.36 | 3.10 |

Interpretation:

- Shared-trunk `random` shows strong negative gradient cosine and $\rho<1$ in embedding, attention, and MLP.
- Shared-trunk `identical_branch` also has negative cosine, but $\rho$ is harder to read because $g_1$ becomes very small after $L_1$ is solved.
- Separate expert removes MLP sharing by construction. Expert groups receive horizon-specific gradients only.
- Attention and embedding conflict can remain even with separate experts.

### 7.7 All-Position Evidence

All-position core result:

| Regime | Condition | Init | $Y_1$ acc | head-2 acc | probe | swap | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `A_clean` | shared trunk | random | 1.00 | 1.00 | 1.00 | 1.00 | branch-specific $L_2$ is learned |
| `A_clean` | shared trunk | identical | 1.00 | 1.00 | 1.00 | 1.00 | branch-specific $L_2$ survives controlled init |
| `B_redundant` | shared trunk | both | 1.00 | 1.00 | 1.00 | 1.00 | learnable but redundant with $Y_1$ |
| `C_noisy` | shared trunk | both | 1.00 | 0.066 | 0.75/1.00 | NA | head-2 stays near noise chance |
| `C_noisy` | separate expert | both | 1.00 | 0.074 | 0.55/1.00 | NA | probe can be high despite useless $Y_2$ |

Gradient result:

| Regime | Condition | Init | embedding $c_s$ | attention $c_s$ | MLP $c_s$ | Interpretation |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `A_clean` | shared trunk | random | -0.943 | -0.943 | 0.091 | strong embedding/attention conflict |
| `A_clean` | shared trunk | identical | -0.938 | -0.946 | -0.125 | strong embedding/attention conflict |
| `B_redundant` | shared trunk | random | -0.945 | -0.949 | 0.239 | conflict can occur even for redundant targets |
| `C_noisy` | shared trunk | random | 0.002 | -0.064 | -0.028 | no comparable strong conflict |

Interpretation: all-position training preserves the useful-signal conclusion and removes the shared-trunk acquisition failure observed in the decision-only run. It does not remove shared-gradient conflict. The conflict is therefore a diagnostic signal, not by itself proof of harmful performance interference.

## 8. Hypothesis Audit

| Hypothesis | Result | Evidence | Claim change |
| --- | --- | --- | --- |
| H1 useful branch signal | supported after all-position control | decision-only A-vs-C gain is 0.25/0.50; all-position A-clean shared trunk reaches head2/swap/probe 1.00 while C head2 stays near chance | keep useful-signal claim under K=2 synthetic objective scopes |
| H2 redundancy | supported with caveat | B shared trunk reaches 1.00 because $Y_2=R(Y_1)$ | B is redundancy/local-predictability control, not long-horizon evidence |
| H3 shared-trunk interference | partially supported / refined | all-position A/B shared trunk has embedding and attention $c_s\approx -0.94$, but $Y_1$ accuracy remains 1.00 | gradient conflict exists, but harmful $L_1$ interference is not established |
| H4 expert localization | supported for decision-only constrained init only | decision-only A-clean identical: shared trunk 0.65, separate expert 1.00; all-position shared trunk already solves A-clean | MLP/expert sharing was a decision-only bottleneck, not a required all-position rescue |
| H5 diagnostic validity | refined | C head-2 chance but probe can be high | head-2/swap guards are mandatory; probe alone is insufficient |

## 9. Failure Analysis

### 9.1 What Failed

The shared-trunk A-clean model does not reliably learn all branch-specific $Y_2$ targets.

Failure examples after 12000 steps:

- random seed 973 remains at head-2/probe/swap `0.50`;
- identical seed 973 remains at `0.25`;
- identical seed 975 remains at `0.25`;
- identical seed 971 remains at `0.75`.

### 9.2 What Did Not Fail

The first-token target is not the failing object. In A-clean, $Y_1$ accuracy is `1.00` across the relevant conditions and $L_1$ losses are near zero.

### 9.3 Most Likely Interpretation

The branch-specific $L_2$ target is useful but can be trapped in partial branch partitions under shared-trunk optimization. Separate experts remove one shared path and fix the most constrained identical-branch case, so the MLP/expert path is a plausible bottleneck. However, attention and embedding remain shared and still show conflict, so the result does not isolate all bottlenecks.

### 9.4 Rival Interpretations Still Possible

- The result may depend on the small synthetic data size and deterministic prefix table.
- Probe training may over-read deterministic branch identity in some streams.
- Extra capacity in separate expert may explain part of its improvement.
- The all-position LM objective may change the interaction by adding dense local supervision.

## 10. Visualization / Table Result Contracts

No central figure is used in this first record. The central evidence is table-based because the decision is a small condition matrix.

### Table: `decision_only_core_metrics.csv`

Question answered: which regimes and model conditions learn $Y_1$, learn $Y_2$, expose branch in hidden states, and pass swap?

Metric definitions:

- `$Y_1$ acc`: top-1 accuracy for $Y_1$.
- `head-2 acc`: top-1 accuracy for $Y_2$.
- `probe`: branch-probe accuracy at `prediction_site`.
- `swap`: branch-swap consistency rate.

Allowed conclusion: condition-level support, failure, or caveat for H1/H2/H5.

Limitation: means hide seed-level partial partitions; use the completion table for seed stability.

### Table: `decision_only_a_clean_gradient_selected.csv`

Question answered: do $L_1$ and $L_2$ point in conflicting directions on shared parameter groups?

Allowed conclusion: local gradient conflict exists or not.

Limitation: gradient conflict is not sufficient causal proof of the final training state, especially when $\|g_1\|$ is tiny.

### Table: `decision_only_completion_a_clean_shared_trunk_12000_per_seed.csv`

Question answered: are the 4000-step shared-trunk failures only due to short training?

Allowed conclusion: persistent failure after 12000 steps weakens the "just train longer" explanation.

Limitation: it does not prove a global impossibility or exclude different learning rates.

## 11. Claim Boundary

Can claim now:

- In this controlled K=2 setup, $L_2$ can carry branch-specific information when $I(B;Y_2\mid Y_1)>0$.
- The useful-signal conclusion survives both `decision_only` and `all_positions_lm_control`.
- Shared-trunk optimization can fail to acquire that information reliably under `decision_only`, but solves `A_clean` under the all-position control.
- Separate experts are a useful localization diagnostic for MLP/expert sharing in the decision-only constrained case.
- Probe-only evidence is unsafe; head-2 accuracy and swap behavior are required guards.
- Shared-gradient conflict can exist without observed $L_1$ accuracy damage.

Cannot claim now:

- $L_2$ harms $L_1$ in this experiment.
- K>2, curriculum, or natural-language settings follow from this result.
- separate experts are a generally better architecture.
- gradient conflict alone proves harmful interference.

## 12. Next Decision

Define and test the smallest K-scaling statement. The next step should not be a broad next-$K$ sweep. It should first use K=3 with one first-informative horizon: earlier targets are shared or redundant, and the later target is branch-specific. The decision question is whether the informative farther horizon improves branch recovery and head prediction beyond NTP and shorter-horizon controls under all-position training.

Completion criterion: a self-contained K=3 anchor and protocol specify the data construction, theorem target, model conditions, and falsifiers; the first run tests K=3 before any curriculum or broad K sweep.

## 13. Artifact Map

Canonical anchor:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_two_token_shared_trunk_signal_interference_anchor.md
```

Protocol:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/protocol.md
```

Result records:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md
```

Curated tables:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/tables/
```

Main raw result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_decision_only_local2gpu_20260707_0411
```

Completion diagnostic result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545
```

All-position result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_02_two_token_shared_trunk_signal_interference/a11_02_all_positions_lm_control_local2_20260707_0815
```

Logs:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/local/a11_02_decision_only_local2gpu_20260707_0411
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/local/a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545
```

Remote job:

```text
ACP job id: pt-tydhqbgx
state at last check: FAILED before aggregation; not an evidence source
```
