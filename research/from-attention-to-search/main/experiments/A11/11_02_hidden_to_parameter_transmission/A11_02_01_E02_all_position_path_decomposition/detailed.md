# Detailed: A11_02_01_E02 All-Position Semantic-Path Decomposition

Primary anchor: [11_02_01 reachability and background-sign subanchor](../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** isolate what K=2 MTP adds beyond the delayed semantic loss already available to NTP under all-position training.

**Hypothesis:** the decision-position H2 loss contributes a positive earlier semantic velocity \(G_D\) at \(h_T\), while later semantic and shared/background paths are signed.

**Experiment logic:** compute all loss-component gradients on the same checkpoint, then use direct-add/direct-mask training contrasts only to test whether the local increment accumulates.

**Conclusion:** supported in the controlled reference-folded all-position SGD model. Direct velocity is positive and exceeds the later semantic component in 5/5 seeds. Full total velocity is positive in only 4/5 because remaining H2 losses can dominate. Direct-enabled conditions nevertheless win both matched early-margin contrasts in 5/5 seeds and finish with native H2 accuracy `0.95/1.00`, versus `0.00/0.00` for their non-direct baselines.

**Evidence:** valid remote 4-GPU run `pt-nbdlvz2e`; 20/20 tasks; 5/5 calibration; 10/10 one-step checks; 5/5 local accuracy guards.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Decision role | Cannot prove |
|---|---|---|---|---|---|
| \(L_D\) | earlier MTP semantic loss | H2 at decision position \(T\) predicting \(S_Z\) | CE contribution | MTP-specific path | global efficiency |
| \(L_I\) | later NTP semantic loss | H1 at position \(T+1\) predicting \(S_Z\) | CE contribution | valid indirect path | native use at \(h_T\) |
| \(L_S\) | local shared loss | H1 at \(T\) predicting \(A\) | CE contribution | local guard | semantics |
| \(L_R\) | remaining all-position losses | residual after \(D/I/S\) | CE contribution | background/interference | one mechanism |
| \(M_Z\) | model-native semantic alignment at \(h_T\) | centered H2 \(S_Z\) rows dotted with branch states | scalar | target quantity | downstream value |
| \(G_c\) | parameter velocity from loss component \(c\) | \(-\langle\nabla_\theta M_Z,\nabla_\theta L_c\rangle\) | margin per unit SGD learning rate | primary attribution | long-run convergence |
| early margin area | normalized area under \(M_Z(t)\) through step 50 | trapezoidal area divided by window length | margin | trajectory guard | sample efficiency |
| branch swap | correct branch row outranks another branch row under counterfactual branch comparisons | pairwise consistency | fraction | native-use guard | natural semantics |

## 2. Anchor Link And Decision Point

A11_10 already showed that probe-readable recovery and model-native readout can separate under all-position training. A11_11 then showed that K=2 direct semantic supervision can enter shared encoder parameters in a decision-only reference-folded model.

A11_02_01_E02 closes the remaining controlled bridge:

```text
same delayed token S_Z
-> NTP receives it later at h_{T+1}
-> MTP additionally receives it earlier at h_T
-> separate their parameter contributions to native h_T margin.
```

The experiment is useful only if it changes the claim from “NTP has no signal” to the grounded statement “MTP adds an earlier signal, while NTP still has a later shared-parameter route.”

## 3. Protocol Compliance Audit

| Protocol item | Actual run | Status |
|---|---|---|
| four mechanism-critical conditions | all present | pass |
| seeds 971-975 | all present | pass |
| remote four-GPU execution | one `n6ls.iu.i40.4` H100 node | pass |
| task coverage | 20/20 tasks | pass |
| checkpoints | 15/15 per task | pass |
| CUDA smoke | four conditions, seed 971, two steps | pass |
| reference-fold guard | 5/5 seeds | pass |
| aligned fixed-head guard | 5/5 seeds | pass |
| loss/velocity reconstruction | all checkpoints | pass |
| frozen embeddings/heads | zero update/drift | pass |
| central figure and decision tables | present | pass |

No condition, K value, or claim boundary was changed after observing the full result. The training window was extended from the initial 200-step smoke to 15,000 steps before the remote run because a single all-position position contributes about one sequence-length fraction of the averaged loss. The 200-step smoke already passed the mechanism ordering but had not completed local Y1 learning.

## 4. Setup

### 4.1 Data construction

For \(z\in\{1,2,3,4\}\):

\[
X_z=(\operatorname{BR}_z,F_{00},\ldots,F_{15},U_{00},\ldots,U_{03},A,S_z).
\]

The final `U03` position is \(T\). The first target is shared, and the second target one-to-one encodes the early branch:

\[
Y_{T+1}=A,
\qquad
Y_{T+2}=S_Z.
\]

There is no stochastic filler or probe split in A11_02_01_E02. The scientific object is parameter-path attribution, not generalization across nuisance examples.

### 4.2 Model and controlled geometry

- one-layer causal Transformer;
- `d_model=64`, one attention head, dropout zero;
- float64 parameters and activations;
- fixed distinct branch-token embeddings;
- all embeddings frozen;
- two fixed full-vocabulary linear softmax heads;
- centered \(S_Z\) rows aligned exactly across H1 and H2;
- attention, MLP, LayerNorm, and position parameters trainable.

Raw decision states differ by branch because the fixed branch inputs differ. The reference fold is:

\[
h_T(z;\theta)
=\bar h_{T,0}
+h_T^{raw}(z;\theta)
-h_{T,0}^{raw}(z).
\]

At the reference checkpoint all folded \(h_T\) values are identical, but their shared-encoder Jacobians retain branch sensitivity. Other positions are not folded. This lets the later \(A\rightarrow S_Z\) loss act through a genuine cross-position shared-parameter path.

### 4.3 Loss partition

The full K=2 objective is partitioned into disjoint normalized terms:

\[
L_D=\ell_{T,2}(S_Z),
\]

\[
L_I=\ell_{T+1,1}(S_Z),
\]

\[
L_S=\ell_{T,1}(A),
\]

\[
L_R=L_2^{all}-L_D-L_I-L_S.
\]

`L_R` includes all remaining H1 and H2 terms. The runner also records its H1 and H2 pieces separately.

### 4.4 Conditions

| Condition | H1 | ordinary H2 | direct H2 at \(T\) | Interpretation |
|---|---:|---:|---:|---|
| `ntp_all_h1` | all | no | no | NTP baseline with later semantic path |
| `ntp_plus_direct_h2` | all | no | yes | add only the earlier semantic path |
| `mtp_all_k2` | all | all | yes | full K=2 MTP |
| `mtp_mask_direct_h2` | all | all | no | full K2 background without earlier path |

### 4.5 Optimization

- full-batch SGD;
- learning rate `0.003`;
- no weight decay;
- 15,000 updates;
- checkpoints `0,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,15000`;
- virtual one-step sizes `0.0015` and `0.003`.

## 5. Metrics And Decision Rules

### 5.1 Native semantic margin

Let \(v_z=u_{2,S_z}-\bar u_2\). Then:

\[
M_Z(\theta)=\frac1m\sum_zv_z^\top h_T(z;\theta).
\]

It measures whether the decision state moves into the geometry used by the model's own H2 head.

### 5.2 Same-checkpoint component velocity

For \(c\in\{D,I,S,R\}\):

\[
G_c=-\langle\nabla_\theta M_Z,\nabla_\theta L_c\rangle.
\]

Linearity gives:

\[
G_{total}=G_D+G_I+G_S+G_R.
\]

This is the primary metric. It avoids attributing differences between already-diverged checkpoints to one loss component.

### 5.3 Finite-step fidelity

For an SGD step:

\[
\Delta M_Z
=M_Z(\theta-\eta\nabla L)-M_Z(\theta)
\approx\eta G_{total}.
\]

Pass requires the same sign and relative error at most `0.25`.

### 5.4 Trajectory and local guards

- normalized \(M_Z\) area through step 50;
- final native H2 accuracy and target probability;
- branch-swap consistency;
- final decision-prefix Y1 accuracy and CE;
- final all-position H1 accuracy and CE.

The local guard is asymmetric: an accuracy failure invalidates the semantic gain, while a CE increase with preserved accuracy is reported as a cost rather than hidden.

## 6. Main Results

### 6.1 Decision evidence: step-0 path decomposition

| Seed | \(G_D\) | \(G_I\) | all non-direct | full total | Net sign |
|---:|---:|---:|---:|---:|---|
| 971 | `0.002395` | `0.000529` | `0.000476` | `0.002872` | positive |
| 972 | `0.002430` | `0.002259` | `0.005240` | `0.007669` | positive |
| 973 | `0.004692` | `0.001606` | `-0.006501` | `-0.001809` | negative |
| 974 | `0.001158` | `0.000730` | `0.000010` | `0.001167` | positive |
| 975 | `0.002409` | `0.002065` | `-0.001793` | `0.000616` | positive |

Aggregate table:

| Component | Mean | Standard deviation | Range | Positive seeds |
|---|---:|---:|---:|---:|
| \(G_D\) | `0.002617` | `0.001281` | `[0.001158, 0.004692]` | 5/5 |
| \(G_I\) | `0.001438` | `0.000778` | `[0.000529, 0.002259]` | 5/5 |
| \(G_S\) | `-0.000094` | `0.000200` | `[-0.000329, 0.000087]` | 2/5 |
| \(G_R\) | `-0.001858` | `0.004250` | `[-0.008193, 0.002987]` | 2/5 |
| all non-direct | `-0.000514` | `0.004238` | `[-0.006501, 0.005240]` | 3/5 |
| total | `0.002103` | `0.003534` | `[-0.001809, 0.007669]` | 4/5 |

Two distinctions are supported:

1. the earlier direct component is positive in every seed and exceeds the later semantic component in every seed;
2. this does not force the full MTP total to be positive because the remaining all-position objective is signed.

### 6.2 Seed 973 failure decomposition

Seed 973 is not an implementation failure. All calibration, fold, head, decomposition, frozen-path, and finite-step checks pass. Its components are:

\[
G_D=0.004692,
\quad
G_I=0.001606,
\quad
G_S=0.000087,
\quad
G_R=-0.008193.
\]

Therefore:

\[
G_{total}=-0.001809.
\]

The direct semantic path remains helpful, but other H2 positions initially overwhelm it. This falsifies the stronger idea that a positive direct term guarantees a positive full-MTP update in every seed.

### 6.3 Finite-step evidence

All 10 main checks at learning rate `0.003` match the predicted sign. Relative errors are:

- full K2: `0.000152-0.000573`;
- direct-masked K2: `0.000153-0.024920`.

Even the negative seed 973 follows the negative predicted step. The local decomposition is therefore an accurate immediate update model at the tested learning rate.

### 6.4 Change evidence: early trajectories

Matched direct contrasts:

- `mtp_all_k2 > mtp_mask_direct_h2` on early margin area in 5/5 seeds;
- `ntp_plus_direct_h2 > ntp_all_h1` in 5/5 seeds.

Full MTP exceeds NTP in 4/5 seeds. The remaining seed, 975, has nearly equal early areas (`0.0000475` versus `0.0000512`). Therefore the matched causal contrasts are stronger evidence than the raw MTP/NTP curve comparison.

### 6.5 Summary evidence: final native readout

| Condition | Final \(M_Z\) mean | Native H2 acc. | Branch swap |
|---|---:|---:|---:|
| NTP | `0.1088` | `0.00` | `0.667` |
| NTP + direct | `4.0973` | `0.95` | `0.983` |
| full MTP | `4.9522` | `1.00` | `1.000` |
| MTP mask direct | `0.1219` | `0.00` | `0.550` |

Later NTP loss can move \(h_T\) slightly through parameter sharing, but in this controlled geometry it does not train the native H2 classifier. Adding the earlier path or retaining it inside MTP produces strong model-native use.

### 6.6 Local-learning evidence

Final decision-prefix Y1 accuracy is 1.0 in all 20 seed-condition runs. Final all-position H1 accuracy means are `0.9932, 1.0000, 1.0000, 0.9886` in condition order.

Losses show a more nuanced picture:

| Condition | Decision Y1 CE | All-position H1 CE |
|---|---:|---:|
| NTP | `0.0882` | `0.1181` |
| NTP + direct | `0.3812` | `0.1006` |
| full MTP | `0.2015` | `0.1350` |
| MTP mask direct | `0.0244` | `0.1627` |

The direct path preserves accuracy and does not worsen overall H1 CE in either matched comparison, but it reduces confidence on the particular decision-prefix Y1 target. The safe statement is preserved local accuracy with a measurable location-specific CE tradeoff.

## 7. Visualization Results

### Earlier direct path versus later all-position transfer

![A11_02_01_E02 semantic-path decomposition](figures/a11_12_semantic_path_decomposition.png)

**Purpose:** combine same-checkpoint attribution, immediate finite-step validation, long-run native margin, and local-learning guard.

**Setup:** five seeds, four conditions, 15,000 full-batch SGD steps; all central quantities come from the valid remote run.

**Metric definition:** upper-left shows \(G_c=-\langle\nabla M_Z,\nabla L_c\rangle\) at step 0. Upper-right shows predicted \(\eta G_{total}\) versus actual \(\Delta M_Z\). Lower-left shows mean \(M_Z(t)\). Lower-right shows normalized early \(M_Z\) area and final decision Y1 accuracy.

**How to read:** a positive direct bar is the MTP-specific increment. A negative full-total bar with a positive direct bar means background interference, not a failed direct path. Identity-line points validate the finite-step interpretation. Separation between direct and matched-mask curves tests accumulation.

**Observed result:** \(G_D\) is positive in all seeds; seed 973 has negative full total; all finite-step points align closely with identity; direct-enabled curves separate sharply; all final Y1 accuracies equal 1.0.

**Take-home:** all-position MTP supplies an earlier native semantic path, while the full objective remains a signed composition of that path and other losses.

**Remaining uncertainty:** trainable heads, embeddings, AdamW, stochastic batches, natural-language semantic states, and sample/token efficiency.

**What this figure does not prove:** universal MTP superiority or cost-free local learning.

**Anchor update implication:** mark 11_12 supported, close the controlled parameter-path bridge, and move to the downstream semantic-proxy anchor.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason / implication | What this rules out |
|---|---|---|---|---|
| head/fold construction | 5/5 calibration | passed | none | initial \(h_T\) leakage and output-row mismatch |
| loss partition | numerical-zero reconstruction | passed | none | omitted all-position terms |
| direct reachability | \(G_D>0\) in 5/5 | passed | none | shared-encoder nullspace bottleneck |
| direct versus later path | \(G_D>G_I\) in 5/5 | passed | none | identical early/later velocity |
| full net sign | positive 4/5 | partial | seed 973 remaining H2 interference | universal positive-total claim |
| one-step fidelity | 10/10 | passed | none | immediate nonlinear failure |
| early matched ordering | 10/10 pair-seed checks | passed | none | direct term failing to accumulate early |
| native final readout | direct `0.95/1.0`, masks `0/0` | passed | none | probe-only explanation |
| final Y1 accuracy | 1.0 all conditions | passed | none | local accuracy sacrifice |
| decision Y1 CE | higher with direct path | cost observed | location-specific confidence tradeoff | cost-free local-learning claim |

**Falsified physical prior:** none of P1-P3 in their stated bounded form.
**Falsified stronger conjecture:** positive \(G_D\) does not guarantee positive full K2 total in every seed.
**Falsified operationalization:** none; all validity guards pass.
**Falsified implementation:** none.
**Falsified metric:** none; the component metric predicts actual one-step motion.
**Remaining rival explanations:** natural trainable heads/embeddings may change the split; AdamW preconditioning may reroute component effects; the synthetic branch variable may not match real semantic invariance.

## 9. Full Experiment Record

**Job:** `pt-nbdlvz2e` (`SUCCEEDED`).
**Run:** `a11_12_all_position_semantic_path_decomposition_4gpu_20260710_164700`.
**Worker:** one `n6ls.iu.i40.4` node, four H100 80GB GPUs.
**Shards:** four; five tasks each.
**Task count:** 20/20.
**Per-task checkpoints:** 15/15.
**Path rows:** 300.
**Finite-step rows:** 600.
**Parameter-group rows:** 1,200.
**Validity:** all implementation and coverage guards true.

Raw result directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_12_all_position_semantic_path_decomposition/a11_12_all_position_semantic_path_decomposition_4gpu_20260710_164700
```

Log directory:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_12_all_position_semantic_path_decomposition_4gpu_20260710_164700
```

## 10. Interpretation

The experiment changes the most useful answer to “what does MTP do better than NTP?”

The answer is not that NTP never sees delayed semantics. In all-position training, NTP sees \(S_Z\) at \(h_{T+1}\). MTP's controlled advantage is that the same semantic token supervises \(h_T\) before the shared intervening token is consumed. This produces a positive earlier component \(G_D\) in every seed and stronger native readout in both direct-add/direct-mask comparisons.

The full MTP objective is still not monotone-good. It adds all H2 losses, not only \(L_D\). Those remaining losses are the dominant source of sign variation. Therefore the right theoretical object is:

\[
\text{earlier semantic advantage}
=G_D,
\]

not:

\[
G_{MTP,total}>G_{NTP,total}
\quad\text{for every seed and step}.
\]

This is a stronger grounded understanding than “MTP predicts more tokens”: MTP shortens the supervision path for a future variable, but realized benefit depends on whether the rest of the objective preserves or interferes with that direction.

## 11. Claim Boundary

**Can claim:** controlled K=2 all-position MTP adds an earlier positive native semantic parameter update; the direct increment exceeds the later NTP semantic component at the reference point in 5/5 seeds; matched direct contrasts improve native margin; background can reverse the full total; final local accuracy is preserved with a location-specific CE cost.

**Cannot claim:** NTP cannot learn the variable; full MTP is better in every seed; local learning is cost-free; local velocity proves sample efficiency; the result transfers automatically to natural text, AdamW, trainable heads, LLM scale, or MoE.

## 12. Next Decision

The controlled parameter-path bridge is now sufficient. The next anchor should audit the task and metric, not another gradient decomposition.

Candidate downstream target: long-document delayed state decisions in which an early passage establishes a state such as a rule, commitment, object status, agent belief, or causal condition; a later local window is insufficient; paraphrasing the early passage preserves the correct decision; and changing the state changes the answer.

The first real-task anchor should decide whether a constructed or existing dataset satisfies these semantic criteria before training MTP and NTP. Only then should a training experiment use a fixed backbone/data budget and compare the number of training tokens or updates needed to reach a joint native, counterfactual, and paraphrase score.

## 13. Links And Artifact Map

**Anchor:** `main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md`
**Protocol:** `main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/protocol.md`
**Summary:** `main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md`
**Code workspace:** `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
**Runner:** `active/synthetic_data_understanding/scripts/run_a11_12_all_position_semantic_path_decomposition.py`
**Analyzer:** `active/synthetic_data_understanding/scripts/analyze_a11_12_all_position_semantic_path_decomposition.py`
**Config:** `active/synthetic_data_understanding/configs/a11_12_all_position_semantic_path_decomposition.json`
**Submitter:** `active/synthetic_data_understanding/scripts/submit_a11_12_all_position_semantic_path_decomposition_4gpu.sh`
**Result dir:** raw result directory above
**Figure dir:** `main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/figures`
**Key tables:** `step0_path_summary.csv`, `step0_path_aggregate.csv`, `finite_step_summary.csv`, `early_trajectory_summary.csv`, `condition_summary.csv`
**Logs:** log directory above
**Job id:** `pt-nbdlvz2e`

Reproduce the curated analysis:

```bash
python active/synthetic_data_understanding/scripts/analyze_a11_12_all_position_semantic_path_decomposition.py \
  --run-dir active/synthetic_data_understanding/results/a11_12_all_position_semantic_path_decomposition/a11_12_all_position_semantic_path_decomposition_4gpu_20260710_164700 \
  --output-dir ../../main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition
```
