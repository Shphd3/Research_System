# A06_03_03_E01 Bounded-Challenger Semantic-Credit Router Protocol

Approval status: approved under the active long-run research instruction.

Purpose: test whether semantic-position credit and bounded unselected-expert
utility coverage are jointly sufficient for wrong-route correction.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/subanchors/06_03_03_bounded_challenger_discovery_anchor.md`.

## Setup And Conditions

Reuse A06_03_02_E02 exactly: learned specialists, rank-2/rank-4 installation, frozen
representation and experts, router-only SGD `0.001`, 300 updates, 32 seeds, four
tasks, and disjoint train/test sequences.

For each rank, run from identical tensors:

- `full_top1`
- `task_top1`
- `full_pair`
- `task_pair`
- `task_soft` positive control

Pair routing evaluates the selected expert and one challenger. For each token,
the challenger cycles through the three nonselected expert IDs according to a
seed-specific random permutation. Candidate probabilities are renormalized
within the pair. Evaluation always uses ordinary top-1 identity.

## Primary Decision

H1 joint sufficiency requires task-pair correction at least `0.90` for ranks 2
and 4, at least `0.50` rank-4 improvement over both full-pair and task-top1, and
a positive seed-clustered 95% confidence lower bound for the factorial
interaction. Task-soft must remain at least `0.90`.

## Validity

- static challenger schedule gives each of the three nonselected expert IDs
  exactly one of every three phases; realized wrong-state inclusion is reported
  descriptively because successful correction censors that state;
- challenger schedule uses no task/target/useful identity;
- maximum two expert forwards in pair branches;
- all A06_03_02_E02 specialist, rank, gap, balance, pairing, and finite guards pass;
- generalist arbitrary-target control stays below `0.10`.

Secondary metrics are capped correction time, normalized cumulative regret,
inclusion-conditioned useful-margin pressure, and final useful probability.

## Boundary

Passing establishes controlled joint sufficiency only. It does not validate an
MTP credit estimator, natural-language specialization, or deployment efficiency.
