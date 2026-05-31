# 01 Theory Derivation

Status: accepted for daily sandbox.

Boundary:

```text
route-pattern specialization only
not utility-aligned specialization
not full NTP
```

## Setup

Features:

$$
x_A=e_1,\quad x_B=e_2
$$

Router:

$$
z(x)=W_rx+b,\quad p(e|x)=\operatorname{softmax}(z(x))
$$

Route-feature heatmap:

$$
H_{f,e}=E_{x\sim f}[p(e|x)]
$$

Top-1 assignment:

$$
\hat e(x)=\arg\max_e p(e|x)
$$

## Expressivity Check

A linear router can express diagonal routing for orthogonal features.

Example:

$$
W_r=
\begin{bmatrix}
\alpha & -\alpha \\
-\alpha & +\alpha
\end{bmatrix},
\quad \alpha>0
$$

Then:

```text
x_A -> E0
x_B -> E1
```

So if training fails in this proxy, pure linear expressivity is not the first explanation.

## Training Question

If the router can express separation, training may still fail when:

```text
experts are too similar
router receives weak differential gradient
one expert can solve both features
metric confuses confident collapse with separation
```

## Metric-To-Claim

| metric | supports | cannot claim | next decision |
|---|---|---|---|
| heatmap diagonal / anti-diagonal | route-pattern separation | utility alignment | remove one favorable condition |
| heatmap one-column confident | confident collapse | feature specialization | inspect expert utility / usage |
| NMI / accuracy high | feature-route association | route confidence | inspect heatmap margin |
| NMI = 0 / accuracy = 0.5 | no top-1 association | exact cause | inspect gradient / expert gap |
| entropy low + one expert dominates | collapse | why collapse happens | inspect expert imbalance |
| loss low | task learned | routing caused learning | keep as sanity check only |

Primary metric:

```text
route-feature heatmap
```

Reason:

```text
It directly shows feature -> expert routing pattern.
```

## Rival Explanations

| rival | minimal observation |
|---|---|
| expressivity failure | hand-set diagonal router cannot make diagonal heatmap |
| optimization drift | initial separation disappears during training |
| expert imbalance | both features route to same expert while loss is good |
| shortcut / metric artifact | heatmap changes when suspected shortcut is balanced |
| weak differential utility | expert outputs are similar and router gradient is tiny |

## User Audit

Before using this theory, user must approve:

```text
hypothesis: first round tests route-pattern only
operational definition: diagonal/anti-diagonal heatmap counts as success
primary metric: route-feature heatmap
claim boundary: no utility-aligned claim
next decision: remove one condition at a time
```

