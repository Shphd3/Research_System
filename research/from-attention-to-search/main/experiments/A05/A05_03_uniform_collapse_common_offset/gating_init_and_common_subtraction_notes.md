# 05_03 Notes: Gating Initialization And Stable Common Subtraction

## 1. Current Understanding Of Gating Initialization

Most MoE routers use a trainable linear router:

```text
z = W_r h + b
p = softmax(z)
route = top-k(p)
```

In many implementations the router is initialized like an ordinary linear layer: small random weights, often zero or absent bias. Stability is then handled by routing design and training regularizers rather than by a mechanism-aware initialization.

Relevant families:

```text
1. Noisy top-k routing: add noise / exploration and use auxiliary balancing losses.
2. GShard / Switch-style load balance: encourage batch-level expert load to be near uniform.
3. Switch-style reduced initialization scale: smaller parameter init improves sparse-model stability.
4. ST-MoE router z-loss: penalize large router logits for numerical/training stability.
5. Loss-free balancing: dynamically add expert-wise routing bias based on recent load instead of gradient-based auxiliary loss.
```

## 2. What This Means For Our Toy Problem

Our question is more specific than generic MoE stability:

```text
Does a shared hidden component c create unequal w_e^T c under random linear routing?
```

So the relevant initialization target is not merely “small logits.” It is:

```text
w_1^T c = w_2^T c = ... = w_E^T c
```

preferably zero.

Reduced scale can reduce margin magnitude, but under hard top-1 it may not change which expert wins. Common-aware initialization directly removes the expert-specific common offset.

## 3. Practical Initialization Variants To Test

### Init A: Default random baseline

```text
W_r ~ PyTorch default Linear init
bias = False or zero
```

### Init B: Reduced-scale router init

```text
W_r <- gamma * W_r
```

Use `gamma in {0.1, 0.3, 1.0}` if needed.

Expected effect:

```text
smaller logits and softer gradients; hard top-1 argmax may remain unchanged.
```

### Init C: Common-orthogonal init

```text
w_e <- w_e - (w_e^T c / ||c||^2) c
rescale ||w_e|| to match original row norm
```

Expected effect:

```text
w_e^T c = 0 for every expert, so the initial common offset is removed.
```

### Init D: Common-score matched init

```text
adjust each row so w_e^T c = mean_j w_j^T c
```

Expected effect:

```text
all experts receive the same common contribution; feature residuals determine routing.
```

### Init E: Residual-subspace orthogonal rows

```text
project rows to c^perp, then orthogonalize rows within that residual subspace.
```

Expected effect:

```text
removes common offset and reduces row redundancy.
```

## 4. Stable Common Subtraction Options

Recommended order:

```text
1. Logit-level common-offset cancellation.
2. Frozen calibration residual routing.
3. Common-aware router-row initialization.
4. EMA / low-rank subtraction only after the above are understood.
```

### Best first option: logit-level correction

```text
c = mean hidden state on balanced calibration grid
a_e = w_e^T c
z'_e = z_e - a_e
```

Why this is stable:

```text
- does not alter expert input;
- targets exactly the hypothesized common offset;
- avoids per-batch noise;
- easy to compare against baseline.
```

### Second option: frozen calibration residual routing

```text
h_route = h - proj_c(h)
z = W_r h_route
expert input = h
```

Use a fixed balanced calibration grid to estimate `c`. Do not estimate `c` from the same batch used for routing in the first decisive experiment.

### Third option: common-row regularization

```text
L_common = Var_e(w_e^T c)
```

This allows the model to use common direction only if it uses it equally across experts.

## 5. Why Previous Batch Mean / SVD Could Be Unstable

Batch mean subtraction is unstable because:

```text
1. the estimator changes every batch;
2. it can remove task signal along with nuisance signal;
3. it creates train/eval mismatch if not carefully frozen;
4. top-1 argmax can flip sharply under small estimator noise.
```

Broad SVD removal is unstable because:

```text
1. top singular directions are not automatically nuisance directions;
2. k selection is arbitrary if not tied to source alignment;
3. removing high-energy directions may remove useful target information;
4. learned representation drift changes the subspace over training.
```

## 6. What To Test First

Minimal first experiment:

```text
baseline vs logit-level common-offset cancellation
same data
same seeds
same training
expert receives full hidden state
```

Success requires:

```text
early max_load decreases
final collapse rate decreases
target accuracy remains near baseline
```

Failure redirects to:

```text
expert utility audit
top-1 amplification / warmup
load-balancing variants
```
