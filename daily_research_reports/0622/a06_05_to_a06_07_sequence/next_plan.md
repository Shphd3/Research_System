# Next Plan After A06_05--A06_07

## Current State

The three-anchor sequence is closed:

- A06_05: residual covariance / structured residual geometry remains after common-centering.
- A06_06: oracle feature-centroid initialization reaches perfect held-out feature routing.
- A06_07: simple label-free global common / residual controls improve load but do not recover feature routing.

## Main Decision

Do not promote global common-centering, top-PC removal, or whitening as a method candidate.

The next method must add one of two missing ingredients:

1. label-free feature discovery, so router directions align with feature structure rather than only removing common load bias;
2. anti-lockin training control, so a known-good or pseudo-good partition is not destroyed by top-1 dynamics.

## Real DCLM Gate

Existing DCLM evidence already shows that real text is not a simple step-0 common-dominance copy of the toy setting:

- `05_04_03`: on DCLM, common-centering reduces step-0 load, but common margin is not the dominant step-0 logit source.
- `06_02`: early training amplifies common-logit concentration through hidden-producer drift and gate-hidden interaction.

Therefore the next DCLM experiment should not ask:

```text
Does global common-centering reduce load?
```

It should ask:

```text
Can a feature/proxy-aware initialization or anti-lockin control improve a feature/proxy specialization metric while preserving LM loss?
```

## Minimal DCLM Protocol To Draft Next

Experiment role:
Real-model proxy transfer / anti-lockin gate.

Model/data:
Use the existing small Qwen-style top-1 MoE DCLM setup from `05_04_03` / `06_02`.

Candidate conditions:

- baseline random top-1;
- common-centering only, as a load-control negative baseline;
- low-rank empirical-centered / calibrated M4-style static target, if frozen hidden activations are available;
- pseudo-feature clustering initialization on early hidden states;
- anti-lockin schedule from a pseudo-oracle partition.

Primary metric:
Not load. Use a route-feature proxy metric, such as:

- route consistency over stable token/context clusters;
- agreement with an empirical-centered M4 / weighted top-r target;
- route persistence without many-to-one collapse;
- LM loss / validation CE as the task-preservation guard.

Required guard:
Report load, but treat load-only improvement as failure unless route-feature proxy also improves.

## Stop Rule

If the DCLM run cannot define a feature/proxy specialization metric before execution, park it. A06_07 shows that load-only improvements can be actively misleading.
