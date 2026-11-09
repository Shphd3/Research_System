# Protocol v0.1: The Frequency–Contribution Bridge and Relation Refinement

Status: for researcher review; execution has not been approved (`DRAFT_NOT_EXECUTABLE`). The first stage is profiling and dispatch analysis without training. Entry conditions for learning are listed separately. Do not rewrite completed experiments or overwrite old results.

## 0. The sole main line for this round

Describe the composition of an input's final-layer contributions by feature frequency → test its correspondence with token frequency and context → test the additional organizational value of relations within the same frequency band → test learning later under a shared budget.

The main routing rule uses raw contribution shares. Baseline-relative calibration is only a control. Do not silently switch from the raw rule to calibration because the raw rule produces undesirable loads.

## 1. Assets, data, and unit of observation

Reuse frozen Qwen3-0.6B Base and the final CrossCoder jointly encoding 14 layers. Verify the dictionary, gating, decoder coordinates, sample IDs, causal positions, and existing caches. Do not retrain the dictionary. The original h and z must align position by position.

The primary data are the same 85,548 answer-prediction positions in TRAIN from the current Tulu SFT experiment. At position t, the observations are h_t/z_t, the target is answer token v_(t+1), and the current token identity is v_t. The first answer-prediction position may be at the end of the prompt; mark it separately. Text to the right is for interpretation only and must not enter routing.

Estimate both p_i and f(v) over these valid TRAIN positions, and state this denominator. Token frequencies over the complete input may be reported only as auxiliary measures. If tokens with zero TRAIN frequency appear in the review split, list them separately as unseen. Do not apply arbitrary smoothing and mix them with known low-frequency tokens.

The existing DEV/EVAL data and results have been inspected repeatedly. Mark all reanalyses in this round as exploratory. Existing EVAL can be used to review statistics, but must not be called a new independent confirmation set. If confirmatory learning follows, freeze a previously unused holdout separated by question. Deduplication of normalized questions does not establish original-document independence or resolve paraphrase overlap or pretraining contamination.

## 2. Fixed definitions and proposed defaults

The Anchor governs all definitions: p is hit frequency; c = z × final-layer decoder norm; M is the sum of contributions within a group; R = M / the sum of contributions over the entire dictionary. c does not contain the sum of decoder norms over 14 layers and is not explained variance.

The following are proposed defaults, not hyperparameters already selected by the user:

- Total experts K = 8; frequency bands B = 4, with K_b = 2 experts per band. This allocation is a simple baseline, not a claimed optimum.
- Divide the range of log10(p) for positive TRAIN frequencies into four equal-width bands, with the final band including the right endpoint. List zero-frequency features separately. Retain all positive-frequency atoms for profiling and routing. Do not manufacture success by removing the rarest atoms.
- Define the low-frequency profile L as the lowest-frequency band F_1. Also report the complete R distributions for all four bands; do not plot only L.
- The profile denominator includes the highest-frequency atoms. The main rule in this round does not remove the Top10. If a historical version excluding Top10 is reused, label it separately as a reference for the old rule; do not mix it into the main comparison.
- Save frequency-band boundaries, support counts for each band, and all tie rules before inspecting this round's review results. If a band is empty or has fewer than two members, stop for design feedback. Do not silently change the number of bands.

Logarithmic bins prevent one large 0–5% bin from swallowing the low-frequency region. They do not assume that Zipf's law holds. Frequency estimates have sampling uncertainty, especially in the tail. Report the proportion and contributions of atoms with fewer than 20 hits and those covering fewer than five dialogues. The 20/5 cutoffs are reliability diagnostics only, not natural semantic boundaries.

## 3. Stage A: Bridging feature frequency and token frequency

### A1. Basic distributions

Output a p-rank plot for the full dictionary, a frequency histogram with zero frequency separate and positive frequencies in logarithmic bins, and the atom count in each frequency band. List the old DCLM p and new SFT p separately. Separate changes in the same atom IDs from curves obtained by ranking each dataset again.

### A2. Current-position profile

For each position, save the current token ID, target ID, dialogue ID, source, position within the answer, M/R for the four bands, total contribution, nonzero-atom count, and contribution share of unknown-frequency atoms. Name amplitude/contribution and frequency separately. Do not present normalized routing scores as raw contribution shares.

### A3. Main token-frequency bridge statistic

At review positions with known tokens, compute s_t = −log10 f(v_t), and test Spearman(s_t, R_1). The main report is position-weighted. Also report a token-ID-equally-weighted aggregation so that repeated common IDs do not dominate every conclusion.

Sort token IDs by their TRAIN frequency and divide them into five groups to display the R_1 distributions. Freeze boundaries on TRAIN, avoid splitting IDs with tied frequencies where possible, and report actual counts. Unseen IDs form a separate group. Compute confidence intervals with 1,000 bootstrap resamples of whole dialogues; do not treat positions as independent samples. The resulting intervals are exploratory only.

Interpretation: a positive correlation whose interval lies entirely above zero supports the proposed descriptive direction. A negative correlation whose interval lies entirely below zero opposes it. An interval crossing zero leaves the direction undetermined. Report effect size regardless of whether the interval excludes zero. Do not call a very small correlation a strong bridge.

### A4. Variation within the same token ID

Preselect token IDs occurring at least 50 times across at least 10 dialogues in TRAIN. Retain missing values when their support in the review split is insufficient. Report the median and IQR of R_1 for each ID.

Use the mean R_1 for each ID in TRAIN to predict R_1 at review positions. Compare its MAE with prediction by the global TRAIN mean. Also report the residual error not explained by the ID-based predictor. This measures how much token identity can explain; it does not prove that all residual variation is semantic.

Display eight eligible IDs sampled randomly with a fixed seed, with at least two types of positions differing in R_1 for each ID. Label random examples separately from high- and low-quantile examples. Show the complete visible prefix and current position. Where needed, show two tokens to the right for reading only. Describe results by answer position, source, and tokenization-prefix format so that format differences are not called semantic discoveries.

## 4. Stage B: Relation-based grouping within frequency bands

### B1. Constructing relations

Use only the current TRAIN binary A to recompute within-band p_ij and φ. Old DCLM φ may serve as a historical reference, not as the current relation. Set w_ij = max(φ_ij, 0) as the positive-coactivation candidate for this round. Negative-edge mechanisms are outside scope.

A proposed simple and reproducible subdivision is: sort features by ID within each band, apply average-linkage hierarchical clustering with distance 1 − w_ij, and cut it into two groups. For atoms with p_i = 1, mark φ as not estimable, use distance 1 for clustering, and list them separately. This does not prove absence of correlation. If a band has no positive edges, report no relation structure in that band. Any forced split into two groups is then only an allocation without relation structure, not a success for relations.

The algorithm requires O(m²) distance storage. The agent must estimate time and memory for the largest band first. If the available implementation cannot handle it, report that and submit a sparse-alternative protocol before proceeding. Do not silently change the algorithm or sample features to meet a deadline. A forced split into two groups is a candidate allocation at fixed K, not a claim that two natural semantic clusters exist.

### B2. Random control and review

For the main random control, subdivide each frequency band into 10 finer bins of log(p), then randomly permute members so that every subgroup retains the relation group's member count in each fine bin. Grouping seed 11 is the candidate for later training. Separately, use 20 seeds fixed in advance to report the range of descriptive dispatch statistics. Report the exchangeable proportion when small bins prevent exchanges. Nearly identical member lists are not a strong random control.

After freezing groups, compute their mean within-group φ on review dialogues and the difference from matched random groups. Pair only estimable feature pairs, and report the number of non-estimable pairs. High within-group TRAIN φ follows from construction. Additional relation evidence requires review φ above the matched random control. As a supplement, split TRAIN in half by dialogue hash, reconstruct groups, and compute the Jaccard similarity of matched group memberships. This is only a diagnostic of conditional stability, not independent validation on new data.

Similar within-group frequency is imposed by the frequency bands and matching conditions. Do not present it as a newly discovered natural law.

## 5. Stage C: Actual dispatch without training

The 2 × 2 candidates are raw share / baseline-relative calibration × φ subgroups / matched random subgroups. All candidates share frequency bands, K, and selection by raw subgroup contribution.

- Main raw rule: first argmax M_b, then argmax of the total subgroup contribution within the selected band.
- Calibrated control: replace only the first step with argmax M_b / μ_b. Keep the second step unchanged.
- Break ties with a fixed stable hash(position ID, seed = 20261019), independent of answer labels. Apply the same fallback when all candidate contributions are zero, and report its rate separately.
- Coactivation computation, banding, group means, and routing must not use the prediction target or future text.

### C1. Receipt and actual composition

For each expert, report position count, dialogue count, hit count for every feature, q_i,e, and r_i,e. Include all observed features and the Top10 high-frequency features, not only members on the expert's list. Set q to NA for empty experts, and retain zero receipt as zero.

Check the identity using denominators from the same split:

\[
q_{i,e} = p_i(\mathrm{split}) \times r_{i,e} / P(\mathrm{split\ routes\ to}\ e).
\]

This shows that higher receipt does not guarantee an equally large increase in within-expert frequency. The identity itself is not an empirical mechanism discovery.

Also report q/p enrichment for every low-frequency atom in its designated expert, and the mean positive log10 frequency ratio between Top10 features and that atom. When the target q = 0, the gap is ∞. List non-estimable cases separately instead of discarding them. This metric describes the relative exposure advantage of high-frequency features; it does not measure gradient dominance or learning interference.

### C2. Consistency of input composition

Restrict each position's c to the selected frequency band and normalize it to unit L2 norm. Use fixed-hash sampling of at most 2,000 positions per expert. Compute their mean cosine similarity to that expert's TRAIN atom-composition center and compare it with matched random groups. List invalid-vector cases separately. This measures similar atom composition, not identical semantics or compatibility for shared learning.

### C3. Readable examples

For each expert, sample five random positions with a fixed seed and separately select three positions with high target low-frequency contribution. Label the two sampling categories explicitly. Show the current token, two tokens on either side, the visible prefix, the main atom IDs/p/c, the four band shares, the selected band/expert, and that expert's q. Do not squeeze an entire relation graph into one text heatmap.

## 6. Learning-stage interface: no automatic launch under this protocol

After the researcher confirms the definitions and resource budget above, freeze a separate training protocol. Retain at least the comparable main arms of the 2 × 2 design. Use the same base, data, expert size, paired initialization, valid supervised-token budget, and optimizer. Do not change expert architecture at the same time.

Given the previous SFT pattern of initial improvement followed by deterioration, freeze a common training budget using independent DEV, then evaluate on a new holdout unused for selection. Do not select the best epoch on an already inspected EVAL and call it formal success. The main learning measures must include answer NLL. Add clearly defined generation evaluation when appropriate for the task. Low-frequency conditional metrics are feature-conditioned; do not call them knowledge-memory measurements.

If a strategy has empty experts, report actual parameter utilization and data coverage. Do not add balancing and continue to call it the raw rule. Do not remove an arm because its result is undesirable; the protocol must explicitly decide whether it enters training.

Future claims about “how many times better” require comparing data, compute, or parameter costs at a common quality threshold. Structural statistics and short-term NLL in this round cannot establish a capacity multiplier. Parameter and compute accounting must include added experts, any learnable router, and the extra online cost of obtaining the joint 14-layer z. Time saved by an offline cache is not free deployment computation.

## 7. Figures and reporting: one question per figure

1. Frequency distributions: feature rank–activation frequency; frequency interval–feature count. List zero frequency separately and expand the low-frequency region.
2. Token-frequency bridge: current token-ID frequency groups on the horizontal axis and R_low on the vertical axis, with panels showing the same ID in different contexts.
3. Relation review: within-group φ differences from matched random controls for each band in TRAIN and review data. Mark insufficient support.
4. Actual receipt: separate panels for expert loads, per-feature receipt rate, and q/p enrichment, with clear denominators.
5. Composition profile: expert ID → feature p/q/c → random and high-contribution text examples.

Keep figure text to quantity names, units, and conditions. Explain outside the figure “what is observed → what it supports → what it cannot yet establish.” Retain every condition and counts of NA, zero, and ∞. Deliver source tables, PNG/SVG figures, frozen configuration, and one concise Chinese synthesis. Do not put every figure into the main presentation.

## 8. Reasoning audit: check before and after execution

- Do not conflate z, decoder norm, c, p, q, and r.
- Do not treat the sum of 14-layer decoder norms as the final-layer contribution. Shared z still comes from 14 layers; this is the measurement source, not independent final-layer encoding.
- Do not conflate feature frequency with token frequency, or the current token with the next target.
- Do not treat frequency-based construction as fresh evidence of natural same-frequency organization.
- Do not treat φ or cosine similarity directly as learning benefit or interference.
- Do not treat repeatedly inspected EVAL as a new confirmation set.
- Do not automatically call score or load changes a capacity improvement.
- Extending this to a shallower-layer MoE cannot let a router access joint z from later layers that have not yet been computed. A deployable encoder would need a separate design. This round concerns only the final layer.
- If results do not support a prediction, retain the original definitions and state which inference is withdrawn. Do not switch metrics to preserve a positive answer.

## 9. Agent handoff prompt

First read the Anchor and this Protocol, and verify existing model/cache/statistics assets. At present, prepare only an analysis execution plan; do not start training. List which items you identify as user-confirmed and which are proposed defaults. Identify implementation blockers, data mismatches, or compute-budget risks. Do not treat this file as approval of all default parameters.

After researcher confirmation, execute the no-training analysis in order A → B → C. At each stage, produce one reviewable update in understanding and its source table. First define the current input's frequency–contribution profile, then test the token-frequency bridge, then test the incremental value of relations within frequency bands, and finally inspect actual expert inputs. Do not fill structural-evidence gaps with learning benefits or semantic conclusions.

Keep old experiments, protocols, and results unchanged. Put every new artifact in a separate directory. Confirm the learning stage separately. Do not silently change hypotheses, sampling, grouping, or stopping rules to meet a deadline.
