# Protocol: A15_27 R03 same-token coactivation, frequency and clue distance

## 0. Approval Snapshot

Status: `APPROVED_FOR_BOUNDED_READ_ONLY_PENDING_HASH_FREEZE`. The researcher explicitly authorized this supplement, delegated operational choices, and requested execution after freezing without routine item-by-item review. This is not fabricated human confirmation of individual A–G blocks. The primary [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/15_27_natural_language_feature_response_anchor.md) and [Focus](../../../../focus/focus_natural_language_feature_response.md) own the question; this Protocol owns exact execution. Root must finish their alignment and record source hashes before actual analysis.

Purpose: separate the baseline-frequency explanation of coactivation from reproducible association beyond marginal rates, then ask whether fixed graph groups respond to distant semantic clues. Role: operationalization and rival-explanation test. R01/R02 remain unchanged. The main object is same-token raw coactivation, not their response-difference groups G02/G04.

The parent endpoint is **1452/1500 forward calls**. R03 may use at most **48** additional calls, including all checks and failures; it does not reset the cap. It plans 36 controlled inputs and 12 qualification calls. Use existing current-container resources only. No training, parameter update, activation replacement, sealed TEST read, deletion, purchase, resource allocation, commit, push or external publication is authorized. Scientific mechanism acceptance and question closure remain `Unknown`.

## 1. Terminology / Definitions

A feature is one coordinate of the fixed final A22 CrossCoder, with model, dictionary and hook identity attached. One coactivation observation is one eligible token position. Binary activity is \(X_{tf}=1[z_{tf}>0]\), using the saved inference gate. Frequency is \(p_f=n_f/N\), the proportion of eligible positions with positive activity; it is not word frequency, amplitude or singular value.

For features A and B, the directed conditional probability is \(P(B\mid A)=n_{AB}/n_A\). Its baseline-corrected association is \(\Delta_{AB}=P(B\mid A)-p_B\). Report both marginal counts, joint count and denominator. Lift is auxiliary and cannot rescue low support. Conditional asymmetry is not causal direction or semantic parenthood.

Three graphs retain separate identities: **O** is the unchanged original graph; **R** is this round's raw conditional graph; **C** is this round's baseline-corrected association graph. A community is a reproducible group under the frozen graph algorithm, not a semantic level or an expert. The cue gap counts tokens after the cue ends and before the target begins: near 1–8, far 48–64. This is a local experimental scale.

## 2. Anchor Alignment

The question is which relations can be explained by feature marginal rates and which retain contextual association. O already uses a frequency-ratio prior and therefore cannot independently establish low-to-high semantic organization. R/C remove that prior and undergo the same graph construction under a margin-preserving null. The controlled panel changes only earlier clues at the aligned target and compares unrelated edits. It tests context response, not frequency-caused cluster formation or information transfer.

## 3. Tested Hypotheses

H-base: broad links to frequent nodes are largely explained by high marginal rates. Disappearance after correction and similarity to the degree-preserving null support this explanation within the sampled corpus.

H-association: some links and groups persist after correction, on separate reference contexts and beyond the null. This supports common activation organization beyond those marginals, without identifying a semantic component or causal module.

H-context: fixed graph groups respond more to relevant than unrelated edits at far targets. Near/far effect differences are relocation sensitivity unless order/recency is separately eliminated. The three outcomes can differ; positive results are not required.

## 4. Rival Explanations

Keep marginal frequency, per-position sparsity, target token, absolute position, source/text type, template, neutral-block order and numerical execution shape as separate rivals. Token/position strata assess some observed alternatives. Reliable text-type labels and original document/sentence units are missing for the DCLM cache; these gaps remain. High frequency and high degree alone do not establish reusable basic semantics.

## 5. Data Construction And Provenance

The main reference reuses the exposed DCLM VAL cache of 10485760 eligible same-token positions. It is not sealed TEST. Original D/V assignments are within-bin review blocks. Select 512 of 16384 dictionary IDs uniformly without replacement with seed 2026102603; select 64 complete contexts per original side with seed 2026102604. Keep all eligible positions. This fixed subgraph does not guarantee inclusion of the globally highest-frequency nodes; O retains its complete universe and hubs.

Original document IDs and verified sentence boundaries were not preserved. Use 2000 whole-context bootstrap draws only as **descriptive sensitivity intervals**. They do not satisfy a document/sentence confidence-interval qualification. Separate-context V reconstruction is not a guarantee of independent documents, near-duplicate freedom or a fresh blind holdout. No punctuation heuristic silently repairs that gap.

The controlled panel contains 12 new basic scenarios, six word-sense and six explicit person-role cases, each A/B semantic clues × near/far plus one unrelated weekday edit U per distance: 72 planned texts. All are constructed natural language and controlled edits. Freeze S01–S03 and R01–R03 as six whole cases/36 inputs; the other six cases/36 inputs remain NOT RUN for budget reasons. Realized lengths are 83–89 tokens, near gaps 6/7 and far gaps 50–55. Each case matches target token, final length, target position and final five tokens across all six versions. Moving the neutral block still changes clause order and recency. The [text execution selection](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/execution_selection.json) records exact IDs and hashes.

## 6. Task And Permitted Supervision

There is no learning task. Natural-reference statistics and predefined clue meanings are permitted analysis labels. Candidate next tokens are fixed before model responses. Word-sense candidates indicate compatibility, not a unique correct continuation. Earlier positions use only their own visible prefixes. The two displayed inputs are fixed as S01_A_far and R01_A_far before activations; do not replace a failed example with an attractive one.

## 7. Frozen Model, Dictionary And Interface

Reuse Qwen3-0.6B Base and final A22 F16384 CrossCoder. Model SHA256 is `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; dictionary SHA256 is `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`. Inputs are zero-based blocks 1,3,…,27 residual-post tensors at the same token, before final global norm. Restore saved TRAIN centering/vector RMS, BF16 Base SDPA, BF16 coder GEMMs and FP32 state/scores. The strict saved score threshold is 0.051281172782182693; it is not per-token Top256.

The encoder produces one shared z. For layer l, native contribution magnitude is \(z_f r_l\|D_{lf}\|_2\), with TRAIN vector RMS \(r_l\); centering and decoder bias remain separate. The concatenated native magnitude is \(c_f=z_f\sqrt{\sum_l(r_l\|D_{lf}\|_2)^2}\). Preserve z, layer contributions, absolute c and c divided by the actual concatenated hook norm. None is an independent layer activation, explained variance or evidence of layerwise generation. E16 and CrossCoder IDs are not aligned. See [asset audit](asset_audit.md).

## 8. Objective And Optimization

No optimizer, loss fitting, checkpoint selection or parameter update occurs. Decoder geometry, normalization, sparsity gate and model remain fixed. The offline binary graph is unchanged by retaining continuous-z first/second moments for later scaling. A zero discovery RMS is unestimable, not replaced by an invented scale.

## 9. Conditions, Seeds And Frozen Candidates

O preserves its original support and frequency rules. R searches all ordered pairs of the selected IDs with nA,nB≥200, nAB≥20 and P(B|A)≥0.8. C searches all supported ordered pairs with deltaP≥0.05; it is not restricted to O/R edges. R/C omit O's reverse-conditional and frequency-ratio gates. Positive marginal-rate quartiles and ratio≥4 are post-group descriptions, never clustering features.

For each graph, symmetrize admitted directed weights by maximum: conditional probability for R, deltaP for C. Use deterministic dictionary-ID order, NetworkX greedy modularity, resolution 1 and minimum group size 3. Save isolated and unclustered nodes. D defines groups; reconstruct V with the identical algorithm. Best V-group Jaccard≥0.5 is the operational membership-replication threshold, not a universal semantic criterion.

## 10. Primary Metrics And Frozen Analysis

**Frequency organization.** For every stable D group, compute mean pairwise absolute log-frequency difference using V rates. Each member needs at least 200 V hits. Average qualified stable groups equally. Missing groups/statistics remain NA. Fixed D-group V cohesion averages deltaP over all ordered non-self pairs; incidental feature-ID ordering cannot choose a direction.

Run 199 degree-preserving null draws in four chains (50/50/50/49). Exact binary 2×2 switches preserve every selected-feature count and every position's selected degree. Unselected columns remain unchanged, so all full-dictionary counts and per-position L0 are also preserved. Each chain starts from a copy of the same observed matrix, burns 10E proposals and spaces draws by 2E, where E is the selected matrix's nonzero count. Rebuild R/C and rerun the complete clustering and V-match pipeline on every draw. Require burn acceptance≥0.01, four split-Rhat values≤1.10 and at least 180 finite statistics. Check D/V overlap and squared cooccurrence mass. Lower-tail MCMC p-values receive BH correction across R/C; they remain conditional descriptions because document/sentence qualification is absent. No added draws on failure. The entire offline run has a 1800-second ceiling, including extraction and intervals; save partial output on timeout.

**Far context response.** Freeze each graph's union of D groups replicated on V with adequate V support before new controlled responses. Scale each member's c by its D contribution RMS, obtained from saved D z second moments and fixed decoder geometry. For each complete base case/distance, E is the member RMS of B−A and U is the member RMS of unrelated−A; the relevant-minus-unrelated contrast is S=E−U. Compute absolute and hook-norm-normalized versions separately; do not infer absolute change from a ratio.

The two primary endpoints are far S for the R and C unions. Use six basic cases as blocks, one-sided exact sign-flip tests and 2000 case-bootstrap draws. Take the maximum of the absolute and normalized p-values as an intersection test, then apply BH2 across R/C. Support needs q<0.05, all six case contrasts available, positive interval lower bounds in both versions, at least four effective cases, both relation types represented, and at least four of six positive directions. Missing/failed cases are not silently dropped to create a smaller passing test. Empty group unions or unmet guards are insufficient. Per-group, per-target-type and near/far differences are descriptive; three cases per relation have limited exact-test power. Output candidate differences are auxiliary and do not prove feature-level understanding.


Effective-case support uses the absolute D-RMS-scaled semantic effect >1e−4 for both representations. The hook-normalized effect has no separate same-number cutoff, since its units differ. Here absolute means the original contribution before hook normalization, still divided by its fixed D RMS; unscaled native c is recoverable from saved z and decoder geometry.

## 11. Secondary Metrics And Measurement Guards

Report low→high edge count/fraction, frequency-ratio≥4 edge fraction, high-frequency nodes adjacent to multiple communities, R edges retained by C, C edge replication on V, support counts and hit-context counts. Repeat the same graph descriptions in each null. Adjust observed conditional association against within-stratum independence for the 20 most common D token IDs plus OTHER, absolute position bins 0–31/32–127/128–511/512–1023, and joint strata. Text type remains MISSING.

Descriptive token projections save all positive shared-z coordinates per token. Separate intensity, frequency and community colors. Contribution-coordinate cosine and active-node overlap are descriptive; near-zero vectors give NA. Shared features at different positions are not information transmission.

The forward gates are fixed: cache replay relative z L2≤0.02 and support Jaccard≥0.95; eight visible-prefix checks additionally require relative h error≤0.01; identical-condition replay maximum z error≤1e−6. Target raw-hook NMSE pooled across measured targets/layers must have mean≤0.30 and p90≤0.50, with finite outputs. These are delegated conservative measurement guards, not semantic scores. A guard failure is retained and stops remaining panel execution; it cannot be repaired by a tolerance change.

## 12. Known Good, Bad And Confusing Cases

Artificial tests cover exact counts, a high-base-rate raw edge removed by delta correction, conserved row/column margins, actual switch movement, immutable input copies, identical chain starts, Rhat drift, zero-group NA, empty-edge intervals and token-stratum explanation. Synthetic data establish implementation properties only. Earlier R01 positive bank/f6401 is exposed E16 evidence, not a CrossCoder confirmation. R02's E16 prefix failure is retained but is not automatically a verdict on this different dictionary/interface.

## 13. Scientific Procedure And Stage Contracts

1. **Freeze:** align Anchor/Focus, this Protocol, analysis code/config and text; save exact identities. No new R03 response is used to set choices.
2. **Offline graph analysis:** audit O without rewriting it; extract fixed D/V submatrices; produce counts, R/C, groups, intervals, covariate checks and all null draws within 1800 seconds. Do not run a parallel large model experiment.
3. **Cache qualification:** two original contexts, each one Base forward, compared to original shared-z cache. Failure stops before the controlled panel.
4. **Panel qualification:** run all six versions of the two fixed display cases (12 inputs); run two same-condition replays and eight fixed visible-prefix checks. Controlled inputs use Base batch 1/right padding to 256, with padding excluded from distance/counts; coder batches stay 1024 positions. This changes the old Base batch 16×1024 shape and therefore needs current qualification. Eight checks are finite coverage, not a proof of every token's independent replay.
5. **Remaining panel:** only if all prior guards pass, execute the other four cases/24 inputs. Recheck target reconstruction over all measured inputs. Maximum cost is 2+12+2+8+24=48 calls. Attempts are charged before model execution.
6. **Report:** retain failures and NOT RUN cases; produce original/corrected graph comparison, two fixed token projections with a counterexample, group near/far responses and bounded candidate names. Name from sorted D contexts' first 32 only; the other 32 and already-used V contexts provide descriptive checks, not fresh blind validation. Multiple members, multiple contexts and boundary examples are required; insufficient evidence gives “mixed” or “uninterpretable.” Do not name a basic semantic component from frequency.

## 14. Algorithms, Outputs And Provenance

Execution owner: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/`. Exact algorithms are `offline/coactivation.py`, `offline/switch.cpp`, `offline/proposed_config.json` and `run_forward.py`; root freezes their hashes with text and this Protocol. `offline/statistical_plan.md` supplies the readable detailed contract. Raw matrices, CSR, logits, continuous moments, all null draws, per-token activations, failed gates and call ledger stay execution-side. Canonical Summary/Detailed and selected figures/tables link exact origins and hashes; actual reusable outputs receive registry IDs. The Protocol is not rewritten after results.

## 15. Supporting, Weakened And Insufficient Outcomes

Links that disappear after correction and resemble the margin-preserving null support the baseline-rate explanation in this corpus; they do not show lack of semantic function. Corrected links that persist across the stated separate contexts, strata and null support bounded coactivation beyond those marginals; missing document/sentence qualification limits population confirmation. Stable far relevant-minus-unrelated responses support context dependence under these inputs. Relocation differences with order still confounded support only relocation sensitivity. Low support, poor null mixing, unavailable units, failed reconstruction/prefix checks, absent groups or incomplete cases each receive their own insufficient/eligibility label.

## 16. Cannot Claim

No frequency-caused cluster formation, verified expert division, causal module, replacement efficacy, learning gain, semantic parent/child relation, universal semantic height, pure distance effect or layerwise generation follows. O's frequency-imposed DAG and C's possible cycles are reported as graph facts. G02/G04 remain auxiliary response-difference groups in another dictionary; they are never renamed as coactivation communities.

## 17. Authorization, Freeze And Amendment Ledger

The current user request authorizes bounded read-only execution and routine local records; operational parameters are delegated choices. Root's pre-analysis receipt owns the exact freeze time and hashes. The A–G self-audit in [internal audits](internal_audits.md) checks consistency without inventing individual human approvals. Record amendments append-only, before dependent work where possible. Stop on a consequential object change, exhausted parent budget or unavailable matched assets; complete independent offline work and report concrete gaps. Do not expand the cap, retrain, change algorithms to improve figures or launch an intervention. At delivery, give exactly two bounded updates and one next question, with scientific acceptance still Unknown.
