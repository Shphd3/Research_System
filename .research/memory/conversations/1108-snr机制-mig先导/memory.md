# Conversation Memory: 1108-snr机制-mig先导

Conversation name: 1108-snr机制-mig先导 (user-suggested `20261108_SNR机制_MIG先导`, normalized to the existing `MMDD-topic` record format)
Processed by: Claude Code (harness: Claude Code CLI 2.1.280; model: claude-opus-5-5). The contract's agent list has no Claude entry; recorded as-is.
Created at: 2026-11-08T12:02:11Z
Latest update at: 2026-11-09T02:27:53Z
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

## 2026-11-09T01:22:10Z -- Research-system simplification implemented (researcher request 2026-11-09)

- Summary: Per uploaded research_system_iteration_prompt_cn.md and the user's instruction to change now: core AGENTS.md rewritten (61 lines: authority, evidence kinds, experiment standard, exploration lane, ≤3 active questions, iteration, training/assets, execution); formal rules moved to docs/formal_lane.md; standing Anchor-sync authorization removed (explicit trigger only); CLAUDE.md, docs/skills.md (3 exploration skills) and project AGENTS.md (32 lines) aligned; new docs/iteration_protocol_cn.md, templates/explore_log_cn.md, tools/meeting_digest.py (+test); 3 exploration skills rewritten lane-aware. PROJECTS.md has an AI-suggested active set (pending researcher confirmation; nothing formally frozen). Pilot log Projects/from-attention-to-search/main/explore/1109_snr_longtail/log.md. Cleanup: 29 dated process docs git-mv'd to docs/archive/process_records/ with relocation rows; 3.0 GB untracked unreferenced A05 payloads moved to /data/250010109/MoE_Router/research_record_archives/20261109_project_payloads/ (MANIFEST.sha256 verified); __pycache__ removed. sync/, XingyuD/, daily backups, kv_cache_main_latest untouched (proposals only). Pre-edit copies: /data/250010109/research_archive/20261109_system_cleanup/. Checks: 95 tests, skills, entrypoints, anchor organization, git payload, math all PASS. No commit/push.
- Current work: none; another Codex conversation (1109-teacher分发训练) owns docs/execution_envelope.md, assets/ and R03 — not touched.
- Next action: researcher confirms the active set and the cleanup proposals.
- References: AGENTS.md; docs/formal_lane.md; docs/iteration_protocol_cn.md; PROJECTS.md; /data/250010109/MoE_Router/research_record_archives/20261109_project_payloads/README.md.

## 2026-11-09T02:27:53Z -- Focus retired; records moved into System; redundant copies removed

- Summary: At the researcher's request: (1) project main/focus (60 files) removed via git rm; bytes archived at /data/250010109/MoE_Router/research_record_archives/20261109_focus_retired/ (MANIFEST verified); research_locations.json maps old paths; roadmaps, research_map.json evidence refs, formal_lane, project rules and research-progress-core updated. (2) Layout now: Research_System/research/from-attention-to-search/main = research history (5849 tracked files incl. .gitignore + explore log; ignored figures/tables moved along on disk, not tracked); Projects/from-attention-to-search (branch Xingyu) = code + README question summary + XingyuD; MoE_Router = payloads. Compatibility symlinks: Projects/from-attention-to-search/main -> research/...; research/.../XingyuD -> Projects/... (both locally excluded from git). Project index: 6006 staged deletions (records, XingyuD/sync, 3 duplicate skills, graph.yaml). check_current_entrypoints now reads research/<project> routes. 22 live System markdown files relinked. (3) System sync/ copies (anchors, research_maps, 1012/1014/1016) git rm'd; README and S000 kept. All checks PASS (95 tests, skills, 151 entrypoints, anchor organization on research/, payload both repos). Nothing committed or pushed.
- Current work: none. R03 (other Codex session) keeps writing through the main symlink; its untracked R03 directory is not added to System git.
- Next action: researcher authorizes commit/push of both repos (Xingyu branch push removes records from the shared team repo branch).
- References: research/from-attention-to-search/AGENTS.md; Projects/from-attention-to-search/AGENTS.md, README.md; docs/research_locations.json; tools/check_current_entrypoints.py.
