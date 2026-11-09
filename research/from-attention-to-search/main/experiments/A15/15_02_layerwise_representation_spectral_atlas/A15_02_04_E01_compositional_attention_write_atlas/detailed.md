# A15_02_04_E01 Detailed Evidence Ledger

## 1. Question And Typed Result

**Question.** In frozen Qwen3-8B, does increasing the number of relation edges required to answer a matched query from one (D0) to two (D1) to four (D2) cause reliable semantic covariance to redistribute toward larger percentiles of each layer's own DCLM activation-covariance spectrum, especially in the isolated post-`o_proj` attention write?

**Typed result:** `insufficient_capability`.

| Clause | Result | Direct evidence |
| --- | --- | --- |
| Data/matching | Pass | 256 worlds; balanced answers; exact within-template lengths; frozen manifest |
| Model capability | Fail | D0/D1/D2 accuracy 0.262/0.227/0.230, below 0.70/0.55/0.40 |
| Required-edge necessity | Pass | all depth bootstrap lower bounds and edge-position estimates are positive |
| Hook/covariance/basis/numerics | Pass | 36/36 layers at both sites; registered tolerances pass |
| Early semantic reliability | Fail | D0 and D2 cross-template covariance lower bounds are negative at both sites |
| Post node-position robustness | Fail | only one of four leaf substitutions shares the positive primary sign |
| Post rank-shift diagnostic | Does not pass | \(T=0.00276\), CI crosses zero, below swap q95 |
| Pre rank-shift diagnostic | Positive but invalid | \(T=0.02409\), but capability and reliability gates fail |
| Composition-relative discriminability | Negative diagnostic | post \(T_D=-0.547\); pre \(T_D=-0.686\) |

Mandatory gates are evaluated before scientific Pass/Fail. The result therefore cannot be reported as a general rank-shift failure, even though the primary post diagnostic itself is not positive.

## 2. What “Moves Right” Means

Every layer \(ell\) and site \(s\) has a separate DCLM activation covariance

\[
\Sigma^{bg}_{\ell,s}=U_{\ell,s}\Lambda_{\ell,s}U_{\ell,s}^{\top}.
\]

The 500th eigenvector at layer 10 is not assumed to be the same object as the 500th eigenvector at layer 30. Cross-layer comparison uses only **local rank percentiles**. The 4096 ranks are divided into 16 projectors \(F_k\) of 256 dimensions. For hierarchy level \(g\), normalized between-class semantic mass in band \(k\) is

\[
p_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}
{\operatorname{tr}(B_{\ell,s,g})},
\]

and its local rank centroid is

\[
\rho^{(16)}_{\ell,s,g}=\sum_{k=1}^{16}\frac{k-0.5}{16}p_{\ell,s,g,k}.
\]

The registered statistic is

\[
T_{rank,s}
=\operatorname{median}_{25:35}(\rho_{D2}-\rho_{D0})
-\operatorname{median}_{1:12}(\rho_{D2}-\rho_{D0}).
\]

A positive \(T_{rank}\) means that D2 semantic variance is relatively farther toward lower-background-variance ranks than D0 in late blocks compared with early blocks. It does not mean that a vector travels rightward, that semantic information is in the tail, or that the tail is a universal complex-semantic module.

The independent discriminability statistic \(T_D\) asks whether D2 becomes more class-separable relative to D0. These are logically distinct: deeper complexity could produce higher \(D\) with no rank shift, a rank shift with no higher \(D\), both, or neither.

## 3. Frozen Model And Representation Boundaries

| Item | Frozen value |
| --- | --- |
| Model | `/data/share/Qwen3-8B` |
| Architecture | 36 decoder blocks; hidden size 4096; 32 attention heads; head width 128 |
| Model mode | frozen bfloat16 forward; no probe, fine-tuning, or intervention |
| Readout | hidden state at the final colon of `Answer:` |
| Pre site | \(a_\ell=\operatorname{Concat}(head_1,\ldots,head_{32})\in\mathbb R^{4096}\) immediately before `o_proj` |
| Post site | \(y_\ell=\mathrm{o\_proj}_\ell(a_\ell)\in\mathbb R^{4096}\) before residual addition |
| Excluded | residual stream, RMSNorm output, MLP state, SAE dictionary, parameter spectrum, Router |

Pre and post use separate calibration covariances at every block. Their values may be compared as normalized diagnostics, but their eigenvectors and raw coordinates are not equated.

## 4. Hierarchical Data Construction

### 4.1 One world

Each world samples five single-token aliases \(e_0,\ldots,e_4\) and four directed 2D spatial steps \(r_1,\ldots,r_4\). They form a path and a complete binary semantic tree:

```text
                         ROOT / D2: e0 -> e4 (r1+r2+r3+r4)
                         /                                  \
          C12 / D1: e0 -> e2 (r1+r2)       C34 / D1: e2 -> e4 (r3+r4)
               /              \                    /              \
 L1 / D0: e0->e1  L2 / D0: e1->e2  L3 / D0: e2->e3  L4 / D0: e3->e4
```

All seven queries see the same four facts and the same eight-word answer alphabet. Only query endpoints change. A frozen Latin schedule selects one of L1--L4, one of C12/C34, and ROOT per world for the equal-sample primary comparison. This prevents D0 and D1 from being permanently tied to the first or left-side edge. All seven positions remain a separate robustness audit.

### 4.2 Concrete example

For world `w000`, the facts are:

```text
Thomas is 1 step right and 1 step down from David.
Kelly is 1 step right and 0 steps up from Thomas.
Taylor is 1 step right and 1 step down from Kelly.
Ross is 1 step right and 0 steps up from Taylor.
```

The frozen primary nodes are:

| Depth | Query | Required edges | Answer |
| --- | --- | ---: | --- |
| D0 / L1 | Thomas relative to David | 1 | southeast |
| D1 / C12 | Kelly relative to David | 2 | southeast |
| D2 / ROOT | Ross relative to David | 4 | southeast |

The generator balances each depth over all eight compass answers, so the shared answer in this single example is not a dataset-level shortcut. A counterfactual flips one required relation with a token-count-matched phrase and recomputes the answer. A query-binding reversal swaps query start and end while preserving all facts and query token inventory; its recomputed correct answer is the opposite direction.

### 4.3 Counts and matching

| Item | Count or value |
| --- | ---: |
| Worlds | 256 |
| Templates | 4 (T1/T2 design; T3/T4 confirmation) |
| Answer classes | 8, exactly balanced per primary depth and per fixed node |
| All-node core prompts | 7,168 = 256 worlds × 7 nodes × 4 templates |
| Equal-sample primary prompts | 3,072 = 256 × 3 depths × 4 templates |
| Primary confirmation prompts | 1,536 = 512 per depth |
| Required-edge counterfactuals | 768 |
| Query-binding reversals | 768 |
| Total model prompts | 8,704 |
| Token lengths by template | T1 160; T2 166; T3 167; T4 160 |
| Generator seed | 20260806 |
| Data manifest SHA-256 | `73546b7699717157f9f18536c43d3f63801d63fda8c7d22c2565ef347128eab9` |

The world family is the statistical unit. Nodes, templates, prompts, and tokens are repeated measurements, not independent samples.

## 5. Calibration And Estimators

The background basis uses 65,536 frozen DCLM tokens, with two independent 32,768-token halves. Calibration tensor SHA-256 is `d88620267dbdc9c2b87ec24c2f51d9e6fb317cb8c051ec96503414ea9bff60b9`. Each layer and site receives its own centered covariance and eigendecomposition.

After removing additive template and world main effects, answer-class means define between-class covariance \(B\) and within-class world/template covariance \(W\).

| Metric | Computation and unit | Decision role | Cannot prove |
| --- | --- | --- | --- |
| \(V\) | \(\operatorname{tr}(B)\), activation squared | semantic signal scale | stable class readability |
| \(D\) | \(\operatorname{tr}(B)/(\operatorname{tr}(W)+\epsilon)\) | semantic discriminability | rank destination or accuracy |
| \(R\) | \(\operatorname{tr}(B)/(\operatorname{tr}(\Sigma^{bg})+\epsilon)\) | scale relative to background | task solution |
| \(p_k\) | band \(B\) divided by total \(B\) | normalized rank allocation | reliable signal if \(V\) is noise |
| \(\rho^{(16)}\) | centroid of \(p_k\) over F1--F16 | primary local-rank location | direction identity across layers |
| \(\bar b_k\) | band \(B\) per direction | raw band scale | specificity |
| \(j_k\) | band \(B\) divided by band \(W\) | band-local discriminability | routing utility |
| \(V_\times\) | cross-product of class means estimated from disjoint templates | reliability gate | nonnegative variance by definition |

A negative \(V_\times\) means independent templates do not agree on the answer-class mean geometry at that layer; it is not a negative physical variance. The location statistic is uninterpretable when this reliability gate fails.

World-family bootstrap and paired within-world D0/D2 condition swaps each use 2,000 replicates. Early blocks are 1--12, late blocks are 25--35, and block 36 is displayed but excluded from the registered contrast.

## 6. Capability And Control Evidence

### 6.1 Frozen next-token capability

| Depth | Correct / total | Accuracy | Wilson lower | Required accuracy |
| --- | ---: | ---: | ---: | ---: |
| D0 | 134 / 512 | 0.2617 | 0.2255 | 0.70 |
| D1 | 116 / 512 | 0.2266 | 0.1924 | 0.55 |
| D2 | 118 / 512 | 0.2305 | 0.1961 | 0.40 |

Chance is 0.125. The model is above chance but far below the registered thresholds, and none of the Wilson lower bounds exceeds the additional 0.25 floor. This is the first mandatory failure and types the experiment `insufficient_capability`.

### 6.2 Required-edge counterfactual necessity

The counterfactual metric is the paired change in new-answer versus old-answer log odds after a required relation edge is changed.

| Depth | Estimate | World-bootstrap 95% interval |
| --- | ---: | ---: |
| D0 | 1.780 | [1.483, 2.075] |
| D1 | 0.625 | [0.490, 0.771] |
| D2 | 0.493 | [0.365, 0.626] |

Every required-edge-position point estimate is positive. This passes the necessity gate: the model's distribution responds to required facts. It does not rescue low exact-answer accuracy.

### 6.3 Query-binding reversal

The reversal control does not independently reproduce the registered shift: pre \(T=0.00609\), interval \([-0.01309,0.01644]\), null q95 0.01317; post \(T=0.00356\), interval \([-0.00758,0.01166]\), null q95 0.00868. The negative-control gate passes.

## 7. Primary Rank And Scale Evidence

| Site | \(T_{rank}\) | Equivalent ranks | Bootstrap 95% interval | Swap q95 | Design \(T\) | Half-basis \(T\) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pre-`o_proj` | 0.02409 | 98.7 | [0.00189, 0.02811] | 0.01393 | 0.02186 | 0.02970 / 0.02963 |
| post-`o_proj` | 0.00276 | 11.3 | [-0.00269, 0.01229] | 0.00792 | 0.00622 | 0.00708 / 0.00461 |

![Registered trajectories](figures/figure1_decisive_rank_redistribution.png)

Post fails the registered effect rule: its interval crosses zero and the point estimate is below the paired-null q95. Pre passes these numerical diagnostics but fails mandatory capability and early reliability, so it is not evidence for the scientific claim.

Composition-relative discriminability decreases from early to late:

| Site | \(T_D\) | Bootstrap 95% interval |
| --- | ---: | ---: |
| pre-`o_proj` | -0.686 | [-0.940, -0.300] |
| post-`o_proj` | -0.547 | [-0.933, -0.222] |

The large-level/small-level scale difference is substantial. For example, post late median \(V\) is 7.153 for D0, 0.866 for D1, and 1.217 for D2; post late median \(D\) is 0.0537, 0.0216, and 0.0255. This is why raw variance, discriminability, and normalized rank location are reported separately.

![Scale-versus-location audit](figures/figure2_scale_location_audit.png)

## 8. Reliability And Node-Position Evidence

For both sites, early D0 and D2 have zero positive \(V_\times\) blocks out of 12 and negative bootstrap intervals. Late signal is positive, but a late-minus-early location contrast cannot be treated as semantic movement when the early class geometry does not reproduce across templates.

| Site/depth | Early \(V_\times\) point median | Early bootstrap 95% interval | Positive early blocks | Late bootstrap 95% interval |
| --- | ---: | ---: | ---: | ---: |
| pre D0 | -0.000194 | [-0.000440, -0.000237] | 0/12 | [0.539, 2.292] |
| pre D2 | -0.000178 | [-0.000438, -0.000225] | 0/12 | [0.096, 0.330] |
| post D0 | -0.000716 | [-0.001535, -0.000845] | 0/12 | [1.493, 6.867] |
| post D2 | -0.000617 | [-0.001508, -0.000773] | 0/12 | [0.171, 1.097] |

For post, ROOT-minus-leaf \(T\) estimates are -0.00105, -0.00032, -0.00103, and +0.00225 for L1--L4. Only one shares the positive primary sign, so the node-position gate fails. Pre estimates are all positive (0.02440, 0.01830, 0.01947, 0.02849), but the earlier mandatory failures remain.

![Seven-node position and aggregate heatmaps](figures/figure5_seven_node_hierarchy_heatmaps.png)

## 9. Band And Background Diagnostics

F1 is the highest-background-variance band and F16 the lowest within each layer/site. The heatmaps report three different D2-versus-D0 quantities:

1. normalized semantic share \(p_{D2,k}-p_{D0,k}\);
2. raw semantic variance per direction \(\log(\bar b_{D2,k}/\bar b_{D0,k})\);
3. band discriminability \(\log(j_{D2,k}/j_{D0,k})\).

![Layer-by-band diagnostics](figures/figure3_layer_band_heatmaps.png)

The maps are descriptive because capability and reliability fail. In particular, a red normalized-share cell cannot be called a semantic destination when the corresponding reliable variance is absent. DCLM effective-rank changes are shown separately and cannot count as semantic movement.

![Background and control separation](figures/figure4_background_and_controls.png)

## 10. Execution Record

Worker surface:

`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_07_e01_qwen3_compositional_attention_write_spectral_atlas/`

Formal run:

`runs/a15-01-07-e01-extract-20260806T182500Z/`

Entry commands were the approved worker scripts:

```bash
bash scripts/submit_extract_acp.sh
bash scripts/submit_analysis_acp.sh
bash scripts/submit_finalize_acp.sh
```

Each submission used one ACP node with 8×5090 SPOT (`n12lp.nn.i10a.8`).

| Job | Role | State | Retries |
| --- | --- | --- | ---: |
| `om-pbybysxg` | extraction and consolidation | SUCCEEDED | 0 |
| `om-bj8mm9ot` | all 36-layer pre/post statistics | FAILED after outputs complete | 1 |
| `om-v4omoym1` | deterministic verdict finalization | SUCCEEDED | 0 |

The analysis job wrote every registered CSV and NPZ for both sites, then failed while serializing one NumPy integer in the final JSON. Its retry repeated and completed the same scientific calculations before the same packaging failure. The repair changed only JSON conversion and deterministic rendering; no data, state tensor, covariance basis, bootstrap/null array, metric, threshold, or scientific condition was recomputed or changed. The finalizer reconstructed the verdict from those completed arrays.

## 11. Hard Guards And Coverage

| Guard | Result |
| --- | --- |
| Generator audit | Pass |
| Core / total prompt coverage | 7,168 / 8,704 |
| Semantic state coverage | 8,704 records × 36 layers × 2 sites |
| Head concatenation replay | exact |
| Direct `o_proj` replay | within registered \(10^{-6}\) tolerance |
| Calibration layers | 36/36 pre and 36/36 post |
| Calibration token tensor | frozen 65,536-token hash matches |
| Basis stability | at least 34/36 plus blocks 35/36; Pass |
| Maximum projection-energy relative error | below \(2.5\times10^{-4}\); Pass |
| Figure file audit | five nonblank images, each at least 1000 px and 20 KB |
| Human visual audit | axes, legends, colorbars, signs, local-rank wording, block-36 boundary, failed gates checked |

## 12. Claim Ledger

| Statement | Status | Boundary |
| --- | --- | --- |
| The experiment uses data-covariance spectra, not parameter spectra | Established by construction | separate site/layer DCLM covariance |
| Cross-layer rank comparison need not identify the same eigenvector | Established definition | local percentile distribution only |
| Post-`o_proj` shows a registered composition-specific right shift | Not supported diagnostically | \(T\) below null; CI crosses zero |
| Pre-`o_proj` shows valid evidence for a right shift | Not established | positive diagnostic invalidated by gates |
| D2 becomes more discriminable relative to D0 in late layers | Contradicted in this diagnostic | \(T_D<0\) at both sites, but capability insufficient |
| The general hypothesis is false | Cannot claim | current task interface fails capability and reliability |
| Composition lives in middle/tail bands | Cannot claim | no reliable destination inference |
| Attention causally performs the composition | Not tested | static states only |
| SAE dictionary nodes should replace constructed semantic nodes | Not tested | no SAE in scope |
| Any spectrum improves routing | Not tested | no Router or training |

## 13. Artifact Map

- Approved design: [protocol.md](protocol.md)
- Concise reading path: [summary.md](summary.md)
- Integrated typed verdict: [provenance/verdict.json](provenance/verdict.json)
- Site verdicts: [pre](provenance/pre_verdict.json), [post](provenance/post_verdict.json)
- Data manifest: [provenance/data_manifest.json](provenance/data_manifest.json)
- Semantic-state manifest: [provenance/semantic_state_manifest.json](provenance/semantic_state_manifest.json)
- Execution jobs: [provenance/execution_jobs.json](provenance/execution_jobs.json)
- Figure audit: [provenance/figure_audit.json](provenance/figure_audit.json)
- Complete exported tables: [tables/](tables)
- Five audited figures: [figures/](figures)

## 14. One Next Decision

Decide whether to run a capability-only interface repair while freezing the current worlds, hierarchy, answer balancing, two representation sites, covariance bases, metrics, and gates. A candidate may enter a new spectral confirmation only if held-out D0/D1/D2 accuracy reaches 70%/55%/40%, every Wilson lower bound exceeds 25%, and early D0/D2 cross-template semantic covariance lower bounds are positive. Spectral trajectories remain sealed during interface selection.
