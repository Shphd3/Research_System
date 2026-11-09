---
experiment_id: A15_11_E01_qwen_native_router_access_gap
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-29
---

# Detailed: Qwen Native Router Accessibility Chain

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
Frozen Protocol: [protocol.md](protocol.md), SHA-256
`658528da0c3388c49f14917c01e8eacda7c7a3c06e1cec511540d8fb65fd2fcf`
Summary: [summary.md](summary.md)

## 0. Quick Recap

- **Question:** where is eight-way parent-label accessibility lost along the
  exact frozen \(H\rightarrow Z\rightarrow Q\) Router interface?
- **Direct result:** four of five fixed confirmation blocks pass the same
  projection-preserved, material-selection-loss, and retained-association rule
  in both C4 and C5.
- **Machine verdict:** `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION`.
- **Boundary:** static semantic accessibility and expert utility are different
  objects.

## 1. Objects And Metrics

| Object | Concrete meaning | Unit / computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| \(H\) | 2,048-dimensional native MoE input at the final decision token | BF16-quantized hidden vector | available parent-label accessibility | native use |
| \(Z\) | 128 native bias-free Gate logits | \(W_gH\) in BF16 | Gate-row-space visibility | useful experts |
| \(Q\) | renormalized weights on the native top eight experts | 128-vector with eight nonzeros | deployed sparse interface | lower LM loss |
| balanced accuracy | mean recall over eight balanced parents | fraction in \([0,1]\) | primary held-out readability | calibration or causality |
| \(D_{proj}\) | accessibility lost at projection | \(BA(H)-BA(Z)\) | projection bottleneck | functional loss |
| \(D_{select}\) | accessibility lost at sparsification | \(BA(Z)-BA(Q)\) | selection bottleneck | why training formed it |
| route association | label--expert weighted mutual information | \(I_Q(Y;E)/H(Y)\) | matched-null association | expert utility |

## 2. Actual Setup

- **Model:** frozen `/data/share/Qwen3-30B-A3B`; exact configuration, index,
  and six Gate tensor hashes matched the Protocol.
- **Blocks:** 4, 12, 20, 28, and 36 are confirmation blocks; Block 44 remains
  visible but pilot-only.
- **Panels:** C4 and C5 are reported separately and required to agree. Each has
  30 complete template families, eight parents, and eight children per parent.
- **Split:** A-to-B and B-to-A cross-fitting over 15 disjoint complete families
  per half.
- **Readout:** matched multinomial L2 linear probes with train-only five-fold
  regularization selection; family-paired 10,000-draw bootstrap.
- **Null:** 1,000 within-family complete-parent label permutations with a
  max-layer statistic.
- **Numeric path:** BF16 \(H\) and Gate multiplication on RTX 5090, FP32 softmax,
  native top eight and renormalization. Original FP32 hidden states form only
  the sensitivity path.
- **Resource:** exactly eight NVIDIA GeForce RTX 5090 devices; no H100 result is
  part of this evidence.

## 3. Registered Criteria And Result

A cell preserves projection only when the lower 95% bound of chance-corrected
\(Z\) retention is at least 0.90 and the upper 95% bound of \(D_{proj}\) is at most
0.05. Selection loss is material when the lower 95% bound of \(D_{select}\) is
at least 0.10. Association is retained only above the matched max-layer null.
At least four of five blocks must pass all three conditions in both panels.

| Block | C4 \(D_{proj}\) | C4 \(D_{select}\) | C5 \(D_{proj}\) | C5 \(D_{select}\) | Cross-panel status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 4 | 0.0021 | 0.4344 | 0.0016 | 0.4620 | pass all three |
| 12 | 0.0057 | 0.4943 | 0.0047 | 0.5036 | pass all three |
| 20 | 0.0130 | 0.5651 | 0.0141 | 0.5484 | pass all three |
| 28 | 0.0281 | 0.5667 | 0.0349 | 0.5130 | pass all three |
| 36 | 0.0557 | 0.5349 | 0.0438 | 0.5026 | C4 projection not preserved |

Every confirmation cell has hidden accessibility above null, material
selection loss, and retained route association. Projection is preserved in
both panels at four blocks. Near-total sparse retention fails at all five.

## 4. BF16/FP32 Sensitivity

The primary and sensitivity paths return the same line verdict. Exact top-eight
set agreement ranges from 0.9323 to 0.9891 over the confirmation cells, while
mean Jaccard ranges from 0.9850 to 0.9976. Near-ties therefore change some
individual expert IDs without changing the registered scientific conclusion.

The full producer result, layer metrics, null ledger, bootstrap ledger,
conditional-fine ledger, and decompressed prediction CSV were reproduced in
two independent 8×RTX5090 attempts. The gzip container hash changed because of
container metadata; decompressed prediction bytes match SHA-256
`1694eb8e57605152c48f18a845353f49e685dcc449434620516dd3558b05bc42`.

## 5. Visualization Audit

![Held-out accessibility ladder](figures/balanced_accuracy_ladder.png)

The black \(H\) and blue \(Z\) curves remain near one; the red \(Q\) curve falls to
0.40--0.56 at confirmation blocks. Block 44 is gray and pilot-only.

![Projection and selection gaps](figures/accessibility_gaps.png)

The blue projection gaps are small through Block 28, while red selection gaps
are large at every confirmation block. The plot supports interface
localization, not a causal explanation.

![Parent-by-expert native route loads](figures/parent_expert_load_heatmaps.png)

The heat map is descriptive. It shows concentrated expert columns and bounded
parent-dependent changes, but it cannot identify expert function. The pilot
label around Block 44 is visually crowded; no decision depends on that panel.

## 6. Execution And Provenance

| Attempt | Run stamp / job | Outcome | Scientific status |
| --- | --- | --- | --- |
| 1 | `20260829T170740Z` / `pt-s3k4gytd` | runtime activation stopped before scientific inputs | no evidence |
| 2 | `20260829T171220Z` / `pt-gwwxjpyw` | CPU probe workers deadlocked in nested thread-pool control; stopped | no Qwen result |
| 3 | `20260829T172018Z` / `pt-3dndd5hl` | E01 completed; E03 later stopped on projection precision | eligible E01 producer evidence |
| 4 | `20260829T180400Z` / `pt-0aopddjj` | E01 reproduced; all science landed; root CSV audit later crashed | canonical E01 evidence |

Attempt 4's remote job state is `FAILED` because the root completion reader hit
Python's default 128-KiB CSV field limit after all producer artifacts existed.
A test-first post-run reader fix admitted the existing immutable artifacts; the
root completion audit now passes. This changed no E01 result, threshold, input,
or producer artifact.

Canonical worker evidence:
`/data/250010109/MoE_Router/experiments/20260829_a15_11_gradient_consistent_hierarchical_routing/runs/full-20260829T180400Z/qwen/`.
The root completion receipt records 36 required artifacts and separate Qwen and
synthetic verdicts.

## 7. Interpretation And Boundary

**Direct evidence:** a linear probe can almost perfectly recover parent labels
from \(H\) and \(Z\), but not from \(Q\); \(Q\) nevertheless retains label association
above null.

**AI interpretation awaiting human confirmation:** the native Gate row space
is not the main semantic-access bottleneck in the registered layers; sparse
top-eight selection is. This does not determine whether the discarded
accessibility was functionally useful.

**Cannot claim:** pretraining mechanism, causal native semantic use,
counterfactual utility, natural hierarchy discovery, or Qwen loss improvement.

## 8. Resume Point

Read this result together with E03 only at the claim-boundary level. E01 says
where one semantic label is lost; E03 says when a controlled expert function
can or cannot be represented. A real-model successor must execute equal-compute
candidate experts and test utility conditional on the Router-visible state.
