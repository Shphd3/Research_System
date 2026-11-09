# Detailed: A15_08_01_E01 Layerwise Long-Range Gain And Representation Rank

Primary Anchor: [A15_08_01 layerwise long-range compositional innovation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), Sections 1--16 SHA-256 `7197183c95b4cbfefeaf431f13da0d06313100c7c10649ea3272ac053430a08a`  
Summary: [summary.md](summary.md)  
Result status: `H2_LC_INSUFFICIENT_STANDARDIZATION`

## 0. Direct Record

The only E01 run that reached scientific data was Reserved ACP job
`pt-b45k84qc`, created at `2026-08-11T13:11:35Z` and stopped at
`2026-08-11T13:19:33Z`. It used the researcher-specified image
`shphd-lite-0710:container1-20260710154849`, one `n6ls.iu.i40.4` worker, and
four H100 GPUs. Its raw root is:

`/data/250010109/MoE_Router/experiments/20260811_a15_08_01_layerwise_long_range_gain_rank_r3`

P1--P4 completed. P5 stopped at its first standardizer before any scientific
metric or confirmation-label access. The registered outcome is therefore
Insufficient, not a numerical Fail.

## 1. Frozen Question And Objects

E01 asked whether the necessity-by-distance added-accessibility interaction
was larger in blocks 25--36 than in blocks 1--12. At each block,

\[
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell.
\]

The gain metric required a frozen old-state readout from standardized \(X_\ell\)
and a correction readout from the part of standardized \(U_\ell\) not linearly
reconstructed from \(X_\ell\). Section 8.1 required each TRAIN pooled scale to
be finite and greater than \(10^{-12}\); otherwise the layer and the registered
all-layer comparison were invalid.

## 2. Execution Lineage

| Job | Resource | Last completed point | Eligibility |
| --- | --- | --- | --- |
| `pt-3qikirn4` | Spot | never allocated | ineligible; stopped at researcher request |
| `pt-luxlf19m` | Reserved | GPU preflight | ineligible runtime-import failure |
| `pt-z5m90trk` | Reserved | runtime and tests | ineligible source-provenance failure |
| `pt-yiwkpm3p` | Reserved, requested image | initial identity check | ineligible checker-shape mismatch |
| `pt-b45k84qc` | Reserved, requested image | full extraction; P5 standardization guard | controlling E01 record |

The earlier runs produced no scientific values. The A5 shape-preserving
identity repair retained the measured module, token, formula, and \(10^{-5}\)
threshold and passed on all four shards.

## 3. Data And Identity Evidence

The data receipt records:

- 320 whole worlds and 10,240 fixed-length 1,024-token records;
- 2,560 records in each of 1N, 1F, 2N, and 2F;
- TRAIN/DEVELOPMENT/CONFIRMATION world counts 128/64/128;
- exact bridge gaps 48 and 640 and terminal gap 8--24;
- zero cross-split entity and exact-token overlap;
- complete quartets, balanced eight-code worlds, and sealed confirmation labels.

The four identity receipts each report:

\[
\text{replay max-absolute logit error}=0,
\]

\[
\frac{\|Z-X-U\|_F}{\max(\|Z-X\|_F,10^{-12})}=0,
\qquad
\frac{\|a-a_{o_{proj}}\|_F}{\max(\|a\|_F,10^{-12})}=0.
\]

All four 2,560-record extraction shards completed both main and bridge-swap
passes. Each retained object shard is approximately 9.06 GB.

## 4. Standardization Guard

The frozen pooled scalar scale was

\[
s_X=
\sqrt{\frac{1}{nd}\sum_{i=1}^{n}\sum_{j=1}^{d}
(X_{ij}-\bar X_j)^2}.
\]

For block 1, all 4,096 TRAIN rows and all 2,048 DEVELOPMENT rows of \(X_1\)
were exactly identical, giving \(s_X=0\). This is consistent with the
architecture: before the first attention write, the selected residual belongs
to the same terminal query token in every prompt, so no earlier contextual
write has yet altered it.

The fitting code raised `ValueError: nonfinite or negligible pooled scale` as
registered. Layers 2--36 had positive TRAIN scales. A partial layer-4 output
created by another rank during distributed shutdown is not a completed
selection artifact and is excluded from evidence.

## 5. Confirmation And Metric Access Audit

Before the stop:

- the public metadata excluded confirmation target labels;
- no standardizer or ridge penalty was frozen;
- no residualized update, common basis, gain, mismatch bank, or bootstrap
  interval was completed;
- the separate confirmation-label vault was not deserialized by P5.

Therefore no diagnostic H2 number exists to interpret, and the immutable data
and extraction may be bound as pre-outcome inputs to a separately frozen
successor.

## 6. Claim Boundary And Next Decision

**Established:** block-1 old-state standardization is structurally undefined
for this fixed decision token and the frozen all-36-block E01 cannot produce
its registered depth contrast.

**Not established:** any sign or magnitude of layerwise gain, deep-versus-early
interaction, representation rank, common-basis energy, model-native use, or
Router utility.

**Only next decision:** execute the human-approved [E02 blocks-2--36
Protocol](../A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/protocol.md), keeping strict standardization and excluding block 1 rather than changing it numerically.
