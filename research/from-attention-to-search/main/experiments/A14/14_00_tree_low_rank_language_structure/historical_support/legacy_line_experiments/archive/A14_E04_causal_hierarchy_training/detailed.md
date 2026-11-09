# A14_E04 Detailed Evidence

## Paired Intervention

- latent dimensions $k_\star\in\{4,8,16,32\}$;
- seeds 0--2, yielding 12 paired hierarchy/shuffled runs;
- 20,000/2,000/2,000 train/validation/test sequence pairs;
- each pair has exactly the same 32-token multiset and root state;
- 4-layer decoder, width 128, 4 heads, FFN width 512;
- identical initial state dict and minibatch indices within each pair;
- 800 updates, checkpoints 0/200/400/800;
- common EOS readout, with next-BOS training target so EOS is an input state.

Execution command:

```bash
python scripts/run_causal_hierarchy_training.py \
  --config configs/exp4_causal_hierarchy_training.yaml \
  --output-dir outputs/A14_E04_full
```

Runtime was 281.3 seconds on two local H100 devices (training and analysis
surfaces). All 16 unit tests passed before execution, including exact token
multiset pairing and a future-token causal-mask test.

## Registered Decision Evidence

| Clause | Result | Verdict |
| --- | ---: | --- |
| final capable pairs | 0/12 | fail guard |
| step-0 maximum mean effect magnitude | 0.0038 | pass $<0.02$ |
| latent dimension/rank Spearman | 0.9487 | pass $\ge0.8$ |
| non-vacuous hierarchy transitions | 0/48 | fail |
| primary tree/composition effect intervals | undefined after guard | insufficient |

Because no pair passed capability, the registered effect means and intervals
are undefined rather than zero.

## Descriptive Paired Evidence

| Quantity | Hierarchy mean | Shuffled mean | Paired effect |
| --- | ---: | ---: | ---: |
| root-state accuracy | 0.699 | 0.150 | +0.550 |
| tree-span advantage | 0.1795 | -0.0001 | +0.1796 |
| shared-composition advantage | 0.7313 | 0.7782 | -0.0469 |
| base 95%-energy rank | 24.9 | 38.6 | -13.7 directions |

Every tree effect was positive (range 0.064--0.253). Every composition effect
was negative (range -0.116 to -0.020). These consistent signs make the split
between subspace alignment and the current composition metric unlikely to be a
single-seed accident.

Final hierarchy median leaf ranks by latent state count were 16, 24, 24, and
28 for $k_\star=4,8,16,32$. The relation is monotone up to the tied middle
conditions and yields Spearman 0.949.

## Theorem Bound

Final hierarchy bound ratios by child span length were:

| Child length | Median | Minimum | Maximum |
| ---: | ---: | ---: | ---: |
| 2 | 2.67 | 1.84 | 4.27 |
| 4 | 3.24 | 2.21 | 5.86 |
| 8 | 4.15 | 3.44 | 7.70 |
| 16 | 4.59 | 3.48 | 7.59 |

The bound becomes looser with scale and never crosses below one. The theorem is
valid but supplies no effective-rank certificate in this trained system.

## Metric and Causal Audit

1. **Tree-subspace outcome:** near-zero at initialization and positive in all
   final hierarchy-minus-shuffle pairs. The paired order intervention is a
   plausible cause within this generator.
2. **Composition outcome:** large even at initialization and larger for the
   shuffled condition. Cross-parent permutation changes parent token content,
   so it is not a syntax-isolating control.
3. **Capability guard:** root-state accuracy is a downstream mediator of the
   hierarchy manipulation, not a neutral capacity variable. Its failure makes
   the registered full-mechanism result insufficient but does not erase the raw
   randomized effect.
4. **Language-model NLL:** hierarchy finished at mean 4.31 versus 5.21 for
   shuffled. This is an intended consequence of changing conditional
   structure and was not used for capability matching.

## Artifact Map

- [machine summary](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/summary.json)
- [checkpoint metrics](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/checkpoint_metrics.parquet)
- [transition metrics](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/transition_metrics.parquet)
- [paired effects](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/paired_effects.csv)
- [training curves](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/training_curves.csv)
- [run manifest](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E04_full/run_manifest.json)
- local central figure: [causal summary](causal_training_summary.png).

## Visualization Audit

Learning curves average all latent dimensions and seeds and show the intended
change in conditional predictability. Paired bars show every registered run,
not only a favorable aggregate. The theorem panel shows medians and full
min--max ranges over final hierarchy runs, with the non-vacuity threshold at
one. The figure therefore exposes both the positive tree effect and the two
mechanism failures.

