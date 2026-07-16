# Projects

Current-state registry for `Research_System`. Read after `AGENTS.md`, then read
`CURRENT.md` for today's work.

## Active Project

| Role | Path / value |
|---|---|
| Theme | feature-level expert specialization in top-1 MoE gating |
| Project | `Projects/from-attention-to-search/` |
| Worker surface | `Projects/from-attention-to-search/XingyuD/` |
| Active branch | `Xingyu` |
| Read-only reference | `Projects/kv_cache/` |
| Graph | `Projects/graphs/expert_specialization.graph.yaml` |
| Root sync | `sync/S000_current_specialization/` |

`Projects/kv_cache` is read-only unless the user explicitly authorizes edits.
Only its `xyDeng` branch is managed here; never push its `main` branch.

## Reading Order

```text
AGENTS.md
-> PROJECTS.md
-> CURRENT.md
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
| A06 | Can route-relevant structure be discovered, preserved, and converted into expert utility? | Primary line; controlled utility chain complete, real-workload headroom gate active. | `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md` |
| A07 | Does functional separation reduce common/rare interference? | Supporting controlled evidence; parked until A06 passes the real-workload gate. | `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/` |
| A11 | What direct training signal does an informative future target add, and does the standard head causally use it? | Exact K/V is branch-readable under all objectives; no registered MTP-specific readability or stable strong-use increment is established, while 5/5 nuisance compaction remains secondary. Relay-required carrier gate active. | `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md` |
| A12 | Does that earlier signal become useful for structured composition? | Supporting line; E04 Stage A completed but failed the NTP capability and row-removal validity gates. No threshold or MTP run is authorized. | `Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md` |
| Long-context functional retrieval (draft) | What should a long-context Router optimize so that retrieved evidence changes the standard prediction? | Cross-line group-meeting theme only; Q0 is closed by R3/R4, while the proposed Q1 loss-utility audit still requires human judgment and an approved Protocol. | `daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme.md` |

Primary route:

```text
A05 failure
-> A06 geometry and state discovery
-> A06 finite-margin preservation
-> A06 expert utility and partial-feedback correction
-> A06 real-workload oracle-headroom gate
-> A07 functional interference value only if the gate passes
```

Supporting objective route:

```text
A11 informative-future signal boundary
-> A12 structured composition and standard-head use
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

- `daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme.md`
- `daily_research_reports/0716/docs/long_context_functional_retrieval_working_theme_cn.md`
- `Projects/from-attention-to-search/main/experiments/archive/R3_perfect_router_retrieval/summary.md`
- `Projects/from-attention-to-search/main/experiments/archive/R4_attention_output_router_retrieval/summary.md`

## A06 Decision Chain

| Parent | Decision | Verdict |
|---|---|---|
| `06_00` | What counts as functional specialization? | Requires conditional expert utility and route-function binding; load balance or route NMI alone is insufficient. |
| `06_01` | Is a route-relevant state reachable and usable for initialization? | Yes under controlled conditions; real-DCLM proxy centers are linearly routable at step 0 but ordinary training overwrites them. |
| `06_02` | What preserves a partition during training? | Finite low-tail margin is the local state; dynamics depend on utility, signed background pressure, representation motion, router motion, and update scale. |
| `06_03` | Can sparse feedback discover the useful expert? | Selected-only feedback can be blind; one bounded challenger plus a lower-tail certificate repairs discovery in the frozen four-expert setting. |
| `06_04` | Does a real workload contain stable expert-utility headroom worth routing? | Active, unresolved. |

Active A06 question:

> Does unfiltered repository-level code completion contain positive,
> cross-split-stable held-out oracle routing headroom after token-identity,
> local-only, load-matched, length, frequency, and split-overfitting controls?

Primary metric: held-out native-Router loss minus calibration-selected
forced-expert loss on a separate test split. This measures oracle routing
headroom; it does not establish that a learned Router can capture that headroom.

Required guards: calibration/test separation, stable best-expert identity,
load-matched random routing, token-identity and local-only controls, length and
frequency controls, and an unfiltered repository-code sample.

Current sources:

- `Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing.md`
- `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A06/README.md`

## A11 / A12 Supporting Boundary

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

Not supported:

- route NMI or balanced load proves functional specialization;
- the current proxy is a semantic or causal expert definition;
- the controlled Router transfers to joint pretrained-LLM training;
- repository code has positive held-out oracle routing headroom;
- the four-expert phase switch scales or reduces wall-clock cost;
- MTP has general compositional or real-workload superiority;
- a nominal million-token context is functionally usable;
- feature specialization alone provides a useful long-context retrieval index.

Controlled synthetic evidence establishes mechanism possibility and metric
validity, not natural-language semantics or deployable routing. Real-DCLM proxy
evidence establishes routability and overwrite behavior, not causal expert
utility.

## Exactly One Project-Level Next Decision

Approve or reject the minimal `A06_04` oracle-headroom protocol before
designing another LLM-scale Router method. Do not run another broad
feature-existence, common-subtraction, spectral-Router, or controlled
sparse-discovery sweep first.

For the 2026-07-17 group meeting, a separate time-bounded discussion gate is to
approve, modify, or reject the proposed Q1 functional-retrieval audit. This
draft gate does not replace the project-level A06 decision unless the
researcher explicitly promotes it after completing the human judgment fields.

## Published Surfaces

- `CURRENT.md`: today's focus, progress, and resume action.
- `Projects/graphs/expert_specialization.graph.yaml`: current thin navigation
  graph.
- `sync/S000_current_specialization/README.md`: root-sync entry.
- `sync/S000_current_specialization/anchor_index.md`: complete mirrored-anchor
  index.
- `sync/S000_current_specialization/anchors/`: generated full mirror of current
  project-local anchors with repository-root-safe external links.

Root sync, graph edits, external collaborator sync, handoff packages, commits,
and pushes remain explicit actions. This registry does not authorize them
automatically.

## Other Root Surfaces

- `daily_research_reports/`: daily cards and meeting materials.
- `paper_reading/`: reading cards.
- `papers/`: paper-writing workspaces.
- `templates/`: reusable templates.
- `prompts/`: reusable prompts.
- `skills/`: repository-tracked workflows.

`Projects/academic_writing/` is a course-delivery wrapper using current
research as source material. It does not own research state.
