# A11_03_02_E02 Result Summary

## Conclusion

The registered verdict is **insufficient**, because the preregistered
single-shuffle accuracy guard failed. The measured result nevertheless gives
two clear bounded observations:

1. exact layer-2 `U03` source K/V contains linearly decodable branch
   information in all three training conditions: confirmation accuracy and all
   four class recalls were `1.0` for every seed;
2. informative-MTP did not improve the registered held-out probe CE over
   matched shared-aux:

   \[
   \bar\Gamma_{\mathrm{read}}
   =
   -0.002299\ \text{nat/example},
   \qquad
   95\%\ \mathrm{CI}
   =
   [-0.004502,-0.000173].
   \]

Four of five paired seeds were nonpositive. This does not support
MTP-specific branch readability at this interface. Because both conditions
already had perfect accuracy and near-zero CE, it also must not be rewritten
as evidence that informative-MTP contains less branch information.

## Primary Metric

The single registered comparison was

\[
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}.
\]

| Seed | shared-aux CE | informative-MTP CE | \(\Gamma_{\mathrm{read}}\) |
|---:|---:|---:|---:|
| 971 | 0.001021 | 0.005675 | -0.004654 |
| 972 | 0.000240 | 0.001165 | -0.000925 |
| 973 | 0.000340 | 0.000437 | -0.000097 |
| 974 | 0.000688 | 0.006637 | -0.005949 |
| 975 | 0.000351 | 0.000222 | 0.000129 |
| mean | 0.000528 | 0.002827 | -0.002299 |

The paired nuisance-and-seed bootstrap interval was entirely below zero, but
the registered label-shuffle guard failed, so the frozen decision remains
`insufficient`.

## Source Formation

All 15 model instances reached confirmation branch accuracy `1.0` from exact
\([K_{2,T};V_{2,T}]\), with recall `1.0` for every branch. The replay also
reproduced the original selected steps, capability values, K/V patch switch
rates, and donor-margin changes for all five seeds and three conditions.

This rules out a simple explanation of E01: the patched K/V object was not
absolutely devoid of stable linear branch information. It does not show that
the readable information was created by MTP, because NTP and shared-aux were
equally perfectly readable.

## Secondary Geometry Observation

The preregistered Fisher separation ratio was larger for informative-MTP than
for shared-aux in `5/5` seeds, by factors `16.90, 9.83, 10.31, 2.91, 49.55`.
The change came mainly from lower within-branch nuisance dispersion; not every
pairwise centroid distance increased.

This supports a candidate geometric interpretation: informative future
supervision may compact nuisance variation and organize branch geometry even
when the branch label is already perfectly readable. Fisher separation was a
secondary diagnostic, so it cannot override the primary verdict and cannot
establish standard-head use.

## Failed Shuffle Guard

The contract required every shuffled-label probe to have confirmation accuracy
at most `0.30`. Three of 15 probes exceeded that limit; the maximum was
`0.3357`. Across all 15 probes, however, the mean shuffled accuracy was
`0.2209` and mean shuffled CE was `1.4427`, compared with four-class chance CE
\(\log 4=1.3863\).

The post-result diagnosis is that a single random label shuffle is a poorly
calibrated maximum-accuracy guard once the representation already forms four
nearly perfect clusters: accidental cluster-to-label alignment can push one
run above `0.30` without broad train-confirmation leakage. This diagnosis does
not retroactively change the registered verdict.

## Central Figure

![Exact source-K/V readability audit](figures/source_kv_information_audit.png)

The left panel shows held-out branch-probe CE for all three conditions. The
right panel shows paired \(\Gamma_{\mathrm{read}}\). It supports the absence of a
positive CE improvement under informative-MTP. It does not display causal use
or the secondary Fisher geometry.

## Claim Boundary And Next Decision

Combined with E01, the evidence now says:

- exact source K/V is linearly branch-readable under every objective;
- informative-MTP does not add registered probe readability over shared-aux;
- informative-MTP produces a strong secondary nuisance-compaction pattern;
- the ordinary head still shows no stable strong answer-control increment from
  this K/V interface.

The current task leaves a direct `BR_z` bypass and saturates both answer
prediction and branch decoding. Therefore it cannot determine whether the
ordinary head would consume the MTP-organized geometry when that route is
necessary.

Exactly one next decision: design and validate a `relay-required` A11 carrier
in which the answer cannot bypass the early message, and require a
non-saturated shared-aux control before comparing training objectives. Shared
unembedding and K/V/Q component sweeps remain parked until that carrier is
valid.
