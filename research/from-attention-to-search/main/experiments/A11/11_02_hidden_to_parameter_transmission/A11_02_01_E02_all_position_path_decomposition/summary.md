# Summary: A11_02_01_E02 All-Position Semantic-Path Decomposition

Primary anchor: [11_02_01 reachability and background-sign subanchor](../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict:** supported in the controlled reference-folded K=2 all-position SGD setting.

**What we established:** K=2 MTP adds an earlier semantic parameter update at the decision state. At the same model checkpoint, the decision-position H2 loss \(h_T\rightarrow S_Z\) contributes a positive velocity \(G_D\) in 5/5 seeds and is larger than the later NTP semantic component \(G_I\) in 5/5 seeds.

**What the experiment shows:** the exact all-position velocity is not always positive because the remaining H2/background losses are signed. Full K2 has positive step-0 net velocity in 4/5 seeds; seed 973 has positive \(G_D\) but negative total velocity. Nevertheless, both direct-add/direct-mask trajectory contrasts favor the direct path in 5/5 seeds, and direct-enabled conditions finish with much stronger native H2 readout while preserving final Y1 accuracy.

**What we do next:** stop refining the controlled tangent-kernel bridge. The next anchor should operationalize a real long-document semantic task using local insufficiency, paraphrase invariance, and counterfactual dependence, then compare MTP and NTP training-token efficiency.

## Purpose

In all-position training, NTP is not deprived of the delayed semantic token. For the sequence

```text
... U03 A_SHARED S_z
```

NTP learns \(A\rightarrow S_Z\) after consuming `A_SHARED`, while K=2 MTP additionally learns \(U03\rightarrow S_Z\) one position earlier. A11_02_01_E02 asks whether this earlier loss creates a distinct native semantic update at \(h_T\), rather than treating NTP as unable to learn the branch.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| direct path | K=2 predicts \(S_Z\) from the earlier decision state | \(L_D=\ell_{T,2}\) | MTP-specific supervision path | global efficiency |
| later semantic path | NTP predicts \(S_Z\) after reading \(A\) | \(L_I=\ell_{T+1,1}\) | valid all-position NTP route | native use at \(h_T\) |
| native semantic margin | alignment of \(h_T\) with the fixed H2 rows for \(S_Z\) | \(M_Z=m^{-1}\sum_zv_z^\top h_T(z)\) | tests model-native readout geometry | downstream usefulness |
| component velocity | first-order margin movement caused by one loss partition | \(G_c=-\langle\nabla_\theta M_Z,\nabla_\theta L_c\rangle\) | separates direct and indirect paths | long-run convergence |
| remaining background | all valid all-position losses except direct, later-semantic, and local-shared terms | \(L_R=L_2^{all}-L_D-L_I-L_S\) | exposes interference from other H2 positions | one causal mechanism |

## Exact Setup

**Data:** four deterministic branches:

```text
BR_z F00 ... F15 U00 U01 U02 U03 A_SHARED S_z
```

**Model:** one-layer causal Transformer, `d_model=64`, one attention head, float64. Token embeddings and both full-vocabulary heads are frozen. Attention, MLP, LayerNorm, and position parameters are trainable.

**No-leakage mechanism control:** distinct fixed branch inputs preserve branch-sensitive shared-encoder Jacobians, but the decision states are reference-folded to be identical at step 0. H1/H2 centered \(S_Z\) rows are aligned.

**Conditions:**

| Condition | Active loss | Meaning |
|---|---|---|
| `ntp_all_h1` | all H1 losses | ordinary all-position NTP path |
| `ntp_plus_direct_h2` | all H1 plus only \(L_D\) | direct-path sufficiency |
| `mtp_all_k2` | all H1 and H2 losses | full K=2 MTP |
| `mtp_mask_direct_h2` | all H1/H2 except \(L_D\) | direct-path necessity |

**Training:** full-batch SGD, learning rate `0.003`, no weight decay, 15,000 steps. Seeds `971-975`. The remote job used one 4-GPU H100 node; each GPU ran one five-task condition shard.

**Known limitation:** the reference fold and fixed heads are controlled interventions. This is an all-position mechanism result, not natural Transformer pretraining.

## Primary Metric

The all-position loss is partitioned as:

\[
L_2^{all}=L_D+L_I+L_S+L_R.
\]

At the same model checkpoint:

\[
G_{total}=G_D+G_I+G_S+G_R,
\qquad
G_c=-\langle\nabla_\theta M_Z,\nabla_\theta L_c\rangle.
\]

This metric decides the anchor because it attributes semantic movement before comparing already-diverged training trajectories. The direct counterfactual increment is exact:

\[
G_{full}-G_{mask-D}=G_D.
\]

## Result

### Same-checkpoint path decomposition

| Component | Mean | Min | Max | Positive seeds |
|---|---:|---:|---:|---:|
| earlier direct \(G_D\) | `0.002617` | `0.001158` | `0.004692` | 5/5 |
| later semantic \(G_I\) | `0.001438` | `0.000529` | `0.002259` | 5/5 |
| local shared \(G_S\) | `-0.000094` | `-0.000329` | `0.000087` | 2/5 |
| remaining \(G_R\) | `-0.001858` | `-0.008193` | `0.002987` | 2/5 |
| all non-direct terms | `-0.000514` | `-0.006501` | `0.005240` | 3/5 |
| full K2 total | `0.002103` | `-0.001809` | `0.007669` | 4/5 |

\(G_D>G_I\) in 5/5 seeds. This is the narrowest measured sense in which the earlier MTP path is stronger than the later NTP semantic path at the common reference point.

Seed 973 is the main boundary case:

\[
G_D=0.004692>0,
\qquad
G_R=-0.008193,
\qquad
G_{total}=-0.001809.
\]

The direct path helps, but the full MTP objective can still initially move in the wrong net direction because other horizons interfere.

### Finite-step fidelity

For `mtp_all_k2` and `mtp_mask_direct_h2`, actual one-step \(\Delta M_Z\) matches \(\eta G_{total}\) in sign for all 10 seed-condition checks. The maximum relative error is `0.024920`, below the protocol threshold `0.25`.

### Early and final behavior

| Condition | Early \(M_Z\) area | Final \(M_Z\) | Final native H2 acc. | Final branch-swap | Final Y1 acc. |
|---|---:|---:|---:|---:|---:|
| NTP all H1 | `0.0000459` | `0.1088` | `0.00` | `0.667` | `1.00` |
| NTP + direct H2 | `0.0002404` | `4.0973` | `0.95` | `0.983` | `1.00` |
| MTP all K2 | `0.0001535` | `4.9522` | `1.00` | `1.000` | `1.00` |
| MTP mask direct H2 | `-0.0000383` | `0.1219` | `0.00` | `0.550` | `1.00` |

The matched early-margin ordering passes in 5/5 seeds for both `MTP > MTP-mask` and `NTP+direct > NTP`. Full MTP exceeds NTP in 4/5 seeds, which supports but does not make a seed-uniform MTP-versus-NTP claim.

### Local-learning boundary

Final Y1 accuracy is `1.00` in all four conditions. Overall all-position H1 loss is also not worse in the matched direct comparisons: `0.1006` versus `0.1181` for NTP+direct versus NTP, and `0.1350` versus `0.1627` for MTP versus MTP-mask.

However, decision-prefix Y1 cross-entropy is higher with the direct path: `0.3812` versus `0.0882` and `0.2015` versus `0.0244`. Therefore the experiment supports preserved local accuracy and overall H1 learning, not zero local confidence cost at the decision prefix.

## Key Figure

### Earlier direct path versus later all-position transfer

![A11_02_01_E02 semantic-path decomposition](figures/a11_12_semantic_path_decomposition.png)

**What this tests:** whether the earlier direct MTP path is a positive same-checkpoint increment, whether the linear velocity predicts a real update, and whether the increment accumulates into native readout without destroying local accuracy.

**How to read:** upper-left separates \(G_D\), \(G_I\), all non-direct terms, and total velocity by seed. Upper-right checks predicted versus actual one-step margin movement. Lower-left shows native semantic margin trajectories. Lower-right compares early margin area with the final Y1-accuracy guard.

**Observed result:** the direct bar is positive in every seed, but non-direct bars are signed and reverse the full total in seed 973. One-step points lie on the identity line. Direct-enabled trajectories separate sharply from their matched masks, while final Y1 accuracy stays at 1.0.

**Allowed claim:** in this controlled K=2 all-position model, MTP adds an earlier positive model-native semantic parameter update that is separable from NTP's later transfer.

**What this does not prove:** natural-language semantics, sample efficiency, trainable-head/AdamW behavior, or larger-model benefit.

## Claim Boundary

**Can claim:** the direct K=2 decision-position semantic loss gives a positive shared-encoder parameter update in 5/5 seeds; it is larger than the later NTP semantic component in 5/5; matched direct-mask contrasts improve early and final native readout; all-position background is signed and can reverse the total; local accuracy is preserved but local decision-prefix CE cost is nonzero.

**Cannot claim:** full MTP has a positive total gradient in every seed; NTP cannot learn \(Z\); MTP is uniformly faster than NTP; local learning is cost-free; natural-language MTP is better; larger K is better; MoE benefits follow.

## Next Decision

Create one downstream-grounded semantic-proxy anchor. Define a long-horizon semantic state by three operational tests:

1. the local window at the delayed decision is insufficient;
2. paraphrasing the early state without changing its meaning preserves the answer;
3. counterfactually changing the early state changes the correct delayed decision.

Only after the proxy passes these metric audits should the line compare MTP and NTP by training tokens or backbone updates needed to reach a fixed native/counterfactual/paraphrase score.
