# A06_02_04_E04 Detailed Record: Event-Triggered Representation Recovery

## 0. Quick Recap

**Purpose:** Determine whether representation learning is needed after a shared first-crossing state and whether any protection is direct or mediated by future router updates.

**Hypothesis:** Representation was expected to be necessary after crossing while its direct center-motion term remained non-corrective, implying indirect router-gradient shaping.

**Experiment idea:** Clone the complete state after the first crossing update; continue jointly, freeze representation, freeze router, or replay joint router updates with representation frozen.

**Conclusion:** The global indirect-shaping hypothesis is rejected. Router and representation are mostly redundant recovery paths. Representation-only continuation recovers every event and nearly matches joint LM loss; router-only continuation recovers 94.05% but has much higher 50-step loss.

**Evidence:** 32 seeds, 84 paired events, exact clone and joint replay, re-entry rates 100% / 94.05% / 100%, and path taxonomy 79 redundant / 4 direct representation-required / 1 indirect representation-required.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Metric / unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Event unit | One first crossing for one non-common feature | \((seed,regime,f,b_c,t_c)\) | paired observation | shared causal start | natural semantics |
| Critical pair | Fixed crossed feature-competitor boundary | \((f,b_c)\) | router boundary | exact pairwise decomposition | full feature safety |
| Critical-pair re-entry | Fixed margin becomes positive | first \(\tau\le50\) with \(m_{f,b_c}>0\) | updates | primary recovery | functional expert value |
| Feature-level re-entry | All matched margins become positive | \(\min_{b\ne f}m_{f,b}>0\) | binary | competitor-switch guard | downstream utility |
| Router term | Applied row-motion contribution | \(r=(\Delta w_f-\Delta w_b)^\top\mu_f\) | margin change | realized router path | raw direction only |
| Direct representation term | Center motion plus finite-step interaction | \(c=(w_f-w_b)^\top\Delta\mu_f+(\Delta w_f-\Delta w_b)^\top\Delta\mu_f\) | margin change | direct geometry | intervention-invariant effect |
| Path taxonomy | Classification by the three freeze/replay outcomes | redundant, direct-required, indirect-required | event count | exposes heterogeneity | real-LLM prevalence |

## 2. Protocol Compliance Audit

| Requirement | Actual | Status |
| --- | --- | --- |
| 32 seeds | 32 | pass |
| Eligible non-common events | 84, minimum 48 | pass |
| Identical model/optimizer/router clone | maximum state error 0 | pass |
| Branch-initial margin and loss equality | maximum spread 0 | pass |
| Crossing identity preserved after recomputation | 0 positive recomputed events | pass |
| Joint clone reproduces uninterrupted trajectory | maximum state error 0 | pass |
| Pairwise margin budget closure | \(1.96\times10^{-7}\) | pass |
| Gradient source closure | \(1.13\times10^{-6}\) | pass |
| Both-frozen zero-change guard | \(5.22\times10^{-8}\) | pass |
| Representation-frozen direct term | maximum \(5.52\times10^{-8}\) | pass |
| Router-frozen applied router term | 0 | pass |

The event-time forward and later clone-time forward differ by at most \(1.60\times10^{-5}\) in one recomputed margin because of GPU floating-point reduction. This is not a clone-state error: all cloned states and branch-start metrics are identical, joint continuation reproduces the uninterrupted trajectory exactly, and every recomputed event remains crossed. It is retained as a non-blocking numerical diagnostic.

## 3. Exact Setup

### Data

- 32 static sequences per batch.
- Sequence length 33 and 32 supervised next-token positions.
- Four uniform features.
- `biased_s8`: 8/32 signal sequences and 24/32 class-0 background sequences.
- `biased_s4`: 4/32 signal sequences and 28/32 class-0 background sequences.
- Features 1--3 are the primary event population.
- No positional embedding.

### Model

- Hidden dimension 64, four attention heads.
- One causal attention layer, residual connection, and layer normalization.
- One weighted-top-1 MoE.
- Four fixed function-matched experts, expert strength 4.0.
- Router initialized from dual feature centers with center-margin p05 target 0.5.

### Training

- Full-sequence cross-entropy over all 32 next-token positions.
- Representation optimizer: AdamW, learning rate 0.002, betas 0.9/0.999, epsilon \(10^{-8}\), weight decay \(10^{-4}\).
- Router update: current negative raw gradient scaled to the norm of the full AdamW candidate.
- Detect events in the first 50 updates; continue each clone for 50 updates.
- Four-GPU ACP job `pt-gq034aru`, state `SUCCEEDED`.

## 4. Exact Finite-Step Model

For the fixed critical pair:

\[
m(t_c+\tau)=m(t_c)+R(\tau)+C(\tau),
\]

\[
R(\tau)=\sum_{s=1}^{\tau}(\Delta w_f-\Delta w_b)^\top\mu_f,
\]

\[
C(\tau)=\sum_{s=1}^{\tau}
\left[(w_f-w_b)^\top\Delta\mu_f
+(\Delta w_f-\Delta w_b)^\top\Delta\mu_f\right].
\]

This identity is exact inside one trajectory. It does not imply that \(R\) or \(C\) remains fixed after deleting the other trainable block.

## 5. Primary Results

### 5.1 Overall Paired Re-entry

| Branch | Re-entry | Seed-clustered 95% CI | Median time | Mean final loss |
| --- | ---: | ---: | ---: | ---: |
| Joint | 1.0000 | [1.0000, 1.0000] | 1 | \(1.5653\times10^{-4}\) |
| Representation frozen | 0.9405 | [0.8791, 1.0000] | 1 among recovered | \(3.0786\times10^{-3}\) |
| Router frozen | 1.0000 | [1.0000, 1.0000] | 5.5--6 | \(1.6901\times10^{-4}\) |
| Joint-router replay | 0.9524 | [0.8889, 1.0000] | 1 among recovered | \(3.0999\times10^{-3}\) |

Representation-freeze necessity is 0.0595 with 95% CI \([0,0.1209]\). Router-freeze necessity is 0.

### 5.2 By Background Regime

| Regime | Events | Joint | Representation frozen | Router frozen | Replay |
| --- | ---: | ---: | ---: | ---: | ---: |
| 8/32 signal | 40 | 1.000 | 0.950 | 1.000 | 0.950 |
| 4/32 signal | 44 | 1.000 | 0.932 | 1.000 | 0.955 |

The qualitative result is stable across both background strengths.

### 5.3 Route Recovery Versus Task Learning

Router-only continuation restores 79/84 boundaries, usually in one update, but its mean 50-step loss is \(3.08\times10^{-3}\). Representation-only continuation restores 84/84 boundaries more slowly and reaches \(1.69\times10^{-4}\), close to joint continuation at \(1.57\times10^{-4}\).

Therefore a positive route margin is not a substitute for task learning. The representation path carries most functional optimization in this fixed-expert task, while the router path accelerates geometric re-entry.

## 6. Event-Level Path Taxonomy

| Class | Count | Evidence pattern |
| --- | ---: | --- |
| Redundant single-path recovery | 79 | both representation-frozen and router-frozen branches re-enter |
| Representation-required direct recovery | 4 | representation-frozen and replay fail; router-frozen re-enters; joint direct \(C>0\) |
| Representation-required indirect router shaping | 1 | representation-frozen fails; joint-router replay re-enters; joint \(C\le0\) |

The five representation-required events occur in three seeds. Four require direct representation motion under the joint trajectory; one is consistent with representation-shaped future router updates.

## 7. Direct And Indirect Budget Audit

- Joint cumulative \(C\) is nonpositive at re-entry in 62/84 events (73.81%).
- Router-frozen cumulative \(C\) is positive at re-entry in 84/84 events.
- Only 11/84 events have larger joint router correction than representation-frozen router correction at joint re-entry.
- The median paired router advantage is exactly 0.

The apparent tension is causal, not algebraic. Freezing the router changes subsequent losses and representation gradients, so the representation-only \(C\) trajectory is not the joint \(C\) trajectory with \(R\) set to zero.

## 8. Visualization Results

### Figure 1: Recovery Curves

![Recovery curves](figures/recovery_curves.png)

- **Purpose:** Test post-cross path necessity.
- **Setup:** All curves begin from the same 84 crossed event states.
- **How to read:** Lower unrecovered fraction means faster and more complete re-entry.
- **Observed:** Joint recovery is nearly immediate; router-frozen recovery is slower but complete; representation-frozen and replay each leave a small persistent failure set.
- **Take-home:** Neither path is globally necessary; recovery is mostly redundant.
- **Remaining uncertainty:** The fixed experts make task utility unusually stable.

### Figure 2: Budget Mediation

![Budget mediation](figures/budget_mediation.png)

- **Purpose:** Compare applied router correction and direct representation correction under each intervention.
- **Setup:** Event-aligned cumulative terms normalized by initial critical-pair margin.
- **How to read:** Positive values repair the crossed boundary.
- **Observed:** Joint router motion rapidly becomes positive. Router-frozen representation motion becomes strongly positive. Joint direct representation motion is initially negative before becoming positive later.
- **Take-home:** The contribution fields are intervention-dependent.
- **Remaining uncertainty:** The plot is a median and does not expose the five representation-required events individually.

## 9. Hypothesis Adjudication

| Hypothesis | Registered result | Final interpretation |
| --- | --- | --- |
| H1 representation necessary | rejected | post-cross representation is necessary in only 5/84 events |
| H2 router necessary | rejected | representation-only continuation recovers 84/84 |
| H3 global indirect shaping | rejected | only 1/84 matches the strict indirect class |
| H4 operational non-necessity | passes | representation is usually not necessary for re-entry, but "pre-cross only" is not supported |

The wording correction is required because router-frozen representation learning has a strong post-cross causal effect and near-joint LM loss.

## 10. Updated Mechanism

The controlled fixed-expert system has two adaptive recovery fields:

\[
\dot m_W=\langle\nabla_W m,\Delta W\rangle,
\qquad
\dot m_\phi=\langle\nabla_\phi m,\Delta\phi\rangle.
\]

Both can restore the boundary. Updating either block changes the future gradient field of the other, so a complete model requires state-dependent co-dynamics rather than a fixed additive reserve estimated from one trajectory.

This does not justify another detailed recovery decomposition in the current fixed-expert table. The stronger missing variable is trainable expert utility.

## 11. Claim Boundary

**Supported:** Mostly redundant post-cross route recovery; five representation-required events; representation-only sufficiency; router-only geometric recovery with weaker task optimization; intervention-dependent budget components.

**Rejected:** Global post-cross representation necessity; global router necessity; one universal indirect recovery path; the claim that representation matters only before crossing.

**Still open:** Whether trainable experts acquire feature-specific utility; whether route-conditioned expert learning stabilizes identity; real-DCLM transfer; useful specialization; compute efficiency.

## 12. Next Decision

Move to a trainable-expert bridge. The next anchor asks whether a correct route partition creates a positive counterfactual utility gap for the assigned expert and whether that learned utility subsequently stabilizes the same route identity.

## 13. Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`
- Protocol: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E04_event_triggered_recovery/protocol.md`
- Summary: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E04_event_triggered_recovery/summary.md`
- Detailed record: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E04_event_triggered_recovery/detailed.md`
- Curated figures: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E04_event_triggered_recovery/figures/`
- Curated tables: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E04_event_triggered_recovery/tables/`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_37_event_triggered_representation_recovery.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_37_event_triggered_representation_recovery.json`
- Submitter: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_37_event_triggered_representation_recovery_4gpu_acp.sh`
- Raw result directory: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_37_event_triggered_representation_recovery/a06_37_full_4gpu_20260710_01/`
- ACP job: `pt-gq034aru`, `SUCCEEDED`

```bash
A0637_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_37_full_4gpu_20260710_01 bash scripts/submit_a06_37_event_triggered_representation_recovery_4gpu_acp.sh
```
