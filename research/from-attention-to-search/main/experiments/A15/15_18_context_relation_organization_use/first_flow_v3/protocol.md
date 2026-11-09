# Protocol: complete frozen-small-model relation audit V3

## 0. Approval Snapshot

Status: APPROVED_EXPLORATORY_EXECUTION. Authority: current chat V3 and explicit approval of the English task, Qwen checkpoint, two single-H100 Reserved jobs and capped budget, followed by authorization to formalize this Anchor. No scientific verdict is approved. Main conclusion: PENDING_RESEARCHER_REVIEW. Exact immutable settings are in [run_manifest](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/run_manifest.json). Existing frozen protocols are untouched.

## 1. Scientific objects and design

C=1/3 is externally necessary graph-path length. D reorders the same 12 facts by moving a fixed five-fact neighborhood including both incident edges of the query entities. F relation/combination exposure is unavailable, and all frequency-proxy comparisons are BLOCKED rather than replaced by word or feature frequency. English mixed left/right templates have unique solver answers, exact reversal word bags, equal facts/entity counts and family/template-disjoint TRAIN/DEV/TEST. 128 families produce 2048 variants: 64/24/40 families, 1024/384/640 rows. Each family has C×D×reversal×paraphrase variants.

## 2. Metrics and registered analysis

Primary descriptive comparison: TEST family-equal C×D difference of correct-candidate log probability margins (nat). Also report candidate accuracy, reversal-pair accuracy, full per-row candidate log probabilities/NLL and 2000 family bootstrap intervals. This is candidate selection, not free generation. No scientific success threshold, posthoc best layer or training-randomness claim. Query last-prefix token and up to three necessary evidence ends are captured at all 28 block outputs, output-minus-input increments, and SAE's separate layer27 MLP input. Duplicate C1 evidence slots do not count as extra observations.

PCA fits TRAIN means/directions, reports raw/centered spectra and TEST retention; ranks 1/16/64. Linear probes fit only TRAIN with 1025 parameters each, full-batch AdamW, LR .03, 100 updates, L2 .001/.01/.1 selected by DEV CE, TEST once; same capacity shuffled-label control. Cross-layer CKA uses aligned rows, fixed-rank16 subspace comparisons and ten random references. E08 uses layers0/7/13/20/27, ranks1/16/64 and amplitudes.1/.5/1, PCA/random/PC1-removal controls, first ten TEST families with paraphrase0. E09 uses two layers selected by DEV probe accuracy (ties earliest), query/evidence-end positions, self/same-relation/different-relation donors, the same TEST subset, and bidirectional reporting. Every registered condition is retained.

## 3. Calibration, assets and resource scope

Model/tokenizer, A22 dictionary and final-layer SAE asset IDs are bound in the manifest. SAE requires a verified match to its distinct recorded parent; otherwise only SAE is blocked. Use saved centered vector-RMS normalization and TRAIN EMA threshold for A22. No-op candidate logp absolute tolerance .005 nat; native full-forward versus query-only head scoring .02 nat, frozen before any forward. Failure is repaired by correct replay, never tolerance widening. Dictionary identity/finite-state failures or nonpositive aggregate reconstruction FVE block its dependent feature interpretation; reconstruction effects are reported regardless. Never refit dictionary normalization or thresholds on these data.

Two h100-1-reserved ACP jobs, one GPU each, each <=7200s, aggregate <=4GPUh; global wall deadline in manifest; output cap20GiB. No resource fallback, download, base/dictionary training, new app thread, publication or Git operations. Existing isolated dependency runtime is reused. Essential label/identity/noop/budget checks retained; redundant checks omitted by instruction. Each independent failure is recorded and does not cancel unrelated work. Jobs stop at the capped deadline.

## 4. Scope and dependent outputs

E00 asset/interface/noop calibration; E01 data/shortcut audit; E02 all C×D behavior; E03 raw states/increments; E04 spectra; E05 readouts; E06 similarity/subspaces; E07 existing dictionaries; E08 projection/removal; E09 donor patches; E10 coverage and reproduction. See execution coverage ledger for final status of every item and optional subitem. Exact code/data/config hashes and per-worker logs remain execution-side. TRAIN directions and DEV selection must finish before TEST intervention choices. Descriptive analysis remains applicable if model behavior is weak, with interpretation limits.

## 5. Fitting and training audit boundaries

T1 readout and T2 statistical fitting are approved under this budget. T3 new dictionary training is not authorized. T4 controlled-frequency main-model training is design-audit-only; counterbalanced exposure assignments and atom/combination marginal constraints require a separately approved training protocol. T5 common/remaining updates are design-audit-only and BLOCKED because the parameter/path split and schedules are unknown. Each has separate scientific, data/statistical and implementation/numerical audit records under execution protocols/. Statistical fits have no optimizer/gradient/token training; classifier supervision counts must not be called LM pretraining tokens.

## 6. Result delivery and amendments

The first factual report starts with exactly three analysis paths, then E00–E10 purpose, real input/operation, numeric results/controls/counts/uncertainty, locally explained terms, figure encodings, and measurement validity/limits. It contains no mechanism acceptance, architecture verdict or proposed scientific direction. End with coverage and one/two understanding questions. Scientific interpretations await researcher review. Preserve this frozen body after execution starts; append amendments with impact rather than rewrite evidence. The run manifest and initial dataset hashes define registration.


## Append-only execution amendments (2026-10-22)

The frozen contract above is preserved. The [execution amendment ledger](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/amendments.jsonl) records serialization repair, exact-batch reference repair without widening tolerances, a strictly aligned donor control, and fixed-objective T1 numerical solver repairs. The original AdamW and bounded L-BFGS attempts remain INVALID. Final CPU float64 exact-Hessian Newton qualifies168 candidates and56 selected heads; DEV selection changed to15/27, and dependent E09 alone was rerun. All5 platform allocations served the same two logical workers within the approved cumulative limits; all are terminal. Prior TEST exposure remains explicit, so results stay exploratory. See [Detailed](detailed.md), [coverage](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/coverage.json) and [execution certificate](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/execution_certificate.json). Scientific judgment is PENDING_RESEARCHER_REVIEW.
