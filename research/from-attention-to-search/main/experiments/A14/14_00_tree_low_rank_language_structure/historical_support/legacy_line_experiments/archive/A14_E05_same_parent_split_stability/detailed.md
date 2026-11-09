# A14_E05 Detailed Evidence

## Question And Registered Contract

Does an ordered, low-dimensional shared parent operator prefer the annotated
Penn Treebank split over a different split of exactly the same parent tokens,
and can that preference coexist with a non-vacuous propagation bound?

For centered parent representations, the primary error was

$$
CE_c=\frac{\|Y-\widehat Y_c\|_F^2}{\|Y-\mu_Y\|_F^2},
\qquad
Adv_{split}=\frac{CE_{alt}-CE_{gold}}{CE_{alt}}.
$$

The strict probe projected both children into the training-leaf 95%-energy
space $U$, used separate left/right matrices, and constrained all predicted
parent variation to $U$. Gold and alternative maps were fitted separately and
selected only by validation error.

## Setup

- Penn Treebank files split 70%/15%/15%; no file overlap;
- 8,192 training coarse leaves;
- 4,096/1,024/1,024 train/validation/test naturally binary parents;
- parent length 3--16 words;
- independent-span final EOS representations;
- Qwen2.5-0.5B and Pythia-410m, pretrained and identical-architecture random
  initialization;
- BF16 model forward and float64 spectral/regression analysis;
- 1,000 sentence-cluster bootstrap replicates;
- ridge grid $10^{-6}$ through $10^5$; gold and alternative selections were
  interior points;
- all parent and ordered-token guards passed; both sample-shape guards passed.

The first smoke run selected the original $10^2$ upper endpoint. Before any
full result was inspected, the grid was expanded once through $10^5$ and an
interior-selection guard was frozen. The full run passed it.

Execution:

```bash
python scripts/run_same_parent_split_stability.py \
  --config configs/exp5_same_parent_split_stability.yaml \
  --output-dir outputs/A14_E05_full
```

All 20 final project tests passed after execution; 19 tests had passed at the
time E05 itself was run.

## Registered Evidence

| Model | Checkpoint | leaf $r_{0.05}/d$ | gold error | alternative error | split advantage [95% interval] | minimum eligible bound |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen | pretrained | 24/896 (2.68%) | 0.5381 | 0.5167 | -0.0415 [-0.1079, 0.0213] | 1.3369 |
| Qwen | initialization | 637/896 (71.09%) | 0.6452 | 0.5871 | -0.0989 [-0.1077, -0.0906] | 1.1200 |
| Pythia | pretrained | 346/1024 (33.79%) | 0.3910 | 0.4592 | +0.1486 [0.1308, 0.1645] | 2.7501 |
| Pythia | initialization | 340/1024 (33.20%) | 0.2933 | 0.2778 | -0.0560 [-0.0799, -0.0318] | 1.2413 |

The Qwen H5 increment is $-0.0415-(-0.0989)=+0.0574$. This only means training
moved the split contrast in the registered direction; the final contrast is
still negative and H2 remains unsupported.

## Shared Space Versus Shared Composition

For pretrained Qwen, held-out parent projection error outside the frozen leaf
space was 0.0582. The best strict gold operator nevertheless had error 0.5381.
Thus most parent variation lies near the same low-dimensional coordinates, but
one global ordered linear map does not predict that variation well enough to
identify the annotated boundary.

The ordered model beat the commutative mean model by 6.98% in Qwen and 14.73%
in Pythia. The same advantage was 11.89% and 30.53% at initialization. Because
the ordered probe has separate left/right features and more capacity, this
secondary result is compatible with architecture or probe flexibility; it is
not evidence that training learned syntactic roles.

## Prediction--Stability Audit

| Condition | selected bound ratio | minimum validation-eligible ratio | compatible points |
| --- | ---: | ---: | ---: |
| Qwen pretrained | 1.8669 | 1.3369 | 0 |
| Pythia pretrained | 2.7501 | 2.7501 | 0 |

Every ratio exceeds one. The theorem remains mathematically valid, but its
worst-case operator-norm certificate is empirically vacuous.

## Post-Hoc Direction Audit

The registered alternative was the closest non-gold word boundary by tokenizer
length. It was always one word from gold, but exact subtoken-profile matches
were impossible in the test sample. Mean left/right profile deviations were
2.53 subtokens for Qwen and 2.39 for Pythia. The chosen alternative shifted
right in 83.1% and 84.3% of records, respectively.

| Model/checkpoint | left-shift advantage | right-shift advantage |
| --- | ---: | ---: |
| Qwen pretrained | -0.1923 | -0.0077 |
| Pythia pretrained | -0.1426 | +0.1997 |

This audit was not registered to establish a new effect. It identifies a rival
explanation for Pythia and justifies E06. Parent-length strata did not remove
Pythia's aggregate positive direction, but boundary direction reversed it.

## Artifact Map

- [machine summary](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E05_full/summary.json)
- [condition table](condition_summary.csv)
- [ridge frontier](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E05_full/metrics.parquet)
- [stratified audit](stratified_robustness.csv)
- [run manifest](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E05_full/run_manifest.json)
- local central figure: [prediction-stability frontier](prediction_stability_frontier.png).

## Visualization Audit

The left panel shows every model/checkpoint split contrast and the registered
5% line. The center panel includes every validation-eligible Qwen penalty, with
the split threshold and non-vacuity boundary shown explicitly; all points lie
below 5% and to the right of one. The right panel displays the three held-out
errors rather than only relative effects. Colors in the frontier encode
$\log_{10}\lambda$.

## Claim Boundary

E05 is observational geometry in two frozen model families and one English
treebank. It does not reveal the model's internal causal computation. Its clean
negative/mixed result weakens a global shared-linear tree mechanism, but it
does not show that syntax is absent or that no nonlinear/state-dependent
composition exists.

