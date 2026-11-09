# A06_03_04_E03 Tail-Safe Utility Certificate: Summary

## What We Established

The 10th-percentile and lower-10% conditional-value-at-risk utility rules both
pass the preregistered stopping contract. Each reaches `128/128` correction,
`128/128` retention, zero premature stops, and zero generalist false triggers.
The 10th-percentile rule saves a median `51.0%` of the 600 allowed audition
updates; lower-CVaR10 saves `43.0%`.

The decisive result is that population-mean utility was not Pareto-optimal.
Protecting the lower utility tail removes its `24/128` premature stops while
retaining substantial counterfactual-expert compute savings.

## Terminology And Primary Decision

For incumbent expert \(e\), challenger \(c\), and routed state \(h\), define the
per-token forced-loss difference

\[
D_{e,c}(h)=\ell(E_c(h))-\ell(E_e(h)).
\]

Positive values favor the incumbent. The mean rule stops when every directed
expert pair has positive mean \(D\). The tail rules replace the mean with either
the 10th percentile \(Q_{0.10}(D)\) or

\[
\operatorname{CVaR}^{low}_{0.10}(D)
=\mathbb E[D\mid D\le Q_{0.10}(D)].
\]

The primary metric is premature-stop rate: the fraction of task cells for
which audition stops before sustained useful-expert correction. It decides
whether the rule is safe in this controlled system. It does not establish
pretrained-LLM or systems safety.

## Exact Setup

- Reused A06_03_04_E02 rank-4 learned specialists, full-sequence LM loss, and the same
  four-task context-defined next-token data.
- Frozen experts and representation; router-only SGD at learning rate `0.001`.
- At most 600 continuous two-expert audition updates, followed by ordinary
  top-1 through update 800.
- All 12 directed expert pairs had to be observed and positive for nine stable
  updates before stopping.
- 32 seeds, four tasks per seed, 128 paired task cells per condition.
- Four-H100 ACP job `pt-oul045lr`; run
  `a06_45_full_4gpu_20260711_01`; state `SUCCEEDED`.

## Primary Results

| Stop rule | Correction | Retention | Premature stop | Trigger rate | Median stop | Median saving |
|---|---:|---:|---:|---:|---:|---:|
| Mean | 127/128 = 99.22% | 100% | 24/128 = 18.75% | 100% | 220.5 | 63.25% |
| q25 | 128/128 = 100% | 100% | 9/128 = 7.03% | 100% | 245.5 | 59.08% |
| q10 | 128/128 = 100% | 100% | 0/128 | 93.75% | 294.0 | 51.00% |
| lower-CVaR10 | 128/128 = 100% | 100% | 0/128 | 65.63% | 342.0 | 43.00% |
| task-oracle q10 | 128/128 = 100% | 100% | 0/128 | 100% | 264.5 | 55.92% |

Both q10 and lower-CVaR10 exceed the required 90% correction/retention, at
most 5% premature stopping, at least 30% median saving, and below 10%
generalist false-trigger rate. q25 misses only the safety threshold.

## Central Figures

![Tail-certificate reliability and saving](figures/tail_certificate_tradeoff.png)

- **Question:** Does lower-tail aggregation remove premature stopping without
  losing useful audition savings?
- **How to read:** The left panel compares correction and premature-stop rates;
  the right panel compares median saving against the 30% requirement.
- **Observed:** q10 and lower-CVaR10 have full correction, zero premature stop,
  and saving above 30%.
- **Take-home:** A lower-tail certificate dominates the unsafe mean rule on the
  registered reliability contract.
- **Does not prove:** Wall-clock speedup, many-expert scalability, or robustness
  when experts and representation continue training.

![Tail-certified phase-switch dynamics](figures/tail_stop_margin_trajectories.png)

- **Question:** How does a more conservative certificate change the route
  trajectory?
- **How to read:** The y-axis is median useful-expert margin. Later bends mark
  later switching from two-expert audition to top-1.
- **Observed:** q10 and lower-CVaR10 delay switching relative to the mean while
  ending at positive, retained margins.
- **Take-home:** The extra safety comes from waiting for lower-tail utility, not
  from changing the learned specialists or initial route state.
- **Limitation:** Median trajectories hide cell-level failures; the primary
  premature-stop table remains the decision evidence.

## Hypothesis Update

- **H1 tail-safe certificate:** supported; q10 and lower-CVaR10 pass.
- **H2 mean is Pareto-optimal:** rejected; safe tail rules retain 43--51% median
  saving.
- **H3 task-position tail is required:** rejected; all-position q10 passes.
- **H4 token tail is the wrong unit:** rejected on this controlled surface.

## Claim Boundary And Next Decision

**Established:** A label-free, all-position lower-tail utility statistic can
safely terminate continuous two-expert audition in the controlled frozen
specialist system.

**Not established:** Joint expert/representation training, natural semantic
specialization, pretrained-LLM transfer, many-expert statistics, communication
cost, or downstream efficiency.

Do not add another synthetic certificate refinement. The next anchor should
test the upstream workload premise: whether repository-level code completion
contains stable counterfactual expert-utility heterogeneity large enough to
justify a semantic Router at matched activated compute.
