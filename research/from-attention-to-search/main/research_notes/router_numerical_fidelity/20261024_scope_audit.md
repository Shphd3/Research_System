# Router numerical fidelity: R00 source and calibration audit

[Chinese](20261024_scope_audit_cn.md) · [Owning Anchor](../../problem_anchors/10_optimizer_learning_rate_mechanism/10_03_router_numerical_update_fidelity_anchor.md) · [Small provenance manifest](provenance.json)

**Outcome:** the literature and local source support a bounded numerical rival worth one natural-state replay. They do not establish that numerical error explains an existing MoE result. R00 is literature, derivation and operator calibration; the natural empirical comparison is NOT RUN. AI recommends placing the question as independent A10_03, without a new A18 research line.

## Purpose, hypothesis and alternative

The researcher asks whether numerical analysis can advance the MoE Router work. The useful scientific question is whether a numerical derivative discrepancy changes the finite effect of a learning update. A large gradient residual alone answers only an implementation question.

The proposed explanation is loss of a small gradient component that survives the complete gate and optimizer. The live alternative is absence of sensitive natural states, normalization cancellation, or negligible finite effect. Both outcomes must remain possible.

The supplied reading correctly distinguishes mathematical gradients, computed gradients and actual parameter updates. Four corrections make its suggested experiment decisive:

1. Zero-sum applies to shift-invariant loss components. A direct logit z-loss intentionally need not satisfy it.
2. The common expert-weight row is not a common input feature. Even exact zero-sum gradients do not force AdamW updates to have zero row mean.
3. Hard Top-K selection, selected-weight normalization and auxiliary losses must be traced separately. A forward gate choice can stay unchanged while its derivative changes.
4. Measure the full update at the same inherited optimizer state, then the finite task-loss effect. Zero moments are useful calibration, but cannot substitute for a trained optimizer history.

## Literature and placement

The full eight sections, equations, table and figure descriptions of [A Fix for Softmax and Cross-Entropy](https://jonbarron.info/softmaxfix/) were read. It supplies stable arithmetic and bounded algorithmic-task evidence; its conclusion explicitly limits the prevalence of its extreme regimes in ordinary large-scale training. It provides motivation, not a MoE result.

[Switch Transformers §2.4](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf) already uses selective Router precision. [ST-MoE §3.3–3.4](https://arxiv.org/html/2202.08906v2) adds numerical-stability evidence and z-loss. Therefore casting a Router to FP32, or proposing z-loss, is not a new contribution. The candidate contribution would be a demonstrated distinction between genuine learning interaction and a numerically induced finite update effect in the owned model.

The current registry had 149 owners in 13 populated research lines before this addition; numbering extends through A17. Every registered title was reviewed and a targeted numerical-term scan covered their canonical text. Relevant full designs were inspected: A05_04_02, A10_01/A10_02 and A15_24_01, plus the A16 line and its ownership boundaries. This scoped search found no registered owner of the proposed finite numerical-gradient comparison.

| Existing owner | Relation | Placement decision |
|---|---|---|
| A05_04_02 | Common hidden components can create different expert advantages; it explicitly restricts its original sparse top-1 toy setting | Related mechanism; preserve its evidence and scope |
| A10_01 / A10_02 | Common/high-gain directions, update scale and optimizer-dependent stability | Place independent sibling A10_03 here; do not make it a new proof of those hypotheses |
| A15_24_01 | Shows why changed clipping does not imply proportional changed AdamW updates | Reuse the fixed-state update logic, not its experiment authorization |
| A16 | Separates task and effective load-control gradient paths | Reuse component separation; numerical fidelity is a different decision |
| A17 | Shared learning/retention consequences | Potential downstream use, not required for the first replay |

A10 can contain this bounded optimization question. A new line would become justified only if independently activated questions outgrow this scope. No existing Focus, priority, mechanism verdict or historical result is reset.

## Source computation and data

Two read-only source files were inspected:

- Clean scaffold routing: /data/250010109/Research_System/Projects/decommon-router-training/src/decommon_router/model/moe.py, lines 244–259; softmax explicitly computes FP32, then Top-K, with renormalization only when top_k is greater than one.
- Original execution source: /data/250010109/MoE_Router/src/model/qwen3_moe/myqwen.py, lines 200–207; softmax also explicitly computes FP32, but enabled renormalization includes top-1.

No checkpoint or run config was loaded, so neither file is asserted to be the source of today's trained model. The source hashes are in provenance.json.

The calibration AST-compiles exactly four routing statements: softmax, Top-K, conditional renormalization and output casting. It does not execute either full MoE block. The comparator changes only softmax to the paper's margin/softplus arithmetic, or to a float64 reference with float64 output. The reference begins with the same exactly representable synthetic logits; it does not restore information lost before the logits.

Inputs are five fixed vectors [a,0,-1], for a in {1,5,12,18,24}, with strict expert-score ordering. Each selected expert has a fixed scalar output/cotangent from [1,0.3,-0.2]. The local loss is the weighted sum of those constants. Each of two source kernels is evaluated at top-1 and top-2 with normalization enabled, under native FP32, stable FP32 and FP64 reference: 60 rows.

This local cotangent is a derivative calibration, not a natural LM objective. Native and stable calibration use FP32 inputs/outputs; a production bf16 output cast and low-precision matrix multiplication remain outside this coverage. There is no train/dev/confirmation split, statistical fitting, dataset asset, checkpoint or GPU use. Every case is exposed calibration data. The five cases receive equal weight in the reported means; they are not a sample from natural tokens.

## Calibration results and counterexamples

Relative logit-gradient error is the Euclidean distance to the FP64 reference divided by its gradient norm. A zero reference gradient produces NA, not an artificial finite ratio.

| Mathematical gate path | Mean native relative error | Mean stable relative error | Interpretation within the fixed grid |
|---|---:|---:|---|
| Clean top-1, no selected-weight renormalization | 0.316675646 | 2.71437e-7 | Native arithmetic can lose the dominant derivative |
| Clean top-2, renormalized | 6.64441e-8 | 9.58140e-8 | Both are close to reference; no improvement established |
| Original top-1, renormalized | NA | NA | All three gradients are zero |
| Original top-2, renormalized | 6.64441e-8 | 9.58140e-8 | Same cancellation boundary as clean top-2 |

All three variants select the same experts in every case. Native/stable gate weights agree within the prefixed eight-FP32-epsilon tolerance. FP64 is a higher-precision comparator, not exact arithmetic. No confidence interval applies to this deterministic constructed grid.

The normalized top-1 counterexample is exact away from selection boundaries: its only selected weight is p/p=1, so its task-path Router derivative is zero. For normalized top-2, the full softmax denominator cancels algebraically; this helps explain the measured accuracy but does not prove numerical safety for every tensor, cast or auxiliary objective.

For a worked positive case, use logits [18,0,-1], clean top-1, input h=[1,0], and three rows W_e=[z_e,1]. The second weight coordinate is identical across experts, so it should cancel from the input derivative. Native has gradient sum -2.08328e-8 and input derivative [5.60280e-9,-2.08328e-8]; stable gives [3.80593e-7,-4.44089e-16]. A cloned two-coordinate AdamW step, with zero moments, learning rate 0.001, epsilon 1e-8 and no weight decay, moves the second coordinate by +0.000675670 under native and approximately +4.44e-11 under stable. This verifies a constructed arithmetic-to-update path. It is not a model-training run or evidence that a natural state has this geometry/history.

## Evidence, failures and proposed next decision

Execution root: /data/250010109/MoE_Router/experiments/20261024_router_numerical_fidelity. The sole code owner is calibrate.py there; spec.json freezes the cases, results.json holds the 60 rows, and manifest.json binds source/code/config/output hashes and extracted kernels. Small provenance.json here records those identities; raw outputs remain execution-side.

The first attempt stopped before producing calibration results: torch.optim imported an installed ONNX/protobuf combination with incompatible generated descriptors. A process-local PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python setting allowed the unchanged numerical script to complete. No package was installed or modified. This environment failure is not a scientific outcome.

**Completed:** source/derivation audit and all 60 calibration rows, with matching-expert and forward-close guards. **NOT RUN:** natural margins, actual model/optimizer replay, finite task-loss difference D, route switches or retraining. The original model/data/optimizer identity and a meaningful error floor must be bound before the natural comparison.

The next AI proposal is one frozen-state replay of the complete objective and inherited optimizer, using a disjoint probe batch. Preserve forward behavior for a backward-only comparison, and separate forward quantization/near-tie effects. Compare finite loss differences with independent no-op/replay uncertainty. If no resolvable finite effect remains, park this explanation rather than expanding a precision sweep.

## Rules read for this round

The current System and project AGENTS, PROJECTS and project roadmap were read together with the applicable rules for skill routing, writing, mathematics, the research exploration kernel, training reuse/observability, analysis review, project access, assets, execution and Anchor synchronization. The operative execution sections and asset lifecycle were read; unrelated historical job authorizations are not imported.

The tracked-only entrypoint check reports one pre-existing untracked diffusion literature entry. The working-tree check passes all 90 entrypoints and reports that pending tracking explicitly. These are navigation results, not scientific or run approval.
