# V2.1 Baselines

## Count controls

- Balanced assignment control.

This is not a feature router and should never be the main method.

## Linear routers

- Fixed random linear top-1.
- Trainable linear top-1.
- Trainable linear top-1 + load-balancing auxiliary loss.
- GA-SPR-init-linear.

## Prototype routers

- Regular simplex prototype top-1.
- Expert-SVD top-1.
- MPI-row top-1 if oriented rows are available.

## GA-SPR routers

- SPR-RandomAxis.
- SPR-FixedBasis.
- GA-SPR-Local.
- GA-SPR-Expert.
- GA-SPR-ExpertLocal.
- GA-SPR-MarginUpdate.
