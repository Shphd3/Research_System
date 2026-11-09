# Figure contracts

## Figure 1 — NLL trajectory

- **Question:** Does Local-HMT outperform a target-motion-matched random local subspace during and at the end of 10B-token training?
- **Metric/unit:** Held-out next-token negative log likelihood, nat/token; lower is better.
- **Data:** The same 1,024 frozen validation documents at all registered milestones; seeds 17 and 29 are shown separately.
- **Axes:** x is cumulative training tokens in billions; y is held-out NLL. Color identifies Centered-Full, Local-HMT, or Local-Random-Matched.
- **Allowed conclusion:** Describes when arm differences appear and whether they persist to 10B.
- **Limitation:** The trajectory is descriptive; the registered decision uses the 10B paired document-level contrast.

## Figure 2 — Endpoint paired contrasts

- **Question:** At 10B, is the HMT identity better than its motion-matched random counterpart, and is a generic dynamic subspace better than Centered-Full?
- **Metric/unit:** Mean per-document NLL difference, nat/token, with 2,000-draw paired bootstrap 95% intervals.
- **Axes:** x is left-arm minus right-arm NLL; negative favors the named left arm. y lists seed and contrast.
- **Allowed conclusion:** Covariance identity is supported only if both Local-HMT-minus-Random intervals lie below zero and tracking comparability passes.
- **Limitation:** Two seeds constrain the registered model and training setting, not a population of architectures.

## Figure 3 — Tracking comparability

- **Question:** Was the random identity control as easy for the online updater to track as Local-HMT?
- **Metrics:** Final deployed-target mean squared cosine overlap for U64/U320 and fraction of noninitial refreshes selecting gamma zero; all are unitless in [0,1].
- **Axes:** x compares HMT and Random; y is the named tracking metric; marker identifies seed.
- **Allowed conclusion:** Protects the identity contrast from a target-tracking difficulty confound.
- **Limitation:** Similar tracking summaries do not prove identical Router optimization or expert formation.
