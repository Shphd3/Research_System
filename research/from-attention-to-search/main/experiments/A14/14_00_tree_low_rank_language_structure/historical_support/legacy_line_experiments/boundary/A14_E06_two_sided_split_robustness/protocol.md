# A14_E06 Protocol: Two-Sided Same-Parent Split Robustness

> One-sentence falsification target: test whether E05's split effect survives
> when every parent is evaluated against equally weighted one-word left and
> right boundary shifts, removing the observed alternative-direction imbalance.

Status: **approved for direct execution by the user's blanket instruction on
2026-07-18**. This protocol was frozen after the E05 direction audit and before
any E06 representation was encoded.

## 1. Problem Definition

E05 held parent text and tokens fixed, but its closest alternative moved right
in 83--84% of test records. Pythia's effect was positive for right shifts and
negative for left shifts. E06 asks whether split specificity survives an
exactly balanced within-parent direction control.

Only naturally binary parents whose gold boundary has at least one word on
both sides after a one-word shift are eligible. For every eligible parent:

\[
b^- = b^{gold}-1,\qquad b^+ = b^{gold}+1.
\]

The parent and ordered token sequence are identical in the gold, left-shift,
and right-shift conditions.

## 2. Physical Priors

1. If an annotated boundary carries composition information beyond token
   containment and shift direction, a shared gold operator should outperform
   the equal-weight average of separately fitted left- and right-shift maps.
2. A result that only appears for one shift direction is compatible with
   position or child-length geometry and is not sufficient evidence for syntax.
3. The learned leaf subspace and ridge penalties must remain training-only.

## 3. Falsifiable Hypotheses

### H6a: Qwen direction-balanced split specificity

For validation-selected maps, Qwen's relative gold advantage over the
equal-weight two-sided control is at least 5%, with sentence-bootstrap lower
bound above zero.

### H6b: Pythia direction-balanced replication

Pythia meets the same criterion. This tests whether its positive E05 effect
survives removal of the direction imbalance; it is not a new primary model.

### H6c: model-general split specificity

Both H6a and H6b pass. Failure means the available evidence is model-specific
or direction-sensitive rather than a general tree-composition phenomenon.

### H6d: stability compatibility

At least one Qwen validation-eligible ridge point has two-sided split
advantage at least 5% and generic bound ratio below 1. This can only maintain,
not rescue, E05 H4.

## 4. Mathematical Model And Metrics

Use the same frozen leaf basis \(U\) and strict ordered output bottleneck as E05:

\[
\widehat h_p=\mu_p+U(B_Lz_L+B_Rz_R+b).
\]

Fit gold, left-shift, and right-shift maps separately. Define

\[
CE_{2s}=\frac{CE_-+CE_+}{2},\qquad
Adv_{2s}=\frac{CE_{2s}-CE_{gold}}{CE_{2s}}.
\]

At the row level, average the two alternative squared residuals before the
1,000-replicate sentence-cluster bootstrap. The 5% effect threshold, positive
confidence lower bound, ridge grid, 1.05 validation-eligibility tolerance, and
bound-ratio threshold 1 are inherited unchanged from E05.

## 5. Computational Realization

- Penn Treebank file split and frozen model revisions: identical to E05.
- Models: Qwen2.5-0.5B and Pythia-410m, each pretrained and identical random
  initialization.
- Training leaves: at most 8,192.
- Interior parent caps: 3,500 train, 500 validation, 480 test, sampled by whole
  sentence.
- Independent-span final EOS readout, BF16 forward, float64 analysis.
- Same-token, disjoint-file, sample-shape, and ridge-interior guards are
  mandatory.

## 6. Decision Rules

- **Robust support:** H6a, H6b, all guards, and the registered thresholds pass.
- **Refutation for a model:** its confidence upper bound is at or below zero.
- **Insufficient:** positive but sub-threshold/noisy, model disagreement,
  endpoint selection, or any guard failure.
- H6d failure preserves the existing conclusion that the recursive norm bound
  is empirically vacuous.

## 7. Claim Boundary

Passing would show only that two pretrained representations prefer a gold
treebank split over symmetric adjacent alternatives under a strict linear
probe. It would not show that Transformers internally execute this recursion,
that the tree is unique, or that natural language and world knowledge are
globally low-rank.

Failing or mixed results rule out a model-general claim for this measurement;
they do not prove that syntax is absent from the representations.

