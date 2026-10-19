# Co-occurrence groups and bounded learning: execution Protocol R1

Date: 2026-10-16 Beijing. Processor: Codex /root. [Chinese companion](protocol_cn.md).

This run tests whether co-occurrence groups contain information beyond frequency, and whether their fixed input allocation helps low-frequency conditional next-token prediction at equal expert capacity and exposure. Structural evidence, learning utility and a local update mechanism are separate claims.

The researcher explicitly authorized drafting, self-auditing, repairing and executing this task without intermediate approval. Scientific interpretation and closure remain researcher-owned. The preceding complete H1 was INSUFFICIENT. Its results remain intact; all repairs below are post-observation exploratory supplements, not retrospectively registered confirmation. The received [Anchor](sources/02_ANCHOR_关系分组到学习验证.md) and [execution request](sources/03_PROMPT_交给现有Agent自主执行.txt) own the requested design. This run creates no parallel scientific design or Focus transition.

**Actual execution freeze R1.8.** The initial design and provisional budget below remain historical; [timestamped amendments](execution_amendments.md) identify every repair. Actual TRAIN:130712 positions/128contexts; EVAL:523136 positions/512contexts. Fixed low/high lists each contain3916 features, EVAL support threshold20. Each arm runs12 drop-last epochs=6120updates=1566720 valid-target exposures. Save/evaluate at0/510/1530/3060/4590/6120; midpoint3060; virtual SGD lr0.1. The primary paired2000-draw interval uses four consecutive contexts per block and fixed-feature ratio linearization, not independent documents. The exact execution config is config/formal_R1_8.json under the run root. Initial caches/configs remain intact.

## A. Questions, rivals and decisions

H1a predicts that D/V group matching exceeds a binary row/column-margin-preserving null after repeating support selection, phi, mutual-neighbor graph construction, community detection and scoring. The rival is that marginal frequencies and the selected pipeline alone produce apparent replication.

H1b predicts lower V within-group log-frequency dispersion than equally sized controls with D mean log-frequency matched within 0.1 dex. The rival is phi's preference for similar margins. Missing groups do not count as zero effect or disappear from the estimand.

Exploratory H2 predicts that relationship allocation R beats both frequency allocation F and matched-random allocation N on a fixed low-frequency feature-equal conditional loss, without materially worsening overall loss. Load, exposure, frequency composition, initialization and generic specialization are live rivals.

A local midpoint intervention changes which inputs update the same expert while holding expert token counts fixed. Raw and per-expert norm-matched virtual SGD updates distinguish local direction from magnitude effects. This intervention does not establish a full training trajectory or every root cause.

## B. Frozen inputs and split roles

Use Qwen3-0.6B-Base revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd and the final14/F16384 CrossCoder checkpoint_000999997440.pt, SHA256 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628. Both stay frozen. Sources are one-based decoder blocks 2,4,…,28, residual-post before final RMSNorm; one shared latent is computed jointly from all sources. Original TRAIN CenteredRMSStats and the fixed EMA norm-weighted threshold 0.051281172782182693 remain unchanged. No inference batch top-k or sequence normalization is allowed.

Selected model, tokenizer, data, CrossCoder and saved representation IDs passed the [current strict access check](../../../assets/checks/2026-10-15_crosscoder_relation_learning_inputs.json). Access does not qualify numerical correctness or scientific eligibility.

Structural D/V reuse the exposed VAL cache: 5,238,097/5,247,663 eligible positions. Original document/near-duplicate identities are unavailable; this is not independent-document confirmation. q10 is primary and existing q20 is sensitivity only.

Learning TRAIN/EVAL use fixed nonoverlapping 1024-token context windows from original CrossCoder TRAIN sources, planned at 128/64 contexts. Exact file identities, offsets, exclusions and final counts are frozen in the cache manifests. They do not overlap the structural VAL source file. CrossCoder was trained on this TRAIN origin; document independence remains Unknown. Therefore learning is exploratory within-distribution evidence. Position t consumes its prefix through t and predicts the true token t+1. Exclude context-final positions and special current/target IDs identically for all arms.

Cache raw terminal residuals, true targets, three fixed routes, full positive-feature CSR and context/source offsets. Never truncate the feature list. Caching removes frozen-base forward cost, not the true vocabulary objective. A native end-to-end check compares the original model's logits with the cached residual through the frozen native norm/head, in addition to exact zero-adapter invariance and prefix/future-alteration tests.

## C. Structural repair

Preserve the preceding strict-log endpoints. Matched controls sample groups uniformly conditional on size and D mean log-frequency within 0.1 dex. The initial implementation uses random-slot exact heat-bath updates, including self-loops: choose uniformly from all legal replacement members, never filter draws by V. Two independent chains, burn-in 50 times group size, spacing 5 times group size, 100 draws per chain; small enumeration, between-chain diagnostics, Rhat/ESS and membership turnover qualify the sampler. Exact small-group accelerations and any budget changes are recorded in append-only execution amendments before the affected endpoints.

Cover all 186 original nonsingleton groups and 13,807 members. Report group-equal and member-weighted summaries and size strata. Unqualified groups retain missing endpoints and explicit coverage.

The binary null reuses 128 contexts times 32 positions per side. Preserve every row L0 and feature column hit count. Use fixed proposal counts including rejected self-loops, two chains, burn-in 32 times nnz and spacing 4 times nnz. Rerun the entire pipeline per retained draw. Target B99 follows runtime and mixing qualification; a reduced budget must be recorded before new endpoints with actual B and minimum resolution 1/(B+1).

The frozen sampled support rules are at least25D hits and8contexts, pair joint count at least5. Full-cache rules remain100D hits/10blocks and joint count10. Each side uses estimable positive phi, mutualq10 and the same weighted greedy modularity community algorithm; retain singletons but score nonsingleton groups. Recompute qualification/graph/groups for each null. These values are from the16:40:36 registered configuration, not chosen from null outcomes.

The strict sampled log-frequency statistic remains undefined for a group with V zero counts. A new common exploratory statistic uses log10((nV+0.5)/(NV+1)) for observed and null matrices. It repairs a definition after seeing the original failure; it is not original confirmation. Stability is the one-to-one nonsingleton Jaccard match mean; dispersion is within-group log-frequency SD relative to matched controls. Null p-values require valid margins, qualified sampling and a defined statistic on every scheduled draw. Do not report selected-valid-draw p-values.

## D. Group definitions and fixed allocation

All arms use the same 13,807-member pool and the 186 original group sizes. R keeps real memberships. F sorts members by D frequency and fills the size multiset in deterministic order. N permutes original group labels within ten D frequency-quantile bins, exactly preserving each group's size and per-bin composition. Diagnose N's member/edge destruction before learning outcomes.

Every arm uses hit-only active-member fraction standardized by its D-only group mean and SD. A zero-SD group receives score zero. No-hit groups do not compete; all-zero positions use a fixed fallback. Ties use the SHA256 order of sorted group member IDs. The same D-only load-constrained assignment maps groups to K4 experts without EVAL targets or losses. Record discarded score mass, ties, never-winning groups, winner-size bias and actual TRAIN/EVAL expert loads/update counts.

Pre-learning amendment R1.1: raw mean-binary scores tied in 99.896% of F's D positions. Before any learning loss, all arms were changed once to the common D-standardized score. Preserve the original diagnosis; do not choose further scoring changes from learning winners.

## E. Learning contract and primary readouts

After the deepest CrossCoder source, before final norm/head, insert four biasless rank32 residual adapters: h'=h+U_e D_e h. Hidden size1024 gives 262144 trainable parameters total and 65536 active per position. Each expert receives the full hidden representation; no input position or common component is removed. Frozen base, CrossCoder, norm and head never update. Nonzero down and zero up give identical initial logits with useful up gradients.

Run R/F/N for paired seeds 20261016,20261017,20261018, sharing initial parameters, input order, loss weights, valid batch256 and optimizer settings. AdamW lr0.001, betas(0.9,0.999), eps1e-8, weight decay0, gradient clip1. Initial common budget is three epochs; a numerical/throughput-only smoke freezes the final common updates and immutable config before formal outcomes. No condition-specific extension. Full real-vocabulary next-token CE uses nat/token. Save initial, early, midpoint and final complete states and per-position EVAL losses.

Fix low/high feature lists using the 15666 D-reliable candidates (at least100 D hits and10 blocks), bottom/top25% by D frequency, feature-ID tie order. The lists are identical across arms and may include route-pool-excluded singletons; report routing coverage. Require20 EVAL hits per feature; count-based support is shared across conditions, with omitted and insufficient-support features explicitly listed. The primary metric averages CE over each low feature's hit positions, then averages features equally. Report high-frequency conditional and overall CE, baseline-to-end gains and token-aligned curves.

Practical low-frequency gain is0.01 nat/feature and overall noninferiority tolerance0.01 nat/token, fixed before outcomes. Explain scale using baseline context variation. Candidate support requires R to beat both controls by this gain, agree in direction in all three paired seeds and satisfy overall tolerance. Report negative, mixed, insufficient and tradeoff outcomes distinctly; intervals crossing zero do not prove no effect. Separate seed variation from paired context-block bootstrap; tokens are not independent inference units.

Persist required token-axis TensorBoard loss/progress tags, target counts, learning rate, gradient norms, resource use and data/forward/backward/optimizer/eval/checkpoint timings under the training observability contract. Checkpoints include optimizer/RNG/order/counters and explicit resume qualification. Register actual saved outputs before handoff, not merely intended endpoints.

## F. Local intervention and first-direction sensitivity

Use the fixed midpoint state,16 donor batches of256 and fixed512-position probes. Sampling depends on D frequencies/context/support, never measured benefits. Within bins of D mean active-feature log frequency, permute route labels, preserving expert token counts in every batch and bin. Report exchange fractions and ineffective bins.

Reset the checkpoint for each donor and each actual/exchanged update. Use one SGD step with no momentum/weight decay; probe routing stays original and no virtual state re-enters formal training. Numerical smoke starts at lr0.1, falling back to0.01 only when maximum relative per-expert parameter step exceeds0.05; freeze before benefit comparisons. A second version rescales exchanged updates to actual per-expert update norms; explicitly mark zero/unmatchable experts. Probe loss change is primary; gradients and cosine explain it. Run each arm. A shared effect cannot be attributed specifically to R.

Auxiliary: on a fixed D sample, compute the first right singular vector of each raw source H without centering, subtract (Hv)v^T, and feed all modified sources through the unchanged joint CrossCoder. First verify no-op reconstruction. Record layer energy removal, reconstruction, L0, frequency and fixed-old-edge/group changes; plot original/removed/difference shared-latent heatmaps with the same texts/features and common original/removed color scale. This direction is not established common semantics and does not create a second training matrix.

## G. Resources and delivery

Use envelope keys h100-4-reserved/shphd-lite-0911 in one allocation, parallel stages inside it, no additional quota. The management container exposes one H100 MIG and no reusable four-H100 running job was found. A single job therefore uses the explicitly authorized Reserved quota after checking four full H100s, occupancy, dependencies and BF16 kernels. Preserve unrelated8x5090 recovery jobs. Maximum6 hours/24 GPU-hours; idle25 minutes exits; no profile fallback or CrossCoder retraining.

Local structural CPU work has a60-minute wall ceiling. Measure before B99; parallelism may optimize computation but not change the statistic. Prefix leakage, native zero mismatch or invalid mapping stops the affected branch for implementation repair, preserving evidence; never replace the real task with synthetic evidence. Consolidate by07:30 Beijing for a readable08:30 report, or deliver earlier if complete. Partial work is uncompleted, not scientific failure.

Execution root: /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z. Code root: the same experiment's analysis_tools/relation_learning. Deliver a one-page Chinese brief, readable bilingual report, actual Protocol/amendments/audits, raw CSVs, at most five main figure types and plotting code, config/checkpoint/log locations and a change manifest. Interpret each decisive result through observation, rivals, distinguishing intervention, exclusions and remaining uncertainty. No skills edits, commits, pushes or scientific-state transitions.
