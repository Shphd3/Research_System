# From activation profiles to fixed-route expert learning

Researcher-supplied design, 2026-10-19. [Chinese original](anchor_cn.md). The subsequent researcher scoring supplement is part of the approved contract: [supplement](supplement_cn.md). This document records the pre-execution design, not a result or scientific closure.

## 1. Problem Definition

The broader purpose is useful expert specialization under explicit parameter and computation budgets. This round asks whether organizing frozen CrossCoder features by TRAIN frequency and routing relative to ordinary group response improves held-out next-token prediction on inputs containing low-frequency features, without materially harming overall prediction. Low feature frequency is neither rare vocabulary nor demonstrated difficult or unlearned knowledge.

## 2. Physical Priors

In the previous cached distribution study, F sent all inputs to expert7; removing exactly ten frequent features to form T still produced nearly single-expert routing. Tphi changed list co-occurrence organization without changing any actual route. This rejects treating list organization as implemented input separation. It leaves the learning usefulness of actual separation untested.

## 3. Falsifiable Hypotheses

H1: within the same T lists, dividing each original group response by its frozen TRAIN mean improves low-feature reception by its listed expert. Narrower actual frequency gaps require a separate measurement.

H2: the primary T/group-calibrated rule improves feature-macro held-out low-input NLL relative to original T scoring and identically sized fixed random R11/group-calibrated lists, while maintaining overall NLL. A credible rival is that greater expert participation or changed exposure, rather than frequency organization, drives any difference; amplified occasional responses and unhelpful separation are also live.

## 4. Mathematical Model

A frozen 14-layer joint CrossCoder produces one shared gated activation z_i(t). Its block28 decoder contribution is z_i D_28,i, with magnitude c_i=z_i||D_28,i||. Frequency p_i is the TRAIN positive-hit fraction. These are distinct quantities; contribution magnitude is not task benefit. Reconstruction uses the actual TRAIN centered vector-RMS inverse and retains residual error.

Routing retains a_i=z_i w_i with w_i=sum of 14 decoder-vector norms, rather than silently substituting the block28 norm. S0 is the mean a_i over all original group members, including zero inactive terms. S1 divides S0 by the group's frozen TRAIN mean. The authorized extension also compares S2=group mean(a_i/m_i) and S3=group mean(a_i/(p_i m_i)), where m_i is TRAIN conditional positive mean a_i. Each denominator class has a positive-median times1e-6 floor; original zeros contribute zero and are reported. These rules are separate, not composed. Lists, normalization and scoring statistics are frozen before learning.

Eight full bias-free SwiGLU experts form a residual branch after block28 residual-post and before the original frozen final norm/head. The whole original hidden vector reaches the selected expert. The base and dictionary remain frozen. Learned-router references alone train a router. Exact architecture, optimization, loss, seeds, data, practical thresholds and resources belong to the Protocol.

## 5. Computational Realization

First show fixed TRAIN/EVAL text windows with frequency, z and actual block28 contribution separately, then measure routes, target reception, actual within-expert frequency and load. All numerically safe conditions train even if routing is unbalanced.

The original primary comparisons are A=T_S0, B=T_S1, C=R11_S1. B-A changes group-score calibration within T; B-C compares T with one preselected random organization under the same calibration. The extension uses T/R11 times S0-S3. Learned gating with/without coefficient.01 load balancing provides two references. All ten conditions have paired initialization/data order seeds11/22 and identical three-epoch budgets. Gate multiplier1 for fixed rules differs from selected softmax probability for learned references and is explicit.

Then force identical probe inputs through each expert, test replacements and zero branch, and only afterward inspect parameter and response spectra. Geometry alone does not establish function or capacity.

## 6. Minimal Falsification Tests

For each paired seed, primary B must beat both A and C in fixed low-feature macro EVAL NLL by at least.01nat/token while overall NLL worsens by no more than.01. Both seeds and both comparisons must satisfy these predeclared practical boundaries for limited support. No such result can establish mediation by frequency rather than exposure. The independent target scene below does not determine the primary verdict.

Choose the first TRAIN-eligible low feature by fixed support/context rules. Exclude its hit positions from a separate S1/seed11 background model's two-epoch updates. Frozen routing statistics may still see unlabeled target features. From one background checkpoint, adapt eight copies, each updating only a different expert on identical target samples for32steps. Compare absolute target EVAL NLL, before-minus-after gain, and old-input harm under background natural routes. Recommendations use TRAIN only; retrospective safe-expert ranking uses absolute adapted target NLL and is an oracle, not a deployed algorithm. This is not truly unseen knowledge.

## 7. Current Evidence

At execution freeze, the previous cached distribution findings in section2 were observed; this round was NOT RUN. Actual factual outcomes belong to the linked Summary/Detailed and do not retroactively change these hypotheses. The following are predeclared interpretation branches.

No reception improvement weakens this specific calibration implementation. Better reception with no held-out learning improvement rejects reception as sufficient evidence of learning usefulness. Learning improvement over S0 but not calibrated R11 leaves frequency organization's extra value unsupported. Improvement over both, with overall quality preserved, supports only this frozen-representation, finite-budget candidate. A discrepancy between prior target assignment and safe adaptation shows frequency alone did not determine the best choice in this one example. Negative and insufficient results remain visible.

## 8. Claim Boundary And Next Decision

Deliver a one-page Chinese overview, complete factual Summary/Detailed, all conditions and paired outcomes, separate activation/distribution/learning/function figures, saved-state and data provenance, and one evidence-based next decision proposal. Use existing authorized four H100 Reserved resources without expanding reservations. Stop at this bounded round. Scientific acceptance, mechanism closure and any follow-on experiment remain researcher decisions; their state is Unknown until supplied.
