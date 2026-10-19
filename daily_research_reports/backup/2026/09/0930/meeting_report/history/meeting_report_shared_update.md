# Meeting report: from shared-update mechanisms to structure in natural language

> Retained as the previous expanded report. The current speaking entry is the [three-minute brief](../0930_组会汇报稿.md). Historical content and evidence boundaries below are preserved, not promoted to new scientific state.

[Current natural-text Summary](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/summary.md) · [Detailed evidence](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/detailed.md) · [中文](meeting_report_shared_update_cn.md)

Status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION. This is a meeting synthesis of completed evidence, audited for mechanism, evidence eligibility and clarity. It changes no registered verdict or researcher-owned question state. Filed under 0930; written on 2026-09-29 UTC. The original purpose is reconstructed from research records, not presented as a verbatim advisor-meeting transcript.

**Take-home:** We can now follow a shared update from parameter change to representation displacement and local loss effect. A controlled experiment measured rule-dependent modulation of benefit. In natural text, domain-average activity recurred, but the current domain-mean gradient estimator did not improve heldout description. The next useful question concerns the relationship between domain, prediction target and update compatibility.

All registered collection, SVD, all-atom and activation-pattern analyses in the current Protocol are complete; the four-GPU job succeeded. See the [completion receipt](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/evidence/completion_receipt.json). This report only replots saved results. No new experiment or statistical test was performed; the target-conditioned comparison remains unrun.

## Speaking order: six slides, about 12 minutes

| Slide | Listener's question | Content | Time |
| --- | --- | --- | --- |
| 1 | Why analyze the mechanism? | How learning A affects B; the eventual sharing decision | 1 min |
| 2 | How do parameters, representations and losses connect? | Objects and the local update chain | 2 min |
| 3 | What empirical mechanism evidence do we have? | One controlled-result figure: modulation without net harm | 2.5 min |
| 4 | What structure appears in natural text? | One figure comparing recurring activity with gradient-description performance | 2.5 min |
| 5 | What understanding changed? | Three bounded updates; roles of SVD and SAE | 1.5 min |
| 6 | What single question should follow? | Total domain association and additional association under comparable targets | 2.5 min |

Only two result figures enter the main presentation. Backup material answers questions rather than expanding the oral result inventory. Statistical language follows each comparison's actual eligibility.

This combines speaking notes and backup; it is not a script to read in full. The oral chain is six sentences: **We ask how learning A affects B. We connect parameter changes to representation displacement and loss. The controlled experiment measures modulation without net harm. Natural domain activity recurs, while the mean-gradient descriptor gives no gain. Static structure and learning effects need separate measurements. Next we compare total and same-target conditional domain-update relations.**

## Slide 1: establish a basis for deciding which data can learn together

Suggested opening:

> We began by asking why learning one kind of data changes performance on another when parameters are shared. We first traced a single update, then examined whether update demands have repeatable structure in real text. Today I will explain what each step answered and the connection that remains open.

At a fixed model state, A supplies an update and independent B data supply the outcome. Define B loss change as after minus before: negative is net help, positive is net harm. Calling A's learning effective additionally requires improvement on independent A examples.

The working mechanism hypothesis was that shared representation components can face agreeing or differing learning requirements. This separates three empirical links: **what is jointly active before updating; what actually changes; and whether that change helps the task.** Each needs its own measurement.

The longer-term purpose is a sharing decision. A local effect alone does not establish that separate parameters improve long-term training; a budget-matched sharing/separation comparison has not been run. [Original purpose and hypothesis](../../../../../../../Projects/from-attention-to-search/main/focus/focus_shared_update_conditional_interference.md)

Transition: make the representation-to-learning connection computationally explicit.

## Slide 2: the local mechanism is specified; geometry and learning requirements act jointly

Fix one state and update only one linear matrix. Other parameters, each example's context and its residual inputs remain fixed.

| Object | Meaning | Location |
| --- | --- | --- |
| Input representation \(c\) | Information entering the shared matrix | Last attention output projection input;2048 coordinates |
| Output representation \(a=Wc\) | The transformed representation | Before residual addition;1024 coordinates |
| Loss derivative \(e\) | How loss responds to increasing each output component | The local descent direction is \(-e\) |
| Parameter gradient \(G\) | This example's matrix-update demand |1024×2048, matching W |
| Compatibility \(K_{AB}\) | Agreement between two local update demands | Frobenius inner product of gradients |

For one loss-affected position, the chain rule gives the exact identity

\[
G_A=e_Ac_A^\top,\qquad
K_{AB}=\langle G_A,G_B\rangle_F
=(c_A^\top c_B)(e_A^\top e_B).
\]

Write A's source-gradient update as \(\Delta W_A=-\alpha_A G_A\), with \(\alpha_A>0\). Since B's input is fixed,

\[
\Delta a_B=\Delta W_Ac_B
=-\alpha_A(c_A^\top c_B)e_A.
\]

This displacement identity is exact. For differentiable downstream loss and a sufficiently small change,

\[
I_{A\to B}
=\ell_B(W+\Delta W_A)-\ell_B(W)
=-\alpha_AK_{AB}+R_B.
\]

\(R_B\) is the finite-step remainder, not an assumed zero. Positive K predicts first-order help; negative K predicts first-order harm. Near zero, higher-order and numerical effects remain material. For multiple positions or examples, aggregate the actual weighted outer products before forming K; the product of separate averages is generally wrong.

Plain example: A's update lowers one output component of B. If B's correct prediction benefits from lowering it, this helps; if B needs it increased, the same displacement is locally adverse. Shared activation alone cannot choose between these consequences. This is an explanatory example, not a new natural-text observation.

Gradients inhabit parameter space; the SAE encodes output-representation space. These objects are connected by computation, not identical geometry. c and e are not statistically independent: the current prediction, true target and downstream sensitivity jointly determine e. Historical learning shapes today's representations; the current loss does not retroactively change an already completed forward pass.

A sparse autoencoder (SAE) approximates a using a small active subset of dictionary directions; each direction is an atom. “Common” here means shared direction IDs with similar firing frequency and positive amplitude, not automatically shared semantics or learning requirements.

For ordinary SGD, \(\alpha_A=\eta\). The controlled experiment used \(\alpha_A=\varepsilon\|W_0\|_F/\|G_A\|_F\): epsilon is relative update norm, not a common learning rate across conditions. The scalar formula does not directly describe coordinate-preconditioned Adam.

**Conclusion:** the mechanism is closed through local loss response; why natural language generates particular K structure remains empirical. [Existing derivation§2–4](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/documents/01_机制推导与原论文审计.md) · [Actual update rule§8](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/protocol.md)

## Slide 3: the controlled experiment found modulation, while the net-harm prediction failed

**Purpose.** Measure how input task directions and answer requirements affect B after effective A learning.

**Hypothesis.** Greater task-direction overlap enlarges the kept-versus-reversed-rule contrast; the original stronger prediction also required net harm under reversal. The strongest rival was that a larger shared benefit could outweigh an adverse component.

**Comparison.** Internal binary tasks use the real S7 downstream network. A maps a positive signal to answer 1 and a negative signal to answer 2. B either retains or reverses the rule. Direction overlap is 0.1 or 0.8. Within an overlap condition, the two B rules reuse the exact same input and A update, so B's task evaluates the same displacement differently. Across overlap conditions, both A and B directions change; this is not a fixed-A intervention throughout.

Actual B loss is measured, and each A update must improve independent A examples. The top uncertainty unit is 12 paired direction families, not GPU count, update amplitudes or individual targets.

![Controlled overlap and rule comparison](../../figures/meeting_shared_update_mechanism/controlled_effect.png)

**Reading.** Left: M is the increase, at high versus low overlap, in the reversed-minus-kept loss-change contrast. At the larger update, \(M=1.5206\times 10^{-4}\) nat/target, with registered paired-bootstrap 95% interval \([1.3617,1.6722]\times 10^{-4}\). It exceeds zero and the registered detection floor in this construction. Right: high-overlap reversed B still improves by about 0.006665; both amplitude intervals lie below zero. The two vertical axes explicitly use different scale factors.

**Conclusion.** The joint direction/rule construction modulates benefit; the stronger net-harm prediction did not hold. Statistical resolution does not establish a practically useful separation benefit. [Registered result](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/summary_cn.md)

Existing posthoc attribution makes the cancellation concrete: the high-overlap reversed task-signal component is approximately \(+0.00008313\), while the other component plus remainder is about \(-0.0067480\). Net loss still falls. This derivative-based decomposition was not a separate intervention on either component, so a shared-background correction has not been isolated as the cause. [Attribution result](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260928_signal_localization/summary_cn.md)

Suggested sentence: “An effective update can contain opposing local effects; we measured those effects separately from the net outcome. We have not established the same net-interference mechanism in natural domains.”

Transition: use the now-defined update demand as the natural-text target of analysis.

## Slide 4: domain-average activation recurs, but domain-mean gradient description does not improve

**Purpose.** Examine common and domain-associated structure in natural text and whether domain labels describe repeatable update demands.

**Hypothesis.** If a domain has a stable mean update demand, its mean estimated on one set should describe another set better than a pooled mean. Two live explanations remain: population domain-mean differences are weak, or they exist but are estimated poorly in high dimensions.

**Comparison.** Fix S7, historical SAE reconstruction coefficient 0.1, and the 33B-training-token checkpoint, with about 281 million backbone parameters. The historical academic panel has 1,024 records from computer science, mathematics, physics and biology, each with two subfields:512 fit and 512 readout. Fit defines means, axes and atom sets. Model and SAE receive no updates; gradients use only real next-token loss. This is a real language model and natural text, bounded to this 281 million-parameter model.

![Natural-text activity and update description](../../figures/meeting_shared_update_mechanism/natural_activation_and_update.png)

**Reading.** Left: each cell compares two domain-average SAE firing-frequency profiles. Same-domain cross-split cosine is 0.972–0.991, above the observed cross-domain comparisons. Right: zero means no improvement over the pooled gradient mean; negative means higher description error. Single-target error increases about 0.572%, and the mean of 16 target gradients also yields no improvement.

The score \(Q_D\) is 1 minus domain-mean MSE divided by pooled-mean MSE. It tests this estimator, not every form of domain structure.

**Conclusion.** Recurring domain-average activation and an unsuccessful domain-mean gradient descriptor coexist on this split. The former provides a real-text structural observation, but does not establish domains as the appropriate sharing units.

This figure has no significance stars or uncalibrated intervals. Refitting high-dimensional means in the original bootstrap adds estimation variance; the existing interval does not establish calibrated population directional inference. Negative empirical Q remains a fact, and the stored NON_SUPPORT category is preserved, but “no population domain structure” is unsupported. Another positive diagnostic cannot rescue that primary comparison. [Result and eligibility](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/summary.md)

Historical exposure and unavailable paper IDs limit this to descriptive record-split replication, not independent-paper or pure-semantic inference. Lack of separation in two dimensions cannot exclude full-gradient structure.

Domain labels are tools for observing and testing structure here. An eventual sharing decision without manual domain labels would still need to establish that pre-update representations provide the required information.

Transition: distinguish which links now have evidence from those still open.

## Slide 5: three bounded changes in understanding

| Working conjecture | Updated understanding | Remaining boundary |
| --- | --- | --- |
| Shared representations with different requirements may create interference | Evaluate input coupling, learning requirements and net loss jointly; controlled modulation can coexist with larger offsetting benefit | No demonstrated natural-domain net conflict or long-term sharing cost |
| Domains visible in representations may also organize updates | Recurring domain-average activity establishes an observable pattern; this domain-mean estimator yields no heldout gain | Weak effects and estimation error remain unresolved; other domain relations stay open |
| Common atoms or leading singular directions may locate the effect | SVD measures concentration and transfer; SAE measures activity and decoder directions. Their update and signed-effect coverage must be tested separately | Readability, gradient energy, compatibility explanation and causal use are distinct |

SVD decomposes variation into leading directions to ask where energy concentrates and whether those directions transfer. All registered SVD and SAE analyses were delivered: estimated gradient directions transfer limited heldout energy, and the selected common SAE output span retains more gradient energy in its specified equal-rank comparison. Neither identifies most compatibility structure. Keep the numbers and dimensional budgets in backup.

A separate earlier natural next-token test found that the specified full-input-representation reader did not meet the registered 5% improvement target. This limits that reader and setting, not all information in the representation. It motivates examining K itself; the current domain analysis did not rerun that prediction test. [Prediction Summary](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/natural_ntp_representation_compatibility/20260930/summary.md)

Suggested synthesis:

> Mechanism analysis gave us the right observables: what displacement learning produces and what that displacement means for another task. Controlled evidence separated adverse components from net harm. Natural-text evidence then showed that domain activation structure cannot substitute for update structure. The next empirical link is how language relations correspond to update demands under specified conditions.

These are proposed bounded interpretations for researcher review, not automatic Focus judgment updates.

## Slide 6: separate domain relations from prediction-target relations

**AI-proposed next question:** At a fixed model state, how much domain-associated K structure varies with true-next-token composition, and how much replicates under comparable target conditions?

The mechanism motivates the question: e depends jointly on context-dependent prediction, the true target and downstream sensitivity. Existing same-target pairs have more aligned gradients, but their contexts and predictions also differ; this does not isolate target identity as the cause.

Concrete example: mathematics and biology predict different next-token distributions. Preserve the overall update relationship under their actual tasks. Then, among targets present in both domains, compare same-domain and cross-domain records with identical target IDs. This asks about additional domain association under the same target, only on common support. The removed part is not automatically spurious: what is predicted belongs to the task.

The following minimal comparison is a proposal, not an executed Protocol:

1. **Qualify coverage and inference first.** Freeze matching, weights and the primary statistic; check independent-document support and calibrate error estimation before reading new outcomes. Preserve source/near-duplicate grouping and explicitly retain unresolved dependence. The current panel is exploratory; new heldout records supply replication and previously viewed records cannot become sealed confirmation again.
2. **Report total and target-conditioned relations together.** A candidate statistic is the mean-K difference between same-domain and cross-domain pairs, testing mean-direction relations rather than all higher-order structure. Specify record/target weights. Alongside the full-panel total, retain an unconditioned comparator on the same common-target support; differences between scores on different populations or weights are not a “fraction explained by targets.” Separate raw K from gradient cosine. Account for shared document endpoints rather than treating every pair as independent. Start at one target; use a fixed 16-target aggregation only as a scale diagnostic, without selecting the best scale after inspection.
3. **Localize only after replication.** Begin with full gradients/native representations, then examine which parts are represented by existing SVD directions and SAE atoms or activation patterns. Later test whether pre-update representations predict those relationships. Target derivatives or post-update information cannot enter an allegedly representation-only reader.

| Future result | Bounded update |
| --- | --- |
| Qualified, calibrated conditional increment replicates on new records | Supports additional domain association on the specified common-target support; then test its accessibility from full representations |
| Qualified and sufficiently precise estimate misses a prespecified effect | Weakens that additional conditional relation; preserves overall task-composition effects and other language groupings |
| Sparse overlap, unresolved dependence, uncalibrated intervals or unstable estimates | Insufficient; improve the data/measurement before a structural or routing conclusion |

The strongest rival is that the observed domain relation mainly follows target composition, norms and aggregation, with no reproducible additional domain increment. Conditioning tests an additional association, not semantic causality; context, confidence and source differences must remain visible.

**One advisor decision:** adopt or reject total-versus-target-conditioned domain association as the next primary question. Exact statistics, meaningful-effect thresholds, target coverage and sample size are fixed after adoption; this report does not claim those choices were scientifically confirmed. Budget-matched shared/separate training benefit remains a later, distinct question.

## Backup: significance, SVD/SAE and completion scope

### What each number can support

| Evidence | Key result | Eligibility and use |
| --- | --- | --- |
| Controlled rule modulation | \(M=1.5206\times 10^{-4}\),95% interval \([1.3617,1.6722]\times 10^{-4}\) | Registered paired-family bootstrap; supports modulation within the construction |
| Net B effect in the same condition | \(-0.0066649\),95% interval \([-0.0066800,-0.0066492]\) nat/target | Measured net help; a positive component does not reverse it |
| Natural domain means | \(Q_D=-0.005715\); saved permutationp=0.022 | Q tests this estimator; the permutation comparison does not show superiority to the pooled mean. Population interval coverage is uncalibrated |
| Full-representation prediction | \(Q=-0.000138\),conditional 95% interval \([-0.002768,0.002294]\) | Different experiment and target from the row above; qualified non-support for registered 5% gain, not an information-theoretic impossibility |
| Target-relation clue | Same-target gradient cosine about 0.193; different-target about 0.000458 | Posthoc description; shared endpoints invalidate treating pair count as independent replication; no isolated target cause |

### Completed SVD and SAE analysis

The first 64 fit-centered gradient SVD directions retain 39.17% of fit energy and 3.18% of readout energy. This measures transfer of estimated directions. The gradient has 2,097,152 coordinates but only 512 fit records; finite-sample spectra cannot exclude population low-dimensional structure.

All 30,000 SAE atoms have frequency, positive/unconditional amplitudes, quantiles, record prevalence, positions, persistence, coactivation and full-pattern summaries. Fit defines common and enriched sets; readout checks them. Enrichment is not exclusivity, and absence in this panel is not global deadness.

The common rank 64 output span retains 8.96% of pooled readout single-target gradient energy, versus 6.21–6.31% for three equal-rank random spaces and 6.74% for native-output PCA. This is a specified descriptive comparison, not an unperformed significance test. Its off-diagonal K relative squared reconstruction error remains about 0.803; trace-energy coverage does not replace signed-compatibility explanation.

The two rank 64 objects differ: gradient SVD retains 64 full-matrix directions, while PG retains 64 output directions and all 2048 input coordinates, giving a parameter-space projection rank 131,072. Comparing 8.96% with 3.18% cannot establish an equal-budget SAE advantage. Pooled enriched-span coverage also does not test selective benefit for its own domain. [Detailed boundaries](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/detailed.md)

### Completion and unrun work

The controlled experiment, its posthoc attribution, the registered natural next-token prediction primary test and current domain geometry/activation diagnostics are delivered. In the prediction experiment, confirmation finite steps were skipped after the DEV bridge failed, and 14 structure readers were skipped by the registered primary-result gate. These are recorded terminal conditions, not measured outcomes for those comparisons. No registered stage remains incomplete in the current domain analysis. [Prediction ledger](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/natural_ntp_representation_compatibility/20260930/summary.md) · [Current completion receipt](../../../../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/evidence/completion_receipt.json)

Target-conditioned natural-text comparisons, attributable finite-step natural-text effects, a new representation-only reader and matched-budget shared/separate training comparisons remain uncompleted and are outside the current empirical claims.

### Three reasoning-audit passes

| Pass | Checks | Repair applied |
| --- | --- | --- |
| Mechanism closure | Objects, signs, dimensions, optimizer and aggregation | Separate exact displacement from local loss approximation; use the actual norm-normalized update; aggregate gradients across positions |
| Evidence and rivals | Comparator, uncertainty unit, interval eligibility and failed predictions | Restrict statistical support to qualified controlled inference; retain estimation-error rivals; do not combine activity, energy or a permutationp into causality; check common support and weights for future total/conditional comparisons |
| First-listener clarity | Purpose, manipulation, measurement, understanding and next decision | Keep two main figures; define before notation; move SVD/atom details to backup; end with one discriminating question |

Both PNG figures were visually inspected for labels and clipping. [Sources, script and hashes](../../figures/meeting_shared_update_mechanism/origins.json). Math-source checks do not verify Markdown rendering or prove mathematical claims.
