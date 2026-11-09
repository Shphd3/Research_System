# A17_03: Old-task-sensitive updates in sequential learning

[中文](17_03_old_task_sensitive_update_anchor_cn.md)

problem_key: `old_task_sensitive_update`. The researcher activated this bounded sequential-learning question through the attached Anchor/Protocol and authorized reasonable correction, placement, execution and result analysis on 2026-10-11 (Asia/Shanghai). Computational choices are AI-adopted implementations within that delegated scope, not established physical facts. Mechanism judgment/closure:Unknown. This is a sibling parent of A17_01 and A17_02; no fourth experiment is added to their Focus.

## 1. Problem Definition

After learning one visible list rule, can the opposite rule be learned while reducing old-rule loss degradation by avoiding estimated old-task-sensitive parameter directions? The parent asks how shared learning helps or harms under finite resources. Earlier A17 found cross-rule CE help, while pair margins were inconsistent; those are local or joint-learning results, not sequential-retention evidence. This experiment opens an explicit sequential comparison without assuming forgetting exists.

Support would show that this bounded strategy can protect old predictions while preserving new learning. No ordinary forgetting stops the proposed forgetting-mechanism interpretation in this setting. Reduced new learning or weak sensitivity qualification limits this projection strategy, not every possible compatible update. Expert utility and global update necessity remain outside scope.

## 2. Physical Priors

Candidate mechanism:old and new prediction losses may depend on overlapping parameter changes. Sensitivity is unsigned:both harmful and helpful changes can lie in a sensitive direction. Overlap or different directions alone therefore imply neither interference nor independence. The old rule is visible and both tasks are jointly satisfiable, but finite optimization may still incur a sequential tradeoff. These claims remain testable, not an assumed explanation of forgetting.

## 3. Falsifiable Hypotheses

A finite-dimensional old sensitivity estimate may identify removable new-update components whose restriction lowers old loss degradation while retaining new gain. Strongest rivals:ordinary new training does not forget old learning; projection only weakens updates or reduces available capacity; estimated sensitivities do not transfer to heldout records; a fixed local basis becomes stale during training. Norm matching and equal-rank random restriction separate generic shrinkage/capacity from direction-specific effects. Failure to find protection is not proof that all new learning must change old-sensitive directions.

## 4. Mathematical Model

Let W be the final Attention o_proj matrix, with other model weights frozen. Old A/new B are FIRST/LAST in both sequential orders. Correct one-token answer CE is L_A(W) or L_B(W), in nats per answer. At the old-trained state W_A, obtain per-example gradients g_i=vec(∇_W ell_A,i) on old training records; the uncentered second moment F_A=n^−1Σ_i g_i g_iᵀ operationalizes squared first-order CE sensitivity, not a complete Fisher/Hessian or functional partition.

Let Q have orthonormal rows spanning its leading fixed-rank directions, and let P=I−QᵀQ. For a new gradient g_B,t, ordinary direction is−g_B,t; protected direction is−Pg_B,t. Each constrained step is normalized to the corresponding ordinary trajectory's step norm s_t:

\[
\Delta w_t^{protected}=-s_t\frac{P g_{B,t}}{\|P g_{B,t}\|},\qquad
\Delta w_t^{random}=-s_t\frac{(I-R^\top R)g_{B,t}}{\|(I-R^\top R)g_{B,t}\|}.
\]

R is an independent orthonormal equal-rank random basis. These are parameter-space directions, not representation directions, experts or SAE features. Ordinary s_t uses clipped plain SGD; no momentum escapes the constraint. The comparison matches actual displacement norms within rounding tolerance, sample order, answers and parameter storage; ordinary unconstrained dimension differs from constrained dimension, while protected/random dimensions match.

For small delta w, per-example old change is g_iᵀdelta w+remainder. The projector removes the fitted subspace term, not all old sensitivities; second-order effects and sensitivity drift remain. Removing unsigned sensitivity can also remove helpful old changes. Measure finite old degradation D=L_A(W_final)−L_A(W_A) and new gain G=L_B(W_A)−L_B(W_final), plus accuracy and pair margins. Positive D is forgetting, positive G is new CE learning. Geometry alone predicts neither sign.

## 5. Computational Realization

Goal:compare useful new acquisition and actual old retention, not prove forgetting by construction. How:from the official Qwen3-0.6B Base train only o_proj on A, then restore the identical A state for ordinary/protected/random B training. Why:the task-specific constraint becomes the manipulated factor with norm/capacity controls.

Estimate Q from individual old training gradients, without centering/cancellation or dev outcome selection. Freeze it at the A endpoint. Check squared gradient coverage and bidirectional finite perturbations on independent old dev records; measure both signs rather than call sensitivity harmful. All data use the earlier paired three-word task, answer-only supervision, separate nominal order-new/combination-new and combined reporting. Test remains unread; already exposed dev gives descriptive evidence, not blind confirmation. Source fit/training precedes evaluation. Full native model forward is used throughout; no SAE or tail-replay approximation.

The [Protocol](../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E01_sequential_projection/protocol.md) owns fitted rank, sample counts, norms, training/token budget, thresholds, Smoke/resume, readouts and source freeze. These operational settings do not establish intrinsic task geometry or optimizer-independent conclusions.

## 6. Minimal Falsification Tests

First qualify old acquisition and ordinary new acquisition. If ordinary B learning does not materially worsen A CE, report that finding and do not force a conflict story. If it does, compare protected old loss with both ordinary and random, while reporting retained new gain. Raw paired seed/order outcomes must accompany aggregates; two directions are dependent within a seed. Any source/model/data/numeric or actual-constraint failure makes affected scientific evidence ineligible.

Protection with useful retained gain supports one constructive compatible-update strategy. Less forgetting with less new learning is a tradeoff, not solved compatibility. Failed protected learning or poor old sensitivity generalization leaves the necessity question unresolved. Practical tolerance is a declared operational screen, not population significance. No single projection failure proves absence of a compatible parameter path.

## 7. Current Evidence

Completed:3seeds,bothorders,6old/18new trajectories,48000validtraininganswers. All6ordinarycases improveold/newCE;ordinarydirectionoldCEmeans−0.078888/−0.082602,no netCEforgetting. ProtectedQ-complement gains exceedordinary6/6,ratios1.1257–1.2600,but LAST→FIRST oldaccuracy−2.083pp,not comprehensiveprotection. Estimatedbasis covers51.6–61.3%mean per-examplegradientenergy on20heldoutoldrecords,not all-oldinsensitive space. Frozenconsistentanti-forgetting criterionunsupported;AI-proposedboundedinterpretation,mechanism/closureUnknown. [Summary](../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E01_sequential_projection/summary.md).

## 8. Claim Boundary And Next Decision

Allowed:given this model, matrix, fitted basis, task pair and sequential training budget, an old-sensitive restriction helped/hurt finite retention and new acquisition relative to the stated controls. Cannot infer necessity across all optimizers/directions, common/unique experts, parameter function partitions, SAE failure implications, natural-text continual-learning mechanisms or separated-architecture benefit. The next researcher decision is whether the qualified sequential contrast supports studying this estimated sensitivity route further, or whether its bounded answer suffices. Mechanism and closure remain Unknown.

### 2026-10-11: Authorized fixed-source mechanism analysis

The researcher requested a causal explanation and necessary experiments from this subproblem. [Subanchor17_03_01](subanchors/17_03_01_component_causality_anchor.md) isolates finite component deletion and remainder amplification at a fixed old state and source update. It addresses the parent joint-intervention gap. E01 frozen evidence is preserved; new measurement is pending and mechanism/closure remain Unknown.

### E02 factual completion / 事实结果完成

2026-10-11: Smoke140/140, replay4/4, Full630/630 qualified. The frozen E01 evidence is unchanged. [E02 Summary](../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E02_component_causality/summary.md) / [中文总结](../../../experiments/A17/17_03_old_task_sensitive_update/A17_03_E02_component_causality/summary_cn.md) owns the new fixed-state deletion/amplification findings. Human mechanism/closure judgment remains Unknown; execution completion does not close this Anchor.
