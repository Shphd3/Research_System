# From Retrieval Hits To Functional Utility

## Status

Working theme for the 2026-07-17 group meeting. This document is an
AI-proposed discussion surface, not an approved anchor or experiment Protocol.
No new run is authorized by this file.

## Proposed Meeting Theme

**From Retrieval Hits to Functional Utility: What Should a Long-Context Router
Optimize?**

One-sentence claim:

> A nominal one-million-token window is not usable context; a Router becomes
> useful only when its selected evidence preserves the ordinary prediction
> head's decision under a fixed compute budget.

This theme keeps long-context retrieval as the workload, while making the
research object precise: not whether information is somewhere in the context,
readable from a hidden state, or grouped by a feature label, but whether the
selected information has measurable downstream utility.

## Why This Theme Is Timely

Current systems advertise context windows at or above one million tokens, but
simple needle retrieval is not equivalent to multi-hop use, aggregation, or
non-literal retrieval. The external evidence motivates the workload; it does
not establish our mechanism:

- [Gemini long-context documentation](https://ai.google.dev/gemini-api/docs/long-context)
- [OpenAI GPT-4.1 announcement](https://openai.com/index/gpt-4-1/)
- [RULER](https://arxiv.org/abs/2404.06654)
- [NoLiMa](https://arxiv.org/abs/2502.05167)

User-supplied phenomenon:

> In agent-heavy workloads, many models can accept extremely long contexts,
> but far fewer can reliably use the relevant evidence inside them.

## Goal Audit

| Layer | Question | Current boundary |
|---|---|---|
| Workload | Can a model use necessary evidence dispersed through a long context? | Context length alone does not define difficulty. |
| Representation | Is the evidence encoded or transported into a usable state? | Readability does not prove use. |
| Prediction | Does the ordinary head causally depend on that evidence? | A11's earlier signal does not guarantee this. |
| Retrieval | Does a selector preserve prediction quality at matched budget? | Recall or attention mass alone is not functional utility. |
| MoE | Can a Router predict which expert or memory item is useful for this query? | Feature identity or balanced load alone is insufficient. |
| Training method | Can MTP, diffusion, or another objective improve the required state? | The method is an intervention, not the research goal. |

The downstream goal is therefore not “prove MTP works” or “make features
separable.” It is:

> Learn a query-conditioned Router whose selections predict held-out functional
> utility under a fixed compute budget.

## Points That Must Be Considered Together

The 0713 advisor recordings imply seven coupled requirements:

1. **Valuable workload:** the task must require difficult long-range structure,
   not token distance alone.
2. **Explicit computation:** local steps, coupling, order, intermediate states,
   and final readout must be modeled separately.
3. **Objective mechanism first:** the next-one versus next-two supervision
   difference must not be confused with long-context performance.
4. **Formation versus use:** more information in a state does not show that the
   ordinary head uses it.
5. **Functional specialization:** separable features matter only if routing
   them changes expert or memory utility.
6. **Capability and carrier validity:** failure to learn the carrier cannot be
   interpreted as a failure of MTP or of composition.
7. **Daily closure:** each day must end with one answered subquestion, a claim
   boundary, and exactly one next decision.

## Evidence Map And Bottleneck Diagnosis

| Line | Direct result | What it rules out | What remains |
|---|---|---|---|
| R3/R4 | Perfect feature alignment still gives worse sparse retrieval quality than a local same-count baseline in the controlled setup. | One-feature-one-expert is not sufficient to create a useful KV index. | Which query-conditioned variable predicts functional utility? |
| A11 | Informative future supervision supplies an earlier signal, but the registered strong standard-head K/V-use increment failed. | Signal formation is not sufficient for strong downstream use. | Is there a weaker useful channel, or is structural necessity required? |
| A12 | E04 completed NTP Stage A, but no scale passed capability and the row-removal guard was structurally invalid. | The current carrier cannot support a formal MTP comparison. | Which isolated capability failed, and what carrier makes evidence necessary? |
| A06 | Controlled route geometry, utility binding, and partial-feedback repair are established. | Geometry or route NMI alone is not the end goal. | Does real data contain stable held-out utility headroom worth routing? |

The common bottleneck is:

> We have repeatedly measured whether a signal exists or aligns, but the
> decisive object is whether selecting it preserves or improves downstream
> loss.

## Problem Chain

```text
P0 nominal context capacity
-> P1 query-relevant evidence is accessible
-> P2 evidence is encoded and transported
-> P3 the ordinary head causally uses it
-> P4 use survives ordered composition or multi-hop aggregation
-> P5 a Router predicts this functional utility at fixed budget
-> P6 routed experts provide stable held-out utility per unit cost
```

Current localization:

- R3/R4 weaken a static-feature answer to `P5`.
- A11 separates `P2` from `P3`.
- A12 is blocked before a clean test of `P4`.
- A06 asks whether the premise for `P6` exists on a real workload.

## Smallest Decisive Questions

### Q0 — already answerable

**Is perfect feature specialization sufficient for useful sparse retrieval in
the existing controlled setup?**

Answer: **No.** R3 and R4 show that even perfect feature-aligned buckets are
inferior to the local same-count baseline on functional sparse-output metrics.
This is a controlled negative result, not a claim about all long-context
Routers.

### Q1 — proposed audit for today

**On existing controlled checkpoints, does a retrieval proxy predict the
causal loss utility of a memory item under a fixed top-$k$ budget?**

Let $q$ be a query, $C_q$ its available memory, and $S_s^k(q)$ the $k$ items
selected by score $s$. Define the primary functional loss gap:

$$
\Delta_s(k)
=
\mathbb E_q\left[
\ell\!\left(q;S_s^k(q)\right)-\ell(q;C_q)
\right].
$$

$\Delta_s(k)=0$ means the sparse selection matches the dense reference loss;
smaller is better. It measures prediction preservation at matched budget. It
does not prove long-context scaling, causal independence among items, or MoE
expert value.

For diagnosis only, define leave-one-out causal utility:

$$
u(q,i)
=
\ell\!\left(q;C_q\setminus\{i\}\right)-\ell(q;C_q).
$$

Positive $u(q,i)$ means removing item $i$ hurts the ordinary head. Because
memory items can interact, individual utilities are not additive and must not
be called an exact top-$k$ oracle.

Minimum matched-budget selectors:

1. random same-count;
2. local same-count;
3. feature-aligned bucket;
4. dense-attention-mass ranking;
5. causal-utility ranking as a diagnostic upper bound, if computationally
   feasible.

Primary metric: $\Delta_s(k)$ on held-out queries. Rank agreement with
$u(q,i)$ is secondary.

Decision rule:

- if attention mass predicts utility but feature identity does not, target a
  query-conditioned attention-like index;
- if attention mass also predicts utility poorly, optimize output/loss utility
  rather than imitate attention;
- if every selector fails mainly with distance, investigate transport or
  position before Router semantics.

## 16:00–22:00 Research Path

| Time | Output | Stop condition |
|---|---|---|
| 16:00–16:25 | Researcher completes the six judgment fields below. | No Protocol before the human mechanism and rival are explicit. |
| 16:25–16:50 | Freeze the meeting theme, Q0 answer, and claim boundary. | Theme must connect workload, mechanism, and MoE utility in one sentence. |
| 16:50–17:30 | Build one evidence table from R3/R4 and close Q0. | One direct result, one cannot-claim boundary, one next question. |
| 17:30–18:00 | Draft the minimal Q1 Protocol: checkpoint, selectors, $k$, split, primary metric, guards, pass/fail/insufficient meanings. | Stop for explicit approval. |
| 18:00–18:45 | After approval only: audit artifacts and run one-query smoke without retraining. | Dense replay and same-count checks must pass. |
| 18:45–20:00 | Evaluate matched-budget selectors on existing checkpoints. | Do not add a new model or method during the run. |
| 20:00–20:45 | Produce one primary table/figure for $\Delta_s(k)$. | Figure must answer Q1 without relying on proxy metrics alone. |
| 20:45–21:20 | Localize failure to index, transport, composition, or readout. | Rival explanations remain explicit. |
| 21:20–21:40 | Researcher writes a closed-book seven-line result summary. | AI audits wording only after the human draft. |
| 21:40–22:00 | Update the relevant anchor/result/CURRENT only if evidence exists. | End with exactly one next decision. |

Fallback: if the Protocol is not approved or the existing artifacts are not
ready, the decisive output remains the closed Q0 result plus an audited Q1
Protocol and artifact-readiness ledger. Do not manufacture a training result.

## 2026-07-17 Morning Gate

| Time | Required output |
|---|---|
| 09:00–10:00 | Reproduce the primary number or complete the Protocol/readiness audit. |
| 10:00–11:00 | Write the one-page group-meeting brief: problem, Q0 answer, Q1 status, boundary, next decision. |
| 11:00–12:00 | Discuss the decision with the advisor/pro: metric target, carrier choice, and falsifier. |
| 12:00–13:00 | Freeze one exact answer and one approved next step; remove every unsupported claim. |

## Human Judgment Required Before Q1

The phenomenon is supplied above. The researcher must complete the remaining
fields before this working theme can become a formal anchor or Protocol:

- Mechanism guess:
- Strongest rival explanation:
- Most uncertain point:
- Evidence that would change the judgment:
- Current next decision:
- Why Q1 is preferable to directly building a new long-context Router:

## Exact Discussion Questions For The Advisor / Pro

1. Is held-out standard-head loss preservation the correct functional target
   for the first Router audit?
2. Should the first audit stay on the existing short controlled checkpoint to
   isolate mechanism, or move immediately to a real long-context workload?
3. Which result would justify the next method step: attention-like indexing,
   direct loss-utility prediction, or a transport intervention?

## Claim Boundary And Immediate Next Decision

This working theme does not establish that current million-token models fail
generally, that attention is the correct Router, that MTP improves retrieval,
or that a controlled short-context result transfers to real agents.

Exactly one immediate decision:

> The researcher should approve, modify, or reject Q1 as the smallest
> functional-retrieval audit after completing the human judgment fields.

## Internal Sources

- [0713 advisor discussion](../../0713/recordings/0713_导师与学长讨论_整理稿.md)
- [0713 research guidance](../../0713/recordings/0713_科研指导_整理稿.md)
- [R3 perfect-router retrieval](../../../Projects/from-attention-to-search/main/experiments/archive/R3_perfect_router_retrieval/summary.md)
- [R4 attention-output retrieval](../../../Projects/from-attention-to-search/main/experiments/archive/R4_attention_output_router_retrieval/summary.md)
- [A11 result](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)
- [A12 E04 result](../../../Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md)
- [A06 research map](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md)
