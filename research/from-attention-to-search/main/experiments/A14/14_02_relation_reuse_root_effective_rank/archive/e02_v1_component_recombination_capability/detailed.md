---
experiment_id: A14_02_E02_component_recombination_capability
status: completed_fail
verdict: fail
run_id: a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1
job_id: pt-zecsxjd8
---

# Detailed Evidence: A14_02_E02 Component-Recombination Capability

## 1. Decision Loop

**Question:** Once every primitive component has appeared in training with
other partners, can NTP recombine two such components in a held-out pairing?

**Key comparison:** Shared algebraic composition versus an independent random
lookup control, with identical prefixes, pair split, answer marginals,
exposure, contexts, model, objective, and checkpoint-selection rule.

**Direct result:** Both conditions passed the seen-pair new-context gate in
5/5 seeds, but shared recombination passed in 0/5 seeds.

**Conclusion:** The registered task did not produce a robust reusable
component computation.

**Cannot claim:** The weak above-chance signal identifies an algorithm, or any
representation-rank or Router conclusion.

**Exactly one next decision:** Decide whether to park this synthetic surface
without running a downstream rank comparison.

## 2. Execution Provenance

| Item | Value |
| --- | --- |
| ACP state | `SUCCEEDED` |
| ACP job | `pt-zecsxjd8` |
| Run ID | `a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1` |
| Workspace / cluster | `share-space` / `share-cluster` |
| Quota | reserved |
| Hardware | 4 × NVIDIA H100 80GB HBM3 |
| ACP create / finish | 2026-07-23 17:32:42 / 17:36:26 UTC |
| Driver start / end | 2026-07-23 17:35:55 / 17:36:21 UTC |
| Completed jobs | 10/10 |
| Conditions × seeds | 2 × 5 |
| Python / Torch | 3.10.20 / 2.5.1+cu121 |
| Config SHA-256 | `08dc4ad39e9d5e041cc78850cb114ca710b5751b1b6aeeee82ba8b9589f48cc0` |
| Source revision | unavailable; exact source, config, per-job records, and logs are retained |

Remote unit tests passed 4/4. The remote smoke completed before the full
shards. All four GPUs were visible and all four shards completed.

## 3. Frozen Realization

### Generator

- Entities: $a\in\mathbb Z_{17}$.
- Components: $\alpha\in\{0,1,2,3\}$ and
  $\beta\in\{1,2,4,8\}$.
- Shared answer:
  $y=\beta(a+\alpha)\bmod17$.
- Lookup answer: one independent random permutation of $\mathbb Z_{17}$ per
  complete component pair.
- Held-out perfect matching:
  $(\alpha_0,\beta_1)$, $(\alpha_1,\beta_3)$,
  $(\alpha_2,\beta_0)$, and $(\alpha_3,\beta_2)$.
- Every component occurs in three remaining train pairs.
- Each seen relation uses eight train contexts, four calibration contexts,
  and four test contexts; these sets are disjoint.

The sequence is:

```text
[alpha] [entity] [nuisance-context] [beta] [ROOT] [ANSWER]
```

The generator audit passed all shape, prefix, answer-marginal, component
coverage, perfect-matching, and context-disjointness checks.

### Model and selection

- two-layer, one-head, width-64 causal Transformer;
- FF width 128;
- full-position NTP cross-entropy;
- maximum 6,000 steps, batch size 256;
- learning rate 0.002, no weight decay;
- checkpoint selected from seen-pair calibration only;
- no held-out-pair result influenced checkpoint or hyperparameter selection.

## 4. Ordered Evidence

### 4.1 Seen-pair capability

| Condition | Passing seeds | Mean test accuracy | Accuracy range |
| --- | ---: | ---: | ---: |
| `shared_components` | 5/5 | 0.9990 | 0.9951--1.0000 |
| `lookup_tables` | 5/5 | 0.9949 | 0.9779--1.0000 |

This guard rules out inability to fit the base mappings and inability to
ignore new nuisance contexts as explanations of the recombination failure.

### 4.2 Decisive recombination test

| Seed | Shared accuracy | Shared consistency | Lookup accuracy |
| ---: | ---: | ---: | ---: |
| 0 | 0.1691 | 0.9375 | 0.0331 |
| 1 | 0.0882 | 0.9228 | 0.0441 |
| 2 | 0.1654 | 0.9485 | 0.0515 |
| 3 | 0.1250 | 0.9338 | 0.0882 |
| 4 | 0.5147 | 1.0000 | 0.1029 |
| **Mean** | **0.2125** | **0.9485** | **0.0640** |

No shared seed met the frozen 0.80 accuracy gate. The result therefore
satisfies the preregistered `fail` rule once both conditions pass seen-pair
capability.

The shared-minus-lookup difference was positive in every paired seed, but the
shared result was highly variable and far below the registered operational
threshold. This descriptive pattern is retained as a weak signal, not promoted
to a compositional-algorithm claim.

### 4.3 Pair guard and leakage

| Held-out shared pair | Mean accuracy |
| --- | ---: |
| $\alpha_0,\beta_1$ | 0.1382 |
| $\alpha_1,\beta_3$ | 0.2147 |
| $\alpha_2,\beta_0$ | 0.2647 |
| $\alpha_3,\beta_2$ | 0.2324 |

All four values were below the 0.70 pair guard. No capability-passing lookup
seed exceeded the 0.20 leakage threshold.

## 5. Formal Gate Ledger

| Gate | Result | Interpretation |
| --- | --- | --- |
| Generator and matching | pass | All frozen construction checks passed |
| Job completion | pass | 10/10 completed |
| Shared seen-pair capability | pass | 5/5 |
| Lookup seen-pair capability | pass | 5/5 |
| Shared recombination | fail | 0/5 at accuracy 0.80 and consistency 0.95 |
| Held-out-pair guard | fail | 0/4 pair means reached 0.70 |
| Lookup leakage | pass | 0/5 exceeded 0.20 |
| Formal verdict | `fail` | Registered capability hypothesis rejected on this surface |

## 6. Central Figure Contract And Audit

![Capability before representation-rank interpretation](capability_before_rank.png)

- **Question:** Is failure caused by base capability, or specifically by
  unseen component pairing?
- **Metric and unit:** exact answer-token accuracy, proportion in $[0,1]$.
- **Data source:** the ten frozen condition-seed result records.
- **Aggregation:** each dot is one seed; black segment is the arithmetic mean.
- **Axes and legend:** left is seen-pair new-context accuracy; right is
  unseen-pair accuracy; dashed lines are registered gates; the dotted line is
  $1/17$ chance.
- **Allowed conclusion:** both conditions learned seen mappings, while shared
  recombination did not meet the capability gate.
- **Limitation:** the plot does not reveal mechanism and contains no rank
  measurement.
- **Rendered audit:** labels, gates, chance line, dots, and mean segments are
  visible; the legend does not obscure the observed points.

## 7. Artifact Map

### Curated evidence

- [English summary](summary.md)
- [Chinese summary](summary_cn.md)
- [Protocol](protocol.md)
- [Chinese protocol](protocol_cn.md)
- [Central figure](capability_before_rank.png)

### Worker evidence

Worker root:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/tree_low_rank/
```

Run root:

```text
results/a14_02_e02_component_recombination_capability/
a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1/
```

Key full-run artifacts:

```text
full/decision.json
full/capability_by_seed.csv
full/heldout_pair_accuracy.csv
full/generator_audit.json
full/jobs/*.json
full/checkpoints/*.pt
full/run_metadata_shard*.json
config_snapshot.yaml
```

Runtime logs:

```text
logs/acp/a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1/
```

Implementation:

```text
src/tree_low_rank/component_recombination_capability.py
scripts/run_component_recombination_capability.py
scripts/run_a14_02_e02_4gpu.sh
scripts/submit_a14_02_e02_4gpu_acp.sh
tests/test_component_recombination_capability.py
configs/a14_02_e02_component_recombination_capability.yaml
```
