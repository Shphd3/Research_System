# Detailed Record: A14_E08 Relation-Reuse Parameter-to-State Bridge

## 1. Registered Question And Verdict

**Question:** when full-model capability is matched, does `share16` require
fewer attention-update directions than `random_unshared` to preserve
first-C-token loss on B identities not used to fit the state subspace?

**Formal verdict:** `insufficient_evidence` because the source provenance gate
failed. The original generator, training implementation, and checkpoints were
not published in the recovered source repository.

**Operational reconstruction verdict:** all non-provenance success criteria
passed for the independent reconstruction. This is reported as conditional
evidence, not as a source replication.

## 2. Provenance Audit

Recovered public source:

- repository: `Frandium/kv_cache`;
- inspected source revision: public history containing
  `fdong_embedding_dim/meeting_docs/NTP_HIERARCHY_FREQUENCY_TALK.md`;
- documented model: one-layer, one-head causal attention, width 64/128,
  three seeds;
- documented data: two-token A/B/C/D fields, 16 B contexts, fixed node
  marginals, `share16/share4/share2/random_unshared`;
- documented 64D learning-speed medians: 350/750/1100/1200;
- documented localization: strong Q/K tail-truncation difference, V/O nearly
  unchanged.

Repository history and filesystem searches found no exact data generator,
training script, checkpoint, or machine-readable result table for this study.
Therefore the run below reconstructs the verbal contract and receives a new
provenance manifest and new data hashes.

## 3. Independent Reconstruction

### Data

- 16 A identities, 16 B identities, 16 C identities, and 16 D identities;
- each identity represented by a distinct two-token field;
- complete 16-by-16 A/B grid, giving 256 sequences per condition;
- D is the identity function of B;
- each B family owns an independently sampled A-to-C permutation;
- family sizes are 16, 4, 2, and 1 for the four conditions;
- all node marginals are uniform and identical across conditions.

The exact mapping tables and SHA-256 data hashes are saved in
`provenance_manifest.json` in the raw output directory.

### Model And Training

- width 64, one pre-norm attention-only layer, one head;
- learned token and position embeddings;
- untied next-token prediction head;
- full-sequence teacher-forced NTP loss;
- full-batch AdamW;
- capability logged every 25 steps;
- matched fit requires both A-to-C and B-to-D CE at or below 0.02 for three
  consecutive logs;
- seeds 0, 1, and 2.

All 12 condition-seed runs met the gate.

| Condition | Seed 0 | Seed 1 | Seed 2 |
| --- | ---: | ---: | ---: |
| `share16` | 125 | 125 | 125 |
| `share4` | 350 | 200 | 200 |
| `share2` | 450 | 275 | 275 |
| `random_unshared` | 525 | 425 | 425 |

The ordering qualitatively matches the source description, but the absolute
steps do not. This is expected under an independently reconstructed
architecture and optimizer.

## 4. State Functional-Rank Analysis

The primary hook captures the attention residual update at the B-end position.
PCA is fitted on calibration B identities only. The test update is replaced by
the affine rank-\(k\) projection, and the model continues to the first C-token
logit. The selected rank is the first rank from which every larger rank keeps
\(\Delta CE\le0.02\).

### Primary split

| Condition | Seed | \(k_H\) | \(k_H/64\) | 95% energy rank | PCA \(\Delta CE\) at \(k_H\) | Random median \(\Delta CE\) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `share16` | 0 | 13 | 0.203 | 12 | 0.0124 | 3.341 |
| `share16` | 1 | 10 | 0.156 | 14 | 0.0102 | 2.630 |
| `share16` | 2 | 10 | 0.156 | 12 | 0.0136 | 3.590 |
| `share4` | 0 | 11 | 0.172 | 18 | 0.0183 | 2.279 |
| `share4` | 1 | 11 | 0.172 | 18 | 0.0135 | 2.135 |
| `share4` | 2 | 10 | 0.156 | 19 | 0.0174 | 2.339 |
| `share2` | 0 | 17 | 0.266 | 16 | 0.0159 | 2.843 |
| `share2` | 1 | 11 | 0.172 | 16 | 0.0109 | 2.391 |
| `share2` | 2 | 11 | 0.172 | 15 | 0.0172 | 2.702 |
| `random_unshared` | 0 | 16 | 0.250 | 14 | 0.0126 | 3.190 |
| `random_unshared` | 1 | 13 | 0.203 | 13 | 0.0155 | 2.841 |
| `random_unshared` | 2 | 12 | 0.188 | 13 | 0.0183 | 3.889 |

The paired extreme-condition rank gaps were 3, 3, and 2 dimensions. Their
normalized values were 0.046875, 0.046875, and 0.03125. A 5,000-replicate
hierarchical paired bootstrap produced mean 0.04072 and percentile interval
[0.02604, 0.05208].

The average ranks of the middle conditions do not form a strict ordering:
`share4` (10.67) is slightly below `share16` (11.0), while `share2` is 13.0.
This rejects a simple monotonic reading.

### Split swap

The swapped ranks were:

- `share16`: 13/10/10;
- `random_unshared`: 16/14/15.

The paired gaps were 3/4/5, so no seed reversed direction.

### Random-space and replay guards

- All 32 equal-rank random spaces per condition/seed failed the 0.02 tolerance
  in the primary contrast; pass rate was 0.
- Learned `share16` PCA spaces passed at each selected rank.
- Full-basis replay absolute loss error was at most approximately
  \(6.3\times10^{-8}\).
- Direct update replay was exactly zero at recorded precision.
- Shuffling states produced very large loss increases, confirming that the
  state/sample association was functionally important.

## 5. Combined-QK Functional Rank

| Condition | Seed 0 | Seed 1 | Seed 2 | Mean |
| --- | ---: | ---: | ---: | ---: |
| `share16` | 17 | 36 | 36 | 29.67 |
| `share4` | 39 | 44 | 48 | 43.67 |
| `share2` | 45 | 48 | 51 | 48.00 |
| `random_unshared` | 48 | 56 | 48 | 50.67 |

The extreme combined-QK gap is 21 dimensions on average, much larger than the
2.67-dimension average state gap. Full-rank combined-QK replay error was below
\(2.3\times10^{-8}\).

Across all 12 condition-seed points, Spearman correlation between normalized
QK and state functional rank was \(\rho=0.247\), \(p=0.438\). Across four condition
means it was \(\rho=0.8\), \(p=0.2\), but four points are not decision-bearing.

Thus the extreme contrast co-occurs at parameter and state levels, but the run
does not establish a strong continuous parameter-to-state mapping.

## 6. Source-Localization Diagnostic

Individual-matrix truncation reproduced the qualitative extreme pattern that
`share16` is much more robust than `random_unshared` in Q/K. It did not
reproduce the source note's reported V/O localization. At rank 16, V/O
truncation increased `share16` A-to-C CE by approximately 0.42--0.89 nat across
seeds. Therefore:

- this implementation is not an exact replay;
- the source-specific claim that the effect is almost exclusively Q/K remains
  unverified here;
- the combined-QK and state findings must be attributed only to this
  reconstruction.

## 7. Registered Gate Ledger

| Gate | Result | Reading |
| --- | --- | --- |
| Source artifacts recovered | **Fail** | public source lacks generator/code/checkpoints |
| Source exact replay | **Fail** | impossible under missing artifacts; V/O localization differs |
| 12/12 matched capability | Pass | no primary rank is explained by failed fit |
| Hook/full-rank replay | Pass | intervention object is numerically consistent |
| 3/3 positive extreme gaps | Pass | gaps 3/3/2 dimensions |
| Bootstrap lower bound \(>0\) | Pass | 95% interval [0.0260, 0.0521] |
| `share16` \(k_H\le16\) | Pass | 13/10/10 |
| Learned PCA passes, random median fails | Pass | random pass rate 0 |
| Split swap no reversal | Pass | gaps 3/4/5 |

Because provenance is a hard gate, the formal verdict remains insufficient
despite all operational reconstruction gates passing.

## 8. Execution And Validation

### Evidential command

```text
CUDA_VISIBLE_DEVICES=0 python scripts/run_relation_reuse_state_bridge.py \
  --config configs/exp8_relation_reuse_state_bridge.yaml \
  --output-dir outputs/A14_E08_full \
  --device cuda:0
```

### Environment

- GPU: NVIDIA H100 80GB HBM3;
- Python 3.10.12;
- PyTorch 2.3.0a0+6ddf5cf85e.nv24.04;
- complete run exit code: 0;
- recorded runtime: approximately 22 seconds after the bootstrap computation
  was vectorized without changing its estimator.

### Validation

- E08 targeted tests: 4/4 passed;
- Python syntax compilation: passed;
- repository-wide test collection: blocked by a pre-existing missing `nltk`
  dependency in unrelated syntax tests. This is an environment validation
  limitation, not an E08 scientific or execution failure.

The first full analysis reached the bootstrap stage but its row-wise pandas
implementation was inefficient. It was interrupted before verdict generation,
the mathematically equivalent paired bootstrap was vectorized, targeted tests
were rerun, and the entire evidential pipeline was then rerun from training to
final artifacts.

## 9. Artifact Map

Curated artifacts in this directory:

- [summary.md](summary.md) and [summary_cn.md](summary_cn.md);
- [state functional-rank figure](figures/state_functional_rank_curves.png);
- [parameter-state figure](figures/parameter_state_functional_ranks.png).

Raw artifacts remain on the worker surface:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/
active/tree_low_rank/outputs/A14_E08_full/
```

Important raw files:

- `summary.json`;
- `run_manifest.json` and `provenance_manifest.json`;
- `run_summary.csv` and `training_curves.csv`;
- `state_functional_curves.csv` and `state_functional_summary.csv`;
- `qk_functional_curves.csv` and `qk_functional_summary.csv`;
- `random_subspace_controls.csv`;
- `source_matrix_truncation.csv`;
- 12 matched-fit checkpoints.

## 10. Claim Boundary And Next Decision

This run conditionally supports one narrow bridge in its own reconstruction:
the extreme high-reuse/low-rule-count condition has a small, reusable,
task-sufficient state-rank advantage alongside a large QK-rank advantage.

It does not isolate frequency from rule complexity, establish monotonicity,
prove gradient alignment, reproduce the source experiment, validate a natural
language tree, establish global low rank, or support a Router architecture.

**Exactly one next decision:** decide whether this independent reconstruction
is acceptable as a standalone evidence item. No orthogonal causal experiment
or Router design follows until that review is complete.

