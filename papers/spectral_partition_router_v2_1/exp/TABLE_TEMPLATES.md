# V2.1 Table Templates

Fill only after experiments run.

## Table 1: Equal-mass sanity

| Data | Method | Cal LoadCV ↓ | Holdout LoadCV ↓ | Max error ↓ | Gap ↓ | Tie rate ↓ | Margin p05 ↑ |
|---|---|---:|---:|---:|---:|---:|---:|
| Gaussian | Vanilla linear |  |  |  |  |  |  |
| Gaussian | SPR-RandomAxis |  |  |  |  |  |  |
| Gaussian | SPR-FixedBasis |  |  |  |  |  |  |
| Gaussian | GA-SPR-Local |  |  |  |  |  |  |
| Gaussian | GA-SPR-Expert |  |  |  |  |  |  |
| Gaussian | Balanced assignment control |  |  |  |  |  |  |

## Table 2: Assumption ladder

| Regime | Method | LoadCV ↓ | NMI ↑ | Purity ↑ | Within-var ↓ | Margin p05 ↑ |
|---|---|---:|---:|---:|---:|---:|
| Isotropic unstructured |  |  |  |  |  |  |
| Isotropic clusterable |  |  |  |  |  |  |
| Expert-aligned isotropic |  |  |  |  |  |  |
| Low-margin overlapping |  |  |  |  |  |  |

## Table 3: Expert-guided geometry

| Expert setting | Method | LoadCV ↓ | NMI ↑ | Purity ↑ | Proto spread ↑ | Proto align ↑ | Margin p05 ↑ |
|---|---|---:|---:|---:|---:|---:|---:|
| Standard init |  |  |  |  |  |  |  |
| Aligned |  |  |  |  |  |  |  |
| Noisy |  |  |  |  |  |  |  |
| Random |  |  |  |  |  |  |  |
| Clustered |  |  |  |  |  |  |  |

## Table 4: Margin-aware update

| Update method | LoadCV ↓ | NMI ↑ | Flip rate ↓ | Margin p05 ↑ | Accepted updates | Val loss ↓ |
|---|---:|---:|---:|---:|---:|---:|
| Frozen GA-SPR |  |  |  |  |  |  |
| Naive slow update |  |  |  |  |  |  |
| Margin-aware update |  |  |  |  |  |  |
| Hysteresis update |  |  |  |  |  |  |
| Route-budget update |  |  |  |  |  |  |

## Table 5: Controlled training

| Router | Val loss ↓ | LoadCV ↓ | NMI ↑ | Purity ↑ | Flip ↓ | Margin p05 ↑ | Spec ↑ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fixed vanilla linear |  |  |  |  |  |  |  |
| Trainable linear |  |  |  |  |  |  |  |
| Trainable linear + LB loss |  |  |  |  |  |  |  |
| Balanced assignment control |  |  |  |  |  |  |  |
| Frozen GA-SPR |  |  |  |  |  |  |  |
| GA-SPR-init-linear |  |  |  |  |  |  |  |
| GA-SPR-Expert |  |  |  |  |  |  |  |
| Margin-aware GA-SPR |  |  |  |  |  |  |  |

## Table 6: Failure modes

| Failure mode | Violated assumption | Expected failure | Observed metric |
|---|---|---|---|
| No latent structure | feature coherence not identifiable | NMI near chance |  |
| Large atom | exact deterministic split impossible | tie/atom failure |  |
| Random expert weights | expert alignment absent | expert guidance not useful |  |
| High drift + low margin | preservation absent | high flip rate |  |
| Calibration/holdout shift | stable distribution absent | holdout LoadCV high |  |
