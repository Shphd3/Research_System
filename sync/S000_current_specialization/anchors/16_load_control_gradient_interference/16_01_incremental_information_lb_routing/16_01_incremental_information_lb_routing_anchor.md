# A16_01 Incremental-Information Routing Under Differentiable Load Balance


## 1. Problem Definition

A16 asks how an MoE can keep sparse-expert load usable without slowing language-model learning. A16_00 established that the effect of a differentiable load-balancing objective is stage-dependent; it did not select a useful Router representation. A15 separately showed that fixed covariance bands can change dispatch without becoming certified functional coordinates. The present parent Anchor therefore tests an operational intervention rather than another band assignment.

For layer $\ell$, let $n_\ell^{old}$ be the normalized token state before the attention write is added, $n_\ell^{new}$ the actual post-attention normalized state visible to the Router, and $u_\ell=n_\ell^{new}-n_\ell^{old}$ the **same-layer visible increment**. An **innovation branch** is a low-rank residual logit path computed from $u_\ell$ while the native full-state Gate remains intact.

The one decision question is: **under identical four-layer MoE initialization, DCLM order, truly differentiable Switch load balance, optimizer, and a 30B-token endpoint, does an explicit innovation branch improve held-out next-token NLL; and, when an independently certified frozen direction exists, is its gain larger than a dimension-matched Haar direction?**

Two realizations are registered. Trainable-Innovation is the engineering realization and learns its low-rank projection end to end. Certified-Innovation is the scientific realization and may start only after a frozen direction passes both a representation certificate and a frozen expert-utility certificate. Native-LB and Haar-Innovation-LB separate ordinary training from extra low-rank capacity. The Anchor does not ask whether the certified semantic target is universal or whether load balance is the only cause of any endpoint difference.

## 2. Physical Priors

1. A residual branch initialized to produce zero logits can expose a candidate input without deleting information or changing the step-0 routing function. This prior is false if the no-op identity fails or the branch perturbs the native path before learning.
2. If the actual increment contains useful expert-selection information that is difficult to isolate inside the full state, a dedicated low-rank path can reduce finite-budget optimization difficulty. This prior is false if Trainable-Innovation does not improve 30B NLL over Native-LB in paired seeds.
3. Direction identity matters only if a direction selected without endpoint NLL outperforms a dimension-, launch-state-, and compute-matched random direction. Otherwise any gain is explained by added capacity, regularization, or a stable side path.

## 3. Falsifiable Hypotheses

- **H1, engineering utility:** a trainable low-rank branch over $u_\ell$ improves 30B held-out NLL over Native-LB in both paired seeds.
- **H2, certified direction identity:** after the same frozen direction has passed E1 representation admission and E2 expert-utility admission, Certified-Innovation improves 30B held-out NLL over both Native-LB and Haar-Innovation in both seeds.
- **Strongest rival:** the complete post-attention state already contains all usable information; any apparent gain comes from extra parameters, delayed branching, regularization, load change, or random low-dimensional conditioning rather than certified direction identity.

An Engineering Pass supports H1 without supporting H2. A Scientific Pass requires H2 and cannot be inferred from H1. Complete valid runs that violate a corresponding two-seed rule are Fail. If no common E1+E2 certificate exists by 10B, the scientific comparison is `INSUFFICIENT_NO_CERTIFICATE`; the pre-submitted Certified/Haar jobs remain dormant Native behavior to 30B and cannot be interpreted as scientific arms.

## 4. Mathematical Model

The actual same-layer objects are

$$
n_\ell^{old}=N_\ell(h_\ell),\qquad
n_\ell^{new}=N_\ell(h_\ell+a_\ell),\qquad
u_\ell=n_\ell^{new}-n_\ell^{old}.
$$

Native-LB uses $g_\ell^{native}=W_\ell n_\ell^{new}$. The engineering branch uses a trainable rank-$k$ factorization,

$$
g_\ell^{eng}=W_\ell n_\ell^{new}+B_\ell A_\ell^\top\operatorname{RMS}(u_\ell),
$$

where $A_\ell\in\mathbb R^{d\times k}$ and $B_\ell\in\mathbb R^{E\times k}$, with $B_\ell=0$ at activation. The certified branch uses a frozen direction and frozen TRAIN statistics,

$$
g_\ell^{cert}=W_\ell n_\ell^{new}+C_\ell P_\ell^\top S_\ell^{-1}(u_\ell-\mu_\ell),
$$

where $P_\ell^\top P_\ell=I$ and $C_\ell=0$ at activation. Haar replaces $P_\ell$ by a fixed same-rank Haar frame and otherwise matches Certified exactly.

All arms optimize

$$
L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{LB,\ell},\qquad
L_{LB,\ell}=8\sum_e\overline p_{\ell,e}f_{\ell,e},
$$

where $\overline p$ is the mean softmax probability and $f$ is the stop-gradient hard top-1 token fraction. The primary observable is the document-paired 30B endpoint contrast $\Delta NLL(A-B)=NLL_A-NLL_B$ in nat/token; negative values favor $A$. It measures predictive quality at fixed tokens, not the causal mediation through expert specialization.

## 5. Computational Realization

Use the verified four-layer, hidden-size-768, eight-sparse-expert plus one-shared-expert, top-1 DCLM MoE. Native-LB and Trainable-Innovation-LB start from common step-0 states in seeds 17 and 29 and train to 30B tokens. The engineering rank is fixed at 56, the maximum rank supported by the registered eight-parent/eight-child conditional-fine construction; the trainable factor is an engineering object and is not called a semantic direction.

At Native checkpoints 2B, 5B, and 10B, apply the frozen [incremental-information method](/daily_research_reports/backup/2026/08/0810/docs/layerwise_incremental_information_routing/README.md). E1 must show that a TRAIN/DEVELOPMENT-built rank-56 direction adds held-out conditional-fine readability beyond the old state and exceeds same-rank Haar and within-parent label permutation. E2 then freezes the model, experts, and direction and requires lower held-out expert-choice regret than old-only and same-rank Haar. The first milestone where both seeds pass at least one common layer is $t^*$; rank is fixed before confirmation and cannot be selected from endpoint results.

All eight jobs start from paired step-0 states. Certified and Haar contain dormant zero-output branches and must remain tensor-identical to Native on model parameters, optimizer state, data cursor, and Router behavior before activation. At $t^*$, the paired dormant jobs load the frozen Certified/Haar frames without changing existing model or optimizer state, activate zero-output heads, and continue to the same 30B total-token endpoint. If no $t^*$ exists by 10B, both remain dormant to 30B and the scientific comparison is insufficient. Online inference uses only the current sample's $u_\ell$; matched double differences are offline direction-learning data, never Router input.

## 6. Minimal Falsification Tests

The decisive evidence is one endpoint NLL metric with two typed comparisons:

1. **Engineering:** Trainable-Innovation minus Native at 30B.
2. **Scientific identity:** Certified minus Haar, protected by Certified minus Native, at 30B.

For a Pass, each seed's point estimate must be negative and its paired-document 95% interval must exclude zero in the same direction. The scientific result additionally requires an eligible $t^*$ and exact Certified/Haar launch matching. A valid complete comparison that misses this rule is Fail; missing LB backward, mismatched step-0 or launch state, data-order divergence, invalid increment reconstruction, missing checkpoint, or incomplete endpoint evaluation is Insufficient.

Hard guards verify $n^{new}=n^{old}+u$, zero-output no-op identity, nonzero finite LB-only Gate gradients at every layer, branch-gradient reachability, exact checkpoint recovery, paired token hashes, and Certified/Haar rank/parameter/FLOP matching. Load, route entropy, branch-logit norm, route flips, and NLL/FLOP explain the result but cannot rescue a failed primary comparison.

## 7. Current Evidence

The endpoint comparison is `NOT RUN`, but execution is active. The corrected immutable implementation passed all four arm-specific 8×5090 smoke contracts: differentiable LB reaches every native Gate, the intended innovation/upstream paths receive gradients, frozen frames do not, all arms preserve step-0/data identity, and checkpoint plus certificate state resumes exactly. All eight 30B jobs were submitted and remained RUNNING with zero retries, finite LM+LB telemetry, and TensorBoard through the registered ten-minute startup audit. These are execution-validity facts only; no milestone supplies an E1+E2 certificate yet and no result establishes that a low-rank same-layer increment improves NLL.

## 8. Claim Boundary And Next Decision

Even an Engineering Pass would support only the practical value of a trainable increment branch under this four-layer, two-seed, 30B, LB-controlled setting. It would not prove that the learned projection represents semantic novelty. A Scientific Pass would additionally show that a pre-admitted direction beats a matched random direction in this setting, but it would not prove universal semantic hierarchy, scale transfer, or that expert specialization is the unique mediator.

The one next decision is to preserve the paired trajectories through the registered 2B milestone and execute the frozen two-seed common E1+E2 admission workflow. Completion of the full anchor still requires eight numerically eligible 30B endpoints; the Certified/Haar pair receives a scientific endpoint verdict only if $t^*$ exists. The resume action is to audit the first complete 2B Native checkpoints and issue the registered common certificate artifact or continue dormant to the next registered milestone; no result-derived architecture or threshold change is allowed.
