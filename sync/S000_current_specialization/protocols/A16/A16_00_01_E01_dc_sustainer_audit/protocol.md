---
experiment_id: A16_00_01_E01_dc_sustainer_audit
legacy_experiment_id: A15_00_E04_vanilla_centered_lb_dc_audit
anchor_id: A16_00_01_dc_sustainer_boundary
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-09
design_frozen_at: 2026-08-09-v1
experiment_role: root-cause audit
---

# Protocol: A16_00_01_E01 DC Sustainer Audit

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`.
- **Block audit:** A--G `CONFIRMED`; cross-block consistency `PASS`.
- **Purpose:** determine whether a token-shared Router-input mean immediately causes Vanilla deep-layer hard-route concentration and reduces the local leverage of the common load-balancing (LB) objective.
- **Primary Anchor:** [A16_00_01](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md).
- **Treatment/control:** remove the independent mean from frozen Vanilla; add the saved running center back to frozen Centered; compare with native routing, wrong-layer shifts, and 256 deterministic matched random shifts.
- **Changed variable:** only a constant Router-input/logit component in offline replay.
- **Held fixed:** model parameters, Gate rows, experts, tokens, document order, checkpoint, layer, Router load bias, and numerical analysis path.
- **Primary metric:** aggregate change in busiest-expert share over registered layer-3/layer-4 checkpoint cells.
- **Pass:** both Vanilla mean removal and Centered center add-back are positive with paired-document 95% lower bounds above zero and exceed their matched-random q95.
- **Fail:** neither direction passes; one-direction outcomes are typed `necessary_only` or `sufficient_only`.
- **Insufficient:** any required checkpoint/data/replay/determinism/artifact guard fails.
- **Approved scope:** documentation, implementation, local smoke, full frozen evaluation, analysis, figures, and result records.
- **Cannot claim:** cumulative training causality, LM-quality improvement, optimal LB coefficient, or a universal Router mechanism.

## 1. Terminology / Definitions

- **Pre-center Router source $h$:** the exact `gating_reference` received by each sparse MLP before its optional running-center subtraction.
- **DC/common component:** a vector constant across the fixed statistics tokens; only its expert-relative logit $C_EW\mu$ can affect top-1 choice.
- **Busiest-expert share $M$:** the largest of eight hard top-1 token fractions; unit is fraction, with $0.125$ ideal uniform and $1$ complete single-expert routing.
- **Normalized route entropy $H$:** hard expert-choice entropy divided by $\log 8$; $1$ is uniform and $0$ is single-expert.
- **LB value:** $8\sum_e f_e\bar p_e$ for hard fraction $f_e$ and mean soft probability $\bar p_e$; uniform is $1$, a perfectly aligned one-expert state approaches $8$.  It is a penalty value, not the realized ability to change routes.
- **LB logit-gradient leverage:** RMS of the sample-scaled analytic derivative $8p_{t,j}(f_j-\sum_e f_ep_{t,e})$; it measures local pressure on logits and cannot include LM gradients, AdamW moments, or upstream Jacobians.
- **Random-shift null:** 256 deterministic isotropic input directions, each rescaled so the expert-relative logit offset has the same norm as the true shift for that checkpoint and layer.

## 2. Anchor Alignment

The parent five/six-arm training established that Centered-Full is far better balanced than Vanilla despite the same $\lambda_{LB}=0.01$.  This experiment tests the Anchor's immediate DC-offset clause.  It does not reopen the registered 10B/30B performance comparison and does not modify any ongoing run.

## 3. Tested Hypothesis

The primary hypothesis is bidirectional: the true common component is necessary for the frozen Vanilla collapse and sufficient to damage the frozen Centered Router.  Its predicted signature is a direction-specific, document-stable hard-load change in both interventions, accompanied by a change from high-penalty/low-leverage toward lower-penalty/higher-leverage routing when Vanilla is centered.

## 4. Rival Explanations

1. **Learned-state rival:** Gate rows or representation residuals already encode collapse, so subtracting the mean does not rescue Vanilla.
2. **Generic-shift rival:** any same-size constant shift changes routes; the true center is not special.
3. **Training-path-only rival:** Centered learned different $W$ and representations, so adding the center back does not recreate concentration even if centering was important during training.
4. **Metric rival:** max share changes while route entropy, margins, and dominant-expert identity show no coherent rescue; this yields bounded rather than strong evidence.

## 5. Data Construction And Provenance

The immutable source is
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`, SHA-256 `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`.

- Statistics split: `wos[0:512, :128]`, 65,536 tokens, SHA-256 `6dd7b83df791c75dd62307b4256acc9d399ed2df8df32ef79e68cb0fb16b930f`.
- Validation split: `dclm[0:1024, :1024]`, 1,048,576 tokens, SHA-256 `91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c`.
- The splits have different source corpora and fixed identities.  Statistics tokens fit means only; validation tokens produce all decision metrics.
- The independence unit is one validation document.  Tokens, layers, and checkpoints are not counted as independent replicates.

## 6. Learning Task And Permitted Supervision

There is no training or fitted prediction task.  The only fitted quantity is an unsupervised per-layer mean of frozen statistics activations.  No validation metric, expert label, loss, or route result may change the mean, controls, checkpoints, or verdict rule.

## 7. Model / Architecture And Frozen Variants

Use the existing four-block, hidden-768, eight-sparse-expert, one-shared-expert, top-1 Qwen3 MoE implementation.  Evaluate seed 17 only because the 30B extension and 20B checkpoints are registered single-seed continuations.  The two arms are:

- `vanilla_full`: $z=Wh$;
- `centered_full`: $z=W(h-c)$ with checkpointed running center $c$.

The Gate is linear and bias-free; any nonpersistent `router_load_bias` remains at its deployment replay value.  Experts receive no counterfactual tokens because only Router decisions are evaluated.

## 8. Training Objective And Optimization

No optimization occurs.  For context, both source runs used the identical total objective

$$
L=L_{LM}+0.01L_{LB}
$$

from step 0, with the same AdamW schedule and untruncated top-1 assignments.  This verified fact motivates the audit but is not re-estimated here.

## 9. Conditions, Seeds, And Checkpoints

Registered checkpoints are steps `0, 64, 127, 318, 636, 1272, 12716, 25432`, corresponding approximately to initialization, 50M, 100M, 250M, 500M, 1B, 10B, and 20B tokens.  Step 0 is a known-confusing negative/control view and is excluded from the primary aggregate.  The primary aggregate uses steps `64,127,318,636,1272,12716,25432` and layers 3--4.

Per checkpoint/layer conditions:

| Arm | Condition | Logits | Evidence role |
| --- | --- | --- | --- |
| Vanilla | deployed/raw | $Wh$ | native reference |
| Vanilla | independent-centered | $W(h-\mu_{WOS})$ | H1 treatment |
| Centered | deployed/centered | $W(h-c)$ | native reference |
| Centered | raw add-back | $Wh$ | H2 treatment |
| Both | DC-only | $W\mu_{WOS}$ and, for Centered, $Wc$ | dominant-expert/margin mechanism |
| Both | cyclic wrong-layer shift | matched shift from layer $\ell+1$ with layer 4 wrapping to layer 1 | structured control |
| Both | 256 matched random shifts | deterministic seed `20260809 + 1009*step + 97*layer + arm_offset` | generic-shift null |

Random and wrong-layer vectors are rescaled to match $\|C_EWd_{true}\|_2$; a zero true norm makes the cell invalid rather than silently choosing another scale.

## 10. Primary Metric And Frozen Analysis Plan

For each fixed cell and validation documents, pool hard expert counts and compute $M$.  Define

$$
\Delta_V=M_{Vanilla,raw}-M_{Vanilla,centered},\qquad
\Delta_C=M_{Centered,raw}-M_{Centered,centered}.
$$

Positive values support the DC mechanism.  The primary arm-level estimand is the equal-weight mean of $\Delta$ over the 14 registered layer/checkpoint cells.  For 2,000 paired bootstrap draws, resample the same 1,024 document indices and recompute every cell and the fixed aggregate.  Report percentile 95% intervals.  No layer/checkpoint multiplicity claim is made.

For each of 256 random indices, average its matched-shift effect over the same cells; its q95 is the direction-null threshold.  Decision rules are one-sided because only the registered causal direction supports H1/H2.  Missing cells are not imputed or dropped: any missing primary cell makes that arm direction insufficient.

Typed verdict:

- `pass_bidirectional_dc_support`: both aggregate lower bounds are $>0$ and both point estimates exceed random q95;
- `necessary_only`: only Vanilla passes;
- `sufficient_only`: only Centered passes;
- `fail_no_bidirectional_dc_support`: neither passes;
- `insufficient_*`: a validity guard prevents either registered direction.

The analysis unseals only after all eight checkpoints for both arms have complete native replay and source-mean artifacts.

## 11. Secondary Metrics And Guards

Report per cell/condition:

- normalized hard-route entropy;
- mean and quartiles of top-1 minus top-2 margin in logits;
- route-flip versus deployed condition;
- LB value and analytic LB logit-gradient RMS;
- gradient-descent tendency to reduce the native winner margin;
- DC-only expert and its match to the native dominant expert;
- fraction and median ratio of native winner margin supported by the true DC term;
- independent mean versus checkpoint center norm and cosine in Centered.

These metrics locate mechanism and training stage; none can overturn the primary typed verdict.

Hard guards:

1. exact checkpoint step, payload and source-manifest receipt;
2. frozen data hashes;
3. exact BF16 native winner replay and maximum native logit replay error at the implemented tolerance;
4. FP32 analysis-native winner agreement reported separately;
5. deterministic repeated controls;
6. finite logits/probabilities/metrics and nonzero token counts;
7. complete 32 condition cells including step-0 diagnostics;
8. result tables, raw per-document counts, random-null arrays, and plot sources all reconstructible.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** Vanilla layer 3/4 native routing at 10B/20B should reproduce the already recorded near-single-expert share; Centered should reproduce broad use.
- **Known bad:** native replay with the wrong sign of Centered's center must fail the exact winner replay guard in a unit/integration test.
- **Known confusing:** step 0 has a zero or untrained running center; it is diagnostic only and cannot dilute the primary aggregate.
- **Known confusing:** a random shift may cause large concentration by chance; this is why the true effect must exceed the aggregate random q95 rather than merely be nonzero.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / how | Required output and gate | Artifact / handoff |
| --- | --- | --- | --- | --- |
| S0 | verify immutable objects | checkpoint/data manifest and shapes | all required files, steps, hashes, center buffers | `preflight.json` -> S1 |
| S1 | prove metric code | literal synthetic logits and shifts | failing-then-passing unit tests for counts, LB derivative, random matching, bootstrap | test log -> S2 |
| S2 | prove model replay | 16 statistics rows and 16 validation docs at step 0/127 | exact native winners, deterministic controls, complete schema | `smoke/` -> S3 |
| S3 | extract full evidence | both arms, eight checkpoints, all frozen tokens | one eligible cell artifact per arm/checkpoint | `cells/` -> S4 |
| S4 | registered inference | per-document counts plus 256 null effects | 2,000-draw intervals, typed verdict, source tables | `analysis/` -> S5 |
| S5 | visual/result audit | curated source tables | rendered figures opened and checked; evidence lineage complete | summary/detailed/Anchor |

Any S0--S2 guard failure stops scale-up and is repaired without altering scientific choices.  Any missing S3 cell is Insufficient; it is not excluded.

## 14. Algorithm, Output, And Provenance Contract

Worker code lives under
`/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v2/`.
Raw outputs live under
`/data/250010109/MoE_Router/outputs/online_spectral_router_training/analysis/A15_00_E04_vanilla_centered_lb_dc_audit/`.

This worker path retains the legacy A15 experiment ID because immutable completed raw artifacts were not renamed during the A16 ownership migration.

The worker must provide a config-free CLI with explicit arm, checkpoint, token counts, device, output root, and deterministic seed; an aggregator must refuse incomplete cells.  Research mainline receives only the Protocol, summary, detailed ledger, curated CSV tables, and audited figures.  No checkpoint, raw activations, or unfiltered logs are copied here.

Required outputs:

- data/checkpoint/code manifests;
- per-cell JSON plus compressed per-document count/margin arrays;
- aggregate and cell CSV tables;
- bootstrap and random-null arrays;
- typed verdict JSON;
- plot-contract JSON and figures;
- stdout/stderr smoke/full receipts.

## 15. Success / Failure / Insufficient Evidence

Pass, one-direction outcomes, Fail, and Insufficient are exactly those registered in section 10.  A Pass supports an immediate DC mechanism in these frozen models.  `necessary_only` means the common term sustains Vanilla collapse but Centered training changes $W$/representations enough that add-back is not sufficient.  `sufficient_only` means adding the center can damage Centered but Vanilla collapse is not removed by its independent mean.  Fail redirects to Gate/residual or gradient-feedback mechanisms.

## 16. What This Cannot Claim

Even a Pass cannot establish that DC was the only historical cause, that centering improves all MoEs, that $\lambda_{LB}=0.01$ is intrinsically too small, that a higher coefficient is safe, or that any Router change improves held-out NLL.  The offline counterfactual does not execute experts and cannot measure feedback or specialization.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question/boundary | CONFIRMED | user approved the proposed measurements and requested direct execution |
| B data/provenance | CONFIRMED | immutable A15 statistics/validation artifact and hashes verified |
| C task/supervision | CONFIRMED | frozen unsupervised mean/replay audit |
| D architecture | CONFIRMED | verified four-layer Vanilla/Centered checkpoints and actual Gate input |
| E objective/optimization | CONFIRMED | no new optimization; source LB implementation verified |
| F comparison/evidence | CONFIRMED | user explicitly required Centered comparison and full analysis |
| G execution | CONFIRMED | implementation, smoke, full frozen run, and records explicitly authorized |

Cross-block consistency: `PASS`.  The scientific body is frozen at `2026-08-09-v1` before implementation.  Post-start changes may only be append-only amendments stating before/after, reason, observed-data status, affected blocks, approval, and eligibility impact.

## 18. Append-Only Amendment Ledger

### A1 — complete two pre-registered secondary diagnostics

- **Time:** 2026-08-09, after the registered primary analysis was first unsealed.
- **Before:** section 11 required route flip and DC support for the native winner margin, but the first full extractor persisted neither field. All primary per-document counts and random-null arrays were complete.
- **After:** the extractor additionally reports

  $$
  F_{flip}=\Pr[\arg\max z_{deployed}\ne\arg\max z_{treatment}]
  $$

  and, for deployed winner $w$, runner-up $r$, native margin $m$, and true DC logit offset $d$,

  $$
  q_{DC}=\frac{d_w-d_r}{m+10^{-12}}.
  $$

  It records the fraction with $d_w-d_r>0$, the mean support, and the median $q_{DC}$. For Vanilla, $d=W\mu_{WOS}$; for Centered, $d=Wc$.
- **Reason:** restore conformance with the already approved secondary-metric contract; no hypothesis, treatment, data, checkpoint, primary metric, null, or threshold changed.
- **Observed-data status:** the `necessary_only` primary result had already been observed.
- **Affected blocks:** secondary diagnostics and output schema in G only; A--F and the typed primary verdict are unchanged.
- **Approval:** covered by the user's explicit instruction to complete the approved measurements and refine explanatory metrics after the first result.
- **Eligibility impact:** these fields are post-unseal secondary diagnostics and cannot alter the registered verdict. The unit test failed before implementation and passed afterward; all 16 cells were re-extracted. Primary arrays retained identical SHA-256 values and the point estimates, intervals, random q95 values, and typed verdict reproduced exactly.

### A2 — administrative migration from A15 to A16

- **Time:** 2026-08-09, after the result was complete.
- **Before:** the curated experiment and owning subanchor used IDs `A15_00_E04` and `A15_00_02` because the load failure was discovered inside the spectral-routing training line.
- **After:** the unchanged evidence is owned by `A16_00_01_E01` and subanchor `A16_00_01`; immutable worker outputs retain the legacy A15 path and the curated metadata records both IDs.
- **Reason:** consolidate load-control evidence under the new A16 line without duplicating or rewriting the completed experiment.
- **Observed-data status:** all results were already known.
- **Affected blocks:** administrative identity, links, and ownership only; hypotheses, conditions, metrics, nulls, values, figures, and verdict are unchanged.
- **Approval:** the researcher explicitly approved moving prior load-balance anchors and training evidence into A16.
- **Eligibility impact:** none.
