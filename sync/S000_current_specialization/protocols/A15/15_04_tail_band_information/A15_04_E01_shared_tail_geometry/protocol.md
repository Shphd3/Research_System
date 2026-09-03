---
experiment_id: A15_04_E01_shared_tail_geometry
legacy_experiment_id: A15_01_11_E01_shared_tail_geometry
anchor_id: 15_04_tail_band_information
legacy_anchor_id: 15_01_11_shared_tail_semantic_relocation
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
canonical_language: en
companion_language: zh
created: 2026-08-09
revised: 2026-08-09
---

# Protocol: Does Late Semantic Variance Enter The Shared F9--F16 Parameter Tail?

Chinese review companion: [protocol_cn.md](protocol_cn.md). Primary source: [A15_04 Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md).

## 0. Approval Snapshot

- **Document state:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN`.
- **Registered revision:** `A15_04_E01_r1`, frozen at `2026-08-09T14:05:43Z` before implementation or result access.
- **Researcher-confirmed spectral partition:** 16 consecutive equal-rank bands of 256 directions; F1=head, F2--F8=middle, F9--F16=tail. Every band and the three broad regions must be reported.
- **Researcher-confirmed scope:** one geometry-only test on the frozen A15_02_06 set. No activation deletion, task loss, downstream benchmark, Router, or functional claim.
- **Researcher-confirmed primary semantic object:** conditional-fine covariance is the only primary semantic object; coarse or complex-minus-simple statistics cannot enter or rescue the verdict.
- **Decision question:** does conditional-fine variance in the actual attention-induced MLP-input increment become more enriched from early to late layers in the global cross-layer shared broad F9--F16 tail than in dimension-matched random geometry, F1 head, and F2--F8 middle?
- **Treatment:** the global cross-layer shared broad tail constructed only from the opposite odd/even layer group.
- **Controls:** matched random 16-band partitions, shared broad head and middle, every shared F1--F16 band, and each layer's local spectrum.
- **Mandatory stage diagnostics:** early-internal, late-internal, early-built-on-late, and late-built-on-early shared geometry for every band and H/M/T. These diagnose global stability, late formation, or stage redirection and never replace the global primary verdict.
- **Held fixed:** frozen Qwen3-8B, 512 records, $\Delta n$, conditional-fine covariance, layers 1--35 for decisions, block 36 as descriptive, and sealed expression halves.
- **Primary statistic:** $D_T=T_T-\max(T_H,T_M)$, where each $T_G$ is the global late-minus-early change in capture divided by that region's random expected dimension fraction.
- **Pass:** the original local right shift remains; broad-tail enrichment is positive, exceeds its matched random interval, and exceeds head/middle with a positive 95% lower bound; layer groups and expression halves do not reverse sign.
- **Fail:** the local shift remains but broad tail is explained by dimension-matched random, is not greater than head/middle, or only local ranks relocate.
- **Insufficient:** raw-$\Delta n$ replay, local phenomenon, shared-tail estimate, or grouped reliability is unstable.
- **Critical provenance repair:** old artifacts retain $\Delta n$ only in a layer-local eigencoordinate. One deterministic replay of the unchanged 512 records is approved to materialize raw 4096-dimensional $\Delta n$ before any cross-layer projection.
- **Block state:** A--G `CONFIRMED` by the researcher's 2026-08-09 instruction to use conditional-fine only, require all four shared-geometry scopes, preserve the global verdict, and complete the experiment directly.
- **Cross-block audit:** `PASS`.
- **Execution scope approved:** implementation, deterministic replay, engineering smoke, one full registered analysis, curated result records, Anchor result update, and today's focus update. Publication, sync, commit, and push remain unauthorized.

## 1. Terminology And Concrete Objects

| Term | Plain meaning | Frozen computation | Cannot establish |
| --- | --- | --- | --- |
| fixed set $S_0$ | texts selected before this result and never replaced afterward | A15_02_06's balanced 512 records | population-wide behavior |
| $\Delta n_\ell$ | the current attention write's change to the input actually consumed by layer $\ell$'s MLP | $RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)$ | information-theoretically pure new information |
| conditional-fine covariance $B_{\ell,F}$ | variance among child centers after removing each parent mean | equal weight over 8 parents and 8 children | coarse/fine task difficulty or nonlinear readability |
| F1--F16 | one layer's MLP-input eigenvectors sorted by gain and split into 16 consecutive groups | 256 directions per band | the same direction identity across layers |
| head / middle / tail | broad parameter regions fixed by the researcher | F1 / F2--F8 / F9--F16 | functional modules |
| local spectrum | variance projected into a layer's own mutually orthogonal F1--F16 bands | absolute variance per direction and normalized shares summing to 1 | cross-layer common orientation |
| shared band/region | the orientation most consistently present in the same parameter ranks of other layers | leading eigenspace of an average of opposite-group local projectors | MLP use |
| capture $c$ | fraction of total fine between-class variance in a tested space | $\operatorname{tr}(QB)/\operatorname{tr}(B)$ | accuracy or causality |
| dimension-normalized enrichment $e$ | capture relative to what a random space of the same dimension captures on average | $e=c/(r/4096)$; random expectation 1 | population significance |
| random spectral partition | one random orthogonal basis split into 16 bands, then aggregated with the same H/M/T rule | same random partition applied to every layer in one draw | a random neural mechanism |
| mutually exclusive layer groups | one group constructs spaces and the other is measured, then roles reverse | odd versus even blocks among 1--35 | independent model replications |
| global shared geometry | one cross-layer orientation fitted across blocks 1--35 without using the evaluated layer | opposite odd/even group | stage-specific formation history |
| early / late internal geometry | consistency estimated separately inside blocks 1--12 or 25--35 | opposite odd/even group inside the same stage | a globally reusable orientation |
| bidirectional stage transfer | an early-built space measured only on late covariance and a late-built space measured only on early covariance | $E\rightarrow L$ and $L\rightarrow E$ | function or causal transmission |

“Middle” means parameter bands F2--F8. “Middle depth” means blocks 13--24 and is not a parameter band.

## 2. Anchor Alignment

- **Anchor uncertainty:** whether target-common local rank relocation aligns with a genuinely cross-layer shared broad low-gain geometry.
- **Representation:** raw actual $\Delta n$, not the raw post-`o_proj` write.
- **Semantic object:** researcher-confirmed conditional-fine covariance only; coarse and complex-minus-simple objects do not enter the verdict or stage labels.
- **Complete spectral evidence:** local absolute variance, local normalized share, and shared-band enrichment for F1--F16 at every layer.
- **Decision evidence:** broad H/M/T capture and dimension-normalized enrichment.
- **Primary proposed metric:** $D_T$; the mandatory random guard tests $T_T$ against matched random partitions.
- **Main falsifier:** broad tail loses its advantage after dimension correction or has no orientation-specific advantage beyond random/head/middle.
- **Claim boundary:** static frozen-set geometry only.

## 3. Tested Hypotheses

### G0 — local-spectrum phenomenon gate

The complete local F1--F16 conditional-fine spectrum of $\Delta n$ retains a positive early-to-late rank-centroid shift, with the same sign in design and confirmation templates.

### G1 — broad shared-tail geometry

After dividing broad-region capture by its matched random dimension fraction, F9--F16 tail enrichment increases more from early to late layers than F1 head and F2--F8 middle, and more than the matched random-partition null.

### Strongest rival

Tail's apparent advantage arises from its 2,048 dimensions, from generic shared geometry, or from local rank redistribution with no common orientation. Under this rival, the broad tail will not show a tail-specific dimension-normalized depth increase.

F1--F16 bandwise values localize the effect but are not separate primary hypotheses. No band can be selected after the result to rescue G1.

## 4. Rival Explanations Separated By The Design

1. **Dimension artifact:** raw tail capture is large because tail contains half of all directions.
2. **Random-projection retention:** any matched random broad space preserves similar finite-set structure.
3. **Local-only relocation:** local F1--F16 mass shifts, but shared orientations add nothing.
4. **Generic shared geometry:** head or middle enrichment changes as much as tail.
5. **Coordinate error:** old local coordinates are combined with a nonidentical basis.
6. **Terminal anomaly:** block 36 creates the visual trend.
7. **Grouped instability:** a small number of parents or templates controls the sign.

## 5. Data Construction And Provenance

### 5.1 Frozen semantic set

- 8 parents × 8 children × 4 label-free templates × 2 fact bundles = 512 records;
- design: templates 1--2; confirmation: templates 3--4;
- dataset manifest identifier `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`;
- dataset file SHA-256 `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1`.

No prompt, label, tokenizer, readout position, record order, or split may change.

### 5.2 Frozen sources

- parameter run `a15-01-09-e01-p-20260807T061000Z`, manifest SHA-256 `2fd84effc280e7090fe33a99e44446df083f2556de592c3fa8ee4faa0b99bf59`, 36/36 bases;
- response run `a15-01-09-e01-r-20260807T061000Z`, manifest SHA-256 `f7c74a1e495f6fed13d852b403693abde15b2ba9dce63b5f264c2d645bb5a72a`, 36/36 layers and 512/512 records;
- frozen A15_02 post-`o_proj` attention-write cache for replay identity.

The old response files store `delta_projection` in a separately recomputed local eigenbasis whose vectors were not saved. They can validate local spectra but must not construct cross-layer projections.

### 5.3 Proposed deterministic raw-$\Delta n$ replay

Replay the unchanged model and $S_0$ once; save raw bfloat16 $\Delta n_\ell\in\mathbb R^{512\times4096}$ for all 36 layers. Mandatory stop guards:

1. exact dataset hashes and record order;
2. 36/36 layers and 512/512 finite vectors;
3. replayed $a_\ell$ has maximum absolute difference 0 from the frozen cache;
4. full-basis projection conserves energy within relative $10^{-4}$;
5. all 16 local-band raw fine values reproduce the old response analysis: centroid absolute difference at most $5\times10^{-4}$ and total between-class trace relative difference at most $10^{-3}$.

Any failure yields `INSUFFICIENT_INPUT_REPLAY` and stops the experiment.

### 5.4 Conditional-fine covariance

For increment $z_{pcet}^{(\ell)}$ with parent $p$, child $c$, template $e$, and fact bundle $t$:

$$
\mu_{pc}^{(\ell)}=\frac{1}{8}\sum_{e,t}z_{pcet}^{(\ell)},\qquad
\mu_p^{(\ell)}=\frac{1}{8}\sum_c\mu_{pc}^{(\ell)},
$$

$$
B_{\ell,F}=\frac{1}{64}\sum_{p,c}
(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})(\mu_{pc}^{(\ell)}-\mu_p^{(\ell)})^{\top}.
$$

Every parent and child is equally weighted. Trace computations use the centered class-mean matrix rather than an explicitly materialized noisy covariance.

## 6. Diagnostic Task

There is no learned probe or model optimization. The analysis:

1. reconstructs the complete local F1--F16 semantic spectrum;
2. builds every shared F1--F16 space and the three broad shared H/M/T spaces from parameters only;
3. measures the same $B_{\ell,F}$ in all actual and random spaces;
4. separates broad tail-specific enrichment from dimension, random, generic-shared, and local-only rivals.

Labels only form balanced class centers. Absolute readability, nonlinear decoding, and task behavior are outside scope.

## 7. Model, Bands, And Shared-Space Construction

### 7.1 Frozen coordinate

- model `/data/share/Qwen3-8B`, frozen;
- 36 blocks, hidden dimension $d=4096$;
- native post-RMSNorm MLP-input operator $K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}$;
- `down_proj` excluded;
- no RMSNorm-folded variant because $\Delta n$ is already in the native MLP-input coordinate.

### 7.2 Fixed spectral partition

Let $P_{\ell,k}$ project onto sorted ranks $256(k-1)+1$ through $256k$.

$$
P_{\ell,H}=P_{\ell,1},\qquad
P_{\ell,M}=\sum_{k=2}^{8}P_{\ell,k},\qquad
P_{\ell,T}=\sum_{k=9}^{16}P_{\ell,k}.
$$

The corresponding dimensions are $r_H=256$, $r_M=1792$, and $r_T=2048$.

### 7.3 Cross-layer separation

Block 36 is excluded from construction and decisions. Among blocks 1--35:

- group A: odd blocks $\{1,3,\ldots,35\}$;
- group B: even blocks $\{2,4,\ldots,34\}$.

For an evaluated layer in group $f$, use only $-f$:

$$
Q_k^{(-f)}=\operatorname{TopEig}_{256}\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,k}\right),
$$

$$
Q_G^{(-f)}=\operatorname{TopEig}_{r_G}\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,G}\right).
$$

Broad $Q_G$ is constructed directly. Independently constructed $Q_k$ spaces may overlap and therefore must not be summed to obtain broad capture.

### 7.4 Stage-resolved shared geometry

Let $E=\{1,\ldots,12\}$ and $L=\{25,\ldots,35\}$. Four diagnostic scopes are mandatory:

1. **early-internal:** construct from the opposite odd/even subset inside $E$ and evaluate the held-out early layers;
2. **late-internal:** construct from the opposite odd/even subset inside $L$ and evaluate the held-out late layers;
3. **early-to-late:** construct $Q_{G,E}$ from all early parameter projectors and evaluate only late conditional-fine covariances;
4. **late-to-early:** construct $Q_{G,L}$ from all late parameter projectors and evaluate only early conditional-fine covariances.

Apply the same construction to all F1--F16 bands and direct broad H/M/T spaces. Report parameter-only cross-stage overlap

$$
O_{EL,G}=\frac{\operatorname{tr}(Q_{G,E}Q_{G,L})}{r_G}.
$$

Global odd/even $Q_G^{(-f)}$ remains the only primary construction. Stage-resolved spaces cannot enter $T_G$, $D_T$, Pass, Fail, or Insufficient except when a numerical construction failure makes required evidence missing.

### 7.5 Projector guards

Every projector requires normalized orthogonality error and eigensolver residual at most $10^{-5}$. The two broad-tail consensus projectors must overlap more than the q95 overlap of 512 matched pairs of random rank-2048 spaces. Report the same stability statistic for all F1--F16 and broad H/M/T; low non-tail commonality is descriptive, while numerical invalidity is a stop condition.

## 8. Objective, Precision, And Randomness

- No training objective, optimizer, checkpoint selection, or result-tuned parameter exists.
- Model replay uses the frozen bfloat16 path.
- Projection construction and multiplication use FP32 with numerical guards; class means, traces, aggregation, and intervals use FP64.
- projector-overlap null seed: `151100`;
- semantic random-partition seed: `151101`;
- grouped bootstrap seed: `151102`;
- proposed null size: 512 Haar orthogonal 16-band partitions;
- proposed uncertainty size: 2,000 paired grouped bootstrap replicates.

Each Haar draw produces one 4096-dimensional orthogonal basis, split into 16 consecutive 256-dimensional random bands. Its F1, F2--F8, and F9--F16 unions give the matched H/M/T nulls. The same partition is applied to all layers and both expression halves within the draw.

## 9. Frozen Conditions And Evidence Outputs

| Role | Frozen value |
| --- | --- |
| representation | raw actual $\Delta n_\ell$ |
| semantics | conditional-fine $B_{\ell,F}$ |
| local bands | F1--F16, 256 directions each |
| broad regions | H=F1; M=F2--F8; T=F9--F16 |
| early / late | blocks 1--12 / 25--35 |
| middle-depth display | blocks 13--24 |
| terminal boundary | block 36, descriptive only |
| construction/evaluation split | odd/even blocks among 1--35 |
| stage-resolved construction | odd/even within early and late; all-early applied only to late; all-late applied only to early |
| random control | one shared Haar 16-band partition per draw |
| wording reliability | templates 1--2 versus 3--4 |

No adaptive band regrouping, selected tail sub-band, alternate layer window, coarse/fine rescue, or post-result smoothing may change the verdict.

## 10. Primary Metric And Frozen Analysis

### 10.1 Complete local spectrum

For every layer and $k=1,\ldots,16$, report

$$
v_{\ell,k}^{local}=\frac{\operatorname{tr}(P_{\ell,k}B_{\ell,F})}{256},
\qquad
p_{\ell,k}^{local}=\frac{\operatorname{tr}(P_{\ell,k}B_{\ell,F})}{\operatorname{tr}(B_{\ell,F})}.
$$

$v$ is absolute between-class variance per direction in activation-squared units; $p$ is a normalized share and sums to 1 across F1--F16. Both are mandatory.

### 10.2 Complete shared-band data

For every layer and shared rank-256 band,

$$
c_{\ell,k}^{shared}=\frac{\operatorname{tr}(Q_kB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,k}^{shared}=16c_{\ell,k}^{shared}.
$$

Because independently constructed shared bands need not be orthogonal, the 16 $c^{shared}$ values are not called shares and need not sum to 1.

### 10.3 Broad H/M/T data and primary statistic

For $G\in\{H,M,T\}$,

$$
c_{\ell,G}=\frac{\operatorname{tr}(Q_GB_{\ell,F})}{\operatorname{tr}(B_{\ell,F})},
\qquad
e_{\ell,G}=\frac{c_{\ell,G}}{r_G/4096}.
$$

Report both raw capture $c$ and enrichment $e$. Only $e$ is fair for comparing H/M/T. The three broad shared spaces are fitted independently, so their raw captures need not sum to 1; only the local H/M/T partition has that conservation property.

$$
T_G=\operatorname{median}_{\ell=25:35}e_{\ell,G}
-\operatorname{median}_{\ell=1:12}e_{\ell,G},
$$

$$
D_T=T_T-\max(T_H,T_M).
$$

$D_T$ is the proposed primary statistic. Its unit is random-normalized enrichment difference. It asks whether tail's depth change exceeds both other broad regions; it cannot prove function.

For random partition $q$, compute $T_{R,T}^{(q)}$ and late-tail enrichment $L_{R,T}^{(q)}$ using its F9--F16 union. Compare the actual $T_T$ and $L_T$ with their q95 nulls.

### 10.4 G0 and local broad-region bridge

Use the frozen 16-band centroid

$$
C_{\ell,F}=\sum_{k=1}^{16}p_{\ell,k}^{local}\frac{k-0.5}{16}
$$

and its late-minus-early contrast $T_{rank}$. Also compute the local H/M/T shares and the local broad-tail enrichment change $T_{LT}$ using $P_{\ell,T}$.

### 10.5 Uncertainty and multiplicity

Use 2,000 paired replicates: resample eight parents with replacement and four template clusters with replacement; a selected template retains both fact bundles and all children. Apply each replicate to every layer and space. Do not resample directions or layers as independent units.

Report percentile 95% intervals for $T_T$, $D_T$, and broad controls. Per-band intervals and F1--F16 curves are localization diagnostics only; no individual-band significance claim or multiple-testing rescue is allowed.

### 10.6 Frozen analysis order

1. input and replay guards;
2. complete local F1--F16 tables and G0;
3. shared-space numerical and stability guards;
4. complete shared F1--F16 tables without selecting a band;
5. broad H/M/T $c$, $e$, $T_G$, and $D_T$;
6. matched random-partition comparison;
7. odd/even and expression-half signs;
8. assign the one global typed verdict;
9. only after the global verdict is frozen, read early-internal, late-internal, bidirectional transfer, and cross-stage overlap and assign one non-primary stage label.

## 11. Secondary Metrics And Guards

1. Parameter-only availability $a_{\ell,G}=\operatorname{tr}(Q_GP_{\ell,G})/r_G$ and bandwise $a_{\ell,k}$.
2. Local H/M/T raw shares, per-direction variances, and enrichment changes.
3. Separate design/confirmation $T_{rank}$, $T_T$, and $D_T$.
4. Separate odd/even evaluated-layer $T_T$ and $D_T$.
5. Block 36 as one isolated descriptive point.
6. Raw layer points are mandatory. A centered three-layer moving median may be overlaid for readability; all decisions use unsmoothed values.
7. For $A,B\in\{E,L\}$, stage tail capture is $S_{A\rightarrow B,T}=\operatorname{median}_{\ell\in B}e_{\ell,T}(Q_{T,A})$; $S_{E\rightarrow E,T}$ and $S_{L\rightarrow L,T}$ use their internal odd/even cross-fits.
8. Assign exactly one non-primary interpretation after the global verdict:
   - `globally_stable_compatible` when $O_{EL,T}$ and both cross-stage captures exceed their matched Haar q95 values;
   - `late_formation_compatible` when late-internal capture exceeds Haar q95 while early-internal capture, $O_{EL,T}$, and both cross-stage captures do not;
   - `stage_redirection_compatible` when both internal captures exceed Haar q95 while $O_{EL,T}$ and both cross-stage captures do not;
   - `mixed_stage_geometry` otherwise.

These labels mean “compatible with,” not causal proof. They cannot rescue or downgrade the global verdict.

## 12. Known Good, Known Bad, And Confusing Cases

| Case | Required reading |
| --- | --- |
| local F1--F16 shares sum to 1 | local partition implementation is coherent |
| random H/M/T mean captures approach $1/16$, $7/16$, $8/16$ | dimension-matched null is coherent |
| synthetic covariance inside a known projector gives capture near 1 | projection implementation passes |
| missing sample/layer, replay mismatch, non-finite value, or invalid projector | stop; no scientific verdict |
| raw tail capture is largest but enrichment is not | dimension artifact, not tail specificity |
| one tail band is high but broad $D_T$ fails | localized diagnostic only; broad claim fails |
| local spectrum shifts but shared tail matches random | local-only relocation |
| tail beats random but head/middle changes as much | generic shared geometry |
| only block 36 is extreme | terminal anomaly |
| smoothed line passes while raw registered metric fails | visual artifact |

## 13. Scientific Procedure And Stage Contracts

### Stage 0 — immutable-input audit

Verify all dataset and run hashes, record order, shapes, and coverage. Any mismatch stops the run.

### Stage 1 — deterministic raw-$\Delta n$ replay

Materialize raw $\Delta n$ from only the frozen model and $S_0$; apply every Section 5.3 guard. Smoke or full analysis cannot proceed after a failure.

### Stage 2 — local and shared spectral construction

Build local F1--F16 and H/M/T; global odd/even cross-fitted shared spaces; early-internal and late-internal cross-fits; and both cross-stage spaces. Audit ranks, orthogonality, residuals, group exclusion, and cross-stage overlap.

### Stage 3 — engineering smoke

Use synthetic covariances plus a fixed small subset to verify complete-spectrum accounting, random-dimension expectations, broad-versus-band non-additivity handling, seed determinism, and artifact schemas. Smoke results are scientifically ineligible.

### Stage 4 — one full frozen analysis

Run all 512 records, blocks 1--36, 512 random partitions, and 2,000 grouped bootstraps once. No scientific definition may change after any full result is visible.

### Stage 5 — evidence and visual audit

Write tables, figures, manifests, `summary.md`, and `detailed.md`; open all central figures at original resolution and audit labels, raw points, units, random baselines, H/M/T dimensions, block 36, smoothing disclosure, and claim boundary.

## 14. Algorithm, Outputs, And Provenance

```text
verify immutable inputs
replay raw delta-n and reproduce old local spectrum
construct local F1--F16 and direct local H/M/T
construct global, early-internal, late-internal, and bidirectional cross-stage shared F1--F16 and direct H/M/T
generate fixed shared random 16-band partitions
compute all local/shared band and broad-region metrics
bootstrap parents/templates in paired form
apply the broad-tail verdict once
assign the non-primary stage-geometry label only after the global verdict
render and audit complete-spectrum and decision figures
```

Approved worker: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e01_shared_tail_geometry/`. Reuse the old immutable basis and attention-write artifacts by path; do not modify them. Raw tensors, logs, and complete random draws remain in the new worker. Resource ceiling: one H100 80GB, six wall-clock hours, and 20 GiB of new storage; exceeding any ceiling stops the run before a scientific verdict.

Required curated artifacts after an approved run:

- `provenance/input_manifest.json`, `numerical_guards.json`, `verdict.json`;
- `tables/local_spectrum_f1_f16.csv` with every layer, band, $v^{local}$, and $p^{local}$;
- `tables/shared_spectrum_f1_f16.csv` with every layer, band, $c^{shared}$, and $e^{shared}$;
- `tables/broad_hmt.csv` with every layer's local/shared H/M/T raw and normalized values;
- `tables/stage_shared_geometry.csv` with every F1--F16 and H/M/T early-internal, late-internal, early-to-late, and late-to-early measurement;
- `tables/stage_overlap.csv` with actual and Haar cross-stage projector overlap;
- `tables/contrast_summary.csv` and `random_null_summary.csv`;
- `figures/figure0_broad_tail_decision.png`;
- `figures/figure1_full_16band_spectrum.png`;
- `summary.md` and `detailed.md`.

The complete-spectrum figure contains local absolute variance, local normalized share, global shared-band enrichment heatmaps, and the F1--F16 early-to-late curve. The decision figure contains global layerwise H/M/T raw capture and enrichment, broad contrasts, random intervals, and group/split robustness. A third diagnostic figure contains stage-internal, bidirectional transfer, and overlap measurements and is visually marked “non-primary.” All files receive SHA-256 provenance.

## 15. Success, Failure, And Insufficient Evidence

Verdict precedence is `Insufficient`, then `Pass`, otherwise `Fail` only when the estimate is decisively non-supporting.

### Pass — `BROAD_SHARED_TAIL_GEOMETRY`

All conditions must hold:

1. input, replay, numerical, and broad shared-tail stability guards pass;
2. G0: the 95% lower bound of $T_{rank}$ is positive and both expression-half point estimates are positive;
3. the local broad-tail bridge $T_{LT}$ is positive;
4. the 95% lower bound of actual broad-tail $T_T$ is positive;
5. actual $T_T$ and late enrichment $L_T$ both exceed the q95 values of the 512 matched random F9--F16 unions;
6. the 95% lower bound of $D_T=T_T-\max(T_H,T_M)$ is positive;
7. broad-tail $T_T$ is positive in odd and even evaluated layers and in both expression halves.

The 16 individual bands are mandatory evidence but are not additional Pass gates.

The stage-geometry label is assigned only after this global verdict and has no effect on it.

### Fail — `LOCAL_RANDOM_OR_NONTAIL_RELOCATION`

G0 and validity guards hold, but a stable falsifier occurs: broad tail does not increase, does not beat matched random, does not exceed head/middle after dimension correction, or only the local spectrum relocates. Fail closes the broad shared-tail explanation and does not permit activation deletion or Router work.

### Insufficient

Use a typed `INSUFFICIENT_*` result for any input/replay/projector failure, unreliable G0, required broad interval crossing zero, or expression/layer-group sign reversal. Only provenance or estimation repair is allowed. A new band grouping, chosen tail subset, metric, or threshold requires another approved amendment.

## 16. Cannot Claim

No outcome establishes knowledge storage, natural-language ontology, absence from head/middle/old state, nonlinear coding, MLP transmission or suppression, a near-null sink, logit or loss effect, downstream utility, model-family generality, or Router value.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Current evidence / required decision |
| --- | --- | --- |
| A. question and boundary | `CONFIRMED` | geometry-only question, global-primary boundary, and F1/F2--F8/F9--F16 partition confirmed |
| B. data and provenance | `CONFIRMED` | reuse $S_0$ and deterministically materialize raw $\Delta n$ |
| C. diagnostic task | `CONFIRMED` | conditional-fine is the only primary semantic object; complete spectrum is mandatory |
| D. model and spaces | `CONFIRMED` | global, early-internal, late-internal, and bidirectional cross-stage geometry are all required |
| E. precision and randomness | `CONFIRMED` | 512 random orthogonal partitions and 2,000 grouped bootstraps |
| F. comparison and verdict | `CONFIRMED` | global $D_T$ strict conjunctive rule; stage labels are non-primary and non-rescuing |
| G. execution and reproducibility | `CONFIRMED` | implementation, replay, smoke, one full run, and local evidence records explicitly authorized |

Cross-block consistency is `PASS`. The scientific design is frozen as `A15_04_E01_r1` at `2026-08-09T14:05:43Z`. After execution starts, any change to $S_0$, $\Delta n$, semantic covariance, layer groups, stage windows, F1--F16 partition, H/M/T grouping, random construction, primary statistics, verdict thresholds, or the global-primary boundary requires an append-only amendment and an explicit eligibility ruling.

**Append-only amendment A1 — mandatory direction-level visual, `2026-08-09T14:18Z`.** Before: the complete-spectrum artifact required 16-band absolute and normalized summaries. After: it additionally requires unsmoothed raw conditional-fine variance and normalized variance share for all 4,096 local parameter directions at every layer, plus a fixed ten-layer display for blocks 1, 5, 9, 13, 17, 21, 25, 29, 33, and 36. The display overlays a 129-rank third-order Savitzky--Golay curve only for readability; tables, metrics, and verdicts use unsmoothed values. Reason: preserve the researcher's previously mandatory curve and guard against band averaging hiding local shape. No new experiment result was visible; only behavior-level unit tests had run. Affected block: output-only part of G. Approval: inherited from the researcher's earlier explicit mandatory-figure instruction and current full-experiment authorization. Eligibility impact: none; no data, metric, threshold, comparison, or verdict rule changed.

**Append-only amendment A2 — exact-run coordinate recovery, `2026-08-09T14:39Z`.** Before: Section 5.3 required a new H100 replay to materialize raw $\Delta n$. During engineering smoke, the unchanged H100 forward pass disagreed with the frozen 5090 bfloat16 attention cache in all 36 layers (maximum absolute error rose from `0.00390625`--`0.015625` in the first layers to `1.5` at block 36), so that replay is ineligible and is not scientific evidence. After: use only the original registered A15_01_09 response run, which already records exact cache replay (`max_abs_error=0`) and full-basis reconstruction error at most $2.73059\times10^{-6}$, and recover raw residual-coordinate $\Delta n$ by multiplying its complete saved FP16 eigencoordinates by the independently saved complete parameter basis. This repair is eligible only if, at every layer, (i) saved response, semantic, and parameter eigenvalue arrays match exactly, (ii) the saved basis reconstructs the independently cached raw attention write with relative $L_2$ error at most $3\times10^{-4}$, (iii) coordinate round-trip error is at most $10^{-4}$, and (iv) the registered centroid and trace reproduction tolerances remain satisfied. Observed guard maxima before any geometry result was read were $2.13193\times10^{-4}$, $2.81957\times10^{-6}$, $8.39460\times10^{-8}$, and $2.88547\times10^{-7}$ respectively, so the repaired source is eligible. A quantization-perturbation sensitivity check remains mandatory before the verdict. Reason: retain the exact original 5090 semantic forward rather than relax the exact-cache guard for a different GPU architecture. Affected block: B/G provenance implementation only. Approval source: the researcher's direct full-experiment authorization plus the frozen rule that only provenance or estimation repair is allowed after an insufficient replay. Eligibility impact: restored conditionally; $S_0$, $\Delta n$ definition, conditional-fine object, layers, bands, metrics, thresholds, random null, and global-primary boundary are unchanged.
