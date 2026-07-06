# V2.1 Implementation Audit Checklist

Use this checklist after Codex implements the scripts.

## Router construction

- [ ] Quantiles are computed inside each node.
- [ ] Split ratios follow child expert counts.
- [ ] Leaf count equals expert count.
- [ ] Each leaf maps to exactly one expert.
- [ ] Prediction uses stored thresholds only.
- [ ] Holdout data are never used for calibration.

## Naming

- [ ] Random-axis baseline is not called fixed-basis.
- [ ] Forced-count baseline is not called load-balancing loss.
- [ ] Naive slow update is separated from margin-aware update.

## Expert-weight handling

- [ ] SVD sign ambiguity is handled.
- [ ] Projective prototypes are available.
- [ ] Prototype spread reports nearest-neighbor cosine and max cosine.
- [ ] Expert weights are not used to access labels.

## Tie handling

- [ ] Lexicographic feature-derived tie keys implemented.
- [ ] Tie rate reported.
- [ ] Max atom mass reported.
- [ ] Exact split impossibility reported when relevant.

## Experiments

- [ ] Calibration and holdout metrics separated.
- [ ] Feature labels used only for evaluation.
- [ ] Balanced assignment used only as control.
- [ ] Training experiments include true learnable-router baseline if claiming training dynamics.
- [ ] Route flip rate and margin p05 reported over time.

## Paper update

- [ ] No numbers manually entered.
- [ ] Claims follow the hierarchy: mass -> coherence -> preservation.
- [ ] Failure modes tied to violated assumptions.
