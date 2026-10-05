# Detailed: exact-33B finite action selection

2026-10-04. [中文](probe_33b_detailed_cn.md) · [Summary](probe_33b_summary.md). Design owner: [Anchor](anchor.md). Execution contract: [Protocol routing-r3 amendment, October 3 at 08:05 UTC](protocol.md) and the frozen execution configuration. Scientific judgment and the practical-effect threshold remain `Unknown`.

## 0. Quick Recap

Purpose: determine whether pre-target information improves selection among fixed computations. Hypothesis: predictable relative utility beats a strong fixed action. Rival: matching information exists but the pooled common action is stronger.

All three checkpoints, 23 model-specific families and 184 conditions are complete: 920 DEV rows and 1840 descriptive source rows. All 92 pooled cross-source conditions beat global-frequency random allocation and lose to the FIT-fixed common action, with the respective conditional pointwise intervals excluding zero. These are not independent replications.

Eligibility: frozen-recipe DEV evidence about local finite utility. No LM/SAE updates, general downstream testing, acquisition trajectory or retention result. The prediction that these policies beat the strong fixed action is unsupported here; scientific judgment remains `Unknown`.

## 1. Terminology

| Object | Concrete meaning | Use | Cannot establish |
|---|---|---|---|
| Exact 33B checkpoint | Existing dense backbone at 33,000,000,000 training tokens | Fixed state, not 33B parameters | Matched training histories or architectural causality |
| Event | A specified position and realized next token in a 257-token record | Sixteen events per record | An independent experimental replication |
| c, a, r, x | Final-block projection input c:2048; output a=Wc:1024; preceding residual r; x=r+a | Causal features and full native tail | A newly trained MoE expert |
| Source banks A/B | Disjoint sets of 256 records, 64 per domain | Construct average gradient actions | Source-population uncertainty |
| Common action | Average raw domain gradients, then normalize independently | One measured finite intervention | Average action loss or average normalized direction |
| FIT-fixed action | Minimum mean measured FIT cost in the prediction-source bank; transport its action name | Strong fixed control | DEV action selection |
| Global-frequency random | Target-free predicted action frequencies over all DEV events | Matching benefit at those frequencies | Within-category matching or a trained domain router |
| Oracle | Lowest realized event cost after seeing outcomes | Nondeployable lower bound | Attainable pre-target risk |

CE uses natural logs. Negative delta CE helps. Comparator gains are comparator minus policy, so positive favors policy. The finite regret gap against fullcx is policy minus the fixed full-input ridge loss; positive is worse.

## 2. Anchor Link and Decision

The original question concerns acquisition and retention through shared/private learning under finite resources. This experiment freezes the present state and computations. It neither compares experts produced by different training allocations nor measures forgetting. Update the claim about these fixed policies without closing the broader question or making this test a prerequisite for joint router/expert training.

## 3. Freeze, Authorization and Deviations

| Item | Contract and actual execution | Eligibility consequence |
|---|---|---|
| Data | Registered 2026-10-03 07:49:40 UTC before new model losses; 2048 records; no TEST arrays | Exact records/token strings disjoint; article, near-duplicate and pretraining overlap unknown |
| Native measurements | FP32 full-tail replay, causal-prefix/no-op/restoration checks; all 8 extraction and 8 finite shards complete | Qualified fixed-state finite measurements |
| Analysis | Producer, tests and config frozen 2026-10-03 08:23:40 UTC, with recorded runtime compatibility amendments; hashes unchanged on October 4 | No result-dependent recipe or family selection |
| Current authorization | Researcher approved repair and progress at 2026-10-04 10:20:58 UTC | Sequential CPU analysis and verification; no resubmission of the existing measurement job |
| FIT rules | Fixed lambda 10; 7/8/8 families retained; FIT-only transformations and selection | Comparison of fitted predictors, not sufficient-information identification |
| Post-hoc work | Independent implementation audit, comparator accounting and literature synthesis | No new confirmation status or retrospective registration |

[Analysis freeze](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/probe_analysis_freeze.json) and [authorization record](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/closeout_20261004T102058Z/authorization.json). No producer analysis failed, retried or excluded conditions. The first reading-table export omitted the no-update-only CSV columns; the exporter was corrected to use the union of fields. Original results were unchanged.

## 4. Actual Setup

**Models.** Each backbone has 281,431,040 parameters, eight layers, hidden width 1024, attention projection input 2048, FFN width 3072 and vocabulary 151936. Fresh S7 has a final-block SAE-sidecar training history with weight 0.1; SALL has unit-weight sidecars across eight layers. Their total parameter counts are 342,902,064 and 773,199,232. Initialization, objectives and resume histories do not form a paired architecture experiment. Equal token counts do not imply equal resources.

Exact paths and complete SHA256 identities are in the [config](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/configs/probe_33b.json). State hashes begin `a0b21cb3` for Dense, `c30b78e5` for fresh S7 and `80e2a46b` for SALL; file bytes were verified. No neighboring-token checkpoint was substituted.

**Data.** The already fixed capacity corpus supplies, per category in `npz_row` order, 32 training records for A, the next 32 for B, the next 64 for FIT, and all 128 DEV records for readout. Categories: cs.CL, cs.CV, math.AP, math.NT, physics.optics, physics.flu-dyn, q-bio.GN and q-bio.NC. Positions 14,30,…,254 predict the following token. Totals per model: 32768 events, including FIT8192, DEV16384 and 4096 per source bank. Selection does not use new losses; TEST remains sealed. [Registration](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/data/probe_33b/registration.json)

**Actions.** For source events, form ecᵀ where e is CE's gradient with respect to a, then average within each domain. Average the four raw matrices for common. Each nonzero matrix M independently gives δW=−0.001‖W‖M/‖M‖. Replay a+δWc through the original residual, MLP, norm and head. No optimizer step occurs; per-token choices generally do not represent a single global W update. Five-action and six-action-with-zero sets are analyzed separately.

**Predictors.** The 389-dimensional baseline contains current/previous token hashes, inclusive prefix frequencies in 128 bins each, position and its square, and log norms of c/a/x. Enhanced families add PCA64 of a, c, x or (c,x), a fixed random orthogonal projection of a, or the 64 SAE atoms most frequently nonzero on FIT, using raw amplitudes. Fullcx concatenates c/x for 3461 total features. PCA/standardization use FIT only; x is formed at cached FP32 before feature promotion. Ridge minimizes summed squared error plus ten times squared coefficients, with an unpenalized intercept. Ten separable A/B output columns are saved together. Selection takes the first exact predicted minimum; zero is first when available.

**Coverage.** A→B/B→A are primary transfer cases; A→A/B→B are secondary. Two action sets and pooled/four-domain scopes yield 184 conditions and 920 DEV rows. The two source roles yield another 1840 descriptive rows; they participate in direction construction.

## 5. Metrics and Decision Rules

Retain FIT-fixed, uniform, global-frequency random, common, no-update, oracle and fullcx controls, alongside coverage, harm and selection/rejection decomposition. Use 2000 paired whole-record draws stratified by category. Reestimate global DEV action frequencies in every DEV draw, including domain-specific tables; source intervals hold DEV frequencies fixed.

The frozen analyzer defines `harm_fraction` as the fraction with actual finite ΔCE strictly above zero, with no practical-harm magnitude threshold. This differs from the old panel's 10⁻⁵ nat threshold, so their fractions are not directly comparable. The definition was not changed after results. Realized loss increases also need not be identifiable or avoidable before the target is observed.

The practical-effect threshold is `Unknown`. Pointwise conditional intervals do not include source-population, paper-cluster or multiple-comparison uncertainty. Correlated conditions are not additional model seeds or independently sampled sources.

## 6. Evidence Lineage

| Claim | Artifact/computation | Observation | Boundary |
|---|---|---|---|
| Complete measurements and analysis | Scheduler, three aggregate and analysis receipts | 3/3 complete, all registered conditions | Completion is not hypothesis support |
| Strong fixed common wins | Each `summary.json`; [92-condition table](evidence/probe_33b_pooled_cross_source.csv) | All fixed-baseline gain intervals negative | Bounds these policies |
| Matching information helps | Same table, `gain_vs_global_marginal` | All respective intervals positive | Does not isolate within-domain/category information |
| Comparator accounting | [Post-hoc identity check](evidence/probe_33b_gain_accounting.json) | Maximum residual 6.62×10⁻¹⁸ | Arithmetic, not a training mechanism |
| Numerical readback | [Audit receipts](evidence/probe_33b_independent_audit.json) | 2760 rows, 235,980 values; maximum error 1.74×10⁻¹⁸ | Independent code path, same data and processing agent |

## 7. Main Results

The [Summary](probe_33b_summary.md) reports ranges over all pooled transfer conditions. Actual DEV improvements from common actions A/B are Dense 1451.41/1470.36, fresh S7 2773.56/2608.81 and SALL 1577.09/1637.71 micro-nats per event.

All 368 individual-domain fixed-baseline gain estimates are negative, but some intervals cross zero. Domain means do not characterize every event. Complete within/cross-source, family, action-set and domain results remain in each model's `analysis/summary.csv`, with descriptive sources in `source_summary.csv`.

First-order and measured effects are close, not identical. DEV correlations for common A/B are Dense 0.999984/0.999988, S7 0.999937/0.999959 and SALL 0.999986/0.999989. First-order-minus-finite bias remains approximately −31 to −129 micro-nats. Policy utility always uses measured finite costs.

Source records are not generalization data. Rejection can remove beneficial as well as harmful updates, so read coverage and the matched-fixed/selection/rejection decomposition together. Some SAE conditions beat the full-input ridge comparator; this neither overturns their loss to fixed common nor identifies an SAE mechanism or sufficient information.

### 7.1 Actual CE, receiving domains and secondary comparisons

These are descriptive summaries of frozen tables, spanning every registered family and both source directions. Ranges are not new tests or winner selection. Absolute CE uses nats; differences use micro-nats. Interval-sign counts are checks, not independent successes.

| 模型 / Model | 未更新CE / Baseline CE | 策略CE范围 / Policy CE range |
|---|---:|---:|
| Dense | 3.494825 | 3.493553 – 3.493878 |
| fresh S7 | 3.497078 | 3.494650 – 3.495276 |
| SALL | 3.498606 | 3.497221 – 3.497483 |

Each domain has 256 DEV records and 4096 events. Every fixed-baseline gain point estimate is negative. Random-control gain is not positive in every domain condition; the fresh-S7 computer-science range crosses zero.

| 模型 / Model | 接收域 / Domain | 策略ΔCE / Policy ΔCE | 固定基线收益 / Fixed gain | 全局随机收益 / Global-random gain | 固定收益CI全负 / Negative fixed CI |
|---|---|---:|---:|---:|---:|
| Dense | computer_science | -747.32 – -573.69 | -316.54 – -111.67 | 28.07 – 223.17 | 22/28 |
| Dense | mathematics | -2280.68 – -1595.59 | -834.11 – -277.65 | 182.93 – 724.88 | 28/28 |
| Dense | physics | -1295.84 – -879.10 | -591.14 – -188.16 | 67.67 – 365.25 | 28/28 |
| Dense | biology | -931.59 – -724.14 | -310.07 – -114.21 | 107.05 – 304.22 | 25/28 |
| fresh S7 | computer_science | -1420.09 – -802.14 | -588.60 – -69.23 | -17.43 – 449.01 | 24/32 |
| fresh S7 | mathematics | -4793.16 – -3566.92 | -1367.85 – -405.22 | 621.77 – 1655.16 | 32/32 |
| fresh S7 | physics | -2063.60 – -1512.60 | -843.01 – -513.64 | 53.30 – 578.93 | 32/32 |
| fresh S7 | biology | -1683.95 – -1117.06 | -712.26 – -145.37 | 108.50 – 594.32 | 25/32 |
| SALL | computer_science | -917.63 – -669.40 | -389.22 – -119.38 | 34.06 – 285.53 | 27/32 |
| SALL | mathematics | -2468.59 – -2078.74 | -723.05 – -211.94 | 399.37 – 794.22 | 30/32 |
| SALL | physics | -1289.60 – -872.35 | -606.96 – -192.06 | 2.21 – 391.42 | 31/32 |
| SALL | biology | -1017.32 – -752.05 | -404.24 – -124.89 | 63.22 – 329.30 | 28/32 |

Within-source A→A/B→B is secondary and is not pooled with cross-source results. Fixed gains range from −431.48 to −102.16 micro-nats for Dense (28 conditions), −791.98 to −145.21 for S7 (32), and−437.65 to −109.79 for SALL (32). Every fixed-gain interval remains negative and every global-random interval positive. These remain DEV evaluations; source-record descriptions are separate.

### 7.2 Action-use proportions

Percent of events, with ranges across every pooled cross-source condition. Column endpoints generally come from different policies and must not be added. Five means five update actions; six adds no update. The [920-row table](evidence/probe_33b_all_readout.csv) retains individual proportions and intervals; source descriptions remain in execution.

| 模型 / Model | 动作数 / Actions | CS | Math | Physics | Biology | Common | No update |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dense | 5 | 18.63 – 22.36 | 22.79 – 25.09 | 16.81 – 22.02 | 14.64 – 19.75 | 12.70 – 24.54 | 0 (excluded) |
| Dense | 6 | 15.26 – 17.77 | 21.51 – 22.82 | 14.20 – 19.50 | 11.69 – 16.37 | 12.70 – 24.54 | 7.56 – 13.39 |
| fresh S7 | 5 | 16.86 – 23.78 | 16.79 – 25.89 | 14.28 – 21.74 | 17.12 – 24.68 | 14.95 – 25.63 | 0 (excluded) |
| fresh S7 | 6 | 14.27 – 17.36 | 14.98 – 24.31 | 12.11 – 20.14 | 12.43 – 20.41 | 14.95 – 25.63 | 8.01 – 16.57 |
| SALL | 5 | 14.02 – 20.37 | 22.34 – 29.92 | 16.41 – 20.59 | 15.62 – 20.06 | 13.95 – 24.38 | 0 (excluded) |
| SALL | 6 | 11.27 – 17.41 | 21.17 – 27.92 | 14.65 – 18.44 | 12.95 – 16.78 | 13.95 – 24.38 | 6.55 – 11.81 |

Action names denote source gradients, not semantic expert labels. The common action receives about 13–26% use even though it is the strongest fixed action. Together with negative fixed gains, this describes the fitted policies; it does not identify estimation error, missing information or function-class limits as the cause, or assign a semantic domain to an expert.

## 8. Visualization

The [Summary figure](probe_33b_summary.md) shows all 92 pooled transfer conditions. Its [manifest](evidence/probe_33b_figure_manifest.json) specifies data, units, axes, expected and observed patterns, rivals and claim limit. It was opened for visual inspection; the Dense no-SAE annotation was moved into its empty row. This is a comparator plot, not a training curve or architecture effect.

## 9. Failure and Inference Layers

| Layer | Status | What remains unresolved |
|---|---|---|
| Prefix causality, native tail, no-op and restoration | Qualified in all three models | Corpus independence |
| FIT recipe and numeric tables | Frozen recipe and separate calculation PASS | Adequacy of the predictor class |
| Current policy improvement over fixed | Unsupported here | Other policies, actions, scales or future learned experts |
| Six-arm acquisition/retention | Formal trajectories NOT RUN | Old zero-step GPU dtype failure is an implementation failure |
| New MoE/downstream improvement | Unmeasured | External papers do not supply this experiment's results |

The separate capacity dtype repair is recorded in its [amendment](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/dtype_amendment_20261004T102058Z/amendment.json). Its CPU smoke is not finite-routing evidence.

## 10. Full Round Record

**October 3 measurement round.** Question: do equal-token checkpoints support target-blind selection and source transfer among five finite actions? Setup: three frozen checkpoints, full final-block input, two sources and equal-norm directions. Training records construct sources/FIT; fixed DEV supplies readout and TEST is sealed. Job `pt-meoxfrko` ran 12:09:09–12:25:11 UTC and succeeded; measurements were 3/3 complete, utility analysis then NOT RUN. Insight/boundary: measurements enable the analysis but do not establish utility.

**October 4 analysis round.** Same question, models, actions and data. Execute the October 3 frozen recipe sequentially on CPU without LM training. Producer times: 86.03/89.37/92.38 seconds; independent readbacks: 26.54/27.28/32.76 seconds. Results: 920 DEV and 1840 source rows verified. Update: matching gain coexists with common-action superiority. The next judgment separates present policy utility from shared/private training effects; neither a scientific transition nor new training authorization follows automatically.

## 11. Interpretation

Let R_f be FIT-fixed risk, R_π policy risk and R_m risk under random allocation at the policy's global frequencies. Adding and subtracting gives

\[
R_f-R_\pi=(R_m-R_\pi)-(R_m-R_f).
\]

The first term is positive here but smaller than the second. This explains the two comparisons without identifying which causal feature produces matching.

The common action also has a construction-specific property. On the balanced source objective that produces its nonzero mean gradient M, a global displacement of normρ has first-order change at least−ρ‖M‖; common reaches that bound. This Cauchy–Schwarz fact belongs with the existing [normalized-gradient discussion](capacity_mathematics.md). Finite DEV advantage still requires measurement. Source steepest descent does not discover universal knowledge and does not extend automatically to conditional per-token computation or long-term AdamW.

## 12. Claim Boundary

Can claim: in these fixed checkpoints/banks/DEV records, the specified predictors have matching benefit over global-frequency random allocation but all fail to beat fixed common; results are traceable.

Cannot claim:92 independent confirmations, arbitrary source/article generalization, SAE causality, universal common knowledge, MoE architecture improvement, long-term acquisition/retention or downstream benefit. Article, near-duplicate and pretraining overlap remain `Unknown`.

## 13. Next Decision

Scientific decision: `Unknown`. **AI recommendation:** retain the fixed-bank result without selecting favorable families, then complete the existing capacity design with comparable initialization, valid-token normalization and separate parameter/compute coordinates. Read acquisition/retention matrices and C/T interventions. New execution requires its current authorization.

## 14. Artifact Manifest

| Artifact | Role | Identity/completion |
|---|---|---|
| [Config](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/configs/probe_33b.json) | Checkpoints, data, recipe | SHA256 prefix 70e6efb0; unchanged |
| [Producer](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/scripts/analyze_probe_33b.py) | Array-only FIT/selection/scoring | SHA256 prefix 0814a699; unchanged |
| [Independent reader](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/scripts/audit_probe_analysis_20261004.py) | Reconstruct features, normal equations, decisions and intervals | No producer imports/refits;3/3 PASS |
| [Output root](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/probe_33b_01) | Native events, finite effects, fits and full results | Raw arrays remain in execution |
| [Reading payload manifest](evidence/probe_33b_manifest.json) | Compact tables, checks and figure | Source hashes retained; no raw arrays copied |

The PCA audit checks FIT centers, orthogonality, signs, singular values and covariance eigen-equations, without reranking the remaining full spectrum. First-order contractions are independently sampled at 128 deterministic events; finite-summary verification is exhaustive. No GPU forward is rerun, so native-tail qualification remains based on the original measurement receipts.

## 15. Reproduction and Links

At the execution root, use the frozen producer with `--config configs/probe_33b.json --output-root runs/probe_33b_01 --model-id <model ID>`. Complete receipts trigger hash verification and ALREADY_COMPLETE instead of refitting. [Current logs/audits](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/closeout_20261004T102058Z) preserve execution evidence. The [literature comparison](sharing_literature_20261004.md) constrains interpretation without changing this contract.
