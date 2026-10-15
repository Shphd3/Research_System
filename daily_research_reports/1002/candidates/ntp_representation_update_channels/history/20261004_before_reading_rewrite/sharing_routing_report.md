# When to share and when to separate: from readable representations to useful routing

2026-10-03. Interim research report in the researcher-selected 1002 candidate location; not a final scientific report or formal project migration. [中文](sharing_routing_report_cn.md). The [Anchor](anchor.md) owns the current design; the [Protocol](protocol.md) owns exact comparisons and authorization.

**We now have a more specific account of when sharing or separation can help, but not a verified better MoE.** This round separates present routing utility, future learning allocation and finite-sample costs: input-predictable mean learning differences create specialization opportunities, while curvature, estimation noise and resource costs can favor sharing. Two completed old-cache analyses find routing information in several representations without stable gains over a strong FIT-fixed action. The full-input fitted linear router does not dominate lower-dimensional representations. SAE and spectral methods remain replaceable analysis tools, not an architectural winner.

A second conclusion is structural: **routers and experts may read different representations; experts can retain the complete causal input within a layer while specializing.** Different parameters, sample exposure, and update responsibilities can produce specialization without first dividing input coordinates into disjoint blocks. A smaller router representation must justify itself through decision quality and actual cost.

## Why move from prediction accuracy to selection utility?

Earlier work connected natural text, source updates, local displacements, and measured finite losses. It also found limited readability of responses across source samples. The missing application link was direct: after predicting more accurately, does choosing an action from those predictions actually reduce loss? Overall MSE can improve by correcting an offset common to every action while preserving exactly the same ranking. It can also decrease while reversing an important action ordering. The [mathematical companion](sharing_routing_mathematics.md) gives exact counterexamples.

Three evidence activities remain distinct: the original six-arm common/specialized architecture experiment; actual routing utility and its decomposition using existing S7 finite actions; and a new panel comparing decision information and finite routing within Dense, S7, and SALL at matched token milestones. Each has its own unresolved object. One positive result does not complete the entire argument.

## Sharing first requires a finite-utility comparison

An exact local comparison holds the new source at the same updated parameters, \(w+\delta\), in both shared and private arrangements. Old tasks use \(w+\delta\) under sharing and their original \(w\) under separation. With other computation and task weights fixed, shared-minus-separated risk equals the weighted sum of old-task finite loss changes. Equal source learning follows here from using the same update in both arrangements; it is not another empirical discovery.

This suggests a useful decision criterion: assess the finite net effect on other users, together with parameter-copying, computation, and future-adaptation costs. Gradient inner products are small-step approximations. Even gradient cosine 1 can accompany a finite step that helps the source and harms an old task because of curvature. Statistical pooling supplies another benefit: more independent observations can reduce estimation variance at the cost of sharing bias. The earlier [capacity derivation](capacity_mathematics.md) states that tradeoff. Repeated tokens cannot be counted as additional independent observations.

**Many harmed realized tokens do not necessarily imply a deployable separation rule.** When comparing CE without extra costs or joint capacity constraints, if the update lowers expected CE at every observable prefix, a router should accept it even though some subsequently revealed targets produce positive loss changes. In a binary CE example, 40% of realized events are harmed, yet always updating is the optimal causal rule. The hindsight oracle's lower loss comes entirely from knowing the answer beforehand. Thus a high harm fraction alone does not establish useful separation. The relevant quantity is expected cost under observable conditions, not grouping events only by their target-informed gradient signs.

## Completed test: select full-input residual experts without the target

Freeze fresh S7 at 33 billion training tokens (33B below denotes training tokens, not parameter count). The final Attention block first computes the common output \(a_0=W_0c\), where \(c\) is its complete 2048-dimensional input. Each of four source domains provides a fixed mean-gradient matrix \(M_d\). Its residual expert computes \(-\eta M_dc\). After selection, \(a_0-\eta M_dc\) passes through the native residual, MLP, normalization, and vocabulary head to obtain actual finite CE. No Attention follows this block, so the complete measured action table exactly supports token-conditional selection without another model forward pass.

This is a local forward test of fixed linear residual experts. The common output is inherited backbone computation, and the source matrices are gradient-constructed fixed actions; neither is a newly jointly trained nonlinear expert. Different tokens may select different matrices; that generally differs from applying one uniform parameter update. It is not yet an online-trained MoE. The model, step size, eight A/B source actions, four predictor families, and readout data were frozen. Router features use only causal token history, position, norms, and optional SAE, PCA, or random coordinates. SAE320 still requires the complete width-30000 encoder; it is not a cheap 320-dimensional layer.

A→B uses scores fitted for source A to choose a domain label, then scores the corresponding expert constructed from source B. B→A reverses this mapping. Mathematics is the FIT-best fixed domain for both sources. That control does not inspect readout targets, but it is selected from first-order FIT labels, so it is not guaranteed to be the best constant action under finite CE. Old R contains 1024 records with 16 fixed positions each. It was already exposed; this entire analysis is exploratory reuse.

The table retains every feature family and both primary source directions with **rejection disabled**. Units are \(10^{-6}\) nat per selected event. Positive gains favor the policy. Brackets show conditional 95% intervals from 2000 category-stratified, paired whole-record bootstrap draws. They exclude source-population uncertainty and have no multiplicity correction.

| Source transfer | Features | Gain over FIT-fixed expert | Gain over global usage-matched random | Gain over category-matched random |
|---|---|---:|---:|---:|
| A→B | Prefix baseline | 2.54 [-9.63, 12.63] | 5.96 [-6.03, 16.24] | 5.49 [-6.65, 16.02] |
| A→B | + SAE320 | 3.39 [-14.08, 20.48] | 22.99 [5.85, 40.29] | 5.25 [-11.38, 22.12] |
| A→B | + PCA320 | 2.68 [-12.92, 17.08] | 14.11 [-1.36, 28.97] | 9.02 [-6.44, 23.52] |
| A→B | + Random320 | 43.57 [11.71, 77.41] | 122.77 [88.27, 155.49] | 42.98 [12.30, 71.28] |
| B→A | Prefix baseline | -0.72 [-17.59, 14.97] | 12.08 [-4.61, 27.36] | 9.72 [-6.90, 24.75] |
| B→A | + SAE320 | -5.79 [-29.89, 20.42] | 57.40 [32.23, 83.97] | 16.58 [-7.11, 40.64] |
| B→A | + PCA320 | -8.90 [-28.77, 11.23] | 23.92 [4.03, 44.36] | 12.51 [-7.08, 32.13] |
| B→A | + Random320 | 6.41 [-36.23, 48.02] | 184.40 [140.41, 227.20] | 62.30 [25.27, 99.10] |

![Actual finite routing utility and controls](figures/cached_routing_utility.png)

[All 32 conditions across five receiving scopes](evidence/routing_utility.csv) also include within-source cases and action sets permitting no update; favorable cells were not selected. Rejection-enabled primary cells still have 99.92676%–100% update coverage. The main pattern therefore does not arise from broadly abandoning updates. Mean unchanged CE is 3.4370429761. The increments are small, no practical threshold is defined, and whether an interval crosses zero does not decide architecture adoption. [Execution and independent recomputation](evidence/routing_utility_audit.json) verified all 160 rows, selection order, pairing, and hashes.

## Does beating random assignment merely reflect coarse domain matching?

The global usage-matched comparator preserves a policy's overall expert frequencies but assigns experts independently of events. Beating it establishes an association between input and useful action; coarse domain or category information could produce that association. After observing the first results, a post-hoc decomposition was explicitly registered: preserve the policy frequencies within each domain or category, then randomize assignment within that group.

These controls use known group labels. They diagnose the observed mechanism; they are not new deployment rules. Global gain exactly equals “global random minus group random” plus “group random minus policy.” This arithmetic identity is not causal proof. The [complete decomposition](evidence/routing_group_decomposition.csv) retains all conditions and intervals.

For SAE, A→B global gain 22.99 becomes category-level residual 5.25, with interval [−11.38,22.12]. B→A falls from 57.40 to 16.58, with interval [−7.11,40.64]. Coarse category matching therefore accounts for most of these point gains under this comparison. It does not establish exactly zero residual or a unique causal explanation. Random projections retain residuals 42.98 and 62.30 with positive conditional intervals, so all representation-dependent utility cannot be attributed to coarse labels.

The fixed-expert comparison supplies a more direct limit. SAE A→B changes the expert on only about 4.99% of events. Multiplying the mean advantage on those events by their frequency gives total gain 3.39. B→A changes about 11.15%; those changed decisions are worse on average, giving −5.79 overall. More varied choices are not themselves success: the changed choices must improve outcomes. These are readings from a fixed, exposed panel, not a new generalization verdict.

## Further test: does a more complete router input improve useful choice?

**Purpose and hypothesis:** preserve full expert input and fixed actions while testing whether router observations a, preprojection c, post-residual x=r+a or their combination improve measured finite-loss selection. Rivals are finite fitting capacity, regularization and an already strong fixed action. Registered at 09:38, this cached analysis completed in 45.49 CPU seconds without loading or forwarding a model. Previously exposed R makes it post-hoc exploration.

The four actions use all of F-half0 and the original full-step scale. FIT is F-half1; both supervision and the fixed comparator use actual finite CE. Eight families share base389 (prefix/position features and c/a/x norms): six add 64 coordinates, with full (c,x) as a larger reference. Axes/atoms, scaling and ridge use FIT only. Compared with the A/B transfer experiment above, the bank, labels and baseline dimension change, so their numerical difference cannot be attributed entirely to input choice. The checkpoint and complete expert interface are preserved. These compare added coordinates: a-PCA64 retains the common base and does not literally observe only a.

The table retains all eight forced-action families. Units are micro-nats per selected event; positive gains favor the policy and intervals condition on the fixed fits, sources and exposed R. [All 80 rows](evidence/cached_router_inputs.csv) also retain zero-plus-four actions and four receiving domains.

| Input feature | Gain over finite-FIT-fixed expert | Gain over category-usage random |
|---|---:|---:|
| Prefix base | -116.57 [-171.50, -65.43] | 53.31 [5.96, 98.67] |
| + a-PCA64 | -9.32 [-57.94, 37.31] | 162.26 [119.28, 206.95] |
| + c-PCA64 | -4.88 [-56.56, 45.92] | 172.51 [126.48, 219.21] |
| + x-PCA64 | 13.94 [-35.76, 62.14] | 193.62 [147.92, 239.09] |
| + (c,x)-PCA64 | 6.05 [-45.02, 54.17] | 186.91 [140.98, 233.71] |
| + a-Random64 | -43.91 [-92.73, 3.51] | 112.06 [69.37, 158.07] |
| + SAE64 | -39.89 [-91.82, 11.40] | 128.76 [82.13, 174.84] |
| + Full (c,x) | -49.39 [-106.71, 8.49] | 195.14 [145.67, 246.48] |

![Router inputs against two different-strength controls](figures/cached_router_inputs.png)

**Available information and net adoption benefit diverge.** Every feature-added family beats category-usage random assignment under both action sets, yet none of the 16 pooled policies has a stable positive gain over the finite-FIT-fixed expert. That action is again the mathematics-source update, improving R by about 808.23 micro-nats on average: a strong input-independent strategy. A policy can be smarter than randomized allocation while still losing to always using this action. Allowing rejection does not change that conclusion.

Full (c,x) also does not dominate. Against this prespecified paired reference, x-PCA64 reduces policy cost by 63.33 micro-nats, with conditional 95% interval [9.33,119.60] under forced-four actions. All comparisons are retained without multiplicity correction. **More information does not imply a better finite-sample fitted learner.** A post-outcome diagnostic without refitting finds full-input contrast-error MSE rising from 5.151 on FIT to 16.035 on R, in units of 10⁻⁶ nat²; x-PCA64 gives 8.606 and 9.069. This contrast error removes the eventwise common error across four nonzero actions; it diagnoses relative four-action predictions and cannot alone explain rejection against zero. FIT is an in-sample diagnostic. The gap is consistent with estimation/regularization or FIT/R distribution differences, identifies no unique cause and does not establish that the raw interface contains less information. MSE itself still does not guarantee selection benefit.

The [execution receipt](evidence/cached_router_inputs_receipt.json), [independent reconstruction](evidence/cached_router_inputs_audit.json) and [post-hoc fitting diagnostic](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/cached_router_inputs_01/posthoc_fit_diagnostics.json) preserve labels, choices, transformations, record pairing and hashes. The frozen new-panel analysis was not retuned after these old-R observations. Even positive within-category residual utility can be error correction for a particular fixed gradient-action bank; it does not establish creation or retention of multistep expert specialization.

## Why compress the router while retaining complete expert input?

Let \(h\) be the complete causal vector within the layer. A valid computation forms \(z=\phi(h)\), selects \(e=\pi(z)\), then evaluates expert \(E_e(h)\). The router selects computation; the expert performs it. “Complete input” means the whole current-layer hidden vector, not future tokens or a guarantee that every detail of the original prefix survives. **The two inputs need not differ.** The same h can support distinct parameters, computations and update responsibilities; changing router observations is a design choice to test. Full input is relative to an expert interface: an MoE FFN can receive the whole hidden vector at its interface, including its prescribed normalization. The fixed Attention residual actions here receive complete 2048-dimensional c; r remains in the shared native tail, rather than being concatenated with c or the entire token history.

![Router information and complete expert input](figures/router_expert_information.png)

For fixed experts and an input distribution, lossless router compression requires a rule depending only on z that still chooses an optimal action at almost every complete state h. It need not reconstruct all of h. Conversely, a representation sufficient for predicting the target need not suffice for choosing experts: their errors may depend on another variable. In a multiplicative example, the router needs only sign S, while the expert needs complete numerical value C. Compressing the entire prediction to S prevents zero error. See the [derivations and counterexamples](sharing_routing_mathematics.md).

An architectural precedent already exists: X-MoE uses a lower-dimensional routing projection while experts process the full hidden vector. This establishes feasibility, not performance for the present causal NTP setting. [X-MoE, §§2–3](https://arxiv.org/html/2204.09179). DeepSeekMoE's shared and routed experts likewise do not require splitting input into common/residual coordinate groups. [DeepSeekMoE, §3.2](https://arxiv.org/html/2401.06066v1).

Identical available inputs can still support specialization because gating changes sample exposure and expert gradients. Router and expert parameters also receive different derivatives. Hard argmax without continuous weighting of the selected output does not give the discrete index an ordinary task gradient; its training estimator must be specified separately. The frozen ridge supervision here does not pretend to solve online router learning.

Complete expert input is a useful comparison baseline, not a universal architectural theorem. Compression sufficient for the expert's own computation could work, but requires separate evidence. The serial form defines \(u=h+C(h)\). An expert can read its entire interface u, although u need not recover the earlier h; h and C(h) are not retained as separate inputs. Holding expert input fixed while changing router information reduces this confounding.

## Weak frozen-bank results do not settle learning allocation

Sharing versus separation also has a time dimension: selecting today's computations differs from allocating examples to train tomorrow's experts. In the fourth analytical example, two zero-initialized, bias-free linear experts have identical costs on every input, leaving no initial routing gain for any representation. A prescribed allocation by input sign, using conditional-mean gradients with \(0<\eta<2\), produces risk \(R_t=\tfrac12(1-\eta)^{2t}\), converging to zero. Both experts retain the full input.

The example deliberately restricts the function class, initialization, per-update balance and tie rule. It does not imply that standard MoE generally stalls or learns the proposed allocation. It establishes a narrower boundary: absent useful differences in a current expert bank do not rule out future specialization; future possibility does not validate an ineffective present selector. Frozen-action analysis locates local information and selection problems, while the architecture training independently tests subsequent acquisition and retention. [Full derivation](sharing_routing_mathematics.md).

The fifth derivation gives a broader local relation: from common initialization, small-step SGD with equal conditional learning rates gives private copies a first-order risk advantage equal to the variance of group-conditional mean gradients times the step size. Copies are free and estimation error is excluded, so separation does not universally win. The relevant object is **mean learning differences predictable from the input**: opposing gradients revealed only after the target need not support routing. Full input may contain allocation information; SAE and spectral methods attempt to read or compress part of it. Current empirical results do not estimate this population coefficient. [Mathematics and precise conditions](sharing_routing_mathematics.md).

Round six puts the opportunity and costs in one finite-sample model: with the same data, conditional step and common quadratic curvature, the expected advantage of splitting equals the benefit from mean-demand differences minus finite-step curvature and noisier group estimates. The same genuine differences can favor sharing with few samples and splitting with more. Independent enumeration verifies this conditional derivation; the current NTP work does not estimate its quantities. A fuller decision asks whether **input-predictable learning differences outweigh estimation error, update size and resource costs**. [Derivation and examples](sharing_routing_mathematics.md).

## Which information gap does the new panel test?

The new task uses exact 33B checkpoints of Dense, fresh S7, and SALL, with 256 source-A, 256 source-B, 512 FIT, and 1024 DEV records. Records and complete token strings are disjoint within the new panel; TEST is unopened. Cross-panel auditing found four exact text/prefix matches with the old panel: two new source-A records and two new FIT records, none in new R. The two entire panels are not fully independent, and article-level near duplication remains Unknown. All three have Dense LM backbones, with different training objectives and continuation histories. Cross-model comparison is descriptive replication.

Within each model, four domain mean gradients and their raw common mean are independently normalized to relative weight displacement 0.001. The common update is replayed directly; averaging four losses cannot substitute for it. With complete expert input and the native tail preserved, comparisons add 64-dimensional PCA of a/c/x/(c,x), a 64-dimensional random projection of a, or 64 SAE atoms to the prefix baseline, alongside a fixed full-(c,x) linear learner. FIT supervision uses measured finite action losses, with cross-source selection primary. Here \(a=Wc\) and \(x=r+a\): the comparison tests preprojection and residual information. Full (c,x) remains a finite-sample fixed learner, not an unrestricted optimal router.

The [registration](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/probe_33b_registration.json) precedes new forward passes. Separate [execution](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/probe_execution_freeze.json) and [analysis freezes](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/probe_analysis_freeze.json) record code, data, model identities, and comparisons. Qualification checks native forward computation, local gradients, temporary perturbations, and complete weight restoration. CPU implementation tests do not replace GPU numerical qualification. A 09:22 pre-execution interface review repaired SALL sequence-container equivalence and scheduler termination cleanup; the [amendment receipt](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/preexecution_amendment_01/amendment.json) preserves originals, 33 CPU regression checks and the unchanged scientific recipe.

<!-- NEW_PROBE_RESULTS_START -->
At the 10:44 UTC live check, `pt-meoxfrko` remained STARTING / worker Pending, with no real GPU qualification or new-panel values. Results remain NOT RUN; missing observations are not zero effects or expected winners. The [job ledger](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/job_ledger.json) and timestamped execution receipts govern subsequent state.
<!-- NEW_PROBE_RESULTS_END -->

## Evidence for faster loss reduction and better downstream performance

![Training CE and differences from Dense over 20–33B exposures](figures/training_curve_20_33b.png)

The plot retains all 130 consecutive 100M-valid-target bins from 20B to 33B, giving 390 model/bin rows. Boundary updates contribute their logged mean loss in proportion to token overlap. Fresh S7 is lower in 125/130 bins and SALL in 97/130; adjacent bins are not independent repetitions. Correct continuation lineages exclude discarded old suffixes, and vertical lines mark Dense/SALL continuation starts. The [complete curve table](evidence/training_curve_20_33b.csv) and [provenance](evidence/training_curve_20_33b.json) preserve original line ranges. These are pre-update training-batch LM losses, not fixed checkpoints evaluated on one common held-out set.

Recomputed logs show fresh S7 training CE below Dense by 0.003442 nat over 20–22B tokens and by 0.002349 over 31–33B. SALL moves from 0.007305 below Dense in the earlier window to 0.000524 above in the later window. This uses pure LM CE weighted by valid tokens, not total objectives. Twenty adjacent 100M-token blocks per window are not twenty independent seeds. The actual later sampling has now been checked: 99.8780672% of valid target positions overlap between Dense and fresh S7 in the 31–33B window, but updates are not paired. Thirteen of 15 prespecified updates have disjoint global sample-ID sets; all 30 historical rank-0 input digests were reproduced. Similar window data do not imply that identical batches were learned at identical parameter states. SAE cannot receive causal credit for the entire difference, nor does this audit estimate how much the sampling differences explain. The [sampler audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/sampler_pairing_audit.md) preserves the conditions. Lower training CE is descriptive evidence, not proof of reaching a quality target with fewer tokens, FLOPs, or seconds.

The completed 21B N8 domain-classification probe places fresh S7 1.375 percentage points above Dense, but the 97.5% paired interval is [−0.125,+2.876] points and the old test was exposed. It measures information readability. Old 10B held-out M2D2 records offer a contrasting observation: SALL had slightly lower training loss but held-out CE about 0.006185 nat above Dense. That historical S7 used λ=1 and must not be conflated with fresh λ=0.1. A bounded search found no general downstream benchmark table tied to the three current exact-33B identities; it does not claim none exists anywhere.

The [training and downstream evidence inventory](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/training_and_downstream_evidence.md) preserves source log rows, token coordinates, lineage, actual results, and hashes. It also corrects an outdated-ledger reading: although the old Detailed still labels the 21B probe NOT RUN, terminal receipts establish completion. Recording that fact does not revise a formal scientific verdict.

## Remaining claims and the next decision

The main gaps are narrower. Local selection must improve on strong fixed/common computation. Compressed routing must yield repeatable selection utility while preserving expert computation. An MoE claim needs joint expert learning with source acquisition, retention, and resource costs. Downstream utility requires its own task endpoint. These are evidence requirements for different claims, not a mandatory serial experiment checklist.

The two queued jobs each address only part of the empirical bridge:

| Job | What it actually tests | What remains unanswered |
|---|---|---|
| pt-uasnh61d | Small-model acquisition, retention and cost under known-domain assignment and shared/private, serial/parallel structures | Learning routing from causal input and general downstream improvement |
| pt-meoxfrko | Input information and finite-action choice at fixed Dense/S7/SALL 33B states | Long-term gains after joint router/expert training |

Even if both jobs subsequently complete, learning a better router remains a distinct empirical bridge. A direct follow-up (AI suggestion) would preserve full expert input, initialization, data and explicit resource coordinates while comparing a trainable causal gate with strong fixed allocation on learned acquisition/retention. SAE need not be selected first. No new execution contract or submission is created here.

**Provisional AI assessment:** The direction has reasons to continue: descriptive lower-training-CE feedback and pre-target action information beyond coarse category matching. The strongest limits are that this information has not become stable gains over a strong constant action, and the same rule has not been shown to improve multistep expert learning. The specific opportunity is learning allocation and finite-sample estimation, rather than treating SAE or spectral structure itself as an architectural result. Adoption and practical-value judgments remain with the researcher.

**AI suggestion:** use the new panel to locate the bottleneck. If no representation beats fixed/common actions, inspect whether the candidate experts offer stable useful differences. If full (c,x) helps but a does not, investigate available-information differences while retaining dimensionality, regularization and fitting error as rival explanations. Similar low- and full-dimensional results require comparing estimation error and actual cost, not declaring sufficiency. Read acquisition and retention from the existing architecture comparison independently, without requiring the local selector to win first. Local routing results inform whether this particular selector merits an online-learning extension. Ordinary projections must not be ignored to preserve an SAE narrative.

**A more direct learning comparison (AI suggestion):** prioritize the existing `common_parallel` versus `private_active` contrast. Within a seed/order combination, it matches the initial function, activated FFN width, full expert input and data sequence, while tying a common channel across domains or copying it privately. Total parameters differ, and tying changes update frequency and optimizer history; acquisition, retention and cost must be read together. Known-domain routing remains privileged information, so the comparison cannot itself establish a better learned router. The [story audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/story_gap_audit_round5.md) specifies the reading scope.

Costs must remain concrete. A residual-expert multiply costs about 2.097 million MAC; the width-30000 SAE encoder costs about 30.72 million, before TopK. A 64-dimensional linear PCA followed by five linear scores can fold into a direct gate. Lower dimensionality therefore does not itself prove computational savings. These are operator counts, not throughput measurements. Architectural potential rests on better deployable choices at lower actual cost, not the representation's name.

<!-- EXECUTION_STATUS_START -->
This window submitted `pt-meoxfrko` at 08:11 and retained the earlier `pt-uasnh61d`. Both use 8×RTX5090 SPOT, conservatively consuming two of the five permitted allocations. At 10:44 UTC both remained STARTING / worker Pending, without real GPU qualification or a training step; scheduling and completion ETA are unknown. Completed work comprises cached routing utility, group decomposition, the eight-family input comparison, training curves and sampler verification, six rounds of conditional derivation, and independent recalculation. No new MoE training or downstream improvement is established. No duplicate submission, resource substitution or frozen-budget reduction occurred.
<!-- EXECUTION_STATUS_END -->

The direct update is that **sharing must be evaluated through actual utility under observable conditions; routing information is defined by differences between experts; experts may retain full input.** We now have a more discriminating research object and two executed local utility comparisons. Architecture adoption, practical thresholds, and scientific question closure remain researcher decisions.

[Continuing process](research_process.md) · [Previous capacity report](capacity_report.md) · [Execution directory](/data/250010109/MoE_Router/experiments/20261003_sharing_routing)
