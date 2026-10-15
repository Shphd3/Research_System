# Detailed: FIT cross-fitting of router-score shrinkage

2026-10-04. [中文](router_shrinkage_detailed_cn.md) · [Summary](router_shrinkage_summary.md). Scientific design: [Anchor](anchor.md). Frozen contract: [Protocol post-hoc addendum at 16:20 UTC](protocol.md). Execution is complete. `ELIGIBLE` means compliant with this exploratory contract, not eligible as independent confirmation. Researcher scientific judgment and the next decision remain `Unknown`.

## 0. Quick Recap

Results compare selection among constructed matrix increments on a frozen model, not continuing expert training. Pooling raw domain mean gradients before scaling constructs common; FIT chooses one candidate everywhere on DEV, defining fixed selection. Candidates never learn further; a selector fits coefficients predicting consequences. Usage-matched random retains policy proportions and removes input correspondence, separating matching gain from net gain over fixed. Exact operations, grouping and prediction-shrinkage conditions are defined below.

This round asks whether choosing the strength of input-dependent predictions within FIT reduces the original selector's loss while retaining gain over fixed common. Three models, two feature families and two selecting banks produce 12 alpha selections: 11 choose0 and only SALL/base/A chooses0.1. All24 selected pooled conditions improve over original alpha1 with corresponding conditional intervals above zero. In22, selected choices exactly equal common; the remaining two also have negative gain estimates against common. Reducing original-policy loss is observed; pooled adaptive gain over common is not delivered here.

Execution includes24 fold-specific ridge solves,300 OOF rows,60 full final choice arrays,600 all-candidate DEV rows and120 selected-alpha pooled/domain rows. No new LM/SAE forward, GPU job, TEST access or neural-network training occurs. [Completion receipt](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json)

## 1. Objects and Units

This section defines the changed score and data roles. Candidates are previously normalized and measured matrix increments: four domain directions plus a pooled raw-gradient common direction, with no zero update and no further candidate learning. Whole-record FIT folds refit ridge predictors and measured finite CE chooses how much input prediction to use; DEV evaluates that chosen rule. Common describes construction, fixed describes selection, and shrinkage describes deviation of prediction scores from candidate means; these are not expert-training architectures.

| Object | Meaning here | Boundary |
|---|---|---|
| Exact33B | Existing Dense, fresh-S7 and SALL checkpoints at33 billion training tokens | Not parameter count or a paired architecture experiment |
| Event/record | Sixteen prediction positions in a257-token record; resample whole records | Positions are not independent replications |
| A/B banks | Two source batches each produce four domain actions and one common action, already measured with actual finite CE | Corresponding actions come from different source gradients |
| base389 | Current/previous token hashes, visible-prefix frequencies, position/square and log norms of c/a/x | No added category-label predictor |
| fullcx3461 | Base plus full projection input c:2048 and residual state x=r+a:1024 | A particular fitted linear predictor, not information sufficiency |
| Alpha | Strength of a prediction's input-dependent deviation from its action mean | Five fixed values, not a new training learning rate |
| OOF | Predict each FIT record using a fold fit that excludes that record | The selected OOF minimum remains selected, not unbiased |

Finite delta CE is action CE minus original CE; negative helps. Gain is comparator CE minus policy CE; positive helps. Differences are reported in micro-nats/event; absolute CE uses nats. Common averages raw domain gradients before separate normalization; it is not the average loss of the domain actions.

## 2. Relation to the Original Question

The parent question concerns acquisition and retention through shared/private learning under finite resources. This round changes only selection within a fixed action library, holding action measurements, model states and expert histories fixed. It distinguishes useful input-dependent selection from avoiding a weaker rule by reverting to common. It cannot replace training trajectories or rule out useful differences created by future learning allocation.

## 3. Contract, Authorization and Deviations

The researcher's15:53:50 UTC instruction authorized another two-hour window without repeated approval. The detailed cross-fitting recipe is an AI implementation choice within that scope, not researcher confirmation of each scientific choice. The Protocol addendum is dated16:20 UTC. Registration at16:33:23.597671 UTC precedes new fits. Original DEV results and the switching audit were already available before recipe selection: **this was post-hoc from the outset**.

| Registered item | Actual execution | Eligibility boundary |
|---|---|---|
| Original3 models,2 families, fixed_five | Complete; no PCA/SAE family or rejection action | Not other families or six-action policies |
| Four whole-record FIT folds; fold-local scaling |24 solves;384 training and128 validation records each | Article/near-duplicate dependence remains unknown |
| Five alphas; exact minimum/smaller-alpha tie rule |12 completed selections; same alpha within/across bank | No DEV reselection |
| Freeze every final choice before scoring | Freeze at16:34:33.646059 UTC, then DEV evaluation | New computation order does not undo prior exposure |
| Original2,000 record-bootstrap draws | Reused without refitting/reselection | Excludes fitting/selection variation; no multiplicity correction |
| At most8 CPU threads and1,800 seconds | Worker completes in70.58 seconds | Not LM training throughput |

No actual-run retry, omitted condition or post-result family exclusion occurred. Source development and synthetic checks preceded registration; debug outputs did not replace readout. Eligibility matches the registered exploratory scope. Execution success cannot supply independent confirmation.

## 4. Actual Algorithm and Data

Reuse the original panel:8 categories in4 domains;512 FIT records,64/category;1,024 DEV records,128/category;16 positions14,30,…,254 per record. Each source bank has256 records. Exact record/token-string disjointness was checked; article-level, near-duplicate and pretraining overlap remain `Unknown`. The [original Detailed](probe_33b_detailed.md) and [configuration](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/configs/probe_33b.json) own checkpoint, direction, finite-effect and data identities. No checkpoint was reloaded here.

Use NumPy Generator seed1004. In sorted category order, sort that category's FIT record IDs, shuffle with the shared generator, then assign cyclically to folds0–3. Every fold has16 records/category, and all positions follow their record. Rebuild raw base/fullcx features. Form x=r+a at cached activation dtype before float64 promotion. Each fold re-estimates feature means, population standard deviations (exact zeros become1) and label intercepts from its training records only; no all-FIT standardized matrix is reused.

Reuse the original ridge objective: summed squared error plus10 times squared coefficients, with an unpenalized intercept. Ten A/B output columns are solved together without a cross-output penalty. Each fit sees6,144 training events and holds out2,048. Save each fold's scaling, label intercept, coefficients and OOF predictions.

For an action, let mu be its training-fold measured finite-delta-CE mean and q its fold-fitted prediction. Select using mu+alpha(q−mu). Alpha1 returns q directly to avoid cancellation changing its endpoint; alpha0 uses means. For every model/family/selecting-bank combination, compare the complete OOF mean measured delta CE for five alphas and break exact ties toward the smaller alpha. Category identity is used for folding/bootstrap, not as a new predictor.

Finally apply the selected alpha to the original all-FIT frozen predictions and all-FIT action means. Save all60 final choice arrays before DEV scoring. Alpha1 must reproduce every original selector choice exactly; alpha0 must equal FIT-fixed common everywhere. The same choice transfers from A→A to A→B, or B→B to B→A, without reselection. [Registered recipe and source hashes](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/registration.json)

## 5. Metrics and Uncertainty

The primary diagnostic is paired measured finite-CE gain for selected alpha against original alpha1 and fixed alpha0. Five alphas×3 models×2 families×2 selecting banks×2 evaluating banks×5 scopes produce600 rows. The selected12×2×5 conditions produce120 rows:24 pooled and96 domain rows. All candidates remain available; no new alpha or family winner is selected from DEV.

Reuse the original2,000 category-stratified paired whole-record bootstrap count arrays, preserving all16 positions. Models, FIT fits, folds and alpha selections remain fixed in each draw. Conditional95% intervals exclude source sampling, article dependence, fitting/selection variation and multiplicity correction. The24 pooled conditions are not independent confirmations.

Switch rate is the fraction choosing an action other than common. Mean extra cost equals switch rate times mean extra cost conditional on switching. With no switches, contribution is zero but conditional cost is undefined, not zero. Switching diagnostics are point estimates without invented ratio intervals. No practical-effect threshold was selected; researcher scientific judgment remains `Unknown`.

## 6. Evidence Lineage

| Checkable claim | Artifacts and computation | Observation | Maximum scope |
|---|---|---|---|
| FIT-only alpha selection | Fold assignment,6 OOF files,300 CV rows→exact argmin→selection freeze | Eleven0, one0.1 | Recipe outcome, not unbiased utility |
| Correct endpoints | Original all-FIT predictions/choices versus final freeze | Alpha1 identical; alpha0 always common | Implementation identity, not mechanism support |
| Lower original-policy loss | Original effects+frozen choices→paired record means/original bootstrap |24 pooled gains and intervals positive | Conditional exposed-DEV observation |
| No pooled adaptive gain over fixed | Same readout versus alpha0 |22 exact zeros,2 negative estimates | Does not prove absent potential routing information |
| Author recomputation | Separately written raw features, normal equations, OOF and point readout |24 folds and600 point rows checked | Author self-audit, not an independent reviewer |

The [complete output manifest](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json) and [author audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/crossfit_author_audit.json) preserve lineage. The execution script computes bootstrap intervals; the author audit did not separately recompute every interval.

## 7. Results

### 7.1 All12 Alpha Selections

| Model | Family | Alpha from A | Alpha from B |
|---|---|---:|---:|
| Dense | base |0|0|
| Dense | fullcx |0|0|
| fresh S7 | base |0|0|
| fresh S7 | fullcx |0|0|
| SALL | base |0.1|0|
| SALL | fullcx |0|0|

SALL/base/A's OOF alpha0.1 gain over OOF alpha0 is+16.14 micro-nats. This mean was used for selection and is not independent validation. Unshrunk alpha 1 loses to its own alpha 0 in all 12 OOF cases; these fold models differ from the original all-FIT model. The [300-row CV table](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/cv_table.csv) retains every alpha and fold, not only winners.

### 7.2 Selected Pooled Readout

Selected gains over original alpha1 range from+265.74 to+707.13 micro-nats across24 pooled conditions; every corresponding conditional interval is positive. In22, alpha0's gain and interval against common are exactly zero because the actions are identical. This is not a statistical equivalence test.

The only nonzero-alpha rule has the following two pooled readouts, in micro-nats with conditional95% intervals.

| SALL/base/A | Gain over original alpha1 [interval] | Gain over fixed common [interval] | Switch rate |
|---|---:|---:|---:|
| A→A |+283.38 [186.37,380.23]|−6.23 [−20.88,+9.06]|2.5269%|
| A→B |+386.35 [297.29,482.37]|−19.72 [−35.49,−3.45]|2.5269%|

Absolute CE is3.4970349093 and3.4969877835 respectively. Conditional extra cost among switches is246.44 and780.48 micro-nats; multiplying by2.5269% recovers pooled extra cost6.23 and19.72. Identical cross-bank switch rates follow from using the same choice array, not independent estimation.

All domains remain available. For this nonzero-alpha rule, A→A mathematics and biology can have positive gain estimates against common, but their intervals include zero. A→B estimates are negative in all four domains, with a negative interval for computer science. Do not describe every domain as strictly harmed or select a positive estimate as a new policy. [120 selected rows](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_selected_alpha.csv) and [600 all-candidate rows](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_all_alpha.csv)

## 8. Stage Checks and Remaining Explanations

Synthetic checks pass endpoints, whole-record balance, duplicate-record rejection, held-out labels not affecting fold fits, held-out features not affecting training-fold scaling, exact-alpha ties and nested switch sets. Rebuilt raw FIT features through the original all-FIT ridge reproduce predictions within6.25×10⁻¹⁷; final endpoint choices are exact. Alpha1 reproduces original readout means and intervals within8.67×10⁻¹⁹. The switch identity's maximum residual is1.08×10⁻¹⁹.

The author wrote a second computation path without importing the production helper. Saved coefficients satisfy24 training-fold ridge normal equations with maximum relative residual4.40×10⁻¹⁵; OOF predictions reconstruct within1.34×10⁻¹⁶. Training-fold means, standard deviations and intercepts match exactly, with no overlapping training/validation records. This verifies the saved fits' training-fold objectives, not independence from articles or pretraining.

No implementation failure or missing condition was observed. Correct fitting does not establish a correct statistical model. Estimation/selection error, function-class bias, FIT/DEV composition and irreducible target uncertainty remain compatible explanations. With lambda fixed at10, training on384 rather than512 records also changes relative regularization and estimation difficulty; this round does not isolate that change.

## 9. Full Round Record

On2026-10-04 the question was whether FIT-only amplitude selection improves the original rule and beats common. Hold fixed3 checkpoints,2 raw-feature families,5 actions,lambda10 and original finite effects. Fit/select on512 FIT records; evaluate on the already exposed1,024 DEV records; leave TEST unopened. After registration, complete24 fold fits, freeze all choices at16:34:33 UTC, and finish readout at16:34:54 UTC in70.58 worker seconds. Observe eleven alpha0 selections and one alpha0.1;24 pooled conditions improve over original without beating common. Understanding remains bounded to the current fitted predictors and fixed library. Preserve the original negative result; researcher next decision is `Unknown`.

## 10. Interpretation, Boundary and Next Decision

**AI interpretation:** shrinkage mainly reduces loss by canceling current input-dependent switching. OOF selection usually reverts to fixed before DEV scoring; in-sample FIT advantage has not become a robust basis for selection under this record split. This does not establish that adaptive routing has been repaired or identify a unique failure cause.

One may claim reduced original-selector loss for this recipe and panel. One may not claim pooled adaptive gain over strong fixed, insufficient full-input information, useless routing in general, an SAE mechanism, causal MoE architecture improvement, or long-term acquisition/retention. Researcher scientific judgment and the next decision remain `Unknown`; the unresolved relation concerns visible information, estimation and future learning allocation. This record neither closes the question nor authorizes another run.

## 11. Artifact Manifest and Reproduction Entry

Hashes below are12-character prefixes; registration/receipts retain fullSHA-256. Computational payloads remain in execution, without copying large arrays into the research repository.

| Artifact | Purpose/producer | Identity and completion |
|---|---|---|
| [registration.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/registration.json) | Recipe, code/helper/original input identities before fitting |`e4fd6ee22698`, complete|
| [Frozen script](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/scripts/crossfit_router_shrinkage_20261004.py) | Reuse raw-feature/ridge helpers; add four folds and shrinkage |`a25dc736e56b`|
| [fold_assignment.npz](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/fold_assignment.npz) and companionCSV |512 whole records and8,192 event folds|`794aefaec08d`, complete|
| Six OOF files in the [output directory](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004) | Predictions, coefficients, scaling, label intercepts and candidate choices per model/family |Complete; individual hashes in receipt|
| [cv_table.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/cv_table.csv) |300 fold/pooled actual-cost rows|`4ecdf8e20c26`|
| [selection_freeze.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/selection_freeze.json) and companionNPZ |12 alpha selections,60 full choices before DEV scoring|`4238e426921f`|
| [evaluation_all_alpha.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_all_alpha.csv) |600 candidates/scopes with switching diagnostics|`c8c4ed249449`|
| [evaluation_selected_alpha.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_selected_alpha.csv) |120 rows for FIT-selected alpha|`023b8455d7ed`|
| [receipt.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json) |Completion, runtime, checks and full output hashes|`791492c453f0`|
| [Author audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/crossfit_author_audit.md) |Separate recalculation path with authorship disclosure|Complete; not an independent reviewer|

The reproduction entry is the script's `--register` then `--run`. Existing completed results are identity-checked and returned without repeating fits. Logs are under execution's `receipts/second_window_20261004/`; they are not model-training logs. There is no GPU job ID, neural-network checkpoint or new figure. Complete numeric tables and lineage support this decision.
