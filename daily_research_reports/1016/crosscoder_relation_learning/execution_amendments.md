# Execution amendments and freeze records

This record appends amendments without overwriting preceding results or the initial Protocol. All times are UTC; add eight hours for Beijing time. [Chinese companion](execution_amendments_cn.md).

## R1.1 · 2026-10-15T16:43Z · Pre-learning score repair

In the D-only allocation check, the original mean-binary score tied on99.896% of F positions and left151/186 groups never winning. No learning loss had been observed. All three conditions were changed to the same hit-only D-standardized score; D-only fitting and the common mapping algorithm remained unchanged. After repair, R/F/N tie rates were0.1007%/0/0 and all four D expert loads were approximately25%. The original version is preserved in execution `data/meanbinary_initial`. Mean winning group sizes still differ and must be reported; similar loads do not establish identical input composition.

## R1.2 · 2026-10-15T16:47Z · Computational repair of conditional-uniform sampling

Twenty-two two- or three-member groups mixed slowly under single-slot heat-bath updates; qualification thresholds were not relaxed. For the same D-only conditional-uniform target, size-two groups now use exact IID sampling of legal unordered pairs. Enumerate the legal second-member interval for each sorted first member, map every pair uniquely to an integer, and sample integers uniformly. Size-three groups independently sample three candidates uniformly and reject duplicates or proposals outside the D mean constraint, with a10,000,000-proposal ceiling per group; every legal subset has the same3! representations. Retain all qualified draws, without viewing V to resample.

Groups of size at least four retain the original two-chain heat-bath procedure:100 draws per chain in the full analysis, burn-in50s and spacing5s, where s is group size. MCMC qualification requires split-Rhat≤1.1 and ESS≥20 for SD and D mean, mean original-membership Jaccard≤0.5 per chain, and original-exact-set occurrence fraction≤0.25. Exact IID methods require algorithm correctness and completion of all planned draws; Rhat/ESS are descriptive and their random variation must not be used to discard draws. The original single-slot attempt is fully archived. The complete conditional control covers186/186 groups and13,807/13,807 members. This is a computational repair after the preceding results were exposed; it remains exploratory.

## R1.3 · 2026-10-15T16:50Z · Common sample-control computation budget

With50 draws per chain, one sampled observed group had D-mean Rhat=1.103, slightly above1.1. Before formal null endpoints, observed and all null conditions were uniformly changed to200 draws per chain and spacing10s; burn-in remains50s. The target distribution, qualification thresholds, candidates and statistics are unchanged. Do not filter groups by V or retain only valid null draws. Preserve the preceding qualification attempt. B99 is planned with three CPU workers. The actual null retains a fixed proposal clock, two chains,32nnz burn-in and4nnz spacing. If Tb is undefined on any scheduled draw, complete Tb Monte Carlo inference is missing. Defined and qualified Ta can be reported separately; valid-only Tb draws cannot generate a p-value.

## R1.4 · 2026-10-15T16:53Z · Data-identity guard repair

Cached learning `position_id` is an absolute offset within each source file; different source files can use the same integer. An integer-only `torch.isin` check would falsely flag leakage. Before execution, the guard was repaired to check nonoverlapping `source_paths` and disjoint global context IDs. Token identity is source SHA plus within-file offset. Actual cached TRAIN/EVAL windows come from original TRAIN files0/1 respectively; manifests contain exact offsets. This repairs identity checking and does not change data based on learning loss.

## R1.5 · 2026-10-15T16:47:49Z · Resource submission

The sole job, `pt-szeffn72`, uses the authorized `h100-4-reserved` quota and `shphd-lite-0911` image. Inspection found no reusable running four-card instance. No quota was added and no other task was changed. Submission establishes only platform acceptance: when this entry was recorded, the worker was still Pending and device smoke and learning had not started. Persistent subsequent receipts own actual devices, throughput and the final common budget.

## R1.6 · 2026-10-15T17:01Z · Separating causality from BF16 sequence-shape sensitivity

The durable device receipt at16:53:59 confirmed four full80GB H100 cards and usable BF16 computation. The first cache qualification stopped. Changing every future token at fixed shape left raw activations, z and gated events exactly unchanged. Truncating the prefix changed matrix shape: BF16 maximum raw differences were2/2/4 and event differences were7/13/9, while every R/F/N allocation at the three positions remained identical. The FAIL receipt and exact source version are fully preserved. Learning caches had not yet been extracted and no learning loss had been viewed.

Bitwise invariance across matrix shapes is not a necessary condition for causality, and this FAIL must remain visible. The main causal gate requires exact raw/z/event invariance under fixed-shape future changes and unchanged operational routes under truncation. Add independent FP32 and fixed-shape zero-future diagnostics, recording layer-relative errors, complete gated events and allocations. Stop if fixed-shape future changes affect outputs or tested routes still differ. Retain BF16 truncation event differences as numerical sensitivity; do not label them future leakage.

Native-model logit reproduction also preserves matrix shape before selecting32 positions for comparison, avoiding confusion between different LM-head GEMM rounding and model differences. Zero-output adapters still require strict invariance under the same cached-head computation. Formal computation retains the original BF16 strategy and fixed gate; diagnostics do not select a new threshold or primary-model precision.

## R1.7 · 2026-10-15T17:02Z · Common training budget after measured throughput

The cache contains130,712 TRAIN and initially65,402 EVAL positions. Native full-model and cached-head logits and CE differ by exactly zero at32 positions. Fixed-shape future changes are exactly invariant in BF16 and FP32. FP32 truncation maximum raw errors are9.16e-5–1.53e-4 with zero gated-event differences; BF16 sequence-shape sensitivity remains disclosed. The12-step numerical smoke passed, including zero adapters, serialized next-update weight/Adam replay and token-axis TensorBoard guards. External-process recovery remains explicitly NOT_QUALIFIED.

Measured smoke median update time is0.00572 seconds at batch256. The initial three-epoch proposal was not the final frozen budget. Before any formal condition comparison, measured throughput froze a common12 drop-last epochs,510 updates per epoch,6120 updates and1,566,720 valid-target exposures per run. Three seeds across three conditions give nine runs and14,100,480 exposures total. Evaluate/save at0/510/1530/3060/4590/6120; the original three-epoch proposal remains an intermediate endpoint, with midpoint3060. Learning rate, batch and other settings remain identical across arms, with no winner-dependent extension. Virtual SGD lr0.1 gives maximum relative expert-parameter step0.0103<0.05 and finite outputs, so lr0.1 is fixed without selecting on probe benefit.

The primary paired bootstrap resamples blocks of four consecutive EVAL contexts2000 times, using ratio linearization of the fixed supported-feature means. It is an approximate conditional interval, not a document-independent confidence interval, and does not replace three-seed differences. Preserve initial configurations and budget receipts at `config/formal.json` and `budget_frozen.json`.

## R1.8 · 2026-10-15T17:05Z · One low-frequency support-count repair

Formal training has not started and comparative losses have not been viewed. A count audit found that only1300 of3916 fixed low features meet≥20 hits in the original64 EVAL contexts,33.197% coverage, with307 features never hit. Expand EVAL once to512 contexts from the same fixed starting point in source file1. Preserve the original64 contexts/cache immutably; the new root is `data_eval512`. TRAIN is hardlinked to the original payload. Low/high lists, support threshold, training budget, routes and all three seeds remain unchanged.

This expansion responds only to insufficient support counts, not condition wins or losses. After one expansion, accept actual coverage and disclose remaining unestimable features; do not repeatedly enlarge samples or reduce the support threshold. The final configuration is `config/formal_R1_8.json`. Register a new representation-asset version and strict access check, leaving the original asset identity unchanged. The primary readout still describes only fixed low features with predeclared support and does not extrapolate to unestimated members.

## R1.9 · 2026-10-15T17:04Z · Repairing the exact three-member sampling budget gap

One size-three group in the formal null reached the original10,000,000 rejection-proposal limit. Tb retained NA under the original rule, while Ta continued through all99 draws. Authorize exact legal-triple counting/indexing IID sampling for the same D-only conditional-uniform target: after sorting, accumulate the number of legal(j,k) choices for each minimum rank using two-pointer counting, then index all legal triples uniformly by integer. After exhaustive-enumeration checks pass, uniformly recompute small-group controls for every already-frozen observed/null group, rather than filling only NA draws. Do not rerun or reselect matrices/graphs, change qualification thresholds or change effect definitions. Preserve the original sampling version, NA results and new complete repair separately. Computation runs on CPUs within the same Reserved node; an algorithm repair is not a new mechanism discovery.

## R1.10 · 2026-10-15T17:12Z · One competing-explanation control for first-direction sensitivity

The original first-direction operation completed and remains preserved. After observing meanL0 rise249.53→512.15, self-refutation identified that raw H projection still subtracts the original TRAIN mean mu. Normalization therefore combines projected centered variation with an extra fixed offset v(vᵀmu)/rms. Alignment between the direction and mu alone cannot establish that the offset causes all observed changes.

Add one separate, explicitly posthoc small control without new SVD, training or primary-result changes. Keep the fixed v and measurement H, set H_c=H−[(H−mu)v]vᵀ, and retain original statistics. This removes centered variation along the direction while preserving the mean. Compare original, direct raw-H removal and mean-preserving removal onL0, reconstruction, gated-event Jaccard and old-edge phi over commonly estimable edges. The prediction was separately saved before execution: if the fixed offset dominates doubledL0, mean-preserving removal should moveL0 toward the original value and increase event Jaccard; otherwise do not invent a root cause from intuition. This control distinguishes components of the operation and does not establish common semantics for v.

Engineering addition: the first Reserved-node CPU exact-control process failed to read a Numba cache from a locally dynamic module, with `ModuleNotFoundError: '<dynamic>'`; retain its log. Restart JIT with a separate empty `NUMBA_CACHE_DIR`, leaving scientific source, target, matrices, graphs and parameters unchanged. The new process has produced actual observed/qualification control outputs.

## R1.11 · 2026-10-15T17:35Z · Response decomposition of training harm

All nine formal runs completed, and all three allocations end materially worse than the original zero adapters. Preserve the primary H2 conclusion, budget and model. Add one posthoc, no-training finite counterfactual to distinguish the response components causing harm at these checkpoints, rather than searching for a winning new model.

At the same final parameters, original routes and full EVAL, write each linear expert response as δ_e(h)=U_eD_e mu_e+U_eD_e(h−mu_e), where mu_e is estimated only from TRAIN hidden states under the original routes. The full h always follows the original base residual. The original complete response and zero response must exactly reproduce saved C per-position losses. Additionally measure constant-only and centered-input-dependent-only responses. Run all three conditions and three seeds with the original supported low/high sets; do not change the C primary metric or retrain based on control results.

Save predictions before execution, with three possibilities: constant-response dominance, input-dependent-response dominance, or nonlinear interaction dominance. Define interaction as L_full−L_constant−L_centered+L_zero without assuming additive loss. Record response reconstruction error, relativeL2≤1e-5, and bitwise reproduction of original zero/full arrays. This control identifies harmful output components at fixed parameters; it does not establish how they were learned or assign semantic-common meaning to the constant response. Add only supplementary figures/tables, preserving the five main figure types.
