# Protocol: A11_08b Output-Geometry Dynamics Audit

## 0. Approval Snapshot

Approval status: approved by user on 2026-07-09 for immediate execution.

Purpose: audit whether the A11_08 output-row geometry explanation is only a step-0 construction, or whether it remains an explanatory mechanism for early hidden semantic updates.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_08b_output_geometry_dynamics_audit_anchor.md`.

Anchor decision question: does the output-row geometry that explains A11_08's step-0 general-K hidden semantic velocity remain explanatory during early training, or is training behavior mainly caused by output-head co-adaptation?

Experiment role: mechanism audit / claim-boundary guard. This is not a broader ablation and not the next-K inclusion-law experiment.

Minimal setup: reuse A11_08 clean decision-only setting; K fixed at 4; seeds `971, 972, 973, 974, 975`; conditions `shared_only_k4`, `single_h3`, `aligned_h3_h4`, `low_conflict_h3_h4`; two output-head variants `trainable_heads` and `frozen_heads`.

Primary decision metric: frozen-head aligned-minus-low/conflict gap in hidden semantic velocity and readout margin, with shared-zero and single-positive guards.

Main falsifier: after freezing prediction heads and passing guards, if `aligned_h3_h4` no longer has stronger hidden semantic update than `low_conflict_h3_h4`, then the A11_08 dynamic mechanism must be downgraded.

Claim boundary: this protocol can only support or weaken the controlled decision-only hidden-update interpretation of A11_08. It cannot prove natural-language benefit, all-position behavior, MoE routing utility, or monotonic benefit from larger K.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| `Z` | Controlled branch identity | Branch label in synthetic data | categorical | Proxy for long-horizon semantic variable | Natural-language semantics |
| `h_T` | Decision hidden state | `h_z(t)=h_T(Z=z,t)` | vector | State whose semantic update is measured | All LM positions |
| Prediction head | Matrix that maps `h_T` to next-token logits for a horizon | horizon-specific output rows | matrix / rows | May either stay fixed or co-adapt | Semantic usefulness by itself |
| Trainable heads | A11_08 default | output rows update during training | variant | Tests natural early-training behavior | Initial geometry causality |
| Frozen heads | Output rows fixed at step 0 | only trunk / hidden-state-producing parameters train | variant | Separates hidden update from head rotation | Trainable-head behavior |
| Current geometry | Output rows at checkpoint `t` | `u(t)` | vector | Shows what the model currently asks `h_T` to align with | Step-0 explanation |
| Reference geometry | Output rows at initialization | `u(0)` | vector | Tests whether A11_08 initial geometry still explains later updates | Co-adapted heads |
| `G_K_hidden_current` | Hidden semantic velocity using current rows | `m^-1 sum_z v_z^cur(t)^T(-grad_hz L_K(t))` | scalar | Current mechanism signal | Full convergence |
| `G_K_hidden_ref` | Hidden semantic velocity using step-0 rows | `m^-1 sum_z v_z^ref^T(-grad_hz L_K(t))` | scalar | Initial-geometry mechanism signal | Current-head use |
| `M_Z_current` | Margin of hidden states against current rows | `m^-1 sum_z v_z^cur(t)^T h_z(t)` | scalar | Accumulated current semantic signal | Natural-language benefit |
| `M_Z_ref` | Margin of hidden states against step-0 rows | `m^-1 sum_z v_z^ref^T h_z(t)` | scalar | Accumulated initial-geometry signal | Current-head behavior |
| `Q_eval` | Conservative branch recovery score | `min(A_decoder,A_probe,C_swap)` | accuracy | Rules out single-readout false positives | Direct supervision proof |
| Local Y1/Y2 guard | Quality on shared near-future targets | CE loss and accuracy | loss / accuracy | Ensures semantic gain does not harm local prediction | Full LM quality |

## 2. Anchor Alignment

Prior result from A11_08:

$$
G_K^{hidden}=\frac1m\sum_z v_z^{(K)\top}\left(-\nabla_{h_z}L_K\right)
$$

followed the predicted general-K vector-sum ordering at step 0:

```text
aligned_h3_h4 > single_h3 > low_conflict_h3_h4 > shared_only_k4.
```

Unresolved issue:

```text
A11_08 controlled prediction-head output rows at initialization, but the
output heads were trainable during the training curves.
```

This protocol tests whether later evidence should be read as hidden-state semantic update or output-head co-adaptation.

## 3. Tested Hypotheses

**H1: Hidden-update geometry remains valid.** If output heads are frozen, the aligned condition still has larger early semantic velocity and readout margin than the low/conflict condition.

**H2: Trainable-head co-adaptation can rewrite the geometry.** If output heads are trainable, the low/conflict condition may rapidly increase its horizon-3 / horizon-4 cosine and reduce the initial geometry gap.

**H3: A11_08 is static-only if frozen heads remove the gap.** If the frozen-head aligned-minus-low/conflict gap disappears after guard checks pass, the A11_08 dynamic explanation must be downgraded.

## 4. Data, Conditions, And Variants

Reuse the A11_08 clean decision-only sequence construction:

```text
shared_only_k4:     Y1=A_SHARED, Y2=C_SHARED, Y3=A_SHARED, Y4=C_SHARED
single_h3:          Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=A_SHARED
aligned_h3_h4:      Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=T_z
low_conflict_h3_h4: Y1=A_SHARED, Y2=C_SHARED, Y3=S_z,      Y4=T_z
```

Variants:

```text
trainable_heads:
  A11_08 default; all prediction heads train.

frozen_heads:
  prediction-head output rows are fixed at initialization;
  trunk / hidden-state-producing parameters train.
```

Fixed settings:

```text
K = 4
seeds = 971, 972, 973, 974, 975
training scope = decision-only
broader ablation = none
```

## 5. Required Metrics

### 5.1 Output Geometry Over Time

For branch semantic rows:

$$
\bar u_3(t)=\frac1m\sum_z u_{S_z}^{(3)}(t),
\qquad
\bar u_4(t)=\frac1m\sum_z u_{T_z}^{(4)}(t).
$$

Record:

$$
\cos_{34}(t)=\frac1m\sum_z
\frac{
\left(u_{S_z}^{(3)}(t)-\bar u_3(t)\right)^\top
\left(u_{T_z}^{(4)}(t)-\bar u_4(t)\right)
}{
\left\|u_{S_z}^{(3)}(t)-\bar u_3(t)\right\|
\left\|u_{T_z}^{(4)}(t)-\bar u_4(t)\right\|+\epsilon
}.
$$

Meaning: whether the two informative horizons stay aligned, low, or conflicting during training.

### 5.2 Head Drift Norm

Record semantic-row drift:

$$
D_u(t)=
\left(
\sum_{j\in\{3,4\}}\sum_z
\left\|u_z^{(j)}(t)-u_z^{(j)}(0)\right\|^2
\right)^{1/2}.
$$

Meaning: whether output heads changed enough to rewrite the initial geometry. Under `frozen_heads`, this should be numerically zero.

### 5.3 Current And Reference Hidden Semantic Velocity

Current aggregate direction:

$$
v_z^{cur}(t)=\sum_{j\in\mathcal I_K}\lambda_j\left(u_{j,z}(t)-\bar u_j(t)\right).
$$

Reference aggregate direction:

$$
v_z^{ref}=v_z^{cur}(0).
$$

Record:

$$
G_{K,current}^{hidden}(t)=
\frac1m\sum_z v_z^{cur}(t)^\top\left(-\nabla_{h_z}L_K(t)\right),
$$

$$
G_{K,ref}^{hidden}(t)=
\frac1m\sum_z v_z^{ref\top}\left(-\nabla_{h_z}L_K(t)\right).
$$

Meaning: `current` asks what the current output heads are supervising; `ref` asks whether the original A11_08 geometry still explains the hidden update.

### 5.4 Current And Reference Readout Margins

Record:

$$
M_Z^{current}(t)=\frac1m\sum_z v_z^{cur}(t)^\top h_z(t),
$$

$$
M_Z^{ref}(t)=\frac1m\sum_z v_z^{ref\top}h_z(t).
$$

Meaning: whether semantic information accumulates in the current or initial readout direction.

### 5.5 Guarded Recovery Score

Record:

$$
Q_{eval}(t)=\min\{A_{decoder}(t),A_{probe}(t),C_{swap}(t)\}.
$$

Components:

```text
A_decoder: native model accuracy on the informative semantic target.
A_probe: frozen probe accuracy from h_T to Z.
C_swap: branch-swap consistency.
```

Meaning: conservative visible recovery of `Z`; it is a guard and secondary curve metric, not the primary mechanism proof.

### 5.6 Local Y1/Y2 Loss And Accuracy

Record cross-entropy loss and accuracy for `Y1=A_SHARED` and `Y2=C_SHARED`.

Meaning: rules out a semantic margin gain that damages local next-token learning.

## 6. Evaluation Plan

Checkpoints:

```text
step 0
then every 100 steps through the same early-training horizon used in A11_08
```

For each checkpoint and seed, record all metrics in Section 5 for every condition and both head variants.

Primary aggregation:

```text
mean over seeds
per-seed aligned-minus-low/conflict sign
early AUC over checkpoints for G_K_hidden, M_Z, and Q_eval
time-to-threshold for Q_eval if threshold is reached
```

No new K sweep, no extra noisy condition, no all-position condition, and no MoE bridge is included.

## 7. Decision Rules

### 7.1 Support For Hidden-Update Geometry

Support if all hold:

```text
1. frozen_heads: aligned_h3_h4 > low_conflict_h3_h4 in early AUC of
   G_K_hidden_ref/current and M_Z_ref/current.
2. frozen_heads: the aligned-minus-low/conflict sign is positive in at least
   4 of 5 seeds for the primary margin/velocity metrics.
3. shared_only_k4 remains near zero on semantic velocity and margin.
4. single_h3 remains positive.
5. Y1/Y2 local loss and accuracy do not materially degrade.
```

Consequence: A11_08's output geometry can be treated as a hidden-state semantic update mechanism in the controlled decision-only setting, not merely as a step-0 artifact.

### 7.2 Evidence For Output-Head Co-Adaptation

Record co-adaptation if, under `trainable_heads`:

```text
low_conflict_h3_h4 rapidly increases cos_34(t) toward the aligned condition,
or its head drift D_u(t) becomes large before hidden recovery separates.
```

Operational flag:

```text
cos_34_low/conflict(t) closes at least half of the initial gap to aligned
within the early window, or D_u(t) is large relative to the initial semantic-row
norm.
```

Consequence: trainable-head learning curves must be explained with current geometry, not only with initial geometry.

### 7.3 Failure / Downgrade

Downgrade the A11_08 dynamic claim if:

```text
1. frozen_heads remove or reverse the aligned greater than low/conflict gap
   after shared-zero and single-positive guards pass; or
2. frozen_heads make all semantic signals disappear despite valid local
   training, suggesting the A11_08 training effect relied on output-head
   co-adaptation.
```

Then A11_08 remains a valid one-step geometry construction, but not a demonstrated early-training hidden-update mechanism.

### 7.4 Insufficient Evidence

Mark insufficient, not fail, if:

```text
the frozen-head implementation is not actually frozen;
the clean A11_08 guards fail;
the low/conflict geometry is not constructed as intended;
gradient diagnostics are numerically unstable;
or local Y1/Y2 training fails in a way that blocks interpretation.
```

## 8. Expected Tables And Curves

Required summary table:

| Variant | Condition | `cos_34(0)` | `cos_34(final)` | `D_u(final)` | `AUC_G_ref` | `AUC_G_current` | `AUC_M_ref` | `AUC_M_current` | `AUC_Q` | Y1/Y2 acc |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

Required learning-curve CSV:

```text
step,seed,variant,condition,cos_34,head_drift,
G_hidden_ref,G_hidden_current,M_Z_ref,M_Z_current,
Q_eval,decoder_acc,probe_acc,swap_consistency,
Y1_loss,Y1_acc,Y2_loss,Y2_acc
```

Recommended figures:

```text
1. cos_34(t) and head drift by variant and condition.
2. G_K_hidden_ref/current(t) by variant and condition.
3. M_Z_ref/current(t) by variant and condition.
4. Q_eval(t) and Y1/Y2 local guard.
```

## 9. What This Protocol Can And Cannot Decide

Can decide:

```text
whether A11_08's geometry-controlled hidden semantic velocity remains
explanatory when output heads are frozen;
whether trainable output heads quickly rewrite low/conflict geometry;
whether training-curve evidence should be read through reference geometry or
current geometry.
```

Cannot decide:

```text
whether larger K is generally better;
whether natural-language MTP is more efficient than NTP;
whether all-position indirect transfer is explained;
whether MoE route preservation or expert utility follows.
```

## 10. Approval Decision Needed

If approved, run exactly this audit first:

```text
A11_08b clean decision-only
conditions: shared_only_k4, single_h3, aligned_h3_h4, low_conflict_h3_h4
variants: trainable_heads, frozen_heads
seeds: 971, 972, 973, 974, 975
```

After results are summarized, decide whether 11_09 can be run as a next-K inclusion-law theorem test.
