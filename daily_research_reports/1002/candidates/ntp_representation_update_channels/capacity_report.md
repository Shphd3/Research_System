# How common computation might help small experts

Working stage report, 2026-10-03. This temporary synthesis is not a final report and does not move the work into the formal project. The execution section and linked receipts distinguish preparation, GPU qualification and scientific results.

The current theoretical boundary is conditional: **common computation may improve finite-budget learning by avoiding repeated storage or pooling data across tasks to improve estimation. Those benefits and drift from shared updates require separate measurements. Serial coupling changes computation and gradients; it does not itself guarantee greater capacity or better learning.** Natural-text trajectories and finite checkpoint interventions still await empirical evidence.

The researcher's goal is for limited specialized experts to approach a larger Dense model while preserving previously learned material. The present study separates acquisition, retention and the shared update path. A final loss ranking alone does not determine method quality.

## A falsifiable model behind the intuition

Suppose tasks require the same map C plus different residual maps E_d. Storing C once can save the repeated copies that would otherwise consume each expert's budget. The important assumption is that the tasks actually admit a useful common part. An architectural branch named common does not establish that property.

Sharing has a second possible benefit: pooling observations can reduce finite-sample estimation error. In an exactly solvable mean-estimation model, complete sharing beats independent task estimates precisely when heterogeneity bias is smaller than the variance saved by pooling. Partial sharing can lower expected error without changing the function family and without serial nonlinear computation. Better learning therefore need not mean greater representational capacity. The [statistical derivation](capacity_mathematics.md) states the data-accumulation conditions. It assumes independent observations and squared loss; repeated language-token exposures cannot be substituted for its sample count.

The same squared-loss model exposes a retention issue: an old private residual may already compensate for error in the old common estimate. Improving that common estimate can break the compensation and worsen the old prediction when its private residual stays fixed. Better common estimation and better old-task retention therefore require separate measurements; more data does not by itself establish both. This is a derived possible mechanism, not an observed mechanism in the current natural-text model.

In a linear low-rank model W_d=C+E_d with private rank at most r, each task difference has rank at most 2r. Two tasks can each fit small independent experts while violating that shared-decomposition condition. The [second mathematical audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/math_capacity_round2.md) gives both constructive and impossible examples. These are mathematical conditions, not measured natural-language structure.

Serial residual computation is (I+E_d)(I+C). Its cross term E_d C looks like an additional interaction, but if I+C is invertible then E_d(I+C) can be absorbed into a private map without increasing its rank. Serial and parallel can therefore express the same function class in this setting. This rejects the claim that a cross term alone necessarily increases capacity; it leaves nonlinear composition and finite optimization benefits open. A [nonlinear example](capacity_mathematics.md) explains why an invertible common map can still change a limited expert family, and why depth and reuse remain separate explanations.

Even equal function families can have different update dynamics. In a scalar squared-error example with all experts fixed, the same common update reduces the source loss from 0.5 to 0.405 in both architectures. The old-task loss falls to 0.405 in parallel but rises to 0.605 in serial. This is a counterexample, not a natural-text result: equal representability does not ensure equal retention along an update. The [worked calculation](capacity_mathematics.md) separates this dynamic bridge. Here the source through-expert gradient is zero, so full/stopped directions coincide while old-task responses still differ through forward dependence. A gradient-direction probe cannot replace the architecture comparison.

The actual SwiGLU serial condition gives the expert z+C(z), their sum rather than two separately available inputs. The residual supplies a direct z path but does not guarantee invertibility or information preservation. Parallel produces C(z)+E_d(z), serial C(z)+E_d(z+C(z)), both inside the same post-attention residual. Serial changes the expert input and the gradient received by C. Equal parameter counts and nominal FFN multiplies do not imply equal depth, optimization or latency.

Every arm already shares embeddings, attention and norms, and attention already precedes the expert. The treatment is the additional explicit common FFN and its connection, not the presence versus absence of all common processing. Private-only is not fully independent learning.

![Common/specialized computation and fixed training exposure](figures/capacity_design.png)

The diagram shows frozen computation and planned training exposure, not a capacity result. Its upper panels isolate the added serial input path; the lower panel distinguishes common and per-expert exposure histories. See [figure provenance and counts](evidence/capacity_design.json).

## Prior work and the present question

[DEMix](https://aclanthology.org/2022.naacl-main.407.pdf) adapts language models by freezing old experts and the shared trunk while adding new experts, increasing capacity. [Lifelong-MoE](https://proceedings.mlr.press/v202/chen23aq/chen23aq.pdf) freezes old experts during expansion while shared computation continues to train with distillation. Frozen experts therefore do not imply a frozen old-domain computation.

[A fixed-capacity MoE continual-pretraining study](https://arxiv.org/html/2503.05029v2) also evaluates shared experts, but changes sharing, expert granularity and active expert count together. Those results do not replace the present finite shared-path rollback or same-forward gradient control. The [primary-source audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/continual_moe_primary_audit.md) records matching details and Unknown items; this is not a novelty claim.

## What the data task looks like

The task is token-by-token continuation of real scientific text. After the illustrated mathematics record's first 32 tokens, its observed continuation is “the critical Sobolev space H”; the biology example continues “in our model. We did this by”. The [four-domain examples](evidence/capacity_task_examples.json) preserve complete prefixes, archive/line identities, token hashes and the fixed first-record selection rule. They were not selected using model outcomes.

These examples identify inputs and supervision, not common features. Whether C reuses grammar, terminology or reasoning patterns requires model evidence. Actual targets are available during training, so predicting update compatibility from the prefix is no longer a prerequisite for learning allocation.

## Acquisition, retention and resource controls

The six conditions form one comparison family. The common_parallel and common_serial arms use a common width of 256 and a private width of 384, with four experts per layer. private_active gives each expert a width of 640 to match the active FFN budget; private_total gives each a width of 448 to match total FFN parameters. The Dense references use widths of 640 and 1792. Both resource controls are necessary because a private-only architecture cannot simultaneously match total and active budgets at a fixed expert count.

common_parallel and private_active have matched initial functions: identical common channels are copied into each private expert's gate/up/down tensors. Their subsequent distinction is whether these channels remain tied across domains. Serial starts from identical C/E tensors but a different forward function. Every arm uses additive domain embeddings, so Dense receives the same domain information that the expert models also use for routing. Known domain identity remains privileged information; learned routing is not tested.

Each trajectory starts with 512 mixed-domain updates, followed by four sequential domain phases of 1024 updates each, without later old-domain replay. Each update uses 8192 valid targets, for a total of 37,748,736 exposures. The earlier shorter draft was expanded before training to reduce the chance of confusing initial undertraining with insufficient capacity. The larger budget still does not establish convergence or saturation.

Shared C participates in all 37,748,736 targets and 4608 updates; each private expert participates in 9,437,184 targets and 1536 updates. During mixed updates, a private expert processes only its domain's quarter of the batch. Their AdamW states and decay histories also differ. The comparison therefore measures finite-budget efficiency of the shared training scheme as a whole; it does not separately identify storage reuse, cross-domain data pooling and update history.

The mixed stage exposes the model to all domains; later phases provide concentrated sequential learning. Each domain contains 4,194,304 selected training target positions and receives 9,437,184 exposures, equivalent to 2.25 traversals. Repeated exposure to the same data does not add independent training data. Four domains with four experts also do not test slot exhaustion.

All four dev domains are evaluated throughout, producing a domain-by-stage loss matrix. Loss reduction during a domain's own phase measures acquisition; later loss minus its own phase-end loss measures signed forgetting, retaining negative values as improvement. Test is opened only at the fixed final endpoint. Two blocks pair seeds with forward/reverse domain orders; comparisons are matched within each block, but seed and order effects cannot be independently identified.

## Finite rollback connects shared updates to old-domain loss

An unselected expert must retain both weights and AdamW state. Zero gradients alone are insufficient because decay or momentum can still move parameters. The implementation uses `grad=None` and verifies exact phase-boundary hashes. This guard must pass before attributing old-domain loss changes to shared parameters.

Split shared parameters into explicit common FFNs C and the remaining trunk T, including tied embeddings/output, domain embeddings, attention and norms. For a domain that has completed its own specialized phase, keep its expert and dev records fixed. Evaluate L00 (old C, old T), L10 (new C, old T), L01 (old C, new T), and L11 (new C, new T).

The four values distinguish harmful common drift, beneficial common changes offset by larger trunk harm, and interactions. Preserve all losses and the interaction before reporting the symmetric two-component allocation. Its sum equals the observed change by algebra; this is not an empirical discovery. Mixed checkpoints are real finite parameter interventions, not necessarily reachable optimization trajectories or unique semantic explanations.

A common update trained on another domain that improves the old domain would support bounded beneficial parameter transfer. It would not prove universal language knowledge. C can itself use the domain embedding and behave conditionally; shared parameter storage is not functional domain invariance.

## What same-forward intervention and expert swaps add

The second diagnostic preserves the forward computation of one trained serial model and forms two common-update directions at layer 4: ordinary backpropagation, or a control that stops the common-to-expert input gradient. Each negative gradient is separately normalized and applied at three fixed finite norms. All other parameters stay fixed. Both training source panels and all four DEV domains are reported, without selecting a layer, scale or panel by outcomes.

This identifies finite effects of two normalized directions, not an additive contribution of the removed path or a replay of AdamW history. On the panel that generated it, the full gradient is locally the steepest descent direction by definition. The undetermined effects concern old domains and the cost of retaining their knowledge while learning the source. The two checkpoints also have different seed/order combinations; they are not independent replications of the same task state.

The third diagnostic sends every domain through each of four expert banks at the final checkpoint, producing a complete 4×4 loss matrix. Text and true-domain embeddings remain fixed; only the expert route at every layer changes. Shared parameters stay fixed, while downstream shared activations may change. The intervention therefore measures expert-chain matching within the existing shared computation.

Mean off-diagonal loss minus mean diagonal loss measures matching advantage. A complete uniformly weighted matrix cancels additive domain difficulty and additive general expert quality. We still retain every cell and each domain's best expert. A larger matching advantage across arms may simply mean worse mismatched routes, so it must be read alongside absolute matched loss and retention. A positive average supports functional matching on these DEV records; it neither guarantees correct matching for every domain nor identifies independently stored semantic knowledge. The [derivation](capacity_mathematics.md) states the cancellation conditions.

## Actual resource accounting

![FFN and whole-model parameter budgets](figures/capacity_resource_budget.png)

These are actual frozen-implementation counts, not training quality or throughput. Both common arms and dense_total each store 51,484,928 parameters. Each common arm uses 35.71% of the active FFN parameters in dense_total, or 86.25% when the shared trunk is included in the active-parameter proxy. The tied vocabulary matrix accounts for 75.55% of total storage in these models. Relative to private_active, each common arm saves 30% in FFN storage and 8.40% in whole-model storage. See the [count table](evidence/capacity_budget_counts.json) and [third audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/gradient_coupling_round3.md).

## How outcomes inform the next question

If acquisition is weak, inspect training curves and resource controls before diagnosing forgetting. If own-domain learning succeeds but later losses rise, rollback locates the shared path. If serial beats parallel, the maximum claim is a benefit of the whole nonlinear computation under this budget; effective depth and optimization remain rivals. If only the larger-total private_active succeeds, the tested sharing compression is challenged. Inconsistent or reversed outcomes remain informative.

The three readouts need joint interpretation:

| Possible pattern | Supported bounded interpretation | Remaining bridge |
|---|---|---|
| Serial beats parallel; the full-gradient direction also helps old domains more | Architecture performance is compatible with a local direction effect | That path caused the trajectory advantage; other layers, times and the optimizer remain unisolated |
| Serial beats parallel; the direction probe is neutral or harmful | The tested layer/state limits that path explanation | Depth, representation changes or other training states may still explain the architecture outcome |
| Matching advantage S increases while matched loss worsens | The assigned-matching loss contrast increases | Useful capacity has increased; S may rise only because mismatched routes worsen |
| Own-phase learning is good, followed by deterioration | C/T rollback locates which shared parameter changes transmit the loss | Constraining them improves a full trajectory, and at what source-learning cost |

These are prospective interpretation branches, not observed patterns. No row is selected as a conclusion without actual results.

The acceptable gap to larger Dense is researcher-owned and currently Unknown. Report continuous gaps, not a post-hoc equivalence threshold. The approximately 38.9M parameters in the vocabulary embedding dominate these small models. A reduction in active FFN width must not be presented as an equal reduction in whole-model compute. Actual parameter counts, memory and throughput will be reported alongside losses.

The next mechanism comparison depends on the strongest unresolved rival explanation. A serial benefit may require controls for depth and parameter tying across experts. If common drift dominates, a later comparison may test private acquisition with common computation held fixed. These are decision branches, not an automatically approved sequence of new projects.

## Current execution evidence

Job `pt-uasnh61d` was submitted at 2026-10-03T04:52:37Z on one 8×RTX5090 SPOT allocation. Data preparation, independent record checks, seven CPU contract tests, tiny six-arm Smoke and synthetic rollback checks are complete. At 06:39 UTC, the platform state was STARTING and its worker was Pending; no pod log or formal training metric existed. Exact GPU Smoke and formal training trajectories await worker startup. There are no new natural-text training conclusions yet.

The [read-only mechanism summary](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/analysis/mechanism_summary/reading.md) separates complete, partial, not-run and invalid states for eight rollbacks, eight expert matrices and two direction probes. The refreshed collection at 06:39 UTC still has 18 NOT_RUN records and no numeric outcomes; the training summary has 0 of 12 completed trajectories. It verifies output hashes and signatures without rehashing checkpoint/data bytes or issuing a scientific judgment.

[Exact Protocol](protocol.md), [execution certificate](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/execution_certificate.md), [current summary](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/analysis/training_summary/summary.json), [audit notes](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/), and [process log](research_process.md) preserve evidence and limitations.
