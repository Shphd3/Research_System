# A15_02_03 Thinking Card: Coarse/Fine Semantic Concentration In MLP-Input Channel Groups

Status: on 2026-08-05 the researcher froze the measured object and authorized an Anchor and non-executable Protocol draft.

## Researcher Judgment

- **Phenomenon:** prior audits found a late fine-relative semantic gain in whole representations and genuine attention-head outputs. The new audit fixes each layer's actual 4096-dimensional MLP input, splits it into 32 contiguous 128-dimensional channel groups, and compares group-level versus full-state coarse/fine variance and discriminability.
- **Mechanism guess:** after multi-head mixing, residual addition, and post-attention RMSNorm, coarse/fine semantic signal may remain unevenly concentrated in a subset of channels; a group may therefore have a higher signal-to-within-class-variation ratio than the full state.
- **Required measurements:** actual coarse/fine between-class variance, within-class variance, discriminability, fine-relative-to-coarse discriminability, and an eight-band covariance atlas inside each group.
- **Required summaries:** report the per-layer mean, typical value, and maximum across 32 groups; the maximum cannot stand in for a typical-group claim.
- **Most uncertain point:** whether contiguous channel groups expose learned functional concentration or whether arbitrary 128-dimensional partitions and post-hoc maximum selection reproduce the same result.
- **Evidence that changes the judgment:** if the typical or maximum advantage of the fixed grouping does not exceed random channel repartitions, or does not replicate on an independent semantic taxonomy, do not interpret it as a model-specific channel coordinate.
- **Current decision:** review the Anchor and Protocol, then decide separately whether implementation and execution are authorized.

## AI Audit

- These objects are `G1--G32 channel groups`, not attention heads.
- Mean per-direction raw variance across groups equals the full-state per-direction raw variance, and full-state discriminability is a within-variance-weighted mean of group discriminabilities. Therefore naive mean-energy and best-greater-than-full statements are partly algebraic.
- The strongest rival is an equally shaped random channel partition; the minimal falsifier compares fixed grouping with that null on untouched evidence and corrects the maximum over layers and groups.
- Recommendation: pursue as a frozen static concentration and metric audit, not as Router construction.

## Researcher Confirmation

- The object is the post-attention RMSNorm output directly entering each block MLP, in native channel order, split into 32 contiguous 128-dimensional groups.
- Each group has eight equal-rank covariance bands: F1=head, F2--F5=middle, F6--F8=tail.
- Formal Anchor writing is authorized; execution is not.

