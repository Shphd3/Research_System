# Detailed: A15_08_01_E02 Layerwise Long-Range Gain, Blocks 2--36

Primary Anchor: [A15_08_01 layerwise long-range compositional innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), Sections 1--16 SHA-256 `ad34982132b948a78998d8afef918349aaecb4dfc165725ea594b15138d6c735`  
Summary: [summary.md](summary.md)  
Registered verdict: `H2_LC_FAIL_CONTROL_DEGRADATION`

## 0. Direct Result

Reserved ACP job `pt-f0agvja0` completed successfully at
`2026-08-11T14:04:41Z` on one `n6ls.iu.i40.4` worker with four H100 GPUs and
the researcher-selected image. It evaluated the pre-registered blocks 2--36
using immutable E01 data/extraction inputs and a fresh P5--P7 root:

`/data/250010109/MoE_Router/experiments/20260811_a15_08_01_e02_blocks_2_36_r1`

All data, identity, capability, bridge-dependency, freeze, artifact, and figure
contracts passed. The typed scientific outcome is
`H2_LC_FAIL_CONTROL_DEGRADATION` because \(A_{2F}\) is strictly negative.

## 1. Question And Registered Comparison

For block \(\ell\), condition \(c\), and held-out example, the experiment compares
a frozen old-state readout from

\[
X_\ell=N_\ell(h_\ell)
\]

with the same readout plus a correction from the old-state-residualized exact
attention effect

\[
U_\ell=N_\ell(h_\ell+a_\ell)-N_\ell(h_\ell),
\qquad
R_{U,\ell,c}=U_{\ell,c}-\widehat m^U_{\ell,c}(X_{\ell,c}).
\]

The held-out cross-entropy reduction is \(G_{\ell,c}\). The layerwise
necessity-by-distance interaction is

\[
I_\ell=(G_{\ell,2F}-G_{\ell,2N})-(G_{\ell,1F}-G_{\ell,1N}),
\]

and the primary depth contrast is

\[
T_{depth}=\operatorname{median}_{\ell=25}^{36}I_\ell
-\operatorname{median}_{\ell=2}^{12}I_\ell.
\]

The absolute-target guard is

\[
A_{2F}=\operatorname{median}_{\ell=25}^{36}G_{\ell,2F}
-\operatorname{median}_{\ell=2}^{12}G_{\ell,2F}.
\]

## 2. Data, Model, And Split Contract

- frozen Qwen3-8B, hidden width 4,096, answer-preceding decision token;
- 320 disjoint worlds and 10,240 records of exactly 1,024 tokens;
- 1N/1F/2N/2F each contain 2,560 records;
- TRAIN/DEVELOPMENT/CONFIRMATION contain 128/64/128 complete worlds;
- bridge gaps are 48 and 640 tokens; terminal gap is 8--24 tokens;
- TRAIN fits readouts and the common basis, DEVELOPMENT chooses ridge
  penalties and headroom slope, CONFIRMATION evaluates frozen objects only;
- 64 balanced within-world mismatch banks and 2,000 complete-world paired
  bootstrap draws.

Block 1 is excluded because E01 established before confirmation access that
\(X_1\) is structurally constant and cannot satisfy the frozen standardization
rule. No epsilon or artificial zero feature is used.

## 3. Execution And Repair Lineage

E01 P1--P4 data and extraction passed and were bound read-only by
[reused_input_receipt.json](evidence/reused_input_receipt.json). The first E02
job `pt-e0wrdh90` completed all 35 per-layer TRAIN/DEV fits but failed before
the common basis because a list position was mistaken for an extraction block
index. No confirmation label was opened. Repair A7 mapped the 35 trace entries
to zero-based extraction indices 1--35 and added a regression test; all 40
tests passed. The fresh `_r1` job then completed the whole chain.

Evidence receipts:

- [result.json](evidence/result.json);
- [protocol conformance](evidence/protocol_conformance.json);
- [result manifest](evidence/result_manifest.json);
- [confirmation unseal receipt](evidence/confirmation_unseal_receipt.json).

## 4. Validity Guards

| Guard | Direct result | Verdict effect |
| --- | ---: | --- |
| 1N capability | 0.9990 [0.9971, 1.0000] | pass |
| 1F capability | 1.0000 [1.0000, 1.0000] | pass |
| 2N capability | 0.9160 [0.8965, 0.9326] | pass |
| 2F capability | 0.8447 [0.8203, 0.8672] | pass |
| bridge \(\Delta_2\) | 3.5794 [3.4452, 3.7336] | pass |
| bridge \(\Delta_2-\Delta_1\) | 3.6658 [3.5031, 3.8474] | pass |
| extraction identity | all four shards; all three errors exactly zero | pass |

These guards make the outcome eligible. They do not make the target depth
hypothesis true.

## 5. Registered Metrics

| Quantity | Estimate | Paired 95% interval | Reading |
| --- | ---: | ---: | --- |
| \(T_{depth}\) | +0.006102 | [0.004119, 0.007669] | interaction increases with depth |
| \(M_D\) | +0.003328 | [0.001715, 0.004508] | deep interaction is positive |
| \(A_{2F}\) | **-0.011422** | **[-0.013994, -0.009812]** | absolute 2F gain decreases; typed Fail |
| \(T_{depth}^{head}\) | +0.018116 | [0.014273, 0.021431] | survives linear headroom adjustment |
| \(T_{cap}\) | +0.001621 | [-0.000873, 0.002821] | matched-capacity separation unresolved |

The positive difference-in-differences is real in the registered linear
readout, but it is not a positive change in the absolute remote two-hop target
cell. The Protocol requires both, so the scientific verdict is Fail.

Complete layer/cell values are in
[layer_condition_gains.csv](tables/layer_condition_gains.csv) and the five
contrasts in [registered_contrasts.csv](tables/registered_contrasts.csv).

![Layerwise accessibility](figures/figure_1_layerwise_accessibility.png)

### Figure 1 audit

- Panel A displays all blocks 2--36 and all four conditions in
  nats/example; no smoothing is applied.
- Panel B displays the registered \(I_\ell\) and fixed early/middle/deep bands.
- Panel C reproduces the five intervals in the table above.
- The figure permits the typed H2-LC verdict; it does not identify a vector
  subspace or native model use.

## 6. Representation Rank And Common Basis

For matched residual-update interactions \(D_{\ell,w,i}\), the experiment reports
the covariance entropy effective rank \(r_{eff}\), 80%-variance rank \(r_{80}\),
trace, and energy in a TRAIN-only equal-layer common basis.

On CONFIRMATION, \(r_{eff}\) ranges from 18.77 (block 2) to 350.76 (block 9), and
\(r_{80}\) ranges from 10 to 338. Selected values are:

| Block | \(r_{eff}\) | \(r_{80}\) | trace |
| ---: | ---: | ---: | ---: |
| 2 | 18.77 | 10 | 610.19 |
| 12 | 260.79 | 279 | 123.51 |
| 25 | 52.04 | 36 | 415.46 |
| 36 | 220.89 | 181 | 179.38 |

The common covariance basis itself accumulates 20.21% of its TRAIN energy in
32 directions, 55.89% in 512, and 86.51% in 2,048. Layer-specific curves
differ strongly; for example, 32 common directions retain 74.18% of block-2
CONFIRMATION energy, 5.85% at block 12, 53.81% at block 25, and 8.56% at block
36. This is redistribution, not a universal compact prefix.

Complete records are in [representation_rank.csv](tables/representation_rank.csv),
[split_stability_64_worlds.csv](tables/split_stability_64_worlds.csv), and
[common_basis_spectrum.csv](tables/common_basis_spectrum.csv).

![Representation geometry](figures/figure_2_representation_rank_common_basis.png)

### Figure 2 audit

- Panel A shows TRAIN/DEVELOPMENT/CONFIRMATION rank fractions and a separate
  log-trace scale.
- Panel B uses unsmoothed cumulative energy in the same 4,096-direction basis.
- Panel C alone uses the frozen nine-rank display smoothing; calculations use
  raw energies.
- The figure supports only a descriptive non-monotonic geometry statement.

## 7. Claim Boundary And Next Decision

**Established:** the registered deep interaction is positive, but the absolute
remote two-hop added-accessibility gain declines; H2-LC therefore fails its
pre-registered \(A_{2F}\) guard.

**Not established:** absence of deep information, global representation rank,
task-sufficient rank, Shannon-information creation, native MLP use, expert
utility, or Router performance.

**Exactly one next decision:** decide whether the next anchor should replace
interaction-first depth adjudication with a direct absolute-gain question for
\(G_{\ell,2F}\) against matched target-independent corrections.
