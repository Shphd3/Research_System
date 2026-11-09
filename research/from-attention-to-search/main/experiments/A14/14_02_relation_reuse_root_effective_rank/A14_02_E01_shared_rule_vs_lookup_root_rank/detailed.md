---
experiment_id: A14_02_E01_shared_rule_vs_lookup_root_rank
status: completed_insufficient
verdict: insufficient
run_id: a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427
job_id: pt-q6hu0fq5
---

# Detailed Evidence: A14_02_E01 Shared Rules Versus Lookup Root-State Rank

## 1. Decision Loop

**Question:** At matched exact-relation frequency, rule-token count, context
pool, output marginal, model, and task utility, does a shared compositional
family require fewer final root-state directions than independent lookup
mappings?

**Decisive experiment:** Train matched shared and lookup synthetic NTP tasks,
intervene on the post-final-normalization `ROOT` state, and find the minimum
calibration-learned subspace that preserves held-out answer loss and accuracy.

**Direct result:** The low-exposure primary pair failed held-out capability, so
the registered rank contrast cannot be adjudicated.

**Conservative conclusion:** Context diversity, not repetition alone, enabled
new-context utility. In capability-passing lookup controls, independent mapping
cardinality was associated with a small monotone increase in functional root
rank.

**Cannot claim:** Shared composition causes low root rank, the model learned
the shared algorithm, or this mechanism generalizes to natural language or
Router design.

**Exactly one next decision:** Decide whether to add a capability-only
calibration stage before any revised rank comparison.

## 2. Execution Provenance

| Item | Value |
| --- | --- |
| Remote platform state | `SUCCEEDED` |
| ACP job | `pt-q6hu0fq5` |
| Run ID | `a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427` |
| Hardware | 4 × NVIDIA H100 80GB HBM3 |
| Start / end | 2026-07-23 14:31:43 / 14:35:13 UTC |
| Completed jobs | 35/35 |
| Conditions × seeds | 7 × 5 |
| Python / Torch | 3.10.20 / 2.5.1+cu121 |
| Config SHA-256 | `c74f9cde067edded4a9a5e2a863a3c2a7100e147399bcb7b179086131b1f1ec6` |
| Manifest source revision | `unavailable`; run used the recorded config and local source tree |

The unavailable Git revision is a provenance limitation. The exact config,
source, local tests, logs, and produced result files remain linked below.

## 3. Frozen Realization

### Data

- Finite field size: 17.
- Shared family: 16 parameter-pair rules with
  \(u=(a+\alpha)\bmod17\) and \(y=\beta u\bmod17\).
- Lookup family: random permutations with the same entity, rule-token, answer,
  sequence, split, and context manifests.
- High exposure: eight occurrences per exact relation.
- Calibration and test each used four unseen nuisance contexts per seen
  relation.
- Sequence: `[alpha, entity, context, beta, ROOT, ANSWER]`.

The generator audit passed all exact checks:

- primary train samples: 256;
- primary calibration samples: 1,024;
- primary test samples: 1,024;
- repeat train samples: 2,048;
- paired prefixes and answer marginals were exact.

### Model and training

- Two-layer, one-head causal Transformer;
- hidden width 64 and FF width 128;
- full-position next-token CE;
- maximum 6,000 steps, batch size 256;
- five paired seeds;
- capability checkpoint selected on calibration only:
  accuracy at least 0.95, CE at most 0.10 nat, three consecutive evaluations.

### Functional-rank intervention

- Primary state: final `ROOT` after final normalization and before the LM head.
- Secondary state: final `ROOT` before normalization.
- Calibration-only task-aware orthogonal basis.
- Frozen loss tolerance: 0.02 nat.
- Frozen accuracy-drop tolerance: 0.01.
- Frozen minimum shared advantage: four directions.
- Thirty-two equal-rank random subspaces per run.

## 4. Ordered Result Audit

### 4.1 Generator and completion gates

The generator and seed-completion gates passed. All 35 runs generated a
checkpoint/result record and all paired primary manifests matched.

### 4.2 Primary capability and utility gates

| Condition | Train accuracy | Calibration accuracy | Test accuracy | Test CE | Capability |
| --- | ---: | ---: | ---: | ---: | ---: |
| `shared_unique` | 1.000 | 0.118 | 0.179 | 9.907 | 0/5 |
| `lookup_unique` | 1.000 | 0.099 | 0.088 | 11.184 | 0/5 |

Both conditions memorized the one observed surface per exact relation but did
not acquire invariance to new context tokens. Consequently:

1. capability failed;
2. matched full-state held-out utility failed;
3. the primary shared-versus-lookup rank difference is undefined for the
   registered scientific question.

The raw `decision.json` reports a `-36`-direction contrast because the
functional-rank routine still emitted values for incapable runs. This number
must not be used as evidence.

### 4.3 Frequency versus context diversity

| Shared condition | Exposure | Context allocation | Capability | Mean test accuracy |
| --- | ---: | --- | ---: | ---: |
| `shared_unique` | 1 | one observed context | 0/5 | 0.179 |
| `shared_repeat_duplicate` | 8 | exact same context repeated | 0/5 | 0.199 |
| `shared_repeat_diverse` | 8 | eight distinct contexts | 4/5 | 0.991 among passes |

Repeating the identical context eight times barely changed new-context
accuracy. Diverse exposure changed capability qualitatively, although one
shared seed still failed training. This isolates a nontrivial distinction:
frequency supplies update count, but varied nuisance contexts are needed here
to learn that context is irrelevant.

### 4.4 Lookup-cardinality control

All 15 lookup-cardinality runs passed capability and achieved 1.0 test
accuracy.

| Unique lookup tables | Post functional rank, mean ± SD | Pre functional rank | PCA functional rank | Entropy effective rank | \(r_{95}\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 10.2 ± 0.45 | 9.4 | 10.8 | 13.14 | 13.0 |
| 4 | 11.0 ± 0.00 | 8.6 | 11.4 | 19.57 | 24.0 |
| 16 | 12.8 ± 0.84 | 11.6 | 14.2 | 25.97 | 34.2 |

The number of surface rule IDs, exposure, total examples, answer set, and
context allocation stayed fixed; `K` changed the number of distinct
permutation tables assigned across the 16 rule IDs. The observed monotone
functional-rank increase is therefore valid within this generator. It remains
a three-point synthetic relationship, not a universal lookup-rank law.

### 4.5 High-exposure shared versus lookup

`lookup_repeat_diverse` passed in 5/5 seeds. `shared_repeat_diverse` passed in
4/5. For the four paired passing seeds:

| Seed | Shared rank | Lookup `K=16` rank | Lookup − shared | Shared composition accuracy |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 9 | 13 | 4 | 0.547 |
| 2 | 11 | 14 | 3 | 0.063 |
| 3 | 11 | 12 | 1 | 0.250 |
| 4 | 10 | 12 | 2 | 0.516 |

The rank direction is consistent but its 2.5-direction mean is below the
frozen four-direction threshold. More importantly, no passing shared seed met
the 0.80 composition-generalization gate. The result is therefore compatible
with context-invariant memorization of seen entries and does not identify
shared algorithm learning.

### 4.6 Intervention guards

**Shuffle:** Passing conditions lost 0.925--0.946 answer accuracy on average
and incurred 8.90--10.28 nat additional CE when root states were shuffled. The
registered root state was causally used.

**Random equal-rank subspaces:** Passing runs had zero random-subspace pass
fraction. The learned task-aware basis was not interchangeable with arbitrary
equal-rank directions.

**Full-rank replay:** The frozen absolute CE tolerance was \(10^{-5}\). Sixteen
of 35 runs exceeded it; the maximum was \(5.15\times10^{-4}\). Among 19
capability-passing runs, one exceeded it, at \(1.16\times10^{-5}\). Inspection
is consistent with float32 reconstruction through a complete QR basis rather
than returning the original state exactly. The raw run and hard-gate failure
are preserved; no post-hoc correction changes the verdict.

### 4.7 Final-normalization localization

The capability-passing lookup means were:

- `K=1`: post 10.2, pre 9.4;
- `K=4`: post 11.0, pre 8.6;
- `K=16`: post 12.8, pre 11.6.

The ordering is present before and after final normalization, so the lookup
cardinality pattern is not solely a post-normalization artifact. The pre/post
values are not algebraically interchangeable and remain secondary.

## 5. Formal Gate Ledger

| Gate | Raw status | Audit interpretation |
| --- | --- | --- |
| Generator | pass | Exact manifests and answer marginals matched |
| Seed completion | pass | 35/35 completed |
| Primary capability | fail | Both `F=1` primary conditions failed |
| Matched full-state utility | fail | Primary test accuracy and CE were poor and unmatched |
| Full-rank replay | fail | Frozen numerical tolerance exceeded |
| Shuffle | pass | Root state causally used |
| Random subspace | raw fail | Incapable runs contaminate aggregate; all capable runs had 0 random pass fraction |
| Shared composition | fail | 0/4 passing shared seeds reached 0.80 |
| Formal verdict | `insufficient` | Neither pass nor fail of H1 |

## 6. Artifact Map

### Curated evidence

- [Chinese summary](summary_cn.md)
- [Condition summary](condition_summary.csv)
- [Capability-passing shared/lookup pairs](passing_shared_lookup_pairs.csv)
- [Capability-aware central figure](capability_and_functional_rank.png)
- [Curated analysis script](analyze_results.py)

### Frozen implementation

- [Configuration](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/configs/a14_02_e01_shared_rule_vs_lookup_root_rank.yaml)
- [Core implementation](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/src/tree_low_rank/shared_rule_root_rank.py)
- [Runner](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/scripts/run_shared_rule_vs_lookup_root_rank.py)
- [Tests](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/tests/test_shared_rule_root_rank.py)

### Raw run evidence

- [Full result directory](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e01_shared_rule_vs_lookup_root_rank/a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427/full)
- [Decision JSON](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e01_shared_rule_vs_lookup_root_rank/a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427/full/decision.json)
- [Per-condition seed table](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e01_shared_rule_vs_lookup_root_rank/a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427/full/condition_seed_summary.csv)
- [Run manifest](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/results/a14_02_e01_shared_rule_vs_lookup_root_rank/a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427/full/run_manifest.json)
- [Remote logs](../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/logs/acp/a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427)

## 7. Visualization Audit

The central figure asks two questions in order:

1. Did the full root state solve the held-out task?
2. Among runs that did, how many learned root directions preserved utility?

The left axis is held-out answer accuracy with the frozen 0.95 capability
line. The right axis is post-norm functional rank in directions and excludes
incapable runs. Points are seeds; horizontal bars are condition means.

Allowed reading: duplicate exposure did not pass context generalization;
lookup functional rank rose over `K=1/4/16` among capable runs.

Disallowed reading: the figure proves shared composition, frequency causality,
natural-language low rank, or Router value.

