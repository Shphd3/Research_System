# Detailed: exact-33B S7 controlled shared update

Primary Anchor: [anchor.md](../../../../problem_anchors/17_shared_and_interference_learning/17_10_shared_update_conditional_interference/17_10_shared_update_conditional_interference_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), registered SHA256 `f8032e8efa7033b9ff06cf9a977636818be3a235ad59ed92ae861932a49ed3f9`  
Summary: [summary.md](summary.md), [summary_cn.md](summary_cn.md)  
Result eligibility: complete and eligible for the registered fixed-checkpoint loss contrast; SAE task-signal proxy fails its own qualification. The researcher's scientific judgment remains unconfirmed.

Execution root (`R` below): `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z`.

## 0. Quick Recap

**Purpose:** Test how a normal A update to one frozen model's shared matrix affects B under crossed input-direction overlap and answer rules, then locate any effect using a frozen SAE.

**Direct result:** Four-H100 job `pt-yzq8kkur` succeeded. The raw auditor accepted 12 confirmation families, 96 source gradients, 192 virtual updates and 384 target condition cells. At step `1e-4`, the registered interaction \(M\) is `0.000152056` nats/target, 95% paired-bootstrap interval `[0.000136172, 0.000167218]`; at `5e-5`, it is `0.0000760280`, interval `[0.0000680777, 0.0000836184]`. High-overlap/reversed-rule B loss remains negative at both steps. The frozen-rule category is `MODULATION_WITHOUT_NET_HARM`.

**SAE direct result:** 32 similarly activated common atoms were selected in every family. All 12 paired task-signal reconstruction relative-error medians exceed the registered 0.5 threshold (range `1.0057–1.1589`). Signed decomposition is available but cannot validate this SAE as a task-signal proxy or an independent predictor.

**Boundary:** The result concerns one exact-33B S7 state and a constructed internal binary task. The strongest net-harm claim is unobserved. Human result/boundary confirmation remains `Unknown`.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation and unit | Cannot prove |
| --- | --- | --- | --- |
| Effective A update | A's ordinary supervised step improves independent A data | \(\Delta W_A=-\varepsilon\|W_0\|_F G_A/\|G_A\|_F\); independent A loss change < \(-\tau\) | Benefit or harm to B |
| B consequence \(I\) | B loss after the A update minus its own baseline | Conditional two-class CE, nats/target; negative helps B | Interference from a positive local component |
| Direction overlap \(\rho\) | Inner product of the generated A/B task-signal directions | `0.1` or `0.8`; both directions change together within a family | SAE overlap or a fixed-A-gradient intervention |
| Interaction \(M\) | Extra reversed-minus-kept B consequence at high versus low overlap | \((I_{H,flip}-I_{H,keep})-(I_{L,flip}-I_{L,keep})\), nats/target | Net harm when positive |
| SAE common atom | Same frozen decoder atom used by A and B with sufficiently similar activation | Each group/\(\rho\): ≥8/256 positive; frequency and positive 25/50/75 quantile ratios ≥0.5 | Task signal, causal necessity, or predictive utility |
| Signed terms | First-order B loss sensitivity along selected SAE span and its complement | \(I^1=C_S+C_{\perp}\), \(I=I^1+R\), nats/target | SAE-only prospective prediction, because B derivatives enter |

## 2. Anchor Link And Decision Point

The [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_10_shared_update_conditional_interference/17_10_shared_update_conditional_interference_anchor.md) asks whether controlled coupling and task rule determine the local consequence of a valid A update, with common-background correction as the strongest rival. The experiment's single next decision, already set in the [Focus](../../../../focus/focus_shared_update_conditional_interference.md), is whether the completed loss and mandatory SAE analyses justify a separate prospective SAE prediction test on untouched direction families. The researcher has not yet made the post-result judgment.

## 3. Protocol Freeze, Conformance, And Deviations

The final registration is [`R/registration.json`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/registration.json), SHA256 `ab201f81cdcfa9ff9b5be7e745d7125ffe4f7908df3d8727f1b479c8c397616c`, timestamp `2026-09-28T01:03:18Z`. It froze the approved common threshold, exact checkpoint hash, Protocol/config/Anchor/Focus, data asset and analysis source hashes before confirmation-family readout. The user explicitly approved the first-round loose threshold and four reserved H100 full execution.

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Checkpoint | S7 fresh, \(\lambda_{rec}=0.1\), exact 33B tokens | State SHA `c30b78e5...37b0803`; all workers report the same hash | PASS | `R/registration.json`; `R/workers/rank_*/receipt.json` | Eligible |
| Hardware and numerical path | One reserved four-H100 node; same replay path | ACP `pt-yzq8kkur` `SUCCEEDED`; four worker receipts; native adapter check passed | PASS | `R/environment.json`; `R/preflight.json`; execution certificate | Eligible |
| Calibration and basis | 256 fixed contexts, 4,096 positions, rank-16 orthogonal basis | 256/4,096; \(\|Q^TQ-I\|_F=1.15\times10^{-15}\) | PASS | `R/preflight.json`; `R/basis.npz` | Eligible |
| Joint feasibility | Independent W* witness, not main initial W | Both endpoints at 2 steps; minimum margin 8.3796 | PASS | `R/witness/receipt.json` | Eligible |
| Development | Four 11001–11004 families, all gates before confirmation | 4/4 complete; \(\epsilon_{repeat}=0\), \(\tau=10^{-7}\), remaining time qualified | PASS | `R/development_gate.json` | Engineering qualification only |
| Confirmation split and counts | 21001–21012, 96 gradients, 192 updates, 384 target cells | Exact counts, all 12 receipts complete | PASS | `R/measurement_complete.json` | Eligible |
| Source and initial-error guards | Each A update improves; A/B and high/low baselines comparable | Every registered source update improved; all verdict guards true | PASS | `R/analysis/verdict.json` | Eligible |
| Frozen analysis | Paired 2,000-draw hierarchical bootstrap and preregistered category | Frozen script completed with 2,000 saved indices | PASS | `R/analysis/bootstrap_indices.npz`; verdict | Eligible |
| SAE selector and guard | Same atom plus similar frequency/strength; separate structure set; task-signal error ≤0.5 | Selector passed and was independently recounted; task-signal error >0.5 in 12/12 | SELECTOR PASS / PROXY FAIL | `R/analysis/sae_atom_eligibility.csv`; SAE table | Primary loss eligible; SAE proxy inference not qualified |

**Amendments and retries:** Two earlier four-H100 jobs, `pt-haiy2hu9` and `pt-i0wsunn0`, failed in Stage 0 before basis/development/confirmation readout. Selected-position FP32 GEMM replay changed batch shape and exceeded an over-strict absolute element tolerance; full-shape native replay, selected-shape relative RMS and global reference relative RMS were independently qualified on local H100. The PyTorch Adam/Protobuf parser compatibility export was also added before this registration. Both failed run roots and `measurement_failed.json` files remain intact, have zero confirmation files and are **ineligible for any scientific aggregate**. The complete [execution record](full_execution_record.md) and Protocol amendment ledger specify each change. No scientific condition, checkpoint, SAE selector, seed, step, analysis or verdict rule was changed after confirmation readout.

**Post-measurement descriptive work:** `R/build_reading_figure.py` only plots the frozen verdict's registered \(M\) and high-overlap/reversed net loss; it does not recompute statistics. The reported common-span share of \(M\), atom-set overlap and paired-positive counts below are descriptive computations from frozen analysis tables, not preregistered selection or a new inferential test. No family was excluded.

## 4. Actual Setup

- **Input and task:** Internal vectors enter `model.blocks[7].attn.o.weight` (`1024 × 2048`) and retain the model's original fixed downstream path at one native residual position. Output rows `[100,101]` define two conditional classes, not text labels or full-vocabulary language-model loss. A's label follows balanced sign \(t\); B's input is identical in kept/reversed worlds and only its label rule changes.
- **Calibration:** `selected.jsonl` sorted by the frozen hash rule; 256 contexts × 16 positions yielded 4,096 native `c`, `a`, `x` observations. The basis SHA is `965827fc67577f2af311f0c723b94bc27483171a7d0eb13d58997cbcfbb04bbe`; \(\sigma=1.1543807900542906\). The natural corpus only fixes background and coordinates; it is not the outcome comparison.
- **Split:** Four development direction families 11001–11004. Twelve untouched confirmation families 21001–21012; per family/\(\rho\), 256 separate structure examples per group, four A batches of 128 records, 512 independent A readout records and 512 B readout records. Frozen `SeedSequence([20260927, family, split_code, repeat])` and per-array hashes are in `R/dataset_manifest.json`.
- **Intervention:** \(\rho\in\{0.1,0.8\}\), B rule kept or reversed, \(\varepsilon\in\{10^{-4},5\times10^{-5}\}\). One A gradient serves both B rules and both step sizes. Only a separate virtual \(\Delta W\) receives gradients; W and all other model/SAE tensors remain frozen. No persistent model-training trajectory or parameter-isolation comparison was run.
- **Cards:** rank0 families 21001–21003, rank1 21004–21006, rank2 21007–21009, rank3 21010–21012. Four GPU workers are execution shards, not independent statistical replications.
- **SAE:** Frozen 30,000-atom dictionary with Top-K 32 per record. Selection uses structure activations alone, capped at 32 atoms/family. B loss derivatives enter only after selection for signed attribution.
- **Numerical and uncertainty path:** FP32 replay and gradient, FP64 conditional CE readout, TF32 disabled; 2,000 paired hierarchical bootstrap draws over 12 families, source repeats and paired logical target examples, seed 20260928. The family is the top-level inference unit.

## 5. Metrics And Registered Decision Rules

The primary effect is \(I=L_B(W_0+\Delta W_A)-L_B(W_0)\). \(M>0\) means the flip-minus-keep difference grows with input-direction overlap. Support for **net help and harm** additionally required the high-overlap kept B interval wholly below \(-\tau\), high-overlap flipped B interval wholly above \(+\tau\), both amplification intervals above \(\tau\), and all guards. The frozen threshold is \(\tau=\max(10^{-7},20\epsilon_{repeat})=10^{-7}\), a numerical detection floor rather than a practical-effect threshold. Primary category follows Protocol §15.

The SAE proxy was to be read separately. A task-signal reconstruction relative-error median above 0.5 marks that family's task signal `SAE_SIGNAL_UNRESOLVED`, even if overall activation reconstruction is good. Static commonness, signed attribution and PCA/random controls do not themselves qualify prospective prediction or causal necessity.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Full measurement | All 12 families, 96 gradients, 192 updates, 384 cells | `R/confirm/f*`, worker receipts | `audit_full.py` frozen hash/schema/count audit | Exact census | 12/96/192/384 | ELIGIBLE | Complete | Does not itself interpret outcomes |
| Effective A source | Independent A change < \(-\tau\) per update and both-\(\rho\) CI upper < \(-\tau\) | `R/confirm/f*/rho*_rep*/step_*.npz` | `analyze_full.py` source arrays | 12 paired families, 2,000 draws | All 192 improvements; source CI upper < \(-\tau\) at both steps/\(\rho\) | ELIGIBLE | PASS | Local step only |
| Direction/rule modulation | Both \(M\) CI lower bounds > \(\tau\) | Same B arrays | Paired difference of differences | 2,000 hierarchical draws | `0.000152056` [`0.000136172`, `0.000167218`]; `0.0000760280` [`0.0000680777`, `0.0000836184`] | ELIGIBLE | Observed | Joint A/B direction construction, one checkpoint |
| Net harm | High-\(\rho\) flip \(I\) CI lower > \(\tau\) | Same B arrays | Same analysis | Same draws | `-0.00666488` [ `-0.00668001`, `-0.00664918` ]; `-0.00337798` [ `-0.00338554`, `-0.00337013` ] | ELIGIBLE | Absent | Mean net consequence; local positive components can remain |
| First-order adequacy | p90 \(|R|/|I^1|\) ≤0.1 where \(|I^1|>5\tau\); closure | Saved `I`, `I1`, `R` | Frozen verdict | All condition cells | p90 `0.0264163`; closure max `0` | ELIGIBLE | PASS | First order explains this local step only |
| Common SAE activation | Same atom, positive counts/ratios at both \(\rho\) | `R/confirm/f*/structure_*.npz`; candidates | Outcome-blind selector; independent recount in analysis | 12 families × 2 \(\rho\) | 32 selected/family, 32–36 eligible/family | ELIGIBLE as structure | Common activation observed | Marginal similarity does not ensure paired similarity or functional relevance |
| Task-signal proxy | Relative-error median ≤0.5 | SAE structure receipts | Paired \(t\)-difference reconstruction | One median per family | `1.0057–1.1589`, 12/12 fail | BOUNDED | Proxy unresolved | Overall reconstruction mean ≈0.10 does not repair it |
| Signed common contribution | \(C_S+C_\perp=I^1\), compared with same-rank controls | Saved `e`, `da`, common span | Frozen signed projection, descriptive difference of differences | Means over 12 families; no separate CI for component share | At `1e-4`, \(M_S=5.56e-6\), \(M_\perp=1.4653e-4\), \(M_R=-3.05e-8\) | DESCRIPTIVE | Common span carries ~3.65% of \(M\) | Proxy guard fails; B derivatives used; no causal atom claim |

Primary and SAE source tables: [`R/analysis/primary_by_condition.csv`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/primary_by_condition.csv), [`primary_by_family.csv`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/primary_by_family.csv), [`verdict.json`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/verdict.json), [`sae_atom_eligibility.csv`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/sae_atom_eligibility.csv), [`sae_reconstruction_checks.csv`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/sae_reconstruction_checks.csv), [`signed_decomposition.csv`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/signed_decomposition.csv).

## 7. Main Results

### Eligible primary loss comparison

| Step | Low kept \(I\) | Low flipped \(I\) | High kept \(I\) | High flipped \(I\) | \(M\), 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1e-4` | `-0.00674320` | `-0.00674147` | `-0.00681867` | `-0.00666488` | `0.000152056` [`0.000136172`, `0.000167218`] |
| `5e-5` | `-0.00341714` | `-0.00341627` | `-0.00345488` | `-0.00337798` | `0.0000760280` [`0.0000680777`, `0.0000836184`] |

All family-level \(M\) values were positive at both steps, but the registered inference is the paired family bootstrap, not a 12/12 sign count. High-overlap kept B helps more than low-overlap kept; high-overlap flipped B helps less than low-overlap flipped. Both simple amplification intervals are positive. Every B condition mean is negative, and the high-overlap flipped interval stays below zero. The near-linear halving of \(M\) across the two step sizes and first-order guard support local step interpretation without proving a training trajectory.

### SAE structure, change and loss relevance

The frozen selector found 32 atoms/family from 32–36 eligible candidates. Across families, 31 atom IDs appear in all 12 selected sets and only 33 distinct IDs appear in their union; this is a **post-measurement descriptive** set-overlap count. Across 768 selected atom/\(\rho\) rows, the median A/B positive-frequency ratio is 1.0 and median minimum positive-quantile ratio is 0.982; three rows have zero paired co-positive examples despite qualifying marginal distributions. Thus the approved loose operational definition is met, but it need not imply per-example matching. The representative paired scatter is only illustrative.

The overall activation reconstruction relative mean is approximately 0.10 in each family, while all 12 task-signal reconstruction medians lie in `1.0057–1.1589`. Hence the selected dictionary/SAE readout retains much of the shared background but fails to reconstruct the constructed sign-dependent change according to the frozen guard. The static selected count is 32 in every family, so selected-count versus family \(M\) Pearson correlation is undefined; [`sae_diagnostics.json`](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z/analysis/sae_diagnostics.json) labels other correlations exploratory, not predictive validation.

At `1e-4`, the descriptive mean signed decomposition of the **interaction** is \(M_{I^1}=1.52087e-4\), \(M_{C_S}=5.55642e-6\), \(M_{C_\perp}=1.46530e-4\), \(M_R=-3.0468e-8\), with exact closure within recorded precision. The common-span share of the observed \(M\) is ~3.65%; the same-rank PCA contribution is `5.1710e-6` and three same-rank random contributions are `4.49–4.63e-6`. The common span does not separate itself strongly from these controls in this descriptive comparison. At `5e-5`, the analogous common contribution is `2.7782e-6` and complement `7.3265e-5`. No component-level bootstrap test, intervention on atoms, held-out predictor or isolation-benefit experiment was registered.

### Ineligible and bounded evidence

The two earlier failed ACP attempts are engineering diagnostics only. Development families and the local H100 qualification are not included in the 12-family result. SAE signed attribution is bounded by the failed task-signal reconstruction guard; its exact calculation cannot promote the SAE to a valid predictor. The demonstration W* witness verifies joint realizability, not an outcome from W0.

## 8. Visualization Results

### Registered interaction and net B consequence

![Registered interaction and net B consequence](../../../../../../../daily_research_reports/backup/2026/09/0927/figures/shared_update_registered_contrast.png)

Source: frozen `R/analysis/verdict.json`, generated by `R/build_reading_figure.py`; 12-family paired hierarchical bootstrap, 2,000 draws. Left: \(M\), nats/target, with 95% intervals and detection threshold. Right: high-overlap/reversed B net loss change with interval and zero. Both \(M\) intervals are above threshold, while both net changes are below zero. The plot cannot show natural data interference or attribute the effect to SAE atoms.

### SAE proxy qualification

![SAE proxy qualification](../../../../../../../daily_research_reports/backup/2026/09/0927/figures/shared_update_sae_proxy_qualification.png)

Source: `R/analysis/sae_reconstruction_checks.csv`, built by frozen `plot_full.py`. The upper panel is selected atom count; the lower panel contrasts overall activation reconstruction error with paired task-signal error across 12 families, with the prespecified 0.5 proxy line. It shows why excellent overall reconstruction cannot substitute for task-signal preservation; it does not show prediction or causality.

### Signed decomposition and activation examples

![Signed decomposition](../../../../../../../daily_research_reports/backup/2026/09/0927/figures/shared_update_signed_decomposition.png)

Source: `R/analysis/signed_decomposition.csv`, frozen `plot_full.py`; means over all 12 families at `1e-4`. Orange is selected common span, blue its complement, gray finite-step remainder, black cross actual \(I\). These are signed contributions to average loss change, with B derivatives; they do not by themselves identify a necessary atom or a useful separator. [Illustrative paired activation scatter](../../../../../../../daily_research_reports/backup/2026/09/0927/figures/shared_update_sae_activation_similarity.png) uses three selected atoms from family 21001, not an outcome-based chosen sample.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it establishes | Remaining uncertainty |
| --- | --- | --- | --- | --- |
| Stage 0 native path | `R/preflight.json`, 256/4,096 calibration, same-shape check | PASS | Exact checkpoint, true SAE observation point, replay and native tail qualified | Scope is one local reference background |
| Stage 1 construction | basis, manifest, W* witness | PASS | Orthogonal controlled signals and a jointly feasible target under fixed downstream function | W* may be distant from W0 |
| Stage 2 development | four receipts and `development_gate.json` | PASS | Finite updates, normalization, repeat floor, runtime | Development is engineering only |
| Stage 3 confirmation | 12 family receipts and independent auditor | PASS | No missing families/conditions, frozen tensors unchanged | Does not decide scientific branch alone |
| Stage 4 primary | frozen bootstrap verdict | `MODULATION_WITHOUT_NET_HARM` | Qualified rule-dependent modulation and absent net harm | Source of broad net help remains a live explanation |
| Stage 4 SAE | common selector, reconstruction, signed controls | PROXY UNRESOLVED | Common activation exists; task signal not faithfully reconstructed | SAE prospective prediction and causal necessity not tested |

The data/construction, numerical adapter and implementation gates did not fail on the completed run. The strong physical prediction of **net harm** failed in this carrier; the weaker rule-dependent modulation is observed. The most immediate representation bottleneck is a **proxy failure**, not absence of common SAE activation. Common-background correction remains a plausible rival explanation for broad help; this experiment did not intervene on that background alone. These are bounded interpretations, pending researcher judgment.

## 10. Full Experiment Record — 2026-09-28 Round

1. **Question/hypothesis:** Does increasing controlled task-direction overlap enlarge the kept-versus-reversed B-loss contrast after a normal A update, and does the updated task signal lie in similarly activated common SAE directions?
2. **Setup/controls:** Exact S7 33B checkpoint, frozen model/SAE, 16-dimensional native calibration basis, crossed \(\rho\) and B rule, two registered step sizes, paired inputs; W* witness separate from W0. Four H100 reserved workers each owned full direction families.
3. **Data:** 256 deterministic natural calibration contexts; generated development, structure, source and source/B readout samples with disjoint split codes and manifest hashes. No natural-domain outcomes were used to select conditions.
4. **Test/confirmation:** Four development families 11001–11004 for gates, then untouched confirmation families 21001–21012. Twelve families, four source repeats/\(\rho\), two step sizes, paired B rules. 2,000 fixed hierarchical bootstrap draws.
5. **Result:** ACP `pt-yzq8kkur` and full auditor succeeded; \(M\) positive at both steps, high-overlap flipped B loss negative at both; registered category `MODULATION_WITHOUT_NET_HARM`. All 12 SAE task-signal proxy guards failed despite selected common atoms. Evidence is in Sections 6–8 and the manifest below.
6. **Insight/boundary/decision:** This constructed task shows modulation of benefit without net interference. Similar common SAE activation is insufficient here to reconstruct task signal or establish prediction. The researcher must decide whether to attempt a separately frozen prospective SAE test after addressing the proxy guard; no human post-result judgment has been recorded yet.

## 11. Interpretation

**Observation:** A-only ordinary updates reduced A loss, and all four B condition means also fell. Higher overlap increased the reversed-minus-kept difference, but the reversed condition remained beneficial in absolute terms. The selected SAE atoms have similar A/B activation by the approved marginal rule; most of the signed interaction falls outside their span, and paired task-signal reconstruction fails.

**AI interpretation, pending researcher review:** A large common background improvement may dominate the smaller rule-dependent transfer, explaining why an interaction occurs without net harm. The SAE selection preferentially captures stable shared background activity rather than the constructed sign-dependent variation. Alternative explanations include the particular W0 operating point, the internal vector task, the chosen output rows, local step sizes and the SAE's coding limits. The current measurements do not isolate one of these as cause.

## 12. Claim Boundary

**Can claim:** At this exact checkpoint and construction, direction overlap modulates the rule-dependent **amount of help** from an effective A update to B. The approved loose SAE common rule selected similarly activated atoms, but this SAE's task-signal reconstruction failed its registered guard.

**Cannot claim:** Net interference, natural-domain conflict, long-term shared-training cost, fixed-A-gradient causal effect of overlap, SAE atom causation, prospective SAE prediction or parameter-isolation benefit. The 12 families are not 12 independently trained models; static activation, change and signed loss consequence remain distinct.

## 13. Next Decision

**Researcher-owned decision:** Whether the completed loss result and failed SAE proxy justify a separate prospective SAE prediction test on untouched families. **AI_PROPOSAL:** require an outcome-blind proxy that passes the same task-signal guard before freezing such a prediction test; otherwise stop or redesign the SAE proxy branch. Completion requires the researcher's judgment and, if proceeding, a new frozen predictor/holdout rule. Resume action is conditional on that decision; current 12 families are already read and cannot be repurposed as prospective holdout.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Protocol](protocol.md) | Frozen scientific and execution rule | Registered 2026-09-28 | Focus, Anchor | `f8032e8e...9ed92ae861932a49ed3f9` | Yes | Contract | Stage-0 engineering amendments pre-confirmation |
| `R/registration.json` | All frozen source and asset hashes | `prepare_full.py` | Protocol/config/checkpoint/data | `ab201f81...c397616c` | Yes | Provenance | Approved threshold and exact 33B state |
| `R/measurement_complete.json` | Completeness/auditor certificate | `audit_full.py` | 12 raw family trees | `e3ee7916...7bd102f26` | Yes | Eligibility | 6.56 GB raw, under 30 GB budget |
| `R/analysis/verdict.json` | Primary registered statistics and guards | Frozen `analyze_full.py` | Raw B/A arrays | `4d3950d4...6eb080` | Yes | Primary | 2,000 saved bootstrap indices |
| `R/analysis/primary_by_family.csv` | Paired 12-family values | Frozen analysis | Raw B arrays | `d9c59c20...b725` | Yes | Primary | Both steps, no exclusions |
| `R/analysis/sae_atom_eligibility.csv` | All candidate thresholds and selected IDs | Frozen analysis recount | Structure receipts | `R/analysis/sae_atom_eligibility.csv` | Yes | Structure only | Outcome-blind selection |
| `R/analysis/sae_reconstruction_checks.csv` | Overall versus task-signal guard | Frozen analysis | Structure receipts | `17e182a7...0301e` | Yes | Bounded SAE | 12/12 signal guard fail |
| `R/analysis/signed_decomposition.csv` | Signed span, complement, controls | Frozen analysis | `e`, `da`, common span | `2f970e6a...2ad6dc2` | Yes | Descriptive | Uses B derivatives |
| [Date figure sources](../../../../../../../daily_research_reports/backup/2026/09/0927/figures/SOURCES.md) | Portable curated reading figures | Frozen plots plus presentation-only contrast plot | Verdict and SAE tables | Individual SHA256s in source ledger | Yes | Derived only | Byte-identical copies; raw arrays stay execution-side |
| [Full execution record](full_execution_record.md) | Jobs, stage failures and amendments | Current conversation | ACP and run roots | Job IDs `pt-haiy2hu9`, `pt-i0wsunn0`, `pt-yzq8kkur` | Yes | Prior jobs no; current job yes | Failure artifacts preserved |

## 15. Links And Final Audit

- Anchor: [anchor.md](../../../../problem_anchors/17_shared_and_interference_learning/17_10_shared_update_conditional_interference/17_10_shared_update_conditional_interference_anchor.md); Focus: [focus card](../../../../focus/focus_shared_update_conditional_interference.md); Protocol: [protocol.md](protocol.md); Summary: [English](summary.md), [Chinese](summary_cn.md).
- Code: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/scripts/`; run, logs, arrays, analysis and evidence figures: `R` defined above. Checkpoint SHA is in registration and every worker receipt. Reproduce the fixed CPU analysis only from a fresh analysis directory with `python scripts/analyze_full.py --run-root R`; do not overwrite this run's analysis.
- Eligibility audit: **PASS** for full measurement and registered primary comparison; **PASS** for transparent pre-confirmation engineering deviations; **FAIL** for SAE task-signal proxy; **PENDING** for human result interpretation, Anchor/Focus promotion and any future scientific decision. The present report is a factual result draft, not the researcher's confirmed conclusion.
