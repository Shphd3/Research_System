# Meeting Brief: Real-DCLM Proxy Gating Initialization

## One-Sentence Result

We can find a real-data proxy feature and initialize a router from it, but ordinary DCLM training erases that routing almost immediately; the next problem is preservation, not utility binding.

## Why We Ran This Iteration

The synthetic experiments showed that if feature labels exist, residual clustering and pseudo-center initialization can work. Real language data has no feature labels. So the first real-data question was:

```text
Can we create a measurable proxy feature, use it to initialize routing, and keep it during training?
```

## What Each Anchor Answered

### A06_10: Proxy Feature Exists

Question:
Do real DCLM hidden states contain stable label-free proxy clusters?

Answer:
Yes, with boundary.

Evidence:
Step-10 late-layer residual proxy stability NMI is 0.5451, while random is 0.0002. Frequency and position do not explain the signal.

Boundary:
Raw and residual k-means are nearly identical, so common-centering is not the reason clusters appear.

### A06_11: Proxy Can Initialize A Router

Question:
Can proxy centers become linear top-1 router rows?

Answer:
Yes, with boundary.

Evidence:
Step-0 raw-center raw-input proxy-route NMI is 0.7449, while random is 0.0343.

Boundary:
Residual centers work well only in centered-input diagnostics. Actual raw-input routing prefers raw centers.

### A06_12: Training Does Not Preserve The Proxy

Question:
Does ordinary DCLM training preserve the initialized proxy routing?

Answer:
No.

Evidence:
Raw-center proxy-route NMI starts at 0.7549, falls to 0.0410 by step 5, and is 0.0131 at step 10. LM loss remains comparable to random.

Boundary:
This does not mean the proxy is useless. It means the current training objective does not protect it.

### A06_13: First Failure Is Training Feedback

Question:
Where did the pipeline first fail?

Answer:
The first failed contract is training preservation, $a(0)\to a(t)$.

Evidence:
Proxy discovery passes, the linear bridge passes, and only the training trajectory fails.

## Current Research State

Known:

- real proxy structure exists;
- step-0 proxy routing can be initialized;
- ordinary LM training destroys the proxy route;
- loss does not prevent this destruction.

Not known:

- whether preservation can be enforced;
- whether preserved proxy routing has expert utility;
- whether utility-aware initialization helps.

## Decision

Do not run utility binding as the next mainline experiment. Utility binding requires stable proxy routing. Since A06_12 failed preservation, A06_14 and A06_15 are parked.

## Next Experiment

The next anchor should test preservation / anti-feedback:

```text
Can a modified training schedule or objective keep raw-center proxy routing through step 10?
```

The most natural first tests are:

- router freeze or delayed router updates;
- lower router learning rate;
- proxy-route preservation auxiliary loss;
- common/load anti-collapse regularization.
