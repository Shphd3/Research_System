# Detailed Record: A06_03_02_E01 Learned-Specialist Rank-Mediated Correction

## 0. Decision Recap

**Question:** Can weighted top-1 discover a learned useful expert from initial
rank 2 or 4 as reliably and efficiently as a utility-bearing soft mixture when
expert function, representation, score ladder, load, optimizer, and router
initialization are controlled?

**Formal verdict:** Utility-coverage advantage supported; rank-mediated top-1
search rejected. Weighted top-1 corrects 0/128 cells at rank 2 and 0/128 at rank
4. Soft mixture corrects 128/128 at both ranks. The primary rank-4 capped-time
penalty is 203 updates, 95% CI \([202,205]\); normalized-regret gap is 0.7387,
95% CI \([0.7342,0.7416]\).

**Mechanism update:** A learned full-LM wrong route is not the sequential
rank-search regime observed in A06_02_03_E02. It is a selected-path blind basin on this
surface. The next causal decomposition must separate selected-only information
loss from background-position gradient override.

## 1. Definitions And Decision Metrics

For task \(f\), useful expert \(u(f)=f\) is defined by the held-out forced-expert
loss matrix after correct exposure. Sustained correction time is

\[
T_{corr}(f)=\min\left\{t:
\operatorname{Acc}_{route,u(f)}(t:t+4)\ge0.95\right\}.
\]

Uncorrected cells at horizon \(T=300\) receive

\[
\widetilde T_{corr}=301.
\]

The primary contrast is

\[
D_{corr}=\operatorname{median}_{f,seed}
\left[\widetilde T_{corr}^{top1,rank4}
-\widetilde T_{corr}^{soft,rank4}\right].
\]

For fixed useful-expert floor \(L_{f,u}^{cf}\),

\[
E_f(t)=L_f^{native}(t)-L_{f,u}^{cf},
\]

\[
NR_f=\frac1{301}\sum_{t=0}^{300}
\frac{[E_f(t)]_+}{\max([E_f(0)]_+,10^{-12})}.
\]

This is a training-efficiency metric on held-out task positions, not a system
throughput metric.

## 2. Data And Model

The controlled language task has four sequence-level transformations. For
instruction \(f\) and content value \(c\), the output is

\[
y=(c+f)\bmod4.
\]

Each length-33 sequence is

```text
[instruction, content_1, output_1, ..., content_16, output_16]
```

All 32 autoregressive targets enter optimization. Each seed has 32 train and 32
disjoint held-out sequences.

The model has hidden dimension 64, four attention heads, one causal-attention
layer, fixed instruction-state visibility control, residual plus LayerNorm,
four MLP experts of width 128, fixed readout, and no learned positional
embedding.

## 3. Exposure And Rank Intervention

Specialists are rebuilt with 200 expert-only AdamW updates in which task \(f\) is
always forced to expert \(f\). Balanced generalists receive equal updates from
every task. Representation and router remain unchanged during exposure.

For task centers \(C\in\mathbb R^{4\times d}\), every rank condition uses the
same target score multiset

\[
[0.75,0.25,-0.25,-0.75].
\]

Only expert identities are permuted. The useful expert occupies requested rank
1, 2, or 4; the remaining experts use cyclic order. The selected wrong expert
is therefore the same for rank 2 and rank 4, and each expert is initial top-1
for one task. Router rows solve

\[
W^\top=C^+S
\]

in float64 before conversion to model dtype.

## 4. Forward And Optimization Intervention

Weighted top-1:

\[
y=h+p_rE_r(h),\qquad r=\arg\max_j s_j.
\]

Soft mixture:

\[
y=h+\sum_jp_jE_j(h).
\]

Experts and representation are frozen. Both conditions use the exact same
router tensor, full-sequence loss, full-batch router-only SGD, learning rate
0.001, no momentum, no weight decay, and 300 updates. The only intervention is
which expert outputs enter \(y\) and therefore the loss.

The code materializes all expert tensors for convenience even in top-1. The
causal distinction is functional forward participation, not measured kernel
FLOPs.

## 5. Protocol Compliance

| Guard | Formal result | Status |
| --- | ---: | --- |
| Completed seeds | 32 | pass |
| Cells per condition | 128 | pass |
| Specialist median utility gap | 8.8947 | pass, threshold 5 |
| Generalist median utility gap | -0.0042 | pass, absolute threshold 0.5 |
| Minimum useful-rank accuracy | 1.0000 | pass |
| Minimum p05 adjacent score gap | 0.4724 | pass, threshold 0.40 |
| Maximum initial load spread | 0 | pass |
| Maximum train center-score error | \(1.97\times10^{-4}\) | pass |
| Top-1/soft initial state error | 0 | pass |
| Non-router state error | 0 | pass |
| Rank-1 top-1/soft correction rate | 1.000/1.000 | pass |
| Soft rank-4 positive control | 1.000 | pass |
| Finite trajectories | complete | pass |

All registered validity guards pass.

## 6. Primary Results

### 6.1 Condition Summary

| Expert state / rule / rank | Corrected | Median capped time | Median boundaries | Final useful probability | Final task loss | Median \(NR\) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| specialist top-1 rank 1 | 128/128 | 0 | 0 | 0.6782 | 0.0244 | 0.2239 |
| specialist top-1 rank 2 | 0/128 | 301 | 0 | 0.2188 | 6.3844 | 1.0133 |
| specialist top-1 rank 4 | 0/128 | 301 | 0 | 0.0877 | 6.3817 | 1.0132 |
| specialist soft rank 1 | 128/128 | 0 | 0 | 0.6397 | 0.0648 | 0.3299 |
| specialist soft rank 2 | 128/128 | 29 | 1 | 0.6216 | 0.0755 | 0.1552 |
| specialist soft rank 4 | 128/128 | 98 | 1 | 0.5748 | 0.1178 | 0.2750 |
| generalist top-1 rank 4 | 0/128 arbitrary target | 301 | 0 | 0.0638 | 0.2478 | 0.3526 |
| generalist soft rank 4 | 0/128 arbitrary target | 301 | 0 | 0.1016 | 0.0810 | 0.0000 |

The generalist target is intentionally arbitrary because experts are
interchangeable. Its zero correction rate shows that soft routing does not
recover an identity merely because the score construction names it useful.

### 6.2 Registered Contrasts

| Contrast | Median | 95% CI | Verdict |
| --- | ---: | ---: | --- |
| top-1 rank4 minus rank2 capped time | 0 | \([0,0]\) | no rank penalty because both fail |
| top-1 rank4 minus rank2 normalized regret | \(-1.31\times10^{-5}\) | \([-5.91,4.49]\times10^{-5}\) | unresolved / effectively identical |
| rank4 top-1 minus soft capped time | 203 | \([202,205]\) | decisive soft advantage |
| rank4 top-1 minus soft normalized regret | 0.7387 | \([0.7342,0.7416]\) | decisive soft advantage |

H1 rank-mediated top-1 correction is rejected. H2 forward utility-coverage
advantage is supported. H3 no material sparse bottleneck is rejected.

## 7. Trajectory Evidence

Median trajectory checkpoints:

| Condition | Step | Task loss | Normalized excess | Useful probability | Useful rank | Boundaries |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| top-1 rank 2 | 0 | 6.2345 | 1.000 | 0.2760 | 2 | 0 |
| top-1 rank 2 | 300 | 6.3844 | 1.024 | 0.2188 | 2 | 0 |
| top-1 rank 4 | 0 | 6.2344 | 1.000 | 0.1017 | 4 | 0 |
| top-1 rank 4 | 300 | 6.3817 | 1.024 | 0.0877 | 4 | 0 |
| soft rank 2 | 0 | 2.1045 | 1.000 | 0.2760 | 2 | 0 |
| soft rank 2 | 300 | 0.0755 | 0.035 | 0.6216 | 1 | 1 |
| soft rank 4 | 0 | 4.4886 | 1.000 | 0.1017 | 4 | 0 |
| soft rank 4 | 300 | 0.1178 | 0.025 | 0.5748 | 1 | 1 |

Wrong-rank top-1 receives nonzero updates: median router update norms are
\(4.24\times10^{-4}\) at rank 2 and \(4.26\times10^{-4}\) at rank 4. The failure is
therefore not zero optimization. Updates move within a route region that lowers
the useful expert probability and preserves the wrong majority identity.

Soft update norms are larger, especially at rank 4, because all expert outputs
contribute utility-bearing gradients. Update magnitude alone does not explain
functional specificity: the generalist soft guard does not recover the
arbitrary identity.

## 8. Visualization Results

### Figure 1: Correction Curves

![Correction curves](figures/useful_expert_correction_curves.png)

- **Plot contract:** one cell is a seed-task pair; Y-axis is fraction not yet
  sustainably corrected; every update is observed.
- **Observed:** soft rank 2 corrects around updates 20--45 and soft rank 4 around
  80--125. Both wrong-rank top-1 curves stay at 1.
- **Allowed conclusion:** correction coverage and latency ordering.
- **Limitation:** full-LM source gradients are not decomposed.

### Figure 2: Normalized Regret

![Normalized regret](figures/normalized_regret_trajectory.png)

- **Plot contract:** held-out task-position excess above each cell's fixed
  useful-expert floor, normalized by its step-0 excess.
- **Observed:** soft rank 4 approaches zero; top-1 rank 2 and 4 overlap slightly
  above one.
- **Allowed conclusion:** soft correction improves functional learning
  efficiency.
- **Limitation:** not compute-normalized.

### Figure 3: Rank-4 Search

![Rank-4 search](figures/rank4_identity_search.png)

- **Observed:** soft useful rank moves through intermediate ranks and crosses
  one majority boundary; top-1 remains rank 4 with zero boundaries.
- **Allowed conclusion:** utility coverage changes the identity-search field.
- **Limitation:** it does not prove that all four experts must always be active.

## 9. Reconciliation With A06_02_03_E02

A06_02_03_E02 used frozen orthogonal feature vectors and fixed class-specialized expert
outputs. Weighted top-1 eventually corrected rank 4 in 153 steps through 142
boundary changes. A06_03_02_E01 uses learned experts, residual output, context-defined
sequence tasks, and full-position LM loss. It has zero boundary changes at
rank 2 and rank 4.

The two results do not conflict. The weighted-top-1 identity

\[
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf1[j=r]-p_j)B_rh
\]

only specifies how the selected-path benefit \(B_r\) moves rows. It does not fix
the sign of \(B_r\) across models, positions, or learned expert functions. A06_02_03_E02
and A06_03_02_E01 occupy different gradient fields. Therefore “top-1 always performs
rank search” is rejected as a general statement.

## 10. Updated Theory

The specialization dynamics now require three separate router contracts:

1. **Utility formation:** stable conditional exposure creates different expert
   functions. A06_03_01_E01 supports this.
2. **Correct-route exploitation:** once the useful expert is selected,
   weighted top-1 preserves and improves it. A06_03_01_E02/A06_03_02_E01 rank 1 support this.
3. **Wrong-route exploration:** when the useful expert is unselected, its own
   function must affect router credit. A06_03_02_E01 shows selected-only top-1 does not
   provide sufficient correction on the current full-LM surface.

The minimum future gate therefore cannot be only a better geometric
initializer. It needs a sparse exploitation path plus a bounded mechanism for
utility-bearing exploration or semantic credit. A06_03_02_E01 does not yet decide
which one because full-LM loss mixes task-dependent and background positions.

## 11. Claim Boundary

**Established:** valid rank geometry, functional learned target, complete
top-1 noncorrection at ranks 2/4, complete soft correction, large correction
time and regret advantages, and target specificity against generalists.

**Not established:** whether task-position-only top-1 can correct; whether
background gradients create the basin; whether sampled two-expert feedback is
enough; natural-language semantic routing; system-level sparse efficiency.

## 12. Next Decision

From the same specialist wrong-rank state, decompose the router gradient into
task-position and background-position sources and run matched causal branches:

- full-LM top-1;
- task-position-only top-1;
- background-position-only top-1;
- task-position soft positive control.

Measure useful-versus-selected boundary pressure and sustained correction. If
task-only top-1 remains trapped, the method target is candidate utility
coverage. If task-only top-1 corrects but full-LM top-1 remains trapped, the
method target is semantic-credit weighting; MTP can then be tested as a
label-free long-horizon credit source rather than inserted speculatively.

## 13. Run Ledger And Artifact Map

| Item | Value |
| --- | --- |
| Formal run | `a06_40_full_4gpu_20260710_01` |
| ACP job | `pt-djlu6j09` (`SUCCEEDED`) |
| GPUs | four H100 80GB |
| Seeds | 0--31 |
| Config | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_40_learned_specialist_rank_correction.json` |
| Runner | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_40_learned_specialist_rank_correction.py` |
| Submitter | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_40_learned_specialist_rank_correction_4gpu_acp.sh` |
| Raw result | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_40_learned_specialist_rank_correction/a06_40_full_4gpu_20260710_01/` |
| Curated tables | `tables/` |
| Curated figures | `figures/` |

Local smoke run 01 was excluded because the initial score guard incorrectly
compared held-out center values to the train target matrix. The construction
was valid: rank accuracy was 1 and p05 score gap was positive. The guard was
corrected before the formal run to apply target-matrix error only on train
construction centers and use direct rank/gap checks on held-out centers. Smoke
run 02 passed. A one-seed 300-step run passed every guard except the
intentionally unmet 32-seed coverage requirement.

