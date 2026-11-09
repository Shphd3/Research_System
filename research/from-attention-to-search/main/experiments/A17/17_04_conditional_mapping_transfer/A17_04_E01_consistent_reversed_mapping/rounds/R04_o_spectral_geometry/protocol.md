# Protocol: A17_04_E01 R04 O-matrix spectral supplement

## 0. Scope and authorization

Revision: `a17_04_e01_r04_o_spectral_geometry_v1`. The researcher explicitly authorized this existing-checkpoint supplement in the current conversation, after accepting the distinction between geometry and functional compatibility. Write this Protocol before measurement. This is a supplementary round of E01, not a new Focus, training run, or mechanism approval. Question closure and researcher mechanism acceptance remain `Unknown`.

Owners: [Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md), [Focus](../../../../../../focus/focus_conditional_mapping_transfer.md), [R02](../R02_single_layer_adamw/summary.md), [R03](../R03_mechanism_audit/summary.md). No new training, model forward, TEST access, SAE, parameter intervention, or publication is part of this supplement.

## 1. Purpose, hypothesis and strongest rival

Parent purpose: determine when different conditional prediction requirements can use shared parameters and when conditional separation is useful. This round tests a descriptive candidate: do O-matrix changes distinguish an endpoint that forgets the old mapping from an endpoint that retains both mappings?

Candidate H: B and C may have different leading O-displacement spectra or input/output subspaces, accompanying their different old-rule performance. This is a geometric association hypothesis, not a claim that those subspaces caused forgetting. A is a reference branch; its new labels differ from B/C, so A need not be closest to C.

Strongest rival: B/C differ in old supervision, new exposure, and optimization history; Q/K/V also change. O geometry may describe the trained endpoint without explaining its function. Full weights may appear similar because they inherit W0. Singular subspaces ignore coefficient signs: M and -M have identical spectra/subspaces but can have opposite prediction effects. Close singular values at the cutoff can make rank16 unstable.

## 2. Objects, data and provenance

Use Qwen3-0.6B Base R02 checkpoints, with only layer27 Q/K/V/O trained. Extract exactly `model.layers.27.self_attn.o_proj.weight`, shape1024×2048. W0 is the common E03 acquired-old AdamW1200 O, not the pretrained O. For continuation orders29/43/71, read A=`consistent`, B=`reversed`, C=`joint_reversed` at fixed steps240 and1200. Primary endpoint is1200;240 is a predefined earlier reference. These are three continuations of one old trained state, not three independent acquisitions.

Old mode1:甲first/乙last. New mode2: A uses the same mapping; B/C use甲last/乙first. C still starts from W0 and then mixes old and reversed-new supervision; it is not joint training from Base. At1200, A/B have24000 new answer exposures, C has12000 old+12000 new. At240 these counts are4800 versus2400+2400. Equal steps match total answer count, not new-task exposure or old supervision.

Read existing native DEV records only. Each mode has400 `order_new` and400 `combination_new` answers, including both commands. `order_new` has an unfamiliar order of a familiar unordered triple; `combination_new` has an unfamiliar unordered triple. Recompute CE, full-vocabulary accuracy and correct-versus-opposite-endpoint logit margin from cached per-record data; report each panel and their equal-weight combination. No regenerated forward, new examples, adaptive endpoint, or TEST confirmation. A new-task margin uses A labels; B/C use their reversed labels.

Required inputs: `adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main`; all nine `adapter_a17_04_transfer_20261011t160256z_full_seed_{29,43,71}_{consistent,reversed,joint_reversed}`; `analysis_a17_04_transfer_20261011t160256z_full_mapping`. Parent identities are `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, `data_a17_conditional_mapping_v1`. [Fresh selected strict access](../../../../../../../../../assets/checks/2026-10-12_a17_r04_spectral_inputs.json) precedes tensor loading. Freeze exact checkpoint member hashes, cached-readout hashes, source config, actual analysis code, and this Protocol. Verify all four step0 matrices equal the acquired-old checkpoint.

## 3. Mathematics and fixed measurements

For branch X, seed s and step t, define W_X,s,t as its saved O matrix and D_X,s,t=W_X,s,t-W0. Convert each saved FP32 operand to FP64 before subtraction. For M in {W,D}, use a deterministic CPU thin SVD:

\[
M=U\,\operatorname{diag}(\sigma_1,\ldots,\sigma_{1024})V^\top,
\qquad \sigma_1\geq\cdots\geq\sigma_{1024}\geq0.
\]

Report raw singular values, normalized squared spectrum, Frobenius norm, D/W0 norm ratio, and first16 squared energy:

\[
E_{16}(M)=\frac{\sum_{i=1}^{16}\sigma_i^2}{\sum_{i=1}^{1024}\sigma_i^2}.
\]

The left basis U16 is in O-output coordinates (1024); right basis V16 is in O-input coordinates (2048). Compare same-seed A/B, A/C and especially B/C:

\[
\rho_U(X,Y;k)=\frac{\|U_{X,k}^\top U_{Y,k}\|_F^2}{k},\qquad
\rho_V(X,Y;k)=\frac{\|V_{X,k}^\top V_{Y,k}\|_F^2}{k}.
\]

Each is the mean squared cosine of the principal angles, between0 and1. These are matrix input/output subspaces, not parameter-vector directions, activation covariance directions, old-task-sensitive gradients or identified functional experts. Rank16 is primary; fixed ranks8/32 are sensitivity checks. Report boundary gap `(sigma_k-sigma_(k+1))/sigma_k`; no outcome-selected rank. Also compare full W against W0 and same-branch cross-seed variation. Save signed Frobenius cosine between displacements, `<D_X,D_Y>/(||D_X||F||D_Y||F)`, because subspace overlap alone loses sign/orientation information. Undefined zero-matrix quantities stay undefined.

## 4. Numerical checks, aggregation and outcome branches

Before real measurements, test known singular values/energy, basis rotations, sign reversal, zero matrices and a tied cutoff. Full SVD reconstruction and U/V orthogonality errors must be below1e-10; singular-energy/norm agreement relative error below1e-10. Verify finite matrices and readouts, correct shape, parent hashes, member seed/branch/step, complete800-record panels per mode, and margin/CE aggregation. Freshly verify source digests after execution. Failures block affected measurements, never get averaged into eligible results.

Report individual continuation orders, their equal-weight means and ranges. Within each mode, both panels and commands have equal record weights. These three conditional orders do not support population-wide p-values. Do not treat the rank cutoff as16 uniquely meaningful mechanisms.

Registered branches: (1) stable D_B/C differences with same-branch variation smaller: descriptive endpoint separation, causal interpretation remains open; (2) similar coarse geometry despite strongly different prediction behavior: weaken the claim that these coarse statistics suffice to describe compatibility; (3) rank/seed instability or mixed spectrum/subspace patterns: no single geometric explanation; (4) failed identity/numerical guards or missing inputs: insufficient for the affected comparison. No geometric pattern establishes distinct attraction basins, separate-expert utility, or a causal parameter module.

## 5. Execution and outputs

Execution root: `/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry`. Reuse R02 state/readout keys after inspecting actual sources; adapt them into a CPU-only reader. No model or optimizer instantiation. Use FP64, eight CPU threads,37 thin SVDs (common W0 plus full/displacement for18 endpoints). The first actual matrix is the startup/throughput check after toy tests; no remote training Smoke is applicable. A30-minute bounded execution budget triggers preserved failure/diagnosis, not an automatic training submission.

Unique run directory; frozen code/config/inputs/Protocol; durable progress log and completion certificate. Save spectra, metric/pair tables, top32 U/V bases, cache-derived behavior, provenance and clearly labeled static figures execution-side. Register actual reusable bases/analysis outputs and a fresh selected output-access check. No newly trained checkpoint exists. Training tokens, optimizer telemetry and resume tests are not applicable to this zero-update analysis.

Canonical bilingual Summary/Detailed and artifact manifest belong in this round. Add a separate dated knowledge-update reading entry linked to the canonical result; retain frozen R02/R03 evidence unchanged. Results may narrow the geometric interpretation but cannot silently change scientific state. No commit or push is requested.

## 6. Completion and reasoning audit

A: bounded geometric supplement to the shared-learning question. B: common old start and fixed checkpoints; supervision/exposure differ explicitly. C: registered exact weights and existing exposed DEV. D: exact SVD and cached predictions, no geometry-to-function identity assumed. E: sign, cutoff, scale, input changes and training history remain rivals. F: hashes, toy/numerical guards and independent result checks. G: self-contained results distinguish observation from AI interpretation; human mechanism judgment remains `Unknown`.

Pre-execution result: `NOT RUN`. Completion requires all37 decompositions or explicit failed cells, B/C and A-reference tables, behavior linkage, fixed-rank sensitivity, actual asset registration and bounded knowledge update. A result that contradicts the candidate geometric story is a completed outcome.
