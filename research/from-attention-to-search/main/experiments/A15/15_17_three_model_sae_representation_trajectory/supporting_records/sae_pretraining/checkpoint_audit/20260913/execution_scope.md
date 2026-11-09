# Dense SAE checkpoint audit: authorized execution scope

Updated at: 2026-09-13T12:35:02Z

The researcher explicitly requested an inference-only audit of the complete
0.5B, 1B, 3B, 5B and 10B checkpoints. This record fixes the operational scope;
it does not own a scientific verdict or authorize changes to either training
run.

## Fixed inputs

- Checkpoints: the five complete paired LM/SAE milestone directories under
  `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/full_50b_bottleneck8_202609121130/milestones/` at exactly 0.5B, 1B, 3B, 5B and 10B trained prediction tokens.
- Representation: the final block's post-`norm2` SAE input immediately before
  the final MLP; the trained MLP consumes the SAE reconstruction.
- Evaluation corpus: every complete 2,048-token sequence in the frozen held-out
  validation shard from manifest
  `/data/250010109/training_data_views/dclm_pair_v1/manifest.json`, SHA-256
  `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`.
  This yields 56,146 identical sequences and 114,987,008 identical causal
  positions per checkpoint. It excludes the frozen training view.
- Feature display: the same 20 continued feature IDs at every checkpoint,
  sampled with seed 17 without replacement from the 100 largest cumulative
  training firing counters at 10B. This is a declared qualitative selection,
  not a semantic label or an unbiased feature sample.

The executable definition is
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/configs/checkpoint_audit_0p5_1_3_5_10b.json`.

## Required outputs

1. Fixed-corpus normalized SAE reconstruction MSE versus checkpoint.
2. Mean number of strictly positive features per token versus checkpoint.
3. Feature coverage and dead-feature fraction versus checkpoint.
4. One activation-frequency distribution per checkpoint, an all-checkpoint
   overlay, and pairwise Spearman/Jensen-Shannon comparisons.
5. Cross-checkpoint frequency and maximum-activation heatmaps for the fixed 20
   features, plus their top-five decoded activation contexts at every
   checkpoint.

All scalar aggregation uses the complete fixed corpus. Training-time cumulative
firing counters and per-update sampled reconstruction loss may be reported only
as provenance or a rival diagnostic; they are not substituted for evaluation.

## Execution and gates

- Authorized exception profile/image: `h100-2-spot` and `shphd-lite-0911`,
  resolved only through `docs/execution_envelope.md`; one node and two ranks.
  The researcher authorized either two H100 or two RTX 5090 SPOT GPUs after the
  default four-H100 request failed. Two H100 is selected because it preserves
  the qualified H100 runtime and avoids an SM120 compatibility layer. No other
  fallback profile is authorized.
- Entry: execution `scripts/run_checkpoint_audit_2h100.sh OUTPUT_DIR`, submitted
  through `templates/execution/acp_submit_template.sh`.
- The entry first runs an eight-sequence, 16,384-token GPU Smoke across all five
  checkpoints. The full held-out sweep starts only if the Smoke receipt is
  `PASS`, every checkpoint identity matches, all scalars are finite, all ranks
  cover disjoint fixed samples, and every required Smoke plot/text artifact
  exists.
- Full completion requires 114,987,008 positions for each checkpoint, five
  per-checkpoint summaries/count arrays, all required plots and text listings,
  a `PASS` audit receipt, terminal exit 0, a durable pod log and platform
  success.

The source checkpoints were written by four-rank training with
`state_layout=replicated`. Two-rank inference loads only the replicated model
state and repartitions the fixed evaluation corpus; it does not restore the
training optimizer, RNG or data cursor. Therefore matching the training
world-size is not required for this read-only evaluation.

## Claim boundary

The audit measures reconstruction, sparsity, coverage and activation-frequency
behavior on one fixed held-out token stream. It does not establish semantic
feature identity, interpretability, causal utility, downstream capability or
SAE benefit relative to the native baseline. Similar marginal frequency
distributions do not prove that the same feature means the same thing over
time; the decoded contexts are qualitative evidence requiring researcher
interpretation.
