# Anchor: Mixed-frequency representations and invocation of a high-frequency path

## 1. Problem Definition

The parent task is to construct more effective routing by feature frequency under a fixed compute budget. Existing evidence shows that one input contains features from several frequency bands. Score calibration improved target reception, but the previous learning comparison did not improve. Subtracting a mean and dividing by a mean are different operations; high frequency must not be equated with all common information. The advisor's further intuition is that distinctive components might use some already learned common computation. The frozen Base remains present throughout. This round therefore concerns the invocation and updating of additional residual FFNs; it cannot claim that the original architecture removed common capabilities.

**The single decision question is: with the same top-2 and expert budget, does retaining one prespecified high-frequency path improve held-out learning on inputs containing low-frequency features, compared with dynamically choosing two paths; and does that increment depend on organizing features by frequency?** Token, feature, geometry, and exposure analyses precede the registered learning test. Static coverage diagnoses routing; it cannot substitute for NLL.

This is an explicit operationalization within the user's authorization for autonomous exploration. The user authorized modeling, learning when warranted after analysis, and four H100 Reserved GPUs. The model and design below are AI operationalizations within that scope; they do not establish the advisor's endorsement of a mechanism. No Focus is created or reset. Final scientific judgment remains Unknown.

## 2. Physical Priors

1. An input can contain components from several frequency bands. Co-occurrence does not establish statistical dependence or compatibility under shared learning. The Base continues to provide common computation. This combines an advisor intuition and prior evidence; the mechanism remains untested.
2. Nonnegative dictionary amplitudes are routing proxies. Actual representation vectors can cancel. The mean and centered PCA describe different objects. These are definitions and mathematical relations.
3. Routing changes which samples additional experts receive and how often they update. A benefit may arise from generic sharing or load changes rather than frequency-specific semantics. This is a competing explanation.

## 3. Falsifiable Hypotheses

**H-T:** Feature activation and frequency composition still vary with context after fixing current-token identity. If conditional prediction from the same token ID almost completely explains variation in the review panels, the context interpretation weakens; inadequate support yields insufficient evidence. The next token is an explanatory label only and never enters the router.

**H-G:** The high-frequency band may carry major directions of variation in centered representations even if it is not a positive principal component of the raw mean. Test this with TRAIN PCA of actual hidden states and signed projections, rather than substituting decoder norms.

**H-L:** The increment in low-frequency held-out NLL from forcing a high-frequency path, \(\Delta_T\), is negative, and the interaction relative to matched random membership, \(I\), is negative. If \(\Delta_T\geq0\), there is no improvement. If only \(I<0\) while \(\Delta_T\geq0\), the condition merely deteriorates less. Intervals crossing zero with these limited seeds imply insufficient evidence. Retain negative results without adjusting routes or budgets to obtain support.

## 4. Mathematical Model

Position \(t\) contains the current token and visible prefix and predicts \(y_t=\operatorname{token}(t+1)\). The shared code \(z\) is jointly encoded from the frozen 14 layers. Let \(h\) be the actual block-28 residual-post representation, \(d_i\) its decoder vector restored to raw coordinates, and \(b\) the offset including the preprocessing mean.

\[
h_t=b+\sum_{j=1}^{4}v_j(t)+v_U(t)+e_t,
\qquad v_j(t)=\sum_{i\in B_j}z_i(t)d_i,
\qquad p_i=P_{\mathrm{TRAIN}}(z_i>0).
\]

This defines reconstruction plus its residual; it does not assume orthogonal atoms. Centered variance includes cross-band terms. A sum of band amplitudes is therefore not representation energy. Obtain the TRAIN centered PCA basis \(U_k\) from actual \(h\), for \(k=1,16\). Measure decoder alignment by

\[
\eta_i=\frac{\lVert U_k^\top d_i\rVert^2}{\lVert d_i\rVert^2},
\qquad
\beta_j=\frac{\mathbb{E}\langle U_k^\top\delta v_j,U_k^\top\delta h\rangle}
{\mathbb{E}\lVert U_k^\top\delta h\rVert^2}.
\]

The signed projected contributions, including the residual, sum to one. \(\eta\) describes directions; \(\beta\) also incorporates actual activation. Neither directly establishes optimization dominance or semantic function.

Define \(c_i=z_i\lVert d_i\rVert\), \(M_j=\sum_{i\in B_j}c_i\), and \(a_j=\mathbb{E}_{\mathrm{TRAIN}}M_j\). Policy F chooses the two distinct group pairs with largest \(M_j/a_j\), then chooses the subgroup with greatest raw amplitude within each pair. Policy H always invokes one expert from group pair with index 3, then one from the best of the other three pairs. Both paths always have weight \(1/2\). The full hidden state is neither projected nor stripped of common information:

\[
h'_t=h_t+\frac{s_h}{2}
\left\{f_{r_1(t)}(h_t/s_h)+f_{r_2(t)}(h_t/s_h)\right\}.
\]

Estimate \(s_h\) only on TRAIN. All parameters of eight ordinary FFNs are trainable; the Base, output head, and dictionary remain frozen. Zero-initialized down projections preserve the initial logits. For membership T, retain the original four frequency bands and split each into two feature subgroups by a fixed hash, avoiding inheritance of old \(\phi\) relations or singleton subgroups. For membership R, randomly allocate the entire feature pool while exactly matching all eight T group sizes. Frequency bands remain the original log-equal-width bands, not equal-count frequency bins.

Compare T_F, T_H, R_F, and R_H with identical data, initialization, top-2, width, and update budget:

\[
\Delta_T=L(T_H)-L(T_F),\qquad
\Delta_R=L(R_H)-L(R_F),\qquad
I=\Delta_T-\Delta_R.
\]

Here \(L\) is DEV per-feature macro NLL over the same T-B1 feature set. Also report position averages and overall NLL. \(I\) is not a common-information mediation effect: invocation, load, and update exposure change together as consequences of a routing strategy. Two seeds support exploratory conclusions only.

## 5. Computational Realization

1. Reuse the same TRAIN, EVAL, and DEV caches and verify hidden states, shared codes, tokens, targets, and positions. TRAIN defines frequency, membership, scores, proxy labels, and PCA; subsequently apply the same computations to review panels.
2. Measure current-token and target-token correspondence for all features. Inspect variation across contexts with the same token ID and random positive, high-activation, and same-ID inactive examples. Preserve insufficient-support outcomes. Individual low-frequency features have only 1–17 TRAIN hits; do not claim stable, single meanings.
3. Compute the new memberships and four routes exactly, including exposure/reception identities and mixed-band inputs. Previous top-1 failures and an equal-budget post-hoc oracle are diagnostics only. Reuse outcomes rather than repeat training if F and H are completely equivalent.
4. If static evidence leaves the question of learning under different update allocations unresolved and implementation qualification passes, use four H100 Reserved GPUs for the four conditions and two seeds, one epoch each. Reveal final DEV results together. Do not adjust routes, update counts, or winner selection using DEV.

## 6. Minimal Falsification Tests

H-T uses TRAIN conditional statistics to predict EVAL and DEV and tests activation heterogeneity within token IDs, separating a lexical-identity explanation; inadequate support remains insufficient. H-G uses actual-hidden-state PCA, projected band vectors, residuals, and cross terms to separate large amplitude from carrying actual directions of variation. H-L is adjudicated by \(\Delta_T\) and \(I\), with lower NLL preferable. Both must support the prediction; relatively less deterioration is not improved learning.

Learning qualification requires different actual routes, exactly two distinct experts per position, identical complete inputs, correct preprocessing and denominators, exact zero-branch equivalence, gradient checks, a small-sample fitting check, and save/resume checks. It does not require H to look better on static routing metrics. If all training conditions deteriorate abnormally, run the registered bounded common-learning-rate diagnostic. Preserve incomplete and failed outcomes instead of expanding conditions indefinitely.

## 7. Current Evidence

Previous final-layer amplitude routing improved low-frequency reception from 0% to 72.22%; this does not establish learning. Mean subtraction reached 17.58%, but 87.33% of positions routed to the low-frequency band lacked an original B1 activation. The mean high-frequency vector had a negative signed projection onto the mean of actual hidden states. Centered re-encoding increased reconstruction MSE. The previous bridge and mean-component records retain the complete evidence; their results are not overwritten.

At design registration, this round's results were not yet computed and success must not be prefilled. An itemized ledger of 18 intuition categories from the two meetings belongs in the round's Detailed appendix. These static statistics cannot adjudicate capacity multipliers, learning-rate superiority, larger-model superiority, causal generation by attention, or dominance inferred from parameter spectra.

## 8. Claim Boundary And Next Decision

At most, this round adjudicates routing and learning increments for the current frozen representations, SFT data, and top-2 budget. It does not establish pretraining capacity, knowledge difficulty, single semantic meanings, learning utility of \(\phi\), gradient interference, or a common-information mechanism. DEV is a new fixed review panel from the original corpus, not an independent external test; near-duplicate independence is unknown. The sole next decision is which explicit frequency-invocation hypothesis to retain, or whether to stop that explanation following negative or insufficient evidence. Do not automatically expand training or replace data to seek positive results.
