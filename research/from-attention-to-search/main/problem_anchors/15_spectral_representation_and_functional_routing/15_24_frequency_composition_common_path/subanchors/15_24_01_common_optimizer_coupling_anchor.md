# Anchor A15_24_01: Does common enter the routed experts' learning through global clipping?

## 1. Problem Definition

**Decision question:** with the same frequency-routed model, additional common expert, initialization, sample order and training budget, does excluding common gradients from the routed experts' clipping denominator improve final prediction on low-frequency-feature positions?

The parent [A15_24](../15_24_frequency_composition_common_path_anchor.md) asks whether invoking a high-frequency or additional common path improves low-feature learning. Its completed additional-common extension retained both routed experts. It improved TRAIN fit but did not consistently improve held-out low-feature loss across seeds. Adding common also increased the number of globally clipped updates. This leaves an optimization explanation unresolved before attributing the result to feature organization.

This subanchor tests that one rival explanation. It does not create new feature groups, replace representations, or test semantic separability. The separate A15_25 workstream owns feature-relation construction. Here, existing inputs and routes remain fixed; the intervention changes how a common gradient participates in scaling other parameter gradients.

The researcher authorized autonomous, distinct mechanism analysis and execution without intermediate approval. The local hypothesis, intervention and decision rule are **AI operationalization under that authorization**, not separately researcher-confirmed mechanism judgments. No Focus is created or reset. Supporting evidence would make this optimization rule a relevant explanation to retain; non-support would weaken this rule as a remedy; incomplete execution would leave the question open.

## 2. Physical Priors

1. **Verified implementation relation:** one norm over all trainable parameters determines the global clipping coefficient. Common can therefore change the clipped gradient of a routed expert even when that expert's raw gradient is held fixed.
2. **Mathematical limitation:** AdamW uses first and second moments of clipped gradients. A smaller clipped gradient does not imply a proportionally smaller parameter update. The first-step near-invariance to positive gradient rescaling is a particularly important rival.
3. **AI hypothesis:** variation in this coupling over training may change the routed experts' trajectory enough to affect low-feature prediction. Its sign and size are empirical questions; greater clipping frequency alone is insufficient evidence.

## 3. Falsifiable Hypotheses

**H-C:** removing common's direct contribution to the routed-gradient clipping denominator lowers final DEV low-feature macro negative log-likelihood (NLL) in both paired seeds, with an attributable difference in actual routed AdamW updates.

**Rival:** AdamW largely absorbs the clipping-scale difference, or any resulting trajectory change fails to improve low-feature prediction. Capacity, functional interaction between branches and ordinary generalization remain possible explanations of the original common result. The present comparison holds architecture constant and tests a clipping policy; it does not remove every form of branch interaction.

## 4. Mathematical Model

Let \(g_R\) concatenate all raw gradients of the eight routed experts and, where present, the router. The current T_F condition has no trainable router. Let \(g_C\) concatenate the common expert's gradients. After the complete effective batch, define

\[
q=\min\left(1,\frac{1}{\sqrt{\lVert g_R\rVert^2+\lVert g_C\rVert^2}+10^{-6}}\right),
\qquad
r=\min\left(1,\frac{1}{\lVert g_R\rVert+10^{-6}}\right).
\]

The threshold is one. The \(10^{-6}\) stabilizer belongs to gradient clipping; it is distinct from AdamW's \(10^{-8}\). Under `global`, clipped gradients are \((qg_R,qg_C)\). Under `route_isolated`, they are \((rg_R,qg_C)\). Thus common retains the global coefficient. At the same raw gradients, only the routed gradient changes. Across training trajectories, both raw gradient groups can subsequently change.

For parameter group \(R\), write its complete AdamW state before an update as \(S\). The observable update is \(U(S,\widetilde g_R)\), including the inherited bias corrections, learning rate and weight decay. A paired shadow update compares \(U(S,rg_R)\) with \(U(S,qg_R)\), holding \(S\), parameters and raw gradients fixed. This isolates the immediate optimizer response; endpoint retraining measures the accumulated policy effect.

At the first update with zero moments, the adaptive term is proportional to \(cg/(|cg|+\epsilon)\) coordinatewise. When \(|cg|\) is well above \(\epsilon\), changing a positive scalar \(c\) largely cancels. Later changing clipping factors interact with moment history. Therefore neither clipping frequency nor cumulative path length alone proves loss of learning ability.

## 5. Computational Realization

1. **Audit observed coupling.** Recompute clipping, raw component gradients and actual parameter-update path lengths from the existing eight completed runs. These already observed quantities motivate the hypothesis; they are not prospective predictions. Preserve the baseline/common pairing and model family.
2. **Intervene on the denominator.** Retrain only T_F plus common under `global` and `route_isolated`, with seeds 11/22. Both policies use the same local hardware, original initialization and data order. Architecture, prediction objective, parameter count, optimizer settings and exposure remain equal. Global controls are rerun locally rather than compared only with a historical remote execution.
3. **Separate immediate and accumulated effects.** At five fixed updates, compare shadow updates from identical current raw gradients and optimizer state without altering the real trajectory. Then compare final per-position NLL and the original low-feature macro metric. The [Protocol](../../../../experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/protocol.md) owns exact settings and qualification gates.

The inherited frozen-cache trainer is reused. Its clipping operation and instrumentation are adapted; no base-model, dictionary, grouping or rank-one implementation is introduced.

## 6. Minimal Falsification Tests

Primary quantity: for each seed, final step-168 DEV low-feature macro NLL under `route_isolated` minus `global`. Each supported low feature receives equal weight after averaging its active-position NLLs; shared positions are dependent. Negative in both seeds gives **exploratory support for this policy in this setting**, subject to valid intervention and update measurements. Mixed or nonnegative directions do not support a stable improvement. A missing/invalid pair is insufficient.

Both seeds are the full planned comparison, not a significance test. DEV is already exposed. Overall NLL, low-feature-union NLL, TRAIN/EVAL curves and update differences must be reported; none can rescue a failed primary criterion. Material overall degradation restricts any favorable reading to the low-feature metric. A numerical-only difference near run/replay precision must be reported as such, without practical-benefit language.

The immediate-update diagnostic also supplies a falsifier for the simplistic claim that “40% less clipped gradient means 40% less learning”: compare actual AdamW updates at fixed state. If the denominator policy changes gradients but little of the actual update, that claim fails even if global clipping is frequent.

## 7. Current Evidence

The completed parent extension found T_F low-feature macro changes of +0.002998 and -0.000958 when adding common, and globally clipped updates increased from 25/24 to 161/159 out of 168. These are historical observations, not results of the present intervention. They establish unstable benefit and altered clipping together, without identifying causation. The [completed Summary](../../../../experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/shared_common_expert_20261022/summary.md) retains full denominators, controls and companion analyses.

The completed [historical log audit](/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling/observational/saved_step_analysis.json) found that adding common increased the eight routed experts' cumulative parameter-update path length by 1.916%–2.309% across all four family/seed pairs. First-step clipping coefficients fell 39.760%–43.734%, whereas actual routed update norms fell only 0.032%–0.042%. Logged raw expert gradient norms were exactly equal at that first step; the logs alone do not establish raw-gradient tensor byte identity. These observations reject the simple description that common reduced total routed parameter movement. They neither measure useful progress nor exclude a moment-history effect. The paired intervention that had not run at draft registration has now completed under the frozen Protocol.

The local paired intervention completed four models on 2026-10-22, each with 168 updates and 85,548 valid training targets. On final DEV, the low-feature macro NLL differences, route_isolated minus global, are −0.000332028 and +0.000529222 nat for seeds 11 and 22. The mixed directions fail the prespecified two-seed improvement rule. Low-position-union NLL changes are +0.000137646 and +0.000411952 nat. Of the low-feature roster, 838 features have support and 856 remain NA; the previously exposed DEV panel supplies exploratory evidence.

Across 20 fixed-state shadow comparisons, common updates are elementwise identical while routed updates can change. At step 42 on the seed11 global trajectory, changing the route clipping coefficient from 0.774878 to 1 changes the update vector by 9.979% of the original update norm, while the norm itself increases only 3.009%. This identifies the local clipping-to-AdamW-update effect; full retraining does not establish low-feature benefit. The new and historical global trajectories are not numerically identical after training, so intervention effects compare only the new same-environment policies. See the [round Summary](../../../../experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary.md) and [independent recomputation](../../../../experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/detailed.md).

## 8. Claim Boundary And Next Decision

This question concerns one optimizer coupling in a frozen final-layer T_F adapter with an always-on common branch. It cannot establish why frequency grouping generally fails, prove semantic function from a feature, justify Rank-one extraction, or establish an improvement across ordinary MoE or pretraining.

The sole next decision is whether to retain removal of this clipping-denominator coupling as a useful local explanation and remedy. Completion requires both valid paired endpoints, actual-update diagnostics and a factual supporting/non-supporting/insufficient record. The fixed Protocol is complete. AI suggestion: retain global clipping as the present reference, and do not promote this clipping change as a low-feature remedy. Further work would need to separate the function learned by common from optimizer-history effects. Preserve the original common experiment and the separate feature-relation workstream. Researcher-level mechanism judgment remains Unknown until reviewed.
