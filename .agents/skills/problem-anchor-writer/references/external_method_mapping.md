# External Design-Workflow Mapping

Use only when importing or comparing the named external workflow. This mapping
does not require installing or executing that workflow.

## Correspondence With `research-exploration-skill`

This Anchor satisfies that method's `design.md` role. The mapping below is
fixed: do not rename Anchor sections to match an external document, and do not
create a parallel `design.md`.

| `design.md` section | Anchor section |
|---|---|
| 1. Problem Definition | `1. Problem Definition` |
| 2. Physical Priors | `2. Physical Priors` |
| 3. Mathematical Model | `4. Mathematical Model` |
| 4. Related Work and Computational Design Decisions | folded into `5. Computational Realization`, which states the sourced adopt/adapt/baseline/reject decision |
| 5. Computational Implementation | `5. Computational Realization` |
| 6. Experiments and Iterative Evidence | `6. Minimal Falsification Tests` together with `7. Current Evidence` |

Two Anchor sections have no `design.md` counterpart because that method carries
their function elsewhere. `3. Falsifiable Hypotheses` is retained here because
the primary hypothesis, the strongest live rival, and the separating outcome
must be adjudicated inside the design. `8. Claim Boundary And Next Decision`
carries the bounded claim and the exactly-one next decision that the method
requires of every active question.

**Question hierarchy is owned here, not by that method.** Where
`research-exploration-skill` describes a `docs/research_map.md` tree, a
`docs/problems/<ID>/` layout, and evidence propagation between parent and child,
this repository keeps its own rule instead: a parent Anchor owns one complete
major research problem, a subanchor inherits the parent question and adjudicates
one local clause, and sibling parents are distinguished from parent-child
ownership by the line `README.md`. Do not create a parallel question tree, a
`research_map.md`, or a `design.md` to satisfy that method.
