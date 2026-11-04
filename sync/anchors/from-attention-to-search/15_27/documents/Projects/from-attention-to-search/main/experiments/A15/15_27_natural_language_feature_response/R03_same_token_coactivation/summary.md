派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/summary.md)；研究修改仍回到原件。

---

# R03: which coactivation links exceed frequency, and do distant clues still affect responses?

**Many high conditional probabilities in the old graph are close to the target node's already high marginal rate. The new subgraph nevertheless contains links absent from margin-preserving randomizations, and distant clue edits still change responses. Within-group frequency similarity, low-to-high organization and whole-group semantic function remain unresolved.** The object is coactivation of fixed features at the same token. The original graph O is preserved; new raw and corrected graphs R/C are separate from the old response-difference groups G02/G04.

## Evidence relevant to baseline frequency

We reuse Qwen3-0.6B and the final A22 CrossCoder's shared-z cache. Frequency is the fraction of active token positions. DeltaP subtracts B's marginal rate from P(B|A). Before analysis, 512 dictionary IDs and 64 contexts on each D/V side were fixed. Graph relationships determine groups; frequency labels do not enter clustering.

| Observation | Interpretation and boundary |
| --- | --- |
| Of 214711 original O edges, 57.7% have deltaP<0.05 and 21.0% have deltaP≤0. Among old-rule review-retained edges, 59.5% remain below 0.05. | High conditional probability often does not imply a large excess association. However, deltaP≤1−p(B): when p(B)>0.95, the 0.05 threshold is unattainable. Small delta does not show lack of function. O's frequency-doubling rule forces its DAG; graph depth is not semantic height. |
| New R has 26 edges, all also in C. C has 2792 edges; about 70.0% reproduce under the same rule on V. In 199 randomizations preserving feature counts and per-position sparsity, C has median 108 and maximum 137 edges. After token/position adjustment, 2658 observed links remain positive and 1763 remain≥0.05. | The sampled subgraph contains coactivation beyond these margins and measured strata. Original document/sentence identity and text types are unavailable, so context intervals are descriptive. This is not a population or causal-module result. No new R edge disappears under correction; old O and the new subgraph cannot be combined into a deletion rate. |
| None of 199 nulls has a qualified stable group, so frequency-comparison p/q values are NA. None of the 124 low-quartile nodes reaches 200 hits. | Within-group frequency similarity and low-to-high links are unestimable, rather than absent. The three nameable stable groups, R-02/C-02/C-03, receive only the candidate description “mixed-context group.” |

## Distant responses persist, with a narrower interpretation

C-03 has 72 members and D/V membership Jaccard 0.744. It is the only group meeting the all-member support requirement. At the aligned target, subtract the magnitude of the unrelated weekday edit A→U from that of the relevant edit A→B. All six far-case contrasts are positive: the discovery-scaled mean is **0.1600, with a 95% case interval [0.0393,0.3203]**. The hook-normalized version is also positive; the registered intersection test and BH2 give **q=0.03125**. This supports distant-edit response on this panel. The [Detailed record](../../../../../../../../UNAVAILABLE.md) retains calculations and qualification.

Only 1–5 members change in each case. The result does not mean that all 72 members jointly express a sentence. Relevant edits change more words than the weekday control, and distance still changes order/recency. Semantic specificity and long/short-range division therefore remain unresolved. Each relation has only three cases. Only S01 favors compatible continuations under both clues; the person-role count is 0/3. This is not overall understanding success.

For fixed S01, target crane (ID 72947, position 84, gap 50), f12277 changes from z=0.01909 to 0.01140; the unrelated value is 0.01860. This feature dominates that case's group change. The counterexample is fixed R01, target was (ID 572, position 82): f2174 changes from 0.04340 to 0.04242, with unrelated value 0.04315. The A/B contribution cosine is 0.99655, yet B favors the wrong candidate. High cosine does not ensure a correct relation. [Exact prefixes and values](../../../../../../../../UNAVAILABLE.md).

[Figure 1: graph and frequency](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/figures/figure1_graphs_frequency.png) · [Figure 3: near/far responses](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/figures/figure3_near_far.png) · [S01 target detail](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/figures/figure2a_sense_target_detail.png) / [R01 target detail](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/figures/figure2b_person_target_detail.png). The original full-sentence maximum-ranking display is dominated by the first token and fails to expose target differences; it is retained. Post-hoc target-detail figures explain instances only. C-- marks lack of coverage by the fixed 512 candidates, not removal by frequency correction.

R02 Q3, concerning joint use of two clues as a sentence progresses, remains **INSUFFICIENT**. R03 adds no four-combination integration test. Passing the current CrossCoder qualification does not repair the earlier E16 prefix-check failure under its different interface.

All 36 panel inputs and 12 qualification calls passed, using 48 new forwards and **1500/1500** cumulatively. There are no further calls, training or interventions. R01/R02 remain unchanged. Shared-z layer decoder contributions are not independent layer activations. The [manifest](../../../../../../../../UNAVAILABLE.md) traces data, definitions, code, assets and gaps. Mechanism acceptance remains Unknown.

## Two updates and one next question

1. **Observation:** most old edges have small delta, while new C has far more links than the margin-preserving random graphs. **Interpretation:** the old-edge pattern is compatible with a high-baseline explanation, while additional coactivation structure remains in the sampled graph. This is not a causal decomposition of connectivity. **Boundary:** the delta threshold limits incoming edges to extremely frequent nodes; within-group frequency similarity and low-frequency links are unresolved, and frequency causation is untested.
2. **Observation:** C-03 passes the far-edit response criterion, but a few members dominate and most candidate outputs do not correspond. **Interpretation:** some graph coordinates respond to distant prefix changes. **Boundary:** this is not whole-group semantic integration, long-range exclusivity or expert specialization.

**One AI-proposed question, not executed:** at S01_A_far's crane, position 84, replace only f12277's contribution at zero-based block 27 residual-post with the B dose (Δz=−0.00769043). Does the flies-minus-lifts logit margin decrease toward B? Matched random features, reverse dose and unrelated-edit dose at the same hook/position are required controls. No change, opposite change or an equally large random effect would weaken this candidate.
