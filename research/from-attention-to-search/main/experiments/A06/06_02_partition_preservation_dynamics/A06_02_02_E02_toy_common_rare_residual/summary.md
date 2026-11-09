# Summary: A06_02_02_E02_toy_common_rare_residual

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

## Result Snapshot

Verdict: Supported on the synthetic mechanism surface, with one execution
boundary.

What we established: In the synthetic setting, raw principal expert proxies are
common-dominated and do not recover rare routing. Residual and differential
residual proxies recover rare routing at step 0. Under synthetic common
recapture, initialization alone fails, while residual input or row projection
preserves rare margin and nearly eliminates sign flips.

What the experiment shows: The user's two update ideas are feasible only with
common control. Smaller common step plus rare step alone improves loss but does
not preserve the route. Zero common step or rare-large step combined with
residual input / row projection preserves the route.

What we do next: Do not claim a real router yet. The next useful protocol is a
real-DCLM proxy audit that tests only the supported mechanism: raw principal
proxy versus residual differential proxy with projector robustness and early
preservation guards.

Execution boundary: The synthetic run completed locally in the current
environment. A requested remote 4-GPU execution did not complete because the
available configured remote entrances did not provide usable 4-GPU access.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Common direction | Shared high-amplitude direction | Synthetic vector \(c\) | Unit vector | Tests common dominance | Real language common semantics |
| Rare direction | Group-specific route feature | Synthetic vector \(r_g\) | Unit vector | Defines target expert | Natural-language feature identity |
| Rare margin | Target expert score minus strongest competitor | \(z_{i,y_i}-\max_{e\ne y_i}z_{i,e}\) | Logit difference | Primary routing safety metric | Expert utility |
| Sign flip | Preserved margin crosses boundary | Step-0 positive margin becomes non-positive | Fraction | Tests early preservation | Cause of flip by itself |
| Synthetic loss | Label cross-entropy on synthetic expert labels | CE over expert labels | Nats | Loss guard | LM loss |

## Exact Setup

Data / model / objective: Synthetic hidden states with one common direction,
four rare directions, four experts, and synthetic labels. Expert gain matrices
were constructed so the raw principal direction is common-dominated.

Conditions: A06_02_02_E02.a--A06_02_02_E02.g, covering sanity split, projector robustness, raw
principal critique, residual differential initialization, early preservation,
functional binding, and differential step-size variants.

Held fixed: same dimensions, experts, data generator, seeds, labels, and
synthetic expert gain construction.

Seeds: 0--7.

Primary result table:
`tables/all_experiment_summary.csv`

Runner:
`scripts/run_synthetic_common_removed_differential_proxy.py`

## Primary Metric

Definition: rare margin is the target expert logit minus the strongest
competing expert logit.

Why it decides: The mainline bottleneck is whether a route enters and remains
inside the correct expert basin. Load balance alone cannot decide this.

## Result

### A06_02_02_E02.a Sanity Split

Hidden mean subtraction improved load (`max_load=0.3103`,
`effective_experts=3.9300`) but did not recover rare routing
(`rare_margin=-0.2426`, `route_accuracy=0.2552`). Differential residual proxy
recovered the route (`rare_margin=1.3881`, `route_accuracy=1.0000`).

### A06_02_02_E02.b Common Operator Robustness

Differential proxy was robust for oracle, mean, and perturbed common projectors
(`rare_margin` about `1.38` to `1.39`, accuracy `1.0000`). Top-PC common was
weaker but still positive (`rare_margin=0.7034`, accuracy `0.9237`).

### A06_02_02_E02.c Raw Principal Common Dominance

Raw principal proxy was almost entirely common-aligned
(`common_overlap=0.9999`) and failed rare routing (`rare_margin=-2.9990`).
Differential residual proxy had near-zero common overlap and perfect synthetic
route accuracy.

### A06_02_02_E02.d Initialization

Residual and differential residual proxies both recovered the synthetic route.
This supports the residual-proxy direction but does not yet distinguish
residual principal from differential residual in this simple synthetic setup.

### A06_02_02_E02.e Early Preservation

Initialization alone failed under common recapture (`rare_margin=-2.9041`,
`sign_flip_rate=0.5260`). Residual input, row projection, and symmetric
residual routing preserved the route (`rare_margin=0.6372`,
`sign_flip_rate=0.0060`, accuracy `0.9940`).

### A06_02_02_E02.f Functional Binding

Load-only hidden centering did not bind route to function
(`selected_utility=0.2552`). Preserved differential residual routing did
(`selected_utility=0.9940`).

### A06_02_02_E02.g Differential Step Size

Scheme 1, smaller common step with base rare step, improved loss but did not
preserve routing (`rare_margin=-0.5796`, `sign_flip_rate=0.5835`). With common
step set to zero, the route was preserved (`rare_margin=1.3882`,
`sign_flip_rate=0.0000`). Scheme 2, smaller common step plus rare 4x, made rare
margin slightly positive but still had high sign flips (`0.5178`). Adding
residual input or row projection made scheme 2 pass (`rare_margin=1.3094`,
`sign_flip_rate=0.0000`, accuracy `1.0000`).

## Key Figures

### Figure: A06_02_02_E02.a Rare Margin

![A06_02_02_E02.a rare margin](figures/a06_26a_rare_margin_mean.png)

Take-home: load-only controls are not enough; residual / differential proxies
are the first conditions with positive rare margin.

### Figure: A06_02_02_E02.e Sign Flip

![A06_02_02_E02.e sign flip](figures/a06_26e_sign_flip_rate.png)

Take-home: initialization alone is not enough under common recapture; residual
input or row projection prevents almost all sign flips.

### Figure: A06_02_02_E02.g Rare Margin

![A06_02_02_E02.g rare margin](figures/a06_26g_rare_margin_mean.png)

Take-home: differential step sizes become reliable only when common recapture
is removed or residualized.

## Claim Boundary

Can claim: The synthetic mechanism supports the anchor chain: raw principal
proxies can be common-dominated; hidden centering can improve load without
specialization; residual / differential proxies improve rare margin; residual
input or row projection is needed for preservation under common recapture; the
two differential-step schemes are feasible only with common control.

Cannot claim: real-DCLM transfer, real semantic experts, LM loss preservation,
or a deployable router.

## Next Decision

Write the real-DCLM protocol only after choosing the exact real common
operator and target proxy labels. The real protocol should not include all
A06_02_02_E02.a--A06_02_02_E02.g stages; it should test raw principal versus residual
differential proxy plus early preservation guards.
