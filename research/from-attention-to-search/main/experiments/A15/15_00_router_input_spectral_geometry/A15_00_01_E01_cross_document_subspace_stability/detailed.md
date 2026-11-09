# Detailed: A15_00_01_E01 Centered Common Subspace Stability

Primary anchor: [A15_00_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_01_cross_document_subspace_stability_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** Test whether demeaning leaves a transferable centered coordinate
or only document-local residual directions.

**Hypothesis:** A centered top-64 fitted on one document group transfers to
unseen documents more strongly than an equal-rank local residual fitted after
an independently pooled top-64 is removed.

**Experiment logic:** Fit bases on documents that never appear in target
evaluation, subtract a matched Haar-64 q95 capture, and compare the original
centered top-64 with residual top-64 under paired document bootstrap.

**Conclusion:** Comparative H1 passes. Centered top-64 is more transferable,
but the residual top-64 also transfers strongly. Therefore the strong
“residual chaos/no learning coordinate” mechanism is falsified.

**Evidence:** In decommon 80k, the model-median top-minus-residual gap is 0.176
with bootstrap 95% interval [0.172, 0.179]. Decommon 40k replicates at 0.179
[0.175, 0.182]. LB has the same direction.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| actual Router input | tensor directly scored by the deployed Gate | direct `mlp.gate` pre-hook | activation | avoids the old expert-input mismatch | semantic content |
| centered top-64 | strongest 64 covariance directions after one fixed mean is removed | top eigenspace of fit-document covariance | 64 directions | candidate transferable centered coordinate | semantic commonality |
| pooled top-64 | centered top-64 fitted on 128 independent pooled documents | \(U_P\) | 64 directions | independent residualization basis | usefulness |
| local residual-64 | top 64 directions after projecting fit covariance into \(U_P^\perp\) | \(U^{res}_s\) | 64 directions | equal-rank challenger | all residual information |
| cross-capture | target energy captured by a source-fitted basis | \(\mathrm{tr}(U_s^\top\Sigma_tU_s)/\mathrm{tr}(\Sigma_t)\) | activation-energy fraction | tests out-of-group transfer | function |
| \(\Gamma\) | cross-capture above a target-specific random-direction threshold | capture minus Haar-64 q95 | energy fraction | rejects arbitrary subspaces | causality |
| gap | centered top transfer minus residual transfer | \(\Gamma_{\mathrm{top}}-\Gamma_{\mathrm{res}}\) | energy fraction | primary comparative metric | that residual is useless |
| projector overlap | direct geometric intersection of two fitted 64-D spaces | \(\|U_s^\top U_t\|_F^2/64\) | \([0,1]\) | distinguishes rotating bases from shared projectors | semantic conditions or utility |

## 2. Anchor Link And Decision Point

The parent Q1 result showed that trained Gates strongly prefer covariance-head
directions, but it did not establish whether those directions are stable across
data groups. This experiment adjudicates only that missing stability clause.
Gate use is owned by parallel A15_00_02.

## 3. Protocol Compliance Audit

- all decision-bearing conditions and hard guards match actual conditions:
  **yes**;
- documented execution amendment: non-claim-bearing 30k macro support and
  descriptive multi-rank/fine-spectrum profiles were stopped before result
  closure and cannot support claims;
- primary metric exists: **yes**, for LB/decommon at 40k/80k and all 12 layers;
- central figure/table exists: **yes**;
- seeds/checkpoints recorded: **yes**, deterministic seed 20260731 and
  checkpoint hashes in the worker manifest;
- known good/bad/confusing cases reviewed: **yes**;
- success/failure/insufficient criteria applied: **yes**;
- retained endpoints use exactly 2,000 document-bootstrap replicates: **yes**.

The 30k activation extraction and point-diagnostic caches predate the amendment
but are excluded from tables, figures, and claims.

## 4. Setup

**Research question:** Does a centered top-64 transfer across disjoint DCLM
documents more strongly than a same-rank local residual?

**Data construction:** One locked held-out DCLM JSONL-Zstandard shard. Documents
were stable-hash sorted after excluding every document in the earlier Q1 and Q2
manifests. The retained set has 640 documents × 256 tokens.

**Split:** 128 documents fit \(U_P\). The remaining 512 form eight disjoint
64-document shards; the first 32 documents in each shard fit a source basis and
the last 32 evaluate transfer.

**Models:** Two 12-layer, hidden-size-768, 8-expert, top-1 MoE lineages:
load-balanced linear Gate (LB) and running-center/no-LB Gate (decommon).

**Representation:** Direct Gate-effective input. LB uses \(r=g\); decommon uses
\(r=g-c\) with the frozen checkpoint running center.

**Training/update:** None. This is a frozen forward and matrix audit.

**Retained checkpoints:** 40k replication and 80k primary. 30k was stopped by
researcher amendment before claim-bearing bootstrap.

**Randomness:** Seed 20260731; 256 full/complement Haar orientations; 2,000
paired document bootstrap replicates.

**Held fixed:** tokens, documents, rank 64, layer mapping, Gate/expert ordering,
source/target assignment, and null construction.

**Known limitation:** one model family and one DCLM distribution; checkpoint
comparisons are macro states, not online dynamics.

## 5. Metrics And Decision Rules

For ordered source-target shards \(s\ne t\):

\[
\Gamma_{\ell}
=\operatorname{median}_{s\ne t}
\left[
\frac{\mathrm{tr}(U_{\ell,s}^{\top}\Sigma_{\ell,t}U_{\ell,s})}
{\mathrm{tr}(\Sigma_{\ell,t})}
-q_{0.95}^{\mathrm{Haar},t}
\right].
\]

The model summary is the median over 12 layers inside each bootstrap replicate;
layers are not independent seeds.

Registered Pass requires decommon 80k bootstrap lower bounds above zero for
\(\Gamma_{\mathrm{top}}\) and the top-minus-residual gap, with decommon 40k point
estimates in the same direction. A positive residual value does not fail the
comparative H1; it rejects the stronger “no stable residual” interpretation.

## 6. Main Results

### Decision evidence

| Lineage | Step | Top \(\Gamma\) | Residual \(\Gamma\) | Gap | Gap 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 0.584 | 0.409 | 0.162 | [0.158, 0.165] |
| LB | 80k | 0.564 | 0.392 | 0.167 | [0.161, 0.169] |
| decommon | 40k | 0.600 | 0.414 | 0.179 | [0.175, 0.182] |
| decommon | 80k | 0.580 | 0.402 | 0.176 | [0.172, 0.179] |

All four retained endpoints have positive top, residual, and gap values in
12/12 layers.

### Stage-level profiling evidence

- Shard-mean pairwise cosine medians are 0.932/0.948 for LB 40k/80k and
  0.935/0.972 for decommon 40k/80k.
- Cross-shard projector-overlap medians are 0.791/0.766 for LB centered top,
  0.729/0.719 for LB residual, 0.784/0.760 for decommon centered top, and
  0.730/0.704 for decommon residual. Matched random q95 is 0.086 in the full
  space and 0.094 in the residual complement.
- The centered-minus-residual model-median overlap gap is only 0.045--0.047.
  It is positive in 10/12, 12/12, 10/12, and 11/12 layers across the four
  endpoints, so the overlap ordering is not a universal per-layer claim.
- Fit-document counts 8, 16, and 32 keep the gap direction positive; decommon
  80k medians are 0.175, 0.178, and 0.176.
- Logical-batch regrouping preserves the top/residual ordering.
- Within-shard half-split capture exceeds its Haar q95 in every retained
  endpoint.
- Residual 64th-eigenvalue rank guards remain far above numerical tolerance.

### Debug and guard evidence

- Actual-input relation error: 0 for all retained endpoints.
- Native logit replay error: 0; top-1 agreement: 1.0.
- Decommon \(g\) versus \(g-c\) centered-covariance relative discrepancy:
  at most 0.000881.
- Minimum centered top-64 projector overlap: 0.999999.
- All 32 retained hard-guard rows pass.

## 7. Visualization Results

### Cross-document centered and residual transfer

![Centered common and residual transfer](figures/centered_common_vs_residual_transfer.png)

**Purpose:** Show whether the centered top-64 and residual top-64 transfer to
unseen documents, layer by layer.

**Setup:** Eight source-fit and target-evaluation shards; full-space and
complement-space Haar q95 controls.

**Metric/unit:** Null-relative captured activation-energy fraction.

**How to read:** Zero is the matched Haar q95. Blue above orange means the
centered top-64 transfers more strongly; orange above zero means the residual
also contains transferable structure.

**Observed:** Every panel and layer has blue > orange > 0. Bands are paired
document-bootstrap 95% intervals.

**Take-home:** The representation contains a hierarchy of stable centered
structure; residualization weakens but does not destroy transfer.

**Remaining uncertainty:** Statistical transfer does not identify semantic or
functional content.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Verdict | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| S0 provenance | disjoint hashes, six compatible caches, retained 40k/80k | passed | none | document leakage and coordinate mismatch |
| S1 object | Gate-input/logit replay and center invariance | passed | none | wrong tensor and DC leakage |
| S2 sample adequacy | 8/16/32 curves keep gap sign | passed | none | sign caused by one fit size |
| S3 transfer | top and residual both above null; gap positive | passed with qualification | none | no stable centered coordinate |
| S4 controls | Haar, regrouping, rank, bootstrap | passed | none | finite-sample arbitrary direction |
| S5 verdict | decommon 80k lower bounds positive; 40k replication | passed | none | insufficient precision |

**Falsified physical prior:** residual space is so document-specific that no
shared learning direction exists.

**Not falsified:** pooled top-64 is more stable than local residual-64.

**Remaining rivals:** stable residual structure may extend beyond rank 64; both
spaces may combine semantic and nuisance variation.

## 9. Full Experiment Record

The 640-document token tensor has SHA-256
`fe9d01714b258734e5624eed67e528f1a2e0cae95ab5187e26d6118fd050d598`.
It excludes 64 prior Q1 and 512 prior Q2 documents.

Extraction ran locally on two H100 80GB GPUs. Each full endpoint took about
33--60 seconds and produced a read-only 3.08GB cache. The exact bootstrap used
GPU-batched covariance aggregation and CPU-parallel SciPy subset eigensolvers,
requesting only the largest 64 eigenvectors. Every layer compared the hybrid
replicate against the original GPU full-spectrum formula; maximum retained
absolute difference was below \(1.3\times10^{-5}\) and within metric-specific
numeric tolerances. Each 2,000-replicate endpoint took about 30 minutes.

No remote job or training job was submitted.

## 10. Interpretation

Demeaning removes one first-moment/DC vector. It cannot, by translation alone,
remove stable covariance directions. The experiment directly demonstrates that
the centered covariance has a strong cross-document top-64. It also shows that
the complement still has structured cross-document variation. Direct
projector overlap further shows that the residual top-64 itself is highly
shared across the random document shards. The appropriate model is therefore
a globally shared hierarchy with different energy concentration, not “common
mean versus randomly rotating residual.”

Because the eight shards are random mixtures rather than domain/topic
conditions, this does not rule out lower-dimensional condition-specific modes
inside the shared residual envelope. That stronger A14-style interpretation
requires condition-stratified groups.

## 11. Claim Boundary

Established: cross-document statistical transfer and a comparative stability
gap at 40k/80k in these two lineages.

Not established: semantics, expert compatibility, causal training dynamics,
validation benefit, or universality. The result does not recommend deleting
the pooled component.

## 12. Next Decision

Decide whether to formalize a condition-stratified frozen follow-up that
jointly measures residual projector overlap and cross-capture across
domain/topic groups, with within-condition half-split reliability as the
estimation ceiling, before any matched training intervention.

## 13. Links And Artifact Map

- anchor: [A15_00_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_01_cross_document_subspace_stability_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- central figure: [PNG](figures/centered_common_vs_residual_transfer.png)
- tables: [model summary](tables/model_summary.csv), [layer metrics](tables/layer_metrics.csv), [sample-size curve](tables/sample_size_curve.csv), [means](tables/mean_metrics.csv), [projector-overlap model summary](tables/projector_overlap_model_summary.csv), [projector-overlap layers](tables/projector_overlap_layers.csv), [projector-overlap pairs](tables/projector_overlap_pairs.csv), [projector-overlap null](tables/projector_overlap_null.csv), [guards](tables/hard_guards.csv)
- historical code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit` (not present in the current checkout)
- data manifest: `data_manifest.json: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/runs/a15_00_02_03/data/data_manifest.json`
- result directory: `analysis: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/runs/a15_00_02_03/analysis`
- key code: `extract.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/extract.py`, `analyze.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/analyze.py`, `bootstrap_hybrid.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/bootstrap_hybrid.py`, `projector_overlap.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_common_residual_audit/projector_overlap.py`
- remote job ID: none
