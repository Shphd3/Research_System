# Protocol: A17_01_E03 Fixed-Pool Frequency

## 0. Approval Snapshot

`DRAFT_NOT_EXECUTABLE`; result `NOT RUN`. This is a complete AI candidate for review, not a submitted study. The researcher confirmed fixed-pool presentation frequency, FIRST/LAST, the Qwen tokenizer, answer-only loss and separate/combined reporting of both novelty types. The current authorization covers E02 bounded engineering Smoke, not E03, confirmation or SAE execution. Unadopted scientific judgments remain Unknown.

Purpose: determine whether adding A practice changes target B learning differently when their conditional rules agree versus differ. Role: operationalization/proxy test of controlled rules and presentation policies for bounded shared-learning effects. [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md) owns the question; [Focus](../../../../focus/focus_list_rule_shared_update.md) owns the next decision; [E02](../A17_01_E02_restricted_update_calibration/protocol.md) qualifies candidate implementations. [中文](protocol_cn.md).

## 1. Terminology / Definitions

A/B are sample-source metadata, never model inputs. B is the target whose learning is evaluated. Run both target roles: B=FIRST and B=LAST. Same-rule A uses B's rule; different-rule A uses the other rule. The lists differ across A/B pools while the rule-defined mapping agrees or differs. FIRST/LAST have visible instructions and are simultaneously satisfiable.

Frequency means presentations of a fixed pool. A800 repeats the same200 A records four times, not800 unique records or more frequent answer words. Fixed-B addition holds B200 and varies total training. Fixed-budget allocation holds1,000 answers and varies B opportunity. These answer different questions.

## 2. Anchor Alignment

Use the visible list rules and one-answer full-vocabulary loss. The AI extension asks whether presentation policy interacts with rule relation. It does not presuppose harm, identify common/unique modules or settle expert utility. Adding two target roles checks FIRST/LAST asymmetry within this one question, not a new Focus.

## 3. Tested Hypothesis

AI candidate: increased A exposure changes the relative learning consequence of same versus different rules. Generic extra practice might improve both equally; fewer B opportunities might explain poor performance under a fixed budget. The four primary cells hold B opportunity, and match total answers/updates between rule relations at each A count. Budget controls separately test allocation. A positive interaction can mean less help, not net harm.

## 4. Rival Explanations

The policy jointly changes mixture weight, optimizer history, update count and order. It cannot isolate a pure count effect while fixing both B exposure and total compute. Same answer totals are not exact FLOP matching: record prefix tokens and measured time. Visible rule prompts can have different positional difficulty; report both target roles. The pretrained carrier may already read lists well; this is adaptation of existing capability, not acquisition from random initialization. An effect under one restricted matrix need not persist under whole-model learning.

## 5. Data Construction And Provenance

Candidate new frequency release: NOT_GENERATED, no actual output asset ID assigned. Use the qualified20-word vocabulary and one fixed prompt template first. Each source pool has200 distinct ordered lists in100 unordered-content groups: five non-overlapping cyclic-shift content orbits, each with20 vocabulary shifts and two chosen permutations. Require three distinct words, unique unordered groups across orbits and exact position/word/answer balance. A and B content groups are disjoint. Freeze pools across conditions, target roles and seeds; changing A's rule never changes its lists.

For each dev/test split, construct200 order-new lists using B's100 seen content groups and two previously unused permutations; construct200 combination-new lists using new unordered-content groups. All A groups are excluded from B evaluation. B has two training, two dev and two test orders per group, exhausting six permutations. Dev/test combination groups do not overlap each other or training. Store both FIRST/LAST variants per evaluation list: n200 per target-rule novelty panel, n400 target-rule combined, n800 paired records per split. Novelty is relative to all actual A/B task-training content, not pretraining. Test remains unopened for model evaluation until an adopted confirmation contract; structural qualification may inspect metadata without model outputs.

Pool200 replay counts are exact. For500 presentations, use two complete cycles plus100 records drawn as five complete20-shift blocks, retaining exact word/position balance. Freeze the selected half-cycle and order per seed, paired across same/different relations. The B presentation sequence within a seed/role is identical in the four fixed-B cells. Use deterministic balanced shuffles, never lexicographic source prefixes. Hash all pools, permutations, sequences and split receipts.

## 6. Learning Task And Permitted Supervision

The prefix ends at the answer marker; the rule and list are visible, source metadata is not. Only the one correct continuation token contributes full-vocabulary CE, in nats/answer. All other labels are ignored. Same-rule A/B are different examples teaching the same operation, not expert labels. Oracle, actual continuation tokenization, pairing, provenance and novelty checks precede training; register data only after it exists.

## 7. Model / Architecture And Frozen Variants

AI primary candidate: original Qwen3-0.6B Base with only layer27 `self_attn.o_proj.weight` trainable. This1024×2048 matrix has2,097,152 parameters; freeze embedding/head and every other parameter. It localizes the update without imposing a fixed low-rank change. E02 rank8 shared LoRA at the same matrix is a capacity sensitivity, not an equivalent learner. Rank8 adds24,576 factors; its effective cumulative matrix change has rank at most8.

Choose one qualified learner before E03; do not average L and LoRA as replications or choose by favorable B test effects. Candidate direct-matrix LR1e-4 must pass future schedule/readout qualification; E02 also checks1e-5. Scientific adoption and the operating window remain Unknown. Restore original Base, optimizer/RNG/counters and matched learner initialization for every trajectory. Never start from E01 saturated endpoints. Dense/S7 results remain separate carrier evidence.

## 8. Training Objective And Optimization

Global20 valid answer targets/update; independent single-GPU arms, micro5×accum4. Equal mixture:10A+10B;4:1:16A+4B; B-only:20B. Source counts are exact, no fake padding examples. Proposed AdamW: betas(0.9,0.95), eps1e-8, weight_decay0, global_grad_clip1.0. BF16 training with the qualified implementation; common native FP32 evaluation is the candidate primary readout, verified against no-op/restoration before use.

Use constant selected LR from the first update, warmup0. A shared40-total-answer warmup would expose B to40/20/8 answers in B-only/1:1/4:1, introducing a source-dependent schedule. This candidate schedule differs from E02's Smoke and requires its own later bounded engineering qualification. Do not scale LR by trajectory length. Record answer-normalized CE/gradient accumulation, source exposures, prefix tokens, effective batch, optimizer steps and time through the existing observability contract.

## 9. Conditions, Seeds, And Checkpoints

For each target role r in {FIRST,LAST}, use seven independent trajectories:

| Arm | A rule | A presentations | B presentations | Total answers | Updates |
|---|---|---:|---:|---:|---:|
| Same-200 | r |200 |200 |400 |20 |
| Different-200 | other(r) |200 |200 |400 |20 |
| Same-800 | r |800 |200 |1,000 |50 |
| Different-800 | other(r) |800 |200 |1,000 |50 |
| B-only | absent |0 |200 |200 |10 |
| Same-budget | r |500 |500 |1,000 |50 |
| Different-budget | other(r) |500 |500 |1,000 |50 |

B always uses r. Primary2×2: rule relation×A200/800, B200 fixed. Budget comparisons separately contrast800/200 with500/500 at1,000 total answers. Per role/seed:5,000 answers,250 updates. Candidate exploratory seeds29/43/71: two roles×seven arms×three seeds =42 trajectories,30,000 answers,1,500 updates. Calibration seed17 is excluded. All conditions within a seed are paired in data/order/initialization; independent seeds sample independent order/initialization draws. The inference population is these stochastic runs for a fixed Base and dataset, not all models or all natural corpora.

Record capability at B exposures0/40/80/120/160/200; budget arms additionally240/320/400/500. These are reachable exact batch boundaries. Save initial, midpoint and endpoint with full state; verify an external-process next-update resume against an uninterrupted continuation. Equal B checkpoints can have unequal total answers/updates; retain both axes. Training budgets exclude capability evaluation, finite probes and calibration.

## 10. Primary Metric And Frozen Analysis Candidate

For seed s, target role r and novelty panel p, let L be mean B answer CE on the same fixed records at B200. The primary interaction is

\[
I_{s,r,p}=(L_{\mathrm{different},800}-L_{\mathrm{same},800})-(L_{\mathrm{different},200}-L_{\mathrm{same},200}).
\]

Units: nats/answer. Positive means additional A increases same-rule A's relative advantage. Both different/same conditions may still help relative to B-only. The sole combined candidate primary per seed is the equal mean over two target roles and two novelty panels. Equal panel sizes make this equal to record-weighted combined CE contrasts. Report all four components, both role aggregates, both novelty aggregates, absolute CE/accuracy, and every seed's paired effects; aggregation never asserts all components agree.

**Exploration:** use only new dev, three independent seeds; report all effects, mean, median and range, without a confirmatory significance label. Three all-positive effects have one-sided sign p=0.125; their min/max interval is not a95% median CI. Do not drop eligible outliers or unfavorable seeds. A missing/failed arm leaves its paired interaction unavailable; preserve the failure, do not substitute an unregistered seed, and mark incomplete confirmation insufficient. Numeric-invalid readouts are ineligible rather than zero effects. Content-group resampling is evaluation-design sensitivity only. Cyclic-shift dependence and fixed-pool reuse cannot turn individual rows into independent training replications.

**Optional future confirmation candidate, not authorized:** freeze learner, schedule, data, checkpoints, primary aggregate, practical threshold and test direction after exploration. Use six NEW independent seeds101/113/127/139/151/163 and unopened new test, with no favorable-test selection. This adds84 trajectories,60,000 answers,3,000 updates. If test influenced selection, replace it before confirmation. Candidate practical threshold δ=0.01nat/answer is an AI convention for audit, not an established scientific cutoff. A single loss gap of0.01 corresponds to about1% perplexity change; this interaction is about a ratio of perplexity ratios. Numeric resolution is a separate qualification, not practical importance.

Candidate distribution-free sign rule tests the median seed interaction, not its mean. Preset positive alternative: all six I_s>δ, exact one-sided p=1/64=0.015625. Preset two-sided alternative: all six aboveδ or all below−δ, conservative two-sided p=2/64=0.03125. With independent continuous seed effects, [min I_s,max I_s] covers the population median96.875%; report a conservative at-least95% interval with assumptions. Only the combined primary receives a confirmation label; component panels show heterogeneity and cannot rescue a failed primary. Confirming components requires a separately frozen multiplicity/sample-size plan. Candidate α=0.05 applies only to the unique combined primary. Direction/δ/α adoption remain Unknown and must freeze together.

Secondary estimands: B-only comparisons measure adding A with extra budget;800/200 versus500/500 measures allocation at equal answer budget while B exposure changes. They are not alternative primary interactions. Report B exposure, total answers and updates as three coordinates; measured cost supplements answer matching.

## 11. Secondary Local Effects And Optional SAE Analysis

At preselected B-exposure0/40/80 checkpoints, candidate balanced A-only finite probes start from the same restored state and use the E02-qualified parameter scope/precision/step rule. Source batches are independent of evaluation,20 answers covering each word exactly once, paired by list IDs across rule relations. Record A's independent same-rule change, B's actual finite CE change, no-op/repeat noise, and full/half-step sensitivity. E02's80-row engineering panel is not the scientific full-panel evaluation. For scientific reader precision, hold the actual effective ΔW fixed and evaluate it in each readout path; E02 recomputed source gradients per precision, so its contrast changes the update as well as the reader and does not supply this qualification. Do not retrofit a useful operating state by looking for B harm.

**A self-improvement is not a gate for the main trajectory estimand.** Complete, valid trajectories can identify a presentation policy's consequence even if A is not effectively learned. The source guard qualifies only a mechanism statement that an effective A update causes local B harm: require resolved A self-improvement and resolved B finite increase at that state. Source failure limits this interpretation without deleting policy outcomes.

**Optional future SAE method, NOT RUN, not a prerequisite for frequency:** first determine the native effect to explain. For frozen upstream and final projection input a/output h, actual effective ΔW gives exact Δh=ΔW a for both L and LoRA. Loss sensitivity e_h gives Δℓ=e_hᵀΔh+R; finite native loss remains primary. Existing [shared-update Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_10_shared_update_conditional_interference/17_10_shared_update_conditional_interference_anchor.md) already derives this model; new evidence is its behavior in this carrier.

Bind SAE to the exact parent, producer checkpoint, layer, hook and preprocessing. Current matching S7 exact33B embedded SAE reads raw Attention output; it is a separate carrier. Current Qwen E16 SAE reads normalized final MLP input v=N(r_in+h), with r_in the incoming residual, not raw h. Current share Base and E16 official-a5 parent have byte-identical config and safetensors, verified by full SHA256 without model loading; [identity receipt](sources/sae_parent_identity_20261010.json). Recheck identity/access at use; this resolves parent identity but does not qualify the observer on adapted states. No matching Qwen raw-output SAE was verified within inspected registry/source families. No new SAE training is authorized.

For a matching raw-output dictionary, freeze encoder E, decoder D and bias b; encode absolute before/after states z_k=E(h_k), retain u_k=h_k−Dz_k−b. Then

\[
\Delta h=D(z_1-z_0)+(u_1-u_0),\qquad
\Delta\ell=e_h^\top D\Delta z+e_h^\top\Delta u+R.
\]

Do not substitute E(Δh), ignore the residual, or treat nonorthogonal coefficient squares as additive energy. Qualify displacement and loss-weighted error as well as absolute reconstruction; error must be small relative to the component claimed. On independent discovery groups select candidate directions; freeze before held-out intervention. Orthogonalizing chosen decoder columns gives P and a realizable global parameter intervention ΔW_P=PΔW, complement(I−P)ΔW. PΔh is a space projection, not the SAE encoding contribution DΔz(x). Input-dependent SAE differences generally cannot be one global parameter update.

Use full/no-op/restore/replay, removal/retention, matched-rank random and native PCA/SVD controls, actual perturbation norms, unscaled removal plus norm-restored redirection, full/half steps, source usefulness and all rule×novelty panels. Feature-selection from losses is post-hoc discovery, not prospective prediction. For the existing Qwen MLP-input SAE, explain only that branch: t=r_in+h+MLP(v), and first-order effect g_tᵀΔh+g_vᵀΔv; the first is the residual bypass. Do not add the second to total e_hᵀΔh, which already includes the MLP path. Activation patching at v does not remove the bypass or prove a global ΔW intervention.

If residuals carry the target effect or SAE performs no better than controls, retain native conclusions and report reader non-support. Successful local intervention supports a conditional local channel, not an identified basic module/unique expert or long-term architecture benefit. The [derived logic explanation](../../../../research_notes/A17_shared_learning_logic.md) explains these steps; observer choice, thresholds, intervention budget and SAE execution remain researcher decisions.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: fixed pool IDs, exact balanced replay counts, paired B streams, both target roles, native no-op restoration and exact frozen weights. Bad:800 unique A lists, reduced B in fixed-B arms, source tags in prompts, evaluation content in A, arm-specific LR duration, favorable panel/seed selection, failed A guard deleting valid trajectory outcomes. Confusing: positive interaction while both A conditions help, equal totals with unequal B opportunity, saturated accuracy but varying CE, static SAE reconstruction good while update effect lies in residual.

## 13. Scientific Procedure And Stage Contracts

1. Researcher reviews direct-matrix versus LoRA capacity, useful window and qualified readout; one learner is frozen before this study.
2. Generate new A/B pools and both dev/test panels; qualify actual tokenizer/oracle/balance/novelty and register actual files.
3. Freeze quotas, paired balanced orders, both roles, reset state, constant-LR candidate and initial capability checks.
4. If separately authorized, run a bounded E03 engineering Smoke with the changed schedule; qualify counts/freeze/resume/telemetry and test-closed handling. E02 does not automatically qualify E03.
5. If separately authorized after adoption, run42 exploratory dev trajectories. Record all cells and eligible failures; no confirmation label.
6. Review usefulness/uncertainty, then optionally freeze six-new-seed test confirmation as a separate authorized scope.
7. Report fixed-B interaction, allocation and local effects separately. Only after native effects are established consider the optional SAE method; net harm is not a prerequisite for analyzing helpful/modulated effects.

## 14. Algorithm, Outputs, And Resource Candidate

Execution code/config/data/checkpoints remain under `/data/250010109/MoE_Router/experiments/`; exact new release/run paths and IDs assigned only when created. Input IDs include `model_qwen3_0p6b_base`, the associated tokenizer and actual new frequency dataset. Consult asset registry and strict-check current inputs before loading; registry existence is not current access. Adapt qualified E02 single-matrix/freeze/probe/resume components; preserve frozen E01/E02 source receipts and reject legacy routing or unrelated SAE training code. Follow `docs/training_observability_contract.md`, without weakening telemetry or answer normalization.

Required manifests: data/rule/pool IDs, all exact presentation sequences/counts, tokens/splits/hashes, source/config/Protocol freeze, initialization/optimizer/RNG, device topology and submission receipts. Per arm: raw and TensorBoard loss/LR/gradient/throughput, all source and prefix counts, per-record dev loss, capability panels, finite/no-op/precision receipts, actual state saves and resume comparison. Register actually saved weights/adapters with exact parent/producing run after completion; missing saves explicit.

AI resource candidate: one four-H100-reserved node, four independent single-GPU processes, no cross-arm reduction. E03 engineering: seed17, two relations×two target roles, max8 updates/arm,1,800-second whole-payload ceiling. Exploratory42 trajectories: one bounded study job, at most4GPU concurrently, proposed7,200-second payload ceiling, at most8 reserved GPU-hours; stop and preserve partial records on ceiling. Optional84-trajectory confirmation: separate scope with proposed14,400-second payload ceiling, at most16 reserved GPU-hours. These are ceilings, not measured ETAs or authorization. Candidate output root is `/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/`, with separate data/source/config/runs directories; it has not been created by this draft. Re-estimate feasibility using measured E02/E03 startup and throughput before adoption. SAE compute is not included. Never convert a ceiling failure into a scientific negative.

## 15. Decision Branches

Exploration yields complete descriptive evidence only. For an adopted confirmatory rule, support requires all engineering/data/confirmation qualifications and the preselected combined median interaction beyond δ with its frozen sign criterion. A valid interval wholly within[−δ,δ] supports a bounded absence of a practically meaningful median interaction. Failure to achieve significance, an interval crossing a relevant threshold, numerical ineligibility or incomplete trajectories is insufficient for that answer; it is not proof of zero effect. A reliable interval entirely below−δ is non-support for a preset positive hypothesis; under the preset two-sided hypothesis it can support a negative interaction if the frozen rule passes. All component disagreements remain visible.

Net local harm separately requires effective source learning plus a resolved positive actual B finite delta. Budget results answer allocation only. SAE intervention support, reader non-support and reader ineligibility are different outcomes; none promote expert utility. Scientific verdict/closure stays researcher-owned and Unknown until adjudicated.

## 16. What This Cannot Claim

No pure frequency effect with B opportunity and compute both fixed, exact FLOP matching from answer totals, stable interference from one update, acquisition from random initialization, expert necessity, natural-pretraining generality or long-term architecture advantage. A constrained learner's conflict is not proof unrestricted sharing must fail. Three exploratory seeds do not settle seed-population significance; six candidate confirmation seeds still condition on one Base, pool construction and stochastic schedule. SAE labels/orthogonality alone are not functional independence.

## 17. A–G Review And Amendment Ledger

| Block | Candidate ready for audit | State |
|---|---|---|
| A purpose | fixed-B rule×presentation interaction; separate allocation/local mechanism | PROPOSED |
| B data | new balanced disjoint A/B pools; both novelty types; actual-training reference | PROPOSED; generation NOT RUN |
| C task | FIRST/LAST; Qwen tokenizer; answer-only loss; separate/combined novelty | researcher-confirmed core |
| D model | one final full matrix preferred; LoRA sensitivity; original Base reset | PROPOSED; E02 engineering authorized only |
| E optimization |20 targets; constant qualified LR; exact quotas/both roles | PROPOSED |
| F evidence |3-seed exploration; optional6-new-seed median confirmation; δ/direction | PROPOSED; human adoption Unknown |
| G resources | bounded future Smoke/study/confirmation ceilings above | PROPOSED; no E03 execution approval |

The current user authorized an agent to compare L/LoRA by bounded Smoke and requested complete frequency/SAE plans. This authorizes E02 implementation/Smoke and draft writing, not automatic scientific adoption or E03/SAE execution. Cross-block audit preserves the fixed-B/compute tradeoff, warmup confound, source-guard scope, independent-seed unit, aggregate/panel boundary and actual SAE interface. Existing E01 results are unchanged; E02 execution has separate frozen ownership. No fourth experiment or scientific state transition is created.
