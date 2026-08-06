# 07 Top-1 Sparse Proxy Result

Status: top-1 sparse MoE-style proxy completed.

Implementation:

```text
forward: only top-1 expert output is used
router gradient: through selected softmax gate
not naive argmax-only training
```

## Result

| condition | separated seeds | mean NMI | key observation |
|---|---:|---:|---|
| top1_known_good | 3/3 | 1.0 | router prior starts correct, training preserves separation |
| top1_no_router_prior | 1/3 | 0.333 | initial random top-1 often collapses and training amplifies it |
| top1_no_prior_no_expert_advantage | 1/3 | 0.333 | same lock-in pattern; no reliable separation |

Final summary:

| condition | seed | top1 A | top1 B | margin | NMI | accuracy | loss | pattern |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| top1_known_good | 0 | 0 | 1 | 0.4567 | 1.0 | 1.0 | 0.000004 | separated |
| top1_known_good | 1 | 0 | 1 | 0.4557 | 1.0 | 1.0 | 0.000004 | separated |
| top1_known_good | 2 | 0 | 1 | 0.4538 | 1.0 | 1.0 | 0.000004 | separated |
| top1_no_router_prior | 0 | 1 | 1 | 0.5661 | 0.0 | 0.5 | 0.000003 | collapsed |
| top1_no_router_prior | 1 | 0 | 1 | 0.3223 | 1.0 | 1.0 | 0.000013 | separated |
| top1_no_router_prior | 2 | 1 | 1 | 0.5640 | 0.0 | 0.5 | 0.000003 | collapsed |
| top1_no_prior_no_expert_advantage | 0 | 1 | 1 | 0.5863 | 0.0 | 0.5 | 0.000001 | collapsed |
| top1_no_prior_no_expert_advantage | 1 | 0 | 1 | 0.3641 | 1.0 | 1.0 | 0.000033 | separated |
| top1_no_prior_no_expert_advantage | 2 | 1 | 1 | 0.5826 | 0.0 | 0.5 | 0.000001 | collapsed |

## Interpretation

```text
Top-1 sparse routing is much more initialization-sensitive than soft mixture.
Without router prior, early top-1 choice can lock in.
Expert advantage alone did not reliably correct collapsed initial routing.
High margin can mean confident collapse, so heatmap + NMI are both required.
```

## Claim Boundary

Can claim:

```text
In this top-1 sparse proxy, router prior is important for reliable
route-pattern separation.
```

Cannot claim:

```text
full NTP behavior
utility-aligned specialization
that expert advantage alone is sufficient under top-1 sparse routing
```

## Evidence

```text
run_top1_sparse_proxy.py
tables/top1_sparse/
figures/top1_sparse/
notes/top1_sparse/
```

## Next

```text
Before NTP-style expansion, decide whether the target mechanism should include
router prior / exploration / load-balancing, because naive top-1 sparse routing
locks in early choices.
```

