# A15_26: Previously learned computations in low-frequency compositions

[中文](15_26_low_frequency_compositional_reuse_anchor_cn.md)

## 1. Problem Definition

The researcher confirmed the core question: **do previously learned operations help a model learn low-frequency compositions, and do operation computations participate in composition prediction?** Learning with the original parameters completely frozen is a stronger hypothesis, not a prerequisite for studying reuse. Controlled composition is an accepted evidence setting. Specific interventions and numerical criteria remain proposals.

This is an independent A15 parent. A15_24 tests frequency-organized expert invocation; A15_25 prepares feature relations and its 15_25_01 child tests a frozen representation decomposition; A17_04 tests conditional-rule reversal. This question changes the learned objects and the intervention target. Those owners supply evidence and methods, not a parent decision inherited here. A12 supplies relevant composition-carrier failure boundaries, not an MTP objective for this question.

The immediate decision is whether an identifiable operation-level reuse test can accompany a learning-help comparison. A better composition score alone cannot answer the mechanism question. Natural-language semantics, shared versus separate experts, and learned gating are outside this round.

## 2. Physical Priors

Researcher-confirmed intuition: known component processing might support a composition that receives little direct practice. This does not equate frequent, mastered, common, or high singular value. Mastery must be measured before composition learning.

AI mechanism proposal: the same operation function may remain causally available across atomic and composition contexts. A credible rival is a composition-specific mapping learned independently of atomic behavior. General format familiarity and answer-vocabulary adaptation also explain faster learning. Distributed or redundant implementations can prevent a proposed intervention from identifying reuse even when reuse exists.

## 3. Falsifiable Hypotheses

- **Learning help:** at matched composition supervision, relevant atomic training improves held-out composition learning over same-origin controls. Equal-format alternative-operation training is informative but may introduce negative transfer; it cannot be the only control.
- **Operation-level reuse:** after composition learning, a qualified change to one atomic operation transfers to its compositions in the direction computed by the unchanged downstream operation, without any new composition labels. Independent whole-composition memorization predicts no such systematic transfer; nonspecific damage predicts changes that fail the prespecified answer and unaffected-task checks. This is an AI-proposed separator, not an approved mechanism conclusion.
- **Exposure effect:** operation-pair exposure can affect generalization when component marginals are fixed; exchange high/low pair identities to distinguish exposure from intrinsic pair difficulty.
- **Stronger frozen hypothesis:** freezing the parent and learning a bounded additional path can be sufficient. Failure of this strategy does not refute the preceding hypotheses.

## 4. Mathematical Model

An atomic operation maps an input symbol to an output symbol. In the candidate task, each operation is a fixed permutation of the symbol set. For input \(x\), first operation \(f_i\), second operation \(g_j\), intermediate symbol \(z\), and target \(y\), the external specification is

\[
z=f_i(x),\qquad y=g_j(z).
\]

The candidate default is 32 symbols and four operations of each kind. These sizes are not frozen. The model receives both operation identities and the starting symbol and predicts only the final symbol in one invocation. It is not given the correct intermediate symbol. The specification does not assert an internal two-stage implementation.

For the proposed rule revision, replace \(f_i\) by a permutation \(f'_i\), for example by swapping two output assignments. Before viewing revised-composition predictions, the external revised target for every affected query is fixed as

\[
y'=g_j(f'_i(x)).
\]

Only queries with \(y'\ne y\) identify an answer switch. On a fixed held-out set of such queries, the primary proposed behavioral quantity is the fraction predicting \(y'\). Report the fraction still predicting \(y\), every other answer, and paired changes from a sham revision. Also report atomic revision success and preservation of unrelated operations. This measures cross-context functional transfer; it does not by itself identify a unique circuit or prove that every original parameter path survived composition training.

A complementary state intervention tests a more specific causal interface. A source with intermediate value \(z'\) is used to replace a locked candidate state in a receiver whose second operation stays \(g_j\). The prediction is \(g_j(z')\), not the source's final answer. Source selection must make those answers different on the diagnostic cases. No equation makes the candidate state exist; locating and qualifying it is an empirical obligation.

## 5. Computational Realization

**Learn and establish the setting.** Train atomic operations and measure each one. Compare relevant atomic training with matched controls during composition learning. Candidate frequency conditions are balanced exposure, 8:1 pair exposure, and exchanged high/low identities with equal component marginals. The proposed held-out task uses unseen pair-input mappings for already seen pairs; it is not automatically an unseen-pair test. Exact counts, splits, model revision, updates, thresholds and budget belong in a future Protocol.

**Primary proposed causal test: change an operation, withhold all revised-composition teaching.** Clone the same qualified composition endpoint. In the revision branch, train only atomic examples of \(f'_i\); never provide revised-composition examples, labels, intermediate targets for composition, or an external two-call solver. In a matched sham branch, rehearse the original atomic \(f_i\). Confirm that the revision actually works and that \(g_j\) and unrelated atomic operations remain usable. Then evaluate all affected compositions and untouched compositions at the same fixed checkpoint. Do not select the edit or checkpoint by revised-composition success. If the edit cannot satisfy its atomic/preservation qualifications within a fixed budget, this test is insufficient, not a negative reuse result.

Illustration only: originally F2 maps s7 to s12 and G3 maps s12 to s4. Revise F2 to map s7 to s19, while G3 maps s19 to s9. The prespecified composition answer changes from s4 to s9. Teaching only the new single-operation rule and observing s9 across appropriate compositions is more diagnostic than merely making the old answer less likely. A different downstream operation must induce its own predicted answer; combinations not using the revised operation supply specificity controls. Repeat with independently selected revisions, original learned parents, and the second-operation role if the final budget permits; their number must be fixed before confirmation.

**Complementary proposal: qualify and exchange an internal state.** Select candidate interfaces using independent diagnostic data, including atomic tasks and the original atomic-trained parent. Freeze location, state mapping, rank and matching rules before confirmation; do not train the task model with interchange targets to manufacture the mechanism. Require same-state replay, same-intermediate/different-surface sources, different-intermediate sources with different final answers, unrelated-location and equal-magnitude random controls. Seek disruption and rescue using the atomic-parent source, rather than only post-composition donors. Preserve downstream operation information. A late state that merely carries an answer, or a patch that erases the downstream identity, is ineligible as an intermediate-state explanation. A decoder/probe or a successful whole-state transplant is not sufficient.

The shared atomic/composition interface, edit qualification thresholds and feasible localization method are **Unknown**. The proposed operation-revision and internal-state tests are complementary: the former tests selective functional coupling; the latter can test a particular shared causal carrier. Neither replaces the other with an unrestricted mechanism claim. At most three experiment owners are anticipated: learning/exposure, operation reuse, and the optional frozen strategy; none is created or run by this draft.

## 6. Minimal Falsification Tests

Learning help is supported only by qualified, matched comparisons, not a gain over the untrained starting point alone. Rule-revision evidence requires successful atomic revision, preservation checks, predicted final-answer switches across affected compositions, and no comparable unexplained changes in unaffected ones. All revisions and seeds are reported. A failed qualified transfer weakens this functional-coupling hypothesis; it does not prove that all reuse is impossible. Failed revision, baseline task capability or measurement qualification yields insufficient evidence.

Internal-state support requires held-out, receiver-specific predicted changes and the locked controls. An answer shift toward the source answer alone is insufficient. Even combined positive results support only the tested functional reuse and carrier hypotheses, not a unique internal algorithm. Numerical margins and confirmation sample sizes remain **Unknown** and must be fixed before results.

## 7. Current Evidence

Task state: question clarification and draft registration complete. Question state: open. Design state: **UNDER_DISCUSSION**. Result state: **NOT RUN**. Researcher acceptance of the proposed mechanism tests: **Unknown**. No experiment or resource budget is approved here; no model/data payload has been loaded for this question.

The [user source package](sources/README.md) records the original draft. Its original intervention section already proposes intermediate-state exchanges. The gap is sharper identification of prior computation, answer copying, and feasible causal interfaces, rather than a total absence of intervention ideas.

[A15_25_01](../15_25_joint_feature_graph/subanchors/15_25_01_component_reuse_anchor.md) tests frozen Boolean-composition components, not newly learned operation reuse. [A15_25_02 results](../../../experiments/A15/15_25_02_learning_history_representation/20261023/summary.md) show useful state transfer but require a same-query mixed-model donor. [R05 residual diagnosis](../../../experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/A_residual_spectral_20261023/summary.md) separates parameter constraints from functional preservation. [A12](../../12_structured_compositional_mtp_workload/README.md) records composition-capability and shortcut failures; task learnability is not assumed. None establishes this question's answer.

Method grounding: [Geiger et al., Causal Abstractions of Neural Networks, 2021](https://papers.neurips.cc/paper_files/paper/2021/hash/4f5c422f4d49a5a807eda27434231040-Abstract.html) tests causal-model alignments through interchange interventions. This motivates a predicted intervention outcome, not a guarantee that the proposed alignment or original-computation reuse exists here.

## 8. Claim Boundary And Next Decision

Keep distinct: benefit of atomic training, atomic behavior preservation, operation-level causal coupling, a shared internal carrier, complete parameter freezing, expert separation, and natural-language MoE utility. Positive evidence at one level does not establish the next. The original source Protocol remains an unregistered proposal and is not silently amended by this draft.

The next researcher decision is whether the selective rule-revision test, together with an explicitly limited internal-state follow-up, separates the intended reuse claim from the independent-composition rival. After that decision, freeze a bounded Protocol or revise the mechanism claim. No training is authorized by placement, registration, this discussion, or synchronization.
