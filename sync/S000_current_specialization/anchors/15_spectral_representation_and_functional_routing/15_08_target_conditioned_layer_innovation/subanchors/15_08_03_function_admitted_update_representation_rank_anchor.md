---
anchor_id: 15_08_03_function_admitted_update_representation_rank
status: COMPLETED_INSUFFICIENT_BASIS_SENSITIVE_HREP_FAIL
canonical_language: en
chinese_companion: 15_08_03_function_admitted_update_representation_rank_anchor_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on: 15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_AND_COMPLETED_FULL_ANALYSIS
created: 2026-08-16
updated: 2026-08-16
---

# A15_08_03 Cross-Layer Function-Admitted Update Parameter-Spectral Location And Representation Rank

Parent definition: [A15_08 Target-Conditioned Layer Innovation](../15_08_target_conditioned_layer_innovation_anchor.md). Functional prerequisite: [A15_08_02](15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md). Chinese companion: [Anchor](15_08_03_function_admitted_update_representation_rank_anchor_cn.md).

## 1. Problem Definition

This child Anchor asks one conditional question:

> How do preregistered layers differ in conditional-fine added accessibility, parameter-spectral energy location, within-parent residual-update rank, and token geometry; do deeper layers jointly show larger functional gain and later common-parameter-spectrum allocation, and which named layers carry that gain in a stable low-dimensional representation?

“Parameter-spectral location” is where the normalized variance energy of within-parent centered $R_U$ lies along MLP directions ordered from stronger to weaker parameter response; it does not define added information. “Representation rank” is the dimensional concentration of the update activation cloud itself, not the rank of an eight-class discriminant. “Stable” means a TRAIN-frozen subspace retains geometry on expression-disjoint DEVELOPMENT and CONFIRMATION without refitting. The deliverable is one complete cross-layer profile: A15_08_02 net gain, each layer's local-MLP dominant band, frozen common-parameter location, representation rank, and pairwise token-geometry CKA. Every eligible block's spectral and projected-gain curves are preregistered before confirmation access; task-related interpretation is restricted to function-admitted layers.

This is the smallest next decision because covariance/PCA can be meaningful only after the update object is exact, while a task-related low-rank claim additionally requires positive added accessibility. Router utility remains out of scope.

## 2. Physical Priors

1. **Local and common parameter spectra have distinct roles.** A local MLP spectrum locates an update relative to that layer's own response geometry; only a frozen common spectrum gives one cross-layer coordinate. Neither location substitutes for same-$X$ functional gain.
2. **Joint token variation exposes representation rank.** A low-dimensional update cloud has concentrated full-covariance eigenvalue energy and a TRAIN-frozen principal subspace that retains held-out variance; coordinatewise parameter-spectrum energy cannot answer this question.
3. **High variance is not automatically task relevant.** A PCA subspace supports a task-related interpretation only if it retains the admitted same-$X$ gain and beats equal-rank random subspaces.

## 3. Falsifiable Hypotheses

**H-DEPTH-SPEC — functional growth with common-parameter spectral right shift.** In a preregistered early-versus-deep trajectory comparison, deeper layers have larger $T_\ell$ and later normalized $R_U$ centroid in the same frozen Mean Response parameter basis. Both clauses must pass separately; movement of a local dominant band is descriptive support only.

**H-REP — stable low-rank update representation with functional retention.** At least one function-admitted layer has a within-parent residual-update spectrum concentrated far below the sample-identifiable rank, reproduces under a TRAIN-frozen PCA subspace on both held-out splits, and retains at least 80% of its full admitted conditional-fine gain beyond equal-rank Haar controls.

**Strongest rival R-GEO/NUIS — geometric redistribution or nuisance concentration.** A right shift may occur only in Mean Response without functional growth; local dominant bands may move because coordinates change by layer; apparent low rank may come from $n<d$, template/scale structure, or one-split covariance noise. The rival predicts no functional-and-spectral conjunction, opposite behavior in the second common basis, poor held-out compactness, or no PCA functional retention.

`REGISTERED`: adjudicate H-DEPTH-SPEC with preregistered early-versus-deep median contrasts; use Mean Response as the primary common coordinate and Rank Consensus only as a basis-sensitivity guard; keep the dominant band descriptive and the full-spectrum centroid primary. Define compactness by $r_{80}^{rep}/(n-P)\le0.10$, require at least 75% held-out variance retention on both splits, and require 80% functional retention plus an equal-rank Haar q95 guard. These definitions were approved and frozen before CONFIRMATION access on 2026-08-16.

All-layer spectra and clustering remain descriptive if A15_08_02 yields $\mathcal L^+=\varnothing$; no function-admitted low-rank verdict is then activated. The projected-gain analysis is nevertheless frozen and computed for all eligible layers so $\mathcal L^+$ is not used for post-confirmation method selection.

## 4. Mathematical Model

For sample $i$ with parent $p(i)$, let $R_{U,\ell,i}\in\mathbb R^d$ be the same-token residual update already frozen by A15_08_02. Remove only the parent-common mean learned from TRAIN:

$$
\widetilde R_{\ell,i}
=R_{U,\ell,i}-\mu^{tr}_{\ell,p(i)}.
$$

The layer-local MLP input-side response operator and its strong-to-weak spectrum are

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}
=B_\ell\Gamma_\ell B_\ell^\top.
$$

Split $B_\ell$ into sixteen equal-rank bands. The sum of projected variance in band $b$, $E^{local}_{\ell,b}$, defines local activation, and $\arg\max_bE^{local}_{\ell,b}$ is the dominant energy band. Local bands share relative rank only; their directions differ across layers.

The cross-layer coordinate is the frozen Mean Response basis $B^{MR}$ from eigendecomposing the equal-layer average of $K_\ell/\operatorname{tr}(K_\ell)$. The Rank Consensus basis $B^{RC}$ eigendecomposes a rank-weighted average of each layer's equal-rank local-band projectors; it retains ordinal cross-layer rank consensus while discarding response magnitude and is only a sensitivity control. For view $v\in\{local,MR,RC\}$, let $p^v_{\ell,j}$ be normalized direction energy and $\rho_j$ normalized rank. Its spectral centroid is

$$
C^v_\ell=\sum_jp^v_{\ell,j}\rho_j.
$$

`REGISTERED`: freeze early layers $\mathcal E$ and deep layers $\mathcal D$, then compute

$$
\Delta_T=\operatorname{median}_{\ell\in\mathcal D}T_\ell-
\operatorname{median}_{\ell\in\mathcal E}T_\ell,
\qquad
\Delta_C^{MR}=\operatorname{median}_{\ell\in\mathcal D}C^{MR}_\ell-
\operatorname{median}_{\ell\in\mathcal E}C^{MR}_\ell.
$$

$\Delta_T$ tests functional growth and $\Delta_C^{MR}$ tests right shift in that common parameter coordinate; neither can substitute for the other. Raw total projected energy is reported separately as update magnitude, not added information.

Stack TRAIN rows in $M_\ell^{tr}\in\mathbb R^{n\times d}$ and compute its SVD. Equivalently, eigendecompose the complete centered covariance

$$
C_\ell^{tr}
=\frac{1}{n-P}(M_\ell^{tr})^\top M_\ell^{tr}
=V_\ell\Lambda_\ell V_\ell^\top.
$$

With $p_{\ell,j}=\lambda_{\ell,j}/\sum_k\lambda_{\ell,k}$, representation effective rank and 80%-variance rank are

$$
r_{eff,\ell}^{rep}
=\exp\left(-\sum_jp_{\ell,j}\log p_{\ell,j}\right),
$$

$$
r_{80,\ell}^{rep}
=\min\left\{r:\sum_{j\le r}p_{\ell,j}\ge0.8\right\}.
$$

The TRAIN projector $P_{\ell,r}=V_{\ell,r}V_{\ell,r}^\top$ is frozen. Its held-out representation retention on split $s$ is

$$
V_{\ell,r}^{s}
=\frac{\operatorname{tr}(P_{\ell,r}C_\ell^{s})}
{\operatorname{tr}(C_\ell^{s})}.
$$

For every eligible layer, project $R_U$ with $P_{\ell,r}$, refit only the registered correction under TRAIN/DEVELOPMENT discipline, and compute gain $G_{\ell,r}^{PCA}$. Functional sufficiency is tested by

$$
D_{\ell,r}^{func}
=G_{\ell,r}^{PCA}-0.8G_{\ell,full},
$$

with paired held-out uncertainty and equal-rank Haar correction controls. This task-linked quantity cannot replace $r_{80}^{rep}$ as the representation-rank definition.

For basis-free token-geometry comparison, construct the parent-centered token Gram matrix $G_\ell=M_\ell M_\ell^\top$ on the same ordered samples and compute linear CKA:

$$
CKA(\ell,m)
=\frac{\langle HG_\ell H,HG_mH\rangle_F}
{\|HG_\ell H\|_F\,\|HG_mH\|_F},
$$

where $H$ centers token rows. CKA measures whether two layers induce similar token-to-token update geometry without requiring a public parameter basis or one-to-one PC alignment. It does not measure rank or functional gain.

## 5. Computational Realization

1. Reuse A15_08_02's exact record order, split manifests, token site, and $R_{U,\ell}$ tensors. Both Protocols must freeze before confirmation and share one model forward; A15_08_03 cannot be added only after seeing A15_08_02's positive layers.
2. Inside each layer and split, subtract TRAIN parent means; do not subtract child means because child differences are part of the conditional-fine object.
3. Compute SVD in sample space to avoid materializing a dense $4096\times4096$ matrix. The identifiable rank cap is $n-P$, not 4096; every reported rank is also normalized by that cap.
4. Freeze PCA directions and candidate ranks from TRAIN. DEVELOPMENT and CONFIRMATION only project and report retention; they never rotate or reorder directions.
5. `REGISTERED`: compare $r_{80}^{rep}$ with 512 independent-coordinate row-shuffle nulls that preserve each coordinate's marginal distribution but destroy cross-coordinate token co-variation.
6. On the same within-parent centered $R_U$, compute each layer's sixteen local-$K_\ell$ band energies, dominant band, and centroid; then compute full energy spectra and centroids in frozen Mean Response and Rank Consensus common bases. No semantic label or CONFIRMATION record selects a parameter basis.
7. Plot all-layer $T_\ell$, local location, both common-basis locations, normalized $r_{eff}^{rep}$, $r_{80}^{rep}$, held-out variance retention, and linear CKA. Only $T_\ell$ defines added accessibility; the other panels are parameter or token geometry.
8. For every eligible layer, evaluate $r\in\{1,2,4,8,16,32,64,128,256,512\}$ up to the identifiable cap, report the smallest rank passing 80% functional retention, and compare every rank with equal-rank Haar. Only the joint intersection with $\mathcal L^+$ receives task-related interpretation.
9. As a secondary token-level analysis, fit parent-specific $k=8$ k-means on TRAIN PCA coordinates at $r_{80}^{rep}$, transfer centers unchanged to held-out splits, and report resampling stability plus child-label ARI/NMI against equal-rank Haar and within-parent label permutations. Clustering cannot alter H-REP.

## 6. Minimal Falsification Tests

For H-DEPTH-SPEC, the decisive comparison requires the simultaneous 95% lower bounds of both $\Delta_T$ and $\Delta_C^{MR}$ to exceed zero. If Rank Consensus does not pass the same positive criterion, the result is `BASIS_SENSITIVE`, not a basis-invariant right-shift claim; the local dominant band cannot create a Pass.

For H-REP, the decisive comparison is the preregistered conjunction, on at least one layer, of A15_08_02 positive added accessibility, representation compactness, frozen held-out geometry, and functional retention. Every layer, band, and rank enters the rule before confirmation is opened.

`REGISTERED` **Pass — `STABLE_FUNCTION_RETAINING_LOW_RANK_UPDATE`:** $r_{80}^{rep}/(n-P)\le0.10$; the real $r_{80}^{rep}$ is below the coordinate-shuffle q05; the TRAIN projector retains at least 75% variance on DEVELOPMENT and CONFIRMATION; and some registered $r$ has a positive paired 95% lower bound for $D_{\ell,r}^{func}$ while exceeding equal-rank Haar q95.

H-DEPTH-SPEC reports `FUNCTION_ONLY`, `SPECTRAL_SHIFT_ONLY`, `BOTH`, or `NEITHER`; only `BOTH` supports the original joint hypothesis. H-REP **Fail — `REPRESENTATION_OR_FUNCTION_NOT_LOW_RANK`:** valid function-positive layers exist, but every such layer decisively fails compactness, held-out geometry, or 80% functional retention. Fail must name the failed conjunct.

**Insufficient:** no function-positive layer exists; covariance trace is negligible; finite-sample or split guards fail; a decisive interval crosses zero; PCA directions or ranks leak held-out truth; or required arrays/provenance are missing.

Cluster instability cannot produce H-REP Fail, and stable clustering cannot rescue failed representation or functional sufficiency.

## 7. Current Evidence

1. The 0813 meeting established the method chain “same-token change → centered covariance → PCA → token clustering” because the earlier coordinatewise variance analysis lost token pairing and cross-direction co-variation. It also explicitly limited PCA to geometric compression rather than evidence of new task information; this boundary is recorded in the [merged meeting record](/daily_research_reports/backup/2026/08/0813/meeting_notes/0813_meeting_merged_clean_record_cn.md).
2. [A15_02_05](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) did not find stable fine-specific local-rank relocation. It did not compute the present within-parent $R_U$ covariance or held-out PCA retention.
3. [A15_08_E04](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md) found that two registered target directions retained only 33.24% of one local full gain. This rules out assuming rank two, but it was a task-retrieval result on another target, not a representation-rank measurement.
4. Prior Attention-write evidence showed a basis-conditioned shift in Mean Response that Rank Consensus did not reproduce, with non-monotonic adjacent-layer changes. This requires a common-basis sensitivity guard and cannot be inherited as an $R_U$ result; see the [0813 meeting update](/daily_research_reports/backup/2026/08/0813/focus_meeting_common_basis_attention_write.md).
5. [A15_08_03_E01](/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_03_E01_function_admitted_update_spectral_rank_analysis/summary.md) completed under the frozen Protocol on 2026-08-16. A15_08_02 admitted $\mathcal L^+=\{24,28\}$. The early 2--12 versus deep 25--35 functional contrast is $\Delta_T=-0.0046$ with a simultaneous interval crossing zero. Mean Response gives positive $\Delta_C=0.0285$, while Rank Consensus gives negative $\Delta_C=-0.0397$; the joint outcome is `INSUFFICIENT_BASIS_SENSITIVE`.
6. No layer passes the four-way stable-representation-low-rank conjunction. Blocks 24/28 have $r_{80}=149/106$, while their TRAIN spaces retain only 42.1%/54.6% confirmation variance. Both pass functional retention first at registered rank 256. This establishes compression to 256 dimensions, not a stable globally low-rank update cloud.
7. Complete 35-by-35 CKA and clustering analyses are archived as secondary geometry. The with-replacement CKA percentile intervals carry a calibration warning because duplicated token rows raise high-dimensional Gram similarity; they are not used to infer layer breakpoints. Blocks 24/28 clustering ARI also does not beat equal-rank Haar q95.

## 8. Claim Boundary And Next Decision

H-DEPTH-SPEC `BOTH` can show only that, for this model, object, task, depth contrast, and frozen common parameter coordinate, conditional-fine net gain increases while normalized parameter-spectral location moves later. H-REP Pass can show only that a named function-admitted layer's residual-update cloud is compact and a small PCA subspace retains most registered gain on unseen expressions. CKA may describe shared token geometry; clustering may describe stable child enrichment.

It cannot call spectral relocation alone increased new information, treat equal local rank as cross-layer direction identity, show that PCA directions are model-native features, establish population-intrinsic rank $r$, identify clusters as experts, or establish routing utility. It cannot convert geometry-only layers outside $\mathcal L^+$ into task-related new information.

**Exactly one next decision:** whether the TRAIN-frozen rank-256 functional-retention spaces at blocks 24 and 28 should enter a separately frozen causal-intervention or Router-utility test. The current experiment cannot establish native use or dispatch benefit and does not authorize that follow-up.

**Completion criterion: satisfied.** The two Anchor languages and canonical Protocol are synchronized; parameter bases, bands, depth windows, data, nulls, ranks, uncertainty, artifacts, and A15_08_02 tensor reuse all have archived receipts.

**Resume action:** no rerun is required. Later citations must keep four claims separate: function-admitted layers are 24 and 28; common-spectral relocation is basis-sensitive; stable representation low rank failed; functional compression passed first at registered rank 256.
