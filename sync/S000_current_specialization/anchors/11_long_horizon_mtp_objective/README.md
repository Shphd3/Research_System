# Long-Horizon MTP Objective Line

This folder tracks the objective-level line for long-horizon prediction and
multi-token prediction. It is separate from the MoE routing preservation line:
the current question is about the training objective's pressure on a single
prefix hidden state, not about expert routing, common subtraction, or expert
utility.

Current role in the research system: this is an evidence-updated supporting
objective line. It tests whether a multi-token objective can directly supervise
the current hidden state to retain a long-horizon variable. It may later inform
route-relevant hidden-state formation in A06, but it does not by itself prove
MoE expert specialization, routing preservation, or expert utility.

## Active Anchors

- `11_01_k2_branch_delayed_next_two_anchor.md`
- `11_02_two_token_shared_trunk_signal_interference_anchor.md`
- `11_03_k2_semantic_efficiency_anchor.md`
- `11_04_k3_first_informative_horizon_anchor.md`
- `11_05_semantic_efficiency_bridge_anchor.md`

The English files are canonical. The current line has moved from a supported
K=2 objective-level separation to an evidence-updated next-K coverage story:
when K covers the first informative future horizon, low loss at that horizon
forces the current hidden state to contain the delayed variable under the
controlled construction.

## Line Story

- `../../stories/11_long_horizon_mtp_objective/story_cn.md`

This story is the line-level Chinese synthesis for the A11 long-horizon MTP
objective line. It explains the research question, controlled data
construction, K=2 theorem route, next-K extension, experiment evidence chain,
claim boundary, and next decision. Anchors remain the source of adjudicable
questions; the story is the reading path that connects them.

## Companion / Legacy Review Copies

- `11_01_k2_branch_delayed_next_two_anchor_cn.md` is not currently present in
  this folder.
- `11_02_two_token_shared_trunk_signal_interference_anchor_cn.md`

Chinese companion files are review copies when present. The English files
remain canonical.

## Evidence Records

- `../../experiments/A11/A11_01_k2_branch_delayed_next_two/protocol.md`
- `../../experiments/A11/A11_01_k2_branch_delayed_next_two/protocol_cn.md`
- `../../experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `../../experiments/A11/A11_01_k2_branch_delayed_next_two/detailed.md`
- `../../experiments/A11/A11_02_two_token_shared_trunk_signal_interference/protocol.md`
- `../../experiments/A11/A11_02_two_token_shared_trunk_signal_interference/protocol_cn.md`
- `../../experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `../../experiments/A11/A11_02_two_token_shared_trunk_signal_interference/detailed.md`
- `../../experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `../../experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- `../../experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `../../experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- `../../experiments/A11/A11_04_02_k3_all_position_control/summary.md`
- `../../experiments/A11/A11_04_02_k3_all_position_control/detailed.md`
- `../../experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md`
- `../../experiments/A11/A11_04_03_k3_efficiency_advantage/detailed.md`
- `../../experiments/A11/A11_04_03_k3_efficiency_advantage/meeting_brief.md`
- `../../experiments/A11/A11_05_semantic_efficiency_bridge/protocol.md`
- `../../experiments/A11/A11_05_semantic_efficiency_bridge/summary.md`
- `../../experiments/A11/A11_05_semantic_efficiency_bridge/detailed.md`

The clean K=2, K=3 first-informative-horizon, all-position control, and
semantic-efficiency runs have been approved, executed, and summarized.
A11_05 is completed. It supports direct decision-prefix horizon-3 supervision
as a mechanism component in clean $\tau=3$ all-position training, while keeping
the boundary that all-position indirect transfer remains a valid recovery path.

## Source Notes

- `daily_research_reports/0707/mtp_k2/long_horizon_next_k_theory_design.md`
  states the broader advisor-facing next-k intuition: multiple future tokens
  that share an early cause can create stronger branch-relevant pressure,
  possibly with signal-to-noise improvement under alignment assumptions.
- `daily_research_reports/0707/mtp_k2/mtp_k2_theory_proof.md` narrows the
  broad intuition to a minimal K=2 theorem: $Y_1$ is shared and $Y_2$ is
  branch-specific, so next-one has a branch-blind optimum at the decision
  state while next-two directly penalizes branch blindness.

## Current Claim Boundary

Can claim after the current A11 evidence:

- In the controlled K=2 branch-delayed distribution, next-two supplies direct
  branch-relevant supervision on the decision hidden state that next-one does
  not supply at that same state.
- In the controlled K=2 shared-trunk setting, a branch-informative second token
  is useful signal under both decision-only and all-position controls, while
  branch probe alone is not a sufficient decision metric.
- In the controlled next-K construction, if the active prediction horizon
  covers the first informative future token $\tau$ and that token is a
  one-to-one code $S_Z$ for the early variable $Z$, low loss at that horizon
  implies that the current hidden state $h_T$ contains information about $Z$.
- In clean decision-only $\tau=3$ runs, K=3 recovers $Z$ earlier and more
  reliably than K=1/K=2; in all-position training, K=3 remains strongest but
  K=1/K=2 can recover through indirect losses.

Cannot claim from this line alone:

- multi-token prediction always outperforms next-token prediction;
- next-token prediction cannot learn long-horizon dependencies;
- curriculum is better than full-horizon multi-token training;
- the synthetic task proves real-language long-range reasoning;
- the objective-level gradient path guarantees optimization success.
- multi-token prediction is already proven more learning-efficient than
  next-token prediction without optimization assumptions;
- K larger than the first informative horizon is always better;
- all-position K=1/K=2 cannot learn the delayed variable;
- gradient cosine sign alone proves whether the extra horizon gradient is
  useful;
- this line proves MoE routing preservation, semantic expert identity, or
  expert utility.

## Bridge Back To The Gating Mainline

The A06 preservation line has repeatedly exposed a related but separate
problem: ordinary training does not automatically protect route-relevant hidden
state structure. A11 supplies an objective-level mechanism candidate for a
future bridge:

```text
Can long-horizon / multi-token supervision make route-relevant hidden states
feature-aware earlier and with thicker margins?
```

This bridge is not yet established. A11 should inform future A06 objective
design only after a protocol explicitly maps the delayed variable $Z$, the
current state $h_T$, and the routing margin / preservation metrics onto the
MoE setting.
