---
experiment_id: A15_03_E01_middle_band_stability_decomposition
legacy_experiment_id: A15_01_12_E01_middle_band_stability_decomposition
anchor_id: 15_03_middle_band_information
legacy_anchor_id: 15_01_12_middle_band_stability_decomposition
status: DRAFT_NOT_EXECUTABLE
canonical_language: en
created: 2026-08-09
---

# Protocol: Decomposing Apparent Middle-Band Spectral Stability

Primary source: [A15_03 Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_03_middle_band_information/15_03_middle_band_information_anchor.md).

## 0. Approval Snapshot

- **Document status:** `DRAFT_NOT_EXECUTABLE`.
- **Approval status:** the researcher authorized creation of an independent middle-band Anchor and draft Protocol only. No design block below has been silently promoted from proposal to confirmation.
- **Block audit:** A `CONFIRMED`; B--F `PROPOSED`; G `BLOCKED_NO_EXECUTION_APPROVAL`.
- **Cross-block consistency:** `AI_AUDIT_PASS_PENDING_RESEARCHER_CONFIRMATION`.
- **Execution scope approved:** none. No implementation, raw-$\Delta n$ replay, smoke, full analysis, remote job, result record, graph edit, publication, commit, or push is authorized.
- **Purpose:** `metric audit / root-cause audit`, not method construction.
- **Primary Anchor:** A15_03, independent of the A15_04 shared-tail decision.
- **One uncertainty:** whether the apparently least-changing normalized F2--F8 semantic-variance curve reflects stable absolute magnitude and cross-layer direction identity, rather than normalization, internal cancellation, or local-rank averaging.
- **Frozen model and bank:** Qwen3-8B; A15_02_06's 512 balanced records; actual post-RMSNorm attention increment $\Delta n_\ell$.
- **Frozen parameter partition:** sixteen local 256-direction bands; F1 head, F2--F8 middle, F9--F16 tail.
- **`AI_PROPOSAL` primary semantic object:** conditional-fine within-parent between-class covariance. Coarse is a replication control and cannot rescue the primary verdict.
- **One primary metric:** $D_M$, the root-mean-square early-to-late log fold-change of absolute per-direction variance in F2--F8.
- **`AI_PROPOSAL` equivalence margin:** $\delta_M=\log(1.25)$, or 25% typical absolute drift.
- **Direction-identity guard:** local and cross-fitted shared F2--F8 capture relative to matched rank-1,792 Haar spaces in early and late layers.
- **Pass:** absolute middle-curve drift is within the confirmed equivalence margin and shared-middle capture beats Haar across registered strata.
- **Fail:** the apparent stability is not reproduced, is explained by absolute/internal aggregation, is only a local-rank pattern without shared direction identity, is Haar-like, or contains both artifacts.
- **Insufficient:** provenance, covariance reliability, equivalence precision, cross-fold stability, or Haar comparison is unresolved.
- **Cannot claim:** semantic content, linear novelty, native MLP use, functional utility, expert specialization, or Router gain.
- **Requested review decisions:** confirm or correct (1) conditional-fine as primary, (2) $D_M$, (3) $\delta_M=\log(1.25)$, (4) the independent raw-$\Delta n$ replay contract, (5) 512 Haar partitions and 2,000 bootstraps, and (6) the typed verdict precedence in Section 15.

## 1. Terminology / Definitions

| Term | Plain meaning | Frozen computation | Unit / decision role | Cannot establish |
| --- | --- | --- | --- | --- |
| fixed bank $S_0$ | texts fixed before this reanalysis and never replaced after viewing a result | A15_02_06's 512 records | sample identity; bounds the claim | population generality |
| actual increment $\Delta n_\ell$ | what attention changes at the input actually consumed by the current layer's MLP | $RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)$ | activation coordinate under audit | information-theoretic novelty |
| local parameter rank | gain order inside one layer's native MLP input operator | descending eigensystem of $K_\ell=W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}$ | rank only | cross-layer vector identity |
| F1--F16 | complete equal-width local parameter spectrum | sixteen contiguous 256-direction projectors | audit partition | functional roles |
| middle F2--F8 | ranks 257--2048 in one layer, total rank 1,792 | $P_{\ell,M}=\sum_{k=2}^{8}P_{\ell k}$ | only band adjudicated here | that F2--F8 is useful |
| absolute per-direction variance | semantic class-center variance carried per parameter direction | $A_{\ell k}=\operatorname{tr}(P_{\ell k}B_\ell)/256$ | squared-activation scale | normalized occupancy or use |
| normalized share | fraction of total semantic variance in one band | $p_{\ell k}=\operatorname{tr}(P_{\ell k}B_\ell)/\operatorname{tr}(B_\ell)$ | dimensionless geometry | absolute magnitude |
| within-middle shape | how the fixed middle mass is distributed from F2 through F8 | $q_{\ell k}=p_{\ell k}/\sum_{j=2}^{8}p_{\ell j}$ | internal rank allocation | direction identity |
| local middle | the evaluated layer's own F2--F8 projector | $P_{\ell,M}$ | local positive/control view | cross-layer persistence |
| shared middle | a rank-1,792 consensus orientation built only from other layers' local middle projectors | $Q_M^{(-f)}$ | cross-layer direction guard | semantic content or function |
| projector overlap | how much two rank-1,792 parameter spaces geometrically coincide | $\operatorname{tr}(P_1P_2)/1792$ | parameter-space stability relative to Haar | semantic capture or use |
| Haar middle | an arbitrary rank-1,792 orientation from a matched random orthogonal 16-band partition | same draw applied to every layer | orientation null | a random neural mechanism |
| early / late | fixed depth blocks | blocks 1--12 / 25--35 | decision contrast | independent samples |
| practical equivalence | a pre-run bound small enough to call absolute curve change negligible for this question | $D_M\le\delta_M$ | stability decision | exact equality |

The **middle parameter band** F2--F8 is distinct from the **middle depth block** 13--24, which is descriptive only.

## 2. Anchor Alignment

- **Anchor clause tested:** whether the normalized middle curve's apparent depth stability survives absolute-scale, internal-shape, and cross-layer-orientation checks.
- **Physical prior:** a stable normalized aggregate is not a stable geometric object unless absolute magnitude, sub-band allocation, and direction identity agree.
- **Primary representation:** raw actual $\Delta n_\ell$ in the native post-RMSNorm coordinate.
- **Primary metric:** $D_M$ only. Scale, shape, normalized share, and orientation measurements explain or guard it; none may replace it after results are visible.
- **Main falsifier:** identical or nearly identical rank curves coexist with a shared-middle capture no better than Haar, or absolute/internal change exceeds the predeclared equivalence margin despite a flat normalized aggregate.
- **Claim boundary:** frozen-model geometry on $S_0$ only.

This Protocol is scientifically and operationally separate from A15_04:

| Boundary | A15_04 | A15_03 |
| --- | --- | --- |
| tested band | broad F9--F16 tail | F2--F8 middle |
| primary decision | late semantic enrichment in shared tail | whether apparent middle stability survives scale, shape, and orientation checks |
| primary metric | tail-specific capture contrast | absolute seven-band drift $D_M$ |
| output root | `A15_04_E01_shared_tail_geometry/` | this directory |
| execution approval | separate and currently absent | separate and currently absent |

No A15_04 implementation, job, amendment, result table, or approval may be extended to include A15_03. Shared immutable source hashes may be cited, but each Protocol must own its own eligible input manifest and verdict.

Earlier A15_05/A15_05_05 functional failures remain binding context: a geometry Pass cannot reopen fixed-band Router training without a new function-aligned admission question.

## 3. Tested Hypotheses

**H1 -- true middle stability.** Absolute F2--F8 per-direction variance is practically equivalent from early to late depth, its seven-band internal shape does not move materially, and the cross-fitted shared middle captures conditional-fine variance above matched Haar in both depth blocks.

**H2 -- aggregation artifact.** The broad normalized F2--F8 share appears flat while the absolute curve changes. A common component indicates total-scale cancellation; a residual component indicates within-middle redistribution. Both may coexist and are not separate primary hypotheses.

**H3 -- rank-averaging artifact.** Absolute and normalized F2--F8 rank curves remain similar, but the shared middle does not beat Haar even when the evaluated layer's local middle does. Stability then belongs to a rank interval, not a persistent cross-layer orientation.

At most these three hypotheses are adjudicated. A mixed H2+H3 outcome must be preserved. No hypothesis predicts functional benefit.

## 4. Rival Explanations

| Rival | Distinct prediction | Registered separator |
| --- | --- | --- |
| total-variance normalization | absolute middle per-direction variance grows with total variance while broad normalized share stays flat | $D_M$, common log-growth $g_M$, total per-direction trace growth |
| canceling movement inside middle | broad F2--F8 share stays flat but F2--F8 changes are nonuniform or move left/right | residual drift $D_{shape}$ and within-middle Wasserstein distance |
| unstable layer-specific directions | local rank curves look stable but cross-fitted shared-middle capture is Haar-like | local/shared/Haar dimension-normalized capture |
| generic high-dimensional retention | both true and random rank-1,792 spaces capture similar variance | matched orthogonal Haar partitions applied globally across layers |
| terminal-block anomaly | block 36 creates the visual impression | block 36 excluded from all decisions |
| wording or parent dominance | one domain or prompt form controls the effect | paired parent/template bootstrap and fixed half reports |
| numerical basis/replay mismatch | curves change because coordinates or samples differ | immutable hashes, same-run replay, hook identity, and projection reconstruction |

The Protocol does not ask which semantic labels middle represents and does not fit a probe. Those are later questions only if a stable object survives.

## 5. Data Construction And Provenance

### 5.1 Frozen semantic bank

Use exactly the A15_02_06 bank:

- 8 parent domains;
- 8 children per parent;
- 4 label-free templates per child;
- 2 fact bundles per template;
- $8\times8\times4\times2=512$ records;
- template reliability half A: templates 1--2 with both bundles;
- template reliability half B: templates 3--4 with both bundles;
- common final `Classification:` readout;
- dataset manifest identifier `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`;
- dataset file SHA-256 `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1`.

No text, record order, label, template, tokenization, readout position, split, or class weight may change.

The template halves have already contributed to earlier A15 analyses. They are fixed reliability strata, not untouched confirmation data. Bootstrap intervals describe uncertainty on $S_0$ under the registered resampling scheme and do not create population confirmation.

### 5.2 Conditional-fine covariance

For raw increment $z_{pcet}^{(\ell)}$ with parent $p$, child $c$, template $e$, and bundle $t$:

$$
\mu_{pc}^{(\ell)}=\frac{1}{8}\sum_{e,t}z_{pcet}^{(\ell)},
\qquad
\mu_p^{(\ell)}=\frac{1}{8}\sum_c\mu_{pc}^{(\ell)},
$$

$$
B_{\ell,F}=\frac{1}{64}\sum_{p=1}^{8}\sum_{c=1}^{8}
(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})
(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})^{\top}.
$$

The displayed formula above is valid only if the first parenthesized vector is interpreted as a column and the second as its transpose. Implementation must use the outer product

$$
B_{\ell,F}=\frac{1}{64}\sum_{p,c}d_{pc}^{(\ell)}d_{pc}^{(\ell)\top},
\qquad d_{pc}^{(\ell)}=\mu_{pc}^{(\ell)}-\mu_p^{(\ell)}.
$$

The second form is the executable definition. It gives every parent and child equal weight. Compute traces from centered class-mean matrices when numerically equivalent; do not form a dense covariance merely for convenience.

`AI_PROPOSAL`: $B_{\ell,F}$ is primary. The matching coarse covariance is computed only after the primary verdict is frozen and cannot rescue it.

### 5.3 Frozen parameter sources

Use the A15_02_06 native input-Gram bases from run `a15-01-09-e01-p-20260807T061000Z`; its artifact-manifest SHA-256 is `2fd84effc280e7090fe33a99e44446df083f2556de592c3fa8ee4faa0b99bf59` and it covers 36/36 layers.

Every layer basis hash, descending order, shape, orthogonality, and eigensolver residual must match the frozen manifest. Recomputing a basis is forbidden unless the Protocol is amended before any semantic result is viewed.

### 5.4 Independent raw-$\Delta n$ materialization

The old A15_02_06 response parts store layer-local `delta_projection` coordinates from a separately recomputed eigensystem whose vectors were not saved. They cannot be combined with the P-run bases to make cross-layer projections.

This draft therefore proposes one A15_03-owned deterministic replay of the unchanged model and $S_0$ to save raw bfloat16 $\Delta n_\ell\in\mathbb R^{512\times4096}$ for all 36 layers. This is an execution stage and is **not authorized** by the present request.

Mandatory replay guards are:

1. exact dataset identity and record order;
2. 36/36 layers, 512/512 records, finite values, exact shapes;
3. same-run repeated-batch replay maximum absolute error 0;
4. direct hook-site identity at blocks 1, 21, and 36 with maximum relative error below $10^{-5}$;
5. projection reconstruction in the frozen P-run basis with relative error below $10^{-4}$ at every layer;
6. all conditional-fine traces and F1--F16 band masses strictly positive and finite;
7. a non-gating report of the difference from the older cross-hardware cache.

The old cache is not an exact stop oracle because A15_02_07 E01 showed reproducible cross-hardware bfloat16 differences even after restoring batch size. Replacing the proven same-run guards with post-hoc cache tolerance is forbidden.

Any failed mandatory item yields `INSUFFICIENT_INPUT_PROVENANCE`; no middle verdict is computed.

## 6. Diagnostic Task And Permitted Supervision

There is no learned probe, model training, label prediction, task loss, or intervention. Labels are used only to form balanced coarse and conditional-fine class centers.

The diagnostic task is:

1. measure the exact absolute directional curve $b_{\ell i}$;
2. aggregate its frozen F1--F16 and F2--F8 band views;
3. separate absolute scale from full-spectrum normalization and within-middle redistribution;
4. compare local and cross-fitted shared F2--F8 capture with matched Haar partitions;
5. assign one typed geometry verdict.

No result may be interpreted as linear readability, conditional novelty, native MLP transmission, or useful routing.

## 7. Model / Parameter Spaces And Frozen Variants

### 7.1 Model and operator

- model: frozen `/data/share/Qwen3-8B`;
- 36 decoder blocks; hidden dimension $d=4096$;
- native post-RMSNorm MLP-input operator $K_\ell$ only;
- `down_proj` excluded because it maps MLP hidden units back to residual space;
- no RMSNorm-folded operator because $\Delta n_\ell$ is already in the native post-RMSNorm coordinate.

### 7.2 Complete rank partition

For each layer, $P_{\ell k}$ contains descending ranks $256(k-1)+1$ through $256k$ for $k=1,\ldots,16$. Middle is exactly F2--F8, ranks 257--2048. No centered-rank alternative, adaptive cutoff, eigenvalue threshold, or result-selected regrouping is permitted.

Retain all exact $b_{\ell i}=v_{\ell i}^{\top}B_{\ell,F}v_{\ell i}$ values. The registered unsmoothed decision curve uses the seven band averages $A_{\ell,2:8}$. A plot may show a frozen 129-rank arithmetic-mean overlay only if the exact thin curve remains visible and no metric uses the overlay.

### 7.3 Cross-fitted shared middle

Exclude block 36. Freeze group A as odd blocks $\{1,3,\ldots,35\}$ and group B as even blocks $\{2,4,\ldots,34\}$. For evaluated layer group $f$:

$$
Q_M^{(-f)}=\operatorname{TopEig}_{1792}
\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,M}\right).
$$

Construct rank-256 shared $Q_k^{(-f)}$ separately for F2--F8. These sub-band spaces localize orientation stability; they are secondary and cannot rescue a failed broad shared-middle gate. Consensus spaces need not be mutually orthogonal and their captures must not be summed.

Require normalized orthogonality error and eigensolver residual at most $10^{-5}$. Report the overlap between odd-built and even-built consensus spaces against matched Haar overlap, but do not use the evaluated layer's activation or labels to construct any shared parameter space.

Freeze local and consensus parameter-overlap metrics:

$$
O_{\ell m,M}=\frac{\operatorname{tr}(P_{\ell,M}P_{m,M})}{1792},
\qquad
O_{shared,M}=\frac{\operatorname{tr}(Q_M^{(A)}Q_M^{(B)})}{1792}.
$$

The registered local guard is

$$
O_{local,M}=\operatorname{median}_{1\le\ell<m\le35}O_{\ell m,M}.
$$

Report adjacent-pair and layer-gap-at-least-18 summaries separately as diagnostics. Compare $O_{local,M}$ and $O_{shared,M}$ with the 95th percentile from 512 independent Haar rank-1,792 projector-pair overlaps, whose expectation is $1792/4096=7/16$. Using the single-pair q95 for the all-pair median is deliberately conservative; it is a geometric control, not a p-value. These parameter-only overlaps are direction-stability guards; semantic capture is still required for `TRUE_MIDDLE_STABILITY`.

### 7.4 Matched Haar construction

For each random draw, sample one 4096-dimensional Haar orthogonal matrix and divide it into the same sixteen 256-direction bands. The F2--F8 union is one rank-1,792 Haar middle. The same complete partition is applied to every layer and both template halves.

An independent random redraw per layer tests a different question and is forbidden. Random partitions are analysis controls only; they are not model interventions.

## 8. Objective, Precision, And Randomness

- No training objective, optimizer, schedule, checkpoint selection, or tuning exists.
- Replay is bfloat16; projector operations are FP32 with audited residuals; class means, traces, logarithms, contrasts, and uncertainty are FP64.
- Replay seed: `0` where applicable.
- Haar-partition seed: `151201`.
- Hierarchical-bootstrap seed: `151202`.
- `AI_PROPOSAL`: 512 matched Haar partitions.
- `AI_PROPOSAL`: 2,000 paired hierarchical bootstraps.
- `AI_PROPOSAL`: equivalence margin $\delta_M=\log(1.25)$.
- Unsealing occurs when any new A15_03 middle metric is computed on $S_0$. After that point, seeds, bands, layer windows, semantic object, metric, margin, random construction, and verdict rules are frozen.

The false-positive cost of `true_middle_stability` is advancing a rank-only artifact toward a later functional design. The false-negative cost is parking a genuinely stable middle coordinate. The Protocol therefore requires both practical equivalence and cross-layer orientation evidence; failure of either cannot be rescued by the other.

## 9. Conditions, Layers, And Frozen Comparisons

| Item | Frozen value | Evidence role |
| --- | --- | --- |
| full spectrum | exact directions plus F1--F16 band means and shares | context and phenomenon audit |
| primary middle | F2--F8, ranks 257--2048 | only adjudicated band |
| primary semantics | conditional-fine $B_{\ell,F}$ | primary |
| coarse semantics | matched coarse covariance | replication control only |
| early depth | blocks 1--12 | primary contrast |
| middle depth | blocks 13--24 | descriptive trajectory |
| late depth | blocks 25--35 | primary contrast |
| block 36 | separate terminal display | excluded from construction and verdict |
| reliability strata | full bank; templates 1--2; templates 3--4 | fixed robustness reports |
| layer folds | odd/even among 1--35 | cross-fitted construction/evaluation |
| absolute view | $b_{\ell i}$ and $A_{\ell k}$ | detects scale and shape change |
| normalized view | $p_{\ell k}$ and $q_{\ell k}$ | detects normalization and internal transport |
| orientation views | local middle, shared middle, shared F2--F8, global Haar partitions | direction-identity guard |
| parameter overlap | local layer-pair and odd/even shared-consensus overlap versus independent Haar pairs | parameter-space stability guard |

No shared head or shared tail verdict is computed here. Head and tail broad normalized shares are used only to check the researcher's premise that middle appears least-changing; they do not import the A15_04 mechanism.

## 10. Primary Metric And Frozen Analysis Plan

### 10.1 Absolute variance curve

For band $k$:

$$
A_{\ell k}=\frac{\operatorname{tr}(P_{\ell k}B_{\ell,F})}{256}.
$$

Let

$$
A_{E,k}=\operatorname{median}_{\ell=1:12}A_{\ell k},
\qquad
A_{L,k}=\operatorname{median}_{\ell=25:35}A_{\ell k},
\qquad
u_k=\log\frac{A_{L,k}}{A_{E,k}}.
$$

All inputs must be strictly positive. No result-dependent floor or clipping is allowed.

### 10.2 One primary metric

$$
D_M=\sqrt{\frac{1}{7}\sum_{k=2}^{8}u_k^2}.
$$

$D_M=0$ only when every registered F2--F8 absolute per-direction band value is identical in the early and late medians. The candidate equivalence rule is:

$$
\operatorname{UCB}_{95\%}(D_M)\le\delta_M=\log(1.25).
$$

The full-bank interval is primary. Both fixed template-half point estimates must also be at most $\delta_M$. The margin and half rule require explicit confirmation before promotion.

### 10.3 Exact decomposition and normalized diagnostics

$$
g_M=\frac{1}{7}\sum_{k=2}^{8}u_k,
\qquad
D_{shape}=\sqrt{\frac{1}{7}\sum_{k=2}^{8}(u_k-g_M)^2},
\qquad
D_M^2=g_M^2+D_{shape}^2.
$$

Report total absolute per-direction semantic-variance growth

$$
g_{all}=\log\frac{
\operatorname{median}_{\ell=25:35}\operatorname{tr}(B_{\ell,F})/4096}
{\operatorname{median}_{\ell=1:12}\operatorname{tr}(B_{\ell,F})/4096}.
$$

If $g_M$ is close to $g_{all}$ while the normalized broad middle share is flat, the descriptive reading is scale cancellation. The relative size of $|g_M|$ and $D_{shape}$ identifies the larger observed component but does not by itself prove a causal mechanism.

For within-middle transport, define early/late $q_{E,k},q_{L,k}$ from block-median band masses and register

$$
W_M=\frac{1}{6}\sum_{j=2}^{7}
\left|\sum_{k=2}^{j}(q_{L,k}-q_{E,k})\right|.
$$

$W_M$ is the one-dimensional earth-mover distance on the seven equally spaced middle bands. It detects left/right redistribution but is secondary.

### 10.4 Direction-identity guard

First compare local layer-pair overlap $O_{\ell m,M}$ and odd/even consensus overlap $O_{shared,M}$ with matched independent-Haar distributions. Overlap is parameter-only and cannot replace semantic capture.

For local or shared middle projector $Q$:

$$
e_{\ell,Q}=\frac{
\operatorname{tr}(QB_{\ell,F})/\operatorname{tr}(B_{\ell,F})}
{1792/4096}.
$$

For every Haar partition $h$, compute the identical early and late block medians $E_{Haar,h}$ and $L_{Haar,h}$. Report local and shared middle against the 95th percentile of the matched Haar distributions in both blocks. $e=1$ is only the expectation; the q95 controls finite-draw and fixed-covariance anisotropy.

### 10.5 Uncertainty and aggregation

Use 2,000 paired replicates that resample the eight parents with replacement and the four template clusters with replacement; selecting a template retains both fact bundles and all children. Apply the same replicate simultaneously to all layers, bands, and tested spaces. Do not resample eigen-directions or layers as independent observations.

Use percentile 95% intervals. Missing records, layers, bands, or non-finite values invalidate the replicate source rather than being imputed or filtered. No outlier exclusion is permitted.

### 10.6 Frozen analysis order

1. verify immutable input, replay, parameter, and covariance guards;
2. reproduce the apparent normalized-middle premise without looking at shared-space results;
3. compute $D_M$ and its interval;
4. freeze the scale/shape decomposition label;
5. compute local/shared/Haar orientation evidence;
6. apply the typed verdict precedence in Section 15 once;
7. inspect per-band, coarse, middle-depth, and block-36 diagnostics only after the verdict is fixed.

## 11. Secondary Metrics And Guards

1. **Apparent-stability premise.** Let $N_G$ be the absolute early-to-late change in broad normalized share for $G\in\{H,M,T\}$. Middle is “least-changing” only if $N_M<N_H$ and $N_M<N_T$ on the full bank and is not the largest in either template half.
2. **Exact directional curves.** Store and plot all 4,096 $b_{\ell i}$ values; no individual direction is an independent replicate or a cross-layer identity.
3. **Seven-band normalized curve.** Report $p_{\ell,2:8}$ and $q_{\ell,2:8}$ for every layer, not only the broad F2--F8 sum.
4. **Within-middle centroid.** Report $C_{M,\ell}=\sum_{k=2}^{8}q_{\ell k}(k-2)/6$ as the signed left/right summary; $W_M$ remains the unsigned transport amount.
5. **Parameter-space overlap.** Report local all-pair, adjacent-pair, and gap-at-least-18 overlap plus odd/even consensus overlap against matched Haar; no pair subset may rescue the registered broad result.
6. **Local versus shared retention.** Report $e_{shared}/e_{local}$ when $e_{local}>0$; do not impose a post-hoc threshold or call the ratio functional efficiency.
7. **Shared F2--F8 projectors.** Report per-band capture and overlap against rank-256 Haar controls. No subset of passing bands rescues a failed broad-middle verdict.
8. **Coarse covariance.** Run the identical frozen analysis after the primary verdict. Agreement strengthens target-common description; disagreement narrows the claim to conditional-fine.
9. **Middle-depth and block 36.** Display all layers. Neither can enter early/late medians or select a new window.
10. **Numerical conservation.** Sum of F1--F16 mass must reconstruct $\operatorname{tr}(B)$ with relative error below $10^{-5}$; exact-direction and band sums must agree within the same threshold.

## 12. Known Good / Known Bad / Known Confusing Cases

| Synthetic or observed case | Required reading |
| --- | --- |
| multiply every F2--F8 absolute value and total variance by 2, leaving normalized shares unchanged | $D_M=|g_M|=\log2$, $D_{shape}=0$: normalization/scale artifact |
| move equal mass from F2 to F8 while holding broad F2--F8 share constant | $D_{shape}>0$ and $W_M>0$: internal-cancellation artifact |
| identical early/late F2--F8 curves with layer-specific orthogonal semantic directions | $D_M=0$, local can beat Haar, shared remains Haar-like: rank-averaging artifact |
| one common middle subspace contains the same semantic covariance at every layer | shared middle beats Haar in both blocks: direction guard known-good |
| both local and shared middle match Haar | stable rank occupancy is spectrally nonspecific; use `haar_like_middle` |
| block 36 alone changes strongly | terminal boundary only; no registered depth verdict |
| smooth overlay looks flat while exact band metrics fail | visual artifact; unsmoothed metrics control |
| shared middle beats Haar but $D_M$ exceeds the margin | stable orientation does not rescue absolute/internal instability |
| $D_M$ is equivalent but shared comparison is unresolved | Insufficient, not true stability |

The third row is the registered **minimal counterexample**: even perfect agreement of every reported rank value does not imply stable direction identity.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / how | Why | Expected output | Pass / stop | Artifact and handoff |
| --- | --- | --- | --- | --- | --- | --- |
| 0. immutable-source audit | prove the intended model, bank, bases, and definitions are fixed | verify all named manifests, hashes, shapes, record order, bands, layer windows, and Protocol revision | prevents a different input from masquerading as mechanism | input/protocol manifest | stop on any mismatch | `provenance/input_manifest.json`; only a passing manifest reaches Stage 1 |
| 1. raw-$\Delta n$ replay | materialize the common-coordinate representation needed for shared projections | one same-run repeated replay of frozen Qwen3-8B and all 512 records; apply Section 5.4 guards | old response coordinates cannot support cross-layer projection | 36 raw tensors plus replay diagnostics | stop on any mandatory replay failure | worker-only tensors; `provenance/replay_guards.json` reaches Stage 2 |
| 2. local curve audit | construct exact absolute and normalized local-rank evidence | compute $B_{\ell,F}$, $b_{\ell i}$, F1--F16 masses, $D_M$, decomposition, and conservation | separates scale and internal aggregation before orientation is viewed | exact/band tables and provisional primary metric | stop on covariance, positivity, or conservation failure | `tables/local_middle_curves.csv`; frozen values reach Stage 3 |
| 3. shared/random construction | test cross-layer direction identity | build odd/even shared middle, local/consensus overlap metrics, 512 independent Haar overlap pairs, and 512 matched global Haar partitions without activations/labels | separates stable parameter orientation and semantic capture from rank averaging | projectors, overlap nulls, local/shared/Haar captures | stop on numerical or fold-leakage failure | `tables/orientation_capture.csv`; reaches smoke/full analysis |
| 4. engineering smoke | verify algorithms without producing eligible science | synthetic cases in Section 12 plus a fixed small shape-only subset | catches sign, fold, normalization, and random-control errors | unit-test and schema report | any failed known-case behavior stops | smoke artifacts remain worker-only and cannot enter result records |
| 5. full frozen analysis | assign one registered verdict | all 512 records, blocks 1--36, frozen seeds, metric, margin, and precedence | answers the one Anchor question | bootstrap tables, random null, typed verdict | no post-result scientific repair; amendment required | `provenance/verdict.json` reaches Stage 6 |
| 6. figure and record audit | preserve auditable evidence lineage | render the registered figure, open at original resolution, write Summary/Detailed only after human closed-book judgment | prevents visualization or prose from strengthening the result | central figure and result records | stop delivery if figure contract or lineage fails | curated artifacts in this directory |

Passing a smoke proves only implementation properties. It does not authorize or predict a scientific outcome, and it does not authorize a full run.

## 14. Algorithm, Outputs, And Provenance Contract

### 14.1 Frozen minimal algorithm

```text
verify immutable inputs and Protocol revision
replay the same 512 records twice in one run and materialize raw delta-n
verify hook identity, reconstruction, positivity, and full-spectrum conservation
form balanced conditional-fine class-center matrices
compute every local directional variance and fixed F1--F16 curve
compute D_M, g_M, D_shape, normalized shares, and within-middle transport
build odd/even cross-fitted shared middle and shared F2--F8 parameter spaces
build 512 independent Haar overlap pairs and 512 matched global Haar 16-band partitions
compute local/consensus parameter overlap, paired uncertainty, and semantic orientation controls
apply typed verdict precedence once
render and audit the central figure
```

### 14.2 Proposed worker and curated roots

- proposed worker implementation, not created or authorized: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_12_e01_middle_band_stability_decomposition/`;
- raw tensors, projectors, full random draws, logs, and machine tables remain on the worker surface;
- canonical curated result root, after an approved run: this Protocol directory.

Required future curated artifacts are:

- `provenance/input_manifest.json`;
- `provenance/replay_guards.json`;
- `provenance/numerical_guards.json`;
- `provenance/verdict.json`;
- `tables/local_middle_curves.csv`;
- `tables/middle_decomposition.csv`;
- `tables/orientation_capture.csv`;
- `tables/random_null_summary.csv`;
- `figures/figure0_middle_stability_decomposition.png`;
- `summary.md` and `detailed.md`.

Every artifact receives byte size and SHA-256 in one manifest. Every verdict field must trace raw tensor and basis identities to a table row, registered rule, observed value, typed outcome, and bounded claim.

### 14.3 Central figure contract

One four-panel figure is registered:

1. **Absolute spectrum:** exact per-direction conditional-fine variance for every selected layer on shared axes, with F2--F8 shaded and seven unsmoothed band means visible.
2. **Normalized middle:** full-spectrum normalized F1--F16 shares plus the F2--F8 within-middle distribution; early, middle-depth, late, and block 36 remain distinguishable.
3. **Scale-versus-shape decomposition:** $D_M$, $g_M$, $D_{shape}$, total growth, and $W_M$ with uncertainty and the confirmed equivalence margin.
4. **Direction identity:** early/late local and shared middle enrichment against matched Haar intervals, with odd/even and template-half markers.

The fourth panel must also show local-pair and odd/even-consensus parameter overlap normalized by the matched Haar expectation; parameter overlap and semantic capture must remain visually distinct.

Axes state squared-activation variance per direction, normalized share, log fold-change, and random-normalized capture as appropriate. The allowed conclusion is only which stability/artifact pattern holds on $S_0$. No panel may imply information content, MLP use, expert utility, or Router benefit.

## 15. Success / Failure / Insufficient Evidence

Verdict precedence is: validity `Insufficient` first; premise-not-reproduced second; then true stability or a typed artifact outcome. One outcome is assigned before secondary coarse/per-band diagnostics are viewed.

### Pass -- `TRUE_MIDDLE_STABILITY`

All conditions must hold:

1. all immutable-input, replay, covariance, numerical, fold-exclusion, and conservation guards pass;
2. the apparent-stability premise holds: full-bank $N_M<N_H$ and $N_M<N_T$, and middle is not the largest normalized-share change in either template half;
3. the full-bank 95% upper bound of $D_M$ is at most the researcher-confirmed $\delta_M$, and both template-half point estimates are at most the margin;
4. $O_{local,M}$ and odd/even $O_{shared,M}$ both exceed their matched independent-Haar q95 controls;
5. local F2--F8 semantic capture exceeds the matched Haar q95 in both early and late blocks;
6. cross-fitted shared F2--F8 semantic capture exceeds the matched Haar q95 in both early and late blocks;
7. shared-minus-Haar point effects are positive in odd and even evaluated groups and both template halves;
8. no result-selected subset, smoothing, alternate semantic object, layer window, or band definition is used.

Pass retains a stable geometry for one later information-identity decision. It does not authorize a probe, MLP intervention, expert-compatibility test, or Router experiment.

### Fail -- `APPARENT_STABILITY_NOT_REPRODUCED`

All validity guards pass, but the fixed full-bank and template-half normalized-share check does not reproduce the claim that middle is least-changing. The route stops at the premise; no artifact subtype is promoted from a failed visual observation.

### Fail -- `AGGREGATION_ARTIFACT`

The apparent-stability premise holds and the 95% lower bound of $D_M$ is above the confirmed margin. Report $g_M$, $D_{shape}$, $g_{all}$, and $W_M$ exactly. Use `scale-dominant` when $|g_M|>D_{shape}$, `shape-dominant` when $D_{shape}>|g_M|$, and `mixed-scale-shape` on equality or overlapping uncertainty. These labels describe the measured decomposition and do not prove causal dynamics.

This outcome applies whether or not shared middle beats Haar: stable orientation cannot convert an absolutely changing curve into true stability.

### Fail -- `RANK_AVERAGED_DIRECTION_INSTABILITY`

The apparent-stability premise holds and $D_M$ passes practical equivalence, but either local/consensus parameter overlap or cross-fitted shared semantic capture is at or below its matched Haar control while the corresponding local middle evidence is positive. The bounded subtype is `haar_like_middle` if neither local nor shared parameter/semantic evidence exceeds Haar despite curve equivalence.

### Fail -- `MIXED_ARTIFACT`

The apparent-stability premise holds, the lower bound of $D_M$ exceeds the margin, and shared middle also fails its Haar gate. Both aggregation and direction-instability evidence remain in the claim; one cannot erase the other.

### Insufficient

Use a typed `INSUFFICIENT_*` outcome if:

- any input, replay, covariance, parameter, numerical, or conservation guard fails;
- a required band value is nonpositive or non-finite;
- the $D_M$ interval overlaps the confirmed equivalence margin;
- template halves or odd/even folds make the apparent premise or shared-middle comparison unresolved rather than decisively positive or non-supporting;
- local middle and shared middle give an unregistered mixed Haar pattern;
- 512 Haar draws or 2,000 bootstraps are inadequate for their registered quantiles;
- the researcher has not confirmed the primary semantic object or practical margin.

Only provenance, precision, or a pre-unsealing Protocol amendment may repair an Insufficient outcome. A new function question requires a new Anchor.

## 16. What This Cannot Claim

No outcome can establish:

- what semantic facts or features F2--F8 contains;
- that middle information is absent from head, tail, or the old residual state;
- information-theoretic creation by attention;
- linear or nonlinear readability beyond the registered covariance;
- that the MLP transmits, suppresses, or uses middle variance;
- causal necessity for logits, loss, or downstream behavior;
- expert-update compatibility, expert differentiation, or functional specialization;
- that selecting middle improves a linear or nonlinear Router;
- that fixed middle-band dispatch should be reopened after A15_05/A15_05_05;
- generality beyond frozen Qwen3-8B, this English bank, these prompts, and this local parameter operator;
- any A15_04 shared-tail verdict.

The future objective of finding useful information and a better routing method remains a research direction, not a claim from this geometry audit.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Current evidence / review decision |
| --- | --- | --- |
| A. question and claim boundary | `CONFIRMED` | researcher explicitly requested an independent middle stability audit and excluded function, implementation, and execution |
| B. data construction and provenance | `PROPOSED` | confirm exact $S_0$ reuse and the A15_03-owned same-run raw-$\Delta n$ replay; old cache is diagnostic, not an exact oracle |
| C. diagnostic task and supervision | `PROPOSED` | confirm conditional-fine as primary, coarse as non-rescuing replication, and no learned readout |
| D. model and parameter spaces | `PROPOSED` | F2--F8 is researcher-fixed; confirm native $K$, odd/even cross-fitting, rank-1,792 shared middle, and matched orthogonal Haar partitions |
| E. precision and randomness | `PROPOSED` | confirm $\delta_M=\log(1.25)$, seeds, 512 Haar partitions, 2,000 bootstraps, and no post-unsealing tuning |
| F. comparison and verdict | `PROPOSED` | confirm $D_M$ as the one primary metric, direction identity as a guard, and Section 15 precedence |
| G. execution and reproducibility | `BLOCKED_NO_EXECUTION_APPROVAL` | implementation surface, resources, smoke, replay, full run, monitoring, and result-writing scopes are all unauthorized |

The candidate is internally aligned: the same $B_{\ell,F}$ enters absolute, normalized, local, shared, and Haar comparisons; $D_M$ answers scale/shape stability while the orientation gate answers direction identity; directions and layers are not treated as replicates; and the A15_04 tail decision remains isolated.

Promotion to `DESIGN_CONFIRMED_NOT_EXECUTABLE` requires explicit confirmation of B--G and a final cross-block consistency pass. Design confirmation would still authorize no execution.

After confirmation, any change to $S_0$, $\Delta n$, covariance role, parameter operator, F2--F8 definition, layer windows, fold assignment, $D_M$, $\delta_M$, Haar construction, resampling, exclusion rule, or typed verdict reopens the affected block. After any approved execution starts, such changes require an append-only amendment with before/after values and evidence-eligibility impact; the registered body must not be silently rewritten.
