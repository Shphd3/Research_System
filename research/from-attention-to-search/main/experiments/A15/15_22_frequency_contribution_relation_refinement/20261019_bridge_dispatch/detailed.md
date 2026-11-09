# Frequency–contribution bridge and relation refinement: execution record

[Summary](summary.md), [complete Chinese record](detailed_cn.md).

## Purpose and scope
Test H1, a descriptive association of lowest-frequency contribution with current-ID rarity, and H2, incremental within-band relations versus frequency-matched random refinement. H3, held-out learning and retention, is NOT RUN by design. The researcher explicitly approved A–C on2026-10-19. Scientific judgment remains pending discussion; no Focus or old result was changed.

## Frozen model and observations
Reuse frozen Qwen3-0.6 B Base and final joint14-layer/F16384 CrossCoder, threshold0.051281172782182693, original TRAIN normalization and cached gated z. Decoder28 norms define c=z||d28||; z still needs joint14-layer representations. Cached h/z at t predict answer token t+1. TRAIN 1024 dialogues/85548 positions; EVAL 256/22446. All labels and positions align. Existing EVAL is exposed and exploratory. Question-hash separation does not resolve paraphrases, source documents or pretraining contamination.

Four log-equal positive-p bands contain1694/5673/7013/1097 features.907 TRAIN-zero features form unknown U, never the lowest band. The mean EVAL shares are0.10793%,2.19758%,31.27465%,66.41865%, with U0.001185%. Contribution sums omit biases, centering means and reconstruction residuals, and ignore vector cancellation. They are not information or explained-variance shares. The common raw-coordinate RMS factor374.3495121 cancels in R and M/mu.

## Stage A
Frequency statistics and calibration are TRAIN-only. No smoothing of unseen IDs. Main rho0.2590512 (95% dialogue-bootstrap interval0.2276775–0.2849053) covers19070 known-ID EVAL positions;3376 unseen-ID positions are separate. Equal-ID rho0.1243706, interval0.1222820–0.1670190. All1000 resamples are whole EVAL dialogues. Five token-frequency bins retain count ties, leaving bin2 empty; actual counts1278/0/761/1112/15919. No post-result rebinning.

The per-ID TRAIN-mean predictor has EVAL MAE0.000627126 versus global-TRAIN-mean0.001444182. This56.58% reduction is not explained variance; a mean is not the MAE-optimal constant for this zero-inflated response. Lowest-band share is zero at83.685% of EVAL positions. All1694 lowest-band features have<20 TRAIN hits (median8);717 cover<5 dialogues. Only1198 are EVAL-observed, with median3 positive review hits.

Eight IDs were selected from TRAIN only. Four have no review variation; IDs82/807 have only8/14 positions. Keep these insufficiencies, without replacement.302 cards represent174 unique positions:32 same-ID,168 expert-random,102 high-ranking. Ten high-ranking cards are zero ties. Current-ID17('2') gives a0-share list-number example and a4.23% year-prefix example; this is context/format variation, not identified semantics.

## Stage B
Current TRAIN binary hits determine signed phi. Clustering uses distance1−max(phi,0), average linkage and exactly2 groups per band, ID-sorted. Positive or negative raw phi remains in review averages; p=0 or1 is undefined. Pair-weighted means and subgroup-specific counts/NA are retained. Random seeds11–30 strictly preserve subgroup membership counts in10 within-band log-frequency strata;11 is prespecified for the main comparison.

EVAL relation/random mean phi by band:0.000338375/0.000293662;0.000720086/0.000719576;0.005117788/0.002400523;0.009986101/0.009986126. Bands1/3 exceed all20 controls, with limited absolute effects. Sizes1308/386,5670/3,1861/5152,1096/1 are not balanced or natural semantic groups. Exchangeable fractions are100%,18.97%,100%,1.09%. Split-half reconstruction retains full-TRAIN frequency bands and recomputes phi in each half; band 3 half-vs-half mean matched Jaccard0.32682. Aggregate coactivation replicability does not imply stable membership.

## Stage C
Main raw routing maximizes band contribution sum, then subgroup sum. Calibration changes only the first stage to M/mu. The full hidden vector remains the expert input. All21 groupings×2 scores×2 splits=84 statistics completed, including counts/q/r, loads, NA/zero/infinity, out-of-list features and consistency. There are no trained experts in this analysis; IDs are receiving slots.

Raw routing assigns95.834%ofEVALpositions to band 4 and0%to bands1/2. Lowest-band macro receipt is0%for both relation and random. Calibrated relation receipt72.2180%, random 11 70.4636%;20 random mean/range70.9852%/[70.3282%,72.0609%]. The relation increment over the20-control mean is1.2328 percentage points, versus a large score-induced allocation change. No significance or learning claim is added.

Lowest-band EVAL observed1198, unobserved496(NA). Relation/calibration leaves162 observed features with0 receipt. Event-weighted receipt75.9822%differs from macro72.2180%and lowest-band input load12.4298%. Median assigned-expert q/p is9.9716. The full fixed1694 list has658 infinite Top10-gap entries,496 from globally unobserved features and162 from observed-but-unreceived features; never describe all658 as dispatch failures. Empty-expert q isNA.

Composition cosine uses unit per-position contribution vectors in the selected band, a TRAIN routed center and at most2000 fixed-hash positions per expert. Position-weighted EVAL estimates are relation/raw0.744671 versus random mean0.743254; relation/calibrated0.360255 versus random mean0.352512. Different scores select different populations, so raw/calibrated absolute cosine is not a learning comparison. Expert 0 in relation/calibration still co-carries an average1.38294 lowest-band and195.53932 highest-band active features per input. Counts do not measure gradient dominance.

## Engineering, provenance and cost
Direct checks passed for160 cached-event pair intersections,1024 independent route calculations and320 feature-by-route counts. Two implementation failures were retained and recovered: sparse materialization and absent transformers. Existing ByteLevel decoding was reused and checked against original text in3840 comparisons; no install, download, forward or new activation extraction occurred. No A/B recomputation was needed.

Core completed-stage plus verification wall-time sum is approximately282.8 s, largest recorded process RSS2.404 GiB, current execution payload213.3 MiB. Eight-core existing CPU quota, no GPU job. Exact final receipts record actual costs and limitations, rather than claiming whole-host RSS measurements.

All complete source tables, compressed count/phi inputs, route arrays, q/r/counts, scripts and logs stay at `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_contribution_bridge/20261019T025630Z`. [Asset pointers](FULL_ASSETS.md), [curated manifest](artifact_manifest.json), [completion](completion_receipt.json). The old frozen draft remains intact; the explicit authorization record governs this run. No learning, expert adaptation, new GPU allocation, commit or push occurred. The next experiment remains a researcher decision.
