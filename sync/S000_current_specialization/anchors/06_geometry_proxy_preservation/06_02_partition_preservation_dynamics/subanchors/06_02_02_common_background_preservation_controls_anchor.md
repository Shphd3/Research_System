# A06_02_02 Common And Background Preservation Controls

Thinking Card source: [06_02_partition_preservation_dynamics_thinking_card.md](../06_02_partition_preservation_dynamics_thinking_card.md)
Status: completed subanchor.

**Parent:** [`A06_02`](../06_02_partition_preservation_dynamics_anchor.md).

## Local Clause

Common/background components may consume route margin, but subtracting them is
not sufficient to create or preserve distinct feature-expert bindings.

## Falsifiable Question

Do common subtraction, residual projection, denoised routing, row projection,
reduced Router learning rate, or early freeze preserve the supplied partition?

## Evidence And Verdict

Toy and Transformer controls show that these interventions can reduce
concentration or slow drift, yet they do not robustly maintain feature-level
specialization under the full-sequence objective. Signal removal can also
discard route-discriminative components.

**Disposition:** retain as preservation controls; do not treat common removal
as the main method.

**Boundary:** the tested controls do not separate Router motion from
representation motion and optimizer history by themselves.
