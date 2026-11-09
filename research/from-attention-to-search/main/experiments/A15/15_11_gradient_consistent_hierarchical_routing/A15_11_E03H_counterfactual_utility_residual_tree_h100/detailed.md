---
experiment_id: A15_11_E03H_counterfactual_utility_residual_tree_h100
status: EVIDENCE_COMPLETE
interpretation_status: HUMAN_CONFIRMED_AS_NON_OWNING_H100_SENSITIVITY
eligibility: E03H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY
completed: 2026-08-29
acp_job: pt-vkikyszj
run_stamp: 20260829T172910Z
resource_profile: h100-4-reserved
---

# Detailed: Counterfactual Utility In A Progressive Residual Expert Tree

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)

Frozen Protocol and registered revision: [protocol.md](protocol.md), SHA-256
`5b0e8163ec831d7cbea81385056e2930e00e439226ad2c1176024cc90bcc59fa`,
scientific body frozen at `2026-08-29T16:18:22Z`

Summary: [summary.md](summary.md)

Result eligibility: `ELIGIBLE`; ACP job `pt-vkikyszj` succeeded, the E03
producer audit passed, and the global evidence-chain audit passed. The
researcher accepted the bounded interpretation as non-owning H100 sensitivity
evidence.

## 0. Quick Recap

- **Purpose:** test whether a supplied correct parent-first factorization makes
  progressive residual MoE training more efficient than a matched flat
  nonlinear Router, and whether direct current-candidate utility labels add
  value.
- **Hypothesis:** the task-only hierarchy should separate work from fail; in
  work, utility supervision and/or the tree bias should produce positive
  registered AULC contrasts against matched controls.
- **Direct result:** the analytic and learned work/fail mechanism passed. The
  tree did not beat the flat task baseline, and utility supervision did not
  beat task-only supervision in either architecture.
- **Eligibility:** all 15 named producer guards passed; the routing mask was
  independently audited in the receipt-hashed executed source, and the
  estimator/tolerance deviations below have no result-eligibility impact.
- **Verdict:** registered umbrella
  `GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`; exact supported branch:
  `MECHANISM_SUPPORTED` plus no utility effect and no hierarchy gain.
- **Claim boundary:** the result concerns a supplied four-state synthetic
  hierarchy and current-candidate pseudo-supervision. It is not evidence for
  semantic-tree discovery, natural-language generality, or Qwen loss benefit.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Parent \(p\) | supplied first split | balanced value in \(\{-1,+1\}\) | binary sign | defines the hierarchy's first routing cue | natural semantic parenthood |
| Child \(b\) | second split inside a parent | independent balanced value in \(\{-1,+1\}\) | binary sign | defines the leaf-specific residual | global affine separability |
| Surface code \(q\) | crossed observable | \(q=pb\); Router input is \(s=(p,q)\) | binary sign | makes \(b=pq\) globally XOR but conditionally linear | that language representations use this code |
| Work / fail | aligned and misaligned function groupings | \(\Theta^{work}=C+pA+bB\); \(\Theta^{fail}=C+qA+bB\) | \(8\times8\) operator | isolates the parent grouping while preserving the teacher multiset | a natural-data causal law |
| Residual | target function not explained by frozen ancestors | \(r=y-\hat y_{ancestors}\) | 8-vector | stage-local learning target | a representational coordinate subtraction |
| Counterfactual utility | current loss reduction from one candidate expert | \(U_{ie}=\|r_i\|_2^2-\|r_i-W_ez_i\|_2^2\) | squared-error difference | supplies a stop-gradient Router label | future expert quality or LM utility |
| `H_task` / `H_util` | conditional tree with task-only / task-plus-utility Router training | \(p\)-only first view; \(q\)-only masked child view | model arm | advisor and utility treatments | autonomous hierarchy discovery |
| `F_task` / `F_util` | flat nonlinear matched controls | full \(s=(p,q)\) at both Router heads | model arm | separates tree bias from generic nonlinearity | a universal non-hierarchical optimum |
| NMSE | exact noise-free task error normalized by signal energy | \(\frac14\sum_{p,b}\|\widehat\Theta_{p,b}-\Theta_{p,b}\|_F^2/3\), equal to the Gaussian \(z\sim\mathcal N(0,I_8)\) operator expectation | dimensionless; lower is better | endpoint guard and learning curve | population error beyond this generator |
| AULC | error accumulated over exposure | trapezoid integral of NMSE over log cumulative examples, normalized by log range | dimensionless; lower is better | primary efficiency metric | wall-clock efficiency |
| Optimizer seed | one independent training realization | seed `151130`--`151137`, paired across all eight cells | replicate | bootstrap unit | data-population generalization |
| Utility route accuracy | agreement with the best current candidate | fraction whose hard Gate choice equals \(\arg\max_e U_{ie}\) | fraction | Router-access diagnostic | that the candidate set is functionally complete |
| Utility regret | missed current-candidate utility | \(\max_eU_{ie}-U_{i,\hat e}\) averaged on the test bank | squared-error difference | local routing-quality diagnostic | low task NMSE by itself |
| Normalized target margin | angular Gate-score separation for the current utility target | fifth percentile of target-versus-best-wrong normalized score difference | dimensionless | robustness diagnostic | stable labels when experts move |
| Load / effective experts | hard-route usage | per-expert shares and inverse concentration | fraction / effective count | identifies starvation and collapse | a standalone performance verdict |

## 2. Anchor Link And Decision Point

The A15_11 decision separates five evidence layers: semantic variables,
representation access, deployed Router access, counterfactual current-expert
utility, and task-function gain. E03H addresses only the last two layers in a
controlled synthetic system. It asks whether the advisor's progressive
\(1\rightarrow2\rightarrow4\) freeze-and-residual architecture is functionally
helpful when its supplied first split is correct, and whether directly
supervising the Router with current-candidate utility improves that result.

The decision point after this experiment is not whether the analytic tree can
represent the work function—it can—but whether the observed evidence warrants
promoting either (a) a training-efficiency advantage of the tree or (b) this
utility objective. Neither promotion is supported.

### 2.1 Theorem erratum and the theorem actually tested

Frobenius orthogonality alone is insufficient to infer
\(\operatorname{rank}(A+B)=2\). For example, two rank-one matrices can be
Frobenius-orthogonal while sharing the same left factor, in which case their
sum remains rank one. The valid E03H theorem uses **doubly orthogonal**
rank-one matrices:

\[
A=u_1v_1^\top,\qquad B=u_2v_2^\top,\qquad
u_1\perp u_2,\quad v_1\perp v_2.
\]

The exact claim is scoped to the registered balanced, stagewise oracle. After
the common operator is exactly \(C\), fix one parent \(p\) and define
\(M_p=pA+B\). The two child residual targets are \(+M_p\) and \(-M_p\). For a frozen
parent operator \(D_p\) shared by those children and rank-one child operators
\(L_+,L_-\) that are exactly Frobenius-orthogonal to \(D_p\), balance cancels the
parent cross terms:

\[
\frac12\left[
\min_{L_+}\|M_p-D_p-L_+\|_F^2+
\min_{L_-}\|-M_p-D_p-L_-\|_F^2
\right]
=\|D_p\|_F^2+
\frac12\left[
\min_{L_+}\|M_p-L_+\|_F^2+
\min_{L_-}\|-M_p-L_-\|_F^2
\right]\geq1,
\]

where each minimum is over rank at most one with
\(\langle D_p,L_\pm\rangle_F=0\). The canonical diagonal \(A,B\) are doubly
orthogonal, so \(M_p\) has two unit singular values and each rank-one tail is at
least 1. Normalizing by total teacher energy 3 gives the \(1/3\) lower bound;
the oracle attains equality with \(D_p=0\). This is not a theorem that every
rank-one tree or every approximately orthogonal learned tree has a \(1/3\)
floor.

The executed learned operators satisfy only numerical near-orthogonality. The
registered aggregate guard enforces normalized ancestor overlap at most
\(10^{-6}\); the observed maximum was \(3.8357\times10^{-7}\) at endpoints and
\(6.2920\times10^{-7}\) over all post-update projections. Therefore the exact
oracle equality is used only as a reference, while learned eligibility uses
the separately registered float32 guard \(\mathrm{NMSE}\geq1/3-10^{-4}\). This
scope correction does not amend the frozen E03H Protocol, which already
registered the canonical doubly orthogonal projectors.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol and execution scope | frozen E03H; implementation, smoke, and full run approved | exact Protocol identity and SHA-256 accepted before outputs were read | pass | [preflight](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/preflight.json), [code receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/code_receipt.json) | none |
| Resource contract | exactly four reserved H100 GPUs; world size 4 | four NVIDIA H100 80GB HBM3; two seeds per rank | pass | [environment](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/environment.json), [manifest](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/run_manifest.json) | none |
| Generator | balanced \(p,b\), \(q=pb\), canonical \(C,A,B\), zero noise, 16 independent \(z\) blocks crossed with four leaves | exact identities, multiset, ranks, Gram, \(\rho\), and signal-energy checks passed | pass | [oracle ledger](tables/oracle_ledger.json) | none |
| Four-arm grid | `H_task`, `H_util`, `F_task`, `F_util` in work and fail | 8 cells per seed, 64/64 cells | pass | [summary table](tables/summary_table.csv) | none |
| Paired fairness | within seed, identical initialization, ordered inputs, test bank, parameters, candidate compute; same target within condition | every fairness check passed | pass | raw seed records under the [final run](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/) | none |
| Stages and optimizer | 128 steps each for common, two experts, four experts; Adam, fixed rates and coefficients, no early stop | exact frozen `TrainConfig` | pass | [run manifest](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/run_manifest.json) | none |
| Expert constraints | rank at most one; frozen ancestors; normalized overlap \(\leq10^{-6}\) | all ranks \(\leq1\); hashes immutable; worst per-update post-overlap \(6.2920\times10^{-7}\) | pass | raw per-seed projection/freeze ledgers | none |
| Primary NMSE estimator | evaluate the registered Gaussian NMSE on a frozen balanced 64-row bank | producer instead computes the exact four-leaf operator expectation \(\frac14\sum_{p,b}\|\widehat\Theta-\Theta\|_F^2/3\) at every checkpoint | audited estimator deviation | [executed metric source](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/e03_run.py), [raw figure contract](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/figure_contracts.json) | none: it is the exact expectation of the registered linear Gaussian estimand and removes finite-row sampling variance |
| Frozen test bank use | one balanced immutable bank per seed | used for utility targets/access, route agreement, regret, normalized margin, load, and paired-bank identity; not used to estimate primary NMSE | audited clarification | [executed diagnostic source](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/e03_run.py), raw seed records | none; diagnostic and fairness roles remain intact |
| Routing mask coverage | hierarchical stage one sees only \(p\); stage two sees only \(q\) and the selected parent's two leaves; flat sees full \(s\) and all leaves | independently audited in the receipt-hashed executed source; the producer's 15 named checks do not contain a mask key | audited guard-coverage deviation | [executed routing source](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/e03_models.py), [code receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/code_receipt.json) | none after code audit; do not call this a producer machine guard |
| Projection tolerance reporting | registered aggregate ancestor overlap \(\leq10^{-6}\) | each cell's local `projection_guard` receipt carries its default \(10^{-5}\) tolerance, while producer aggregation independently rechecks endpoints and every update at \(10^{-6}\); all observed values pass \(10^{-6}\) | audited receipt/aggregate deviation | [executed model source](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/e03_models.py), [executed aggregate source](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/e03_analysis.py) | none; decision eligibility uses the aggregate \(10^{-6}\) check |
| Fail-floor guard | learned hierarchical fail endpoint not below \(1/3-10^{-4}\) | no hierarchical fail cell leaked below the floor tolerance | pass | [summary table](tables/summary_table.csv), E03 completion audit | none |
| Load and Router ledgers | finite valid shares, effective count in \([1,K]\), finite regret/margin; hidden/Gate identity error \(\leq10^{-7}\) | all ledger checks passed | pass | `utility_ledger.csv` and raw seed records | none |
| Seeds and bootstrap | seeds `151130`--`151137`; 10,000 paired whole-seed draws; root seed `151124`; one shared index matrix | exact match; index hash `f5ea7cc3ca265991ab0ac4b1f01dfd80826199e3adbb479a657bf9b9128207c9` | pass | `bootstrap_draws.csv`, `results.json` | none |
| Required outputs | results, source ledgers, four figures, producer completion receipt | all present and hash-audited | pass | [E03 completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/completion_audit.json) | none |
| Global completion | Qwen and E03 kept as separate verdicts; all 27 artifacts validated | `passed: true`, `EVIDENCE_CHAIN_RECORDED_SEPARATE_VERDICTS` | pass | [global completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/completion_audit.json) | none |
| H100/5090 ownership | E03H is a collision-isolated H100 successor; no mutation or execution of the concurrent RTX-5090 lane | only E03H H100 artifacts used here | pass | Protocol Section 11 and final run manifest | no claim about 5090 Focus state |
| Earlier execution attempts | exclude any run without a global completion pass | `162845Z` stopped after a Qwen thread-pool deadlock; `164730Z` had complete E03 output but failed the global CSV reader; neither enters estimates | excluded | preserved attempt diagnostics and logs | none; final run starts fresh |
| Clean-run reproducibility | final run must use the repaired reader from preflight and independently complete | `172910Z` succeeded; the decision-bearing E03 analysis artifacts are byte-identical to the excluded `164730Z` producer | pass | paired SHA-256 audit; final completion receipt | strengthens execution reproducibility; old run remains noncanonical |
| Companion failure-mode figure | no result-derived primary threshold or verdict change | created append-only from the final seed table after the registered result | secondary diagnostic | [companion figure](figures/companion_seed_failure_modes.png) | cannot alter a registered verdict |

There were no missing cells, seed replacements, early stops, post-result
changes to E03 scientific code, threshold changes, or exclusions inside the
final aggregate. The only code change between the second and final attempts
was the global CSV reader's large-field handling. Final `results.json`,
`summary_table.csv`, `learning_curves.csv`, `utility_ledger.csv`,
`oracle_ledger.json`, `bootstrap_draws.csv`, `completion_audit.json`, and all
four registered E03 figures match their prior producer counterparts byte for
byte; timing-bearing raw seed files are not asserted to be byte-identical.

### 3.1 Producer guard, independent mask, and fairness audit

The producer's 15 named scientific checks were all `true`. This exact list is
important: it does not include a named mask check.

| Guard key | Status | Protected failure |
| --- | --- | --- |
| `ancestor_projection` | PASS | final expert leakage into frozen ancestors |
| `complete_grid` | PASS | missing condition, arm, or seed cell |
| `eckart_young` | PASS | incorrect analytic rank-one tail-energy floor |
| `fail_tree_floor_no_leak` | PASS | learned hierarchy illegally below \(1/3-10^{-4}\) in fail |
| `finite` | PASS | NaN or infinite decision values |
| `finite_load_compute_ledgers` | PASS | invalid load shares, effective counts, or compute fields |
| `freeze` | PASS | mutation of completed experts or stage-one Router |
| `generator` | PASS | teacher multiset, rank, Gram, \(\rho\), or signal-energy mismatch |
| `generator_noise_free_canonical` | PASS | noise or noncanonical teacher substitution |
| `manifest_full_eight_seed_four_rank` | PASS | wrong seeds, sharding, receipts, or world size |
| `oracle_four_values_1e10` | PASS | work/fail hierarchy/flat oracle mismatch beyond \(10^{-10}\) |
| `paired_fairness` | PASS | unequal initialization, stream, test bank, parameters, or compute |
| `projection_update_ledger` | PASS | missing or invalid pre/post projection record |
| `rank_one` | PASS | expert numerical rank above one |
| `router_hidden_gate_identity` | PASS | diagnostic head differing from the deployed Gate head |

The mask contract was instead independently checked against the executed
`routing_view` source authenticated by the run's code receipt: hierarchical
stage one returns \((p,0)\), hierarchical stage two returns \((0,q)\) with only the
selected parent's two leaves allowed, and flat routing returns full \((p,q)\)
with all four leaves allowed. This passes the frozen-code audit but is not a
producer machine-guard result.

The result-level maximum final ancestor leakage was
\(3.8357\times10^{-7}\); the maximum over every recorded post-update projection
was \(6.2920\times10^{-7}\). A cell-local receipt reports its default tolerance as
\(10^{-5}\), but producer aggregation independently checks both maxima against
the registered \(10^{-6}\) limit, which they pass. The exact analytic reference
is \(1/3\) only under Section 2.1's oracle assumptions; the learned float32 guard
allows a \(10^{-4}\) downward tolerance.

For every raw seed record, the paired fairness receipt separately reports
`complete_eight_cell_grid`, `all_cells_same_initialization`,
`all_cells_same_input_stream`, `all_cells_same_parameters`,
`all_cells_same_candidate_compute`, `all_cells_same_test_bank`,
`work_same_target`, and `fail_same_target` as `true`. Each rank receipt maps
exactly its two registered seeds and authenticates both immutable seed JSON
files. These checks establish comparability and integrity; they do not force
load balance or guarantee successful optimization.

## 4. Actual Setup

- **TRAIN:** each step draws 16 independent \(z\sim\mathcal N(0,I_8)\) blocks,
  crosses each with all four \((p,b)\) leaves, and shuffles the resulting 64
  rows. Work and fail reuse the same ordered \((p,b,q,z)\) stream per seed.
- **DEVELOPMENT:** none. The CPU smoke was non-scientific and could check only
  schema and numerical stability; it could not select an arm, seed,
  coefficient, threshold, or checkpoint.
- **CONFIRMATION:** one frozen balanced, noise-free 64-row test bank per seed,
  with the same full-factorial construction. It supplies current-candidate
  utility targets/access diagnostics, route agreement, regret, normalized
  margins, load, and a paired-bank identity hash. Primary NMSE is instead the
  exact Gaussian operator expectation. The optimizer seed, not a row, layer,
  stage, or checkpoint, is the inferential unit.
- **Learning target:** for condition \(c\),
  \(y=(C+g_cA+bB)z\), where \(g_{work}=p\) and \(g_{fail}=q=pb\).
- **Expert system:** seven dense stored \(8\times8\) matrices—one common, two
  stage-one, four stage-two—projected after every update to rank at most one
  and exact ancestor-orthogonal feasibility. Inference activates one expert
  per level and sums three outputs.
- **Routing:** all arms use the same two-layer Router MLP dimensions and hard
  top one with a straight-through gradient. `H` reads \(p\) at stage one and
  reads \(q\) within the selected two-child mask at stage two. `F` reads full
  \(s=(p,q)\) and is unrestricted over its candidates.
- **Supervision:** all arms optimize task MSE. Utility arms additionally use
  coefficient 1.0 times cross-entropy to the detached current-candidate
  utility argmax. Every arm evaluates all same-level candidates, including
  task-only controls. All use load coefficient 0.01.
- **Optimization:** Adam betas `(0.9,0.999)`, zero weight decay, expert learning
  rate 0.03, Router learning rate 0.01, gradient clip 5.0, 128 steps at each of
  three stages, evaluations at steps 1/2/4/8/16/32/64/128.
- **Seeds:** `151130`--`151137`, assigned by seed-index modulo four:
  rank 0=`151130,151134`; rank 1=`151131,151135`; rank 2=`151132,151136`;
  rank 3=`151133,151137`.
- **Capacity/compute:** 550 parameters per cell: 448 stored expert parameters,
  192 active expert parameters, and 102 Router parameters. Each cell records
  57,344 candidate expert forwards, 7,340,032 registered candidate-forward
  training FLOPs, and 544 inference FLOPs per example under the Protocol's
  convention.
- **Resource/runtime:** four NVIDIA H100 80GB HBM3 GPUs; Python 3.12.3;
  PyTorch `2.8.0a0+5228986c39.nv25.06`; NumPy 1.26.4; SciPy 1.15.3;
  scikit-learn 1.6.1; matplotlib 3.10.3.
- **Known setup limitation:** complete-factorial batches expose every surface
  state every step. This is a clean factorization test, not a sparse-data or
  natural-language sample-complexity model.

## 5. Metrics And Registered Decision Rules

The executed primary metric is exact noise-free Gaussian/operator NMSE,

\[
\operatorname{NMSE}=
\frac{\mathbb E_{p,b,z\sim\mathcal N(0,I_8)}
\|\widehat\Theta_{p,b}z-\Theta_{p,b}z\|_2^2}{3}
=\frac{\frac14\sum_{p,b}
\|\widehat\Theta_{p,b}-\Theta_{p,b}\|_F^2}{3}.
\]

Its AULC over log cumulative examples is primary; lower is better. Endpoint
NMSE is a fixed-budget companion metric. This deterministic operator
expectation is an audited execution deviation from the registered finite
frozen-bank estimator of the same Gaussian estimand. The test bank is used for
the diagnostics listed in Section 4, not for primary NMSE. For each condition,
the paired contrasts are

\[
S_H=A(H_{task})-A(H_{util}),\qquad
S_F=A(F_{task})-A(F_{util}),
\]

\[
A_T=A(F_{task})-A(H_{task}),\qquad
A_U=A(F_{util})-A(H_{util}),\qquad
X=S_H-S_F.
\]

Positive \(S\) favors utility supervision; positive \(A\) favors hierarchy.

- **Mechanism support:** eligible `H_task` work endpoint \(\leq0.05\), fail
  endpoint \(\geq0.25\), and fail-minus-work AULC paired 95% lower bound \(>0\).
- **Utility effect:** corresponding \(S_H\) or \(S_F\) AULC lower bound \(>0\) and
  utility endpoint no worse than task-only by more than 0.01. Work is the
  headline; fail is a structural diagnostic.
- **Hierarchy gain:** in work, corresponding \(A_T\) or \(A_U\) lower bound \(>0\),
  median gain at least 5% of matched flat median AULC, and hierarchical
  endpoint no worse than flat.
- **Insufficient:** any generator, oracle, rank, projection, freeze, mask,
  load-ledger validity, paired fairness, compute, sharding, numerical, or
  completion guard failure.

All intervals use 10,000 paired whole-seed bootstrap resamples from the one
registered shared index matrix. They summarize eight optimizer seeds and do
not license population-generalization claims.

## 6. Evidence Lineage

All machine-reported AULC and endpoint medians and confidence intervals below
come directly from the final [raw result and interval ledger](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json),
whose inputs are the eight immutable seed records. The local CSVs are curated
reading surfaces and do not replace that raw lineage.

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Analytic grouping obstruction | exact work H=0, fail H=\(1/3\), flat=0; exact \(\rho\) and separability identities | per-seed generator/oracle records | finite-support identities and Eckart--Young tail energy | deterministic, no sampling interval | work H=0; fail H=\(1/3\); flat work/fail=0 | eligible | oracle guard pass | capacity, not learned optimization |
| Learned mechanism | work endpoint \(\leq0.05\), fail \(\geq0.25\), fail-work AULC lower bound \(>0\) | final raw result ledger plus 8 `H_task` work/fail seed records | exact Gaussian operator NMSE; log-exposure trapezoid AULC; paired subtraction | paired median and 10,000-draw 95% interval | work \(1.9403\times10^{-5}\); fail 0.336926; AULC gap +0.053155 \([0.050140,0.054230]\) | eligible | `MECHANISM_SUPPORTED` | supplied hierarchy only |
| Tree utility effect in work | \(S_H\) lower bound \(>0\) plus endpoint guard | paired `H_task`/`H_util` records | paired AULC and endpoint differences | same shared bootstrap | AULC \(-0.012057\) \([-0.067979,-0.007610]\); endpoint \(-0.167010\) \([-0.667769,-0.166681]\) | eligible | `NO_UTILITY_EFFECT_TREE_WORK` | current-candidate objective only |
| Flat utility effect in work | \(S_F\) lower bound \(>0\) plus endpoint guard | paired `F_task`/`F_util` records | paired AULC and endpoint differences | same shared bootstrap | AULC \(-0.005792\) \([-0.007309,-0.000315]\); endpoint \(-4.2372\times10^{-5}\) \([-1.5913\times10^{-4},-6.2049\times10^{-6}]\) | eligible | `NO_UTILITY_EFFECT_FLAT_WORK` | small synthetic system |
| Task-only hierarchy gain | positive \(A_T\) lower bound, 5% median rule, endpoint guard | paired `F_task`/`H_task` records | paired AULC/endpoint differences | same shared bootstrap | AULC \(-0.000082\) \([-0.004211,0.002458]\); endpoint \(-4.5021\times10^{-6}\) \([-2.2536\times10^{-5},2.2390\times10^{-5}]\) | eligible | `NO_HIERARCHY_GAIN_TASK` | flat model has full nonlinear access |
| Hierarchy gain under utility | corresponding \(A_U\) rules | paired `F_util`/`H_util` records | paired AULC/endpoint differences | same shared bootstrap | AULC \(-0.009689\) \([-0.065236,0.000670]\); endpoint \(-0.166996\) \([-0.667270,-0.166608]\) | eligible | `NO_HIERARCHY_GAIN_UTILITY` | affected by seed-dependent tree starvation |
| Wrong-tree reversal | flat should solve fail while hierarchy remains near the registered oracle reference | all fail cells | same paired contrasts | same shared bootstrap | fail \(A_T=-0.052984\) \([-0.054568,-0.048606]\); fail \(A_U=-0.052058\) \([-0.064653,-0.045907]\) | eligible diagnostic | `PASS_FAIL_MINUS_WORK` | expected structural negative control |
| Utility starvation modes | no registered verdict; localize negative result | final per-seed load, expert, margin, regret, and endpoint records | classify only observed discrete endpoint/load modes | eight individual paired seeds; no new inferential threshold | work `H_util`: 1 near 0, 4 near \(1/6\), 3 near \(2/3\) | secondary diagnostic | supports optimization localization | post-hoc; cannot revise primary verdict |

## 7. Main Results

### 7.1 Exact layered machine verdicts

| Layer | Exact machine value | Reading |
| --- | --- | --- |
| Guard | `PASS` | all registered evidence is eligible |
| Mechanism | `MECHANISM_SUPPORTED` | aligned and misaligned trees separate as registered |
| Failure reversal | `PASS_FAIL_MINUS_WORK` | wrong grouping retains more error |
| Tree utility, work | `NO_UTILITY_EFFECT_TREE_WORK` | utility does not improve the tree |
| Flat utility, work | `NO_UTILITY_EFFECT_FLAT_WORK` | utility does not improve the flat control |
| Tree utility, fail | `NO_UTILITY_EFFECT_TREE_FAIL` | no fail-condition utility effect |
| Flat utility, fail | `NO_UTILITY_EFFECT_FLAT_FAIL` | no fail-condition utility effect |
| Task hierarchy, work | `NO_HIERARCHY_GAIN_TASK` | task-only tree does not beat flat |
| Utility hierarchy, work | `NO_HIERARCHY_GAIN_UTILITY` | tree does not add value under matched utility supervision |
| Legacy utility aggregate | `NO_UTILITY_GAIN` | no supervision-level gain |
| Legacy task architecture aggregate | `NO_TREE_ADVANTAGE_TASK_ONLY` | no task-only tree advantage |
| Legacy utility architecture aggregate | `NO_TREE_ADVANTAGE_UNDER_UTILITY` | no tree advantage under utility |
| Combined | `GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT` | supported sub-branch is generic nonlinearity, because all utility-effect verdicts are negative |

### 7.2 Cell-level primary results

| Condition | Arm | AULC median | AULC 95% interval | Endpoint NMSE median | Endpoint 95% interval |
| --- | --- | ---: | ---: | ---: | ---: |
| work | `H_task` | 0.762739 | [0.737538, 0.771615] | \(1.9403\times10^{-5}\) | [\(1.2147\times10^{-5}\), \(3.0740\times10^{-5}\)] |
| work | `H_util` | 0.785897 | [0.743072, 0.827095] | 0.167032 | [0.166702, 0.667786] |
| work | `F_task` | 0.763735 | [0.730700, 0.771414] | \(1.0398\times10^{-5}\) | [\(8.1473\times10^{-6}\), \(4.4152\times10^{-5}\)] |
| work | `F_util` | 0.772147 | [0.737873, 0.776553] | \(5.5529\times10^{-5}\) | [\(1.3892\times10^{-5}\), \(1.6790\times10^{-4}\)] |
| fail | `H_task` | 0.815778 | [0.786587, 0.827442] | 0.336926 | [0.334220, 0.356077] |
| fail | `H_util` | 0.816021 | [0.800670, 0.828456] | 0.334240 | [0.333566, 0.668019] |
| fail | `F_task` | 0.764226 | [0.732019, 0.773391] | \(3.1083\times10^{-5}\) | [\(1.3843\times10^{-5}\), \(7.2021\times10^{-5}\)] |
| fail | `F_util` | 0.768687 | [0.738365, 0.775418] | \(5.9951\times10^{-5}\) | [\(1.5903\times10^{-5}\), \(1.7618\times10^{-4}\)] |

The flat task model is near zero in both work and fail. Thus the tree's
work/fail contrast validates the structural mechanism, but the matched flat
control removes the proposed empirical hierarchy advantage.

### 7.3 Stage-level optimization

| Condition / arm | Stage 0 median [range] | Stage 1 median [range] | Stage 2 median [range] |
| --- | --- | --- | --- |
| work `H_task` | 0.666669 [0.666668, 0.666671] | 0.333340 [0.333338, 0.333346] | \(1.9403\times10^{-5}\) [\(8.5713\times10^{-6}\), \(3.5610\times10^{-5}\)] |
| work `H_util` | 0.666669 [0.666668, 0.666671] | 0.333345 [0.333339, 0.667349] | 0.167032 [\(2.0673\times10^{-5}\), 0.667920] |
| fail `H_task` | 0.666669 [0.666668, 0.666671] | 0.666947 [0.666730, 0.667120] | 0.336926 [0.333864, 0.390364] |
| fail `H_util` | 0.666669 [0.666668, 0.666671] | 0.666801 [0.666694, 0.667892] | 0.334240 [0.333493, 0.669369] |
| work `F_task` | 0.666669 [0.666668, 0.666671] | 0.333339 [0.333338, 0.333343] | \(1.0398\times10^{-5}\) [\(7.6872\times10^{-6}\), 0.000264] |
| fail `F_task` | 0.666669 [0.666668, 0.666671] | 0.333342 [0.333339, 0.333356] | \(3.1083\times10^{-5}\) [\(7.6003\times10^{-6}\), 0.000105] |

The common stage consistently learns \(C\), leaving two of three signal-energy
units and therefore NMSE \(2/3\). In aligned work, `H_task` then learns \(pA\)
and \(bB\). In fail, conditioning the first stage on \(p\) explains no residual
energy, and the final rank-one leaf can retain only one of the two doubly
orthogonal residual components.

### 7.4 Exact seed modes for utility-supervised hierarchy

#### Work

| Mode | Seeds | Endpoint NMSE | Final hard load | Functional reading |
| --- | --- | --- | --- | --- |
| complete | `151135` | 0.00002067 | `[0.25,0.25,0.25,0.25]` | both stage-one and both child splits learned |
| one child branch missing | `151130` | 0.16689992 | `[0.25,0.25,0,0.5]` | one half of the \(B\) residual remains |
| one child branch missing | `151131` | 0.16670239 | `[0.25,0.25,0.5,0]` | same \(1/6\) energy mode |
| one child branch missing | `151133` | 0.16716354 | `[0,0.5,0.25,0.25]` | same \(1/6\) energy mode |
| one child branch missing | `151136` | 0.16686532 | `[0.25,0.25,0.5,0]` | same \(1/6\) energy mode |
| stage-one collapse | `151132` | 0.66778648 | `[0,0,1,0]` | neither residual component is recovered |
| stage-one collapse | `151134` | 0.66791958 | `[0,0,0,1]` | neither residual component is recovered |
| stage-one collapse | `151137` | 0.66743797 | `[0,1,0,0]` | neither residual component is recovered |

At stage one, five seeds reached the intended balanced split and three
(`151132`, `151134`, `151137`) froze a single-route state. Of the five that
passed stage one, only `151135` used all four leaves at the endpoint; the other
four used three leaves and retained approximately \(1/6\) NMSE. The wide
endpoint interval is therefore a genuine discrete optimizer-seed mixture, not
test-row sampling noise.

#### Fail

| Mode | Seeds | Endpoint NMSE | Reading |
| --- | --- | --- | --- |
| near analytic reference | `151130,151132,151134,151135,151136` | 0.333493--0.334814 | one residual component learned; the other remains |
| partial residual | `151131` | 0.483863 | incomplete approximation, above the reference |
| collapsed | `151133,151137` | 0.669369, 0.668019 | nearly no residual component learned |

The fail interval \([0.333566,0.668019]\) is wide for the same reason: five
reference-like seeds, one intermediate seed, and two collapsed seeds.

### 7.5 Router, margin, regret, and load diagnostics

At the work endpoint, diagnostic medians were:

| Arm | Route accuracy | Utility regret | Margin p05 | Effective leaf experts | Load CV | Endpoint NMSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `H_task` | 1.000000 | 0 | 0.545541 | 4.000000 | 0 | \(1.9403\times10^{-5}\) |
| `H_util` | 0.914062 | 0.005259 | 0.000440 | 2.666667 | 0.707107 | 0.167032 |
| `F_task` | 0.984375 | \(7.16\times10^{-7}\) | 0.001156 | 2.000000 | 1.000000 | \(1.0398\times10^{-5}\) |
| `F_util` | 1.000000 | 0 | 0.324644 | 2.000000 | 1.000000 | \(5.5529\times10^{-5}\) |

Two boundaries follow. First, balanced load is not itself an outcome: flat
arms can solve the task with only two used leaves because their nonlinear
Router can choose a different functional decomposition. Second, high agreement
with the best **current** expert and low regret do not imply that all needed
experts were learned. For example, partial `H_util` work seeds reached route
accuracy 0.875--0.984 while retaining approximately \(1/6\) task NMSE.

## 8. Visualization Results

### 8.1 Does the exact grouping swap create the registered floor?

![Oracle and separability audit](figures/oracle_and_separability.png)

- **Purpose:** audit the analytic work/fail construction before interpreting
  learning.
- **Metric/unit:** exact \(\rho_p,\rho_q\), oracle NMSE, and learned endpoint
  NMSE; dimensionless ratios.
- **Raw source:** [oracle ledger](tables/oracle_ledger.json) and
  [summary table](tables/summary_table.csv).
- **Aggregation:** deterministic identities plus median over eight optimizer
  seeds for learned endpoints.
- **Axes/legend:** bars name the grouping-energy ratios, four oracle values,
  and task-only learned endpoints.
- **Expected under registered outcomes:** hierarchical work oracle 0,
  hierarchical fail oracle \(1/3\), and flat work/fail oracle 0; eligible learned
  `H_task` should be at most 0.05 in work and at least 0.25 in fail.
- **Observed:** the parent-aligned energy swaps from \(p\) in work to \(q\) in
  fail; the hierarchy oracle changes from 0 to \(1/3\), while flat remains 0.
- **Allowed conclusion:** the construction contains the registered structural
  obstruction and learned task-only endpoints follow it.
- **Anchor implication:** retain the supplied-factorization mechanism at the
  controlled synthetic-function layer only; this figure does not promote an
  empirical architecture-efficiency claim.
- **Limitation:** exact capacity does not prove an optimizer will reach an
  oracle, nor that natural semantics use this factorization.

### 8.2 How quickly do the four arms learn?

![Noise-free NMSE learning curves](figures/nmse_learning_curves.png)

- **Purpose:** compare training efficiency through all three frozen stages.
- **Metric/unit:** exact noise-free NMSE versus cumulative training rows on a
  logarithmic horizontal axis.
- **Raw source:** final `learning_curves.csv`.
- **Aggregation:** pointwise median across eight optimizer seeds.
- **Axes/legend:** left panel work, right panel fail; one line per registered
  arm.
- **Expected under registered outcomes:** a hierarchy or utility advantage
  would lower the corresponding work curve and registered AULC while passing
  the endpoint guard; the wrong hierarchy should retain the fail reference.
- **Observed:** task-only tree and flat converge together in work; flat solves
  fail; the tree remains near its registered fail reference. Median `H_util`
  work ends near \(1/6\).
- **Allowed conclusion:** no median hierarchy-efficiency advantage is visible,
  and the work/fail capacity pattern is learned.
- **Anchor implication:** the curve shape supports the learned mechanism, but
  cannot promote hierarchy or utility gain without the registered paired
  contrasts in Section 8.3.
- **Limitation:** a median line hides the discrete `H_util` seed modes; use the
  companion figure and seed table for failure localization.

### 8.3 Are utility and hierarchy effects distinct?

![Registered paired AULC contrasts](figures/grid_contrasts.png)

- **Purpose:** apply the registered architecture/supervision contrasts without
  conflating them.
- **Metric/unit:** paired AULC contrasts \(S_H,S_F,A_T,A_U,X\); positive favors
  the named treatment.
- **Raw source:** final `bootstrap_draws.csv`; curated values in
  [primary contrasts](tables/primary_contrasts.csv).
- **Aggregation:** paired whole-seed median and 95% interval from 10,000 shared
  bootstrap draws.
- **Axes/legend:** work and fail panels; bars are medians, error bars are 95%
  intervals, dashed line is zero.
- **Expected under registered outcomes:** positive \(S_H\) or \(S_F\) favors
  utility, positive \(A_T\) or \(A_U\) favors hierarchy, and a registered gain
  requires its paired 95% lower bound above zero plus the companion magnitude
  and endpoint guards; fail \(A\) is expected to be negative.
- **Observed:** both work utility contrasts are negative; neither work
  hierarchy contrast has a positive lower bound. Fail correctly favors flat.
- **Allowed conclusion:** no registered utility or hierarchy gain; expected
  wrong-tree reversal.
- **Anchor implication:** retain only the mechanism result; do not promote the
  current utility objective or a hierarchy-efficiency advantage.
- **Limitation:** the interaction \(X\) is diagnostic and cannot replace either
  registered main effect.

### 8.4 Does the Router select the best current candidate?

![Utility access diagnostics](figures/utility_diagnostics.png)

- **Purpose:** separate current-candidate Router access from end-task error.
- **Metric/unit:** utility regret, route agreement, and fifth-percentile
  normalized target margin.
- **Raw source:** final `utility_ledger.csv`.
- **Aggregation:** final checkpoint per seed/cell, pooled by arm across work
  and fail as registered in the figure producer.
- **Axes/legend:** one box per arm for each diagnostic.
- **Expected under registered outcomes:** useful Router access should show
  better current-target agreement, lower regret, and positive margin; a
  functional-benefit claim additionally requires lower task NMSE in the
  registered treatment contrast.
- **Observed:** utility arms often achieve high current-target agreement and
  low regret, but `H_util` has broad negative-margin and high-regret seed
  outliers.
- **Allowed conclusion:** current-candidate access can coexist with missing
  expert functions.
- **Anchor implication:** access diagnostics cannot promote method-level
  utility; expert-set completeness remains a separate functional requirement.
- **Limitation:** work and fail are pooled and utility targets move with the
  experts; this plot cannot diagnose one condition or establish causal task
  benefit by itself.

### 8.5 Registered figure-set conclusion

The four registered figures jointly establish: the exact \(1/3\) reference is
valid under Section 2.1's canonical oracle assumptions; the task-only tree
follows the registered work/fail pattern within the learned tolerance; the
flat nonlinear control prevents a hierarchy-efficiency promotion; and
current-candidate utility access does not imply functional gain. Their source,
aggregation, allowed conclusion, and limitation are frozen in the producer's
`figure_contracts.json`; the expected-pattern and Anchor-implication bullets
above make the result-record contract explicit without changing that producer
metadata.

### 8.6 Append-only companion seed-failure diagnostic

![Companion seed-wise utility-supervision failure modes](figures/companion_seed_failure_modes.png)

- **Status:** append-only secondary diagnostic; not a primary verdict and not
  used to choose a threshold, checkpoint, arm, or exclusion.
- **Question:** which optimizer seeds create the wide `H_util` endpoint
  intervals, and does endpoint error track missing leaf use?
- **Metric/unit:** final noise-free NMSE and count of leaves with nonzero hard
  route load.
- **Raw source:** [summary table](tables/summary_table.csv).
- **Aggregation:** none; every colored point is one registered paired optimizer
  seed.
- **Axes/legend:** columns are task-only and utility-supervised hierarchy;
  panels separate work and fail; dashed horizontal lines mark \(1/6\), \(1/3\),
  and \(2/3\) analytic energy scales.
- **Expected under registered outcomes:** none; this is a post-hoc localization
  view and has no registered success pattern or decision threshold.
- **Observed:** work `H_task` uses four leaves and reaches zero for all seeds;
  work `H_util` separates into 4-leaf/zero, 3-leaf/\(1/6\), and 1-leaf/\(2/3\)
  modes. Fail `H_util` similarly separates into reference-like, partial, and
  collapsed modes.
- **Allowed conclusion:** the wide interval is localized to seed-dependent
  missing-expert optimization states rather than missing runs or row noise.
- **Anchor implication:** none by itself; the companion cannot change the
  registered verdict, Claim Boundary, or Anchor state.
- **Limitation:** this post-hoc visualization does not by itself prove the
  unique causal gradient path or validate a repair.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Generator and theorem | exact multiset, Gram, \(\rho\), separability, and oracle ledgers | passed | none | data mismatch, noise, or a false rank-two premise | natural-language relevance |
| Common expert | every arm/condition ends stage zero at approximately \(2/3\) | passed | none | failure to learn \(C\) | later routing/expert co-adaptation |
| Task-only work stage one | 8/8 balanced parent load and experts approximately \(\pm A\) | passed | none | insufficient rank-one capacity for aligned first residual | empirical hierarchy advantage |
| Task-only work stage two | 8/8 balanced four-leaf load and near-zero endpoint | passed | none | inability of the tree to realize work | matched flat sufficiency |
| Task-only fail | stage one remains near \(2/3\); stage two remains at/above \(1/3\) | passed expected negative | wrong grouping forces two orthogonal residuals through rank one | nothing about natural semantics | wrong-factor grouping remains a controlled synthetic result |
| Flat task control | near zero in work and fail at the same fixed budget with matched parameters/compute | passed | none | necessity of a tree to solve this four-state task | harder-data hierarchy effects; no equivalence claim |
| Utility-supervised work | 3/8 stage-one collapse; then 4/5 remaining seeds miss one child branch | failed to improve | seed-dependent expert starvation / route collapse | the claim that direct current-candidate labels automatically help | exact causal contribution of each gradient term |
| Utility target access | some failed cells have high route accuracy and low regret | mixed | candidate set is incomplete even when current choice is locally best | utility access as a substitute for task NMSE | alternative fixed-target or exploration schemes, not tested |
| Rank/freeze/load/compute implementation | all named producer guards and the independent mask code audit passed | passed | none | leakage, extra capacity, missing candidates, invalid load rows, or frozen-parameter mutation | optimization-objective failure |
| Metric | exact noise-free operator error exposes \(0,1/6,1/3,2/3\) modes | passed | none | a threshold-only artifact | population claims beyond eight seeds |

### 9.1 Lowest-level supported failure path

The implementation and paired trajectories support this path:

```text
current experts define detached utility argmax labels
-> utility cross-entropy updates the Router, not candidate experts
-> hard top-one task forwarding updates only selected experts
-> an expert receiving balanced opposite residuals is driven toward their zero mean
-> unselected experts are starved of task gradient
-> the current near-zero expert can remain the locally preferred self-consistent action
-> a missing route/expert persists
-> the stage freeze prevents later recovery
```

This path explains the observed energy levels. If one of two parent branches
fails to split its \(\pm B\) residual, half of one unit of \(B\) energy remains;
normalizing by total signal energy 3 gives \(1/6\). If both \(A\) and \(B\) residual
units remain, the endpoint is \(2/3\). In fail, learning one of the two residual
units gives the \(1/3\) analytic reference under Section 2.1's exact assumptions.

The path is the narrowest evidence-grounded interpretation, not a universal
causal theorem. The Protocol did not include a fixed-oracle-label, forced
exploration, or expert-pretraining repair arm, so it cannot select among such
repairs or prove that endogenous utility labels are the unique possible cause.

### 9.2 Failure type

- **Physical/theoretical prior:** not falsified at the capacity level; the
  aligned versus misaligned structural theorem is supported.
- **Architecture necessity:** not established for this generator; the flat
  nonlinear matched baseline reaches near-zero error in both conditions at the
  same fixed budget, and no registered hierarchy-efficiency gain is established.
- **Optimization/objective:** current utility supervision fails to improve and
  introduces seed-dependent missing-expert states.
- **Implementation:** not falsified; all named producer implementation guards
  pass and the receipt-hashed routing mask passes independent code audit.
- **Metric:** not falsified; exact NMSE and paired AULC distinguish the modes
  and controls.
- **Remaining rival:** the precise gradient-level share of utility CE, task
  STE, load balancing, initialization, and freezing was not separately
  intervened on. Any such decomposition requires a newly registered successor.

## 10. Full Experiment Record

- Final ACP job: `pt-vkikyszj`; terminal state `SUCCEEDED`.
- Final run stamp: `20260829T172910Z`.
- Scientific resource: one reserved worker exposing exactly four H100 80GB
  GPUs; world size 4.
- Preflight: passed before scientific outputs were read.
- Automated verification: 86 tests passed, 1 skipped in the main suite; the
  dedicated GPU projection regression passed 1/1.
- Seeds: 8/8 registered; four immutable rank-completion receipts.
- Cells: 64/64 = 8 seeds × 2 generator conditions × 4 arms.
- Training records: 1,536 = 24 registered evaluations per cell.
- Optimizer steps: 24,576 = 384 per cell.
- Projection updates: 57,344 = 896 per cell.
- Candidate expert forwards: 57,344 per cell.
- Bootstrap: 10,000 paired whole-seed draws for every registered contrast,
  using the same seed-index matrix.
- Retry/exclusion record:
  - `full-20260829T162845Z`: stopped after a Qwen-side thread-pool deadlock;
    no result entered this record.
  - `full-20260829T164730Z`: E03 producer completed, but the global audit failed
    on the Qwen CSV reader's default field-size limit; retained only as an
    implementation diagnostic and excluded from canonical inference.
  - `full-20260829T172910Z`: fresh clean run with pre-run repaired audit code;
    producer and global completion passed. Its E03 scientific artifacts match
    the excluded producer byte for byte.
- 5090 boundary: no RTX-5090 job, shared Focus execution, or shared 5090 result
  is represented here. The H100 successor does not close that separately owned
  lane.

## 11. Interpretation

The result resolves two previously conflated questions. First, the advisor's
factorization intuition is correct as a controlled structural statement:
after learning \(C\), a correct \(p\) split turns the remaining decisions into two
rank-one stages, while the paired wrong grouping retains a rank-two residual
inside a rank-one leaf. The learned task-only tree reproduces that exact
work/fail distinction.

Second, that structural correctness is not enough to establish a training
advantage. The matched flat Router is nonlinear, sees all four surface states
in every complete-factorial batch, and reaches near-zero error in both work and
fail at the same fixed budget. The registered task hierarchy contrast does not
pass its positive-CI, magnitude, or endpoint decision rule; therefore no
registered hierarchy-efficiency gain is established. This failure to establish
a gain is not an equivalence or equal-efficiency proof. The machine's registered
umbrella label resolves here to the generic-nonlinearity fallback branch, not
to a formal sufficiency theorem.

Direct utility supervision also does not rescue or improve the result. It
trains the Router to prefer the best current candidate, but does not itself
make an unselected expert useful. The seed ledgers show that high
current-candidate agreement can coexist with a missing semantic leaf and large
task error. Functional completeness of the expert set and Router access to
current utility are separate evidence layers.

This is an AI-verified interpretation of complete eligible evidence. The
researcher accepted this bounded interpretation only as collision-isolated,
non-owning H100 sensitivity evidence under the current Focus.

## 12. Claim Boundary

### Can claim

- The supplied correct \(p\)-first factorization is exactly realizable by the
  progressive rank-one tree. In the registered balanced stagewise oracle, the
  paired wrong grouping with exact ancestor orthogonality and the canonical
  doubly orthogonal rank-one pair has a \(1/3\) lower bound; the learned run
  passes only the registered tolerance-aware guard around that reference.
- The learned task-only tree reproduces that work/fail separation across the
  eight registered optimizer seeds.
- In this controlled generator and fixed budget, the matched generic nonlinear
  Router also reaches near-zero error; no registered hierarchy-efficiency gain
  is established. This is not an equivalence result.
- The registered online counterfactual-utility supervision provides no gain
  and induces seed-dependent missing-expert modes in this implementation.

### Cannot claim

- That natural-language semantics have this hierarchy, or that a network can
  discover it without the supplied structural mask.
- That hierarchy is generally useless, or that every alternative utility
  objective must fail.
- That routing to the best current expert is equivalent to learning a complete
  expert candidate set.
- That Qwen's native Router uses these variables or that the method improves
  language-model loss.
- That the concurrently owned RTX-5090 lane or its Focus has been executed or
  closed.

## 13. Next Decision

**Decision:** E03H is admitted as non-owning H100 sensitivity evidence. The
sole A15_11 next decision is to freeze a frequency (high/low) by cross-child
gradient-consistency (high/low) representation-formation test before another
Router intervention.

**Completion criterion:** the successor contract holds total tokens, target
positions, parent/child counts, vocabulary, templates, and label entropy fixed
and defines frozen measurements for gradient consistency, parent between-class
energy, held-out fifth-percentile normalized margin, and discriminant-subspace
spectral location.

**Resume action:** retain the structural work/fail mechanism and the negative
hierarchy/utility results under the non-owning sensitivity label, then use the
current Focus/Anchor to design the \(2\times2\) successor. Do not launch it before
a new confirmed Anchor and Protocol.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | SHA-256 or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen scientific contract | human-authorized E03H revision | A15_11 question | `5b0e8163...bcc59fa` | yes | yes | already used doubly orthogonal theorem |
| [global completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/completion_audit.json) | validate complete Qwen/E03 evidence chain | `completion_audit.py` | 27 final artifacts | `acafbbc3...13e9d38` | yes | yes | separates Qwen and E03 verdicts |
| [E03 completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/completion_audit.json) | producer-local schema/hash/verdict receipt | `e03_analysis.py` | final E03 outputs | `efb86fd0...cd576bf` | yes | yes | 8 paired seeds |
| [raw results](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json) | full registered contrasts, endpoint intervals, and verdicts | `e03_analysis.py` | eight raw seed files | `429b4d50...de97ef63` | yes | yes | contains 10,000 draw summaries |
| [summary table](tables/summary_table.csv) | curated per-seed cell metrics | byte copy of final producer table | raw seed records | `606d876e...2c3f3d8` | yes | yes | 64 rows |
| [primary contrasts](tables/primary_contrasts.csv) | compact registered AULC contrasts | deterministic curation from final `results.json` | registered contrast objects | `0defa4e7...902f6a` | yes | yes | no new estimator |
| [oracle ledger](tables/oracle_ledger.json) | exact generator, separability, oracle proof | byte copy of producer ledger | canonical \(C,A,B\) | `258200ef...9060c33` | yes | yes | deterministic identities |
| `e03/learning_curves.csv` | all stage/checkpoint metrics | `e03_analysis.py` | 1,536 raw training records | `ded53e7e...a18276c` | yes | yes | source for learning curve and stage audit |
| `e03/utility_ledger.csv` | Router access, margin, regret, load | `e03_analysis.py` | checkpoint records | `3b849b39...5a03965` | yes | eligible diagnostic | current targets move with experts |
| `e03/bootstrap_draws.csv` | all paired bootstrap draws | `e03_analysis.py` | shared whole-seed index matrix | `243df505...57b4a8e` | yes | yes | 10,000 draws per registered contrast |
| [oracle figure](figures/oracle_and_separability.png) | exact structural mechanism | registered producer | oracle ledger and summary table | `6d7402a2...539cf5` | yes | yes | central mechanism figure |
| [learning curves](figures/nmse_learning_curves.png) | exposure profile | registered producer | learning curves | `518ccebc...6c709229` | yes | yes | medians hide seed modes |
| [grid contrasts](figures/grid_contrasts.png) | registered effect separation | registered producer | bootstrap draws | `060877fe...9d8679f5` | yes | yes | AULC verdict figure |
| [utility diagnostics](figures/utility_diagnostics.png) | current-candidate access | registered producer | utility ledger | `ff9cbc02...c668e0` | yes | eligible diagnostic | pools work/fail |
| [companion seed modes](figures/companion_seed_failure_modes.png) | show post-hoc seed/load modes | append-only secondary rendering | curated summary table | `48a3b63f...e80d87f` | yes | secondary only | does not alter verdict |
| [run manifest](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/run_manifest.json) | immutable seed/config/code contract | pre-run E03 producer | frozen config and code hashes | `202b9853...ec8158` | yes | yes | world size 4 |
| [environment](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/environment.json) | runtime identity | E03 producer | live worker | `d85deb0e...c3414` | yes | provenance | four H100 names recorded |
| raw rank/seed records | complete experts, freeze, projection, timing, route ledgers | `e03_run.py` | scientific training | four rank receipts; eight seed JSON files | yes | yes | canonical raw source |

## 15. Links

- anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: [/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure)
- data / manifest: [final E03 run manifest](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs/run_manifest.json)
- result directory: [final run](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z)
- raw E03 result: [results.json](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json)
- raw seed ledgers: [e03_runs](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03_runs)
- figure directory: [figures](figures)
- table directory: [tables](tables)
- logs: [logs](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs)
- job: ACP `pt-vkikyszj`

## 16. Final Audit

| Audit item | Status |
| --- | --- |
| Human result judgment not invented; researcher acceptance and non-owning sensitivity scope are explicit | PASS |
| Frozen Protocol and execution scope identified | PASS |
| Conformance, retries, exclusions, and companion diagnostic recorded before interpretation | PASS |
| Every primary result classified eligible | PASS |
| Decision-bearing numbers trace to raw artifacts, estimator, bootstrap, rule, and verdict | PASS |
| Observation, derived statistic, interpretation, boundary, and next decision separated | PASS |
| Summary is conclusion-first and links curated sources | PASS |
| Detailed is the complete evidence ledger | PASS |
| All five displayed figures have source, aggregation, expected pattern, observed result, Anchor implication, and limitation | PASS |
| Summary and Detailed use the same verdict, boundary, and next-decision gate | PASS |
| Focus and Anchor were updated only after researcher acceptance; the RTX-5090 execution contract and frozen H100 Protocol remain unchanged | PASS |
| Exactly one upstream next decision, completion criterion, and resume action recorded | PASS |
