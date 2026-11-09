---
experiment_id: A15_11_E03H_counterfactual_utility_residual_tree_h100
status: EVIDENCE_COMPLETE
interpretation_status: HUMAN_CONFIRMED_AS_NON_OWNING_H100_SENSITIVITY
eligibility: E03H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY
completed: 2026-08-29
acp_job: pt-vkikyszj
run_stamp: 20260829T172910Z
resource_profile: h100-4-reserved
---

# Summary: Counterfactual Utility In A Progressive Residual Expert Tree

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)

Frozen Protocol: [protocol.md](protocol.md)

Detailed record: [detailed.md](detailed.md)

Raw machine result and interval ledger:

[results.json](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json)

Result status / eligibility: `ELIGIBLE`; the clean four-H100 run and both
producer/global completion audits passed. The researcher accepted the bounded
interpretation as collision-isolated, non-owning H100 sensitivity evidence
under the current Focus; it is not an execution of the eight-RTX-5090 contract.

## Result Snapshot

**Registered umbrella verdict:**
`GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`.

**Exact layered reading:** `MECHANISM_SUPPORTED`, but
`NO_UTILITY_GAIN`, `NO_HIERARCHY_GAIN_TASK`, and
`NO_HIERARCHY_GAIN_UTILITY`. The umbrella label is a registered fallback for
“the mechanism gate passes while a matched flat model matches or beats the
tree.” Because neither utility-supervision contrast passed, the supported
branch here is **generic nonlinear task routing is sufficient in this
generator**, not “utility is sufficient.” This registered fallback records the
flat model's fixed-budget success; it is not an equivalence or sufficiency
theorem.

The task-only hierarchy learned the registered work decomposition
\(C\rightarrow pA\rightarrow bB\): work endpoint normalized mean-squared error
(`NMSE`) was \(1.9403\times10^{-5}\), 95% paired-seed bootstrap interval
\([1.2147\times10^{-5},3.0740\times10^{-5}]\). Under the permutation-equivalent
wrong grouping, its endpoint was \(0.336926\), interval
\([0.334220,0.356077]\), near the registered \(1/3\) canonical-oracle reference.
That exact lower bound requires the balanced, stagewise oracle with exact
ancestor orthogonality and the doubly orthogonal rank-one pair used here; the
learned float32 run instead used overlap at most \(10^{-6}\) and the registered
\(1/3-10^{-4}\) guard. Its fail-minus-work
area-under-the-learning-curve (`AULC`) contrast was \(+0.053155\), interval
\([0.050140,0.054230]\). Thus the analytic grouping obstruction and its learned
work/fail reversal are supported.

That valid mechanism did not establish a tree advantage. In work,
\(A_T=A(F_{task})-A(H_{task})=-0.000082\), interval
\([-0.004211,0.002458]\). Direct counterfactual-utility supervision was worse,
not better: \(S_H=-0.012057\), interval \([-0.067979,-0.007610]\), and
\(S_F=-0.005792\), interval \([-0.007309,-0.000315]\). The `H_util` work
endpoint was \(0.167032\), interval \([0.166702,0.667786]\). The strongest observed
failure mode was endogenous utility-label/expert co-adaptation: hard top-one
routing starved unselected experts, balanced opposing residuals cancelled in
the selected expert, and stage freezing preserved the resulting missing
branch. This is a stage-local interpretation supported by the registered
contrast and ledgers; it is not a universal theorem about utility supervision.

No RTX-5090 experiment or shared 5090 Focus was executed by this result. E03H
is the collision-isolated four-H100 successor lane only.

## Decision-Bearing Setup

- **Question:** when the supplied parent-first residual factorization is
  correct, does a frozen \(1\rightarrow2\rightarrow4\) rank-one expert tree learn
  more efficiently than a parameter- and compute-matched flat nonlinear MoE,
  and does direct counterfactual-utility supervision add value?
- **Treatment and controls:** conditional tree (`H`) versus flat nonlinear
  routing (`F`), crossed with task-only (`task`) versus current-candidate
  counterfactual-utility (`util`) Router supervision.
- **Changed variables:** Router structure and Router supervision only.
- **Held fixed:** exact balanced work/fail generators, all four semantic leaves
  per batch, seven stored rank-one experts, Router parameter count, active
  expert count, initialization within seed, training/test streams, optimizer,
  steps, candidate-forward compute, and eight paired optimizer seeds.
- **Primary metric:** exact Gaussian/operator-expectation NMSE AULC over log
  cumulative training examples; lower is better. Endpoint NMSE is the
  fixed-budget guard. This exact operator evaluation replaces the registered
  finite frozen-bank estimator of the same Gaussian estimand; the audited
  deviation and the test bank's actual diagnostic use are in the
  [detailed record](detailed.md#3-protocol-freeze-conformance-and-deviations).
- **Independence and uncertainty:** eight paired optimizer seeds; 10,000
  paired whole-seed bootstrap draws from one shared index matrix, root seed
  `151124`.
- **Known limitation:** this is a four-state, zero-noise synthetic function
  system with a supplied hierarchy. It is not evidence of autonomous semantic
  discovery or Qwen language-model benefit.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Curated evidence |
| --- | --- | --- | --- | --- |
| Mechanism: `H_task` work endpoint \(\leq0.05\), fail endpoint \(\geq0.25\), fail-minus-work AULC CI lower bound \(>0\) | work \(1.9403\times10^{-5}\); fail \(0.336926\); AULC difference \(+0.053155\) \([0.050140,0.054230]\) | producer guards, independent frozen-code mask audit, and registered aggregate projection check passed | `MECHANISM_SUPPORTED` | [summary table](tables/summary_table.csv), [primary contrasts](tables/primary_contrasts.csv), [raw interval ledger](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json) |
| Tree utility effect in work: \(S_H\) AULC CI lower bound \(>0\) and endpoint no worse by \(>0.01\) | \(S_H=-0.012057\) \([-0.067979,-0.007610]\); endpoint contrast \(-0.167010\) \([-0.667769,-0.166681]\) | eligible | `NO_UTILITY_EFFECT_TREE_WORK` | [primary contrasts](tables/primary_contrasts.csv), [summary table](tables/summary_table.csv), [raw interval ledger](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json) |
| Flat utility effect in work: \(S_F\) AULC CI lower bound \(>0\) and endpoint guard | \(S_F=-0.005792\) \([-0.007309,-0.000315]\); endpoint contrast \(-4.2372\times10^{-5}\) \([-1.5913\times10^{-4},-6.2049\times10^{-6}]\) | eligible | `NO_UTILITY_EFFECT_FLAT_WORK` | [primary contrasts](tables/primary_contrasts.csv), [summary table](tables/summary_table.csv), [raw interval ledger](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json) |
| Task-only hierarchy gain in work: \(A_T\) lower bound \(>0\), median gain at least 5% of flat AULC, endpoint no worse | \(A_T=-0.000082\) \([-0.004211,0.002458]\) | eligible | `NO_HIERARCHY_GAIN_TASK` | [primary contrasts](tables/primary_contrasts.csv) |
| Hierarchy gain under utility in work: corresponding \(A_U\) rules | \(A_U=-0.009689\) \([-0.065236,0.000670]\); endpoint contrast \(-0.166996\) \([-0.667270,-0.166608]\) | eligible | `NO_HIERARCHY_GAIN_UTILITY` | [primary contrasts](tables/primary_contrasts.csv), [summary table](tables/summary_table.csv), [raw interval ledger](/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/e03/results.json) |
| Admission | 8/8 seeds, 64/64 cells, four rank receipts, producer rank/freeze/load/compute/oracle/completion guards, independently audited mask, and aggregate \(10^{-6}\) projection check | producer, independent code, and global audits passed | `PASS` | [oracle ledger](tables/oracle_ledger.json), [detailed record](detailed.md#3-protocol-freeze-conformance-and-deviations) |

## Key Evidence

The stagewise task-only result is the decisive mechanism evidence:

| Condition / model | Stage 0 endpoint | Stage 1 endpoint | Stage 2 endpoint |
| --- | ---: | ---: | ---: |
| work `H_task` | 0.666669 | 0.333340 | \(1.9403\times10^{-5}\) |
| fail `H_task` | 0.666669 | 0.666947 | 0.336926 |
| work `F_task` | 0.666669 | 0.333339 | \(1.0398\times10^{-5}\) |
| fail `F_task` | 0.666669 | 0.333342 | \(3.1083\times10^{-5}\) |

The hierarchy therefore realizes the correct decomposition and follows the
wrong-tree near-floor reference, while the matched nonlinear flat model solves
both generators at the same budget. Utility-supervised work endpoints split
into optimizer modes:
`H_util` had one near-zero seed, four near-\(1/6\) seeds, and three near-\(2/3\)
seeds. The exact seed ledger and append-only companion visualization are in
[detailed.md](detailed.md#86-append-only-companion-seed-failure-diagnostic).

## Claim Boundary

### Can claim

- The supplied correct \(p\)-first factorization is exactly realizable by the
  progressive rank-one tree. In the registered balanced stagewise oracle, the
  paired wrong grouping with exact ancestor orthogonality and the canonical
  doubly orthogonal rank-one pair has a \(1/3\) lower bound; the learned run
  passes only the registered tolerance-aware guard around that reference.
- The learned task-only tree reproduces that work/fail separation across the
  eight registered optimizer seeds.
- In this controlled generator and fixed budget, the matched generic nonlinear
  Router also reaches near-zero error; no registered hierarchy-efficiency gain
  is established. This is not an equivalence result.
- The registered online counterfactual-utility supervision provides no gain
  and induces seed-dependent missing-expert modes in this implementation.

### Cannot claim

- That natural-language semantics have this hierarchy, or that a network can
  discover it without the supplied structural mask.
- That hierarchy is generally useless, or that every alternative utility
  objective must fail.
- That routing to the best current expert is equivalent to learning a complete
  expert candidate set.
- That Qwen's native Router uses these variables or that the method improves
  language-model loss.
- That the concurrently owned RTX-5090 lane or its Focus has been executed or
  closed.

## Next Decision

**Decision:** E03H is admitted as non-owning H100 sensitivity evidence. The
sole A15_11 next decision is to freeze a frequency (high/low) by cross-child
gradient-consistency (high/low) representation-formation test before another
Router intervention.

**Completion criterion:** the successor contract holds total tokens, target
positions, parent/child counts, vocabulary, templates, and label entropy fixed
and defines frozen measurements for gradient consistency, parent between-class
energy, held-out fifth-percentile normalized margin, and discriminant-subspace
spectral location.

**Resume action:** retain the structural work/fail mechanism and the negative
hierarchy/utility results under the non-owning sensitivity label, then use the
current Focus/Anchor to design the \(2\times2\) successor. Do not launch it before
a new confirmed Anchor and Protocol.
