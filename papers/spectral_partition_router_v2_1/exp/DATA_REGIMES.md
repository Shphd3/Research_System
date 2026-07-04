# V2.1 Data Regimes

## R1: Isotropic unstructured

```text
X ~ N(0, I)
```

Expected: equal mass possible; feature NMI not meaningful.

## R2: Isotropic clusterable

```text
F uniform
X = mu_F + noise
whiten globally
```

Expected: feature coherence possible if split directions find the cluster structure.

## R3: Expert-aligned isotropic

Same as R2, but expert weights contain principal directions aligned with `mu_F`.

Expected: GA-SPR-Expert should improve NMI/purity.

## R4: Low-margin overlapping

Same as R2, but larger noise / smaller separation.

Expected: equal mass possible; training preservation fragile.

## R5: Atom-supported / discrete

Large repeated feature atoms.

Expected: exact deterministic equal mass may be impossible; report tie/atom boundary.
