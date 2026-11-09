# Summary: A15_13_E15 Gold-label layerwise static audit

Primary Anchor: [A15_13_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md)
Frozen Protocol: [protocol.md](protocol.md)
Detailed evidence: [detailed.md](detailed.md)
Result status: `FULL_RUN_COMPLETE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`
Registered typed verdict: `UNQUALIFIED_SHUFFLE_CONTROL`

## Result Snapshot

The unqualified primary estimate is exact and does **not** support staggered insertion: both the parent-domain readout and the true-parent-conditioned child readout first satisfy the registered three-block stability rule at zero-indexed block `9` on development and confirmation. The estimated gap is `0` blocks, its 2,000-bootstrap interval is `[0,0]`, and \(P(\ell_f-\ell_c\geq2)=0.000\) on both splits.

The registered experiment nevertheless fails full qualification. The confirmation conditional-child shuffled-label median cross-entropy is `1.148744` nats, while the allowed upper edge is \(\log 3+0.05=1.148612\); the excess is `0.000132` nats. Its shuffled accuracy is `0.313740`, and it has no stable shuffled onset. The development null and all parent null checks pass. Because the Protocol requires every null check to pass, block `9` remains a **provisional same-layer candidate**, not an approved Oracle-LoRA insertion decision.

## What Actually Ran

- One ACP SPOT worker, job `om-kqsc3ncy`, with one NVIDIA H100 80GB HBM3 GPU completed successfully with zero retries. No 5090, reserved quota, or multi-GPU fallback was used.
- Training was not staged. In one probe-fitting stage, all `6,353,788` readout parameters were trainable and all `596,049,920` Qwen3 parameters were frozen. The run made three fixed train passes, `768` optimizer updates, used 36 windows per update with four from each of nine cells, no accumulation, no scheduler, and final-update checkpoint selection.
- The stage jointly fitted independent linear real-label and shuffled-label heads, five smaller nested-budget head sets, fixed-width two-layer nonlinear heads, and three leave-one-child-out parent heads. Development was evaluated first; its rule, code, checkpoint, and subset hashes were written to `confirmation_freeze.json`; confirmation was then evaluated once.

## Primary Layer Estimate

Cross-entropy is first averaged inside each window and then balanced over the nine parent-child cells. Lower cross-entropy is better. Recovery is the registered fraction of the best across-layer improvement over random three-way prediction.

| Split | Task | First stable block | Bootstrap selection | 95% bootstrap interval | Block-9 CE | Block-9 balanced accuracy | Block-9 margin 5th percentile |
|---|---|---:|---:|---:|---:|---:|---:|
| Development | Parent | `9` | `1.000` | `[9,9]` | `0.471644` | `0.819519` | `-0.457606` |
| Development | Conditional child | `9` | `1.000` | `[9,9]` | `0.378842` | `0.857976` | `-0.520469` |
| Confirmation | Parent | `9` | `1.000` | `[9,9]` | `0.482906` | `0.812298` | `-0.582999` |
| Confirmation | Conditional child | `9` | `1.000` | `[9,9]` | `0.363137` | `0.864030` | `-0.266432` |

| Split | \(\ell_c\) | \(\ell_f\) | Gap | Gap 95% interval | \(P(\mathrm{gap}\geq2)\) |
|---|---:|---:|---:|---:|---:|
| Development | `9` | `9` | `0` | `[0,0]` | `0.000` |
| Confirmation | `9` | `9` | `0` | `[0,0]` | `0.000` |

![Primary linear recovery](figures/01_primary_linear_recovery.png)

How to read: the dotted vertical lines coincide at block 9 in both panels; both colors remain above the registered 0.95 line for blocks 9--11, so the selector finds no coarse-before-fine delay.

The negative 5th-percentile margins mean that at least 5% of balanced windows still contain positions for which the strongest wrong class beats the true class. The candidate is a population-level readout onset, not uniform per-window certainty.

## Linear Accessibility And Robustness

The two-layer `1024 → 32 → 3` nonlinear ceiling also first stabilizes at block `9` for both tasks and both splits. At block 9, its CE advantage over the linear head is only `0.013149/0.011629` nats for parent labels on development/confirmation and `-0.000588/+0.000090` nats for child labels. There is no earlier nonlinear-only layer hidden by the linear probe.

![Linear versus nonlinear](figures/02_linear_vs_nonlinear.png)

How to read: the linear and nonlinear curves nearly overlap, including around block 9; the added nonlinearity does not reveal a different depth transition.

All early, middle, and late position bins independently select block `9` for both tasks on both splits, so neither candidate is position-fragile. The parent candidate needs `25%` of train windows to recover 95% of its own full-data gain; the child candidate needs `50%` and is therefore sample-fragile under the registered `>25%` rule.

The parent leave-one-child-out readout has no stable layer in any fold or in their mean. At block 9 its mean CE is `1.280881` on development and `1.312866` on confirmation, both worse than random CE \(\log 3=1.098612\). Parent readability is therefore child-identity-fragile: it does not transfer to an unseen child within each parent under this test.

![Leave-one-child-out parent readout](figures/06_leave_one_child_out.png)

How to read: the standard parent curve is far below random CE, while every held-out-child curve stays at or above random; the ordinary parent signal may rely on the nine observed child identities rather than a transferable parent abstraction.

The block-9 held-out Fisher eigenvalue sums are `2.082556/2.013094` for parent and `4.477566/4.541372` for mean conditional child on development/confirmation. Parent-versus-child normalized subspace overlaps are only `0.0405`, `0.0797`, and `0.0684`; pairwise child-head overlaps are `0.0471`, `0.0236`, and `0.0263`. These are descriptive readout geometries: they show largely different fitted decision directions at the same depth, not a requirement for different insertion layers and not a LoRA-rank estimate.

## Qualification Failure

| Split | Task | Median shuffled accuracy | Median shuffled CE | CE minus \(\log3\) | Stable shuffled onset | Pass |
|---|---|---:|---:|---:|---:|---|
| Development | Parent | `0.298621` | `1.132845` | `+0.034232` | none | yes |
| Development | Conditional child | `0.316059` | `1.148097` | `+0.049485` | none | yes |
| Confirmation | Parent | `0.297037` | `1.133857` | `+0.035245` | none | yes |
| Confirmation | Conditional child | `0.313740` | `1.148744` | `+0.050132` | none | **no** |

![Shuffled-label qualification](figures/07_shuffle_control.png)

How to read: the upper row stays in the registered accuracy band and no shuffled curve has a stable onset, but the confirmation child CE median exceeds the shaded \(\log3\pm0.05\) band by `0.000132`; that single hard guard changes the registered verdict from descriptive “same layer” to “unqualified.”

## Claim Boundary And One Next Decision

**Can report descriptively:** with the frozen seed and readout contract, both real-label tasks peak sharply enough around block 9 to produce identical `[9,9]` bootstrap selectors; block 9 is position-robust, the child head is sample-fragile, and the parent head fails unseen-child transfer.

**Cannot promote as a qualified conclusion:** that block 9 is the selected LoRA insertion layer, that parent and child Routers should be co-located, or that the model natively uses these labels. This experiment did not train an online Router, did not add LoRA experts, did not intervene on expert function, and did not measure next-token gain.

**One proposed next decision, awaiting human confirmation:** decide whether to authorize one fresh-seed, independently trained repeat of this same static audit to adjudicate the `0.000132`-nat null-control miss. Until then, do not send block `(9,9)` into the matched-budget Oracle LoRA functional test.

## Evidence Map

- [Layerwise core metrics](tables/layerwise_core_metrics.csv)
- [Stable layers and bootstrap](tables/stable_layers_bootstrap.csv)
- [Candidate fragility](tables/candidate_fragility.csv)
- [Shuffled-label qualification](tables/shuffle_qualification.csv)
- [Geometry metrics](tables/geometry_metrics.csv)
- [Detailed run and repair ledger](detailed.md)
