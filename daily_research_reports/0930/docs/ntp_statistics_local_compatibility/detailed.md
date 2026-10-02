# Detailed: natural-language statistics and local update structure

[Anchor](anchor.md)；[Protocol](protocol.md)；[Summary](summary.md)；[执行记录 / execution record](execution_record.md)。

## 0. Quick Recap

Fixed-state local-update means and functional sensitivity were measured. T=0.006637, CI95=[−0.003738,0.017012], primary INSUFFICIENT; collection/registered analyses complete. Human judgment Unknown; evidence BOUNDED by historical exposure and approximate record independence. No finite-W or long-term sharing outcome ran.

## 1. Terminology / Definitions

F/R are first/tool-fit and second/source-test pools, without model training. Same real target means identical token ID, not identical model prediction. c is2048D matrix input, a its1024D native output, e loss derivative, G=e c-transpose. K is the Frobenius gradient inner product, an ordinary-small-SGD first-order candidate. T is matched-target domain-mean contrast recurrence scaled by historical gradient energy. SAE alpha records firing; unit decoder d defines a direction. I=d-transpose F_a d is model predictive sensitivity, distinct from signed data interaction. MC SE measures probe-computation uncertainty conditional on contexts, not corpus uncertainty.

## 2. Anchor Link And Decision Point

The current object remains a local-update candidate. Functional profiles do not replace the primary mean conclusion. [Anchor](anchor.md) retains its registered scientific body; [Summary](summary.md) owns fresh factual first reading. Human interpretation/question transition Unknown.

## 3. Protocol Freeze, Conformance, And Deviations

Full/source/protocol.md and registration.json identify the frozen scientific contract; current Protocol appends factual amendments.

| Registered item | Actual | Impact |
| --- | --- | --- |
| Fixed33B model/block/SAE |0updates, identical state/checkpoint | PASS |
|2048records,16positions,192quartets | All collected;768unique primary endpoint documents | PASS |
| F-only selection before R | fit_freeze.json generated before R collection | PASS |
| Original numerical thresholds |2failed Smoke;1instrumented DEBUG_ONLY; FP64 backward accumulation then strict PASS | Engineering amendment, no forward/scientific/threshold change |
| Single1% Welch rule |28×5000calibration PASS; primary interval crosses rule | INSUFFICIENT |
| Target-functional≥8documents | F math period6, R physics comma/of7 | Corresponding INSUFFICIENT_COVERAGE; no refill |
| Secondary diagonal renderer | Integer IDs compared with names,16NaNs; original retained and registered1/3summary repaired | No primary value/hash change |
|≤2h/8GPUh | Strict Smoke34.9s; Full223.0s, retries within budget | PASS; default4H100 Reserved |
| Exposure/independence | Prior33B1024panel excluded; N8 historically exposed at21B, no paper-independence certificate | BOUNDED; no untouched confirmation |

No outlier clipping, target changes, R direction selection, sample/probe expansion. Post-run raw domain-difference/MC-SE exports and numeric-ID label repair remain registered quantities, not new statistical tests.

## 4. Actual Setup

S7 sidecar33B checkpoint, historical33,000,000,000tokens/optimizer_step125894,8layers; final W_O1024×2048. TopK32/30000-atom SAE observes native1024D attention output before residual addition. State SHA c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803. Current experiment0training/SAE/router/optimizer steps.

N8_v1 fit/test records:128/category/pool,8categories,2048records,2subcategories/domain. Exclude prior33Bpanel; exact text/token and5-gram Jaccard≥0.8screen gives0collisions. Selection uses registered metadata hashes. Each input uses255tokens; predictor positions14,30,…,254 and actual targets15,31,…,255:16events/document,32768total. Actual targets11/279/315/13 represent comma/space+the/space+of/period. Metadata selects at most1primary event/document, with24strata×8disjoint quartets=192. The primary-selected and all-position populations differ.

Functional panel16records/category/pool:256records/4096contexts/8Rademacher vocabulary probes/context=32768VJPs; SAE activation measured at all32768positions. F-only common/enriched sets select64each,320unique illustrated atoms. Centered pooled-F native-a PCA, SVD-orthonormal decoder spans and random-QR seeds31/43/59; ranks8/32/64 capped by actual rank with matching controls. Bounded c/e/G spectra use64records/domain/pool,4096events/pool. Simulation/calibration/report/probe seeds2026093001/2/3/4; metadata hash keys in Protocol/manifests.

Native FP32 forward, FP64 full-vocabulary probabilities; FP64 projection-backward accumulation and independently checked split VJPs at native primals. No FP64-forward surrogate, reconstruction substitution or encoder differentiation. All numerical/SAE/repeat/state/KL guards qualified by strict Smoke; all shard finite/target-identity checks pass.

## 5. Metrics And Registered Decision Rules

Historical v0=100.77199611476297 unchanged. Quartet Z=A+B−C_FR−C_RF; T averages24strata/v0. Eight independent-record quartets/stratum yield the approximate stratified Welch95%interval. Lower>0.01supports; upper<0.01does not support; overlap insufficient. Observed SE0.005170, df51.9037, CI=[−0.003738,0.017012].

Signed natural/common-support/uniform-target matrices use cross-pool and preregistered within-pool document halves; point estimates only. Real-label mean/covariance and model Fisher remain distinct. Full-p model probes estimate I by8squared projections; MC SE combines probe variance/8 with squared context weights. Below2MCSE flags unresolved computation, not a30000-feature population test. p=q is not assumed.

## 6. Evidence Lineage

| Object | Raw→computation→aggregation | Result | Eligibility/boundary |
| --- | --- | --- | --- |
| Primary means | features e/c→4FP64Gram terms→24×8Z→registeredWelch | T0.006637, interval crosses0.01 | Numerically qualified, record-approximate, INSUFFICIENT |
| Signed group interaction | Quartet terms or natural mean G→cross-pool/half matrices | Natural10points4.291e−5…3.570e−4, all positive | Exploratory, no population sign verdict |
| Sensitivity profiles | fisher u→decoder squares→weighted I/MCSE→domainF/R | Raw same-domain cosine0.9973; centered0.5012 | Natural-context description; incomplete target coverage |
| Firing | encode indices/values→positive counts/amplitudes |240000pool/domain/atom rows;320illustrations | Firing is not causal use |
| Equal-rank control | Same u→F-onlyQ→projected trace/total | rank32common4.472%,PCA3.672%,random3.092–3.154% | Descriptive, no capacity partition/superiority test |
| Gradient geometry |4096events/pool→c/e/GGram→F eigenaxes→R | rawGcenteredrank64Rcoverage7.698%,Kerror0.3633 | Covariance geometry, no H1 rescue |
| Freeze/completion | state/file hashes,target identities/shard counts→receipts |2048records/32768targets/0updates,PASS | Operational fact, not scientific support |

## 7. Main Results

[Primary](evidence/primary.json) is qualified under the stated approximate independence and bounded exposure assumptions, but its interval crosses both0and1%; precision does not distinguish no recurrence from an effect exceeding the candidate scale.

[Domain profiles](evidence/functional_domain_relations.csv) and [selected atoms](evidence/sae_selected_functional_profiles.csv) expose common positive pattern versus domain deviations. Same-domain centered cosines0.7206/0.4705/0.6794/0.1341; overall centered alignment0.5752. About69.8%–86.7%of corresponding-entry differences remain within2conditionalMCSE; this is not proof of population equality. Target-controlled coverage is incomplete and not refilled.

[Controls](evidence/functional_span_controls.csv) distinguish common/enriched sensitivity without requiring SAE victory. [Mixtures](evidence/compatibility_mixture.csv) change point-estimate scale under support/weight changes, not a frequency-explained causal percentage. [Mean/covariance](evidence/mean_covariance_decomposition.csv) and [geometry](evidence/anisotropy.csv) stay independent. Failed/instrumented Smoke evidence never gates or contributes to the primary; strict Smoke and complete Full qualify measurement.

## 8. Visualization Results

[Origins](figures/origins.json) retain source tables/paths/hashes/captions; date-local copies match originals. Primary graph: T/historicalenergy plusWelch interval versus0.01; observed crossing permits no absence claim. SAE paired heatmaps: identicalF-selected atoms acrossRdomains, separate firing/sensitivity scales, no semantic labels or causal necessity. Functional recurrence: raw versus equal-domain-centeredcosines, rowsF/columnsR; no semantic/source causal identification. Span controls: rank32 R natural-contexttrace fractions, samecontext/probes; no parameter capacity interpretation. Signed mixtures: exploratory symmetric point matrices without manufactured intervals. All five figures were visually checked; a legend obscuring data was moved outside and crowded repeated row labels removed. Originals remain in Full/repair/figures_original; numerical sources are unchanged. No Anchor scientific promotion follows.

## 9. Stage Evidence And Failure Decomposition

Source/calibration/CPU mechanism and precision tests PASS. Smoke1 split precision failed; Smoke2 native vocabulary backward precision failed; Smoke3 instrumented only; Smoke4 restored original guards, maximum split relativeerror3.3502e−7,48directions with3adjacent perturbation scales pass localKL checks. Implementation precision failures do not falsify the physical prior or algebra. Primary insufficiency is not a falsification of the candidate mean hypothesis. Integer-ID secondary repair preserves primary hash. Remaining rivals: pooled sensitivity, targetcomposition, source differences, sampling/probe error. Sensitivity does not identify truep−qorcapacitycompetition.

## 10. Full Experiment Record

One2026-09-30round asks fixed-NTP local mean compatibility and functional sensitivity; setup/data/splits in§4. FreezeFtools then measureR, no model training or untouched-corpus certificate. Preserve4Smokequalification/debug attempts. Fullpt-z162gb1w started05:32:22UTC, succeeded05:36:14UTC; program223.0s. All2048records/32768positions/4096functionalcontexts delivered, with primaryINSUFFICIENT and independent descriptive/insufficient branches. Human knowledge update/next decisionUnknown; no long-term inference.

## 11. Interpretation

AI_PROPOSAL: insufficient primary precision coexists with meaningful separate activation/sensitivity measurements; pooled pattern and domain deviations must be distinguished. This remains an interpretation proposal, not a researcher-approved Focus/question transition.

## 12. Claim Boundary

Can state complete bounded frozen measurement, primaryINSUFFICIENT, and descriptive functional quantities/coverage flags. Cannot establish language-statistic-caused conflict, true conditional calibration bias, causalSAEuse/capacity competition, predictive routing, finiteWbenefit or long-term shared/separate benefit.

## 13. Next Decision

Human decisionUnknown. One AI_PROPOSAL: decide whether to improve primary sampling precision before a registered refinement. Completion requires the researcher choosing the uncertainty and new sample/resource contract. Resume from completedFull/Summary; no duplicate submission, diagnostic rescue or automatic expansion.

## 14. Artifact Manifest

[Curated manifest](evidence/artifact_manifest.json) records origins/hashes/frozen code/Protocol; [figure origins](figures/origins.json) add producer/source/caption. Small primary/compatibility/profile/noise/control/geometry reading copies live here; raw arrays/all30000-atom tables/checkpoints remain execution-side. Shards preserve e/c/a/r,targets,loss/p_y,ep/et,codes,reconstruction/residual sensitivity; decoder.npy is the actual dictionary. ContextI/MCvariance/real-label moments,1024²modelFisherand selectedD-transposeF D remain raw; no30000²matrix. Completion/analysis/functional/postrun receipts certify their own operational/analytic scope, not human judgment.

## 15. Links

- [code](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts)
- [runner](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts/stage.py)
- [data/endpoint/functional manifests](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data)
- [Full registration](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/registration.json)
- [frozen Protocol](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/source/protocol.md)
- [immutable sources](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/source)
- [collection arrays and receipts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial)
- [analysis outputs](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/analysis)
- [post-run audit](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/analysis/postrun_audit.json)
- [original failed diagonal rendering](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial/repair/conditional_diagonals.original.csv)
- [qualified Smoke](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/smoke_qualified)
- [failed/debug Smoke ledger](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs)
- [ACP receipts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts)
- [durable pod logs](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts/pod)
- [checkpoint](/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000)

Job IDs: pt-wd184bbc / pt-gqxil5g2 / pt-xm7fqnf3 / pt-k68kogs3 / pt-z162gb1w. Monitor owner: this Codex chat. Default tuple and exact template gates: [execution record](execution_record.md).

Historical command (not automatically rerun; a new attempt requires fresh immutable roots):

```bash
source runtime.sh
python scripts/stage.py --mode full --out runs/full_initial --smoke-root runs/smoke_qualified
```


## Supplement: lexical_readout_01 — existing-atom lexical association screen

**Complete exploratory post-run evidence.** This interprets the existing activation/domain association; original primary T is unchanged. [Registry/provenance](evidence/lexical_readout_manifest.json); [receipt](evidence/lexical_readout_receipt.json).

**Purpose:** test whether the320previously F-selected common/enriched atoms associate with specific lexical identities, separating current input, previous context and actual continuation.

**Hypothesis/rival:** concentrated recurring lexical association versus frequent labels, domain composition or grammar/format co-occurrence. Association cannot identify a unique or causal feature meaning.

**Method:** CPU-only cached positive codes at32768positions. Five separate modes: current token, previous token, previous16-token presence, completed English words in that window, real next target. F chooses one maximum-cooccurrence identity with>=8distinct coactive documents, frozen before lexical R analysis. Report P(label|firing), P(firing|label), base rate, lift, conditional amplitude and within-domain quantities. Whole-word detection uses visible-prefix boundaries/case-sensitive strings, no stemming; unaligned byte boundaries exclude183F/182R events only from word-mode denominators. Other modes retain all events. Lift divides firing-conditional label prevalence by base prevalence; an always-on feature has lift1.

**Result:** F-selected counts188/163/320/320/176; R>=8coactive-document coverage154/131/318/318/152. The prewritten descriptive precision>=80%/lift>=2/8-document flag holds for0atoms in each mode, not a significance or absence verdict.

|Atom/set|F-selected identity|Rprecision|Rrecall|Rlift|Rcoactive documents|
|---|---|---|---|---|---|
|28737/common|current` (`ID320|66.23%|82.59%|43.93|180|
|21638/physics|current` the`ID279|36.00%|3.66%|7.99|27|
|21737/common|actual next` to`ID311|31.32%|53.69%|25.28|105|

These are posthoc illustrations, with[all320×5rows](evidence/lexical_readout_candidates.csv)including insufficient cases. Atom28737's within-domain lift38.69–56.89 has>=8coactive documents in all4Rdomains; its strongest off-label example has current` ((`, suggesting an untested bracket-family alternative. Atom21638 has adequate within-domain coactive coverage only in physics; enrichment does not certify a domain-specific word. Atom21737's continuation association exceeds the1.239%base rate in all4domains; a future actual target is not a forward input.

[True contexts and both counterexample types](evidence/lexical_readout_examples.json)retain firing without label and label without firing. Most previous-context mappings select frequent`the`; highest word-mode precision79.41%has lift only1.55. Base frequency matters; maximum-cooccurrence selection has limited sensitivity to rare exclusive words/atoms.

**Qualification:**7CPUcheck classes PASS: word-selective, always-on frequent item, domain-confound/no-variation, readout reversal, document-dependence guard, whole-word boundaries, CSCidentity. Run18.8s,0model loads/updates,noGPU. F-map and protectedFullprimary/completion hashes unchanged. Reuses cached indices/values/targets and original tokenizerJSON SHA c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539; no training implementation changed. Corpora and originalFulldomain/Fisher results already exposed; lexical fitting uses F alone but is not untouched confirmation. Protocol appendLEXICAL_READOUT_01 owns modes/flags.

**Boundary/next decision:** some selected atoms show lexical/symbol/continuation association, with counterexamples. Not all30000atoms/words/positions, unique semantics, beyond-window context, grouped wordforms, paraphrase invariance or causal necessity/sufficiency. AI_PROPOSAL: lexical association explains part of the observations while one-word-one-atom remains unestablished; human judgmentUnknown. Decide whether to test same-word/different-context and structure-preserving word edits on nominated candidates; not executed or automatically expanded.

Sources:[script](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts/lexical_readout.py),[Fmaps](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/fit_maps.json),[allassociations](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/atom_lexical_associations.csv),[within-domain](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/within_domain_associations.csv),[descriptivecomposition readout](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/lexical_readout_01/domain_frequency_readout.csv).
