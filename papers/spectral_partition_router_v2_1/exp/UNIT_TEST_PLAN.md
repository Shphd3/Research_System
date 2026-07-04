# Unit Test Plan

## Tree mass tests

- continuous Gaussian with E=8;
- non-power-of-two E=6;
- each leaf receives target calibration count up to rounding.

## Tie tests

- identical atoms smaller than target mass;
- identical atom larger than target mass;
- lexicographic tie handling does not use sample index.

## Expert prototype tests

- flipping signs of SVD vectors does not change projective grouping;
- projective distances are invariant to sign;
- aligned expert prototypes improve alignment metric.

## Preservation tests

- if drift norm is below margin, route is unchanged;
- if drift crosses boundary, route may change;
- margin-aware update respects route-change budget.
