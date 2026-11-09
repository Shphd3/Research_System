# Summary: A14_E08 Relation-Reuse Parameter-to-State Bridge

Primary subanchor:
[A14_01 relation-reuse bridge](../../../../../../problem_anchors/14_tree_low_rank_language_structure/14_01_relation_reuse_parameter_state_bridge/14_01_relation_reuse_parameter_state_bridge_anchor.md)

Protocol: [protocol.md](protocol.md) · [中文协议](protocol_cn.md)

## Result Snapshot

**Formal registered verdict: insufficient evidence.** The public source
contains the experimental description but not its generator, training code, or
checkpoints, so the registered source-replay gate cannot pass.

**Independent reconstruction result:** the extreme composite contrast is
positive. Across seeds, `share16` needed 13/10/10 state directions while
`random_unshared` needed 16/13/12. The normalized paired gaps were
0.0469/0.0469/0.0313, and the 5,000-replicate hierarchical-bootstrap 95%
interval was [0.0260, 0.0521]. All `share16` runs met the 16/64 budget, learned
PCA spaces passed, equal-rank random spaces failed, and split swapping did not
reverse the result.

**Most important update:** parameter compression and task-state compression
must not be treated as the same magnitude. The combined-QK rank gap was large
(mean 50.7 versus 29.7), while the state-rank gap was only 2.67 dimensions
(mean 13.7 versus 11.0). Across all 12 condition-seed points, their Spearman
correlation was weak and nonsignificant (\(\rho=0.247\), \(p=0.438\)).

## Direct Results

| Condition | Matched steps, seeds 0/1/2 | State functional rank | Combined-QK functional rank |
| --- | ---: | ---: | ---: |
| `share16` | 125 / 125 / 125 | 13 / 10 / 10 | 17 / 36 / 36 |
| `share4` | 350 / 200 / 200 | 11 / 11 / 10 | 39 / 44 / 48 |
| `share2` | 450 / 275 / 275 | 17 / 11 / 11 | 45 / 48 / 51 |
| `random_unshared` | 525 / 425 / 425 | 16 / 13 / 12 | 48 / 56 / 48 |

All 12 runs reached the frozen matched-fit gate. The training-speed ordering
agreed with the source report, although the absolute steps differ.

The middle state conditions were not monotonic: `share4` was slightly lower
than `share16`. Therefore this run does not support a general rule that more
reuse or more frequency monotonically lowers task-state rank.

## Central Figures

### Held-out task-state functional rank

![Held-out state functional-rank curves](figures/state_functional_rank_curves.png)

The right panel zooms into the preregistered 0.02-nat decision region. The
extreme condition gap is small but consistent; intermediate conditions do not
form a strict dose-response curve.

### Parameter and state functional ranks

![Parameter and state functional ranks](figures/parameter_state_functional_ranks.png)

High reuse is associated with strong combined-QK compression, but state-rank
compression is much smaller and the continuous correspondence is weak.

## Guards And Controls

- Full-state and direct-update replay errors were at numerical precision.
- Combined-QK full-rank replay error was below \(2.3\times10^{-8}\).
- At the selected `share16` ranks, learned PCA \(\Delta CE\) was at most 0.02;
  equal-rank random-space medians were 2.63--3.59 nat and had 0 pass rate.
- Split-swap extreme gaps were 3/4/5 dimensions, so the direction did not
  reverse.
- The independent reconstruction did not reproduce the source note's claimed
  near-null V/O localization: V/O rank-16 interventions substantially damaged
  A-to-C loss. This is an additional reason not to label the run a source
  replication.

## Claim Boundary

Allowed as conditional reconstruction evidence: under this documented
implementation, the high-reuse/low-rule-count composite condition has a small,
consistent held-out functional-state-rank advantage and a much larger QK
functional-rank advantage over `random_unshared`.

Not allowed: pure frequency causality, a monotonic reuse-rank law, gradient
alignment as the mechanism, exact replication of the senior experiment,
natural-language or tree generalization, global low rank, or a Router design.

## Exactly One Next Decision

Decide whether to register this independent reconstruction as a standalone
piece of evidence. Until that review is accepted, do not start the orthogonal
frequency-versus-rule-complexity study or a Router experiment.

