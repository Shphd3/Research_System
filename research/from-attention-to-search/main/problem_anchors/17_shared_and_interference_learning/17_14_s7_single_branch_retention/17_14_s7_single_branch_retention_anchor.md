# Anchor: acquisition and retention with one Dense or routed LoRA branch

## 1. Problem Definition

**Decision question:** after learning an old task, does selecting one low-rank branch per prediction position reduce the old task's held-out loss increase while retaining the new task's loss improvement, under the same training-compute budget?

Status: **researcher-requested review draft; scientific design not yet approved**. [中文](17_14_s7_single_branch_retention_anchor_cn.md). The researcher confirmed the purpose, an eight-layer fresh S7 backbone with a fixed final-Attention-output sparse autoencoder, and one insertion position: one Dense branch or one selected expert, without an additional shared expert. The insertion point, optimizer, data, budgets and scientific thresholds below remain `AI_PROPOSAL`. This draft does not create or reset a Focus. The present conversation owns activation; a stable Focus identity remains to be reviewed separately.

The root problem is why data that update shared parameters help or harm one another. The practical purpose is to improve new-task prediction with less damage to old-task prediction. Existing mixed training and one-step update selection do not establish this sequential-learning phenomenon in the proposed architecture. Establishing the phenomenon is the smallest next decision; sparse-autoencoder analysis is preparation, not the reason to run the experiment.

Here a **low-rank branch**, abbreviated LoRA, adds a product of two trainable matrices to one frozen projection. Dense uses the same pair for all positions. MoE stores multiple pairs and a **router** computes probabilities from the current visible-prefix representation, selecting one pair per position. Old-task branches remain trainable in the new stage; whether they receive a direct task gradient depends on routing. No task-specific branch is frozen to protect old performance.

Support would justify a separate mechanism question. Non-support would remove the current reason to explain a retention advantage. Insufficiency, including failure to learn the new task, would require repairing the phenomenon measurement rather than beginning many subspace tests. Generative answer accuracy is outside the primary claim; the primary outcome is reference-answer prediction loss.

## 2. Physical Priors

1. **Analysis assumption:** for the same teacher-forced visible prefix, frozen upstream weights produce the same input to the last Attention output projection. The trainable branch can therefore change its output while leaving its input fixed.
2. **Empirical assumption to audit:** held-out reference-answer cross-entropy can measure task-prediction acquisition and retention for this small model. It does not by itself measure independently generated correct solutions. Answer-template and token-length effects remain possible.
3. **Candidate mechanism, not an established prior:** assigning examples to different experts changes which examples contribute direct task gradients to each expert. It might reduce harmful shared updates, but may also reduce useful transfer or new-task learning. Trainable routing, optimizer state and greater stored capacity remain competing causes.

## 3. Falsifiable Hypotheses

The first experiment tests a **phenomenon hypothesis**: at the registered compute endpoint, MoE causes less old-task loss increase than Dense while its new-task loss improvement and final new-task loss are non-inferior. The strongest immediate rival is that MoE protects old predictions merely by learning the new task less. A joint new-learning guard and old-damage comparison can distinguish this rival at the registered loss scale. Larger improvement alone is insufficient: an arm starting at worse new-task loss could improve more and still end worse.

Further rivals survive this first comparison: more stored parameters, different old-stage starting skills, probability gating that attenuates the branch, and unmatched routing or optimizer computation. They must be reported. A favorable comparison establishes an advantage of the complete registered architecture under its budget, not a causal proof that routing reduces gradient conflict.

The **mechanism hypothesis**, reserved for a later approved test, is that the actual parameter update changes old-sample representations less in loss-increasing directions without deleting new-task-useful change. A smaller representation distance or a more separated sparse code cannot establish that hypothesis.

## 4. Mathematical Model

The proposed branch modifies the last Attention output projection, zero-index `blocks[7].attn.o`. For each token position, its frozen input is \(c\in\mathbb R^{2048}\), the frozen projection is \(W_O\in\mathbb R^{1024\times2048}\), and the output before the block residual is \(a\in\mathbb R^{1024}\). A rank-\(r\) branch has \(A\in\mathbb R^{r\times2048}\), \(B\in\mathbb R^{1024\times r}\), with fixed scaling \(s\). The two architecture computations are

\[
a_{\rm Dense}=W_Oc+sBAc,\qquad
a_{\rm MoE}=W_Oc+p_k sB_kA_kc,
\quad p=\operatorname{softmax}(Rc+b),\quad k=\arg\max_j p_j.
\]

The router has \(R\in\mathbb R^{E\times2048}\), \(b\in\mathbb R^E\), and \(E\) experts. The selected softmax probability is retained rather than replaced by one; this provides a differentiable path to the router but also attenuates the expert output. The fixed residual and full downstream MLP, norm and vocabulary head map \(a\) to probabilities. They are not replaced by a linear probe or a sparse-autoencoder reconstruction.

The token loss is \(\ell=-\log P_\theta(y\mid X)\), using natural logs, where \(X\) is the visible prefix and \(y\) the next reference-answer token. Neither router nor SAE reads that target. Let \(e=\partial\ell/\partial a\in\mathbb R^{1024}\). Dense factor gradients are exactly \(\nabla_B\ell=s e(Ac)^\top\) and \(\nabla_A\ell=sB^\top e c^\top\); selected-expert gradients gain the factor \(p_k\). For a fixed selected index, router-logit \(q_j=(Rc+b)_j\) has derivative \(\partial\ell/\partial q_j=p_k(\mathbf1[j=k]-p_j)e^\top sB_kA_kc\). There is no ordinary derivative through the discrete selected index. Aggregate these token gradients using the registered valid-answer-token denominator.

The optimizer produces factor increments, not a free full-matrix increment. For any optimizer, the exact induced matrix change is

\[
\Delta(sBA)=s(B\Delta A+\Delta B A+\Delta B\Delta A).
\]

These factor identities hold in real arithmetic. Actual native activation changes after BF16 casts/addition are measured separately; their rounding residual is not assumed zero. AdamW additionally uses moment state, coordinate scaling, clipping and weight decay. An unselected expert has no direct current-token task gradient, but an allocated zero gradient does not guarantee an unchanged parameter when historical moments or decay are active; a separate Parameter with `grad=None` is skipped by the proposed optimizer. Router updates can also change the expert selected by an old sample. A first-order loss approximation is valid only within a sufficiently small region with fixed selections; finite route changes must use native recomputation.

At evaluation stage \(t\), define \(L_{d,t}\) as the sum of reference-answer losses divided by the number of valid answer tokens in the **same fixed held-out task set** \(d\). It is empirical held-out total cross-entropy, in nat per valid token; no irreducible noise is subtracted. Stage 1 ends old-task training; stage 2 ends new-task training. The joint decision quantities are

\[
G_{\rm new}=L_{{\rm new},1}-L_{{\rm new},2},\qquad
F_{\rm old}=L_{{\rm old},2}-L_{{\rm old},1},\qquad
D_F=F_{\rm old,Dense}-F_{\rm old,MoE}.
\]

Positive \(G_{\rm new}\) means prediction learning; positive \(F_{\rm old}\) means prediction damage; positive \(D_F\) favors MoE retention. Compare \(D_F\) only with new-task improvement, final new-task loss, starting-loss and compute guards. The practical margins and compute budget are `BLOCKED` pending researcher review.

The fixed sparse autoencoder, abbreviated SAE, encodes \(a\) into a sparse vector \(z\), then reconstructs it with a fixed decoder \(D\) and bias \(b_{\rm SAE}\). Defining reconstruction residual \(\varepsilon=a-b_{\rm SAE}-Dz\) yields the exact bookkeeping relation \(\Delta a=D\Delta z+\Delta\varepsilon\). This does not identify causal harmful directions. Both the raw displacement and unrepresented residual must be retained. SAE reconstruction is excluded from the training objective and the native prediction path.

## 5. Computational Realization

**Goal: isolate a measurable learning and retention trajectory. How:** start both arms from one frozen fresh S7 checkpoint; learn GSM8K, then learn MMLU without replay in the first proposed test. Why: sequential exposure supplies before/after old-task measurements that mixed training did not. These dataset and no-replay choices remain `AI_PROPOSAL`; the cache uses internal resplits, including MMLU source records from official test, so scientific split eligibility remains pending. Exact sources and splits belong to the [formal Protocol](../../../experiments/A17/17_14_s7_single_branch_retention/20261007/protocol.md).

**Goal: close the parameter-to-loss computation. How:** retain the last projection input, native output, residual, full frozen tail and reference targets for the same old records at stage boundaries. Why: the branch changes exactly the vector observed by the existing SAE, while native loss tests the consequence. The verified [S7 implementation](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/dense_sae/model/modeling_qwen3_sae.py) defines this Attention output before residual addition.

**Goal: establish trustworthy measurements before scientific spending. How:** run a separate bounded training-plus-analysis [Smoke Protocol](../../../experiments/A17/17_14_s7_single_branch_retention/20261007/smoke_protocol.md), already authorized by the researcher on four reserved H100 GPUs. Why: check frozen weights, gradient paths, target alignment, counters, resume and SAE/native-tail analysis without using engineering results as scientific support.

## 6. Minimal Falsification Tests

One paired two-stage Dense/MoE comparison is proposed. Its decisive table contains old-stage acquisition, new-stage acquisition, old-stage damage, starting losses, cumulative valid answer tokens, actual/estimated train-compute components, total stored parameters and active parameters. Same rank or same update count alone is not compute matching.

The supporting branch requires: both arms first learn the old task; both learn the new task by an approved minimum; Dense exhibits meaningful old loss damage; MoE's new improvement and final new-task loss satisfy their approved non-inferiority guards; and MoE reduces old damage beyond the approved practical margin under the registered compute budget and uncertainty rule. It supports only this phenomenon.

The non-supporting branch occurs when an otherwise eligible comparison reliably rules out the registered retention advantage. If neither architecture damages old predictions, the proposed harmful-retention phenomenon is absent at this setting and there is no current reason to explain it. Insufficient evidence includes failed learning, unmatched compute, a large starting-skill mismatch, interval overlap with the decision boundary, or an invalid measurement. Numeric margins, seed aggregation and uncertainty criteria remain proposed or `BLOCKED` in the formal Protocol; no scientific Pass can be assigned before approval.

## 7. Current Evidence

In eight-task mixed Qwen3-0.6B training including GSM8K, the final-layer Dense rank-16 arm and trainable-router MoE arm had mean held-out answer cross-entropy 0.737787 and 0.689914 over three seeds. That MoE included an unconditional shared rank-8 branch plus a selected rank-8 expert; this draft removes the shared branch and uses fresh S7. The observation supports a mixed-loss difference, not sequential retention or the present architecture. Stored capacity and actual compute were not both matched. [Owning Summary](../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/summary.md).

The existing exact-33B S7 analysis constructed fixed matrix increments and selected among them on a frozen model. It did not train LoRA experts or measure acquisition and forgetting. [Evidence scope](../../../../../../daily_research_reports/1002/candidates/ntp_representation_update_channels/probe_33b_summary.md).

Current two-stage phenomenon experiment: **NOT RUN**. Smoke execution is separately recorded by its receipts; no hypothetical completion or verdict is imported here.

## 8. Claim Boundary And Next Decision

Exact gradient and factor-product relations close the proposed computation. They do not prove a MoE benefit. Sparse-code movement, activation distance, cluster separation and probe accuracy cannot replace native held-out loss; representation edits cannot be called implementable parameter training.

**One next decision:** review and freeze the two-stage phenomenon Protocol, using the authorized Smoke only to repair measurement and execution. Completion requires approved architecture detail, data splits, compute definition/budget, margins and decision rules plus engineering qualification. Resume by running only the subsequently approved formal scope; if the phenomenon is unsupported or unmeasured, do not escalate to a catalogue of SAE direction analyses.
