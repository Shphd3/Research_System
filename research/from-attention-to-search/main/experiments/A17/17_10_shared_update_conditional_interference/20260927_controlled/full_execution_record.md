# Exact-33B Four-H100 Full Run — Execution Record

Owner: [Protocol](protocol.md). Main measurement status: `FULL_MEASUREMENT_AND_ANALYSIS_COMPLETE`; researcher interpretation pending. Successful ACP job: `pt-yzq8kkur`.

## Authorized scope at registration

The researcher requested a complete supervised full run and SAE analysis on one `h100-4-reserved` node, using the exact-33B fresh S7 checkpoint and the Protocol's fixed direction families, ordinary A updates, two step sizes, and both B rules. The same researcher defined SAE common as the same atom with similar A/B activation frequency and positive strength. The numerical similarity cut-off proposed in Protocol §11.2—at least 8/256 positives per group per rho, frequency and each positive-quantile ratio at least 0.5—was explicitly confirmed by the researcher on 2026-09-28 for the first loose screening round, before confirmation-family SAE or loss data were read.

## Completed preparation

- [Smoke execution record](smoke_execution_record.md): attempt `pt-jtp7to06` passed all four H100 engineering workers. Earlier numerical-check failures remain preserved.
- The full worker and launcher are in `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/scripts/`. The worker fixes one family to one GPU, freezes the exact state, builds the 256-context basis, tests the original downstream adapter and joint-feasibility witness, runs one full-size development family per GPU, and stops if the remaining two-hour envelope cannot contain three confirmation families plus analysis allowance.
- The independent raw-output auditor requires all 12 families, 96 source gradients, 192 virtual updates, 384 target cells, unchanged frozen tensors and the exact source/checkpoint hashes. The paired 2,000-draw analysis and SAE structural/signed diagnostics scripts are implemented before confirmation-family readout.
- Local checks: Python compilation; shell syntax; `check_numerical_core.py` PASS; synthetic paired-bootstrap and common-threshold boundary checks PASS. ACP template dry run resolves the prescribed four-H100 reserved profile, image and mount; no full ACP job was submitted by that dry run.

## Planned execution sequence before submission

Freeze the approved Protocol/config SHA256s with the source set in a unique registration, submit one four-H100 full job through the envelope template, supervise to terminal completion, audit all arrays, run the frozen analysis, then write Summary/Detailed and route the completed material to the requested 0926 conversation for review. If the cut-off changes, amend and retest the selector before registration; do not relabel an already-read confirmation result as preregistered.

## 2026-09-28 full submission

- Researcher confirmed the first-round common threshold before registration; Protocol/config were updated before any confirmation readout.
- Registration: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T004906Z/registration.json`, SHA256 `8b9aae4a045812da255838ffeb9e204b6f03570a617cb6080a3a3d7877abe364`.
- ACP job `pt-haiy2hu9` submitted at `2026-09-28T00:49:25Z` through the envelope template on one `h100-4-reserved` node and `shphd-lite-0911`; initial platform state `QUEUEING`, zero worker replicas. Submission receipt and execution certificate are in `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T004906Z`.
- Monitoring owner is the current Codex conversation. Stage 0–2 and confirmation outcomes are not yet known; no secondary job is authorized by queueing.

## 2026-09-28 attempt 1 terminal diagnosis

- ACP `pt-haiy2hu9` reached `FAILED` at 00:55:24 UTC. Three ranks stopped at Stage 0 attention-output correspondence, each with exactly 1/131,072 elements slightly above the old 1e-5 absolute per-element tolerance (observed maxima 1.0867e-5–1.3471e-5). Rank0 stopped when the peer abort marker appeared.
- Only one partial 64-context calibration shard exists; no basis, witness, development receipt or confirmation-family loss/SAE file exists. Original registration, rank failures, pod log and `measurement_failed.json` remain preserved. Scientific result: `NOT_EVALUATED`.
- Diagnosed as FP32 batch-shape GEMM rounding in an overly strict engineering check. The revised check records absolute maximum and relative RMS, with limits 2e-4 and 1e-5 respectively; the 2e-4 native-adapter limit was already exercised by the passing four-H100 Smoke. Protocol amendment and new source hash precede a fresh same-scope registration.

## 2026-09-28 attempt 2 submission

- Fresh same-scope run `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T005649Z`; registration SHA256 `75bdcbfc370bf6d2d5cb1cb9cb7e7142918e5b375757b04d266961a10f91d65f`; ACP job `pt-i0wsunn0` submitted at 2026-09-28T00:57:06Z.
- This job retains the exact checkpoint, directions, seeds, ordinary updates, SAE selector, full analysis and four-H100 reserved profile. Only the Stage 0 native-versus-replay engineering comparison changed as recorded in Protocol. The first run is preserved and not resumed.

## 2026-09-28 attempt 2 terminal diagnosis and local full-size qualification

- ACP `pt-i0wsunn0` reached `FAILED` at 00:57:50 UTC, still in Stage 0. All four ranks reported selected-position GEMM maximum absolute differences 2.2888e-4–3.2043e-4 while relative RMS stayed about 7e-7; no basis, development or confirmation files were read. The run root, registration, `abort.json`, `measurement_failed.json`, rank failures and pod log remain intact.
- Exact-33B local H100 read-only check on all 256 fixed contexts produced 4,096 native positions. Full-shape W replay matched native attention output exactly on all four 64-context shards; selected-shape replay differed by at most 1.3733e-4 with relative RMS at most 3.1354e-7. The frozen basis and reference adapter were built; witness passed with minimum margin 8.3796.
- All four development families 11001–11004 completed locally at full planned sizes without accessing a confirmation family. Each yielded 8 source gradients, 16 virtual updates and 32 target condition cells; microbatch gradient relative differences were about 1e-7 and zero-repeat differences were zero. This local check is engineering evidence only and does not replace the four-card task gate.
- The same-shape interface check and PyTorch Adam/Protobuf compatibility setting are now frozen before a fresh same-scope registration. Local evidence: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/checks/local_stage01_full_20260928/`.

## 2026-09-28 attempt 3 submission

- Fresh registration: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/registration.json`, SHA256 `ab201f81cdcfa9ff9b5be7e745d7125ffe4f7908df3d8727f1b479c8c397616c`.
- ACP job `pt-yzq8kkur` submitted at 2026-09-28T01:03:29Z on one `h100-4-reserved` node, image `shphd-lite-0911`, four H100 workers; dry-run resolved the same tuple. Submission receipt and execution certificate are in the new run root.
- Frozen scope remains exact-33B checkpoint, approved first-round loose SAE common selector, four development and twelve confirmation direction families. No confirmation results have been read at submission.

## 2026-09-28 attempt 3 terminal measurement and analysis

- ACP `pt-yzq8kkur` reached `SUCCEEDED` at 2026-09-28T01:10:16Z. Four H100 workers each finished its three fixed confirmation families in 54.6–56.7 seconds after the gated setup; no worker resubmission or family exclusion occurred. Stage 0 preflight, Stage 1 common-solution witness and four Stage 2 development families passed. The development gate froze `epsilon_repeat=0`, `tau=1e-7`.
- Frozen raw auditor wrote `measurement_complete.json`: 12/12 confirmation families, 96 A source gradients, 192 virtual updates, 384 B target condition cells; state hash `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`, all frozen worker tensors unchanged. Raw output was 6,556,574,214 bytes, below 30 GB. Complete run root: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z`.
- Frozen CPU `analyze_full.py` and `plot_full.py` completed after raw audit. Registered category: `MODULATION_WITHOUT_NET_HARM`; both step-size `M` intervals are above `tau`, but the high-overlap flipped B-loss intervals are wholly below zero. The approved common-atom rule selected 32 atoms in each of 12 families, while every family failed the prespecified task-signal reconstruction guard. Signed SAE decomposition and same-rank controls were computed; these are descriptive and do not establish prospective prediction or atom causality.
- Canonical factual results are [Summary](summary.md), [Chinese Summary](summary_cn.md), and [Detailed](detailed.md). Scientific interpretation and next decision remain researcher-owned; this completion is not a Focus-level human verdict.

## 2026-09-28 requested report review handoff

- The completed evidence was sent to the existing `0926-共享参数冲突整理分析` Codex conversation (thread `01a0db36-5ae0-7e23-8e61-6f154608d8a4`). That conversation reviewed the frozen verdict, raw SAE summaries and the four-part advisor report, then made limited edits only to [00_导师汇报稿.md](../../../../../../../daily_research_reports/backup/2026/09/0927/meeting_report/meeting_brief_controlled_cn.md), preserving its original structure and marking the researcher's final scientific judgment as pending.
- The requested conversation titled `审核研究假设文字` was not located through the available App listing or local title index, so the review does not claim to have read it. This missing conversational context does not change the registered measurements or the file-based result boundary.
