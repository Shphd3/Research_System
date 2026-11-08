# Mathematical Mechanism Closure

Use when a mechanism is claimed to produce an observed or predicted outcome,
including claims made without equations, or when toy models, curves or
computational models explain that mechanism.
This extends the [audit contract](reasoning_audit_contract.md); it does not demand
closed-form theory or a new model for every empirical question.

## Check What Already Exists

Inspect the named current report and relevant existing derivation/Anchor/result
before declaring a gap. Separate these findings; several may coexist:

| Finding | Appropriate repair |
|---|---|
| No suitable model found in the inspected sources | State search/access limits; define the missing relation |
| Model exists but is absent or opaque in the report | Reconstruct its explanation, not a replacement experiment |
| Model exists but an empirical link is untested | Name that link and a discriminating test |
| Local model is valid but a broader decision is unsupported | State the missing comparison or assumption |
| Model and evidence answer the scoped question | Preserve the bounded answer; do not invent another gap |

A missing file, stale summary or inaccessible repository is not proof of absence.
Read source content, not its title. State what changed if an earlier audit was wrong.

## Follow The Actual Computation

Name the target outcome first: measured result or prediction, signed direction,
and local contribution or net effect. Keep these distinct throughout the audit.

For each consequential relation identify objects and dimensions, initial/frozen
state, model mapping, objective or observable, intervention/update rule and output.
The usual learning chain is input -> prediction -> loss -> gradient -> parameter
update -> another prediction/loss. Other models use their own valid chain.
Explain why each arrow follows and label it exact, approximate (with regime and
remainder), assumed, empirical or interpretive. Numerical simulation can close a
specified computation without proving its real-world applicability.

Distinguish parameter coordinates, matrix inputs, output representations, sparse
codes, and actual displacements. Do not substitute one for another. For example,
with fixed input and only a linear matrix updated, \(a=Wc\) implies
\(\Delta a=\Delta Wc\) exactly; loss changes still require the downstream map.
A scalar schematic illustrates possibilities; it cannot establish the high-dimensional
mechanism, feasibility, observed curve or experimental result.
Labels constructed to create a conflict demonstrate only that toy setting's
possibility, not the same effect in the actual model.

For learning models audit optimizer, normalization, aggregation and model state.
Single-sample factorization need not survive taking separate averages. A normalized
update does not imply a common learning rate across conditions. An identity test
checks implementation; an empirical proposition requires independent evidence.

Where they affect the claim, inspect units and normalization, limiting cases or
counterexamples, mean and covariance terms, optimizer history, and the difference
between a theoretical quantity and its finite-sample estimate. Resampling a fixed
gradient library does not create new independent documents or establish its
population mean. A variance contribution's sign depends on the downstream
curvature; positivity requires an assumption or evidence. Select the relevant
checks rather than returning a universal formula checklist.

## Locate The Empirical Obligation

Map the decisive term to a measured quantity, manipulation/comparison, held-fixed
conditions and surviving alternative. If changing geometry also changes the source
update or downstream sensitivity, do not attribute the whole contrast to geometry.
Use a fixed-source control or another justified identification strategy where feasible;
if factors cannot be isolated, state the identifiable joint claim.

A first-order attribution is not an intervention. Compare approximation error to
the particular component claimed; accuracy relative to a large total can conceal
an error larger than a small adverse component. Verify finite interventions when
claiming their finite effect, and distinguish representation edits from realizable
shared-parameter changes. A failed operationalization leaves other ones open.

## Match The Question Level

State whether the output is a formal result, descriptive relation, intervention
effect, unseen-data prediction or design decision. A broader population, time
horizon or use needs a justified bridge, assumptions and comparison appropriate
to its objective and resources. An open bridge neither invalidates the bounded
result nor makes the broader comparison the mandatory next project.

For example, a negative cross-update alone does not show separate experts train
better; that requires matched objectives, parameter/compute/data/update budgets,
initialization, useful transfer and a time horizon. This example is not a general
research sequence.

## Return Only The Decisive Finding

Give the existing source, exact gap type, smallest missing arrow and maximum
supported claim. If the original formula overreaches, give a usable conditional
model and its observable prediction where possible. Preserve what it explains
and locate the unsupported bridge rather than deleting the model. Propose a
separator only when needed, with support, non-support and insufficient outcomes.
Keep scientific decisions with the researcher. Explain
a local gap in the reply; use the explainer for a requested deeper explanation,
communication for a requested brief/Story/handoff, and the artifact owner for
canonical edits. Do not load another skill merely to restate the finding.
