---
experiment_id: A14_02_E01_shared_rule_vs_lookup_root_rank
status: completed_insufficient
verdict: insufficient
run_id: a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427
job_id: pt-q6hu0fq5
companion_cn: summary_cn.md
---

# Summary: A14_02_E01 Shared Rules Versus Lookup Root-State Rank

Primary subanchor:
[A14_02 task-functional root-state rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Protocol: [protocol.md](protocol.md) · [中文协议](protocol_cn.md)

## Direct Result

**The preregistered primary verdict is `insufficient`.** Both low-exposure
conditions memorized their training entries but failed the held-out
new-context capability gate:

- `shared_unique`: 0/5 seeds passed; mean test accuracy 0.179;
- `lookup_unique`: 0/5 seeds passed; mean test accuracy 0.088.

The automatic primary rank contrast, including the raw `-36`-direction value
in `decision.json`, is therefore invalid as scientific evidence. Functional
rank is not interpretable when the full state does not solve the registered
task.

## Established Diagnostic Updates

1. **Raw repetition was insufficient; context diversity was necessary.**
   `shared_repeat_duplicate` reached 1.0 training accuracy but 0/5 capability
   passes and mean test accuracy 0.199. At the same exposure, the
   diverse-context shared condition passed in 4/5 seeds; passing runs averaged
   0.991 test accuracy.

2. **Among solvable lookup tasks, more independent mappings required more
   task-functional root directions.** With exposure and context diversity
   fixed, all five seeds passed for each condition, while mean post-norm
   functional rank increased from 10.2 (`K=1`) to 11.0 (`K=4`) to 12.8
   (`K=16`).

3. **A shared-versus-lookup compression effect remains only suggestive.**
   Among the four paired high-exposure seeds in which both tasks passed,
   `lookup K=16 - shared` rank gaps were 4, 3, 1, and 2 directions (mean 2.5).
   This is below the frozen four-direction effect threshold. One shared seed
   failed training, and all four passing shared seeds failed the registered
   unseen-composition threshold; their composition accuracies were
   0.547, 0.063, 0.250, and 0.516. The run therefore does not establish that
   the network learned the shared algorithm.

## Central Figure

![Capability and capability-filtered functional rank](capability_and_functional_rank.png)

The left panel prevents failed tasks from being interpreted as low-rank. The
right panel reports functional rank only for capability-passing runs.

## Capability-Filtered Results

| Condition | Capability passes | Held-out accuracy | Post-norm functional rank |
| --- | ---: | ---: | ---: |
| Shared, `F=1` | 0/5 | 0.179, all seeds | not interpretable |
| Lookup `K=16`, `F=1` | 0/5 | 0.088, all seeds | not interpretable |
| Shared, `F=8`, exact duplicate | 0/5 | 0.199, all seeds | not interpretable |
| Shared, `F=8`, diverse contexts | 4/5 | 0.991, passing seeds | 10.25 |
| Lookup `K=1`, `F=8`, diverse | 5/5 | 1.000 | 10.20 |
| Lookup `K=4`, `F=8`, diverse | 5/5 | 1.000 | 11.00 |
| Lookup `K=16`, `F=8`, diverse | 5/5 | 1.000 | 12.80 |

## Guard Audit

- Generator matching and all 35 condition-seed completions passed.
- Shuffling the root state strongly damaged every capability-passing task:
  mean accuracy drops were 0.925--0.946 and CE increases were 8.90--10.28 nat.
- At the selected ranks, equal-rank random subspaces passed in 0% of
  capability-passing runs.
- The frozen full-rank replay tolerance was exceeded in 16/35 runs. Among the
  19 capability-passing runs, only one exceeded it, at
  \(1.16\times10^{-5}\) versus the \(1.00\times10^{-5}\) threshold. This appears
  consistent with full-basis float32 reconstruction error, but the registered
  hard gate remains failed.

## Claim Boundary

Allowed:

> In this synthetic NTP task, exposure count alone did not create
> context-invariant root states. Diverse-context exposure was necessary, and
> among capability-matched lookup tasks, increasing independent mapping
> cardinality from 1 to 16 increased the task-functional root rank.

Not allowed: low-frequency shared composition lowers root rank; the model
learned the compositional algorithm; frequency alone causes rank; the lookup
curve is universal; natural language is tree-structured or low-rank; or this
result establishes Router utility.

## Exactly One Next Decision

Decide whether to revise A14_02 so that a capability-only stage first finds a
matched regime where both shared and lookup tasks pass new-context utility and
the shared task passes unseen-composition accuracy, before any rank contrast is
interpreted.

