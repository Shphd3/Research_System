# Does Relay Necessity Amplify the Standard-Head Utility of Next-2 Supervision?

Thinking Card source:
[long_horizon_compositional_workload_thinking_card_cn.md](/daily_research_reports/backup/2026/07/0717/mtp_long_horizon_compositional_workload/long_horizon_compositional_workload_thinking_card_cn.md)

Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

**Single decision question:** on the validated, entropy-matched single-value
carrier, does forcing the ordinary next-token head to use an early relay state
increase the finite-budget benefit of Next-2 auxiliary supervision relative to
a matched auxiliary control?

`Next-2 supervision` means that the second head predicts the token two
positions ahead. `Matched shared-aux` means that the same second head predicts
the next token with the same number of active cross-entropy terms and the same
loss weight. Only the ordinary next-token head is evaluated.

For path condition $r\in\{\mathrm{relay},\mathrm{bypass}\}$, define

$$
U_r
=
\operatorname{AULC}_{\mathrm{SA},r}
-
\operatorname{AULC}_{\mathrm{MTP},r},
$$

where AULC is the area under the standard-head answer-NLL learning curve,
divided by the registered 1,000-step horizon. Positive $U_r$ means lower
finite-budget answer loss for Next-2 supervision.

The relay-necessity interaction is

$$
\Delta_{\mathrm{relay}}
=
U_{\mathrm{relay}}-U_{\mathrm{bypass}}.
$$

## 2. Physical Priors

1. In the relay path, the answer state can receive $A$ only through the relay;
   in the bypass path it can read $A$ directly.
2. At the relay position, the Next-2 auxiliary target is the answer value
   $A$, whereas the matched next-token auxiliary target is the fixed
   `[ANSWER]` marker.
3. An earlier answer-aligned gradient can help only if it improves the state
   consumed by the standard head and is not cancelled by the other
   all-position losses.

These are mechanism priors, not established conclusions.

## 3. Falsifiable Hypotheses

**H1:**

$$
U_{\mathrm{relay}}>0
\quad\text{and}\quad
\Delta_{\mathrm{relay}}>0.
$$

This says both that Next-2 has positive standard-head utility when relay is
required and that the utility is larger than when a direct answer path exists.

**Strongest rival:** the ordinary answer loss already trains the relay
sufficiently, so moving a duplicate answer target one position earlier has no
marginal value; or the all-position Next-2 background introduces enough noise
to erase the local direct-credit benefit.

**Pass:** all six objective/path cells remain capable, relay interventions
remain causal, both paired bootstrap lower bounds are above zero, mean
$U_{\mathrm{relay}}$ and mean $\Delta_{\mathrm{relay}}$ are each at least
$0.02$ nats, and at least seven of eight paired seeds have the expected sign.

**Fail:** the carrier remains capable and causally used, but the upper
confidence bound of either required effect is at or below zero.

**Insufficient:** a capability/use gate fails or uncertainty overlaps both
positive and null regions.

## 4. Mathematical Model

Let $A,B\sim\operatorname{Unif}(\mathcal V)$ be independent and let $Y=A$.
The frozen serialization is

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

For input positions $t=0,\ldots,5$, the ordinary objective is

$$
\mathcal L_{\mathrm{NTP}}
=
\frac{1}{6}\sum_{t=0}^{5}
\operatorname{CE}(p_1(h_t),x_{t+1}).
$$

The two matched dual-head objectives are

$$
\mathcal L_{\mathrm{SA}}
=
\frac12\mathcal L_{\mathrm{NTP}}
+
\frac{1}{2\cdot5}\sum_{t=0}^{4}
\operatorname{CE}(p_2(h_t),x_{t+1}),
$$

and

$$
\mathcal L_{\mathrm{MTP}}
=
\frac12\mathcal L_{\mathrm{NTP}}
+
\frac{1}{2\cdot5}\sum_{t=0}^{4}
\operatorname{CE}(p_2(h_t),x_{t+2}).
$$

The auxiliary label sets have two independent value targets and three
deterministic structural targets each. Their Bayes conditional-entropy sums
are therefore matched, although realized gradients need not be.

At $t=4$, shared-aux predicts fixed token $x_5=[\mathrm{ANSWER}]$, while
Next-2 predicts $x_6=A$. NTP still predicts $A$ at $t=5$; the comparison is
earlier direct credit versus later credit, not visibility versus invisibility.

## 5. Computational Realization

Use the frozen `copy_matched` data split, width-64 two-layer Transformer,
four attention heads, and sparse masks from the passed carrier. Cross

```text
path:       relay-required | bypass-available
objective:  NTP | matched shared-aux | informative Next-2
```

All paired conditions use identical initialization seeds, mini-batch indices,
optimizer, token budget, evaluation grid, vocabulary, labels, and train/eval
split. The six final-capability cells use 3,000 steps. The primary learning
window is frozen at 1,000 steps because four of five NTP relay seeds had
already crossed 95% held-out accuracy by that point in the carrier audit.

NTP is a secondary system baseline. The primary causal contrast is
Next-2 versus matched shared-aux because only those conditions match active
head count and nominal loss allocation.

## 6. Minimal Falsification Tests

1. **Capability guard:** each objective/path cell has mean final accuracy at
   least 0.95 and at least seven of eight seeds at or above 0.90.
2. **Causal-use guard:** each relay objective has mean different-label donor
   follow at least 0.90.
3. **Primary utility:** paired-seed $U_{\mathrm{relay}}$ over 0--1,000 steps.
4. **Primary interaction:** paired-seed $\Delta_{\mathrm{relay}}$.
5. **Optimization diagnostics:** initial shared-trunk gradient norm and cosine
   between answer loss and auxiliary loss. These explain; they do not decide.

The main falsifier is a non-positive
$\Delta_{\mathrm{relay}}$ with every capability and causal-use guard passing.

## 7. Current Evidence

`13_00_02 E02` passed the frozen carrier. E01 and fresh-seed E02 then each
found positive relay utility and positive interactions in 8/8 paired seeds.
Their registered verdicts remain insufficient: E01 had an incoherent all-seed
causal-use gate, while E02 failed the shared-aux 7/8 post-treatment capability
gate. E02 revealed that requiring every objective arm to be capable conditions
on an outcome of the treatment.

The downstream one-label localization and nuisance-matched control now own the
passed causal result; this subanchor remains historically insufficient under
its original contract.

## 8. Claim Boundary And Next Decision

This test identifies the complete objective effect of putting an answer-related
target on an earlier state relative to a repeated next-token auxiliary target.
It does not isolate semantic information from horizon, prove compute
efficiency, or establish a result for standard MTP implementations, code,
natural language, long context, planning, or MoE.

**Exactly one next decision:** use `13_00_04` and `13_00_05` to localize the
candidate effect without post-treatment arm selection.
