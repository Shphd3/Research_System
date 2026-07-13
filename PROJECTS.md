# Projects

This file is the current project-state registry for `Research_System`.
Read it after `AGENTS.md`.

`AGENTS.md` defines general operating rules. This file defines the active
research line, active branch, current evidence boundary, and next decision.

## Reading Rule

For project-specific work:

1. Identify the active project here.
2. Read the relevant graph under `Projects/graphs/`.
3. Read only the linked project-local anchor, experiment `summary.md`,
   `detailed.md`, sync note, meeting note, or paper note needed for the
   current question.

Do not scan whole project repositories by default.

## Active Research Line

Primary research theme:

```text
feature-level expert specialization in top-1 MoE gating
```

Current working project:

```text
Projects/from-attention-to-search/
Projects/from-attention-to-search/XingyuD/
```

Reference project:

```text
Projects/kv_cache/
Projects/kv_cache/main_specialization/specialization_overview.md
```

`Projects/kv_cache` is read-only unless the user explicitly asks to edit it.
Only the `xyDeng` branch is under our management; do not push `main`.

Current graph hub:

```text
Projects/graphs/expert_specialization.graph.yaml
Projects/graphs/kv_cache_retrieval.graph.yaml
Projects/graphs/specialization_papers.graph.yaml
```

For graph display, use Sidecar with workspace root:

```text
/data/250010109/Research_System
```

## Research Vision And Adjudication Ladder

The whole specialization project should be read as a staged adjudication
ladder, not as a single method claim. Each level answers one narrower
question and earns only the claim that its metric can support.

| Level | Decision question | Primary metric | Cannot claim |
|---|---|---|---|
| 0. Failure | Why ordinary top-1 routing collapses or merges under apparently uniform features. | step-0 NMI, max load, common margin | A working method. |
| 1. Proxy discovery | Whether a route-relevant proxy exists. | cluster stability, proxy NMI, nuisance guards | Semantic experts. |
| 2. Initialization | Whether the proxy can be converted into gate rows. | step-0 `proxy_route_NMI`, load | Training success. |
| 3. Preservation | Whether the partition survives early training. | `proxy_route_NMI@step5/10` plus LM loss | Expert utility. |
| 4. Utility | Whether a preserved partition reduces interference or has causal expert value. | rare loss, route-function binding, causal ablation | Specialization from load/NMI alone. |
| 5. Scaling | Whether many experts increase activated capacity. | per-expert effective rank, routing stability, utility per activated FLOP | Scaling from active-expert count alone. |

`NMI` is normalized mutual information, used here as a route-label agreement
metric. It can show alignment or collapse, but it does not prove functional
expert value by itself.

Current position in this ladder:

```text
active bottleneck: 3. Preservation
```

Practical reading:

```text
Level 0 has failure-mechanism evidence.
Level 1 has controlled and real-DCLM proxy evidence, with semantic boundaries.
Level 2 has real-DCLM step-0 proxy-center router evidence.
Level 3 is the current unsolved bottleneck: ordinary training erases the proxy
partition by step 5/10. Controlled evidence now separates three mechanisms:
matched expert utility creates positive local margin pressure; weighted top-1
correction is rank-mediated rather than absent; and systematic
boundary-projected background bias can exhaust the finite margin buffer.
Transfer to trainable hidden states and AdamW remains open.
Level 4 has controlled D07 support only; neural/real-DCLM utility is not yet
supported.
Level 5 is parked until preservation and utility are both better defined.
```

Do not promote a higher-level claim when only a lower-level metric passed.
For example, balanced load or high route NMI can support non-collapse or
alignment, but cannot by itself support utility or scaling.

## Current Question

Current decision question:

```text
Under one-layer Transformer + weighted-top-1 MoE full-sequence LM training,
which causal path is necessary for matched-margin first crossing and later
re-entry: router-only motion, representation-only motion, or their joint
optimizer-conditioned coupling?
```

This question is downstream of A06_31--A06_33 frozen-dynamics evidence and
upstream of any preservation method or stronger A07 utility claim.

## Current Route

The current route is:

```text
05 failure mechanism
-> 06 route-relevant proxy discovery, initialization, and preservation
-> 07 functional interference value after preservation
```

Supporting objective line:

```text
11 long-horizon MTP objective
```

Line stories:

```text
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum_cn.md
```

Role:

```text
This line tests whether multi-token prediction can directly supervise the
current hidden state to retain a long-horizon variable. It is a mechanism
candidate for future route-relevant hidden-state formation, not a replacement
for the MoE gating preservation mainline.
```

Current A11 boundary:

```text
Controlled evidence supports a representation guarantee: if K covers the first
informative future horizon and the covered target is a one-to-one code for the
early variable, low loss at that horizon forces h_T to contain that variable.
A11_05 further supports direct decision-prefix horizon-3 supervision as one
mechanism component for faster and more stable recovery in clean tau=3
all-position training. A11_06 supports the first-order hidden readout-margin
mechanism: K3 has positive G_M_hidden while K1/K2 are near zero in the
no-leakage decision-prefix setup. A11_07 supports direct decision-prefix
horizon-3 supervision as the stronger all-position path: direct conditions
reach native H3=1.0 and large M_Z_ref, while K1/K2/masked K3 can still recover
nontrivial Q through indirect transfer. Therefore Q alone is not direct
supervision evidence. A11_08 supports the general-K vector-sum mechanism:
under the same K=4 and the same two informative horizons, aligned output-row
geometry produces much larger hidden-state semantic velocity than
low/conflicting geometry. A11_08b shows this primary velocity mechanism is not
only a step-0 artifact: with frozen heads, aligned still has much larger early
hidden semantic velocity than low/conflict, although trainable-head curves must
record current output geometry because the heads drift. A11_09 supports the
next-K inclusion law in controlled frozen-head decision-only dynamics: K2 is
zero before the informative horizon, K3 turns on at the first informative
horizon, adding a shared H4 gives no direct one-step semantic increment,
aligned informative H4 amplifies, and low/conflict informative H4 weakens.
Therefore K size alone is not the efficiency object; the covered informative
horizons' centered readout directions are. A11_10 supports the all-position
native/probe split: direct H3 conditions reach native H3=1.0 and large
M_Z_ref, while K2 and masked K3 can keep nontrivial Q but native H3 remains 0
and M_Z_ref stays near zero. Therefore Q alone is not direct-supervision
evidence. A11_10 finite-step audit supports persistent positive early semantic
velocity in direct informative conditions and native H3=1.0 / Q=1.0 in direct
all-position conditions, but its Transformer parameter-space curvature
certificate is often nonpositive or extremely loose. The active A11 story now
separates this failure from hidden-state optimization: it proves the exact
finite-step identity M_K(t+1)-M_K(t)=eta G_K_hidden(t), an explicit K=2
recovery bound under regular-simplex output geometry and semantic-subspace
decoupling, and a conditional stochastic sample-hitting bound. A11_02b has
completed the advisor's K=2 diagnostic design: informative H2 passes native,
probe, swap, and final task-directed-gradient guards; the lambda audit finds a
small dose-dependent local L1 convergence cost but no final next-token accuracy
loss. A11_11 now supports the controlled K=2 parameter-transmission
prerequisite: in the folded-reference decision-only model, direct parameter
semantic velocity is positive in 5/5 seeds, full-K2 net velocity remains
positive in 5/5 seeds, and actual one-step margin movement follows eta times
the tangent-kernel velocity. Its algebraic alpha-scaling laws remain
implementation guards; the empirical support is native magnitude, positive net
sign, and finite-step fidelity. A11_12 now closes the controlled all-position
path decomposition: the earlier decision-position component G_D is positive
and exceeds the later NTP semantic component G_I in 5/5 seeds; remaining
all-position losses are signed, so the full K2 net velocity is positive in 4/5
seeds rather than universally positive. Matched direct/mask trajectories favor
the direct path in 5/5 seeds and preserve final Y1 accuracy, with a measurable
decision-prefix CE cost. A11_13 closes one downstream construct-validity gate:
the paired persistent-assistant task has Q_task=1.0 in 5/5 seeds, exact
local/cue insufficiency, complete paraphrase/counterfactual guards, and maximum
tested lexical-shortcut accuracy 0.5375. A11_14/14b separate local-language
fit from unseen-paraphrase transfer; random small models fit seen wording but
do not make the evaluation efficiency comparison adjudicable. A11_15 uses
Qwen3-0.6B and raises held-out Q to roughly 0.8, but neither method reaches the
sustained threshold; MTP's private H2 reaches about 0.90 without a stable
common-H1 advantage. A11_16--A11_18 locate the missing mechanism: the extra H2
gradient is mostly on shared parameters, and after a full-vocabulary burn-in
it is useful under both H2 and standard H1 at the current h_T in 5/5 seeds,
but becomes adverse under either head at h_{T+1} in 5/5 post-burn-in AUC
comparisons under the original Decision bridge. A11_19 shows this is not a
bridge-independent position law: Decision/Answer have positive AUC in 0/5
seeds, while Therefore/colon have positive AUC in 4/5. Its strict
preregistered verdict remains insufficient because the all-cell finite-
difference guard passes in only 3/5 seeds, with failures concentrated at
near-zero predictions. Thus horizon coverage and current-state formation do
not imply downstream use-position preservation; the cross-position condition
must include the intervening token/state transition. A11_20 tests this local
ordering end to end: the standard-H1 margin interaction is positive in 5/5
seeds, but the Q_real interaction is positive in only 3/5, favorable-bridge
MTP gain in only 2/5, no run reaches the sustained threshold, and local guards
fail. Thus local bridge-conditioned margin alignment is not sufficient for a
downstream MTP efficiency advantage. The A11 bridge phase remains closed; do
not add bridge, weight, or duration sweeps. Under the user's explicit return to
the MTP mechanism question, A11_22 now tests the paired one-step standard-loss
interference law on the exact permutation-composition task. Its numerical
component passes at relative step norm $10^{-5}$ (slope `1.0174`, Pearson
`0.9990`, sign agreement `1.0000`), but the formal task-mechanism verdict is
insufficient because all five validation answer accuracies remain at chance
`0.125`. The only current A11 decision is one minimal task/model calibration
repair while holding the data, losses, seeds, and finite-difference audit
fixed. A11_23/23b now show that bounded depth/time/width and explicit pair-token
repairs still leave the from-scratch sequence task near chance. A11_24 supports
structural rank competition in an oracle-factor linear model: rank-1 MTP
standard-loss gap is `0.9084--1.0218`, while rank 2 removes it to numerical
zero. A11_25 shows dose-matched curriculum does not Pareto-repair the rank-1
deficit (`0/5`). A11_26 therefore parks scale/real transfer until a calibrated
neural bridge exists. A11_27 now defines the immediate utilization question:
after one shared pretrained-model checkpoint passes the two-hop task gate,
does informative Next-2 increase counterfactual control of the answer by the
standard next-token head relative to NTP? Its anchor is complete and protocol
is a draft; no run is authorized yet. A11_21, MoE, and Router remain parked.
A11 still does not
prove natural-language or code MTP efficiency, pure-pretraining benefit, MoE
routing preservation, semantic expert identity, or expert utility.
```

Sharper logic:

```text
ordinary top-1 routing can collapse under uniform features
-> collapse can come from common components, wrong hidden-state populations,
   and early-training feedback
-> route-position feature geometry can be discovered and linearly routed
-> all-position clustering is not a valid proxy population
-> controlled center initialization is preserved by positive margin buffer,
   not by active router-center tracking
-> A06_21 decomposes this buffer: controlled center-init preservation keeps
   positive current and cluster-aware margins with zero sign flips; the main
   negative pressure is feature-center drift, not router-side active tracking
-> A06_23 sharpens this buffer claim: preservation has a finite safe-margin
   threshold in the controlled no-position bridge; $q\ge0.05$ preserves, while
   $q=0.02$ starts correct but crosses boundaries during training
-> real-DCLM proxy routing exists at step 0 but ordinary training erases it
-> A06_22 reproduces the real-DCLM collapse, but common/residual dominance
   flips across common projectors, so "common causes collapse" is not yet a
   stable claim
-> A06_31 shows that expert utility, not route-center geometry alone, controls
   the sign of local soft-router margin pressure
-> A06_32 shows that weighted top-1 has correction, but it searches by current
   score rank because unselected expert utilities are not compared
-> A06_33 shows that background count alone is insufficient; systematic
   boundary-projected bias creates separate first-cross and recovery thresholds
-> the next decision is to use router-only, representation-only, joint-SGD, and
   joint-AdamW freeze interventions on the trainable full-LM bridge; exact
   margin reconstruction remains an algebraic guard, not causal evidence
-> functional value must be tested through common/rare interference or expert
   utility, not load balance alone
```

## Current Evidence Boundary

Can claim:

```text
Controlled route-position feature partitions are reachable. Ordinary top-1
routing does not naturally discover or preserve the right partition. In the
controlled no-position bridge, center initialization preserves by a positive
margin buffer, not by active router-center tracking; A06_23 shows this buffer
has a finite safe threshold rather than "any positive margin is enough." In
real DCLM early training, proxy routing can be overwritten by step 5/10. A06_22
shows that common/residual dominance is projector-dependent: mean-common
supports common dominance, but top hidden-PC and router-row projectors do not.
In frozen controlled dynamics, A06_31 shows that matched expert utility creates
positive margin pressure; A06_32 shows that top-1 correction is rank-mediated
but not absent; A06_33 shows that systematic boundary-projected background bias
can exhaust margin while orthogonal or balanced background does not. Margin
crossing can be transient and must be separated from final failure.
```

Cannot claim:

```text
Real semantic experts exist.
Balanced load proves specialization.
High route NMI proves expert utility.
The current common projector is the true causal common operator.
Common subtraction is already a validated routing method.
The frozen-SGD margin budget transfers unchanged to trainable hidden states or
AdamW.
Any first sign flip proves irreversible routing collapse.
A07 neural proxy already proves useful MoE specialization.
Reverse KV retrieval follows from the current evidence.
```

## 05 / 06 / 07 Reading Entry

Root sync now stores research-line synthesis, not full anchor mirrors:

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
sync/S000_current_specialization/research_lines/05_failure_mechanism_line_cn.md
sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md
sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md
```

Project-local source anchors remain the source of truth:

```text
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
```

Most important current evidence:

```text
Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_08_label_free_feature_discovery_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum_cn.md
Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/summary.md
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_27_standard_head_causal_representation_use_anchor.md
Projects/from-attention-to-search/main/experiments/A11/A11_27_standard_head_causal_representation_use/protocol.md
Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/summary.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0701/meeting_brief.md
```

## Active Mainline Sync Rule

For this active specialization line, `PROJECTS.md` and the active root sync
entry must move together when the mainline state changes.

A mainline state change means an accepted update to any of these objects:

```text
current decision question
active ladder level
current route
current evidence boundary
claim boundary
next decision
web-side source links
```

When that happens, update the active root sync entry in the same task:

```text
sync/S000_current_specialization/README.md
sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md
and the affected 05 / 06 / 07 research-line note when needed
```

This rule is for keeping web-side and cross-project readers current. It is not
a raw-output mirror and does not authorize graph edits, external collaborator
sync, handoff packaging, commits, pushes, or copying full anchors unless the
user explicitly asks for those actions.

## Synthetic Versus Real Boundary

Controlled synthetic experiments can establish:

```text
whether a mechanism is possible;
whether a metric surface is valid;
whether a known feature partition can be discovered, routed, preserved, or
used under controlled labels and controlled nuisance variables.
```

They cannot establish:

```text
natural-language semantics;
real-checkpoint behavior;
deployable routing;
real expert utility;
robust transfer from controlled labels to open text.
```

Real-DCLM proxy experiments can establish:

```text
whether stable hidden-state proxy clusters exist;
whether those proxy clusters are linearly routable at step 0;
whether ordinary next-token training preserves or erases that proxy routing.
```

They cannot establish by themselves:

```text
semantic feature identity;
causal expert utility;
dense-beating MoE value;
final pretrained-MoE behavior.
```

## Next Decision

Do not run another broad feature-existence, common-subtraction, or spectral
router sweep. The next anchor should decide one causal bottleneck:

```text
representation-router-optimizer co-dynamics under full-sequence LM training
```

Primary metric:

```text
whether router-only, representation-only, joint-SGD, or joint-AdamW freeze
interventions reproduce or remove matched-margin first crossing and re-entry
```

Required guards:

```text
margin p05, matched identity, route NMI, LM loss, first-cross time, re-entry
time, X/A/Q/h source-center trajectories, raw source gradients, AdamW moments,
actual preconditioned boundary updates, max load, and active experts
```

The exact three-term finite margin decomposition is an algebraic validity guard,
not causal evidence. Method construction is allowed only after freeze
interventions localize the necessary path to representation formation, router
correction, optimizer transmission, or their interaction.

## Root Surfaces

- `AGENTS.md`: general agent behavior and repository rules.
- `PROJECTS.md`: this current project-state registry.
- `sync/`: compact research-line synthesis for web-side or cross-project readers.
- `Projects/graphs/`: Sidecar-readable graph manifests.
- `daily_research_reports/`: daily cards and meeting materials.
- `paper_reading/`: paper and blog reading cards.
- `templates/`: maintained reusable templates.
- `prompts/`: reusable prompts.
- `skills/`: repo-tracked skill sources.

## Web-Side Rule

Web-side agents should not rely on chat history. If they cannot inspect
`Projects/`, use this file and `sync/` first, then ask a local Codex agent to
expose the relevant graph, anchor, or experiment record.

## Course Delivery Projects

Academic Writing Project 2 is a course-delivery wrapper:

```text
Projects/academic_writing/
```

It uses the current MoE gating specialization work as source material for
slides, a poster, and a CVPR-format manuscript. It does not replace the
research mainline and should not update graphs, root sync, or experiment
records unless explicitly requested.
