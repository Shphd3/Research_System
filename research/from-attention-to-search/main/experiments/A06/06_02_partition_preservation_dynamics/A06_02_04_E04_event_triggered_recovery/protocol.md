# Protocol: A06_02_04_E04 Event-Triggered Representation Recovery

## 0. Approval Snapshot

**Approval status:** Approved by the user's instruction to continue the research goal.

**Purpose:** Starting from an identical first-crossing state, decide whether continued representation learning repairs the crossed boundary directly through feature-center motion or indirectly by changing future router updates.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Anchor decision question:** Is post-cross representation learning necessary for critical-pair re-entry, and if so, is its effect mediated by future router updates?

**Physical prior tested:** For a fixed crossed boundary, post-cross margin change is exactly the sum of applied router motion \(R\) and direct representation motion \(C\). If \(C\le0\) while representation learning is still necessary, its protective effect must enter through the future router-update path.

**Core model term tested:**

\[
m(t_c+\tau)=m(t_c)+R(\tau)+C(\tau).
\]

**Main falsifier:** Post-cross representation freezing reduces re-entry by at most 0.10 and does not materially delay it.

**Experiment role:** Root-cause audit, not method construction.

**Primary metric:** Paired post-cross representation-freeze necessity

\[
N_{repr}(re)
=\Pr(re_{joint}=1,re_{freeze\_repr}=0\mid re_{joint}=1).
\]

**Claim boundary:** The run can classify recovery in the controlled one-layer full-LM bridge. It cannot establish a deployable controller, real-LLM transfer, learned-expert specialization, MTP benefit, or downstream value.

**Minimal setup:** Reuse A06_02_04_E03's one-layer Transformer and weighted-top-1 MoE, fixed function-matched experts, full-sequence LM loss, no positional embedding, and full-norm raw-gradient router rule. Use 32 seeds, two event-bearing regimes, and 50 post-cross updates.

**Causal conditions:** Joint continuation; post-cross representation freeze; post-cross router freeze.

**Mechanism guard:** Freeze representation and replay the exact joint router updates. This is an oracle mediation diagnostic, not a method condition.

**Support indirect recovery:** \(N_{repr}(re)\ge0.75\); router freeze also removes at least 75% of joint re-entry; at least 75% of joint re-entry cells have \(C\le0\); joint cumulative router correction exceeds the representation-frozen branch; and router-update replay preserves re-entry within 0.10.

**Support pre-cross-only representation:** Re-entry rate falls by at most 0.10 after post-cross representation freeze and paired median delay is at most two updates.

**Insufficient evidence:** Fewer than 32 seeds, fewer than 48 eligible events, failed deterministic clone replay, closure error above \(10^{-5}\), or non-finite values.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Event unit | One explicit first-crossing sample | \((seed,regime,f,b_c,t_c)\) | paired observation | gives every branch the same failure state | natural-feature independence |
| Critical pair | Feature and lowest-margin competitor fixed at first crossing | \(b_c=\arg\min_{b\ne f}m_{f,b}(t_c)\) | one router boundary | keeps the algebraic object fixed | all other boundaries are safe |
| Critical-pair re-entry | The fixed crossed margin becomes positive within 50 updates | \(T_{re}=\min\{\tau\le50:m_{f,b_c}(t_c+\tau)>0\}\) | updates | primary recovery event | full feature recovery |
| Feature-level re-entry | Every matched margin for the feature is positive | \(\min_{b\ne f}m_{f,b}>0\) | binary event | guards competitor switching | expert utility |
| Router contribution | Margin change from the applied router-row update | \(r=(\Delta w_f-\Delta w_b)^\top\mu_f\) | router-score difference | realized correction path | raw-gradient direction |
| Direct representation contribution | Margin change from center motion plus finite-step interaction | \(c=(w_f-w_b)^\top\Delta\mu_f+(\Delta w_f-\Delta w_b)^\top\Delta\mu_f\) | router-score difference | tests direct geometric repair | future-gradient shaping |
| Raw-gradient boundary velocity | Alignment of the negative raw gradient with margin increase | \(v^{raw}\) | \([-1,1]\) | separates direction from update norm | actual optimizer transmission |
| Paired freeze necessity | Joint recovery events removed by path deletion | \(N_k(re)\) | \([0,1]\) | identifies post-cross necessity | sufficiency |
| Seed-clustered confidence interval | Resample seeds rather than correlated feature events | 10,000 seed-level bootstrap draws | 95% interval | prevents pseudo-replication | distribution transfer |
| Mediation replay | Freeze representation and apply joint branch router updates | \(\Delta W_t=\Delta W_t^{joint}\) | diagnostic branch | tests whether router trajectory carries recovery | deployable method |

## 2. Anchor Alignment

**Parent result:** A06_02_04_E03 supports a direction-fixed router-scale transition but rejects a router-only physical threshold. Direct representation motion supplies missing crossing budget and remains margin-consuming through re-entry.

**Uncertainty reduced:** Whether representation protection acts before crossing only or remains necessary after crossing by shaping future router updates.

**Mainline impact:** The result changes the method family. Indirect post-cross support requires a joint representation-conditioned risk model; pre-cross-only support permits a router-local recovery controller.

## 3. Tested Hypotheses

### H1. Post-cross representation learning is necessary

Support requires joint critical-pair re-entry rate at least 0.25, \(N_{repr}(re)\ge0.75\), and seed-clustered 95% confidence lower bound above 0.50.

### H2. Post-cross router updates are necessary

Support requires \(N_{router}(re)\ge0.75\) with the same confidence guard.

### H3. Representation recovery is indirect router-update shaping

H1 and H2 must hold, plus:

1. at least 75% of joint-recovered events have cumulative \(C\le0\) through joint re-entry;
2. at joint re-entry time, at least 75% satisfy

\[
D_R
=\frac{R_{joint}(T_{re}^{joint})-R_{freeze\_repr}(T_{re}^{joint})}
{m_{f,b_c}(0)}>0;
\]

3. the seed-level median \(D_R\) is positive with bootstrap lower bound above zero;
4. \(P_{replay}(re)\ge P_{joint}(re)-0.10\).

### H4. Representation matters only before crossing

Support if joint and representation-frozen re-entry rates differ by at most 0.10 and paired median re-entry delay is at most two updates.

## 4. Rival Explanations

| Rival | Expected pattern | Separating intervention |
| --- | --- | --- |
| Router alone recovers | representation freeze preserves re-entry | joint vs representation freeze |
| Center directly returns | router freeze re-enters with \(C>0\) | router freeze plus exact \(C\) |
| Both post-cross paths are necessary | both freezes remove recovery and \(C>0\) | both freezes plus \(C\) sign |
| Representation indirectly shapes router updates | both freezes remove recovery, joint \(C\le0\), joint \(R\) is more corrective | three branches, \(R/C\), gradient diagnostics |
| Earlier result used different failure states | differences disappear after event cloning | shared crossing checkpoint |
| Clone/update-order bug | joint clone fails uninterrupted replay | deterministic replay guard |

## 5. Data / Model / Router / Objective

### 5.1 Data

- Static batch of 32 sequences.
- Sequence length 33; all 32 next-token targets contribute to the loss.
- Four uniform features and four fixed function-matched experts.
- No positional embedding.
- Critical regimes: 8/32 or 4/32 signal sequences; remaining sequences are class-0 background.
- Primary population: non-common features 1--3.
- The static batch makes every post-cross branch share the same future data stream.

### 5.2 Model

- Hidden dimension 64 and four attention heads.
- One causal self-attention layer, residual connection, and layer normalization.
- One weighted-top-1 MoE: only the highest-score expert executes, while its router probability weights the output.
- Four fixed function-matched experts; expert strength 4.0 and readout-type strength 1.0.
- Dual-center router initialization with initial center-margin p05 target 0.5.

### 5.3 Objective

\[
\ell_{LM}
=\frac{1}{32B}\sum_{i=1}^{B}\sum_{t=1}^{32}
-\log p_\theta(x_{i,t+1}\mid x_{i,\le t}).
\]

Signal and background contributions use the same total-position denominator, so losses and raw router gradients add exactly.

### 5.4 Update rules

Representation parameters use AdamW with learning rate 0.002, \(\beta_1=0.9\), \(\beta_2=0.999\), \(\epsilon=10^{-8}\), and weight decay \(10^{-4}\).

The router uses A06_02_04_E03's full-norm raw-gradient rule:

\[
\Delta W_t
=-\lVert\Delta W_t^{full\_AdamW}\rVert_F
\frac{g_t}{\lVert g_t\rVert_F}.
\]

This tests how representation changes future raw gradients and transmitted norm, not standard AdamW direction.

## 6. Conditions, Seeds, And Checkpoints

### 6.1 Event generation

- Seeds 0--31.
- Two critical regimes per seed.
- Run the pre-event trajectory for at most 50 updates.
- For each non-common feature, trigger once when \(\min_{b\ne f}m_{f,b}\le0\).
- Fix \(b_c\) at the event and clone the complete post-update state.
- Cluster inference by seed because multiple feature events can share one trajectory.

### 6.2 Post-cross conditions

| Item | Representation update | Applied router update | Role | Primary evidence |
| --- | --- | --- | --- | --- |
| Joint continuation | yes | yes | reference recovery | yes |
| Representation frozen | no | yes | representation necessity | yes |
| Router frozen | yes | no | direct representation sufficiency | yes |
| Representation frozen + joint router replay | no | exact joint \(\Delta W_t\) | mediation sufficiency | guard |
| Both frozen | no | no | zero-change check for one update | validity only |

Every causal and replay branch runs 50 updates and records every update.

## 7. Primary Metric

\[
N_{repr}(re)
=\frac{\sum_i\mathbf 1[re_i^{joint}=1,re_i^{freeze\_repr}=0]}
{\sum_i\mathbf 1[re_i^{joint}=1]}.
\]

The point estimate is event-level. Confidence intervals resample seeds. This metric dominates the decision because it deletes only future representation updates after a shared failure state.

## 8. Secondary Metrics

1. \(N_{router}(re)\).
2. Critical-pair and feature-level re-entry rates and times.
3. Cumulative \(R\), \(C\), and exact budget closure through joint re-entry.
4. Paired \(D_R\).
5. Total, signal, and background raw-gradient velocity, norm, and actual boundary projection.
6. Full candidate norm, actual router-update norm, and router moment norms.
7. Route identity, route NMI, minimum center margin, and LM loss.
8. Mediation-replay re-entry.

Raw-gradient metrics refine whether the indirect effect changes direction, scale, or both. They do not replace H1.

## 9. Known Good / Known Bad / Known Confusing

**Known good:** Joint clone reproduces uninterrupted joint continuation; both-frozen state has zero change; representation-frozen \(C=0\); router-frozen applied \(R=0\); source gradients close exactly.

**Known bad:** Branches differ before the first post-cross update; joint clone diverges from uninterrupted replay; the critical competitor changes silently during analysis.

**Known confusing:** Critical-pair re-entry is weaker than feature-level re-entry; mediation replay is an oracle diagnostic; the raw-gradient rule inherits its norm from a shadow AdamW candidate; feature events within a seed are correlated.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- |
| Data / initialization | Does the setup reproduce A06_02_04_E03? | data audit, function match, and initial margin pass | `data_audit.csv` | event generation |
| Pre-event trajectory | Are enough early events produced? | at least 48 eligible events | `event_manifest.csv` | cloning |
| Clone parity | Are all branches identical at start? | state error below \(10^{-7}\) | `clone_audit.csv` | branches |
| Joint replay | Does clone reproduce uninterrupted training? | max error below \(10^{-6}\) | `replay_audit.csv` | causal analysis |
| Margin budget | Does \(R+C\) reconstruct margin? | max error below \(10^{-5}\) | `pairwise_budget.csv` | adjudication |
| Gradient sources | Do signal and background close to total? | max error below \(10^{-5}\) | `gradient_source.csv` | source interpretation |
| Aggregation | Are all paired metrics complete? | 32 seeds and all event keys present | `decision_summary.json` | result report |

## 11. Algorithm Specification

**Event checkpoint contains:** model state; representation AdamW step, first and second moments; router transmission step and moments; random state; batch identity; \(t_c,f,b_c\); pre/post-cross margins; and initial pairwise margin.

**Per-step order:**

1. Forward the current branch and compute full-sequence loss.
2. Compute total, signal, and background raw router gradients.
3. Save pre-update router weights, feature centers, and pairwise margins.
4. Apply or skip the representation AdamW update according to branch.
5. Apply, skip, or replay the router update according to branch. Router-frozen uses a shadow transmission state for diagnostics only.
6. Recompute centers and margins; record \(r\), \(c\), and closure.
7. Update re-entry events and times.

The update order remains identical to A06_02_04_E03: compute router raw gradients from the same forward state, then apply representation update, then apply the router update derived from that raw gradient.

**Outputs:** `event_manifest.csv`, `clone_audit.csv`, `replay_audit.csv`, `branch_events.csv`, `branch_trajectory.csv`, `pairwise_budget.csv`, `gradient_source.csv`, `mediation_replay.csv`, `decision_summary.json`, and two central figures.

## 12. Success / Alternative / Insufficient Outcomes

| Pattern | Judgment | Next decision |
| --- | --- | --- |
| H1, H2, H3 pass | indirect post-cross router-update shaping | build representation-conditioned joint margin-risk model |
| H4 passes | representation matters before crossing only | control pre-cross co-dynamics; keep post-cross controller router-local |
| Router freeze re-enters with \(C>0\) | direct representation recovery | model center-motion reserve first |
| Both freezes remove recovery and \(C>0\) | mixed direct and indirect recovery | next anchor models state-dependent path allocation |
| Joint recovery is low or unstable | 50-step window unresolved | audit prior-event reproduction before extending horizon |
| Any validity guard fails | insufficient evidence | repair implementation; no claim update |

## 13. Plot Contracts

### Figure 1. Recovery after the identical crossing state

Show post-cross updates on the x-axis and unrecovered-event fraction plus final re-entry rate on the y-axis, with seed-clustered confidence intervals. It decides path necessity, not the hidden direction carrying the path.

### Figure 2. Direct representation term versus router mediation

Show event-aligned cumulative \(R\) and \(C\), normalized by initial pairwise margin, for joint, representation-frozen, router-frozen, and replay branches. It classifies direct, indirect, or mixed recovery, but cannot establish real-LLM transfer.

## 14. Remote Four-GPU Execution Contract

- Code workspace: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`
- Runner: `scripts/run_a06_37_event_triggered_representation_recovery.py`
- Config: `configs/a06_37_event_triggered_representation_recovery.json`
- Submitter: `scripts/submit_a06_37_event_triggered_representation_recovery_4gpu_acp.sh`
- GPU count: 4; eight seeds per shard.
- Smoke: known event-bearing seeds 0 and 1, both regimes, pre-event 10 updates, post-cross 10 updates. All expected tables and clone/budget guards must pass.
- Full: 32 seeds, pre-event at most 50 updates, four 50-update event branches.
- Record ACP job id, command, config, logs, result directory, and first diagnosis in `detailed.md`.

## 15. Review Notes And Protocol Changes

The approved English protocol preserves the Chinese audit draft's question, event unit, conditions, primary metric, thresholds, and claim boundary. The only explanatory refinement is to make the mediation replay inequality explicit as \(P_{replay}\ge P_{joint}-0.10\).
