# Spectral Partition Router v2.2

This folder contains the revised static-dispatch research stage for the spectral routing line.

The scope is intentionally narrower than dynamic MoE training:

```text
Goal: define and solve static feature-level specialization under
      globally spectrally isotropic and frequency-uniform feature distributions.

Out of scope: training-time route preservation, representation drift,
              slow router updates, learned-router dynamics.
```

## Core research question

We study the following controlled problem:

> If route-relevant features are globally spectrally isotropic and feature families are frequency-uniform, can we construct a non-cheating static router that sends whole feature families to experts while achieving balanced expert usage?

This is the static problem requested by the advisor's clean mathematical case: first make the uniform feature / uniform spectrum setting self-contained, prove what can be proved, and design experiments that close this stage before moving to non-uniform spectra or training preservation.

## Main correction from the previous scaffold

Quantile routing is no longer the main proposed mechanism.

Quantiles are useful for controlling mass along a projection, but they are not causally tied to the new target of feature-level specialization. Under the current problem definition, the more natural causal mechanism is:

```text
frequency-uniform feature families
+ recoverable local feature structure
+ globally spectrally isotropic metric
-> recover feature families in the normalized space
-> assign recovered feature families to experts under a balanced constraint
-> route new tokens by feature-family identity
```

Thus the primary method is now **BFSR: Balanced Feature-Specializing Routing**.

## Why spectral isotropy still matters

Spectral isotropy alone does not identify good routing. An isotropic Gaussian with random independent labels gives no recoverable feature specialization.

In this paper, spectral isotropy plays a more precise role:

1. It removes global high-variance directions that would dominate distance or gating geometry.
2. It gives a clean metric in which local feature families are comparable.
3. It allows the paper to separate global spectrum uniformity from local feature structure.

The actual causal source of specialization is not isotropy alone. It is **recoverable feature-family structure inside a globally isotropic distribution**.

## Working assumptions

The controlled feature model is:

```text
F ~ Uniform({1,...,K})
X | F=k = mu_k + eps
```

with:

- frequency-uniform feature families;
- globally approximately isotropic covariance after centering / whitening;
- locally separated or recoverable feature-family structure;
- a static scope: feature-dependent utility and expert-side semantic alignment are downstream optional audits, not part of the current stage claim.

A typical construction is a balanced mixture whose centers form a spherical or spectrally balanced code, so the aggregate distribution is isotropic while each family remains locally identifiable.

## Static good dispatch definition

A good static dispatch is not just low load CV. It should satisfy:

1. **Mass balance**: every expert receives equal probability mass.
2. **Feature specialization**: each feature family is routed consistently to a small number of experts, ideally one expert.
3. **Non-trivial expert usage**: the router should not collapse to a single expert or to arbitrary per-batch balancing.
4. **Downstream utility audit**: controlled feature-dependent learning may be tested later, but it is not part of the current stage claim.

## Primary method: BFSR

BFSR has four steps:

```text
1. Spectrally normalize calibration features.
2. Recover feature-family prototypes using unsupervised clustering or a controlled oracle anchor.
3. Assign recovered feature families to experts with a balanced objective.
4. Route each new token to the expert assigned to its nearest recovered feature family.
```

For BFSR, the mass mechanism is family-level frequency balance, not projection quantiles:

```text
uniform feature frequencies + equal number/mass of feature families per expert
-> equal expected expert usage
```

Quantile-SPR remains a baseline because it can balance mass without respecting feature identity. It is useful as a negative control for the claim that mass balance is not sufficient for specialization.

## Files

```text
README.md                         # this overview
PROBLEM_STATEMENT.md              # self-contained scope and definitions
METHOD_AND_THEORY_NOTES.md         # method, assumptions, theorem sketches
RESEARCH_PLAN.md                   # falsifiable hypotheses and research anchors
exp/EXPERIMENT_PLAN.md             # executed E1--E5 experiment chain and parked downstream audits
exp/CODEX_TASKS.md                 # implementation tasks for Codex
latex/paper.tex                    # self-contained result draft
latex/math_commands.tex            # LaTeX macros
latex/references.bib               # bibliography
```

## Stage closure criterion

This stage is closed only when the paper can say:

```text
In globally spectrally isotropic and frequency-uniform feature distributions,
feature-level specialization is possible when local feature families are recoverable.
BFSR uses that condition directly: it recovers feature families and assigns them to experts under a balanced constraint.
When recoverability or feature-frequency uniformity is removed, the method should fail in predictable ways.
```

The experiments should therefore include both positive and negative anchors. A method that succeeds only on load balance but not on feature specialization does not solve this stage.
