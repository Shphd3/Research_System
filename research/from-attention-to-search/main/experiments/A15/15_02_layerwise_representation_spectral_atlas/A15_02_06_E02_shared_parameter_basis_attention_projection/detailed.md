# A15_02_06_E02 Detailed Evidence Ledger

> Status: `RESULT_COMPLETE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 1. Question And Typed Outcome

**Question.** Can two parameter-only constructions define non-random cross-layer MLP input coordinates, and, in those fixed coordinates, does conditional-fine variance of the isolated Attention write move from earlier to later parameter rank with model depth?

**Typed outcome:** `basis_sensitive_shift`.

| Clause | Direct result | Verdict |
| --- | --- | --- |
| Mean-response coordinate screen | median diagonal energy / Haar 1.0777; 36/36 layers > 1 | Minimal Pass |
| Rank-consensus coordinate screen | median diagonal energy / Haar 1.0527; 36/36 layers > 1 | Minimal Pass |
| Mean-response depth contrast | +0.03171; CI [+0.02058, +0.04433]; A/B positive | Pass |
| Rank-consensus depth contrast | -0.00755; CI [-0.01869, +0.00121]; A/B negative | No positive shift |
| Cross-basis agreement | registered positive-shift decisions disagree | `basis_sensitive_shift` |

The result is complete numerically. The knowledge wording is an AI draft until the researcher confirms or corrects the interpretation and boundary.

## 2. Research Context And Scope

The broader research goal is to route by features newly produced at each depth. The current minimal experiment addresses only the coordinate obstacle:

```text
layer-specific MLP parameter spectra
-> parameter-only shared coordinate
-> isolated Attention-write projection
-> normalized layerwise variance location
```

It does not define “new information” relative to the incoming residual stream and does not test a Router. The Attention branch output is used as the requested operational proxy, not asserted as information-theoretically new.

The five meeting records from 0802, 0803, 0805, 0807, and 0810 consistently motivated: variance rather than activation magnitude; `o_proj` output before residual addition; all-layer depth curves; normalized comparison; and a common coordinate before cross-layer rank language. The 2026-08-11 researcher instruction authorized this bounded implementation and execution without another review round.

## 3. Frozen Data And Representation

| Item | Frozen value |
| --- | --- |
| Model | `/data/share/Qwen3-8B` |
| Architecture | 36 decoder blocks; hidden size 4096; MLP width 12,288 |
| Representation | direct `self_attn.o_proj` output before residual addition |
| Semantic object | conditional-fine child identity within parent |
| Semantic cube | 8 parents × 8 children × 4 templates × 2 fact bundles = 512 records |
| Expression replication | balanced A/B halves, four records per parent-child cell in each half |
| Readout | common padded absolute position 57 |
| Dataset byte SHA-256 | `c37329fad2e48d759b659483ed6705306eeb5c19f32c0e98a505901ed588ed88` |
| Model-manifest byte SHA-256 | `a27a04e41a76b84e1d2a515e726a0607bb313032d432615d37172f347ecc214b` |
| Extraction-manifest byte SHA-256 | `6b9554702020e0aef2e51e6022937015c090414fad1c945afda1374f1da68f62` |
| Source run | `a15-02-05-e01-20260809T165500Z` |

All nine files named by the model manifest and all 36 Attention-state files were rehashed before analysis. Each state file contains 512×4096 bfloat16 states, the exact record-index permutation, correct layer identity, and `site == attention_write`.

For layer \(\ell\), parent \(p\), child \(c\), and expression record \(r\):

\[
\mu_{\ell pc}=\mathbb E_r[a_{\ell pcr}],\qquad
\mu_{\ell p}=\frac{1}{8}\sum_c\mu_{\ell pc},
\]

\[
d_{\ell pc}=\mu_{\ell pc}-\mu_{\ell p},\qquad
B^{fine}_\ell=\frac{1}{64}\sum_{p,c}d_{\ell pc}d_{\ell pc}^{\top}.
\]

The population denominator is registered because every cell is balanced. The A/B guard repeats the complete estimator using four expressions per cell.

## 4. Parameter Operator And Shared Bases

The native MLP input-side operator is

\[
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}.
\]

For a unit direction \(x\), \(x^{\top}K_\ell x\) is the squared parameter response of the gate and up projections. `down_proj` is excluded because it maps MLP hidden units back to residual space rather than defining input directions.

### 4.1 Mean parameter-response basis

\[
\widetilde K_\ell=K_\ell/\operatorname{tr}(K_\ell),\qquad
\overline K=\frac{1}{36}\sum_\ell\widetilde K_\ell
=V^{MR}\Lambda^{MR}(V^{MR})^{\top}.
\]

Rank is ordered by decreasing eigenvalue of \(\overline K\). Every block has equal total trace weight, while local gain anisotropy remains. This basis asks where semantic variance lies relative to average normalized MLP response magnitude.

### 4.2 Rank-consensus basis

Each local eigensystem is divided into 16 bands of 256 ranks. For local band \(b\in\{0,\ldots,15\}\),

\[
\omega_b=1-\frac{b+1/2}{16},
\]

\[
S=\frac{1}{36}\sum_\ell\sum_b\omega_bP_{\ell b}
=V^{RC}\Lambda^{RC}(V^{RC})^{\top}.
\]

This basis asks whether a subspace is consistently assigned to early or late local rank. It ignores eigenvalue magnitude and is invariant to rotations within each fixed local 256-dimensional band.

Semantic activations do not construct, select, orient, or tune either basis.

## 5. Coordinate Validity Metric

For shared basis \(V\),

\[
\delta_{\ell,V}=
\frac{\sum_j(v_j^{\top}K_\ell v_j)^2}{\operatorname{tr}(K_\ell^2)}.
\]

The exact local eigenbasis has \(\delta=1\). The analytic Haar-random expectation is

\[
\delta^{Haar}_\ell=
\frac{2+(\operatorname{tr}K_\ell)^2/\operatorname{tr}(K_\ell^2)}{4098}.
\]

The frozen minimal screen requires a finite median ratio above one and at least 30/36 layer ratios above one.

| Basis | \(\delta\) min / median / max | Haar median | Ratio min / median / max | Layers > Haar |
| --- | --- | ---: | --- | ---: |
| Mean response | 0.3595 / 0.7225 / 0.7757 | 0.6720 | 1.0373 / 1.0777 / 1.9151 | 36/36 |
| Rank consensus | 0.1981 / 0.7180 / 0.7725 | 0.6720 | 1.0105 / 1.0527 / 1.0895 | 36/36 |

Both pass the registered screen. The pass is limited: median improvements over random orientation are only about 7.8% and 5.3%, and about 28% of local operator Frobenius energy remains off-diagonal in the median shared coordinate.

Mean-response validity is depth-asymmetric: its largest ratios occur in blocks 2--5 (1.92, 1.58, 1.40, 1.35), while most late blocks are close to 1.04--1.08. Rank-consensus validity is more uniform and peaks around middle depth. This is evidence about coordinate fit, not semantics.

## 6. Projection, Normalization, And Registered Statistic

For either fixed basis:

\[
e_{\ell j}=v_j^{\top}B^{fine}_\ell v_j
=\frac{1}{64}\sum_{p,c}(d_{\ell pc}^{\top}v_j)^2,
\]

\[
p_{\ell j}=\frac{e_{\ell j}}{\sum_k e_{\ell k}},\qquad
r_j=\frac{j-1/2}{4096},\qquad
C_{\ell,V}=\sum_jp_{\ell j}r_j.
\]

The registered depth contrast excludes block 36:

\[
T_V=\operatorname{median}_{25:35}C_{\ell,V}
-\operatorname{median}_{1:12}C_{\ell,V}.
\]

Uncertainty uses 2,000 paired parent-domain bootstrap resamples with replacement, seed 8110602. The estimator reaggregates raw parent energies and renormalizes inside every draw. Layers are not treated as independent samples.

## 7. Direct Result

| Basis | Early median | Late median | \(T\) | 95% parent-bootstrap interval | Positive draws | A / B contrast |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| Mean response | 0.44549 | 0.47721 | +0.03171 | [+0.02058, +0.04433] | 100.0% | +0.03304 / +0.03320 |
| Rank consensus | 0.48816 | 0.48061 | -0.00755 | [-0.01869, +0.00121] | 5.05% | -0.00749 / -0.00526 |

The mean-response result satisfies the registered positive-shift rule. Rank consensus does not; its point estimate and both expression halves are slightly negative, while its confidence interval narrowly includes zero.

The full layer trajectories are irregular rather than monotonic. Mean-response centroids range from 0.3755 to 0.5408 in blocks 1--35; rank-consensus centroids range from 0.3992 to 0.5606. Therefore the evidence supports only the registered early/late contrast, not a monotone progression claim.

![Centroid and coordinate audit](figures/figure4_centroid_and_coordinate_audit.png)

## 8. Why The Bases Disagree

Let \(Q=(V^{MR})^{\top}V^{RC}\). The squared entries \(Q_{ij}^2\) define how one orthogonal rank order distributes over the other.

| Alignment quantity | Result |
| --- | ---: |
| Shared-rank correlation | 0.90625 |
| Mean absolute normalized-rank displacement | 0.06648 |
| Mean same-256-band overlap | 0.46714 |
| Haar same-band expectation | 0.06250 |
| First-band overlap | 0.57908 |
| Last-band overlap | 0.92169 |

The two bases are therefore globally aligned, especially in the late tail. The semantic-location difference is concentrated at shallow depth:

| Window | Median \(C_{MR}-C_{RC}\) |
| --- | ---: |
| blocks 1--12 | -0.04217 |
| blocks 25--35 | +0.00058 |
| late minus early difference | +0.04275 |

This difference of basis readings is larger than the positive \(T_{MR}\). The gain-sensitive basis places shallow-layer fine variance substantially earlier; both bases locate late-layer variance almost identically. Combined with the mean-response basis's unusually high coordinate fit in blocks 2--5, the most conservative interpretation is that its positive shift depends on how parameter-gain anisotropy anchors the shallow end of the shared rank.

![Cross-basis alignment](figures/figure5_basis_alignment_and_reading_difference.png)

## 9. Absolute Scale Hidden By Normalization

The normalized curves answer only “where within this layer?” The unnormalized conditional-fine trace changes greatly:

| Quantity | Direct value |
| --- | ---: |
| Early-window median trace | 0.42962 |
| Late-window median trace | 260.96911 |
| Late / early median ratio | 607.45 |
| Minimum layer trace | 0.01118, block 1 |
| Maximum layer trace | 1153.89032, block 35 |
| Maximum / minimum ratio | \(1.0323\times10^5\) |

This scale increase may reflect branch scale, semantic signal, expression noise, or other depth effects. The present fine-only location experiment has no noise-normalized reliability or residual-relative “newness” estimator, so it cannot interpret the scale causally.

## 10. Execution And Guards

### 10.1 Execution surface

| Item | Value |
| --- | --- |
| Worker root | `/data/250010109/MoE_Router/experiments/20260811_a15_02_06_shared_parameter_basis_attention_projection/` |
| Full run | `runs/a15-02-06-e02-20260811-shared-basis/` |
| Device | local NVIDIA H100 80GB HBM3, `cuda:0` |
| Torch / CUDA | 2.9.0a0+50eac811a6.nv25.05 / 12.9 |
| Safetensors | 0.8.0, installed under the experiment-local `vendor/` directory |
| Full command | `PYTHONPATH=vendor:. python scripts/run_analysis.py --config configs/experiment.json` |
| Full elapsed time | 106.9 seconds, including complete model-shard hashing |

### 10.2 Test and smoke lineage

1. The first expected red test failed because `src.shared_basis` did not exist.
2. After core implementation, five primitive tests passed.
3. A second expected red test failed because bootstrap normalization functions were not yet implemented.
4. The final suite passed 6/6: trace-balanced mean operator, within-band rotation invariance, projection energy conservation, normalized centroid, analytic Haar expectation, and parent-bootstrap renormalization.
5. The real smoke constructed both bases from blocks 1/18/36 and projected layer-1 Attention states. Maximum parent energy errors were \(1.92\times10^{-7}\) and \(2.26\times10^{-7}\).

### 10.3 Full-run guards

| Guard | Maximum/result | Frozen tolerance |
| --- | ---: | ---: |
| Local operator symmetry error | 0 | \(10^{-6}\) |
| Local eigensolver residual | \(1.7341\times10^{-5}\) | \(5\times10^{-4}\) |
| Local orthogonality error | \(2.8059\times10^{-6}\) | \(5\times10^{-4}\) |
| Shared eigensolver residual | \(2.8192\times10^{-6}\) | \(5\times10^{-4}\) |
| Shared orthogonality error | \(2.7073\times10^{-6}\) | \(5\times10^{-4}\) |
| Projection-energy relative error | \(2.3297\times10^{-7}\) | \(5\times10^{-4}\) |
| Coverage | 36/36 layers; 512/512 records | exact |

### 10.4 Deviations and rendering audit

The first full-run launch was terminated after one second by the orchestration wrapper's too-short timeout before scientific computation began. The unchanged command was relaunched with an asynchronous wait and completed successfully in the same partial run directory. No data, estimator, basis, or decision rule changed.

Initial figure rendering showed colorbars overlapping right-hand panels, a statistic annotation overlapping evidence, and edge-replicated moving-average endpoints. Render revision 1 moved colorbars, moved the annotation, and used available-point centered windows at boundaries. It did not change unsmoothed arrays, statistics, or verdict. A fifth basis-alignment figure was added from frozen arrays. All five revised images were opened at original resolution and passed the visual audit.

## 11. Figure Reading Contracts

1. **Normalized log curves.** \(4096p_{\ell j}\) on a log y-axis; 129-rank arithmetic moving average for display only. Allowed: compare relative shapes within a basis. Not allowed: infer absolute variance or individual direction identity.
2. **Layer×rank heatmaps.** Unsummed direction-level \(\log_{10}(4096p_{\ell j})\) with identical robust color limits. Allowed: locate relative bands. The outer one percent clips color only.
3. **Centroid and coordinate audit.** Unsmoothed registered centroids and analytic Haar ratios. Allowed: read the early/late statistic and minimal screen. Passing Haar is not simultaneous diagonalization.
4. **Basis alignment.** Fixed 256-rank projector overlap and per-layer centroid difference. Allowed: identify where coordinate readings diverge. High band overlap does not identify individual eigenvectors.

## 12. Claim Ledger

| Claim | Verdict | Boundary |
| --- | --- | --- |
| A parameter-only non-random common coordinate can be constructed | Minimally supported for both bases | Ratios only slightly exceed Haar; not exact shared eigenvectors |
| Fine Attention-write variance shifts right with depth in mean-response rank | Supported on the frozen TAX cube | Gain-sensitive coordinate; early/late contrast only |
| The same shift holds in ordinal rank-consensus | Not supported | Slight negative point estimate; interval includes zero |
| A universal common-parameter-rank right shift exists | Not established | Registered bases disagree |
| Attention write equals information newly learned at that block | Not tested | No residual-relative novelty estimator |
| The added information is low rank | Not tested | Diagonal variance curves do not estimate effective covariance rank |
| Later rank corresponds to finer semantics | Not tested | Fine-only data; no coarse comparison |
| Shared-rank location is a valid Router signal | Not tested | No routing or utility experiment |

## 13. Artifact Map

- [Protocol](protocol.md)
- [Summary](summary.md)
- [Typed verdict](provenance/verdict.json)
- [Basis summary table](tables/basis_summary.csv)
- [Coordinate validity table](tables/coordinate_validity.csv)
- [Projection and absolute-trace table](tables/projection_diagnostics.csv)
- [Cross-basis 16-band overlap](tables/mean_response_vs_rank_consensus_band_overlap.csv)
- [Figure contracts](provenance/figure_contracts.json)
- [Source verification](provenance/source_verification.json)
- [Visual audit](provenance/visual_audit.json)
- [Worker artifact manifest](provenance/worker_artifact_manifest.json)
- Worker arrays and shared bases: `/data/250010109/MoE_Router/experiments/20260811_a15_02_06_shared_parameter_basis_attention_projection/runs/a15-02-06-e02-20260811-shared-basis/arrays/`

## 14. One Next Decision

Run one held-out-coordinate falsifier: construct both unchanged bases from blocks 13--24 only and evaluate the unchanged blocks 1--12 versus 25--35 contrast. If the gain-sensitive and ordinal readings still disagree, close the universal common-rank right-shift hypothesis and do not search additional basis families.
