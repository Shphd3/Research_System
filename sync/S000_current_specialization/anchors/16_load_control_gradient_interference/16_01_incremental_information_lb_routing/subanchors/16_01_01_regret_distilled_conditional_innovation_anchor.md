# A16_01_01 Regret-Distilled Conditional-Innovation Routing


## 1. Problem Definition

A16_01 asks whether the actual same-layer Router-visible increment can improve routing under verified differentiable load balance. Its current trainable branch is supervised only through language-model and load losses and has no replicated advantage through 20B; every eligible geometric direction also failed the frozen expert-choice-regret gate. The smallest live uncertainty is therefore objective alignment, not another spectral coordinate.

For layer $\ell$, let $x_{\ell,t}=n^{old}_{\ell,t}$ be the pre-Attention normalized state, $u_{\ell,t}=n^{new}_{\ell,t}-n^{old}_{\ell,t}$ the actual same-layer increment, and $r_{\ell,t}=u_{\ell,t}-A_\ell x_{\ell,t}$ the part not linearly predictable from $x$. The decision question is: **on two frozen Native-LB 10B checkpoints, can a rank-56 branch trained from counterfactual expert utility use $r$ to lower held-out target-token expert-choice regret relative to Native, a utility-trained raw-$u$ branch, and a matched Haar residual branch?**

A Pass qualifies the branch for an already conditionally approved 10B-to-30B NLL test. A Fail closes this objective-and-feature realization before long training. An engineering or data-identity failure is Insufficient. This decision does not ask whether the teacher remains correct after experts jointly evolve.

## 2. Physical Priors

The retained prior is that the useful routing signal, if present, is a token-conditioned **relative expert advantage** rather than covariance rank or semantic readability. Removing the component of $u$ predicted by $x$ should reduce duplication of the Native path. The prior is false for this realization if conditional residuals do not reduce held-out regret beyond raw and Haar controls in both seeds.

## 3. Falsifiable Hypotheses

**H1:** $r$ contains cross-document relative-expert utility not already exploited by the frozen Native logits, and direct utility distillation binds that signal to routing. It predicts lower held-out regret for Conditional-Utility than Native, Raw-Utility, and Conditional-Haar in both seeds.

**Strongest rival:** the teacher is local noise, $r$ removes useful signal, or extra low-rank capacity alone explains any apparent gain. It predicts no replicated advantage over Native and the matched controls. A Conditional advantage over Native but not Raw supports utility supervision only; an advantage over Raw but not Haar does not support learned direction identity.

## 4. Mathematical Model

On FIT documents only, fit the residualizer $A_\ell$ by document-level cross-fitting. Let $P_\ell\in\mathbb R^{768\times56}$ be a learned or fixed-Haar orthonormal frame and $C_\ell=A_\ell P_\ell$. The deployed branch is

$$
z_{\ell,t}=z^{native}_{\ell,t}+\alpha_{\ell,t}B_\ell\left(u_{\ell,t}P_\ell-x_{\ell,t}C_\ell\right).
$$

This equals $z^{native}+\alpha B(rP)$ but avoids an online $768\times768$ residualizer. For each target token, force each of eight experts only at that token and layer, obtaining next-token losses $\ell_e$. The teacher is

$$
q_e=\operatorname{softmax}_e\left(-\frac{\ell_e-\min_j\ell_j}{0.1}\right).
$$

The primary metric is expert-choice regret $R=\ell_{\arg\max_e z_e}-\min_e\ell_e$ in nat/token. It measures the local cost of the chosen expert under frozen experts; it cannot prove long-horizon training utility.

## 5. Computational Realization

Use each seed's own Native-LB 10B checkpoint and the existing document-disjoint 384-document functional bank. FIT/DEVELOPMENT/CONFIRMATION contain 128 whole documents each, with eight fixed target positions per document. FIT uses five-fold document cross-fitting for $A$; DEVELOPMENT selects only registered ridge/optimization candidates; CONFIRMATION is opened once after all choices freeze.

The branch reuses the dormant rank-56 projection and expert-logit tensors already present in the Native checkpoint. Frozen standardizers and the matrix $C$ are reconstructed from a hashed artifact, so no new trainable parameter or missing optimizer slot is introduced. During frozen distillation, backbone, experts, and Native Gate remain fixed. Online long training never forces all experts and uses only $x,u$ plus the small branch.

## 6. Minimal Falsification Tests

The decisive test is the two-seed document-paired confirmation comparison. Regret is first averaged within each document over the four layers and eight registered positions. Conditional-Utility passes only if, in each seed, the paired-bootstrap 95% upper bound is below zero for all three differences versus Native, Raw-Utility, and Conditional-Haar. Layerwise results are explanatory only and cannot select favorable layers or replace the registered aggregate verdict. Data-hash, forced-expert locality, no-op replay, cross-fit leakage, artifact integrity, orthonormality, and frozen-gradient guards protect eligibility.

Complete eligible evidence that misses the rule is Fail. Broken checkpoint identity, functional-bank separation, counterfactual locality, or numerical/recovery guards is Insufficient.

## 7. Current Evidence

The parent evidence establishes the motivation but not H1: Trainable-Innovation has opposite-signed 20B effects across seeds, and every 2B/5B/10B E2 gate failed. Native checkpoints and the frozen functional bank exist, while the proposed conditional branch and gate are `NOT RUN`. The safest interpretation is that geometric or NLL-only incremental routing has not yet exposed expert utility; it does not establish that conditional innovation lacks such utility.

## 8. Claim Boundary And Next Decision

An E01 Pass supports only local frozen-expert utility for this four-layer DCLM model and teacher definition. It does not establish 30B NLL improvement, expert specialization, universal semantic novelty, or a public spectral basis. A Fail stops this conditional-innovation realization before long training; Insufficient requires repairing the invalid guard without changing the scientific contract.

**Exactly one next decision:** execute the approved two-seed frozen regret gate. **Completion criterion:** eligible confirmation arrays and a typed Pass/Fail/Insufficient verdict for all registered comparisons. **Resume action:** if and only if E01 is Pass, automatically execute the separately frozen A16_01_01_E02 continuation to a 30B total-token endpoint.
