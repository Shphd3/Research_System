# A14_E03 Detailed Evidence

## Models, Data, and Readout

| Model | Role | Frozen commit | Width | Leaf train/test | Composition train/val/test |
| --- | --- | --- | ---: | ---: | ---: |
| Qwen2.5-0.5B | primary | `060db6499f32faf8b98477b0a26969ef7d8b9987` | 896 | 8,192 / 1,839 pairs | 4,096 / 1,024 / 1,024 |
| Pythia-410m | replication | `9879c9b5f8bea9051dcb0e68dff21493d67e9d4f` | 1,024 | 8,192 / 1,881 pairs | 4,096 / 1,024 / 1,024 |

Every span was independently tokenized, followed by one shared EOS readout.
Leaf controls matched sentence, word length, exact tokenizer subtoken length,
and approximate training frequency. Composition used only naturally binary
annotated nodes. Random baselines used identical architecture/configuration and
seed 1403.

Execution command:

```bash
python scripts/run_pretrained_tree_geometry.py \
  --config configs/exp3_pretrained_tree_geometry.yaml \
  --output-dir outputs/A14_E03_full
```

Environment: Python 3.10.12, PyTorch 2.3.0a0+nv24.04, Transformers 4.57.6,
BF16 model forward passes on CUDA and double-precision spectral/probe analysis.

## Final-Layer Evidence

| Model/checkpoint | Leaf $k/d$ | Leaf advantage | Composition error | Composition advantage | Bound ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen pretrained | 0.0268 | 0.2766 | 0.4893 | 0.6651 | 10.803 |
| Qwen initialization | 0.7087 | 0.2011 | 0.7724 | 0.4520 | 1.459 |
| Pythia pretrained | 0.3359 | 0.2132 | 0.4603 | 0.6071 | 1.772 |
| Pythia initialization | 0.3291 | 0.2004 | 0.4455 | 0.6926 | 1.693 |

All leaf and composition confidence intervals exclude zero. Qwen's training
increments meet the registered five-point threshold; Pythia's do not.

## Why the Main Mechanism Does Not Pass

The Qwen ridge probe selected the largest registered penalty, $\lambda=100$,
yet had $\|W\|_2=36.36$. Its child rank-$k$ error was 668.97 and test
innovation norm was 1,190.76, producing $B=18,389.93$ and
$B/\|H_{parent}\|_F=10.80$. Pythia's corresponding ratio was 1.77.

The bound inequality itself holds because the fitted test residual is included
as innovation. The informative result is that the bound is not non-vacuous.
This separates predictive composition from stable low-rank propagation.

## Rival Audit

- **Mean pooling:** EOS readout was primary; mean pooling was diagnostic.
- **Global direction:** every primary matrix used the training mean.
- **Readout position:** leaf controls matched exact subtoken count.
- **Probe capacity:** one shared ridge operator, file-level split, and
  validation-only regularization selection.
- **Architecture prior:** large positive gaps at random initialization show
  that true-span geometry is not by itself evidence of learned hierarchy.
- **Replication:** Pythia reverses the composition-emergence contrast, so the
  Qwen training increment is not architecture-general.

## Artifact Map

- [machine summary](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E03_full/summary.json)
- [condition table](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E03_full/condition_summary.csv)
- [run manifest](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E03_full/run_manifest.json)
- per-model leaf and composition records live under the corresponding worker
  output subdirectories;
- local central figure: [geometry and bound guard](tree_geometry_advantages.png).

## Visualization Audit

The first two panels report the exact registered relative advantages; dotted
lines mark the 0.10 thresholds. The third panel reports the one-step bound
ratio, with the dotted line at the non-vacuity threshold 1. The figure makes
the mixed verdict visible rather than presenting only the positive geometry
gaps.

