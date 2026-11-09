# A to C and B to C: leading full-O operators and endpoint differences

## 1. Purpose

**A/B/C differ measurably, but B is closer to C than A is**, both for full-O differences and leading16 full-weight operators. This parameter-only supplement asks how strong processing channels differ, without gradients. It serves the shared-versus-conditional-learning question by testing proximity as a compatibility proxy, not by identifying task causality.

## 2. Model

Read O from the trained Qwen3-0.6B final-layer Q/K/V/O states. A learns consistent new labels, B reversed new labels only, C mixes old and reversed-new supervision from the common acquired-old state. Three continuation orders share that state. Existing1200 old/new accuracy is A100%/100%, B0%/99.25%, C99.83%/99.67%.

For a=Wc, the exact SVD relation is

\[
W=\sum_i\sigma_i u_i v_i^\top,\qquad
Wc=\sum_i\sigma_i u_i(v_i^\top c).
\]

Large singular directions are strongly amplified input/output processing channels. Actual input alignment also matters; rank alone does not assign rule semantics. Compute endpoint differences T_AC=W_C-W_A and T_BC=W_C-W_B, not executed training paths. Separately compare full-weight truncated operators

\[
W_{X,k}=\sum_{i=1}^{k}\sigma_{X,i}u_{X,i}v_{X,i}^{\top},\qquad
d_k(X,C)=\frac{\|W_{C,k}-W_{X,k}\|_F}{\|W_{C,k}\|_F}.
\]

This retains gains, signs, and paired left/right directions. Leading16 of a difference is not the difference of leading16 operators.16 is primary,8/32 fixed sensitivity. No new training, forward, gradient or TEST; behavior is inherited exposed-DEV evidence.

## 3. Hypothesis

Candidate: A/C leading channels might be closer than B/C. Rival: A/C new mappings differ whereas B/C agree; parameter proximity may reflect the common new requirement, rather than old retention. Supervision, exposure and Q/K/V also differ. Truncated-operator comparisons address information lost by plain subspace overlaps, while cutoff instability remains. See [frozen supplement Protocol](protocol.md).

## 4. Conclusion

All12 difference SVDs completed.1200 equal continuation-order means:

| Parameter comparison | A to C | B to C |
| --- | ---: | ---: |
| Full difference Frobenius norm | 3.799585 | 2.988761 |
| Full difference / full C norm | 8.876% | 6.982% |
| Difference maximum singular value | 1.223322 | 1.047897 |
| Difference sigma1 / C sigma1 | 34.286% | 29.326% |
| Difference first16 squared energy | 79.621% | 78.237% |
| Leading16 full-operator difference / C leading16 norm | 38.697% | 30.316% |
| Signed leading16 operator cosine | 0.9222 | 0.9526 |

Full and rank16 operator distances are lower for B/C in every continuation order. At ranks8/16/32, normalized truncated differences average37.947%/38.697%/32.929% for A/C and32.638%/30.316%/28.644% for B/C. T_AC/T_BC rank16 U/V overlaps are0.8239/0.2953; signed matrix cosine0.5005.

The candidate A/C-closer ordering is not supported. Leading channels change measurably, but proximity does not track old retention: B/C are closer with different old function; A/C are farther and both retain old rules. This does not deny linear processing meaning or establish absent all-parameter specialization. Mechanism acceptance/closure remain Unknown.

## 5. Analysis

Relative to full C rank16 coordinates, difference squared-energy blocks are:

| Output/input coordinates | A to C | B to C |
| --- | ---: | ---: |
| Both leading | 1.708% | 2.642% |
| Leading output / other input | 5.937% | 7.209% |
| Other output / leading input | 3.770% | 4.269% |
| Both other | 88.584% | 85.880% |

Most endpoint differences lie outside the leading16 full-C coordinates, yet approximately80% of each difference lies in its own leading16 components. These are different reference spaces. Full C rank16 explains only approximately5.5% matrix energy; other coordinates are not functionless.

Using C's continuation displacement D_C as a separate reference, both-leading energy is65.114% for A/C and34.548% for B/C. Leading-output/other-input energy is12.593% versus38.383%. B/C differences often retain dominant C-displacement output coordinates while changing input couplings. This is parameter localization, not an identified old-rule repair function.

An **AI candidate explanation** of B/C proximity is their common reversed-new requirement, unlike A's consistent requirement. C additionally receives old supervision; B does not. These factors were not independently isolated. B has24000 new answers versus C12000 new+12000 old; changed Q/K/V also supplies different O inputs. Those remain causal alternatives.

Sigma1(T)=max_{||c||=1}||Tc|| measures maximal same-input linear difference. A7%–9% Frobenius difference can coexist with a29%–34% change relative to C's maximal gain; these are operator capabilities, not task-effect percentages.30%–39% truncated distances show measurable changes in strong paired channels, but small16/17 gaps can move cutoff directions. Truncated differences may exceed full differences because residual differences can cancel; they are not orthogonal parts of the full difference. Fixed-rank means preserve ordering without eliminating every cutoff alternative.

For the parent problem, distinguish inherited full-weight channels, learned displacement channels and conditional task function. C is already a shared-compatible example. Separate-module net utility is unmeasured. **AI suggestion, not executed:** insert leading16 T_BC or its residual while freezing other parameters, then evaluate both tasks. This would test directional function without gradients; the current supplement is parameter-only.

[Detailed evidence](detailed.md) · [Artifact manifest](artifact_manifest.json)
