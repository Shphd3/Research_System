# R001 DCLM MoE-Input Sparse Atom Summary

Sources:

- `daily_research_reports/0507/Draft_moe_input_corrected_bundle/report.md`
- `daily_research_reports/0507/Draft_moe_input_corrected_bundle/sparse_dict_summary_moe_input.csv`
- `daily_research_reports/0507/Draft_moe_input_corrected_bundle/true_atom_ablation_summary_moe_input.csv`
- `daily_research_reports/0507/Draft_moe_input_corrected_bundle/coarse_block_summary_moe_input.csv`
- `daily_research_reports/0507/Draft_current_results_rewrite_bundle/report.md`

## Scope

This result summarizes the real DCLM sparse-atom analysis for 5B-token trained Flat and Hierarchical MoE models with 16 final paths.

The MoE-input corrected bundle is the primary source. It replaces the earlier draft numbers because the corrected analysis uses the hidden state actually received by the MoE/MLP block: after attention and post-attention layer norm, before the expert computation.

## Stable Results

1. After correcting the analysis point to MoE block input, current evidence does not support the claim that Hierarchical MoE has stronger path-level sparse atom differentiation than Flat MoE.
2. Flat raw top-1 + LB has the strongest path-atom diversity across layers. At layer 7, its atom diversity is 0.229, compared with 0.036 for Hierarchical full_input and 0.030 for Hierarchical conditional_input.
3. Hierarchical models do not collapse: active paths are 16 and UsageNorm is close to 1. The issue is not path usage collapse, but that different hierarchical paths receive more similar sparse atom profiles.
4. Top path atoms are functionally relevant for all models. Removing top path atoms at layer 7 raises loss much more than random atom removal.
5. Hierarchical models show a weak but consistent coarse-block structure. The coarse block gap is positive across layers, but it shrinks with depth and is small at layer 7.

## Key Numbers

Layer 7 sparse atom differentiation:

| Model | Atom diversity ↑ | Top atom overlap ↓ | UsageNorm |
|---|---:|---:|---:|
| Flat raw top-1 + LB | 0.229 | 0.379 | 0.999 |
| Flat middle spectral top-1 | 0.104 | 0.439 | 0.967 |
| Hierarchical full_input | 0.036 | 0.661 | 0.992 |
| Hierarchical conditional_input | 0.030 | 0.669 | 0.995 |

Layer 7 top-atom ablation with `k=16`:

| Model | Original loss | Top atom loss delta | Random atom loss delta | Top-random gap |
|---|---:|---:|---:|---:|
| Flat raw top-1 + LB | 4.023 | 0.522 | 0.085 | 0.437 |
| Flat middle spectral top-1 | 4.082 | 0.553 | 0.113 | 0.440 |
| Hierarchical full_input | 4.112 | 0.508 | 0.120 | 0.389 |
| Hierarchical conditional_input | 4.163 | 0.567 | 0.153 | 0.414 |

Hierarchical coarse block gap:

| Layer | Hier full_input | Hier conditional_input |
|---|---:|---:|
| 1 | 0.148 | 0.106 |
| 3 | 0.043 | 0.031 |
| 5 | 0.030 | 0.034 |
| 7 | 0.016 | 0.012 |

## Interpretation

The current real-DCLM evidence separates two ideas that should not be merged:

1. Whether paths receive different sparse atom profiles.
2. Whether the atoms received by a path matter for the model's computation.

The first is not supported for Hierarchical MoE: Flat raw top-1 + LB has stronger path-atom differentiation.

The second is supported across all models: path top atoms are causally relevant under ablation because removing them increases loss substantially more than removing random atoms.

Hierarchical MoE shows an internal coarse-block structure, but this is a weak structural signal, not proof of semantic hierarchy recovery.

## Claim Strength

## Claim 1

Hierarchical MoE is better than Flat MoE at path-level sparse atom division on real DCLM representations.

Status: unsupported.

Evidence: Hierarchical full_input and conditional_input have much lower atom diversity and higher top atom overlap than Flat raw top-1 + LB after MoE-input correction.

Public wording: Current real-DCLM sparse-atom diagnostics do not show stronger path-level atom differentiation for Hierarchical MoE.

What not to say: Do not say Hierarchical MoE has learned cleaner sparse feature partitions.

## Claim 2

The path top atoms are actually used by the model computation.

Status: supported.

Evidence: For all models, top path atom ablation produces much larger loss increases than random atom ablation at layer 7.

Public wording: Sparse atoms identified by the path profiles are not only visualization artifacts; they affect model output when ablated.

What not to say: Do not say this proves different paths use mutually different atoms.

## Claim 3

Hierarchical MoE contains a coarse-block organization signal.

Status: weakly supported.

Evidence: Coarse block gap is positive across layers for both Hierarchical variants, but the signal is small at deeper layers.

Public wording: Hierarchical MoE shows a weak but consistent internal coarse-block structure.

What not to say: Do not say it recovers true semantic hierarchy, because DCLM has no ground-truth coarse/fine labels.

## Current Safest Claim

On real DCLM representations, MoE-input sparse-atom diagnostics do not support stronger path-level sparse atom differentiation for Hierarchical MoE compared with Flat MoE. However, the diagnostics do show that path top atoms are computationally relevant, and Hierarchical MoE has a weak internal coarse-block structure.

## Main Limitation

The experiment uses sparse dictionary atoms as diagnostics, not ground-truth semantic mechanisms. Therefore, it can test path-atom differentiation and ablation sensitivity, but it cannot prove recovery of true semantic hierarchy or continual-learning benefit.

## Next Diagnostic Need

1. Explain why Flat raw top-1 + LB has stronger sparse atom differentiation than Hierarchical MoE.
2. Separate path-level atom differentiation from function-level recovery and continual-learning interference.
3. Test whether the weak coarse-block structure predicts any downstream benefit, such as lower interference or better tail-feature retention.
