# A14_E02 Detailed Evidence

## Data and Representation

- NLTK Penn Treebank parsed sample: 199 source files, 3,914 sentences;
- file-level split: 139/30/30 files and 3,068/433/413 sentences;
- eligible length-2-to-4 coarse leaves: 14,888/2,134/1,970;
- training-only 2,048-token vocabulary and PPMI counts, symmetric window 5;
- no SVD or learned projection was used to create word vectors;
- seed 1402 and 1,000 paired sentence bootstrap replicates;
- corpus archive SHA-256:
  `9da92d76c3666cfb6cddeaed0f7e86b344cce0f0928a286d439e555f19c37399`.

Execution command:

```bash
python scripts/run_gold_syntax_ppmi.py \
  --config configs/exp2_gold_syntax_ppmi.yaml \
  --output-dir outputs/A14_E02_full
```

## Primary Evidence

| Metric | Gold | Matched control | Coordinate permutation |
| --- | ---: | ---: | ---: |
| frozen-subspace projection error | 0.0606 | 0.0921 | 0.6744 |
| sentence-bootstrap 95% interval | [0.0561, 0.0652] | [0.0860, 0.0985] | diagnostic only |

The paired relative advantage was 0.3420 with interval [0.2907, 0.3894]. The
held-out generalization clause therefore passes with a large margin. The
absolute rank clause does not: $r_{0.05}=657$, so $r_{0.05}/2048=0.3208$.

## Interpretation Audit

- **Observation:** gold constituents lie closer than controls to the frozen
  training-gold subspace.
- **Interpretation:** syntactic selection is associated with shared
  distributional covariance beyond exact length and approximate frequency.
- **Cannot claim:** that the 657-dimensional space is low enough for the main
  theorem premise, that mean composition caused it, or that a neural model
  represents the same space.

## Environment

Python 3.10.12, NumPy 1.24.4, SciPy 1.12.0, NLTK 3.10.0, PyTorch
2.3.0a0+nv24.04, CUDA spectral analysis.

## Artifact Map

- [machine metrics](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E02_full/metrics.json)
- [paired span records](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E02_full/span_records.parquet)
- [run manifest](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E02_full/run_manifest.json)
- local central figures: [spectrum](spectrum.png) and
  [projection errors](projection_error.png).

## Visualization Audit

The spectrum is computed from centered training-gold spans only; the red line
marks the frozen $k=657$ and the black line marks 95% energy. Projection bars
use held-out matrices centered by the training mean. Confidence intervals are
reported numerically above rather than inferred from bar height.

