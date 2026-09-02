# Projects

Current-state registry for `Research_System`. Read after `AGENTS.md`. The
repository may contain multiple explicitly named active workstreams. For any
task, first select the owning workstream below, then read that workstream's one
active `daily_research_reports/MMDD/focus_<problem>.md` and resume point.

## Active Project

| Role | Path / value |
|---|---|
| Theme | feature-level expert specialization in top-1 MoE gating |
| Project | `Projects/from-attention-to-search/` |
| Worker surface | `Projects/from-attention-to-search/XingyuD/` |
| Active branch | `Xingyu` |
| Read-only reference | `Projects/kv_cache/` |
| Graph | `Projects/graphs/expert_specialization.graph.yaml` (navigation snapshot; known stale A06 active markers) |
| Root sync | `sync/S000_current_specialization/` |

## Current Focus Priority And Conversation Ownership

| Problem key | Role | Owning Focus | Conversation owner | Ownership status |
|---|---|---|---|---|
| `A15.m2d2_semantic_representation_geometric_form` | `PRIMARY` | `daily_research_reports/0901/focus_m2d2_semantic_geometric_form.md` | `codex-thread:01a05d72-0a0c-7a61-be1d-d5df101a2ef2` | `CLAIMED`; PCA-64 and centered raw-1,024 full audits both complete with `RADIUS_CONTRIBUTING`; AI result wording awaits human confirmation; token screening requires new explicit approval |
| `A15.semantic_supervision_middle_layer_separability` | `SECONDARY` | `daily_research_reports/0901/focus_m2d2_causal_lm_semantic_routing.md` | `codex-thread:01a054b9-ff32-7012-aae0-ccfea85152cf` | `CLAIMED`; M2D2 full evidence complete, typed Oracle Pass and learned-Router Fail awaiting human result wording |
| `A15.qwen3_30b_fixed_fact_expression_separability` | `SECONDARY` | `daily_research_reports/backup/2026/08/0830/focus_qwen3_30b_semantic_representation_separability.md` | `codex-thread:01a04dd1-ba8c-7131-b880-c48646566d66` | `CLAIMED`; independent execution may continue |
| `A15.counterfactual_utility_residual_expert_growth` | `SECONDARY` | `daily_research_reports/backup/2026/08/0829/focus_gradient_consistent_hierarchical_routing.md` | `UNCLAIMED` | `RELEASED`; completed cycle, no implementation or run authorized |

The first row is the current main attention route. The remaining rows are
retained as secondary scientific routes and do not share a problem key with
the primary route. Other legacy evidence-closure rows below remain independently readable;
before any is resumed for edits or execution, register its stable problem key,
role, and conversation owner here and in its Focus. A conversation must not
work around an existing claim by renaming the same question.

## Active Research Workstreams

There is no repository-wide singleton execution state. Every listed workstream
has its own current Focus, evidence state, and next decision; work in one does
not silently pause or replace another.

| Workstream | Priority / state | Current Focus | Evidence or contract | Current decision / resume point |
|---|---|---|---|---|
| A15 M2D2 semantic representation geometric form | **PRIMARY**; PCA-64 E01 and centered raw-1,024 E02 full runs complete; E02 passes 14/14 guards and reproduces `RADIUS_CONTRIBUTING`; AI wording awaits human confirmation | `daily_research_reports/0901/focus_m2d2_semantic_geometric_form.md` | E01 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/summary.md`; E02 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E02_m2d2_full_dimension_geometry_robustness/summary.md` | Preserve the bounded answer: whole-window domain information is direction-primary and radius-contributing with or without PCA; fine diagonal-density advantage weakens in raw 1,024 dimensions, final-token signal remains near zero, and independent shape is not established. Stop and await explicit approval before current-token versus causal-prefix screening; the second gate remains unauthorized. |
| A15 semantic supervision for middle-layer separability | **SECONDARY**; M2D2 E07/E08 full execution is complete and eligible. Hard semantic grouping passed the next-token value and child-intervention gates with worst-control NLL advantage `0.001506 [0.001396, 0.001618]`, while learned semantic supervision improved route semantics and child utility but was worse than task-only by `0.001054` NLL/token. Typed verdicts are Oracle `PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP` and learned `FAIL_NO_LEARNED_FUNCTION`; human wording remains pending. | `daily_research_reports/0901/focus_m2d2_causal_lm_semantic_routing.md` | E07 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E07_m2d2_learned_semantic_router_ntp/summary.md`; E08 Summary is adjacent under `A15_13_E08_m2d2_hard_semantic_route_ntp/` | Confirm the bounded result, then run only an evaluation-time predicted/gold index × probability/unit coefficient decomposition. Keep this functional result independent from the separate geometric-form verdict. |
| A15 Qwen3-30B fixed-fact cross-expression semantic separability | **SECONDARY**; E01/E02 computation and independent audit complete; AI wording awaits human confirmation; E03 is `NOT_RUN` and awaits resource confirmation | `daily_research_reports/backup/2026/08/0830/focus_qwen3_30b_semantic_representation_separability.md` | `Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/summary.md` | Preserve the layer-local boundary: Blocks 4/12/44 establish within-bank robust but cross-bank-incompatible readout; full two-bank training yields a common certified boundary at Blocks 4/12/20/44 but mixes coverage and sample count. The audited 4x RTX5090 candidate awaits user confirmation; an 8x choice requires a separately frozen entry. Execute only the frozen-probe TAX-C4A joint-shift test next; do not infer Gate use, expert utility, or LM gain. |
| A15 native-$G$ domain-consensus MVP | computation complete; registered machine verdict `PASS`; awaiting human result wording | No separate Focus; predecessor evidence under the A15 primary workstream | `Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_01_E01_native_g_domain_consensus_variance_atlas/protocol.md` | Preserve the bounded reading: all eight stability guards passed and Block-46 overlap exceeded its matched-null 97.5% threshold, but the null-corrected effect was only 0.000779 and does not establish that reuse explains the 16-versus-53 compression. Do not create an experiment-level Focus or start Router training; reactivate only if the researcher declares an independent next question. |
| A15 rank-specific multi-representation subspace audit | computation complete; canonical evidence drafted; awaiting human result wording | `daily_research_reports/backup/2026/08/0827/focus_rank_specific_multirepresentation_subspace.md` | `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/summary.md` | Confirm or correct the bounded evidence update in the active Focus before any Anchor update, daily report, or new representation-learning run. |
| A15 cross-parent fine-function transfer | evidence complete; 0/6 layers established registered transfer; AI interpretation awaiting human result wording | No separate Focus; predecessor evidence under the A15 primary workstream | `Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md` | Preserve the bounded reading as predecessor evidence. Do not create an experiment-level Focus or start Router training; reactivate only if the researcher declares an independent next question and approves a new Protocol. |
| A15 counterfactual-utility residual expert growth | **SECONDARY**; cycle complete and daily report human-confirmed; 8×RTX5090 evidence owns the cycle; collision-isolated 4×H100 E01H/E03H accepted only as non-owning sensitivity | `daily_research_reports/backup/2026/08/0829/focus_gradient_consistent_hierarchical_routing.md` | `Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/summary.md`; H100 package: `daily_research_reports/backup/2026/08/0829/docs/gradient_consistent_hierarchical_routing_h100/README.md` | Preserve the bounded result: the supplied correct residual tree realizes the theorem, but no hierarchy advantage or current online-utility gain is established, and Qwen top-8 accessibility is not expert utility. Within this secondary workstream, the sole next decision is an upstream frequency (high/low) × cross-child gradient-consistency (high/low) representation-formation contract; park its separate utility-search variants, and do not implement or run before a new confirmed Anchor/Protocol. |
| A15 native-Router representation boundary | computation complete; awaiting human result wording and external H1 review | `daily_research_reports/backup/2026/08/0824/focus_random_projection_router_preservation.md` | `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/summary.md` | Preserve the measured readability result and its negative-margin boundary; do not reinterpret it as the current coarse--fine geometry question. |
| A15 stable discriminant-space evidence | evidence complete; awaiting human judgment | `daily_research_reports/backup/2026/08/0820/focus_stable_domain_discriminant_subspaces.md` | `Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/summary.md` | Record the human claim boundary for the completed controlled/natural tracks; it is prior evidence, not the current execution contract. |

The 0821 E05 result is now predecessor evidence for the explicitly approved E06
metric audit rather than an executable task. A06, A15, and A16 retain independent scientific states and
may be active concurrently when each has an explicit Focus and resume point.

`Projects/kv_cache` is read-only unless the user explicitly authorizes edits.
Only its `xyDeng` branch is managed here; never push its `main` branch.

A15 spectral representation geometry and functional routing, and A16
load-control gradient interference, are both research lines inside
`Projects/from-attention-to-search/`. A15 owns Router-input geometry, spectral
learning dynamics, representation atlases, independent middle/tail information
audits, functional coordinate admission, and online spectral routing; A16 owns load-control mechanism,
LM-versus-load-gradient interaction, and mechanism-conditioned intervention
selection. Neither line scientifically pauses or gates the other. Their checkpoints, raw logs,
calibration caches, and full run outputs remain under the verified
`/data/250010109/MoE_Router/` worker surfaces.

## Incubating Project — Diffusion Language Models

| Role | Path / value |
|---|---|
| Theme | objective, sampling, and systems causes of the diffusion-LM quality--cost gap |
| Project | `Projects/diffusion-language-models/` |
| Graph | `Projects/graphs/diffusion_language_models.graph.yaml` |
| State | literature audit complete; human Thinking Card approval required before formal anchors or experiments |
| Current source | `Projects/diffusion-language-models/main/literature/2026-07-17_diffusion_language_model_evidence_audit.md` |

This new line does not replace the active A06 project or inherit its worker
surface. Its candidate D00--D03 anchor decomposition remains draft. No remote
workspace, protocol, job, or result record is authorized until the researcher
approves or corrects the independent Thinking Card.

## Implementation Project — De-common Router Training

| Role | Path / value |
|---|---|
| Theme | representation routing after subtracting a deployable common estimate |
| Project | `Projects/decommon-router-training/` |
| Model surface | `Projects/decommon-router-training/src/decommon_router/model/` |
| Mechanism route | M01 estimator validity -> M02 Router-input causality -> M03 matched-load functional utility |
| State | pairs 01--04 are invalidated/retired: pair-04 reserved baseline `om-edftl2bs` and idle de-common `om-q7ozeo0u` both failed the checkpointable loss-reversal guard at step 2,260 / 1.851B tokens; no replacement production pair is approved |

This user-requested implementation surface refactors the current
`/data/250010109/MoE_Router` baseline and explicitly excludes the older
spectral/Oja injection path. The provisional common estimator is a
distributed, per-layer exponential moving mean; only the Router sees the
centered representation, while sparse and shared experts receive the original
state. Native DDP is the measured primary path for the maintained 342M and
576M 8E/top-2 candidates; native EP=2 remains the memory-scaling fallback.
Two-H100 capacity, real signal-driven resume, EP-sharded resume, and guarded
reserved/idle ACP launch paths are complete. The target 342M model then passed
a four-H100 idle ACP full-pipeline acceptance at 26.2144M tokens: cumulative
throughput including checkpoint I/O was 166.0k token/s, full-state saves had
an 8.27-second median, all five evaluation suites completed, and all 12
machine gates passed. This remains engineering evidence only. AFS quota and
storage controls are audited: canonical 342M/576M runs have 150/230 GiB hard
caps, retain two rolling full recovery checkpoints, and retain one full
weights-plus-optimizer milestone every 1B tokens. Read-only ACP monitoring is
implemented locally. The four-GPU acceptance used an audited temporary
compatibility bridge for the installed component/API mismatch and restored the
original component afterwards; future live monitoring requires an updated
component or an explicitly audited compatibility layer. No recurring Codex
monitor has been activated.
The final local replicated-DDP full-pipeline smoke passed 12/12 gates after a
real `SIGTERM`: it resumed from 64 tokens, finished at 768 tokens, retained two
rolling recovery points and three complete milestones, loaded the final
milestone for held-out loss and limited LAMBADA/PIQA scoring, and occupied
0.277 GiB excluding linked dataset targets. This is engineering evidence only.

Pair-04 used a 342M, 12-layer, 8E/top-2, 19B-token seed-17 comparison with
microbatch 20, accumulation 10, LR $10^{-4}$, weight decay 0.01, and a
token-equivalent 1,920-step warm-up. Both arms initially learned, reached their
best logged loss near step 1,220 while LR was about $6.35\times10^{-5}$, then
reversed together as warm-up approached $10^{-4}$. At step 2,260 both hit the
same three-violation guard; fixed-batch replay rose from about 9.25 NLL at the
1B milestone to about 12.73 at the last complete 1.81B checkpoints, with
embedding and logit scales rising in parallel. This falsifies the earlier
claim that pair-03's 0.629B prefix validated the production stability repair:
that run stopped before peak LR and before the observed failure horizon.
Pair-04 checkpoints are structurally complete but scientifically ineligible
for continuation because exact resume deterministically re-enters the failed
contract. The next production lineage requires a new approved pair ID, step-0
start, and a current-implementation stability gate that runs beyond peak LR;
analogy to the older DeepSpeed trainer is no longer sufficient. The full DCLM
source contains about 302.2B uint32 tokens, and the retired pair used one frozen
symlink view that excludes the held-out shard rather than the 0.075B-token
smoke view.

The 2026-07-27 root audit localizes the harmful checkpoint drift to radial
growth of the tied input/output embedding; aligned old/new logits, loss, and
gradients match, and DDP accumulation plus fused AdamW parity pass. The
maintained default now restores the inspectable old Router reference,
non-renormalized top-2 weights, and zero load-auxiliary coefficient while still
logging load metrics. A one-H100 multiplier-0.25 continuation controlled
embedding scale but did not beat or reproduce failure in its multiplier-1.0
control, so no embedding multiplier or production configuration is approved.

Creating the scaffold does not promote the method claim, edit the active graph,
or replace the A06 decision after the frozen CrossCodeEval headroom failure.
Better balance, route separation, or route continuity remains insufficient;
functional promotion requires an approved training-time held-out utility
protocol.

## Implementation Project — De-common Router Evaluation

| Role | Path / value |
|---|---|
| Theme | reproducible base-model downstream evaluation for de-common Router checkpoints |
| Project | `Projects/decommon-router-evaluation/` |
| Primary metric / suite | paired held-out NLL; five-shot LAMBADA, HellaSwag, PIQA, ARC-Easy, OpenBookQA, SciQ as external validation |
| Compatibility suite | union of historical MultiHeadMoE and SD-MoE tasks |
| State | evaluator scaffold, fixed suites, 30B schedule, and replicated-DDP full-pipeline smoke complete; no research-eligible trained-checkpoint result exists |

The evaluator pins `lm-eval==0.4.12` and `transformers==4.53.3`, reads complete
replicated DDP milestones without copying them, and records checkpoint,
tokenizer, task, shot, seed, and package provenance. Every 1B milestone gets a
fixed cheap trajectory evaluation; every 5B milestone gets the full primary
and group-compatibility suites; the final 30B milestone gets hard diagnostics.
MMLU and other near-floor tasks are excluded from primary sub-billion model
selection. BoolQ remains only a standard/compatibility member: the 26M-token
acceptance scored 0.620795 against a 0.621713 majority-label baseline and
effectively predicted the majority label. Exact OLMES, corrected DCLM CORE v2,
and PALOMA are selected final broad checks but still require validated
custom-checkpoint adapters. EP-to-single-process consolidation remains
unimplemented and must not be approximated by loading one expert shard.
The limited two-example LAMBADA/PIQA acceptance suite loaded the final local
DDP milestone and produced versioned results, but is explicitly ineligible for
model selection or capability claims.

## Reading Order

```text
AGENTS.md
-> PROJECTS.md
-> relevant daily_research_reports/MMDD/focus_<problem>.md (when present)
-> expert_specialization.graph.yaml
-> linked project-local anchor / story / summary / detailed record
```

Do not scan whole project repositories by default. Project-local artifacts are
the source of truth; the graph is navigation and root sync is the published
reading surface.

## Research Map

| Line | Question | State | Current source |
|---|---|---|---|
| A05 | Why can ordinary top-1 routing collapse under apparently uniform features? | Failure mechanisms established under controlled and real-text audits. | `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/research_map.md` |
| A06 | Can route-relevant structure be discovered, preserved, and converted into expert utility? | Primary line; controlled utility chain complete; first registered CrossCodeEval final-layer headroom clause failed; training-time selective-sharing decision active. | `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md` |
| A07 | Does functional separation reduce common/rare interference? | Supporting controlled evidence; parked until A06 establishes stable positive expert utility on a registered real workload. | `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/` |
| A11 | What direct training signal does an informative future target add, and does the standard head causally use it? | Exact K/V is branch-readable under all objectives; no registered MTP-specific readability or stable strong-use increment is established, while 5/5 nuisance compaction remains secondary. Relay-required continuation moved to A13. | `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md` |
| A12 | Does that earlier signal become useful for structured composition? | Supporting line; E04 Stage A completed but failed the NTP capability and row-removal validity gates. No threshold or MTP run is authorized. | `Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md` |
| A13 | Which task properties convert earlier task-relevant supervision into ordinary-head utility? | The hard-relay sufficient condition remains established. Soft-relay Stage 0 produced ordered causal path use but no common non-saturated comparison window, so the objective comparison is blocked pending a measurement-only carrier repair decision. | `Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/README.md` |
| A14 | Can a globally high-capacity hierarchy support conditionally low-dimensional computation? | The controlled conditional-functional-rank theorem is retained, while global shared-linear propagation remains closed. E01 established that duplicate exposure is not context diversity and that capability-passing lookup `K=1/4/16` controls used 10.2/11.0/12.8 functional ROOT directions; archived E02-v1 matched seen-pair capability but failed strong unseen-pair recombination in 5/5. Improved E02 now isolates exact frequency inside one learned common mapping: all 10 pairs passed strict zero-exposure capability and rank-validity gates, LowF-minus-HighF functional rank averaged 0.2 directions, and its one-sided 95% upper bound was 0.5 against a frozen two-direction margin. This supports frequency non-inferiority in the registered task, not a shared-versus-independent mapping advantage. E03 was parked before treatment because a 32-probe common AdamW step basis captured only 0.478--0.631 of held-out common-update energy, so raw parameter-space reuse remains unidentified. E04--E06 retain the local-versus-finite bridge result: exact optimizer/ROOT secants were effectively eight-dimensional, while single-point H11 was refuted in 5/5. A14_03 remains blocked and Router utility remains unverified. | `Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/README.md` |
| A15 | How do spectral coordinates arise, what information do different representation regions carry, and when can a coordinate be admitted into functional routing? | A15.13 E06 full execution is complete. With Router prediction and probability scaling removed, hard gold-intent grouping improved held-out CLINC150 intent loss over balanced-random and common-child controls in both seeds and passed both child-function interventions. Typed verdict is `PASS_SEMANTIC_FUNCTIONAL_VALUE`; this is an Oracle post-training value result, not learned routing or native-representation evidence. Human wording and the learned-Router next decision remain pending. | Current Focus: `daily_research_reports/0901/focus_semantic_gradient_functional_alignment.md`; E06 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/summary.md`; E06 Protocol, Detailed, and Anchor are linked there. |
| A16 | Can expert load remain operationally controlled while the Router exposes functionally useful same-layer incremental information? | The DC audit establishes an immediate sustainer of frozen Vanilla collapse, while the completed shadow audit bounds Centered relief to an early counterfactual and rejects a global harmful-LB mechanism. The NLL-only increment branch did not show a replicated 20B advantage. The active decision is the approved A16_01_01 two-seed frozen expert-choice-regret gate comparing Conditional-Utility with Native, Raw-Utility, and Conditional-Haar; 30B continuations remain fail-closed unless that gate passes. | `Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/README.md` |
| Long-context functional retrieval (draft) | What should a long-context Router optimize so that retrieved evidence changes the standard prediction? | Cross-line group-meeting theme only; Q0 is closed by R3/R4, while the proposed Q1 loss-utility audit still requires human judgment and an approved Protocol. | `daily_research_reports/backup/2026/07/0716/docs/long_context_functional_retrieval_working_theme.md` |

Primary route:

```text
A05 failure
-> A06 geometry and state discovery
-> A06 finite-margin preservation
-> A06 expert utility and partial-feedback correction
-> A06 registered frozen real-code headroom clause fails
-> A06 training-time selective-sharing decision
-> A07 functional interference value only if stable positive utility is established
```

Supporting objective route:

```text
A11 informative-future signal boundary
-> A12 structured composition and standard-head use
-> A13 task-property decomposition and necessary-relay utility
```

Independent representation-structure route:

```text
A14 conditional low-rank theorem
-> held-out constituent subspace geometry
-> pretrained/random architecture separation
-> paired hierarchy-order intervention
-> same-parent alternative-split and stability frontier
-> within-parent two-sided direction balance
-> global shared-linear propagation claim closed
-> probabilistic sparse-activation theorem
-> A14_01 parameter-to-state bridge with bounded standalone reconstruction
-> A14_02 E01 rank comparison insufficient; E02 capability revision failed
-> A14_02 E04 local H9 supported
-> A14_02 E05/E06 point-to-finite H11 refuted; finite secant bridge adopted
-> only if a composition-capable shared surface exists, revisit reuse-caused rank reduction
-> only after that, A14_03 state-to-parameter functional-rank demand
```

Independent spectral-routing diagnostic route:

```text
actual Router-input spectral access
-> controlled covariance learning-speed causality
-> real-trajectory load-stability boundary
-> fixed-band compatibility and matched-training Fail
-> layer-specific information identity and natural hierarchy audit
-> balanced actual-input fine-specific local-rank Fail
-> shared broad-tail relocation Fail
-> fixed covariance-band functional admission and matched dispatch Fail
-> two parameter-only common bases disagree on depth shift (`basis_sensitive_shift`)
-> fixed Mean Response basis gives coarse < medium < fine, but same-layer shapes overlap and do not identify one continuous semantic band
-> all 35 adjacent-layer variance redistributions are non-monotonic, so normalized Attention-write variance is closed as a definition of added information
-> A15_03 band audit archived and removed from the active route
-> A15_08 exact transition difference plus conditional held-out accessibility
-> E03 INELIGIBLE_GUARD; E04 eligible local H2 Pass and registered rank-two H1' Fail at 33.24% retention
-> researcher parks the layer-25 task-readout rank ladder
-> A15_08_01 E01 stops at structural-null block-1 standardization
-> E02 blocks 2--36 completes on Reserved 4xH100: positive depth interaction but negative absolute 2F depth change, typed Fail
-> E03/E04 expose the next meeting uncertainty: supervised directions with low observed PCA-head overlap look compact, while local geometry is reproducible, but fresh-expression stability, PCA-head non-enrichment, and shared-specific identity remain unproved
-> researcher reactivates A15_07 with $R_U$ at blocks 24/28 and requires a new sealed expression bank
-> current: review A15_07_E01; no implementation, confirmation opening, or Router work is authorized
```

Draft cross-line meeting route:

```text
nominal context capacity
-> evidence access
-> state formation and transport
-> standard-head causal use
-> ordered composition
-> query-conditioned retrieval utility
-> held-out expert utility per unit cost
```

Incubating diffusion-language-model route:

```text
D00 comparison contract
-> D01 matched training-objective and data-repeat audit
-> D02 fixed-denoiser unmasking-path audit
-> D03 dense versus static/adaptive MoE audit
```

The current literature boundary is that pure masked diffusion remains weak on
compute-normalized training and exact dependency-sensitive generation, while
blockwise and AR--diffusion hybrids substantially improve the practical
frontier. MoE improves active capacity and can improve routing/system
efficiency, but no audited result establishes that it removes the denoising
quality--parallelism trade-off. Source:
`Projects/diffusion-language-models/README.md`.

The proposed 2026-07-17 meeting theme is:

> From Retrieval Hits to Functional Utility: What Should a Long-Context Router
> Optimize?

This route does not replace the A06 primary line or turn long context into a
mechanism claim. It connects the R3/R4 retrieval failure, A11 formation/use
boundary, A12 carrier failure, and A06 utility gate around one missing object:
held-out downstream loss preservation under a fixed selection budget.

Q0 is already closed in the controlled setting: perfect feature specialization
is not sufficient for a useful sparse KV index. Q1 is only a proposal: test
whether retrieval proxies rank causal loss utility on existing checkpoints.
The researcher must complete the mechanism, rival, uncertainty,
judgment-changing evidence, and next-decision fields before a formal anchor or
Protocol is created.

Sources:

- `daily_research_reports/backup/2026/07/0716/docs/long_context_functional_retrieval_working_theme.md`
- `daily_research_reports/backup/2026/07/0716/docs/long_context_functional_retrieval_working_theme_cn.md`
- `Projects/from-attention-to-search/main/experiments/archive/R3_perfect_router_retrieval/summary.md`
- `Projects/from-attention-to-search/main/experiments/archive/R4_attention_output_router_retrieval/summary.md`

## A06 Decision Chain

| Parent | Decision | Verdict |
|---|---|---|
| `06_00` | What counts as functional specialization? | Requires conditional expert utility and route-function binding; load balance or route NMI alone is insufficient. |
| `06_01` | Is a route-relevant state reachable and usable for initialization? | Yes under controlled conditions; real-DCLM proxy centers are linearly routable at step 0 but ordinary training overwrites them. |
| `06_02` | What preserves a partition during training? | Finite low-tail margin is the local state; dynamics depend on utility, signed background pressure, representation motion, router motion, and update scale. |
| `06_03` | Can sparse feedback discover the useful expert? | Selected-only feedback can be blind; one bounded challenger plus a lower-tail certificate repairs discovery in the frozen four-expert setting. |
| `06_04` | Does a real workload contain stable expert-utility headroom worth routing? | Active parent; the first registered CrossCodeEval final-layer clause failed split stability and positive absolute headroom. |

Current A06 result:

> Relevant cross-file context changes final-layer expert counterfactual effects,
> but the calibration-selected expert is not split stable and its absolute
> headroom over native routing is below the registered threshold.

The direct held-out values are $I_{ctx}=0.01163$ nats per target token, 95% CI
`[0.00336, 0.02022]`, and $H_{49}^{REL}=0.00540$, 95% CI
`[-0.00105, 0.01225]`. Interaction passed, but expert identity stability and
positive absolute headroom failed. This is a valid negative result for the
registered frozen last-layer surface, not a conclusion for every repository-
code workload or layer.

Active A06 question:

> After this frozen-pool failure, should A06 approve one training-time
> selective-sharing test on an explicit real rare/common workload?

If approved, positive held-out expert utility, split-stable identity,
rare/common controls, and matched activated compute must be registered before
implementation. Lower switch rate or context interaction alone is insufficient.

Current sources:

- `Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing.md`
- `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md`
- `Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/anchor_threads/06_04/story_fragment.md`
- `Projects/from-attention-to-search/main/experiments/A06/README.md`

## A11 / A12 / A13 Supporting Boundary

A11 establishes an earlier direct first-order signal from informative future
targets, conditional hidden-to-parameter reachability, and a cross-position
sufficiency failure. It does not establish long-range composition, neural
scale effects, real-workload transfer, or MoE value.

A11's revised stronger audit is complete. It compared model-local `U03` source
K/V causal control under standard-CE informative-MTP and a shared-aux condition
matched for active heads, CE terms, nominal loss coefficients, and standard-head
capability, with NTP as a secondary system baseline. All registered guards
passed, but the strong behavioral information-content increment failed:
$\bar\Gamma_{info}=0.01675$ and `0/5` seeds reached `0.10`.

The source-information follow-up reproduced those states and found exact K/V
branch accuracy `1.0` under every condition and seed. It did not identify an
informative-MTP-specific readability increment: mean
$\Gamma_{\mathrm{read}}=-0.002299$ nat/example and 4/5 seeds nonpositive. The
formal verdict was insufficient because the single-shuffle guard failed.
Informative-MTP reduced within-branch nuisance dispersion in 5/5 seeds, but
that Fisher pattern is secondary geometry rather than use evidence.

Exactly one A11 decision:

> Validate a learnable `relay-required` carrier with no direct answer bypass
> and a non-saturated shared-aux baseline before another objective comparison.

A12 currently establishes:

- a valid depth-two joint-evidence workload;
- an exactly learnable in-support short-range fixed-rule surface for both NTP
  and MTP at 1, 2, and 4 layers;
- a positive NTP-versus-MTP interaction only under the exact-accuracy threshold
  `1.0` on that memorization-prone fixed-table surface;
- an E03 rejection because one-step and two-step tasks had asymmetric
  query-relevant structure;
- a completed E04 NTP-only Stage A in which no 2- or 4-layer scale stably
  learned both task depths, no threshold was frozen, and the proposed
  row-removal necessity guard failed because bijection completion recovers the
  missing value;
- failed or unstable unseen-composition surfaces;
- a controlled linear missing-rank mechanism that is not a neural scale law.

A12 does not establish neural causal use, general MTP superiority, unseen-pair
composition, curriculum benefit in a capacity-sufficient regime, real-workload
transfer, or MoE value.

Exactly one A12 decision:

> Decide whether to close E04 under its frozen 2/4-layer, 20,000-step contract
> or reopen carrier/capability design in a new Protocol. Stage B and every MTP
> run remain blocked until a structurally valid carrier has at least one
> NTP-eligible scale and a frozen threshold.

A13 resolves the relay-required carrier gate on a smaller controlled surface.
After closing a query-conditioned carrier as unstable, it validated a
single-value NTP relay and changed one auxiliary label at a time. The decisive
answer-$A$ versus nuisance-$B$ relay-target comparison found
$R_{\mathrm{relay}}=0.2315$ nats,
$R_{\mathrm{bypass}}=0.0181$ nats, and a
$0.2134$-nat interaction with 95% interval
`[0.1646, 0.2585]`; all eight paired seeds had the expected relay and
interaction signs. Every objective/path cell reached final accuracy `1.0` and
every relay donor-use audit scored `1.0`.

A13 establishes only a synthetic finite-budget sufficient condition:
task-relevant earlier supervision helps when the supervised state is on the
only answer path and is consumed by the ordinary head. It does not establish
distance, composition, code/text transfer, long-context scaling, planning, or
MoE utility.

The frozen soft-relay Stage-0 audit then varied only the two-layer
`ANSWER -> A` attention-logit penalty across `0`, `2`, `4`, and hard mask.
All four NTP-only carriers reached final accuracy `1.0`, and the measured
direct-path effect decreased while the relay effect and relay-reliance ratio
increased at every level. However, the unpenalized condition reached at least
`0.90` accuracy at the first positive checkpoint (`20` steps) in `8/8` seeds,
so there was no common measured non-saturated window. Under the frozen stop
rule, Stage 1 was not run; no soft-relay MTP-specific utility trend is
identified.

Exactly one A13 decision:

> Decide whether to approve a measurement-only Stage-0 repair that records
> every optimization step through step `40`, while preserving the data,
> model, objectives, penalties, seeds, optimizer updates, and budgets.

Current sources:

- `Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md`
- `Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md`
- `Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md`
- `Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/detailed.md`
- `Projects/from-attention-to-search/main/stories/13_mtp_task_property_decomposition/01_task_relevant_relay_supervision.md`
- `Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md`
- `Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_06_E01_soft_relay_mtp_ntp_audit/summary.md`

## Claim Boundary

Supported:

- Route-relevant hidden geometry can initialize a controlled partition.
- Real-DCLM proxy centers are routable at step 0 and can be overwritten by
  ordinary training.
- Expert utility, signed background pressure, and representation-router-
  optimizer co-dynamics jointly determine local margin preservation.
- Correct conditional exposure creates held-out specialist utility in the
  controlled system.
- Selected-only top-1 feedback can miss an unselected specialist; a rotating
  challenger and lower-tail certificate repair this in a frozen four-expert
  system.
- On the registered CrossCodeEval final-layer surface, relevant context changes
  expert counterfactual effects, but context interaction alone does not imply
  stable positive expert utility.

Not supported:

- route NMI or balanced load proves functional specialization;
- the current proxy is a semantic or causal expert definition;
- the controlled Router transfers to joint pretrained-LLM training;
- unfiltered repository code has positive held-out oracle routing headroom;
- the four-expert phase switch scales or reduces wall-clock cost;
- MTP has general compositional or real-workload superiority;
- the A13 synthetic sufficient condition transfers to code, long context, or MoE;
- a nominal million-token context is functionally usable;
- feature specialization alone provides a useful long-context retrieval index.

Controlled synthetic evidence establishes mechanism possibility and metric
validity, not natural-language semantics or deployable routing. Real-DCLM proxy
evidence establishes routability and overwrite behavior, not causal expert
utility. The CrossCodeEval result is a registered local failure and must not be
generalized to every layer, model, or repository-code distribution.

## Exactly One Project-Level Next Decision

Confirm, correct, or block the cold-read-revised four-part Focus and the
A15_07_E01 Protocol choices for the current meeting-cycle core task. In
particular, decide the sealed-v4 construction,
the frozen E03 standardization, one-rank/no-C4-scan rule, PCA-head non-enrichment
gate, denominator guard that finalizes admission, and shared/specific null definitions.
This decision does not authorize a run.

The earlier A06 training-time selective-sharing decision and A16 expert-regret
gate retain their evidence state but are parked for this cycle; they do not
replace the active Focus.

## Current Working And Published Surfaces

- `daily_research_reports/MMDD/focus_<problem>.md`: the one living meeting-cycle
  task, from confirmed plain-language design through the researcher's result
  account; it is not canonical result evidence.
- `daily_research_reports/MMDD/docs/daily_report_<topic>.md`: delayed self-
  contained story written only after canonical evidence and the human result.
- `daily_research_reports/MMDD/focus_meeting_<topic>.md`: optional explicitly
  requested meeting brief or human-scoped synthesis; it is not project truth.
- `Projects/from-attention-to-search/main/parking_lot/README.md`: concise key
  non-active questions and reopening conditions.
- `Projects/graphs/expert_specialization.graph.yaml`: thin navigation snapshot;
  its A06 `active` markers are known stale and do not override this registry or
  the active Focus. Updating the graph still requires explicit authorization.
- `sync/S000_current_specialization/README.md`: root-sync entry.
- `sync/S000_current_specialization/anchor_index.md`: complete mirrored-anchor
  index.
- `sync/S000_current_specialization/anchors/`: generated full mirror of current
  project-local anchors with repository-root-safe external links.

Root sync, graph edits, external collaborator sync, handoff packages, commits,
and pushes remain explicit actions. This registry does not authorize them
automatically.

## Other Root Surfaces

- `daily_research_reports/`: dated problem knowledge updates, meeting
  syntheses, and working materials. Legacy bare `focus.md` files may remain.
- `paper_reading/`: reading cards.
- `papers/`: paper-writing workspaces.
- `templates/`: reusable templates.
- `prompts/`: reusable prompts.
- `.agents/skills/`: repository-tracked, natively discovered workflows.

`Projects/academic_writing/` is a course-delivery wrapper using current
research as source material. It does not own research state.
