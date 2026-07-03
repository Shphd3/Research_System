---
anchor_id: A06_11_real_dclm_proxy_center_router_initialization
parent_node: rq.real_data_feature_specialization.gating_initialization
status: supported_with_boundary
created: 2026-06-22
canonical_language: en
---

# A06_11 Real-DCLM Proxy-Center Router Initialization Anchor

## 0. Thinking Card
父问题：真实数据上能否构造一个比 random init 更好的 gating initialization，使 router 先进入 proxy-feature 分区而不是 common/load collapse？
当前子问题：若 A06_10 找到稳定 proxy clusters，用这些 clusters 的 residual centers 初始化 router，是否能在 step 0 得到稳定、非 common-dominated 的 proxy routing？
当前判断：支持，但有边界。proxy center 可以转成线性 router；真实 raw-input 下最强的是 raw-center rows，不是 residual-center rows。
关键证据：A06_11 full01 中 step0 raw-center raw-input proxy_route_NMI = 0.7449，random = 0.0343；step10 raw-center raw-input = 0.8811；label-shuffled guard 约 0。
最危险边界：residual-center 在 centered-input 诊断中很强，但 raw-input 会被 common bias 压低；因此不能把 residual-center 当成已解决的初始化。
下一步决策：进入 A06_12，用 raw-center equal-norm 作为主初始化，residual-center 作为 common-bias 对照。

Question: Can A06_10 proxy centers initialize a linear top-1 DCLM router whose step-0 assignments preserve the proxy partition better than random init without common-driven concentration?
Physical prior: if proxy clusters are geometrically real, equal-norm residual centers should be linearly readable by the router at initialization.
Core model: $w_e=\alpha\nu_e/\|\nu_e\|$ from proxy centers $\nu_e$, route $a_i=\arg\max_e w_e^\top h_i$, and compare $NMI(q_i,a_i)$.
Model term being tested: proxy-center-to-linear-router bridge at step 0.
Primary metric: held-out `proxy_route_NMI = NMI(proxy_cluster, routed_expert)` with load and common-margin guards.
Falsifier: high load balance but low proxy_route_NMI, or high proxy_route_NMI only through common/frequency concentration.
Can claim: proxy centers can be converted into a valid step-0 linear router initialization.
Cannot claim: training preservation, semantic specialization, or expert utility.
Next decision: proceed to A06_12 training preservation or A06_13 bridge failure decomposition.

## 1. Problem Definition

Parent problem: real DCLM gating initialization needs a measurable proxy partition and a router that can implement it.
Sharper subproblem: convert proxy centers into linear top-1 router rows and test step-0 routing.
Decision question: does proxy-center initialization produce better held-out proxy routing than random and common-filtered baselines?
Not in scope: training dynamics, expert utility, top-2 routing, real semantic labels.

## 2. Physical Priors

P1: Stable residual clusters should have linearly readable centers.
Meaning: cluster means should form directions that separate proxy groups in router-input space.
Could be wrong if: the proxy partition is nonlinear or has low margin under a linear router.

P2: Equal-norm centers are required to avoid row-norm load artifacts.
Meaning: A06_03 showed row-norm variation can create load imbalance unrelated to specialization.
Could be wrong if: norm carries useful compatibility signal; this is a later utility question.

P3: Common-margin must remain a guard.
Meaning: A06_02 showed real DCLM training can amplify common channels quickly.
Could be wrong if: proxy routing succeeds even with a high common margin and remains stable in A06_12.

## 3. Falsifiable Hypotheses

H1: proxy-center init improves proxy_route_NMI over random.
Supported if: held-out proxy_route_NMI improves substantially over random with acceptable load and active experts.
Weakened if: proxy_route_NMI is random-like.

H2: residual centers outperform raw centers.
Supported if: residual-center rows have lower common-margin and higher proxy_route_NMI.
Weakened if: raw centers match or outperform residual centers without more common concentration.

H3: the linear bridge is adequate.
Supported if: proxy assignment is well approximated by linear top-1 rows with positive margins.
Weakened if: oracle proxy assignment is stable but linear router agreement is low.

## 4. Mathematical Model

Objects: proxy label $q_i$ from A06_10, residual center $\nu_k$, router row $w_e$, assignment $a_i$, common vector $c$, residual $r_i$.

Initialization:
$$
w_{\pi(k)}=\alpha\frac{\nu_k}{\|\nu_k\|}.
$$

Routing:
$$
a_i=\arg\max_e w_e^\top h_i.
$$

Decision metric:
$$
NMI(q_i,a_i)
$$
with load $L$, active experts, and common-margin guards.

## 5. Computational Realization

- Use A06_10 selected proxy construction and DCLM audit splits.
- Conditions: random Gaussian, equal-norm random, raw proxy center, residual proxy center, whitened proxy center, A06_01 common-filtered spectrum reference.
- Evaluate step-0 only.
- Save center norms, center pairwise cosines, proxy route heatmaps, common/residual margin decomposition.

## 6. Minimal Falsification Tests

Test: step-0 proxy-center initialization.
Question: does proxy-center init route held-out tokens by proxy cluster?
Primary metric: held-out proxy_route_NMI.
Supports: proxy_route_NMI high and not load-only.
Weakens: low NMI, severe common concentration, or empty experts.
Insufficient: A06_10 proxy failed, labels leak from evaluation, or no random/common baselines.

## 7. Current Evidence

- A06_08 synthetic pseudo centers transfer to perfect synthetic routing.
- A06_09 synthetic pseudo init preserves routing under a simple training objective.
- A06_01 real expert-spectrum linear bridge has low oracle-to-linear agreement, so bridge adequacy must be tested explicitly.
- A06_10 supports a stable real-data proxy, especially at step 10 late layers, but weakens the claim that common-centering is needed for k-means proxy discovery.
- A06_11 full01 supports proxy-to-linear routing. Step-0 raw-center raw-input proxy_route_NMI is 0.7449 versus random 0.0343; step-10 raw-center raw-input proxy_route_NMI is 0.8811. Residual-center centered-input routing is strong, but residual-center raw-input routing is weaker due to common bias.

## 8. Claim Boundary And Next Decision

Can claim: real DCLM proxy centers can initialize a valid linear top-1 router, with raw-center rows as the best actual raw-input bridge in this setup.
Cannot claim: training stability, semantic meaning, expert utility, final router design, or residual-center robustness to common bias.
Next decision: run A06_12 training preservation with raw-center equal-norm as the main initialization and residual-center equal-norm as a common-bias comparison.
