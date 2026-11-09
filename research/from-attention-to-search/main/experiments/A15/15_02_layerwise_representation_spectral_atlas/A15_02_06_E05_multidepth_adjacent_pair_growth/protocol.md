---
experiment_id: A15_02_06_E05_multidepth_adjacent_pair_growth
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: EXECUTED_RESULTS_RECORDED
canonical_language: en
approved: 2026-08-12
---

# Protocol: Multi-Depth Adjacent-Layer Attention-Write Redistribution

## 0. Approval Snapshot

- Purpose: test whether the block-8→9 result is local or whether adjacent-layer normalized spectral redistribution changes significantly across depth.
- Human authorization: the researcher requested four shallow-to-deep adjacent pairs, required inclusion of 8→9, requested separate pair analyses and a significance analysis of depth differences, and authorized execution on 2026-08-12.
- Frozen pairs: 2→3, 8→9, 17→18, and 34→35. These span early, early-middle, middle-late, and late computation while excluding the known display-only boundary block 36.
- Changed variable: source/target depth pair only.
- Held fixed: model, 512 records, token position, post-`o_proj` pre-residual Attention-write hook, Mean Response basis and rank order, centering, variance estimator, within-layer normalization, 16 bands, F9--F12 semantic region, parent-bootstrap draws, smoothing, and plotting rules.
- Primary per-pair metric: normalized variance-share change \(D_q\) in frozen ranks `[0.50,0.75)`.
- Primary cross-depth evidence: all six deeper-pair minus shallower-pair contrasts in \(D_q\), with one 95% simultaneous centered-bootstrap family.
- Pass for depth heterogeneity: at least one of the six simultaneous intervals excludes zero.
- No resolved heterogeneity: all six simultaneous intervals include zero.
- Insufficient: any identity, balance, projection, bootstrap, completeness, or figure guard fails.
- Execution scope: implementation, tests, all eight cached layer tensors, 2,000 paired parent bootstraps, exactly two final figures, and canonical result records.
- Cannot claim: information-theoretic novelty, low rank, semantic causality, monotone layerwise law, or Router utility.

## 1. Objects And Coordinate

For record \(x\) and block \(\ell\), \(A_\ell(x)\in\mathbb R^{4096}\) is the direct `self_attn.o_proj` output before residual addition at the final `Classification:` colon.

All blocks use the exact frozen Mean Response basis \(V=[v_1,\ldots,v_{4096}]\), ordered from larger to smaller average trace-normalized MLP gate/up input-side parameter response. No activation from the selected pairs constructs or changes \(V\).

Projection precedes normalization:

\[
z_{\ell xj}=A_\ell(x)^\top v_j,
\qquad
e_{\ell j}=\operatorname{Var}_x(z_{\ell xj}),
\qquad
p_{\ell j}=\frac{e_{\ell j}}{\sum_k e_{\ell k}}.
\]

Record vectors and projection coefficients are not normalized individually. \(p_{\ell j}\) is the fraction of block \(\ell\)'s total across-record Attention-write variance in direction \(j\).

## 2. Frozen Pairs And Per-Pair Estimands

Let pair \(q=(s_q,t_q)\) be one of

\[
(2,3),\quad(8,9),\quad(17,18),\quad(34,35).
\]

For each direction and pair:

\[
\Delta p_{qj}=p_{t_qj}-p_{s_qj}.
\]

Aggregate the 4096 directions into 16 fixed 256-direction bands \(F_1,\ldots,F_{16}\):

\[
\Delta Q_{qb}=\sum_{j\in F_b}\Delta p_{qj},
\qquad
G_{qb}=\log_2\frac{\sum_{j\in F_b}e_{t_qj}}
{\sum_{j\in F_b}e_{s_qj}}.
\]

The independently frozen fine-enriched region is

\[
B_{sem}=F_9\cup F_{10}\cup F_{11}\cup F_{12}.
\]

The per-pair endpoints are

\[
D_q=\sum_{b=9}^{12}\Delta Q_{qb},
\qquad
G_q=\log_2\frac{E_{t_q}(B_{sem})}{E_{s_q}(B_{sem})}.
\]

\(D_q\) is relative redistribution; \(G_q\) is the mandatory raw-scale guard. Neither is silently called new knowledge.

## 3. Cross-Depth Difference Contract

Order the four transitions by midpoint depth \(m_q=(s_q+t_q)/2\). For every ordered pair \(a<b\), define

\[
H_{ab}=D_b-D_a.
\]

There are six registered \(H_{ab}\) contrasts. Positive means the deeper transition reallocates more normalized share to F9--F12 than the shallower transition. The six contrasts receive one 95% simultaneous centered-bootstrap interval using the maximum absolute centered deviation over all contrasts.

The four \(D_q\) values also receive one simultaneous 95% family, and all 64 fixed band changes \((q,b)\) receive one simultaneous family. These families answer different registered questions and are not pooled.

An ordinary least-squares slope of \(D_q\) on \(m_q\) is reported with a paired-bootstrap 95% interval as a secondary ordered-depth summary. With only four selected depths it cannot establish a smooth or universal monotone law.

## 4. Data And Uncertainty

- Reuse the audited 512-record balanced taxonomy cube: 8 parents × 8 children × 4 templates × 2 bundles.
- Use total across-record Attention-write covariance for each block. Coarse/medium/fine components do not enter the transition estimator.
- Generate 2,000 paired bootstrap draws over the eight parent domains with replacement, seed `8120605`.
- Every draw recomputes each block's mean, direction variance, total normalization, 16 bands, four \(D_q\), four \(G_q\), six \(H_{ab}\), and the depth slope.
- Use identical parent draws across all eight blocks, preserving the paired comparison.
- Expression halves A/B recompute every pair endpoint as sign guards, not independent replicates.
- No layer, direction, record, parent, or bootstrap draw is selected or dropped from observed outcomes.

## 5. Typed Results

For each pair, report `positive`, `negative`, or `unresolved` normalized region change according to its four-comparison simultaneous interval. Report raw growth separately.

The experiment-level typed verdict is:

- `significant_depth_heterogeneity`: at least one familywise six-contrast interval for \(H_{ab}\) excludes zero.
- `no_resolved_depth_heterogeneity`: all six familywise intervals include zero.
- `insufficient_<guard>`: a required guard fails.

If heterogeneity passes, name exactly which registered deeper-versus-shallower contrasts exclude zero and their signs. Do not infer a monotone law unless the slope interval excludes zero and the four point estimates follow that direction; even then the claim is limited to the selected pairs.

## 6. Guards And Reproducibility

- Verify frozen SHA-256 identities for dataset, model manifest, extraction manifest, basis, and every selected layer cache.
- Require exact 512-record order and balanced parent blocks.
- Require Mean Response basis relative orthogonality error below \(5\times10^{-4}\).
- Require projected centered variance trace to match direct centered-state variance within relative error \(5\times10^{-4}\) for every block and split.
- Unit-test variance centering, band aggregation, paired parent bootstrap, simultaneous intervals, registered pair construction, and pairwise contrasts.
- Preserve E04 8→9 point estimates within absolute tolerance \(5\times10^{-6}\).
- Stop as insufficient rather than interpreting any failed guard.

## 7. Exactly Two Figures

### Figure 1: four separate same-direction transition panels

- Four rows, one per frozen pair from shallow to deep.
- Left column: source and target \(4096p_{\ell j}\) curves on log scale.
- Right column: \(4096\Delta p_{qj}\) with zero line.
- Use a centered 129-direction moving average for display only; statistics remain unsmoothed.
- Shade `[0.50,0.75)` consistently.
- Allowed conclusion: qualitative location of relative redistribution for each pair in identical directions.
- Limitation: visual differences are not cross-depth significance evidence.

### Figure 2: registered across-depth evidence

- Panel A: 4×16 heatmap of unsmoothed fixed-band \(\Delta Q_{qb}\).
- Panel B: four \(D_q\) values with four-comparison simultaneous 95% intervals and the bootstrap depth slope.
- Panel C: four \(G_q\) raw log2 growth values with simultaneous 95% intervals.
- Panel D: all six deeper-minus-shallower \(H_{ab}\) contrasts with six-comparison simultaneous 95% intervals.
- Allowed conclusion: which selected transitions differ significantly and whether relative and absolute changes agree.
- Limitation: selected-pair robustness, not all-adjacent-layer or causal evidence.

## 8. Execution Contract And Freeze

1. Create the configuration and tests; record expected RED and GREEN states.
2. Hash-verify all sources and run the eight-cache projection.
3. Run the full paired bootstrap and all registered simultaneous families.
4. Render exactly two figures and inspect both at full resolution.
5. Write `summary.md` and `detailed.md` as `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` until the researcher states the post-result judgment.

No new inference, basis search, sliding-window search, probe, Router training, graph edit, publication, commit, or push is authorized.

## 9. Confirmation And Consistency Ledger

- A, question and boundary: `CONFIRMED` by the direct request.
- B, frozen data and provenance: `CONFIRMED` by reuse of E04 assets.
- C--E, no learning task/model/optimization: `NOT_APPLICABLE`; static audit only.
- F, comparisons and decision evidence: `CONFIRMED`; four pairs and cross-depth significance were explicitly requested, with pair selection delegated.
- G, execution and reproducibility: `CONFIRMED`; complete execution was requested.
- Cross-block consistency: `PASS`.
- Scientific body frozen before access to the six newly selected layer caches.

## Execution Receipt — APPEND ONLY

- Full execution completed on 2026-08-12 under run ID `a15-02-06-e05-20260812-multidepth-pairs`.
- All eight layer caches, source identities, basis, projection-energy, paired-bootstrap, E04 cross-check, and figure guards passed.
- Registered experiment-level outcome: `significant_depth_heterogeneity`.
- Canonical result records: [summary.md](summary.md) and [detailed.md](detailed.md).
