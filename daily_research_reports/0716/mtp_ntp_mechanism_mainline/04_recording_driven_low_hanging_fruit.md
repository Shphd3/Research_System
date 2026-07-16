# Recording-Driven Low-Hanging Fruit

Date: 2026-07-16, 19:00

Status: AI audit and candidate theorem; not a formal anchor or approved
Protocol.

Chinese companion:
[04_recording_driven_low_hanging_fruit_cn.md](04_recording_driven_low_hanging_fruit_cn.md)

> **Current-entry update:** this file preserves the recording-to-low-hanging-
> fruit derivation. The complete theory boundary, curvature correction, and
> final meeting theme are consolidated in
> [05_theory_clarification_and_meeting_anchor.md](05_theory_clarification_and_meeting_anchor.md).

## Conclusion from the Recordings

The recordings do connect MTP to the project, but only as a candidate training
objective for changing representation formation. They do not state or
establish that MTP solves common/rare interference.

The advisor's explicit priority is:

1. identify the essential causal difference between next-one and next-two;
2. ask whether the changed objective makes mixed representations easier to
   separate;
3. ultimately route different frequencies or feature types to different
   experts;
4. close one small question per day.

Therefore, tomorrow's smallest defensible topic is not “why MTP works on code”
or “how to build an MTP Router.” It is:

> **Can informative next-two supervision escape common-subspace interference,
> or does it merely reweight the common/rare compromise inside the same
> subspace?**

## Human Definitions Preserved

- **Long tail:** low-frequency latent features, not merely rare tokens.
- **Conflict:** a rare feature is learned in a common-dominated subspace; when
  frequent common updates disagree with the direction required by the rare
  feature, rare learning becomes extremely slow or stalls.

These definitions replace the orthogonal two-mode model as the active
mechanism.

AI audit: directional difference alone is not destructive conflict. If
$\langle g_R,g_C\rangle>0$, common updates still help rare. If the inner
product is near zero, the main problem is rare-update starvation. Destructive
interference requires a sufficiently negative frequency-weighted projection.
The minimal model must keep these two rivals separate.

## Minimal First-Order Model

Let $L_C$ and $L_R$ be the standard-head NTP losses on common and rare latent
features. Define

$$
g_C=\nabla_\theta L_C,\qquad
g_R=\nabla_\theta L_R,
$$

with frequencies $\pi_C\gg\pi_R$. An NTP training gradient is

$$
G_N=\pi_Cg_C+\pi_Rg_R.
$$

After one gradient-descent step, the first-order rare-loss decrease is

$$
D_R^N
=
\langle g_R,G_N\rangle
=
\pi_R\|g_R\|^2+\pi_C\langle g_R,g_C\rangle.
$$

Positive $D_R^N$ means rare loss decreases. If the gradients conflict, rare
learning stalls when

$$
\pi_C[-\langle g_R,g_C\rangle]_+
\geq
\pi_R\|g_R\|^2.
$$

This is the precise version of the researcher's mechanism definition:
frequent common pressure cancels the rare feature's own learning signal.

## What MTP Must Add

To isolate future information rather than extra heads or loss scale, compare:

- matched shared-aux, whose second head duplicates next-token information;
- informative next-two, whose second target contains additional information.

Let their auxiliary shared-parameter gradients be $a_{\mathrm{shared}}$ and
$a_{\mathrm{info}}$. The information-content-specific increment in rare
descent is

$$
\Gamma_R
=
\left\langle
g_R,\,
a_{\mathrm{info}}-a_{\mathrm{shared}}
\right\rangle.
$$

Then:

- informative next-two helps rare relative to matched shared-aux iff
  $\Gamma_R>0$ to first order;
- it rescues a stalled rare feature iff
  $D_R^{\mathrm{shared}}+\Gamma_R>0$.

“MTP contains more information” is therefore insufficient. The extra gradient
must be aligned strongly enough with the standard-head rare objective to
overcome the common pressure.

## Rank-One Impossibility and Escape Condition

Let $P_C$ be the frozen rank-one common-subspace projector. Suppose, throughout
the local trajectory being analyzed,
$g_C$, $g_R$, $a_{\mathrm{shared}}$, and $a_{\mathrm{info}}$ all lie in
$\operatorname{range}(P_C)$. Every weighted sum and every infinitesimal update
then remains in that same subspace.

**Proposition:** under this assumption, MTP cannot separate the rare feature
from the common subspace. It can only change the scalar common/rare compromise.

**Proof:** a linear subspace is closed under weighted sums. The total gradient
is a weighted sum of vectors in $\operatorname{range}(P_C)$, so it has zero
component in $I-P_C$. Repeated infinitesimal updates cannot create an
orthogonal rare direction.

For MTP to create a separate rare direction while preserving the established
common subspace, a necessary condition is

$$
E_\perp
=
\frac{
\left\|
(I-P_C)
(a_{\mathrm{info}}-a_{\mathrm{shared}})
\right\|^2
}{
\left\|
a_{\mathrm{info}}-a_{\mathrm{shared}}
\right\|^2+\epsilon
}
>0.
$$

This is necessary for geometric escape, not sufficient for functional
benefit. Functional benefit additionally requires $\Gamma_R>0$, common-loss
preservation, state transport, and standard-head use.

## The Decisive Meeting Answer

By tomorrow the line should be able to state:

> NTP rare-feature stalling can be formalized as frequency-amplified negative
> gradient pressure inside a shared common subspace. Informative next-two
> supervision does not automatically solve it. If the information-specific
> auxiliary gradient remains inside the same rank-one subspace, MTP only
> reweights the compromise. A new rare direction requires a nonzero
> information-specific gradient component outside the common subspace, and
> standard-head benefit requires that component to be target-aligned and used.

This is a new conditional understanding, not a claim that standard MTP already
passes the condition.

## 19:00 to 13:00 Route

| Time | Output | Gate |
| --- | --- | --- |
| 19:00–19:30 | Researcher approves the question, strongest rival, and mind-changing evidence | No approval, no Protocol |
| 19:30–20:30 | Finalize the first-order conflict proof and rank-one impossibility result | One theorem, one counterexample, one boundary |
| 20:30–21:00 | Draft a minimal three-condition Protocol | NTP / shared-aux / informative-next-two |
| 21:00–23:00 | If approved, run only the registered sanity check on the worker surface | Measure $\Gamma_R$, $E_\perp$, rare loss, and common guard |
| 23:00–23:30 | Record pass / fail / insufficient | Do not infer code, planning, or Router value |
| 09:00–10:00 | Researcher writes a closed-book summary | AI audits only after the human draft |
| 10:00–11:00 | Connect the result to A11, A07, and the recordings | Separate established links from hypotheses |
| 11:00–12:00 | Prepare the minimal meeting brief | One claim, one figure/table, one next decision |
| 12:00–13:00 | Rehearse objections and freeze the boundary | Then update sync and commit/push if still requested |

## Human Gate

The researcher still needs to approve or correct:

1. strongest rival: any rare improvement is ordinary loss reweighting or
   common undertraining, not a new MTP-induced direction;
2. most uncertain point: whether the information-specific next-two gradient
   has a rare-aligned component outside $P_C$;
3. mind-changing evidence: matched shared-aux and informative-next-two have the
   same $E_\perp$ and $\Gamma_R$, or informative-next-two improves rare loss
   without the proposed geometric change.

No formal anchor or Protocol is authorized until these judgments are human
approved.
