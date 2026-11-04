# Within-sentence organization: coordinate recurrence, without established old-graph replacement

**Question.** Do earlier active coordinates recur later in the same math/biology sentence, or connect to different later coordinates through an old graph, beyond unrelated-document controls? This completed cache analysis reuses exposed texts and is exploratory.

**Representation.** Each token is a column of native sparse positive activations, each row a fixed dictionary coordinate. SAE has 32 active coordinates per position. CrossCoder has one shared code across 14 residual-post hooks, not independent layerwise activations. Persistent, intermittent and position-local coordinates coexist; heatmap row order has no semantic-level meaning.

## Conclusion and recognition update

These are bounded evidence-based conclusions and AI interpretation. Human mechanism acceptance and question closure remain Unknown.

1. **Matched positions exhibit extra same-coordinate recurrence, including different token IDs.** Of the primary H1 cells, 41 pass both positive simultaneous matched intervals and qualified fixed-margin-null diagnostics; 31 of these are different-ID cells. For CC/biology/middle-frequency at distance 16–31, real persistence is 16.75% versus 4.48%, an excess of 12.26 percentage points with simultaneous interval [6.77, 17.75]. Random empty denominators invalidate the affected cell-null envelope; they are never converted to zero. The [336-cell ledger](evidence/primary_336_final.csv) retains all missing and insufficient cells.
2. **Excess is descriptively larger nearby and can persist farther away.** All-frequency diagnostic excess is about 20–27 points at distance 1 and 7–11 points at 16–31. This is not a monotonic decay law or a causal effect of distance: sentence length, positions and matching support differ. There are no exact-ID lexical matches at 64+.
3. **Near-saturated old-graph coverage does not establish replacement.** Forward coverage is about 99% in both conditions, often 100% for low/middle-frequency sources. The biology/high-frequency distance-1 conditional excess is +0.590 points. Yet all defined common-lost-source forward differences are exactly zero across the 2,383 T1 different-ID lexical pairs; all-source forward differences are also zero. Changing lost-source composition generates the small conditional advantage, without demonstrating preferential connection for a fixed source set. Neither small biology/high-frequency near-distance advantage exceeds the degree-null envelope; no H2 primary cell passes the complete background controls.

**Scope.** T1 covers only 3,529/161,251 (2.19%) SAE and 2,383/161,251 (1.48%) CC different-ID lexical pairs. About 84% of matched target instances are `the`, `and`, `of`, `a`, or `with`. Findings therefore concern this narrow support, not all scientific concept words. No causal transfer, complete retention or semantic hierarchy is established. SAE H2 remains blocked by the old graph's unqualified activation interface.

## Analysis and reading the figures

The following all-frequency table is descriptive; it does not replace the frequency-specific primary tests. Real and control use the identical matched mask and equal pair-within-sentence, sentence-within-document, document-within-block, then block weights. [Source table](evidence/distance_reading.csv).

| Dictionary/domain | Distance 1: real/control | Excess (pp) | Distance 16–31: real/control | Excess (pp) | Contributing blocks, near/far |
| --- | ---: | ---: | ---: | ---: | ---: |
| SAE / math | 38.44% / 18.60% | +19.84 | 24.06% / 16.77% | +7.29 | 26 / 15 |
| SAE / biology | 40.63% / 15.52% | +25.11 | 25.09% / 13.75% | +11.34 | 20 / 17 |
| CC / math | 46.24% / 20.03% | +26.21 | 25.30% / 17.94% | +7.35 | 22 / 12 |
| CC / biology | 44.45% / 17.34% | +27.10 | 23.63% / 15.86% | +7.77 | 18 / 14 |

**Figure 1:** token order horizontally, fixed coordinates vertically, binary positive activity in dark color. Only the frozen top 24 recurring rows are displayed; omitted union and per-token counts are saved. The biology sentence has 222 SAE coordinates (161 occur at one position, one at all 13 positions) and 1,681 CC coordinates (963 occur once, 12 at every position). This shows coexistence of recurring backgrounds and local coordinates, not that all features persist. [Math](figures/figure1_math.png), [biology](figures/figure1_biology.png), [weak case](figures/figure1_counterexample.png).

**Figure 2:** top blue/orange curves are real/control persistence, bottom purple is real minus control. Horizontal categories are token-distance bins; top uncertainty is pointwise, bottom uncertainty simultaneous across the registered primary family. A missing band does not imply a known zero. [Figure 2](figures/figure2_distance.png).

**Figure 3:** separate forward/reverse old-edge coverage of lost source coordinates. Its denominator differs from H1, so the percentages cannot be added. Read the excess and common-source diagnostic, not the near-100% forward level alone. The arrow diagram uses actual old same-token coactivation edges; it does not show information flow or state transitions. [Figure 3](figures/figure3_distance.png), [sentence edges](figures/figure3_sentence_edges.png), [composition audit](evidence/composition_diagnostic.json).

## Actual examples and weakest case

- **Math:** “Power is determined by computing the Banzhaf power index for each player, resulting in a power distribution for the weighted voting system.” Five eligible different-ID pairs give SAE 42.50% versus 9.38%, +33.12 points. `computing → the` gives 21/32 versus 4/32 retained coordinates. All five pairs share one target/control, so they are not independent replicates. No qualifying CC T1 pair exists for this sentence; no coordinate has been assigned a voting-power semantic label.
- **Biology:** “Cell division in the papilla is either rare or non-existent.” Three eligible pairs give CC identity 37.98% versus 18.46%, and forward graph coverage 99.76% versus 98.12%. For `Cell → the`, all 165 common-lost coordinates connect in both conditions: 100% versus 100%. This is a concrete denominator-composition warning.
- **Weak case:** “A typical example here is to use the abstract tensor formalism to understand Hopf algebras.” Four pairs give SAE 21.88% versus 26.56%, CC 28.77% versus 29.44%; CC forward excess is −0.336 points, reverse +0.115. No sentence meets the frozen requirement that all three CC excesses be nonpositive. This is the weakest available case and a counterexample to universal extra identity recurrence, not zero raw recurrence.

Examples were selected by frozen extremes and are not representative. [Selected cases](evidence/selected_cases.json), [pair walkthrough](evidence/case_pair_walkthrough.json). Full methods, null qualification, limitations and lineage are in [Detailed](detailed.md). The researcher decides whether any bounded residual warrants a separate context-replacement intervention; none was run or authorized by these results.
