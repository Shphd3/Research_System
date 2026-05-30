# Metric Definitions For 0531 Gating Auto Research

## 1. Primary Metric Bundle

不能用单个指标证明 specialization。主判据是 bundle：

```text
route-slot NMI
+ assignment-utility agreement
+ forced expert loss diagonal margin
+ train stability
+ inference stability
+ target CE / accuracy non-regression
```

## 2. Metrics

### route-slot NMI

Question:

```text
route assignment 是否与 target-deciding feature 对齐？
```

Supports:

```text
feature-aligned routing
```

Cannot claim:

```text
selected expert 对该 feature 有 causal utility
```

Failure caught:

```text
route 被 B identity / common / frequency factor 控制，而不是 slot/target feature
```

### route-B NMI / conditional B-NMI

Question:

```text
route 是否被 surface token identity 或 B identity 控制？
```

Supports:

```text
identity shortcut diagnosis
```

Cannot claim:

```text
低 B-NMI 不代表 functional specialization 成功
```

### assignment-utility agreement

Definition:

```text
selected route == utility-best expert/path
```

where utility-best is computed by forced expert loss or ablation utility at the target position.

Question:

```text
router 选中的 path 是否是对 prediction causally useful 的 path？
```

Cannot claim alone:

```text
route 按 slot 分。高 Assign-Utility 可能来自所有 samples 共用同一个 utility-best path。
```

### forced expert loss diagonal margin

For slot $s$ and expert $e$:

$$
L_{s,e}=CE(y|force\ route=e, s).
$$

Diagonal margin:

$$
M=\frac{1}{|S|}\sum_s \left(\min_{e\ne e_s} L_{s,e}-L_{s,e_s}\right).
$$

Question:

```text
是否形成 slot-specific expert utility？
```

Cannot claim:

```text
如果 route-slot NMI 低，则 expert 可能有 utility 但 router 没选它。
```

### train stability

Compute over last checkpoints $T_K$:

```text
route-slot NMI std
assignment-utility std
route map flip rate
expert load entropy drift
```

Success:

```text
final performance high and last-checkpoint variation small
```

Failure:

```text
只在中间 checkpoint 对齐，最后被 NTP wash out
```

### inference stability

Perturbations:

```text
same slot, different B identities
slot-preserving common-component noise
frequency-rank reshuffle
small hidden-state Gaussian noise
batch-order / seed rerun
```

Metric:

```text
route consistency under target-preserving perturbation
```

Success:

```text
target-deciding feature unchanged时 route mostly unchanged
```

Failure:

```text
route 对 common/B/noise 更敏感，而不是对 slot/target feature 敏感
```

## 3. Minimal Report Table

```markdown
| Experiment | Model | Target Acc | Route-Slot NMI | Route-B NMI | Assign-Utility | Forced Diag Margin | Train Stability | Inference Stability | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
```

## 4. Claim Rules

```text
High CE / accuracy only -> task learned, not specialization.
High route-slot NMI only -> route aligned, not functional.
High Assign-Utility only -> selected path useful, but may be collapse.
High route-slot NMI + high Assign-Utility + diagonal forced utility -> supported synthetic feature-level specialization.
Add stability metrics -> candidate for practical routing mechanism.
```
