# Sharing, learning and routing: stage-report reading guide

**2026-10-07 exposition version note:** This remains the 1002 temporary candidate directory, not a promoted Focus. Maintained report/math bodies now explain objects, operations, control rationale and boundaries; values and frozen contracts remain unchanged. Dated records below retain their cutoffs: “current” refers to that historical window, and capacity NOT RUN does not describe other projects. The separate router-feedback [Summary](/data/250010109/Research_System/Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/summary.md) owns its new state, not results for these capacity arms. See the [revision delivery](../../../1007/editorial_revision_audit_cn.md) for roles, edits and retained history.

**Later-window entry:** [2026-10-04 understanding update](../../../1004/cognition_update.md) and [daily summary](../../../1004/daily_summary.md). The body preserves the argument and status from before the second window. Later CPU results are in [amplitude checks](router_shrinkage_summary.md) and [within-category controls](probe_33b_group_summary.md); later execution status is in Section 7 of the update.

Updated: 2026-10-04, Asia/Shanghai (UTC+8). [中文](reading_guide_cn.md).

These two days of work pursue one question: **when should texts share learning, when is separate learning worthwhile, and how can routing decide using information available before the target?** The work models update responses, finite action selection, learning from finite samples, and common computation separately, then examines their connections. Predictable local responses do not by themselves establish routing gains. Sharing gains in a conditional model do not by themselves establish gains in natural-text training.

Start with the [current stage report](sharing_routing_report.md). It carries the complete argument; this guide supplies the reading order and source locations. This remains a daily candidate folder. Reading materials do not change researcher-owned scientific judgments or formal record states.

All project-relative paths start at `Research_System/`. The reading directory is `daily_research_reports/1002/candidates/ntp_representation_update_channels/`. Add `_cn` before `.md` to locate each Chinese companion.

This round adds the [33B Summary](probe_33b_summary.md) and [Detailed](probe_33b_detailed.md), owning the four-part result and complete setup/domain/action-use/audit record, plus [17 primary-paper comparisons](sharing_literature_20261004.md) for external methods, information costs and limits. Their project-relative paths are this reading directory followed by `probe_33b_summary.md`, `probe_33b_detailed.md` and `sharing_literature_20261004.md`.

The new panel has been analyzed and reconstructed; the capacity repair passes CPU checks. Exact GPU Smoke and formal trajectories have not run. Sections 5.5–5.6 of the main report own current result/state reading. Historical Pending observations below are no longer current state.

## 1. Read the current report in full first

Read by question: start with the [two-minute brief and expanded explanation](../../../1006/meeting_report/meeting_brief_sharing_research_recovery_cn.md), then the [frozen-update Summary](probe_33b_summary.md) to distinguish common construction, fixed selection and frozen candidates. Stage-report Section 4 explains why one effect cannot decide long-term sharing; expand the mathematics as needed. Definitions are in those bodies, not required glossary memorization.

Responsibility: connect purpose, observations, explanations, models, checks, and changes in understanding. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_report.md`.

Read sections 1 through 6 in order. Each answers a different question:

| Order | Question answered | Distinction to retain |
|---|---|---|
| 1. Purpose | What understanding would an answer about shared and separate learning change? | Research purpose versus the smaller question currently measurable |
| 2. Observations | What has been observed, under which comparison and conditions? | Measurements versus proposed explanations |
| 3. Hypotheses and rivals | What could produce the observations, and which comparisons distinguish explanations? | Candidate hypotheses versus supported judgments |
| 4. Mathematical stages with common objects | How are actions chosen at a fixed model state? How do samples and specialization affect learning from a common initialization? How does common computation change representation and updates? | Fixed action selection, learning dynamics, and architecture computation |
| 5. Experimental checks and result analysis | Which relation does each actual comparison test, and what do validity and uncertainty allow us to infer? | Formula checks, natural-text measurements, and execution facts |
| 6. Updated understanding and the next question | What understanding has changed, and which unresolved question merits further work? | A scientific conclusion versus another metric inventory; researcher judgment versus AI suggestions |

For a shorter first pass, read sections 1, 2, 3, and 6, then return to sections 4 and 5 to examine the derivations and evidence. This gives an initial overview; full understanding still requires all six sections.

## 2. Trace the five stage documents in development order

The first four preserve the questions, comparisons, and limits of earlier stages. The fifth connects them to the current sharing and routing question. Dates and execution states in historical files are snapshots of their own periods. Read current execution facts in the current report and its cited receipts, rather than inferring them from historical entry points.

1. [Natural-text update responses](research_report.md) first connects actual continuations, shared-matrix updates, native representation movements, and finite loss changes. It explains what SAE readouts can describe and what they cannot replace. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/research_report.md`.
2. [Transfer between source batches](source_transfer_addendum.md) changes source batches while keeping the reader fixed. It separates predicting across sources from distinguishing which source is preferable. A and B contain different records within the same source domain. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/source_transfer_addendum.md`.
3. [Domain-response structure](domain_response_structure.md) separates within-domain A/B contrasts from relative effects across domains. It then examines prediction from an earlier prefix and update inputs omitted by the current output. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/domain_response_structure.md`.
4. [Common computation and limited capacity](capacity_report.md) extends the question to acquisition and retention by small experts. It discusses duplicated storage, statistical pooling, serial computation, and shared drift, and explains what architecture comparisons and local interventions each test. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_report.md`.
5. [Sharing decisions and routing](sharing_routing_report.md) synthesizes these developments and connects response prediction to finite action utility. It distinguishes selection at a fixed state, learning from a common initialization, and common computation. This is the rewritten primary reading entry. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_report.md`.

The source-transfer statement that “about 99% of the improvement comes from the mean component” refers to **the mean of A/B source-batch responses within each domain**. It does not average the four domains into one object or establish that their update effects are identical. Retain this definition in the second document; use the third to examine comparisons across domains.

## 3. Read mathematical details in dependency order

Section 4 of the current report first introduces the common objects and connections between stages. Consult the three mathematical documents below when checking derivations. Reading every formula is not a prerequisite for entering the main report.

1. [From updates to responses](mathematical_analysis.md) defines text events, the shared matrix, inputs, outputs, and next-token loss. It derives representation movements and loss changes from gradients, then distinguishes Fisher quantities, SAE coordinates, source means, and contrasts. It provides the basic response objects used by the other documents. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/mathematical_analysis.md`.
2. [Common structure and serial benefit](capacity_mathematics.md) specifies function families and learning rules before examining linear equivalence, nonlinear distinctions, different functional trajectories under the same parameter update, and statistical pooling with finite samples. It separates expressivity, estimation error, and retention, supplying conditions for the routing document's discussion of learning gains. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_mathematics.md`.
3. [Sharing decisions and routing information](sharing_routing_mathematics.md) relates finite sharing differences, information available before the target, prediction errors, and action selection. It then connects learning specialization, curvature, and estimation noise. Its conditions for compressed router information do not impose the same restriction on the expert's computational input. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics.md`.

Proofs and counterexamples answer questions within their assumptions. Conditions such as squared loss, independent samples, fixed tasks, fixed actions, or fixed step sizes cannot be dropped. Return to section 5 of the main report for actual measurements of the corresponding next-token relationships. Repeated language-token exposures cannot be substituted directly for independent sample counts.

## 4. Consult process and contracts by purpose

- The [process record](research_process.md) answers when work happened, why it continued, and where outputs are located. It preserves operational and reasoning history; completion records do not replace scientific conclusions. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/research_process.md`.
- The [current candidate Anchor](anchor.md) owns the candidate's question, hypotheses, model, and next decision. The report does not create a parallel design, and unconfirmed judgments remain Unknown. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/anchor.md`.
- The [current candidate Protocol](protocol.md) specifies comparisons, inputs, budgets, contracts, and amendments. Read it with its Chinese companion when checking the exact execution agreement. Finishing a report does not grant new authorization or produce a result. Project-relative path: `daily_research_reports/1002/candidates/ntp_representation_update_channels/protocol.md`.

The pre-rewrite README files, main report, and process records are preserved in `daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261004_before_reading_rewrite/`. Use that directory for version tracing. Start current reading with this guide and the main report.

## 5. Identify the comparison before interpreting a result

**Result analysis** explains a measurement, comparison, uncertainty, and rival explanations. **Scientific conclusions** explain how the evidence changes understanding of the original question. Section 5 of the main report handles the former; section 6 handles the latter. Where scientific judgment has not changed, retain the unresolved question rather than presenting a completion label as a conclusion.

Old-S7 finite updates, old Dense/S7/SALL training curves, the new fixed-state panel, and the capacity experiment's small-model architecture comparisons concern different models and time ranges. Training CE, finite interventions at a fixed checkpoint, and downstream task scores are not interchangeable. Check model identity, whether targets are available before the decision, baselines, and measured quantities in the main report before interpreting an outcome. Read execution facts separately from scientific conclusions.
