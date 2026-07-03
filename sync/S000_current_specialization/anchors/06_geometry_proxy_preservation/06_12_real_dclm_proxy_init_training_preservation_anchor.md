---
anchor_id: A06_12_real_dclm_proxy_init_training_preservation
parent_node: rq.real_data_feature_specialization.training_dynamics
status: weakened_training_feedback_failure
created: 2026-06-22
canonical_language: en
---

# A06_12 Real-DCLM Proxy-Init Training Preservation Anchor

## 0. Thinking Card
父问题：真实 DCLM 上好的 step-0 proxy routing 是否会被 ordinary top-1 LM training 保持？
当前子问题：A06_11 若成功，proxy-center init 是否降低 step-10 common/load amplification，并保持 proxy_route_NMI？
当前判断：不支持保持假设。raw-center proxy init 在 step0 很强，但普通 DCLM 训练到 step5/10 迅速坍缩到 random-like routing。
关键证据：A06_12 full01 中 raw_center proxy_route_NMI 从 step0 0.7549 降到 step5 0.0410、step10 0.0131；random step10 为 0.0047；LM loss 与 random 基本相同。
最危险边界：这不是说 proxy 没有用，而是说当前 next-token objective 不会自动保护 proxy partition。
下一步决策：进入 A06_13 failure decomposition；暂不进入 A06_14 utility binding。

Question: Does real-DCLM proxy-center initialization preserve proxy routing through early top-1 LM training while controlling the A06_02 common/load spike?
Physical prior: a better initial partition may change the early training basin, but DCLM hidden-producer drift may override it.
Core model: track $NMI(q_i,a_i(t))$, load $L_t$, and common-margin $\Delta_t$ over checkpoints.
Model term being tested: training-time preservation of real-data proxy routing.
Primary metric: final or step-10 proxy_route_NMI with LM loss and load/common guards.
Falsifier: high step-0 proxy_route_NMI collapses by step 10/50 while LM loss remains acceptable.
Can claim: whether proxy-center initialization changes early DCLM top-1 training dynamics.
Cannot claim: final long training, semantic specialization, or expert utility.
Next decision: utility binding if preserved; failure decomposition if not.

## 1. Problem Definition

Parent problem: real-data specialization requires both good initialization and training preservation.
Sharper subproblem: test whether proxy-center initialization survives the early DCLM amplification window.
Decision question: does proxy-center init preserve proxy routing better than random and reduce step-10 concentration?
Not in scope: full pretraining, top-2 routing, expert utility, or semantic labels.

## 2. Physical Priors

P1: Good initialization may define a basin.
Meaning: A06_09 synthetic pseudo init stayed at NMI 1.0 under a simple training objective.
Could be wrong if: real DCLM gradients and hidden drift overwhelm the initial partition.

P2: Step-10 is the critical early window.
Meaning: A06_02 showed late-layer common/load concentration spikes rapidly around step 10.
Could be wrong if: proxy init changes later dynamics only after step 10.

P3: LM loss is a constraint, not the target.
Meaning: a router can preserve a proxy partition while harming prediction, or learn loss while losing proxy routing.
Could be wrong if: proxy partition is irrelevant to loss and should not be preserved; that is handled in A06_14.

## 3. Falsifiable Hypotheses

H1: proxy init preserves proxy_route_NMI through early training.
Supported if: proxy_route_NMI remains high at steps 10/50 compared with random.
Weakened if: it collapses to random-like NMI.

H2: proxy init reduces common/load amplification.
Supported if: step-10 common_margin_delta and raw_max_load are lower than random.
Weakened if: common/load spike is equal or worse than random.

H3: preservation does not harm LM loss.
Supported if: LM loss is within a small tolerance of random baseline.
Weakened if: preservation succeeds only by damaging prediction.

## 4. Mathematical Model

Objects: proxy label $q_i$, assignment $a_i(t)$, router row $W_t$, hidden state $H_t$, common vector $c_t$, LM loss $\ell_t$.

Trajectory:
$$
S_t=NMI(q_i,a_i(t)),\qquad L_t=m\max_e|p_{t,e}-1/m|.
$$

Common margin:
$$
M_t=\operatorname{margin}(W_t c_t).
$$

Falsifier:
$$
S_0\text{ high},\quad S_{10}\text{ low},\quad \ell_{10}\text{ acceptable}.
$$

## 5. Computational Realization

- Train DCLM top-1 MoE for 0--300 steps with random, equal-norm random, A06_11 proxy-center init, and a label-shuffled proxy guard.
- Checkpoints: 0, 1, 2, 3, 5, 10, 20, 50, 100, 300.
- Metrics: proxy_route_NMI, raw/centered load, active experts, common/residual margin, LM loss, exact gate-input replay for selected layers.
- Artifacts: trajectories, heatmaps, cross-checkpoint replay, stage audit.

## 6. Minimal Falsification Tests

Test: early training preservation.
Question: does proxy-center init survive the A06_02 early amplification window?
Primary metric: proxy_route_NMI at step 10 and 50.
Supports: NMI preserved and loss acceptable.
Weakens: NMI collapse or worse common/load spike.
Insufficient: A06_11 step-0 failed, no exact gate audit, or no loss guard.

## 7. Current Evidence

- A06_09 supports preservation in synthetic route-position target training.
- A06_02 shows real DCLM hidden-producing path can rapidly override random step-0 routing.
- A06_01 shows common-filtered expert-spectrum init did not reduce step-10 concentration.
- A06_11 full01 supports the step-0 bridge: raw-center raw-input proxy_route_NMI is 0.7449.
- A06_12 full01 weakens training preservation: raw-center proxy_route_NMI drops from 0.7549 at step 0 to 0.0410 at step 5 and 0.0131 at step 10, while LM loss remains comparable to random.

## 8. Claim Boundary And Next Decision

Can claim: proxy-center initialization does not survive ordinary early real DCLM training in this setup.
Cannot claim: long-run pretraining, semantic specialization, expert utility absence, deployable routing, or impossibility of preservation with a modified objective.
Next decision: run A06_13 failure decomposition and park A06_14/A06_15 until preservation is restored.
