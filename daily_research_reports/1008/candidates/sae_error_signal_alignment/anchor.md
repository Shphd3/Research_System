# Candidate Anchor: SAE similarity and native loss-gradient alignment

## 1. Problem Definition

**Question:** at a fixed S7fresh or Qwen3-0.6B-Base state, do token positions with similar SAE activation codes have more aligned native next-token loss gradients than matched random positions?

The researcher explicitly activated H2: “tokens with similar SAE atoms also have similar error signals δ,” and authorized candidate design and a four-H100 reserved diagnostic without a separate review gate. This dated candidate does not create a Focus, replace a canonical Anchor, or confirm the hypothesis. Question status is `USER_ACTIVATED`; numerical operationalization and rival analysis are `AI_PROPOSAL_UNDER_AUTHORIZED_CANDIDATE_SCOPE`; scientific conclusion is `Unknown`.

“Token” means a contextual prediction position, not a vocabulary type. “SAE similarity” means similarity between the complete sparse activation codes at two positions, not similarity between two individual dictionary columns. “Error signal” means the gradient of that position’s real next-token cross-entropy with respect to the native tensor observed by its SAE.

This is a necessary bridge for evaluating SAE-based grouping for shared learning. A positive association supports that bridge locally; no association weakens this particular SAE operationalization; an unresolved interval leaves it open. No Router or Expert is trained here.

## 2. Physical Priors

One candidate prior motivates H2: similar SAE activation patterns may identify positions that request similar local changes from the model. The live alternative is that SAE codes reflect input or lexical similarity while the observed next-token targets and downstream computation produce different gradient directions.

Two models observe different tensors: S7fresh uses the final Attention output projection before residual addition; Qwen uses the final MLP input after layer normalization. Each hypothesis test is defined within its own model and hook. Equality of their dimensions does not make their signals interchangeable.

## 3. Falsifiable Hypotheses

H2 predicts that held-out positions’ five nearest SAE neighbors in the fitting reference pool have both positive mean δ-direction cosine and greater mean δ-direction cosine than twenty matched random reference draws.

The strongest operational rival is that apparent alignment comes from domain, position or current-token identity rather than an SAE grouping property. Main neighbors and random controls share domain and position bins; native-representation neighbors and a strict same-current-token analysis test whether the SAE contributes more than these alternatives. Next-token identity is excluded from neighbor selection and used only for loss computation and post-hoc strata.

The main test is predictive association at frozen model states. It does not identify a causal semantic mechanism or demonstrate the benefit of routing.

## 4. Mathematical Model

For position i, let a_i ∈ R^1024 be the native SAE hook tensor, z_i ∈ R^30000 its nonnegative Top-32 code, and y_i the actual next token. Let f_m be the fixed downstream computation in model m. Its cross-entropy and native error signal are

\[
\ell_i=-\log p_m(y_i\mid\text{prefix}_i),\qquad
\delta_i=\nabla_{a_i}\ell_i.
\]

These are measured by native forward computation and automatic differentiation; they are not SAE reconstruction gradients. Code similarity uses cosine after multiplying each code coordinate by its decoder-column norm. For held-out query i, N_i is the five nearest fitting positions under this similarity, and R_i contains twenty matched random draws excluding N_i. Neither set uses δ or y for selection.

The decision quantity is the advantage in loss-gradient direction alignment:

\[
s_i=\frac{1}{5}\sum_{j\in N_i}\cos(\delta_i,\delta_j)
-\frac{1}{20}\sum_{j\in R_i}\cos(\delta_i,\delta_j),\qquad
S=\frac14\sum_{d=1}^{4}\operatorname{mean}_{\text{query records in }d}
\operatorname{mean}_{i\text{ in record}}s_i.
\]

Cosine and S are dimensionless. Equal domain weighting prevents a domain with more valid positions from dominating. Positive S alone can mean “less opposed,” so positive neighbor mean cosine is a separate support requirement.

The route to parameter compatibility is conditional. For a linear projection with input u_i and output sensitivity κ_i,

\[
G_i=\kappa_i u_i^\top,\qquad
\cos_F(G_i,G_j)=\cos(\kappa_i,\kappa_j)\cos(u_i,u_j).
\]

S7 has u_i=c_i and κ_i=δ_i at its Attention output projection. For Qwen’s MLP down projection, u_i is the gated intermediate activation and κ_i is the gradient at the down-projection output; δ_i at the SAE’s MLP-input hook is generally different. Parameter-gradient cosine is therefore a secondary measurement using the actual projection inputs and output gradients. Even aligned δ does not unconditionally imply aligned parameter updates, finite-step benefit or long-term Router utility.

## 5. Computational Realization

1. **Measure the proposed relation.** Use fixed 1024-record natural-text sampling, split into disjoint fitting and readout records. Capture a, δ, sparse SAE codes and the true next-token target at sixteen fixed positions per record. Freeze the backbone and SAE; compute only natural next-token CE. This makes the signal an actual model error sensitivity.
2. **Separate similarity from target-informed selection.** Construct SAE and native-a neighbors from fitting inputs only, with domain and position-bin matching. Compare their gradient alignment with fixed random draws, a same-current-token subgroup and a gradient-shuffle diagnostic. These controls expose lexical and stratum explanations without using the outcome to choose favorable pairs.
3. **Report the bounded evidence.** Average positions within query records, then records within each domain, then domains equally. Bootstrap readout records with fitting references fixed. Record effect intervals, absolute neighbor cosine, negative-cosine frequency, validity coverage and actual parameter-gradient alignment. These measurements answer the local association question rather than an unrun sharing intervention.

The [Protocol](protocol.md) fixes sampling, masks, computations and execution limits.

## 6. Minimal Falsification Tests

Evaluate each model independently. Measurement eligibility requires at least 256 valid readout records and at least 90% valid planned readout positions. Use 2000 domain-stratified record-bootstrap draws and two-sided 95% percentile intervals.

- `SUPPORT`: the lower interval bound of S is positive **and** the lower bound of absolute SAE-neighbor mean δ cosine is positive.
- `NON_SUPPORT`: the upper interval bound of S is nonpositive.
- `INSUFFICIENT`: otherwise, or measurement eligibility fails.

Zero is an AI-proposed association threshold: it separates alignment advantage from no advantage, not a useful Router effect size. Two separately reported model tests do not establish population-wide replication. Native-a, current-token, centered-code and shuffled-δ diagnostics cannot rescue a failed primary test. The strict current-token subgroup is descriptive if it contains fewer than 64 query records.

## 7. Current Evidence

**H2 result: NOT RUN.** Existing evidence establishes asset identity, not H2.

S7fresh’s exact 33B-token checkpoint contains eight layers, a 1024-dimensional Attention output, a 30000-feature Top-32 SAE and reconstruction weight 0.1. Existing token-level caches contain native a, δ and aligned SAE codes, but this experiment collects the newly selected records. The [existing local-update report](../../local_update/full_report_cn.md) explains the related one-step evidence and its limits.

Qwen3-0.6B-Base has a frozen-backbone, layer-27 MLP-input SAE trained on 1,000,001,536 DCLM tokens. Its checkpoint, config hash and tensor shapes were directly checked; its [owning Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E16_dclm_final_layer_topk_sae_teacher/summary.md) establishes dictionary qualification, not semantic or routing validity.

The prepared new sample has zero exact overlap with the earlier 20260925 1024-record selection but overlaps the historical 20260930 2048-record NTP-statistics panel by 768 records. The source corpus was previously audited; paper IDs are unavailable. It is readout data for this diagnostic, not untouched confirmation.

## 8. Claim Boundary And Next Decision

Allowed conclusion: a model-specific, hook-specific association between input-only SAE similarity and native next-token gradient direction, with stated controls and uncertainty. Unresolved issues include lexical/target confounding, reference-pool dependence, approximate record independence and transfer across states or objectives.

Cannot claim: SAE atoms cause similar errors; aligned errors necessarily yield compatible complete updates; routing improves training; different Experts should share parameters; one model’s signal equals the other’s. Scientific confirmation remains with the researcher.

**One next decision:** after both fixed tests and controls are reported, the researcher decides whether this SAE-based similarity has enough local gradient-alignment evidence to retain as a candidate grouping signal. Completion requires measurements, eligibility and separate outcome branches for both models; resume by reading their resulting analysis tables and execution receipts, not by automatically starting Router training.
