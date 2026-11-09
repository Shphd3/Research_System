---
experiment_id: A15_02_E01_qwen3_residual_semantic_variance_atlas
anchor_id: 15_02_layerwise_representation_spectral_atlas
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-04
canonical_language: en
---

# Protocol: Layerwise Coarse/Fine Semantic Variance And 16-Band Atlas In Qwen3-8B

Chinese companion: [protocol_cn](protocol_cn.md).

## 0. Approval And Confirmation Ledger

On 2026-08-04 the user approved the full question, two-level semantic definition, balanced 8-by-8 dataset, frozen model, 16-band boundaries, metrics, controls, heatmaps, implementation, smoke, and full execution. Publication, commit, push, and graph edits are not approved.

| Block | Status | Frozen decision |
| --- | --- | --- |
| A Question / boundary | CONFIRMED | Frozen-Qwen coarse/fine relative discriminability and spectral location |
| B Data / provenance | CONFIRMED | 8 parents x 8 children x 8 definitions; independent DCLM basis |
| C Diagnostic task | CONFIRMED | Matched eight-way coarse and conditional-fine variables from the same states |
| D Model / representation | CONFIRMED | Qwen3-8B embedding plus 36 raw block residual outputs |
| E Objective / optimization | CONFIRMED | No Qwen training; ridge probes are capability gates only |
| F Comparison / evidence | CONFIRMED | \(R_\ell\), 16-band \(b/q/j/e\), nested controls |
| G Execution | CONFIRMED | Smoke then full; Figures 0--3 require visual audit |

Cross-block consistency: PASS. The data expose both variables; task, representation, and metrics align; sealed confirmation data cannot affect selection; the evidence separates depth and spectral hypotheses from scale and random-orientation rivals; resources and artifacts cover all conditions.

## A. Question And Claim Boundary

Does coarse semantic discriminability become strong in shallow layers while conditional fine-semantic discriminability gains more with depth, and do both variables remain actually head-dominant while fine semantics have greater relative middle/tail enrichment?

This is a frozen static audit. It can establish a layer-specific representation atlas, not compositional computation, Router utility, or training benefit.

## B. Data Construction And Provenance

### B1. Balanced taxonomy

Freeze eight parents with eight children each:

| Parent | Children |
| --- | --- |
| mathematics | algebra; analysis; geometry; topology; number theory; combinatorics; probability; statistics |
| physics | mechanics; electromagnetism; thermodynamics; optics; quantum physics; relativity; condensed matter physics; particle physics |
| chemistry | organic; inorganic; physical; analytical; electrochemistry; nuclear; polymer; theoretical chemistry |
| biology | genetics; ecology; evolutionary biology; cell biology; molecular biology; microbiology; developmental biology; physiology |
| computer science | algorithms; operating systems; networks; databases; artificial intelligence; programming languages; graphics; cybersecurity |
| economics | microeconomics; macroeconomics; econometrics; international; labor; public; development; financial economics |
| medicine | cardiology; neurology; oncology; immunology; endocrinology; gastroenterology; pulmonology; nephrology |
| linguistics | phonetics; phonology; morphology; syntax; semantics; pragmatics; sociolinguistics; psycholinguistics |

Each child receives at least six human-audited factual atoms that contain neither the correct parent nor child label string. Four template families use two disjoint fact bundles each, yielding eight descriptions per child and 512 total texts.

All examples use

```text
Topic description: <definition without label names>
Identify the broad academic field and the specific subfield.
Classification:
```

Read the final colon token. Before results, apply tokenizer-aware length and readout-position matching. Any failed item permits only a semantically equivalent minimal wording repair; concept selection cannot depend on model results.

Pre-result implementation clarification: masked left padding and explicit position ids place every final colon at one absolute RoPE position without adding visible filler text. Natural text length is retained as a recorded nuisance. A length-only classifier and a label-free residualization over length, template, and fact-bundle indicators must not explain the primary direction.

### B2. Split and provenance

- Design: T1/T2, four texts per child.
- Sealed confirmation: T3/T4, four texts per child.
- Freeze labels, texts, token ids, readout span, template, fact atoms, source, split, and SHA-256.
- Open confirmation once only after rules, probes, statistics, and plot contracts are frozen.
- Prior 32 chains are not in the primary statistics and may only be a descriptive external control.

### B3. Background covariance

Reuse the A15_02_02_E02 128-document, 65,536-token independent DCLM corpus with token hash `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`. Verify that no new definition is duplicated verbatim.

## C. Diagnostic Task And Supervision

The same \(h_{\ell,p,c,t}\) defines:

1. eight-way coarse label \(p\);
2. eight-way fine label \(c\mid p\), fitted separately within each parent and then averaged.

Ridge multinomial probes only establish readout capability. Coarse fitting repeatedly matches the per-class sample size of each conditional-fine problem. Qwen receives no gradients.

## D. Model And Representation

- Path: `/data/share/Qwen3-8B`.
- Architecture: `Qwen3ForCausalLM`, 36 blocks, hidden size 4096.
- bfloat16 forward, FP64 moments/eigendecomposition/statistics.
- Sites: embedding output plus blocks 1--36 raw residual outputs before final model norm.
- Object: the shared final `Classification:` colon token.
- Do not inspect concept-token states or introduce attention-head/MLP-update objects.

Model, tokenizer, and weight hashes must match the existing reviewed `model_manifest.json`.

## E. Objective And Optimization

Qwen has no training, optimizer, or checkpoint selection. Probe standardization, ridge strength, and every operational threshold are selected on design data only. Confirmation labels cannot affect fitting, layer/band selection, thresholds, or stopping decisions.

## F. Comparison And Decision Evidence

### F1. Depth metric

\[
D_{\ell,g}=\frac{\operatorname{tr}(B_\ell^g)}{\operatorname{tr}(W_\ell^g)+\epsilon},
\quad
R_\ell=\log\frac{D_{\ell,\mathrm{fine}}}{D_{\ell,\mathrm{coarse}}}.
\]

The primary contrast is

\[
T_{\mathrm{depth}}
=\operatorname{median}_{25:35}R_\ell
-\operatorname{median}_{1:12}R_\ell.
\]

Depth Pass requires a nested-bootstrap 95% lower bound above zero, consistent direction across four templates and leave-one-parent-out subsets, and the same fine-relative gain in matched held-out probes. Block 36 is separate.

### F2. Sixteen bands

Order each layer by decreasing background \(\lambda\). F1 is ranks 1--256; F2--F8 are ranks 257--2048; F9--F16 are ranks 2049--4096. Primary inference is bandwise; H/M/T are registered summaries only.

Per-direction actual semantic variance is

\[
b_{\ell,g,k}=\frac{\operatorname{tr}(U_{\ell,k}^\top B_\ell^gU_{\ell,k})}{256}.
\]

Also report \(q\) relative to background variance, \(j\) relative to within-class/template noise, and \(e\) relative to the full-spectrum per-direction semantic mean.

Head dominance requires model-level \(b_{F1}\) above the per-direction mean of F2--F16 and reports whether F1 is the 16-band argmax.

Fine non-head enrichment is

\[
\Delta_{\ell,M}=\log\frac{\operatorname{mean}_{2:8}e_{\ell,\mathrm{fine},k}}
{\operatorname{mean}_{2:8}e_{\ell,\mathrm{coarse},k}},
\]

\[
\Delta_{\ell,T}=\log\frac{\operatorname{mean}_{9:16}e_{\ell,\mathrm{fine},k}}
{\operatorname{mean}_{9:16}e_{\ell,\mathrm{coarse},k}}.
\]

Spectral Pass requires positive lower bounds for both late-layer \(\Delta_M\) and \(\Delta_T\), consistent direction for \(q/j\), sealed templates, three eigenvalue floors, half-split bases, and equal-dimensional random orientations.

### F3. Statistics and controls

- 2,000 parent-to-child-to-template nested bootstrap draws.
- 5,000 hierarchical label permutations.
- 256 equal-dimensional Haar-random subspaces.
- BH-FDR over the 37-by-16 family.
- Leave-one-parent-out analysis.
- Calibration half-split and wrong-layer basis.
- Fine-band projector overlap is reported for all 16 bands. A fine band that rotates across calibration halves cannot support a band-identity claim even if its descriptive heatmap cell is large; broad H/M/T conclusions additionally require the corresponding semantic profile to preserve direction under both half bases.
- Eigenvalue floors \(10^{-6},10^{-5},10^{-4}\lambda_1\).
- Semantic families and children, not 512 sentences, are the statistical units.

### F4. Verdict

- Joint Pass: both Depth and Spectral clauses pass.
- Clause-specific result: report the clause that passes without promoting a joint conclusion.
- Fail: validity gates pass and the corresponding clause does not hold.
- Insufficient: any data, capability, basis, token, numerical, or confirmation guard fails.

## G. Execution And Reproducibility Boundary

### G1. Stages

1. S0: freeze taxonomy, fact bank, texts, model manifest, and calibration manifest.
2. S1: smoke on 2 parents x 2 children x 2 texts and sites 0/12/24/35/36.
3. S2: extract all 512 texts at all sites and run the full-state capability gate.
4. S3: reuse or reconstruct bases; compute 16-band \(b/q/j/e\), bootstrap, permutations, and random nulls.
5. S4: render Figures 0--3 and open every image for visual audit.
6. S5: write summary/detailed and update the anchor's Current Evidence and Claim Boundary.

### G2. Stop rules

Stop interpretation and repair data/engineering if label leakage, readout-position matching, balanced eight-way variables, full-state probes, basis stability, energy reconstruction, or tail-floor sensitivity fails. Do not remove adverse concepts, templates, bands, or random controls.

Failure of an individual near-degenerate tail projector does not erase the depth-discriminability clause, which is basis-free. It restricts that fine cell to descriptive status and makes the spectral clause insufficient unless the registered broad profile remains stable under both independently fitted half bases.

### G3. Required figures

**Figure 0, singular/eigenvalue spectrum:** x is rank 1--4096; y is \(\sqrt\lambda\) or \(\lambda\) on log scale. Show early, middle, late, blocks 35/36, mark all 16 bands, and include a layer-by-normalized-rank spectral heatmap.

**Figure 1, depth trajectories:** x is site 0--36; y shows \(D_{coarse}\), \(D_{fine}\), and \(R_\ell\) with 95% nested-bootstrap intervals. Block 36 is visually separate.

**Figure 2, decisive heatmaps:** rows are 37 sites; columns are F1--F16. Plot coarse, fine, and fine-minus-coarse for each of \(b\), \(q\), and \(j\). Colorbars define units, sign, and limitation.

**Figure 3, selected-layer 16-band curves:** show embedding, early, middle, late, blocks 35/36; coarse/fine colors and uncertainty; mark H/M/T.

Open every figure and inspect axes, units, colorbars, dynamic range, final-layer visibility, and sign readability.

### G4. Artifacts

The worker owns code, raw states, moments, bases, and logs. The Research mainline owns only curated taxonomy/fact/text/model/calibration manifests, compact CSVs, Figures 0--3, `summary.md`, and `detailed.md`.

### G5. Approval scope

Implementation, smoke, and full execution: approved. Publication, graph edits, root sync, commit, and push: not approved.
