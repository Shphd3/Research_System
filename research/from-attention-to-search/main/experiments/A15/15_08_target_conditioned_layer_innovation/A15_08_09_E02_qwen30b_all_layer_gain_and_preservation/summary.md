# Summary: A15_08_09_E02 Qwen3-30B-A3B All-Layer Gain And Preservation

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED`

## Result Snapshot

The all-layer rerun changes the interpretation but not the preservation verdict. On Qwen3-30B-A3B, \(R_U\) has reproducible incremental parent-label information beyond same-layer \(X\): 31 of 48 blocks have a familywise simultaneous 95% lower bound above zero. Block 39 has the largest controlled added utility, 0.10994 nats/example with simultaneous 95% interval [0.09872, 0.12080]. H0 therefore `Pass`.

This incremental information is not organized as a stable standalone routing geometry. The frozen downstream primary is block 48, selected among H0-admitted layers for the best DEV standalone low-tail margin; block 38 is the separated replication. Block 48 is H2 `Fail` and H3 `Fail`; block 38 is H2 `Pass` but H3 `Fail`. Every TEST low-tail margin interval is entirely negative. H4 is consequently `SKIPPED_H3_NOT_PASS` under the frozen dependency.

The precise update is therefore: **the update residual is not information-free, but it is not a robust standalone linear Router space.** Layer transfer from Qwen3-8B was a real protocol error, yet correcting it does not establish the premise required by the random-projection theorem.

![All-layer gain and gate result](figures/qwen30b_ru_layer_gain_curve.png)

The upper panel shows controlled incremental utility beyond \(X\) and annotates its maximum at block 39. The lower panel shows that standalone DEV low-tail margins remain negative at every block. Gold and purple lines mark the independently frozen H3 primary and replication layers; they are not claims that block 48 has the largest incremental gain.

## Registered Verdicts

| Gate | Verdict | Direct basis |
| --- | --- | --- |
| H0 all-layer localization | `Pass` | 31/48 simultaneous lower bounds \(>0\); maximum at block 39 |
| H1 data validity | `Insufficient` overall; machine guards inherited Pass | Existing 19,200-row binding dataset and lexical guards pass; independent 64-row human review remains external |
| H2 full-space accessibility, block 48 primary | `Fail` | TEST-new accuracy 0.12969 with lower CI 0.12445, not strictly above chance 0.125 |
| H3 positive-margin admission, block 48 | `Fail` | TEST-same/new margin \(Q_{.05}\) -5.82955 / -11.19046; both intervals entirely negative |
| H2/H3 replication, block 38 | `Pass` / `Fail` | Accuracies 0.31016 / 0.23125, but margins -3.52356 / -6.66276 |
| H4 dense-Gaussian preservation | `SKIPPED_H3_NOT_PASS` | Primary H3 failed; normalized margin retention is ineligible |

## Exact Layer Localization

The experiment deliberately separates two meanings of “best layer”:

| Role | Block | Controlled excess [simultaneous 95% interval] | Standalone DEV margin \(Q_{.05}\) | Why selected |
| --- | ---: | ---: | ---: | --- |
| Maximum incremental utility | 39 | 0.10994 [0.09872, 0.12080] | -0.54060 | Largest \(R_U\) gain beyond \(X\) after duplicate-\(X\) and mismatched-\(R_U\) controls |
| Frozen H3 primary | 48 | 0.01369 [0.00248, 0.02456] | -0.52554 | Best standalone low-tail margin among H0-admitted layers |
| Frozen replication | 38 | 0.06442 [0.05320, 0.07529] | -0.53000 | Best eligible layer at least four blocks from the primary |
| Historical E01 primary | 24 | 0.10244 [0.09122, 0.11331] | -0.60267 | Historical comparison only; not used to freeze E02 |

TEST labels were removed from the selection view. The complete 48-row table is [tables/layer_scan.csv](tables/layer_scan.csv), and the immutable selector receipt is [tables/layer_freeze.json](tables/layer_freeze.json).

## Full-Space H2/H3 Results

| Block | TEST panel | Balanced accuracy [95% CI] | Margin \(Q_{.05}\) [95% CI] |
| ---: | --- | --- | --- |
| 48 | same | 0.17125 [0.16484, 0.17813] | -5.82955 [-5.95216, -5.74825] |
| 48 | new | 0.12969 [0.12445, 0.13500] | -11.19046 [-11.40759, -11.06038] |
| 38 | same | 0.31016 [0.30203, 0.31805] | -3.52356 [-3.59236, -3.46685] |
| 38 | new | 0.23125 [0.22429, 0.23859] | -6.66276 [-6.79532, -6.54119] |

All registered fits converged. Seed accuracy standard deviations are at most 0.000214. Permuted-label controls contain chance and the identity/common-offset controls pass at both blocks.

## Descriptive Diagnostics

These diagnostics cannot change H0--H4:

| Diagnostic | Block 48 | Block 38 | Boundary |
| --- | ---: | ---: | --- |
| Exact extreme \(D_{out}/D_{in}\), TEST-same/new | 0.3321 / 0.2027 | 0.2314 / 0.2205 | All 3,275,520 unordered pairs per panel; every ratio \(<1\) |
| Robust distance ratio, TEST-same/new | 0.7026 / 0.5315 | 0.5832 / 0.5357 | Every ratio \(<1\) |
| Learned orthogonal fine-label \(r_{90}\) | 64 | 64 | Functional readout only; not geometric rank |
| Fine-label accuracy, TEST-same/new | 0.05547 / 0.03281 | 0.15742 / 0.08750 | Weak 64-way task readout; chance 0.015625 |
| SVD-subspace coherence / Haar mean | 2.04 / 1.71 | 3.56 / 1.71 | Descriptive maximum leverage, not a dense-Gaussian premise |
| Normalized spectral entropy | 0.9888 | 0.9534 | High entropy does not imply Haar-uniform leverage |
| TRAIN coordinate theorem bound | 83,892 | 114,975 | Both exceed registered maximum 1,024; coordinate branch ineligible |

## Claim Boundary

**Can claim:** on the frozen model, data, token, residualizer family, and TRAIN/DEV selector, many Qwen3-30B-A3B layers contain controlled incremental label accessibility in \(R_U\) beyond \(X\). At the best H3-readiness admitted layer and a separated replication, standalone \(R_U\) does not satisfy the registered robust positive-margin gate. Therefore the current experiment has no valid premise for interpreting a dense-Gaussian preservation scan.

**Cannot claim:** that every layer is TEST-linearly inseparable; that \(R_U\) contains no information; that nonlinear or joint \((X,R_U)\) routing is impossible; that parent labels measure expert utility; or that random projection would fail when its positive-margin premise is met.

## Next Decision

**Proposed decision, awaiting human confirmation: open representation-space learning as the next research question, but define it as organizing existing conditional information into an expert-utility-aligned positive-margin routing space.** The minimal falsifier should compare a learned standalone representation with a joint \((X,R_U)\) baseline on genuinely held-out data and require positive low-tail margin before any compression study. Do not reopen preservation by changing layers, probes, or thresholds.
