# Mainline Report: From Spectral Decoupling to Continual-Learning Factorized MoE

This markdown mirrors the English LaTeX report and is provided for easier reading.

## Recent Updates

Our long-term goal is to build a Hierarchical MoE that can move toward the target of “learn from very few examples and do not forget old knowledge.”

The Phase8p2 result changes the mainline in a precise way:

1. The factorized `u50_ext` block has formal CL value.
2. Routing is not yet established as an additional CL mechanism.
3. The best structural model is near but still below the replay baseline under strict matched-forgetting criteria.
4. The next bottleneck is router-function alignment, not more band slicing.

The concise update is:

$$
\text{formal CL value of } u50\_ext \text{ factorization is established, but routing advantage is not established.}
$$

## Background and Theoretical Critique

The original intuition was that language follows a Zipfian distribution, so a MoE should separate high-frequency and low-frequency knowledge. This intuition remains useful, but it is incomplete.

The main theoretical correction is:

$$
\text{separating data is not the same as creating useful experts.}
$$

A router can separate tokens by domain, frequency, or spectral position, but that does not imply that the selected expert has lower next-token loss, or that updating this expert will cause less forgetting.

## Hypotheses and Mathematical Modeling

### H1: common/plastic factorization is necessary

A stable common branch should preserve high-frequency and general language ability, while a plastic branch should absorb few-shot mid-tail updates.

### H2: `u50_ext` is the current best practical plastic input

Full PCA tail is too broad, and `u25` is too narrow for CL. `u50_ext` offers a better tradeoff between learnability and functional coverage.

### H3: current learned routing is not yet aligned with expert advantage

A router that separates inputs can still fail if its scores do not predict which expert has lower token loss or lower forgetting risk.

### H4: PCA is a diagnostic scaffold, not the final semantic basis

Phase7 suggests that sparse dictionary features reconstruct hidden states better than PCA top-K, so future hierarchy may need feature-based rather than purely PCA-based decomposition.

## Factorized Block

The current responsible architecture is:

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}}
+
F_c(x)
+
F_p(x_{u50\_ext})
$$

A routed version remains a candidate:

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}}
+
F_c(x)
+
\sum_e g_e(\phi(x,x_{u50\_ext}))F_e(x_{u50\_ext})
$$

But the routed version should only be expanded if router-function alignment is verified.

## Empirical Study

Phase8p2 fixed:

- expert input: `u50_ext`;
- adaptation horizon: `U=8`;
- compared groups: `G0`, `G2_u50_ext`, `G4_u50_ext`, `G0_ER`;
- main regime: `0.5x`.

Main result:

| Group | LG | FC | RAS | ReachRate | Matched Forgetting |
|---|---:|---:|---:|---:|---:|
| `G0` | -0.000251 | 0.000786 | -0.001121 | 0.450 | -0.000017 |
| `G0_ER` | 0.000774 | -0.000282 | 0.000571 | 0.367 | -0.000502 |
| `G2_u50_ext` | 0.000803 | 0.000082 | 0.000503 | 0.217 | -0.000212 |
| `G4_u50_ext` | 0.000785 | -0.000122 | 0.000671 | 0.200 | -0.000184 |

The gates are:

1. `G2_u50_ext > G0`: true.
2. `G4_u50_ext > G2_u50_ext`: not established.
3. best structure vs `G0_ER`: near, but below under matched forgetting and ReachRate.

## Next Iteration

Immediate experiments:

1. router-function audit;
2. oracle routing upper bound;
3. advantage-supervised router, only if oracle routing shows clear upside;
4. common/plastic cooperation ablation;
5. `u50_ext` projection cost and surrogate extractor.

The next step should not be hierarchy yet. It should be to determine whether routing has real functional upside beyond the already established split-dense `u50_ext` block.
