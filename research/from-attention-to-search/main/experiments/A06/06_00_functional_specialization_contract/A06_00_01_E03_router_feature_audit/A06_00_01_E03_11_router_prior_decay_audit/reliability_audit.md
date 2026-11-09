# Reliability Audit: H0528a Router Prior Decay Audit

## 1. Artifact Validity

| Check | Result |
|---|---|
| H0527a final checkpoints exist | pass, 8 / 8 |
| H0527a intermediate checkpoints exist | fail, not saved by H0527a |
| Step-0 routers reconstructable | pass |
| Final `model.pt` loadable | pass |
| Calibration and eval splits separated | pass |
| Recentered router fitted only on calibration hidden states | pass |
| Eval uses router input before MoE dispatch | pass |

## 2. Boundary Correction

The original H0528a purpose card proposed auditing steps:

```text
0, 200, 400, 800, 1200, 1600
```

Actual available model checkpoints support only:

```text
step 0 reconstruction
step 1600 final checkpoint
```

Therefore this run is valid as a final-checkpoint prior-decay audit, but not as a full trajectory checkpoint replay.

## 3. Main Validity Result

Primary comparison:

| Condition | Recentered-current NMI | Trained-final NMI | Unused semantic gap |
|---|---:|---:|---:|
| random_init | 0.2126 | 0.0452 | 0.1674 |
| semantic_context_init | 0.3040 | 0.0422 | 0.2618 |

This validates the central diagnostic:

```text
semantic boundary remains recoverable in final hidden states but is not used by trained router.
```

## 4. Forced Utility Caveat

Forced utility uses:

```text
gate_mode = router_prob
```

So forced expert output is:

\[
p_e(h)E_e(h)
\]

This matches the actual selected-gate sparse path, but it is not a pure expert-only utility test. A future audit may set:

```text
gate_mode = one
```

to ask whether expert functions differ when gate probability is removed.

## 5. Residual Risk

The recentered semantic router is an offline diagnostic, not a trainable router. High recentered NMI only proves recoverability of B-context structure under this construction; it does not prove training would preserve it.

The forced utility margin is measured on the same final model; it does not prove the margin was small throughout training.
