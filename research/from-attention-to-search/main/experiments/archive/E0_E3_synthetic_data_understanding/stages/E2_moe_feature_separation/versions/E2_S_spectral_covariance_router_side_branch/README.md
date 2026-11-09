# E2-S Spectral Covariance Router Side Branch

This is a side branch of the E2 MoE feature-separation line.

Question:

```text
Can routing on the middle-to-late subspace of global hidden covariance produce more feature-aligned MoE routing than ordinary full-hidden routing?
```

Key constraint:

```text
Spectral projection routers use no LB loss.
The main ordinary-router comparison is full_hidden_lb.
```

Read order:

1. `purpose_card.md`
2. `execution_plan.md`
3. `summary.md`
4. `detailed.md`

Runnable implementation:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/e2_s_spectral_covariance_router_all_trigram_v1000.json
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_spectral_covariance_router.py
```

Current result:

```text
Negative side-branch result. Middle-to-late covariance projection preserves
readback but does not improve feature-aligned routing over full-hidden router
or same-dimensional random projection.
```
