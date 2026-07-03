---
anchor_id: A06_10_real_dclm_proxy_feature_operationalization
parent_node: rq.real_data_feature_specialization.proxy_definition
status: supported_with_boundary
created: 2026-06-22
canonical_language: en
---

# A06_10 Real-DCLM Proxy Feature Operationalization Anchor

## 0. Thinking Card
父问题：从 synthetic feature specialization 进入真实 DCLM 时，必须先定义可评估的 feature proxy，不能直接用 load 当成功指标。
当前子问题：真实 DCLM route-position hidden states 是否存在稳定、可复现、非纯 token-frequency 的无标签 proxy clusters？
当前判断：支持，但有边界。真实 DCLM hidden geometry 存在稳定 proxy；step10 后期层最强，step0 后期层较弱。
关键证据：4 卡 A06_10 full01 中 residual step10 mean stability NMI = 0.5211，random NMI = 0.0002；layer5 step10 residual NMI = 0.6501；frequency/position NMI 明显低于稳定性指标。
最危险边界：raw 和 residual k-means 几乎相同，因此不能声称 common-centering 是发现 cluster 的关键；也不能声称 proxy 已经语义化或可线性路由。
下一步决策：进入 A06_11，但必须把 raw-input routing 与 centered-input diagnostic routing 分开测。

Question: Can real DCLM router-input residual hidden states produce stable label-free proxy features that are not explained mainly by token frequency, token id, position, or batch split?
Physical prior: real text has repeated latent factors, but their labels are missing; stable residual clusters are the minimum measurable proxy before real-data gating initialization.
Core model: $h_i=c_b+r_i$, discover $q_i=\operatorname{Cluster}(r_i)$ on calibration tokens, and test $q_i$ stability and nuisance dependence on held-out tokens.
Model term being tested: label-free proxy-feature recoverability in real DCLM residual hidden states.
Primary metric: held-out cluster stability, measured by split-to-split assignment agreement after center matching; nuisance metrics are guards.
Falsifier: clusters are unstable across splits/checkpoints or mostly explained by token id/frequency/position.
Can claim: a usable real-data proxy feature exists for the next gating-initialization test.
Cannot claim: semantic feature discovery, expert utility, or training stability.
Next decision: use the proxy clusters in A06_11, or revise the proxy if the audit fails.

## 1. Problem Definition

Parent problem: real-data expert specialization requires a measurable feature axis before router initialization can be judged.
Sharper subproblem: define a label-free proxy feature on DCLM hidden states that is stable enough to evaluate routing.
Decision question: are residual hidden-state clusters stable and sufficiently independent of obvious nuisance variables?
Not in scope: semantic labeling, expert utility, deployable router method, or full training intervention.

## 2. Physical Priors

P1: Repeated real-text latent factors should leave repeated structure in router-input residual states.
Meaning: after subtracting a batch/common component, tokens with similar local function may occupy nearby hidden directions.
Could be wrong if: residual geometry is dominated by token identity, frequency, position, or random batch noise.

P2: A valid proxy must be stable before it is useful.
Meaning: calibration-derived centers should assign held-out batches similarly after matching centers.
Could be wrong if: clusters rotate across batches/checkpoints or depend on the exact audit sample.

P3: Load balance is a nuisance guard, not the target.
Meaning: balanced clusters are useful only if they are stable and not purely frequency/position buckets.
Could be wrong if: downstream utility later proves load-only grouping is enough; that is not the current claim.

## 3. Falsifiable Hypotheses

H1: Real DCLM residual states contain stable proxy clusters.
Supported if: calibration centers give high held-out assignment stability across independent DCLM splits and neighboring checkpoints.
Weakened if: center matching is unstable or held-out agreement is near random.

H2: Proxy clusters are not reducible to token frequency, token id, or position.
Supported if: cluster labels have bounded mutual information with nuisance variables and remain stable after removing top-frequency tokens.
Weakened if: clusters are mostly token-id/frequency buckets or position buckets.

H3: Common-centering is needed before proxy discovery.
Supported if: raw-hidden clusters are less stable or more nuisance-aligned than residual clusters.
Weakened if: raw clusters are equally stable and less nuisance-driven.

## 4. Mathematical Model

Objects: token index $i$, router-input hidden state $h_i$, batch/common vector $c_b$, residual $r_i=h_i-c_b$, discovered proxy cluster $q_i$, nuisance variables $n_i$ including token id, token frequency bin, absolute position, and layer.

Core decomposition:
$$
h_i=c_b+r_i.
$$

Proxy discovery:
$$
\{\nu_k\}_{k=1}^{K}=\operatorname{Cluster}(\{r_i:i\in C\}),\qquad
q_i=\arg\max_k r_i^\top \nu_k.
$$

Observable metrics: split stability after center matching, assignment entropy, cluster load, $NMI(q,n)$ for nuisance variables, stability after top-frequency-token removal.
Falsifier: high cluster load balance with low split stability or high nuisance dependence.

## 5. Computational Realization

- Input: random-initialized Qwen-style DCLM MoE checkpoints from A06_02-compatible code path.
- Audit layers: late layers 3--5 plus one early layer guard.
- Data: two disjoint DCLM audit splits, same tokenization and sequence length as A06_02.
- Conditions: raw hidden clustering, common-centered residual clustering, whitened residual clustering, random projection control.
- Profiling: center occupancy, split matching, nuisance NMI, top-frequency removal audit, representative token/context examples per cluster.
- Artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/proxy_cluster_summary.csv`, `figures/proxy_stability_by_condition.png`.

## 6. Minimal Falsification Tests

Test 1: split stability.
Question: do discovered centers transfer to held-out DCLM splits?
Primary metric: matched split-to-split assignment agreement or NMI.
Supports: residual clusters are stable above random and above raw / whitened controls.
Weakens: no condition is stable.

Test 2: nuisance audit.
Question: are clusters mostly token id, frequency, or position?
Primary metric: $NMI(q,n)$ and stability after removing top-frequency tokens.
Supports: nuisance NMI is bounded and stability remains.
Weakens: proxy is mostly nuisance.

## 7. Current Evidence

- A06_08 synthetic result: route-position residual clustering can recover artificial feature labels when labels exist only for evaluation.
- A06_07 synthetic result: load-only controls are misleading.
- A06_02 real DCLM result: common directions are batch-stable at fixed checkpoints, but training-specific; real-data proxy audits must track checkpoint/layer.
- A06_01 real DCLM result: expert-spectrum linear initialization failed partly because a reliable real feature proxy and linear bridge were missing.
- A06_10 full01 result: real-DCLM proxy clusters are stable above random. Residual mean held-out assignment NMI is 0.2565 at step 0 and 0.5211 at step 10; random NMI is about 0.0002. Step-10 residual layer-5 NMI reaches 0.6501. Frequency and position NMI are much lower than proxy stability, and top-frequency-token removal preserves the signal.
- A06_10 boundary: raw and residual k-means are effectively identical, so the result supports stable hidden geometry but weakens the claim that common-centering is needed for proxy discovery.

## 8. Claim Boundary And Next Decision

Can claim: a stable label-free real-data proxy feature is available for the next router-initialization experiment, especially at step 10 late layers.
Cannot claim: semantic feature discovery, causal expert specialization, training preservation, deployable routing, or that common-centering improves k-means proxy discovery.
Next decision: run A06_11 proxy-center router initialization with both raw-input routing and centered-input diagnostic routing.
