# Final Figure Contracts

## Figure 1 — Five-arm held-out NLL trajectory

- Question: which arm learns the best model and when does the ordering appear?
- X: cumulative training tokens; Y: held-out NLL in nat/token, lower better.
- Source: 1,024 fixed documents at 11 milestones, seeds separate.
- Allows trajectory description; the 10B endpoint remains primary.

## Figure 2 — Registered 10B paired contrasts

- Question: which registered comparison is directionally stable?
- X: paired Delta NLL, negative favors the first arm.
- Error bar: 10,000-draw document-level paired-bootstrap 95% interval.
- Allows the primary within-seed endpoint decision; not population seed inference.

## Figure 3 — Pairwise NLL differences through training

- Question: is the endpoint ordering persistent or late-emerging?
- X: training tokens; Y: registered paired Delta NLL.
- Allows trajectory interpretation; does not replace Figure 2.

## Figure 4 — Effective expert count

- Question: does an arm broadly use the eight sparse experts or collapse?
- X: training tokens; Y: arm and layer; color: \(\exp(H)\) from 1 to 8.
- Allows a routing-health description; not useful-specialization proof.

## Figure 5 — Fixed-token route churn and margin

- Question: how fast are assignments rewritten between checkpoints?
- X: milestone; heatmap color: fixed-token route-change fraction.
- Companion Y: layer-averaged median top1--top2 logit margin.
- Allows routing-dynamics description; not routing correctness.

## Figure 6 — Online tracking versus continuity

- Question: does the deployed flag beat never updating, and what would hard
  replacement do to routes?
- X: training tokens; Y: subspace overlap or high-confidence route flip.
- Allows the tracking--continuity verdict; not NLL utility.

## Figure 7 — Refresh loss event study

- Question: do projector refreshes systematically co-occur with training-loss jumps?
- X: refresh tokens; Y: treatment post-minus-pre loss change minus the matched
  Centered-Full change; point size: all-token flip.
- Allows a co-occurrence check; not a causal loss effect.

## Figure 8 — Expert mechanism trajectories

- Question: how do route regret, best-expert match, gradient conflict, and
  output redundancy change at 0/2B/6B/10B?
- X: training tokens; Y: each metric in its native unit, seeds separate.
- Allows mechanism interpretation; no panel replaces held-out NLL.

## Figure 9 — Quality versus compute and wall-clock

- Question: is an ordering explained by more training compute or refresh overhead?
- X: matched 10B compute fraction or observed hours; Y: held-out NLL.
- Allows implementation-specific fairness interpretation; not universal
  deployment efficiency.

## Visual audit

All nine final renderings were opened.  Axes, legends, error-bar signs,
colorbars, seed styles, zero lines, and distinct 50M/100M/250M/500M labels
were verified.  Full renderings live in the self-contained report directory;
Figures 1, 2, and 6 are copied beside the canonical result record.
