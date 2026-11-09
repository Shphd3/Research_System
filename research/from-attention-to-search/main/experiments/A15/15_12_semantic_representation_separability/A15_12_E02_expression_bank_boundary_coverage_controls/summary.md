---
experiment_id: A15_12_E02_expression_bank_boundary_coverage_controls
status: COMPUTATION_COMPLETE_BOUNDED
run: full-20260830T184100Z
human_result_confirmation: pending
---

# E02 Result Summary: Expression-Bank Boundary Coverage

## Conclusion

E02 partially closes and, crucially, localizes the main logical gap left by
E01. On the fixed 64 fact bundles,
C5E is linearly readable within its own held-out template split: every
`C5A -> C5B` layer has a positive observed all-task fifth-percentile margin,
with mean accuracy across the ten tasks between 99.1% and 100%. However, only
Blocks 4, 12, and 44 have a positive lower bound under the one simultaneous
band protecting all 48 regime-panel-layer cells. Blocks 20 and 36 have positive
point estimates but uncertified lower tails; Block 28 is especially fragile
and changes bottleneck sign under one leave-family-out deletion and across the
registered fixed penalties.

The decisive result is therefore not "C5E is non-separable." At Blocks 4, 12,
and 44, where both banks have certified within-bank readout while both
cross-bank directions fail, it is:

> A linear boundary learned from one expression bank is not a stable semantic
> boundary for the other bank, even though each bank is robustly readable from
> its own training split at those blocks.

At Blocks 20, 28, and 36, C5E remains highly accurate and has positive observed
low tails, but its simultaneous lower bound is not positive. E02 therefore
cannot assign the E01 failure there exclusively to boundary transfer; internal
low-tail fragility remains a live rival. Exposure to both banks can learn a
much more common boundary, but the repair is not uniform at every middle layer.

This result concerns fixed facts and a full 2,048-dimensional offline linear
learner. It does not establish unseen-fact semantic invariance, native Gate
use, expert utility, or language-model gain.

## Central Evidence

The registered statistic is the minimum fifth-percentile geometric margin over
the parent head, the global 64-way head, and all eight parent-conditional fine
heads. Positive lower bounds below use one studentized simultaneous band across
all 48 comparisons.

| Training regime | Evaluation panel | Robust blocks / 6 | Direct reading |
|---|---:|---:|---|
| C4A only | C4B | 5 | Strong same-bank readout; Block 36 is positive as a point estimate but not certified by the stricter E02-wide band. |
| C4A only | C5B | 0 | The E01 boundary never becomes cross-bank robust. |
| C5A only | C5B | 3 | C5E has strong internal readout, but middle-layer low tails are not uniformly certified. |
| C5A only | C4B | 0 | Reverse transfer also fails, so the incompatibility is not one-directional. |
| Matched two-bank training | C4B | 2 | With 896 rows and no sample-size advantage, only Blocks 4 and 44 are certified. |
| Matched two-bank training | C5B | 2 | The same two edge blocks are certified. |
| Full two-bank training | C4B | 5 | All except Block 36 are certified. |
| Full two-bank training | C5B | 5 | All except Block 28 are certified. |

The full two-bank regime therefore supplies one certified common boundary for
both panels at Blocks 4, 12, 20, and 44. This is a coverage-plus-more-data
result: it must not be attributed to bank coverage alone.

![All-task bottlenecks and simultaneous lower bands](figures/simultaneous_bottleneck_comparison.png)

## Mechanism Contrast

`C4A` and `C5A` each use 960 training rows. Switching from the C4-trained head
to the C5-trained head improves the C5B raw-unit bottleneck at all six blocks,
with every paired 95% interval above zero. The same switch worsens C4B at all
six blocks, with every interval below zero. Thus the same number of training
examples selects materially different bank-compatible boundaries.

Matched two-bank exposure also improves C5B over C4A at every block despite
having only 896 training rows, but it generally trades away C4B margin and does
not certify the four middle blocks. Full two-bank training strongly improves
C5B while mostly preserving the C4B boundary.

![Paired raw-unit margin contrasts](figures/paired_raw_margin_differences.png)

The permitted interpretation at Blocks 4, 12, and 44 is
**expression-bank-conditioned boundary incompatibility**. At Blocks 20, 28,
and 36 the result is weaker: bank-specific fitting improves the matching panel,
but C5E internal low-tail robustness is itself uncertified. "Boundary
rotation" is a possible geometric description, not a measured result here;
E02 does not estimate a unique rotation or prove a causal representation
mechanism.

## Stability and Audit

- Completion audit: passed.
- Models: 240 ledger entries, including 60 frozen E01 references and 180 new
  fitted heads; every main and fixed-penalty fit converged.
- Evaluation cells: 480; predictions: 138,240.
- Simultaneous bottlenecks: 48; paired raw-unit contrasts: 36.
- Fixed-penalty sign stability: 47/48. The only unstable cell is
  `C5A -> C5B`, Block 28.
- Leave-one-family-out sign stability: 47/48, with the same exceptional cell.
- Removing row-level atom-order overlaps changes no bottleneck sign in any of
  the three regimes whose training data contain C5A.
- The E02 fixed-`C=100` C4A reference reproduces all 120 frozen E01 task cells
  to a maximum absolute error of approximately `1.78e-15`.
- An independent recomputation rehashed 200 registered artifacts and reproduced
  all 48 observed bottlenecks, the simultaneous band, and all paired intervals;
  its receipt passed.

The E02 simultaneous band is stricter than E01's registered per-experiment
Bonferroni procedure. Consequently, C4A-to-C4B Block 36 has a positive observed
margin (`1.195`) but an E02-wide lower bound of `-0.326`. This does not
retroactively alter E01's registered verdict; it only governs E02's 48-cell
cross-regime comparison.

## Claim Boundary

### Established

Within the frozen checkpoint, fixed fact bundles, C4E/C5E metadata split, six
registered MLP/Gate-input blocks, and fitted full-space linear learner:

1. both expression banks contain strong same-bank multigranular semantic
   readout by accuracy and observed margin, while C5E simultaneous robustness
   is certified only at Blocks 4, 12, and 44;
2. neither single-bank boundary is certified in the opposite bank at any of
   the six layers;
3. two-bank exposure changes this trade-off, and full two-bank training yields
   a common certified boundary at four of six blocks;
4. Blocks 4, 12, and 44 specifically establish boundary-transfer failure as
   distinct from C5E internal unreadability;
5. the residual bottlenecks are predominantly parent-conditional fine tasks,
   not a separate failure unique to the global 64-way head.

### Not established

- intrinsic or universal linear non-separability;
- generalization to a different fact package;
- expression-bank coverage alone as the cause of the full-pooled repair;
- a measured rotation, low intrinsic rank, or a deployable low-budget Router;
- native Gate accessibility, top-k routing, expert utility, or LM improvement.

## Next Decision

Evaluate the 60 frozen E01 C4A probes on TAX-C4A, a different six-atom fact
package per leaf, without fitting or normalization on TAX-C4A. That experiment
determines whether the current evidence is fixed-fact expression readability or
extends to this one additional fact package. The TAX-C4A surface also changes
length and naturalness, so a failure will remain a joint-shift result rather
than a pure fact-identity effect.

## Evidence Links

- [Protocol](protocol.md)
- [Complete evidence record](detailed.md)
- [48-cell bottleneck table](tables/bottlenecks.csv)
- [Paired raw-unit contrasts](tables/paired_raw_margin_differences.csv)
- [Independent recomputation receipt](validation/independent_recompute.json)
- [Test receipt](validation/pytest.xml)
