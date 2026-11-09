# Detailed: A15_17_01_E03 Lambda-Transition Reuse Audit

Primary Anchor: [shared SAE atom reuse](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), `A15_17_01_E03-direct-full-v1`  
Summary: [summary.md](summary.md); Chinese companion: [summary_cn.md](summary_cn.md)  
Result eligibility: `ELIGIBLE` for the registered descriptive checkpoint contrast. Human mechanism judgment: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

**Purpose:** test whether lower native effective dimension after the coefficient
transition is accompanied by increased model-local same-ID Top-32 activation
reuse on one identical frozen panel.

**Hypothesis:** post-transition reuse should be higher and post-transition native
effective dimension lower. The strongest rival is low dimension from decoder
geometry, coefficient covariance, or training-history drift without increased
same-ID reuse.

**Experiment logic:** align the two checkpoint conditions and the 192 records;
measure model-local usage-profile cosine with paired bootstrap; independently
measure native-write effective dimension and verify read-only/numerical guards.

**Direct result:** reuse was higher before the transition: pre `0.6476181362`,
post `0.6253022967`, `post - pre = -0.0223158395`, paired record-bootstrap
95% CI `[-0.0352508453, -0.0088839748]`. Native effective dimension fell from
`15.6743606802` to `8.4184916947`, a contrast of `-7.2558689855`.

**Eligibility:** application terminal `PASS`, four of four workers passed, 192
records and 49,152 valid tokens per model were aligned, no exclusions, all
registered full-run guards passed, and independent post-run numerical/artifact
audit passed. Separate Smoke was `NOT_RUN_DIRECT_FULL_USER_REQUEST` by the
approved direct-full scope; it was not relabeled as Smoke PASS.

**Registered verdict:** `PRE_HIGHER_REUSE`. The specific necessary condition
“post reuse increases while native dimension decreases” is not supported in
this transition contrast. This is an AI draft of the mechanism reading and
awaits the researcher’s judgment.

**Claim boundary:** this is a before/after training-history association, not an
isolated causal estimate of `lambda_rec`.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Same-ID reuse | Whether different records use similar distributions of the same model’s atom IDs | Per-record frequency vector over 30,000 selected Top-32 IDs, normalized over 256 tokens and 32 slots | Mean off-diagonal cosine \(R\) | Direct observable for the candidate shared-atom mechanism | Semantic identity, cross-model feature alignment, or decoder-direction alignment |
| Native write | The attention output before residual addition | `blocks[7].attn.o`, after output projection and before residual add | 1,024-dimensional vector; mean pooled per record | Measures the backbone representation being audited | SAE reconstruction quality or task utility |
| Effective dimension | How many covariance-equivalent directions carry the native variance | Centered participation ratio of the 192 pooled native writes | \(d_{eff}=\operatorname{tr}(\Sigma)^2/\operatorname{tr}(\Sigma^2)\) | Quantifies variance concentration | Literal rank, semantic dimensionality, or quality |
| Paired bootstrap | Resampling the same record IDs for both conditions | 2,000 paired resamples, seed `20260922` | 95% percentile interval | Quantifies fixed-panel record uncertainty | Training-seed or causal uncertainty |
| Transition contrast | Difference between two historical endpoints | Exact 17B post checkpoint minus exact 15B pre checkpoint | `post - pre` | Tests whether the pattern persists across the recorded transition | The isolated effect of changing only the coefficient |

## 2. Anchor Link And Decision Point

The Anchor asks whether lower native dimension is accompanied by stronger
cross-example reuse of the same model-local SAE atom identities. The E03
follow-up removes the S7/SALL architecture comparison and instead compares the
selected 15B pre-transition and 17B post-transition checkpoints within the
same S7 sidecar lineage.

The decision point is whether the “shared same-ID atom reuse” explanation
remains viable as a necessary companion to low native dimension in this
transition. A negative reuse interval weakens this explanation for the current
contrast; it does not prove that decoder geometry or coefficient covariance is
the cause.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| Protocol and scope | E03 direct full, read-only, four RTX5090 | Job `pt-7stjld8g`, application terminal `PASS` | `PASS` | `terminal_receipt.json`, `FULL_MEASUREMENT_PASS.json` | Eligible |
| Checkpoints | Exact 15B pre `lambda=1.0` and exact 17B post `lambda=0.1` | Step 57224 / 64854; 15B / 17B manifests complete | `PASS` | four worker receipts, frozen assets | Eligible |
| Coefficient boundary | Fork source step 59000 at 15,465,567,744 tokens | Source lineage and before/after labels verified | `PASS` | `training_lineage_audit.json`, `fork_lineage.json` | Defines causal boundary; no isolation claim |
| Inputs | 192 ordered fixed N8 records, 256 valid tokens | 192/192 aligned; 49,152 tokens/model; zero exclusions | `PASS` | `ALIGNED_FULL_PANEL_PASS.json`, panel manifest | Eligible |
| Native extraction | Layer-7 native Attention output, native Top-32 | Exact site and native encode verified in four workers | `PASS` | worker receipts and support arrays | Eligible |
| Primary statistic | Mean usage-profile cosine, `post - pre` | Delta and paired 2,000-draw interval produced | `PASS` | `analysis/result.json`, `tables/primary.csv` | Eligible |
| Dimension statistic | Same-panel centered native participation ratio | Both conditions computed and independently recomputed | `PASS` | `tables/conditions.csv`, `independent_audit.json` | Descriptive gate eligible |
| Numerical/read-only guards | finite values, exact repeat, CPU/GPU agreement, no mutation | All workers passed; repeat RMS `0`; non-tie support mismatch `0` | `PASS` | four worker receipts | Eligible |
| Separate Smoke | Not required under direct-full registration; do not call it PASS | `NOT_RUN_DIRECT_FULL_USER_REQUEST` | `CONFORMING` | identity/alignment stage records | No reduction because full embedded guards were required |
| Resources | One 4x RTX5090 Spot node, registered image/runtime | Four RTX5090 workers; runtime and target preflight passed | `PASS` | execution certificate and terminal receipt | Eligible |
| Artifact completion | worker receipts, arrays, result, tables, figures, hashes, terminal | All present; independent audit verified 22 manifest artifacts | `PASS` | `artifact_manifest.json`, `independent_audit.json` | Eligible |
| Retry/exclusion | no hidden retry or partial-condition pooling | Four workers completed; zero exclusions; no alternate resource | `PASS` | terminal/stage receipts | Eligible |

Frozen Protocol revision: `A15_17_01_E03-direct-full-v1`.  
Execution scope approved: researcher’s current request for exact 15B/17B
read-only comparison on four RTX5090 GPUs.  
Amendments: none after execution started.  
Retries and exclusions: none; all four workers are claim-eligible.  
Missing conditions or artifacts: none for the registered measurement.  
Post-hoc analyses: `audit_completed.py` independently recomputed the primary
reuse contrast, native dimensions, and paired bootstrap from the completed
artifacts. It is QA and does not introduce a new endpoint.

## 4. Actual Setup

**Research question:** does lower post-transition native effective dimension
co-occur with higher same-ID Top-32 reuse?

**Data construction and provenance:** the frozen 192-record N8 panel is stored
in `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/manifests/full_inputs.json`.
Each record has 256 valid body tokens. Labels are absent from the executable
panel and were not used for selection or fitting.

**Train / development / confirmation split:** no training, fitting, or split
selection. This is a frozen checkpoint measurement; the 192 records are the
paired confirmation units.

**Learning task and permitted supervision:** no task loss, optimizer, labels,
or intervention. Four independent read-only extraction processes only.

**Model / architecture / algorithm:** eight-layer hidden-1024 Qwen3 SAE
sidecar, layer-7 native Attention-output hook, width 30,000, native Top-32
encoder support, same model source hashes and same initial tensor/backbone
identity across the two lineage records.

**Input representation / position encoding:** fixed token IDs, right-padded
worker batches, valid-token mask, native attention output after \(W_O\) and
before residual addition. Native writes are mean pooled over the 256 valid
tokens of each record.

**Training objective and constraints:** no training in this experiment. Source
checkpoint histories have `lambda_rec=1.0` before the fork and `0.1` after the
fork, but the endpoint contrast also contains microbatch, gradient-accumulation,
CE-chunk, optimizer/RNG, and training-stage differences.

**Training steps / tokens / batch size:** pre step 57,224 at 15,000,000,000
tokens; post step 64,854 at 17,000,000,000 tokens. Measurement batch is four
records per worker batch and 49,152 valid tokens per model across 192 records.

**Checkpoints:**

- Pre: `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b/runs/formal50b_last_attention_4h100/milestones/token_015000000000`
- Post: `/data/250010109/MoE_Router/experiments/20260917_attention_output_sidecar_last_reweighted_resume/runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/milestones/token_017000000000`

The exact fork source is step 59,000 at 15,465,567,744 tokens. Therefore the
selected 15B endpoint is 0.465567744B tokens before the boundary, and the 17B
endpoint is 1.534432256B tokens after it.

**Seeds:** source lineage seed 17; paired bootstrap seed `20260922`. There is
one checkpoint per condition and no training-seed replication.

**Conditions and plain-language labels:** `15b_pre_lambda1` means the user-
selected pre-reduction 15B endpoint; `17b_post_lambda0p1` means the user-
selected post-reduction 17B endpoint.

**Changed variables:** training history, checkpoint token coordinate, recorded
reconstruction coefficient, and associated microbatch/accumulation/CE-chunk/
optimizer/RNG history.

**Held fixed:** input IDs and masks, panel order, native site, width, Top-K,
pooling, analysis precision, statistical seed/draw count, source implementation
hashes, initial state identity, training-data manifest, tokenizer, and nominal
262,144 source-training tokens per update.

**Code / config / data identities:**

- Execution code: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/scripts/`
- Full config and source freeze: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/manifests/`
- Run root: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z/`
- Runtime: `5090-4-spot`, `shphd-lite-0911`, mounted SM120 layer.

**Known setup limitations:** model-local atom IDs are not aligned across
conditions; the panel bootstrap does not cover training stochasticity; the
before/after endpoints do not isolate coefficient causality; no semantics,
downstream utility, or language-loss endpoint was measured here.

## 5. Metrics And Registered Decision Rules

For record \(i\), let \(u_i\) be the 30,000-dimensional vector of selected-atom
frequencies over 256 valid tokens and 32 selected slots, normalized to sum to
one. The primary reuse statistic is the mean off-diagonal cosine

\[
R=\frac{2}{n(n-1)}\sum_{i<q}
\frac{u_i^\top u_q}{\|u_i\|_2\|u_q\|_2},
\qquad \Delta R=R_{post}-R_{pre}.
\]

The 95% interval resamples the 192 record IDs in pairs, 2,000 draws, seed
`20260922`. The uncertainty unit is a record, not a token, pair, checkpoint,
or training seed.

Native effective dimension uses centered covariance over the 192 mean-pooled
native writes:

\[
d_{eff}=\frac{\operatorname{tr}(\Sigma)^2}
{\operatorname{tr}(\Sigma^2)}.
\]

Registered branches are:

- `POST_HIGHER_REUSE_AND_LOWER_DIMENSION`: reuse CI entirely above zero and
  post dimension lower;
- `REUSE_INCREASE_WITHOUT_LOWER_DIMENSION`: reuse CI above zero but dimension
  gate fails;
- `PRE_HIGHER_REUSE`: reuse CI entirely below zero;
- `LOWER_DIMENSION_WITHOUT_REUSE_INCREASE`: dimension lower but reuse CI is not
  entirely positive;
- `UNRESOLVED_REUSE_DIFFERENCE`: reuse CI includes zero;
- `INSUFFICIENT`: identity, alignment, numerical, or artifact guard fails.

The current branch is `PRE_HIGHER_REUSE`.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| Post does not have higher same-ID reuse | CI entirely above zero would support post | Four `native_support.npz` files; hashes in `artifact_manifest.json` | `full_analysis.py` usage profiles and `reuse_metrics.py` paired cosine | 2,000 paired record bootstrap, seed `20260922` | \(\Delta R=-0.0223158395\), CI `[-0.0352508453,-0.0088839748]` | `ELIGIBLE` | `PRE_HIGHER_REUSE` | Fixed panel only; no training-seed uncertainty |
| Native dimension falls after transition | post dimension lower is the registered point gate | same four arrays, `a_mean` fields | centered covariance participation ratio; independently recomputed by `audit_completed.py` | 192 records; point estimate | pre `15.6743606802`, post `8.4184916947`, difference `-7.2558689855` | `ELIGIBLE` | dimension lower, but not sufficient for positive branch | not a semantic dimension or causal test |
| Native Top-32 extraction is faithful | no non-tie prefix mismatch and no zero selected values | four worker receipts | native encoder `encode`, score top-128 audit, finite checks | all `49,152` tokens/model | non-tie mismatches `0`; zero slots `0` | `ELIGIBLE` | guard pass | ties exist but produced no mismatches |
| Read-only numeric integrity | exact repeat and numerical agreement required | worker receipts and aligned arrays | repeated forward; CPU/GPU Gram and PR comparison | all four workers | repeat RMS `0`; Gram error `<=6.66e-16`; PR error `<=7.11e-15` | `ELIGIBLE` | guard pass | numerical integrity does not validate mechanism |
| Artifact/terminal completion | all required artifacts and terminal receipt | terminal/stage/artifact manifests | independent post-run audit | 22 manifest artifacts | application `PASS`; independent audit `PASS` | `ELIGIBLE` | measurement complete | separate Smoke was not run |

## 7. Main Results

### Eligible decision evidence

| Condition | Reuse \(R\) | Native \(d_{eff}\) | Distinct atoms | Effective atoms |
|---|---:|---:|---:|---:|
| 15B pre, `lambda=1.0` | 0.6476181362 | 15.6743606802 | 139 | 67.6265202728 |
| 17B post, `lambda=0.1` | 0.6253022967 | 8.4184916947 | 134 | 67.1667463649 |

The primary reuse change is `-0.0223158395` (`-3.45%` relative to pre), with
the entire paired-record interval below zero. Native effective dimension falls
by `7.2558689855` (`-46.29%`). Thus the two measured changes move in opposite
directions. Global atom coverage also changes only slightly: distinct atoms
fall by 5 and effective atom count falls by `0.4597739079` (`-0.68%`). These
coverage values are descriptive and do not rescue the failed primary branch.

### Bounded evidence

The result weakens “same-ID support reuse increases” as a necessary companion
of low native dimension for this transition. It does not distinguish decoder
direction geometry from coefficient covariance, residual covariance, or general
training-stage effects.

### Debug-only and ineligible evidence

No debug-only observation was used to determine the branch. No worker failed,
no condition was excluded, and no missing required artifact was found.

## 8. Visualization Results

### Intuition versus observation

![Intuition versus observation](figures/intuition_vs_observation.png)

**Purpose:** compare the registered expectation with the measured direction of
the two quantities.  
**Metric and source:** the right panel reads `analysis/result.json`; reuse is
the model-local mean usage-profile cosine contrast and dimension is native
participation ratio.  
**How to read:** the reuse interval lies entirely below zero while dimension
falls from 15.67 to 8.42.  
**Take-home:** lower dimension is present without higher same-ID reuse.  
**Limitation:** the diagram cannot identify why native covariance became lower
or attribute it to `lambda_rec`.

### Reuse and native-geometry concentration curves

![Reuse and native geometry](figures/reuse_history_contrast.png)

**Purpose:** show the primary interval beside descriptive atom-use and native
variance concentration curves.  
**Source:** `tables/primary.csv`, `tables/conditions.csv`, and
`tables/concentration_curves.csv`; figure manifest hash is recorded below.  
**Aggregation:** primary is paired record bootstrap; curves are whole-panel
descriptive cumulative distributions.  
**How to read:** the left interval is wholly negative; the center and right
curves are not independent significance tests and atom ranks are independently
sorted within each model.  
**Take-home:** the registered branch is `PRE_HIGHER_REUSE`, despite a lower
post native dimension.  
**Limitation:** no cross-model feature-ID alignment or decoder-angle analysis is
shown.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
|---|---|---|---|---|---|
| Source and local audit | frozen-source SHA checks; 12 unit tests | `PASS` | none | schema and estimator regressions | checkpoint-history confounding |
| Target preflight | mounted Blackwell runtime, four RTX5090 identity, frozen inputs | `PASS` | none | wrong profile/image/GPU and changed inputs | scientific endpoint uncertainty |
| Worker extraction | four receipts, 96 records per worker, model manifest validation | `PASS` | none | partial worker completion and wrong checkpoint lambda | no training-seed replication |
| Panel alignment | 192 IDs, token positions, counts equal across conditions | `PASS` | none | sample/mask mismatch | panel representativeness |
| Native Top-32 support | finite values, zero slots `0`, non-tie mismatch `0` | `PASS` | none | known top-k boundary substitution | decoder geometry |
| Read-only/numerical | repeat RMS `0`, state/version/dictionary unchanged, CPU/GPU checks | `PASS` | none | mutation and arithmetic drift | causal interpretation |
| Registered analysis | primary table, condition table, figures, terminal | `PASS` | none | incomplete measurement | mechanism rival |
| Independent post-run audit | 22 artifacts, recomputed cosine/PR/bootstrap | `PASS` | none | producer-only numerical error | interpretation remains human-owned |

**Falsified physical prior:** not a general falsification of sparse
reconstruction pressure; only the predicted increase in this same-ID reuse
observable fails in this endpoint contrast.  
**Falsified mathematical model:** the necessary conjunction “reuse increases
and dimension decreases” is not supported here; the broader covariance model is
not falsified.  
**Falsified operationalization / proxy:** not a failed measurement proxy;
native support and statistics passed their guards.  
**Falsified implementation:** no implementation failure found.  
**Falsified metric:** no metric arithmetic failure found.  
**Remaining rival explanations:** decoder direction collinearity, coefficient
covariance, residual/cross-covariance changes, and ordinary history/stage drift.

## 10. Full Experiment Record

**Question or hypothesis tested:** whether post-transition lower native
dimension is accompanied by increased same-ID reuse.

**Setup:** exact 15B pre and 17B post checkpoints, fixed 192-record panel,
native layer-7 site, Top-32, four read-only RTX5090 workers, no optimizer
updates.

**Training data:** no new training data pass; checkpoint provenance uses the
recorded source training manifest and tokenizer identity.

**Testing data and split:** one fixed 192-record paired N8 panel, 256 valid
tokens per record; no labels or fit/tune split.

**Result:** terminal and application PASS; eligible branch
`PRE_HIGHER_REUSE`; independent QA agrees. Primary and full artifacts are in
the execution run root listed in §15.

**Insight and next decision:** the lower-dimensional post endpoint does not
show higher same-ID reuse. AI建议 is to redirect the next mechanism test to
decoder geometry/coefficient covariance, or design a strict matched fork if the
question is specifically the causal effect of `lambda_rec`. Researcher
confirmation is required before updating the Anchor judgment.

## 11. Interpretation

The direct scientific update is negative for the current mechanism’s necessary
prediction: lower native effective dimension occurred together with *lower*,
not higher, same-ID activation-profile similarity. The result therefore stops
the simple explanatory chain

```text
coefficient reduction -> shared same-ID support reuse -> lower native dimension
```

as an adequate explanation for this transition contrast. It does not imply
that the post model has no reuse, or that decoder directions are not shared;
the measured reuse statistic is limited to within-model ID-frequency similarity.

The most informative remaining observation is the mismatch between the two
metrics. It makes a decoder-geometry/coefficient-covariance explanation more
plausible than the current same-ID reuse explanation, but this is an
interpretive update, not a measured decomposition. The comparison remains
confounded by endpoint position and training-history changes beyond the
coefficient.

## 12. Claim Boundary

**Can claim:**

- The full read-only measurement is complete and eligible under E03.
- On this fixed 192-record panel, `R_pre=0.647618` and `R_post=0.625302`, with
  `post - pre=-0.022316` and paired 95% CI `[-0.035251,-0.008884]`.
- Native effective dimension falls from `15.674361` to `8.418492`.
- The registered positive necessary-condition branch is not met; the typed
  branch is `PRE_HIGHER_REUSE`.

**Cannot claim:**

- The isolated causal effect of reducing `lambda_rec`.
- That lower native dimension is beneficial, semantic, or task-useful.
- That same-ID reuse is absent or irrelevant in every model or training stage.
- Cross-model atom identity, training-seed generalization, or article-level
  replication.
- That decoder geometry or coefficient covariance has already been proven as
  the cause.

## 13. Next Decision

**Decision:** `AI 建议` — treat increased same-ID support reuse as not supported
for this transition and choose one discriminator before making a mechanism
claim: (a) decompose decoder-direction geometry and coefficient covariance on
the two existing checkpoints, or (b) if the target claim is specifically a
coefficient effect, run a matched fork that changes only `lambda_rec` while
holding the training contract fixed.

**Completion criterion:** the chosen next analysis must report the contribution
of the candidate decoder/coefficients terms on the same panel and state whether
it explains the native dimension drop independently of the failed reuse
prediction; a matched fork must preserve effective batch, CE chunking, sampling,
optimizer, and token-aligned schedules.

**Resume action:** researcher confirms the mechanism update and selects either
the existing-checkpoint geometry decomposition or a strictly matched causal
ablation. Do not update the Anchor or close the Focus solely from the AI draft.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|---|---|
| `stages/FULL_MEASUREMENT_PASS.json` | terminal full-run gate | `run_full.py` E03 | four worker receipts and analysis | `5063860ff892154852bca664030665f6b4488bb0c591a23a7ae2b27388552fde` | yes | yes | registered branch `PRE_HIGHER_REUSE` |
| `analysis/result.json` | primary result and typed verdict | `full_analysis.py` E03 | aligned worker arrays | `d6e0f99d335e58f0802ed7ba69039355a8361872548e2d5a3c96a0a99f05c3a0` | yes | yes | human mechanism field remains awaiting researcher |
| `tables/primary.csv` | primary delta and CI | `full_analysis.py` E03 | usage arrays | `e763af18f68973bb024907c0ab595fdf0f862a43009ada74a0d8f9fcbf88a79b` | yes | yes | 2,000 paired draws |
| `tables/conditions.csv` | condition-level reuse/dimension | `full_analysis.py` E03 | aligned arrays | `b71792eb427d9477ca7b97be08b45e1e722158ebe50d47e66bb62b3d42480d24` | yes | yes | descriptive dimension gate |
| `figures/figure_manifest.json` | figure sources and hashes | `build_full_figures.py` E03 | result and curves | `b0abf1b2ccd1a9a038b915359b7089fbcf0d0bd60af4b5d7465d3f36868982dd` | yes | yes | two decision-bearing figures |
| `artifact_manifest.json` | all 22 raw/derived artifact hashes | `run_full.py` E03 | worker outputs and derived files | `72e1acd0cd8b0ac4bad6b69f8389c72459f21fd25894a4ae6968940a501cc637` | yes | yes | source of worker-array hashes |
| `independent_audit.json` | independent numerical/artifact QA | `audit_completed.py` | artifact manifest and result | `687530942e10570023f55a62bf0dc592cc0d5ce617f17c98ec8509e7dc33159d` | yes | QA only | agrees with delta, CI, dimensions |
| `terminal_receipt.json` | platform/application completion | `run_full.sh` | stage gate and worker receipts | `66a97498fa88aae6c613c309348a481eb3ba2cc9afd0b3cef3ec4a3c52d3ba20` | yes | execution only | platform `SUCCEEDED`, app `PASS` |

The four worker arrays and receipts are listed individually in the run root's
`artifact_manifest.json`; all 22 listed artifacts were independently verified.

## 15. Links

- Anchor: `/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md`
- Protocol: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E03_lambda_transition_reuse_audit/protocol.md`
- Summary: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E03_lambda_transition_reuse_audit/summary.md`
- Chinese summary: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E03_lambda_transition_reuse_audit/summary_cn.md`
- Code workspace: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit`
- Run root: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z`
- Config and freeze: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/manifests/full_config.json` and `manifests/full_freeze.json`
- Primary result: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z/analysis/result.json`
- Figures: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z/figures/`
- Logs and receipts: `/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z/worker_*.log` and `worker_*/receipt.json`
- Job: `pt-7stjld8g`
- Reproduction command: `export RUN_ROOT=/data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/runs/full_4x5090_20260922T134500Z && bash /data/250010109/MoE_Router/experiments/20260922_s7_lambda_transition_reuse_audit/scripts/run_full.sh`
