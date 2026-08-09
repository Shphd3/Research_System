# Thinking Card: Does Local-HMT Have Covariance-Specific Value?

- **Phenomenon:** In the completed two-seed 10B study, Local-HMT had the lowest endpoint NLL point estimate in both seeds, but its paired advantage over Centered-Full was decisive only in seed 17.
- **Mechanism judgment:** Layer-local covariance-ranked H/M/T may provide a routing inductive bias that a generic dynamic low-dimensional constraint cannot reproduce.
- **Strongest rival:** The weak Local-HMT advantage comes only from centering, smooth updates, or a dynamic low-dimensional bottleneck rather than covariance-rank identity.
- **Largest uncertainty:** The completed matrix had no Local-Random arm, while the old Relay-Random mixed the complete eigenbasis and therefore had materially harder target motion.
- **Judgment-changing evidence:** After matching dimensions, target-subspace motion, statistics, refresh cadence, EMA, Grassmann update, and continuity guard, Local-HMT beats Local-Random in seeds 17 and 29 with paired-document support.
- **Current next decision:** Run only the two missing 10B Local-Random-Matched jobs and compare them with the completed Local-HMT and Centered-Full runs.

