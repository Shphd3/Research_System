# A06_02_03 Utility-Signed Local Dynamics

Status: completed mechanism subanchor.

**Parent:** [`A06_02`](../06_02_partition_preservation_dynamics_anchor.md).

## Local Clause

Router movement is governed by the signed utility difference between selected
and competing experts plus background pressure projected onto the routing
boundary.

## Core Model

For boundary direction $d=w_a-w_b$,

$$
\Delta m
\approx
-\eta\,d^\top g_{utility}
-\eta\,d^\top g_{background}.
$$

The sign of each projection decides whether a step restores or spends margin.

## Evidence And Verdict

Soft-routing, top-1 counterfactual, and background-bias experiments reject the
idea that background noise alone explains collapse. Expert advantage and
selection-dependent feedback determine whether correction is available.

**Disposition:** retain as the minimal local dynamics model.

**Boundary:** the approximation is local and does not yet include optimizer
state or representation drift.
