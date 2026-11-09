# A06_04_01_E01 Result Summary

## Verdict

**Failed on the registered surface.** The experiment is complete and
numerically valid, and the native model does use relevant context relative to
length-matched nuisance context. A held-out expert-by-context interaction is
also detectable. However, the calibration-selected expert identity is not
stable across the two calibration halves, and the context-favored expert does
not have the registered positive absolute headroom over native routing.

This is a scientific failure of the joint hypothesis, not an infrastructure or
power failure.

`REL` means relevant retrieved cross-file context, `NUIS` means an equally long
context from a different repository, and `LOCAL` means no cross-file context.
Expert headroom \(H\) is native NLL minus matched-swap NLL, so positive \(H\) means
the candidate expert improves target prediction. A 95% confidence interval
(CI) is the repository-clustered bootstrap uncertainty range.

## Decisive Results

| Clause | Result (nats / target token) | Registered rule | Verdict |
| --- | ---: | --- | --- |
| Native context gain, \(L^{NUIS}-L^{REL}\) | 0.20370, 95% CI [0.05908, 0.35929] | CI lower bound \(>0\) | Pass |
| Calibration identity | \(a=49\), \(b=53\); \(a\) ranks 8th on cal-A but 16th on cal-B | \(a\) top-8 and \(b\) bottom-8 on both halves | Fail |
| Held-out interaction, \(I_{ctx}\) | 0.01163, 95% CI [0.00336, 0.02022] | estimate \(\ge0.01\) and CI lower bound \(>0\) | Pass |
| Relevant absolute headroom, \(H_{49}^{REL}\) | 0.00540, 95% CI [-0.00105, 0.01225] | estimate \(\ge0.01\) and CI lower bound \(>0\) | Fail |
| Numerical and completeness guards | 256/256 samples, 128/128 experts, all finite; replay/no-op error 0 | all guards pass | Pass |

The positive interaction does **not** mean that native routing missed a useful
context expert. On test, expert 49 changed little between contexts:

\[
H_{49}^{REL}-H_{49}^{NUIS}=0.00082.
\]

Most of \(I_{ctx}\) came from expert 53 becoming more harmful under relevant
context:

\[
H_{53}^{REL}-H_{53}^{NUIS}=-0.01081.
\]

The absolute-headroom guard therefore performed its intended role: it stopped
a context-dependent **bad-expert avoidance** effect from being reported as
missed positive expert utility.

![Primary context and headroom result](artifacts/primary_context_and_headroom.png)

## Native Loss and Routing Diagnostics

Held-out native mean NLL was `LOCAL=1.97503`, `REL=2.12697`, and
`NUIS=2.33067`. Relevant context significantly recovers loss relative to
length-matched nuisance context, but it does not establish a net improvement
over local-only context: \(L^{LOCAL}-L^{REL}=-0.15193\), 95% CI
[-0.29636, 0.00012].

For aligned target-predicting positions, the mean full-probability route
overlap was 0.03174, native top-8 Jaccard was 0.76412, and final-MoE-input
distance was 26.1267. These only show that contextual representations and some
routing decisions differ; they do not rescue the failed functional criteria.

Across experts, test-set REL and NUIS headroom rankings were strongly similar
(Spearman 0.891), while calibration context shifts were poorly reproducible
between cal-A and cal-B (Spearman 0.083).

![Calibration instability](artifacts/calibration_stability.png)

## Claim Boundary and Updated Belief

Supported:

- Qwen3-Coder's final MoE expert functions have measurable context-dependent
  counterfactual effects on CrossCodeEval.
- Relevant evidence is better than equally long irrelevant evidence for native
  target NLL.
- Context interaction alone is insufficient evidence of useful specialization.

Not supported:

- a stable context-favored expert with positive native-Router headroom;
- a learned Router that would improve this workload;
- faster rare learning, common-information preservation, or conflict isolation;
- generalization to other layers, models, languages, or million-token context.

**Exactly one next decision:** do not construct a new Router from this frozen
last-layer oracle result; next test whether training-time selective sharing can
*create* stable positive context-conditioned utility on a real rare/common
workload.

Canonical metrics: [primary_metrics.json](artifacts/primary_metrics.json).
Complete setup and evidence ledger: [detailed.md](detailed.md).
