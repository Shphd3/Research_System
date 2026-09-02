# Plot Contracts

## Figure 1 — Five-arm held-out NLL trajectory

- Question: which arm learns the best model and when does the ordering appear?
- X: cumulative training tokens in billions.
- Y: held-out NLL in nat/token; lower is better.
- Aggregation: 1,024 fixed documents; seeds shown separately.
- Decides: trajectory and 10B point ordering.
- Does not prove: mechanism or universal scaling.

## Figure 2 — Registered 10B paired contrasts

- Question: which registered causal comparison is directionally stable?
- X: the five registered arm differences for seed 17 and 29.
- Y: paired $\Delta$NLL; negative favors the first arm.
- Error bars: document-level paired-bootstrap 95% interval.
- Decides: pass/fail of each direct comparison within the two seeds.
- Does not prove: population-level seed uncertainty beyond the two seeds.

## Figure 3 — Pairwise NLL differences through training

- Question: does an endpoint ordering persist or emerge late?
- X: training tokens; Y: registered paired $\Delta$NLL.
- Zero means tied; negative favors the first arm.
- Does not replace: the 10B primary decision.

## Figure 4 — Expert-use map through training

- Question: does an arm use the eight experts broadly or collapse onto a few?
- X: training tokens; Y: network layer; color: effective expert count
  $\exp(H)$, from 1 to 8.
- Decides: routing-health description.
- Does not prove: useful specialization.

## Figure 5 — Fixed-token route churn and margin

- Question: how quickly does the Router rewrite its assignments between saved points?
- X: destination milestone; Y: layer; color: fraction of fixed tokens changing expert.
- Companion curve: median winner margin; larger means more decisive routing.
- Does not prove: changed assignments are better.

## Figure 6 — Online tracking accuracy versus continuity

- Question: does the deployed subspace track the exact EMA target better than never
  updating, and what route discontinuity would hard replacement cause?
- X: training tokens.
- Left Y: deployed/target and step0/target subspace overlap, 0--1.
- Right Y: actual-refresh versus hard-replace high-confidence flip.
- Decides: tracking--continuity tradeoff and random-control difficulty.
- Does not prove: NLL utility.

## Figure 7 — Refresh event study

- Question: are statistics refreshes accompanied by sudden training-loss changes?
- X: refresh event index/tokens; Y: post-minus-pre LM loss after subtracting
  Centered-Full's same-step change.
- Color: treatment arm; point size: all-token flip. Accepted gamma remains in
  the linked event table and is not encoded in this figure.
- Decides: whether jumps systematically co-occur with refreshes.
- Does not prove: causal loss effect under changing mini-batches.

## Figure 8 — Expert mechanism trajectories

- Question: do arms differ in expert-choice regret, gradient conflict, or output redundancy?
- X: 0/2B/6B/10B; Y panels: each metric in its native unit.
- Seeds shown separately; layer-average is a descriptive summary.
- Does not replace: held-out NLL or isolate a mechanism without a direct arm comparison.

## Figure 9 — Quality versus compute and wall-clock

- Question: is a quality difference explained by more training compute or statistics overhead?
- X: theoretical training FLOPs fraction or elapsed wall-clock; Y: held-out NLL.
- Decides: fairness interpretation for the registered arms.
- Does not prove: deployment efficiency outside this implementation.

## Rendered-artifact audit

All nine PNG files were opened after final regeneration. Axes, legends,
colorbars, zero lines, error bars, treatment colors, seed styles, and the four
sub-billion milestone labels were visually checked. No clipped labels,
missing panels, reversed signs, or unreadable colorbar semantics remained.
