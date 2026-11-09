# Protocol A: A11_05 Semantic Efficiency Mechanism Decomposition

Approval status: approved by user and completed on 2026-07-08.
Anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_05_semantic_efficiency_bridge_anchor.md`

Run record:

- ACP job: `pt-u0od5jmz`
- Run name: `a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`
- Summary: `summary.md`
- Detailed record: `detailed.md`

## 0. Protocol Question For Approval

In the clean $\tau=3$ construction, does the K=3 semantic-efficiency advantage come from direct horizon-3 supervision on the decision prefix state $h_T$, rather than from all-position indirect transfer, generic auxiliary loss effects, or a local next-token learning tradeoff?

Plain version:

```text
If Y3=S_Z is the first future token that needs Z, is the speed advantage caused
by directly training h_T to predict S_Z?
```

## 1. Why This Protocol Is Needed

A11_04_03 already shows a qualified efficiency pattern:

- in clean decision-only $\tau=3$, K=3 learns $Z$ earlier than K=1/K=2;
- in clean all-position training, K=3 remains strongest, but K=1/K=2 can also recover $Z$;
- noisy all-position controls can produce false-positive recovery;
- gradient cosine and norm diagnostics are mixed.

Therefore the next protocol should not repeat a broad K comparison. It should decompose the mechanism behind K=3:

```text
direct supervision at h_T
vs
indirect transfer through other all-position losses
vs
local-loss tradeoff
vs
gradient routing / interference
```

## 2. Data Construction

Use only the clean $\tau=3$ task first:

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

Decision prefix:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U).
$$

Future targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Do not add larger K or natural-language data in this protocol.

## 3. Experimental Variables

### 3.1 Variables We Manipulate

| Variable | Values / conditions | What it tests |
|---|---|---|
| direct decision-prefix horizon-3 loss | present vs masked | whether direct $h_T\to S_Z$ supervision causes speed |
| all-position indirect horizon-3 losses | present vs absent outside decision prefix | whether other positions can transfer $Z$ into $h_T$ |
| active horizon K | K=1, K=2, K=3 | baseline coverage comparison, using existing A11_04_03 where possible |
| direct loss weight $\lambda_3$ | default 1.0 first; optional 0.25/0.5/1.0 after first pass | direct supervision strength |
| one-step update direction | $g_1$, $g_3$, $g_1+\lambda_3g_3$ | gradient usefulness and interference |

### 3.2 Variables We Hold Fixed

| Fixed object | Value |
|---|---|
| data regime | clean $\tau=3$ |
| number of branches | 4 |
| first informative target | $Y_3=S_Z$ |
| local targets | $Y_1=A$, $Y_2=C$ |
| model | same one-layer Transformer family as A11_04_03 |
| optimizer / schedule | same as A11_04_03 unless implementation requires a documented change |
| seeds | 971, 972, 973, 974, 975 |
| evaluation state | decision prefix $h_T$ |
| primary threshold | $Q\ge0.9$ |

### 3.3 Variables We Measure

| Metric | Formula / computation | What it answers |
|---|---|---|
| guarded recovery $Q(t)$ | $Q(t)=\min\{A(t),P(t),S(t)\}$ | whether $h_T$ robustly contains $Z$ |
| time-to-threshold $T_\theta$ | first step with $Q(t)\ge0.9$ for consecutive evals | whether learning is faster |
| early AUC | average $Q(t)$ over early window | whether learning is more stable early |
| local $Y_1/Y_2$ accuracy and CE | decision-prefix and structured-position metrics | whether MTP hurts local learning |
| $\Delta R_\phi$ after one-step update | probe loss change after counterfactual update | whether $g_3$ helps recover $Z$ |
| $\Delta Q$ after one-step update | guarded recovery change | whether update improves semantic recovery |
| $\Delta L_{\mathrm{local}}$ after one-step update | local loss change | whether update damages local prediction |
| gradient compatibility | cosine $c_{13}$ and $\rho$ | diagnostic only, not standalone proof |

## 4. Conditions

Use existing A11_04_03 outputs as the baseline reference when possible.

| Condition | Loss structure | Purpose |
|---|---|---|
| K1 all-position | active $Y_1$ only | NTP-style baseline |
| K2 all-position | active $Y_1,Y_2$ | non-covering MTP baseline |
| K3 full all-position | active $Y_1,Y_2,Y_3$ at all valid positions | full direct-plus-indirect K=3 |
| K3 no-decision-L3 | K3 all-position, but decision-prefix $L_3(h_T,S_Z)$ masked | measures all-position indirect transfer without direct $h_T$ supervision |
| K2 plus decision-L3 | K2 all-position plus only decision-prefix $L_3(h_T,S_Z)$ | isolates direct $h_T$ supervision |

Minimal first pass:

```text
run only the two new intervention conditions:
K3 no-decision-L3
K2 plus decision-L3
```

Compare them against the existing K1/K2/K3 A11_04_03 baseline.

## 5. Primary Decision Logic

### Direct supervision supported

Expected pattern:

```text
K2 plus decision-L3 improves over K2 all-position
K3 no-decision-L3 is weaker than K3 full
K3 full remains strongest or tied strongest
local Y1/Y2 guard passes
```

Interpretation:

```text
direct h_T -> S_Z supervision explains a measurable part of the efficiency gain
```

### Indirect transfer sufficient

Expected pattern:

```text
K3 no-decision-L3 matches K3 full
K2 plus decision-L3 does not improve over K2 all-position
```

Interpretation:

```text
all-position shared-parameter transfer is sufficient in this setup; direct
decision-prefix supervision is not the measured efficiency cause
```

### Direct signal useful but costly

Expected pattern:

```text
K2 plus decision-L3 improves Q
but local Y1/Y2 CE or accuracy degrades
```

Interpretation:

```text
direct supervision trades local learning for semantic recovery
```

### Gradient bridge supported

Expected pattern:

```text
one-step update with -g3 or -(g1 + lambda3 g3)
improves R_phi / Q more than -g1
without worsening local loss
```

Interpretation:

```text
the future-token gradient has measured semantic usefulness
```

## 6. Pass / Fail / Insufficient Criteria

Pass:

```text
direct-supervision condition improves T_theta or early AUC over non-covering baseline
masking decision-prefix L3 weakens full K3
local guard passes
one-step counterfactual supports positive semantic usefulness or clearly explains why not
```

Fail:

```text
direct-supervision condition does not improve Q, T_theta, or early AUC
masking decision-prefix L3 has no effect
K1/K2/K3 differences are fully explained by indirect transfer
```

Insufficient:

```text
high seed variance
threshold heavily censored
local guard and Q disagree
one-step counterfactuals are too noisy
intervention implementation changes unintended loss scale or data distribution
```

## 7. Required Outputs

```text
protocol.md
summary.md
detailed.md
tables/condition_summary.csv
tables/efficiency_by_seed.csv
tables/local_guard.csv
tables/counterfactual_update.csv
figures/q_curves.png
figures/local_guard.png
figures/counterfactual_update.png
```

The summary must answer:

```text
Does direct decision-prefix horizon-3 supervision explain K=3's semantic
efficiency advantage beyond all-position indirect transfer?
```

## 8. Approval Checklist

Approve this protocol only if the intended next question is mechanism
decomposition at fixed $\tau=3$.

Do not approve this protocol if the intended next question is:

```text
bigger K scaling
natural language transfer
full MoE expert utility
new architecture comparison
```
