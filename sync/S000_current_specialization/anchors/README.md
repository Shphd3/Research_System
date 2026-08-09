# Problem Anchors

This folder stores the project-local source-of-truth anchors for
`from-attention-to-search`.

Canonical anchors are grouped by research line:

```text
Projects/from-attention-to-search/main/problem_anchors/00_foundation_definition/
Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/
Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/
Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/
Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/
Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/
Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/
Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/
Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/
Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/
```

Do not create a generic nested `anchors/` subfolder inside this project-local
source tree. Each folder above is a research-line folder. Root `sync/S000_*`
may copy these anchors into its own `anchors/` mirror when explicitly synced,
but the project-local files remain the source of truth.

Do not create closure or hypothesis-card trees. Hypotheses belong in anchors,
and line-level synthesis belongs in `main/stories/<line>/`.

Current classification maps:

```text
00_foundation_definition/README.md
05_failure_mechanism/research_map.md
06_geometry_proxy_preservation/research_map.md
09_common_rare_spectral_discrimination/README.md
13_mtp_task_property_decomposition/README.md
14_tree_low_rank_language_structure/README.md
```

## Canonical Parent-Anchor Folder Rule

Active multi-parent research lines use this structure:

```text
<line_id>/
  README.md
  <parent_id>_<topic>/
    <parent_id>_<topic>_anchor.md
    <parent_id>_<topic>_anchor_cn.md
    <parent_id>_<topic>_thinking_card.md
    <parent_id>_<topic>_thinking_card_cn.md
    subanchors/
      <parent_id>_<NN>_<topic>_anchor.md
      <parent_id>_<NN>_<topic>_anchor_cn.md
      <parent_id>_<NN>_<topic>_thinking_card.md
      <parent_id>_<NN>_<topic>_thinking_card_cn.md
```

Each numbered major decision is a sibling parent folder, even when the line
README orders it after or makes it depend on another parent. `subanchors/` is
reserved for a child that inherits one parent's decision question and tests a
local clause, rival, repair, robustness check, or metric guard. A dependency
arrow does not establish parent--child ownership.

Keep the parent anchor and its Thinking Card together; keep a child anchor and
its Thinking Card together under `subanchors/`. The line README owns reading
order and dependency order. Structural migrations move the only canonical
copy, update all active references and indexes, remove the old path, and end
with zero duplicate canonical files and zero broken local links.

## Active Research Shape

Current mainline:

```text
definition / failure mechanism
-> route-relevant state and proxy discovery
-> initialization and finite-margin preservation
-> expert utility formation
-> partial-feedback discovery and phase control
-> registered real-code frozen-pool headroom audit
-> training-time utility-creation decision before Router transfer
```

Current strongest judgment:

```text
The A06 controlled chain is now coherent from geometry to function. Route-
relevant states can initialize a partition, but real proxy routing is rapidly
overwritten by ordinary training. Finite low-tail margin is the local
preservation buffer; its motion depends on utility, signed background pressure,
representation, router, and optimizer-transmitted step scale. Correct exposure
creates held-out specialist utility, while selected-only weighted top-1 can
preserve a correct specialist but fail to discover it from a wrong rank. One
rotating challenger plus a q10 or lower-CVaR10 utility certificate repairs that
controlled failure and safely returns to top-1 under frozen four-expert
assumptions. On the first registered CrossCodeEval final-layer surface,
relevant context changes expert counterfactual effects, but expert identity is
not split stable and positive absolute headroom fails. The only next decision
is whether to approve one training-time selective-sharing test on an explicit
real rare/common workload.
```

## Anchor Groups

| Group | Anchors | Role | Current status |
|---|---|---|---|
| 00 foundation / definition | `00_foundation_definition/README.md` | Redirects the historical definition layer into consolidated `A06_00`. | No independent active anchor. |
| 01 common-operator mechanism line | `01_common_operator_mechanism/README.md`, `01_common_operator_mechanism/README_cn.md`, `01_common_operator_mechanism/route_document.md` | Plan and audit the mechanism-first line for defining, identifying, and validating a common operator before method construction. | Stage 1 supports criterion-dependent common (`criterion_winner_diversity=4`); Stage 2 supports gradient common over activation common (`n_passed_mismatch_regimes=4/4`); Stage 3 controlled bridge supports feedback replay/removal (`n_passed_main_feedback_regimes=2/2`). The bounded real-DCLM gate-logit bridge reproduces collapse but rejects simple low-rank logit common as the main explanation (`pass=false`). |
| 05 failure-mechanism line | `05_failure_mechanism/02_*`, `05_failure_mechanism/05_01_*` to `05_failure_mechanism/05_04_03_*` | Diagnose why ordinary top-1 fails: early top-1 lock-in, inhibition limits, feature-axis ambiguity, common offset, and common-logit feedback. | Mechanism evidence. It supplies the physical priors used by 06. |
| 06 functional Routing line | `06_geometry_proxy_preservation/research_map.md`; parent anchors `06_00` to `06_04` with local `subanchors/` | Five decisions from functional definition through geometry, preservation, expert utility, sparse discovery, and a real-workload gate. | Four completed parents; active `06_04` contains one completed failed CrossCodeEval subanchor; no LLM Router claim. |
| 07 interference / value line | `07_features_overlap/07.md`, `07_features_overlap/07_01_*` to `07_features_overlap/07_06_*` | Tests whether parameter separation reduces common/rare feature interference or creates utility. | Controlled diagnostics; hierarchy/utility evidence is absorbed into A06. |
| 09 common/rare spectral-discrimination line | `09_common_rare_spectral_discrimination/04_*`, `09_common_rare_spectral_discrimination/09_*` | Tests frequency / high-gain common-band explanations for rare discrimination failure. | Mechanism side line. It can inform A06/A07 but does not by itself prove a routing method. |
| 10 optimizer learning-rate mechanism line | `10_optimizer_learning_rate_mechanism/10_*` | Seminar-driven optimizer root-cause line: test whether common / high-gain gradient directions constrain SGD-style critical learning rate before comparing Adam, Nesterov, or other optimizers. | Support line. It does not update the MoE preservation claim unless later bridged back through routing margin evidence. |
| 11 informative-future branch mechanism | parent-anchor registry: `11_informative_future_branch_mechanism/README.md`; three complete parents `11_01`--`11_03`; story: `../stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md` | Isolates the objective-level NTP/MTP difference on a short matched branch: informative-future signal, parameter reachability, and the cross-position use boundary. | Stable bounded baseline. No active run; structured workload claims are excluded. |
| 12 structured compositional MTP workload | parent-anchor registry: `12_structured_compositional_mtp_workload/README.md`; three complete parents `12_01`--`12_03`; story: `../stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md` | Tests whether the A11 signal becomes functional on a computation-tree workload, starting from a depth-two ordered-composition base case. | Workload valid; current from-scratch learner gate failed; linear rank mechanism supported; active design is a shared capability gate followed by intermediate-state causal use. |
| 13 MTP task-property decomposition | parent-anchor registry: `13_mtp_task_property_decomposition/README.md`; parent `13_00` with local `subanchors/` | Tests which workload properties convert earlier task-relevant supervision into ordinary-head utility. | Hard-relay sufficiency retained; soft-relay objective comparison remains blocked pending a measurement-only carrier repair decision. |
| 14 conditional low-rank hierarchy | parent-anchor registry: `14_tree_low_rank_language_structure/README.md`; sibling parents `14_00`--`14_03`; only `14_02` currently owns local `subanchors/`; current synthesis: `../stories/14_tree_low_rank_language_structure/03_ntp_conditional_function_rank.md` | Separates global capacity from input-conditioned functional rank and audits the parameter-to-ROOT bridge. | Conditional theorem retained; point Jacobian is local only; finite training uses the low-dimensional secant/path-integrated image. Reuse-caused rank reduction remains open because unseen composition failed. |
| 15 spectral representation geometry and functional routing | parent-anchor registry: `15_spectral_representation_and_functional_routing/README.md`; sibling parents `15_00`--`15_06`; current synthesis: `../stories/15_spectral_representation_and_functional_routing/02_spectral_representation_to_functional_routing.md` | Separates Router-input geometry, learning/feedback dynamics, representation atlases, independent middle/tail information audits, functional coordinate admission, and online routing. | No universal semantic rank coordinate or middle/tail functional gain is established; `A15_04` is the active geometry review and `A15_03` remains an independent draft. |
| 16 load-control gradient interference | parent-anchor registry: `16_load_control_gradient_interference/README.md`; parent `16_00` with local subanchor `16_00_01` | Tests whether differentiable load control improves hard load while worsening next-step held-out language learning. | Frozen DC sustainer boundary complete; global-batch LM/LB gradient and shadow-step audit is the active mechanism decision. |

## Historical Placement

Earlier definition, hierarchy, geometry, and real-proxy anchors have been
absorbed into A06 parent/subanchor folders. Current documents use the new
identifiers; immutable remote jobs remain in artifact maps and Git history is
the source for the pre-consolidation file layout.

## Experiment Folder Rule

Experiment folders inherit the full parent/subanchor identity:

```text
../experiments/A06/<parent_id>_<topic>/<parent_id>_<subanchor_id>_E<run>_<topic>/
```

A parent anchor tells the complete major decision story. Small repairs,
controls, rival-explanation tests, and method audits belong to its
`subanchors/` directory and the matching grouped experiment directory. They do
not receive a new line-level parent number. Renumber the directory and all
active references when ownership changes; Git history preserves the previous
layout.

## Next Decision

Decide `A06_04` before any new protocol:

```text
After the registered CrossCodeEval final-layer frozen pool failed split
stability and positive absolute headroom, should A06 approve one training-time
selective-sharing test on an explicit real rare/common workload?
```

If approved, the future protocol must require positive held-out expert utility,
split-stable useful-expert identity, rare/common conditional controls, matched
activated compute, and no utility prefiltering. Lower switching or a positive
interaction alone is insufficient.
