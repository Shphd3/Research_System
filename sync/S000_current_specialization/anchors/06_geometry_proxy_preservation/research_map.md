# A06 Research Map: Functional Routing Under Partial Feedback

This file is the current anchor registry for the Routing line. Current parent
and subanchor IDs are authoritative; immutable remote job and result IDs remain
inside detailed artifact maps, while Git history preserves the earlier layout.

## Terminology / Definitions

| Term | Plain meaning | Decision role | Cannot prove |
|---|---|---|---|
| Operational condition | A controlled or registered input group $z$ | Defines what may need a different expert | That $z$ is a natural semantic category |
| Functional specialization | Different conditions prefer different expert functions and routing captures that value under cost | Terminal meaning of specialization | Route purity alone |
| Route margin | Assigned expert's score lead over its strongest competitor | Local preservation budget | Expert usefulness |
| Counterfactual expert utility | Loss change when the same state is forced through another expert | Separates expert function from route identity | Deployable routing by itself |
| Partial feedback | Top-1 evaluates the selected expert but not every alternative | Explains discovery failure | That dense routing is necessary |
| Held-out oracle headroom | Native Router loss minus split-stable forced-expert oracle loss | Decides whether a real workload is worth routing | That a learned Router captures the headroom |

## Parent Question

> Under approximately fixed activated compute, can a top-1 mixture-of-experts
> model bind different input conditions to experts that are measurably more
> useful for them?

The five parent decisions are:

```text
functional specialization contract
-> geometry and route-relevant state discovery
-> partition-preservation dynamics
-> expert-utility binding and sparse discovery
-> real-workload utility headroom
```

## Current Judgment

The controlled evidence supports the mechanism through a frozen four-expert
discovery-and-switch primitive. The first registered real-code clause is also
complete: on the CrossCodeEval final-layer frozen expert pool, relevant context
changes counterfactual expert effects, but the selected identity is not split
stable and positive absolute headroom fails. This does not support an LLM
Router and does not adjudicate every unfiltered repository-code workload.

## Ordered Anchor Registry

| Order | Anchor | One decision question | Current verdict |
|---:|---|---|---|
| 00 | [`06_00`](06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md) | What evidence is sufficient to call a partition functional specialization? | Held-out function and value are required; route agreement and load are guards only. |
| 01 | [`06_01`](06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md) | Can unlabeled hidden-state structure provide a stable, trainable initial partition? | Geometry is reachable with the correct states; tested label-free selectors and real-proxy preservation are insufficient. |
| 02 | [`06_02`](06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md) | Which signed training dynamics determine preservation, crossing, and recovery? | Low-tail margin is the local budget; utility, boundary pressure, representation, Router, and actual step jointly move it. |
| 03 | [`06_03`](06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md) | Can training create useful expert functions and can sparse feedback discover them? | Correct exposure creates specialists; one challenger plus a lower-tail switch repairs the controlled selected-path blind basin. |
| 04 | [`06_04`](06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md) | Does unfiltered repository code contain stable uncaptured expert-function headroom? | **Active parent; `06_04_01` completed and failed on the registered CrossCodeEval final-layer surface.** |

Each parent anchor is a complete decision story. Its `subanchors/` directory
contains only local falsifiers, nuisance controls, or method audits needed to
support one clause of that story. Experiment IDs inherit both levels:

```text
A06_<parent>_<subanchor>_E<experiment>
```

## Evidence Compression

The earlier flat sequence contained repeated variants of common subtraction,
projection, whitening, denoising, warmup, spectral initialization, crossing
decomposition, and stopping-threshold tuning. These remain auditable evidence
inside the relevant subanchor and experiment group but no longer receive
separate parent decisions:

- common subtraction and global projection can improve load without identifying
  different useful experts;
- warmup strengthens all-position geometry but does not identify the clean
  route-relevant population;
- expert singular directions and manifold power iteration do not establish
  feature-aware initialization or positive low-tail margin;
- mean-DNS, denoised gradient selection, Router-row projection, Router learning-
  rate reduction, and early freeze do not provide a general preservation rule;
- after the Router/representation/optimizer freeze audit, more fixed-expert
  recovery decomposition does not change the method decision;
- after the lower-tail certificate passes, more synthetic stopping-threshold
  tuning does not address the real-workload premise;
- after `06_04_01`, more mining of the same frozen last-layer expert pool does
  not address training-time utility creation or the broader unfiltered scope.

Static 2x2 geometry and spectral-direction extraction are parked side evidence.
Their experiment records live under `A06_01_07` and `A06_01_06`; they are not
independent current lines.

## Claim Boundary

**Supported:** route-relevant geometry can initialize a partition; finite
low-tail margin describes local preservation; expert utility and signed
boundary pressure determine Router movement; conditional exposure can create
specialists; selected-only top-1 has a controlled counterfactual-feedback
failure; one challenger plus a lower-tail stopping rule repairs that failure in
the frozen four-expert bridge. On the registered CrossCodeEval surface,
relevant evidence changes final-layer counterfactual expert effects and the
matched-slot methodology is numerically validated.

**Weakened on the registered surface:** the frozen final-layer pool does not
provide a split-stable, context-favored positive headroom target that a better
Router could simply recover.

**Not supported:** a conclusion for all unfiltered repository code, natural
semantic experts, positive pretrained-LLM routing headroom, a deployable LLM
Router, joint long-horizon stability, many-expert scaling, systems-level
compute savings, or an MTP-Router benefit.

## Only Next Decision

Decide within [`A06_04`](06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md):

> After the registered CrossCodeEval final-layer pool failed split stability
> and positive absolute headroom, should A06 approve one training-time
> selective-sharing test on an explicit real rare/common workload?

Do not continue frozen-pool mining or design another Router before this human
decision is recorded.
