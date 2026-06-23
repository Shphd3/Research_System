# Exp Line: Real-DCLM Proxy Gating Iteration A06_10-A06_15

## Parent Question

Can we move from synthetic feature routing to real-DCLM gating initialization without confusing load balance with expert specialization?

## Final State Of This Iteration

Main conclusion:

```text
Real-data proxy features can be measured.
Proxy centers can initialize a router.
Ordinary DCLM training does not preserve that proxy routing.
Therefore the next mainline is preservation / anti-feedback, not utility binding.
```

## Decision Chain

```text
A06_10 proxy discovery
-> supported with boundary
-> real DCLM hidden geometry has stable label-free proxy clusters

A06_11 proxy-to-router bridge
-> supported with boundary
-> raw proxy centers linearly initialize raw-input routing

A06_12 training preservation
-> not supported
-> proxy routing collapses by step 5--10 under ordinary LM training

A06_13 failure decomposition
-> supported
-> first failed stage is training feedback override

A06_14 utility binding
-> parked
-> invalid before routing preservation is restored

A06_15 utility-aware init
-> parked
-> invalid before A06_14 has a utility table
```

## Anchor Decisions

| Anchor | Question | Decision | Main Evidence | Next |
| --- | --- | --- | --- | --- |
| A06_10 | Do real hidden states define stable proxy clusters? | Supported with boundary | Step-10 residual late-layer stability NMI 0.5451 vs random 0.0002 | Use proxy labels |
| A06_11 | Can proxy centers become router rows? | Supported with boundary | Step-0 raw-center raw-input proxy-route NMI 0.7449 vs random 0.0343 | Test training |
| A06_12 | Does training preserve proxy routing? | Not supported | Raw-center NMI 0.7549 at step 0, 0.0410 at step 5, 0.0131 at step 10 | Decompose failure |
| A06_13 | Where is the first failure? | Supported | Proxy and bridge pass; preservation fails with comparable LM loss | Test preservation mechanisms |
| A06_14 | Do routed experts have proxy utility? | Parked | A06_12 preservation failed | Resume after preservation |
| A06_15 | Can utility improve initialization? | Parked | A06_14 dependency absent | Resume after utility table |

## What We Now Know

1. Real DCLM has measurable label-free proxy structure.
2. The proxy is not mainly explained by the measured frequency or position nuisances.
3. Raw-center rows are a strong step-0 linear router initialization.
4. The standard LM objective quickly destroys the initialized proxy routing.
5. The collapse is not caused by worse LM loss.

## What We Do Not Know Yet

1. Whether a preservation intervention can keep proxy routing through step 10.
2. Whether preserved proxy routing would bind to expert utility.
3. Whether utility-aware initialization helps after preservation is solved.

## Next Mainline

The next anchor should not be A06_14. It should test preservation:

```text
Can we keep raw-center proxy routing through the step-5/10 collapse window?
```

Candidate interventions:

- freeze router for early steps;
- delay router updates;
- lower router learning rate;
- add proxy-route preservation loss;
- add common/load anti-collapse regularization.
