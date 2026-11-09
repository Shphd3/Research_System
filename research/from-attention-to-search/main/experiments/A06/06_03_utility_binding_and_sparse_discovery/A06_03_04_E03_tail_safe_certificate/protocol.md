# A06_03_04_E03 Tail-Safe Utility Certificate Protocol

Approval status: approved under the active long-run research instruction.

Purpose: determine whether lower-tail pairwise expert utility prevents the
premature stopping produced by population-mean utility.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`.

## Fixed Setup

Reuse A06_03_04_E02 exactly: learned rank-4 specialists, frozen representation and
experts, router-only SGD `0.001`, full LM loss, maximum 600 continuous audition
updates, total horizon 800, 32 seeds, and four tasks. All stopping branches start
from identical tensors and differ only in the aggregation functional applied to
per-token utility.

For incumbent \(e\) and challenger \(c\),

\[
D_{e,c}(h)=\ell(E_c(h))-\ell(E_e(h)).
\]

Positive values favor the incumbent.

## Conditions

- `fixed600`: A06_03_04_E02 continuous-audition baseline.
- `oracle_route`: true route-correction lower bound.
- `mean`: reproduce A06_03_04_E02 population mean.
- `q25`: 25th percentile of \(D_{e,c}\).
- `q10`: 10th percentile.
- `cvar10`: mean of values at or below the 10th percentile.
- `task_q10_oracle`: q10 using only task-dependent positions.
- `generalist_q10` and `generalist_cvar10`: false-trigger guards.

Each directed pair statistic uses EMA decay `0.9`. Stop when all 12 directed
pairs are positive for nine updates with at most 1% assignment change. If no
rule triggers by 600, switch to top-1 at 600.

## Primary Decision

A non-oracle tail rule passes if:

- correction and retention are each at least `0.90`;
- premature-stop rate is at most `0.05`;
- median audition saving is at least `0.30`;
- corresponding generalist trigger is below `0.10`.

Hypotheses:

- **H1 tail-safe certificate:** at least one of q25/q10/CVaR10 passes.
- **H2 mean is Pareto-optimal:** every tail rule that lowers premature stop below
  5% loses the 30% saving target or correction target.
- **H3 task-position tail is required:** task-q10 passes while all all-position
  tail rules fail.
- **H4 token tail is the wrong unit:** no tail rule passes and task-q10 does not
  isolate the failure; routed-subpopulation grouping is required.

## Mechanism Evidence

At every update, record the minimum across directed pairs for mean, q25, q10,
and CVaR10. Around each stop, preserve pair-level statistic values and token
counts. A tail mechanism is supported only if safe rules remain nonpositive
after the mean becomes positive in cells where mean stopping is premature.

## Validity Guards

- all A06_03_04_E02 utility, rank, score-gap, load, finite-value, pairing, fixed600,
  oracle, and generalist guards pass;
- forced losses reuse the two already executed experts;
- quantile/CVaR computation is deterministic and finite for every observed pair;
- every certificate observes all 12 directed pairs before stopping.

## Claim Boundary

Passing establishes a controlled distributionally robust stop, not joint
training, pretrained-LLM transfer, scalable many-expert statistics, or systems
throughput.
