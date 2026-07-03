# Experiment Plan: Uniform Feature MoE Initialization

## Decision

The first paper should close the simplest case before moving to nonuniform
features:

```text
If feature frequencies are uniform and the route-relevant feature states have
approximately uniform geometry, can a center-initialized top-1 router distribute
features evenly and preserve the assignment through training?
```

## Terms

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| Uniform feature frequency | Every synthetic feature appears equally often. | Four features with probability 0.25 each. | Removes Zipf frequency as a rival explanation. | Real language behavior. |
| Uniform feature geometry | Feature states have comparable norms and no dominant singular direction. | Route-position hidden states after centering, or idealized points on a sphere. | Makes the clean mathematical case auditable. | Natural hidden-state spectra. |
| Center initialization | Initialize router rows from feature centers. | Cluster or oracle centers from route-position states. | The proposed clean baseline. | Label-free route-position discovery. |
| Margin | Safety distance to the nearest competing expert. | Matched expert logit minus strongest competitor logit. | Decides whether routing survives drift. | Expert utility. |
| Matched preserve fraction | Whether the original feature-to-expert identity survives. | Fraction of features still routed to their initial matched expert. | Stronger than NMI because NMI ignores expert swaps. | Functional specialization. |

## Required Story From The Meeting

The 2026-07-03 meeting asks for a self-contained paper on the uniform case:

```text
uniform features
uniform spectral / representation space
the first optimal or clean baseline
theory proof
experiment result
claim closure before studying nonuniform spectra or Zipf frequency
```

This differs from the broader current research system, where the next live
method question is gradient/Fisher route-state selection. The paper should not
claim that the label-free selector is solved. It should close the clean baseline
case that the advisor wants separated.

## Minimal Experiment Set For The Draft

### E1: Two-dimensional uniform circle routing

Purpose:

```text
Show why random routing centers are not enough even with uniform token
features, and why balanced center geometry removes the initialization floor.
```

Setup:

- tokens uniformly on the unit circle;
- experts represented by unit routing centers;
- top-1 nearest-center routing;
- compare random centers, evenly spaced centers, minimum-angle centers, and
  repulsive optimized centers.

Primary metric:

```text
normalized load error = m max_j |p_hat_j - 1/m|
```

Required decomposition:

```text
p_hat_j - 1/m = (p_j - 1/m) + (p_hat_j - p_j)
```

Pass condition:

- sampling error decays as token count grows;
- random-center initialization error does not vanish with token count;
- evenly spaced centers remove the initialization floor.

### E2: Controlled no-position Transformer-MoE center initialization

Purpose:

```text
Show that route-position centers distribute four uniform features cleanly.
```

Setup:

- one causal attention layer;
- one top-1 MoE layer;
- four equally frequent features;
- no learned absolute position embeddings;
- route on the final token of the repeated feature slot.

Conditions:

- random router;
- all-position k-means;
- route-position k-means;
- oracle feature centers;
- row-gap scaling from A06_23.

Primary metric:

```text
matched preserve fraction
```

Secondary metrics:

```text
feature NMI, margin p05, sign-flip rate, max load, target accuracy
```

Pass condition:

- route-position center initialization reaches high feature NMI;
- matched preserve fraction remains high when margin is above the safe region;
- `q=0.02` or an equivalent thin-margin stress fails.

### E3: Rival method comparison

Purpose:

```text
Show why the clean baseline is not replaced by global common subtraction,
warmup-only all-position clustering, expert SVD, or MPI.
```

Use existing evidence:

- A06_24: all-position common subtraction does not match route-position centers
  and keeps negative rare-margin lower tail.
- A06_25: warmup improves all-position and expert SVD source quality, but route
  centers remain stronger.
- A06_26: MPI improves feature NMI over vanilla but fails the margin guard.

Primary conclusion:

```text
The clean uniform case is center-initialized routing with a positive margin
guard, not a stronger router alone.
```

### E4: Planned label-free source selection

Purpose:

```text
Define the next experiment after the paper baseline, not as a claim in this
paper.
```

Candidate selectors:

- gradient-norm route-position selector;
- gradient-weighted clustering;
- Fisher-metric clustering.

Required comparison:

```text
all-position controls vs route-position positive control vs gradient/Fisher
selector
```

Main guard:

```text
feature NMI must improve together with margin p05.
```

## Paper Claim Boundary

Can claim if the above is written cleanly:

```text
In a controlled uniform-feature setting, center initialization gives a clean
top-1 routing baseline, and preservation is controlled by a finite positive
margin basin.
```

Cannot claim:

```text
real semantic experts
label-free route-position discovery
Zipf / nonuniform frequency solution
common/rare utility
real-DCLM preservation
MPI or spectral routing failure in its intended large-scale setting
```
