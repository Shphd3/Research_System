# A15_17_02_E02 detailed ledger — 2026-09-23

## Question or hypothesis tested

Post-result descriptive supplement to E01: at exact 15B and 17B, do native N8 domain readability, representation geometry, and model-local SAE atom reuse move together across Dense, original S7, fresh S7, and original SALL? E01's registered 17B verdict remains frozen.

## Setup and controlled variables

The [protocol](protocol.md) fixes the two token coordinates, four model roles, native layer-8 attention output after projection and before residual addition, frozen `N8_v1` input, fit/dev/test 2,400/800/1,600, 256 body tokens per record, E01 reader/geometry method, and separate 192-record atom panel. Exact source/checkpoint and panel hashes were frozen in `/data/250010109/MoE_Router/experiments/20260923_sae_n8_15b17b_matrix/manifests/resolved_assets.json`. Only 15B S7, 15B fresh S7, and 17B SALL need new GPU extraction. The other five conditions are completed source caches subject to row and provenance gates. The user selected one single-node `5090-2-spot` direct full run with image `shphd-lite-0911`; a separate new Smoke was explicitly skipped and is recorded as `NOT_RUN_DIRECT_FULL_USER_REQUEST`.

## Data

E01's `N8_v1` panel and exact-17B completed caches; the completed exact-15B Dense/SALL N8 caches; the identical 192-record atom panel (SHA-256 `b561920ed3ce5f89a837019b778d806d1e0db7111b0be5a857d5141c586cc2bc`). Local adapter preflight reconciled all 4,800 15B Dense and SALL records per model against the E01 row IDs, input hashes, source groups, and labels; outputs are under `/data/250010109/MoE_Router/experiments/20260923_sae_n8_15b17b_matrix/runs/local_adapter_preflight/cache`. The prior 15B SALL observer panel also matched 192 sample IDs and input hashes; its descriptive atom reuse was 0.5207409296 before the complete matrix gate.

## Testing or confirmation split

The N8 fit/dev/test split is previously viewed, so all E02 contrasts are post-result descriptive. E01's original 17B registered analysis and intervals are not rerun as a new confirmatory test. The atom reuse panel is separate from the 1,600-record domain test. The four-model LM-loss figure is a separate 0–21B training telemetry comparison, not part of E02's N8 verdict.

## Result

The **GPU extraction completed** for all three missing conditions: 4,800 records and 1,228,800 body tokens each. All worker receipts report frozen state, zero optimizer updates, finite outputs, and `PASS`; every recorded chunk hash was independently rechecked. The original ACP job `pt-xzh1bprs` nonetheless ended `FAILED` at 03:47:16 UTC. Its terminal receipt must remain `FAIL`.

The failure was in post-extraction analysis: the script required the newly computed 15B S7 atom-reuse statistic to equal the separate historical audit within `1e-6`. The first comparison failed for original S7: new eight-record-batch reuse `0.6477477183` versus historical four-record-batch reuse `0.6476181362` (difference `0.0001295821`). Fresh S7 likewise differed by `0.0000551169`. The same checkpoint manifests, 192 sample IDs and input hashes were verified. Unordered token support differed on 14,189/49,152 original-S7 tokens and 14,634/49,152 fresh-S7 tokens; the aggregate reuse difference is small, but exact support reproduction did **not** pass. The different batch shapes are a plausible numerical source, not an isolated causal diagnosis. Full diagnostics are in `reuse_compatibility_audit.json`.

The analysis was corrected to preserve historical four-record-batch atom-reuse values as the reported prior measurements and show the new eight-record-batch values separately as sensitivity. It was rerun **locally on existing caches, with zero new GPU jobs**. The independent `recovery_receipt.json` records `CPU_ONLY_ANALYSIS_RECOVERY: PASS`, source cache `PASS`, alignment `PASS`, and original ACP `FAILED`. This is a post-hoc technical recovery, not a rewrite of the original run or a new confirmatory test. The recovered eight-condition output is `analysis_cpu_recovery_20260923T040000Z`; the artifact manifest hashes its tables and the input cache manifests.

| Exact coordinate | Condition | N8 test accuracy | Effective dimension | Between/within scatter | Atom reuse (192 records) |
| --- | --- | ---: | ---: | ---: | ---: |
| 15B | Dense | 87.3750% | 13.1279 | 0.4639 | N/A |
| 15B | original S7 | 70.1875% | 15.5843 | 0.1015 | 0.6476 (historical batch 4) |
| 15B | fresh S7 | 87.6250% | 17.3553 | 0.3872 | 0.4256 (historical batch 4) |
| 15B | SALL | 87.6875% | 14.7527 | 0.4641 | 0.5207 (completed observer batch 4) |
| 17B | Dense | 87.1875% | 13.7074 | 0.4425 | N/A |
| 17B | S7 continuation | 73.6875% | 7.4958 | 0.1324 | 0.6253 (historical batch 4) |
| 17B | fresh S7 | 88.6250% | 20.7354 | 0.3704 | 0.4050 (historical batch 4) |
| 17B | SALL | 88.3125% | 17.8592 | 0.4279 | 0.5225 (new batch 8) |

All native-vector N8 readouts use the E01 fit/dev/test reader at the same coordinate; the atom-reuse panel is distinct. The 15B original-S7 effective dimension is **higher** than Dense even though its top-16 variance fraction and atom reuse are higher: concentration depends on the chosen statistic. Paired record-bootstrap intervals are in `paired_statistics.json`; E02 intervals are descriptive and do not replace E01's registered verdict.

## Insight, boundary, and next decision

The direct measurements are now available through a bounded CPU recovery. This permits a descriptive eight-condition presentation with the original job failure and atom-batch discrepancy attached. It does not create a new registered verdict, isolated SAE-coefficient effect, broad semantic or model-utility claim, or human mechanism judgment. The next decision is researcher-owned: whether the measured pattern warrants a separate scale/conditioning versus discriminative-direction test. No 5090 rerun is needed for the requested matrix.

## Evidence and failure lineage

| Stage | Evidence | Status | Eligibility impact |
| --- | --- | --- | --- |
| ACP allocation | `pt-xzh1bprs` description; single two-5090 worker | `FAILED` terminal | Do not call original job successful |
| Checkpoint/data preflight | pod log, `resolved_assets.json` | `PASS` | Exact 15B/17B and N8 sources fixed |
| New GPU extraction | three cache manifests and worker chunk hashes | `PASS` | 3 × 4,800 native records reusable |
| Initial analysis | pod traceback line 177 | `FAIL` | No original analysis verdict |
| Atom reproduction audit | `reuse_compatibility_audit.json` | `BOUNDED` | Historical and new batch values are not exactly interchangeable |
| CPU recovery | `recovery_receipt.json`, `recovery_artifact_manifest.json`, alignment receipt | `PASS` | Descriptive matrix usable with named deviation |
| Scientific judgment | researcher response | `AWAITING_RESEARCHER` | No mechanism/Anchor transition |

Raw source to computation: immutable old/new NPZ caches → `analyze_matrix.py` using E01's fixed fit/dev/test reader and geometry → `primary_metrics.json`, `paired_statistics.json`, `atom_reuse.json` → `recovery_artifact_manifest.json`. The 192-record atom panel is identified by SHA-256 `b561920ed3ce5f89a837019b778d806d1e0db7111b0be5a857d5141c586cc2bc`. Original failure and local recovery are preserved separately under the same execution workspace.
