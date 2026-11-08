# Conversation Memory: 1108-snr机制-mig先导

Conversation name: 1108-snr机制-mig先导 (user-suggested `20261108_SNR机制_MIG先导`, normalized to the existing `MMDD-topic` record format)
Processed by: Claude Code (harness: Claude Code CLI 2.1.280; model: claude-opus-5-5). The contract's agent list has no Claude entry; recorded as-is.
Created at: 2026-11-08T12:02:11Z
Latest update at: 2026-11-08T12:55:37Z
Continues from: none (related context read: 1108-教师特征与专家分发检查, 1106-分层MoE长尾学习验证, 1108-mig-research-organize)
Environment: repo=/data/250010109/Research_System (visible); exec=/data/250010109/MoE_Router (visible); GPU=1× H100 MIG 3g.40gb (visible)

## 2026-11-08T12:02:11Z -- Conversation start: SNR mechanism MIG pilot authorized by uploaded prompt

- Summary: Researcher uploaded `20261108_MIG_SNR_______Prompt.md` authorizing: Task A (asset/throughput check on MIG), Task B (H1 one-step mean/noise decomposition on block7 single expert of the 33B MoE, ≤3 GPU-hours total), Task C (H3 nesting vs reuse, CPU only on S11/S13 caches), Task D (write-only 4×H100 H2 config and memory-experiment diagnostic design), and a 11/9 meeting report. Not authorized: 4×H100, training/continued training, commit/push, new Focus.
- Current work: Reading required sources; MIG verified as 1× H100 MIG 3g.40gb, 40448 MiB.
- Next action: Read roadmap, A17/A15_05_04/S11/S13/S14–S17 records; run entrypoint and asset checks.
- References: uploaded prompt (`/root/.claude/uploads/e871db4c-abea-5ac9-b868-aa00226b01b6/4d8bdb2f-20261108_MIG_SNR_______Prompt.md`, ephemeral path; authorization scope).

## 2026-11-08T12:55:00Z -- Tasks A-C executed; records and meeting brief being written

- Summary: Task A/B ran on the local MIG (≈10.4 GPU-min of the 3 h cap); Task C ran on CPU; all controls (zero update, exact restore, tail-vs-native) passed. H1 noise-term scaling (η² and ≈1/n) observed; primary cross pair mean help not distinguishable from zero (z=1.28), crossing η* only via post-hoc control-variate estimator/derivation. H3: reuse-type sibling discriminative members are frequent, nested ones rare, both SAEs. Interpretations provisional, researcher acceptance Unknown.
- Current work: writing A17_13 R02 Summary/Detailed, S18 records, Task D designs (NOT RUN), 1109 meeting brief; asset registration pending.
- Next action: finish records, register analysis assets, run entrypoint check, final memory entry.
- References: exec /data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/ (evidence/, results/probe_analysis.json, results/probe_supplement_A01.json); /data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S18_nesting_reuse_1108/results/.

## 2026-11-08T12:43:04Z -- Delivery complete: records, meeting brief, asset registration

- Summary: All authorized tasks delivered. H1 (A17_13 R02, placement is an AI choice pending confirmation): noise term scales ≈η² (slopes 1.95–2.35) and ≈1/n, dominates past the crossing; cross mean help on the primary pair z=1.28 (6/6 cross pairs help in point estimate, 3 with z>2, none harm); crossing η* only via post-hoc control variate (A01) and derivation → AI verdict: noise part supported, crossing part insufficient, conflict branch not triggered. Same-group vs cross η* similar because high-loss/high-gate tokens raise signal and noise together; groups unmatched in loss/gate (limitation). H3 (A15_27 S18): nested sibling-discriminative members rare, reused ones frequent, both SAEs/thresholds/wordings; shared members mostly not nested. H2: 4×H100 config only, NOT RUN. Memory diagnostic: checkpoints saved, design only, NOT RUN. Researcher acceptance Unknown everywhere. GPU wall ≈10.4 min.
- Current work: none running. Not done: commit/push (not authorized), Anchor body edits and Anchor sync (no Anchor revision made; roadmap navigation updated instead), research_map.json refresh (not done). Handoff package 01_research_handoff_cn.md and 11/4–11/6 minutes not found in workspace; Codex-history grep for 信噪比 timed out (incomplete search).
- Next action: researcher reviews the meeting brief; decides on R02 placement, acceptance of the bounded H1 reading, and H2 4×H100 approval. Do not start training or resubmit anything automatically.
- References: daily_research_reports/1109/meeting_report/meeting_brief_snr_longtail_mig_pilot_cn.md (speaking brief); Projects/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R02_20261108_snr_mig_pilot/summary_cn.md (H1 owner record, with protocol_cn.md/detailed_cn.md/h2 config/memory design); .../R17_D1/controlled_steps/S18_nesting_reuse_1108/summary_cn.md (H3); assets/catalog.json ids analysis_snr_one_step_decomposition_20261108, analysis_s18_nesting_reuse_20261108 (strict PASS); exec evidence /data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/evidence/ (gpu_clock.log, probe_complete.json, authorizing_prompt_20261108.md).

## 2026-11-08T12:55:37Z -- Discussion package (<20 MB) built and verified

- Summary: User requested a handoff discussion package under 20 MB. Built with System tools/build_reading_bundle.py (11 selected sources + companions; byte-preserved sources/ layer), added 00_导读_cn.md and execution_evidence/ (H1 frozen files, raw rows, analyses, controls, prompt, code; H3 tables, evidence, code). No checkpoints/SAE weights/DCLM text/caches/logs/private memory. Readable layer 318 links, 0 broken. ZIP 2,271,252 bytes, SHA256 312296c35c581d6471db37523a70e0f167a632d4627e7eb68405667ef57774f9; fresh extraction 86 files, SHA256SUMS PASS. No new claims, no publication/commit.
- Current work: answering user's questions on remaining tasks and hypothesis updates (chat only).
- Next action: researcher review; no automatic execution.
- References: /data/250010109/MoE_Router/experiments/20261108_snr_mig_pilot/handoff/20261108/1108-snr机制-mig先导-讨论包.zip (deliverable) and the same-name directory (00_导读_cn.md, SHA256SUMS.txt, manifest.json).
