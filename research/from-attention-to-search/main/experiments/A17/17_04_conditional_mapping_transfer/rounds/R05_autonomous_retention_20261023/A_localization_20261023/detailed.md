# A localization: complete evidence record

[Summary](summary.md) · [Frozen Protocol](protocol.md) · [R05 Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/anchor.md). Scientific ownership is unchanged. No Focus/Anchor state or original 1200-update utility gate is changed. Factual reporting is complete; researcher mechanism judgment and next scientific decision remain Unknown. Suggestions are AI_PROPOSAL.

## Eligibility and actual computation

All 40 planned interventions and one baseline completed and passed measurement guards. They qualify for local finite-perturbation probability sensitivity in this model and dataset. Necessity for old-rule correctness remains unresolved. Process analysis covers U/TS × three continuation orders × nine points = 54 existing evaluations and is post hoc on exposed DEV. Candidate replacement, cross-task reuse, and functional-preservation interventions are NOT RUN.

The reading paths are behavior and controls; parameter coordinates rather than new representation fitting; and functional intervention with measurement quality. The record follows the requested starting-state, process, and candidate-decision dependencies.

Mode one maps command 甲 to the first word and 乙 to the last. Mode two reverses the mapping. Each answer is one token, predicted across the entire vocabulary of 151,936 IDs. DEV contains 800 old and 800 new answers. Each mode has two panels, unseen order and unseen combination, each with 200 answers per command. No fitting occurs here, but DEV was exposed by earlier evaluations and is not a fresh confirmation set.

The model is Qwen3-0.6B Base with the acquired-old adapter. The original continuation changes four layer-27 query/key/value/output matrices, 6,291,456 parameters. U applies no directional protection; TS attenuates candidate optimizer displacement by a coefficient decreasing from 0.1 to 0.01. This constrains parameter coordinates rather than fixing the computation produced by an old-mode input. The [prior A audit](../a_stage_audit.md) owns exact update formulas, original source locations, and cumulative displacement accounting.

For matrix j, singular value decomposition (SVD) is performed on **the complete acquired-old W0,j**, not the old-task parameter increment. Its top 16 paired unit rank-one atoms are Aj,i = uj,i vj,i^T. The projection is Pj(X) = Σi〈Aj,i,X〉Aj,i and C0,j = Pj(W0,j). This spans 16 scalar coordinates per matrix, 64 in total, rather than the entire 16-by-16 left/right product space. R denotes the complement.

Draw d uses a unit coefficient vector zj,d and Dj,d = Σi zj,d,i Aj,i. The intervention is W±,j = W0,j ± ρ‖C0,j‖F Dj,d/‖Dj,d‖F. Random controls replace the atoms with independently drawn orthonormal left/right frames while preserving coefficients and each matrix's displacement norm. All four matrices change together, so their individual causal contributions are not identified. See [probe.py](/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/analysis/A_localization_20261023/probe.py:43).

Doses are ρ=0.001 and 0.003; direction seeds are 1701–1705; both signs are tested. The 2×5×2×2 design yields 40 interventions plus one baseline. Joint C0 norm is 22.6734065 and joint W0 norm 76.5711037. Joint perturbation norms are approximately 0.0226734/0.0680202, or 0.02961%/0.08883% of full W0. Original parent loading, native-prefix cache, Projector, and evaluation are reused from retained retention.py; the bounded perturbation and analysis are added separately.

## Freeze, conformance and provenance

| Item | Actual evidence | Qualification |
| --- | --- | --- |
| Scope and resources | User-selected A localization; one reserved H100 | No training, other stage, or alternative candidate |
| Conditions | 40/40 plus baseline, no added doses/draws | No failed condition substitution |
| Starting identity | All 1600 predictions and CE match original update 0 exactly | Maximum CE discrepancy 0 |
| Numeric guards | Per-matrix actual norm error ≤0.1%; C perturbation complement leakage <0.1% | Every condition passes; raw conditions.json retains values |
| Pre-forward freeze | 02:51:32.761899 UTC binds Protocol, source, configs, parent state, retained implementation | Saved before the first model forward |
| Aggregation implementation | Metric and paired bootstrap were fixed in Protocol; analysis source hash recorded 02:53:26 UTC with 40 outputs present | Entire aggregation code was not sealed before data existed |
| Process analysis | 54 existing readouts; update 2 from prior read-only supplemental evaluation | Post hoc, not an original training prediction |
| Concentration check | Added after observing primary results | Descriptive stress check; no primary exclusions |
| Endpoint | Original update 1200 retained | Coverage landmarks do not replace utility qualification |
| Training and restoration | No optimizer/gradients/updates; in-memory restoration exact | No new trained checkpoint; directions.pt stores bases only |

Reserved-H100 job `pt-j1zvgh90` was created 2026-10-23 02:50:35 UTC, started 02:51:25, and succeeded at 02:52:49. Forward program time was 70.07 seconds; peak allocated GPU memory 2,658,246,656 bytes. Runtime: shphd-lite-0911, PyTorch 2.3.0a0+6ddf5cf85e.nv24.04, CUDA 12.4. The previous update-2 recovery-evaluation job belongs to the prior audit and is not counted as a new job in this round. Receipts and source hashes are in the [execution directory](/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/analysis/A_localization_20261023).

## Metrics, denominator and uncertainty

Cross entropy (CE) is minus log correct-answer probability, in nats per answer. Primary sensitivity takes |CE(W±)−CE(W0)| per old answer before averaging signs, 800 answers, and five fixed draws. Signed CE and accuracy are secondary; cancellation of signed effects does not remove absolute sensitivity. Full-vocabulary accuracy uses the global highest-scoring ID and denominator 800.

Each panel contains 200 disjoint unordered word groups, each with two commands; the two panels have no overlapping groups. Each of 2000 bootstrap replicates samples 200 groups per panel with replacement, carries both commands, applies the same sampled groups to both compared conditions, and averages panels equally. Intervals condition on one parent and fixed directions or continuation order. Direction variation is separately reported. Ten dose/draw comparisons are correlated and have no multiplicity adjustment; repeated evaluations do not create independent examples or acquired-old models.

The Protocol's consistent-sensitivity reading requires both doses and all five draws to agree. Actual agreement is 4/5, so the supported observation is an average signal rather than universal direction consistency. The secondary gold-minus-opposite-rule logit margin cannot replace the primary metric merely because its result is more uniform.

## Complete starting-state results

The [two pooled rows](tables/probe_pooled_2.csv), [ten contrasts](tables/probe_contrasts_10.csv), [20 sign-averaged conditions](tables/probe_sensitivity_20.csv), and [40 individual conditions](tables/probe_conditions_40.csv) retain all measurements.

In units of 10^-6 nats/answer, C/random sensitivities are 0.946671/0.409733 and 2.832300/1.235694; ratios 2.31046/2.29207. Conditional 95% intervals for the differences are [0.084024,1.330114] and [0.250841,3.825309]. Counter-draw 1702 gives 0.328662/0.647177 and 1.006387/1.941464, ratios 0.50784/0.51836. Both doses favor C in 4/5 draws.

Old accuracy is 100% in all 40 conditions: no old-rule prediction error is observed. Baseline old CE is 0.000691032 nats/answer and baseline new accuracy is zero. New-mode probe readouts therefore do not establish reuse of an acquired new function. Every raw JSON retains both modes. Secondary absolute gold/opposite-rule margin sensitivity favors C in all five draws but remains secondary.

### Concentration and a real example

A post-hoc check finds that `dev/old/甲/11-10-2` contributes 62.95%/62.84% of total C sensitivity; five answers contribute 84.34%/84.31%. Per-answer counts C>random, random>C, and equal are 280/23/497 and 364/37/399. Equal FP32 CE changes do not establish identical output distributions.

For command 甲 and list “狗 猫 蓝”, the correct old answer is “狗”. Top draw 1701 at ρ=0.003, positive sign, changes CE from 0.373940587 to 0.376725644 and probability from 0.6880178 to 0.6861043, while the predicted answer stays “狗”. This illustrative case was selected post hoc for maximal sensitivity; it is not a representative average answer.

After excluding that entire two-command group, 798 answers remain; equal-panel C/random ratios are 2.2460/2.2427. This is a concentration stress check, not a new primary analysis: the original 800-answer result is retained. Source: concentration.py and sensitivity_concentration_posthoc.json.

## Complete process classifications

Six mutually exclusive categories exhaust every pair: same old-rule answer; same new-rule answer; both correct under their respective modes; same middle word; same outside-list word; and different-other answers. The final category can contain one-sided correctness and is not an outside-list count. Each U/TS count below has denominator 800. [All 54 rows](tables/process_54.csv) retain old/new accuracy and CE separately; both-correct counts cannot substitute for single-mode accuracy.

| seed | update | same-old U/TS | same-new U/TS | both correct U/TS | middle U/TS | outside U/TS | different-other U/TS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 29 | 0 | 799/799 | 0/0 | 0/0 | 0/0 | 0/0 | 1/1 |
| 29 | 1 | 797/797 | 0/0 | 2/2 | 0/0 | 0/0 | 1/1 |
| 29 | 2 | 755/755 | 3/3 | 40/40 | 0/0 | 0/0 | 2/2 |
| 29 | 16 | 396/396 | 377/377 | 7/7 | 8/8 | 0/0 | 12/12 |
| 29 | 50 | 279/279 | 441/442 | 26/26 | 28/28 | 0/0 | 26/25 |
| 29 | 120 | 18/18 | 761/761 | 5/5 | 7/7 | 0/0 | 9/9 |
| 29 | 240 | 8/9 | 777/781 | 3/0 | 6/7 | 0/0 | 6/3 |
| 29 | 600 | 1/1 | 796/794 | 0/1 | 1/3 | 0/0 | 2/1 |
| 29 | 1200 | 0/0 | 800/800 | 0/0 | 0/0 | 0/0 | 0/0 |
| 43 | 0 | 799/799 | 0/0 | 0/0 | 0/0 | 0/0 | 1/1 |
| 43 | 1 | 792/792 | 0/0 | 6/6 | 0/0 | 0/0 | 2/2 |
| 43 | 2 | 725/725 | 4/4 | 69/69 | 0/0 | 0/0 | 2/2 |
| 43 | 16 | 381/381 | 374/374 | 5/5 | 19/19 | 7/7 | 14/14 |
| 43 | 50 | 313/312 | 427/427 | 20/20 | 16/16 | 0/0 | 24/25 |
| 43 | 120 | 17/17 | 770/769 | 3/3 | 4/4 | 0/0 | 6/7 |
| 43 | 240 | 7/7 | 781/787 | 8/5 | 2/1 | 0/0 | 2/0 |
| 43 | 600 | 2/0 | 798/798 | 0/0 | 0/0 | 0/0 | 0/2 |
| 43 | 1200 | 0/0 | 800/799 | 0/0 | 0/0 | 0/0 | 0/1 |
| 71 | 0 | 799/799 | 0/0 | 0/0 | 0/0 | 0/0 | 1/1 |
| 71 | 1 | 789/789 | 0/0 | 9/9 | 0/0 | 0/0 | 2/2 |
| 71 | 2 | 721/721 | 9/9 | 64/64 | 0/0 | 0/0 | 6/6 |
| 71 | 16 | 381/381 | 384/384 | 2/2 | 19/19 | 4/4 | 10/10 |
| 71 | 50 | 335/334 | 337/337 | 23/23 | 60/59 | 0/0 | 45/47 |
| 71 | 120 | 66/64 | 647/647 | 13/16 | 52/49 | 3/3 | 19/21 |
| 71 | 240 | 16/18 | 752/752 | 5/7 | 11/13 | 6/6 | 10/4 |
| 71 | 600 | 7/4 | 771/772 | 1/2 | 10/8 | 4/6 | 7/8 |
| 71 | 1200 | 3/4 | 785/787 | 3/0 | 6/3 | 0/1 | 3/5 |


First nonzero same-new is update 2 for all arms/orders. First saved 50% is 50 for orders 29/43 and 120 for 71. First saved 95% is 120 for 29/43 and 600 for 71. [The landmark table](tables/process_first_points_6.csv) also records preceding saved points. These are not the original four-cell new-learning qualification; for example seed 43 reaches 95% coverage at 120 but qualifies under the original new-learning gate at 240.

The largest absolute saved-point TS-minus-U difference is 0.75 percentage points; signs vary across points. [All 27 contrasts](tables/process_contrasts_27.csv) retain conditional paired intervals. U seed 71 same-new counts are 0,0,9,384,337,647,752,771,785: coverage is not monotone. No sustained delay is observed; unsaved-step equality or general ineffectiveness is not established.

The fixed real example `dev/old/甲/1-0-12` changes only mode one/two in “模式：一/二。口令：甲。列表：黄 红 鸟。答案：”. Under order 29, U and TS answer “黄” in both modes at updates 0/1/2 and “鸟” in both modes from update 16 in this example. Old target is 黄 and new target 鸟. process_real_examples.json retains every point and both arms; process_pairs_43200.csv retains all pair records; process_sources.json binds the 54 input JSON paths and hashes. This distinguishes old-default from new-default outputs without showing that internal first/last computations were erased.

## Parameter stability and functional boundary

[C-coordinate stability](tables/C_coordinate_stability_48.csv) normalizes the prior audit's 48 saved-state C/R records by initial C norm without new model forwards.

| Order seed | U endpoint C net displacement / C0 | TS endpoint C net displacement / C0 |
| --- | ---: | ---: |
| 29 | 0.189589% | 0.018474% |
| 43 | 0.179159% | 0.017111% |
| 71 | 0.499556% | 0.036618% |

Net displacement is ‖C1200−C0‖; path length is Σt‖Ct−Ct−1‖; squared displacement sum is Σt‖Ct−Ct−1‖². These cannot substitute for one another. The prior audit retains per-update path/squared quantities and R records; none is inferred from endpoints here. TS net displacement is below the smallest probe dose, but directions, R, and input states differ, so this does not guarantee function preservation.

## Evidence lineage and bounded next decision

| Question | Raw evidence → computation | Coverage and eligibility | Claim boundary |
| --- | --- | --- | --- |
| Is C more sensitive? | 41 full-DEV JSONs → analyze_probe.py → ten contrasts/two pooled rows | DONE_VALID, numeric guards pass | Average local probability signal; consistency/necessity unresolved |
| Does overwrite differ? | 54 existing JSONs → process.py → 54 rows/27 differences/per-answer pairs | DONE_EXPLORATORY, exposed DEV | No observed sustained delay; no full-trajectory equivalence |
| Are coordinates stable? | Prior 48 C/R rows → initial-C normalization | DONE_VALID, saved net displacement | Parameter coordinates, not a functional guarantee |
| Alternative or shared candidate? | No alternative-candidate or controlled cross-task reuse test | NOT RUN | Old-specific, generic, and shared remain Unknown |

Probability sensitivity does not establish necessity for old correctness. Coordinate stability does not establish conditional-function preservation. The change from an old default to a new default is compatible with altered conditional use, but changes elsewhere, generic computational sensitivity, and distribution-dependent effects remain live.

AI proposal: do not immediately replace the candidate; first discuss the required old-mode input/output constraint and conditional use. This is not new-run authorization. The researcher's next decision remains Unknown. Original bounded utility judgment remains in the prior audit; completion does not close the broader research question.

## Reproduction and artifacts

[artifact_manifest.json](artifact_manifest.json) binds source/config/freeze/job receipts/raw readouts/directions/tables/figures by SHA256. execution_manifest.json indexes execution-side files; verification.json contains independent checks. directions.pt contains perturbation bases and coefficients, not a trained model. The prior A audit ZIP is unchanged.

CPU recomputation, from the execution directory: `python process.py`, `python analyze_probe.py`, `python concentration.py`, then `python plot.py`. These read saved outputs and perform no training or model forward. Do not rerun completed probe.py; its duplicate guard also prevents this. Selected strict access receipts cover six input IDs and the new output analysis ID. Access PASS is not scientific support.

review_receipt.json records scientific-identification, data/statistical, and implementation/numerical audits. Both figures were opened and visually checked for readable labels. The global navigation checker still has two unrelated preexisting findings; no repository-wide PASS is claimed.
