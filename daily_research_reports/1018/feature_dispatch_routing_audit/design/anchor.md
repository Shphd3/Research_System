# Anchor | From feature groups to actual expert reception

Version: 2026-10-18 v1.0. English companion to the researcher-supplied [Chinese source](anchor_cn.md), which remains unchanged. Recipient: the existing Agent in the 11109 conversation. The current user explicitly authorized this bounded CPU cache diagnostic and its records. This does not authorize a new learning experiment, a GPU allocation, a changed production route, or commit/push.

## 1. Understand the task in one minute

The broader objective is to improve the effective learning capacity of an MoE under a fixed parameter and compute budget. Frequency and feature relationships might guide expert specialization, but a feature is a grouping object whereas an expert receives a complete token representation containing many features. A frequency-homogeneous membership list therefore need not yield frequency-homogeneous expert inputs.

This round asks only: **What division of input reception did the existing groups and router actually implement? When low-frequency targets miss their designated expert, does the evidence primarily implicate scoring, conflicts between grouping and input co-occurrence, or remain unable to distinguish them?** Locate the issue in particular features, positions and score terms before deciding what to change. This round does not directly establish learning benefit or capacity gain.

## 2. Starting evidence and its status

The user supplied the following handoff facts. Job `pt-vv7zkyxf` passed engineering checks but stopped at the predeclared TRAIN reception gate; formal learning did not start.

- A divides raw TRAIN activation probability into eight equal-width intervals. Its 9,615 eligible features have group sizes `9253,183,124,34,7,3,2,9`.
- A's top-1 input counts are `0,0,0,129,201,646,9893,119843`, totaling 130,712.
- The highest-frequency group's expert receives 91.68% of inputs. The designated low-feature union covers 95,544 positions, of which 88,524 reach that expert.
- Both B random groupings preserve A's group sizes and pass the original eight-expert reception gate. This is not evidence of learning benefit.
- A's routes are identical across its two seeds; these are not independent learning replications.
- Formal A/B learning, C/D learning and post-training spectra are `NOT RUN`.

The counts imply that the low-feature union occupies 73.095% of all TRAIN positions and 73.867% of the highest-frequency expert's inputs, an enrichment of approximately 1.01056. This is a union statistic; it does not imply that every individual low-frequency feature lacks enrichment.

These were supplied facts, not a fresh remote-cache verification by the source document's author. The executing Agent must check them against existing files, explain scope differences, and preserve old values rather than overwrite discrepancies.

## 3. Connection to the research discussion

The broader questions are what routing optimizes; how an input containing both common and rare features should be assigned; why correlation with an expert does not guarantee coverage; and how much parameter efficiency ultimately improves.

This round advances only **how a feature grouping becomes an input assignment, and whether identified low-frequency content receives the intended exposure**. It defines comparisons for later learning experiments. It does not solve new knowledge outside the dictionary or dynamic expert expansion. State a judgment, evidence and reason, and then the resulting revision. Do not repeatedly rescue an unsupported outcome or replace the question with elaborate tools.

## 4. Terms and distinct objects

- **Feature:** one coordinate of the fixed CrossCoder; use the cached activation-event definition.
- **Frequency grouping A:** membership lists formed directly from global frequency intervals; not φ relationship groups.
- **φ relationship groups:** candidate groups from binary co-occurrence correlation. φ is neither causal contribution nor decoder-direction collinearity.
- **Designated expert:** the expert ID assigned to a feature's membership list. It does not imply that this expert learned the feature.
- **Actual reception:** routing the full input to one expert, rather than splitting its features among separate experts.
- **Common:** the accompanying high-frequency set predefined from TRAIN. It is not automatically syntax, the first principal component, or already mastered knowledge.
- **Global frequency p:** occurrence proportion over all positions. **Within-expert frequency q:** occurrence proportion among positions sent to an expert.
- **Learning-opportunity proxies:** reception rates and exposure counts, not gradients, task value, or acquired knowledge.

A low-frequency expert may also process common features. Equal loads, equal membership sizes, or common-feature deletion are not the objective.

## 5. Diagnostic judgments and competing explanations

This diagnosis follows inspection of preliminary outcomes; it is not a preregistered test of wholly unseen results.

**J1: Membership has not translated into selective reception.** Inspect per-feature reception by the designated expert, within-expert frequency and enrichment. Distinguish receiving almost everything from selectively receiving particular content.

**J2: Accompanying high-frequency components dominate the current fixed score.** Decompose winner scores and winning margins. Keep the dictionary, lists and denominators fixed, and remove only selected score terms virtually. This identifies a scoring computation path, not natural-input causality or learning harm.

**Rival J3: Some reception requirements conflict with input co-occurrence.** A top-1 router cannot send the same co-occurring input to multiple designated experts. Inspect concrete conflicts. Neither attribute every zero reception to scoring nor generalize a single conflict to all groups.

Retain other explanations: counting scope errors, amplitude scale, coupling between group size and frequency, insufficient samples, and imperfect dictionary reconstruction. Reuse existing engineering checks rather than repeat full training preparation.

## 6. Intended knowledge updates

| Evidence | Permitted update | Next step |
|---|---|---|
| Target inputs exist; a score-only removal improves target reception beyond zero-score ties, with costs to other targets reported | A localizable contribution of scoring is supported; co-occurrence and other causes remain possible | Propose and separately register one new score |
| Cross-group co-occurrence gives an explicit infeasible reception bound | Some requirements conflict with the current groups/top-1 budget | Discuss regrouping or a reception tradeoff |
| A high-frequency expert receives many inputs but individual enrichments approach one | High input volume alone does not establish a content division | Stop assessing dispatch solely by expert load |
| Some features are selectively received | Union statistics conceal differences | Identify features/inputs permitting specialization |
| Samples, text alignment or counterfactuals are insufficient | Explanations remain unresolved | Report the gap without inventing a root cause |

A positive outcome is not promised. A reliable failure diagnosis or feasibility boundary is an update; lack of significance does not imply no effect.

## 7. Stage boundaries and deliverables

1. Check existing assets and core counts, then report immediately.
2. Complete per-feature dispatch statistics and the first three of the four key figures; report the largest understanding update.
3. Complete natural-text cases, score-path and co-occurrence checks; report what is supported and excluded.
4. Deliver a one-page meeting summary, full evidence index and **one priority follow-up**.

Do not automatically train, regroup, add regularization, remove PCA directions, or add experts. A follow-up may be described, but execution requires the user's next decision.

## 8. Operational handoff to the existing Agent

Read this Anchor, its Protocol, applicable AGENTS.md and research guidance. Reuse the records, caches and code in `frequency_interval_moe/20261018T103820Z`. Write the diagnostic into a new analysis subdirectory and preserve old results.

Check definitions, counts, controls and inference boundaries first. Apply the reasoning skill if accessible; otherwise state that it was unavailable and use the Protocol's explicit checklist without claiming skill execution. Continue authorized stages without repeated approvals unless the scientific question or permissions would expand. Report each stage; a missing asset blocks only its dependencies.

Deliver clear Chinese explanations in the order purpose → method → observations → analysis → conclusion → next step. Put only necessary labels inside figures and explanations outside. Trace claims to tables and figures. Distinguish the fixed score's computation, representation interpretation and untested learning mechanisms. Recommend only one priority correction. Do not open a new Work, submit training, start learning experiments, or commit/push.
