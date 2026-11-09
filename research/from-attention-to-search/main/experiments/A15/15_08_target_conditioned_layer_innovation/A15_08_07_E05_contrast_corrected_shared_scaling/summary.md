# Result summary

## Status

`RESULT_COMPLETE_NEGATIVE_FOR_PRIOR_LOW_RANK_CLAIM`

The architectural redo completed on one 8xRTX-5090 node (`pt-sd0hpsc7`, succeeded) and a new 640-row confirmation-v4. The full contrast-corrected \(R_U\) map has a positive 95% lower confidence bound for all eight domains at both blocks, so the negative rank result is not caused by an absent \(R_U\) gain.

## Main findings

1. **The old “one domain needs only a low-rank space” claim is not confirmed.** After removing the common-logit direction, an eight-class task has at most seven effective contrasts. At block 24, none of the eight domains has an admitted \(r_{90}\). At block 28, only biology passes, at rank 7. Although rank-7 point estimates retain approximately 100% of the full-map gain, the registered familywise 95% lower bounds remain below 0.90 for 15/16 layer-domain tasks.
2. **Class scaling is consistent with the classifier ceiling, not demonstrated representation compression.** Among the admitted class-subset tasks, every \(r_{90}\) equals \(C-1\): 25/32 binary subsets per layer pass at rank 1; no four-class subset passes; only one six-class subset passes (block 28, rank 5); and only one eight-class task passes (block 28 biology, rank 7).
3. **Low cross-domain overlap is only a diagnostic, not an admitted Router result.** At fixed rank 7, same-task bootstrap refits overlap by 14.37%/13.79% at blocks 24/28, versus cross-domain overlap of 1.67%/2.03% and a Haar expectation near 0.17%. The relative gap indicates task-specific signal, but the absolute retraining stability is low. Because almost all formal \(r_{90}\) values are NA, no registered \(r_{90}\) cross-domain heatmap exists.
4. **The old shared 56D result was an oracle-union construction, not evidence for a naturally learnable shared space.** Under the registered cross-rank and cross-task confidence correction, no multi-domain method has an admitted shared \(r_{90}\). In a disclosed fixed-rank sensitivity that omits only the cross-rank familywise correction, the local-union oracle reaches 90% at 54D/52D for blocks 24/28, while direct joint learning remains NA. Thus the near-56D curve can be reproduced only after local answers are known.

## Decision

Do not state that a single domain has a compact functional subspace or that a directly learnable shared functional dimension grows with task count. The corrected evidence supports only a weaker diagnostic statement: task-conditioned rank-7 directions contain more reproducible within-task structure than cross-task structure, but they are not stable enough, and not compressed enough below \(C-1\), to promote as tokenwise Router coordinates.

