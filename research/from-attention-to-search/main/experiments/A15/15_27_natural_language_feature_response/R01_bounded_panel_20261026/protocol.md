# Protocol: A15_27 R01 bounded natural-language feature response

## 0. Approval Snapshot

Document status: `APPROVED_FOR_BOUNDED_READONLY_ANALYSIS_PENDING_SOURCE_FREEZE`.
Approval source: the researcher's 2026-10-26 request explicitly authorizes writing the Anchor/Protocol/text manifest, freezing, and direct bounded execution without intermediate item-by-item review. Numerical conventions below are `DELEGATED_BOUNDED_ANALYSIS_CHOICES`; no separate human A–G confirmations are asserted. Cross-block consistency: internal source review PASS. This Protocol becomes executable only with its first pre-forward source/config/text freeze receipt. Registered revision: `A15_27_R01_v1`.

Purpose: determine which existing sparse features are stable or show reproducible related responses when a preceding clue changes at the same target token. Primary [Anchor ](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/15_27_natural_language_feature_response_anchor.md) and confirmed [Focus ](../../../../focus/focus_natural_language_feature_response.md) own this one bounded question. Role: `operationalization or proxy test`. Rival: lexical/template identity, position/length, unrelated edits, sparse support or common amplitude. Primary quantities: paired target contribution changes, holdout directional excess over unrelated edits, and holdout within-group response correlation against two nulls. H1/H2/H3 have separate SUPPORT/WEAKENED/INSUFFICIENT branches; no positive result is required.

Execution scope: existing assets, current container and existing H100 40 GB MIG only; at most 288 panel sequence forwards and four planned replay forwards, absolute total cap 1,000, at most 256 tokens per sequence. `execution_surface=current_container`; `resource_profile=USER_AUTHORIZED_EXISTING_RESOURCE`. This is the current user's explicit scoped choice over the default submission profile; no new allocation or purchase occurs. No model/dictionary/expert training, updates, activation intervention, model comparison, sealed TEST access, deletion, commit/push or external publication is authorized.

## 1. Terminology / Definitions

A base case contains at most four controlled text versions, each ending at the same target token. A sample is the target position plus the visible prefix through that token; no suffix is forwarded or used to explain its response. A feature is one of the existing SAE's 30,000 coordinates. A relationship group is a cluster of features defined by paired response changes. It is not a validated expert or knowledge module. Discovery fixes candidates and processing; holdout is the new constructed confirmation panel, not any sealed TEST.

A source group records independently constructed clue wording. Average rows within any repeated source group before primary relation statistics and resample whole source groups. Final text has 72 distinct source groups, so each currently corresponds to one base case. Related target-token and relation concepts recur across cases and limit population generalization.

## 2. Anchor Alignment

The experiment asks whether a fixed response definition survives controlled editing and separated wording families. It tests H1 clue-response replication, H2 response-group replication and H3 near/far differences independently. The core observable is a feature's vector of same-token contribution differences across cases. Token heatmaps explain instances; neither their appearance nor a two-dimensional projection decides replication. Passing measurements do not establish functional usefulness.

## 3. Tested Hypothesis

H1: some clue responses reproduce across expression families, exceeding unrelated edits in holdout. H2: some paired-response groups reproduce beyond support/marginal and frequency/intensity controls. H3: distance sensitivity can be distinguished from clue dependence when the same relationship and target are retained. The decisive falsifier for each is loss of its frozen holdout criterion or comparable null behavior, subject to measurement and support qualification.

## 4. Rival Explanations

A separates local modifier/collocation effects from unrelated weekday edits. B changes an explicit preceding sense clue while keeping the target and target-local wording. C moves the identical neutral block around the same clue, preserving the relation, text contents, token length and target position. The same-distance semantic contrast separates clue content from relocation. Sentence order still changes with distance, so an H3 positive result is distance/order sensitivity under this construction. Global amplitude regression and two nulls address common magnitude and sparse marginals. Cross-split template/entity/source separation and leave-one-template-out checks address expression dependence.

## 5. Data Construction And Provenance

Freeze 24 cases per panel, 12 discovery and 12 holdout, four versions each: 72 cases and 288 sequences. All text is English artificial natural-language construction by the Codex agent under the researcher's constraints, followed by controlled editing. None is an unmodified natural-corpus excerpt. Cases cover six fixed target words: bank, bass, bat, crane, port and seal. No existing sealed TEST or natural-corpus extraction is needed.

A/B versions are base, changed clue, neutral-base and neutral-changed. Unrelated edits change a weekday and have exactly matched token counts/positions. C versions are near-base, near-changed, far-base and far-changed. It relocates the same neutral block while retaining clue content for each sense; B/C use independently constructed clue wording for the same relation concepts. Ambiguous intended readings are rejected before feature observation and recorded in the text exclusion manifest, never based on SAE responses.

Each row records sequence/case ID, panel, split, origin and construction agent, template/entity/source group, text, target token/character position, full clue span, measured clue-end distance, changed/held-fixed items and pair role. Discovery/holdout have no overlap in template, entity or source groups; approximate versions stay together. Model-independent tokenizer qualification verifies the exact target IDs, matched target position and length and no suffix. The qualified case authority is `panel/qualified_cases.jsonl`; executable tokens and offsets are in `panel/tokenized_sequences.jsonl`. The original `panel/cases.jsonl` is an initial construction view, not the qualified authority. Final panel token counts are 14–77; C clue-end distance is 1 near versus 40/41/45/46 far tokens. Full clue spans remain recorded because clue-end distance alone omits clue width.

Execution text owner: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/`. Final tokenized manifest SHA256: `945914b9007a4a576f6de99b00b791af56e8daf4464de9169959e733b20d2246`. If the actual final manifest disagrees before the first forward, freeze stops for reconciliation.

## 6. Learning Task And Permitted Supervision

There is no learning task or model update. Inputs are only the visible prefixes and masks. Outputs are target activation, hook state/norm, decoder reconstruction/contributions and native next-token log probabilities. Predeclared single-token continuation candidates supply a semantic-compatibility difference, not a reliable correctness label. Candidate log probability and top-five continuations are auxiliary only; they cannot establish understanding or reasoning success. No feature response is used to relabel text or select favorable examples.

## 7. Model / Architecture And Frozen Variants

Use `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, `sae_qwen3_0p6b_e16_layer27_final_1b`, and reference `representation_qwen3_0p6b_e17_dclm_sparse_activation`. The official model directory is `/data/250010109/model_cache/Qwen3-0.6B-Base-official`. Model: 28-layer Qwen3-0.6B, native BF16, eval, no gradients, SDPA, `use_cache=False`; no chat template or special tokens. SAE: native frozen FP32 `TopKSAE.from_pretrained`, 1,024 inputs, 30,000 features, ReLU Top32, no input unit normalization or decoder-bias subtraction. Hook: zero-based layer27 MLP `forward_pre_hook(args[0])`, after post-attention normalization. There is one asset set and no architecture comparison.

Let native hook input be h, activation be z and saved decoder column be d. Raw contribution magnitude c=z·L2(d); reconstruction is W_dec z + b_dec. Preserve absolute z, c, c/L2(h) and raw versus ratio changes separately. Contribution vectors can cancel; magnitude is not additive variance. This single-layer SAE has no shared-z cross-layer generation claim. The [asset audit](asset_audit.md) supplies loader/state/hash evidence and local interpretation.

## 8. Training Objective And Optimization

Not applicable: zero trainable model/dictionary parameters, zero updates, no optimizer, objective, scheduler, checkpoint modification or training resume. Statistical OLS nuisance fitting is discovery-only closed-form analysis; it is not model or dictionary training. The historical checkpoint and reference cache are read-only.

## 9. Conditions, Seeds, And Checkpoints

One seed, 20261026, governs analysis resampling and reproducible model execution. Use existing `/root/anaconda3/envs/spectral-hier/bin/python` with `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3`: Torch 2.5.1+cu121 and Transformers 4.53.3. Model weights SHA256 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; SAE SHA256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`. Every tokenizer/source/config hash is bound by the machine audit and pre-forward freeze. No checkpoint is selected by panel performance.

## 10. Primary Metric And Frozen Analysis Plan

**Readouts and primary contrasts.** For A/B, main delta is c_changed−c_base. The signed neutral vector is the mean of (neutral-base−base) and (neutral-changed−changed); its absolute control is the mean of their absolute values, preventing signed cancellation. C main delta is near-changed−near-base; retain far contrast, relation-preserving far-base−near-base and their interaction separately. Let s be feature RMS raw contribution over all discovery cases/versions, floor 1e-8. Apply s unchanged on holdout. No normalized ratio substitutes for an absolute change.

**Eligibility and candidate freeze.** A feature needs activation in at least six discovery cases and six independent source groups, and nonzero main delta (absolute value>1e-8) in at least six cases and six groups. Rank by mean absolute main delta across source-group means divided by s, descending; tie by feature ID ascending. Retain at most 64, excluding zero-variance controlled-response features from clustering. Save every feature's eligibility and support, including non-estimable features. Separately freeze a stability pool requiring discovery activation case/group support≥6 but not response support.

**Common amplitude control and relation.** Regress each feature's discovery delta/s on an intercept, change in log total c across all features, and change in log hook norm, with log floor 1e-8. Fit OLS on source-group means; reuse coefficients unchanged on holdout. The main relation is Pearson correlation of controlled response vectors, using source-group mean rows. Undefined similarities remain NA. Average-linkage hierarchical clustering uses distance 1−Pearson r, cut 0.5 and minimum group size three. Keep this algorithm fixed. Use 200 discovery source-group bootstrap resamples with the same candidates/scales/coefficients/linkage/cut; zero-variance features become singletons. Group stability is mean coassignment probability over original within-group pairs; support later requires≥0.70.

**H1.** Fix semantic-delta direction on discovery within each A/B panel×target-token stratum. Evaluate holdout A/B signed semantic delta minus absolute neutral control, divided by s, averaging source groups first. Use 9,999 one-sided source-group sign flips on signed semantic delta for directionality; the neutral control stays fixed and a separate 2,000-draw bootstrap tests excess over neutral. BH FDR≤0.05 applies across all frozen candidates. Support requires≥6 independently supported holdout A/B groups,≥3 template families, sign agreement≥2/3 among valid nonzero-response groups (at least six; report all-case agreement separately), positive two-sided 95% bootstrap lower bound for excess, q≤0.05, every leave-one-template-out excess>0, and largest case absolute-excess share<0.35. General holdout candidate activation/response support must also meet six cases and six groups. An estimable excess with upper 95% bound≤0 weakens; otherwise a non-pass is insufficient.

**H2.** For each frozen group, compute the mean of all pairwise holdout controlled-response correlations. Each member needs≥6 independent activation groups; group response needs≥6 independent groups; each pair needs at least four independent groups in which either member has a nonzero raw response; all member variances must be finite and nonzero. Against the first null, independently permute each feature's source-group response rows 1,000 times, retaining its exact marginal values and support. Against the second null, draw 1,000 random matched groups from all discovery-eligible features except current members. Match three coordinates: log1p(discovery independent activation support), log(reference frequency+1e-9), and log(s). Standardize by eligible-pool SD per coordinate, floor1e-8. Each coordinate must lie within one SD of its member; keep nearest20 by squared standardized distance and sample without replacement within each random group. Do not relax the caliper; fewer than800 finite complete random draws makes matching insufficient.

Apply separate BH FDR0.05 across groups to the two null p-values. Support requires eligibility, qualified matching, discovery coassignment≥0.70, both q≤0.05, positive mean correlation with 95% source-group bootstrap lower bound>0 (2,000 draws), and every leave-one-template-out correlation>0. Qualified groups failing the criterion weaken; inadequate eligibility or matching is insufficient. Frequency is annotation/matching only. E17 TRAIN discovery frequencies have a missing historical backbone digest and used BF16-autocast SAE encoding, whereas R01 uses native FP32 encoding; TopK near ties may differ. Frequency-matched interpretation is conditional on both historical identity and precision, and historical NMSE cannot replace local qualification.

**H3.** Compute interaction (far-changed−far-base)−(near-changed−near-base) in raw c units, then divide by s; report base near/far separately. Fix each candidate's interaction direction from discovery, and test oriented holdout interaction with 9,999 one-sided source-group sign flips, BH0.05 across candidates and 2,000-draw 95% bootstrap. Require≥6 independent C activation groups and≥6 nonzero interaction groups, direction agreement≥2/3 among valid nonzero interaction groups (at least six), q≤0.05 and positive bootstrap lower bound. Same target, length, position and retained relation must qualify first. Support wording is distance/order sensitivity in this relocation construction. A non-pass is insufficient, not proof of no distance effect or long-range exclusivity.

**Stability.** On the frozen stability pool, require holdout activation support≥6 independent groups, a 90% source-group bootstrap interval for mean raw delta/s strictly within ±0.2, and one-sided95% upper bound for mean absolute raw delta/s≤0.2. Preserve within-group absolute values before averaging. Use2,000 draws. This is operational stability for registered contrasts, not universal context invariance. A nonsignificant difference alone is not stable.

All uncertainty uses source-group/base-case blocks; variants stay together. No adaptive algorithm, threshold relaxation, candidate replacement or holdout fitting occurs. The machine-readable exact counterpart is [statistical_plan.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/statistical_plan.json), frozen alongside this Protocol and root `analysis_config.json`.

## 11. Secondary Metrics And Guards

Record raw and normalized response, feature support, current-panel hit rate, independent reference frequency, global amplitude, actual clue distance and per-template exclusions. Missing/undefined/failed results remain NA, non-estimable or insufficient, never zero. No post-feature outlier deletion occurs. Preserve auxiliary candidate log probabilities without correctness claims.

For both discovery and holdout, require all finite target activations/hooks/reconstructions, mean target NMSE≤0.15 and p90≤0.30. NMSE is sum squared reconstruction error divided by sum squared native target h. Manual sparse decoder sum plus bias must match native reconstruction with relative L2 error≤1e-5. Four discovery sequences receive identical-condition replay; maximum target-z absolute difference must be≤1e-5+1e-4 times the reference maximum absolute z. Failure stops dependent analysis, records the exact condition and does not select another model/dictionary. Holdout reconstruction failure leaves its hypotheses insufficient.

## 12. Known Good / Known Bad / Known Confusing Cases

Before feature observation, fix A01 local modifier, B01 explicit preceding sense, C01 same-clue near/far relocation, and A02's unrelated edit as a negative-control illustration. Ambiguous pronoun reference and distinctions requiring unseen suffixes are excluded before results. The three main examples are A01/B01/C01. A real counterexample follows the frozen rule: first discovery-ranked candidate that does not support H1 on holdout, illustrated at its discovery maximum-response case; if every candidate supports, use the fixed A02 negative control and state that no failing H1 candidate exists. No example decides stability.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | Operation and reason | Output / gate / handoff |
| --- | --- | --- | --- |
| Assets/text | Qualified existing interface and controlled cases | Current strict assets/hash/source checks; tokenizer alignment and pre-result exclusions | Asset audit and text manifest; mismatch blocks dependent forwards |
| Pre-forward freeze | Preserve intended comparison | Hash Protocol, text, code, exact statistical plan and resource bounds | `pre_forward_freeze.json`; no forward before receipt |
| Discovery | Credible target measurement |144 panel forwards plus4 replay; finite/NMSE/decoder/replay checks | Discovery arrays and qualification; fail stops candidate selection |
| Candidate freeze | Define one reproducible relation | Discovery-only support/rank/scales/OLS/tree/group/bootstrap/plot IDs | `offline/candidate_freeze.json` with hashes; no holdout access before receipt |
| Holdout | Challenge fixed definition |144 panel forwards; identical reconstruction gates; fixed H1/H2/H3 and nulls | Tables, arrays, figures or explicit insufficiency; no retuning |
| Delivery | Answer the bounded question | One-page Chinese conclusion, three examples and real counterexample; traceability | Bilingual Summary/Detailed, figures/data and one AI-suggested next question; no automatic extension |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/`. Inputs: `asset_audit.json`, `panel/tokenized_sequences.jsonl`, `offline/statistical_plan.json`; forward code: `run_forward.py`; analysis code: `offline/analyze.py`. Record dirty source identities in a SHA256 freeze instead of implying a clean committed revision. Durable sequence ledger counts every attempted panel/replay forward and enforces288 panel/1,000 total. Do not rerun an existing started phase; inspect its receipt. Any necessary failure recovery must remain within scope/budget and preserve the original attempt.

Save `forward/discovery.npz`, `forward/holdout.npz`, metadata, target h/reconstruction/norm/z and sparse all-token caches for fixed examples; save candidate freeze, discovery/holdout statistics, reference-frequency provenance, all-feature support and candidate/H1/H2/H3/stability tables. Preserve source/data/hash manifests. Figure1 uses first8 variance-eligible discovery candidates, raw-z token heatmaps for A01 base/changed, B01 base/changed and C01 near-base/far-base, with one color scale across edits. Figure2 shows discovery and holdout response-correlation heatmaps in the frozen discovery dendrogram order, reference frequency, support, response descriptions and replication. Figure3 is optional after C qualification and uses fixed candidates. Every figure's text states the question, measurement object, direct observation, allowed interpretation and what it cannot establish. No two-dimensional visual separation is a decision criterion.

Canonical small research records live in this R01 directory; raw data/code/caches/figures stay execution-side. The final reading bundle is a bounded derived copy. No new model/dictionary checkpoint is produced.

## 15. Success / Failure / Insufficient Evidence

Apply H1/H2/H3 independently. A hypothesis is operationally supported if at least one frozen eligible feature/group passes its full criterion. H1 is weakened only for estimable nonpositive excess under its registered interval; H2 is weakened for eligible, matched groups failing its frozen structure criterion. Other non-passes retain insufficiency, and a mixed set of features is reported item by item. H3 non-rejection remains insufficient. Failed measurement, sparse support, insufficient matching, invalid text controls, resource unavailability or source identity failure cannot be reported as scientific refutation. A valid bounded negative or insufficient result completes its factual record.

## 16. What This Cannot Claim

Groups do not establish experts, knowledge modules, functional necessity, routing benefit or sentence-level semantics. Frequency does not define common versus higher-order features. Native log probabilities lack a reliable functional success label here. Distances/order changes do not prove causal long-range computation; a single-layer SAE cannot establish a layerwise generation chain. No research question is closed or scientific mechanism accepted automatically.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G content is covered in sections0–16. State for A/B/F/G: researcher-defined scope plus `DELEGATED_BOUNDED_ANALYSIS_CHOICES`; C/E: no learning/optimization; D: source-verified existing assets under the same delegation. This reuses the explicit current authorization and does not claim fabricated block-by-block approval. Internal identification/statistical/numerical reviews are in [internal_audits.md](internal_audits.md).

At first execution, the pre-forward receipt records exact time and SHA256s for this unchanged Protocol, its companion, qualified panel, code and machine plan. After that boundary, change only status/receipt links or append amendments. A material amendment records old/new values, reason, visible evidence, affected blocks, authorization and eligibility impact; never overwrite the registered body or relax a failed gate. Existing authorization ends at this bounded analysis. Scientific interpretation, functional intervention, expert division and any new experiment remain the researcher's next decision.
