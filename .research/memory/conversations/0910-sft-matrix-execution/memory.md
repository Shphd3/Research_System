# Conversation Memory: 0910-sft-matrix-execution

Conversation name: 0910-sft-matrix-execution (execution continuation of the 0910-clustering change record)
Processed by: DeepSeek via Claude (harness: Claude Code; model: unknown)
Created at: 2026-09-09T20:59:00Z
Latest update at: 2026-09-11T14:45:00Z
Continues from: 0910-clustering-change/memory.md
Environment: container /data/250010109 (`repo`=Research_System, `exec`=MoE_Router);
  also read from the Windows checkout C:\Users\250010109\data\Research_System.
  /data is a network mount (quarkfs_client); /root/** is container-local and lost
  on recycle. From the Windows checkout, `exec` and /root/** are not-visible.
Continuation: continuation.md in this record directory is the CURRENT entry point
  for this workstream. It supersedes the four historical handoff documents.

> **Consolidation note (2026-09-10T12:25Z, explicit researcher request).** The 13 entries written
> 20:59Z–11:37Z were merged into the four entries below. Merged, not deleted: every decision,
> constraint, negative result, retracted claim, and open uncertainty is preserved. Dropped:
> the repeated debugging narration of qualification rounds r3–r9, the container-restart log,
> SCO reinstall steps, and process-management detail. `Created at` is unchanged.

> **Consolidation note (2026-09-11T14:45Z, explicit researcher request — second pass).** Removed:
> (a) the list of five figure defects that were found and fixed on real data, now resolved
> operational detail — the two that remain live traps are kept; (b) the per-channel numeric
> detail of the training-dynamics findings, which is owned by
> `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md`, replaced by a pointer
> plus the reading pitfalls; (c) the render-progress counters and per-run file counts, which
> were superseded by the next checkpoint. Preserved in full: every binding constraint, the
> identity contract, both `fm` defects, both mechanism closures, both retractions, the typed
> `INSUFFICIENT` states, the cross-host reproducibility boundary, and every open loop. The
> 16.3 KB → 13.6 KB reduction is deduplication only, smaller than the first estimate because
> nearly everything in this record proved decision-bearing; the prior text is recoverable at
> commit `bcadd93`.

## 2026-09-09T20:59:00Z -- Setup, identity contract, qualification PASS, full job submitted [consolidated]

- Run root `runs/full-20260909T203104Z/`; execution root `MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`. 14 conditions (task / sae_a / sae_b / gmm_a / gmm_b / high28_a / high28_b × F/U) × 3 seeds (17/29/43) = 42 trajectories × 512 updates; shared frozen Qwen3-0.6B backbone + injected adapter; teachers frozen; structural gradients router-only.
- **Identity contract (binding, still in force).** `source_hashes()` covers `fm/**/*.py` (and `matrix.json`, `runtime.sh`, `vendor_provenance.json`, `acp_full.sh`, `README.md`). Any edit to a live `fm` source invalidates `run_identity.json` *and* the teacher target manifest — both must be rebuilt as one batch, and the cluster's qualification artifacts recorded under the old hash must be wiped. Cluster pods read the same files over the shared `/data` mount, so live code == node-side code: **never edit `fm/` while a pod runs.** Cluster stages therefore run from the frozen snapshot `$RUN/source/`, not from the live tree. Decision: live `fm` stays frozen for the whole run; the two known `fm` defects are handled by post-processors outside `fm/` (see next entry).
- **Negative result (preserved).** Bitwise-exact resume is not achievable on these H100s for the open-attention path: resume is exact in adapter params, adapter-group Adam momenta, optimizer step tensors, schedule position, cumulative tokens and RNG, but the open-attention weights and their momenta carry ~1e-8/step cublasLt/SDPA kernel-choice noise (measured 4-step drift: adapter 0.0–2.2e-7, attention 2.1e-8, attention Adam 3.9e-9, history NLL 2.9e-6 — node-dependent). The recovery gate is therefore *discrete fields exact + float fields within a measured backend noise floor*, not bitwise.
- Qualification PASS (36 updates, 14/14 conditions); full training completed: **42/42 `training.json` COMPLETE**, 882 checkpoints + sidecars, 1764 representation shards, 0 `failure.json`.
- Contrast contract `matrix.json`: G1=12 (teacher arm − task), G2=7 (U−F), G3=6 (b−a), G4=4 (sae−gmm), G5=4 (high28−sae), G6=6 (attention interaction) = 39. CI95 (`fm/analysis.py:139-146`) resamples panel records only (2000 draws, multiplicities shared across arms ⇒ arms paired); **it excludes seed-to-seed training variance** — that lives in `seed_values` (≈0.14 nats at u512).

## 2026-09-10T05:07:00Z -- Cluster segment complete; two `fm` defects frozen not fixed; two mechanism questions closed [consolidated]

- Cluster segment verified by **re-counting shared storage, not by reading job state**: 42/42 identities match, 882/882 `.pt` + sidecars, 1764/1764 shards, 0 mismatches, `source_hashes_live_matches_recorded=true`. The job's final `FAILED` state and `analysis exit rc=1` are verifier/launcher artifacts (`cmd_verify` exits 1 while analysis is by design still pending; the parallel launcher's prune step raised `OSError: Directory not empty` *after* every numeric artifact had landed). Neither is a computation failure.
- **Defect 1 — `fm/verify.py:44-47` sidecar naming**: it expects `update_SSSS.pt.json` / `recovery.pt.json`; `fm/training.py:checkpoint_save` writes `update_SSSS.json` / `recovery.json`. Effect: 22 phantom `missing` per trajectory → training `found: -882` → PARTIAL. **Not fixed in place** (would void all 42 identities + the target manifest). Handled by `postprocess/correct_verify.py`, which re-counts with the real names and re-checks identity/digests; it ran clean (`analysis/verify_training_corrected.json`).
- **Defect 2 — `fm/report.py` coverage-table bug**: the fix must not be applied to live `fm` at finalize time, or every trajectory identity is flagged. Plan: finalize with frozen code; splice the coverage table from `analysis/teacher_coverage_metrics.csv` via `postprocess/splice_coverage.py`, recorded as a documented deviation in `result_draft/evidence_index.md`.
- **Mechanism closure 1**: `task_router_gradient_norm` is **exactly 0.0 at update 1 on 42/42 trajectories** (2.5–3.3e-6 from update 2). Cause: the expert Bank's up-projection `b` is zero-initialised, so at t0 `E_k(h)≡0` and `∂L/∂coefficient ≡ 0`. Update 1 therefore belongs to the structural prior alone (structural arms' u1 router displacement equals the structural gradient exactly). Task-driven router training effectively begins at update 2. Not a bug.
- **Mechanism closure 2 / retraction**: single-update `train_nll` step-to-step ratio std ≈ 0.09–0.12, so a +35–40% single-step rise is ~3σ noise. The earlier claim that large rises *cluster* at updates 261/356/447/462 is **not reproducible and is withdrawn**. Trend readings must use window means/EMA; decisive NLL comparisons use the fixed panel from `fm analyze`.
- **Retraction**: the earlier "cross-source share of movers is 0.35–0.43× the independent expectation ⇒ significant deficit" is **withdrawn**. Correct reading: observed 0.56–0.74 against a source-blind, cluster-size-aware null of 0.837, ratio 0.67–0.89, on only 20–31 records per condition — not evidence either way.
- Offline ten-config hierarchy (G8) computed locally and independently of the cluster: `OFFLINE_COMPUTED_WITH_TYPED_INSUFFICIENCY_NOT_SCIENTIFIC_VERDICT`, 40 views, 1200 matched rows, `path_evidence.json` (158 real deepest paths). Matched-control sign convention: `right_minus_left_* = high − leaf`; on all check records 1014/1026 rows negative (median −0.1056, CI95 contains 0 in 18/1026), reversing to +0.0198 when restricted to records both sets cover. The two must be read as a pair: the overall deficit is carried by coverage/abstention, not by grouping quality on common records.

## 2026-09-10T11:37:00Z -- Analysis moved off the container; full-matrix analysis and seven figure families complete [consolidated]

- **Why the host changed**: `fm analyze` has no resume path in `fm/analysis.py`, and the container is recycled roughly every 4 h, so a 7–8 h single-process pass could never finish; it was killed four times. The pass was moved to the reserved ACP pod `pt-qb1ffm7q` via `postprocess/acp_analyze.sh`. Result: **`analysis/compute_receipt.json` at 10:50:45Z**, 42 trajectories × 21 checkpoints × 2 splits, 1764 shards all identity-verified, 641 s; resume accounting 1062 bootstrap artifacts reused / 702 recomputed.
- **Cross-host reproducibility boundary (measured, canonical).** Same-host recomputation is **bitwise identical** (including through an npz round-trip, at 1 vs 4 BLAS threads). Container ↔ pod is **numerically equivalent, not identical**: `max|ΔS| = 4.4e-16`, `max|ΔNLL| = 6.7e-16`, `max|ΔD| = 3.1e-33`, all CI95 endpoints unchanged to 6 decimals; inputs proven identical (shard sha256 == receipt), so the residual is host-level BLAS GEMM dispatch. **Never call cross-host artifacts bitwise-equal.**
- Seven figure families `fig01`–`fig07` (`postprocess/figures/`) produced from real data, 162 files + per-family `method_cn.md` + `index.html`, all `DERIVED_NOT_SCIENTIFIC_VERDICT`; `fm/` imported read-only (`fm.legacy.data.render_record`, `fm.geometry`). Five defects surfaced only on real data and were fixed (details in the 2026-09-11 consolidation note). **Two remain live traps**:
  1. `panel_metadata.csv` — `<run>/panel_metadata.csv`'s `index` is the dataset row number 0..8479; only `analysis/postprocess/panel_metadata.csv`'s `index` is the panel position.
  2. `common.axis_limits()` prefers the canonical `analysis/global_axis_limits.json` written by `fm render` and records its source in `AXIS_LIMITS_SOURCE`; the canonical file is written *after* the scan starts, so axis limits can differ between an early and a late reader.
- **Deliverable**: `daily_research_reports/0910/docs/sft_matrix_full_analysis_cn.md` — four-part meeting format, no placeholders left. The researcher's boundary sentence in §5 is kept **verbatim** and AI does not lift it.
- **Completion judging rule for the remote chain**: judge by `<run>/postprocess_chain/*.done` and `acp/REMOTE_STATUS`. Never by the chain log's "finished" line — `complete_chain.sh`'s `step()` logs FAIL but does not abort. Decision taken: do **not** run `complete_chain.sh` locally while the pod's `render` is writing into the same output directory (duplicate render, contention on an 8-CPU cgroup).
- **Compute conclusion (verified by this round)**: every stage — analysis, bootstrap, clustering, projection, figures — is CPU numerical work; the 4×H100 were never used. The value of the reserved node was its 88 vCPU and independence from container recycles. **Do not re-submit 4-GPU reserved unless a new batch of conditions is to be trained.**

## 2026-09-10T12:40:00Z -- Training-dynamics report; handoff [superseded in part]

- Summary: 研究者要求围绕 0909 组会问题的本意——「看训练过程中发生的剧烈变化」——讲解结果。产出 `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md`（四段式收束 + 训练结果表 + 口径索引），并新增两个只读探针：`postprocess/probe_change_timing.py` → `analysis/postprocess/change_timing.json`；`postprocess/probe_routing_churn.py` → `analysis/postprocess/routing_churn.json`（读分片 `actual` 成员；npz 为 zip，单成员读取约 13 ms）。
- **核心结论（指向读面，数值不再在此复制）**：剧烈变化在**路由侧**，且在**前 1/8 训练内基本完成**；零假设对照显示 t0 归属对 t512 几乎无预测力，是整体重掷而非少数记录搬家，因此「改选比例大」本身**不能**推出分配变好；读出结构几乎不动，是边界抖动而非结构重建。全部数值、五通道表、时间表与训练结果表见 `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md`。
- **必须随稿继承的口径坑（不得绕开）**：`clusters/*.npz` 的 `transition_from_previous` 存在于 **display 对齐空间**；对齐置换翻转会把稳定分区整体改标误报成大量流动，读数前必须**先做匈牙利重匹配**，且结果只能标为**下界**。F 条件在全部 20 个区间上流动恒为 0.0000，与「h 逐位不变」互证。
- **不得代研究者解除的边界**：t0 专家输出严格为 0（42/42 分片 `max|E|=max|shared|=0`），故 t0 的专家归属在功能上是空转的——该比较度量的是重掷程度，不是功能上的改换门庭。研究者边界句仍为稿中 §8 原文。
- **交接（已被取代）**：原先的交接包 `sft_continuation_prompt_cn.md` 及另外三份入口文档，已由本记录目录下的 `continuation.md` 取代（四份原件保留，仅标 SUPERSEDED）。接手方按 memory 合约**新建自己的记录**并 `Continues from` 本文件，绝不覆盖本文件。
- **交接期并发风险**：本会话的会话内 cron `fc9038cb` 会在收据已出、链未跑完时自动本地执行 `complete_chain.sh`。该 cron **已于 2026-09-10T12:41Z 停止**（研究者指示）。接手方接手前**仍须复认**该 cron 已停，否则两个 agent 会同抢同一输出目录。`docs/execution_envelope.md` §6 因此明令：用受管后台作业监控，**不要建会话内定时任务**。
- References: `daily_research_reports/0910/docs/sft_matrix_training_dynamics_cn.md`（五通道表、时间表、训练结果表、边界）；`daily_research_reports/0910/docs/sft_matrix_full_analysis_cn.md`（四段式读面）；会议原话 `daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md`（09:05 / 09:35 / 10:36 / 14:52）；`continuation.md`（本工作流当前入口）。本记录非 canonical；科学判决仍由 researcher 拥有。
