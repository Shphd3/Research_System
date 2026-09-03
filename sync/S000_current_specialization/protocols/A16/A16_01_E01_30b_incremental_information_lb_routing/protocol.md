---
experiment_id: A16_01_E01_30b_incremental_information_lb_routing
anchor_id: 16_01_incremental_information_lb_routing
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-10
design_frozen_at: 2026-08-10
resource_profile: 5090-8-spot
primary_metric: paired_document_30b_endpoint_nll_contrast
---

# Protocol: A16_01_E01 30B Incremental-Information Routing Under Differentiable LB

## 0. Approval Snapshot

**Purpose.** Test whether an explicit low-rank path over the actual same-layer attention-visible increment improves 30B language modeling under verified differentiable load balance (LB), and whether a separately certified direction has value beyond a same-rank random path.

**Primary Anchor.** [A16_01 Incremental-Information Routing](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md).

**Treatment and controls.** Native-LB, Trainable-Innovation-LB, Certified-Innovation-LB, and Haar-Innovation-LB in seeds 17 and 29. All eight jobs start at step 0. Certified and Haar remain exact dormant Native behavior until the first common 2B/5B/10B milestone that passes both registered admission gates.

**Changed variable.** The source and identity of one residual Router-logit branch over the same-layer increment. **Held fixed:** base model, expert computation, top-1 routing, data order, initialization within seed, optimizer, scheduler, differentiable LB coefficient, capacity, total-token endpoint, evaluation documents, and Certified/Haar launch state.

**Primary metric.** Document-paired held-out next-token NLL at 30B total tokens, in nat/token; lower is better. Engineering compares Trainable minus Native. Scientific identity compares Certified minus Haar and requires Certified minus Native in the same direction.

**Pass.** Each registered comparison is a typed verdict. A Pass requires a negative point estimate and a paired-document 95% interval below zero separately in both seeds. **Fail:** complete valid evidence misses that rule. **Insufficient:** any hard identity, LB-gradient, recovery, data, admission, or endpoint guard fails. No common E1+E2 certificate by 10B yields `INSUFFICIENT_NO_CERTIFICATE`; Certified/Haar remain dormant to 30B and do not form a scientific comparison.

**Execution scope approved.** Protocol, implementation, unit tests, single-GPU smoke, four-arm 8×5090 smoke using a synthetic fixed frame for Certified/Haar implementation checks, submission of all eight full jobs, and milestone E1/E2 evaluation/activation are approved. Full submission does not authorize Git, graph, sync, or publication actions.

**Cannot claim.** A Pass cannot establish universal semantic hierarchy, scale transfer, that the engineering projection is semantic, that LB causes the gain, or that expert specialization is the unique mediator.

## 1. Terminology / Definitions

- **Old state** $n_\ell^{old}$: the normalized token state immediately before the layer's attention output is added.
- **New state** $n_\ell^{new}$: the normalized post-attention state actually available to the current MoE Router.
- **Visible increment** $u_\ell=n_\ell^{new}-n_\ell^{old}$: what the attention write changes at the Router-visible normalization site. It is not a claim of new Shannon information.
- **Innovation branch:** an additive low-rank Router-logit path over $u_\ell$ that leaves the native full-state Gate present.
- **Certified direction:** a frozen rank-56 frame learned without endpoint NLL and admitted by both E1 conditional-readability and E2 expert-utility tests.
- **Haar direction:** a fixed orthonormal random frame with the same layer set, rank, scaling, parameters, launch state, and training duration as Certified.
- **Differentiable LB:** the Switch auxiliary loss whose soft-probability path produces an actual nonzero Gate gradient; logging a scalar LB value is not sufficient.
- **30B endpoint:** 30,000,021,504 cumulative training tokens (step 38,147), not 30B additional tokens after a conditional branch is activated.

## 2. Anchor Alignment

This experiment implements the A16_01 core model and primary metric without changing its claim boundary. It is a **method-construction comparison** supported by the established actual-increment identity and protected by a certified-direction gate. It does not replace A15_07: A15 owns semantic direction admission; A16_01 owns long-run Router training under verified LB.

The strongest rival is that any gain comes from extra low-rank capacity, regularization, delayed activation, or load changes. Native controls the absence of a branch; Haar controls direction identity after admission; paired tokens/FLOPs and launch state protect optimization comparisons.

## 3. Tested Hypotheses

1. **Engineering utility:** Trainable-Innovation-LB has lower 30B held-out NLL than Native-LB in both seeds.
2. **Scientific direction identity:** if a common certificate exists, Certified-Innovation-LB has lower 30B held-out NLL than both Haar-Innovation-LB and Native-LB in both seeds.

The two hypotheses receive separate typed verdicts. Engineering success cannot rescue a missing or failed scientific comparison.

## 4. Rival Explanations

| Rival | Separating condition or guard |
| --- | --- |
| Extra parameters or generic low-rank regularization | Certified versus parameter-matched Haar; report parameter and FLOP differences for Trainable versus Native |
| Different launch checkpoint or training duration | Certified and Haar run dormant from step 0, verify exact Native identity before $t^*$, activate together, and end at the same 30B total tokens |
| LB telemetry without LB optimization | LB-only backward and LM+LB shadow-update guards under activation checkpointing |
| The native Gate already uses all useful increment information | Trainable versus Native endpoint comparison |
| Semantic readability without expert utility | E2 expert-choice-regret gate before Certified training |
| NLL gain caused only by different hard load | paired load/capacity telemetry; it explains but does not replace endpoint NLL |

## 5. Data Construction And Provenance

### 5.1 Language-model training and endpoint evaluation

- Training source: `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`.
- Sequence length: 1,024; global batch: 768 sequences; 786,432 tokens per optimizer step.
- Endpoint evaluation uses the frozen 1,024-document artifact currently registered by the verified 30B runner:
  `/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`, with its companion manifest `eval_tokens.json`.
- Preflight must record SHA-256 for training binaries, tokenizer, evaluation tensor, and manifest. All arms use identical document order. Endpoint documents cannot fit a direction, readout, threshold, or checkpoint.

### 5.2 E1 representation bank

Use the frozen 1,920-record English conditional-fine taxonomy bank with SHA-256 `ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4`: eight parents, eight children per parent, and ten TRAIN, ten DEVELOPMENT, and ten CONFIRMATION expressions per child. Only TRAIN constructs $\mu,S,P$; DEVELOPMENT verifies cross-expression direction stability; CONFIRMATION is opened once per registered milestone after choices freeze. The bank is evaluation/calibration material and never enters LM optimization.

### 5.3 E2 expert-utility bank

Before smoke, freeze a DCLM functional bank disjoint by document hash from the LM endpoint artifact and the training shard. Split by whole documents into FIT, DEVELOPMENT, and CONFIRMATION. FIT trains frozen small Router readouts; DEVELOPMENT selects optimizer stopping only; CONFIRMATION computes expert-choice regret once. Counterfactual expert losses and semantic labels from E1 are forbidden from LM training.

The frozen bank contains 384 independent 256-token DCLM documents, 128 per split. Its tensor SHA-256 is `827129cdf5b1d44af06a034b607e40c98d5353ac8e5276b994b906c917479fd5`; its manifest SHA-256 is `0a8a00d2370735821bb553fcc5f27a8c7c0006a749e4d5b4628c8df2ee6f0192`. The manifest records every source line, document hash, deterministic slice, and token hash, and verifies zero document-hash overlap with the 1,024-document endpoint artifact.

## 6. Learning Task And Permitted Supervision

The full training task is ordinary next-token prediction. Each online Router receives only tensors causally available at its current layer and returns eight expert logits for top-1 selection.

Trainable-Innovation receives $u_\ell$ and learns a rank-56 factor end to end from LM+LB gradients. It receives no taxonomy label or expert-utility target. Certified/Haar receive frozen projections of the current sample's $u_\ell$; offline matched pairs are never online inputs.

E1 may use taxonomy child identities only to learn and certify $P$. E2 may use frozen counterfactual per-expert losses only to test whether $P^\top u$ predicts expert relative utility. Neither supervision source may update the backbone, experts, native Gate, or the 30B training objective.

## 7. Model / Architecture And Frozen Variants

All conditions use the verified four-layer Qwen-style MoE: hidden size 768, six query heads, three key/value heads, head dimension 128, eight sparse experts plus one shared expert per layer, sparse-expert intermediate size 1,536, and top-1 routing. Native construction must reproduce 251,199,232 trainable parameters, 152,108,800 active parameters per token, and 24,576 native Router parameters before arm-specific additions.

For every layer:

$$
n_\ell^{old}=N_\ell(h_\ell),\quad
n_\ell^{new}=N_\ell(h_\ell+a_\ell),\quad
u_\ell=n_\ell^{new}-n_\ell^{old}.
$$

1. **Native-LB:** $g=Wn^{new}$.
2. **Trainable-Innovation-LB:** $g=Wn^{new}+BA^\top\operatorname{RMS}(u)$, with $A\in\mathbb R^{768\times56}$ trainable and $B\in\mathbb R^{8\times56}$ zero-initialized. The branch exists in all four layers and adds 173,824 trainable parameters.
3. **Certified-Innovation-LB:** on the common E1+E2 eligible layer set $\mathcal L^*$, $g=Wn^{new}+CP^\top S^{-1}(u-\mu)$; $P,\mu,S$ are frozen and $C$ is zero-initialized. Other layers remain Native.
4. **Haar-Innovation-LB:** identical to Certified except $P$ is replaced by a deterministic per-seed same-rank Haar frame. Its trainable parameter count and online matrix multiplications must equal Certified exactly.

Certified and Haar use rank 56 at the admission test and after activation. Before $t^*$ their branches are present but multiply to exact zero. The eligible layer set is the intersection of layers passing E1 and E2 in both seeds at $t^*$. No endpoint result may choose the layer set. Experts always receive the full native local representation.

## 8. Training Objective And Optimization

The next-token cross-entropy $L_{LM}$ and microbatch Switch LB are

$$
L_{LB,\ell}=8\sum_{e=1}^8\left(\frac1T\sum_xp_{\ell,e}(x)\right)f_{\ell,e},
\qquad
L=L_{LM}+0.01\sum_{\ell=1}^4L_{LB,\ell}.
$$

$p$ is the full softmax probability and $f$ is the stop-gradient hard top-1 token fraction. The implementation must preserve the repaired auxiliary-tensor autograd path under activation checkpointing.

Use BF16, AdamW, learning rate $10^{-4}$, betas $(0.9,0.95)$, weight decay 0.01, 636 warm-up steps, the verified 100B-token scheduler horizon, ZeRO-1, and activation checkpointing. New zero-output branch parameters receive zero AdamW moments at creation. No performance-based checkpoint selection or early stopping is allowed.

## 9. Conditions, Seeds, And Checkpoints

Seeds are 17 and 29. Within each seed, Native and Trainable share the same common model/expert initialization, data order, and applicable RNG stream. Arm-specific initialization must not consume the common model RNG stream.

| Arm | Start | Endpoint | Jobs |
| --- | --- | --- | ---: |
| Native-LB | step 0 | 30B total | 2 |
| Trainable-Innovation-LB | step 0, zero-output branch | 30B total | 2 |
| Certified-Innovation-LB | step 0, dormant until $t^*$ | 30B total | 2 |
| Haar-Innovation-LB | step 0, dormant until $t^*$ | 30B total | 2 |

Full checkpoints and independent evaluations occur at 2B (step 2,544), 5B (6,358), 10B (12,716), 20B (25,432), 25B (31,790), and 30B (38,147). Certified/Haar save all registered milestones plus any activation receipt. Their jobs may wait at each admission milestone for the frozen gate receipt; they may not activate from a partial or post-endpoint choice. SPOT recovery is allowed only from a complete registered checkpoint.

Full-job count is eight, each on one node with eight RTX 5090 GPUs. A dormant Certified/Haar trajectory is an executed engineering run but is not eligible as a scientific arm without the gate receipt.

## 10. Primary Metric And Frozen Analysis Plan

For each endpoint document $j$, compute mean next-token NLL under each arm. For comparison $A-B$ in seed $s$:

$$
\Delta_{s,j}(A-B)=NLL_{s,j}^{A}-NLL_{s,j}^{B}.
$$

The seed-specific estimate is the equally weighted document mean. Resample complete documents with replacement 2,000 times using a frozen seed to form a two-sided 95% paired bootstrap interval. No document, token, layer, or seed is excluded as an outlier. A missing or non-finite document makes the affected endpoint insufficient until deterministically reconstructed.

- **Engineering Pass:** for both seeds, mean $\Delta(Trainable-Native)<0$ and the 95% upper bound is below zero.
- **Scientific Pass:** an eligible $t^*$ exists and, for both seeds, the means and 95% upper bounds of both $\Delta(Certified-Haar)$ and $\Delta(Certified-Native)$ are below zero.
- **Fail:** the relevant full comparisons are valid and complete but the corresponding Pass rule fails.
- **Insufficient:** a hard guard or evidence-completeness rule fails. No $t^*$ by 10B is the typed scientific outcome `INSUFFICIENT_NO_CERTIFICATE`, not a training Fail.

The two-seed equal-weight mean is descriptive only. NLL AUC and late slope cannot replace the endpoint rule. Analysis unseals only after both relevant 30B endpoints and per-document arrays are complete.

## 11. Secondary Metrics And Guards

Record per milestone and layer: LM NLL, LB scalar and coefficient, LB-only/native/innovation Gate gradient norms, busiest-expert share, route entropy, capacity drop, branch/native logit RMS ratio, branch/native logit cosine, route divergence from Native, expert-choice regret on the frozen bank, throughput, theoretical FLOPs, wall clock, and TensorBoard scalars.

For Certified/Haar also record $P^\top P$ error, standardization statistics, direction hash, eligible layer set, launch hash, and frozen-frame identity. Secondary metrics explain mechanisms and compute cost; they cannot reverse a primary Fail.

Hard guards:

1. $n^{new}=n^{old}+u$ within registered BF16/FP32 replay tolerance at every layer.
2. Zero-output branches reproduce Native logits, top-1 route, LM loss, and LB loss at launch.
3. LB-only backward gives finite nonzero gradients to every native Gate; after one update it reaches the innovation head, and after the head becomes nonzero it reaches Trainable $A$ and the upstream increment path.
4. Certified $P$ is frozen; Haar is orthonormal; Certified/Haar layer set, rank, parameter count, and online FLOPs match.
5. Model, optimizer, scheduler, RNG, data cursor, branch state, and token hashes recover exactly at registered precision.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** an injected rank-56 signal in $u$ that predicts a constructed expert utility is recovered by E1/E2 and changes only the innovation logits after the head is nonzero.
- **Known bad:** $u=0$, identical paired expressions, within-parent label permutation, and a zero LB coefficient must not create a certificate or LB-only Gate gradient.
- **Known confusing:** a trainable branch can improve NLL while Certified does not; this supports engineering capacity but not certified identity. Certified and Haar can both improve over Native; this supports a generic stable side path, not semantic direction identity.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / How | Required output and handoff |
| --- | --- | --- | --- |
| P0 preflight | Freeze identities and resources | Verify model/data/eval/TAX artifacts, hashes, 30B schedule, 8×5090 profile, storage | signed manifest; failure blocks implementation smoke |
| P1 unit and single-GPU smoke | Validate object and gradients | synthetic and real microbatches; reconstruction, no-op, LB backward, two-step branch-gradient test | typed smoke JSON; all hard guards must pass |
| P2 distributed smoke | Validate real 8-GPU execution | each arm interface, synthetic frozen frame for Certified/Haar only, save/resume, token hash, TensorBoard | distributed smoke verdict; synthetic certificate cannot authorize scientific full |
| P3 full submission | Produce all paired trajectories | submit all four arms × seeds 17/29 from step 0; Certified/Haar stay dormant | eight job receipts and milestone checkpoints |
| P4 admission | Find earliest eligible scientific launch | run E1 then E2 on 2B, else 5B, else 10B Native checkpoints | gate receipt with per-seed/layer evidence and $t^*$, or `NO_CERTIFICATE_BY_10B` |
| P5 activation | Test direction identity | if and only if P4 passes, load Certified/Haar frames into the already running matched dormant jobs; otherwise keep them dormant through 30B | activation and identity receipts, or dormant-to-30B receipt |
| P6 endpoint evaluation | Freeze primary evidence | evaluate all eligible 30B arms on same documents and run paired bootstrap | per-document arrays, contrasts, typed verdicts |

Scientific underperformance, concentrated load, small innovation logits, or poor early NLL must not stop a numerically valid full run. NaN/Inf, OOM, communication failure, corrupted checkpoint, data/hash divergence, invalid LB backward, broken frame, or unrecoverable missing endpoint stops the affected job and records Insufficient until repaired without scientific change.

## 14. Algorithm, Output, And Provenance Contract

Implementation must be copied into a new immutable worker surface derived from the verified differentiable-LB runner; no raw output, checkpoint, activation cache, or unfiltered log enters Research_System. Raw roots are under `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/`.

Required artifacts are: source manifest and hash, frozen configs, data manifests, unit/smoke verdicts, step-0 and launch identity receipts, job ledger, TensorBoard event files, milestone metrics, complete checkpoints, E1/E2 gate ledger, per-document endpoint NLL arrays, paired-bootstrap table, parameter/FLOP table, and failure receipts. Curated `summary.md`, `detailed.md`, tables, and decision figures are written here only after evidence audit.

Job names:

- `a16-inc-native-s17`, `a16-inc-native-s29`
- `a16-inc-trainable-s17`, `a16-inc-trainable-s29`
- `a16-inc-certified-s17`, `a16-inc-certified-s29`
- `a16-inc-haar-s17`, `a16-inc-haar-s29`

Resources are ACP, workspace `share-space`, AEC2 `computing-cluster-5090-01g`, worker spec `n12lp.nn.i10a.8`, eight processes, SPOT quota, normal priority.

## 15. Success / Failure / Insufficient Evidence

The experiment produces two typed endpoint verdicts, `engineering_utility` and `certified_direction_identity`, plus one execution-validity verdict. Only the rules in Section 10 decide them. A run receipt or smooth loss curve is not a scientific Pass. An E1-only semantic certificate is not E2 functional admission. A missing certificate is preserved as scientific Insufficient rather than replaced by an arbitrary frozen direction.

## 16. What This Cannot Claim

This experiment cannot establish that conditional-fine directions are universal, that every layer creates new information, that the engineering projection has semantic identity, that two seeds establish scale-general behavior, that LB is beneficial or harmful in general, or that endpoint NLL changes are caused uniquely by expert specialization rather than optimization or regularization.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Confirmation basis |
| --- | --- | --- |
| A Question and boundary | CONFIRMED | user approved two implementations, matched LB training, 30B comparison |
| B Data and provenance | CONFIRMED | reuse verified DCLM/evaluation sources; semantic and utility banks remain isolated |
| C Task and supervision | CONFIRMED | LM+LB online task; E1/E2 supervision cannot enter LM training |
| D Architecture | CONFIRMED | native residual path plus engineering/certified/Haar innovation variants |
| E Objective and optimization | CONFIRMED | verified microbatch Switch LB, coefficient 0.01, inherited 30B optimizer contract |
| F Comparison and decision evidence | CONFIRMED | four-arm maximum, two seeds, endpoint paired NLL, typed gate and verdict rules |
| G Execution and reproducibility | CONFIRMED | implementation, smoke, all eight full submissions and registered activation on 8×5090 approved |

Cross-block consistency: `PASS`. Scientific body and decision-bearing configuration freeze at the first implementation smoke. After execution starts, any material change requires an append-only amendment stating before/after values, reason, observed-data status, affected arms, user approval, and evidence-eligibility impact. Execution receipts and result links may be appended; observed results and interpretations belong in `summary.md` and `detailed.md`.

### Amendment A16_01_E01-AMEND-20260810-01: deterministic certificate coordination

- **Time:** 2026-08-10T18:28:17Z.
- **Before:** Sections 7, 9, and 13 froze a two-seed common E1+E2 certificate and matched dormant Certified/Haar activation, but did not fully specify producer/consumer ordering, wait semantics, or the state-identity check at artifact consumption.
- **After:** the seed-17 and seed-29 Native jobs independently produce candidate layer decisions; only layers admitted by both Native candidates form the common certificate layer set. Certified and Haar are independent, lazy consumers of their own arm-specific artifact. Before either consumer activates, its canonical model-state digest (parameters, persistent buffers, and registered step) must exactly equal the same-seed Native digest. `wait_seconds=0` means wait without a timeout; any finite timeout raises and stops the affected consumer and must never mark that milestone as checked. Production E1 rank is fixed at 56. Full submission order is Native 17/29, Trainable 17/29, Certified 17/29, then Haar 17/29.
- **Reason:** remove certificate-arrival races and prevent a late artifact or timeout from silently becoming a false no-certificate decision while preserving the registered two-seed common gate and paired launch identity.
- **Observed-data status:** implementation tests and smoke receipts existed; no full-run milestone, admission, endpoint NLL, or scientific result had been observed.
- **Affected blocks / conditions:** execution block G and stages P3--P5; Native, Certified, and Haar coordination only. The four scientific conditions, E1/E2 thresholds, rank, training objective, primary metric, and verdict rules are unchanged.
- **Approval:** user-approved execution amendment in the 2026-08-10 implementation-and-submission request.
- **Eligibility impact:** none when the added digest, wait, and ordering guards pass. A digest mismatch or finite-timeout exception makes the affected activation path Insufficient; it cannot be reclassified as `NO_CERTIFICATE_BY_10B`.

### Amendment A16_01_E01-AMEND-20260810-02: device-independent projection validation

- **Time:** 2026-08-10T19:02:00Z.
- **Before:** the rank-56 projection orthogonality and Gram guard was evaluated on the active CUDA tensor in float32, so RTX 5090 TF32 matrix multiplication could make a valid QR basis appear to exceed the unchanged $10^{-5}$ tolerance.
- **After:** projection validation is computed deterministically on a detached CPU float64 copy before installation. The registered $10^{-5}$ tolerance, rank 56, projection values used by the model, and all scientific conditions remain unchanged. The same validator is used by install, certificate activation, smoke, and resume paths; an actually non-orthogonal basis is still rejected.
- **Reason:** the first distributed smoke rejected a valid QR basis with a GPU Gram error of about $7\times10^{-5}$ although the same stored basis had CPU-float64 error about $1.4\times10^{-6}$. This was a device-precision false rejection, not a scientific failure.
- **Observed-data status:** the fault was observed only during P2 smoke job `om-jmdqeig5`; no full job, milestone, certificate decision, endpoint NLL, or scientific comparison existed.
- **Affected blocks / conditions:** execution block G and numerical parts of P1--P2 only. Training data, initialization, model equations, LB objective, rank, optimizer, checkpoint schedule, admission thresholds, endpoint metric, and verdict rules are unchanged.
- **Approval:** covered by the user's explicit request to repair the implementation, complete smoke, and submit all full jobs once correctness was established.
- **Eligibility impact:** none for jobs launched from the corrected immutable worker after the validator and bad-basis regression tests pass. The failed pre-fix smoke is retained as engineering provenance and is not scientific evidence.

### Amendment A16_01_E01-AMEND-20260811-03: canonical hashing of scalar persistent state

- **Time:** 2026-08-11T03:42:00Z.
- **Before:** the certificate coordinator read canonical model-state bytes with `tensor.view(torch.uint8)`. At the first 2B milestone, PyTorch rejected direct byte reinterpretation of the zero-dimensional `int32` persistent buffer `active_rank`; all six Native, Certified, and Haar trajectories stopped after writing complete `checkpoint-2544` artifacts. Trainable does not invoke this certificate-coordination path and continued uninterrupted.
- **After:** without changing tensor name, dtype, shape, registered step, or byte content, the tensor is first flattened with `reshape(-1)` and then read as `uint8`. Two regressions prove that scalar persistent buffers hash successfully and that the registered step still changes the digest. Recovery begins only from each original run's complete registered `checkpoint-2544`; the endpoint remains step 38,147.
- **Reason:** repair a shape-compatibility defect in certificate-state serialization. The failure occurred in milestone orchestration, not Router forward, LB backward, optimizer update, or checkpoint writing.
- **Observed-data status:** the six affected trajectories exposed only their 2B checkpoints and an engineering milestone exception; no certificate verdict, 30B endpoint NLL, or primary contrast existed. Both Trainable trajectories were uninterrupted. Observed 2B losses were not used to change the model, data, thresholds, or recovery point.
- **Affected blocks / conditions:** canonical-state digesting in P4--P5 and engineering recovery of the six Native/Certified/Haar trajectories only. Arms, seeds, step-0 states, training tokens, LB coefficient, rank, optimizer, scheduler, saves, E1/E2 gate, primary metric, and verdict rules are unchanged.
- **Approval:** explicitly authorized by the user's 2026-08-11 request to inspect the jobs, correct the new implementation, and submit the 30B training.
- **Verification and eligibility:** immutable worker v8 passed 86/86 local tests; the target 8×5090 runtime passed both scalar-hash regressions; distributed smoke `om-lo6v9cvi` `SUCCEEDED` with all four arms passing differentiable LB, 0/2/3 save-resume, common step-0 and token hashes, plus zero-error active-certificate continuation on all eight ranks for Certified and Haar. The old failed jobs are not endpoint evidence. Trajectories recovered by v8 from complete 2B checkpoints retain their original scientific eligibility if all resume guards pass.
