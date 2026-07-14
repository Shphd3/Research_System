# A06_00_01 Operational Definition And Failure Evidence

Status: completed subanchor.

**Parent:** [`A06_00`](../06_00_functional_specialization_contract_anchor.md).

## Local Clause

Feature specialization means that inputs requiring different conditional
computations are routed to experts that provide different held-out utility. A
cluster, balanced load, or stable route is not sufficient by itself.

## Falsifiable Question

Do synthetic slot and context tasks establish that route partitions can be
measured independently from expert utility?

## Evidence And Verdict

The controlled tasks expose route collapse, context dominance, and feature
partition failure under top-1 routing. They establish valid failure metrics,
but do not establish functional specialization because the best expert for
each condition is not identified by counterfactual held-out loss.

**Disposition:** retain as the operational failure baseline. Do not use it as
positive evidence that semantic or functional experts formed.

**Boundary:** synthetic identities are evaluation labels, not deployable
Router supervision.
