# Theory Iteration: Why Uniform Features Can Still Collapse

## 1. Starting Belief

Initial belief:

If feature frequency is uniform, there should be no common component capable of
making many different features route to the same expert.

Audit correction:

This belief mixes two meanings of "common":

1. frequency common: some feature appears more often;
2. representation common: hidden states for different features share a large
   vector component.

The audit supports the second meaning, not the first.

## 2. Operational Definitions

Feature:

- intended feature for this line: `slot`;
- exact diagnostic feature: `(slot,B)`.

Routed position:

- `b_position = 15`, immediately before the target token at position 16.

Feature centroid:

$$
h_f(t)=\mathbb{E}[h(x,t)\mid f]
$$

Common direction:

$$
c(t)=\frac{\frac{1}{F}\sum_f h_f(t)}
{\left\|\frac{1}{F}\sum_f h_f(t)\right\|}
$$

Residual feature direction:

$$
r_f(t)=h_f(t)-\frac{1}{F}\sum_f h_f(t)
$$

This `common direction` is a hidden-state mean direction. It is not a frequency
vector and not a label count.

## 3. Hypothesis 0: Collapse Is Caused By Feature-Frequency Imbalance

### Mathematical Model

If feature frequency is the only common source, then under uniform features:

$$
P(f)=\frac{1}{F}
$$

and if feature representations are centered:

$$
h_f=u_f,\quad \frac{1}{F}\sum_f u_f\approx 0
$$

then a random top-1 router should assign features close to balanced random
buckets, up to finite-sample noise.

For 1024 features and 4 experts, the random baseline max load should be close
to 0.25. The measured Monte Carlo p99 is about 0.288.

### Experiment

Check counts in:

- fixed train set;
- training batches sampled with replacement;
- exact feature-variant eval grid.

### Result

Slot is exactly uniform:

- train fixed dataset: each slot has 5000 rows;
- feature-variant eval: each slot has 4096 rows.

Exact `(slot,B)`:

- train fixed dataset is finite-sample approximate because `B_i` is sampled;
- feature-variant eval is exactly uniform: every `(slot,B)` has 16 variants.

However, step-0 feature routing on the exact eval grid still has full-hidden
max load:

- `R0-dot/20260522`: 0.691;
- `R0-cos/20260522`: 0.686;
- `S1-cos/20260522`: 0.892.

### Hypothesis Update

Frequency imbalance is not a sufficient explanation. It may add finite-sample
noise in the train fixed set, but it is not necessary for the observed step-0
load concentration.

## 4. Hypothesis 1: Router Random Initialization Is Buggy

### Mathematical Model

A bug would mean the router starts with a systematic expert preference, such as:

$$
z_e(h)=w_e^\top h+b_e
$$

with a nonzero shared bias $b_e$, or with non-random identical rows.

### Experiment

Check model code and initialization statistics.

### Result

The router is:

```text
Linear(d_model, num_experts, bias=False)
```

For `R*` conditions, router rows are PyTorch default random weights. Example
`R0-dot/20260522`:

- row norms: `0.589 0.542 0.562 0.577`;
- pairwise cosine mean: `-0.0002`;
- bias exists: `0`.

For `S*` conditions, the router is intentionally overwritten by slot-centroid
initialization. Example `S1-cos/20260522`:

- row norms: `4.000 4.000 4.000 4.000`;
- pairwise cosine mean: `-0.333`;
- init type: `slot_centroid_overwrite`.

### Hypothesis Update

No router-initialization software bug was found. Random initialization is not
"bad" in the sense of being incorrectly implemented. The problem is that
ordinary random rows are not neutral when the input hidden states have a large
nonzero common direction.

## 5. Hypothesis 2: Random Rows Project A Large Hidden Common Direction

### Mathematical Model

Let each feature centroid decompose as:

$$
h_f=c+u_f
$$

where $c$ is shared across features and $u_f$ is feature-specific residual.

For dot-product routing:

$$
z_{e,f}=w_e^\top h_f=w_e^\top c+w_e^\top u_f
$$

Define:

$$
a_e=w_e^\top c
$$

If one expert has a larger $a_e$, then it gets a constant score advantage for
many features. Collapse appears when:

$$
a_{e^*}-a_e
>
w_e^\top u_f-w_{e^*}^\top u_f
$$

for many $f$ and competing experts $e$.

For cosine routing the same structure remains, but scores are directional:

$$
z_{e,f}=\tau\cdot
\cos(w_e,h_f)
$$

If $h_f$ directions are dominated by $c$, the expert most aligned with $c$
receives many unrelated features.

### Experiment

Route exact feature centroids at step 0 in two ways:

1. full hidden: use $h_f$;
2. residual-only: use $h_f-\bar h$.

Then compare full vs residual max load and compare both to random bucket
baseline.

### Result

For seed `20260522`:

| Condition | Full Hidden Max Load | Residual-Only Max Load |
|---|---:|---:|
| `R0-dot` | 0.691 | 0.308 |
| `R1-dot` | 0.691 | 0.308 |
| `R0-cos` | 0.686 | 0.298 |
| `R1-cos` | 0.686 | 0.298 |
| `S1-cos` | 0.892 | 0.274 |

Random isotropic baseline p99 for 1024 features and 4 experts is about 0.288.

### Hypothesis Update

The hidden common direction explains the main step-0 concentration pattern.
After subtracting the mean feature centroid, routing becomes much closer to
load-matched random behavior.

## 6. What Is The Common Direction Physically?

### Tested Sources

The audit compared the hidden common direction to:

- fixed position 15 embedding;
- raw input vector at the `B` position;
- mean `B` token embedding;
- background token embedding;
- prefix position mean;
- slot-code token mean.

### Result

For `R0-dot/20260522`:

| Candidate Source | Cosine To Hidden Common |
|---|---:|
| raw input at B position | 0.973 |
| position 15 embedding | 0.971 |
| position + mean(B) | 0.973 |
| mean(B token embedding) | -0.006 |
| background embedding | -0.068 |
| mean(slot-code embedding) | -0.092 |

### Hypothesis Update

The common direction is mainly a routed-position/template direction. It is not
mainly the average `B` identity, not slot frequency, and not background token
frequency.

Physical interpretation:

All routed tokens are read at the same pre-target position. Before any feature
separation is learned, their hidden states share a strong role vector: "this is
the token position used to predict the next target." Random router rows then
score this shared role vector differently. The expert with the largest score
on this role vector receives many unrelated features.

## 7. Hypothesis 3: Top-1 Training Amplifies The Early Winner

### Mathematical Model

Top-1 selected routing updates only the selected path:

$$
e^+(h)=\arg\max_e z_e(h)
$$

The selected expert and its router row receive the strongest task-coupled
signal for the selected tokens. If many features are initially selected by the
same expert, training can increase that expert's advantage:

$$
w_{e^+}(t+1)\approx w_{e^+}(t)-\eta\nabla_{w_{e^+}}L
$$

while under-selected experts receive weaker or different updates.

### Experiment

Run a 10-step local diagnostic for selected conditions and record:

- max route load;
- dominant expert;
- router row gradient norm;
- movement from initialization.

### Result

Examples:

- `S1-cos/20260522`: max load starts at 0.875, reaches 0.987 by step 10.
- `R0-dot/20260522`: max load starts at 0.661; dominant expert can switch by
  step 10, showing early dynamics are not purely static.
- `S1-cos/20260523`: early load reaches 0.932 by step 10 in this local replay,
  but the earlier checkpoint audit showed this seed can later recover.

### Hypothesis Update

Training amplifies early geometric imbalance, but early high load alone is not
a sufficient condition for final collapse. The safer statement is:

> Step-0 geometry selects a likely winner; top-1 training can lock it in unless
> later dynamics or regularization redistribute routing.

## 8. Paper Intuitions

These papers do not prove our toy mechanism, but they explain why the mechanism
is plausible and why many MoE systems add balancing/stabilizing machinery.

| Paper | Relevant Intuition |
|---|---|
| Shazeer et al., 2017, "Outrageously Large Neural Networks" https://arxiv.org/abs/1701.06538 | Sparsely-gated MoE already needed noisy gating and load-balancing terms because gating can concentrate work on a few experts. |
| Lepikhin et al., 2020, "GShard" https://arxiv.org/abs/2006.16668 | Large sparse MoE uses auxiliary load-balancing losses to avoid uneven expert use. |
| Fedus et al., 2021, "Switch Transformers" https://arxiv.org/abs/2101.03961 | Switch uses simple top-1 routing but keeps an auxiliary load-balancing loss because top-1 routing is not naturally balanced. |
| Lewis et al., 2021, "BASE Layers" https://arxiv.org/abs/2103.16716 | Balanced assignment reframes routing so token-to-expert allocation is explicitly constrained rather than left to unconstrained argmax. |
| Zhou et al., 2022, "Mixture-of-Experts with Expert Choice Routing" https://arxiv.org/abs/2202.09368 | Expert-choice routing lets experts choose tokens under capacity, which directly targets load balance. |
| Zoph et al., 2022, "ST-MoE" https://arxiv.org/abs/2202.08906 | Router stabilization, including router-specific regularization, is treated as necessary for stable sparse expert training. |

Initialization intuition:

There is probably no universal "good random init" that works independently of
the hidden-state distribution. A better init must be neutral with respect to
the actual router input distribution. In this experiment, that means matching
or removing the common score $w_e^\top c$ across experts.

## 9. Updated Hypothesis

Updated conclusion:

Uniform feature frequency does not imply balanced top-1 routing. Balanced
routing also requires the feature centroids at the routed position to be
centered or for router rows to be neutral along the shared hidden direction.

Current mechanistic hypothesis:

1. all features share a large pre-target position/template hidden component;
2. random router rows assign different scores to this shared component;
3. the expert with the largest common score receives many features at step 0;
4. selected-expert top-1 training can amplify this early load into collapse.

Claim boundary:

This is a mechanism explanation, not a solved intervention. The next experiment
must intervene on the common score or early load to test causality.

## 10. Next Decision

The next smallest decision is:

> Should the first anti-collapse intervention remove the common score at the
> router input, or should it keep the input unchanged and force balanced early
> routing?

Recommended order:

1. router-input centering: route on $h_f-\bar h$ or batch/EMA-centered hidden;
2. common-score-neutral initialization: enforce equal $w_e^\top c$ at step 0;
3. early load-balance warmup or softened/noisy top-1 before hard routing.

Decision criterion:

If common-score removal prevents step-0 to step-50 lock-in while preserving
target accuracy, the common-direction hypothesis becomes causal evidence. If it
does not, the next rival explanation is training-time utility or expert-output
gradient asymmetry.
