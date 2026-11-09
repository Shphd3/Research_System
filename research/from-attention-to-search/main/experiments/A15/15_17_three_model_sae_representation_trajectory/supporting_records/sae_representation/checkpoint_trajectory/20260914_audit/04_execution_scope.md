# Analysis1 checkpoint-only execution scope

## Authority and objective

On 2026-09-13 the researcher authorized two separate jobs on `5090-2-spot`: a
bounded Smoke and, only after that Smoke passes, the full `analysis1` semantic
evaluation. Both jobs only read immutable checkpoints and write analysis
artifacts. They contain no optimizer and must report `optimizer_updates: 0`.

This authorization does **not** permit starting a model-training process,
stopping or modifying any existing training process, changing checkpoint
contents, or submitting on another resource profile.

## Frozen inputs

- SAE-mediated trajectory: 0.5B, 1B, 3B, 5B and 10B cumulative-token
  milestones from `full_50b_bottleneck8_202609121130`.
- Candidate panel: 864 English statements, 216 facts, SHA-256
  `7d11e9625eb7fcf4885e46ca7928926b621d6c6e4485d06f5bd86cc91dc69c55`.
- Representation: final block post-`norm2`, immediately before the final MLP.
  In the SAE-mediated model, `h` is the pre-SAE value and `h_hat` is the
  reconstruction actually consumed by that MLP.
- External reference: `/data/share/Qwen3-0.6B-Base`, frozen and read at its
  final MLP input. This is an unmatched mature endpoint, not a no-SAE matched
  baseline.
- Execution tuple: profile `5090-2-spot`, image `shphd-lite-0911`, current
  isolated SM120 runtime layer if the base image lacks RTX 5090 support.

## Eligibility boundary

The matched Dense baseline job has not produced a usable checkpoint. It must
not be stopped or resubmitted by this analysis. The Qwen endpoint therefore
serves only as a panel/readout sanity reference.

The panel was programmatically constructed and has not been adjudicated by the
researcher. All outputs are therefore `BOUNDED_EXPLORATORY_ONLY`: they can
diagnose the analysis pipeline and suggest patterns, but cannot establish the
registered semantic-formation hypothesis.

## Gates

Smoke passes only if exactly two CUDA ranks run, the stratified 24-example set
covers all 12 leaves, finite caches exist for 0.5B, 10B and Qwen3-0.6B, the
receipt says `PASS`, and optimizer updates equal zero.

The full job may be submitted only after that receipt exists. Startup
supervision ends when the ACP job is scheduled/running, both GPUs are visible,
the fixed contract is written, and at least one cache-completion progress event
or equivalent healthy bounded progress is present. The full result itself is
not required before supervision stops.
