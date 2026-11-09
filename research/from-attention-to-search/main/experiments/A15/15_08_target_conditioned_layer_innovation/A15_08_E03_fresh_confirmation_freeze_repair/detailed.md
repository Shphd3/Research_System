# Detailed: A15_08_E03 Fresh-Confirmation Freeze Repair

Primary Anchor: [A15_08 Target-Conditioned Layer Innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)  
Frozen Protocol: [A15_08_E03_v1](protocol.md), SHA-256 `41b361d95975aa1f630055fe6b7ddd41f5b10753785c3cde8821e7e21c91a486`  
Summary: [summary.md](summary.md)  
Result eligibility: `INELIGIBLE_GUARD`

## 0. Direct Record

E03 was intended to repair E02's confirmation-label timing violation using a
fresh confirmation set. The numerical computation completed, but the retained
record does not conform to three explicit E03 Protocol clauses. Under the
registered rule that a missing required identity, receipt, array, or manifest
makes a scientific result ineligible, E03 is `INELIGIBLE_GUARD`.

This status is a record-qualification failure. It is not a re-interpretation
of E03's numerical values, and those values have not been changed. They remain
diagnostic only. The fresh [E04 strict repair](../A15_08_E04_strict_conformance_repair/detailed.md)
is the only record allowed to adjudicate the unchanged question.

## 1. Frozen Question And Objects

E03 asked whether, on fresh complex confirmation episodes, the part of one
layer-25 normalized attention write not linearly predicted from the pre-write
state adds held-out terminal-code accessibility beyond the old-state readout
and target-independent same-budget corrections; conditionally on that passing,
it asked whether two frozen target-conditioned directions retain at least 80%
of the full gain and beat equal-rank nulls.

The unchanged objects were

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

Subtraction is valid because \(X\) and \(Z\) share the same token, hook,
normalization, and hidden coordinate. It does not itself define new knowledge.
\(K_{new}\) is a supervised direction selector, not a knowledge covariance or a
Router.

## 2. Registered Metrics

All gains are nats/example under a frozen linear readout family:

- \(G_{true}=CE_X-CE_{X+R_U}\) is the full residual-update gain;
- \(G_{state}=CE_X-CE_Z\) is the same-dimensional state sign guard;
- \(G_2=CE_X-CE_{X+P_2R_U}\) is the gain from two frozen directions;
- \(T_{cap}=G_{true}-Q_{.95}^{higher}(G_{mismatch,1:64})\) compares the full
  update with target-independent same-budget corrections;
- \(D_{80}=G_2-0.8G_{true}\) is the registered rank-two retention gate;
- \(T_{random}\) and \(T_{perm}\) subtract, respectively, the within-draw q95 of
  64 random-rank-two and 64 TRAIN-label-permutation controls.

The complete eight-target episode is the independent unit. Intervals use 2,000
paired episode-bootstrap draws with seed 7281. These definitions survive as
design objects; E03's guard failure prevents their numerical outputs from
carrying a verdict.

## 3. Post-Hoc Protocol-Conformance Audit

The machine-readable audit is
[posthoc_protocol_conformance_audit.json](evidence/posthoc_protocol_conformance_audit.json).

| Frozen requirement | Retained E03 evidence | Finding | Eligibility effect |
| --- | --- | --- | --- |
| record, pair, map, episode, and generation IDs use the new namespace | rows contain namespaced `record_id` and `pair_id`; `episode` is numeric; `episode_id` and `map_id` are absent | Fail | fatal |
| each extraction stage has a structured success receipt with exact argv, interpreter, UTC bounds, environment, inputs/outputs, hashes, and status | only `simple/extraction_manifest.json` and `complex/extraction_manifest.json` exist; neither `extraction_receipt.json` exists | Fail | fatal |
| result archive retains all per-record, per-episode, per-control, and bootstrap arrays | complex arrays are detailed, but simple NPZ contains only `gain_true`, `gain_state`, `gain_top2`, and `d80` scalars | Fail | fatal |
| artifact manifest covers the registered chain | manifest contains 13 analysis outputs and omits direct freeze, data, extraction, and input inventory | Fail | fatal |

One fatal clause is sufficient for `INELIGIBLE_GUARD`; E03 has three groups of
fatal findings. The earlier `ELIGIBLE` label relied on the evaluator's narrower
internal audit and is superseded by this Protocol-level cold read.

## 4. Data And Artifact Facts

- full data SHA-256:
  `d3cd89b8640ab6374d4c4f1d6bde576a7e836babaf452234c4612cb1b442a5d4`;
- simple confirmation arrays SHA-256:
  `45a3046acc736cd6ca8285e80bb2e5cb5f2b46a191e63aa75df48b6abde5fffe`;
- 13-entry analysis manifest SHA-256:
  `89d4d03097eeed2e816ad81b0fb90d6b455fcc1d361b9453e36a79e492c7f91d`;
- 128 episodes and 1,024 records per condition were generated;
- E03's retained internal access-order and balanced-bank audits passed their
  implemented checks, but those checks did not cover the missing Protocol
  clauses above.

The original figures, arrays, tables, freeze records, and manifests are kept
unchanged so that the diagnosis is reproducible. No E03 artifact has been
silently repaired in place.

## 5. Diagnostic Results Only

Had the conformance guard passed, the E03 numerical bundle would have produced
the machine label `H2_PASS_H1_FAIL`:

| Quantity | Estimate | Paired 95% interval | Permitted use |
| --- | ---: | ---: | --- |
| \(G_{true}\) | +0.743018 | [0.725404, 0.759395] | stability diagnostic |
| \(G_{state}\) | +0.729254 | [0.711346, 0.745917] | stability diagnostic |
| \(T_{cap}\) | +0.742678 | [0.724672, 0.758767] | control-design diagnostic |
| \(G_2\) | +0.247688 | [0.237605, 0.257467] | rank-design diagnostic |
| \(D_{80}\) | -0.346726 | [-0.357191, -0.335917] | rank-design diagnostic |
| \(T_{random}\) | +0.037900 | [0.027142, 0.044516] | null-family diagnostic |
| \(T_{perm}\) | +0.226904 | [0.216627, 0.237576] | null-family diagnostic |

The two-direction point retention was 33.34%. These values justify rerunning
the exact design under a stricter evidence contract; they do not establish a
scientific result and must not be pooled with E04.

## 6. Repair Lineage

E04 changes only conformance:

1. it requires namespaced `episode_id` and `map_id` in addition to `record_id`,
   `pair_id`, and the exact generation ID;
2. both extraction stages write structured success or failure receipts;
3. both conditions retain record-, episode-, and bootstrap-level arrays;
4. a full manifest inventories the frozen Protocol/code, E02 inputs, freeze,
   fresh data, extraction, controls, arrays, metrics, figures, receipts, and
   audits;
5. it uses seed 8103 and wholly new episodes, and does not open E03 raw data
   after the E04 freeze.

This is not a new hypothesis or a favorable rerun selected after seeing E03.
The model, layer transition, residualizers, direction family, rank two, metric
definitions, bootstrap unit, thresholds, and null families remain fixed.

## 7. Claim Boundary And Decision

**Can claim from E03:** a diagnostic pattern was observed and a cold read found
specific evidence-contract defects that required a fresh conformance repair.

**Cannot claim from E03:** H2 Pass, H1' Fail, global low rank, adjacent-layer
novelty, nonlinear information creation, native use, expert utility, or Router
gain.

**Only next decision for this record:** read E04. Do not revise E03 artifacts,
retroactively rename its IDs, synthesize missing receipts, or use its values in
the final A15 knowledge update.
