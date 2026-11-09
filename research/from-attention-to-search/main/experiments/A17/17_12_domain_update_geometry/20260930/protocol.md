# Protocol: domain_update_geometry v1

## 0. Approval Snapshot

**APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_WITHIN_SCOPE; NOT RUN.** [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor.md) · [Focus](../../../../focus/focus_domain_update_geometry.md) · [中文](protocol_cn.md). Experiment role: root-cause/operationalization audit of common versus domain-associated update geometry.

On 2026-09-29 the researcher accepted the domain-first analysis and explicitly requested its completion using SVD, trained SAE atoms and full activation-pattern analysis, first writing Anchor/Protocol, then submitting necessary four-H100 Reserved experiments without another approval. This is explicit delegated authority for in-scope implementation, engineering qualification and full analysis. It overrides a redundant block-by-block approval conversation; it does not assert that the researcher individually chose the AI-specified thresholds below. Scientific result interpretation remains Unknown. No model/SAE training, router, parameter intervention, old-result rewrite, commit or push is included.

One experiment has three mandatory parts: same-record capture and domain-prototype comparison; spectral/common/specific/scale analysis; all-atom activation and decoder-span correspondence. A negative primary result does not gate either diagnostic part. Complete required facts and report failures without substituting an attractive subgroup.

## 1. Terminology / Definitions

An N8 record is a natural academic excerpt with 256 original content tokens and an existing category. **Fit** means the historical 512-record half used to define means, coordinates and atom selections; **readout** is the other 512 records. These are not untouched historical data and are not called CONFIRM.

Input is tokens 0..254. Observed output positions are t=14,30,...,254, predicting tokens t+1. The last event is a 255-token prefix predicting token 255 (the 256th token), unlike the earlier 256→257 DCLM experiment. All 255 input positions contribute to descriptive SAE activation, but only 16 targets contribute to the aggregated loss. No future token is available at its own prediction position.

c has 2048 coordinates; native a and record-specific residual r have 1024; W is 1024×2048. e_it is the derivative of one full-vocabulary NTP CE, not yet divided by 16. G_i^last=e_i,254 c_i,254^T and G_i^16=(1/16)Σ_t e_it c_it^T. K^last and K^16 are their Frobenius Gram matrices. kappa is the corresponding gradient cosine, undefined at zero norm. Common mean, domain mean deviation, common activation and decoder-span coverage are distinct concepts.

## 2. Anchor Alignment

Primary H1 tests whether fit-domain prototypes outperform the pooled prototype on readout gradient error. SVD describes where update variation lies; SAE describes native activation and whether independently selected decoder directions overlap that variation. Matched random directions/groupings and magnitude controls address alternatives. One core experiment, no search for negative K as a completion criterion. The older controlled Focus is historical context, not the owner of this new question.

## 3. Tested Hypothesis

H1: Q_D^last>0 on independent records. H2: pooled/domain/within update variation has reproducible spectral structure, beyond large means/norms. H3: fit-defined common or domain-enriched SAE activity replicates and its decoder spans capture relevant updates beyond equal-rank random spans. H4: fixed within-record averaging changes domain association beyond matched arbitrary grouping. H2-H4 are registered descriptive diagnostics, not additional primary discoveries; their failures do not erase H1 and their successes do not rescue it.

## 4. Rival Explanations

| Rival | Distinguishing comparison | Remaining boundary |
| --- | --- | --- |
| Pooled mean sufficient; fit domain differences are sampling noise | Domain versus pooled prototypes; two-split bootstrap; balanced fit-label permutations | Record-level rather than paper/source-level population |
| Large gradient norms create apparent domain structure | Raw versus unit-gradient Q and spectra; diagonal/norm distributions | Normalized K no longer measures raw SGD effect |
| A shared mean is mistaken for low-dimensional variation | Raw versus fit-centered spectra; mean/between/within decomposition | Finite fit rank is not population dimension |
| Lexical target, difficulty or subfield composition explains domains | Target-overlap and loss/norm diagnostics; two cross-subfield transfers | Association, not isolated semantic cause |
| Averaging alone creates stability | Mean of 16 targets versus last target; matched 1/4/16/64-record random groups | Target count and context position differ; no full-document claim |
| Shared atom IDs are called common despite different amplitudes | All-domain frequency and positive-amplitude criteria, fixed fit selections, readout replication | Similar activation is not similar gradient or causal use |
| Decoder span is large or redundant | SVD rank qualification, cap64, matched random spans; native-a PCA | No whole-dictionary span success claim |

## 5. Data Construction And Provenance

Reuse exactly `/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/selected.jsonl`, SHA256 `7e8858adfbf1ead8330937dc147eee3eb815be9025e620e53c0af0fc86d155d9`. No result-based resampling. Exactly 1,024 records, 512 fit and 512 test/readout; each category/split has64. Existing categories map cs.CL/cs.CV→computer_science; math.AG/math.NT→mathematics; physics.flu-dyn/physics.optics→physics; q-bio.GN/q-bio.NC→biology. Domain order is computer_science, mathematics, physics, biology; subfield order is as written.

Original N8 revision is `6ae613ba744ee56f645aee9c577d04f7e3d48b30`. Original fit/test hashes are `647ce2662da53b31520c11203657338f237fd4be02a299c05203f17d4b1fedd1` and `440531b2c6670eec8c853a0dbc0b7e0b10e3eede5943f36ec0f1f8d6fda1148d`. These sources were used in previous audits. `source_group_scope=record_only_paper_id_unavailable`: sample IDs do not establish paper independence. No fresh-confirmation or absence-of-pretraining-exposure claim.

Preflight verifies source hash, 256-token lengths, vocabulary range, exact split/category counts, unique sample IDs and complete input hashes, no input-hash overlap. Compute cross-split 5-token-shingle Jaccard≥0.80 collisions as an audit without reading outcomes. If any occur, retain the panel but flag affected record-level inferential results INELIGIBLE_DEPENDENCE; do not silently remove/resample records. Existing category labels are source labels, not generated semantic annotations. Preserve original text/IDs/token hashes; do not inject category names into input.

OPS consists of the first two fit IDs per subfield ordered by SHA256(`domain-geometry-20260930|sample_id`), 16 records total. It is an engineering subset of fit, never additional independent evidence. Freeze fit/readout indices and atom-selection scripts before full readout analysis. Historical activation results remain known; no claim of blind research-program design.

## 6. Learning Task And Permitted Supervision

No learned predictor, LM update or SAE retraining. Closed-form prototypes, SVD axes, atom sets and descriptive nuisance controls are fit on fit records only. Domain labels are permitted to construct domain means; actual targets and gradients are permitted because the purpose is explanation of K. This is not representation-only prospective prediction.

SAE atom selection uses only fit activations and domain labels; it must not use fit/readout e, K, loss, target identity or projected-update performance. Fit means/axes/selected IDs are saved before readout summaries. Target/loss/norm diagnostics may use readout labels after choices are frozen and are descriptive only. No later atom naming as mathematics/biology solely from a high enrichment score.

## 7. Model / Architecture And Frozen Variants

Use `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`. State SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`; tokens_seen33,000,000,000; optimizer_step125894. Eight-layer dense S7; backbone281,431,040 parameters. W=`model.blocks[7].attn.o.weight`, no bias, shape1024×2048. SAE61,471,024 parameters, width30,000, TopK32, hook7 after attention output projection before residual addition, historical reconstruction coefficient0.1. SAE is a sidecar.

FP32 eval, TF32/autocast disabled; final full-vocabulary logits/logsumexp CE cast to FP64. All model parameters and activity buffers frozen. Load no historical optimizer. Native residuals remain per record and position. Input prefixes are identical for all variants; normalization, centering, scale and projection are analysis transformations with separate labels. Original decoder uses the model's normalized decoder columns, not an assumed orientation.

Tokenizer assets at `/data/share/Qwen3-0.6B-Base` are for readable token windows only; no pretrained weights from that directory. Source pretokenized IDs are the actual model input.

## 8. Training Objective And Optimization

**NOT_APPLICABLE: no optimization.** Measure 16 CE values per record, each denominator1 valid target; the aggregated objective is their arithmetic mean. SAE reconstruction/AuxK loss does not enter e/G/K. Model and SAE optimizer updates are0. Repeated analyses do not count as newly seen training tokens.

Following [observability](../../../../../../../docs/training_observability_contract.md), register LM-training and optimizer tags NOT_APPLICABLE, log measurement/ntp_loss (nat/target), measurement/valid_targets_seen, records_seen, activation_positions_seen, stage wall time, peak GPU allocated/reserved memory and finite/freeze guards. Counts must reconcile with records×16 targets and records×255 activation positions. Restart uses a new attempt or immutable completed shards with exact manifest validation, never duplicate rows/counters.

## 9. Conditions, Seeds, And Checkpoints

One checkpoint. Primary last-target raw gradients; mandatory diagnostics: last-unit, 16-target raw/unit; c_last, a_last, e_last, c_body_mean, a_body_mean; SAE last, body-frequency and body-amplitude patterns. No winning condition selection. Seed20260930 defines ordering; bootstrap20261001 (2,000 draws); permutations20261002 (999); random groupings20261003 (100); random orthogonal spans seeds31,43,59. Spectral transfer ranks1,2,4,8,16,32,64,128,256, capped by numerical rank. SAE/native-a projector ranks8,32,64; actual lower ranks are reported and random controls use those exact ranks.

## 10. Primary Metric And Frozen Analysis Plan

Let F/R be fit/readout, g_j the flattened last-target gradient, μ the fit pooled mean, μ_s the fit mean of domain s. Equal record weights also give equal domain/subfield weights under the balanced panel.

\[
Q_D=1-\frac{\sum_{j\in R}\|g_j-\mu_{s_j}\|^2}{\sum_{j\in R}\|g_j-\mu\|^2}.
\]

Compute via Gram entries and mean weights in FP64. Exclude self-pairs only from pairwise relationship summaries; keep each event's squared norm for prototype error. No target clipping, sign balancing or outlier deletion. Report numerator/denominator, raw units, Q and norms. If denominator≤100 times the measured per-gradient squared numerical discrepancy or ≤1e−12, primary is INSUFFICIENT_LOW_VARIATION.

Bootstrap2,000 times, independently resampling64 records with replacement inside each of eight subfields in **both** F and R; refit prototypes each draw. Compute two-sided percentile95% interval with linear quantiles. This is conditional record-level uncertainty and does not cover unknown paper clusters, different checkpoints or sources. The 999 permutation control independently shuffles balanced fit-domain labels across all fit records, leaves readout labels fixed and computes Q without choosing parameters; p=(1+#Q_perm≥Q_observed)/1000. It is a label-association diagnostic under exchangeability, not a causal randomized treatment.

Support: qualified data/numerics, CI lower>0 and p≤0.05. Non-support: qualified CI upper≤0. Otherwise insufficient for the primary directional claim. No practical-gain threshold is imposed, and statistical support is not router usefulness. Only one primary test. All other intervals, ranks, atoms and comparisons are descriptive; no uncorrected feature-wise discoveries. Historical exposure is retained in every conclusion.

## 11. Secondary Metrics And Guards

### A. Domain relationships, commonness and scale

For last and16 gradients report raw K and kappa fit/readout4×4 block means, standard deviations, medians, positive/negative fractions, counts and norm distributions. Same-domain blocks omit self-pairs. Pair counts are not independent sample counts; uncertainty derives from record resampling. Also show fit-to-readout4×4 mean-gradient inner products, pooled μ, domain δ_s and within-domain residual energy. Fit total second moment equals pooled-mean energy + between-domain energy + within-domain energy; verify relative closure≤1e−6. Between-domain rank≤3 is structural.

Report Q for unit gradients and the16-target scale with the same bootstrap draws, without selecting the best variant. Cross-subfield robustness: fit each domain mean from its first category and evaluate only its second category on readout, then reverse. These two secondary Q values are not additional confirmation tests.

Scale grid m=1,4,16,64 records:100 fixed draws take the first m records of a fresh permutation in each split/domain, and compare these four true-domain means with four disjoint globally mixed groups of size m from a fresh permutation. No source balancing beyond the original balanced panel is claimed for a sampled group. Compute same-label fit/readout mean alignment and domain-minus-random alignment. At m=1 the definition remains comparable. Random averaging is a control, not a semantic null that erases all source structure.

Nuisance table covers target identity overlap, target frequency estimated only from fit16 targets, CE, c/e/gradient norms, and pair products. Fit loss and log-gradient-norm quartiles define bins applied unchanged to readout. Show domain relationship contrasts within those bins where each contributing cell has≥20 pairs; report omitted sparse cells and retained coverage, never remove those records from the primary. Same/different-target strata are separate descriptive results. These controls do not isolate semantic causation or prove all lexical effects removed.

### B. SVD and relation to native representations

For last/16 gradients, c_last/a_last/e_last/body means and SAE last/body-frequency/body-amplitude vectors, save the entire fit sample-visible eigenvalue/singular-value spectrum. Analyze raw second moments, fit-centered variation and row-unit-normalized geometry separately. Negative eigenvalues below −1e−7×largest eigenvalue fail the Gram guard; numerical negatives within tolerance are recorded and clipped to0. Numerical rank uses eigenvalue>1e−10×largest. Report participation ratio, entropy effective rank and counts to50/90/95% energy with their precise denominators.

Axes are fit-pooled, never separately rotated per domain. For centered gradients, use centered fit/readout cross-Gram to compute readout coefficients on the fit right-singular directions; report retained readout energy at every rank. Same procedure applies to other vectors. No train-only spectrum is called stable population rank. Plot readout coordinates on the first two fit axes with explained readout fraction. Kernel alignment between representation/SAE and gradient centered Gram matrices uses all off-diagonal entries; report raw and label-block-deviation versions, only descriptive. Similar geometry is neither a successful future predictor nor causal use.

### C. Complete trained-SAE activation patterns

Collect indices/positive values for all255 causal input positions, all1,024 records, all30,000 atoms. Positive firing means value>0, not merely TopK index membership. Keep zero/unobserved atoms in every all-atom table; do not call a zero count globally dead.

For each split×domain×atom and pooled split: positive-token frequency; record prevalence; unconditional amplitude mean/SD; conditional-positive mean/SD and10/50/90% quantiles; maximum and original record/position pointer; conditional decoder contribution norm; last-position counterparts. Aggregate within records first where the uncertainty unit is a record. For each record retain full30,000-dimensional frequency/amplitude vectors, active-atom count, positive TopK count, activation entropy/effective count, a norm, reconstruction relative squared error and cosine, and e·(a−reconstruction) at target positions (sensitivity diagnostic, not measured loss change).

Activation-position profiles use bins0..31,32..63,...,224..254 and preserve bin lengths; report per-atom positive counts/sums. Adjacent-position persistence includes mean support Jaccard, per-atom stay-active count/opportunities and run-length histograms (1..255), resetting at every record boundary. Coactivation uses every positive same-token atom pair, unordered k<l; store sparse counts for all observed pairs per split/domain and marginal counts. Lift is count×tokens/(count_k count_l); infer no significance from large rare-pair lift. Show only fit-selected edges with count≥20, ranked by count then atom IDs, cap100/domain, and their unchanged readout values. The full observed-pair sparse table remains available.

Common selection, separately for body and last: all-domain frequency≥0.01(body) or≥0.05(last), max/min frequency≤2, and max/min conditional-positive amplitude≤2. Specific/enriched selection: p_s≥0.01(body)/0.05(last) and (p_s+1e−4)/(mean_other_p+1e−4)≥2, excluding the common set. A feature may be enriched in multiple domains; report overlaps. Similar activation is an operational criterion, not proof of semantic sameness. Keep all qualifying IDs; never relax thresholds for empty sets.

Common illustrative/projection atoms: first64 by decreasing min-domain frequency, tie atom ID. Domain-enriched: first64 by decreasing enrichment, then p_s, then atom ID. Body selection defines the primary decoder sets; last selection is a separately reported robustness table. Freeze these lists before readout. Every atom gets a readout effect/statistic; selected common criteria and enrichment sign/ratio replication are reported without multiple-testing claims. Example contexts are fit-selected maximum-activation original token windows, not invented semantic names. Whole-pattern distances use all30,000 atoms: cosine, normalized-profile TV and support overlap, showing same-domain fit/readout versus other domains.

### D. Connect SAE to update geometry

Use normalized decoder columns of each fit-selected body set (common and four enriched sets). SVD produces an orthonormal span of ranks8/32/64 or actual available rank; duplicate/collinear columns do not count twice. Native-a fit-centered PCA and three Gaussian-QR random spans at identical ranks are mandatory controls. SAE encodes a, so this comparison is anchored to full a, not silently to c.

Compute PG for last and16 gradients, projected Gram K_P, and complementary K−K_P. Report trace/energy retention, fit-common-mean and fit-domain-deviation capture, readout projected 4×4 signed means, projected Q_D, and heldout off-diagonal reconstruction error of K by K_P. Check K=K_P+K_complement to relative1e−5 on explicit small gradients. Distinct sets' projectors may overlap; never add their reported fractions. Empty/low-rank sets are named outcomes; rank-zero capture0 does not mean no SAE information.

For each of the30,000 individual normalized decoder directions d_k, save fit/readout single-target mean projected-gradient energy E[(d_k^T e)^2||c||²] by domain, plus whether/how frequently that atom fired. This separates activation from output-direction gradient sensitivity. Individual atoms are nonorthogonal, so their energies cannot be summed into total energy. All-atom associations are descriptive; no posthoc top-gradient atom selection enters the registered span comparison.

### E. Numerical and freeze guards

Full-forward W autograd must agree with e c^T for the last target, and with the mean16 outer products for the aggregated target, relative Frobenius error≤1e−5; non-target-position derivatives≤1e−7 of selected derivatives. Wc versus native a relative≤1e−5; captured a equals native SAE input. Tail CE versus full CE absolute≤2e−5. Exact-repeat encodings/CE are checked; frozen buffers and in-memory state digest remain unchanged. Checkpoint file SHA must match before and after. Gradients finite; zero norm is retained but normalized metrics mark undefined. If >1% gradients zero, normalized inference is insufficient; raw remains separately eligible. SAE widths, indices, nonnegativity, normalized decoder norms, TopK≤32 and exact repeated encoding must pass.

## 12. Known Good / Known Bad / Known Confusing Cases

Before full: synthetic same-domain gradient prototypes give positive readout Q; random labels do not automatically pass; identical pooled/domain prototypes yield Q0; wrong record permutation is rejected; last/mean16 outer products match explicit flattened gradients; raw/centered mean decomposition closes; negative off-diagonal entries coexist with a PSD Gram; projection+complement closes; duplicated decoder atoms reduce rank; constant high firing across domains with unequal amplitude is rejected by common criterion; zero-valued TopK entries do not count; run lengths stop at document boundaries; cross-split ID/hash collision fails; deliberate NaN fails. These are implementation tests, not natural-language evidence.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal/input → operation → output | Pass, stop and handoff |
| --- | --- | --- |
| S0 | Authorized documents + original panel → schema/hash/exposure/duplication audit and immutable indices → manifest | Missing/mismatched source stops; duplicate dependence is flagged, never silently filtered |
| S1 | OPS16 + exact checkpoint → native/gradient/SAE/freeze tests, resource measurement → smoke receipt | All mathematical/numerical guards required; no readout-driven choice |
| S2 | Panel + passed S1 → four independent GPU extraction shards → c/a/e, mean16 gradients, all-position SAE indices/values, losses | Every record/target accounted for; any invalid required record stops analysis rather than deletion |
| S3 | Fit arrays only → prototypes, spectral axes, activation sets → frozen fit registration | Save IDs, rules, axes and hashes before readout summary |
| S4 | Frozen fit + readout → primary Q/uncertainty, spectra, scale, activation and span diagnostics | All diagnostics required irrespective of main result; stage failure is local and explicit |
| S5 | Receipts + outputs → numerical/accounting audit, figures, bilingual Summary/Detailed | Separate operational completion, registered comparison and Unknown human judgment |

Engineering smoke may use a standalone allocation or an internal S1 at the start of one authorized staged allocation. In the latter, the job is named `*-analysis`, and code **must** abort before S2 unless S1 passes and estimated1.5×remaining duration fits budget. It is not a waived smoke. Local known-case tests precede submission. Register this staged execution as one allocation, not a completed smoke claim in advance.

Execution surface `acp`; resource profile `h100-4-reserved`; image `shphd-lite-0911`; single node, four independent extraction workers, no gradient averaging across workers. Resolve all physical values from [execution envelope](../../../../../../../docs/execution_envelope.md). Budget≤24 GPU-hours total, one allocation≤6 hours, output≤50GiB; local preparation/read-only work≤60 minutes per bounded analysis. No automatic profile change or extra full sweep. Repairing an engineering failure must preserve original evidence and use a new attempt with a documented source revision; scientific choices freeze at first measurement. Initial startup observation≤5 minutes absent a longer user instruction; if still queued, report the existing job rather than resubmit.

## 14. Algorithm, Output, And Provenance Contract

Execution root `/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/`; attempts `runs/<UTC>`. Research documents here, raw data/arrays/scripts/logs there. Intended modules: `prepare.py`, `collect.py`, `analyze.py`, `run.py`, `test_contract.py`, `plot.py`; actual hashes recorded before submission. Reuse inspected `20260930_natural_ntp_compatibility/scripts/core.py` for the frozen loader/capture, adapt vector CE and positions; inspect underlying model/SAE code. Runtime reuses the existing offline dependency layer. No binary toy task or old21B arrays.

| Artifact | Required contents |
| --- | --- |
| `data_manifest.json` / `selected.jsonl` | Original hashes, retained IDs/order, categories, splits, positions, exposure and duplicate audit |
| `registration.json` | Anchor/Protocol/config/code/source hashes, authorization, stages, seeds, selected checkpoint |
| `smoke_receipt.json` | Each guard, observed error, device/memory/time and full estimate; PASS only after execution |
| `collection/shard_*` / collection receipt | Record IDs; c/a/r/e per16 positions; losses/targets; last/body summaries; mean16 gradients; all-position SAE index/value; reconstruction/persistence inputs; exact counts |
| `fit_registration.json` / fit arrays | Means, axes/eigenvalues, atom-set IDs and ranking, random bases/seeds; immutable before readout summaries |
| `primary.json` / `domain_relations.csv` | Q, MSE terms, CI/permutation, statuses,4×4 raw/normalized relations and valid counts |
| `spectra.csv` / spectral arrays | All sample-visible singular/eigenvalues, ranks, fit/readout energy, common/between/within decomposition |
| `activation_stats.csv` / `activation_patterns.npz` | All30,000 atoms including zeros; every domain/split; frequency/amplitude/quantiles/context pointers, body/last/position/run statistics |
| `coactivation/*.npz` / pattern tables | Full observed sparse pair counts/marginals; fit-selected display edges; all-atom profile distances |
| `atom_sets.json` / `atom_replication.csv` | Exact common/enriched IDs/criteria, intersections, heldout replication and empty sets |
| `atom_gradient_energy.csv` / `projection_results.csv` | All atoms' direction sensitivity; selected SAE/PCA/random spans, rank, energy, signed K, reconstruction and Q |
| `scale.json` / `nuisance.csv` | Scale/random-group contrasts, subfield transfer, nuisance strata counts and coverage |
| `verification.json`, `failure.json` if needed | Required-file/count/hash checks, frozen checkpoint, stage eligibility/failure, human judgment Unknown |
| `figures` + source manifest | Domain K/kappa matrices; raw/centered spectra and transfer; pooled/between/within energies; all-atom activity distribution and fit-selected heatmaps; position/persistence/coactivation; SAE/random update capture; scale |

Collection uses four workers partitioned by retained record index modulo4; each record appears once. Sparse SAE arrays remain authoritative, and every summarized number has a source field/formula. Full sample gradients may be memmapped to avoid duplicated RAM; single-target K can use factor products. Pairwise analyses respect shared endpoints in uncertainty. No all-pair matrix is reconstructed by placing only old disjoint-pair observations into zeros.

The runner saves an append-only stage log, immutable source snapshot, resolved device/image tuple, durable mounted pod log and failures. Refuse existing nonempty output roots. SHA256 hashes identify source checkpoint, panel, code and scientific contract. Software-only changes after a failed smoke are recorded; outcome-based changes require a separate amended eligibility statement.

## 15. Success / Failure / Insufficient Evidence

Operational COMPLETE requires every mandatory stage and artifact, or an explicit local failure/empty result with its scope. Primary support/non-support/insufficient follows §10 only. H2: describe reproducible retained energy and mean/norm alternatives, without inventing a low-rank cutoff. H3: activation replication and update-span coverage are separately reported; equal-rank random controls delimit meaningful capture. H4: improved stability must be compared with arbitrary grouping and cannot rescue H1. Missing source IDs, violated numerical identities, failed freeze or invalid primary data make affected evidence ineligible; never rename failure as a semantic finding.

## 16. What This Cannot Claim

Not untouched confirmation; not paper-independent population inference; not domain-semantic causality; not all possible linguistic groupings; not SAE atom semantic purity or causal use; not irreducible conditional variance; not actual finite-step loss harm; not a prospective c-only predictor; not improved training or expert isolation. All positive/negative associations are state/matrix/source/scale conditional. Low-dimensional four-mean geometry and finite-sample rank caps are mathematical constraints, not discoveries. The previous `NON_SUPPORT`, `MODULATION_WITHOUT_NET_HARM` and unrun branches remain unchanged.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Basis and status |
| --- | --- |
| A question/boundary | Researcher accepted domain-first common/specific analysis; HUMAN_CONFIRMED_DIRECTION |
| B panel/provenance | Verified existing panel; AI_SPECIFIED_UNDER_EXPLICIT_DELEGATION; historical exposure explicit |
| C task/supervision | Explanatory analysis with labels/gradients, no representation-only claim; within accepted scope |
| D model/architecture | Verified S7/SAE assets; same-state mapping; AI operationalization |
| E objective | Frozen pure NTP measurement, no training; AI operationalization |
| F comparisons | Main prototype contrast plus mandatory SVD/activation/projection/scale controls; AI operationalization |
| G execution | Four-H100 Reserved explicitly authorized; bounded budget/stages specified here |

The user's explicit no-further-approval delegation supplies execution authority for these concrete in-scope choices; do not fabricate individual A-G confirmations or ask them again. Cross-block audit checks fixed targets, causal positions, SAE site, projection dimensions, fit/readout separation, record-level uncertainty, complete activation coverage and budget before registration. Its result is recorded with source hashes, not presumed.

Freeze the scientific body before the first S1 measurement. Execution/result state goes in separate append-only records; this NOT RUN snapshot is retained. Any material deviation is an appended dated amendment with reason and effect on eligibility, never a silent rewrite. Human result interpretation and next research priority remain Unknown until supplied.
