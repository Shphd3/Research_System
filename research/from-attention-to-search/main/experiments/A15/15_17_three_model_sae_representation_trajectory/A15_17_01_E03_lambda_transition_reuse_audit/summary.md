# Summary: A15_17_01_E03 Lambda-Transition Reuse Audit

Primary Anchor: `15_17_01_sae_shared_direction_reuse_anchor.md`  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `PASS`; `ELIGIBLE` for the registered descriptive checkpoint contrast. Human mechanism judgment: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 1. Purpose

Test whether the lower native effective dimension observed after the
reconstruction-coefficient transition is accompanied by increased
model-local Top-32 activation reuse on the same frozen 192-record panel.

## 2. Hypothesis

The post-transition 17B checkpoint should have higher cross-record cosine
similarity of normalized Top-32 usage profiles and lower native effective
dimension than the pre-transition 15B checkpoint. The main rival is that native
low dimension arises from decoder geometry, coefficient covariance, or ordinary
training-history drift without increased same-ID support reuse.

## 3. Analysis Method

- Compare the exact 15B `lambda_rec=1.0` milestone with the exact 17B
  `lambda_rec=0.1` milestone using the same 192 N8 records, 256 valid tokens,
  layer-7 native attention-write site, and native Top-32 encoder output.
- Compute the primary mean off-diagonal cosine of each record's normalized
  atom-usage profile; estimate `post - pre` with 2,000 paired record bootstrap
  draws, seed `20260922`.
- Compute centered native-write participation-ratio effective dimension and
  require all loader, alignment, finite-value, Top-32, repeat-forward,
  CPU/GPU, state-immutability, and artifact guards to pass.

## 4. Conclusion

**Registered verdict: `PRE_HIGHER_REUSE`.** The measurement is eligible, but the
registered positive necessary-condition pattern is not observed.

1. **The low-dimension / increased same-ID-reuse conjunction is not supported
   in this transition contrast.** Reuse decreased from `0.647618` at 15B to
   `0.625302` at 17B; `post - pre = -0.022316`, paired-record bootstrap 95% CI
   `[-0.035251, -0.008884]`, entirely below zero. Native effective dimension
   nevertheless decreased from `15.674361` to `8.418492` (`-7.255869`,
   `-46.29%`). The registered rule therefore selects `PRE_HIGHER_REUSE`, not
   `POST_HIGHER_REUSE_AND_LOWER_DIMENSION`.

   **Important figure:** [intuition versus observation](figures/intuition_vs_observation.png).

   **How to read:** the right panel shows the measured reuse contrast below
   zero while native effective dimension falls, so the two changes move in
   opposite directions.

   The figure cannot establish that coefficient reduction caused either change.

2. **The direct engineering and numerical evidence is complete.** All four
   RTX5090 workers passed; 192 records and 49,152 valid tokens per model were
   aligned with zero exclusions. Native Top-32 versus the top-128 prefix had
   zero non-tie mismatches; repeated forwards had zero pooled-write drift; all
   CPU/GPU checks, state-immutability checks, artifact checks, and the
   independent post-run audit passed.

   **Important figure:** [reuse and native-geometry curves](figures/reuse_history_contrast.png).

   **How to read:** the left interval is wholly negative; the center and right
   curves are descriptive concentration summaries, not additional independent
   significance tests.

### Claim Boundary

Can claim: on this fixed panel and these two checkpoints, the post-transition
model has lower native effective dimension but lower model-local same-ID usage
profile similarity. This weakens the specific explanation that the observed
low dimension is accompanied by increased shared-atom reuse.

Cannot claim: isolated causal effect of `lambda_rec`, semantic quality,
downstream utility, training-seed generalization, cross-model atom identity,
or that activation reuse is the only possible route to low dimension.

### Next Step Analysis

**Decision: `AI 建议` — stop treating increased same-ID support reuse as the
default explanation for this transition, and next test decoder-direction
geometry or coefficient covariance on the same two checkpoints.**

Why it follows: native effective dimension fell by 46.29% while the primary
reuse contrast was significantly negative, so the current necessary condition
fails and the strongest rival remains live.

Unresolved uncertainty: the two endpoints are separated by training stage and
additional microbatch, accumulation, CE-chunk, optimizer/RNG history; the
bootstrap covers record sampling, not training seeds or causal uncertainty.

Completion criterion: a same-panel decomposition shows whether decoder
geometry, coefficient covariance, or residual terms account for the native
dimension drop independently of same-ID reuse. A strict causal statement would
instead require a matched fork with only the coefficient changed.

Stop or redirect condition: do not promote a causal coefficient explanation
from this result; redirect to a matched ablation if the scientific question is
specifically the effect of `lambda_rec`.

Resume action: read the full evidence ledger in [detailed.md](detailed.md) and
obtain the researcher's mechanism judgment before updating the Anchor or
closing the Focus.
