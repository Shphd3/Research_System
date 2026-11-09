---
experiment_id: A15_11_E01H_qwen_native_router_access_gap_h100
status: MACHINE_EVIDENCE_COMPLETE
interpretation_status: HUMAN_CONFIRMED_AS_NON_OWNING_H100_SENSITIVITY
eligibility: E01H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY
completed: 2026-08-29
acp_job: pt-vkikyszj
run_id: full-20260829T172910Z
resource_profile: h100-4-reserved
---

# Summary: Qwen3-30B-A3B Native Router Accessibility Chain

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)

Frozen Protocol: [protocol.md](protocol.md)

Detailed record: [detailed.md](detailed.md)

Curated primary table: [primary_layer_metrics.csv](tables/primary_layer_metrics.csv)

Canonical worker result: [results.json](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/results.json)

Result status: `MACHINE_EVIDENCE_COMPLETE`. Eligibility is scoped to
`E01H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY`; the machine evidence is
complete under the frozen E01H Protocol, and the researcher accepted its
bounded interpretation as collision-isolated sensitivity evidence under the
current Focus. It is not an execution of the Focus's eight-RTX-5090 contract.

## Result Snapshot

**Registered machine verdict:**
`TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION`.

In the BF16 primary path, Blocks 4, 12, 20, and 28 satisfy all three required
conditions in both C4 and C5: the native Gate projection preserves parent-label
accessibility, top-8 selection causes a material accessibility loss, and the
resulting sparse route remains associated with the parent label above its
matched max-layer null. Block 36 fails only the strict projection-preservation
compound rule. Across the five confirmation blocks, the cross-panel counts are
therefore `4/5` projection-preserved, `5/5` material-selection-loss, `5/5`
retained-route-association, and `0/5` near-total sparse retention.

The FP32 sensitivity path independently returns the same four counts and the
same line verdict. Thus the verdict is not reversed by BF16/FP32 differences
near the eighth-versus-ninth expert boundary.

The bounded knowledge update is:

> For this frozen Qwen3-30B-A3B checkpoint, controlled C4/C5 data, fixed
> cross-fitted linear-probe family, and five registered blocks, most held-out
> eight-parent accessibility available in the native MoE input \(H\) remains
> available in Gate logits \(Z\). Converting \(Z\) to the native top-8 sparse route
> \(Q\) removes a large amount of that accessibility at every confirmation block,
> while \(Q\) still retains parent-label association above the registered null at
> every block. This is an accessibility-and-association diagnosis, not evidence
> of expert utility, causal native semantic use, or language-model benefit.

This E01H result came from the collision-safe reserved-H100 successor lane. It
does **not** execute or complete the current
[8×RTX5090 Focus](../../../../focus/focus_gradient_consistent_hierarchical_routing.md),
whose approved resource contract explicitly prohibits H100. Its eligibility is
relative only to the frozen E01H Protocol. The 8×RTX5090 E01/E03 owner has
completed its machine-evidence run and owns the A15_11 workstream's sole next
decision; E01H creates no second mainline next decision.

## Decision-Bearing Setup

- **Question:** where is held-out eight-parent linear accessibility lost along
  the exact frozen native chain \(H\rightarrow Z\rightarrow Q\)?
- **\(H\):** the 2,048-dimensional final-decision-token hidden vector received by
  the Qwen MoE MLP and its Gate.
- **\(Z\):** the 128 native bias-free Gate logits,
  \(Z=W_gH\), computed with BF16 \(H\) and BF16 Gate weights on H100.
- **\(Q\):** the 128-dimensional native sparse route: FP32 softmax of \(Z\), native
  top eight experts, selected weights renormalized to sum to one, and zeros at
  all unselected experts.
- **Balanced accuracy (BA):** mean held-out recall across the eight equally
  weighted parent classes; chance is \(1/8=0.125\).
- **Projection gap:** \(D_{proj}=BA(H)-BA(Z)\); **selection gap:**
  \(D_{select}=BA(Z)-BA(Q)\).
- **Chance-corrected retention:**
  \(R_Z=(BA(Z)-0.125)/(BA(H)-0.125)\) and analogously \(R_Q\); these values are
  empirical, dimensionless, and unclipped.
- **Held fixed:** rows, labels, A/B template-family cross-fit, train-only
  centering and regularization selection, probe family, scoring, layers, and
  bootstrap/null rules.
- **Known limitation:** C4 and C5 share semantic atoms and are required to
  agree, but they are not statistically independent replications.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Frozen inputs and native construction | all activation, metadata, split, checkpoint, and six Gate tensor hashes matched; exactly four H100-80GB devices | preflight passed | eligible | [preflight.json](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/preflight.json) |
| Complete prediction and metric matrix | 69,120 prediction rows; 12 BF16 metric rows; 12 FP32 rows; every registered cell valid | all 72 BF16 outer fits and all 2,520 inner-fold fits converged | complete | [predictions.csv.gz](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/predictions.csv.gz), [layer_metrics.csv](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/layer_metrics.csv) |
| Hidden accessibility admission | all ten BF16 confirmation cells have \(BA(H)=0.994792\)--\(1.000000\), above panel null thresholds 0.171354 and 0.175000 | 1,000 matched label-null draws; max over five confirmation layers | pass | [null_ledger.json](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/null_ledger.json) |
| Projection preserved | both panels pass at Blocks 4/12/20/28; Block 36 fails | requires lower 95% bound \(R_Z\ge0.90\) and upper 95% bound \(D_{proj}\le0.05\) | `4/5` | [primary table](tables/primary_layer_metrics.csv) |
| Material selection loss | both panels pass at all five blocks | lower 95% bound \(D_{select}\ge0.10\) | `5/5` | [bootstrap ledger](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/bootstrap_ledger.json) |
| Retained route association | both panels pass at all five blocks | \(I_Q(Y;E)/H(Y)\) exceeds matched max-layer 97.5th-percentile null | `5/5` | [null ledger](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/null_ledger.json) |
| Near-total sparse retention | no confirmation block passes in both panels | lower 95% bound \(R_Q\ge0.90\) | `0/5` | [primary table](tables/primary_layer_metrics.csv) |
| BF16/FP32 qualitative stability | FP32 gives the same `4/5, 5/5, 5/5, 0/5` profile | different line verdict would make E01H insufficient | pass | [FP32 sensitivity rows](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/fp32_sensitivity_layer_metrics.json) |
| Pilot exclusion | Block 44 is present but marked `PILOT_NOT_BLIND` in C4 and C5 | excluded from confirmation layers, counts, and line verdict | pass | [results.json](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/results.json) |

## Key Evidence

The ladder shows the central location result: \(H\) and \(Z\) remain near-perfect
under the registered readout, while \(Q\) falls to roughly 0.40--0.56 on the five
confirmation blocks. Error bars are paired complete-template-family bootstrap
95% intervals. The dotted line is eight-way chance; the gray Block 44 band is
pilot-only.

![Held-out parent balanced-accuracy ladder](figures/balanced_accuracy_ladder.png)

The paired gaps isolate the two interfaces. The BF16 selection-gap lower 95%
bounds are 0.411458--0.544792, all well above the registered 0.10 material-loss
threshold. Projection gaps are much smaller; only Block 36 fails the stricter
preservation rule because its upper interval crosses 0.05 in both BF16 panels.

![Projection and top-8 selection gaps](figures/accessibility_gaps.png)

All decision-bearing BF16 values, including the two panel-specific route-null
thresholds and four Boolean criteria, are in the
[curated primary table](tables/primary_layer_metrics.csv). Full-precision
values and fit diagnostics remain in the worker `layer_metrics.csv`.

## Claim Boundary

### Can claim

- the registered BF16 and FP32 analyses agree on the typed accessibility
  profile for this checkpoint, dataset, readout family, and fixed layers;
- the Gate projection preserves the registered parent accessibility at four of
  five confirmation blocks in both panels;
- the top-8 operation produces material held-out accessibility loss at all five
  blocks, while the resulting route retains parent-label association above its
  matched null at all five;
- Block 36 shows enough projection loss to fail the strict preservation rule,
  but `0/5` blocks meet the separate Gate-projection-bottleneck lower-bound
  rule.

### Cannot claim

- that the native Router causally uses parent semantics rather than carrying a
  correlated route pattern;
- that the selected experts are counterfactually useful or functionally
  appropriate;
- that this routing improves Qwen prediction, language-model NLL, training
  efficiency, or sample efficiency;
- that Qwen pretraining produced the pattern through the proposed A15_11
  gradient mechanism;
- that C4/C5 are independent replications or that the result generalizes to
  other checkpoints, datasets, labels, or probe families;
- that E01H completes the current 8×RTX5090 synthetic/Qwen Focus or authorizes
  a Router intervention.

## Next Decision

**Decision:** E01H is admitted as non-owning H100 sensitivity evidence. The
sole A15_11 next decision is to freeze a frequency (high/low) by cross-child
gradient-consistency (high/low) representation-formation test before another
Router intervention.

**Completion criterion:** the successor contract holds total tokens, target
positions, parent/child counts, vocabulary, templates, and label entropy fixed
and defines frozen measurements for gradient consistency, parent between-class
energy, held-out fifth-percentile normalized margin, and discriminant-subspace
spectral location.

**Resume action:** retain E01H only under the non-owning sensitivity label and
use the current Focus/Anchor to design the \(2\times2\) successor. Do not create a
second E01H decision, reinterpret accessibility as utility, or launch a Qwen
intervention before a new confirmed Anchor and Protocol.
