# One priority next decision: define what the score should compare

[中文](next_decision_cn.md)

**AI recommendation: retain A/B membership and top-1, and design one bounded score-calibration comparison. Not executed; researcher decision pending.** Sending every input to expert 0 by deleting all C terms is not a solution. No automatic regrouping or training follows this round.

Per-feature zero reception is confirmed; C terms determine the original winning margin, while inspected A co-occurrence bounds do not force zero. Defining a comparable score is therefore more specific than immediately attributing zero reception to grouping structure. Frequency, amplitude and composition remain causally entangled, and grouping conflicts are not excluded.

The next Protocol should first specify whether routing compares raw weighted amplitude or response relative to each group's own TRAIN baseline, the designated-expert reception required for each low-frequency target, and which other groups may lose how much reception. These define acceptable tradeoffs. This round did not retrospectively introduce thresholds or a calibration formula.

Any future bounded comparison should apply the same scoring family to A/B, freeze parameters on TRAIN and avoid validation tuning. Evaluate per-feature reception, loads, empty experts and costs to other frequency bands. Merely moving all inputs to one expert does not solve dispatch. Only after reception qualifies and new authorization is given should an independent learning-loss test follow: better reception does not automatically imply better learning.

Three discussion questions:

1. Does “responsible” require a minimum fraction of each target's hits, or a higher target frequency within the expert? These have different denominators.
2. Which other targets may lose how much opportunity to improve rare-target reception?
3. Should the next comparison distinguish unfair amplitude scale from infeasible grouping, and what outcome would make us abandon the current scoring direction?

This round stops here. These are pending design choices, not new execution authority.
