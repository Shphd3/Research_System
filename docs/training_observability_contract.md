# Model Training Observability And Comparison Contract

Effective for new training implementations and runs from 2026-09-13 onward.
Historical runs are not retroactively made comparable by this document.

This contract defines engineering evidence and comparison coordinates. It does
not approve a run or determine a scientific verdict.

## 1. Required TensorBoard Record

Every training run writes TensorBoard event files under
`<run_root>/tensorboard/`. Only the designated logging rank writes events, after
metrics and token counts have been reduced across the data-parallel group.

The primary task quantity is:

| TensorBoard tag | Definition |
| --- | --- |
| `tokens/train_lm_loss` | Globally token-weighted next-token cross-entropy before adding regularization, in natural-log units per valid prediction token. Its TensorBoard `global_step` is cumulative valid prediction tokens. |

Record the same value for update-level debugging as `updates/train_lm_loss`,
with optimizer update as TensorBoard `global_step`.

Regularization and auxiliary losses are conditional on the actual objective;
there is no repository-wide mandatory named component. For every component
that is enabled or decision-relevant in a comparison, register a stable
`<name>` in the Protocol and record:

- `tokens/loss_component/<name>_raw` and
  `tokens/loss_component/<name>_weighted`, against cumulative valid prediction
  tokens;
- matching `updates/loss_component/<name>_raw` and
  `updates/loss_component/<name>_weighted`, against optimizer update;
- its coefficient, eligible positions or samples, reduction denominator, and
  aggregation over layers or modules.

Examples may include router regularization, load balancing, reconstruction, or
distillation, but none is imposed on a model that does not define it.

Also record enough information to interpret them:

- `tokens/train_total_loss`: the actual scalar objective used for backpropagation;
- `updates/learning_rate`;
- `progress/tokens_seen`, `progress/optimizer_step`, and
  `progress/effective_tokens_per_update`;
- the component registry and exact reduction definitions in the frozen config
  or Protocol.

Within one comparison family, if a treatment enables a component and a control
sets its coefficient to zero, keep the same component tags in the control when
the raw term remains well-defined and practical to compute. Otherwise record
`NOT_APPLICABLE` and the reason; never invent a metric for an unrelated model.

Log `progress/tokens_seen` and `progress/effective_tokens_per_update` against
optimizer update; log `progress/optimizer_step` against cumulative valid
prediction tokens. This makes the mapping between the two coordinates explicit.

Do not compare a per-rank mean with a global token-weighted mean. For language
model loss at update $u$:

$$
L_{\mathrm{LM},u} =
\frac{\sum_{r,m,t} \ell_{r,m,t}\,\mathbf{1}[y_{r,m,t}\neq\mathrm{ignore}]}
{\sum_{r,m,t}\mathbf{1}[y_{r,m,t}\neq\mathrm{ignore}]}.
$$

The sums cover data-parallel ranks $r$, accumulation microbatches $m$, and
valid prediction positions $t$. Count each example once: tensor- or
pipeline-parallel replicas do not create additional training tokens.

On resume, restore both cumulative token count and optimizer update. Prevent
overlapping or conflicting TensorBoard steps by continuing the existing event
series correctly or starting an explicitly named resume segment.

## 2. Canonical Comparison Coordinate

The primary x-axis for model-quality training curves is **cumulative valid
prediction tokens**. This is the number of non-ignored target tokens actually
processed by completed gradient-accumulation windows, accumulated once across
the data-parallel group. If an optimizer update is skipped, record the skip and
follow the Protocol-frozen counting rule; never silently change the coordinate
semantics between runs.

The optimizer update is a required secondary axis, but it is a valid primary
comparison axis only when every compared run has exactly the same effective
tokens per update throughout training. In the common fixed-length case:

$$
\text{tokens/update} =
\text{microbatch sequences/GPU}
\times \text{gradient accumulation}
\times \text{data-parallel size}
\times \text{valid prediction tokens/sequence}.
$$

For padded or packed batches, use the observed non-ignored target count rather
than this nominal product.

Changing from four to eight GPUs is allowed without changing the scientific
coordinate only when the effective global batch, token order, loss reduction,
and optimizer semantics remain fixed. Adjust microbatch size or gradient
accumulation to preserve the effective global batch.

A token axis aligns data exposure; it does not erase the optimization effect of
a different global batch. Therefore:

- strict method comparisons keep effective global batch fixed;
- a run with a different global batch is a non-matched optimization condition
  unless batch size is itself the registered variable;
- such a run may be shown on the same token axis, but it cannot by itself support
  a clean method-effect claim.

## 3. Alignment Of Schedules And Measurements

For comparisons that may use different GPU counts or accumulation factors:

1. Freeze the total token budget and common evaluation-token checkpoints in the
   Protocol.
2. Express warmup, decay, regularization schedules, evaluation, checkpointing,
   and stopping points in tokens. If software accepts only updates, convert from
   tokens using the run's effective tokens per update and record the rounding.
3. Compare validation metrics at the same reached token checkpoints, on the
   same frozen validation data and reduction rule.
4. Use the same smoothing method and window unit for displayed curves. Preserve
   unsmoothed scalar events.
5. Use wall-clock time only for throughput or systems efficiency, never as the
   model-quality fairness axis.

The Protocol must freeze: tokenizer and data view, model inputs and targets,
global batch, token-count rule, loss denominators, optimizer and schedules,
comparison checkpoints, TensorBoard log directory, and required tag names.

## 4. Preflight And Eligibility

Before a full run, a bounded smoke must prove that:

- TensorBoard event files are created in the declared run directory;
- the primary loss and every Protocol-required component tag contain finite
  values;
- `tokens_seen` is monotonic and equals an independent valid-target count for at
  least one optimizer update;
- only completed accumulation windows advance the primary token coordinate,
  and skipped optimizer updates are visible;
- resume preserves both coordinates without conflicting event steps.

A missing required tag, an ambiguous component reduction, or a
wrong/non-monotonic token counter makes the affected cross-run loss-curve
comparison `INELIGIBLE` until repaired. It does not automatically invalidate
unrelated artifacts from the run.

## 5. Basis For This Convention

- [DeepSpeed batch configuration](https://www.deepspeed.ai/docs/config-json/)
  defines effective training batch as microbatch per GPU times gradient
  accumulation times GPU count, so optimizer-step equivalence depends on this
  product.
- [Megatron Core training examples](https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/training-examples.html)
  distinguish microbatch, global batch, and training iterations.
- [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)
  analyzes language-model loss using training-token and compute budgets, and
  matches schedule length to the token budget.
- [PyTorch TensorBoard documentation](https://docs.pytorch.org/docs/stable/tensorboard.html)
  provides scalar logging with an explicit `global_step`; this contract assigns
  that coordinate explicitly rather than relying on a framework default.
