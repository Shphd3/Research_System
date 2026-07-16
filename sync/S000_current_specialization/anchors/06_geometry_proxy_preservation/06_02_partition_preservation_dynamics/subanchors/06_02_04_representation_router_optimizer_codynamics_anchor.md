# A06_02_04 Representation-Router-Optimizer Co-Dynamics

Thinking Card source: [06_02_partition_preservation_dynamics_thinking_card.md](../06_02_partition_preservation_dynamics_thinking_card.md)
Status: completed mechanism subanchor.

**Parent:** [`A06_02`](../06_02_partition_preservation_dynamics_anchor.md).

## Local Clause

First boundary crossing is a coupled event involving Router-row motion,
hidden-state motion, and optimizer-preconditioned updates.

## Falsifiable Question

Which path is necessary for first crossing and which path enables recovery:
Router motion, representation motion, their coupling, or optimizer history?

## Evidence And Verdict

Freeze and intervention audits show that raw gradient norm alone does not
predict boundary pressure. Adam-style preconditioning changes the effective
direction and scale, while representation and Router updates can either
reinforce or cancel. Event-triggered recovery requires measuring these paths
at the crossing boundary.

**Disposition:** retain as the full preservation mechanism layer.

**Boundary:** the evidence is controlled and local; it does not establish a
general optimizer theorem for pretrained language models.
