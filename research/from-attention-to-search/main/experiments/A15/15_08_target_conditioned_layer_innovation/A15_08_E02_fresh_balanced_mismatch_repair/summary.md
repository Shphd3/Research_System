# A15_08_E02 Fresh Balanced-Mismatch Repair — Result Summary

## Outcome

**Evidence qualification: `INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE`.**
The frozen arithmetic maps to `H2_PASS_H1_FAIL`, but E02 does not adjudicate
either hypothesis. Before writing its selection-freeze receipt, the analyzer
read CONFIRMATION labels and episode groups to materialize the 64 confirmation
mismatch banks. No confirmation loss, gain, direction, or hyperparameter was
used, but Protocol Sections 5 and 7 allowed pre-freeze confirmation-label use
only for the capability guard and made any other use ineligible.

The numerical result is therefore a strong diagnostic: it specifies the pattern
that a compliant fresh confirmation must retest, not a knowledge update that may
be promoted to the Anchor. Even after repair, any verdict remains local to one
answer-token transition, target, dataset, and linear readout family.

## Reconstructible Diagnostic Evidence

![E02 confirmation gates](figures/figure_e02_confirmation_gates.png)

For 128 complex confirmation episodes:

| Registered quantity | Estimate (nats/example) | Paired-episode 95% interval | Diagnostic reading |
| --- | ---: | ---: | --- |
| full residual-update gain \(G_{true}\) | +0.735082 | [0.715608, 0.756246] | H2 gate-1 pattern positive |
| same-dimensional \(Z\) versus \(X\) gain \(G_{state}\) | +0.721760 | [0.702151, 0.742898] | H2 state-gate pattern positive |
| true gain minus within-draw mismatch q95 \(T_{cap}\) | +0.734620 | [0.715064, 0.755466] | H2 control pattern positive |
| two-direction gain \(G_2\) | +0.238819 | [0.228856, 0.248747] | 32.49% of full point gain |
| \(D_{80}=G_2-0.8G_{true}\) | -0.349247 | [-0.362226, -0.336496] | H1' failure pattern |
| two directions minus random q95 \(T_{random}\) | +0.030400 | [0.020933, 0.037635] | non-null pattern |
| two directions minus label-permutation q95 \(T_{perm}\) | +0.219446 | [0.209049, 0.229597] | non-null pattern |

Independent reconstruction from the stored episode and bootstrap arrays matches
every estimate and interval to numerical precision. Thus the failure is not a
numerical discrepancy or hidden result selection; it is a frozen-contract data-
access violation.

## Why Valid Banks Still Do Not Make E02 Eligible

E01 used one global cyclic relabeling, which was invertible and still encoded
the target. E02 repaired that algebra: across each eight-episode block, every
target was paired exactly once with every source label, aggregate target-source
mutual information was zero, and the 64 controls' point q95 gain was only
+0.000462 nats/example. All bank arrays, split mappings, search budgets, and
mechanical guards were valid.

However, validity of the resulting maps is separate from when their labels were
opened. E02 constructed its confirmation maps before the selection freeze. The
Protocol explicitly required Stage S5 to use TRAIN/DEVELOPMENT only. That one
timing violation controls the evidence status even though no confirmation loss
or selection statistic leaked.

## Knowledge Boundary And One Next Decision

E02 supports a method lesson, not a scientific existence claim: a raw difference
is not knowledge. A defensible metric must remove the update part linearly
predictable from the old state and then require fresh held-out target improvement
beyond target-independent same-budget controls. E02's numerical pattern says
this metric deserves one clean repair; it does not establish H2 or reject H1'.

It cannot establish Shannon-information creation, adjacent-block novelty,
whole-representation rank, natural-language generality, native MLP use, expert
utility, or Router gain.

**Exactly one next decision:** run one fresh-confirmation eligibility repair
that hashes all TRAIN/DEVELOPMENT-selected models, directions, and label-free
confirmation-bank recipes before the new confirmation labels are opened. Only
its eligible verdict may decide whether a rank ladder is warranted.

Full conformance evidence and artifact lineage are in
[detailed.md](detailed.md).
