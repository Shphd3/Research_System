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
| AULC | Answer-NLL learning-curve area divided by its fixed step horizon | Measures ordinary-head finite-budget learning efficiency | Wall-clock speed or final capability |
| Task-relevance relay interaction $\Delta_R$ | Answer-$A$ versus nuisance-$B$ AULC benefit under relay, minus the same benefit under bypass | Tests whether downstream relevance matters specifically when the early state is necessary | Code, long-context, composition, or MoE transfer |

## Current Snapshot

Date: 2026-07-18

Overall specialization mainline:

> Decide whether unfiltered repository-level code completion has positive,
> cross-split-stable held-out oracle routing headroom after registered nuisance
> controls.

Source: [A06 research map](Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md) and [A06_04 anchor](Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md).

Today's working focus:

> Decide whether a verified tree low-rank propagation theorem has a
> non-vacuous empirical bridge to gold syntax, pretrained decoders, and a
> paired hierarchy-training intervention.

Source: [A14 anchor](Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_tree_low_rank_language_structure_anchor.md) and [overall result](Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/summary.md).

Result state: the theorem/implementation audit passed with maximum normalized
violation `2.92e-8`. Gold PPMI constituents had a 34.2% held-out subspace
advantage but required 657/2048 directions and missed the strict rank budget.
Qwen and Pythia showed strong true-span and parent-child geometry, but their
pretrained bound ratios were 10.80 and 1.77; the Pythia training increment did
not replicate. In the paired causal intervention, all 12 descriptive
tree-subspace effects were positive (mean `+0.1796`), all 12 composition
effects were negative (mean `-0.0469`), latent rank tracked latent state count
(`rho=0.949`), and no final hierarchy transition had a non-vacuous bound.

Next action: design one same-parent, same-token alternative-split experiment
that traces prediction versus stability. Continue the propagation mechanism
only if an out-of-sample operator beats the alternative split and has
`B / ||H_parent||_F < 1`.

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

### 2026-07-16 — A11 exact source-K/V information audit

Question: did the exact layer-2 `U03` K/V patched in E01 contain stable branch
information, and did informative-MTP strengthen its held-out readability beyond
matched shared-aux?

Action completed: implemented an approved same-contract replay and source probe
on the remote four-GPU ACP surface. Job `pt-rqtb6bw0` succeeded. No local or CPU
model smoke was run.

Measured result: E01 checkpoints and behavior statistics replayed exactly.
NTP, shared-aux, and informative-MTP all reached held-out branch accuracy and
four-class recall `1.0` for exact $[K_{2,T};V_{2,T}]$ in every seed. The
registered primary metric had mean
$\bar\Gamma_{\mathrm{read}}=-0.002299$ nat/example, 95% CI
`[-0.004502,-0.000173]`, and was nonpositive in `4/5` seeds.

Formal verdict: insufficient. Three of 15 single-shuffle probes exceeded the
registered `0.30` maximum-accuracy guard. Post-result audit found mean shuffled
accuracy `0.2209` and mean CE `1.4427`, suggesting a miscalibrated maximum guard
rather than broad leakage, but the registered verdict was not changed.

Confirmed: the patched exact K/V object is not linearly branch-empty.

Weakened or rejected: informative-MTP does not make the branch label more
readable under the registered saturated probe. The combined E01/E02 evidence
cannot be stated as “MTP-specific information formed but the standard head did
not use it,” because NTP and shared-aux are equally perfectly readable.

Current mechanism and reason: informative-MTP may reorganize already-readable
branch information. Its Fisher separation exceeded shared-aux in `5/5` seeds
by `2.91–49.55` times, mainly through within-branch nuisance contraction. This
is secondary geometry, not causal-use evidence.

Claim boundary: no total ordinary-head non-use, general MTP failure,
shared-unembedding repair, long-range transfer, natural-language benefit, or
MoE value is established.

Next decision: validate a learnable `relay-required` carrier with no direct
answer bypass and a non-saturated shared-aux baseline before any new objective
comparison.

Sources: [summary](Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md), [detailed record](Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/detailed.md), and [advisor-response note](daily_research_reports/0716/docs/a11_exact_source_kv_result_and_advisor_response_cn.md).

### 2026-07-16 — A13 task-relevant necessary-relay result

Question: which minimal task property makes earlier future-style supervision
useful to the ordinary next-token head?

Action completed: created the A13 parent hierarchy and executed a staged
carrier-first chain. The query-conditioned carrier was closed as unstable; an
entropy-matched single-value NTP relay passed; two broad objective comparisons
remained formally insufficient; fresh-seed one-label localization and
answer-$A$ versus nuisance-$B$ controls were then executed.

Measured result: the decisive $B$-versus-$A$ control passed. Relay utility was
`0.2315` nats with interval `[0.1792, 0.2791]`; bypass utility was `0.0181`
nats; the interaction was `0.2134` nats with interval
`[0.1646, 0.2585]`. Relay utility and interaction were positive in `8/8`
paired seeds. All four final capability cells and both relay donor-use audits
were `1.0`.

Confirmed: earlier supervision has finite-budget ordinary-head value when it
names the downstream answer variable and is attached to a state on the only
answer path.

Weakened or rejected: token distance, target variability, a generic auxiliary
head, or “NTP never sees the answer” are not sufficient explanations. Requiring
every post-treatment objective arm to pass capability is also rejected as a
performance inclusion rule.

Current mechanism and reason: answer-aligned auxiliary credit trains the relay
state toward the variable that the later ordinary head must consume; the same
supervision has little marginal value when the answer can read the variable
directly.

Claim boundary: no general MTP, standard-implementation equivalence, long-range
scaling, composition, paraphrase invariance, code/text transfer, planning, or
MoE utility is established.

Next decision: validate query-conditioned binding as a separate NTP-only
carrier property before adding composition.

Sources: [Chinese story](Projects/from-attention-to-search/main/stories/13_mtp_task_property_decomposition/01_task_relevant_relay_supervision_cn.md), [decisive summary](Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md), and [meeting-ready report](daily_research_reports/0717/mtp_long_horizon_compositional_workload/mtp_task_property_decisive_report_cn.md).

### 2026-07-17 — A13 soft-relay Stage-0 stop

Question: as the direct `ANSWER -> A` attention edge is progressively
weakened, does informative-MTP utility grow with measured causal reliance on
the relay rather than appear only under a hard mask?

Action completed: froze penalties `0`, `2`, `4`, and hard mask; ran the
NTP-only carrier audit on eight fresh seeds per path using four H100 GPUs; and
applied the registered stop rule before any objective comparison.

Measured result: every path reached final accuracy `1.0`. Across the four
paths, the direct-deletion NLL effect decreased from `9.2764` to `0`, the
wrong-relay donor effect increased from approximately `0` to `11.8856`, and
the relay-reliance ratio increased from approximately `0` to `1`. The direct
condition nevertheless reached `0.90` accuracy at step `20` in `8/8` seeds,
the first positive checkpoint, so the common non-saturated-window gate failed.

Confirmed: the frozen attention penalties cause an ordered shift in actual
causal path use, not merely an ordered change in nominal attention strength.

Weakened or rejected: the current 20-step measurement cadence is sufficient
to identify a fair common early-learning window. No MTP hypothesis is rejected
because shared-aux and informative-MTP were not run.

Current mechanism and reason: weakening the direct edge moves answer control
onto the relay, but it also slows NTP learning sharply; without resolving the
early direct-condition learning curve, an apparent utility trend could be a
ceiling or baseline-difficulty artifact.

Claim boundary: the result does not identify informative-MTP utility, its
continuity with relay reliance, a gradient-dose explanation, or transfer to
code, natural language, long context, planning, or MoE.

Next decision: approve or reject a measurement-only rerun that records every
step through step `40` while preserving all data, model, objective, path,
seed, optimization, and budget choices.

Sources: [soft-relay summary](Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_06_E01_soft_relay_mtp_ntp_audit/summary.md) and [detailed record](Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_06_E01_soft_relay_mtp_ntp_audit/detailed.md).

### 2026-07-17 — diffusion-language-model line incubation

Question: why do diffusion language models still trail autoregressive models
on important quality--cost comparisons, and does MoE repair the cause or only
change per-forward capacity and systems cost?

User-supplied phenomenon: “Diffusion语言模型结果不是那么好.” The user also
requested a new research mainline, accurate anchors, independent experiments,
and a specific MoE assessment.

Action completed: audited primary literature through 2026-07-17; separated
pure masked diffusion, block diffusion, joint AR--diffusion objectives, and
AR-context/verification hybrids; created an independent project entry,
candidate D00--D03 roadmap, literature evidence record, human Thinking Card,
and thin graph. The existing expert-specialization graph was not edited.

Direct literature result: pure masked diffusion remains disadvantaged in the
studied compute-normalized training regime and on dependency-sensitive exact
sequence generation. Blockwise and AR--diffusion hybrids substantially improve
the practical frontier. MoE establishes sparse-capacity and routing/system
benefits; expert-choice routing gives a matched-FLOP result for allocating more
capacity at low mask ratios, but no audited result shows that MoE removes the
unmasking quality--parallelism trade-off.

Measured local result: none. The user has not yet supplied or approved the
mechanism guess, strongest rival, judgment-changing evidence, and exactly one
scientific decision required for a formal anchor. Therefore no formal anchor,
Protocol, remote workspace mutation, cluster job, or result record was created.

Claim boundary: the literature audit does not establish a universal diffusion
failure, a single algorithm that is best under every deployment regime, a
local causal reproduction, or semantic MoE expert specialization.

Next decision: approve, modify, or reject the diffusion Thinking Card and the
D00 comparison-contract -> D01 objective -> D02 sampler -> D03 MoE order.

Sources: [project entry](Projects/diffusion-language-models/README.md),
[Thinking Card](Projects/diffusion-language-models/main/problem_anchors/00_diffusion_language_model_failure_mechanism/00_diffusion_language_model_failure_mechanism_thinking_card_cn.md),
[evidence audit](Projects/diffusion-language-models/main/literature/2026-07-17_diffusion_language_model_evidence_audit.md),
and [project graph](Projects/graphs/diffusion_language_models.graph.yaml).

### 2026-07-18 — A14 tree low-rank language-structure audit

Question: does a shared low-dimensional leaf state plus stable hierarchical
composition give a non-vacuous explanation of low-rank language-model node
representations?

Action completed: formalized and proved the conditional propagation theorem;
created approved protocols; implemented 16 passing unit tests; ran 809
synthetic conditions, a gold-treebank PPMI audit, pretrained Qwen/Pythia with
identical random baselines, and 24 paired small-Transformer training runs;
audited and copied all central figures; wrote per-experiment and overall result
records; and updated the bilingual anchor.

Measured result: E01 passed with maximum normalized violation `2.92e-8`.
E02 found a 34.2% gold-constituent projection advantage but selected rank
657/2048. E03 found Qwen leaf/composition advantages 27.7%/66.5%, yet its
bound ratio was 10.80; Pythia did not replicate the training-created
composition effect. E04 produced an all-pair descriptive tree effect `+0.1796`
and composition effect `-0.0469`, rank correlation `0.949`, and 0/48
non-vacuous final bounds. Its registered verdict remained insufficient because
0/12 pairs passed the root-probe equality guard.

Confirmed by direct evidence: the conditional theorem is implemented
correctly; true spans have shared subspace geometry in the tested coordinates;
and hierarchy-aligned order can causally create tree-boundary compression in
the controlled generator.

Weakened or rejected: universal absolute leaf low rank, a replicated
training-created shared-linear parent operator, and the claim that the current
recursive norm bound explains pretrained or trained geometry. Cross-parent
permutation is also weakened as a syntax control because it changes child
content while the parent is their literal concatenation.

Current mechanism and reason: the evidence favors scale- or tree-conditioned
subspace selection/compression over one globally stable linear propagation
operator. This is an AI evidence synthesis; the researcher has not supplied a
separate closed-book post-run judgment.

Claim boundary: no coordinate-invariant language rank, internal gold-tree
construction, causal pretrained-LLM computation, or behavioral necessity is
established.

Next decision: run one same-parent, same-token alternative-split and
prediction/stability-frontier experiment; continue only if the same operator
beats that control and gives a non-vacuous held-out bound.

Sources: [overall summary](Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/summary.md), [overall detailed record](Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/detailed.md), and [bilingual anchor](Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_tree_low_rank_language_structure_anchor_cn.md).

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
