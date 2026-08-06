---
anchor_id: 15_00_02_centered_common_subspace_stability
parent_anchor: 15_00_covariance_head_gate_alignment
status: completed_pass_energy_transfer_gap_projectors_shared
canonical_language: en
companion_language: zh
thinking_card: 15_00_02_centered_common_subspace_stability_thinking_card_cn.md
updated: 2026-07-31
---

# A15_00_02 Centered Common-Subspace Stability After De-meaning

Thinking Card source:
[15_00_02_centered_common_subspace_stability_thinking_card_cn.md](15_00_02_centered_common_subspace_stability_thinking_card_cn.md).

## 1. Problem Definition

A15_00 establishes that trained linear Gates retain strong equal-energy
alignment with the covariance head of their actual input, while middle/tail
remain accessible but weaker. It does not determine whether the post-mean head
is a centered-common subspace that transfers across data groups or a different
high-variance subspace in every group.

**Decision question:**

> Across disjoint DCLM document groups, does the top-64 subspace of the
> within-group centered Router input transfer, and is the equal-dimensional
> local remainder less stable after an independently pooled top-64 component is
> removed?

Stability means held-out cross-group activation capture. It does not mean
semantic commonality, shared expert function, or training benefit.

The primary metric is the top-64 held-out cross-capture gap above a
dimension-matched Haar q95, $\Gamma_{64}$, measured in held-out activation
energy fraction.

## 2. Physical Priors

1. A fixed translation does not change centered covariance:
   $\operatorname{Cov}(g-c)=\operatorname{Cov}(g)$. Decommon directly removes
   mean/DC, not centered common variation.
2. A single Gate can accumulate a coherent projection when directions recur
   across data groups. Rotating group-local residuals instead expose only their
   average or most stable component.
3. Finite-sample PCA is a strong rival in 768 dimensions, so transfer must
   converge with document count and exceed a direction null.

## 3. Falsifiable Hypotheses

**H1:** The centered top-64 has positive cross-group $\Gamma_{64}$. After an
independently pooled top-64 is removed, local residual top-64 transfer is
smaller and lies in or near the matched null.

**Strongest rival R0:** Both apparent subspaces are finite-sample noise and fail
to transfer beyond Haar.

**R1:** Stable centered structure is wider than 64 dimensions, so both the
registered top-64 and the orthogonal remainder transfer.

**R2:** Geometry is stable but unrelated to expert function; this subanchor
cannot reject that rival.

**Pass:** Decommon 80k top-64 transfer exceeds the matched null, the direction
replicates at 40k, and equal-dimensional residual transfer is lower. LB
determines whether the pattern is lineage-shared.

**Fail:** A valid precise measurement supports R0 or R1.

**Insufficient:** Actual-input replay, document independence, sample-size,
center invariance, rank, or numerical guards fail.

## 4. Mathematical Model

For layer $\ell$, group $s$, and token $t$,

$$
g_{\ell,s,t}=\mu_\ell+U_{\ell,*}a_{\ell,s,t}
+\epsilon_{\ell,s,t}.
$$

With actual Gate input $r=g-c$, within-group centering gives

$$
x_{\ell,s,t}
=r_{\ell,s,t}-\mathbb E_s[r_{\ell,s,t}]
=g_{\ell,s,t}-\mathbb E_s[g_{\ell,s,t}].
$$

Let $U_{\ell,s,k}$ be fitted on source-shard documents. For an independent
target evaluation matrix $X_{\ell,t}^{eval}$,

$$
E_{\ell,s\rightarrow t,k}
=\frac{\|X_{\ell,t}^{eval}U_{\ell,s,k}\|_F^2}
{\|X_{\ell,t}^{eval}\|_F^2},
$$

and

$$
\Gamma_{\ell,64}
=\operatorname{median}_{s\ne t}
\left[
E_{\ell,s\rightarrow t,64}
-q_{0.95}(E_{\ell,R_{64}\rightarrow t})
\right].
$$

After removing an independently pooled projector $P_{\ell,*}$, the same
calculation on $(I-P_{\ell,*})x$ gives
$\Gamma_{\ell,64}^{res}$. H1 predicts
$\Gamma_{\ell,64}>\Gamma_{\ell,64}^{res}$.

## 5. Computational Realization

The [approved canonical E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_02_E01_centered_common_subspace_stability/protocol.md)
uses existing 12-layer H768 LB/decommon checkpoints and directly hooks the Gate
input plus upstream $g$ for decommon. The primary endpoint is 80k, 40k is a
replication, and 30k is trajectory support only.

New DCLM held-out documents disjoint from the Q1/Q2 manifests are hash-frozen
into eight groups with fit/evaluation document halves. All 12 layers are
reported. The primary dimension is $k=64$; $k\in\{16,32,128,256\}$ is a
dimension and sample-size sensitivity analysis.

This experiment shares frozen activation extraction with A15_00_03 but has an
independent metric and verdict, so the two measurements can execute in
parallel after explicit execution authorization.

## 6. Minimal Falsification Tests

1. Verify numerical equality of the centered covariance of $g$ and $r=g-c$ at
   the same frozen decommon checkpoint.
2. Compute document-held-out top-64 cross-capture against 256
   dimension-matched Haar orientations and wrong-layer bases.
3. Repeat the same-dimensional test in the remainder after removing an
   independent pooled top-64.
4. Use 8/16/32 fit-document curves to reject local-PCA sample noise.
5. Bootstrap document groups and document blocks; tokens are not independent
   uncertainty units.

## 7. Current Evidence

The approved [E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_02_E01_centered_common_subspace_stability/protocol.md)
completed with verdict
`pass_stable_centered_less_stable_local_residual`; see the
[summary](/Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_02_E01_centered_common_subspace_stability/summary.md)
and [detailed evidence ledger](/Projects/from-attention-to-search/main/experiments/A15/15_00_covariance_head_gate_alignment/A15_00_02_E01_centered_common_subspace_stability/detailed.md).

At 40k/80k, the null-relative centered-top-64 transfer is 0.600/0.580 for
decommon and 0.584/0.564 for LB. The independently residualized local top-64
also transfers above its matched null at 0.414/0.402 and 0.409/0.392,
respectively. The paired top-minus-residual gap is positive in every layer and
has model-level values 0.179/0.176 for decommon and 0.162/0.167 for LB; every
gap bootstrap interval lies above zero.

The registered secondary projector overlap now sharpens the interpretation.
Across 40k/80k, model medians are 0.760--0.791 for centered top-64 and
0.704--0.730 for residual-64, versus matched random q95 values 0.086 and
0.094. The model-median top-minus-residual overlap gap is only 0.045--0.047
and has local layer exceptions. Thus residual energy transfer is weaker, but
the residual projector itself is highly shared across the random document
shards.

All actual-input replay, center-invariance, rank, sample-size, Haar, and
numerical guards pass. Shard means are highly aligned, but the decision does
not rely on mean cosine. The direct observation is a hierarchy of
cross-document stability: the centered top-64 transfers more strongly, while
the local residual-64 remains substantially transferable.

The strong rival that demeaning leaves mutually unrelated residual spaces is
therefore falsified. The narrower interpretation is that a fixed translation
leaves a globally shared hierarchy with different energy concentration. Per
the researcher execution amendment, 30k is excluded from the evidence path.

## 8. Claim Boundary And Next Decision

A15_00_02 establishes cross-document statistical transfer, not semantic
commonality or functional utility. It does not show that the residual is
useless, that the stability gap caused decommon's training result, or that the
pooled component should be retained or removed. “Local residual” is also not
equivalent to random noise: it passes the transfer null.

The current stable-hash shards mix DCLM conditions and therefore cannot rule
out condition-specific low-dimensional modes inside the shared residual
envelope.

**Exactly one next decision:** decide whether to formalize a condition-
stratified frozen follow-up using domain/topic groups, within-condition
half-split reliability, projector overlap, and cross-capture before any
matched training intervention.
