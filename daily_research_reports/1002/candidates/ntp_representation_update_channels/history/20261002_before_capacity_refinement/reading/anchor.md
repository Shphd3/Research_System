> Historical reading copy: relative links resolve against the original directory; scientific prose is unchanged. [Original byte snapshot](../anchor.md).

# Candidate Anchor: Can S7 representations explain natural-text responses to shared updates?

2026-10-02, Asia/Shanghai. `CANDIDATE_FOR_REVIEW`. The researcher confirmed natural-text representation analysis alongside mechanism work, S7 with its existing SAE as the tool, and storage in today's candidate folder. New comparisons and operational choices below are AI_PROPOSAL. No formal Focus or historical verdict is changed. [中文](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/anchor_cn.md).

## 1. Problem Definition

**Given a fixed S7 checkpoint and a fixed update from source texts, can another natural text's pre-update representation explain its response and locate output directions carrying that response?** Response means actual next-token cross-entropy change. In the primary candidate test, explanation means improved prediction on records excluded from fitting; it does not mean pure semantics or causal explanation.

The broader question is which data should share parameters and when separation has net value. Domain averages conceal event variation, while SAE activation and sensitivity do not specify signed loss effects. This round connects actual texts, fixed source updates and representation responses. Domains organize source updates rather than supplying a future Router's answer.

Additional readable information on independent records advances a representation-based learning relation. A precise lack of improvement limits this tool/readout/scale. Insufficient precision or numerical qualification leaves the relation unresolved. Long-term separation value is outside this test.

## 2. Physical Priors

1. Candidate language prior: contexts and continuations have structure; current model error, downstream sensitivity and representation jointly determine update demands. Zipf frequency or anisotropy alone cannot determine effect sign.
2. Mathematical condition: change only the final attention output matrix, holding its input, pre-addition residual and downstream parameters fixed. No later attention mixes positions, permitting native finite tail replay.
3. Measurement condition: source construction, readout fitting and result evaluation use separate records from a declared population. Distinct rows do not establish paper independence or absence from model training. Historical pools are already exposed and support exploration only.

## 3. Falsifiable Hypotheses

Primary candidate H: conditional on source updates, pre-update S7 outputs/frozen SAE coefficients contain response information beyond the registered baseline of current/previous token, preceding16-token bag, position and representation scales. Adding the representation should reduce squared error for actual finite responses on new records. SAE320 is the proposed primary branch; native projections are tool controls. SAE need not beat them, and its failure does not imply absence of information in the full native representation.

Strongest rival: readable differences mainly reflect lexical composition, realized target identity and common update directions. SAE domain profiles may repeat that composition. The actual target may enter an independent explanatory diagnostic but not a primary predictor claimed to be available before it appears.

Mechanism diagnostic: an output subspace can carry helpful or adverse components while the full update still helps. Activation, prediction sensitivity, actual displacement and signed effect are distinct measurements, not interchangeable success criteria.

## 4. Mathematical Model

An event is prefix \(x\) and true next token \(y\). Let \(c\in\mathbb R^{2048}\) enter \(W\in\mathbb R^{1024\times2048}\), producing native output \(a=Wc\); let \(r\) be the pre-addition residual. Frozen downstream computation produces \(z=g(a,r)\), probabilities \(p\) and loss \(\ell=-\log p_y\). With \(J=\partial z/\partial a\) and true-target one-hot \(u_y\),

\[
e=\nabla_a\ell=J^\top(p-u_y),\qquad G=\nabla_W\ell=ec^\top.
\]

Let \(M_A=N_A^{-1}\sum_{i\in A}G_i\) be the token-weighted source mean. Under \(W\mapsto W-\eta M_A\),

\[
v_{Aj}=-M_Ac_j,\qquad a_j'=a_j+\eta v_{Aj},\qquad
I_{Aj}(\eta)=\ell_j(a_j+\eta v_{Aj},r_j)-\ell_j(a_j,r_j).
\]

Displacement is exact for this parameter block; actual \(I\) is computed by the native tail. Its derivative is

\[
h_{Aj}=e_j^\top v_{Aj}=-\langle G_j,M_A\rangle_F,\qquad
I_{Aj}(\eta)=\eta h_{Aj}+O(\eta^2).
\]

Representation similarity determines only part of coupling; the loss direction also determines its sign. The object is actual learning response, with no SAE replacement forward.

The frozen SAE gives \(a=b+D\alpha+\varepsilon\). A preselected orthonormal output basis \(Q\) gives \(P=QQ^\top\). The split \(v=Pv+(I-P)v\) has exactly additive first-order effects; \(PM_A\) and \((I-P)M_A\) also define realizable shared matrix updates. Finite effects are generally nonadditive, requiring full, only-component and removed-component arms. Nonorthogonal atom scores cannot simply be summed as independent contributions. In particular, \(\Delta a=D\Delta\alpha+\Delta\varepsilon\); dynamic residual cannot be omitted on the strength of static fidelity.

For baseline \(B(x)\) and augmented features \(F(x)\), predict actual \(I_{Aj}\) on new records. Define the equal-source primary candidate statistic

\[
Q_A=1-\frac{\sum_j(I_{Aj}-\widehat I^F_{Aj})^2}{\sum_j(I_{Aj}-\widehat I^B_{Aj})^2},\qquad
Q_{\rm macro}=\frac14\sum_AQ_A.
\]

This is a source-balanced relative prediction-error improvement, not adverse-event prevalence, separation benefit or atom causation. The exploratory pooled-SSE ratio remains a secondary readout. Historical derivative fits cannot serve as untouched finite-response confirmation.

## 5. Computational Realization

First define the effect. Reuse the exact S7 checkpoint at 33B training tokens, final `attn.o.weight` and native tail. Sources form pure-NTP average gradients; SAE loss is excluded. This ordinary-gradient diagnostic does not replay AdamW or S7's SAE-augmented training objective. The source and response must refer to the same model state.

Next test readable information. Freeze the dictionary and F-selected atoms; fit the baseline, baseline+SAE and native projection controls on separate records. Actual targets enter loss labels and the separate composition diagnostic only. This separates pre-target information from after-target explanation.

Finally locate effects. For actual readout texts, display activation, native movement, signed first-order contribution and finite matrix response together. Retain complement, reconstruction residual and negative cases. A readable sensitive direction may carry no update, or its adverse part may be offset by other helpful directions.

The [existing tool audit](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/sae_tool_source_audit.json) identifies the SAE input as native output. This round reuses those objects/interfaces and adapts cached and finite-response analysis; it rejects old synthetic binary targets and any relabeling of exposed R as blind confirmation.

## 6. Minimal Falsification Tests

The proposed primary comparison tests additional readable response information: with new records, fixed sources and frozen models, interval lower bound>0 supports the specified readout; upper bound≤0 does not support it; otherwise evidence is insufficient. A practically useful increment remains Unknown. Detecting nonzero improvement does not establish engineering value.

Qualify no-op, outer-product identity, full-matrix versus tail replay, smaller-step linear approximation, and projection/complement closure separately. Include helpful averages with harmed events, sensitive but unmoved directions, coactivation with opposing demands, adverse components with helpful totals, and nonorthogonal double counting as confusing cases.

The candidate inference conditions on sources. Freeze new records, independent groups, fitting choices and secondary comparisons. Generalization to newly sampled sources would require an additional source-resampling contract, not included here. The [Protocol](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/protocol.md) is not yet approved for a new confirmation run.

## 7. Current Evidence

The [old natural-statistics primary test](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary.md) remains INSUFFICIENT: \(T=0.006637\), 95% interval \([-0.003738, 0.017012]\), allowing values below and above the historical1% candidate scale. SAE/Fisher profiles are a separate descriptive branch.

The [21B natural-direction study](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/atom_mechanism/20260926/summary.md) already located local helpful channels. The [33B controlled study](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/summary.md) showed adverse components offset by greater help. Their conclusions cannot be transplanted to current natural texts.

Today's finite evaluation shows each source improves its separate source-validation mean. All16 source/R-domain means are negative, from−0.001953 to−0.000182 nat; adverse-event fractions at a1e-5-nat deadband are 43.97%–52.81%. These are fixed-source exploratory results on old R.

The initial SAE predictor improves pooled squared error for actual finite response by 1.41%, versus2.26% for PCA and 2.53% for random projection. Stronger history baselines and swapped F halves give SAE derivative gains of 1.11%/1.21%, with equal-source averages about 0.76%/0.89%. Target diagnostics give about 21%–24%. This does not support SAE-exclusive or pure-semantic information.

On 64 R records, static reconstruction squared error of 6.51% does not guarantee dynamic fidelity: stable-support dynamic residual ratios are 0.979–1.000; 7.6%–11.8% of full-step events switch support, yielding all-event ratios about 48–82. The local affine formula was checked against S7 endpoints. The [report](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/research_report.md) and selected tables own detailed values, denominators, intervals and natural-text examples.

Replacing source construction by the other F half preserves helpful finite R-domain means, but same-sign rates among jointly resolved events are only 63.64%–79.13%; source-matrix cosines are 0.100–0.422. This further limits extrapolation from fixed-source readout gains to stable data properties. Two observed source sets do not estimate population source stability.

Continuation evidence: within-domain A/B batch transfer retains small gains, mainly in the within-domain mean; this does not exclude between-domain effects. The new [domain-response analysis](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/domain_response_structure.md) records partial replication, limited earlier-prefix increments and current-output input-channel boundaries. The [source-transfer continuation](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/source_transfer_addendum.md) preserves earlier values. Both are old-panel explorations and do not replace the question or confirmation design below.

## 8. Claim Boundary And Next Decision

The supported advance is a measurable connection among natural-text representations, fixed source updates, native movement and signed loss effects at S7. Universal semantic conflict, SAE-exclusive information, prospective Router utility, long-term harm and net separation benefit remain unsupported.

One next decision, AI_PROPOSAL for researcher review: whether to pursue new independent-record confirmation of finite-response information. Before that, settle data independence, fixed-source inference and the primary readout scope; keep old exploration separate from confirmation. Continue from qualified measurement and freeze lists rather than repeating the old Full.
