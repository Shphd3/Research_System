# A06_04 Source Fragment: Routing Continuity, Feature Context, And Systems Cost

Status: adjacent source evidence from `Frandium/kv_cache`; this fragment does
not override the canonical `A06_04_01` functional verdict.

Source snapshot: `kv_cache/main@c189bd7ea773582b3f26b2e102c22d6628ee6a77`,
pulled locally on 2026-07-31 UTC.

## Provenance And Push Times

Git commits record author and committer times, not the time a branch was pushed.
The actual `main` push times below were therefore checked against GitHub's
public repository `PushEvent` records.

| Source update | Commit time | Confirmed `main` push time | Scope |
|---|---|---|---|
| `f46637d` (`FEATURE_CONTEXT_FROZEN.md`) | 2026-07-22 16:44:37 UTC+08 | 2026-07-22 08:44:41 UTC / 16:44:41 UTC+08 (`PushEvent` `15527281448`) | Feature-conditioned frozen-input MoE report and code update |
| `c189bd7` (`moe_0731.md` and phase-3 patent proposal) | 2026-07-30 20:02:33 UTC+08 | 2026-07-30 12:02:38 UTC / 20:02:38 UTC+08 (`PushEvent` `16216685384`) | Attention-Mean routing results, analytic load-cost model, figures, and systems proposal |

Only `c189bd7` was new in the 2026-07-31 local fast-forward from `d9886b1`;
`f46637d` was already in the local history but is the latest direct update to
the feature-context specialization report.

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| Routing continuity | Neighboring tokens keep the same routed expert more often | expert switch/stay rate | Can reduce expert-weight movement or loading | Expert function is useful |
| Feature-context input | A frozen contextual feature is added to the Router input while expert input stays unchanged | `FEATURE_CONTEXT_FROZEN.md` condition | Tests whether a contextual route signal changes one-run NLL | Stable expert ownership or causal specialization |
| Functional specialization | Different conditions stably prefer different expert functions under held-out loss | forced-expert utility and headroom | A06 terminal target | Route continuity, balanced load, or lower NLL alone |
| Systems cost \(C(S)\) | Communication and activated-compute penalty for executing expert set \(S\) | analytic load/compute latency model | Enters the functional Router objective | Measured end-to-end latency without a real implementation |

## Direct Results

### Attention-Mean Routing

The report routes from the causal mean of the previous 16 attention outputs;
the expert still receives the full post-attention residual. In one 28-layer,
approximately 1.917B-parameter top-1 MoE training comparison:

- measured expert switch rate falls from `81.84%` to `7.30%` and stay rate
  rises from `18.16%` to `92.70%`;
- expert-loading events fall from `23,471.5` to `2,120.2`, a `90.97%`
  reduction under the report's accounting;
- test loss changes from `3.1395` to `3.1920`, so the lower-switch method is
  worse on this loss;
- the eight-task zero-shot macro average changes from `0.4812` to `0.4787`,
  with four wins and four losses.

Under the report's no-prefetch, no-overlap analytic latency model, predicted
weight-loading overhead falls from `+180.29%` to `+16.08%` on H200, from
`+222.20%` to `+19.82%` on RTX 3090, from `+305.67%` to `+27.27%` on RTX 3080,
and from `+181.68%` to `+16.21%` on PPU. These are model-based estimates, not
measured end-to-end serving latency.

### Feature-Context-Frozen Routing

In one Qwen3-0.6B LoRA-MoE comparison with approximately 1,056,768 matched
trainable parameters, validation NLL is `3.46948` for standard routing and
`3.46535` for the feature-context condition, a difference of `-0.00413`.
Removing the feature gives `3.47317`, which is `+0.00782` worse than the
feature-context condition.

The report lacks the controls required for functional specialization: shuffled
feature ownership, a full forced-expert utility matrix, split-stable useful
expert identity, and multiple seeds. It is therefore a bounded routing-input
diagnostic.

### Systems Proposal

The phase-3 parameter-stationary memory-compute-domain document is an
architecture and patent proposal. It is useful for defining possible terms in
\(C(S)\), but it is not experiment evidence for expert utility, correctness, or
realized latency.

## Relation To A06_04

| Audit question | Answer |
|---|---|
| Affects the hypothesis? | Yes, narrowly: a contextual routing state can materially alter route continuity and may lower communication cost. |
| Affects the claim boundary? | Yes: lower switching and a small one-run NLL change must not be reported as functional specialization without held-out counterfactual expert utility. |
| Affects the next decision? | No direct change: the frozen CrossCodeEval final-layer test still fails stable positive headroom. A training-time selective-sharing test requires a separate human approval. |
| Recommendation | Retain as an A06_04 source fragment; do not create a Router or promote the patent proposal to evidence. |

## Source Map

- [`FEATURE_CONTEXT_FROZEN.md` at `f46637d`](https://github.com/Frandium/kv_cache/blob/f46637dbca00f71baafa29bffbd262782fc6ed95/main_specialization/FEATURE_CONTEXT_FROZEN.md)
- [`moe_0731.md` at `c189bd7`](https://github.com/Frandium/kv_cache/blob/c189bd7ea773582b3f26b2e102c22d6628ee6a77/main_swapmoe/docs/moe_0731.md)
- [phase-3 systems proposal at `c189bd7`](https://github.com/Frandium/kv_cache/blob/c189bd7ea773582b3f26b2e102c22d6628ee6a77/main_swapmoe/patents/phase3_parameter_stationary_memory_compute_domain_proposal.md)
- [GitHub repository events used for push-time verification](https://api.github.com/repos/Frandium/kv_cache/events?per_page=100)
- [Canonical local functional result](../../../../experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md)
