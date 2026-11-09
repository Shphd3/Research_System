# A15_08_E01 Layer-25 Conditional Innovation — Result Summary

## Outcome

**Evidence qualification: `PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN`.** The run
completed and its frozen arithmetic maps mechanically to
`H2_INSUFFICIENT_H1_NOT_ADJUDICATED`, but the primary cyclic control preserved a
globally learnable one-to-one target code. It therefore did not instantiate the
registered target-independent capacity rival. E01 does not adjudicate whether
the layer-25 transition adds target accessibility, and H1' remains unjudged.

This is not a claim that no increment exists. It is a concrete measurement
update: a positive old-plus-update readout gain is not sufficient when an
equally parameterized, invertibly relabeled update performs just as well.

## Decisive Evidence

![E01 confirmation gains](figures/figure_confirmation_gains.png)

For the complex two-hop condition on 128 fresh confirmation episodes:

| Registered quantity | Estimate (nats/example) | Episode-bootstrap 95% interval | Reading |
| --- | ---: | ---: | --- |
| raw-update gain \(G_{full}\) | +0.661428 | [0.646973, 0.675533] | bounded positive sequential-readout observation |
| cyclic-control gain \(G_{shuffle}\) | +0.688412 | [0.673629, 0.703148] | control retains a learnable relabeling |
| true minus cyclic \(T_{shuffle}\) | -0.026983 | [-0.030384, -0.023705] | registered H2 conjunction does not pass |
| same-dimensional \(Z\) versus \(X\) gain | +0.686176 | [0.672119, 0.700464] | bounded accessibility observation; not an H2 rescue |
| two-direction gain \(G_2\) | +0.225890 | [0.215740, 0.235682] | descriptive only because H2 is unresolved |
| \(D_{80}=G_2-0.8G_{full}\) | -0.303253 | [-0.313918, -0.292715] | additionally uses mismatched full/top-two objects |

The control failure is algebraic. TRAIN, DEVELOPMENT, and CONFIRMATION all use
the same cyclic map \(y\mapsto y+1\) and fit a dedicated correction. The map is
invertible, so a readout can learn \(y+1\mapsto y\); the control has not removed
target information. A read-only post-hoc root-cause check with split-independent
episode-randomized offsets reduced the control gain to approximately zero, but
that check is diagnostic only and cannot replace the registered result.

The H1' comparison also cannot be interpreted: \(G_{full}\) used raw \(U\), whereas
\(G_2\) used the residualized update \(R_U\), and its nulls did not receive the real
direction's full four-\(\rho\) selection budget. H1' therefore stays
`NOT_ADJUDICATED`, irrespective of the descriptive numbers.

## Validity And Bounded Observations

All non-construct guards passed: 5,120 records were complete and balanced;
restricted-choice confirmation accuracy was 99.12% for simple and 77.73% for
complex; replay, `o_proj` identity, and stored-difference errors were zero. The
TRAIN-only common coordinate had orthogonality error \(7.53\times10^{-7}\), exact
trace reconstruction at reported precision, and covariance-identity errors at
\(1.29\times10^{-15}\)--\(1.41\times10^{-15}\).

The bounded observations are therefore real properties of these fitted
readouts, but they do not answer H2: raw-\(U\) sequential gain is positive, and a
same-dimensional readout of \(Z\) outperforms one of \(X\). Neither observation by
itself separates added target accessibility from reparameterization or added
readout capacity.

## Claim Boundary And One Next Decision

E01 does not establish information-theoretic novelty, adjacent-layer novelty,
whole-representation low rank, native MLP use, expert utility, or Router gain.
It also does not show absence of any of these properties.

**Exactly one next decision:** execute the independently frozen
[A15_08_E02 fresh balanced-mismatch repair](../A15_08_E02_fresh_balanced_mismatch_repair/protocol.md).
E02 uses wholly new episodes, makes full and rank-two comparisons share \(R_U\),
uses exactly target-independent balanced control banks, matches null selection
budgets, and adds a same-dimensional \(X\) versus \(Z\) gate.

Full conformance, failure history, numerical lineage, and artifact paths are in
[detailed.md](detailed.md).
