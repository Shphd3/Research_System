# 0518 Report: Why MoE Routers Do Not Naturally Learn One-Feature-One-Expert, And Whether That Helps Retrieval

## 1. Main Message

The safest conclusion is:

```text
In the controlled synthetic trigram setting, the model can learn the features,
and supervised router signals can produce one-feature-one-expert routing.
However, natural NTP training does not produce this specialization.

Moreover, even perfect one-feature-one-expert routing is not sufficient
to become an efficient and reliable KV retrieval index in the current setup.
```

This splits the mainline into two questions:

1. Why does the natural router not learn `one feature -> one expert`?
2. If we force `one feature -> one expert`, does it make index retrieval efficient and reliable?

The first question is not fully closed, but several wrong explanations are now ruled out. The second question is clearer: in the current setup, the answer is no.

## 2. Research Goal

The long-term goal is to test whether:

```text
an MoE router can act as a model-native index,
assigning different context features to different experts or buckets,
and thereby supporting efficient KV retrieval.
```

The intended chain was:

```text
controlled data features
-> learned feature representations
-> feature-aligned expert routing
-> feature-aligned buckets retrieve the KV states needed by attention
```

The 0518 results show two breaks in this chain:

- Representation separability does not imply feature-aligned router specialization.
- Feature-aligned router specialization does not imply a good KV retrieval index.

## 3. Line A: Why Does The Natural Router Not Learn One-Feature-One-Expert?

### 3.1 Experimental Setup

The data contains synthetic trigram features:

| feature | relation |
|---|---|
| ABC | `[1,2] -> 22` |
| DEF | `[3,4] -> 23` |
| GHI | `[6,7] -> 20` |
| JKL | `[8,9] -> 21` |

The model is a tiny causal Transformer with a 4-expert top-1 MoE FFN. The training objective is next-token prediction.

We tested three explanations:

| experiment | question | conclusion |
|---|---|---|
| E2-B3 prototype centers | If each expert has a trainable center $c_e$, will routing naturally become feature-aligned? | No. Centers receive gradients and move, but do not align to features. |
| E2-C contrastive router representation | If router representations become more separable, is that sufficient? | No. Feature labels are linearly readable, but expert assignment is still not clean. |
| E3 failure-mode diagnostic | What explains natural routing? | It is better explained by hidden geometry / router projection than by human feature labels. |

### 3.2 Key Result 1: Prototype Centers Receive Gradients But Do Not Naturally Specialize

We fixed the hard top-1 gradient issue by multiplying the selected expert output by its gate value:

$$
\begin{aligned}
e^* &= \arg\max_e p_{t,e}, \\
y_t &= p_{t,e^*}\,\mathrm{Expert}_{e^*}(h_t).
\end{aligned}
$$

This allows the NTP loss to update expert centers $c_e$.

Results:

| variant | first prototype grad | readback | NMI | best-perm acc |
|---|---:|---:|---:|---:|
| natural NTP | 0.0050 | 0.9957 | 0.5772 | 0.5000 |
| center separation | 0.0706 | 0.9955 | 0.1924 | 0.3333 |
| supervised CE | 4.1205 | 0.9969 | 1.0000 | 1.0000 |

Interpretation:

- Under natural NTP, centers do receive gradients and move.
- But they do not naturally become four feature centers.
- Center separation pushes centers apart, but does not assign feature clusters to different centers.
- Only supervised CE reliably reaches `NMI=1`.

![E2-B3 prototype gradient](figures/e2b3_prototype_grad_norm_over_steps.png)

![E2-B3 routing matrix](figures/e2b3_routing_matrix_by_variant.png)

### 3.3 Key Result 2: Features Are Readable, But The Router Does Not Use Feature Labels

In E3, feature labels are linearly readable from hidden states:

```text
feature-linear-probe = 1.0
```

However, feature labels alone do not predict the router's expert choices well:

| dataset / no-LB | feature-linear-probe | feature-only -> expert | router-projection -> expert | PCA-only -> expert |
|---|---:|---:|---:|---:|
| unique | 1.000 | 0.539 | 0.973 | 0.941 |
| shared-B | 1.000 | 0.510 | 0.984 | 0.968 |
| shared-target | 1.000 | 0.435 | 0.963 | 0.908 |
| crossed-factorial | 1.000 | 0.457 | 0.978 | 0.957 |

This means:

```text
The model internally distinguishes the features.
The router is not random.
But it learns a different low-loss partition of hidden space,
not the human-defined ABC/DEF/GHI/JKL one-to-one partition.
```

![E3 predictor crossed](figures/e3_predictor_accuracy_crossed.png)

### 3.4 Conclusion For Line A

We can rule out:

- The feature was not learned.
- The model or code cannot specialize.
- Prototype centers do not receive gradients.
- Representation separability alone is sufficient.

The stronger explanation is:

```text
NTP only requires next-token prediction.
If some hidden-geometry partition or redundant expert utility is enough to reduce loss,
the router does not need to map human feature labels to experts one-to-one.
```

This question is not fully closed. We still need to explain why the natural router chooses its particular low-loss partition, and what pressure would make feature-aligned routing necessary.

## 4. Line B: If One-Feature-One-Expert Holds, Does It Become A Good KV Index?

### 4.1 Experimental Setup

R3 is an upper-bound test:

```text
Instead of waiting for natural specialization,
we force perfect one-feature-one-expert routing using RouterFeatureCE.
```

Mapping:

```text
ABC -> expert 0
DEF -> expert 1
GHI -> expert 2
JKL -> expert 3
```

Then we test whether these feature-aligned buckets can retrieve the high-mass KV positions used by block2 full attention.

### 4.2 Key Result: Perfect Feature Routing Is Still Not A Good KV Index

The premise succeeds:

| Dataset | NMI | ARI | fixed-label routing | feature readback acc |
|---|---:|---:|---:|---:|
| uniform | 1.000 | 1.000 | 1.000 | 1.000 |
| longtail | 1.000 | 1.000 | 1.000 | 1.000 |

But retrieval does not succeed. On feature queries:

| Dataset | K | Router recall | Random recall | Local recall | Router mass | Local mass |
|---|---:|---:|---:|---:|---:|---:|
| uniform | 1 | 0.310 | 0.279 | 0.404 | 0.346 | 0.681 |
| uniform | 2 | 0.536 | 0.530 | 0.680 | 0.528 | 0.838 |
| longtail | 1 | 0.328 | 0.298 | 0.433 | 0.378 | 0.735 |
| longtail | 2 | 0.582 | 0.580 | 0.746 | 0.614 | 0.887 |

The result:

```text
Perfect feature routing is only slightly better than random,
and clearly worse than the same-count local baseline.
```

![R3 uniform retrieval](figures/r3_uniform_perfect_router_topk_recall_mass_l2_baselines.png)

![R3 longtail retrieval](figures/r3_longtail_perfect_router_topk_recall_mass_l2_baselines.png)

### 4.3 Conclusion For Line B

In the current synthetic all-trigram setup:

```text
one-feature-one-expert is not sufficient for KV retrieval.
```

This means R1/R2 did not fail only because the natural router lacked specialization. Even with perfect feature specialization, the high-mass KV positions needed by attention are not mainly grouped by feature labels.

More likely variables are:

- locality;
- token identity;
- hidden similarity;
- value/output similarity;
- head-specific attention patterns.

## 5. Overall Interpretation

The current mainline should be:

```text
We originally wanted to treat the MoE router as a feature index.
The experiments show that this requires two additional conditions:

1. the router must actually form a feature-aligned partition;
2. the feature-aligned partition must retrieve the KV states needed by attention.

In the current synthetic trigram setting, neither condition naturally holds.
```

Short version:

```text
feature representation separability does not imply router specialization;
router specialization does not imply a KV retrieval index.
```

## 6. Claim Boundary

Supported claims:

- In the controlled synthetic trigram setting, natural top-1 routing does not automatically form clean one-feature-one-expert.
- With feature supervision, the model can form clean routing.
- Even perfect feature routing is not sufficient for efficient KV retrieval in the current setup.
- The next step should diagnose what variables explain high-mass attention KV positions.

Unsupported claims:

- Real LLM MoEs do not learn semantic experts.
- MoE routers can never act as retrieval indexes.
- Feature specialization has no retrieval value in all tasks.

## 7. Next Step

The next priority is attention source decomposition:

```text
locality / token identity / hidden similarity / value similarity / feature identity
```

We need to measure how much attention mass each variable explains.

We should also run a utility gap test:

```text
learned router vs feature-oracle router vs best-utility router
```

If the feature-oracle router is not better than the learned router, then one-feature-one-expert is a human-desired partition, not a necessary solution for the current NTP/attention mechanism.

## 8. 30-Second Update

My main question is whether the MoE router can become a feature index and then support KV retrieval. I separated this into two questions. First, why does the router not naturally learn one-feature-one-expert? E2/E3 show that the feature is readable from hidden states and supervised routing can reach `NMI=1`, but natural NTP does not turn the feature into an expert assignment. Second, if we force perfect feature routing, does retrieval work? R3 says no: perfect router buckets are only slightly better than random and much worse than local retrieval. So the current conclusion is: feature separability does not imply router specialization, and router specialization does not imply a KV index. Next, I need to diagnose what actually explains the high-mass KV positions in dense attention.
