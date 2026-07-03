---
anchor_id: A06_13_real_dclm_proxy_init_failure_decomposition
parent_node: rq.real_data_feature_specialization.failure_decomposition
status: supported_training_feedback_bottleneck
created: 2026-06-22
canonical_language: en
---

# A06_13 Real-DCLM Proxy-Init Failure Decomposition Anchor

## 0. Thinking Card
父问题：如果真实数据 proxy init 失败，失败发生在 proxy 定义、linear bridge、还是训练反馈？
当前子问题：把 A06_11/A06_12 的失败拆成可观测 bottleneck，而不是直接换方法。
当前判断：支持。第一失败点是训练反馈覆盖 step0 proxy route，不是 proxy 发现失败，也不是 step0 线性桥接失败。
关键证据：A06_10 proxy discovery 通过；A06_11 raw-center step0 proxy_route_NMI = 0.7449；A06_12 raw-center step10 NMI = 0.0131，loss 与 random 差值仅 0.0032。
最危险边界：这只定位当前 pipeline 的失败点，不说明 expert utility 不存在，也不说明 anti-collapse 方法无效。
下一步决策：暂停 A06_14/A06_15，优先设计 preservation/anti-feedback anchor。

Question: When real-DCLM proxy-center initialization fails, is the bottleneck proxy instability, linear-router bridge mismatch, common/nuisance capture, or early hidden-feedback override?
Physical prior: a multi-stage pipeline can fail locally; changing the final method before locating the failed stage destroys research information.
Core model: proxy discovery $q$, linear bridge $\hat a_0$, training trajectory $\hat a_t$; decompose failure into $q$ instability, $q\to \hat a_0$ mismatch, and $\hat a_0\to \hat a_t$ drift.
Model term being tested: stage-local bottleneck in the real-data proxy initialization pipeline.
Primary metric: the first stage where the pass criterion fails.
Falsifier: no stage-local metric explains the final failure.
Can claim: the local bottleneck for the failed real-data gating-initialization attempt.
Cannot claim: final solution or broad impossibility of real-data feature discovery.
Next decision: revise proxy, revise bridge, or test anti-feedback intervention.

## 1. Problem Definition

Parent problem: real-data gating initialization is a pipeline, not a single score.
Sharper subproblem: explain failure of A06_11/A06_12 without overclaiming.
Decision question: which stage first violates its contract?
Not in scope: proposing a new method before bottleneck localization.

## 2. Physical Priors

P1: Proxy failure and router failure are different.
Meaning: unstable clusters cannot support any router, while stable clusters may still be nonlinear.
Could be wrong if: proxy and linear bridge fail indistinguishably under all audits.

P2: Linear bridge mismatch is plausible.
Meaning: A06_01 showed oracle-to-linear agreement can be low even when oracle assignment is balanced.
Could be wrong if: linear bridge matches proxy at step 0 but training later collapses.

P3: Training feedback can override initialization.
Meaning: A06_02 showed hidden drift and gate-hidden interaction can quickly concentrate routes.
Could be wrong if: collapse is already present at step 0.

## 3. Falsifiable Hypotheses

H1: proxy instability is the bottleneck.
Supported if: A06_10 split stability fails or nuisance explains clusters.
Weakened if: proxy is stable and nuisance-bounded.

H2: linear bridge is the bottleneck.
Supported if: proxy is stable but step-0 proxy_route_NMI / margin is low.
Weakened if: step-0 proxy routing is high.

H3: training feedback is the bottleneck.
Supported if: step-0 routing is high but step-10/50 collapses with hidden/replay evidence.
Weakened if: collapse happens before training.

## 4. Mathematical Model

Stages:
$$
h_i\to q_i,\qquad q_i\to a_i(0),\qquad a_i(0)\to a_i(t).
$$

Stage metrics:
$$
S_{proxy}=Stability(q),\quad S_{bridge}=NMI(q,a(0)),\quad S_{train}=NMI(q,a(t)).
$$

Bottleneck rule: the first stage with metric below threshold defines the next decision.

## 5. Computational Realization

- Reuse A06_10/A06_11/A06_12 artifacts.
- Add diagnostics only for the failed stage: center margin, linear classifier upper bound, prototype router oracle, nuisance ablations, replay freeze split.
- Save a bottleneck table with one row per stage and explicit pass/fail/unclear status.

## 6. Minimal Falsification Tests

Test: stage contract audit.
Question: where does the pipeline first fail?
Primary metric: first failed stage contract.
Supports: a single bottleneck is localized.
Weakens: multiple stages remain ambiguous.
Insufficient: missing A06_10/A06_11/A06_12 artifacts.

## 7. Current Evidence

- A06_01 suggests linear bridge mismatch is plausible.
- A06_02 suggests training feedback override is plausible.
- A06_08/A06_09 show synthetic pipeline succeeds, so real-data failure should be decomposed rather than assumed.
- A06_13 full01 localizes the bottleneck: proxy discovery passes with boundary, raw-center linear bridge passes, and training preservation is the first failed contract.

## 8. Claim Boundary And Next Decision

Can claim: the localized bottleneck for the failed real-data proxy-init pipeline is training feedback override.
Cannot claim: broad impossibility, final method, or expert utility absence.
Next decision: test anti-feedback / preservation interventions before utility binding.
