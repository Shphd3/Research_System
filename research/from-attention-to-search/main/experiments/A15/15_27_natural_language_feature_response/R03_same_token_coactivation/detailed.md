# Detailed: frequency-compatible links and far-context response

**This round yields bounded positive evidence and distinct unresolved questions.** In archived O, 57.7% of edges fall below the chosen incremental-association threshold, and 21.0% do not exceed the destination baseline. In the fixed 512-coordinate analysis, C retains organization beyond the preserved margins and per-position sparsity. Its only support-qualified group, C03, has relevant-minus-unrelated far responses in all six new cases. Frequency similarity within groups, lowest-frequency structure and semantic/function naming remain unresolved. The [Summary](summary.md) owns the concise answer; the [Protocol](protocol.md) retains the original contract. Mechanism acceptance and question closure are Unknown.

## Objects and source

O is the original A15_25 graph over all 16384 coordinates of the final A22 CrossCoder. Each observation is one token's shared z, jointly encoded from residual-post states of zero-based blocks 1, 3, ..., 27 before final global normalization. Layer decoder contributions are not independent layer activations. The exact Base/checkpoint hashes, saved TRAIN centering/vector RMS, BF16 GEMMs, FP32 state/scores and score threshold 0.051281172782182693 are reused. This is not per-token Top256. Old E16 G02/G04 IDs are not aligned.

O requires nA,nB>=200, joint>=20, P(B|A)>=0.8, P(A|B)<=0.5 and pB>=2pA. Its increasing-frequency arrows force a DAG; the recorded maximum depth of 5 is not semantic height. Original outgoing composition lists and list Jaccard are not community clustering. O remains unchanged. [Asset/source audit](asset_audit.md).

## Actual data and measurement qualification

The original exposed-VAL DCLM cache has 10485760 eligible positions in 640 CSR chunks. It is not sealed TEST. Before new statistics, we uniformly selected 512 IDs and 64 original D plus 64 V contexts, resulting in 65464/65484 positions. Original document IDs, reliable sentence boundaries, near-duplicate independence and text types are unavailable. The 2000 context-bootstrap intervals are descriptive sensitivity intervals, not document/sentence confidence intervals. V is neither recovered independent documents nor fresh blind validation.

The text manifest contains 12 constructed scenarios/72 sequences. Only S01–S03 and R01–R03, six complete cases/36 sequences, fit the remaining parent budget; the other 36 texts remain NOT RUN. Each case has semantic A/B and unrelated weekday U at near/far distance. Targets, lengths, absolute positions and the final 5 tokens match; actual lengths are 83–89, near gaps are 6/7 and far gaps are 50–55. Moving neutral filler also changes order/recency. Source/template/entity IDs are distinct from old rounds, but some reading frames/fillers recur; different metadata IDs do not establish statistical independence. [Text manifest](text_manifest.md).

Two cache replays preceded 12 primer sequences, two identical replays and eight prefix checks at a fixed input shape of 256 positions. All gates passed, then the remaining 24 sequences ran. R03 used 48 calls and the conversation reached 1500/1500. Changing Base batch size from 16 to 1 introduces up to 1.936% relative cached-z discrepancy, within the predeclared 2% gate; it is not exact equality. Prefix hook differences and identical-replay z differences are both 0. Target/layer raw-hook NMSE has mean 0.08070 and p90 0.12803, below 0.30/0.50. Eight fixed checks provide finite coverage, not independent replay of every token. Per-token errors are saved. [Qualification](provenance/panel_qualification.json).

## Frozen graph comparison

O preserves 16384 nodes, 214711 D edges and 206136 old-rule V-retained edges. R/C use identical 512 IDs and support nA,nB>=200, joint>=20. R requires conditional probability >=0.8 and has 26/18 D/V edges. C searches all supported pairs for conditional-minus-baseline >=0.05 and has 2792/2916 edges. C is not merely R with edges deleted; all 26 R_D edges also pass C. Both use max symmetrization, fixed greedy modularity, resolution 1 and a minimum of 3 members, with isolated nodes retained. Frequency labels/ratios and semantic names do not enter clustering. Positions on the ID-ordered circle have no evidential role. [Figure 1](figures/figure1_graphs_frequency.png).

The 199 draws across four chains used 10E burn proposals and 2E spacing. Every draw exactly preserved column counts and the selected-coordinate L0 at each row; unselected columns remained unchanged. Maximum split-Rhat was about 1.0221, and burn acceptance was 0.718–0.730. Offline execution took 174.214 seconds, with no model calls or timeout. Finite-chain diagnostics do not prove independent samples.

## Evidence relevant to baseline frequency

Of 214711 O_D edges, 123898 (57.70%) have delta<0.05 and 45171 (21.04%) have delta<=0. Feature f13964 has pD=0.99296 and 15469 incoming edges; f8060 has pD=0.97490 and 15471. All their incoming edges are below 0.05. High conditional probability alone therefore does not establish incremental association or semantic parenthood.

Weak association is not complete frequency explanation. Algebraically, delta<=1−pB, so pB>0.95 cannot admit an incoming delta>=0.05 edge even under perfect conditional coactivation. This threshold has unequal detection capacity across frequencies and cannot decide the function of near-universal components. Nodes are retained; their semantic role remains open. The nonpositive 21.04% is a more direct finite-corpus baseline counterexample. [O summary](provenance/original_O_frequency_summary.json).

The random 512 IDs do not guarantee global-hub coverage. C_D has 2792 edges versus a degree-null median of 108 and maximum of 137. About 69.99% pass the same rule on V; 2703/2792 retain positive V delta. Token/position-stratified adjustment leaves 2658 positive and 1763 >=0.05. The reduction is compatible with these measured factors accounting for some associations; it is not a causal proportion attributable to frequency, token or position. Unknown text types, document structure, templates and duplicates remain rivals. [Structural descriptions](provenance/descriptive_structural_summary.json).

## Group frequency and support gaps

R/C have 2/6 D groups; 1/2 respectively match V at Jaccard>=0.5. Requiring every D member to have >=200 V hits leaves only C03: 72 members, J=0.7439 and minimum 223 hits. C02 has 64 members and J=0.6974, but a minimum of 175; R has no support-qualified union. C03's mean pairwise absolute log-frequency difference is about 1.0821.

None of the 199 nulls produces a qualified stable group. Both frequency comparisons have 0/199 valid null statistics, and p/q remain NA. Missing groups are not zero, infinity or proof of closer observed frequencies. In the positive-frequency bottom quartile, all 124 nodes fail the 200-hit support gate; zero low→high edges is unestimable, not absence. Among estimable edges, the fractions with frequency ratio >=4 are 92.31% for R and 45.13% for C. O's low→high direction is imposed by its rule. [Frequency/support](tables/feature_frequency.csv), [nulls](provenance/null_results.json).

## Far-clue effects and limits

On the only eligible C03 union, member contributions are scaled by fixed natural-reference D RMS. E is the RMS semantic B−A change, and U is the RMS weekday U−A change. The hook-normalized representation is evaluated separately. All 6 far cases have E−U>0: mean 0.160037, with a 95% case interval [0.039337,0.320294]. The normalized mean is 0.00017293, with interval [0.00004461,0.00034596]. Both exact one-sided p values are 0.015625; intersection/BH2 q=0.03125. R is NA because its eligible union is empty. [Figure 3](figures/figure3_near_far.png), [case values](tables/group_case_effects.csv).

This supports a response to preceding content at gaps of 50–55 tokens for some C03 coordinates. Only 1–5 of 72 members change per case; the largest member contributes 46.6%–100% of the squared effect, and dominant IDs differ across cases. It is not a joint semantic response of all 72 members. Semantic edits change more words than the weekday control, so relation-specific meaning is not isolated from general lexical editing. Order/recency remains confounded with relocation. There is no group range specialization or long-range-only inference.

Only S01 favors compatible outputs under both meanings; no person case favors both prescribed names. The two fixed sentence examples demonstrate the success and counterexample without selection for favorable results. [Candidate outputs](tables/candidate_outputs.csv), [worked examples](examples.md).

R02 Q3, concerning joint use of two clues as a sentence progresses, remains **INSUFFICIENT**. R03 adds no four-combination integration test. Passing the current CrossCoder qualification does not repair the earlier E16 prefix-check failure under its different interface or change R02's verdict.

## Naming and token projections

R-02, C02 and C03 all receive mixed-context candidate names under the predeclared rule using the first 32 D contexts. Their function-word proportions are about 2.0%, 10.7% and 40.7%, below 60%; punctuation also fails the threshold. Multiple members, high-z prefixes from distinct contexts and singleton boundary cases are retained. The last 32 D contexts and reused V are descriptive checks, not fresh naming validation. [Selected naming evidence](provenance/naming_summary_selected.json).

The original pooled-maximum display rule selects 12 coordinates dominated by the first token, with zeros at the target. Those images/rules remain as an amplitude-ranking counterexample. Explicitly post-hoc target-focused details improve instance reading without changing groups, thresholds or tests: [crane](figures/figure2a_sense_target_detail.png), [person](figures/figure2b_person_target_detail.png). All 12 displayed target coordinates lie outside the selected 512; C-- denotes candidate coverage, not removal by correction. Every token's active coordinates and original O relations remain execution-side; drawn snapshots display only the first 300 arrows. Neither circle distances nor arrows establish information transfer.

## Existing interventions and proposed next test

25_02 used the same dictionary but different parent states/FP32 evaluation, answer positions and intervention sets. Coordinate overlap cannot supply functional evidence for this group. 25_03 stopped at data qualification, with interventions NOT RUN. A22 whole-layer reconstruction is not a single-feature replacement. [Historical audit](provenance/existing_intervention_audit.json).

One future candidate is f12277 at S01_A_far target crane, index 84, zero-based block 27 residual-post. Replacing its contribution by measured B uses delta_z=−0.00769043, with a native layer-vector change norm of about 2.2063. The falsifiable prediction is a decrease of the flies-minus-lifts candidate margin toward B. Reverse, unrelated-dose and frequency/intensity-matched random-feature controls are necessary; no change, opposite change or equally large random effects weaken the candidate. No replacement was performed, and shared z does not imply independent layer generation.

The [manifest](artifact_manifest.md) traces protocols, hashes, nulls, engineering attempts, NOT RUN cases and calls. Factual delivery is complete; mechanism acceptance and question closure remain Unknown. Two updates and one final question are stated only at the [Summary end](summary.md).
