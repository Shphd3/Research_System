# Thinking Card — Anchor 12_0 — Short-Range Single-Step versus Two-Step Composition

> Migrated from [12_0_short_range_single_vs_two_step_composition_anchor.md](12_0_short_range_single_vs_two_step_composition_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** A fixed finite rule table can be memorized and produced a threshold-sensitive exact-fit tail in E02. The target phenomenon is instead whether MTP reaches the same standard-head mastery level sooner than NTP when every example contains a newly generated local relation graph and the answer requires one or two ordered edge applications.

**Mechanism guess:** The standard $K=2$ second head places direct supervision for the final answer at `DECIDE`, two positions before `ANSWER_Y`. On a two-step example, that earlier answer signal may help the shared backbone learn the ordered relation-composition computation more than it helps a matched one-step lookup.

**Key variables:** task composition depth $c\in\{1,2\}$, objective $o\in\{\mathrm{NTP},\mathrm{MTP}\}$, separately eligible model depth $d\in\{2,4\}$, and a carrier plus mastery threshold frozen using NTP alone.

**Causal relation under test:** after the carrier, eligible model scales, and mastery threshold are frozen without MTP results, is MTP's reduction in standard-head steps-to-threshold larger for two-step than for one-step examples?

**Observable metric:** the first optimizer step at which the common standard next-token head reaches the same frozen answer-accuracy threshold on independent, newly generated test graphs.

**Rival explanations:** general benefit from an extra full-position loss, larger gradient dose, prediction of syntax or random fact tokens rather than composition, residual one-step/two-step difficulty mismatch, capacity floor or ceiling, and optimizer-step rather than wall-clock fairness.

**Decision:** first use NTP only to choose a fresh-graph workload that is stably learnable but not immediately saturated. Freeze the generator, eligible scales, accuracy threshold, seeds, and budget before any MTP result exists. If the capability gate later fails for either objective, stop without a composition-mechanism interpretation.
