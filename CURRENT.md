# Current Research Log

This file is the operational entry for the current day. It does not replace
`PROJECTS.md`, project-local anchors, stories, or experiment records.

## Role

- `AGENTS.md` owns stable repository rules.
- `PROJECTS.md` owns the cross-project research map, active routes, claim
  boundaries, and project-level next decisions.
- `CURRENT.md` owns today's focus, what changed today, and the next action to
  resume. The current snapshot may be rewritten; dated ledger entries are
  append-only.
- Anchors own adjudicable questions and current claim boundaries.
- `summary.md` and `detailed.md` own measured experimental evidence.
- Stories own line-level synthesis.

Do not copy full theory or result tables here. Link to their source artifacts.

## Daily Use

At the start of the day, the researcher writes the question, current judgment,
uncertainty, and one intended decision without AI. During the day, record only
decision-bearing evidence or actions. At the end of the day, close the chat and
write the result, changed belief, claim boundary, and next decision from memory;
AI may then audit links and revise wording.

## Terminology / Definitions

| Term | Plain meaning and computation | Decision role | Cannot prove |
|---|---|---|---|
| NTP / shared-aux / informative-MTP | NTP activates only the next-token head; shared-aux activates a second head on the same next-token target; informative-MTP activates it on the second-future target | Separates system baseline, auxiliary-training structure, and future information content | That any condition is generally better |
| Source K/V | The key and value stored at `U03` for a later token to address and retrieve | Second-layer $K_{2,T},V_{2,T}$ patched inside each model | Tests whether the later standard head is causally controlled by the early source channel | That K or V alone is responsible |
| $\Gamma_{info}$ | informative-MTP controlled donor-switch effect minus matched shared-aux effect | $(p_{info}^{diff}-p_{info}^{same})-(p_{shared}^{diff}-p_{shared}^{same})$ | Primary metric for future-information-content-specific strong behavioral use | Weak margin-only use, natural-task value, or exclusive MTP information |
| Held-out oracle routing headroom | Native Router loss minus the loss from expert choices selected on calibration data and evaluated on a separate test split | Decides whether real expert-function differences are large and stable enough to justify Router work | That a learned Router can capture the gap |
| Mastery threshold $\tau$ | The standard-head accuracy used to declare the E04 task learned; Stage A chooses the largest eligible value from `0.80`, `0.90`, `0.95`, and `0.99` using NTP only | Freezes a non-saturated comparison point before any MTP result | A compositional algorithm or causal use of an intermediate state |
| Functional retrieval loss gap $\Delta_s(k)$ | Held-out standard-head loss using the $k$ memory items selected by score $s$, minus loss using the full memory | Tests whether a selector preserves prediction quality at a matched budget | Million-token scaling, independent item utility, or MoE expert value |

## Current Snapshot

Date: 2026-07-16

Overall specialization mainline:

> Decide whether unfiltered repository-level code completion has positive,
> cross-split-stable held-out oracle routing headroom after registered nuisance
> controls.

Source: [A06 research map](Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md) and [A06_04 anchor](Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md).

Today's working focus:

> Prepare one group-meeting claim around long-context functional retrieval:
> distinguish nominal capacity, evidence access, state formation, standard-head
> use, composition, Router selection, and real expert utility.

Source: [English working theme](daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme.md) and [Chinese companion](daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme_cn.md).

Result state: working theme drafted; no formal anchor, Protocol, or new run.
Existing R3/R4 evidence decisively answers the controlled Q0: perfect feature
specialization is not sufficient for a useful sparse KV index. The proposed Q1
asks whether current retrieval proxies predict causal loss utility under a
fixed top-$k$ budget.

Next action: the researcher completes the mechanism, strongest rival, most
uncertain point, judgment-changing evidence, and one next-decision fields, then
approves, modifies, or rejects Q1. Do not implement Q1 before an approved
Protocol.

## Daily Ledger

### 2026-07-15

Question: Does fixed-distance two-step composition amplify the training-speed
benefit of MTP over NTP on the common standard head?

Measured result: the in-support carrier is exactly learnable in all 24 tested
conditions. The objective-by-composition interaction is positive across both
formal model depths and both calibration seeds only at exact accuracy $1.0$;
it is not stable at thresholds through $0.99$.

Interpretation: the current evidence supports a candidate last-mile
exact-fitting effect, not a general composition-learning-speed advantage and
not causal use of the intermediate state.

Operationalization update: E03 was rejected because the task depths had
asymmetric query-relevant structure. E04 replaced it with paired per-sample
dual maps and completed 12 NTP-only trajectories. No scale passed both depths:
2-layer two-step accuracy ended near `0.250`, 4-layer two-step near `0.329`,
and one of three 4-layer one-step seeds remained at `0.838`. The post-run audit
also found that deleting one row from a full bijection leaves its value
recoverable by elimination.

System decision: remove the legacy `hypotheses/` and closure-report surfaces.
Keep hypotheses inside anchors, evidence inside experiment records, line-level
synthesis inside stories, and daily resumption state in this file.

Workflow decision: keep Thinking Cards independent from anchors; formal anchors
now link the approved human card and use sections 1-8. Meeting briefs contain
only a human-first executive summary, revised by AI after the initial draft.

Organization update: all 51 embedded historical Thinking Cards were extracted
verbatim into subject-bearing files, all formal anchors now link them, and the
obsolete active `00_handwrite_anchor.md` surface was removed. Root
`AGENTS.md` now contains only stable roles and hard boundaries. The root anchor
mirror is generated by `publish_anchor_mirror.py`, which rewrites cross-tree
links and can verify whether the published copy is current.

Claim boundary: no general MTP superiority, unseen-composition generalization,
intermediate-state causal use, real-task transfer, or MoE value is established.

Next decision: close E04 under the frozen contract or reopen carrier/capability
design in a new Protocol. Do not run MTP.

### 2026-07-15 — A11 model-local causal-use audit

Question: after matching standard-head capability, does K=2 MTP increase the
causal control of the later ordinary head by `U03` source K/V relative to NTP?

Human judgment: use must be separated from readability. The desired claim is
MTP-specific use, not merely that either trained model contains branch
information. The researcher approved source K/V intervention, capability
matching, the $\Gamma_{use}$ primary metric, and ordinary full-vocabulary CE
for every active prediction head.

AI audit: source Q is not the direct memory read by the later token. The later
`A_SHARED` query matches the source key and retrieves the source value, so the
first decisive intervention jointly patches source K/V. Q, K-only, V-only,
layer, horizon, and long-range variants remain parked.

Action completed: the Thinking Card was completed; bilingual `11_03_02`
anchors were written and approved; the Chinese-first
`A11_03_02_E01_model_local_kv_causal_use` Protocol was drafted. No code or run
was authorized.

Claim boundary: the proposed audit can establish only a controlled K=2 strong
behavioral causal-use increment at one model-local K/V interface. It cannot
establish general MTP, long-range, natural-language, composition, disentanglement,
or MoE value.

Next decision: approve, modify, or reject the Chinese Protocol draft. Only
after approval should the English canonical Protocol and implementation be
created.

### 2026-07-15 — A11 causal-control correction after comprehension audit

Question correction: NTP-versus-MTP alone cannot identify the effect of future
information content because active-head count, CE-term count, and loss
coefficients also change.

Human judgment: use source `U03` K/V as the primary intervention; keep both
source $Q_T$ and receiver $Q_{T+1}$ fixed; use ordinary full-vocabulary CE for
every active head; average the two active losses to preserve nominal scale.

AI audit: add a shared-aux condition whose second head duplicates the next-token
target. The primary contrast is now
$\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}$; NTP is a secondary
system baseline. Averaging losses does not match realized gradient norms,
directions, target difficulty, or optimization trajectories, so those quantities
are diagnostics rather than dynamically controlled variables.

Action completed: revised the Thinking Card, bilingual subanchor, parent-line
references, and Chinese Protocol draft. No code, English execution contract, or
run was created.

Claim boundary: a passing result can establish only that informative future
target content increases strong standard-head causal dependence on the tested
model-local K/V channel relative to matched shared-aux in this controlled task.
It cannot establish that the NTP target itself contains branch information or
that MTP is better on real tasks.

Next decision: approve, modify, or reject the revised Chinese Protocol. Only
after approval may the English canonical Protocol and implementation be created.

### 2026-07-15 — A11_03_02_E01 four-GPU execution started

Approval: the researcher approved informative-MTP versus matched shared-aux as
the primary causal contrast, $\Gamma_{info}$ as the single primary metric, the
revised Chinese Protocol, and a four-GPU remote run.

GPU smoke: all three ordinary heads and both active `U03` auxiliary targets
reached accuracy `1.0`; double-precision full-versus-incremental replay errors
were about `1e-14`, self-patch error was `0`, same-branch change rate was `0`,
and positive-control donor switching was `1.0`. At 200 smoke steps the
shared-aux/informative-MTP answer CE gap remained `0.133 > 0.05`, so the smoke
correctly did not claim a capability-matched research result.

Execution: ACP job `pt-pz6zjzzn`, run name
`a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`, one
`n6ls.iu.i40.4` node with four N6LS-80GB GPUs. Initial state: `INIT`.

Next decision: after the job completes, audit the frozen capability, cache,
same-branch, positive-control, pair-coverage, and confirmation guards before
reading the $\Gamma_{info}$ verdict.

### 2026-07-15 — A11_03_02_E01 result

Direct result: ACP job `pt-pz6zjzzn` succeeded. Five of five seeds passed the
common-capability and intervention guards. The mean primary metric was
$\bar\Gamma_{info}=0.01675$; `0/5` seeds reached `0.10`.

Decision: the registered strong behavioral information-content increment
failed. Seed 972 reached `0.08374`, concentrated in one branch direction; the
other four seeds were zero.

Secondary observation: informative-MTP minus shared-aux donor-margin movement
was positive in `4/5` seeds but dominated by seed 972. It is candidate weak or
redundant influence and cannot override the primary verdict.

Claim boundary: this rejects a reliable, independently answer-controlling
increment at layer-2 `U03` K/V in the controlled task. It does not establish
total non-use of MTP information or general MTP failure.

Next decision: preregister a weak-margin audit, or close this interface and move
to a task where the early state is structurally necessary.

Sources: [summary](Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md) and [detailed record](Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/detailed.md).

### 2026-07-16 — long-context functional-retrieval working theme

Question: what should a long-context Router optimize if the goal is not merely
to retrieve a matching item, but to preserve the ordinary head's correct
decision under a fixed compute budget?

User-supplied phenomenon: agent-heavy workloads increasingly place very long
histories into nominal million-token windows, while reliable use of the
necessary evidence remains limited.

AI-proposed synthesis: use long context as the workload and held-out functional
loss preservation as the candidate Router target. Keep the chain explicit:
access, formation/transport, standard-head use, ordered composition,
query-conditioned selection, and expert utility are different claims.

Existing decisive answer: R3/R4 already reject the controlled sufficiency
claim that perfect feature specialization automatically yields a useful sparse
KV index. A11 independently shows that earlier signal formation is not
sufficient for a strong standard-head use increment. A12 E04 cannot support an
MTP comparison because the capability and carrier-validity gates failed. A06
still owns the real-workload expert-utility premise.

Proposed smallest audit: on existing controlled checkpoints, compare random,
local, feature-aligned, and attention-based selectors using the matched-budget
standard-head loss gap $\Delta_s(k)$. Leave-one-out causal utility is secondary
and non-additive.

Claim boundary: the working theme does not establish general failure of
million-token models, a correct long-context Router target, an MTP retrieval
benefit, or transfer from the controlled checkpoint to real agents.

Next decision: the researcher completes the human judgment fields and
approves, modifies, or rejects the Q1 audit before any Protocol or execution.

Sources: [English working theme](daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme.md), [Chinese companion](daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme_cn.md), [R3](Projects/from-attention-to-search/main/experiments/archive/R3_perfect_router_retrieval/summary.md), and [R4](Projects/from-attention-to-search/main/experiments/archive/R4_attention_output_router_retrieval/summary.md).

## Entry Template

```text
### YYYY-MM-DD

Question:
My initial judgment:
Most uncertain point:
Evidence that would change my mind:
Action completed:
Measured result:
Confirmed:
Weakened or rejected:
Current mechanism and reason:
Claim boundary:
Next decision:
Source links:
```
