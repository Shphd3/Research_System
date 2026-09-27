# Detailed: task update compatibility, 2026-09-25

Primary design: [anchor_cn.md](anchor_cn.md). [Protocol](protocol.md) scientific body at the pre-SCREEN freeze had SHA256 `c0f34ab365325c5dbfe1bcae054721f2bd291b493ef0cc1a35645b2ad0252edf`; later execution-status bullets were appended, so the current file hash differs. Execution workspace: `/data/250010109/MoE_Router/experiments/20260925_task_update_compatibility/`.

## 0. Direct stage result and eligibility

The registered screening stage completed on four RTX 5090 Spot GPUs. Six data sources qualified for screening. All 15 source pairs had independent-half representation separability \(D\geq0.75\), but **zero** pairs had full-weight gradient cosine \(C\leq-0.05\) in both halves. The deterministic selector therefore returned `SCREEN_NO_ELIGIBLE_CONTRAST` and no \(P-\)/\(P+\) assignment. The nearest negative candidate, MATH–MMLU, had \(C_{H0}=-0.0634991341\) and \(C_{H1}=-0.0481501639\); the second value fails the preregistered \(-0.05\) cutoff. This is a screening eligibility result, not a test of the proposed training effect.

The four-GPU seven-arm engineering smoke `pt-af2pg6wj` **SUCCEEDED / engineering PASS**: all seven arms completed eight updates with independent-process recovery at step 4, finite required TensorBoard scalars, and continuous token coordinates. It used GSM8K/MATH only as a variable-length engineering pair; that pair was not scientifically selected. Solo qualification, paired full training, rollback, and CONFIRM are **NOT RUN by the registered screen gate**. After viewing the screen failure, the researcher explicitly selected **stop under the original Protocol**. This is an execution decision; no broader mechanism judgment is inferred here.

## 1. Registered decision rule and actual comparison

Protocol §5.4 required two pairs with \(D\geq0.75\), one pair with \(C_{H0},C_{H1}\leq-0.05\), a comparator with both cosines \(\geq+0.05\), exactly one shared source, and \(|D_- - D_+|\leq0.10\). Protocol §13 ends formal training when no such contrast exists. The 15 pair rows and deterministic selector output are in `selection/selection_manifest.json`; its SHA256 is `b343f91f45a9ac23d1e29a7523c14b12f2869978ec5fb77e7ebe7f729a362538`.

The measurement used 64 independent families per source per half, the frozen 21B fresh S7 checkpoint, the same native final-block down-input coordinates for all sources, and answer-only teacher-forced loss. The six screened sources were MMLU, MMLU-Pro, BBH, GSM8K, MATH, and MBPP. GPQA and HumanEval lacked the required role inventory and were excluded before model screening. Every eligible source used separate SCREEN, TRAIN, DEV, DIAG, and unopened CONFIRM family roles in the frozen role ledger.

## 2. Conformance and evidence lineage

| Registered item | Actual | Status and boundary |
| --- | --- | --- |
| Execution scope | Researcher requested 5090 Spot smoke then conditional full run on 2026-09-25 | Authorized; stages remain gated |
| Resource | Single node, four RTX 5090 Spot, `shphd-lite-0911` plus mounted SM120 layer | Screen verified four RTX 5090 and PyTorch 2.8.0 CUDA 12.8; no reserved H100 used |
| Data | Raw source versions reconstructed from the 2026-09-08 derived split, family deduplication and frozen role ledger | Six of eight sources inventory eligible; local known-history audit PASS; near-duplicate recall and pretraining contamination remain unknown |
| Model | Fresh S7 21B checkpoint SHA256 `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33` | Screen receipt records this checkpoint and role ledger identity |
| Scientific freeze | Protocol and selector source hashes recorded before any new SCREEN model score | `receipts/pre_screen_freeze.json` at 2026-09-25T02:45:54Z |
| H0/H1 screen | Six sources × two halves; save 64 record vectors and one full-weight virtual gradient each | 12 artifacts and hash receipt PASS |
| Pair selection | Apply frozen \(D/C\) and shared-source rules to all 15 pairs | `SCREEN_NO_ELIGIBLE_CONTRAST`; no selected pair |
| Seven-arm engineering smoke | Four RTX 5090, real answer batches, 8 steps per arm and step-4 independent-process resume | PASS for code/telemetry only; performed on unselected GSM8K/MATH engineering pair, so it does not remove screen failure |
| Training and confirmation | Only after data, screen, smoke, and Solo gates | NOT RUN by stage 2 failure; no \(Γ\) or capacity result exists |

| Decision | Raw evidence | Transformation | Observed value | Registered rule | Typed outcome |
| --- | --- | --- | --- | --- | --- |
| Pair eligibility | `selection/screen_20260925/{source}_{half}.pt`, `screen_receipt.json` | `scripts/analyze_screen.py` computes ridge \(D\) and cosine \(C\), then `scripts/select_pairs.py` applies frozen rules | 15/15 \(D\geq0.75\); 0/15 both \(C\leq-0.05\); 7/15 both \(C\geq+0.05\) | At least one valid negative pair and shared positive reference | `SCREEN_NO_ELIGIBLE_CONTRAST`; full training blocked |
| Closest negative candidate | MATH/MMLU H0/H1 gradient artifacts | Frobenius cosine in FP64 aggregation | \(-0.0634991341,-0.0481501639\) | Both \(\leq-0.05\) | Not eligible; no rounding or post-result threshold change |

The pair is the unit of the deterministic selection table; the two screen halves are required replicated filters, not a bootstrap confidence interval. This screen does not observe actual LoRA/Adam interference or held-out training benefit.

## 3. Stage record

| Stage | Evidence | Status | Consequence |
| --- | --- | --- | --- |
| 0. Material, approval, freeze | Protocol §17; `receipts/pre_screen_freeze.json` | PASS for bounded execution | Proceed to data and screen |
| 1. Data construction | `data/frozen_v1/data_manifest.json`, `historical_audit.json` | PASS for six sources; two excluded | Six sources enter SCREEN |
| 2. Target GPU SCREEN | Job `pt-gesdlgr7`, persistent pod log, 12 artifact hashes, selection manifest | Compute PASS; contrast INSUFFICIENT | Registered stop before Solo/full |
| 3. Seven-arm engineering smoke | Job `pt-af2pg6wj`; `receipts/target_5090_smoke_20260925/smoke_receipt.json` | SUCCEEDED / engineering PASS for seven arms | Does not override stage 2 or certify a selected-pair formal run |
| 4. Solo headroom | No run | NOT RUN | No can-learn judgment for new task pairs |
| 5. Mixed-arm training and rollback | No run | NOT RUN | No interference/benefit trajectory |
| 6. CONFIRM | Sealed | NOT RUN | No \(Γ\), \(Q\), or \(E\) verdict |

## 4. One-day full record

1. **Question.** Can the registered eight-source screen construct a high-\(D\) low-\(C\) task pair and high-\(D\) positive-\(C\) comparator sharing one source?
2. **Setup.** Frozen 21B S7 model, answer-only supervision, final down-projection virtual full-weight gradient, 64 SCREEN families in each of H0/H1, single-node four-5090 Spot.
3. **Data.** Six inventory-qualified sources in `data/frozen_v1`; GPQA and HumanEval excluded before screening. No training data were optimized in this stage.
4. **Testing split.** H0/H1 are separate screening halves. DEV, DIAG_READOUT, and CONFIRM remain outside this measurement.
5. **Direct result.** No eligible negative pair: 0 of 15 meets both \(C\leq-0.05\); closest MATH–MMLU fails H1 by 0.0018498361. Registered full-training comparison is `NOT RUN`.
6. **Boundary and decision.** The existing task-pair contrast cannot be constructed under the frozen rule. This does not show that interference is absent. The researcher chose to stop this round under the original Protocol. Any altered cutoff, proxy, or candidate set would be a separate human-owned design decision and need a new freeze before execution.

## 5. Artifact map

| Artifact | Purpose | Identity / completeness | Claim boundary |
| --- | --- | --- | --- |
| `receipts/pre_screen_freeze.json` | Protocol, selector, screen and training-code hashes before first new SCREEN readout | Complete | Science rule identity only |
| `data/frozen_v1/roles.jsonl`, `data_manifest.json`, `historical_audit.json` | Original-record role, target, source and known-history provenance | Frozen role SHA256 `ea56fbef18edd11d16de1dda324aa742ecafe7c717a58d8d4837c81ce87b12d7` | No guarantee of zero near-duplicate misses or pretraining contamination |
| `selection/screen_20260925/screen_receipt.json` and 12 `.pt` files | Raw H0/H1 \(u\), gradient and target counts | 12 hashes checked; screen receipt SHA256 `8567e76dd36cafd933e9f83e7f25efd6c35e3e413bac70ee99d96fae2f6ea7f3` | Screening only |
| `selection/selection_manifest.json` | All 15 \(D/C\) pairs and deterministic selection outcome | SHA256 `b343f91f45a9ac23d1e29a7523c14b12f2869978ec5fb77e7ebe7f729a362538` | No training verdict |
| `receipts/stage2_screen_terminal.json` | Stage 2 terminal rule application | Complete | `INSUFFICIENT`, not evidence of zero interference |
| `receipts/submit/submit-tuc-0925-screen-20260925T024921Z.json` and `receipts/pod/tuc-0925-screen-20260925T024929Z.log` | Submission and persistent worker output | Job `pt-gesdlgr7` SUCCEEDED | Scheduling success alone was not the screen result |
| `receipts/submit/submit-tuc-0925-smoke-20260925T024602Z.json`, `receipts/pod/tuc-0925-smoke-20260925T025254Z.log`, `receipts/execution_certificate_smoke.md` | Smoke identity and persistent worker output | Job `pt-af2pg6wj` SUCCEEDED at 03:16:34Z | Engineering only |
| `receipts/target_5090_smoke_20260925/smoke_receipt.json` | Seven-arm resume and telemetry audit | PASS; SHA256 `feaf5f1d2396fb8aa11dc90e32023bb11ea753a75f5f46873af5baeaa69aaaa9` | No scientific effect result |

All paths in this map are relative to the execution workspace unless stated otherwise. No generated results are copied into Git. No `summary.md` or Focus-level mechanism conclusion is finalized without the researcher's initial scientific judgment; the explicit decision to stop is recorded above.
