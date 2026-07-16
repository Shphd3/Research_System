# Candidate Minimal Question and Evening Decision Gate

Date: 2026-07-16

Status: candidate plan; execution is blocked pending human judgment and an
approved Protocol.

Chinese companion:
[02_minimal_question_and_evening_gate_cn.md](02_minimal_question_and_evening_gate_cn.md)

> Superseded at 19:00 by the researcher's shared-subspace conflict definition.
> Use
> [05_theory_clarification_and_meeting_anchor.md](05_theory_clarification_and_meeting_anchor.md)
> for the consolidated current question and meeting theme.

## Candidate Question

> Does standard MTP automatically improve rare-mode learning relative to
> common-mode learning, or is a future-horizon rare-enrichment condition
> necessary?

## Candidate Decisive Answer

Inside the registered two-mode quadratic model, standard MTP is not an
automatic long-tail remedy. Its relative effect is determined by

$$
\rho_M
=
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}}
\quad\text{versus}\quad
\rho_N=\frac{q_{1,r}}{q_{1,c}}.
$$

The decisive theoretical step is to prove the sign condition and audit one
null case, one positive case, and one negative case.

## Required Controls for a Later Numerical Check

1. NTP: one active next-token target.
2. Shared-aux: matched active heads and loss scale, but the auxiliary target
   duplicates the next-token information.
3. Informative-MTP, ratio-preserving world: future information is added without
   changing the rare/common curvature ratio.
4. Informative-MTP, rare-enriched world: the future horizon increases the
   rare/common curvature ratio.
5. Informative-MTP, common-enriched world: a falsifying negative control.

Primary metric candidate:

$$
D_{\mathrm{rel}}
=
\log\frac{\widehat Q_{M,r}}{\widehat Q_{M,c}}
-
\log\frac{\widehat Q_{N,r}}{\widehat Q_{N,c}}.
$$

This measures a relative mode-learning change. It does not measure real
long-tail accuracy, standard-head causal use, or Router utility.

## 16:00–22:00 Route

| Time | Output | Decision gate |
| --- | --- | --- |
| 16:00–16:30 | Researcher fills the Thinking Card from memory | Freeze one mechanism guess and one strongest rival |
| 16:30–17:15 | Agree on MTP variant, common/rare object, efficiency unit, and main-head-use definition | Reject the question if any object remains mixed |
| 17:15–18:30 | Audit the two-mode proposition and proof | Confirm theorem assumptions and three sign cases |
| 18:30–19:00 | Write the cannot-claim boundary and a counterexample | Decide whether the result is new enough for the meeting |
| 19:00–19:30 | If approved, create the formal anchor and Protocol | No approval means no implementation |
| 19:30–21:00 | Run only the registered minimal numerical sanity check on the worker surface | Treat it as implementation verification, not real-task evidence |
| 21:00–21:30 | Compare measured slopes with the analytic prediction | Pass, fail, or insufficient under frozen tolerance |
| 21:30–22:00 | Researcher writes a closed-book result summary; AI audits wording | Freeze exactly one next decision for tomorrow |

## By 13:00 Tomorrow

Prepare one meeting answer:

> Standard MTP does not automatically correct common/long-tail imbalance.
> It changes relative learning only if added horizons are relatively enriched
> for the underlearned mode; current real-task relevance and standard-head use
> remain open.

The meeting package should contain the theorem, one counterexample, the
minimal-check verdict if approved and run, the claim boundary, and one next
decision. It should not contain a broad code/planning claim or a new Router
method.

## Current Stop Condition

Do not create the formal anchor, Protocol, implementation, project sync, or
commit until the researcher approves or modifies the candidate question and
completes the human judgment fields.
