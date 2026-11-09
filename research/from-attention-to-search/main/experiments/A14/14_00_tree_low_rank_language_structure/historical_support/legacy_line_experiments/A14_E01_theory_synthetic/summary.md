# A14_E01 Summary: The Conditional Propagation Bound Is Correct but Often Loose

## Direct Result

**Verdict: pass for the theorem/implementation audit.** Across 809 registered
conditions and 5,663 layer records, the maximum normalized violation was
\(2.92\times10^{-8}\), below the \(10^{-5}\) threshold. Exact rank-\(8\) conditions
had maximum relative tail error \(2.83\times10^{-8}\), below \(10^{-6}\). All 17
deterministic counterexample checks passed.

This establishes that the implemented recurrence

\[
B_{\ell+1}=\|A_\ell\|_2\|W_\ell\|_2B_\ell+
\|E_{\ell+1}\|_F
\]

upper-bounds the best rank-\(k\) error in the registered finite matrices.

## What the Stability Sweep Shows

The bound was non-vacuous, \(B_\ell/\|H_\ell\|_F<1\), in 75.9% of noisy layer
records, but strong enough to certify 95%-energy rank at most \(k\) in only
37.5%. At the root, median bound ratio rose from 0.50 with zero leaf noise to
3.35 with leaf noise 0.1. Thus theorem validity and empirical explanatory
power are distinct.

![Actual error and recursive bound](bound_vs_actual.png)

The root tail-energy sweep confirms that innovations and off-subspace leaf
noise, not tree structure alone, control approximate rank.

![Root tail-energy sweep](root_tail_energy_heatmap.png)

## Boundary

E01 proves no premise about real language, syntax trees, or pretrained models.
It only validates the conditional matrix theorem and shows that node-specific
operators, orthogonal innovations, summation gain, and DAG reuse can break or
weaken its intended low-rank interpretation.

## Next Decision

Test whether real short constituents satisfy a shared held-out subspace premise
without using a Transformer representation.

