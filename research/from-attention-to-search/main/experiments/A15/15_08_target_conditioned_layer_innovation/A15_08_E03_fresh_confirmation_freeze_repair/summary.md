# Summary: A15_08_E03 Fresh-Confirmation Freeze Repair

Primary Anchor: [A15_08 Target-Conditioned Layer Innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)  
Frozen Protocol: [A15_08_E03_v1](protocol.md), SHA-256 `41b361d95975aa1f630055fe6b7ddd41f5b10753785c3cde8821e7e21c91a486`  
Detailed record: [detailed.md](detailed.md)  
Post-hoc conformance audit: [posthoc_protocol_conformance_audit.json](evidence/posthoc_protocol_conformance_audit.json)  
Result status / eligibility: `INELIGIBLE_GUARD`

## Conclusion First

E03 cannot carry the registered H2 or H1' conclusion. Its retained numerical
bundle is internally useful as a diagnostic, but a cold read found three fatal
departures from its frozen Protocol:

1. rows namespace `record_id` and `pair_id`, but use a numeric `episode` and
   contain neither the required namespaced `episode_id` nor `map_id`;
2. neither condition has the registered structured extraction success receipt
   with exact argv, interpreter, timestamps, environment, input/output hashes,
   and completion status;
3. the simple result archive contains only four scalar keys rather than the
   required episode/bootstrap arrays, and the 13-entry analysis manifest does
   not inventory the complete freeze-to-result chain.

The controlling label is therefore `INELIGIBLE_GUARD`, not `ELIGIBLE`. No
numerical value below may be used as confirmation evidence or as the source of
the A15 knowledge update.

[A15_08_E04](../A15_08_E04_strict_conformance_repair/summary.md) is the fresh,
conformance-only repair. It changes no scientific object, model, metric,
threshold, or control family; it uses new data and completes the missing
identity, receipt, array, and full-manifest contracts.

## Diagnostic Numerical Bundle

Had the guard been satisfied, the E03 complex-condition evaluator would have
returned `H2_PASS_H1_FAIL`:

| Quantity | E03 diagnostic estimate and paired 95% interval (nats/example) | Status |
| --- | ---: | --- |
| full residual-update gain \(G_{true}\) | +0.743018 [0.725404, 0.759395] | diagnostic only |
| same-dimensional state gain \(G_{state}\) | +0.729254 [0.711346, 0.745917] | diagnostic only |
| gain beyond balanced-mismatch q95 \(T_{cap}\) | +0.742678 [0.724672, 0.758767] | diagnostic only |
| two-direction gain \(G_2\) | +0.247688 [0.237605, 0.257467] | diagnostic only |
| 80% retention contrast \(D_{80}\) | -0.346726 [-0.357191, -0.335917] | diagnostic only |
| random-rank-two contrast \(T_{random}\) | +0.037900 [0.027142, 0.044516] | diagnostic only |
| TRAIN-label-permutation contrast \(T_{perm}\) | +0.226904 [0.216627, 0.237576] | diagnostic only |

These values motivated an exact repair because they suggested a stable local
existence effect and a clear rank-two failure. They do not establish either
claim.

## What Remains Reusable

The E02 TRAIN-only definitions frozen into E03 remain useful as design inputs:

\[
X=N_{25}(h),\qquad Z=N_{25}(h+a),\qquad U=Z-X,
\]

\[
R_U=U-\widehat{\mathbb E}_{lin}[U\mid X],\qquad
R_Y=Y_c-\widehat{\mathbb E}_{lin}[Y_c\mid X],
\]

\[
K_{new}=C_{UY}S_Y^+C_{UY}^{\top}.
\]

The common pooled basis remains a descriptive TRAIN-only location diagnostic.
None of these objects requires E03 eligibility. What fails is the attempt to
use the E03 confirmation bundle as registered evidence.

## Claim Boundary And Decision

**Can claim from E03:** the implementation produced a diagnostic bundle whose
point pattern justified a strict, fresh-data conformance repair.

**Cannot claim from E03:** local added accessibility, rank-two sufficiency or
failure, global low rank, adjacent-layer novelty, native use, expert utility,
or Router gain.

**Decision:** use only the fresh E04 record to adjudicate the unchanged H2 and
H1' gates. Do not retroactively amend E03 or pool its data with E04.
