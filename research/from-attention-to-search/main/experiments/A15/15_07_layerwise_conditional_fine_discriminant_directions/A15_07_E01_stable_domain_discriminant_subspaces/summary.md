# Summary: A15_07_E01 Stable Domain Discriminant Subspaces

Primary Anchor: [A15_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md), SHA-256 `619472d7dfed41fe757967ccc62b549fe10d3a436905ec00b0fad70318f5360c`  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `EVIDENCE_COMPLETE_AWAITING_HUMAN_JUDGMENT`

## Result Snapshot

**Registered empirical outcomes:** controlled C4-expression `PASS`; controlled
C4-atom `PASS`; controlled spectral result `FUNCTIONAL_BAND_LOCALIZED`; natural
full-\(R_U\) entry `PASS` at block 24; natural shared-dimension hypothesis
`INSUFFICIENT_EVIDENCE`.

**Direct measurements:** at block 28, the frozen task-local rank-8 and shared
rank-56 spaces retained at least 0.988 of full-\(R_U\) gain by simultaneous 95%
lower bound on both fresh controlled panels. On C4-expression, spectral band 1
(TRAIN ranks 1–127 of identifiable rank 632) exceeded its matched
conditional-Haar overlap threshold and had positive simultaneous keep-only and
drop-one lower bounds for every controlled domain. On MASSIVE, block 24 cleared
the entry gate, but no task-local or shared 90%-retention lower-bound crossing
existed.

**Researcher judgment:** `AWAITING_HUMAN_JUDGMENT`  
**Updated judgment:** `AWAITING_HUMAN_JUDGMENT`  
**Next decision:** `AWAITING_HUMAN_JUDGMENT`

## Decision-Bearing Setup

- **Question:** do exact low-rank functional spaces survive unseen expressions
  and facts, where do they lie in the TRAIN \(R_U\) spectrum, and does analogous
  local-versus-shared dimension expansion transfer to natural intent data?
- **Treatment and controls:** full \(R_U\), frozen or learned supervised
  low-rank spaces, five PCA bands; duplicate-\(X\), mismatched-\(R_U\), label-null,
  and matched conditional-Haar controls.
- **Changed variable:** which part of \(R_U\) can affect the frozen fine-class
  correction.
- **Held fixed:** Qwen3-8B, blocks 24/28, same-token hook, split roles,
  residualization/classifier family, ranks, thresholds, and bootstrap plan.
- **Primary metric:** paired cross-entropy gain over \(X\)-only, in nats/example;
  retention is projected gain divided by admitted full-\(R_U\) gain.
- **Known limitation:** natural full gains are small enough that retention-ratio
  intervals are unstable; point-estimate rank curves cannot replace registered
  lower-bound crossings.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| C4-expression admission LCB \(>0\), task-rank-8 retention LCB \(>0.80\), shared-rank-56 retention LCB \(>0.90\) at one block | block 28: `0.0348`, `0.9879`, `0.9878` | corrected condition-specific simultaneous interval; Amendment 001 | `PASS` | [controlled table](tables/controlled_h1_corrected.csv) |
| C4-atom same rule | block 28: `0.0981`, `0.9922`, `0.9875` | corrected condition-specific simultaneous interval; Amendment 001 | `PASS` | [controlled table](tables/controlled_h1_corrected.csv) |
| Same band exceeds overlap q95 and has positive simultaneous keep-only or drop-one LCB | band 1; task/shared minimum keep LCB `0.01491`/`0.01493`; minimum drop LCB `0.01471`/`0.01472` nats/example | eligible only at H1-admitted block 28 | `FUNCTIONAL_BAND_LOCALIZED` | [controlled spectrum](tables/controlled_spectrum_block28.csv) |
| Natural full-\(R_U\) margin LCB above strongest control | block 24: full gain `0.01996`, control q95 `0.01010`, corrected margin LCB `0.00110` nats/example | block 28 numerically ineligible; not pooled | `NATURAL_ENTRY_PASS` | [natural entry](tables/natural_entry_corrected.csv) |
| Shared all-task 90% crossing exists and exceeds every local crossing | no local crossing and no shared crossing | final Amendment 005 rank truncation; missing crossings are not extrapolated | `INSUFFICIENT_EVIDENCE` | [natural curves](tables/natural_rank_curves.csv) |

## Key Evidence

1. The controlled result is a true held-out confirmation: old task rank 8 and
   shared rank 56 were frozen before two 1,920-row panels were opened.
2. Controlled function and direction agree on band 1. This locates the held-out
   correction but does not make PCA itself the supervised optimum.
3. Natural task-local rank-3 projector overlap is only `0.13%–0.37%`
   (`0.23%` mean), compared with a `0.073%` conditional-random baseline. This is
   eligible geometric evidence but not a confirmed functional dimension
   expansion.
4. Natural point estimates are near complete by local rank 3 and shared rank 15,
   but every registered 90% confidence crossing is missing. They remain
   descriptive.

## Central Figures

![Controlled held-out confirmation](figures/fig1_controlled_confirmation.png)

The three panels show admission margin, minimum-domain task-local retention,
and minimum-domain shared retention. Crosses mean the registered interval is
unavailable; they are not failures. Both fresh panels pass all three gates at
block 28.

![Controlled spectral localization](figures/fig2_controlled_spectral_localization.png)

The heatmaps show orientation overlap divided by matched random expectation;
the right panels show simultaneous held-out functional lower bounds. Only band
1 is both unusually aligned and functionally sufficient/necessary across every
controlled domain.

![Natural entry, rank curves, and geometry](figures/fig3_natural_entry_rank_geometry.png)

The left panel admits block 24. The center displays point estimates only and
explicitly records that formal 90% crossings are absent. The right panel shows
near-disjoint local directions in absolute overlap.

## Claim Boundary

Pending the researcher's closed-book judgment, the evidence record permits only
the following bounded statements:

- exact frozen supervised low-rank spaces survived both controlled held-out
  shifts at block 28;
- their controlled held-out correction function was localized to the first of
  five TRAIN spectral bands;
- MASSIVE block 24 contained a small positive candidate update beyond the
  matched controls, and its learned task-local directions had low pairwise
  overlap;
- MASSIVE did **not** establish a 90%-retention local/shared dimension ordering.

It cannot establish native causal use, new knowledge, a variance-only Router,
expert utility, LoRA mechanism, no forgetting, or universal transfer.

## Next Decision

**Decision:** `AWAITING_HUMAN_JUDGMENT`  
**Completion criterion:** the researcher supplies or confirms the five fields
`question`, `direct result`, `updated judgment`, `cannot claim`, and `next decision`.  
**Resume action:** after that confirmation, update this Summary, the Anchor and
active Focus consistently, then derive the meeting report. Do not infer that
decision from the figures alone.
