# Anchor: natural-language statistics and local update structure

2026-09-30, Asia/Shanghai. `CANDIDATE_FOR_REVIEW`; result `NOT RUN`; proposed key `ntp_statistics_local_compatibility`. The researcher confirmed signed compatibility, natural-target mixtures, and using the existing SAE as a domain/direction-sensitivity analysis tool. Exact hypotheses, estimators, sampling and thresholds remain **AI_PROPOSAL**. [Chinese](anchor_cn.md); [Protocol](protocol.md). No Focus reset or execution approval.

## 1. Problem Definition

**At a fixed language-model state and shared attention block, does natural text exhibit recurring local update structure, distinguished into signed mean demands and prediction-sensitive directions?** Domains and actual targets are the first conditioning variables, not the definition of all language structure. The parent purpose is to understand what relations could inform later data sharing; current readers have not established this bridge.

One bounded experiment uses selected academic excerpts. Its first-order primary test asks whether domain mean-gradient contrasts recur at comparable targets; signed cross-effects and natural-target mixtures accompany it. A separate mandatory functional branch asks which native-output directions change predictions, using the frozen SAE dictionary to give feature-level coordinates. SAE superiority, semantic names, pre-update prediction and long-term allocation are not assumed. A mean non-support leaves a functional-only answer possible; neither branch can establish the other's claim.

## 2. Physical Priors

**Candidate prior:** structured context–continuation distributions and model mismatch may create recurring mean demands; even without mismatch, model predictions may be sensitive to a structured set of output directions. Context representations and downstream sensitivity jointly determine gradients. The Fisher/KL relation is a mathematical derivation, not evidence that these structures differ by domain.

Marginal Zipf-like frequencies, activation anisotropy, centered gradient fluctuations and signed mean effects are distinct. None proves conflict. Small pooled gradients may hide cancelling group demands, but stationarity is not assumed. Shared sensitivity is not measured capacity competition or a reason to split experts.

## 3. Falsifiable Hypotheses

**Primary H1:** target-matched, subcategory-balanced domain mean contrasts agree across pools above the proposed 1% historical squared-gradient scale. Rival: composition, finite-sample mean error or generic averaging without recurring conditional contrasts.

**Functional H2:** domain-conditioned model-Fisher profiles differ reproducibly, including cases where H1 is not supported. Rival: pooled sensitivity, target/context composition, scale or probe noise explains the apparent differences. **Tool H3:** frozen SAE coordinates expose recurring occurrence/sensitivity patterns; compare equal-rank PCA/random controls to distinguish generic directions from dictionary-specific description. SAE need not outperform them. Signed compatibility, mixture and empirical-covariance diagnostics remain required. H2/H3 have separate descriptive outcomes, no proposed confirmatory threshold, and cannot rescue H1.

## 4. Mathematical Model

For context x, actual target y and domain s, freeze all parameters. Let c be the shared matrix input, a=Wc its native output, r the residual, logits z=g(a,r), probabilities p, one-hot target u_y, loss -log p(y), and J=partial z/partial a. Then

\[
e=J^\top(p-u_y),\qquad G=ec^\top,\qquad
K_{ij}=\langle G_i,G_j\rangle_F=(c_i^\top c_j)(e_i^\top e_j),\qquad
\Delta\ell_j=-\eta K_{ij}+O(\eta^2).
\]

The last relation assumes a sufficiently small ordinary SGD step on W alone. Unknown real continuations q_x give E[G|x]=J^T(p-q_x)c^T. Selected-target means may remain nonzero even at p=q_x; one continuation/context does not identify calibration.

Define **model Fisher**, with labels averaged under model p, regardless of calibration:

\[
F_a(x)=J_x^\top[\operatorname{Diag}(p_x)-p_xp_x^\top]J_x,\qquad
D_{\rm KL}(p_a\Vert p_{a+\delta a})=\tfrac12\delta a^\top F_a(x)\delta a+o(\|\delta a\|^2).
\]

Hold x/r/other parameters fixed for this local native-output change. At p_x=q_x, conditional mean gradient is zero and Cov(e|x)=F_a(x); with column-major vectorization,

\[
\operatorname{Cov}(\operatorname{vec}G\mid x)=(c_xc_x^\top)\otimes F_a(x)\qquad(p_x=q_x).
\]

This is a conditional identity, not a low-rank population finding. Outside calibration, true-target second moments/covariance are not model Fisher. Estimate model sensitivity directly; do not infer q_x or replace it with observed targets. [Empirical-Fisher limitations](https://arxiv.org/abs/1905.12558) motivate this separation.

The existing SAE encodes a, not c: a approximately equals its fixed decoder bias plus D alpha, with unit decoder columns d_k and sparse code alpha. Its local readout is

\[
I_k(x)=d_k^\top F_a(x)d_k,\qquad F_\alpha(x)=D^\top F_a(x)D,\qquad \delta a=D\delta\alpha.
\]

Here the chart keeps reconstruction residual fixed around native a; it does not replace a with its reconstruction or differentiate through TopK encoding. Pair activation with I_k to distinguish occurrence from directional prediction sensitivity. F_alpha is positive semidefinite but off-diagonal entries can be negative; those signs are not cross-data help/harm. Nonorthogonal atom sensitivities cannot be summed as independent capacity or energy shares.

Retain primary-selected means mu_s,y^b, pools b=F,R, four targets Y_*, and historical reference v0:

\[
T=\frac1{24v_0}\sum_{y\in\mathcal Y_*}\sum_{s<t}
\langle\mu^F_{s,y}-\mu^F_{t,y},\mu^R_{s,y}-\mu^R_{t,y}\rangle_F,\qquad
S^{\rm cond}_{st,y}=\frac{\langle\mu^F_{s,y},\mu^R_{t,y}\rangle_F+\langle\mu^F_{t,y},\mu^R_{s,y}\rangle_F}{2v_0}.
\]

Each T term is S_ss+S_tt-2S_st; positive contrasts need not imply negative compatibility. For all natural measured positions use separate means nu_s,y, marginal target weights q_s(y), and M_s=sum_y q_s(y)nu_s,y; substitute M into S. Uniform-mixture S includes cross-target products, unlike averaged same-target S. Functional profiles are conditioned on specified context/target sampling populations; they do not measure true target-conditional Fisher.

## 5. Computational Realization

Reuse frozen S7 33B, pure NTP and `model.blocks[7].attn.o.weight` (1024×2048). The same checkpoint's TopK32 SAE has 30,000 atoms at the native 1024-dimensional attention output before residual addition; verified encode/decode/dictionary interfaces supply codes and directions. No auxiliary loss, new SAE or optimizer.

Keep document-disjoint quartets on comma, space+the, space+of and period for T/S. Separately use all 16 measured positions per record for natural/common-support/uniform-target comparisons. Record-level exposure/duplicate qualification precedes use.

For the functional branch, compute real-target directional gradient moments separately from model-Fisher probes on a fixed balanced context panel. Pair all-atom activation/conditional-amplitude profiles with model-Fisher directional sensitivity and active-versus-inactive contexts; select illustrative/common/enriched atom sets on F activation only, never R or Fisher scores. Fixed F native-a PCA and seeded random orthogonal directions provide rank-matched controls. Apply identical probes/context weights to each tool, including orthonormalized decoder spans; decoder coordinates and span summaries have different meanings. Exact panel, probe, qualification and budget choices live in Protocol. Empty sets or controls explaining the same structure are legitimate outcomes.

## 6. Minimal Falsification Tests

H1 retains one primary verdict: 192 disjoint quartets and a previously calibrated proposed stratified Welch 95% interval. Eligible lower bound >0.01 supports; upper <0.01 does not support the proposed scale; overlap or qualification failure is insufficient. Signed S stays exploratory without a qualified sign interval.

H2/H3 are delivered independently: F-selected profiles/sets/directions fixed before R; report pooled versus domain deviations, R profile transfer, model-Fisher versus real-target moments, Monte Carlo noise and matched controls. No cherry-picked atom, uncorrected feature test or energy fraction establishes a functional mechanism. Missing cells, probe qualification or untested resource feasibility constrain the functional branch without changing H1's result.

Known cases must separate zero mean/nonzero Fisher, high activation/low sensitivity, low activation/high sensitivity, all-positive S with recurring differences, and nonorthogonal atom overlap. Only qualified descriptive recurrence is reported; new functional effect thresholds and population tests are not invented.

## 7. Current Evidence

The [prediction Summary](../summary.md) reports Q=-0.000138 (upper confidence limit 0.002294), not supporting registered 5% improvement. The [domain Summary](../domain_update_geometry/summary.md) reports Q_D=-0.005715 with uncalibrated inference, same-target cosine about 0.193 versus 0.00046, and common SAE rank64 K reconstruction error 0.803. The existing study measured all-atom activation and directional gradient energy; it did not establish model-Fisher sensitivity or causal feature use.

Candidate metadata coverage meets the pre-screening 12-endpoint requirement, not independence certification. New T/S, mixture relations, functional profiles and control comparisons are **NOT RUN**. [SAE source audit](sae_tool_source_audit.json) records inspected interfaces, not new model measurements.

## 8. Claim Boundary And Next Decision

Bound conclusions by checkpoint, block, source records and sampled positions. Mean demand, signed first-order relation, model-sensitive direction, SAE occurrence and empirical covariance are separate objects. A sensitive decoder direction is not semantic purity, necessity, capacity consumption, cross-data conflict, feasible routing or long-term benefit. Conditional output edits are a local sensitivity probe, not a verified shared-parameter intervention.

**One next decision:** review this mean-plus-functional analysis as the bounded investigation before selecting a later prediction/routing target. A functional-only finding remains informative when H1 fails; SAE-control parity limits dictionary-specific interpretation rather than nullifying model structure. The researcher confirmed using SAE as a tool; exact functional operationalization and execution eligibility remain proposed/blocked. Resume through Protocol gates, keeping long-time interaction outside this round.
