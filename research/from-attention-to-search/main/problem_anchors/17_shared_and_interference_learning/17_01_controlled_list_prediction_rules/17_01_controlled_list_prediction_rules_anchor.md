# A17_01: Controlled List Rules And Shared Learning

[中文](17_01_controlled_list_prediction_rules_anchor_cn.md) · [A17](../README.md)

Problem key: `list_rule_shared_update`; identity preserved after authorized relocation. Researcher confirmed FIRST/LAST, Qwen3-0.6B tokenizer, answer-only loss and both novelty panels. On 2026-10-10 the researcher adopted direct final Attention `o_proj` as primary and rank-8 LoRA as a capacity control, authorized E03 Smoke→four-H100 reserved Full, independent frequency execution and matched raw-output SAE training/analysis, and requested terminal supervision. Exact implementation settings are delegated within this consensus. Scientific mechanism judgment remains `Unknown`.

`task_state=E03_NATIVE_FULL_COMPLETE_SAE_PENDING`; `question_state=HUMAN_CONFIRMED`; `design_state=DIRECT_PROJECTION_ADOPTED_EXACT_SETTINGS_DELEGATED`; `result_state=DESCRIPTIVE_NATIVE_EFFECTS_RECORDED`.

## 1. Problem Definition

At one shared-model state, does effective learning of a list's first-item rule help or harm its last-item prediction, and vice versa? The upstream purpose is to understand useful/harmful shared learning under finite resources. Controlled content and answer marginals let us vary visible conditional rules.

FIRST/LAST use the same ordered list but different instructions, so complete prefixes differ and both labels are simultaneously satisfiable. Task difference does not itself require experts. The independent A17_02 frequency question compares presentation policies. SAE is an authorized explanation/intervention tool for observed native effects; it is not required to succeed as a proxy. Data/engineering failure repairs the carrier, not refutes sharing.

## 2. Physical Priors

Researcher intuition: the rules may reuse list reading while needing different position selection. Functional reuse is unverified; three distinct words and a visible instruction make both tasks solvable by an expressive conditional predictor. Current errors, position preference and update size may alter shared-update effects.

Basic processing plus useful conditional corrections is a candidate functional decomposition, later a candidate architecture. One sample may require both; orthogonality or common activation does not identify functions. Restricting final-layer learning cannot inventory shared functions already computed upstream.

## 3. Falsifiable Hypotheses

A useful FIRST update may raise independent LAST loss, or vice versa. A rival is shared parsing/answer-vocabulary learning that helps both. Positional difficulty and excessive step size also compete with an intrinsic-conflict account.

Report all four source/recipient cells and no-update references. Useful-source qualification plus actual finite recipient loss defines local help/harm; gradient overlap is secondary. The AI frequency extension asks whether extra A changes B differently under same/different rules. Its positive interaction may mean less help, not net harm. Smoke validates implementation, not scientific replication.

## 4. Mathematical Model

Let L=(w_1,w_2,w_3) be an ordered list, r its visible FIRST/LAST rule, and x=T(r,L) end at the answer marker. The correct word legally occurs among list candidates, not after the marker.

\[
f_{\mathrm{FIRST}}(L)=w_1,\qquad f_{\mathrm{LAST}}(L)=w_3.
\]

Qualified continuation y is one token. Answer loss is full-vocabulary \(\ell_\theta(x,y)=-\log p_\theta(y\mid x)\), nats/answer; other labels are ignored. From the same state θ, source s produces θ'_s; independent recipient records D_r define

\[
\Delta_{s\to r}=\overline\ell_{D_r}(\theta'_s)-\overline\ell_{D_r}(\theta).
\]

Negative means help, positive harm. E01 freezes one virtual plain-SGD step without changing the training optimizer. E02 qualified restricted implementations. E03 freezes effective matrix steps at early and terminal states, uses the same actual perturbation under FP32/BF16 readers and distinguishes finite local effects from the training trajectory.

For final projection input a/output h with frozen upstream and no bias, actual effective ΔW gives exact Δh=ΔW a. Native loss derivative e_h gives first-order e_hᵀΔh, with remainder defined by actual finite loss. This existing local model is not a new empirical discovery. Proposed frequency observable: at B200, compare different-minus-same B loss at A800 versus A200; budget allocation is a separate observable. SAE must preserve its reconstruction residual and actual hook; it cannot substitute for native loss.

## 5. Computational Realization

Confirmed carrier: local Qwen tokenizer,20 distinct one-token Chinese continuations; paired visible FIRST/LAST, answer-only full-vocabulary CE. E01 has4,000 train/800dev/800test rows. Correct list candidates are allowed, completed answers are not input. Constructed balance does not establish natural-text evidence.

The two constructed novelty panels are relative to membership in the registered task-training split. Each checkpoint additionally audits actually presented content groups; unpresented groups cannot be called seen content. Preserve nominal panels and the full800 aggregate; actual-exposure reclassification is qualification post-processing, not a replacement primary. Order-new: order-new retains seen unordered content but holds out order; combination-new holds out the unordered group. Dev/test lists and new groups are disjoint. Report rule×panel and weighted combined, preserving group dependence. Model test access remains closed until an adopted confirmation contract.

Completed E01 briefly adapted whole-LM Dense/Qwen; S7 only supplied initial capability. Their architectures/history differ, and S7's sidecar does not establish SAE analysis or random-initialization acquisition.

**Adopted restricted learner:** original Qwen Base, final layer27 Attention `o_proj` only; all other weights are frozen. Direct1024×2048 has2,097,152 parameters; shared rank8 LoRA has24,576 factors and cumulative rank≤8. They are not equivalent and equal LR does not match displacement. [E03 Protocol](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/protocol.md) owns three seeds,100 balanced updates, full dev probes and final-only test opening. The restriction localizes updates; it does not establish format-only learning or slower saturation. E01/E02 frozen contracts remain historical.

**Independent frequency and matched observer:** [A17_02 Anchor](../17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor.md) and its [Protocol](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/protocol.md) own fixed-pool presentation-frequency addition and separate allocation comparisons. They do not inherit this Anchor's local estimand. The chosen representation is raw final `o_proj` output before residual addition. Existing Qwen E16 SAE reads normalized MLP input and mismatches; retrain its30,000-latent/Top32 configuration on the matching raw output for at least1B valid prediction tokens, retaining separate raw/reconstruction-eligible counts. Matching S7 uses its own raw-output dictionary and exact parent. E03's append-only SAE stage contract owns training/analysis, residual-preserving displacement decomposition and held-out finite interventions. Dictionary mismatch/OOD failure limits the SAE claim, not the native effect. [Derived explanation](../../../research_notes/A17_shared_learning_logic.md) owns no design.

## 6. Minimal Falsification Tests

Data admission checks exact oracle, continuation boundary, pairing/counts, both novelty definitions and no completed answer leakage. Failure rejects the release.

Smoke admission checks four GPU devices, finite answer-normalized loss, independent source/answer counts, required TensorBoard, native initial equivalence, exact frozen weights, actual saves, external-process resume and finite no-op/cross-rule readouts. Initial ability is separate;100% dev accuracy flags saturation, not complete mastery.

Scientific local harm/help needs a qualified useful source and resolved positive/negative recipient finite effect. Unresolved source/sign is insufficient. Repeated source batches are within-seed sensitivity, not independent scientific replications; three training seeds have descriptive uncertainty only. For the frequency trajectory, source improvement is not a gate: it only qualifies effective-update mechanism interpretation. Independent seeds and frozen threshold/test handling are required before confirmation. SAE must preserve reconstruction residuals, qualify the adapted-state reader and compare held-out finite interventions with effective-rank PCA/random and perturbation-size controls. New analysis source groups and recipient discovery/heldout groups are frozen separately; original Full source-batch leaveout may overlap records and is only a sensitivity panel. Proxy failure preserves native evidence.

## 7. Current Evidence

Researcher-supplied1009 text defined the carrier. E01 dataset and31 engineering gates passed; job pt-2m4rvpt4 completed on four reserved H100 GPUs. Its Summary reports initial capability/short adaptations; source coverage and saturation restrict scientific meaning. E02 retry job pt-i3ianttt completed;64/64 engineering checks passed. Its Summary/Detailed preserve the failed zero-step attempt, repair and numeric limits. E03 Smoke pt-fleom0t0 passed64/64 engineering gates; Full pt-ujjb8f7a SUCCEEDED with six trajectories/12,000 answers and96/96 engineering PASS. The [current Summary](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/summary.md) owns complete native facts and bounded local readouts. SAE is pending; mechanism Unknown.

Historical internal-vector work modulated help while four mean effects remained beneficial; it motivates net-loss controls but is not a list-task result. Existing verdicts are preserved.

## 8. Claim Boundary And Next Decision

Qualified data establishes conditional rules; qualified Smoke only establishes implementation and bounded dev readouts. Local effects do not identify complete common/specific functions, expert necessity, natural-pretraining effects or long-term utility. SAE description/intervention and architecture utility require distinct evidence.

The researcher adopted the update scope and authorized the full sequence. AI now completes the registered measurements and factual records. The next researcher decision, after complete evidence, is whether bounded sharing effects and observer controls justify a mechanism interpretation or carrier adjustment. Training completion cannot close the scientific question. E01/E02 frozen contracts/results and this problem identity are preserved.

[Focus](../../../focus/focus_list_rule_shared_update.md) · [E01 Protocol](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E01_stage1_smoke/protocol.md) · [E01 Summary](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E01_stage1_smoke/summary.md)

### 2026-10-10: authorized paired-answer-margin supplement

[Sub Anchor](subanchors/17_01_01_rule_conditioned_answer_margin_anchor.md) and [sub Protocol](../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/subprotocols/paired_rule_margin/protocol.md) fix relative-selection readouts before/after saved updates. Parent question, recorded evidence and Unknown mechanism judgment are unchanged. The new supplement is NOT_RUN; earlier E03 completion is scoped to previously authorized stages.
