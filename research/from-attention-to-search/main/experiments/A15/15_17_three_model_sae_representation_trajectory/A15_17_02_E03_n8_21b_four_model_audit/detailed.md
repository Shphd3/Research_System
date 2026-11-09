# A15_17_02_E03 detailed ledger — 2026-09-23

## Question or hypothesis tested

Does the already observed 15B/17B relationship among native representation concentration, N8 domain readability, and SAE atom reuse persist at the exact 21B checkpoint across Dense, S7, Fresh S7 and SALL? This is a descriptive extension of [E02](../A15_17_02_E02_n8_15b17b_matrix/detailed.md), not a new registered verdict.

## Setup and controlled variables

The [protocol](protocol.md) fixes the same `N8_v1` input, native layer-8 attention write and body-mean reader. The four checkpoints are exact 21B milestones. Three old 21B cache sets are reused only after terminal, chunk-hash, checkpoint and row-alignment gates; only Fresh S7 requires new GPU extraction. The separate 192-record atom panel uses four-record batches for all three SAE roles.

## Data

`N8_v1` fit/dev/test contains 2,400/800/1,600 records, each with 256 body tokens. Existing Dense, S7 and SALL caches came from the previously completed 21B three-model audit. Local preflight of the adaptation read all 4,800 records per model and passed alignment of sample IDs, input hashes, source groups and labels to E01's frozen reference. Existing S7 and SALL atom selections each matched all 192 panel IDs and hashes. Fresh S7's complete exact-21B milestone manifest was verified; its full state-file hash is checked inside the submitted job before extraction.

## Testing or confirmation split

The fit/dev/test split and old 21B outputs have been viewed before this extension. Every E03 interval is therefore post-result descriptive. E01's original registered 17B result remains unchanged; model utility, broad semantic quality and training efficiency are outside this audit.

## Result

`NOT RUN` at this ledger checkpoint. One read-only full task, `pt-u0hqi0v9`, was submitted at 2026-09-23 05:14:44 UTC on `5090-2-spot` and was `QUEUEING` at 05:15 UTC. The exact command and resource tuple are in the [execution certificate](/data/250010109/MoE_Router/experiments/20260923_sae_n8_21b_four_model_audit/submissions/execution_certificate.md). No scientific result or mechanism judgment is recorded from submission.

## Insight, boundary, and next decision

The current evidence supports only feasibility of the 21B read: all four exact checkpoint manifests exist, old three-role caches passed local alignment, and the single missing role was submitted. Await the job's terminal receipt, then audit its worker hashes, alignment receipt, metric JSON and any failure before interpreting 21B. The researcher's mechanism judgment and next scientific decision remain open.
