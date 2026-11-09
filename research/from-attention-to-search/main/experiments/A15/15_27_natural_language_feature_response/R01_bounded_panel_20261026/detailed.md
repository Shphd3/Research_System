# Detailed: A15_27 R01 natural-language feature response

Read sections1–3 for the bounded answer and measurement validity, sections4–6 for the actual computation, sections7–8 for instances/figures, and sections9–10 for conformance and complete provenance. The [Protocol](protocol.md) remains frozen; this record owns observations and their AI operational interpretation. Mechanism acceptance and question closure remain Unknown.

## 1. Bounded answer and the three analysis paths

The completed run uses one pretrained Qwen3-0.6B and its existing layer27 MLP-input SAE. All288 panel sequences and four replays completed on the existing H100 MIG. Under the frozen criteria, H1 is supported by10 of20 estimable candidates; H2 has conditional support in G02/G04 of three estimable groups; H3 supports distance/order sensitivity in f26149/f16240. One of97 activation-qualified features, f12039, meets operational equivalence. These are separate outcomes, not semantic-module or expert evidence.

1. Behavior and factor controls: only predeclared continuation compatibility probabilities are read; there is no reliable correctness label, so no understanding or reasoning-success conclusion.
2. Representations and organization: same-token paired response and feature-group statistics reproduce under the frozen operational definition, with the lexical-composition limit below.
3. Functional interventions and measurement quality: no intervention was authorized or performed; local reconstruction and exact-condition replay qualify the readout.

The strongest remaining H2 rival is target-token support composition: G02 responds only on six `bass` cases, while random groups were matched on total support/frequency/intensity rather than target-word support distribution. Thus the run does not establish that all relationship groups exceed lexical-stratum explanations. H3 jointly changes clue distance and sentence order. Reference-frequency interpretation is additionally conditional on its missing historical parent hash and BF16-autocast versus current FP32 SAE precision.

## 2. Measured setup and text controls

A sample is one final target token plus its visible prefix, never an unseen suffix. The native model is28 layers/hidden1024; the hook is zero-based layer27 MLP input after post-attention normalization. The SAE has30000 features, ReLU Top32 and its original frozen FP32 encoder/decoder. Model computation is frozen BF16 eval/no-grad SDPA. No input unit normalization or decoder-bias subtraction is added.

The72 cases are Codex-constructed English natural language plus controlled edits, not unmodified corpus excerpts. Panels A/B/C each contain24 cases, split12 discovery/12 holdout; each case has four versions. Six target words recur: bank/bass/bat/crane/port/seal. Final qualified sources are `panel/qualified_cases.jsonl` and `panel/tokenized_sequences.jsonl`; original `cases.jsonl` is a construction view. Each case records full clue span, target position, exact tokenization, source/author, template/entity/source groups and changed/held-fixed objects. There are72 independently worded source groups,36 on each side, with no cross-split template/entity/source overlap. Shared target/relation concepts still limit population independence.

A changes a local modifier, B a prior explicit sense description, and C relocates the same neutral block around an identical clue. A/B weekday controls preserve token length/position. All matched C versions preserve total token length and target position, with clue-end distance1 near versus40/41/45/46 far. Full clue spans remain available, since end distance omits clue width. Sequence lengths are14–77, below256. Pre-result ambiguity exclusions and neutral-block revisions are recorded before the first forward; no text was removed based on feature responses.

## 3. Measurement qualification and actual resource use

| Split | sequences | mean target NMSE | p90 target NMSE | max decoder-formula relative error | qualification |
| --- | --- | --- | --- | --- | --- |
| Discovery | 144 | 0.0762048 | 0.1059966 | 1.15e-07 | PASS |
| Holdout | 144 | 0.0667846 | 0.0935571 | 1.25e-07 | PASS |

NMSE divides target squared reconstruction error by squared hook norm. Gates were mean≤0.15 and p90≤0.30. Manual sparse decoder sum plus bias agrees with native reconstruction well below1e-5. Four repeated A01 versions have target-z maximum difference exactly0. Both phases retain unchanged model/dictionary hashes, zero parameter updates and no gradients. Historical validation NMSE0.053382 is background only; the local values above qualify this panel.

The ledger contains292 attempts:288 panel+4 replay, 11612 forwarded prefix tokens including replay, maximum77 tokens. Discovery completes144+4 in20.026s; holdout144 in19.664s. Peak allocated CUDA memory is1687291392 bytes. These phase elapsed times include loading and checks; they are not a compute-efficiency benchmark. Execution used the current container's existing H100 80GB MIG3g.40gb (40448MiB), no ACP job, no new resources, no purchases. The actual environment is Torch2.5.1+cu121/Transformers4.53.3 using existing spectral-hier Python and existing dependency PYTHONPATH. The constructed holdout was executed; sealed TEST was not read. See [execution_certificate.json](execution_certificate.json).

## 4. Computation, selection and nulls

For activation z and decoder column d, raw contribution c=z·L2(d) uses native hook units; decoder bias stays separate. Absolute z/c and c/L2(h) are saved independently, so ratio changes never replace absolute differences. Main contrast is changed−base for A/B and near-changed−near-base for C. The neutral control averages the two absolute weekday effects; its signed vector is separately saved. Scale is discovery RMS c over all cases/versions, minimum1e-8.

Eligibility requires six case and six source-group activations and six nonzero main responses.83 of30000 features qualify; rank by mean absolute source-group delta/RMS, tie feature ID, freezes64. OLS removes intercept, delta log total c and delta log hook norm using discovery-only coefficients. Pearson correlation between controlled source-group vectors defines the relation. Average-linkage distance1−r, cut0.5, minimum3 creates seven groups.200 discovery source-group bootstraps measure original-pair coassignment; support needs≥0.70. No algorithm or cutoff changes after holdout.

H1 fixes direction within discovery panel×target strata, then tests holdout signed semantic delta beyond absolute neutral edits. It requires≥6 valid independent direction groups,≥3 templates,≥2/3 agreement, positive95% excess interval, BHq≤0.05, positive leave-one-template-out excess and maximum case share<0.35. Direction agreement excludes zero-direction/zero-response groups; all-group agreement is separately reported. H2 requires supported finite-variance members/pairs, held-out mean pair correlation, and both1000-draw nulls: feature-wise row permutations preserving marginals, and random groups matched on discovery support, historical reference frequency and RMS strength. Matching calipers are fixed at one standardized SD per coordinate, nearest20 candidates/member and at least800 valid draws. Both null q values must pass0.05, as must bootstrap lower bound and template deletion.

H3 uses (far-changed−far-base)−(near-changed−near-base), with discovery direction and separate raw near/far/base-distance values. It requires six independent activation and interaction groups,≥2/3 valid-group agreement, BHq≤0.05 and a positive95% interval. Hypothesis tests use9999 sign flips; intervals use2000 source-group bootstraps, seed20261026. Operational stability uses a separate frozen pool,90% mean-delta interval within±0.2 discovery RMS and one-sided95% mean-absolute-delta upper≤0.2. Nonsignificance alone never means stable. Full exact rules remain in the unchanged [Protocol](protocol.md) and [statistical_plan.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/statistical_plan.json).

## 5. H1, stable features and H3 results

H1 has52 candidates with general holdout support,20 meeting the full H1 estimability requirements, and10 passing all criteria. The passing features and their actual heldout values are:

| feature | H \|delta\| | H neutral \|delta\| | signed excess / D RMS | 95% CI | BH q | valid direction groups | agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 18711 | 6.7276 | 0.0291 | 1.1548 | [0.7870, 1.5152] | 0.0064 | 16 | 1.000 |
| 26149 | 3.5235 | 0.0334 | 0.9872 | [0.5373, 1.4554] | 0.0096 | 10 | 1.000 |
| 3743 | 4.7924 | 0.0457 | 0.7945 | [0.4098, 1.1931] | 0.0096 | 17 | 0.824 |
| 6401 | 1.8591 | 0.0214 | 0.6847 | [0.2529, 1.1844] | 0.0442 | 7 | 1.000 |
| 12986 | 1.9306 | 0.0268 | 0.7569 | [0.3413, 1.2008] | 0.0282 | 8 | 1.000 |
| 2453 | 2.1501 | 0.0299 | 0.8859 | [0.4117, 1.4290] | 0.0282 | 8 | 1.000 |
| 20058 | 4.1274 | 0.4212 | 0.5098 | [0.2089, 0.8053] | 0.0096 | 19 | 0.947 |
| 22464 | 2.8717 | 0.0808 | 0.7209 | [0.2701, 1.2547] | 0.0282 | 8 | 1.000 |
| 16240 | 3.8582 | 0.0657 | 0.3246 | [0.1229, 0.5315] | 0.0282 | 11 | 0.818 |
| 27076 | 10.1049 | 0.2089 | 0.8565 | [0.6116, 1.0988] | 0.0064 | 23 | 0.957 |

The native absolute-effect and neutral columns are not normalized percentages. For f18711,16 evaluable A/B direction groups all agree, while the all24-group agreement is16/24=0.667. This distinction prevents sparse features from appearing universally responsive. Complete failures, non-estimable candidates and per-case raw/ratio values remain in [H1_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H1_features.csv) and [holdout_case_feature_responses.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/holdout_case_feature_responses.csv).

The frozen stability pool contains97 features. Only f12039 passes: holdout support6, mean delta/RMS0.0711,90% interval[0.0174,0.1419], mean absolute delta/RMS0.0881, one-sided95% upper0.1539<0.2. Only6 of36 holdout base cases activate f12039; zero activation dominates the remainder. This is equivalence of the panel-average registered effect with sparse support, not universal context invariance. Source: [stable_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/stable_features.csv).

H3 has25 estimable candidates and two passing features:

| feature | near semantic delta | far semantic delta | far−near interaction | oriented / D RMS | 95% CI | BH q |
| --- | --- | --- | --- | --- | --- | --- |
| 26149 | -5.6700 | -2.4511 | 3.2189 | 1.1156 | [0.6149, 1.6603] | 0.0288 |
| 16240 | 6.9704 | 1.5124 | -5.4580 | 0.5471 | [0.2905, 0.8072] | 0.0288 |

Raw contribution interaction is positive for f26149 and negative for f16240; the oriented values use frozen discovery signs. Both have q0.0288. The result supports this specific relation-preserving distance/order manipulation. The experiment does not isolate pure distance, show long-range exclusivity or identify information propagation. Source: [H3_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H3_features.csv).

### Auxiliary next-token readout

Define margin L as log probability of the prespecified base-sense-compatible candidate minus that of the changed-sense-compatible candidate,in nats. The heldout mean changed-minus-base margin is−10.542 over12 B cases,and−10.359/−4.354 over12 near/far C cases. A negative difference describes a shift between these two candidates in the clue-compatible direction. Neither candidate is a unique correct continuation; no functional accuracy,understanding or reasoning success is claimed. The [per-sequence table](tables/auxiliary_next_token_readouts.csv) preserves literal candidates and probabilities. This descriptive summary introduces no new hypothesis test or H1–H3 decision.

## 6. H2 groups, nulls and the surviving lexical rival

| Group (size) | D coassignment | H mean r | 95% CI | min member H support | matched / permutation q | typed result |
| --- | --- | --- | --- | --- | --- | --- |
| G01 (6) | 0.915 | 0.7192 | [0.6014, 0.8036] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |
| G02 (3) | 1.000 | 0.8356 | [0.7541, 0.9483] | 6 | 0.0163 / 0.0023 | SUPPORT |
| G03 (4) | 0.487 | 0.4346 | [0.1966, 0.6521] | 6 | 0.0163 / 0.0023 | WEAKENED |
| G04 (4) | 0.845 | 0.6563 | [0.4988, 0.8260] | 6 | 0.0070 / 0.0023 | SUPPORT |
| G05 (5) | 0.532 | 0.4461 | [0.2627, 0.6502] | 2 | 1.0000 / 1.0000 | INSUFFICIENT |
| G06 (5) | 0.716 | 0.6957 | [0.5506, 0.8063] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |
| G07 (3) | 0.727 | 0.3438 | [0.0833, 0.6504] | 5 | 1.0000 / 1.0000 | INSUFFICIENT |

G02/G04 pass the registered structure rule. G02's matched-group95th percentile is0.3262 versus observed0.8356; G04's is0.1662 versus0.6563. Their minimum leave-one-template-out correlations are0.8058 and0.5600. G03 has positive holdout correlation and significant null comparisons, but discovery coassignment0.4867 fails0.70; it is weakened under the registered complete criterion. G01/G05/G06/G07 have a member below six holdout activation groups and remain insufficient despite visually positive correlation. The p/q=1 entries for ineligible groups are conservative sentinels, not measured evidence that random groups are comparable.

Target-level support composition, derived descriptively from the frozen raw deltas without refitting, is:

| Group | target-token response-support composition | any-response cases |
| --- | --- | --- |
| G01 | {"bank": 6, "bass": 4, "bat": 4, "crane": 6, "port": 3, "seal": 4} | 27 |
| G02 | {"bass": 6} | 6 |
| G03 | {"bank": 6, "crane": 3, "port": 6} | 15 |
| G04 | {"bank": 1, "bass": 6, "bat": 1, "crane": 2} | 10 |
| G05 | {"bank": 6, "crane": 1, "port": 6} | 13 |
| G06 | {"bank": 3, "bat": 4, "port": 2, "seal": 5} | 14 |
| G07 | {"bass": 6, "bat": 6, "crane": 6, "port": 5, "seal": 6} | 29 |

G02's entire support is `bass`; G04's10 any-response cases include six `bass`. The matched null controls total activation support, corpus frequency and strength, but not this target distribution. Paired same-token editing excludes a change of target token within each contrast; it does not exclude shared token-stratum sparsity as an explanation of correlations across cases. Thus H2 is conditional operational support, while the stronger claim “beyond all lexical explanations” remains insufficient. The historical E17 reference also lacks its producing backbone digest and used BF16 autocast whereas R01 encodes SAE FP32, so near-tie TopK incidence may differ. Both limitations are preserved, not repaired by retuning or new inference. Per-target member support is also saved in [H2_target_support_description.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_target_support_description.csv). Source: [H2_groups.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_groups.csv) and [reference_frequency_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/reference_frequency_provenance.json).

## 7. Three fixed examples and the actual counterexample

Complete visible-prefix texts, token pieces, clue spans and target offsets are in [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) and [examples.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/examples.json). All examples below are discovery instances; held-out statistics are separately identified.

### A01: local lexical/collocation control

Target `bank`, token ID6073, zero-based target position16. The baseline clue is “river”; its edited counterpart is “savings”. Both versions stop at the target. In this preselected case, f6401 raw contribution changes 0.0000→4.0446, delta=4.0446. Cases A01/B01/C01 were fixed before inference; the example feature is the maximum absolute change within the frozen eight plot features. This explains the readout and does not assign whole-sentence meaning. The local modifier changes river→savings; equal-position/length weekday edits are negative controls. This is not a long-range example.

### B01: sense determined by preceding context

Target `bank`, token ID6073, zero-based target position32. The baseline clue is “The account describes land beside a river, with water washing against soft soil.”; its edited counterpart is “The account describes an office handling money, with clerks arranging new loans.”. Both versions stop at the target. In this preselected case, f12986 raw contribution changes 0.0000→4.4283, delta=4.4283. Cases A01/B01/C01 were fixed before inference; the example feature is the maximum absolute change within the frozen eight plot features. This explains the readout and does not assign whole-sentence meaning. The target-local text remains “The bank”, and the full disambiguating clue precedes it. Replication evidence comes from the complete held-out H1 test, not this sentence.

### C01: the same relationship at near/far distance

Target `bank`, token ID6073, zero-based target position62. The baseline clue is “A stream runs past the strip of soil that forms its outer edge.”; its edited counterpart is “Customers regularly bring their savings to the business, which also lends money.”. Both versions stop at the target. In this preselected case, f26149 raw contribution changes 4.1442→0.0000, delta=-4.1442. Cases A01/B01/C01 were fixed before inference; the example feature is the maximum absolute change within the frozen eight plot features. This explains the readout and does not assign whole-sentence meaning. The identical baseline clue ends 1 versus 40 tokens before the unchanged target position. The feature’s semantic contrast is -4.1442 near and 0.0000 far. The same neutral block is relocated; sentence order changes too, so this instance does not identify a pure distance cause.

### Counterexample C10: large instance change without qualified replication

The frozen rule picks f24995, the first discovery-ranked H1 non-supporting feature, at its maximum discovery-response case C10 (target `crane`). Raw contribution changes 10.5743→0.0000, delta=-10.5743. Holdout A/B has only 4 evaluable direction groups, below six; q=0.1072, and the largest case contributes 0.5069 of absolute excess, above0.35. A positive average excess and striking image do not qualify cross-expression replication. The typed outcome is insufficient, not evidence of no response.

## 8. Figures and their direct evidential roles

**Figure1:** question—how fixed visible-prefix instances respond across tokens; object—raw SAE z for the eight frozen discovery plot features. The common color scale spans both edited versions, cyan marks target/clue, and full prefixes/token pieces remain visible. Direct observation is the instance changes quantified in section7. Allowed interpretation is an activation profile in those instances; it cannot establish cluster stability, complete sentence meaning or functional success. Data: token cache and `token_cache_index.json`. Reading copy: [token heatmaps](figures/figure1_token_feature_heatmaps.png).

**Figure2:** question—which paired-response relationships reproduce; object—discovery and holdout Pearson correlations of the controlled raw-contribution differences, with the same frozen discovery dendrogram order. Direct observation: seven discovery groups, two complete registered passes, one weakened and four support-insufficient groups. The annotation companion records native baseline/response magnitude, reference frequency and support. Allowed interpretation is this defined response group on the constructed panel; neither color blocks nor annotations establish semantic modules, experts or mentor-defined clusters. Data: frozen discovery/holdout statistics and H2 table. Reading copies: [response relations](figures/figure2_response_relations.png), [feature annotations](figures/figure2_feature_annotations.png).

**Figure3:** question—whether relation response changes under the near/far construction; object—mean raw changed−base contrast for the first eight frozen candidates on holdout C. Direct observation: candidate lines differ between the matched positions; only the full H3 test establishes which changes pass. Allowed interpretation is distance/order sensitivity under this relocation, not pure distance causality or long-range specialists. The mean lines are descriptive; interval/q evidence is in section5 and the complete H3 table. Reading copy: [near/far contrasts](figures/figure3_distance_pairs.png). Figure contracts/data remain at [figure_contracts.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/figure_contracts.json). Readable reading copies may change layout only; the pre-forward statistics and candidate identities remain unchanged.

## 9. Conformance, failures and full round record

The pre-forward freeze at2026-10-26T10:57:10.043841+00:00 recorded zero model forwards and no observed feature-based text selection. The first discovery receipt is2026-10-26T10:57:20.343895+00:00. Candidate freeze SHA256 is`a54c37ab0854c4a2e9c535c87d9720cdc8a03c719d19856ae148ad3ea66b5838`; holdout start recorded exactly this hash before its144 forwards. The current primary runner/analysis/plan/config/qualified manifests and both Protocol languages match frozen hashes. No post-start material amendment, alternative candidate, threshold change, parameter update, activation intervention or new allocation is observed. There is one started receipt per split and no retry in the ledger. Model-independent text/precision clarification before freeze is not post-result selection. Current source checks are recorded in the execution certificate.

| Item | Registered | Actual / evidence | eligibility |
| --- | --- | --- | --- |
| Panel | 72cases/288seq; ≤256tokens | 72/288;14–77; qualified manifest exact hash | ELIGIBLE |
| Forward budget | 288panel+4planned replay; total≤1000 | 292 total; sequence ledger | ELIGIBLE |
| Measurement | mean NMSE≤.15,p90≤.30; formula/replay | D/H PASS;4 exact replay | ELIGIBLE |
| D→H order | D-only scale/candidates/tree; freeze before H | candidate hash in H start receipt | ELIGIBLE |
| H1 | frozen complete criterion | 20estimable/10pass | ELIGIBLE_BOUNDED |
| H2 | both nulls+stability+support | 3estimable/2pass; lexical-composition rival remains | BOUNDED |
| H3 | qualified same relation/length/position | 25estimable/2pass; order co-varies | BOUNDED |
| Functional success/intervention | not authorized | not run; compatibility scores only | NOT_RUN |
| Training/sealed TEST/new resources | forbidden | 0updates; sealedTEST false;0new resources | CONFORMING |

This round's six fields are complete: question/H1–H3; one frozen parent/SAE and controlled variants; no new training data or updates (historical SAE/reference provenance retained); separately constructed discovery/holdout; actual measured results and failures above; and a bounded interpretation plus next researcher decision. The measurements qualify; sparse support, unstable discovery grouping and token composition explain distinct non-passes without falsifying an untested causal mechanism.

## 10. Evidence lineage, artifacts and next decision

| Decision | Raw → computation | independence / uncertainty | bounded result |
| --- | --- | --- | --- |
| Measurement | target h,z,hhat → NMSE/formula/replay | 144target sequences/split;4replays | D/H qualify |
| H1 | target c → oriented semantic-minus-neutral | source groups;2000boot/9999sign/BH | 10pass;20estimable |
| H2 | controlled c deltas → pair r/2nulls | source groups;200boot stability/2000CI/1000null | G02/G04 operational pass; lexical-stratum rival live |
| H3 | four C versions → difference of semantic differences | source groups;2000boot/9999sign/BH | 2pass for distance/order only |
| Stability | raw main delta/RMS → equivalence | frozen97pool;90%meanCI/one-sided95%absupper | f12039only |
| Examples | fixedcase+frozen8plot IDs; deterministicfailure rule | single instances, not replication units | A01/B01/C01 plus f24995C10 |

The complete artifact ledger follows. Each item is at its existing execution owner, with exact identity, rather than copied as a second editable source. Core result records are complete; raw NPZ and tables preserve all candidates, support, missingness and unsuccessful groups. Selected figures are derived reading copies. No trained checkpoint was produced. Any reusable-cache asset registration is a separate factual handoff, not asserted merely from file existence.

| Artifact | Role | SHA256 |
| --- | --- | --- |
| [pre_forward_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/pre_forward_freeze.json) | provenance / statistics | 29f5b17169f5f15c2e9ec61214b2ecf8edbd4574e9eaeebe38848def865594a9 |
| [analysis_config.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/analysis_config.json) | provenance / statistics | 1f57d8d70a865fed205e5531395d70b29af61fe2c5e35be410c4da72874f7bbb |
| [asset_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/asset_audit.json) | provenance / statistics | f2743c3d64f9cdcb8c852ce97e26ef6b62545ca6a7688d580e57972327884cd0 |
| [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) | provenance / statistics | 33a2f75ae0ea6ed6225e089d4d4ac7ae6230390af6e1ca3ddb06e1f93be4f4ee |
| [tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/tokenized_sequences.jsonl) | provenance / statistics | 945914b9007a4a576f6de99b00b791af56e8daf4464de9169959e733b20d2246 |
| [discovery.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/discovery.npz) | raw measurement | 51793c0bb38b05517a21f2a961ff4471e0c5edaf5c5085198b7f7613959fb2f5 |
| [holdout.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/holdout.npz) | raw measurement | c9331111ba0cf318f488500b47ee68ab26556be3c5cd025eddc6e754cfe7b8e2 |
| [forward_ledger.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/forward_ledger.jsonl) | provenance / statistics | 85d26d14062a5eafa1359ee29e63e417fcdedddeee225964ccad036438ac8a9f |
| [discovery_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/discovery_qualification.json) | provenance / statistics | b2636fdf593228ba2dc81000dc1536570001b88981a14207431c6b46e1c7c82c |
| [holdout_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/forward/holdout_qualification.json) | provenance / statistics | 4d4b9c86682a10b81676c75801f33a125359beb8040e450e41fe70c2c1597b5b |
| [candidate_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/candidate_freeze.json) | provenance / statistics | a54c37ab0854c4a2e9c535c87d9720cdc8a03c719d19856ae148ad3ea66b5838 |
| [discovery_statistics.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/discovery_statistics.npz) | raw measurement | 927852281b420118a6a27aba34f9dfd779c32d440295d897735a73a10a6e2279 |
| [holdout_statistics.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/holdout_statistics.npz) | raw measurement | 1af6339236f348a0c22fe6f160a3e568be426b924f19a7f32b25513f6d380f74 |
| [statistical_plan.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/statistical_plan.json) | provenance / statistics | 2d316e8fa20d0d0843ea5e8afe995c32c30f4b7e390594331fb2ed497c170f03 |
| [results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/results.json) | provenance / statistics | 4b4c69c2b3cac2e261d17eb5dd2bebbfc55d2e16b56e0e01600345dededf4bca |
| [H1_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H1_features.csv) | provenance / statistics | 8693b45019abb03e79701faa040517b24056568e46aa129561629c9136c256db |
| [H2_groups.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H2_groups.csv) | provenance / statistics | f65b409d6024eee20112a4d0ca361b14f75742eb27501983074e43aa6846021c |
| [H3_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/H3_features.csv) | provenance / statistics | c81e8e2d015418aa9eea2c0e7480dca2e8ae3ea357a437437f5db312fe110361 |
| [stable_features.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/stable_features.csv) | provenance / statistics | cc50e9c089298101e6b2ed6d235c9d6fe31ad8b1806cd11af552fadb77aff51c |
| [examples.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/examples.json) | provenance / statistics | 97092d984abc33db74f27815871cb732a632ea2e1aff91f112a25efea09a8530 |
| [reference_frequency_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/reference_frequency_provenance.json) | provenance / statistics | c66039cc69bf6238cf52831d68d9e2720d0f8c856e81d3c8fb64e246f8558fb6 |
| [figure_contracts.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/figure_contracts.json) | provenance / statistics | 7eb2a4efac6a0afddf507d0c15e204f6015cb0e837f3bc2841f5a81300f4d377 |

Exactly one researcher-owned next decision remains: refine the relationship definition using these bounded results before deciding whether to enter functional intervention and expert division. **AI suggestion for the minimal follow-up question:** with target `bass` fixed and target-conditional support matched, do G02/G04 relationships still reproduce? This question was not executed or automatically authorized as another experiment. It addresses the strongest live rival without converting the present groups into experts. Mechanism acceptance and closure remain Unknown.
