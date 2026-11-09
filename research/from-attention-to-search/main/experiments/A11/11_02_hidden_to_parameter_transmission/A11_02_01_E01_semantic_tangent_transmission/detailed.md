# Detailed: A11_02_01_E01 K=2 Semantic Tangent-Kernel Transmission

Primary anchor: [11_02_01 reachability and background-sign subanchor](../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** test whether the controlled K=2 hidden-state semantic signal is transmitted into shared Transformer encoder parameters.

**Hypothesis:** at a folded reference point, direct K=2 semantic transmission follows \(\alpha^2\), branch-common H1 background follows \(\alpha\), and the native total velocity remains positive:

\[
G_{\theta,total}
=G_{\theta,direct}+G_{\theta,background}.
\]

**Conclusion:** supported. The valid remote 4-GPU run completed 35/35 tasks, passed calibration in 5/5 seeds, and supported H2/H3/local guards.

**Evidence:** native direct velocity is positive in 5/5 seeds; native full-K2 net velocity is positive in 5/5 seeds; one-step margin movement matches the linear prediction in 20/20 main comparisons.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Semantic margin | branch state alignment with correct H2 output row | \(M_2=\frac1m v^\top H_\alpha(\theta)\) | scalar | target of the parameter update | downstream semantics |
| Direct velocity | K=2 H2 contribution to semantic margin movement | \(G_{\theta,direct}\) | velocity | MTP-specific parameter signal | total training result |
| Background velocity | shared H1 contribution to semantic margin movement | \(G_{\theta,background}\) | signed velocity | tests interference/help | all-position effects |
| Total velocity | sum of direct and background terms | \(G_{\theta,total}\) | velocity | primary anchor metric | long-run convergence |
| Kernel signal | encoder reachability along \(v\) | \(v^\top\Theta v/m^2\) | velocity scale | detects parameter bottleneck | finite-step persistence |
| Net-preservation ratio | retained direct signal after background | \(\rho_{\theta,net}=G_{\theta,total}/G_{\theta,direct}\) | unitless | reversal test | absolute speed |
| Jacobian scale | semantic sensitivity intervention | \(\alpha=0,0.5,1\) | condition | tests the proved scaling law | natural variation |
| One-step fidelity | actual finite update versus linear prediction | \(\Delta M_2\approx\eta G_{\theta,total}\) | relative error | checks nonlinear remainder | long-run curvature |

## 2. Anchor Link And Decision Point

The anchor decision was whether the objective-level K=2 semantic direction survives shared-encoder parameterization after removing trivial output-head and embedding paths.

The main falsifier was:

```text
positive hidden semantic velocity
but unresolved shared-encoder J^T v or nonpositive full-K2 net velocity.
```

This falsifier did not occur.

## 3. Protocol Compliance Audit

| Item | Status |
| --- | --- |
| Conditions match protocol | pass: 7 conditions per seed |
| Seeds | pass: 971, 972, 973, 974, 975 |
| Remote 4-GPU full run | pass: job `pt-50l5l908` |
| Shards | pass: 9 / 9 / 9 / 8 tasks |
| Task count | pass: 35/35 |
| Checkpoints | pass: all 35 tasks have 9/9 checkpoints |
| Calibration | pass: 5/5 seeds |
| Frozen embeddings and heads | pass: drift/update norms are zero |
| Central figure | pass: `figures/a11_11_transmission_and_dynamics.png` |

The earlier remote run `a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_123830` is not used as evidence. It failed the calibration guard because GPU float32 head construction made the fixed-head geometry error too large. The implementation was corrected by constructing the regular-simplex heads in CPU float64 and by making the ACP command fail on invalid smoke/aggregate results. The valid evidence run is `a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`.

## 4. Setup

**Data construction:** four deterministic branches with:

\[
Y_1=A,\qquad Y_2=S_Z,\qquad Z\in\{1,2,3,4\}.
\]

**Model:** one-layer causal Transformer, `d_model=64`, one attention head, float64, dropout 0.

**Frozen components:** token embeddings, H1 output head, and H2 output head.

**Trainable components:** shared attention, MLP, LayerNorm, and position parameters.

**Objective conditions:**

| Condition | Loss | \(\alpha\) values | Role |
| --- | --- | --- | --- |
| `shared_only_k1` | \(L_1\) | 1 | no-direct guard |
| `direct_only_k2` | \(L_2\) only | 0, 0.5, 1 | direct semantic transmission |
| `full_k2` | \(L_1+L_2\) | 0, 0.5, 1 | background plus direct |

**Training:** full-batch SGD, learning rate `0.003`, no weight decay, 200 steps.

**Checkpoints:** `0,1,2,5,10,20,50,100,200`.

**Result directory:**

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_11_k2_semantic_tangent_kernel_transmission/a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514
```

## 5. Metrics And Decision Rules

### 5.1 Reference calibration

Direct transmission should obey:

\[
G_{\theta,direct}(\alpha)
=\alpha^2G_{\theta,direct}(1).
\]

Background transmission should obey:

\[
G_{\theta,background}(\alpha)
=\alpha G_{\theta,background}(1).
\]

These are implementation guards, not the scientific claim.

### 5.2 Native parameter transmission

The scientific quantity is the native \(\alpha=1\) velocity:

\[
G_{\theta,total}(1)
=G_{\theta,direct}(1)+G_{\theta,background}(1).
\]

Pass requires resolved positive \(G_{\theta,direct}(1)\) and positive \(G_{\theta,total}(1)\) in at least 4/5 seeds.

### 5.3 Net-preservation ratio

When the direct term is above numerical floor:

\[
\rho_{\theta,net}
=\frac{G_{\theta,total}}{G_{\theta,direct}}
=1+\chi_\Theta r_\Theta.
\]

This tells whether H1 reverses the K=2 direct term. Negative \(\chi_\Theta\) alone is not a failure.

### 5.4 One-step fidelity

For an SGD step:

\[
\Delta M_2
=M_2(\theta-\eta\nabla_\theta L)-M_2(\theta)
\approx \eta G_{\theta,total}.
\]

Pass requires sign match and relative error at most `0.25` in at least 4/5 seeds.

## 6. Main Results

### 6.1 Decision evidence

| Metric | Mean | Min | Max | Pass meaning |
| --- | ---: | ---: | ---: | --- |
| direct \(\alpha=0\) | \(8.92\mathrm{e}{-33}\) | \(0\) | \(4.46\mathrm{e}{-32}\) | semantic-null intervention is zero |
| direct \(\alpha=0.5\) | `0.014097` | `0.009663` | `0.020274` | positive half-scale direct signal |
| direct \(\alpha=1\) | `0.056388` | `0.038651` | `0.081096` | native encoder carries \(J^\top v\) |
| direct half ratio | `0.250000` | `0.250000` | `0.250000` | \(\alpha^2\) law |
| background \(\alpha=0.5\) | `0.001760` | `-0.002985` | `0.007455` | signed background exists |
| background \(\alpha=1\) | `0.003520` | `-0.005970` | `0.014910` | H1 may help or oppose |
| background half ratio | `0.500000` | `0.500000` | `0.500000` | \(\alpha\) law |
| native total velocity | `0.059908` | `0.045335` | `0.082070` | full K2 net remains positive |
| native \(\rho_{\theta,net}\) | `1.089587` | `0.886259` | `1.362119` | no seed reverses |
| native kernel cosine | `0.002640` | `-0.003681` | `0.010621` | sign varies, but small |
| native kernel norm ratio | `29.699544` | `23.325358` | `34.093272` | background norm can be large |

H2 is supported because direct transmission and full-K2 net velocity are positive in 5/5 seeds.

### 6.2 One-step fidelity

| Condition | \(\alpha\) | Sign matches | Mean relative error | Max relative error | Protocol pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| `direct_only_k2` | 0.5 | 5/5 | `0.000459` | `0.000933` | yes |
| `direct_only_k2` | 1.0 | 5/5 | `0.000918` | `0.001866` | yes |
| `full_k2` | 0.5 | 5/5 | `0.018242` | `0.033786` | yes |
| `full_k2` | 1.0 | 5/5 | `0.008165` | `0.013457` | yes |

H3 is supported at the one-step level.

### 6.3 Early training dynamics

Early margin AUC through step 50:

| Condition | \(\alpha=0\) | \(\alpha=0.5\) | \(\alpha=1\) |
| --- | ---: | ---: | ---: |
| `direct_only_k2` | approximately `0` | `0.001078` | `0.004453` |
| `full_k2` | approximately `0` | `0.001107` | `0.004524` |

The ordering \(\alpha=1>0.5>0\) holds in 10/10 seed-condition checks.

Final local guard:

| Guard | Result |
| --- | ---: |
| shared-only Y1 accuracy | mean `1.0` |
| full-K2 Y1 accuracy | mean `1.0` |
| full minus shared Y1 accuracy | `0.0` |
| full-K2 H2 accuracy | mean `0.9`, min `0.5` |
| full-K2 branch-swap consistency | mean `0.966667`, min `0.833333` |
| embedding update norm | `0.0` |
| head drift norms | `0.0` |

The seed974 final H2 accuracy in `full_k2, alpha=1` is `0.5`, although its margin is positive and branch-swap consistency is `0.833333`. This does not violate the protocol because A11_02_01_E01's primary question is local parameter transmission and one-step fidelity, not guaranteed 200-step H2 convergence in every seed.

## 7. Visualization Results

### Tangent-kernel transmission and finite-step dynamics

![Tangent-kernel transmission and finite-step dynamics](figures/a11_11_transmission_and_dynamics.png)

**Purpose:** summarize the four decision checks in one figure.

**Setup:** valid 4-GPU run `a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`.

**Metric definition:** parameter semantic velocity is \(-\langle\nabla_\theta M_2,\nabla_\theta L\rangle\); actual one-step movement is measured by virtual SGD updates.

**Metric unit:** semantic-margin change per unit learning rate, except for the lower-left plot where the unit is actual \(\Delta M_2\).

**How to read:** upper-left checks scaling; upper-right checks native seed-wise decomposition; lower-left checks linearized versus actual one-step motion; lower-right checks early margin curves.

**Observed result:** direct transmission follows \(\alpha^2\), H1 background follows \(\alpha\), full native total stays positive, and one-step points lie close to the identity line.

**Take-home:** the K=2 direct semantic signal is not only a hidden-state objective signal; it is locally transmitted by the shared encoder parameters in this controlled setting.

**Remaining uncertainty:** all-position losses, stochastic batches, AdamW, larger models, and natural-language semantics are outside this experiment.

**Anchor update implication:** A11_02_01_E01 can move from "implementation in progress" to "supported"; next anchor should test all-position parameter decomposition.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | What this rules out |
| --- | --- | --- | --- |
| Head and fold construction | forward guard max `0`, head geometry max around `2.2e-15` | passed | unequal reference states or head-geometry artifact |
| Direct kernel identity | max relative error around `1.71e-16` | passed | autograd or kernel-measurement error |
| Parameter-group reconstruction | max relative error around `1.69e-16` | passed | missing shared-encoder parameter groups |
| Native direct velocity | 5/5 positive | passed | encoder nullspace bottleneck in this setting |
| Native full-K2 velocity | 5/5 positive | passed | H1 background reversal in this setting |
| One-step update | 20/20 sign matches | passed | immediate nonlinear-remainder failure |
| Frozen paths | embedding/head drift `0` | passed | output-head adaptation or embedding lookup |
| Local Y1 learning | full-K2 Y1 accuracy `1.0` in 5/5 | passed | local shared-token failure |

Remaining rival explanations:

- all-position background may behave differently;
- stochastic sample noise may change hitting time;
- the reference-folded intervention is not natural Transformer training;
- natural-language semantic directions may not be aligned or well separated.

## 9. Full Experiment Record

**Job id:** `pt-50l5l908`.

**Run name:** `a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`.

**Worker:** one ACP node, 4 GPUs, `n6ls.iu.i40.4`.

**Submit log:**
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514_submit_20260710_124514.log`

**Runtime log dir:**
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`

**Raw result dir:**
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_11_k2_semantic_tangent_kernel_transmission/a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`

**Curated output dir:**
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission`

**Static audit:**

```json
{
  "calibration_pass_count": 5,
  "calibration_seed_count": 5,
  "all_calibration_pass": true,
  "actual_task_count": 35,
  "expected_task_count": 35,
  "all_tasks_complete": true
}
```

## 10. Interpretation

The experiment confirms the local parameter-transmission part of the A11 theory. The important point is not the \(\alpha^2\) law itself, because that law is built into the reference intervention and proved algebraically. The important point is that the native shared-encoder Jacobian has nontrivial magnitude along \(v\), the H1 background term does not reverse the sign, and the finite SGD step follows the predicted direction.

The negative kernel cosine seed is useful: seed972 has \(\chi_\Theta=-0.003681\) and background velocity `-0.005970`, but \(\rho_{\theta,net}=0.886259>0\). This supports the current claim boundary that cosine sign alone is not a harm metric; the norm ratio and net velocity must also be read.

## 11. Claim Boundary

**Can claim:**

- controlled K=2 direct semantic supervision is locally reachable through the shared encoder parameterization in this setup;
- H1 background can be signed, but it does not reverse the direct semantic velocity in this run;
- the one-step finite update is well predicted by the tangent-kernel velocity;
- frozen embeddings and heads rule out trivial lookup and output-head co-adaptation for this test.

**Cannot claim:**

- natural-language MTP benefit;
- all-position sample efficiency;
- K larger is better;
- NTP cannot learn long-horizon information;
- long-run convergence follows only from local velocity;
- MoE routing preservation or expert utility.

## 12. Next Decision

Proceed to an all-position parameter decomposition anchor. The next minimal question should be:

```text
In LM-style all-position K=2 training, can the direct decision-prefix semantic
velocity be separated from all-position background and indirect-transfer
terms using the same tangent-kernel accounting?
```

The new anchor should not yet introduce natural-language data or broader K sweeps.

## 13. Links And Artifact Map

**Anchor:** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md`

**Protocol:** `Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/protocol.md`

**Summary:** `Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md`

**Code workspace:** `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

**Runner:** `active/synthetic_data_understanding/scripts/run_a11_11_k2_semantic_tangent_kernel_transmission.py`

**Analyzer:** `active/synthetic_data_understanding/scripts/analyze_a11_11_k2_semantic_tangent_kernel_transmission.py`

**Config:** `active/synthetic_data_understanding/configs/a11_11_k2_semantic_tangent_kernel_transmission.json`

**Submitter:** `active/synthetic_data_understanding/scripts/submit_a11_11_k2_semantic_tangent_kernel_transmission_4gpu.sh`

**Curated tables:**

```text
tables/native_transmission.csv
tables/finite_step_summary.csv
tables/early_curve_metrics.csv
tables/early_ordering.csv
tables/local_guard.csv
```

**Raw tables:**

```text
transmission_decomposition.csv
parameter_group_transmission.csv
finite_step_transmission.csv
curve_metrics.csv
fold_and_local_guard.csv
kernel_scaling.csv
coverage_audit.csv
```

**Figure:** `figures/a11_11_transmission_and_dynamics.png`

**Repro analysis command:**

```bash
python active/synthetic_data_understanding/scripts/analyze_a11_11_k2_semantic_tangent_kernel_transmission.py \
  --run-dir active/synthetic_data_understanding/results/a11_11_k2_semantic_tangent_kernel_transmission/a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514 \
  --output-dir /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission
```
