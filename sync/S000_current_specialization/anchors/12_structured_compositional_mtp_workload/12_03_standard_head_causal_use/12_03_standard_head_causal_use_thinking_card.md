# Thinking Card — Intermediate-State Causal Use By The Standard Head

> Migrated from [12_03_standard_head_causal_use_anchor.md](12_03_standard_head_causal_use_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** A11 shows that informative future supervision can create an
earlier task signal, but readable information and private future-head accuracy
do not show that the ordinary next-token head uses an intermediate
compositional state.

**Mechanism guess:** After one shared checkpoint already solves the depth-two
task, informative Next-2 strengthens an intermediate-state component $B$ that
survives the shared format-token transition and causally controls the standard
answer $Y=\pi_2(B)$.

**Key variables:** task-gate accuracy, cross-fitted intermediate-state
subspace, counterfactual standard-head effect, matched random-subspace effect,
and clean standard-head accuracy.

**Observable metric:** the NTP-to-MTP change in counterfactual control of the
standard head that is specific to the $B$ subspace.

**Decision:** test causal use only after the shared capability gate passes;
otherwise stop without interpreting probes or patches.
