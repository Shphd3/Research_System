# 05_03 Uniform Collapse Common-Offset Anchor

Thinking Card source: [05_03_uniform_collapse_common_offset_thinking_card.md](05_03_uniform_collapse_common_offset_thinking_card.md)

## 1. Problem Definition

Parent problem: route consistency can come from collapse, shortcut, or early lock-in rather than expert specialization.

Sharper subproblem: after auditing data frequency and random router initialization, identify the remaining mechanism that makes one expert dominate under uniform features.

Decision question: does the shared hidden component induce an expert-specific common offset that determines early routing concentration and sets up later collapse?

Not in scope: compositional features, Zipfian frequency, real language data, proof that selected experts are utility-wrong, or a general anti-collapse solution.

## 2. Physical Priors
P1: uniform feature frequency does not imply zero-mean hidden states.
Meaning: fixed positions, template tokens, residual stream offsets, and attention can create a shared component at the routed position.
Could be wrong if: the measured common component is small or unrelated to route load.

P2: a bias-free linear router can still have an effective expert bias.
Meaning: if $h_f=c+r_f$, then $w_e^T c$ shifts all features toward some experts even without a learned bias term.
Could be wrong if: $w_e^T c$ fails to predict early dominant experts.

P3: fixed routed position can be a causal source of common hidden offset.
Meaning: if every feature is routed at the same absolute position, the position embedding can inject a shared direction into the router input.
Could be wrong if: zeroing routed-position embedding or randomizing logical feature position does not reduce common ratio or step-0 load.

P4: training collapse is not only initialization imbalance.
Meaning: common-offset or position-source control can reduce step-0 concentration, but top-1 training may still re-concentrate load.
Could be wrong if: removing the position/common source alone prevents final collapse across seeds.

## 3. Hypothesis

H1: common-offset predicts the step-0 dominant expert.
Supported if: $\arg\max_e w_e^T c$ matches the step-0 dominant expert across seeds and slot patterns.
Weakened if: agreement is near the random baseline.

H2: common-offset cancellation reduces early concentration without destroying target learning.
Supported if: removing $w_e^T c$ lowers step-0 max load and keeps target accuracy high.
Weakened if: load stays high or accuracy fails.

H3: final collapse requires top-1 amplification beyond the step-0 offset.
Supported if: common-aware initialization, cancellation, or position ablation balances step 0 but final max-load remains seed-dependent.
Weakened if: offset cancellation alone reliably solves final collapse.

H4: fixed routed position / positional embedding is a causal source of the step-0 common component.
Supported if: zeroing only the routed-position embedding sharply lowers common ratio and step-0 max-load.
Weakened if: common ratio and step-0 load remain high after routed-position ablation.

## 4. Mathematical Model
Objects: $h_f$ is the hidden centroid for feature $f$ at the routed position; $c$ is the mean hidden centroid; $r_f$ is the feature residual; $w_e$ is router row $e$.

Core decomposition:

$$
h_f = c + r_f
$$

Mechanism relation:

$$
z_{f,e}=w_e^T h_f = a_e + b_{f,e}, \quad a_e=w_e^T c,\quad b_{f,e}=w_e^T r_f
$$

Observable metrics: common-score argmax agreement, common ratio, cosine with routed-position embedding, step-0 max-load, logit-cancel max-load, final max-load, collapse rate, load entropy, and target accuracy.

Falsifier: if common-score argmax does not predict step-0 routing, or if common-offset cancellation fails to reduce early load, the common-offset hypothesis is too weak.

## 5. Minimal Tests

Experiment: P0-P2 common-source and common-score audit.
Question: does the shared hidden component explain step-0 dominant expert selection?
Intervention: compare full hidden routing with residual or logit common-offset cancellation.
Primary metric: common-score argmax agreement and step-0 max-load reduction.
Supports: H1/H2 if agreement is 1.0 and load approaches balanced routing.
Weakens: H1/H2 if agreement is near 0.25 or load does not change.

Experiment: P3-P5 offset-control and common-aware initialization.
Question: does controlling the common offset reduce final collapse?
Intervention: logit cancellation, common-orthogonal initialization, residual-subspace initialization, and stable common-subtraction variants.
Primary metric: final max-load and collapse rate under high target accuracy.
Supports: H3 if early load improves but final load remains seed-dependent.
Weakens: H3 if offset control alone reliably prevents final collapse.

Experiment: P7 position / template source ablation.
Question: is fixed routed position or positional embedding a causal source of the common component?
Intervention: zero all position embeddings at step 0, zero only routed-position embedding at step 0, shuffle position vectors, train with frozen zero position embeddings, and train/evaluate with random logical feature positions.
Primary metric: common ratio, step-0 max-load, final max-load, target accuracy, and seed-level route heatmaps.
Supports: H4 if zeroing routed position sharply lowers common ratio and step-0 max-load while no-position training preserves accuracy.
Weakens: H4 if position ablation leaves common ratio and step-0 load unchanged.

Experiment: P8 no-position slot-init and inhibition supplement.
Question: after excluding absolute positional embedding throughout training, can slot-init or inhibition produce slot/feature-level routing structure?
Intervention: zero and freeze `pos_emb.weight` from initialization; compare random vs slot-init and no-inhibition vs true token-conditioned inhibition under dot-product and cosine routers.
Primary metric: seed-level `route_slot_nmi_feature_eval`, `route_feature_key_nmi`, expert max-load, target accuracy, and slot x expert heatmaps.
Supports: slot-init as a viable route-structure control if slot NMI is high, load is non-collapsed, and accuracy is high across seeds.
Weakens: inhibition as an anti-collapse path if inhibition-only or slot-init-plus-inhibition routes concentrate into a dominant expert.

## 6. Falsifiable Outcomes

Supported: common-score argmax predicts step-0 dominant expert; common-offset cancellation reduces step-0 load; routed-position ablation sharply reduces common ratio and step-0 load.

Weakened: data or init bug explains the load; common-offset cancellation has no effect; routed-position ablation leaves common ratio and step-0 load unchanged.

Insufficient evidence: only CPU-shortened runs exist, early hidden states are missing, target accuracy fails, or figures average away seed-level collapse.

## 7. Current Evidence

Observation: P1/P2 show common-score argmax agreement is 1.0 across repeated and distributed-complex patterns, versus a random baseline of 0.25; dot-product logit cancellation lowers step-0 max-load from about 0.62-0.63 to about 0.28-0.29.
Interpretation: $w_e^T c$ is a strong explanation for step-0 dominant expert selection.
Boundary: this is a mechanism diagnostic, not a full training solution.

Observation: P3/P4/P5 reduce hard collapse in several variants, but final training remains seed-dependent; P5B logit cancellation avoids hard collapse in tested shortened runs with final max-load around 0.62-0.67.
Interpretation: controlling the common offset helps but does not fully stop top-1 re-concentration.
Boundary: P3 was CPU-shortened, and P4/P5 were not full 4-card verification.

Observation: the 4GPU position-source ablation shows zeroing only the routed-position embedding lowers step-0 common ratio from about 0.51 to about 0.045 and lowers step-0 max-load from about 0.62 to about 0.33-0.36. Training with frozen zero position embeddings keeps accuracy near 0.998 and lowers final max-load relative to baseline in both patterns.
Interpretation: fixed routed position / positional embedding is a major causal source of the step-0 common component, and the toy target rule does not require absolute position embeddings for high accuracy.
Boundary: position removal does not fully solve final collapse; distributed-complex no-position final max-load remains about 0.744, and random feature position still collapses in the repeated pattern.

Observation: the no-position slot-init/inhibition supplement completes 24/24 runs on 4GPU. `S0-cos` reaches slot NMI 0.720-0.781 across three seeds with four active experts and target accuracy 0.991-0.999. Inhibition-only conditions collapse under both dot and cosine routers, with mean final max-load about 0.91-0.92 and slot NMI about 0.07-0.08.
Interpretation: after position removal, cosine slot-init is the strongest current positive control for slot-level route structure, but true token-conditioned inhibition still amplifies selected-expert lock-in rather than creating specialization.
Boundary: the supported positive result is slot-level route structure, not exact `(slot, B_i)` feature-level or functional expert specialization; exact feature-key NMI remains modest.

## 8. Claim Boundary And Next Decision

Can claim: in the tested uniform toy setting, common-offset is the best current explanation for step-0 collapse, and fixed routed position / positional embedding is now causally implicated as a major source of that common component.

Cannot claim: position embedding is the only common-source mechanism, collapse is solved, load balance equals specialization, selected experts are utility-wrong, or the mechanism transfers directly to compositional or real data.

Next decision: use no-position `S0-cos` as the positive route-structure control, and only revisit inhibition after defining an explicit lock-in fix or a different inhibition target.
