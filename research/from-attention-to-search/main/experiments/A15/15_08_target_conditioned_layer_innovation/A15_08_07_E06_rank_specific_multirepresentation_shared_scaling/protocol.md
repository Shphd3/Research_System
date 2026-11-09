# Protocol: A15_08_07_E06 Rank-Specific Multi-Representation Shared Scaling

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
Approval status: researcher explicitly confirmed the four-representation design and waived another review on 2026-08-27
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, smoke, full 5090 run, analysis, figures, summary, detailed
Design frozen at: 2026-08-27
Purpose: correct the old maximum-rank-prefix error and test local versus shared functional dimension
Primary Anchor: A15_08_07 semantic-conditioned functional subspace
Anchor decision question: does domain conditioning reveal compact local function while the union requires broader coordinates?
Anchor physical prior tested: distinct domain-local discriminative directions can broaden a shared span
Anchor core model term tested: held-out rank-r functional retention
Anchor falsifier: rank-specific shared learning reaches the local functional target at a compact rank
Experiment role: metric and implementation audit with representation controls
Primary metric from Anchor: smallest rank whose simultaneous lower bound retains 90% of the full-map held-out benefit
Claim boundary from Anchor: label accessibility only; no native gate use or expert utility
Minimal setup: Qwen3-30B-A3B, frozen 8-domain x 8-child taxonomy, four representations, local and shared linear tasks
Treatment and controls: independent fit at every rank; local union oracle; old maximum-rank prefix; Haar and permutation guards
Changed variable: representation and local-versus-shared constraint
Held fixed: model, decision token, taxonomy, rows, splits, labels, loss, rank grid, uncertainty rule
Conditions to run: retrospective 19,200-row stage and frozen fresh-expression confirmation stage
Pass: corrected shared r90 is materially larger than local need and the direction replicates on fresh confirmation
Fail: corrected shared r90 is compact or no larger than the registered local comparator
Insufficient: full-map benefit is not positive, optimization guards fail, or intervals do not identify r90
Cannot claim: Router use, expert utility, causal routing, nonlinear rank, or universal model behavior
Approval decision: execute without another review
```

## 1. Terminology / Definitions

For block \(\ell\), \(X_\ell\) is the normalized state before the attention write and \(U_\ell\) is the normalized state change caused by that write. The four candidate inputs are

\[R_{U,\ell}=U_\ell-\widehat{\mathbb E}_{lin}[U_\ell\mid X_\ell],\quad U_\ell,\quad G_\ell=X_\ell+U_\ell,\quad \Delta G_\ell=G_\ell-G_{\ell-1}.\]

The residualizer and all standardizers are fitted on TRAIN only. A local task predicts one of eight children inside a known parent domain. A shared input space uses one projection for all eight parent domains and a separate eight-way head per domain. “Rank-specific” means the projection at rank \(r\) is optimized as its own model; it is not a prefix of a model trained at rank 56.

Numerical rank counts non-negligible singular values under the registered floating-point tolerance. Entropy effective rank is \(\exp(-\sum_j p_j\log p_j)\) for normalized squared singular values \(p_j\). Neither is the primary functional rank.

## 2. Anchor Alignment

The approved A15_08_07 Anchor requires one independently learned basis per candidate dimension and defines functional dimension through held-out benefit retention. E05 violated the intended learning semantics for the direct shared condition by fitting only a maximum-rank space and evaluating its prefixes. This successor tests whether the local-versus-shared conclusion survives that correction. \(U\), \(G\), and \(\Delta G\) are controls that determine whether any observed scaling is specific to \(R_U\) or appears in broader same-model representations.

## 3. Tested Hypothesis

Primary hypothesis: after every rank is optimized independently, eight domain-local tasks retain their full-map function at low individual ranks, while one space shared across all eight domains requires a larger rank because it must carry differently oriented discriminative directions.

Strongest rival: the old near-56D behavior came from a poorly ordered prefix of one maximum-rank solution; a rank-specific learner can find a compact shared space.

## 4. Rival Explanations

1. **Algebraic-ceiling artifact:** 7 and 56 are output-contrast ceilings rather than empirical functional ranks. Guard: use held-out benefit with uncertainty; report algebraic rank separately.
2. **Layer-selection artifact:** different representations peak at different layers. Guard: representation-specific DEVELOPMENT selection plus a matched-layer robustness panel.
3. **Optimization failure:** a low-rank shared model looks bad because it did not converge. Guard: multiple restarts, known-subspace recovery, monotonic full-rank sanity, and oracle comparison.
4. **Opened-test overclaim:** existing 19,200-row TEST panels have been inspected in predecessor experiments. Guard: label their result retrospective and require a separately frozen fresh-expression stage for independent confirmation.

## 5. Data Construction And Provenance

The retrospective population is the frozen 19,200-row robustness dataset with 11,520 TRAIN, 2,560 DEVELOPMENT, 2,560 same-template TEST, and 2,560 new-template TEST rows. It contains a balanced 8-parent by 8-child taxonomy. One row is one prompt ending at the final token of the common `Answer:` suffix. Labels come only from the frozen taxonomy. Prompt text and label fields are forbidden as model inputs to the subspace learner; only the extracted representation and the within-parent child label are permitted.

The representation source is the verified Qwen3-30B-A3B array of shape `[48,19200,2,2048]` containing \((X,U)\). Its recorded SHA-256 is `cba20c5e3eb484a82c03246f6471b8da1e1c1a40f29c7cde9a037a99fa8ea144`.

Before any retrospective TEST value is opened by this successor, code, rank grids, selected layers, hyperparameters, and a freeze receipt are written. A new confirmation set uses the same frozen 64-cell taxonomy, expressions and semantic compositions absent from all four existing splits, balanced rows per cell, and no normalized-text/template-family overlap. It is generated and sealed before retrospective successor metrics are read. Its exact manifest and hash are run artifacts.

## 6. Learning Task And Permitted Supervision

The common four-representation task is standalone within-domain eight-way child classification. For representation \(Q\), a rank-\(r\) model produces logits \(Q P_r A_{d,r}\) for known domain \(d\). TRAIN fits \(P_r,A_{d,r}\); DEVELOPMENT selects layer, ridge, restart, and stopping; confirmation only evaluates the frozen state.

To correct the exact old claim, one additional primary audit uses \(R_U\) as a correction on a frozen \(X\)-only baseline and retains E05's conditional cross-entropy-gain semantics. This conditional result is not compared numerically with standalone \(U,G,\Delta G\) gains.

## 7. Model / Architecture And Frozen Variants

- Local: one independently optimized rank-\(r\) linear map per domain, \(r=1,\ldots,7\).
- Direct shared: one independently optimized orthonormal input basis per candidate rank and separate domain heads. Registered grid is every integer \(1,\ldots,56\) for the eight-domain endpoint; task-count diagnostics use their exact ceilings.
- Local-union oracle: SVD of all fitted local coefficient maps; it is non-deployable because it consumes local answers.
- Old-prefix control: one rank-56 direct shared fit, deterministically rotated by head energy, then truncated.
- Haar control: equal-rank random orthonormal bases with frozen seeds.

All coefficient outputs are contrast-centered, so an eight-class local map has rank at most seven and eight unconstrained local maps have union rank at most 56.

## 8. Training Objective And Optimization

For each task \(d\), centered one-hot target \(Y_d\), centered representation \(Q_d\), shared orthonormal basis \(P_r\), and task head \(A_{d,r}\), minimize equal-domain mean squared logit residual with ridge:

\[\frac18\sum_{d=1}^8\left[\frac1{n_d}\lVert Y_d-Q_dP_rA_{d,r}\rVert_F^2+\lambda\lVert A_{d,r}\rVert_F^2\right],\qquad P_r^\top P_r=I.\]

The conditional \(R_U\mid X\) variant replaces \(Y_d\) by the TRAIN out-of-fold correction target left by the frozen \(X\) head. Candidate ridge values, step counts, learning rates, and restart seeds are frozen in the run configuration. DEVELOPMENT chooses separately for every rank; confirmation never chooses a setting.

## 9. Conditions, Seeds, And Checkpoints

- Representations: `ru`, `u`, `g`, `delta_g`.
- Primary endpoint: eight domains, eight children each.
- Local ranks: 1--7; shared ranks: 1--56.
- Task-count diagnostic: deterministic nested parent sets of sizes 1, 2, 4, and 8.
- Layer selection: all legal blocks on TRAIN/DEVELOPMENT; `delta_g` begins at block 2. Ties use lower DEVELOPMENT cross entropy, then smaller block.
- Matched-layer panel: union of the four representation-specific selected blocks, with no new selection.
- Optimizer restarts: three frozen seeds per rank; DEVELOPMENT chooses one.
- Bootstrap: 2,000 template-family resamples, equal weight per domain; maximum-statistic correction across ranks within each representation/condition.
- Resource: ACP `5090-8-spot`, one worker, `n12lp.nn.i10a.8`, eight GPUs, spot quota, normal priority.

## 10. Primary Metric And Frozen Analysis Plan

For each task or shared condition define held-out benefit \(B_r=CE_{null}-CE_r\) for standalone tasks and \(B_r=CE_X-CE_{X+R_U,r}\) for the conditional audit. The full contrast map gives \(B_{full}\).

\[r_{90}=\min\{r:\operatorname{LCB}_{sim}(B_r-0.9B_{full})>0\}.\]

The unit is projection dimensions. The observation unit is a row; the independence unit is a template family. Local results report each domain and the equal-domain distribution. The shared primary statistic is the worst-domain retention, so no domain can be sacrificed by averaging. A full-map benefit whose one-sided simultaneous lower bound is not positive makes \(r_{90}\) `NA_FULL_NOT_ADMITTED`. No crossing makes it `NA_NOT_IDENTIFIED`.

The decision comparison is the corrected eight-domain shared \(r_{90}\) versus the local requirements, reported both as the sum of eight local \(r_{90}\) values when all are identified and as the complete local-rank curve otherwise. A larger shared number is descriptive evidence of union growth, not a theorem that ranks must add.

## 11. Secondary Metrics And Guards

Report held-out balanced accuracy, point retention, numerical coefficient rank, entropy effective rank, same-task bootstrap subspace overlap, cross-domain overlap, oracle-union curve, Haar curve, old-prefix curve, optimization loss, orthogonality error, convergence, and known-subspace recovery. Secondary metrics cannot rescue a failed or unidentified primary r90.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: synthetic rank-3 shared signal must be recovered at rank 3 within tolerance and beat Haar.
- Known bad: permuted labels must not yield an admitted positive full-map benefit.
- Known confusing: an 8-class coefficient has numerical rank at most 7 even when the input representation is high-dimensional; this ceiling is not empirical functional rank.
- Identity: independently fitting rank \(r\) must not return the exact leading columns of the rank-56 old-prefix state for all \(r\) on a non-degenerate synthetic problem.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Expected output | Stop rule / handoff |
| --- | --- | --- | --- | --- | --- |
| 0 | freeze inputs | verified 19,200 array and metadata | hash, split audit, construct four objects lazily | freeze receipt | stop on hash/schema/finite failure |
| 1 | validate correction | synthetic and small real subset | run rank-specific, oracle, prefix, Haar guards | smoke audit | full run only if all guards pass |
| 2 | select without TEST | TRAIN/DEVELOPMENT | scan layers and per-rank settings | frozen state registry | no TEST access before registry |
| 3 | retrospective correction | existing TEST panels | evaluate frozen local/shared curves | retrospective tables/figures | cannot call independent confirmation |
| 4 | independent confirmation | sealed new expressions | extract \((X,U)\) and evaluate frozen states | confirmation tables/figures | no tuning after unseal |
| 5 | evidence audit | all artifacts | completeness, provenance, plot-contract audit | summary/detailed-ready manifest | no conclusion if audit fails |

## 14. Algorithm, Output, And Provenance Contract

Worker root: `/data/250010109/MoE_Router/experiments/20260827_a15_08_06_e06_rank_specific_multirepresentation_shared_scaling/`.

Expected outputs include frozen configuration and hashes, selected layers, one state per representation/rank/restart, local and shared curve CSVs, effective-rank table, bootstrap arrays or reproducible seeds, completion audit, and report-ready PNG/PDF figures. Canonical curated result records live beside this protocol. Raw arrays/logs remain in the worker root.

No existing E05 or E03 code, state, data, or result file may be modified. Reuse occurs by read-only imports or copied minimal modules in the new worker root.

## 15. Success / Failure / Insufficient Evidence

- **Pass:** per-rank direct shared learning still requires materially more dimensions than local tasks and the registered direction replicates on fresh confirmation.
- **Fail:** a compact per-rank shared solution removes the claimed local-versus-multi-domain expansion, or the shared requirement is not larger under the registered comparison.
- **Insufficient:** full maps are not admitted, optimization/identity guards fail, confirmation construction fails, or simultaneous uncertainty does not identify the crossing.

## 16. What This Cannot Claim

The experiment cannot show that the native MoE gate uses the fitted subspace, that the subspace predicts expert-relative utility, that projection creates label information, that nonlinear useful rank is large, or that the result generalizes beyond this model, token position, taxonomy, and linear objective.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Status | Grounding |
| --- | --- | --- |
| A. Question and boundary | CONFIRMED | researcher requested correction of the old rank interpretation |
| B. Data and provenance | CONFIRMED | researcher approved reuse plus a fresh confirmation stage |
| C. Task and supervision | CONFIRMED | researcher approved the four-representation discriminant experiment |
| D. Model and architecture | CONFIRMED | every rank independently learned; local/shared/oracle/prefix controls |
| E. Objective and optimization | CONFIRMED | functional retention rather than algebraic rank |
| F. Comparison and evidence | CONFIRMED | local versus unified rank with trustworthy correction controls |
| G. Execution and reproducibility | CONFIRMED | explicit immediate execution on remote 5090 |

Cross-block audit: `PASS`. Execution approval: implementation, smoke, and full run. Any post-start change to data roles, task, objective, rank grid, primary metric, or confirmation boundary requires an append-only amendment and eligibility audit.

### Execution status ledger

| Time (UTC) | Scope | Job | Resource | State |
| --- | --- | --- | --- | --- |
| 2026-08-27 14:00 | smoke | `pt-qka7865q` | ACP `5090-8-spot`, one node, eight RTX 5090, spot | SUBMITTED |
| 2026-08-27 14:10 | smoke | `pt-qka7865q` | ACP `5090-8-spot`, one node, eight RTX 5090, spot | STOPPED_BEFORE_ALLOCATION; zero replicas; superseded because the executable omitted the registered conditional and matched-layer guards |

### Execution clarification 1 (2026-08-27, before successor TEST access)

The matched-layer robustness panel is the TEST-blind matrix of DEVELOPMENT within-domain balanced accuracy and cross entropy for every representation at the union of the four representation-specific selected blocks. It diagnoses whether descriptive cross-representation differences are a selected-layer artifact; it is not an additional held-out functional-rank curve and cannot change the primary within-representation local-versus-shared verdict. This clarifies the previously underspecified panel without changing data roles, task, rank grid, primary metric, or confirmation eligibility.

The executable must also contain the registered `R_U | X` branch before any valid smoke may pass: eight local rank curves and one eight-domain direct shared rank curve, with TRAIN template-family-grouped five-fold out-of-fold \(X\) predictions defining the correction target. Its local and shared candidate ranks are fitted independently exactly as in the standalone branch. Full expected direct-fit receipts are therefore 728: 616 standalone receipts plus 112 conditional receipts.

Corrected-smoke execution entry: at 2026-08-27 14:20 UTC, job `pt-hob3j8jq` was submitted to ACP `5090-8-spot` with one node and eight RTX 5090 GPUs. It covers 12 fit-state smoke cases plus conditional, permutation, synthetic, and matched-layer guards.

### Execution amendment 2 (2026-08-27 14:52 UTC, before successor TEST access)

The researcher explicitly replaced the queued 8×RTX 5090 execution resource with one 4×H100 node on reserved quota to avoid the observed whole-node queue. Job `pt-hob3j8jq` was stopped while still at zero replicas and produced no run root or result. The replacement tuple is ACP workspace `share-space`, AEC2 cluster `share-cluster`, worker spec `n6ls.iu.i40.4`, one node, four H100 GPUs, four launcher processes, `reserved` quota, and normal priority. Only job sharding and model-parallel device count change; data, representation definitions, selected-layer rule, rank grids, per-rank optimization, seeds, metrics, bootstrap, pass/fail rules, and confirmation boundary remain unchanged. Results from the superseded 5090 submissions are ineligible because neither acquired a worker.

The first H100 reserved smoke, job `pt-735me1i6`, acquired four GPUs but failed before creating a run root. Root-cause tracing found that the launcher still sourced the frozen 5090/Blackwell runtime contract before run-root creation. The H100 execution environment was corrected to the already successful E02 H100 pair: image `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0710:container1-20260710154849` and the E02 H100-compatible activation script. A regression test now rejects any H100 launcher that points back to the 5090 runtime. No scientific input or result was accessed by the failed job.

The second H100 smoke, job `pt-znkcm1kx`, passed resource, source, sealed-confirmation, layer-scan, matched-layer, and scientific-freeze gates, then stopped during conditional-target construction. The frozen TRAIN data have exactly three template families per domain, so the registered five-fold template-family-grouped OOF split is impossible without splitting an independence unit. Before TEST access, the OOF rule was therefore corrected to three-fold leave-one-template-family-out: each of the three folds holds out one complete template family. This preserves the intended leakage guard and changes only the feasible fold count, not the baseline model, correction target definition, data rows, rank model, or evaluation rule. The failed run exposed no TEST result.

Corrected H100 smoke job `pt-ft8h2x91` succeeded with completion audit PASS: all four H100 devices and reserved resource tuple passed, the eight-domain three-fold conditional baseline passed, synthetic rank-3 recovery passed, every permuted-label domain had a non-positive one-sided lower bound, all 12 smoke fit receipts were present, and no registered smoke check failed. Full job `pt-21hckxi9` was then submitted with this exact smoke audit as its required gate.

Full job `pt-21hckxi9` completed the TEST-blind 48-layer scans, scientific freeze, conditional baseline, both negative/positive guards, all 728 rank-specific fit receipts, and all overlap diagnostics. It then failed before creating the confirmation directory because `extract_confirmation.py` retained an eight-5090 device guard and an eight-device 29 GiB map. No confirmation row and no retrospective TEST metric was evaluated. The extractor was made resource-driven and regression-tested for four H100 devices with a 75 GiB-per-device balanced map. To avoid recomputing the already hashed pre-TEST chain, the registered recovery is an exact continuation of the same run root. A resume receipt must first revalidate H100 preflight, 728-fit manifest, three-fold conditional manifest, synthetic and permutation guards, overlap audit, TEST-blind freeze, and absence of confirmation, analysis, figures, and completion artifacts. Only then may the recovery run confirmation extraction through final completion audit.

The first continuation job, `pt-huqq6imc`, passed that source audit and stopped while loading the model, before forwarding any confirmation row. The H100 runtime intentionally lacks the optional `accelerate` package required by the attempted `device_map="balanced"` loader. The extractor is therefore corrected to the already exercised H100 execution pattern in this repository: four `torchrun` processes, one complete frozen Qwen3-30B-A3B replica on each H100, disjoint confirmation-row shards, and an exact global-index merge. Automated guards require the four shards to cover every one of the 640 rows exactly once and restore metadata order. A second append-only resume receipt revalidates the same pre-TEST chain and absence of confirmation/results before execution. This changes only model placement and row parallelization; model weights, prompts, captured layers and tensors, data roles, frozen states, metrics, and decision rules are unchanged.

The next continuation submission, `pt-q5gc50uo`, was correctly stopped by that source audit before launching extraction: the preceding failed loader had left an empty `confirmation_extraction` directory even though it wrote no file or row. Inspection established that the directory contained zero entries and predated `pt-q5gc50uo`; it was removed with exact `rmdir`, while the failed append-only receipt was retained. The third resume receipt must again pass every source and absence check before the four-process extractor is launched. This is provenance cleanup only and does not delete data or alter scientific state.

Third continuation job `pt-v0b1o6sb` succeeded. It extracted all 640 sealed confirmation rows as four disjoint 160-row H100 shards, merged an exact global-index partition, produced the full retrospective and confirmation analysis, rendered all registered figures, and passed the completion audit. Post-render visual inspection found that non-admitted full-map benefits had been divided by values near zero in two descriptive retention plots, producing meaningless axes of order \(10^{30}\)--\(10^{31}\). The registered \(r_{90}\) implementation had already typed those cases as `NA_FULL_NOT_ADMITTED`; the renderer was corrected to mask undefined retention ratios, show conditional mean cross-entropy benefit in nats, and label undefined \(r_{90}\) explicitly. This changes presentation only.

The same visual audit found that the secondary numerical-rank diagnostic used a float64 machine-epsilon threshold on coefficient products formed in float32. Float32 rounding noise was therefore counted as 64 directions even at requested rank 1. The diagnostic threshold now respects the source floating-point precision; a regression test requires a float32 rank-1 outer product to report rank 1. Reserved H100 job `pt-riot0k4f` reran the complete 2,000-bootstrap aggregation into a separate candidate directory. Its correction receipt verified byte-identical hashes for `results.json` and all six decision-bearing curve tables, corrected 840 of 3,360 diagnostic rows, and found zero numerical ranks above requested rank. Only the corrected diagnostic table and regenerated figures were promoted; all superseded outputs remain archived beside the run for provenance.

Canonical result records: [summary.md](summary.md) and [detailed.md](detailed.md). Both remain `AI_DRAFT_AWAITING_HUMAN_JUDGMENT` until the researcher completes the result account in the active Focus.
