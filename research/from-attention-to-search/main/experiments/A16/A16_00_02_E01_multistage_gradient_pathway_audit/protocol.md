---
experiment_id: A16_00_02_E01_multistage_gradient_pathway_audit
anchor_id: A16_00_02_multistage_gradient_pathway
status: approved_for_implementation_smoke_and_full_audit
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: centered_mediation_of_lb_shadow_step_nll
---

# Protocol: Multistage Load-Control Gradient-Pathway Audit

## 0. Approval Snapshot

**Decision question.** At matched early, middle, and late states, does running-centering reduce the immediate language-learning cost of the Switch load-balance (LB) gradient, and is that reduction accompanied by less conflict in the Router-source, Gate, and routed expert-update pathways?

**Treatment and control.** Centered-Full is the treatment; Vanilla-Full is the control. Seeds 17 and 29 and checkpoints 50M, 6B, and 10B nominal tokens are paired. Architecture, checkpoint state, data, tokenizer, objective coefficient \(\lambda_{LB}=0.01\), and evaluation documents are held fixed within each comparison.

**Primary metric.** From one complete checkpoint state, apply an LM-only AdamW shadow step and an LM+LB AdamW shadow step. Their paired WoS validation NLL difference is \(\Delta NLL_{LB}\) in nat/token. The treatment effect is \(M=\Delta NLL^{Vanilla}_{LB}-\Delta NLL^{Centered}_{LB}\); positive values mean centering reduces the immediate LB cost.

**Verdicts.** Outcome Pass requires both seeds to have positive direction at at least two of three stages and a positive paired-document bootstrap lower bound for the frozen three-stage median. Shared-path and expert-update mechanisms receive separate verdicts. Any missing optimizer shard, unpaired batch, inexact branch state, nonzero same-layer direct expert derivative from that layer's own LB term, or incomplete cell is Insufficient.

**Approved scope.** Protocol, implementation, single-GPU synthetic tests, one 8x5090 smoke, and the four full audit jobs (two arms by two seeds, each reading three checkpoints) are approved. This is a read-only checkpoint audit; it does not continue training.

**Cannot claim.** The experiment cannot prove that one-step effects explain the 30B trajectory, that lower expert conflict creates useful specialization, or that dynamic expert bias is superior.

## A. Anchor Alignment — CONFIRMED

The Protocol implements [A16_00_02](../../../problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_02_multistage_gradient_pathway_anchor.md) without changing its hypothesis, primary outcome, or boundary. The strongest rivals are useful regularization and hard/soft load-control mismatch.

## B. Data And Stage Contract — CONFIRMED

### B1. Checkpoints

For each of `vanilla-full` and `centered-full`, seeds 17 and 29:

| Stage | Step | Nominal tokens | Selection rule |
| --- | ---: | ---: | --- |
| early | 64 | 50,331,648 | first registered nonzero checkpoint |
| middle | 7,629 | 5,999,951,872 | first registered checkpoint at or above half of 10B |
| late | 12,716 | 10,000,269,312 | registered endpoint |

Every cell must contain one `mp_rank_00_model_states.pt` and eight optimizer-state shards. The audit records file size and SHA-256 before execution.

### B2. DCLM optimizer batch

The shared-path gradients and AdamW shadow update replay the exact next global DCLM batch encoded by the checkpoint's sampler/data-cursor state from:

`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`

The expected global batch is 768 sequences of length 1,024. Both shadow branches must record the same per-rank and global token SHA-256. No data cursor is advanced in the source run.

### B3. Web of Science documents

Source directory:

`/data/share/109_cache_dir/hf_data/datasets/river-martin___web-of-science-with-label-texts/default/0.0.0/1a243df40ebf701e0d6a8c402ad9ae05f7ee5002/`

Frozen source hashes:

| Split | Rows | SHA-256 | Use |
| --- | ---: | --- | --- |
| train | 32,890 | `213765a7be46524fddcc14b9fa0bc6a8c3ac094730b85d7e6c79117792358aed` | expert-gradient groups |
| validate | 7,048 | `d19cff6a15d295c6a5da2dd390934892b373aa8f2f037bc743cd91e4593f198e` | shadow-step NLL |
| test | 7,047 | `25fc1fc037077315c97552054daad8c4b4d5076ded0d7bfd02a9959eb397f979` | untouched |

The manifest is selected before gradients by SHA-256 ordering within each of the seven `domain` labels. Expert conflict uses 32 train documents per domain, split into two fixed 16-document shards (14 groups total). Shadow NLL uses 16 validation documents per domain (112 documents). Each abstract is tokenized independently, truncated to 512 tokens, right padded, and padding labels are masked. Documents are never concatenated across boundaries.

## C. Model And Objective Contract — CONFIRMED

The model is the completed four-layer, hidden-size-768, eight-sparse-expert plus one shared-expert, top-1 DCLM MoE. Vanilla uses \(z=Wg\); Centered uses \(z=W(g-m)\) with the checkpointed running mean. Experts receive full local representations in both conditions.

For each DCLM optimizer batch, reconstruct:

- LM loss alone;
- unscaled Switch LB loss alone;
- coefficient-scaled LB loss with \(\lambda_{LB}=0.01\);
- LM+LB total exactly as trained.

The LM loss is next-token cross entropy. The LB loss must match the training implementation and be reconstructed from the native `aux_loss` object; no substitute balance proxy is allowed.

## D. Gradient And Shadow-Step Contract — CONFIRMED

### D1. Router-upstream representation

At every layer capture the pre-center Router source \(g_\ell\) and retain its gradient under LM-only and LB-only backward passes. Report cosine, norms, negative cosine mass, and layer aggregation. This tensor is the upstream representation immediately consumed by the Router transform; it is not an upstream parameter proxy.

### D2. Router update

For every layer record the full Gate-weight LM and coefficient-scaled LB gradients, their cosine and norms, and the corresponding AdamW applied-update alignment. Bias-like load telemetry is excluded from the parameter cosine.

### D3. Expert update

For each WoS document group, compute the LM gradient over all sparse-expert parameters by layer and expert. Compare group pairs only when both contribute at least 256 routed non-padding tokens to that expert. The primary expert mechanism metric is routed-token-weighted negative cosine mass. Also report within-domain versus cross-domain pairs and the number of eligible cells.

Additionally record LM-versus-total-LB gradient cosine and norm for each sparse expert. The own-layer LB term has no direct derivative through the experts selected by that same layer, so this same-layer direct derivative must be at most \(10^{-10}\) relative to Gate LB-gradient norm. Total LB is allowed to reach earlier-layer experts through later Router-source representations; that cross-layer upstream gradient is a registered mechanism measurement rather than an implementation failure.

### D4. Exact shadow branches

For every cell initialize two independent DeepSpeed engines from the same complete checkpoint and verify model, optimizer, scheduler, RNG, Router buffers, and batch hashes. One branch applies LM-only; the other applies LM+LB. Evaluate both on the same 112 WoS validation documents and the same hard-load guard tokens. Neither branch is saved as a continuation checkpoint.

## E. Comparison And Analysis — CONFIRMED

For each seed and stage compute:

\[
M_{s,t}=\Delta NLL^{Vanilla}_{LB,s,t}-\Delta NLL^{Centered}_{LB,s,t}.
\]

The seed summary is the median of the three stage effects. A paired bootstrap resamples the 112 WoS validation documents, recomputes each stage mean, then the frozen stage median; 2,000 draws produce a 95% interval. Stages and seeds are always shown separately.

Typed verdicts:

1. **Outcome Pass:** each seed has \(M_{s,t}>0\) in at least two stages and its median bootstrap 95% lower bound exceeds zero.
2. **Shared-path mechanism Pass:** for each seed, Centered has higher Router-source and Gate LM/LB cosine in at least two stages; layerwise values remain visible.
3. **Expert-conflict mechanism Pass:** for each seed, Centered has lower expert negative cosine mass in at least two stages with eligible cells in all four layers.
4. **Combined H1 support:** all three typed verdicts pass and the LB branch reduces hard concentration in the cell where a positive NLL cost is attributed to balance.
5. **Fail:** outcome rule fails with complete valid evidence. Mechanism verdicts may separately pass or fail.
6. **Insufficient:** any hard validity guard fails or one of twelve cells is missing.

No practical-effect threshold is added. A negative cosine without positive NLL cost supports the regularization rival. Positive NLL cost without hard-load improvement supports ineffective interference.

## F. Preflight, Smoke, And Failure Rules — CONFIRMED

Preflight must verify all 12 checkpoint cells, model/optimizer shards, model configuration, seed/step metadata, DCLM source, WoS hashes/schema, tokenizer, and free output space.

Unit tests cover cosine aggregation, zero-norm behavior, expert pair eligibility, document manifest determinism, paired bootstrap, and typed verdicts. The 8x5090 smoke uses one early checkpoint, one optimizer microbatch, two documents per WoS domain, exact double load, and one real shadow update. It must verify state and batch identity, native loss reconstruction, all three gradient captures, zero same-layer direct expert derivative, registered cross-layer upstream expert gradients, and output reconstruction.

NaN/Inf, OOM, communication failure, checkpoint mismatch, incomplete global gradient, branch-state mismatch, data/hash mismatch, or missing outputs stops the affected job. Scientific outcomes such as negative cosines, poor load, or worse NLL do not stop it.

## G. Execution And Artifact Contract — CONFIRMED

Resource profile is one ACP node with eight RTX 5090 GPUs (`5090-8-spot`), eight distributed processes, workspace `share-space`, cluster `computing-cluster-5090-01g`, worker spec `n12lp.nn.i10a.8`, and `SPOT` quota. Four jobs are named:

- `a16-gradpath-vanilla-s17`
- `a16-gradpath-vanilla-s29`
- `a16-gradpath-centered-s17`
- `a16-gradpath-centered-s29`

Raw artifacts live under `/data/250010109/MoE_Router/outputs/a16_multistage_gradient_pathway/`. Required outputs are the frozen data/checkpoint manifest, per-cell JSON, per-document shadow NLL arrays, gradient summary tables, expert-pair tables, job ledger, logs, and exact source manifest. Curated tables and figures are copied to this experiment folder only after evidence audit.

Cross-block consistency: `PASS`. Scientific body and verdict rules are frozen at first smoke execution. Any later change requires an append-only amendment with eligibility impact.

## H. Amendment 1 — Cross-layer Expert Gradient Path (2026-08-09)

**Trigger.** The first real checkpoint smoke showed a nonzero total-LB gradient on early-layer sparse experts. Code inspection and layerwise differentiation established that later-layer LB terms depend on representations produced by earlier experts. The old statement that all sparse-expert LB gradients must be zero was therefore mathematically too broad.

**Change.** The zero-gradient guard now applies only to the derivative of layer \(\ell\)'s own LB term with respect to layer \(\ell\)'s expert parameters. Total-LB gradients reaching earlier experts through later Router sources are measured against their LM gradients and reported as a cross-layer pathway.

**Eligibility impact.** None. The decision question, treatment, checkpoints, data, primary shadow-step NLL outcome, and verdict direction are unchanged. The amendment prevents a valid mechanism from being mislabeled as an implementation failure and adds no post-outcome tuning.

## I. Amendment 2 — Differentiable LB Shadow Engine And Source-Trajectory Boundary (2026-08-09)

**Trigger.** The first end-to-end shadow smoke used the original training command with re-entrant activation checkpointing. The LM-only and nominal LM+LB branches logged different total objectives, but all eight optimizer shards and every saved model tensor were identical. The original model returns LB inside a nested auxiliary dictionary; under the registered re-entrant checkpoint path, that first-pass auxiliary tensor is not connected to the recomputed backward graph. Thus the 30B source runs recorded the configured LB value as telemetry but did not apply an LB gradient.

**Execution repair.** Both counterfactual one-step branches now disable activation checkpointing. No model, checkpoint, batch, objective, optimizer state, or hyperparameter changes. A hard smoke guard requires the repaired LM-only applied update to be tensor-exact with the original LM-only applied update, while the repaired LM+LB branch must change at least one optimizer shard relative to repaired LM-only. The original detached branches are retained as invalid engineering evidence under their unsuffixed names; eligible branches use suffix `v2`.

**Interpretation repair.** A16 now measures the counterfactual immediate effect of making the registered LB objective differentiable at frozen states from the completed trajectories. It does not claim those source trajectories were trained under effective LB regularization. Centered-versus-Vanilla comparisons, the primary WoS shadow NLL metric, stages, seeds, and verdict directions remain frozen.

**Eligibility impact.** The first smoke shadow outcome is ineligible. Raw gradient-pathway results remain eligible because they explicitly differentiate native LB without activation checkpointing. Full execution is eligible only after the LM-only equivalence and LM+LB optimizer-effect guards pass.
