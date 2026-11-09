# Detailed: A15_00_03_E01 Condition-Stratified Residual Modes

Primary anchor: [15_00_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_03_condition_local_residual_modes_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** distinguish a global residual projector from condition-specific
projectors hidden by random mixed-document shards.  
**Hypothesis:** real domain/topic labels yield higher within-condition than
cross-condition residual overlap, while cross-condition capture stays above a
matched random null.  
**Experiment logic:** estimate disjoint A/B bases per condition, compare
projector overlap, then test whether a source-condition basis captures an
independent target condition.  
**Conclusion:** Pass for condition-specific modes, with a strong shared
envelope. The strong fragmented-residual version is rejected.  
**Evidence:** domain gap bootstrap intervals 0.032--0.044; random-group q95
0.0012--0.0015; cross/within capture 0.951--0.964 at domain level.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| condition | a known grouping variable | 7 WOS domains or 28 nested areas | label | tests structured heterogeneity | label causality or semantic sufficiency |
| within overlap | whether two independent samples of one condition recover the same directions | A-basis versus B-basis of the same label | \(\|U_c^{A\top}U_c^B\|_F^2/64\) in [0,1] | estimation reliability plus condition stability | utility |
| cross overlap | whether different conditions use the same exact directions | source A-basis versus another condition's B-basis | \(\|U_c^{A\top}U_d^B\|_F^2/64\) | separates global from rotating modes | captured energy |
| \(\Delta O\) | condition-specific overlap advantage | median within minus median cross | overlap points | primary decision metric | isolated subspaces |
| cross-capture | how much target residual energy a source basis retains | target residual variance inside source basis | variance fraction | detects a shared envelope despite rotation | better routing or loss |
| capture margin | capture beyond generic residual directions | cross-capture minus target complement-Haar q95 | variance fraction | rejects accidental energy capture | semantics |
| document projector overlap | exact directions shared by two independently fitted document bases | \(\|U_s^\top U_t\|_F^2/64\) after per-document centering and pooled-top removal | [0,1] | tests local-mode identity | utility or causal semantics |
| self-normalized cross-capture | how much of a target document's own best rank-64 capture a foreign basis retains | source capture divided by target-own capture | ratio | separates a broad envelope from exact local modes | same directions |
| split-half reliability | whether one document reproduces its mode from disjoint tokens | even-token rank-32 versus odd-token rank-32 | overlap [0,1] | tests finite-token estimation rival | full rank-64 population projector |

## 2. Anchor Link And Decision Point

Random mixed DCLM shards had high residual overlap, but each shard mixed many
latent domains. The anchor asks whether conditioning reveals reproducible local
rotations while retaining transfer across conditions. It does not own the
training-benefit decision.

## 3. Protocol Compliance Audit

- approved conditions match actual conditions: **yes**;
- primary metric exists: **yes**, domain \(\Delta O\);
- central figures/tables exist: **yes**;
- checkpoints recorded: **yes**, LB/decommon 40k/80k;
- known good/bad/confusing cases reviewed: **yes**;
- success/failure/insufficient criteria applied: **Pass conditional modes / shared envelope**.

Both registered uncertainty layers were completed: 200 document/basis-refit
draws and a separate 2,000-draw domain-block bootstrap. They are uncertainty
checks over documents and observed conditions, not independent training-seed
confidence intervals.

## 4. Setup

**Data construction:** local `river-martin/web-of-science-with-label-texts`;
only `abstract` enters the model. Labels are grouping metadata only. Every
document contributes one stable-hash-selected 128-token slice.  
**Split:** per domain, 64 pooled-common train documents, 64 A, 64 B, 64
validation-mean, and 64 test-capture documents. Per nested topic, 32 A, 32 B,
32 validation-mean, and 32 test-capture documents. All 5,824 document roles are
globally disjoint.  
**Models:** 12-layer H768, eight-expert top-1 LB and decommon lineages at 40k
and 80k.  
**Representation:** the tensor actually consumed by the Gate.  
**Band:** remove an independently fitted pooled top-64, then fit residual
top-64 per condition. Centered top-64 is a comparator.  
**Seed:** 20260731. Layers, labels, and checkpoints are repeated measurements,
not independent training seeds.  
**Token artifact:** shape `[5824,128]`, SHA-256
`20aefff21f8d738387cfc6325a0b0a49bd055e00a1fed3f69329be003e0c0dcc`.  
**Known limitation:** WOS labels are observational and abstracts differ in
content beyond the label.

**Document-level follow-up:** all 448 domain-A and 448 domain-B documents are
used at every layer. Each target has six same-domain and six cross-domain
source documents under a fixed balanced pairing contract. Every document
subtracts its own token mean before fitting its residual top-64. A disjoint
even/odd 64-token rank-32 analysis supplies the estimator-reliability guard.

## 5. Metrics And Decision Rules

Primary Pass requires a positive domain basis-bootstrap lower bound for
\(\Delta O\), a positive cross-capture margin over complement-Haar q95, and
directional topic replication. Equal-size random groups must not reproduce the
gap. No practical effect-size threshold is imposed.

The ratio `cross_capture / within_capture` is descriptive. Values near one mean
that a foreign condition's basis loses little relative to the target's local
basis even if exact projector overlap is lower.

For document pairs, cross/within capture compares foreign-domain and
same-domain source documents. Cross/target-own optimum is stricter: it asks
how much of the target's locally strongest rank-64 variance a foreign document
basis retains. These ratios answer different questions and are not
interchangeable.

## 6. Main Results

### Decision evidence

| Model | Step | Level | Within residual | Cross residual | \(\Delta O\) point summary | Cross/within capture |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| decommon | 40k | domain | 0.777 | 0.725 | 0.046 | 0.964 |
| decommon | 80k | domain | 0.756 | 0.698 | 0.052 | 0.958 |
| LB | 40k | domain | 0.758 | 0.708 | 0.049 | 0.958 |
| LB | 80k | domain | 0.754 | 0.700 | 0.053 | 0.951 |
| all four | topic | 0.673--0.700 | 0.615--0.646 | 0.053--0.060 | 0.922--0.938 |

The domain basis-bootstrap intervals for \(\Delta O\) are:

- decommon 40k: `[0.0319, 0.0382]`;
- decommon 80k: `[0.0350, 0.0421]`;
- LB 40k: `[0.0337, 0.0407]`;
- LB 80k: `[0.0361, 0.0442]`.

The corresponding 2,000-draw domain-block intervals are `[0.0195,0.0613]` to
`[0.0210,0.0694]` across endpoints; all lower bounds remain positive.

Matched random-group q95 is only 0.00125--0.00155. Cross-capture margin over
the target complement-Haar q95 has lower bounds 0.353--0.384. Every one of the
12 layers at every endpoint has positive overlap gap and capture margin.

### Rival and comparator evidence

Centered top-64 is more stable in absolute overlap (within 0.831--0.845 and
cross 0.769--0.794 at domain level), but it also has a within-cross gap. Thus
condition structure is real but not residual-specific. Residual cross overlap
itself remains high (0.698--0.725 at domain level), rejecting isolated or
fully unstable condition subspaces.

### Document-level projector evidence

The document-level follow-up adds the following result:

| Endpoint | Residual within-domain overlap | Residual cross-domain overlap | Cross/same-domain capture | Cross/target-own optimum |
| --- | ---: | ---: | ---: | ---: |
| decommon 40k | 0.308 | 0.302 | 0.981 | 0.341 |
| decommon 80k | 0.301 | 0.295 | 0.979 | 0.330 |
| LB 40k | 0.308 | 0.302 | 0.978 | 0.335 |
| LB 80k | 0.301 | 0.296 | 0.978 | 0.327 |

The residual rank-64 Haar q95 is 0.0939. Thus different-document residual
projectors share much more than random directions, but much less than
condition-aggregated bases. Domain-block intervals for the document-level
within-minus-cross gap remain positive: approximately 0.0026--0.0118 across
endpoints.

The split-half guard is decisive against pure estimator noise. Across
endpoints, residual rank-32 overlap is 0.516--0.534 for two disjoint halves of
the same document, 0.173--0.181 for different same-domain documents, and
0.168--0.177 across domains. The same-document minus same-domain domain-block
interval is 0.340--0.358; the same-domain minus cross-domain interval is
0.0026--0.0065.

Centered top/common is more transferable: document-level rank-64 overlap is
0.362--0.383 across documents, and cross-document capture retains 0.513--0.533
of the target's own optimum versus 0.327--0.341 for residual.

### Reliability evidence

For all four endpoints and all 12 layers, replaying native logits from the
captured Gate input has relative Frobenius error 0 and top-1 agreement 1.0 over
745,472 token-layer observations per endpoint.

## 7. Visualization Results

### Residual rotations and shared capture

![Residual rotations and shared capture](figures/condition_overlap_and_cross_capture.png)

**Purpose:** show both clauses needed for the conclusion.  
**Setup:** four endpoints; domain and topic summaries across all 12 layers.  
**Metric:** rank-64 projector overlap and cross/within variance capture.  
**How to read:** open-to-filled vertical gaps in panel A show condition-specific
directions; values near one in panel B show transfer inside a shared envelope.  
**Observed:** within is consistently above cross, while cross capture retains
more than 92% of within capture.  
**Take-home:** modest structured rotations inside strong global sharing.  
**Remaining uncertainty:** labels need not be the causal source.  
**Does not prove:** routing or LM benefit.

### Condition gap versus random grouping

![Condition gap versus random grouping](figures/condition_gap_vs_random_group.png)

**Purpose:** test whether any equal-size grouping creates the overlap gap.  
**Setup:** 200 basis refits and 64 matched random groupings.  
**Metric:** median within-minus-cross projector overlap.  
**How to read:** blue intervals must remain above both zero and orange q95.  
**Observed:** all four intervals are roughly 0.032--0.044; random q95 is near
0.001.  
**Take-home:** real domain identity predicts projector similarity.  
**Does not prove:** that domain labels are the optimal latent conditions.

### Document-local modes versus the shared envelope

![Document-local residual projectors and capture](figures/document_projector_overlap_and_capture.png)

**Purpose:** directly test whether individual-document residual projectors
coincide, and whether low overlap is finite-token noise.  
**Setup:** 448 A and 448 B documents, balanced same/cross-domain pairs, all 12
layers and four endpoints; rank-32 disjoint-token guard.  
**Metric:** projector overlap, cross-capture relative to same-domain capture,
and cross-capture relative to the target's own optimum.  
**How to read:** panel A compares exact document directions with Haar and
centered-top; panel B compares same-document, same-domain, and cross-domain
views; panel C separates envelope transfer from local optimum retention.  
**Observed:** document residual overlap is about 0.30, same-document
split-half overlap exceeds 0.51, cross/same-domain capture is about 0.98, and
cross/target-own capture is about one third.  
**Take-home:** local modes vary genuinely, while a broader residual envelope
is shared; coarse domain labels explain only a small part of the variation.  
**Remaining uncertainty:** 128 tokens still limit the population-projector
estimate, and unlabeled latent conditions may explain document modes.  
**Does not prove:** functional routing benefit.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Verdict | What this rules out |
| --- | --- | --- | --- |
| S0 | frozen disjoint 5,824-document manifest | passed | sample leakage |
| S1 | exact Gate-input/logit replay | passed | wrong representation or hook |
| S2 | four complete endpoint captures | passed | endpoint missingness |
| S3 | domain within/cross and capture | passed | fully global/no-gap account |
| S4 | nested topics and matched random groups | passed | domain-only chance grouping |
| S5 | 200 basis refits, 2,000 domain-block draws, figures audited | passed | fragile point or condition sample |
| S6 | document rank-64 pairs plus disjoint-token rank-32 guard | passed | pooled-condition stability mistaken for exact document stability |

**Falsified:** fully global/no-gap residual and fully unstable/isolated residual.  
**Remaining rivals:** labels proxy another condition; finite-rank choice affects
effect size; a nonlinear mixture may explain the same geometry.

## 9. Full Experiment Record

The curated full tables are
[condition_stratified_summary.csv](tables/condition_stratified_summary.csv) and
[condition_stratified_inference.csv](tables/condition_stratified_inference.csv).
The document-level follow-up is in
[document_projector_summary.csv](tables/document_projector_summary.csv),
[document_split_half_summary.csv](tables/document_split_half_summary.csv), and
the adjacent inference/null JSON records.
Condition-pair, layer, null, bootstrap, raw activation, and replay records
remain on the worker surface listed below.

## 10. Interpretation

The user's A14-style intuition is correct in a bounded form: conditioning
reveals reproducible local residual rotations hidden by mixed random shards.
The document-level follow-up makes the bounded form sharper. Exact local modes
change substantially across documents, and this is not primarily an estimator
artifact. However, domain identity explains only a small share of that change:
a cross-domain basis transfers almost as well as a same-domain foreign basis,
and both sit well above Haar. The correct model is therefore local or latent
low-dimensional modes inside a shared broad envelope, not seven isolated
domain residual spaces. Removing the mean changes a large DC component but
does not force the Gate into coherent per-domain semantic spaces.

## 11. Claim Boundary

This is frozen geometry in two related 12-layer lineages and one labeled
scientific-abstract corpus. It cannot establish causal semantics, preferred
Router inputs, compatible expert updates, or held-out loss improvement.

## 12. Next Decision

The matched 2B band-dispatch experiment is now complete: fixed bands changed
routes but no true band improved NLL over native. Close fixed residual-band
dispatch as a design target; require any successor to predict expert-update or
task utility directly before large training.

## 13. Links And Artifact Map

- anchor: [15_00_04 anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_03_condition_local_residual_modes_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_00_condition_stratified_residual`
- runner: `run.py`, `infer.py`
- condition-block inference: `condition_block_infer.py`
- document projector audit: `document_projector_audit.py`
- split-half reliability guard: `document_split_half_guard.py`
- data manifest: `runs/a15_00_04_e01/data/data_manifest.json`
- checkpoint manifest: `runs/a15_00_04_e01/checkpoint_manifest.json`
- raw results: `runs/a15_00_04_e01/raw/`
- full analysis: `runs/a15_00_04_e01/analysis/`
- figure generator: `make_result_figures.py`
- local execution: LB on H100:0; decommon on H100:1
