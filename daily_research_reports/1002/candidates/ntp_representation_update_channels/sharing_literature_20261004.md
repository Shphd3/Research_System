# Sharing or separate learning: how 17 primary papers constrain the current interpretation

2026-10-04. [中文](sharing_literature_20261004_cn.md) · [Stage report](sharing_routing_report.md) · [33B results](probe_33b_summary.md). This is a targeted reading, not an exhaustive review. The [source index](evidence/sharing_literature_20261004_sources.json) records versions and sections. Adopting an interpretation or check below does not authorize another algorithm, arm or training job.

**Sharing cannot be decided from task similarity, gradient angles or specialization alone. Acquisition, later retention and resource costs must be evaluated together.** These papers address different parts of that relationship; none answers the whole question under this project's conditions.

## 1. Shared representations: similarity is not the only useful condition

This literature review checks an inference: whether task differences or gradient conflict alone justify parameter separation. Identify what each paper shares first—backbone weights, an always-active expert or a frozen function used by new modules—then identify changed connections, assignment or learning status. Frozen-update selection is not those training ablations. The review retains versions, sections and values checked on October 4, without claiming later coverage; external configuration-specific findings cannot supply this project's unrun results.

| Primary source and reading scope | Method, information and cost conditions | Use and boundary here |
|---|---|---|
| [Maurer, Pontil and Romera-Paredes, 2016](https://jmlr.org/papers/volume17/15-242/15-242.pdf), Sections 2–3 | Generalization bounds for shared features and task mappings depend on tasks, samples and function classes; tasks and supervised targets are available. | Supports conditional statistical pooling. A bound does not establish this AdamW trajectory, compute savings or retention. |
| [Tripuraneni, Jordan and Jin, 2020](https://proceedings.nips.cc/paper_files/paper/2020/file/59587bffec1c7846f3e34230141556ae-Paper.pdf), Sections 2–3 | Learn shared features, then a new task mapping; assumptions include common input distributions, realizability, regularity and task coverage of features. | Diversity can identify shared features; it is not gradient conflict. Our four domains have not been shown to satisfy the assumptions. |

**AI synthesis:** our earlier finite-sample quadratic model describes noisy separate estimation. These papers raise a distinct issue: which representation is shared, and whether tasks provide complementary constraints. Repeated token exposures are not independent samples; no applicable numerical theory bound has been estimated here.

## 2. Local help and grouped training are separated by a learning trajectory

| Primary source and reading scope | Computation and additional information/work | Use here |
|---|---|---|
| [Standley et al., 2020](https://proceedings.mlr.press/v119/standley20a/standley20a.pdf), setup and grouping experiments | Empirical joint training of known supervised tasks; relations change with data and capacity. Group search requires repeated training. | Measure combinations at specified resources; domain names do not rank our groups. |
| [Fifty et al., 2021](https://proceedings.neurips.cc/paper/2021/file/e77910ebb93b511588557806310f78f1-Paper.pdf), Sections 4, 4.3 and 6 | Update shared parameters with heads fixed, read other task losses, aggregate during training, then retrain groups. Requires task losses and extra evaluation. | Adopt separate validation of local affinity and final training. Counterexamples limit unconditional inference between them. |
| [Yu et al., 2020, PCGrad](https://proceedings.neurips.cc/paper_files/paper/2020/file/3fe78a8acf5fda99de95303940a2420c-Paper.pdf), method and theory | Projects conflicting task gradients; the analysis also involves domination and curvature. Per-task gradients add work. | Angles are diagnostics, not a complete sharing rule. Keep actual finite CE; do not add this optimizer to frozen arms. |
| [Sun et al., 2020, AdaShare](https://proceedings.neurips.cc/paper/2020/file/634841a6831464b64c072c8510c7f35c-Paper.pdf), Section 3 | Learns task-conditioned block execution with Gumbel-Softmax, sharing and sparsity constraints; policy search costs training. | Allocation can be learned, but known tasks and supervision do not directly provide a domain-free NTP router. No implementation adoption now. |

**AI synthesis:** a fixed checkpoint and action bank cannot settle whether allocating training data creates useful future differences. The existing capacity study addresses trajectories under known domains. It still does not show how an input-conditioned router discovers useful groups; that requires a separately proposed comparison.

## 3. Retention: which objects must remain fixed?

| Primary source and reading scope | Mechanism and cost | Implication for our checks |
|---|---|---|
| [Kirkpatrick et al., 2017, EWC](https://arxiv.org/html/1612.00796v2), method and discussion | A diagonal-Fisher quadratic penalty uses old-task statistics and additional state. This softly constrains parameters rather than fixing predictions. | Small movement is not no forgetting, and approximate Fisher is not exact functional importance. No new regularization arm. |
| [Rusu et al., 2016, Progressive Neural Networks](https://arxiv.org/html/1606.04671v4), Section 2 and Appendix B | Old columns remain frozen while new columns read old features; task-column selection and growing storage are required. | Retention guarantees concern the complete old path. This does not establish superiority at fixed total resources. |
| [Mallya and Lazebnik, 2018, PackNet](https://arxiv.org/html/1711.05769v2), Section 3 | Prune/retrain, freeze allocated weights and use task masks; biases and normalization states are also controlled. Capacity is finite; unstructured sparsity need not save wall time. | Inspect all prediction-relevant states and selection, not expert hashes alone. Count task information and pruning work. |

**AI synthesis:** preserving an unselected expert and its AdamW state is an implementation requirement. With a changing shared trunk, it does not guarantee unchanged old-domain predictions. The registered C/T rollback, expert swap and serial same-forward gradient diagnostics address different paths. All long-term mechanism results remain `NOT RUN`.

## 4. MoE evidence: shared-expert benefits depend on the training contract

| Primary source and reading scope | Computation and information | Supported use and transfer limit |
|---|---|---|
| [DeepSeekMoE, 2024](https://arxiv.org/html/2401.06066v1), Sections 3.2 and 4.4–4.5 | Always-active shared experts replace some routed activations; its matched-budget ablations improve most benchmarks. Removal establishes branch importance. | A worthwhile design candidate; importance does not establish universal semantic knowledge. |
| [OLMoE, 2024](https://arxiv.org/html/2409.02060v1), Section 4.1.3, Figure 6 | Shared experts are slightly worse in its matched active/total-parameter and FLOP ablation; reduced routing freedom is a proposed explanation. | Opposite outcomes under different conditions preclude a universal verdict. The explanation is not isolated causality. |
| [OpenMoE, 2024](https://arxiv.org/html/2402.01739v1), Section 4 | Studied routing depends strongly on token identity, emerges early and is weakly context dependent. Domain profiles can reflect lexical composition. | Domain preference is not learning utility. Retain lexical/history controls; do not generalize to every MoE. |
| [FlexOlmo, 2025](https://allenai.org/papers/flexolmo), Sections 3.3 and 4.3–4.4 | Freezes public experts and shared non-expert parameters, trains private experts independently and combines them. Router initialization uses an external domain embedder; router tuning is optional. | It combines frozen shared parameters with expert coordination; intermediate activations need not remain fixed. Count public pretraining, storage and tuning; it does not validate our mutable common path. |
| [Yoon et al., 2026, When Are Experts Misrouted?](https://arxiv.org/html/2605.07260v1), Sections 3, 5 and limitations; May 8 preprint | Equal-compute alternative routes receive post-hoc target-CE labels. Verified reasoning traces and extra candidate forwards train a last-layer router with other weights frozen. | A bounded existence check, not deployable target access or established scalable pretraining. Our fixed global-update-bank failure does not cover all native expert routing. |

**AI synthesis:** an always-active expert, a jointly updated shared trunk and a frozen public feature provider are different objects. Their compute, update exposure and retention conditions cannot be collapsed into one conclusion because all are called shared.

## 5. How native routing learns: computation outside the fixed-bank test

| Primary source and reading scope | Computation and training conditions | Use or retained boundary |
|---|---|---|
| [Fedus, Zoph and Shazeer, 2022, Switch Transformers](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf), Sections 2.1–2.4 | Top-1 retains a softmax gate amplitude, allowing task gradients into routing. Balancing, overflow and communication matter; main experiments use T5-style denoising. | Unselected-expert utility labels are not required. This is not our NTP contract or an optimal-allocation guarantee. |
| [Zhou et al., 2022, Expert Choice Routing](https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf), Sections 3.2–3.3, 4.1 and 6 | Each expert selects a fixed token count; tokens receive variable expert counts. Allocation is coupled by capacity. The paper explicitly notes future-token access in its implementation. | Do not directly transfer it to causal NTP. Specify active compute, batch capacity and available information together. |
| [Chi et al., 2022, X-MoE](https://proceedings.neurips.cc/paper_files/paper/2022/file/df4f371f1f89ec8ba5014b3310578048-Paper-Conference.pdf), Sections 2–4.5 | Learns a reduced routing projection, normalization and temperature while experts read full hidden inputs; also studies freezing during fine-tuning. Multilingual MLM/downstream ablations supply evidence. | Already cited in earlier stage material; controls and derivation were reread. Combined results do not establish current PCA/SAE sufficiency. |

**Computational explanation, not a new experiment.** For a top-1 gate retaining its amplitude, fix input \(h\), expert outputs and selected expert \(i\). Let logits be \(v_j\), probabilities \(p_j=\operatorname{softmax}(v)_j\), module output \(m=p_iE_i(h)\), and task gradient \(g=\nabla_m\ell\). Within a region of unchanged selection and no overflow,

\[
\frac{\partial\ell}{\partial v_j}
=p_i(\mathbf1_{j=i}-p_j)\langle g,E_i(h)\rangle.
\]

One executed expert can therefore provide routing gradients. These are not counterfactual evaluations or an optimality guarantee. Renormalizing the single selected weight to 1 removes this task-gradient path. Training targets do not violate inference-time causality. [Three local checks](evidence/native_router_gradient_check_20261004.json) verify the chain rule, with no LM data or empirical support.

**AI review:** we cannot promote the gate gradient's membership in the routing-vector span into a theorem of inevitable full representation collapse. Directly updating only the first coordinate does not erase the second; other paths also contribute gradients. Models update parameters, so the earlier network's Jacobian also determines hidden-state changes: a gradient with respect to a hidden state is not its next displacement. These stronger inferences remain distinct from X-MoE's trend diagnostics. Here routing compression may affect both estimation and backward learning paths; the frozen ridge test cannot measure the latter.

This clarifies the bridge: current selection exploits existing differences, whereas joint learning changes those differences and the states seen by routing. Future gate proposals must specify amplitudes, causal information and capacity constraints. This reading adds no implementation or training run.

## 6. What changed, and which evidence decides next?

Our own new observation is that all 92 pooled cross-source conditions beat global usage-matched random allocation yet lose to the FIT-selected fixed common action. This supports matching information, not adoption over that fixed baseline. The reading clarifies why action choice, representation estimation, learning allocation and old-function protection require separate comparisons.

| Question component | Current evidence state | Next evidence within the contract; branches |
|---|---|---|
| Adopt the current fixed-state selector? | **Not supported for this operationalization:** actual finite CE is worse than the strong fixed action; not a rejection of all routers. | Analysis complete; preserve the negative outcome and do not rerun the old 80 rows because of it. Practical utility threshold remains Unknown. |
| Does shared/private learning improve acquisition and retention? | **Insufficient:** implementation repair produces no training outcome. | Exact GPU Smoke first, then six arms × two complete blocks. Under [Protocol Section 15](protocol.md), corresponding benefit in both blocks with valid guards is exploratory support; no benefit or the retention harm the hypothesis aimed to avoid is non-support. Missing endpoints/guards, inconsistent blocks or unresolved strong rivals remain insufficient. Report domain/resource tradeoffs separately. |
| Is any benefit due to common reuse, interface change or another path? | **Insufficient:** registered interventions have not run. | Read rollback, swaps and same-forward diagnostics separately; structure, unchanged parameters or final averages alone cannot confirm mechanism. |
| How can allocation be learned from input? | **No direct project result.** | **AI suggestion:** propose a learned-router comparison after researcher prioritization. No new arm, model expansion or submission now. |

A working principle for researcher consideration is to pool reliably estimable common learning, separate exploitable differences when data support them, and specify which old computations may keep changing. This reconnects evidence to the original question; it is not a validated threshold or approved design. Anchor, Protocol and unconfirmed scientific states retain their authority.
