# A06_03_02_E01 Result Summary: Learned-Specialist Wrong-Rank Correction

## Conclusion

Native weighted top-1 does not recover a learned useful expert from either
initial rank 2 or rank 4 in 300 router-only full-LM updates. Correction is
0/128 task-seed cells at both ranks, with zero majority-boundary changes. An
identically initialized soft mixture corrects 128/128 cells: median sustained
correction time is 29 updates at rank 2 and 98 updates at rank 4.

At rank 4, the paired top-1-minus-soft capped correction-time penalty is 203
updates with seed-clustered 95% confidence interval \([202,205]\). The normalized
cumulative-regret difference is 0.7387 with 95% confidence interval
\([0.7342,0.7416]\). The utility-coverage control is therefore supported.

The result is stronger than the fixed-expert A06_02_03_E02 rank-search picture. On
this learned full-sequence LM surface, wrong-rank top-1 is a selected-path blind
basin: rank 2 is no easier than rank 4. The remaining causal ambiguity is
whether the basin is intrinsic to selected-only expert feedback or is sustained
by background-position gradients in the full LM objective.

## Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Useful expert | Learned specialist with lowest forced task loss | expert \(u(f)=f\) | functional route target | natural semantics |
| Wrong-rank start | Useful expert begins below top-1 | requested rank 2 or 4 | tests identity correction | natural occurrence frequency |
| Sustained correction | Useful expert is top-1 on at least 95% of task positions for five updates | \(T_{corr}\) | excludes transient crossing | permanent stability |
| Capped time | Non-corrected cells receive value 301 | \(\widetilde T_{corr}\) | retains failures in comparison | full survival analysis |
| Normalized cumulative regret | Time-average routing loss above useful-expert floor, normalized by initial excess | \(NR\) | training-efficiency evidence | wall-clock efficiency |
| Utility coverage | Expert outputs that enter the forward loss | one selected output vs all four outputs | tested mechanism | equal activated compute |

## Exact Setup

- Four equally frequent context-defined modular tasks; instruction \(f\) at the
  sequence start defines later target \((c+f)\bmod4\).
- Length-33 sequences; all 32 next-token positions enter the training loss.
- One causal-attention layer, residual plus LayerNorm, no learned positional
  embedding, four MLP experts, fixed readout.
- Specialists/generalists rebuilt with 200 expert-only exposure updates.
- Experts and representation frozen during correction; router-only full-batch
  SGD, learning rate 0.001, 300 updates.
- One score ladder \([0.75,0.25,-0.25,-0.75]\); only expert identities are
  permuted to create useful ranks 1, 2, and 4.
- Weighted top-1 and soft mixture start from the exact same router tensor.
- Formal evidence: 32 seeds and 128 task-seed cells per condition.

## Primary Evidence

| Specialist condition | Correction rate | Median capped time | Median boundary changes | Final task loss | Normalized regret |
| --- | ---: | ---: | ---: | ---: | ---: |
| top-1, rank 1 | 1.000 | 0 | 0 | 0.0244 | 0.2239 |
| top-1, rank 2 | 0.000 | 301 | 0 | 6.3844 | 1.0133 |
| top-1, rank 4 | 0.000 | 301 | 0 | 6.3817 | 1.0132 |
| soft, rank 1 | 1.000 | 0 | 0 | 0.0648 | 0.3299 |
| soft, rank 2 | 1.000 | 29 | 1 | 0.0755 | 0.1552 |
| soft, rank 4 | 1.000 | 98 | 1 | 0.1178 | 0.2750 |

The rank-4 top-1-minus-soft contrasts are:

| Paired metric | Median | Seed-clustered 95% CI |
| --- | ---: | ---: |
| Capped correction-time difference | 203 updates | \([202,205]\) |
| Normalized cumulative-regret difference | 0.7387 | \([0.7342,0.7416]\) |

Rank-2 and rank-4 top-1 trajectories are statistically indistinguishable:
their capped-time difference is 0 with CI \([0,0]\), and regret difference is
\(-1.31\times10^{-5}\) with CI crossing zero. H1 rank-mediated top-1 correction
is rejected. H2 soft utility-coverage advantage is supported.

## Central Figures

### Correction Coverage

![Useful-expert correction curves](figures/useful_expert_correction_curves.png)

- **Question:** Does the useful learned expert become top-1?
- **Read:** Lower means more cells have sustained correction.
- **Observed:** Soft rank 2 and 4 reach zero uncorrected cells; top-1 rank 2 and
  4 overlap at 100% uncorrected.
- **Take-home:** Learned wrong-rank top-1 does not perform the sequential search
  observed in the fixed-expert toy.
- **Limitation:** The full-LM gradient mixes task and background positions.

### Training Regret

![Normalized regret trajectory](figures/normalized_regret_trajectory.png)

- **Question:** Does routing approach the useful-expert task floor?
- **Observed:** Soft rank 4 reduces normalized excess to about 0.025 by update
  300. Both wrong-rank top-1 curves increase slightly above 1.
- **Take-home:** The contrast is functional, not only geometric.
- **Limitation:** The soft condition uses four utility-bearing expert paths.

### Rank-4 Search Dynamics

![Rank-4 identity search](figures/rank4_identity_search.png)

- **Observed:** Soft raises useful probability from about 0.102 to 0.575 and
  crosses one majority boundary. Top-1 lowers it to about 0.088 and never
  changes majority identity.
- **Take-home:** The current selected path suppresses rather than discovers the
  useful unselected specialist.
- **Limitation:** This does not yet identify which loss-position population
  supplies the suppressive gradient.

## Controls And Validity

- Specialist median held-out utility gap: 8.8947.
- Generalist median gap: -0.0042.
- Minimum train/test useful-rank accuracy: 1.000.
- Minimum p05 adjacent score gap: 0.4724.
- Initial top-1 load spread: 0.
- Maximum train center-score error: \(1.97\times10^{-4}\).
- Top-1/soft and non-router state errors: 0.
- Rank-1 top-1 and soft stability: 128/128.
- Generalist arbitrary-target correction: 0/128 for top-1 and soft.

The generalist control matters: soft routing does not geometrically force
expert id \(f\) when all experts are functionally interchangeable. Soft correction
in the specialist condition therefore depends on learned expert function.

## Hypothesis Update

| Hypothesis | Verdict | Meaning |
| --- | --- | --- |
| Top-1 correction becomes slower from rank 2 to rank 4 | Rejected | both wrong ranks remain trapped |
| Soft utility coverage improves rank-4 correction and regret | Supported | 128/128 vs 0/128; both paired CIs decisive |
| No material sparse-feedback bottleneck | Rejected | correction and regret gaps are large |
| Correction is only geometric relabeling | Weakened | generalist arbitrary target never corrects |

## Claim Boundary And Next Decision

**Supported:** On this learned context-task bridge, selected-only weighted top-1
can preserve a correct route but cannot discover the useful specialist from
rank 2 or 4 within 300 full-LM router updates. Forward exposure to all expert
outputs removes the observed blind basin.

**Not supported:** Natural-language semantic specialization, from-scratch
feature discovery, production superiority of soft routing, or the claim that
all top-1 MoE implementations have permanent lock-in.

**Next decision:** Decompose the full-LM router gradient into task-position and
background-position components from the same wrong-rank state. If task-only
top-1 still fails while task-only soft corrects, explicit candidate utility
coverage is necessary on this bridge. If task-only top-1 corrects but full-LM
top-1 fails, the method target becomes semantic-credit weighting, with MTP as a
candidate source of long-horizon route credit.

