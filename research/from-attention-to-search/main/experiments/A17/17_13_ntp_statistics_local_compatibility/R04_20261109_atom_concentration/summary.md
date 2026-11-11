# R04: atom concentration and learning

Status: seven arms analyzed. Researcher judgment: Unknown. Interpretation is an AI proposal.

Question: does concentrating repeated low-frequency SAE atoms improve held-out learning, rather than merely correlate with it? A6 adds router-only conditional order-3 entropy regularization; A5 replaces token clustering with frozen atom coactivation groups. Architecture, initialization, data order, optimizer and2000-update budget match A0.

| arm     |     总体NLL |     M中位数 |   频次加权logM |        bin0 |        bin1 |        bin2 |
|:--------|------------:|------------:|---------------:|------------:|------------:|------------:|
| A5      | 4.039118998 | 1.344967711 |   -0.080334963 | 3.720251498 | 3.872186784 | 3.865717683 |
| A0      | 4.083141622 | 1.010460056 |   -0.401735217 | 3.794580477 | 3.942305977 | 3.929827148 |
| A1-deep | 4.085093112 | 0.870828768 |   -0.360922850 | 3.789857108 | 3.930946271 | 3.917200750 |
| A4      | 4.129441802 | 0.810891851 |   -0.472061195 | 3.867186691 | 4.009898194 | 3.986286052 |
| A1      | 4.157604347 | 0.585752336 |   -0.453948743 | 3.901086299 | 4.028563391 | 3.998681224 |
| A6      | 4.174997252 | 0.924780174 |   -0.284026317 | 3.985564060 | 4.104733180 | 4.059321536 |
| A2      | 4.286027700 | 0.256798644 |   -1.345580429 | 4.187885924 | 4.277627418 | 4.202913688 |

For the existing five arms, A1 minus A2 overall NLL=-0.128423353; A1 minus A0=+0.074462725. Atom-median concentration ordering matches NLL ordering, but count-weighted log concentration changes that ordering. Neither correlation establishes a training benefit through gradient noise. See the [source NLL table](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/A1_eval_nll_by_step.csv) and [concentration table](/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/out/B3_Mbar_distribution.csv).

| arm     |   learned |   forgotten |   net_forgotten |   chi_mean |   position_flip_rate |
|:--------|----------:|------------:|----------------:|-----------:|---------------------:|
| A0      |     29281 |         212 |             236 |   0.407636 |             0.392096 |
| A1      |     29244 |         181 |             526 |   0.197567 |             0.198141 |
| A2      |     29553 |         130 |             275 |   0.002753 |             0.002755 |
| A4      |     29295 |         212 |             158 |   0.560060 |             0.569260 |
| A1-deep |     29277 |         171 |             120 |   0.275392 |             0.262880 |
| A6      |     29525 |         133 |             381 |   0.771362 |             0.762490 |
| A5      |     29229 |         199 |             547 |   0.082039 |             0.088713 |

Ledger comparisons use matched1000-to2000 intervals in addition to each arm's available adjacent intervals. Fixed scores retain changing load bias; zero route flips are an empirical prediction, not a definition. Loss-change significance uses paired position SE, BH q<.05 and an absolute0.01nat threshold, for atoms with at least50 occurrences. Net forgetting additionally corrects selection of the preceding minimum. Position independence within documents is not established.

The [Chinese Summary](summary_cn.md) and [1111 report](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/atom_concentration/report_cn.md) contain exact P1–P4 readings and declared insufficiency. Boundaries: one seed;2000 updates; teacher exposure to training tokens; circularity of optimizing and evaluating the same dictionary;98.962% bf16-vs-fp32 teacher Top32 index agreement; missing old250-step states; non-bitwise MIG reruns; fp16 storage rounding. Conditional atom NLL is not semantic acquisition. [Detailed](detailed.md) owns provenance. Next scientific decision: Unknown.


| prediction   | AI_assessment                                                                                                                                                                                                        |
|:-------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P1           | NOT_SUPPORTED_OR_MIXED: concentration change A6-A0=-0.085679882; per-bin changes and reference magnitudes in prediction_metric_fluctuation.csv                                                                       |
| P2           | INSUFFICIENT: overall A6-A0 NLL=+0.091855630; low-bin differences=[0.19098358296192108, 0.1624272028831233, 0.12949438803992175]; metric-specific adjacent-checkpoint reference in prediction_metric_fluctuation.csv |
| P3           | DIRECTIONALLY_SUPPORTED: A5-A1 concentration=+0.759215375, NLL=-0.118485348; joint direction and metric-specific fluctuation conditions applied                                                                      |
| P4           | NOT_SUPPORTED as a blanket prediction: fixed-score A1 flips19.81% of position-level route sets; high-chi quartiles do not uniformly forget most. Causal attribution remains insufficient.                            |

The quantitative definitions and precise execution details are in the [English Detailed](detailed.md). All researcher judgments remain Unknown.
