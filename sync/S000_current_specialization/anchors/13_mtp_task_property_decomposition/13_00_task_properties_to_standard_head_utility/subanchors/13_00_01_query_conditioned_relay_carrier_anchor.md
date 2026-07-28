# Is the Minimal Query-Conditioned Relay Carrier Valid and Learnable?

Thinking Card source:
[long_horizon_compositional_workload_thinking_card_cn.md](/daily_research_reports/0717/mtp_long_horizon_compositional_workload/long_horizon_compositional_workload_thinking_card_cn.md)

Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

**Single decision question:** Can a two-layer NTP Transformer solve held-out
query-conditioned selection only by forming a relay state that the standard
head causally uses?

The **carrier-eligibility verdict** is a Boolean conjunction of registered
structural, capability, generalization, counterfactual, and relay-intervention
gates. It decides only whether objective comparison is admissible.

## 2. Physical Priors

1. With the frozen attention graph, one layer cannot move evidence into
   `RELAY` and then consume it at `ANSWER`; two layers can.
2. If the two-layer model is capable, changing the selected value must change
   the answer while changing the unselected value must not.
3. If the standard head uses the intended path, replacing the layer-1 relay
   state with an in-distribution donor state must make the answer follow the
   donor label.

## 3. Falsifiable Hypotheses

**H1:** the two-layer relay model reaches at least `0.95` held-out accuracy and
passes counterfactual and relay-state interventions, while the one-layer relay
model remains at or below `0.15` and the one-layer bypass control reaches at
least `0.95`.

**Rival:** success comes from a direct edge, a memorized triple, a label leak,
or an output interface that does not actually consume the relay.

**Pass:** the carrier-eligibility conjunction is true.

**Fail:** a registered gate gives a decisive negative result.

**Insufficient:** training, split construction, intervention pairing, or
implementation replay is invalid.

## 4. Mathematical Model

For independently sampled $A,B$ and balanced $Q$,

$$
Y=A\mathbf 1[Q=0]+B\mathbf 1[Q=1].
$$

The relay-required graph implements

$$
S_1=f_{\theta,1}(A,B,Q),
\qquad
\hat Y=g_{\theta,2}(S_1),
$$

with no other evidence-to-answer path. The one-layer model instead evaluates
$g_{\theta,1}(S_0)$ where $S_0$ is the constant relay-token embedding, so
$Y$ is conditionally uniform and its optimal accuracy is $1/|\mathcal V|$.

The NTP-only training loss is the all-position next-token objective. The
primary answer metric is computed only at the `ANSWER` position with the
ordinary head.

## 5. Computational Realization

- value vocabulary: 16 equiprobable value tokens;
- sequence length: 7 tokens including the answer target;
- train/evaluation split: disjoint triples $(A,B,Q)$ with every value and both
  selectors represented in both splits;
- model: tied-embedding causal Transformer, width 64, four heads, dropout 0;
- registered conditions: one-layer relay, two-layer relay, one-layer bypass;
- objective: NTP only; the future head is instantiated but inactive;
- attention: `RELAY` reads $A,B,Q$; relay-required `ANSWER` reads only
  `RELAY` and itself; bypass `ANSWER` may directly read $A,B,Q$.

## 6. Minimal Falsification Tests

The primary metric is

$$
C_{\mathrm{eligible}}
=
\bigwedge_{j=1}^{6}G_j,
$$

a Boolean with `pass`, `fail`, or `insufficient` state.

| Gate | Computation | Pass | Fail | What it prevents |
| --- | --- | --- | --- | --- |
| $G_1$ graph validity | exact reachability from $A,B,Q$ to `ANSWER` | relay path is unique; bypass has a direct path | any unregistered direct path | answer leakage |
| $G_2$ held-out capability | two-layer relay standard-head accuracy | mean $\ge0.95$, at least 4/5 seeds $\ge0.90$ | powered result remains below | objective comparison on an unlearned task |
| $G_3$ depth control | one-layer relay accuracy | every seed $\le0.15$ | stable above `0.15` | hidden shortcut in the mask |
| $G_4$ interface control | one-layer bypass accuracy | mean $\ge0.95$, at least 4/5 seeds $\ge0.90$ | remains low | general learner/output failure |
| $G_5$ input counterfactuals | selected and unselected value swaps | selected-follow and unselected-invariance each $\ge0.90$ | either below | fixed-output or selector-ignoring solution |
| $G_6$ relay causal use | in-distribution layer-1 relay donor patch | donor-label follow $\ge0.90$ and same-label preservation $\ge0.95$ | output does not follow relay content | readability without use |

The main falsifier is a capable two-layer model whose answer does not follow an
in-distribution relay-state intervention.

## 7. Current Evidence

The carrier is closed as the first objective-comparison surface.

- [E01](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_01_E01_query_conditioned_relay_carrier/summary.md)
  passed data, graph, and one-layer depth controls but failed the 1,000-step
  two-layer capability gate (`0.7243` mean).
- [E02](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_01_E02_budget_extension/summary.md)
  rejected budget alone: 3,000 constant-rate steps reached only `0.8097`.
- [E03](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_01_E03_cosine_schedule/summary.md)
  showed that decay matters and that every relay seed can reach at least
  `0.9806`, but final mean remained `0.9437`, below the registered gate.
- [E04](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_01_E04_width_capacity/summary.md)
  weakened missing width as the explanation: width 128 reduced mean relay
  accuracy to `0.6194`.

Across all runs, one-layer relay remained at chance and the bypass interface
was learnable. The unresolved instability belongs to query-conditioned binding
plus relay, not to a data leak or an absent path.

## 8. Claim Boundary And Next Decision

Supported: the frozen graph implements a genuine two-transition relay and can
carry content-specific causal control at capable checkpoints.

Weakened: this query-conditioned task is not a stable low-cost carrier for the
first objective comparison.

Not supported: MTP benefit, general learner incapability, multi-evidence
composition, long token distance, code transfer, or MoE value.

**Exactly one next decision:** remove query-conditioned selection, validate
single-value relay under the same graph, and treat selection as a later task
property rather than a carrier prerequisite.
