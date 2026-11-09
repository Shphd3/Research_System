# Summary: A13_00_01_E01 Query-Conditioned Relay Carrier

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

## Result Snapshot

Verdict: **fail at the registered 1,000-step capability budget; objective
comparison remains blocked.**

What we established: the dataset and attention graph are valid, and the
one-layer relay control stays at chance (`0.0641` mean versus `0.0625`
chance). A one-layer bypass solves the same task in four of five seeds, so the
task is not generically blocked by the output interface.

What the experiment shows: the two-layer relay model learned partially but did
not satisfy the capability gate: mean held-out standard-head accuracy was
`0.7243`; only one seed exceeded `0.90`. The complete carrier verdict therefore
failed before any NTP/MTP comparison.

What we do next: change only the training budget from 1,000 to 3,000 steps and
replay the same task, masks, model, optimizer, seeds, and gates. This tests the
specific rival that E01 stopped during late, seed-dependent acquisition.

## Purpose

Test whether the fixed query-conditioned relay carrier is structurally valid,
learnable by a two-layer NTP model, and causally consumed by the standard head.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| carrier verdict | whether all validity gates pass | conjunction of six registered gates | Boolean | blocks invalid objective comparisons | MTP utility |
| relay condition | answer can read evidence only through position 4 | frozen sparse attention mask | path condition | tests two-stage formation/use | natural long context |
| bypass condition | answer directly reads values and selector | additional registered answer edges | path condition | verifies learner/interface capability | matched task difficulty |

## Exact Setup

Research question: can the two-layer NTP model solve unseen value-pair/selector
triples through the relay?

Data / model / objective: all 512 triples over 16 values and two selectors;
409 training and 103 held-out triples; width-64 four-head Transformer;
all-position NTP.

Conditions: one-layer relay, two-layer relay, one-layer bypass.

Changed variables: layer count and the registered answer-access path.

Held fixed: sequence, labels, split, vocabulary, width, optimizer, batch order,
1,000-step budget, and standard-head evaluation.

Seeds / checkpoints: seeds 1301--1305; step 0 and every 20 steps.

Paths: runner and raw outputs are listed in [detailed.md](detailed.md).

Known limitation: held-out triples reuse individual token identities and test
combination generalization, not unseen symbols.

## Primary Metric

Definition: \(C_{\mathrm{eligible}}=\bigwedge_{j=1}^{6}G_j\).

Unit: Boolean pass/fail/insufficient verdict.

Why it decides: any failed gate makes an objective comparison uninterpretable.

False-positive cost: high, because a false pass would turn capacity or shortcut
failure into a false MTP claim.

## Result

| Gate | Result | Verdict |
| --- | ---: | --- |
| graph and data validity | no split overlap; exact relay/bypass reachability | pass |
| two-layer relay capability | mean accuracy `0.7243`; 1/5 seeds above `0.90` | fail |
| one-layer relay depth control | mean accuracy `0.0641` | pass |
| one-layer bypass interface control | mean accuracy `0.9320`; 4/5 seeds at `1.0` | fail under the registered mean threshold |
| selected/unselected counterfactuals | follow `0.7359`; invariance `0.8350` | fail, downstream of capability |
| relay donor patch | different-label follow `0.4155`; same-label preservation `0.7243` | fail, downstream of capability |

The strongest capable seed reached `0.9320` clean accuracy and `1.0`
different-label donor follow. This is suggestive that the intended relay can
control the answer, but it cannot override the registered multi-seed failure.

## Key Evidence

The formal run and same-contract replay produced identical metrics; their CSV
files differ only in elapsed-time fields.

## Key Figures

### Figure: Carrier capability and structural depth controls

![Carrier capability and structural depth controls](figures/carrier_trajectory.png)

What this tests: whether one layer fails only when the relay is structurally
required, and whether two layers learn within the fixed budget.

Metric shown: held-out standard-head answer accuracy.

Metric unit: fraction correct.

Data source: five registered seeds, averaged at each 20-step checkpoint.

How to read: the one-layer relay curve should remain at chance; one-layer
bypass and two-layer relay should cross the `0.95` gate.

Observed result: the depth negative control behaved exactly as predicted, but
two-layer relay acquisition was late and seed-dependent; one bypass seed also
remained slow.

Allowed claim: the structural mask works, while the 1,000-step learner gate
does not.

What this does not prove: that longer training will pass, or that MTP is useful.

Anchor update implication: retain the carrier structure and test budget
insufficiency before changing the task or optimizer.

## Claim Boundary

Can claim: E01 rejects eligibility at 1,000 steps and localizes the failure to
capability/dynamic range rather than data leakage or a relay-mask shortcut.

Cannot claim: MTP failure, general two-layer impossibility, multi-evidence
composition, code/text transfer, or MoE value.

## Next Decision

Run the budget-only E02 replay. Do not add MTP, another task property, or a
larger model first.
