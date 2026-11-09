---
experiment_id: A15_06_E03_30b_single_seed_extension
status: complete
scientific_verdict: complete_seed17_persistence_with_relay_failure
last_updated: 2026-08-09
---

# Final result summary

All six seed-17 continuations reached 30B tokens with complete paired endpoint
evidence.  Local-HMT had the lowest DCLM NLL (3.391913), beating Centered-Full
by 0.004072 nat/token [0.002555, 0.005586 better] and Local-Random by 0.004886
[0.003359, 0.006425 better].  Relay-HMT was worse than Local-HMT by 0.015617
[0.014139, 0.017159] and worse than Centered by 0.011545 [0.009926, 0.013140].

The result establishes persistence only within seed 17.  It does not rescue a
cross-seed covariance-identity claim because the registered seed-29 10B result
did not reproduce that ordering.  The later A16 audit also showed that the
logged LB auxiliary value was detached from backward in these source runs;
their model comparison is valid, but it is not evidence about effective LB
regularization.

The complete eight-task evaluation is reported in
[A15_06_E04](../A15_06_E04_30b_downstream_evaluation/summary.md).

