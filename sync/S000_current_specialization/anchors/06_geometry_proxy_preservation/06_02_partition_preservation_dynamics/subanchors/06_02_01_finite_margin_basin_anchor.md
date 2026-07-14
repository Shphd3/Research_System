# A06_02_01 Finite-Margin Basin

Status: completed subanchor.

**Parent:** [`A06_02`](../06_02_partition_preservation_dynamics_anchor.md).

## Local Clause

An initialized partition is preserved only while each condition's route margin
remains inside a finite basin.

## Falsifiable Question

Does larger initial margin delay or prevent first boundary crossing under the
same training objective?

## Evidence And Verdict

Center tracking, feature-drift decomposition, forced crossing, robustness
replay, margin-budget audits, and noise-free full-slot controls show a
thresholded basin: sufficiently large positive margins stabilize, while small
positive margins can converge to negative values.

**Disposition:** retain as the core preservation fact.

**Boundary:** margin is a state variable, not an explanation of which gradient
term spends the budget.
