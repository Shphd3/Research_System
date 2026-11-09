# A15_17_02_E02: exact 15B/17B N8 four-model matrix

Document state: `AUTHORIZED_DIRECT_FULL_DESCRIPTIVE_SUPPLEMENT`.
Researcher instruction (2026-09-23): complete the four-model N8 representation comparison at both exact 15B and 17B; submit the missing full read-only extraction directly on one two-RTX5090 Spot node. Separate new Smoke status: `NOT_RUN_DIRECT_FULL_USER_REQUEST`.

This is a post-result descriptive supplement. The [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md) and [E01 protocol](../A15_17_02_E01_n8_17b_separability_audit/protocol.md) own the original registered hypothesis and decision rule. E01's fresh−Dense `INSUFFICIENT` and reweighted−fresh `REWEIGHTED_LOWER_THAN_FRESH` verdicts remain fixed.

## Purpose and hypothesis

Describe, at each matched token checkpoint, whether SAE-associated native attention representation concentration, N8 domain readability, and atom reuse move together. The working hypothesis is that stronger SAE pressure concentrates native representations and atom selection, and might improve domain separation. A rival is that concentration compresses domain-discriminating directions and harms readability. This matrix distinguishes observed directions, but distinct training histories, sidecar topologies, and microbatch settings prevent an isolated causal conclusion.

## Conditions and frozen input

At each of exact 15B and 17B compare Dense, original S7, fresh S7 coefficient 0.1 from initialization, and original all-eight-layer SALL. Original S7 is coefficient 1 at 15B and the 1→0.1 reweighted continuation at 17B. Never label these as a single constant-coefficient trajectory. Read the native layer-8 attention output after output projection and before residual addition, averaged over 256 body tokens, on frozen `N8_v1`: fit/dev/test 2,400/800/1,600 records. Reuse completed exact-15B Dense/SALL caches and exact-17B Dense/fresh S7/reweighted S7 caches only after row ID, input hash, mask hash, group, label, split and checkpoint provenance checks. Newly extract only 15B fresh S7, 15B original S7, and 17B SALL. No training or checkpoint mutation.

## Analysis method

1. Apply E01's fit-only centering and global RMS scale, L2 multiclass logistic probe (`C=0.01,0.1,1,10,100` chosen on dev), and test accuracy on 1,600 records. Compute paired class-stratified record-bootstrap intervals (2,000 draws) for within-coordinate comparisons. These are post-result descriptive intervals, not new registered tests.
2. On the same test native vectors, report effective dimension, top-16 variance share, between/within scatter ratio (the stated Fisher-like ratio), and five-seed K-means ARI. An omnibus Fisher criterion with a different denominator is not interchangeable with this ratio.
3. On the distinct frozen 192-record N8 observer panel, compute model-local atom-selection-frequency cosine reuse for the layer-8 SAE, plus distinct/effective atoms. Dense has no SAE and is N/A. Reuse existing eligible 15B/17B atom-selection evidence only after panel identity checks; extract 17B SALL selections in this job. The 192-record reuse statistic and 1,600-record test geometry must be labeled as different panels.

## Outcome branches and boundaries

- If lower effective dimension or higher reuse accompanies higher accuracy and Fisher-like ratio at both coordinates, report descriptive consistency with the working hypothesis, not causal confirmation.
- If more concentrated conditions have lower accuracy or Fisher-like ratio, reject concentration as a monotonic proxy on these checkpoints.
- If rows fail identity/alignment/finite/immutability checks, mark them `INELIGIBLE`; if directions disagree or intervals span zero, record `INSUFFICIENT` for that descriptive relation. Do not substitute nearby checkpoints.

No N8 result establishes broad semantic quality, model use of the information, language-model performance, or training speed. Training-loss curves are a separate telemetry comparison at common valid-token coordinates and retain their lineage/order qualifications.

## Execution and receipts

One single-node `5090-2-spot` ACP task, `shphd-lite-0911` image and mounted SM120 runtime, through `templates/execution/acp_submit_template.sh`. First wave reads the two 15B S7 roles on separate GPUs; second wave splits the 17B SALL role across both GPUs. Each worker must check exact model/source identity, 5090 device, frozen native site, finite arrays, 256 tokens per record, zero optimizer updates, and sampled state before/after. The full runner validates every cache and writes a durable terminal receipt and artifact manifest. No fallback profile, automatic retry, commit, push, or publication.

Execution workspace: `/data/250010109/MoE_Router/experiments/20260923_sae_n8_15b17b_matrix`. New role caches, legacy adaptation and source hashes, alignment receipt, metrics, predictions, atom reuse, failures, stage gate, terminal receipt, and ACP certificate belong there. This protocol's execution approval does not set a human mechanism judgment or alter the Anchor.
