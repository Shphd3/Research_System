# Protocol: Bounded analysis and learning test of mixed-frequency representations and high-frequency-path invocation

## 0. Approval Snapshot

Status: `APPROVED_FOR_BOUNDED_ANALYSIS_AND_CONDITIONAL_LEARNING`. The user explicitly requested autonomous modeling, hypothesis validation after analysis, and submission of four H100 Reserved GPUs without stepwise reviews. This authorization does not assert that H-L is true. The question is whether the increment from retaining a high-frequency path under matched top-2 depends on frequency-organized membership. This does not test a pure compute advantage of previous top-1 versus top-2 models. The owning Anchor is `frequency_composition_common_path/anchor_cn.md`; Focus remains unchanged. The experiment combines a root-cause audit and a finite comparison guided by a model. AI operationalized and audited blocks A–G within this explicit delegation; scientific conclusions remain for researcher discussion.

## 1. Terminology / Definitions

Feature frequency \(p_i\) is the proportion of valid TRAIN answer-prediction positions with \(z_i>0\). It is not activation amplitude, final-layer \(z\times\text{decoder norm}\), token frequency, or semantic difficulty. B1–B4 are the original four positive-frequency bands with equal widths in log frequency; U is separate. A group pair consists of two candidate experts for one frequency band; the same pair indices in R designate random groups. A high-frequency path is not a validated common-function module. Top-2 selects two distinct experts with weights fixed at \(1/2\). Target reception and \(q\) use all original activations. Total expert load sums to two, not one.

## 2. Anchor Alignment

First characterize mixed token/feature structure and score proxies, then separate frequency-specific invocation from the strategy effect of a generic fixed path. The Anchor owns the mathematical relations, hypotheses, and boundaries. Reports must not substitute lists of spectra and loads for this inference. Classify each of 18 advisor intuitions as measurable, locally testable, or untested, without converting ambiguous transcription into fact.

## 3. Tested Hypothesis

H-T: current-token identity does not explain all feature activation and frequency composition. H-G: carrying variation in actual centered-hidden-state PCA is different from mean composition or amplitude. H-L: \(\Delta_T<0\) and \(I<0\). The primary learning metric is DEV per-feature macro NLL over the common T-B1 set. Support requires actual improvement, not merely less deterioration. Disclose paired dialogue intervals and both seeds completely.

## 4. Rival Explanations

Live rivals include current/target token identity, format/source, limited support, a generic shared path or load change, group size and update counts, and nonorthogonality or mismatch of the frozen measurement tool. T splits each band by a fixed hash and does not use the previous \(\phi\) groups, avoiding the claim that relation-based subdivision validates frequency utility. R matches all eight group sizes without matching within-group frequencies. The complete hidden-state input and Base are identical in all four conditions.

## 5. Data Construction And Provenance

Reuse `sft_route_learning/20261019T012300Z`: TRAIN has 85,548 positions from 1,024 dialogues; EVAL has 22,446 from 256; DEV has 10,340 from 128. TRAIN and EVAL have already been used. Inspection of named previous training/analysis entrypoints found no DEV comparison use, but DEV representations and previous routes already exist. Call it a new fixed review panel for this round, not independent new material. Check exact prompt and assistant hashes across splits; near-duplicate independence is unverified. Targets are shifted once: position \(t\) predicts \(t+1\), so the first answer is predicted at the final prompt position. Include EOS targets. Padding does not enter the cache.

## 6. Learning Task And Permitted Supervision

Train only NTP/SFT cross-entropy against original answer targets, averaged uniformly over all valid answer positions. Future token values enter outcome analysis or supervision only, never the router. Freeze the Base, output head, and CrossCoder; every expert receives the full hidden state. Low B1 and high B4 evaluation sets are common definitions from T's original bands; do not change evaluation targets for R. Report per-feature support and overlap; unavailable quantities remain NA.

## 7. Model / Architecture And Frozen Variants

Use shared codes from 14 layers, raw final-layer decoder norms, and existing block-28 hidden states before final normalization. New T membership sorts each original band by `SHA256(seed:fid)` and splits it into two groups. R sorts all 15,477 positive-frequency features by a hash with an independent seed and assigns them according to the exact eight T group sizes. B1 retains its original frequency definition. The 907 zero-hit features participate only in composition diagnostics. Estimate TRAIN means once and freeze them.

F chooses the two highest calibrated group-pair scores. H selects group pair 4 and the highest of the other three. Within a pair, select the subgroup with greatest raw amplitude. Resolve ties by minimum ID. Record zero-mass and fallback cases separately; do not remove inputs. Every position uses two distinct expert IDs.

Use eight bias-free, ordinary SwiGLU FFNs of dimensions \(1024\times1024\times1024\), totaling 25,165,824 trainable parameters. Activating two experts costs \(6\times1024^2\) matrix multiply–accumulates per position. Add `scale × mean(two FFN outputs)` to the original hidden state. Here

\[
\mathrm{scale}=\sqrt{\mathbb{E}_{\mathrm{TRAIN}}\lVert h\rVert^2/1024}.
\]

Do not subtract a mean. Initialization is paired within each seed: random CPU-initialized input projections and zero down projections. Retain the original Base path.

## 8. Training Objective And Optimization

Use answer-only cross-entropy, without load balancing or auxiliary spectral loss. AdamW: learning rate \(3\times10^{-4}\), betas \((0.9,0.95)\), epsilon \(10^{-8}\), weight decay 0.01, and gradient clipping at 1. Train one epoch, 168 updates, effective batch 512 and microbatch 128. Warm up for nine updates and decay by cosine to 0.1 times the peak learning rate. Each condition sees the same 85,548 targets in the same PCG64 order for its paired seed. Normalize accumulated gradients by the actual number of valid positions in the effective batch, not separately within each expert. Pair initialization, order, and budget. TensorBoard follows the repository observability contract.

## 9. Conditions, Seeds, And Checkpoints

Train T_F, T_H, R_F, and R_H with seeds 11 and 22: eight models. Record complete TRAIN and previously exposed EVAL curves at updates 0, 42, 84, 126, and 168. Reveal DEV only once at the endpoint after every model completes; do not tune hyperparameters or select an epoch with DEV. Save two shared initializations, model weights at 42/84/126, and full resumable model/optimizer/RNG/cursor/valid-target state at 168. Preserve older models. All endpoint comparisons use the same update count; do not assemble each condition's best checkpoint.

## 10. Primary Metric And Frozen Analysis Plan

For each B1 feature, average DEV NLL over positions where it activates, then average equally over estimable features. This is \(L\). Report both individual seeds and their mean. Define

\[
\Delta_T=L(T_H)-L(T_F),\qquad
\Delta_R=L(R_H)-L(R_F),\qquad
I=\Delta_T-\Delta_R.
\]

Primary support requires negative \(\Delta_T\) and \(I\), with both primary 1,000-replicate dialogue-bootstrap intervals excluding zero. Otherwise report descriptive improvement, non-support, or insufficient evidence rather than a stable mechanism. The preregistered practical marker is 0.01 nats; a statistically negative quantity is not automatically useful. Disclose the direction of both seeds, their mean, and all intervals. Do not claim population significance or generality across models. Deliver overall, low-position-union, and high macro/union metrics and all source NLL arrays. Resample whole dialogues jointly to preserve pairing. An unobserved feature is NA; an active feature never received by its designated expert has reception zero.

## 11. Secondary Metrics And Guards

Static analyses cover current-token and target-token top-ID purity, recall, and support for all features. Use current-ID conditional means to predict B1 contribution share in EVAL/DEV and report MAE/R², also after removing first-answer prediction positions. Preselect four features per band using TRAIN only: at least five hits and three dialogues, then the smallest fixed hashes. Inspect two random positive examples, one high-activation example, and one same-ID inactive example. Report computable proxies without assigning semantic names.

Compute PCA of actual TRAIN hidden states for \(k=1,16\). Report signed band-vector \(\beta\), decoder \(\eta\), offsets/residuals, and cross terms together, with random orthogonal directions as reference. PCA of activations is not a parameter-weight spectrum and cannot establish optimization dominance.

Routing outputs include all exposure \(q\), reception, loads and occupied slots, actual update counts and gradient steps, F/H route agreement, forced paths lacking own-group activation, multiple owners on the same input, and decomposition of previous top-1 failures. A post-hoc macro-reception oracle is only an upper bound, not a deployable metric. Evaluate every condition against complete original activations and contributions.

## 12. Known Good / Known Bad / Known Confusing Cases

A known-good case has one known active feature and independently recomputable scores and two experts. Reject wrong label shifts, invalid denominators, duplicate experts, and dropped tokens. A confusing case is invoking a forced path with zero own-group mass: this is the intervention, not evidence of content matching. Top-2 exposure and load sum to two, so top-1 sum-to-one identities cannot be reused unchanged. At initialization the down projection is zero but input projections are not. Input-projection gradients can initially be zero, while down-projection gradients must be present; verify gradients through all projections after an update.

## 13. Scientific Procedure And Stage Contracts

S1: Read both reports completely and classify all 18 intuitions. Check assets, positions, and actual source code read-only.

S2: Freeze TRAIN statistics, PCA, membership, and code, then apply the same computations to EVAL/DEV.

S3: Check that F/H actually differ, top-2 is matched, and future information does not leak into routing. Report representation results first.

S4: Run the qualified GPU smoke, then the registered one-epoch training of all eight models. Smoke uses only a small TRAIN subset; never tune the design on DEV.

S5: Reveal final DEV results together, report paired findings and negative outcomes, and restrict the next decision.

The learning gate does not require static H results to look better. It requires an actual strategy difference, identical underlying information and positions, and a learning uncertainty worth testing. If policies are identical, reuse the same results rather than create duplicate computation.

## 14. Algorithm, Output, And Provenance Contract

`config/frozen.json` fixes fields, seeds, paths, and resources. Code, caches, logs, and weights remain execution-side; Anchor and Protocol remain project-side. Local analysis uses at most eight CPU threads in aggregate and 16 GiB RSS. Training uses one node with four H100 Reserved GPUs and existing image `shphd-lite-0911`: eight CPU threads in aggregate, 64 GiB aggregate RSS, and 16 GiB allocated per GPU. New disk is limited to 24 GiB; active remote training to 35 minutes; total active wall time to 120 minutes. Account for external queue time separately. No Spot substitution, Base/CrossCoder training, continuation beyond budget, or automatic commit/push. A failed branch does not block independent deliverables.

## 15. Success / Failure / Insufficient Evidence

Engineering PASS is not scientific support. Apply the primary rule and boundaries in Section 10 and deliver complete negative evidence. If there is no learning benefit, revise the shared-high-frequency-invocation hypothesis rather than retuning frequency bands. If all conditions deteriorate abnormally even on TRAIN, use the same bounded TRAIN-smoke diagnostic at learning rates \(3\times10^{-4}\) and \(10^{-4}\), choosing a finite, decreasing setting by the same rule for all conditions. A change to the formal learning rate requires an append-only amendment before use, applied uniformly without inspecting DEV. Declining training loss with rising validation loss indicates overfitting; it must not automatically be attributed to an implementation error.

## 16. What This Cannot Claim

This cannot establish mastery of rare knowledge, semantic difficulty, increased capacity from pretraining, naturally orthogonal features, equivalence of common information with high frequency or the first principal direction, causal origin in attention, utility of \(\phi\), equal-compute superiority of top-2 over top-1, or common-semantics mediation. Previous top-1 outcomes are not a causal control for new top-2 training.

## 17. Block Confirmation, Freeze, And Amendment Ledger

The user explicitly delegated autonomous modeling and bounded execution. This document and configuration fix A/question, B/data, C/supervision, D/model, E/optimization, F/controls, and G/resources. Execute only after self-audit PASS. This does not rewrite an AI mechanism proposal as a human scientific confirmation. Before execution, register the new design's removal of previous relation-based groups and its even subdivision within frequency bands to avoid singleton or unstable-relation confounds. It is not the same model as previous T_S1. After execution begins, append amendments and result links only; do not change primary definitions in response to results.
