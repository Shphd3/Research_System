# Protocol: A15_07_E02 Fixed-Axis and Learned Low-Rank Domain Atlas

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: researcher explicitly approved Protocol, implementation, smoke, full execution, figures, and concise meeting synchronization on 2026-08-20
Block audit status: A=CONFIRMED B=CONFIRMED C=CONFIRMED D=CONFIRMED E=CONFIRMED F=CONFIRMED G=CONFIRMED
Cross-block consistency: PASS
Execution scope approved: protocol + local implementation + tests + sealed C5 construction + smoke + full extraction + full analysis + three registered figures + canonical result records
Execution scope excluded: Router implementation or evaluation, graph edit, root sync, commit, push, publication, and delayed daily report
Purpose: identify where each domain's fine-class function appears in three frozen spectra and in a freely learned low-rank space
Primary object: native-coordinate candidate attention update R_U at Qwen3-8B blocks 24 and 28
Primary metric: paired held-out cross-entropy gain over the old-state-only classifier, in nats/example
Strongest rival: a low-dimensional classifier may generalize while no fixed spectral basis gives stable axes; alternatively neither method survives new expressions
Claim boundary: one frozen model, two blocks, eight registered domains, linear residualization/readouts, and one controlled unseen-expression population
Approval decision: RUN; this Protocol is the execution contract
```

The researcher-confirmed [active Focus](../../../../../../../daily_research_reports/backup/2026/08/0820/focus_layerwise_domain_direction_atlas.md)
states the same design in plain language. The linked
[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/subanchors/15_07_01_layerwise_domain_direction_atlas_anchor.md)
owns the research boundary. This Protocol does not refer to a person-defined
method: every analysis is defined below by its computation.

## 1. Block A — Question, Object, and Decision

### A1. Single question

At blocks 24 and 28, for each of eight parent domains, which frozen spectrum,
which axes, and what minimum subspace dimension stably carry its within-domain
eight-way fine-class function on unseen expressions? Conditional on held-out
function, which components are reused across domains and which are
domain-specific candidates?

### A2. Long-term relation

The long-term aim is a low-rank layerwise Router. This experiment does not test
a Router. It decides whether the representation supplies a stable, layerwise,
low-dimensional input signal worth testing in a later Router experiment.

### A3. Representation object

For layer \(\ell\), let \(X_\ell\) be the registered normalized state immediately
before the attention write and \(U_\ell\) the same-token attention update. A
TRAIN-fitted affine predictor removes the part of \(U_\ell\) linearly predictable
from \(X_\ell\):

\[
R_{U,\ell}=U_\ell-(X_\ell A_\ell+b_\ell).
\]

Fixed-axis spectral analyses use native-coordinate \(R_U\). Classification heads
standardize their selected coordinates using TRAIN means and scales. The
freely learned low-rank comparison uses the already frozen TRAIN-standardized
\(R_U\) and maps its input modes back to native coordinates before spectral
localization. \(R_U\) is a candidate update, not proof of new knowledge.

### A4. Adjudication unit

The smallest verdict-bearing unit is one `(layer, domain)` pair. The final
atlas must contain all \(2\times8=16\) pairs. A global summary may count types,
but no average may replace a missing domain-level outcome.

## 2. Block B — Data, Splits, and Leakage Contract

### B1. Existing construction and development data

Use the exact registered eight-domain by eight-fine-class hierarchy and the
E03 construction/development split. Each split contains ten examples per
domain-by-fine-class cell. Construction data may fit residualizers, feature
scales, direction scores, and classifier heads. Development data may choose
ridge strength and the smallest registered dimension. Neither may contribute
to the final confidence interval.

### B2. New C5 unseen-expression confirmation bank

Before any C5 activation is computed, create and seal exactly
\(8\times8\times30=1,920\) rows. C5 reuses the six registered source
propositions per fine class so that the changed variable is expression, but it
uses new sentence frames, proposition orders, template IDs, combination IDs,
record IDs, and prompt hashes. The final question remains:

```text
Determine the broad academic field and its specific subfield.
Classification:
```

The builder must verify all of the following before sealing:

- 64 balanced cells and 30 rows per cell;
- no duplicate normalized C5 text or record ID;
- zero normalized-text, template-ID, combination-ID, or record-ID overlap with
  construction, development, C3, C4-expression, and C4-atom;
- no explicit parent or fine-class label in the description body;
- deterministic generation from the registered seed and source atoms;
- SHA-256 receipts for source files, rows, manifest, builder, Protocol, model,
  and frozen analysis code.

C5 is opened once after the freeze receipt. It never selects axes, dimensions,
ridge values, thresholds, plotting subsets, or interpretation wording. A
failed audit makes the experiment `INSUFFICIENT`; C5 may not be regenerated
after activations or predictions are visible.

### B3. What C5 can establish

C5 tests unseen-expression stability with fixed source propositions. It does
not test new facts, natural language populations, unseen parent domains, or
new fine classes.

## 3. Block C — Frozen Model, Hooks, and Three Spectral Rulers

### C1. Model and hooks

- model: frozen `/data/share/Qwen3-8B`, evaluation mode, `use_cache=False`;
- width: 4,096, verified at runtime;
- layers: blocks 24 and 28 only;
- hook, decision token, residualizer, feature standardizer, old-state
  classifier, and full-\(R_U\) classifier: exact frozen E03
  construction/development artifacts; the freely learned low-rank comparison
  reuses the same frozen data and fitting logic but is refit before C5 in an
  explicit seven-dimensional orthonormal contrast basis;
- no language-model, Router, expert, or adapter parameter is updated.

### C2. Local parameter-response spectrum

For each tested layer, let \(W_g\) and \(W_u\) be its frozen MLP gate and up
projection matrices. Form

\[
K_\ell=W_g^\top W_g+W_u^\top W_u=V_\ell\Lambda_\ell V_\ell^\top.
\]

Eigenvectors are ordered by decreasing eigenvalue. Rank 1 is the direction to
which that layer's MLP input maps with the greatest squared response. This is
a parameter-response spectrum, not an activation-variance spectrum.

### C3. Mean-response common parameter spectrum

Use the already frozen trace-normalized mean MLP-response operator across all
layers and its full \(4,096\times4,096\) orthonormal eigensystem. Eigenvectors
are ordered by decreasing mean response. It supplies one common coordinate
system for comparing blocks and domains.

### C4. Large-sample activation spectrum

Use the already frozen top-500 PCA vectors of centered final-block states fit
on 131,072 DCLM TRAIN tokens. Rank 1 has the largest activation variance. Only
the identified top-500 span supports an axis-level claim. Its orthogonal
complement is reported as one unresolved bin. The previous million-token run
evaluated this basis on more tokens; it did not fit 4,096 PCA axes from one
million tokens.

### C5. Numerical-rank contract

All eigensystems and singular-vector spaces use float64 decomposition. A
singular/eigen mode is numerically retained when its value exceeds

\[
\tau=\epsilon_{64}\max(n,d)\sigma_{\max}.
\]

If an identified span cannot supply a requested rank, that condition is
`INSUFFICIENT`; no zero padding or invented complement basis is allowed.

## 4. Block D — Two Direction-Finding Methods

### D1. Fixed-axis discriminant selection

For domain \(p\), fine class \(c\), example \(i\), and one frozen orthonormal basis
\(V=[v_1,\ldots,v_D]\), define class and domain means from construction data and

\[
B_p=\frac1{8}\sum_c(\mu_{pc}-\mu_p)(\mu_{pc}-\mu_p)^\top,
\]

\[
W_p=\frac1{8}\sum_c\frac1{n_c}\sum_i
(r_{pci}-\mu_{pc})(r_{pci}-\mu_{pc})^\top.
\]

Each frozen axis receives the score

\[
s_{pj}=\frac{v_j^\top B_pv_j}{v_j^\top W_pv_j+\rho_p},
\qquad
\rho_p=10^{-2}\frac{\operatorname{tr}(W_p)}{4096}.
\]

In plain language, an axis ranks high when fine classes have separated means
but repeated expressions of the same class fluctuate little. Ties use smaller
spectral rank. The entire procedure is repeated at \(10\rho_p\) as the frozen
small-denominator stress test.

For \(k\in\{1,2,4,8,16,32,64\}\), retain the top-\(k\) scored axes, standardize
their coordinates from construction data, and fit a ridge correction to the
residual centered one-hot target after a five-fold out-of-fold \(X\)-only
classifier. Ridge is selected on development cross entropy from
\(\{10^{-8},10^{-7},\ldots,10^2\}\); ties choose the stronger ridge.

For each `(layer, domain, basis)`, development chooses the smallest \(k\) whose
gain reaches at least 90% of development full-\(R_U\) gain. If no \(k\le64\)
crosses, the condition is recorded as `NO_COMPACT_CROSSING`; \(k=64\) remains a
descriptive curve endpoint and cannot be promoted post hoc.

### D2. Freely learned supervised low-rank space

Use the same reduced-rank ridge correction previously learned from standardized
\(R_U\), refit on the frozen construction/development rows before C5 is opened.
To prevent floating-point leakage into a redundant eighth output coordinate,
map every centered eight-logit correction target through a fixed orthonormal
Helmert contrast matrix \(C\in\mathbb R^{8\times7}\), fit in seven contrast
coordinates, and map predictions back with \(C^\top\). Requested ranks are
\(\{1,2,4,7\}\). Rank seven is the maximum independent contrast rank for eight
classes and is therefore a full task-contrast ceiling, not evidence of useful
low rank. Development chooses the smallest rank reaching 90% of development
full-\(R_U\) gain.

The ordered native-coordinate input modes are obtained by undoing TRAIN
feature scaling in the frozen coefficient map and taking its ordered SVD.
These modes can be localized in each frozen spectrum, but their individual
semantic signs are descriptive; the low-rank subspace is the invariant
functional object.

### D3. Relationship between the methods

The fixed-axis method asks whether named axes of a frozen spectrum suffice.
The learned low-rank method asks whether some freely rotated low-dimensional
space suffices. Agreement supports a basis-explicit atlas. Learned-only success
supports low-dimensional function but rejects a fixed spectral-axis rule.
Neither method is treated as ground truth for the other.

## 5. Block E — Controls, Metrics, and Uncertainty

### E1. Full-access admission gate

For each C5 row \(i\), the functional unit is

\[
g_i^{(m)}=CE(f_X(x_i),y_i)-CE(f_X(x_i)+f_m(r_i),y_i)
\]

in nats per example. Positive values mean the candidate update lowers loss
beyond the old state. The full-\(R_U\) condition must beat both:

- duplicate-\(X\): apply the registered update path to duplicated old-state
  information;
- mismatched-\(R_U\): pair each row with another row's update inside the same
  domain under 64 registered derangements.

Admission requires the simultaneous lower confidence bound of full gain minus
the larger control q95 to exceed zero. All downstream retention and semantic
labels are `NOT_APPLICABLE` when this gate fails.

### E2. Fixed-axis controls

At every registered \(k\), compare selected axes with:

1. the first \(k\) spectral axes;
2. same-\(k\) axes sampled uniformly without replacement from the identified
   basis, using 64 registered draws at the development-selected \(k\) and 16
   draws elsewhere for curves;
3. 64 within-domain fine-class label permutations that rerun scoring,
   dimension selection, standardization, and head fitting end to end.

The activation-PCA controls sample only inside the identified top-500 span.
All controls use the same splits, ridge grid, and evaluation rows.

### E3. Learned-space control

Use 64 within-domain label permutations that refit the full low-rank pipeline
on construction/development data. Geometric localization also reports 1,000
same-rank Haar subspaces inside the exact identified spectrum, but this Haar
comparison is descriptive and cannot substitute for held-out classification.

### E4. Aggregation and intervals

Report each domain separately. Within a domain, average rows equally inside
each of the eight fine classes and then average classes equally. Generate 2,000
paired bootstrap draws by resampling rows with replacement inside each
domain-by-fine-class cell. Identical bootstrap weights are reused across all
paired conditions.

One-sided simultaneous 95% bounds use a max-statistic family across both
layers, all eight domains, all registered bases, and all positive qualification
statements in the corresponding hypothesis family. A missing denominator in
more than 5% of draws makes retention `INSUFFICIENT`; ratios are never clipped,
smoothed, or repaired.

Retention for condition \(m\) is

\[
\operatorname{Retain}^{(m)}=
\frac{\overline g^{(m)}}{\overline g^{(full)}}.
\]

It measures accessible linear classification function relative to the full
candidate update. It does not measure reconstruction or native causal use.

## 6. Block F — Frozen Verdict Rules and Atlas Semantics

### F1. Fixed-basis qualification

One `(layer, domain, basis)` qualifies only if all are true on C5:

- full-\(R_U\) admission passes;
- development-selected \(k\le16\);
- simultaneous retention LCB \(>0.80\);
- gain minus the maximum of spectral-head, random-axis q95, and permutation
  q95 has simultaneous LCB \(>0\);
- under \(10\rho_p\), the same inequalities hold and the selected top-\(k\) axis
  set has Jaccard overlap at least 0.50 with the primary selection.

Failure of a bounded inequality is `FAIL`; an interval crossing a boundary or
a numerical/data guard failure is `INSUFFICIENT`.

### F2. Learned low-rank qualification

One `(layer, domain)` learned space qualifies only if full admission passes,
the development-selected effective rank is at most four, simultaneous
retention LCB \(>0.80\), and gain minus permutation q95 has simultaneous LCB
\(>0\). Rank-seven-only success is reported separately as
`FULL_CONTRAST_ONLY`.

### F3. Per-domain-layer type

Assign exactly one type to every `(layer, domain)` pair:

| Type | Meaning |
| --- | --- |
| `STABLE_BASIS_ROBUST` | learned space qualifies and at least two of three fixed bases qualify |
| `STABLE_BASIS_SENSITIVE` | learned space qualifies and zero or one fixed basis qualifies |
| `STABLE_FIXED_ONLY` | at least two fixed bases qualify but the learned-space qualifier does not |
| `STABLE_FULL_CONTRAST_ONLY` | no compact qualifier; rank seven alone qualifies |
| `NO_STABLE_COMPACT_DIRECTION` | full access is admitted but all compact methods boundedly fail |
| `NO_ADDED_FUNCTION` | full-\(R_U\) admission boundedly fails |
| `INSUFFICIENT` | a required interval, data, identity, or numerical guard is unresolved |

The global result is `BASIS_ROBUST_ATLAS` only if at least five of eight
domains at the same layer are `STABLE_BASIS_ROBUST`. It is
`LEARNED_LOW_RANK_ONLY` if at least five learned spaces qualify at one layer
but fewer than five are basis-robust. Otherwise the result is `MIXED`,
`NEGATIVE`, or `INSUFFICIENT` according to the 16 typed rows. The full table,
not the global label, answers the research question.

### F4. Shared and domain-specific candidates

Labels are assigned inside each frozen basis and layer only after F1:

- **shared candidate:** the same basis axis is independently selected for at
  least two qualifying domains, and its held-out one-axis marginal gain has a
  simultaneous LCB above zero in every participating domain;
- **domain-specific candidate:** selected for exactly one qualifying domain,
  and the simultaneous LCB of its own-domain marginal gain minus its maximum
  cross-domain marginal gain and fixed zero is above zero;
- **unresolved:** every other selected or nearby axis.

Cross-basis subspace overlap is reported, but axes from different bases are
not declared identical merely because their spectral ranks are similar.

### F5. Fine-class information fingerprint

For each qualifying fixed axis, orient its sign so that the fine class with the
largest absolute C5 mean has positive mean. Report all eight class means after
division by the pooled within-class standard deviation, plus the highest and
lowest classes. For a learned input mode, report the analogous ordered-mode
fingerprint but state that rotations within a nearly tied subspace are not
unique. These are task-label contrasts, not proof of intrinsic natural-language
semantics.

### F6. Spectral localization of the learned space

For a learned rank-\(r\) native input basis \(Q\), the energy in contiguous
spectral band \(b\) is

\[
e_b=\frac{\lVert V_b^\top Q\rVert_F^2}{r}.
\]

The two full parameter spectra use 16 contiguous rank bands with sizes
differing by at most one. The activation spectrum uses eight bands inside its
top-500 span plus one unresolved-complement bin. Report energy minus the
matched Haar median and q95. This answers where a learned low-rank classifier
lies relative to each spectrum; it does not make location functional without
F2.

## 7. Block G — Procedure, Artifacts, Figures, and Stop Rules

### G1. Stage contract

| Stage | Input visible | Required output | Stop condition |
| --- | --- | --- | --- |
| 0. Freeze | Protocol, source artifacts, code, no C5 activations | receipt with hashes and environment | any missing/changed source |
| 1. Build C5 | registered atoms and old metadata text only | sealed rows, manifest, zero-overlap audit | any audit failure |
| 2. Test and smoke | synthetic unit cases, then at most 16 C5 rows | passing tests and shape/identity receipt | mismatch, nonfinite values, wrong hook |
| 3. Extract | sealed 1,920 C5 rows | native/standardized \(X,U,R_U\) arrays for both layers | row/order/hash mismatch or nonfinite data |
| 4. Analyze | construction/development plus frozen C5 arrays | all registered curves, controls, intervals, 16-row verdict table | no post-C5 refit or rule change permitted |
| 5. Render and record | frozen analysis tables only | three figures, `summary.md`, `detailed.md` | figure-source mismatch |

Any code or rule change after C5 predictions are visible requires an amendment
record stating whether it is purely mechanical. A scientific change creates a
new experiment ID; it cannot overwrite E02.

### G2. Registered figures

1. **Functional dimension curves:** C5 retention versus dimension for all
   three fixed bases and the freely learned low-rank space, faceted by layer
   and domain, with full-access and controls visible.
2. **Direction and spectral-band atlas:** selected fixed axes plotted at their
   spectral ranks, with learned-space band energy underneath; nonqualifying
   points are gray and cannot be read as semantic directions.
3. **Shared/specific and fine-class fingerprint:** within-basis domain overlap
   matrix plus the eight-class response fingerprints of only qualified axes.

Every figure must name its question, unit, rows, aggregation, allowed
conclusion, and limitation in its caption. The rendered PNG/PDF is visually
audited against its source table before delivery.

### G3. Canonical outputs

Research records:

```text
Projects/from-attention-to-search/main/experiments/A15/
  15_07_layerwise_conditional_fine_discriminant_directions/
  A15_07_E02_fixed_axis_and_learned_subspace_atlas/
    protocol.md
    summary.md
    detailed.md
    figures/
    tables/
```

Worker root:

```text
/data/250010109/MoE_Router/experiments/
  20260820_a15_07_e02_fixed_axis_low_rank_atlas/
```

The worker owns code, raw arrays, logs, receipts, and complete intermediate
tables. `summary.md` and `detailed.md` own the canonical evidence reading path.
No daily research report is written until the researcher supplies or approves
the actual result, boundary, and next decision in the active Focus.

### G4. Resources and command boundary

Execution may use the currently visible H100-class GPU, automatic mixed
precision for model extraction, float32 stored activations, and float64
analysis. Batch size may be lowered after an out-of-memory error without a
scientific amendment; row order, hooks, arrays, and predictions must remain
identical. Resource changes cannot alter data, precision of the final analysis,
or registered rules.

### G5. What the experiment cannot claim

No outcome establishes native causal use, new knowledge, universal semantic
directions, Router quality, expert usefulness, expert specialization, load
balance, LoRA behavior, resistance to forgetting, or transfer beyond the
registered model, layers, task, and expression population.

## 8. Confirmation and Freeze Ledger

| Block | Status | Frozen content |
| --- | --- | --- |
| A | `CONFIRMED` | one atlas question, native \(R_U\), domain-layer adjudication |
| B | `CONFIRMED` | old construction/development, sealed C5 expression bank |
| C | `CONFIRMED` | model, hooks, local/common/activation spectra |
| D | `CONFIRMED` | fixed-axis score and freely learned low-rank comparison |
| E | `CONFIRMED` | functional gate, controls, aggregation, simultaneous uncertainty |
| F | `CONFIRMED` | per-domain types, shared/specific and semantic boundaries |
| G | `CONFIRMED` | stages, three figures, outputs, resources, execution scope |

Final cross-block audit: `PASS`. The methods answer the Anchor's question on
the registered data; controls target small denominators, PCA-head preference,
arbitrary low rank, old-state duplication, mismatch, and expression
overfitting; the figures are derived only from verdict-bearing tables; the
claim boundary does not promote representation diagnostics into a Router
result.

## 9. Append-Only Full-Run Receipt

```text
Execution status: FULL_RUN_COMPLETE
Completion date: 2026-08-21
Executed scope: sealed C5 build + smoke + 1,920-row two-layer extraction + full registered analysis + learned-overlap completion + three registered figures + canonical result records
Scientific body changed after freeze: no
Formal extraction passed: true
Formal analysis passed: true
Domain-layer rows complete: 16 / 16
Registered PNG/PDF figures complete: 6 / 6
Supplemental spectral-curve PNG/PDF files complete: 12 / 12
```

The frozen scientific-body receipt is
`/data/250010109/MoE_Router/experiments/20260820_a15_07_e02_fixed_axis_low_rank_atlas/frozen/freeze.json`
(SHA-256 `532a257852e4ab6b324e8c2146cc079416f25191d5925d1b9d42cc508562d029`).
The sealed data manifest, formal extraction manifest, result manifest, and
analysis payload have SHA-256 values
`cdd4d5600a12fa7169cd56af61a97c35167e07985e6c622ec6d7a855737ca013`,
`e09566daac22db37fdf8935fc1118fa8a107f9607b788b7332a40aa7696a6e8c`,
`307ee4b62051fd2e2bcf6b031bda653d360fc4f53f666c8ddd03e534c8957c32`,
and `7dab27ab7ab839cd3abc1d0a8caa91fcd59412b88dd327efbcbf88cf46201780`
respectively. The formal activation array has shape
`(2, 1920, 2, 4096)` and SHA-256
`f1675a666272ef831cbd7f1fb52b7d9744aee95e0c7f24e0665db187118c9f41`.

Results: [summary](summary.md), [complete evidence](detailed.md),
[Chinese self-contained explanation](detailed_cn.md), and
[concise meeting synchronization](meeting_sync_cn.md). Amendments 001, 002, and
003 are recorded on the worker and are mechanical only; none changes a frozen
scientific rule or result eligibility. Amendment 003 renders the same frozen
spectral-energy table as six individual curves plus the six-panel overview.
