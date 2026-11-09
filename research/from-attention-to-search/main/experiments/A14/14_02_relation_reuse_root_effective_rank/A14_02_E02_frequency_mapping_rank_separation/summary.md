---
experiment_id: A14_02_E02_frequency_mapping_rank_separation
status: completed
verdict: pass_noninferior
completed_date: 2026-07-26
---

# Summary: A14_02_E02 Frequency–Mapping Rank Separation

Primary anchor: [A14_02_01](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor.md)  
Protocol: [approved contract](protocol.md)

## Result Snapshot

**Verdict:** `pass_noninferior`.

**What we established:** in this registered common-mapping NTP task, lowering
target exact frequency from \(8\) to \(1\) did not force a meaningful increase in
frozen-readout ROOT functional rank. All 10 pairs were capability- and
rank-valid. Mean LowF-minus-HighF rank was \(0.2\) directions and its one-sided
95% upper bound was \(0.5\), below the preregistered two-direction margin.

**What the experiment shows:** a cell can be rare while its task direction is
supplied by a mapping learned across other surfaces. Frequency alone is not a
sufficient explanation of task-functional rank in this controlled setting.

**What we do next:** the E03 full run is parked. Its preregistered common-step
parameter-space stability gate failed in 0/10 seeds, so outside-common
parameter novelty is not currently identifiable without a new protocol.

## Purpose And Exact Setup

Sixteen aliases and seventeen entities called one seed-frozen common bijection
\(y=\pi(a)\). Four target cells per alias appeared once in `Common-LowF` and eight
times in `Common-HighF-Duplicate`. Seven target presentations were moved to or
from donor cells by an integer transportation table, leaving 1,535,744 total
presentations, 5,999 AdamW steps, and every alias/entity/answer/context marginal
unchanged. Eight different cells per alias had zero optimizer exposure and
formed the unseen-cell capability guard.

The model was a two-layer, one-head, width-64 causal Transformer trained with
full-position NTP cross-entropy. Ten paired seeds used the same initialization
within each LowF/HighF pair.

## Primary Metric

With the original output head frozen, ROOT was projected to a calibration-fit
ordered subspace:

\[
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
\]

The rank-selection split chose

\[
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le0.02\ \mathrm{nat},\ \Delta Acc_q\le0.01\},
\]

and the disjoint final test only validated that frozen rank. The paired decision
quantity was

\[
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}}.
\]

Observed ranks were:

- LowF: mean \(7.6\), range \(7\)--\(8\);
- HighF: mean \(7.4\), range \(7\)--\(8\);
- paired \(D_s=[0,1,0,0,-1,1,0,0,1,0]\);
- \(\bar D=0.2\), one-sided 95% interval endpoints \([-0.1,0.5]\);
- 10/10 pairs had \(D_s\le2\).

## Capability And Validity Evidence

- LowF unseen-cell accuracy: mean/min \(1.000/1.000\);
- HighF unseen-cell accuracy: mean \(0.9926\), min \(0.96875\);
- LowF target-new-context accuracy: 10/10 seeds at \(1.0\);
- final-rank replay passed in 20/20 runs;
- full-rank identity replay maximum absolute CE error: \(6.71\times10^{-8}\) nat;
- ROOT shuffle produced mean CE increases \(14.65\) nat (LowF) and \(14.42\) nat
  (HighF);
- 0/640 matched-rank random subspaces passed.

## Key Figures

### Exact frequency versus functional rank

![Exact frequency versus functional rank](figures/frequency_functional_rank.png)

**Metric:** frozen-readout ROOT functional rank, in directions.  
**Data:** ten paired seeds per condition.  
**How to read:** the two distributions remain in the same 7--8 direction band;
the paired non-inferiority statistic, not visual overlap alone, decides.  
**Allowed conclusion:** \(F=1\) did not force more than two additional directions.  
**Does not prove:** frequency is irrelevant in other tasks or scales.

## Claim Boundary

**Can claim:** in the registered controlled task, a low-frequency exact cell
that passed strict zero-exposure cross-surface reuse did not require a larger
answer-task ROOT functional subspace than its matched high-frequency version.

**Cannot claim:** the raw state is absolutely low rank; parameters and ROOT have
the same rank; independent mapping count is a universal causal law; rare facts
in natural language behave identically; NTP implies H9-F.

## Next Decision

Keep the E02 phenomenon result. Before retrying E03, define a stable common
parameter or functional space on calibration data under a new versioned
protocol; do not raise rank or change probes against the current confirmation
split.
