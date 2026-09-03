# 05_01 Inhibition And Early Lock-In Anchor


## 1. Problem Definition

Parent problem: a useful MoE expert partition must be stable, non-collapsed, feature-aligned, and eventually utility-relevant; same-feature route consistency alone is a weak signal.

Sharper subproblem: inhibition should prevent one expert from absorbing unrelated routed states while allowing stable feature-to-expert assignment.

Decision question: can the current inhibition direction produce non-collapsed, feature-structured routing, or does it mainly harden early top-1 lock-in?

Not in scope: real corpus behavior, Zipfian frequency, new router architecture, or claims that routed experts are causally utility-best.

## 2. Physical Priors
P1: hard top-1 selection creates a self-reinforcing training loop.
Meaning: the selected expert receives the routed token update, and the next routing decision can become more confident for the same expert.
Could be wrong if: early load imbalance repeatedly disappears without an explicit balancing or correction pressure.

P2: route consistency can be a false positive.
Meaning: a single-expert collapse gives high $\max_e P(route=e \mid f)$ for every feature.
Could be wrong if: high consistency always co-occurs with multi-expert load and interpretable feature composition.

P3: inhibition is useful only if it changes competition over token states, not only router-row geometry.
Meaning: separating router rows is not enough unless routed states become non-collapsed and feature-structured.
Could be wrong if: row separation alone reliably predicts non-collapsed feature assignment.

## 3. Hypothesis

H1: center separation is insufficient.
Supported if: router rows become geometrically separated but final feature routing remains collapsed or seed-unstable.
Weakened if: center separation alone robustly improves non-collapsed feature composition under matched seeds.

H2: token-conditioned inhibition is the right mechanism class but unsafe in the current form.
Supported if: it increases same-feature consistency while also amplifying dominant-expert lock-in or collapse.
Weakened if: it consistently improves same-feature stability, load balance, and different-feature composition.

H3: collapse in the original uniform setting is mostly early-geometry dominated.
Supported if: final collapsed runs already point to the final dominant expert at step 0 to early checkpoints, and margins grow during training.
Weakened if: early routing is balanced and the final dominant expert appears only late.

## 4. Mathematical Model
Objects: $h_f(t)$ is the hidden centroid for operational feature $f$ at the routed pre-target position; $w_e(t)$ is router row $e$; $e^+(f,t)=\arg\max_e w_e(t)^T h_f(t)$.

Core decomposition:

$$
h_f(t) = c(t) + r_f(t), \quad c(t)=\frac{1}{|F|}\sum_f h_f(t)
$$

Mechanism relation:

$$
z_{f,e}(t)=w_e(t)^T h_f(t)=w_e(t)^T c(t)+w_e(t)^T r_f(t)
$$

Observable metrics: max-load fraction, normalized load entropy, active experts, feature-route assignment, top-1 margin, cosine between $w_e(t)$ and $c(t)$, and target accuracy.

Falsifier: if collapsed runs are not predictable from early dominant expert, early cosine, or margin growth, the early-lock-in account is insufficient.

## 5. Minimal Tests

Experiment: A05_01_geometric_inhibition_center_separation.
Question: does router-row separation alone stabilize routing?
Intervention: add center-separation pressure or slot-stable initialization.
Primary metric: non-collapsed route load plus route-feature structure, not consistency alone.
Supports: H1 if geometry improves but routing remains unreliable.
Weakens: H1 if center separation robustly produces non-collapsed feature composition.

Experiment: A05_01_true_token_conditioned_inhibition_replay.
Question: does token-conditioned inhibition improve useful routing or amplify current top-1 choices?
Intervention: add selected-expert attraction and competitor repulsion during NTP.
Primary metric: max-load and different-feature composition under high target accuracy.
Supports: H2 if consistency rises but collapse persists or increases.
Weakens: H2 if inhibition improves load and composition across seeds.

Experiment: A05_01_uniform_feature_collapse_mechanism_audit.
Question: is collapse present at initialization, early training, or late training?
Intervention: no broad new dataset; audit checkpoints and replay missing early states when necessary.
Primary metric: route-load and top-1 agreement timeline by seed and condition.
Supports: H3 if final collapsed runs are already biased toward the final dominant expert early.
Weakens: H3 if collapse emerges late from balanced early routing.

## 6. Falsifiable Outcomes

Supported: center separation fails as a sufficient mechanism; token-conditioned inhibition is lock-in prone; final collapsed seeds are early-geometry dominated.

Weakened: inhibition produces stable non-collapsed composition; final dominant experts are not visible early; common-direction alignment does not distinguish collapsed and non-collapsed runs.

Insufficient evidence: early checkpoints are missing and cannot be replayed; target accuracy fails; heatmaps are only aggregate averages and hide seed-level collapse.

## 7. Current Evidence

Observation: A05_01 center-separation and stability runs show that high same-feature consistency can occur with collapse or arbitrary load concentration.
Interpretation: consistency is not specialization.
Boundary: this does not reject all inhibition mechanisms.

Observation: A05_01 uniform collapse audit found 9 final-collapsed condition-seeds; all 9 had the same final dominant expert already at step 0, and all 9 matched again at steps 50 and 100.
Interpretation: final collapse is better described as early-geometry dominated plus training amplification than as late drift.
Boundary: early hidden/router states at steps 10, 20, and 50 came from same-config diagnostic replay when original early states were unavailable.

Observation: in final-collapsed runs, the final expert's common-direction cosine rose from 0.148 at step 0 to 0.873 at final, while residual alignment stayed small.
Interpretation: the selected expert behaves more like an attractor for the shared hidden direction than a feature-residual separator.
Boundary: forced-routing utility was not computed in this A05_01 audit, so utility mismatch cannot be claimed here.

## 8. Claim Boundary And Next Decision

Can claim: ordinary top-1 plus the tested inhibition losses can produce stable-looking routes without reliable non-collapsed specialization; the original uniform collapse audit supports early-geometry dominated collapse with a common-direction clue.

Cannot claim: collapse is solved, common direction is the only cause, selected experts are utility-wrong, or these toy results transfer directly to real language data.

Next decision: run a minimal anti-lock-in test on the original uniform setting, prioritizing router-input common-direction control, auxiliary load-balance warmup, or delayed/softened top-1 routing before returning to route-utility binding.
