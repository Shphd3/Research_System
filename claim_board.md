# Claim Board

Last updated: 2026-05-07

Use this board before reports and meetings. Do not present a claim more strongly than its current status.

Status labels:

- `supported`
- `weakly supported`
- `unsupported`
- `contradicted`
- `unclear`

## Claim A: Feature-Zipf synthetic data is more reasonable than leaf-Zipf data.

Status: supported.

Evidence: Zipf acts on sparse feature occurrence rather than directly on labels. This better matches a common/group/unique feature view of language.

Meeting boundary: say this is a better controlled diagnostic setting, not a full simulation of natural language.

## Claim B: The synthetic mechanism is recoverable.

Status: supported.

Evidence: Oracle flat and oracle hierarchical models reach Leaf NMI 1.000 and high feature selectivity. Oracle hierarchical conditional input reaches function cos 0.973 in the variable-A setting.

Meeting boundary: oracle proves recoverability, not that learned routing already solved it.

## Claim C: Learned routers exploit sparse feature signal.

Status: weakly supported.

Evidence: Learned models beat random flat on loss in variable-A and show modest improvements in Leaf NMI and feature selectivity.

Meeting boundary: the signal is real but weak; it is not yet clean mechanism recovery.

## Claim D: Hierarchical MoE is better than flat MoE at sparse feature specialization.

Status: unsupported.

Evidence: Hierarchical models do not clearly beat flat middle spectral + common on Leaf NMI or sparse dictionary feature division metrics.

Meeting boundary: do not claim hierarchy is better at sparse feature division yet.

## Claim E: Hierarchical MoE is better at function-level mechanism recovery.

Status: weakly supported.

Evidence: In variable-A, Hier conditional input has the highest learned function cos among non-oracle models, and oracle hierarchical has much higher function cos than oracle flat.

Meeting boundary: say function-level signal is stronger than feature-level signal, not that the architecture is solved.

## Claim F: Middle spectral routing helps sparse feature division.

Status: supported by current synthetic diagnostics.

Evidence: Flat middle spectral + common has the best learned Leaf NMI and strongest sparse dictionary division metrics among learned models.

Meeting boundary: this is currently the strongest diagnostic phenomenon and should become a target of explanation.

## Claim G: Fixed-A feature selectivity proves expert functional specialization.

Status: unsupported.

Evidence: In fixed-A, all models have the same output function, so function cos is essentially identical. Fixed-A only shows that input features can induce weak routing differentiation.

Meeting boundary: fixed-A is a control, not proof of functional expert specialization.
