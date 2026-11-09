# A15_02_03_E01 Result: Semantic Concentration In True Attention Heads Versus MLP-Input Groups

## Conclusion

The typed result is:

- `attention_sparse_concentration_pass` for coarse, fine, and fine-relative discriminability;
- `attention_typical_concentration_fail` for all three metrics;
- `mlp_concentration_fail` for fixed contiguous MLP-input groups;
- `within_unit_eight_band_spectral_fail` under the registered 16-d random-orientation control.

Thus, semantic discriminability is exceptionally concentrated in a sparse set of true pre-`o_proj` attention heads, not broadly improved across heads. After `o_proj`, residual addition, and RMSNorm, fixed contiguous 128-d MLP-input groups are not more special than random groups. The qualified attention-head signals also do not identify a fixed within-head covariance-rank band.

## Object And Metric

The frozen `/data/share/Qwen3-8B` snapshot was hooked at all 36 inputs to `self_attn.o_proj` and all 36 direct MLP inputs. The former was reshaped into 32 architectural query heads ×128 dimensions; the latter was split into 32 contiguous 128-d coordinate groups. Both branches reused the exact 512-description, 8×8 coarse/fine semantic cube and the independent 65,536-token DCLM calibration set from A15_02_E01.

For each semantic level, discriminability is

\[
D=\frac{\operatorname{tr}(B)}{\operatorname{tr}(W)+\epsilon},
\qquad
C=\log\frac{D_{unit}}{D_{full}}.
\]

\(B\) is between-class variance and \(W\) is within-class template/fact variance. \(C\) is a dimensionless part-versus-whole discriminability ratio, not accuracy or causal utility. Maximum and median \(C\) were separately compared against 1,024 random 32×128 partitions, with 2,000 paired nested-bootstrap draws.

## Decisive Evidence

| Metric | Attention fixed max / random max q95 | MLP fixed max / random max q95 | Verdict |
| --- | ---: | ---: | --- |
| Coarse | 3.221 / 1.216 | 0.877 / 0.965 | attention only |
| Fine | 1.045 / 0.589 | 0.624 / 0.732 | attention only |
| Fine relative to coarse | 2.544 / 1.408 | 0.945 / 1.106 | attention only |

Attention median \(C\) values were -0.022, -0.067, and -0.026, so the pass is sparse rather than typical. Cross-site, null-calibrated attention-minus-MLP maximum effects were 2.093 [1.648, 2.437], 0.564 [0.279, 0.893], and 1.296 [0.187, 1.574].

![Null-calibrated cross-site comparison](figures/figure6_cross_site_null_calibrated_concentration.png)

Raw semantic energy is also far more uneven across attention heads: the median effective number of heads over blocks 1--35 was 12.51 for coarse and 12.26 for fine semantics, versus 31.38 and 31.46 contiguous MLP groups. Because pre-`o_proj` scaling may be compensated by `o_proj`, this is an allocation description rather than an output-contribution claim.

The registered within-unit audit split every 128-d unit into eight 16-d covariance-ranked bands (F1 head, F2--F5 middle, F6--F8 tail). None of the concentration-qualified attention cells exceeded the maximum over eight matched random 16-d subspaces. The result therefore supports sparse architectural-head identity, not reusable within-head rank identity.

## Execution Boundary

ACP jobs `om-y32ahxua` (attention) and `om-vjowli0r` (MLP) each used one 8×5090 node and completed the full Qwen extraction and statistics. Both platform jobs later exited during plotting because a NumPy `median` method was passed as a numeric value. The plotting-only defect was repaired, and the complete analysis was replayed locally from the unchanged extraction artifacts. No scientific condition, seed, metric, or decision rule changed.

All hook, replay, site-identity, calibration-half, orthogonality, label-permutation, and eigenvalue-floor guards passed. The platform `FAILED` state is therefore an engineering record, while the scientific verdict comes from the reproducible repaired analysis.

## Boundary And Next Decision

This frozen, single-model, single-taxonomy audit does not establish semantic causality, universal head identity, MLP absence of semantic information, fixed covariance-band function, expert utility, or training benefit.

The one next decision is whether an independent label-free taxonomy reproduces at least one selection-corrected attention-head maximum and whether its layer/head identity is stable across taxonomies. Only that replication qualifies the candidate coordinates for expert-counterfactual or Router-training tests.

See [detailed.md](detailed.md) for the complete evidence ledger and [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json) for every input text.
