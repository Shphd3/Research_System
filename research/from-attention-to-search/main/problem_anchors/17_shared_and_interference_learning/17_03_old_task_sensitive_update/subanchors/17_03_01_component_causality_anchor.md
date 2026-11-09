# A17_03_01: Deletion, amplification and rule bias under sensitivity restriction

[中文](17_03_01_component_causality_anchor_cn.md)

Inherited problem: old_task_sensitive_update. No new Focus. On 2026-10-11 the researcher delegated deeper mechanism analysis, necessary experiments on four reserved H100 GPUs, and a meeting report without further approval. Mechanisms below remain AI candidates; scientific closure is Unknown.

## 1. Problem Definition

Does the larger new-task CE gain with some old-answer failures arise from deleting estimated old-sensitive components, amplifying the remaining update, or subsequent training trajectories? Fix the old state and source batch to identify the first two finite effects. This serves the parent question of useful versus harmful shared updates; existing sequential endpoint evidence remains separate.

## 2. Physical Priors

Formal assumptions: distinct first/last words, visible rule prefixes, and realizable parameter interventions. CE concerns correct-word probability; selection also depends on competitors. Sensitivity has no signed help/harm meaning. Whether a local effect explains a sequential endpoint is empirical.

## 3. Falsifiable Hypotheses

H1 candidate: deleting sensitive components itself improves new development CE and amplification increases that effect. The rival is that only amplification helps, or that the endpoint advantage requires later trajectories. Measure deletion and amplification separately.

H2 candidate: increased response to the rule prompt can coexist with a larger bias toward the new answer, worsening old selection. The algebraic implication is proved; its occurrence and parameter source require intervention. Increased pair probability alone is a distinguishable alternative.

## 4. Mathematical Model

For correct probability p_y and opposite-rule probability p_o, let M=p_y+p_o and m=log(p_y/p_o). Exactly,

\[
\ell=-\log p_y=\ell_{mass}+\ell_{choice}=-\log M+\log(1+e^{-m}).
\]

This decomposes output loss and its gradient, not parameter functions. On a paired list let b=(m_F+m_L)/2, c=(m_F-m_L)/2 and h=c for new FIRST, h=−c for new LAST. Then m_new=b+h and m_old=b−h. Both pair margins improve iff Δb>|Δh|; both pair decisions are correct iff b>|h|, by direct substitution. Full-vocabulary correctness additionally requires beating all other tokens. b is previous S/2, not a new discovery.

At old matrix W, fixed orthonormal-row basis Q and source CE displacement d, define d_in=QᵀQd, d_out=d−d_in and λ=||d||/||d_out||. For any readout Y, exactly,

\[
Y(W+λd_{out})-Y(W+d)=[Y(W+d_{out})-Y(W+d)]+[Y(W+λd_{out})-Y(W+d_{out})].
\]

The brackets identify deletion and amplification without a first-order approximation. The four-corner interaction is Y(W+d)−Y(W+d_in)−Y(W+d_out)+Y(W). For fixed source gradient g and norm s, ordinary and restricted directions give source first-order CE changes −s||g|| and −s||P_out g||; the latter cannot be more negative. A source-batch first-order advantage therefore cannot explain the development endpoint advantage.

## 5. Computational Realization

Restore saved old endpoints; perturb only final o_proj. Hold state, source batch and evaluation inputs fixed across interventions. Four corners plus normalized remainder separate deletion, amplification and interaction. The mass/choice objective gradients test the relation between geometric and predictive components. Native forward reads per-example losses, margins and full-vocabulary decisions. Existing endpoints receive descriptive exact decomposition; freeze new intervention choices before GPU measurement.

## 6. Minimal Falsification Tests

Primary scale is one original SGD step. Average three source batches within each case and report new-CE deletion gain, amplification gain and their sum with old-margin/accuracy costs. Positive deletion supports a local deletion account; only amplification helping supports the amplification account; no total advantage limits the immediate old-state explanation of endpoint gains. Mixed cases remain heterogeneous; batches are not independent seeds. Failed numerical/restoration qualification gives insufficient evidence. Smaller/larger scales assess finite boundaries, never select the best result.

## 7. Current Evidence

E01 ordinary updates improve old/new CE in all six cases. Restricted trajectories improve new CE more but do not preserve all old accuracy. This is not anti-forgetting confirmation. Previous paired-margin work already measured S but not the finite deletion/amplification contrast. E02 completed630/630 GPU cells with independent verification and actual-output registration. Three source batches averaged within each case yield negative new-CE deletion gains in all6 cases and positive amplification gains in all6; total gains are4 positive and2 nonpositive, including1 near zero. Both order means are positive. The one-step old-accuracy contrast does not reproduce the extra100-step cost. Endpoint and saved-trajectory decompositions remain separate exposed-development descriptions. [E02 Summary](../../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E02_component_causality/summary.md) owns factual results and bounded AI interpretation; human mechanism judgment and closure remain Unknown.

## 8. Claim Boundary And Next Decision

Identify finite causal contrasts for the specified state, displacement and readers; do not infer a 100-step mechanism, common/unique modules, expert utility or natural NTP. Next decision: does the immediate effect constrain the endpoint account, or must that account remain trajectory-dependent? Completion requires qualified component contrasts, per-example responses and bounded interpretation.
