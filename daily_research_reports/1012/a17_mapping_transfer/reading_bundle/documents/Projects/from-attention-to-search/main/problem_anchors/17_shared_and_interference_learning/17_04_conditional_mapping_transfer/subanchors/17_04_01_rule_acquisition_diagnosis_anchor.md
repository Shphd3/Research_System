派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md)；研究修改仍回到原件。

---

# A17_04_01: Diagnose acquisition of conditional list rules

## 1. Problem Definition

Which bounded change can establish reliable command-dependent selection before we interpret learning transfer between two conditional rules? The parent asks when shared updates help or harm an old rule. Its first experiment did not establish the required learned old rule: development accuracy was only 33%–54% across commands and unseen-data panels. This child tests that acquisition prerequisite; it does not repeat the consistent-versus-reversed transfer comparison.

The researcher explicitly requested diagnosis, assessment of data versus trainable parameters, and feasible training with a larger parameter budget, without another approval turn. The finite diagnostic choices below are AI operationalizations under that delegation. Candidate explanations and scientific judgment remain proposals or Unknown; execution authorization does not establish their truth.

The local decision is whether optimization, the location of trainable parameters, or input presentation is the more useful route to a qualified old-rule starting point. Success identifies a feasible route in this carrier. Failure preserves the unresolved bottleneck rather than proving that the model lacks capacity. Invalid measurements or absent controls give insufficient evidence. New-task transfer, expert separation, SAE analysis and natural-text generalization are outside this child.

## 2. Physical Priors

These are AI candidate premises, not verified internal mechanisms. First, increasing probability on words appearing in a list can lower answer loss without learning which word a command selects. Second, freezing almost all computations may constrain instruction-controlled retrieval even when the remaining projection has many parameters. Third, neutral-command semantics and input tokenization may make the observed task harder than an explicit first/last instruction with the same target words. Comparisons test these premises separately where possible; no premise says that a larger model or changed delimiter must succeed.

## 3. Falsifiable Hypotheses

Candidate H is that the acquisition failure is repairable by a bounded change to the optimizer, trainable computation, or presentation. Its alternatives are that the original setting only needed more exposure, that fitting succeeds but unseen-list generalization fails, or that none of these operational changes establishes command selection within the fixed budget.

Five conditions distinguish these routes: original final-projection SGD; the same projection with AdamW; the final four attention blocks with the same AdamW; explicit first/last instructions with the original projection and AdamW; and a neutral-command presentation whose separator is selected by a model-independent token-ID check, with the same projection and AdamW. The last condition runs only if its input/target encoding criterion can be met before GPU execution. Optimizer comparisons are not trainable-range comparisons. Larger attention scope changes both parameter count and information processing. Explicit instructions and separator normalization change presentation as a whole, so neither isolates a single linguistic or token-count mechanism.

## 4. Mathematical Model

The actual model is registered Qwen3-0.6B Base. An input contains mode one, a command and a list of three distinct words. Command 甲 selects the first word and 乙 the last. Explicit instructions preserve these labels while replacing neutral command text. A separator control preserves the neutral commands, list and labels. Each answer is one registered vocabulary token. A candidate's occurrence inside the original spaced list may use a different token sequence; this is an encoding property, not proof of an incorrectly located answer loss.

For condition \(j\), let \(T_j\) be its allowed trainable tensors and \(\theta_{\bar T_j}\) the frozen remainder. With \(n\) valid answer targets in a completed batch, training minimizes their mean next-token loss:

\[
L_j(\theta_{T_j})=\frac1n\sum_{i=1}^{n}-\log p_{\theta_{T_j},\theta_{\bar T_j}}(y_i\mid x_i^{(j)}).
\]

This is empirical answer-token CE, in natural-log units per target; it is not full-text pretraining risk. All conditions start from the same Base and see matched list/label exposure. Optimizers and allowed inputs differ only as registered. In projection-only conditions the upstream projection input \(a(x)\) is fixed, so \(\Delta h(x)=\Delta W a(x)\) is exact. Downstream predictions remain nonlinear. In the expanded attention condition upstream inputs can change, and that fixed-feature identity cannot be carried over unchanged.

The acquisition reader is \(Q_j=\min_{c,p}\operatorname{Acc}_{j,c,p}\), the minimum full-vocabulary accuracy over the two commands \(c\) and two development panels \(p\). The inherited operational qualification is \(Q_j\ge0.80\). It prevents a mean dominated by one command or one panel from masquerading as task mastery; it is not a population confidence threshold. Also measure the fraction of lists for which both command answers are correct, and separate CE into probability assigned to the three candidates and conditional choice within them.

## 5. Computational Realization

First evaluate each of the three existing old endpoints on a fixed training-list panel and its development panels. This post-hoc diagnostic asks whether the earlier run failed to fit seen inputs or to generalize; it never selects a setting from the original TEST.

Then run all eligible conditions on a tiny, fixed set of complete command pairs. This checks whether the actual computation can fit those examples. Tiny-set success is compatible with memorization and cannot establish rule generalization. Restart every full diagnostic from Base, without carrying over tiny-set weights or optimizer state, and give each condition the same bounded answer-target budget. Save common milestones rather than extending whichever arm has not yet succeeded.

Construct explicit and normalized-separator views from the same original old-mode records. Retain list IDs, split ownership and labels. The normalized view uses the fixed separator `、`; a CPU tokenizer check must establish that every candidate occurrence inside the list has exactly the intended answer-token ID and boundaries, while prefix-plus-answer remains prefix IDs plus that one target ID. If generated data fail this condition, report that arm NOT_RUN rather than selecting a replacement after learning results. The original and explicit views remain valid tasks even if their input candidate encoding differs from answer encoding.

The [Protocol](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol.md) owns exact optimizer settings, finite budgets, tensor names, source freezes, current asset checks, engineering Smoke and output registration. This realization changes the acquisition route only; it supplies no evidence yet about cross-rule transfer.

## 6. Minimal Falsification Tests

At the fixed final answer exposure, compare development command/panel accuracy with the corresponding fixed training panel. The decisive qualification is the minimum development accuracy \(Q_j\), with first qualifying saved milestone reported only as a descriptive learning-time reader. The pre-run operational threshold remains 80% for each command and panel. One training-order seed supports a diagnostic comparison, not replicated scientific confirmation.

If projection SGD fails but projection AdamW qualifies, optimization is a viable repair and a claim that this projection cannot learn is weakened. If projection AdamW fails but expanded attention qualifies, trainable scope is a viable repair under the same optimizer; parameter count alone is not identified. If explicit or separator-normalized projection conditions qualify while neutral projection AdamW fails, presentation is a viable repair; the linguistic or encoding factor responsible remains unresolved. A high training accuracy with low development accuracy points to a generalization bottleneck. If original SGD qualifies with additional matched exposure, exposure remains a sufficient practical explanation here.

If no condition qualifies, the bounded routes have not solved acquisition; this does not establish architectural impossibility. Nonfinite updates, wrong labels, invalid freeze/resume, unavailable payloads or an unmet optional tokenizer criterion yield an explicitly ineligible or NOT_RUN condition. Such outcomes cannot be used as scientific failures of the associated mechanism.

## 7. Current Evidence

The parent comparison completed, but old development command/panel accuracy was 33%–54%, below the 80% criterion. Both new branches improved mean old CE; their reversed-minus-consistent old-answer advantage effect was only −0.005165 nat. These observations support diagnosing acquisition before interpreting retention. The direct evidence and its limits are in the [parent experiment Summary](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md).

The answer target is a single token, while a word in a spaced list can use several input tokens. This source-data/tokenizer distinction motivates a separator control; it does not itself establish the cause of failed learning. A CPU full-prefix check found zero normalized-view boundary failures over9,600 candidate occurrences in the source old TRAIN/DEV and120 vocabulary-probe occurrences. Parent safetensors-header inspection found16 expanded attention weight tensors totaling25,165,824 parameters versus2,097,152 in the original projection; runtime inventory remains required. These are engineering facts, not learning results. No new GPU acquisition result exists at contract writing: all five diagnostic conditions are NOT_RUN. Scientific mechanism acceptance and question closure are Unknown.

## 8. Claim Boundary And Next Decision

This is a finite root-cause audit of old-rule acquisition in one pretrained carrier, one dataset family and one training-order seed. It can identify an effective adjustment and eliminate some absolute impossibility explanations. It cannot identify a universal bottleneck, isolate raw parameter count from computation location, claim a pure tokenizer mechanism from a format change, or establish benefits of experts. Development evidence is exposed diagnostic evidence; an eventual independent transfer confirmation requires a newly frozen heldout set.

Exactly one next decision is which, if any, acquisition setting supplies a qualified starting point for a renewed conditional-mapping transfer comparison. Completion requires all eligible bounded arms, the prior-endpoint diagnostic, actual saved-state and readout registration, and an evidence-bounded bilingual Summary; success is not required. Resume through the parent [Focus](../../../../focus/focus_conditional_mapping_transfer.md) and this child's Protocol. The researcher owns acceptance of the diagnostic interpretation and the subsequent scientific decision.

### Authorized scope supplement: one final attention layer (2026-10-11)

After the completed [E02 Summary](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary.md) established a feasible four-layer neutral-command route, the researcher explicitly requested two narrower tests: train the final layer's q/k/v/o projection weights with SGD or AdamW. This is a reduction within the same acquisition prerequisite question, not a new conditional-transfer question. Its candidate hypothesis is that four trainable attention layers are unnecessary for qualification; the rival is that one final layer does not supply an effective route under these fixed optimizer packages and budget. The observation and falsifier remain reliable command-controlled selection on both DEV panels, not candidate mass or tiny-set fit alone. The [E03 Protocol](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/protocol.md) owns exact matrices, budgets and computation. Success establishes sufficiency in this setting, not absolute minimality, QKV necessity or a pure parameter-count effect. Failure does not prove four layers necessary. Only these two tests are authorized; later steps require another researcher approval. Results are NOT_RUN at this supplement; scientific judgment remains Unknown. The prior eight-section design and completed E02 evidence retain their frozen identities.
