# 1002 temporary candidate: sharing, finite utility and MoE routing

## Second research window, 2026-10-04: latest understanding

Read the [new understanding update](../../../1004/cognition_update.md), at `daily_research_reports/1004/cognition_update.md`. The separate [daily summary](../../../1004/daily_summary.md) retains its 15:53:50 UTC cutoff. The update keeps the same Anchor and adds within-source/switch accounting, category-matched controls, out-of-fold amplitude selection, and explicit derivations of effects through future learning. Its Section 7 and execution receipts own the current four-GPU job status.

New canonical results: [amplitude Summary](router_shrinkage_summary.md) / [Detailed](router_shrinkage_detailed.md), and [group-decomposition Summary](probe_33b_group_summary.md) / [Detailed](probe_33b_group_detailed.md). These are exploratory analyses of exposed fixed banks, not new joint-training results. Earlier statements below about no submission or pending permission are historical snapshots; this window has explicit researcher execution authorization.

## 2026-10-04 current reading entry (Asia/Shanghai, UTC+8)

Start with the [reading guide](reading_guide.md), then read sections 1 through 6 of the [sharing and routing stage report](sharing_routing_report.md): purpose, observations, hypotheses and rivals, mathematical stages, experimental checks and result analysis, and updated understanding with the next question. For an initial overview, read sections 1, 2, 3, and 6, then return to sections 4 and 5 to check the derivations and evidence.

The guide locates five stage documents, three mathematical explanations, and the process record, Anchor, and Protocol. The main report carries the complete argument. Their project-relative paths are `daily_research_reports/1002/candidates/ntp_representation_update_channels/reading_guide.md` and `daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_report.md`. Result analysis explains measurements; conclusions explain how evidence changes understanding. Keep proofs in conditional models distinct from natural-text measurements.

The dated historical text below is preserved. Its job states and authorization statements describe their own snapshots. Read current execution facts in the main report and its cited receipts. The “about 99% mean component” always means the within-domain A/B source-batch mean, not an absence of differences across the four domains. Pre-rewrite versions are preserved in `daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261004_before_reading_rewrite/`.

## 2026-10-04 closeout: new analysis, repair and literature

Frozen new-panel analysis and independent numerical reconstruction are complete. All 92 pooled cross-source conditions beat global usage-matched random allocation but lose to the FIT-fixed common action. Matching information does not yet justify adoption. The capacity dtype error has a minimal CPU-validated repair; exact GPU Smoke remains unsubmitted, with all 12 formal trajectories and 18 mechanism outputs NOT RUN.

- [Current stage report](sharing_routing_report.md): Section 5.5 explains the new result, Section 5.6 inventories live state, repair and missing runs, and Section 6 reconnects evidence to the original question.
- [33B Summary](probe_33b_summary.md) and [Detailed](probe_33b_detailed.md): actual finite CE, domains, action use, within-source secondary comparisons and provenance. All [920 DEV rows](evidence/probe_33b_all_readout.csv) are retained.
- [17 primary-paper comparisons](sharing_literature_20261004.md): shared representations, multitask grouping, old-function protection and MoE evidence, with information, computation and transfer limits.

This round did not rerun the old 80-row comparison, submit another GPU job, expand scientific scope or change scientific state. New GPU Smoke permission was requested separately; CPU completion does not certify GPU execution. A [snapshot](history/20261004_before_closeout_update/snapshot.json) preserves nine entrypoint/manifest originals from before this update.

## 2026-10-03 07:27–10:47 UTC: sharing decisions and MoE routing

Start with the [current sharing/routing report](sharing_routing_report.md), then the [decision mathematics](sharing_routing_mathematics.md). The researcher authorized approximately 3h20 of continued work toward better MoE routing and architecture; SAE and spectra remain analysis tools.

The old-S7 finite-action utility, group controls and eight-family input comparison are complete. Several representations retain within-category decision information without stable gains over the strong FIT-fixed action; the full-input fitted linear rule does not dominate lower-dimensional representations. Conditional derivations join predictable learning differences, finite-step curvature and estimation noise into a more complete sharing criterion. Routers may use decision features while experts retain complete causal inputs. Better online MoE or downstream performance has not been established. Read the report for all values, counterexamples, intervals and boundaries.

The [Anchor](anchor.md) owns the current question. The [Protocol](protocol.md) preserves capacity contracts with appended routing comparisons; [previous originals and reading copies](history/20261003_before_routing_refinement/) remain available. New job `pt-meoxfrko` measures a new Dense/S7/SALL exact 33B panel; capacity job `pt-uasnh61d` stays separate, both on 8×5090 SPOT. Submission is not a result. Latest verified state is in the report and [job ledger](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/job_ledger.json).

## 2026-10-03 04:14–06:44 UTC: preceding capacity research window

The question is refined to whether limited private experts can reuse common computation and approach a larger Dense model while retaining learned domains. The researcher explicitly authorized approximately 2.5 hours of autonomous work and 8×RTX5090 SPOT training. Earlier no-remote-training/approval statements below belong to the October 2 historical window.

This window produced the [capacity and mechanism report](capacity_report.md).

That window's temporary design: [Anchor](history/20261003_before_routing_refinement/reading/anchor.md), [Protocol](history/20261003_before_routing_refinement/reading/protocol.md); [previous versions](history/20261002_before_capacity_refinement/) remain intact. No formal project promotion. The [new execution root](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity) holds six arms × two seed/order blocks, each with 37,748,736 valid-token exposures. Job `pt-uasnh61d` is submitted; submission is not completion or scientific support.

Read the [linear capacity argument and counterexample](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/math_capacity_round2.md) and [implementation audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/code_audit_round1.md). Results and finite rollback analyses will be added here. The [process log](research_process.md) records actual progress.

The text below is the October 2 history with its original numerical and claim boundaries.


This is the researcher-requested daily candidate folder. It is outside the formal project and does not replace any existing Focus, Anchor, Protocol, or frozen result.

**Purpose:** understand reproducible learning relations between natural texts and use S7 with its SAE sidecar to explain those relations in representation space. The net benefit of longer shared versus separate training remains a separate question.

Research window: 2026-10-02 16:44–18:44 Asia/Shanghai. Authorized work includes sustained research, mathematical analysis, bounded local analysis of existing natural-text caches, and candidate design/report writing. This task does not launch a new expensive remote experiment or long training trajectory.

The presentation starts with the question and bounded answer, gives a concrete example, connects the computation, and ends with the evidence boundary and next decision. Derivations, measurements, and AI proposals remain separate.

**Deeper update (from2026-10-02 17:30 UTC):** the previous99% mean component averages A/B batches within each domain; it is not the common response across four domains. Relative domain effects partly reproduce. Removing amplitude along the selected common parameter axis retains about69% of derivative cross-half response inner product. Yet an earlier-prefix forecast of eight future targets yields only about0.077%/0.289% incremental SAE Q, with stronger ordinary projections. Inputs annihilated in the current output still contribute to update effects; this is neither a lost-information fraction nor an identified cause of low Q. See [domain effects, continuations and visible information](domain_response_structure.md).

**Continuation update (from 2026-10-02 16:35 UTC):** frozen predictors retain about 0.48%–0.60% finite-response prediction-error improvement across two sources with disjoint records. About 99% of the current fixed-regularization own-source absolute MSE improvement comes from the within-domain A/B mean response. Within-domain A/B contrast-specific tuning yields an SAE gain of about 0.009%: very small, but not established as zero. These are two-source exploratory readings on the old panel under previously constructed features, not general source-population transfer. See the [source-transfer continuation](source_transfer_addendum.md).

## Current answer

These source updates help every readout-domain mean, while about 44%–53% of individual effects are adverse and changing source halves reverses some event signs. Pre-update SAE features provide modest finite-response readout gains; native projections also help. Low static SAE reconstruction error does not guarantee faithful code-difference reconstruction of small native movements.

This round connects natural texts, source updates, native displacement and actual loss while exposing tool and source-stability limits. Long-term separation value still needs a direct comparison. Values concern the old scientific-text panel and the specified S7 state.

## Reading order

Start with the [stage report](research_report.md), which connects purpose, hypothesis, three analysis steps, exact natural events, findings and boundaries. Each of its three figures has source tables and provenance.

| File | Purpose | Status |
| --- | --- | --- |
| [Research report](research_report.md) | Understand the advance and unresolved question | Exploration on exposed natural texts |
| [Deeper domain-response analysis](domain_response_structure.md) | Within-domain batches versus domains, strict prefix forecast, common axis and input kernel | Additional old-panel exploration |
| [Mathematical analysis](mathematical_analysis.md) | Continuation → gradient → native displacement → finite loss; Fisher/SAE counterexamples | Conditional derivations with numerical checks |
| [Candidate Anchor](history/20261002_before_capacity_refinement/reading/anchor.md) | One question, hypothesis, model, falsifier and next decision | `CANDIDATE_FOR_REVIEW` |
| [Candidate Protocol](history/20261002_before_capacity_refinement/reading/protocol.md) | Concrete prospective comparison, inputs, fitting, inference and scope | `DRAFT_NOT_EXECUTABLE`; independent groups/resources unresolved |
| [Process record](research_process.md) | Stage operations, bounded conclusions and repairs | Actual time sequence |

## Evidence and ownership

[Selected evidence](evidence/) and [figures](figures/) support this reading bundle; the [payload manifest](payload_manifest.json) records sizes, hashes and origins. Models, raw data, per-event arrays, code and logs remain in the [execution workspace](/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/README.md).

The researcher owns scientific judgment and state transitions. Written documents, passed identities and completed CPU evaluation do not approve new confirmation. Formal historical Summaries retain their verdicts; this candidate bundle does not re-adjudicate them.

[中文入口](README_cn.md).
