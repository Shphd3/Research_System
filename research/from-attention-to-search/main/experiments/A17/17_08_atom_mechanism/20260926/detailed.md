# Detailed: atom usage and local update channels

Primary [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_08_atom_mechanism/17_08_atom_mechanism_anchor.md); frozen [Protocol](protocol.md); [English Summary](summary.md); [Chinese Summary](summary_cn.md).

## 0. Quick recap

Static reanalysis and the registered176-branch intervention are complete. A common atom dominates the coefficient-square proxy while reproducible domain preferences remain. The registered aggregate rule returns SUPPORT for conditional local functional selectivity of matchable enriched decoder spans. Full updates help every cross-domain mean; this is not a destructive-interference finding. Engineering qualification passed and job `pt-2lj66pne` SUCCEEDED. No persistent training or checkpoint changes occurred.

## 1. Objects and definitions

| Object | Meaning and computation | Boundary |
|---|---|---|
| Native attention output | Block7 output of `attn.o`, before residual addition | The SAE observes this tensor; it is not the last MLP input |
| Atom | Runtime unit-normalized decoder column; coefficient from the same fixed SAE | Not a verified semantic concept or independent functional unit |
| Frequency | Positive coefficient count divided by 256 per record, then equal-weight domain mean | Not coefficient magnitude |
| Mean magnitude | Zero-inclusive per-record mean coefficient times runtime column norm | Not a firing probability |
| Contribution proxy q | Per-record mean squared coefficient times squared runtime column norm | Cross-atom terms, decoder bias and residual omitted; not total representation energy |
| Local help | Baseline minus updated heldout next-token loss, nats/target | Not long-run shared training or isolation benefit |
| Decoder span removal | Remove the orthogonal projection of the parameter delta on selected output directions | Not deletion of base activations or setting latent coefficients to zero |
| M | Target-relative-other-domain loss change for target span minus matched controls, averaged over twelve cross-source pairs | Conditional fixed-panel mechanistic discriminator; no universal predictor claim |

## 2. Design and evidence connection

Previous [same-panel measurement](../../17_12_domain_update_geometry/historical_support/structure_update/20260926/summary_cn.md) updated the final down projection and found average help. Its observed attention outputs were upstream and therefore unchanged. This round deliberately updates the attention output projection itself: with cached attention context c and block input x, changing W changes a=Wc; all subsequent residual, norm, nonlinear MLP and prediction operations are replayed. Thus the observed representation and functional readout belong to one actual update path.

## 3. Conformance, freeze and deviations

Registration: `/data/250010109/MoE_Router/experiments/20260926_atom_mechanism/registration.json`. This records the exact Protocol, Anchor, selection, source-data and script hashes; predecessor registrations are preserved in `registrations` when an engineering correction is necessary. The researcher authorized object selection and four-H100 Reserved execution without a further permission round; operational definitions remain labeled AI choices within that scope, not individually approved scientific judgments.

| Item | Actual evidence | Eligibility |
|---|---|---|
| Fixed static cache | Same 1,024 records and 30,000-atom dictionary as prior frozen extraction | Descriptive; source batches previously exposed |
| Matchable targets | All four domains have 32 final target atoms and three controls; 384 atom matches satisfy both pooled frequency and q ratios in [0.5,2] | Approximate matching, not exact exchangeability |
| Mathematics extreme atoms | IDs10171 and4949 remain in the unrestricted static list and plots; excluded from the mathematics target set because comparable controls were unavailable; replaced by5428 and22343 from fit ranking. Atom4949 remains in the computing target and some control sets | Their function as mathematics-enriched target members is untested; this is not a global atom exclusion |
| Initial engineering attempt | `runtime/smoke_source_0` was interrupted before model readout while coordinating registration | No scientific evidence |
| First frozen smoke | `runtime/smoke_source_0_frozen/failed.json`: scalar integer buffer cannot be byte-viewed without flattening | Implementation failure before readout; no scientific evidence |
| Amendment A1 | Hash helper flattens buffers before byte view; no tensor computation or scientific rule changed | Separate new smoke; original failure retained |
| Amendment A2 | Actual W_O checkpoint shape1024x2048 replaces incorrect1024x1024 assertion; observed before forward execution | No change of checkpoint, parameter object or update equation |
| Qualified smoke | `runtime/smoke_source_0_a2/complete.json`:44/44 branches, zero no-op/reset error, model/buffers/dictionary unchanged | Engineering only,4 fit+16 readout records on local H100 MIG |
| Full intervention | `pt-2lj66pne` SUCCEEDED; four full H100s,4/4 source receipts,176/176 branches,0 worker exit codes | Eligible for registered conditional exploratory interpretation |

## 4. Actual setup and provenance

Execution root: `/data/250010109/MoE_Router/experiments/20260926_atom_mechanism`.

Checkpoint: fresh-S7 lambda_rec0.1, exact21,000,000,000 pretraining tokens, source root `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100`; milestone `runs/S7_lambda0p1_from_scratch_4h100/milestones/token_021000000000`; state SHA256 `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`. This token count is not model parameter count.

Data: prior `20260925_sae_domain_activation/selected.jsonl` and `activations.npz`. Four domains have two subfields each, 128 records per domain per batch and 256 body tokens per record. Cache indices/values shape1024x256x32. Natural text, no question/answer wrapper. Selection and input hashes are retained. Record-level separation does not establish article independence, and prior inspection prevents a new blind-confirmation claim.

Code reuse: `smoke_sites.py` owns verified model loading and native captures; the earlier `collect_structure_update.py` supplied a functional-delta pattern. The down-only object was not reused for changing SAE-visible attention outputs. The exact runtime model and SAE source hashes are recorded in every worker receipt. Existing mounted Python/HuggingFace compatibility packages are used; no base-image installation.

## 5. Metrics and registered rule

Static profiles average per-record token statistics; per-token concentration first normalizes within each token, whereas domain-total concentration sums q before normalization. Curves use fit-derived order also for readout. The common-atom-excluded remainder is a separate diagnostic with a different denominator.

Functional setup, conditions and primary formula are defined precisely once in Protocol sections C-F. There are four source gradients, two independent step sizes and22 conditions per size:176 branches. Each uses all512 readout records at16 fixed prediction positions. The primary M and unscaled guard use12 cross-source pairs. Bootstrap draws2000 within domain/subfield, sharing record draws across all conditions. Intervals condition on the fit gradients, chosen atom sets, checkpoint and fixed control seeds; they do not cover source-data, paper, seed or model uncertainty. Secondary per-cell intervals are not simultaneous discoveries.

## 6. Evidence lineage

| Claim | Raw source | Transformation and aggregation | Direct result | Boundary |
|---|---|---|---|---|
| Common atom dominance | Cached positive indices/values, normalized runtime decoder | Per-record q, equal-weight domain mean, common fit atom retained in both batches | Atom24605; readout-domain shares85.83%–90.50% | Coefficient-square proxy, not original energy or function |
| Broad cross-text use | Same cache | Union of positive atom IDs over all records |14,192/30,000 | Finite selected panel, not population dictionary occupancy |
| Domain usage replication | Fit-only unrestricted32 frequency-enriched atoms | Recompute same enrichment signs in separate batch |32/32 each domain; frequency-profile r0.972–0.992 | Descriptive; not pure semantics or control-matched intervention set |
| Dispersed remainder | Same per-domain q profiles | Exclude24605, renormalize remainder, retain fit ordering for readout |90% needs700–1,898 atoms | Secondary denominator; cannot replace full contribution curve |
| Selective update-channel mechanism |176 branch arrays and per-record readouts | Registered M, paired bootstrap and qualification gates |Full M9.416966e-6 [5.497630e-6,1.349434e-5]; half4.678837e-6 [2.707425e-6,6.740931e-6] | Conditional fixed-panel aggregate SUPPORT; not every domain/pair independently confirmed |

Numbers and full domain table: `analysis/static_statistics.json`; arrays: `analysis/atom_profiles.npz`; transformation: `scripts/build_atom_portrait.py`. Mechanism selection refinement: `scripts/refine_matchable_sets.py` with `analysis/atom_sets.json`. The static figure list remains the unrestricted descriptive list; the formal target list is explicitly matchable.

## 7. Main figures and eligibility

The two static figures are the minimal current deliverable. Purpose, setup, axis definitions, observed conclusions and limits are adjacent to each figure in Summary. The portrait uses common atom identity, split replication and distinct frequency/magnitude panels. Concentration separates per-token sparsity from domain-total concentration and explicitly shows the dominant common atom. Atom order is a display convention, not a Gaussian variable. Images physically live in the date's `figures` directory; their execution originals and identical reading-copy hashes are in `analysis/static_manifest.json`.

## 8. Round record and execution

Question: does stable atom enrichment locate selective local learning effects? Controlled setup: same frozen model, dictionary and natural text panel; only virtual final-attention projection changes. Fit records choose spans and gradients; previously exposed disjoint readout records measure effects. Static analysis and all176 intervention branches completed. Static evidence gives a common high-contribution background plus weaker domain preferences; controlled update redirection adds conditional aggregate functional selectivity. The next decision is independent-text replication of the fixed rule, not a claim that sharing is harmful or that isolation would improve training. Detailed execution and outcome evidence follow below.

## 9. Interpretation and next decision

Static evidence supports a common dominant component plus reproducible, more dispersed domain preferences. The intervention supports a conditional aggregate local functional relation for matchable enriched spans. It does not establish Gaussian structure, semantic specialization, independent atom causality or destructive interference. The single AI-proposed next decision is whether to freeze this selection/intervention rule and test it on new article-independent text: replication would justify deeper input/error-signal decomposition; failure would stop treating the rule as transferable. This further experiment was not run.

## 10. Artifact map

| Artifact | Role |
|---|---|
| `analysis/static_manifest.json` | Input/code hashes and identical evidence/reading copies for both figures |
| `analysis/static_statistics.json` / `static_findings.md` | Direct static table and bounded reading |
| `analysis/atom_profiles.npz` / `figure_atom_order.json` | Full dictionary profiles and fixed identity order |
| `analysis/atom_sets.json` | Frozen matchable targets, controls, skipped extremes and all matching diagnostics |
| `registration.json` / `registrations` | Current registered hashes and preserved predecessors |
| `runtime/smoke_source_0*` | Isolated engineering attempts, receipts and failures |
| `runtime/source_<domain>` | Complete full caches, derivatives, branch arrays and completion receipts |
| `acp_receipts` / `runtime/execution_certificate.json` | Submission versus actual execution evidence |
| `analysis/mechanism_*` | Complete-result aggregation and lineage; supplementary readout explicitly post-hoc |

Code workspace and all execution-relative paths above resolve under the stated execution root. No existing live run, Focus, PROJECTS state, commit or publication was changed.

## 11. Submission and engineering receipt

ACP job: `pt-2lj66pne`, display `atom-mechanism-0926-full`, accepted2026-09-26T05:41:21Z. Resource profile `h100-4-reserved`, resolved spec `n6ls.iu.i40.4`, one node/four H10080GB, quotaRESERVED, image key `shphd-lite-0911`. Exact expanded image, mounted volume and command are in `acp_receipts/submit-atom-mechanism-0926-full-20260926T054120Z.json`. Supported submission template was dry-run checked before create. Runtime `scripts/runtime.sh`; launcher `scripts/run_four_h100.sh`; four independent source workers with distinct CUDA_VISIBLE_DEVICES. The registered script verifies hashes, repeats target-GPU/numerical guards, persists pod/worker logs, aggregates only four complete workers and terminates at the3600-second bound.

Smoke A2 elapsed55.17 seconds, source4 fit records/16 readout records,44 independent virtual branches,0 optimizer updates. Full-sequence FP32 replay maximum hidden error0 at zero and both source deltas; selected-position replay error<=1.72e-5. Native attention output replay error0. This is the qualified mixed numerical path, not a claim of exact equality to the all-native BF16 model. The smoke proves implementation qualification only, not H1. Frozen input/source hashes remain unchanged. Supervision owner: Codex thread `01a0db36-5ae0-7e23-8e61-6f154608d8a4`.

## 12. Completed full execution and functional evidence

ACP reports start2026-09-26T05:46:09Z and completion05:48:09Z, stateSUCCEEDED. Persisted launcher receipt `runtime/complete.json` records104.317 seconds including aggregation,4 zero worker exit codes and176 expected branches; each source has44 actual branch receipts. `runtime/execution_certificate.json` verifies four distinct assigned CUDA devices, each full H10080GB, with all profile/image/runtime values. Durable pod log: `acp_receipts/pod/atom-mechanism-0926-full-20260926T054610Z.log`. Four workers took93.76–94.36 seconds each and used about2.03GB peak allocated GPU memory. This was four independent source workers, not distributed optimizer training.

Every worker preserved base W, full buffer hashes, normalized dictionary hash within that execution, and sampled all-model state. Full replay of the registered FP32 tail matches the complete modified forward exactly; selected-position replay has small FP32 kernel-order differences (recorded per worker), with exact zero-delta repeat/reset readouts. Neither these checks nor the arbitrary tiny virtual step establish long-run training stability. Runtime dictionary hashes may differ from the local MIG diagnostic because normalization is computed on different devices; the checkpoint, dictionary source and norm rules are fixed, with within-worker immutability checked.

Primary source: `analysis/mechanism_results.json`;32 source-target-step contrasts: `analysis/mechanism_source_target_contrasts.csv`; all704 branch/readout-domain cells: `analysis/mechanism_all_conditions.csv`; raw values in `runtime/source_<domain>/rho_*__*.npz` and `results.npz`; transformation `scripts/analyze_mechanism.py`; exact2,000 paired draws in `analysis/mechanism_bootstrap_indices.npz`; hashes in `analysis/mechanism_manifest.json`.

All eight source-improvement lower bounds exceed zero. Full and half M values and conditional intervals are in the lineage table. The unscaled target-selectivity guard is4.573188e-6 [2.071528e-6,7.083099e-6] and2.294472e-6 [1.029515e-6,3.551536e-6]. All four target-averaged points are positive, but biology's intervals cross zero. Physics-source/computing-target is the sole negative cross-pair point at both steps, also with intervals crossing zero. Eight of twelve individual cross-pair intervals exclude zero at each step; these are descriptive, not simultaneous discoveries. Update norm restoration factors range1.012499–1.046300. Matching frequency/q within a factor of two and restoring total parameter norm do not make all representation perturbation magnitudes equal.

Full-update cross-domain means are all helpful: full-step1.044962e-4–3.253249e-4, half-step5.251355e-5–1.628180e-4 nats/token, with each conditional interval lower bound positive. Thus the identified contrast concerns selective removal of benefit relative to full update, not harm relative to baseline. Per-record attention changes, SAE coefficients/support changes and loss sensitivities are stored; they are measurements on the affected pathway, not merely an algebraic story. Selected decoder-span interventions do not prove that independent SAE coefficients mediate the effect.

The new reading figure `../../figures/atom_update_consequences.png` displays full help, all source/target contrasts, pooled primary/guard intervals and target heterogeneity. Its four panels answer those four questions; colors and numbers use millinats/token. The only registered result is the aggregate SUPPORT under the stated gates. It cannot be upgraded to pure semantics, all-domain universal specialization, destructive interference or an isolation method recommendation.

Editorial clarification: the frozen Anchor's phrase that unmatched extreme atoms are outside the primary test means exclusion from their mathematics target-set role. It was overbroad if read as exclusion from every target/control set:4949 also participates elsewhere. The frozen `atom_sets.json` always specified those roles exactly and execution followed it. No sets, comparisons or results changed; Summary states the corrected role-specific boundary.

## 13. Post-hoc descriptive connection to local loss sensitivity

After viewing the registered result, `scripts/summarize_mechanism_readout.py` generated `analysis/mechanism_supplementary_readout.json` from existing arrays and CSVs. It records formulas, aggregation, source/script hashes and verifies all176 branch hashes. It changes no frozen script, model run, atom selection, bootstrap or support criterion.

For native attention output a=Wc, a branch produces delta-a=delta-W c. First-order predicted help is minus the inner product of the baseline loss derivative with delta-a; the derivative already includes the16-position mean normalization. All16 source/readout cells are equally weighted, with128 records per cell. Sources reuse the same512 readout texts; there are not2048 independent texts.

| Descriptive quantity | Full step | Half step |
|---|---:|---:|
| Mean per-token native representation-change norm |0.101330|0.050665|
| Mean SAE-coefficient L2 change |0.285787|0.145927|
| Mean SAE support-set Jaccard distance |0.002377|0.001202|
| Mean-level relative absolute first-order error |0.5191%|0.2660%|
| First-order prediction substituted into registered M |9.37181e-6|4.68590e-6|

The error ratio is the sum of absolute mean prediction errors over16 cells divided by the sum of absolute measured cell means; it is not a sample-level relative-error guarantee. No supplementary confidence interval or threshold is introduced. The small-step effects are consistent with the alignment of actual representation displacement and target loss sensitivity. This does not explain how the domain preferences formed, prove independent latent-coefficient mediation, match all representation perturbations or establish long-run interference. The supplementary file is linked as evidence for the derived route's explanation, while the registered outcome remains owned by `mechanism_results.json`.
