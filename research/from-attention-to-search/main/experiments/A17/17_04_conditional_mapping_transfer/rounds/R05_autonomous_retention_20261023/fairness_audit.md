# R05 fairness and numerical audit

Snapshot: 2026-10-22T17:46:07.547181+00:00. State: `COMPLETE`.

89 of 89 queue-defined formal cases have completion evidence. This audit checks exposure, capacity, saved-state lineage and numerical records. It assigns no scientific verdict.

The complete machine-readable evidence is [fairness_checks.json](/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/analysis/fairness_checks.json). Missing and running cases remain explicit below.

## Matched exposure

Within one stage and seed, the auditor compares complete frozen record-ID orders and checks every observed 20-target window against its metrics. A/C train only the reversed new mode. B/D/E use ten old and ten new targets per completed window. F uses natural next-token targets. A and B use different training distributions, so raw scores across them are not treatment contrasts. Seeds 29/43/71 change continuation order and registered randomness while sharing one acquired-old parent; they are not independent old-model acquisitions.

| Stage | Seed | Completed arms | Pending or missing | Order check |
|---|---:|---|---|---|
| R1/A | 29 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/A | 43 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/A | 71 | U, TS, UL, US, TC, RS, LS | none | PASS |
| R1/B | 29 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/B | 43 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/B | 71 | Full, SN, SP, DN, DP, SRN, RN, SRP, RP | none | PASS |
| R1/C | 29 | fixed, sham, dynamic | none | PASS |
| R1/D | 29 | multi_normal, ordinary, single_normal, single_protected, multi_protected | none | PASS |
| R2_full_native_SwiGLU/D | 29 | multi_normal, ordinary, single_normal, single_protected, multi_protected | none | PASS |
| R1/F | 29 | dense_normal, dense_protected, ordinary2, shared2_protected | none | PASS |
| R2_full_native_SwiGLU/F | 29 | dense_normal, dense_protected, ordinary2, shared2_protected | none | PASS |
| R1/E/fixed | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R1/E/joint | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R2_full_native_SwiGLU/E/fixed | 29 | full, summary, random_summary, oracle, random | none | PASS |
| R2_full_native_SwiGLU/E/joint | 29 | full, summary, random_summary, oracle, random | none | PASS |

## B: total and per-mode capacity

Degrees of freedom count independently changeable effective matrix coordinates. Stored optimizer tensors include redundant coordinates. Full is ordinary dense Adam. SN/SP share a full complement. DN/DP duplicate it, preserving each mode’s space while increasing total capacity. SRN/SRP versus RN/RP match total effective capacity but change the available per-mode space.

| Arm | Seed | State | Effective total DOF | Available per mode | Stored trainable coordinates |
|---|---:|---|---:|---:|---:|
| Full | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 29 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 29 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 29 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 29 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 29 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 29 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 29 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| Full | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 43 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 43 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 43 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 43 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 43 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 43 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 43 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| Full | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291456 |
| SN | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| SP | 71 | COMPLETE | 6,291,456 | 6,291,456 | 6291520 |
| DN | 71 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| DP | 71 | COMPLETE | 12,582,848 | 6,291,456 | 12582976 |
| SRN | 71 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RN | 71 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |
| SRP | 71 | COMPLETE | 6,291,392 | 6,291,392 | 6291520 |
| RP | 71 | COMPLETE | 6,291,392 | 3,145,728 | 6291520 |

The row controls remove the restricted candidate atoms with a separate Gram-matrix inverse in each row half. They avoid the invalid assumption that row masking commutes with the full-space candidate projector. Candidate-coefficient Adam in B differs from native dense Adam; Full qualifies capacity and learning, while B’s internal factorial contrasts retain their own optimizer coordinates.

## D/E: actual computation and router supervision

R1 trains only the native final SwiGLU down projection; gate/up remain frozen. R2 is an independently identified qualification repair that trains native gate/up/down matrices. Its shared candidates are composed at each linear projection before the native SiLU/product computation. R1 and R2 results stay separate. Oracle/random/inference execute the selected expert only. Learned straight-through training evaluates both expert outputs to form its surrogate gradient. The top-1 inference budget is therefore not a claim of identical training FLOPs. Declared projection/head estimates exclude backward, normalization, parameter synthesis and prefix acquisition.

| Case | State | Expert DOF | Active DOF/token | Router parameters | Training expert matmuls | Inference matmuls |
|---|---|---:|---:|---:|---:|---:|
| R1/D/multi_normal/main/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/D/ordinary/main/seed29 | COMPLETE | 6291456 | 3145728 | 0 | 1 | 1 |
| R1/D/single_normal/main/seed29 | COMPLETE | 3145728 | 3145728 | 0 | 1 | 1 |
| R1/D/single_protected/main/seed29 | COMPLETE | 3145728 | 3145728 | 0 | 1 | 1 |
| R1/D/multi_protected/main/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/full/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 6146 | 2 | 1 |
| R1/E/full/joint/seed29 | COMPLETE | 6291440 | 3145728 | 6146 | 2 | 1 |
| R1/E/summary/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/summary/joint/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/random_summary/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/random_summary/joint/seed29 | COMPLETE | 6291440 | 3145728 | 34 | 2 | 1 |
| R1/E/oracle/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/oracle/joint/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/random/fixed/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R1/E/random/joint/seed29 | COMPLETE | 6291440 | 3145728 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/multi_normal/main/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/ordinary/main/seed29 | COMPLETE | 18874368 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/single_normal/main/seed29 | COMPLETE | 9437184 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/single_protected/main/seed29 | COMPLETE | 9437184 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/D/multi_protected/main/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/full/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 65730 | 2 | 1 |
| R2_full_native_SwiGLU/E/full/joint/seed29 | COMPLETE | 18874320 | 9437184 | 65730 | 2 | 1 |
| R2_full_native_SwiGLU/E/summary/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/summary/joint/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/random_summary/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/random_summary/joint/seed29 | COMPLETE | 18874320 | 9437184 | 1218 | 2 | 1 |
| R2_full_native_SwiGLU/E/oracle/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/oracle/joint/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/random/fixed/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |
| R2_full_native_SwiGLU/E/random/joint/seed29 | COMPLETE | 18874320 | 9437184 | 0 | 1 | 1 |

Fixed-expert bank byte comparisons against the prespecified D source: R1/full/seed29=PASS, R1/summary/seed29=PASS, R1/random_summary/seed29=PASS, R1/oracle/seed29=PASS, R1/random/seed29=PASS, R2_full_native_SwiGLU/full/seed29=PASS, R2_full_native_SwiGLU/summary/seed29=PASS, R2_full_native_SwiGLU/random_summary/seed29=PASS, R2_full_native_SwiGLU/oracle/seed29=PASS, R2_full_native_SwiGLU/random/seed29=PASS. Joint training is a separate case: only its initial bank must equal the fixed-phase source. Learned routers receive answer CE and load loss, not the true mode input supplied to the known-mode reference. Full activation input uses more router parameters than the 16-dimensional summaries; random summary matches summary dimension. “Oracle regret” compares against the known-mode assignment of the same experts and may be negative; that assignment is not an optimal per-example expert lower bound.


D expert learning qualification is separate from these engineering checks. Unqualified or incomplete D qualification: R1/multi_normal/seed29=FAIL, R1/ordinary/seed29=FAIL, R1/single_normal/seed29=FAIL, R1/single_protected/seed29=FAIL, R1/multi_protected/seed29=FAIL, R2_full_native_SwiGLU/multi_normal/seed29=FAIL, R2_full_native_SwiGLU/ordinary/seed29=FAIL, R2_full_native_SwiGLU/single_normal/seed29=FAIL, R2_full_native_SwiGLU/single_protected/seed29=FAIL, R2_full_native_SwiGLU/multi_protected/seed29=FAIL. E claims about functional expert selection remain bounded by the qualification of their exact D source; R2 cannot retroactively qualify R1 experts.

## F: natural-text denominator and scope

Split audit: `PASS`. TRAIN documents=128; validation documents=64; targets/document=127; validation targets=8128. Document-text and token-window hashes are checked across the split. Pretraining exposure remains Unknown. The list-task 95% accuracy qualification has no meaning as a natural-language CE threshold.

F’s four whole-package arms change routing, capacity, sharing and protection together. Their differences do not independently isolate sharing or protection. Separate native A-endpoint natural readouts execute the changed attention through full Qwen; their completion is recorded in JSON.

## Numerical and source-version evidence

Each completed case checks observed batch IDs/counters, required TensorBoard coordinates and saved checkpoint metadata. Previously independently verified full-file payload hashes are reused with their source explicitly labeled; only newly encountered saves receive another full SHA256 and CPU tensor audit. E expert-bank byte digests are separately cached per immutable payload digest.

Per-task disk-file hashes come from the legacy or v2 queue freeze. They are not assumed identical across cases, and they are not hashes captured from imported Python bytecode. The documented retention engineering-v2 difference adds B original-projection version/end-byte guards only; the preserved source diff changes no model computation, metric or RNG operation. Historical v1 smoke keeps its original guard scope. Any unrecognized executed/current source difference remains a review item in JSON.


R2 also has a documented evaluator-only source change: natural readout uses a two-expert mixture only when two experts exist. The preserved AST comparison finds all code outside evaluate_natural identical. Five formal queue freezes precede the fix; four corresponding environment disk hashes agree with that version, while F/dense_protected crosses the patch window. Its exact imported source bytes remain Unknown. Both possible versions use the same training code, and this dense case never enters the changed oracle readout branch. The full timestamp/source reconciliation is retained in JSON.

## Missing and running evidence

All queue-defined formal cases in this snapshot have completion records.


Completed cases with bounded/missing audit evidence:

- D_multi_normal_29: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- D_ordinary_29: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- D_single_normal_29: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- D_single_protected_29: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- D_multi_protected_29: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_full_fixed: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_full_joint: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_summary_fixed: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_summary_joint: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_random_summary_fixed: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_random_summary_joint: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_oracle_fixed: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_oracle_joint: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_random_fixed: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- E_random_joint: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- F_dense_normal: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- F_dense_protected: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- F_ordinary2: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].
- F_shared2_protected: BOUNDED_MISSING_EVIDENCE; MISSING=['case-level environment version/precision receipt']; issues=[].