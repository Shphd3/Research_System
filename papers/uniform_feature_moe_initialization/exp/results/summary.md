# Synthetic Experiment Summary

Conclusion: the main supported mechanism is representation geometry. Uniform top-1 expert usage appears when token directions are close to the spherical model and expert prototypes are well spread. Covariance isotropy alone is insufficient: the four-axis counterexample has condition number 1 but nonuniform load. In the elliptical toy setting, spectral shrinkage and whitening repair anisotropic features and restore the routing diagnostic.

Rows: 481

## Terminology

- LoadCV: coefficient of variation of expert load; lower means more uniform expert usage.
- init_error: Monte Carlo estimate of the fixed cell-mass imbalance caused by one prototype draw.
- sampling_error: finite-token deviation around that fixed cell mass.
- condition_number: largest covariance eigenvalue divided by the smallest nonzero covariance eigenvalue; 1 is spectrally uniform.
- effective_rank: entropy-based count of active covariance directions; higher means less spectral concentration.

## Key Readout

- E1: symmetric spherical prototypes have mean LoadCV 0.00822; clustered prototypes have 0.1134, showing the prototype-geometry side of the theorem.
- E2: for d=64, E=8, the random-prototype geometry floor is init_error 0.09306; sampling_error decreases from 0.16 at N=1000 to 0.03061 at N=50000.
- E3: exact SVD recovers expert directions in both cases, but symmetric prototypes have alignment 1 and LoadCV 0.009222, while clustered prototypes have alignment 1 and LoadCV 0.1606; spectral alignment alone is not a balance guarantee.
- E4: the four-axis distribution has covariance condition_number 1 but LoadCV 0.3536 and max/min load ratio 2; spectral isotropy alone is not directional uniformity.
- E5: at anisotropy alpha=20, raw condition_number is 419.5 and effective_rank is 2.615; whitened normalization gives condition_number 1.003, effective_rank 64, and LoadCV 0.005122.
- E6 control: unconstrained top-1 mean LoadCV is 0.1011; exact balanced assignment forces LoadCV 0 with mean selected-score drop 0.0003852. This is forced count equality, not representation geometry.

## Tables

- `tables/e1_uniform_sphere.md`: prototype geometry and expert load.
- `tables/e2_high_dim_geometry_floor.md`: fixed random-prototype geometry floor versus sampling noise.
- `tables/e3_spectral_prototypes.md`: spectral alignment is not sufficient for balanced usage.
- `tables/e4_covariance_counterexample.md`: covariance-isotropy counterexample.
- `tables/e5_anisotropy_whitening.md`: representation repair by spectral flattening under preprocessing.
- `tables/e6_balanced_assignment.md`: non-geometric forced-balance control and score cost.

## Claim Boundary

These are synthetic controlled experiments. They do not establish semantic expert specialization, downstream utility, or that trained language-model hidden states naturally satisfy the spherical or whitened assumptions.
