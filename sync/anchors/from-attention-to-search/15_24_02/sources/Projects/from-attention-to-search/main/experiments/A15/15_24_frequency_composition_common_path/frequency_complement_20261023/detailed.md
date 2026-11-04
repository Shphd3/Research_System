# Detailed A15_24_02: rollback and complement updates along frequency-related directions

[Summary](summary.md) · [Frozen Protocol](protocol.md) · [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md) · [中文](detailed_cn.md)

**All 24 conditions completed and measurement checks passed; researcher mechanism judgment is Unknown.** Complete-displacement projection preserves the specified matrix responses within numerical tolerance. Matched PCA complement has lower primary loss than the two comparison updates in both seeds, but slightly higher loss than the original model. Partial rollback also raises primary loss. The full record below does not update scientific understanding on the researcher's behalf.

## Objects, controls and actual computation

The object is original T_F expert E0's up matrix: 1,048,576 eligible parameters. Fixed routing selects two of eight experts with weights 0.5 each. Each receives the full 1,024-dimensional final hidden state of frozen Qwen3-0.6B Base, divided by the original TRAIN scalar scale. SwiGLU gate/up products pass through down into a residual. Cached Base inputs, the other 23 expert matrices, scale, routing, head and norm remain fixed. Positions not routed to E0 are invariant under this intervention.

V contains 16 existing centered TRAIN input PCs; Q is the saved 16-column random orthonormal basis from the same historical file. Neither is fitted or selected on current DEV. No activation whitening or weight SVD is performed, and task specificity is not established.

For rollback, D is saved step-168 W minus initialization. Remove 0.25DP or 0.5DP and compare with same-rank random rollback matched in actual edit norm. Arbitrary perturbations can damage predictions, so the random control remains necessary.

For updates, take the first 512 E0-hit positions in each saved TRAIN permutation. Accumulate next-token cross entropy sum /512 with microbatch 64. Compute one raw gradient per seed on that batch. Restore the full saved step-168 AdamW state to independently propose an ordinary displacement and a gradient-projected diagnostic displacement. Each temporary optimizer call moves its counter 168→169 and is then discarded; these are neither two consecutive steps nor resumed training.

Actual learning rate is 0.00003; betas=(0.9,0.95), eps=1e-8, decay=0.01. Clip only the eligible matrix to norm1. Raw gradient norms are 0.176753 / 0.180659; projected gradient norms are 0.077283 / 0.078746, all below the clip threshold. TRAIN batches span 337 / 325 dialogues and have baseline batch losses 0.526664115 / 0.512897465 nat. The full proposal includes historical moments and weight decay; it is not a pure current-batch gradient.

From the ordinary complete displacement derive PCA and random complements, each at natural norm and rescaled to the full-displacement norm. The gradient-only arm is a separate implementation diagnostic, without an additional final norm match; it is not equivalent to projection of the same actual displacement.

## Data and support

Original TRAIN contains 85,548 valid next-token targets in 1,024 dialogues; DEV contains 10,340 positions in 128 dialogues. These existing caches are not new confirmation data. Frequency uses original TRAIN CrossCoder activation bands B1/B4, never the legacy cache low_ids/high_ids.

E0 is routed at 693 DEV positions across 109 dialogues. All 693 are in both low- and high-feature unions. Full DEV has low union1,701, high union10,340 and overlap1,701. These are overlapping readouts, not independent tasks or separately attributable samples.

The primary metric averages NLL within each B1 feature on E0-hit DEV, then equally over supported features. Of1,694 B1 IDs,417 have support and1,277 are NA. Support median1, minimum1, maximum16; none has support>=20. The full-DEV historical readout has838 supported low features and856 NA. The417 is an additional E0-conditioned subset, not the same metric as the838-feature panel.

Both seeds share DEV; this is not independent data resampling. Positions, features and dialogue signs do not increase the number of independent model replicates. No population confidence interval is constructed from two seeds. All conditions remain; no winner, rank, scale or support threshold was selected from outcomes.

## Complete primary metric

Unit nat, lower is better. Delta is condition minus same-seed unchanged model; positive means increased loss. Every row uses the same417 supported features.

| Condition | seed 11 NLL | Δ 11 (nat) | seed 22 NLL | Δ 22 (nat) |
|---|---:|---:|---:|---:|
| Saved model | 1.007749989 | +0.000000000 | 1.004129048 | +0.000000000 |
| Exact rewrite | 1.007749989 | +0.000000000 | 1.004129048 | +0.000000000 |
| 25% PCA net-displacement rollback | 1.007965317 | +0.000215328 | 1.004978932 | +0.000849884 |
| Random rollback matched to 25% edit | 1.007971889 | +0.000221900 | 1.004261486 | +0.000132439 |
| 50% PCA net-displacement rollback | 1.008319567 | +0.000569578 | 1.006046609 | +0.001917561 |
| Random rollback matched to 50% edit | 1.008195751 | +0.000445762 | 1.004395395 | +0.000266347 |
| Full AdamW displacement | 1.007756083 | +0.000006095 | 1.004151317 | +0.000022269 |
| PCA complement, natural norm | 1.007751743 | +0.000001754 | 1.004135871 | +0.000006823 |
| Random complement, natural norm | 1.007756537 | +0.000006548 | 1.004150806 | +0.000021759 |
| PCA complement, full-matched norm | 1.007751599 | +0.000001610 | 1.004136524 | +0.000007476 |
| Random complement, full-matched norm | 1.007756830 | +0.000006841 | 1.004150878 | +0.000021830 |
| Gradient projection before AdamW | 1.007747660 | -0.000002329 | 1.004147632 | +0.000018584 |


Prespecified descriptive signs require both contrasts below−0.000001 nat in both seeds; all four observed contrasts cross that floor. This numerical relation does not itself decide scientific acceptance, practical value or mechanism.

| Primary contrast (first minus second) | seed 11 (nat) | seed 22 (nat) |
|---|---:|---:|
| Matched PCA complement − full | -0.000004484661 | -0.000014793063 |
| Matched PCA − matched random | -0.000005231122 | -0.000014353697 |


Natural-norm PCA complement minus full update is−0.000004340 /−0.000015446 nat. Its norm is smaller, motivating the separately retained matched-norm readout. Full, PCA-complement and random-complement primary losses are all higher than their unchanged model. Gradient-only projection has a negative baseline contrast in seed11 and positive in seed22, while failing to preserve the specified response. No row repairs another comparison.

The [primary_feature_paired_effects.csv](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/primary_feature_paired_effects.csv) export contains10,008 rows of feature means/support and differences against the original model, full update and matched random update. It derives only from saved NLL, with no added measurement or selection.

## Secondary metrics and dialogue differences

Overall NLL weights all DEV positions equally; full-DEV low/high macros weight supported features equally. High macro therefore differs from overall NLL. All deltas use the same-seed baseline. The last column averages affected low-union position deltas within each of109 E0-hit dialogues, then counts below−1e-6, above+1e-6, and remaining cases. It is neither the primary metric nor a significance test.

| Seed/condition | Overall NLL | Δ overall | Full DEV low macro | Δ low macro | High macro | Δ high macro | Dialogue lower/higher/small |
|---|---:|---:|---:|---:|---:|---:|---|
| 11 Saved model | 1.225544363 | +0.000000000 | 1.055208157 | +0.000000000 | 1.191354649 | +0.000000000 | 0/0/109 |
| 11 Exact rewrite | 1.225544363 | +0.000000000 | 1.055208157 | +0.000000000 | 1.191354649 | +0.000000000 | 0/0/109 |
| 11 25% PCA net-displacement rollback | 1.225557677 | +0.000013314 | 1.055349216 | +0.000141059 | 1.191380461 | +0.000025811 | 56/51/2 |
| 11 Random rollback matched to 25% edit | 1.225554527 | +0.000010165 | 1.055290352 | +0.000082195 | 1.191366190 | +0.000011541 | 38/62/9 |
| 11 50% PCA net-displacement rollback | 1.225579733 | +0.000035371 | 1.055546960 | +0.000338803 | 1.191415778 | +0.000061129 | 56/51/2 |
| 11 Random rollback matched to 50% edit | 1.225564828 | +0.000020466 | 1.055373356 | +0.000165199 | 1.191377873 | +0.000023224 | 41/62/6 |
| 11 Full AdamW displacement | 1.225544556 | +0.000000193 | 1.055211291 | +0.000003134 | 1.191355264 | +0.000000614 | 46/52/11 |
| 11 PCA complement, natural norm | 1.225544461 | +0.000000098 | 1.055208388 | +0.000000231 | 1.191354764 | +0.000000115 | 49/48/12 |
| 11 Random complement, natural norm | 1.225544570 | +0.000000208 | 1.055211364 | +0.000003206 | 1.191355268 | +0.000000618 | 46/52/11 |
| 11 PCA complement, full-matched norm | 1.225544462 | +0.000000100 | 1.055208249 | +0.000000092 | 1.191354771 | +0.000000121 | 46/48/15 |
| 11 Random complement, full-matched norm | 1.225544567 | +0.000000204 | 1.055211447 | +0.000003290 | 1.191355273 | +0.000000624 | 46/52/11 |
| 11 Gradient projection before AdamW | 1.225543784 | -0.000000579 | 1.055206018 | -0.000002139 | 1.191354042 | -0.000000608 | 52/41/16 |
| 22 Saved model | 1.226654859 | +0.000000000 | 1.058818973 | +0.000000000 | 1.192550426 | +0.000000000 | 0/0/109 |
| 22 Exact rewrite | 1.226654859 | +0.000000000 | 1.058818973 | +0.000000000 | 1.192550426 | +0.000000000 | 0/0/109 |
| 22 25% PCA net-displacement rollback | 1.226657229 | +0.000002370 | 1.059206612 | +0.000387639 | 1.192555455 | +0.000005029 | 55/52/2 |
| 22 Random rollback matched to 25% edit | 1.226655959 | +0.000001100 | 1.058862096 | +0.000043123 | 1.192551931 | +0.000001505 | 47/56/6 |
| 22 50% PCA net-displacement rollback | 1.226672307 | +0.000017448 | 1.059680380 | +0.000861407 | 1.192574924 | +0.000024498 | 55/52/2 |
| 22 Random rollback matched to 50% edit | 1.226657191 | +0.000002332 | 1.058905785 | +0.000086812 | 1.192553587 | +0.000003161 | 49/56/4 |
| 22 Full AdamW displacement | 1.226655276 | +0.000000417 | 1.058826838 | +0.000007865 | 1.192551027 | +0.000000601 | 49/47/13 |
| 22 PCA complement, natural norm | 1.226654999 | +0.000000140 | 1.058821258 | +0.000002285 | 1.192550619 | +0.000000194 | 42/49/18 |
| 22 Random complement, natural norm | 1.226655267 | +0.000000408 | 1.058826582 | +0.000007609 | 1.192551014 | +0.000000589 | 49/47/13 |
| 22 PCA complement, full-matched norm | 1.226655019 | +0.000000160 | 1.058821445 | +0.000002472 | 1.192550645 | +0.000000219 | 42/49/18 |
| 22 Random complement, full-matched norm | 1.226655265 | +0.000000406 | 1.058826638 | +0.000007665 | 1.192551010 | +0.000000585 | 49/47/13 |
| 22 Gradient projection before AdamW | 1.226655964 | +0.000001105 | 1.058826307 | +0.000007334 | 1.192551678 | +0.000001252 | 44/48/17 |


Full values and deltas are in [results.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/results.json). Per-position values, support masks and dialogue differences are saved in each measurements.npz rather than only aggregates.

## A real worked example and contrary case

Choose feature74, the smallest supported B1 ID, without choosing on its effect. This is a post-result teaching illustration, not a confirmatory analysis. It occurs at E0-hit DEV zero-based cache positions1710,4580,6629 in dialogues28,61,82. No semantic meaning is assigned from the ID.

| seed 11, feature 74 DEV position | Dialogue ID | Original NLL | Full-update NLL | Matched PCA-complement NLL |
|---|---:|---:|---:|---:|
| 1710 | 28 | 4.651295662 | 4.650666714 | 4.651201248 |
| 4580 | 61 | 0.820118904 | 0.820068598 | 0.820127428 |
| 6629 | 82 | 1.134220123 | 1.134006262 | 1.134181142 |


For seed11, the original feature mean is (4.651295662+0.820118904+1.134220123)/3=2.201878230 nat. The primary metric then equally averages this with416 other feature means. The example retains a contrary ordering: full update has lower loss on this feature than PCA complement, and the PCA-complement loss at the second position exceeds the original. A macro comparison therefore does not claim uniform feature or position effects. The same feature's full seed22 observations are retained in audits.json.

## Numerical eligibility

Branch and head use FP32, promoting the original stored BF16 head values rather than loading a different model. TF32 is off and deterministic algorithms are enabled. Projection uses FP64 before FP32 application. Optional historical BF16 replay was NOT RUN; no exact old-metric reproduction or cross-environment micro-effect is claimed.

Baseline evaluates E0-hit and non-hit subsets separately; every edited evaluation repeats identical affected microbatches. Both no-op per-position NLL arrays are exactly equal. Four initialization/final tensor digests match original receipts. Each proposal starts from the identical optimizer digest; other matrices and head are unchanged; final restored model digests equal their saved endpoints.

Norm fraction along V is \(\lVert\Delta WV\rVert_F/\lVert\Delta W\rVert_F\); response residual is \(\lVert\Delta WV\rVert_F/\lVert W_*\rVert_F\). The fraction is not squared energy. Preservation gates apply only to complements claiming to preserve the corresponding basis. Rollback/full proposals intentionally may change V responses.

| Seed/condition | Applied norm | Norm fraction along V | Response residual / original W norm | Norm-match relative error |
|---|---:|---:|---:|---:|
| 11 25% PCA net-displacement rollback | 0.252217789 | 1 | 0.007867606 | — |
| 11 Random rollback matched to 25% edit | 0.252217789 | 0.13312028 | 0.0010473379 | 2.83e-09 |
| 11 50% PCA net-displacement rollback | 0.504435581 | 1 | 0.015735212 | — |
| 11 Random rollback matched to 50% edit | 0.504435579 | 0.13312028 | 0.0020946759 | 3.31e-09 |
| 11 Full AdamW displacement | 0.009707032 | 0.41796792 | 0.00012655995 | — |
| 11 PCA complement, natural norm | 0.008818468 | 1.1415724e-05 | 3.1402447e-09 | — |
| 11 Random complement, natural norm | 0.009630994 | 0.41506787 | 0.00012469732 | — |
| 11 PCA complement, full-matched norm | 0.009707032 | 1.037541e-05 | 3.1416558e-09 | 3.88e-08 |
| 11 Random complement, full-matched norm | 0.009707031 | 0.41506798 | 0.00012568185 | 6.54e-08 |
| 11 Gradient projection before AdamW | 0.009060189 | 0.19233905 | 5.4359017e-05 | — |
| 22 25% PCA net-displacement rollback | 0.241657130 | 1 | 0.0075459599 | — |
| 22 Random rollback matched to 25% edit | 0.241657128 | 0.12874422 | 0.00097149869 | 5.97e-09 |
| 22 50% PCA net-displacement rollback | 0.483314257 | 1 | 0.01509192 | — |
| 22 Random rollback matched to 50% edit | 0.483314257 | 0.12874422 | 0.0019429974 | 2.58e-11 |
| 22 Full AdamW displacement | 0.009841345 | 0.40697331 | 0.00012506485 | — |
| 22 PCA complement, natural norm | 0.008989478 | 1.1090901e-05 | 3.1132654e-09 | — |
| 22 Random complement, natural norm | 0.009765772 | 0.40435078 | 0.00012330474 | — |
| 22 PCA complement, full-matched norm | 0.009841345 | 1.0232451e-05 | 3.1444812e-09 | 2.19e-08 |
| 22 Random complement, full-matched norm | 0.009841344 | 0.40435059 | 0.00012425886 | 1.26e-07 |
| 22 Gradient projection before AdamW | 0.009302543 | 0.21671485 | 6.2951377e-05 | — |


PCA complement precast residual relative to displacement is approximately5.1–5.3e-16, below1e-6. After FP32 application it is approximately1.0–1.1e-5 relative to displacement, and3.1e-9 relative to original W, below the frozen5e-7 guard. Exact algebra and finite-precision residuals are distinct. Random-complement checks against Q also pass; all values remain in edit_diagnostics. Maximum norm-match relative error is1.264e-7, below0.002.

Gradient-only final displacements have V norm fractions0.192339 /0.216715 and do not preserve the specified responses. That is the prespecified confusing-case diagnostic, not an execution failure. Matched PCA complement changes NLL at579 /582 positions, with maximum absolute position differences0.000611067 /0.000319719 nat. Preserving selected linear responses is therefore distinct from preserving real mixed-input predictions.

Independent CPU verification explicitly enumerates position-feature incidence and recomputes all24 primary, overall and full-DEV low/high metrics without calling the worker CSR metric function. Maximum discrepancy is2.22e-16. It checks unique feature incidence per position, support/NA counts, invariant positions, frozen design hashes and full coverage. This verifies aggregation, not cross-hardware stability of small FP32 effects.

## Contract, deviations and three audits

English frozen Protocol SHA256: `690645b2c13d6de540811d2cc196df337b787a0858576f8fa1e297346fc22703`; Chinese: `4159e082acc216b43227fd5e4d551a9a88e2ad8f95098db0dd3f37113f0569cf`. Final pre-outcome freeze was2026-10-23 12:17:05 UTC. Original bytes are in [frozen_documents](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/frozen_documents/protocol.md); [frozen.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/frozen.json) holds machine settings and [design_freeze.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/design_freeze.json) records identities.

| Item | Frozen contract | Actual | Effect |
|---|---|---|---|
| Object/basis | E0 up; existing TRAIN PCA/random rank16 | Identical | Local comparison eligible |
| Data | Two original seeds;512 TRAIN each; full DEV | Identical; recompute693 affected positions, reuse invariants | Same DEV panel |
| Conditions |12 per seed |All24 complete |No failure, retry or omission |
| State |Step168,85,548 targets; original AdamW |Model/optimizer hashes checked |Controlled start |
| Precision |FP32 forward, FP64 projection, TF32off |Identical |Same-environment scope, not old BF16 replay |
| Budget |900s;12GiB GPU;1GiB output |37.805 s; GPU 0.973 GiB; CPU RSS 3.205 GiB; initial analysis output about1.21MB |Within limits |
| Pre-execution clarification |Fixed affected microbatches; typography |Recorded before freeze |No scientific change |
| Post-execution exposition |Expanded Anchor, real example and reading tables |Frozen source retained; Protocol unchanged |Not outcome-driven redesign |
| Optional historical BF16 replay |Optional descriptive comparison |NOT RUN |No historical replay claim |
| Continuation/new model |No accepted continuation |Accepted steps0; no checkpoint |No trajectory claim |

The same executing agent Codex /root recorded three separate audits, not independent reviewers:

1. **Scientific identification:** separate rollback/prospective update and matrix response/loss; retain same-rank random and norm controls. Basis specificity, one matrix, frequency causation and long-horizon inference remain limited. PASS_BOUNDED.
2. **Data/statistics:** TRAIN sets bases, frequency and batches; DEV only reads out; all conditions retained. Low support, overlap, prior exposure and independence limits verified. PASS_EXPLORATORY.
3. **Implementation/numerics:**1,048,576 eligible parameters;2 gradient batches,4 independent optimizer calls,0 accepted steps; no-op, freeze, projection, norms, restore, resources and independent aggregation pass. PASS.

Full audits and coverage are in [audits.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/audits.json). No PCA, dictionary or readout fitting was added. Outputs are analysis NLL and selectors, not new trained models or reusable hidden-state caches. No new checkpoint requires registration, and planned paths are not presented as saves.

## Evidence lineage and assets

| Quantity | Raw material | Transformation | Scope |
|---|---|---|---|
| Primary/paired contrasts |Two seeds' position NLL and feature incidence |Within-feature mean, equal supported-feature mean, paired subtraction |417 features/693 exposed DEV positions |
| Rollback effects |Initial/final W, fixed V/Q, four edits |Net-displacement projection, scale/norm matching, finite forward |Not prospective-update effects |
| Complement preservation |Full proposal, FP64 projection, actual FP32 edit |Two residuals; no-op/freeze controls |Selected matrix/basis numerical property |
| Actual local update |Saved optimizer, TRAIN order/labels |Same-state independent proposals and readouts |Nonaccumulating, not long training |
| Coverage/provenance |Design freeze/run start/audits/manifest |Digests, counters, independent aggregation |Completion is not scientific acceptance |

Six input assets passed the current strict check before execution, recorded in [input_access.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/input_access.json):

- `model_qwen3_0p6b_base`
- `data_tulu_sft_route_20261019t012300z`
- `representation_tulu_sft_route_20261019t012300z`
- `analysis_crosscoder_frequency_composition_common_path_20261019t164834z`
- `checkpoint_family_crosscoder_frequency_composition_20261019t164834z_t_f_seed11`
- `checkpoint_family_crosscoder_frequency_composition_20261019t164834z_t_f_seed22`

Original parameter tensor SHA256:

| Seed | Initialization | Step168 endpoint |
|---|---|---|
| 11 | `8fa58ef0a71639e30ccce68f36a6ad91ab6fec9707e91c6cce4699650b6da3da` | `9c800dee6b51d3af46475cfb050e02d531fde1b5e8d77f8c8ca9ba9e93d5f736` |
| 22 | `4c5966639491767e75b216c76b9d53452ec6eb112b8e923517f685e84d90cc4e` | `59feed7f7137e282d69f91b4ad26e2470bb35111d0bd052790c9a0845ebdf1e6` |

The small [artifact_manifest.json](artifact_manifest.json) retains asset IDs, source paths, frozen versions, actual code/config/result/audit digests and sizes. Payloads remain on execution storage.

| Record | Purpose/completion |
|---|---|
| [worker.py](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/worker.py) / [run_start.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/run_start.json) |Actual program, launch identity and dependency/basis/route hashes; complete |
| [seed11_measurements.npz](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/seed11_measurements.npz) / [seed22_measurements.npz](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/seed22_measurements.npz) |Position NLL, masks, support, TRAIN indices, feature/dialogue readouts; complete |
| [results.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/results.json) |All metrics, contrasts, edits, restore and resources; complete |
| [verify_results.py](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/verify_results.py) / [audits.json](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/audits.json) |Independent aggregation and three audits; pass |
| [run.log](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/run.log) / [progress.jsonl](/data/250010109/MoE_Router/experiments/20261023_frequency_complement/progress.jsonl) |Local worker record; no remote job ID |

Verification command in the execution root: `python verify_results.py`. The analysis command is `python -u worker.py`; it would rerun tests and was not repeated for display. Actual runtime and memory: 37.805 s; GPU 0.973 GiB; CPU RSS 3.205 GiB. No trained checkpoint was created.

## Discussion after researcher reading

Record completeness, numerical eligibility and the tabulated values are verified. Mechanism support/refutation, preferred explanation, practical value and the next scientific experiment remain Unknown. No architecture ranking or new training choice is supplied here. Follow reading, explanation of preserved/changed objects and references, then discussion of understanding.
