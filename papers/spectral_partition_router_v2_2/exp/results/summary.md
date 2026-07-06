# V2.2 Static Dispatch Experiment Summary

## What We Established

The E1--E5 suite supports the static clean-case claim: under frequency-uniform,
globally spectrally isotropic, locally recoverable feature-family data,
BFSR-Cluster builds a balanced and feature-consistent static router using only
calibration features. In E1, BFSR-Cluster reaches LoadCV 0.003, family
consistency 0.990, and cluster accuracy 0.986.

## What The Experiments Show

- E2 confirms the impossibility anchor: when labels are independent of isotropic
  features, the best admissible label-free method has expert information
  fraction 0.002, i.e. spectral isotropy alone does not identify feature-family
  dispatch.
- E3 shows that specialization follows local recoverability. As separation
  increases from 0.45 to 2.50, cluster accuracy rises from 0.063 to 0.942, and
  family consistency rises from 0.294 to 0.956.
- E4 shows that spectral normalization is metric repair. On anisotropically
  distorted structured data, whitening changes cluster accuracy from 0.250 to
  0.958; on distorted null data, whitening still leaves expert information
  fraction at 0.002.
- E5 shows why frequency uniformity matters for mass balance. On imbalanced
  feature frequencies, with whitening used to keep the routing metric controlled,
  equal-number BFSR has LoadCV 0.149 while mass-aware BFSR has LoadCV 0.029.

## Full-Run Setup

- Seeds: 0, 1, 2, 3, 4
- Dimension: 16
- Feature families: 32
- Experts: 4
- Calibration examples: 8000
- Holdout examples: 16000
- Feature recovery: k-means with known K, 8 restarts, fitted only on calibration features

## Reliability Assessment

The current results are reliable for the narrow static claim because the suite
uses held-out evaluation, multiple seeds, an oracle upper bound, an isotropy-only
null, a recoverability sweep, a normalization ablation, and a frequency ablation.

They are not evidence for downstream task learning, learned-router dynamics,
semantic expert identity, automatic selection of K, or route preservation during
training.

## Artifact Map

- Runner: `papers/spectral_partition_router_v2_2/exp/run_static_dispatch_suite.py`
- Source package: `papers/spectral_partition_router_v2_2/exp/src/static_bfsr_suite.py`
- Raw metrics: `papers/spectral_partition_router_v2_2/exp/results/*_raw.csv`
- Aggregates: `papers/spectral_partition_router_v2_2/exp/results/*_aggregate.csv`
- Paper tables: `papers/spectral_partition_router_v2_2/latex/tables/`
- Paper figures: `papers/spectral_partition_router_v2_2/latex/figures/`
