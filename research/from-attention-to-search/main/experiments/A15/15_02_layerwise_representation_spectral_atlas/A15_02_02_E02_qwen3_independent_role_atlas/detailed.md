---
experiment_id: A15_02_02_E02_qwen3_independent_role_atlas
status: completed
verdict: pass_layer_specific_role_selectivity
date: 2026-08-02
---

# Detailed evidence ledger: Qwen3-8B independent-covariance semantic-role atlas

## 1. Decision question

In frozen Qwen3-8B, when every layer's covariance basis is estimated from independent natural text, does the same middle concept occupy systematically different spectral positions when it acts as a child versus a parent?

This is a representation atlas. It does not test Router utility, expert compatibility, compositional capability, or training efficiency.

## 2. Registered objects

For representation site \(\ell\), the calibration covariance is

\[
\Sigma_\ell=U_\ell\Lambda_\ell U_\ell^\top.
\]

For a semantic target state \(h\), the centered state is \(x=h-\mu_\ell\) and coefficient \(a_i=u_i^\top x\). The two registered energies are

\[
\operatorname{raw}_i=a_i^2,
\qquad
\operatorname{white}_i=\frac{a_i^2}{\max(\lambda_i,\lambda_1\rho)},
\]

with primary floor ratio \(\rho=10^{-6}\) and sensitivity ratios \(10^{-5},10^{-4}\). Effective-rank masking at each ratio is reported separately. Raw energy has units activation² per direction. Whitened energy is dimensionless and asks whether a target is unusually strong relative to ordinary variation along that direction.

The paired effect is parent minus child, averaged first over all subtokens in the identical target span, then over four templates within each chain, with 32 chains as the statistical units.

## 3. Model provenance and hook contract

| Item | Frozen value |
| --- | --- |
| Model path | `/data/share/Qwen3-8B` |
| Architecture | `Qwen3ForCausalLM` |
| Decoder blocks / hidden width | 36 / 4096 |
| Tokenizer | `Qwen2TokenizerFast`, vocabulary 151,669 |
| Model dtype | bfloat16 |
| Device | one NVIDIA H100 80GB, CUDA device 0 |
| Device mapping | the complete frozen model on `cuda:0` |
| Representation sites | embedding output (layer 0) and each raw decoder-block residual output before final model norm (layers 1--36) |
| Revision | local filesystem snapshot |
| Combined model/tokenizer manifest SHA-256 | `3e33117aebc01710cf1011093bbf4c2700336fce4600788f15d80d69f165dc25` |

The five model shard hashes and tokenizer/config hashes are recorded in [model_manifest.json](provenance/model_manifest.json). All 37 sites were captured twice on the same semantic batch; maximum hidden-state replay error was exactly 0.

## 4. Independent natural covariance data

Source:

```text
/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/
global-shard_02_of_10/local-shard_0_of_10/
shard_00000000_processed.jsonl.zst
```

- Source SHA-256: `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`.
- Selection: first 128 documents by stable document hash among the first 1,024 eligible documents, after exact semantic-sentence leakage exclusion.
- Slice: 512 Qwen tokens per document, 65,536 effective tokens total.
- Calibration token SHA-256: `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`.
- Exact semantic template leakage: 0.
- Half split: 64 documents / 32,768 tokens in each independently accumulated half.

Document hashes, line numbers, slice starts, token hashes, and previews are in [calibration_manifest.json](provenance/calibration_manifest.json). Calibration text is never used as a semantic-role test label.

## 5. Semantic hierarchy data and gates

The 32 inherited chains were not changed. Examples include `mathematics → algebra → linear algebra`, `physics → mechanics → classical mechanics`, and `computer science → algorithms → graph algorithms`. Every chain used four relation-equivalent templates, creating 128 parent/child pairs and 256 actual sequences.

For `mathematics → algebra → linear algebra`, template 0 is:

```text
child: Taxonomy evidence states that mathematics contains algebra as a recognized field. The relation is fully stated. clearly The target concept is algebra. This target is evaluated only after the relation above.
parent: Taxonomy evidence states that algebra contains linear algebra as a recognized field. The relation is fully stated. The target concept is algebra. This target is evaluated only after the relation above.
```

Both targets tokenize as `[46876]`, occupy span `[24,25)`, and have sequence length 36. Neutral one-token fillers equalize prefix and total length without changing the registered relation. The same checks were applied to every pair:

| Pair gate | Full result |
| --- | --- |
| Same target string and token ids | 128/128 pass |
| Same absolute target span | 128/128 pass |
| Same sequence length | 128/128 pass |
| Complete relation visible before target | 256/256 pass |
| Four templates for every chain | 32/32 pass |

All texts, input ids, target spans, relation roles, template ids, and chain ids are in [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json), semantic manifest SHA-256 `b1b5545fff3893fad5d673c03ef5db6893b8e6cfaae1fd0d55d9624355cc8df5`.

## 6. Execution

Worker surface:

```text
XingyuD/MoE_Routing_Experiments/active/
a15_01_03_e02_qwen3_independent_covariance_role_atlas/
```

Environment:

- Python 3.10
- PyTorch `2.3.0a0+6ddf5cf85e.nv24.04`
- Transformers `4.51.3`
- pandas `1.5.3`
- matplotlib `3.8.4`
- zstandard `0.23.0`

Full commands, executed locally in the project worker environment:

```bash
python prepare_data.py --output data
python extract.py --mode full --data data --output runs/full --device cuda:0 \
  --calibration-batch-size 8 --semantic-batch-size 16
python analyze.py --extraction runs/full --output runs/full_analysis_final --device cuda:0
```

Full extraction took 311.3 seconds; final analysis took 115.4 seconds. No model training or remote job was used.

## 7. Smoke, invalid attempt, and repair

The first smoke passed the pair, hook, replay, reconstruction, and plotting paths on a reduced sample. The first full numerical attempt accumulated \(X^\top X\) in FP32. It preserved projection energy but produced maximum covariance trace error \(2.18\times10^{-4}\), exceeding the registered \(5\times10^{-5}\) guard after tiny negative eigenvalues were clamped.

That attempt is retained under `runs/invalid_fp32_*` and is not scientific evidence. The only repair was FP64 moment accumulation and eigendecomposition. No text, model, band, floor, inference rule, or threshold changed. A new smoke and the final full analysis then passed all registered numerical guards.

## 8. Validity evidence

### 8.1 Numerical guards

| Guard | Maximum / minimum result | Status |
| --- | ---: | --- |
| Covariance reconstruction relative error | \(8.80\times10^{-15}\) | pass |
| Projection energy relative error | \(1.69\times10^{-6}\) | pass |
| Hidden-state replay max absolute error | 0 | pass |
| Covariance trace and orthogonality | below registered thresholds | pass |

Complete values are in [energy_conservation.csv](tables/energy_conservation.csv) and [basis_stability.csv](tables/basis_stability.csv).

### 8.2 Split-half spectral stability

Overlap is the normalized trace overlap of the same rank band estimated on independent calibration halves. The normalized excess subtracts the random-subspace expectation and rescales the remaining range to \([0,1]\).

| Band | Minimum overlap | Minimum normalized excess | Passing sites |
| --- | ---: | ---: | ---: |
| H | 0.551 | 0.510 | 37/37 |
| M | 0.524 | 0.285 | 37/37 |
| T | 0.746 | 0.390 | 37/37 |

All coarse bands pass the preregistered 0.25 excess guard, including layers 35 and 36.

### 8.3 Statistical inference

- 2,000 paired bootstrap draws over 32 chains, seed 20260803.
- 5,000 within-chain parent/child label-swap draws, seed 20260804.
- Benjamini-Hochberg FDR applied within metric × resolution families.
- Local cell requirements: 95% interval excludes zero, \(q<0.05\), at least 3/4 templates have the same sign, and at least 18/32 chains have that sign.
- Stable cell requirements: the local cell passes, a neighboring layer has the same locally passing sign, and whitened results preserve a nonzero same-sign interval under all registered floor and effective-rank conditions.

The final table contains 94 stable whitened fine/coarse cells; none has `epsilon_robust=false`. See [band_role_summary.csv](tables/band_role_summary.csv) and [epsilon_effective_rank_sensitivity.csv](tables/epsilon_effective_rank_sensitivity.csv).

## 9. Main results

### 9.1 Raw energy

Both roles place much more actual energy in the largest-background-variance directions, and absolute residual energy grows strongly with depth. This scale growth is not itself semantic evidence. Within-layer paired contrasts show child-greater-than-parent H effects in several early/middle blocks and parent-greater-than-child H effects throughout blocks 25--32. In layers 35--36, raw H returns negative while M/T remain positive.

### 9.2 Whitened role selectivity

After dividing out background eigenvalues:

- H is stably child-greater-than-parent at blocks 5, 6, 9, 10, 11, 12, 14, 16, 18, and 19.
- H is stably parent-greater-than-child at every block 25--32.
- M is stably parent-greater-than-child at blocks 28--36.
- T is stably parent-greater-than-child at blocks 33--36.

Representative paired head log ratios are \(-0.0396\) at block 10, \(+0.0774\) at block 29, and \(-0.0884\) at block 36. These equal parent/child multiplicative ratios 0.961, 1.080, and 0.915 respectively.

This pattern establishes a layer-specific role atlas. It rejects a depth-invariant parent=head rule.

### 9.3 Final-layer reversal audit

The preregistered terminal reversal required layer 36 to be significant and opposite both layer 35 and the median of layers 1--35, with template and chain support. No H/M/T raw or whitened row passed. In whitened H, layer 36 is negative, layer 35 is already slightly negative and nonsignificant, and the layers 1--35 median is also negative. The terminal block therefore sharpens a local child-head association but is not a unique sign reversal.

See [final_layer_reversal.csv](tables/final_layer_reversal.csv).

## 10. Figure contracts and visual audit

### Figure 1: per-direction projection curves

![Per-direction curves](figures/figure1_direction_projection_curves.png)

- **Question:** where does each role's activation lie along the full ranked spectrum?
- **Axes:** x is rank from largest to smallest calibration eigenvalue; y is raw activation² on a log scale or dimensionless whitened energy.
- **Aggregation:** role means and 95% chain-bootstrap intervals; thin traces preserve all 4,096 directions and thick traces show a 64-rank rolling display mean.
- **Allowed claim:** raw energy is head-heavy; whitened profiles reveal residual direction preference.
- **Limitation:** visual overlap is not the inference test; no curve proves semantic causality or utility.
- **Rendered audit:** opened at original resolution; labels, legends, panels, intervals, penultimate, and final layers are readable.

### Figure 2: layer × band × role heatmaps

![Heatmaps](figures/figure2_layer_band_role_heatmaps.png)

- **Question:** how do role profiles and their paired difference vary jointly across depth and rank band?
- **Axes:** x is F1--F12; y is layer 0--36.
- **Colorbars:** raw role panels use \(\log_{10}\) activation² per direction; raw difference uses activation²; whitened panels are dimensionless; red difference means parent>child and blue means child>parent.
- **Allowed claim:** the sign and spectral location of role differences are layer-specific.
- **Limitation:** color intensity across raw layers includes residual-scale growth.
- **Rendered audit:** opened at original resolution; all 37 rows, 12 bands, six colorbars, and terminal rows are distinguishable.

### Figure 3: layerwise role-difference trajectory

![Trajectories](figures/figure3_layer_role_difference_trajectories.png)

- **Question:** does each coarse-band role contrast evolve monotonically, and is the final layer exceptional?
- **Axes:** x is representation site; y is parent-minus-child per-direction energy. Raw uses a symmetric-log display; white uses a linear dimensionless display. The dashed line identifies layer 35.
- **Allowed claim:** H changes sign across depth; the terminal state redistributes H versus M/T.
- **Limitation:** plotted intervals alone do not define stable cells; the registered table also requires permutation, FDR, templates, chains, adjacency, and epsilon robustness.
- **Rendered audit:** opened at original resolution after changing the raw display to symmetric log; early, late, and terminal signs are legible.

## 11. Fixed and uncontrolled factors

Fixed within every parent/child pair: model snapshot, tokenizer, representation site, target string and token ids, target absolute span, sequence length, relation visibility, template skeleton, covariance basis, calibration mean, band boundaries, and analysis seeds. Multi-token targets are compared after averaging the same subtoken ids in the same order.

Not fully fixed:

1. The necessary relational concepts differ: child-role context contains root→middle whereas parent-role context contains middle→leaf. This is the semantic-role intervention itself but also changes surrounding lexical content.
2. The 32 chains have different target frequencies, token lengths, and domain familiarity. Pairing removes these within each chain; the 32-chain population remains a finite ontology sample.
3. All templates are English and all representation evidence comes from one Qwen3-8B snapshot.
4. One DCLM source defines the natural covariance geometry. Split-half stability protects sampling noise but not corpus-distribution shift.

These uncontrolled factors are acceptable for the narrow model-specific statement that relational role is associated with different spectral positions. They are not acceptable for a universal semantic hierarchy law. The minimal external-validity repair is to reuse the exact 256 semantic sequences under a second independently sampled natural covariance corpus or a second frozen model, without changing chains after viewing results.

## 12. Verdict and claim boundary

- **Pass:** layer-specific whitened semantic-role selectivity in this frozen Qwen3-8B.
- **Fail:** a uniform parent=head, child=tail rule.
- **Fail:** a final-layer-only reversal.
- **Insufficient:** cross-model, cross-language, alternative-corpus, and ontology-wide generality.

The experiment cannot claim that covariance rank causes semantic hierarchy, that later blocks are compositional, that role-selective bands are useful Router inputs, or that any routing/training benefit follows.

## 13. Artifact map

| Artifact | Role |
| --- | --- |
| [protocol.md](protocol.md) / [protocol_cn.md](protocol_cn.md) | Approved contract |
| [summary.md](summary.md) / [summary_cn.md](summary_cn.md) | First reading path |
| [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json) | All actual texts, token ids, spans, roles, chains, templates |
| [calibration_manifest.json](provenance/calibration_manifest.json) | Natural document and token provenance |
| [model_manifest.json](provenance/model_manifest.json) | Model/tokenizer hashes and hook object |
| [extraction_manifest.json](provenance/extraction_manifest.json) | Full hook/moment/state audit |
| [band_role_summary.csv](tables/band_role_summary.csv) | Complete fine/coarse paired results and decisions |
| [direction_profiles.csv](tables/direction_profiles.csv) | Full 4,096-direction profiles for selected layers |
| [eigenvalue_spectra.csv](tables/eigenvalue_spectra.csv) | All 37 layer spectra |
| [basis_stability.csv](tables/basis_stability.csv) | Half-split and numerical guards |
| [epsilon_effective_rank_sensitivity.csv](tables/epsilon_effective_rank_sensitivity.csv) | Tail/floor sensitivity |
| [curated_artifacts.sha256](provenance/curated_artifacts.sha256) | Curated-file integrity manifest |

Raw hidden states, covariance moments, bases, and invalid-run diagnostics remain on the worker surface and were not promoted into the research mainline.

## 14. Next decision

The only next decision is whether to replicate the two-phase head pattern—child-selective in early/intermediate blocks and parent-selective in blocks 25--32—using an independent model or independently sampled natural covariance corpus before any layer-band cell enters a functional Router test.
