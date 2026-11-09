# Detailed: A15_13_E19 A/B Paired Router-Input Readout Re-audit

Primary Anchor: [A15_13_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), frozen run copy SHA-256 `7f5d65afff810dc7d15039df6a869eb4afc6d014b010e3cb5bab13d45d576b40`  
Summary: [summary.md](summary.md)  
Result eligibility: full static execution complete; registered typed result `QUALIFICATION_FAILED`; representation observations are bounded; functional launch `NOT_RUN`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

Purpose: re-audit layerwise label accessibility at the exact Router input A and compare it with MLP input B under a paired two-seed contract.  
Hypothesis: A contains a qualified, seed-stable joint parent/child linear-readability plateau; the strongest rival is a wrong-site, single-seed, packed-window, or shuffled-null artifact.  
Experiment logic: reconstruct article provenance and validate A/B tensors, run four full A/B-seed workers, apply the A-only point selector and 2,000 component resamples, then apply every hard guard before any functional launch.  
Direct result: point estimates gave A primary `10` and descriptive set `{0,10,13}`; 5 of 16 shuffled-label checks failed.  
Eligibility: tensor, identity, completion, finite, reload, and base-freeze guards pass; the global candidate qualification fails.  
Verdict: `QUALIFICATION_FAILED`; `functional_launch_authorized_by_review=false`.  
Claim boundary: static representation readability only; no functional Router or expert conclusion.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Site A | Tensor read by the maintained Router | Forward input to zero-indexed Transformer block \(\ell\) | `[token,1024]` | Only site allowed to select functional candidates | That a learned Router can exploit it |
| Site B | Within-block comparison tensor | MLP forward input after attention residual addition and normalization | `[token,1024]` | Tests whether the old block-9 finding came from a later tensor | Authorization to change Router input |
| Parent task | Three coarse M2D2 domains | One linear or fixed nonlinear `1024→3` head per layer | balanced window CE / accuracy | Coarse-label accessibility | Transferable coarse abstraction |
| Conditional child | Three children within the true parent | Three parent-specific `1024→3` heads per layer | balanced window CE / accuracy | Fine-label accessibility without a parent-routing error | End-to-end hierarchical routing |
| Recovery | Fraction of across-layer CE improvement captured at one layer | \((\log3-\mathrm{CE}_\ell)/(\log3-\min_m\mathrm{CE}_m)\) | ratio | Defines the frozen onset rule | Absolute task quality or causal use |
| Article component | Windows connected by any shared source article | Connected component within an M2D2 cell | component | Resampling unit for packed dependence | High effective sample size when one component dominates |
| Historical confirmation | Previously viewed held-out split | 512 windows per child from the frozen dataset | split | Robustness bridge | New untouched confirmation |

## 2. Anchor Link And Decision Point

The Anchor asks whether the exact Router input A contains a qualified joint parent/child readability onset. E19 is the minimum falsifier because the former E15 evidence used only B and one probe seed and was already `UNQUALIFIED_SHUFFLE_CONTROL`. The pre-authorized branch was binary: all gates pass and exactly three A layers enter a separate A15.15 Protocol, or any gate fails and the functional launch stops without changing criteria.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| Approval and freeze | Full static scope approved; scientific body frozen before first E19 optimizer update | Frozen Protocol copied into replacement run before full updates | PASS | `receipts/protocol_frozen.md`, SHA above | Eligible |
| Read sites | A=block input; B=post-attention normalized MLP input; distinct tensors | Shapes both `[28,2,192,1024]`; mean/max absolute A-B difference `1.652788/424.40625` | PASS | `preflight/tensor_contract.json` | Eligible |
| Causal prefix | Future suffix perturbation cannot change earlier captured prefixes | Maximum A/B prefix change both `0.0` | PASS | tensor contract | Eligible |
| Base freeze | Zero trainable base parameters; unchanged identities | `0`; all four identity checks pass; model/data/config hashes unchanged | PASS | worker `provenance.json`, candidate review guards | Eligible |
| Data identity | Frozen M2D2 `3×3` tensor SHA-256 `8cd04d…51a8` | Exact match | PASS | worker provenance | Eligible |
| Article reconstruction | Every stored window and selected record recoverable; zero known cross-split title/content overlap | Ambiguous occurrences `0`; all overlap lists empty | PASS | `preflight/article_manifest.json` | Eligible, with component-count limitation |
| Full worker matrix | A/B × seeds 170903/170907 | 4/4 full workers, each three passes and `768` optimizer updates | PASS | full logs, resume checkpoints, result JSON | Eligible |
| Paired training | Same data, initialization tensors, order, optimizer, mask, and budget within seed | Initialization/identity guards pass for all workers; frozen config identical except site/seed | PASS | worker guards and provenance | Eligible |
| Finite/reload | Finite losses and gradients; exact reload | All four pass; reload maximum absolute difference `0.0` | PASS | worker guards and provenance | Eligible |
| Candidate selector | A-only, two-seed development point rule | Primary `10`, seed primaries `10/10`, shallow `0`, deep `13`; B and nonlinear unused | PASS | `analysis/candidate_review.json` | Descriptive set exists |
| Component resampling | 2,000 paired resamples, seed 20260908 | Completed on development and historical confirmation | PASS | candidate review and `candidate_bootstrap.csv` | Bounded by giant components |
| Null qualification | Every site×seed×split×task check passes | 11/16 pass; 5/16 fail | **FAIL** | `shuffle_qualification.csv` | Global candidate set ineligible |
| Functional handoff | Only `QUALIFIED` can launch A15.15 | Review authorization false; no functional Protocol/job submitted | PASS | candidate review; ACP job list for this execution | Correct stop branch |
| Resource ceiling | One reserved node, 4×H100, zero retries, ≤1 h / 4 GPU h | Replacement `pt-0bisktrz`, reserved `n6ls.iu.i40.4`, 4×H100, retries 0, 7m47s control-plane runtime | PASS | ACP control-plane record | Within ceiling |

Frozen Protocol revision: run copy at `2026-09-07T04:37:14Z`, SHA-256 `7f5d65…76b40`.  
Execution scope approved: implementation, tests, provenance reconstruction, smoke, one static 4×H100 job, candidate review, and bounded result record.  
Amendments: none to the scientific body.  
Retries and exclusions: first job `pt-jkkuglxx` failed at `2026-09-07T04:33:17Z` before any probe update because worker-local `logs/` directories did not exist. It produced no decision evidence. The directory and reload-path defects received regression tests; local H100 smoke passed. Replacement job `pt-0bisktrz` used the identical scientific contract and completed with platform retry count `0`.  
Missing conditions or artifacts: no static condition is missing. There is no functional job, functional update, or functional checkpoint because the hard stop fired.  
Post-hoc analyses: the three curated figures and CSV tables merely render registered metrics from the immutable candidate review. Inherited sample-fragility and leave-child-out fields present in worker outputs are secondary/debug evidence and do not affect E19 qualification.

## 4. Actual Setup

Research question: at which block does true parent and conditional-child information become jointly and stably linearly readable at site A, and does this survive the frozen qualification gate?  
Data construction and provenance: frozen M2D2 Wikipedia `3×3`; stable-hash selected articles are tokenized, concatenated with EOS, and packed into 256-token windows. E19 exactly reconstructed every stored window and retained all contributing source article identities and offsets.  
Train / development / confirmation split: per child, train `1,024`, development `256`, historical confirmation `512` windows. The confirmation split was previously viewed and is not independent new confirmation.  
Learning task and permitted supervision: probes receive true parent or true-parent-conditioned child labels; the base, LM head, Router, and experts receive no updates. Input positions 63--254 predict labels attached to windows whose next-token positions are 64--255.  
Model / architecture / algorithm: Qwen3-0.6B-Base, 28 blocks, width 1,024; per-layer linear heads and fixed two-layer `1024→32→3` GELU diagnostic; independent fixed-shuffle heads.  
Input representation / position encoding: current-token hidden tensors at A or B; no future token is permitted to change captured prefixes.  
Training objective and constraints: supervised three-way cross-entropy, balanced four windows per each of nine cells per update; non-finite values hard-fail.  
Optimizer or update rule: AdamW, linear LR `1e-3`, nonlinear LR `3e-4`, weight decay `1e-4`, no scheduler or early stopping.  
Training steps / tokens / batch size: three full passes, batch 36, `256` updates per pass, `768` optimizer updates per worker; four full workers.  
Checkpoints: atomic resume after each update plus final heads; final update only. Every resume checkpoint reports `next_epoch=3`, `next_step=0`.  
Seeds: probe initialization/order `170903/170907`; fixed shuffle `170905`; component bootstrap `20260908`.  
Conditions and plain-language labels: Router input A and MLP input B, each under two independent probe seeds; each worker fits real linear, shuffled linear, and real nonlinear heads.  
Changed variables: site A versus B and probe seed.  
Held fixed: model/data, labels, window order within seed, paired initialization tensors within seed, head class, optimization budget, mask, aggregation, and thresholds.  
Code / config / data identities: paired worker SHA-256 `1babc251…3cd`; analyzer `0d2f81dc…767`; frozen data `8cd04d99…51a8`; model weights `cd2a5120…3eba`; worker-recorded imported audit code `34a626f4…3d5`.  
Script and result paths: execution root and immutable full-run root are listed in Sections 14--15.  
Known setup limitations: packed streams create giant connected components; confirmation cell 5 has one component and several other cells only 2--3. Resampling correctly preserves dependence but can have low information. The Protocol did not register a minimum component-count gate, so this is a limitation rather than an added post-hoc failure. The nonlinear diagnostic uses one fixed optimization contract and is not proof of the global best nonlinear classifier.

## 5. Metrics And Registered Decision Rules

1. For each site, task, seed, and layer, balanced CE is averaged over prediction positions within a window, windows within each cell, then equally across nine cells. Accuracy uses the same weighting.
2. Recovery is \(R_\ell=(\log3-\mathrm{CE}_\ell)/(\log3-\min_m\mathrm{CE}_m)\). Non-positive denominators reject the candidate.
3. At A, \(J^s_\ell\) is the smaller parent/child recovery. The primary is the earliest three-layer run with the two-seed mean \(J\ge0.95\); seed primaries must differ by at most two blocks. Shallow/deep references follow the frozen distance and extremum rules.
4. Each null row passes only if shuffled median accuracy is in `[0.28,0.39]`, shuffled median CE is within `0.05` nat of \(\log3\), and no three-layer shuffled onset exists.
5. `QUALIFIED` requires every guard. One failure yields `QUALIFICATION_FAILED`; B, nonlinear, or historical confirmation cannot rescue A.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| A descriptive candidate set exists | A-only development selector | four development result JSON/NPZ files | `analyze_paired.py` SHA `0d2f81dc…767` | point curve plus two-seed rule | `{0,10,13}`, primary `10`, seed gap `0` | BOUNDED | Candidate existence passes | Global qualification fails |
| A onset is later than B under this probe | paired A/B real-label metrics | A/B development and confirmation result files | matched per-seed CE/recovery curves | seed-specific and two-seed descriptive means | A `10`; B `9`, both tasks/splits/seeds | BOUNDED | One-block site difference | Representation comparison, not intervention |
| Null gate fails | 16 null rows | worker shuffled metrics | frozen median accuracy/CE/onset checks | no averaging across rows | 5 failed rows | ELIGIBLE decision evidence | `QUALIFICATION_FAILED` | Does not erase real-label readability |
| Article identities are traceable | exact reconstruction and zero cross-split reuse | `article_manifest.json` SHA `7e4b29ab…9958` | stable reconstruction and overlap audit | article/component enumeration | 0 ambiguous; 0 title/content overlaps | ELIGIBLE guard | PASS | Several cells have tiny component counts |
| Component-selector robustness is limited but centered at the point candidate | 2,000 paired resamples | per-window NPZ plus article manifest | connected components resampled within cell | selection rate counts missing-candidate draws as unselected | A two-seed block 10 selection `0.7195` development, `0.9670` confirmation; selected-layer quantiles `[10,10]` | BOUNDED | Consistent selected layer when selected | Development has `28.05%` no-candidate resamples |
| Nonlinear probe shows no reproducible earlier A onset | fixed nonlinear real-label heads | nonlinear arrays in result JSON | compare CE and frozen three-layer onset | both seeds separate; mean shown only descriptively | block-10 gains dev `0.008301/0.004896`, conf `0.008019/0.005395`; A onset parent `10/10`, child `10/21` | BOUNDED | No earlier nonlinear-only support | Not a universal nonlinear-capacity bound |
| Functional training must not start | every gate must pass | candidate review SHA `31aa761f…69a7` | registered boolean handoff | none | `functional_launch_authorized_by_review=false` | ELIGIBLE decision evidence | `NOT_RUN` | Functional science remains unknown |

## 7. Main Results

### 7.1 Eligible decision evidence

The completed candidate review contains all four worker guards, both splits, both sites, both seeds, article-component resampling, and 16 null rows. Its `status` is `QUALIFICATION_FAILED`; the pipeline completion receipt has `analysis_exit_code=3`, `scientific_review_status=QUALIFICATION_FAILED`, and `status=COMPLETE`. Exit code 3 is the registered scientific failure code, not an engineering crash.

The five null failures are exactly the five rows in [shuffle_qualification.csv](tables/shuffle_qualification.csv): A/170903 child CE on both splits, B/170903 child CE on historical confirmation, and B/170907 parent accuracy on both splits. All shuffled stable-layer fields are `null`, but the conjunction still fails.

### 7.2 Bounded representation evidence

For every split and seed, A linear parent and child onsets are both `10`; B onsets are both `9`. At the development point estimate, mean A joint recovery is `0.892348` at block 9, `1.000000` at block 10, `0.982995` at block 11, and `0.971277` at block 12. This satisfies the point selector at 10. The historical confirmation arrays show the same onset, but that split cannot be called newly independent.

The article-component bootstrap selects A block 10 in `1439/2000` development resamples and `1934/2000` historical-confirmation resamples; in the remaining resamples no A two-seed candidate exists. Conditional on selection, all selected development and confirmation candidates are block 10. This supports location consistency but exposes weaker selection existence under development component resampling.

### 7.3 Nonlinear audit

At site A, the fixed nonlinear diagnostic remains close to the linear head around block 10:

| Split | Task | Linear mean CE at 10 | Nonlinear mean CE at 10 | Linear minus nonlinear | Nonlinear stable onset by seed |
|---|---|---:|---:|---:|---|
| Development | Parent | `0.508652` | `0.500351` | `0.008301` | `10 / 10` |
| Development | Conditional child | `0.428810` | `0.423914` | `0.004896` | `10 / 21` |
| Historical confirmation | Parent | `0.520651` | `0.512632` | `0.008019` | `10 / 10` |
| Historical confirmation | Conditional child | `0.414201` | `0.408806` | `0.005395` | `10 / 21` |

Site B nonlinear onsets are `9/9` for both tasks, splits, and seeds. Because the nonlinear child onset at A moves to 21 under seed 170907 rather than earlier than 10, E19 supplies no reproducible evidence that linear capacity hid an earlier A-site transition. The nonlinear result remains diagnostic and cannot alter the A linear candidate or repair the null gate.

### 7.4 Stage-level and debug-only evidence

All worker finite, shape, identity, reload, and base-freeze guards pass. The inherited per-position diagnostics keep A seed 170903 and 170907 linear onsets at 10 across early/middle/late bins. Inherited sample-budget and leave-child-out outputs are not registered E19 decision criteria and are retained only in worker artifacts.

### 7.5 Ineligible, missing, and not-run evidence

- The failed first job has no probe update and no development or confirmation result; it is ineligible engineering evidence.
- The descriptive candidates `{0,10,13}` are not eligible for A15.15 launch because the null conjunction failed.
- Functional conditions, optimizer updates, checkpoints, five-minute checks, ETA, and functional conclusions are `NOT_RUN` / not applicable.

## 8. Visualization Results

### Paired A/B linear recovery

![Paired A/B linear recovery](figures/01_ab_linear_recovery.png)

Purpose: locate the site-specific linear onset.  
Setup: A/B matched real-label heads; two seeds; development and historical confirmation.  
Metric definition and unit: recovery ratio, two-seed mean with seed range.  
Raw source and lineage row: candidate review `readout`; Lineage row 2.  
Aggregation and uncertainty: balanced CE per seed, then descriptive seed mean/range.  
How to read: red B reaches the three-layer 0.95 rule at 9; blue A reaches it at 10.  
Expected under registered outcomes: a qualified A plateau plus all independent guards.  
Observed result: descriptive A/B onsets 10/9.  
Take-home: the old B finding is one block earlier than the maintained Router input A.  
Remaining uncertainty: global qualification and effective component count.  
What this figure does not prove: causal use or the value of changing Router input.  
Anchor update implication: A block 10 is descriptive only.

### Fixed nonlinear diagnostic at A

![Linear versus nonlinear A-site readout](figures/02_a_linear_vs_nonlinear.png)

Purpose: test whether the fixed nonlinear head reveals an earlier transition missed by the linear head.  
Setup: matched real-label A heads, two probe seeds.  
Metric definition and unit: balanced CE in nats, lower better.  
Raw source and lineage row: candidate review `readout`; Lineage row 6.  
Aggregation and uncertainty: two-seed descriptive mean and seed range.  
How to read: curves nearly overlap around block 10; the nonlinear late-layer CE advantage grows, but onset is not earlier.  
Expected under the rival: a stable nonlinear onset clearly before the linear onset.  
Observed result: parent 10/10 and child 10/21 across seeds.  
Take-home: no reproducible earlier nonlinear-only onset is observed.  
Remaining uncertainty: one fixed width, optimizer, and budget do not exhaust nonlinear readouts.  
What this figure does not prove: absence of all nonlinear semantic structure.  
Anchor update implication: retain linear Router-readability boundary.

### Shuffled-label qualification

![Shuffled-label qualification](figures/03_shuffle_qualification.png)

Purpose: show the decisive hard-gate failure.  
Setup: all 16 site×seed×split×task null rows.  
Metric definition and unit: shuffled median CE minus \(\log3\) in nats; red means any registered null component failed.  
Raw source and lineage row: `shuffle_qualification.csv`; Lineage row 3.  
Aggregation and uncertainty: median across layers per row; no pooling across rows.  
How to read: three red rows exceed the CE band; two other red rows are inside the CE band but fail the separate accuracy band.  
Expected under qualification: all rows green and no shuffled stable onset.  
Observed result: 5/16 fail.  
Take-home: the global qualification fails.  
Remaining uncertainty: cause of null miscalibration.  
What this figure does not prove: absence of real-label readability.  
Anchor update implication: stop the functional handoff.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
|---|---|---|---|---|---|
| Object/data contract | exact A/B tensor checks, causal prefix, hashes, article reconstruction | PASS | none | Wrong tensor alias, base training, known cross-split reuse | Low effective component count |
| Four paired workers | 4/4, 768 updates each, finite/reload/frozen guards | PASS | none | Missing seed or incomplete probe run | Probe-family generality |
| Point selector | A `{0,10,13}`, primary 10, seed gap 0 | PASS as descriptive computation | none | One-seed-only onset | Bootstrap candidate nonexistence in some resamples |
| Nonlinear diagnostic | no reproducible earlier A onset | BOUNDED | seed170907 child onset 21 | Simple claim of a hidden earlier nonlinear-only transition | Other nonlinear capacities/budgets |
| Null qualification | 5/16 failed | **FAIL** | three CE-band and two accuracy-band failures | Qualified layer handoff | Cause of null behavior |
| Functional handoff | not submitted | PASS as stop behavior | hard gate fired | Accidental bypass | All functional questions remain unknown |

Falsified physical prior: not adjudicated as a scientific generalization; the A point curve is readable, but qualification fails.  
Falsified mathematical model: the selector computation works; no failure of the recovery formula is observed.  
Falsified operationalization / proxy: the frozen null qualification rejects this probe outcome, so it cannot operationalize an approved functional candidate here.  
Falsified implementation: no; all required guards and local tests pass after the pre-update directory defect was repaired.  
Falsified metric: not established; changing the null rule post hoc is forbidden.  
Remaining rival explanations: null-head optimization/calibration, packed-component dependence, and the possibility that this probe contract is not a reliable functional-candidate gate.

## 10. Full Experiment Record

| Event | UTC time | Record |
|---|---|---|
| First job submitted | `2026-09-07T04:31:37Z` | `pt-jkkuglxx`, reserved 4×H100, zero retries |
| First job started / failed | `04:32:24Z` / `04:33:17Z` | pre-update directory error; no scientific output |
| Regression tests and local H100 smoke | before replacement | 9 tests pass; smoke status PASS |
| Replacement submitted / started | `04:36:33Z` / `04:36:55Z` | `pt-0bisktrz`, same frozen scope |
| Tensor preflight complete | `04:37:39Z` | PASS |
| Four full workers complete | approximately `04:43:23--04:43:27Z` | 4×768 updates, all result artifacts present |
| Candidate review complete | `04:43:46Z` | analysis exit 3, registered qualification failure |
| ACP terminal state | `04:44:42Z` | `SUCCEEDED`, retries 0 |

Operational completion and scientific qualification are different: the replacement ACP job succeeded and the requested static matrix is complete, while the scientific handoff gate failed.

## 11. Interpretation

Observation: A has a point-estimate joint linear onset at 10 and B at 9; the nonlinear diagnostic does not consistently move A earlier; five null rows fail.  
Interpretation: the within-block site difference plausibly explains why the old site-B audit nominated block 9, but the current null behavior prevents treating A block 10 as a qualified insertion layer.  
Claim: this execution supports only a bounded descriptive A/B readability comparison and the registered negative qualification decision.  
Speculation: the null failures may reflect idiosyncratic shuffled-head optimization or a mismatch between a layer-median null rule and the paired-seed design; E19 does not distinguish these causes.  
Boundary: no functional model was trained, so expert usefulness and task gain remain unknown.

## 12. Claim Boundary

Can claim: four complete frozen-base paired workers find A/B linear onsets `10/9`; A point candidates are `{0,10,13}`; the fixed nonlinear A readout is not reproducibly earlier; five frozen null checks fail, so qualification fails.

Cannot claim: qualified candidate layers, a new independent confirmation, a universal semantic-formation depth, an architecture change from A to B, online Router competence, expert specialization, intervention utility, or next-token improvement.

## 13. Next Decision

Decision: `STOP_NO_FUNCTIONAL_LAUNCH`, the branch already confirmed in the execution request.  
Completion criterion: complete static artifacts plus a candidate review naming all failed gates and no unauthorized functional submission; met.  
Resume action: `UNKNOWN` until the researcher confirms this result boundary and owns a new next decision.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|---|---|
| Frozen run Protocol | prove pre-result contract | pipeline copy | canonical Protocol | SHA `7f5d65af…76b40` | yes | yes | immutable run copy |
| Article manifest | identity, offsets, overlap, components | `build_article_manifest.py` | raw M2D2 source + processed tensor | SHA `7e4b29ab…9958` | yes | yes | 14.5 MB |
| Tensor contract | A/B site and causal-prefix guard | `tensor_contract.py` | model + two dev windows | status PASS | yes | yes | base trainables 0 |
| Four worker result sets | real/shuffle/nonlinear metrics and heads | `paired_worker.py` + imported audit code | frozen model/data/config | A/B × 170903/170907 | yes | bounded/yes by row | 768 full updates each |
| Candidate review | registered selector and qualification | `analyze_paired.py` | four worker sets + manifest | SHA `31aa761f…69a7` | yes | yes | authoritative review |
| Pipeline receipt | completion and analysis code | pipeline | candidate review | `COMPLETE`, analysis exit 3 | yes | yes | scientific failure is intentional code 3 |
| Curated CSV tables | readable transformations | `render_canonical.py` SHA `a5ad3f3d…e359b` | candidate review | files under `tables/` | yes | yes, derived | no new decision rule |
| Curated figures | compact visual reading | same | curated CSV/review | files under `figures/` | yes | yes, derived | figure contracts saved |
| Failed-job run root | engineering failure record | first ACP job | same code before directory fix | `full-20260907T043136Z` | partial | no | no probe update |
| Functional artifacts | would record A15.15 training | not produced | qualification required | `NOT_RUN` | no | no | correctly absent |

## 15. Links

anchor: [A15_13_07 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md)  
protocol: [protocol.md](protocol.md)  
summary: [summary.md](summary.md)  
code workspace: `/data/250010109/MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/`  
runner: `/data/250010109/MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/run_pipeline.sh`  
config: `/data/250010109/MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/paired_contract.py`  
data / manifest: `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`; `runs/full-20260907T043632Z/preflight/article_manifest.json`  
result dir: `/data/250010109/MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/runs/full-20260907T043632Z/`  
figure dir: [figures](figures)  
logs / checkpoints: `runs/full-20260907T043632Z/logs/`; `runs/full-20260907T043632Z/workers/*/checkpoints/`  
repro command: `RUN_STAMP=<stamp> RUN_ROOT=<persistent-run-root> timeout --signal=TERM 3600s bash run_pipeline.sh`  
job ids: failed engineering job `pt-jkkuglxx`; completed static job `pt-0bisktrz`; functional job `NOT_SUBMITTED`.
