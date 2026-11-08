派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol.md)；研究修改仍回到原件。

---

# Protocol: R01 paired expert allocation and token frequency

## 0. Approval Snapshot

- Document status: `APPROVED_FOR_SMOKE_AND_GATED_PAIRED_TRAINING`; implementation, joint smoke and complete paired training/evaluation are authorized, with formal training gated by the registered joint engineering freeze below.
- Approval source: the researcher's 6 November 2026 request, including “请完整执行” and the explicit four-H100 reserved requirement. This covers source checks, architecture/accounting, common smoke qualification, budget selection, A/B training and full evaluation. No repeated approval is required for that same scope.
- Block audit: A–G are covered by the user's explicit question/design and delegated engineering choices below; actual smoke-derived S/thresholds and current hashes are filled in the immutable joint freeze before formal training. This is a factual engineering gate, not a missing human judgment.
- Cross-block consistency: question/model/metric alignment PASS; exact executable configuration PENDING joint freeze.
- Registered revision: R01, scientific plan fixed before final-test model metrics/evaluation; exact code/config/data hashes and token budget are recorded in the joint freeze before full training.
- Purpose: determine whether moving the same expert capacity deeper has potential for relatively low-frequency token prediction and what overall cost accompanies it.
- Primary Anchor: [15_31](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_31_depth_expert_allocation/15_31_depth_expert_allocation_anchor.md).
- Confirmed active Focus: [depth_expert_allocation](../../../../focus/focus_depth_expert_allocation.md).
- Experiment role: operationalization or proxy test; token-frequency learning, not a semantic or causal mechanism confirmation.
- Primary metric: final low-frequency token NLL difference, B minus A, in nat/token.
- Minimal comparison: random-initialized, eight-layer native ordinary MoE; A uniform versus B deep-increasing.
- Changed variable: expert count at each layer. Held fixed: expert-count sum, hidden width, expert width, attention, top-k, shared-expert setting, vocabulary interfaces, training objective/policy, exposure and order.
- Supporting/non-supporting/insufficient outcomes: see §15. Cannot claim semantic long-tail representations, gradient signal-to-noise improvement or causal routing mediation.
- Conditions: A and B required; C decreasing allocation is not scheduled and must not displace A/B completion. A shallow-narrow/deep-wide sketch is accounting only, `NOT RUN`.

## 1. Terminology / Definitions

An expert is a separate SwiGLU feed-forward module. Top-k selects k experts per token at every layer. Dispatch means selecting, gathering and combining their computations. The router computes scores for all local experts. “Active parameters” denotes the explicitly declared accounting convention, not measured FLOPs.

A target token is one valid next-token prediction counted once across data-parallel ranks. A token type is a tokenizer vocabulary ID. An exposure count is a type's number of appearances in the frozen actual training stream; its scope and treatment of context/target positions are frozen in the data manifest. Low-frequency seen types and unseen types are separate. NLL is mean negative log probability in natural logarithms; perplexity is exp(overall NLL). Frequency-bucket means are token-weighted unless explicitly labeled otherwise.

## 2. Anchor Alignment

The advisor's proposed shallow/few-expert and deep/many-expert shape motivates the allocation variable. The core uncertainty is predictive behavior under fair capacity and exposure. This round deliberately leaves the residual width unchanged. Its result can justify or discourage further tests of this allocation, without inferring a representation mechanism from token-frequency loss.

## 3. Tested Hypothesis

H1: B lowers low-frequency seen-token endpoint NLL at the same training token budget. H2: it may trade low-frequency performance against high-frequency or overall performance, or yield no advantage. H3: route loads may change, but those changes require measurement and remain correlational. The user's final boundary is preserved: even favorable results show potential only in this tested data/budget.

## 4. Rival Explanations

| Rival | Distinguishing guard | Remaining boundary |
| --- | --- | --- |
| Extra total capacity | Actual unique-parameter enumeration, exact expert-count sum | Router/dispatch work can differ by layer |
| More selected expert capacity | Same hidden width, expert width and top-2 | Active count does not equate measured compute |
| More or different exposure | Same deterministic stream and target-token count; hashes/cursors | Source overlap and recoverable document structure must be reported |
| Different inherited knowledge | Shared random initialization rule; shared tensors aligned; no pretrained weights | One seed does not average initialization sensitivity |
| Frequency trade-off | Overall and high-frequency NLL beside low-frequency NLL | No invented noninferiority margin |
| Routing mechanism | Observe loads, entropy and receipts | No causal mediation claim without later intervention |

## 5. Data Construction And Provenance

Prefer the existing trusted DCLM source and tokenizer after current asset lookup and strict access checks. Do not silently replace the distribution to enlarge the sample. Do not write to corpus/checkpoint source paths.

Before final testing, record in a frozen data manifest: required asset IDs, resolved locations, source file fingerprints, tokenizer fingerprints, training sequence construction and order, document-boundary availability, normalization, deduplication, train/dev/final split, counting scope, deterministic sampling seed and frequency thresholds. Count only the actual common exposure selected for this pair. Never call reference-corpus counts the model's actual historical pretraining frequency.

The bucket algorithm must be common to A/B and frozen from training counts before test losses are inspected. Report bucket cutoffs, training type counts, held-out target counts, coverage, zero-count types, and whether counts use input tokens, targets or both without double counting. Save manually inspected examples with original text, token IDs, counts, bucket and target labels. A test type absent from training belongs to “unseen,” not the low-frequency seen bucket.

Retain the trusted general validation view as an overall measure. Dev is for pipeline/capacity checks and common policy selection. Final test cannot select model, bucket or checkpoint. Recover and deduplicate document IDs/text if source metadata permits; otherwise explicitly identify the available sequence/source units and record that document deduplication and document-level independence are unverified. Do not label a block bootstrap as document bootstrap.

Entity/relation tasks are `NOT RUN` unless reliable training occurrence counts, aliases, template strata and fact/entity/relation/paraphrase splits can all be verified before final evaluation. Do not manufacture a fact score from token loss.

## 6. Learning Task And Permitted Supervision

Train a causal decoder to predict each next token from the permitted prefix. Targets come only from the frozen training corpus. Vocabulary interfaces are shared across arms. Valid targets obey the inherited masking/packing contract. Report the exact valid-target count; padded or ignored targets do not enlarge the comparison budget. There is no teacher supervision, SAE reconstruction loss or pretrained weight inheritance in this pair.

## 7. Model / Architecture And Frozen Variants

| Component | A uniform | B deep-increasing |
| --- | --- | --- |
| Layers (1-based) | 1–8 | 1–8 |
| Experts per layer | 8,8,8,8,8,8,8,8 | 6,6,6,8,8,10,10,10 |
| Stage depths | 3/2/3 | 3/2/3 |
| Residual hidden width | 1024 | 1024 |
| Expert intermediate width | 1536 | 1536 |
| Top-k | 2 | 2 |
| Query/KV heads; head dim | 16/8;128 | 16/8;128 |
| Shared experts | none | none |
| Embedding/head binding | tied | tied |
| Total experts | 64 | 64 |
| Bias-free expert parameters | 4,718,592 each | 4,718,592 each |
| Expert total | 301,989,888 | 301,989,888 |
| Router total | 65,536 | 65,536 |
| Unique total/trainable parameters | 507,988,992, to verify on adapted model | 507,988,992, to verify on adapted model |

All layers have more experts than top-k. Instantiate actual parameter tensors and verify formulas with forwards; record norms, buffers and tied-weight uniqueness separately. Every layer's table must include attention, expert, router and other parameters. Report both conventional active-parameter accounting and its exact embedding/head convention. Expert-forward matrix FLOPs are approximately twice selected matrix parameter count per token, with activation/route/attention terms separately stated; training FLOPs must disclose backward/recomputation assumptions. Measured profiler costs remain distinct from this estimate.

## 8. Training Objective And Optimization

Reuse the inspected ordinary-MoE training family rather than fabricate new precise settings. Verified historical policy is AdamW, peak learning rate 3e-4, betas (0.9,0.95), epsilon 1e-8, matrix weight decay 0.1 with norm/scalar exclusions, gradient clip 1, BF16 autocast and FP32 optimizer states. Historical schedule warms over 262,144,000 valid tokens, then stays constant. Historical effective batch is 262,144 target tokens/update at sequence length 2048 (four ranks; microbatch 16, accumulation 2). These are source values, not a claim that every value fits this bounded new pair.

Use a short common smoke to check memory, finite loss/gradients and throughput. If a historical value cannot be used, record tested candidates and failures and select one policy feasible for both. Freeze the final learning-rate schedule in token coordinates, optimizer details, batch/accumulation, precision, seeds, total tokens, checkpoints/evaluation times and all objective components before full training. Do not change one arm's budget or learning policy to force completion.

The source ordinary MoE has no router auxiliary loss, no capacity truncation and no token dropping; it uses a load-bias update of 0.001 times sign(expected assignments minus observed assignments). Preserve the source semantics unless the joint configuration explicitly records an authorized necessary adaptation. Record load-bias buffers in checkpoints. The same objective applies in both arms.

Apply the repository [training observability contract](../../../../../../../../UNAVAILABLE.md): global token-weighted LM loss, true objective, stable raw/weighted tags for actual enabled components, learning rate, optimizer step, valid-token totals and effective tokens/update. TensorBoard global steps use valid tokens for `tokens/*`; update views remain secondary. Failed/nonfinite updates are explicitly recorded and never silently count as completed tokens.

## 9. Conditions, Seeds, And Checkpoints

A/B start from the same initialization rule. Shared attention, embedding/norm structures and shared (layer,expert-ID) expert tensors have identical initial values. Router rows use a deterministic aligned rule where shapes differ. Additional experts use the same frozen distribution, without copying a trained expert. Save the mapping and initial shared-tensor equality audit. No existing checkpoint is modified.

At least one paired seed is required. A second paired seed is conditional on resources after full A/B completion and evaluation; absence is a limitation. Record actual seeds before training. Checkpoints include start, common midpoint and endpoint; the final common token budget and exact save positions are frozen after smoke. Endpoint is the primary comparison; no best-final-test selection. Save model, optimizer, scheduler, load bias, data cursor, RNG, token count and config identity. Qualify save/reload and external-process continuation at the smoke boundary.

## 10. Primary Metric And Frozen Analysis Plan

Estimand: `delta_low = token_mean_NLL(B, low_seen) - token_mean_NLL(A, low_seen)` at the frozen endpoint. Lower is better. Units: nat per eligible token. Primary sample is the frozen final test; frequency labels use training only. Use exactly the same target positions in A/B and preserve paired raw losses or sufficient grouped sums/counts. Report raw arm means, paired differences and coverage.

Use a two-sided 95% paired resampling interval. Verified document IDs are the preferred unit; otherwise freeze the actually available block/source unit and disclose residual dependence, with no document-level label. Report the selected unit, number of units, resampling seed/repetitions and weighting in the freeze. A single primary endpoint/frequency metric requires no selection from many favorable metrics; secondary breakdowns are exploratory unless separately frozen. Missing units and zero-count buckets remain explicit; never remove hard examples because of high loss. Sampling intervals do not quantify across-training-seed uncertainty.

## 11. Secondary Metrics And Guards

Report low/mid/high seen token groups, unseen tokens separately, and the complete general validation set's NLL/perplexity. Provide common-token learning curves from start/middle/end and state differences at comparable estimated FLOPs without pretending unequal endpoints are identical-compute training. If compute coordinates do not overlap, report no matched point.

For every layer record expert token receipts/assignment counts, mean routing entropy, dead experts under a stated zero-receipt window, drop count, load-bias statistics and route normalization. Per-step selected assignments must equal eligible tokens times top-k. Report theoretical and measured FLOPs, observed throughput, peak memory, dispatch time, data-parallel communication and wall-clock training/evaluation time. A DP-local expert implementation has no expert-parallel exchange; that does not mean zero communication. Profiler overhead must be separated from ordinary-step throughput.

## 12. Known Good / Known Bad / Known Confusing Cases

- Good: parameter enumeration matches the formula and tied-head identity; all selected assignments are retained; a saved/reloaded state reproduces evaluation.
- Bad: route counts miss top-k assignments, finite checks fail, shared initial tensors differ, exposure/order or token totals diverge, or checkpoint restoration omits load bias/RNG/cursor. Stop the dependent full stage and retain evidence.
- Confusing: train-unseen types, missing bucket coverage, a favorable type-average with unfavorable token-average, short-run noise, low-frequency gains alongside worse total NLL, or large dispatch differences despite equal active parameters. Preserve these distinctions.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Output / handoff | Failure and gate |
| --- | --- | --- | --- | --- |
| S0 source/access | Actual available model/data, user source | Inspect source and registry; preserve hashes | Source audit, current strict access record | Missing input blocks only dependent stage |
| S1 construction/accounting | A/B variants and training view | Enumerate parameters; align initialization; freeze split/frequency rules; inspect samples | Parameter tables, data manifest, initialization map | Capacity/exposure identity failure blocks full pair |
| S2 joint GPU smoke | Requested 4H100 reserved; both variants | Forward/backward, finite/load tests, performance, save/reload/resume and evaluation replay | Smoke receipt; jointly feasible policy and throughput | Retain failed candidates; no scientific claim from smoke |
| S3 joint freeze/full train | S1/S2 pass | Freeze common tokens/config/hashes; train both, permitted exact resume | Start/mid/final checkpoints and telemetry | NaN/resource interruption diagnosed; preserve incomplete state |
| S4 locked final eval | Fixed buckets, checkpoints, code | Evaluate paired held-out positions and general validation; compute registered interval and costs | Raw metrics, curves, routing/cost tables | Missing final data remains explicit; no re-bucketing |
| S5 record | Validated actual outputs | Assemble factual Summary/Detailed and readable Chinese report; register actual checkpoints | Reproducible artifact entry and Unknown human judgment | Saved-but-unregistered or missing output is reported |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation`. Code, configs, run logs, raw per-unit metrics and checkpoints stay there. Record source-file hashes/code manifest because the execution workspace is not automatically a Git repository. Use an isolated package; never patch frozen baseline outputs.

Resource selection is exactly the envelope's `h100-4-reserved` with its current default image/runtime and supported submission wrapper. The current request requires actual allocation/startup; a queued acceptance is not completion. Inspect existing job state before retry; never duplicate a live pair. Record job ID, resolved tuple, durable pod logs, observed GPU identity and actual progress. The platform runtime limit is checked live; do not treat an old per-job limit as account credit.

The final joint freeze must name input asset IDs, data/tokenizer manifests, code hashes, selected hyperparameters, actual initialization map, common total tokens, allowed checkpoint positions, frequency algorithm/cutoffs, final split/evaluation units, estimator code and runtime ceiling. This file and that immutable freeze together identify the executable round. Full training cannot precede it.

## 15. Success / Failure / Insufficient Evidence

- **Potential in the measured proxy:** negative primary difference and its paired interval below zero. Report high-frequency/overall cost separately. No practical noninferiority margin is invented.
- **Observed trade-off:** low-frequency improvement accompanies worse high-frequency or overall NLL; state both raw effects/intervals. Whether the cost is acceptable is the researcher's judgment.
- **No observed advantage:** the primary point estimate is nonnegative. If its interval crosses zero, preserve uncertainty rather than claim equality or universal failure.
- **Uncertain sign:** interval spans zero; report the point estimate and interval.
- **Insufficient intended comparison:** incomplete arm/budget, failed parameter/exposure guards, missing eligible bucket, or unverified decisive data lineage. A smaller or proxy result may be reported only with the narrower eligibility label.

## 16. What This Cannot Claim

No semantic long-tail representation, entity/relation learning, gradient signal-to-noise improvement, causal effect of route loads, expert-memory localization, universal architecture superiority or invalidity, or success of the width-varying sketch is established by this round. Even a complete engineering run does not confirm scientific acceptance, question closure or a next experiment.


### Exact registered pre-run data and execution policy

These are verified engineering choices within the user's delegated scope, recorded before formal A/B training. The final joint freeze supplies the actual smoke-derived even step count and frequency cutoffs without changing this rule.

- Source: first 67,108,864 token IDs of the existing DCLM pair view's first source file, not the whole DCLM corpus. Token 151645 (`<|im_end|>`) delimits recovered documents. Discard leading/trailing fragments and short fragments (8,827 tokens); globally remove 16 duplicate documents by exact uint32-byte SHA-256. Near duplicates are `NOT_CHECKED`.
- Split: first 64 bits of exact document SHA-256 modulo100; dev=0, test=1, train=2..99. Training has 53,813 documents/65,766,910 tokens; dev 528/630,980; final test 544/700,308. Evaluation predicts all but the first global token, hence dev 630,979 and test 700,307 target positions. Complete dev/test overall loss is the general validation measure. The original 115M holdout is **NOT EVALUATED** this round.
- Training stream: cyclic packed causal stream with the reused context semantics. At each update all four ranks jointly consume 262,144 targets. The exact supervised positions are 1..T in that cyclic stream; count type occurrences by exact bincount over those positions. No full-corpus or historical-exposure claim is made.
- Buckets: sort positive target-exposure counts across token types; for n positive types, take integer order statistics q1 at index floor((n−1)/3) and q2 at floor(2(n−1)/3), using zero-based indexes. Low is 0<count≤q1, mid q1<count≤q2, high count>q2; zero is unseen. Keep ties together. Exact integer cutoffs/type counts/test coverage freeze after the common budget is known and before final losses are read.
- Initialization: seed20261106; SHA-256 of semantic tensor names produces deterministic random seeds, with all expert matrices drawn from normal(0,0.02). The CPU audit verifies 242 shared same-shape tensors and 42 shared rows across six differently shaped routers exactly equal. Both start fresh; no checkpoint transplantation.
- Joint smoke: four updates per candidate; initial candidate seq2048, micro16, accumulation2, world4. If memory requires smaller microbatch, adjust both arms' accumulation to preserve 262,144 targets/update. No test metric selects the candidate. Preserve failed candidates.
- Full optimizer: AdamW, lr3e-4, beta(.9,.95), eps1e-8, matrix weight decay.1/norm0, clip1, BF16, fused optimizer; no router auxiliary objective/drop, load-bias update.001. Warmup explicitly adapts the historical policy: W=min(1000,max(1,floor(.1S))) updates for S common updates, then constant lr. The inherited initial scheduler uses lr0 for the first update; preserve and disclose it in both arms.
- Budget selection: measure A and B non-first-step median seconds sA/sB in successful dual smoke. Freeze S=max(20,min(4000,2 floor(3600/(sA+sB)/2))). This uses a one-hour combined-training target plus a separate one-hour evaluation/I/O reserve; it is an observed-throughput budget rule, not a wall-clock guarantee. Both arms receive exactly T=262,144S valid targets. Never shrink one arm after final-test model metrics/evaluation.
- Checkpoints and evaluation: full state at steps0,S/2,S, with full dev and final-test evaluations under already frozen rules. Primary comparison is the endpoint; intermediate test observations cannot change training/buckets or select checkpoints. No C or second seed is scheduled; prioritize one complete pair.
- Paired intervals: 2,000 document resamples, percentile2.5/97.5, RNGseed20261106; draw the same recovered document IDs in both arms and divide summed paired losses by summed eligible target counts. Packed evaluation may carry context across document boundaries, so document grouping does not eliminate all cross-document dependence. Single-seed uncertainty remains unmeasured.

Data provenance is the execution-side `data/manifest.json`; its copied small metadata is [data_manifest.json](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/data_manifest.json). Training/dev/test payload SHA-256 values are respectively `2d9f44eea9e42fa120af1fc505b00917cec1bcf3811d4c649b0733ee27a6addb`, `6fd8b999ea4572e15c00a906f6f13f6098b40a3876aba02a79de64014570f582`, and `a07cf3d28a26022bfff20fce279aad09de8994adba78ed4467776ba525d3511e`. Data-derived thresholds and actual training status are not invented here. Smoke frequency files stay under `data/frequency_smoke/`; formal frequency files stay under `data/frequency_formal/`, without overwriting smoke. The freeze receipt explicitly records `final_test_model_evaluation_before_freeze=False` and `test_metadata_and_examples_inspected=True`. Source examples and test metadata were inspected as requested; no final-test model metric selects the design.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Item | State and authority |
| --- | --- |
| Human question, hypotheses and fairness | Confirmed in current user request |
| Implementation, smoke and complete A/B execution scope | Explicitly authorized in current user request |
| Exact source architecture | Inspected source; adapted-model recount pending |
| Data split/counting/buckets and exact common policy | To be recorded before full training in joint freeze after source/dual-model checks |
| Scientific acceptance/mechanism judgment | Unknown; belongs to researcher |
| Commit/push/publication, next architecture/causal run | Not included in this authorization |

Scientific plan freeze: 2026-11-06, immediately before embedded-smoke job submission. The full-file SHA-256 is recorded externally in the submission/freeze provenance to avoid a self-referential hash.

No new human-confirmation turn is inserted for engineering choices already delegated by the user. The full-stage approval is activated only for the jointly frozen configuration that passes the stated guards. Record actual freeze time/hash before execution. After first approved execution, preserve the scientific body. Any material change is an append-only amendment stating old/new value, reason, already-seen data, affected arms/blocks, authority and evidence-eligibility impact. Record failed attempts and exact resumes without erasing them.
