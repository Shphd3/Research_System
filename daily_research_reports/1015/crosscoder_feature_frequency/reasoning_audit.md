# Reasoning audit: feature relation groups and frequency

[中文](reasoning_audit_cn.md) · [Protocol](protocol_draft.md) · [Assets](assets_checked.md)

**Assessment: the actual draft separates structure, frequency similarity and learning benefit, and addresses phi bias with a full-pipeline random baseline. It is suitable for discussion within its stated limits. Complete H1, method qualification, scientific approval and execution approval remain unresolved.** All new statistics, figures and learning results are `NOT RUN`. This audit grants no `PASS` and does not confirm the researcher's question, thresholds or conclusions.

## Scope and sources actually read

Reviewer: Codex subagent `/root/anchor_protocol_audit`, 2026-10-15, Asia/Shanghai. This review applies [research-reasoning-auditor](../../../.agents/skills/research-reasoning-auditor/SKILL.md) and its reasoning audit contract to the actual Chinese Protocol. Sources read were that Protocol, the Chinese asset inventory, the received Anchor v0.1, the initial execution prompt and the [subsequent integration prompt](sources/PROMPT_报告与绘图整合要求_先写Protocol.txt). The Chinese draft is the reviewed source; this is not a claim of an independent line-by-line audit of its entire English translation.

The subsequent prompt names a report v0.2 whose body was not supplied. It was not read or checked. This review did not load checkpoints, scan CSR payloads, generate counts, encode inputs, plot, run swaps/statistical tests or search literature. Asset facts refer to the same-round inventory and its receipts, rather than implying a new independent payload inspection by this reviewer.

## 1. Hypothesis names and inference chain

Use the revised names consistently: **H1a concerns co-occurrence structure and replication; H1b concerns frequency similarity within groups. Both are necessary for the revised H1. H2 refers only to future learning benefit from input assignment.** The Anchor's original H2 may appear only as a historical correspondence, not as the name of the current frequency endpoint.

The actual chain is: activation events of a fixed dictionary at input positions → positive relations beyond marginal background → candidate groups formed without a direct frequency-distance objective → evaluation of membership replication and within-group frequency on the other side → inspection of input coverage and overlap. This can supply candidate assignments for later work. Predictive loss, capacity, expert specialization and sustained learning still require a separate empirical bridge; the draft does not substitute a structure graph for that evidence.

Future H2 still needs researcher choices about the learning object, assignment rule, K, expert capacity, exposure, budget, low-frequency definition and overall-loss noninferiority margin. Failure to support H1 does not logically rule out a separately motivated frequency-based H2.

## 2. Facts, proposals and design blockers

| Category | What the current records support | Unsupported upgrade |
|---|---|---|
| Asset facts | A final 14-layer/F16384 dictionary and complete sparse cache exist; they are not the 0.5B or full 28-layer/F32768 variant. Cache N=10,485,760 and nnz=2,669,034,642 | Access is not a new load test, complete payload rehash or scientific qualification |
| Sides and denominators | N_D=5,238,097 and N_V=5,247,663, summing to 10,485,760; 81 existing blocks and 10,249 contexts | Do not write equal half sizes or call contexts/blocks documents |
| Encoding | Training uses BatchTopK with average budget 256; cached inference uses the saved TRAIN gate, with mean L0 about 254.54 | Do not claim exactly 256 activations per position or whole-window numerical invariance from a small check |
| Proposed design | Phi bias, bounded mutual-neighbor graph, one grouping method, matched controls and pipeline null are specified | A specified method is neither an implemented qualified method nor a result |
| AI proposals | q=10, q=20 sensitivity, modularity γ=1, at most 128×32 positions per side, B=99, Holm α=0.05 and 1000 bootstrap repeats | These are not automatically frozen or executable |
| Independence gap | Both sides have been inspected; original document, near-duplicate and source mappings are incomplete | Relabeling, repartitioning or sampling an existing cache cannot create untouched document confirmation |

The evaluation side denotes a separation of algorithmic roles, not an untouched confirmation set. Observations are positions; independent uncertainty units should be documents/duplicate groups. Current context/block intervals require an explicit, unverified block-independence assumption.

## 3. Inference problems already repaired in the actual draft

**Frequency is not an exclusive category probability.** The draft defines events and denominators, separates frequency from amplitude and decoder norms, and does not multiply sample size by the 14 observed layers.

**Phi-based grouping is not frequency-neutral grouping.** For 0<p_i≤p_j<1, the positive upper bound is sqrt[p_i(1−p_j)/(p_j(1−p_i))]. The draft uses this to explain the equal-frequency preference and requires null repeats of support filtering, relations, graph construction, grouping, matching and both endpoints. Ordinary random groups and group-mean matching cannot replace that algorithm-bias check. Large lift for a rare feature is not treated as sufficient evidence.

**Validation cannot repair membership retrospectively.** D determines the candidate pool and parameters; V evaluates them. Zero V counts cannot justify deleting members, adding epsilon or selecting better-looking groups. Mean matching uses D means, avoids exact memberwise frequency matching, and does not select controls using V. Control membership and sampling rules should also be frozen before V effects are evaluated.

**Sample nulls cannot certify the full graph.** Existing full counts support description and discovery. Bounded S_D/S_V must rediscover groups and repeat the complete process. Their null calibrates only that sampled process, not the full graph, all edges or independent-document H1. Sampling depends on position identity, not features or a desired result.

**Replication is more than one attractive number.** T_a matches non-singleton groups one to one, counts unmatched discovery groups as zero, and accompanies this with group counts, coverage, largest-group share and held-out relation readouts for frozen discovery groups. One giant group or many singletons cannot be packaged as useful grouping. Fixed-group bootstrap is not called rediscovery stability.

**Common features are not defined through self-inclusion.** Disjoint communities do not literally share members. Common instead refers to features appearing in inputs associated with several groups. When a feature contributes to a group's hit rule, its own score contribution is excluded for that diagnostic. Unique, multiple and no-group coverage use all valid positions; top-1 assignment is not forced to hide overlap.

## 4. Revisions raised in this audit and rechecked

1. **The V-side domain of phi: revised.** Freezing P does not ensure 0<p_i<1 in V. The revised draft retains zero/always-active members and missingness flags, prohibits 0/0 and retrospective pool reduction, and records unestimable relations and group/overall coverage loss.
2. **Undefined null endpoints: revised.** A null without nontrivial or estimable groups can leave T_b undefined. The revised draft prohibits zero filling, discarding such draws to reach B valid draws, and selective rank p values. A shared observed/null estimability and coverage rule must be fixed first; failure makes H1b calibration insufficient.
3. **MCMC and p-value qualification: revised.** Stable two-chain diagnostics do not prove uniform null sampling. The revised draft explicitly limits correlated draws to approximate conditional calibration, prohibits substituting ESS into the rank denominator, and makes no claim that Holm has guaranteed nominal FWER. Mixing and independence failures still block inference.
4. **Qualification precedes freezing.** Reliability and feasibility choices may use D, but must not be selected by V frequency effects or final p values. Qualification determines implementation/resource/mixing feasibility; it must not select favorable seeds, burn-in or B. Any inspection of V endpoints remains exposed and cannot later be called blind confirmation.

After the root agent made these first three revisions, this reviewer reread Chinese Protocol sections 4.3, 5.2 and 5.3 to verify them. Item four states the required execution order, not an observed violation. These repairs added no algorithms, experiments or execution scope. This audit is not a parallel scientific design. Text repairs do not establish implementation correctness; concrete coverage and qualification rules still need freezing.

## 5. Remaining blockers and permitted belief update

**Complete H1 remains blocked by independence.** Without identity-preserving original document/near-duplicate mapping, independent-text replication cannot be claimed. Current work can only inspect structure and frequency conditional on the cache and block assumptions. Source effects remain unresolved; neither remove every source difference as noise nor call it universal structure.

**Statistical execution remains blocked by qualification and pending decisions.** Minimum support/coverage, meaningful effects δ_a/δ_b, matching tolerances, input thresholds and null burn-in/spacing/budgets are not confirmed. Unestimable low-frequency members, invalid nulls, wide intervals or absent practical margins do not establish absence, support or meaningful non-support.

**Resources remain unmeasured for the new method.** B=99 entails 198 D/V random matrices and about 2.62×10^10 pair updates, plus swaps. Historical full-count timing does not qualify this null. Any later work must obey the approved small qualification scope and failure stop rules; removing a decisive control to meet a deadline is not a valid repair.

This audit updates only the assessment of the proposal: it now contains discussable repairs for known metric bias, sample extrapolation, member deletion and common-feature self-inclusion. It supplies no empirical support. The researcher should review parameters, scope and budget before deciding whether to authorize qualification. Future H2 remains planning only.

This review added only this bilingual audit pair. It did not change the Protocol, historical evidence or scientific state, and did not launch analysis.
