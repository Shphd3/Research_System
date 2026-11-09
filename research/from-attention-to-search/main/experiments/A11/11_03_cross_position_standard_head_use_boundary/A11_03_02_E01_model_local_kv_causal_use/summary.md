# A11_03_02_E01 Result Summary

## Conclusion

The registered strong behavioral-use hypothesis **failed**. All capability and
intervention guards passed, but the mean information-content increment was

\[
\bar\Gamma_{info}=0.01675<0.10,
\]

and `0/5` seeds reached the registered `0.10` threshold. Informative K=2 MTP
therefore did not reliably strengthen answer-switching control by layer-2
`U03` K/V beyond matched shared-aux in this task.

This does not show that MTP formed no branch information or that the ordinary
head had no weak dependence on `U03`. It rejects only the registered strong,
seed-stable answer-control increment.

## Primary Metric

For each condition \(o\),

\[
C_o=p_o^{diff}-p_o^{same},
\]

and the single primary comparison is

\[
\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}.
\]

| Seed | \(C_{NTP}\) | \(C_{shared\text{-}aux}\) | \(C_{info\text{-}MTP}\) | \(\Gamma_{info}\) |
|---:|---:|---:|---:|---:|
| 971 | 0 | 0 | 0 | 0 |
| 972 | 0 | 0 | 0.08374 | 0.08374 |
| 973 | 0 | 0 | 0 | 0 |
| 974 | 0 | 0 | 0 | 0 |
| 975 | 0 | 0 | 0 | 0 |
| mean | 0 | 0 | 0.01675 | 0.01675 |

Seed 972 was below threshold and highly direction-specific: almost all of its
switches came from donor branch `1` replacing receiver branch `3`. It is not a
stable cross-seed or branch-symmetric mechanism.

## Validity Guards

- All five seeds found a common capability-matched checkpoint at steps
  `500, 500, 900, 600, 700` for seeds `971–975` respectively.
- All three ordinary heads had confirmation clean accuracy `1.0`.
- Both active auxiliary heads had `U03` target accuracy `1.0`.
- Shared-aux versus informative-MTP ordinary-head answer CE gaps were
  `0.00010–0.00706`, below the `0.05` limit.
- Cache replay errors were at most `2.36e-14`; self-patch errors were `0`.
- Same-branch answer-change rates were `0`; positive-control donor switching
  was `1.0` for every seed and condition.
- All 12 ordered branch pairs had 1,024 confirmation examples per condition
  and seed.

The result is therefore a registered mechanism failure, not insufficient
evidence from capability or implementation failure.

## Central Figure

![Model-local K/V causal-use result](figures/kv_causal_use_main.png)

Purpose: compare within-model controlled switch effects and the registered
informative-MTP-minus-shared-aux increment. The left panel shows \(C_o\) for all
three conditions; the right panel shows \(\Gamma_{info}\) with zero and the
`0.10` threshold. Four seeds are exactly zero. Seed 972 is positive but remains
below threshold. The figure supports rejection of a reliable strong behavioral
increment; it cannot reject weak margin-only or redundant use.

## Secondary Observation

The informative-MTP minus shared-aux donor-margin change was positive in `4/5`
seeds, with mean `0.560`, but it was dominated by seed 972 and did not usually
flip the answer. This is a candidate weak or redundant influence, not a second
success criterion and not grounds to override the primary verdict.

## Claim Boundary and Next Decision

Supported: informative MTP can form a directly supervised branch state, but in
this controlled two-layer task it does not reliably make layer-2 `U03` K/V a
strong, independently answer-controlling channel for the ordinary head beyond
matched shared-aux.

Not supported: total non-use of MTP information, general MTP failure, real-task
value, longer-horizon behavior, or conclusions about K-only, V-only, or Q.

Exactly one next decision: decide whether the next audit should target the
stable weak margin effect or close this interface and seek a task where the
early source state is structurally necessary. No sweep is authorized by this
result.
