# A15_04_E01 Shared-Tail Geometry — Detailed Evidence Record

## 1. Evidence Status

- Protocol: [protocol.md](protocol.md), frozen as `A15_04_E01_r1`, with append-only output amendment A1 and provenance-repair amendment A2.
- Execution status: one eligible full analysis completed locally on 2026-08-09.
- Registered global verdict: `LOCAL_RANDOM_OR_NONTAIL_RELOCATION`.
- Non-primary stage label: `mixed_stage_geometry`.
- Semantic scope: conditional-fine within-parent between-child covariance only.
- Claim scope: geometry only; no MLP use, task function, or Router benefit.

## 2. Frozen Inputs

| Object | Frozen value |
| --- | --- |
| model | `/data/share/Qwen3-8B`, 36 blocks, hidden size 4,096 |
| model `config.json` SHA-256 | `deaa300e5384a480c2cafd0db33cba0da89db8eeeb8ddc2b584b89bd46d52ffb` |
| semantic set | 512 records = 8 parents × 8 children × 4 templates × 2 expression bundles |
| dataset SHA-256 | `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1` |
| dataset manifest identifier | `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859` |
| representation | \(\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)\) |
| parameter operator | \(W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}\) in native MLP-input coordinates |
| fixed bands | F1=head; F2--F8=middle; F9--F16=tail; 256 directions per band |
| decision layers | blocks 1--35; block 36 descriptive only |
| early/late windows | 1--12 / 25--35 |

The worker input manifest is at `XingyuD/MoE_Routing_Experiments/active/a15_04_e01_shared_tail_geometry/runs/a15-04-e01-full-20260809T144500Z/provenance/input_manifest.json` relative to the project repository.

## 3. Provenance Repair And Eligibility

The first engineering replay used the same model and records on an H100. It failed the frozen exact-cache guard in all 36 layers: the maximum bfloat16 attention-write discrepancy began at 0.00390625--0.015625 and accumulated to 1.5 at block 36. No scientific geometry was read from that replay, and its smoke directory was removed after the source repair was recorded in Protocol amendment A2.

The eligible source instead retained the original registered 5090 semantic forward from A15_01_09. That run had exact attention-cache replay (`max_abs_error=0`) and complete-basis reconstruction error at most \(2.730589\times10^{-6}\). Raw residual-coordinate \(\Delta n\) was recovered from its complete saved FP16 eigencoordinates and the independently saved complete parameter basis. All 36 layers passed:

| Recovery guard | Maximum observed | Limit |
| --- | ---: | ---: |
| independently cached attention reconstruction relative \(L_2\) | \(2.131922\times10^{-4}\) | \(3\times10^{-4}\) |
| coordinate round-trip relative \(L_2\) | \(2.819567\times10^{-6}\) | \(10^{-4}\) |
| local rank-centroid absolute error | \(8.394595\times10^{-8}\) | \(5\times10^{-4}\) |
| conditional-fine total-trace relative error | \(2.885474\times10^{-7}\) | \(10^{-3}\) |

The full recovery manifest and recovered tensors remain in `runs/a15-04-e01-recovered-full-20260809T143600Z/` in the worker. The 32-draw coordinate-quantization sensitivity preserved the registered signs of \(T_{rank}\), \(T_T\), and \(D_T\).

## 4. Registered Estimation

1. Conditional-fine deviations average both bundles and the selected templates within each child, then subtract the equally weighted eight-child mean inside each parent.
2. Global shared spaces use odd/even layer cross-fitting among blocks 1--35. An evaluated odd layer uses only even-layer parameter projectors and vice versa.
3. Broad H/M/T consensus projectors are constructed directly; independently fitted F1--F16 projectors are never summed into the broad decision statistic.
4. Capture is divided by rank/4,096 to obtain dimension-normalized enrichment. Random expectation is 1.
5. Uncertainty uses 2,000 paired grouped bootstrap replicates over parent and template clusters. Children and expression bundles remain intact inside a selected cluster.
6. Random comparison uses 512 full Haar orthogonal partitions, shared across all evaluated layers within a draw.
7. Global tail is adjudicated before stage-resolved results are read. Stage diagnostics cover early-internal, late-internal, early-to-late, late-to-early, and early/late parameter-projector overlap for all F1--F16 and direct H/M/T spaces.

Seeds were `151100` for Haar partitions, `151102` for grouped bootstrap, and `151103` for coordinate-quantization sensitivity.

## 5. Direct Results

### 5.1 Local phenomenon gate

The median local-rank centroid increased from 0.369909 in early layers to 0.471137 in late layers, giving \(T_{rank}=0.101228\) with 95% interval [0.087289, 0.113888]. Its sealed design- and confirmation-expression changes were separately positive at 0.100967 and 0.092501. Local broad-tail enrichment increased from 0.682277 to 0.929858, giving \(T_{LT}=0.247581\) with interval [0.210290, 0.276835]. G0 and the local bridge therefore pass.

### 5.2 Global shared H/M/T decision

| Region | Early median enrichment | Late median enrichment | Change | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| head H | 1.839067 | 1.211353 | -0.627714 | [-0.752033, -0.529997] |
| middle M | 0.799710 | 1.028152 | +0.228442 | [0.193216, 0.278302] |
| tail T | 1.053568 | 0.950114 | -0.103453 | [-0.142083, -0.076752] |

The registered tail-specific contrast was \(D_T=-0.331895\) with interval [-0.412888, -0.271072]. Tail change was negative in every sealed check:

| Check | \(T_T\) | \(D_T\) |
| --- | ---: | ---: |
| odd evaluated layers | -0.133993 | -0.344148 |
| even evaluated layers | -0.095583 | -0.322818 |
| design expressions | -0.108435 | -0.347464 |
| confirmation expressions | -0.098851 | -0.323207 |

The Haar q95 values were 0.005189 for \(T_T\) and 1.002485 for late tail enrichment \(L_T\). The actual values, -0.103453 and 0.950114, fail both comparisons. Global odd/even tail consensus overlap itself was numerically strong (0.694019 versus Haar q95 0.500301), so the failure is not absence of a shared parameter-tail orientation; it is absence of late conditional-fine enrichment in that orientation.

### 5.3 Complete F1--F16 localization

Late-minus-early shared enrichment was positive for F2--F13, negative for F1 and F14--F16, and most negative at F16 (-1.755276). The registered broad tail remains F9--F16, whose directly fitted enrichment decreases. F9--F13 cannot be selected post hoc as a replacement tail.

### 5.4 Stage-resolved diagnosis after the global verdict

| Tail diagnostic | Actual enrichment/overlap | Haar q95 | Exceeds q95 |
| --- | ---: | ---: | --- |
| early-internal enrichment | 1.035302 | 1.002915 | yes |
| late-internal enrichment | 0.955330 | 1.002485 | no |
| early-built → late enrichment | 0.970624 | 1.002485 | no |
| late-built → early enrichment | 1.062454 | 1.002915 | yes |
| early/late parameter-projector overlap | 0.527685 | 0.500301 | yes |

This asymmetric pattern is `mixed_stage_geometry`. It is inconsistent with the registered pure late-formation and symmetric stage-redirection patterns. Because it was read after the global verdict, it neither rescues nor downgrades the Fail.

## 6. Verdict Logic

| Registered gate | Result |
| --- | --- |
| input, recovery, projector, and global tail-stability guards | pass |
| G0 local-rank shift | pass |
| local broad-tail bridge | pass |
| global tail change positive | fail; stably negative |
| global tail change and late level beat Haar | fail |
| tail depth change exceeds head and middle | fail; middle increases while tail decreases |
| odd/even and expression-half tail changes positive | fail; all are stably negative |

No Insufficient condition remains. The registered result is therefore the stable Fail `LOCAL_RANDOM_OR_NONTAIL_RELOCATION`.

## 7. Visualization Audit

All four central figures were opened at original resolution after the final verdict regeneration.

- [figure0_broad_tail_decision.png](figures/figure0_broad_tail_decision.png): axes, H/M/T dimensions, early/late windows, block-36 boundary, grouped intervals, Haar line, split signs, and geometry-only title are legible.
- [figure1_full_16band_spectrum.png](figures/figure1_full_16band_spectrum.png): local absolute, local normalized, shared enrichment, and F1--F16 depth changes are all visible without selecting a band.
- [figure2_stage_geometry_non_primary.png](figures/figure2_stage_geometry_non_primary.png): the stage label and the fact that it cannot modify the global verdict are explicit.
- [figure3_direction_variance_curves.png](figures/figure3_direction_variance_curves.png): ten registered layers share each panel; raw and normalized curves use log10 axes. Faint traces are unsmoothed values, while the 129-rank third-order Savitzky--Golay overlay is display-only. This smoothing reduces direction-level visual noise so the spectral shape can be inspected; every table, interval, and verdict uses unsmoothed values.

## 8. Artifact Map

Curated evidence beside this record:

- `evidence/verdict.json`, `evidence/numerical_guards.json`, `evidence/random_null_summary.json`, and `evidence/quantization_sensitivity.json`;
- `tables/local_spectrum_f1_f16.csv`, `shared_spectrum_f1_f16.csv`, `broad_hmt.csv`, `contrast_summary.csv`, `random_null_summary.csv`, `split_robustness.csv`, `global_consensus_overlap.csv`, `stage_shared_geometry.csv`, and `stage_overlap.csv`;
- the four audited figures listed above.

Complete worker output: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e01_shared_tail_geometry/runs/a15-04-e01-full-20260809T144500Z/`. It contains 173 manifested files, including all consensus bases, 2,000 bootstrap records, 512 Haar draws, the full 147,456-row direction table, and SHA-256 provenance. Raw tensors and complete random draws remain outside the curated mainline as required.

## 9. Execution And Verification

Worker: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e01_shared_tail_geometry/`.

The eligible full command used one H100 and the registered counts:

```bash
CUDA_VISIBLE_DEVICES=0 PYTHONPATH='<frozen-compatible-dependencies>:.' python full_analysis.py \
  --recovered runs/a15-04-e01-recovered-full-20260809T143600Z \
  --output runs/a15-04-e01-full-20260809T144500Z \
  --device cuda:0 --bootstrap 2000 --haar 512 --quantization-draws 32
```

The implementation suite covers semantic centering, direction/band accounting, projector construction and overlap, grouped resampling, provenance recovery, verdict precedence, global/stage separation, and sign stability. Fresh verification after the final verdict correction is recorded in the handoff response; no commit, push, root publication, or collaborator sync was performed.

## 10. Claim Boundary And One Next Decision

Established: on this frozen set, local conditional-fine variance relocates toward later layer-local ranks, but the registered global shared broad tail does not gain late-depth enrichment. The positive global change is in the direct shared middle, not the broad tail.

Not established: that middle or tail carries task function, that the MLP uses either region, that late information is nonlinear, or that any Router design would benefit.

**Exactly one next decision:** review the independent A15_03 middle-band audit in light of the positive \(T_M\) result and decide whether it is the next admissible geometry test. It must distinguish real within-middle structure from normalization and rank averaging before any functional interpretation.
