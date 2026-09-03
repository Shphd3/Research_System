# Informative-Future-Target Standard-Head Causal-Use Audit Anchor

Status: completed; all guards passed and the preregistered strong behavioral information-content increment failed.


## 1. Problem Definition

Parent problem: [11_03 cross-position standard-head use boundary](../11_03_cross_position_standard_head_use_boundary_anchor.md).

The parent anchor established that useful current-state formation is not sufficient for later standard-head behavior. This subanchor asks whether informative K=2 MTP, relative to a shared-aux condition matched for active heads, CE terms, and nominal loss coefficients, increases the causal control exerted by the `<DECIDE>` source state over the later ordinary next-token head. NTP remains a secondary system baseline.

### Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Decision role | Cannot prove |
|---|---|---|---|---|
| source state | information at `<DECIDE>` that later tokens can attend to | preregistered source-position attention memory $S_o(x)=\{K_{\ell,T},V_{\ell,T}\}_{\ell\in\mathcal L}$ inside model $o$ | intervention target | that every component was learned only by MTP |
| receiver | example whose input continuation and standard-head output are retained | branch-$z$ example $r_z$ | fixes the downstream computation | generalization |
| different-branch donor | a real example supplying a source state with a different branch | $d_{z'}$, $z'\neq z$, patched into $r_z$ within the same model | tests directional counterfactual control | MTP specificity by itself |
| same-branch donor | an independent matched example with the receiver branch | $d_z$ patched into $r_z$ | measures patch-induced nuisance | that every off-manifold effect is removed |
| standard-head causal use | changing only the source channel changes the ordinary head toward the donor answer | counterfactual answer switch after normal processing of `<SHARED>` | stronger than readability or gradient alignment | natural-task benefit |
| controlled switch effect $C_o$ | donor-directed switch rate minus irrelevant switch rate for objective $o$ | defined in Section 4; unit is probability difference | within-model causal-use metric | cross-objective advantage |
| shared-aux | the second head duplicates the standard next-token target | two active full-vocabulary CE heads with averaged loss | controls the presence of an auxiliary head/loss | equal realized gradients |
| information-content increment $\Gamma_{info}$ | informative-MTP controlled effect minus shared-aux controlled effect | $C_{info\text{-}MTP}-C_{shared\text{-}aux}$; unit is probability difference | primary metric | that the patched component is exclusively MTP-created |
| capability match | the two primary-comparison standard heads solve the clean task comparably | preregistered clean-accuracy band and clean-correct receiver set | prevents learning-level confounding | identical algorithms or realized gradients |

**Single decision question:** On the controlled A11 K=2 branch task, does informative MTP, relative to training-structure-matched shared-aux, increase causal use of the `<DECIDE>` source state by the later standard next-token head?

## 2. Physical Priors

1. **Use requires causal dependence.** If the later standard head uses a source-state branch channel, replacing that channel with a real opposite-branch donor while holding the receiver continuation fixed should move the answer toward the donor branch. This prior is falsified if valid donor replacement leaves the standard head unchanged.
2. **Separately trained coordinates are model-local.** Shared architecture does not make NTP and MTP hidden bases interchangeable after training. The intervention must be performed within each model, and only scalar causal effects may be compared across objectives. Cross-model state insertion would falsify the implementation contract, not the mechanism.
3. **Auxiliary training structure is a live rival.** An NTP/MTP-only comparison changes the active-head count, CE-term count, and future-target content together. Shared-aux matches the first two, so $\Gamma_{info}$ isolates the registered content contrast; differences from NTP remain secondary system comparisons.

## 3. Falsifiable Hypotheses

**Primary hypothesis:** informative K=2 MTP strengthens the causal channel from the `<DECIDE>` source state to the later standard head beyond matched auxiliary training structure, so capability-matched models satisfy $\Gamma_{info}>0$ with preregistered seed consistency and a nontrivial effect.

**Strongest rival:** the added active auxiliary head/loss explains the effect, so shared-aux and informative-MTP have equal source-state causal control, $\Gamma_{info}\approx0$, even if both models show positive within-model effects.

**Adverse alternative:** informative future content weakens the usable early channel relative to shared-aux, giving $\Gamma_{info}<0$.

**Pass:** all validity guards pass, and $\Gamma_{info}$ exceeds the Protocol-frozen minimum effect in at least 4/5 confirmation seeds with a confirmation mean at least as large as that threshold.

**Fail:** all guards pass, but the confirmation mean is nonpositive, or the minimum-effect criterion passes in at most 2/5 seeds. Equal positive $C_{info\text{-}MTP}$ and $C_{shared\text{-}aux}$ rejects information-content specificity while supporting the weaker statement that both auxiliary-training conditions use the channel.

**Insufficient:** exactly 3/5 seeds pass; the mean is positive but below the frozen effect threshold; either model fails capability; capability is materially unmatched; same-branch patches are not null; bidirectional switching fails; the source tensor is not fixed; or any completeness, pairing, or confirmation-separation guard fails.

## 4. Mathematical Model

Let $o\in\{NTP,shared\text{-}aux,info\text{-}MTP\}$ index the training condition and $z\in\{1,\ldots,m\}$ the receiver branch, with $m=4$ in the current A11 construction. Let $r_z$ be a clean-correct receiver, $d_z$ an independent matched same-branch donor, and $d_{z'}$ a different-branch donor with $z'\neq z$. All patches are internal to model $o$.

Let

$$
\hat y_o(r_z;S)
$$

be the ordinary next-token head prediction after the receiver processes `<SHARED>` while the `<DECIDE>` source memory is set to $S$. Define

$$
p_o^{diff}
=
\Pr\left[
\hat y_o(r_z;S_o(d_{z'}))=y_{z'}
\mid
\hat y_o(r_z;S_o(r_z))=y_z
\right],
$$

and the same-branch nuisance rate

$$
p_o^{same}
=
\Pr\left[
\hat y_o(r_z;S_o(d_z))\neq y_z
\mid
\hat y_o(r_z;S_o(r_z))=y_z
\right].
$$

The within-model controlled switch effect is

$$
C_o=p_o^{diff}-p_o^{same},
$$

and the primary cross-condition metric is

$$
\Gamma_{info}=C_{info\text{-}MTP}-C_{shared\text{-}aux}.
$$

$C_o$ tests whether the source state controls the ordinary head inside one model. $\Gamma_{info}$ tests whether informative future content strengthens that control beyond matched auxiliary training structure. $\Gamma_{system}=C_{info\text{-}MTP}-C_{NTP}$ is secondary. Donor-versus-receiver logit-margin change is a continuous secondary diagnostic, not a second decision metric.

## 5. Computational Realization

Use the existing A11 K=2 branch layout:

```text
BR_z F00 ... F15 U00 U01 U02 U03 A_SHARED S_z
```

The earlier `BR_z` token supplies the branch variable. `U03` is the decision index $T$ (the abstract `<DECIDE>`), `A_SHARED` is the branch-shared immediate target (the abstract `<SHARED>`), and `S_z` is the informative answer. The local decision suffix is matched across branches; the entire causal prefix is not identical.

Add only a branch-independent nuisance or instance identifier needed to produce independent matched donors within each $Z$. It must not change the answer or expose a shortcut. Do not add sequence distance, compositional depth, natural-language variation, or a K sweep.

Train NTP, shared-aux, and informative-MTP models with the same backbone, two instantiated heads, data stream, optimizer contract, and seeds. Select capability-matched shared-aux/informative-MTP checkpoints using calibration data before evaluating confirmation patches. The decisive patch replaces the real donor `<DECIDE>` attention memory in all preregistered source layers, then processes the receiver `<SHARED>` normally and reads the ordinary head.

Every active prediction head uses ordinary full-vocabulary cross-entropy. NTP activates only the standard one-step head. Shared-aux and informative-MTP activate the same standard head plus a trainable second head predicting $x_{t+1}$ and $x_{t+2}$, respectively, and average the two losses. This matches head count, CE-term count, and nominal coefficients, but not realized gradient norm, direction, target difficulty, or trajectory; those are reported rather than dynamically normalized.

The source-position query $Q_T$ is not patched. A later token reads the source through its own receiver query $Q_{T+1}$, the source key $K_T$, and source value $V_T$. $K_T$ controls whether the source is addressed, and $V_T$ controls the retrieved content. Patching $Q_T$ would instead change how the source position formed its state from earlier context; patching $Q_{T+1}$ would change the receiver's retrieval policy. K-only, V-only, and receiver-Q interventions are therefore parked as post-result decompositions.

Within-model patching is mandatory. MTP states are never inserted into NTP models or vice versa.

## 6. Minimal Falsification Tests

### Decisive test

Measure $\Gamma_{info}$ on held-out receiver/donor pairs after the threshold, capability band, source layers, and patch interface are frozen on calibration data.

### Required guards

1. **Clean capability:** all three conditions pass the standard-head clean task; shared-aux and informative-MTP pass the frozen capability-match rule, and both auxiliary heads learn their registered targets.
2. **Formation guard:** the branch variable is present at the source state; a common held-out readout may diagnose formation but cannot decide use.
3. **Real-donor guard:** every patched state comes from a valid example in the same model.
4. **Same-branch guard:** independent same-$Z$ patching remains below the frozen nuisance threshold.
5. **Bidirectional guard:** each registered branch pair shows the expected effect in both directions.
6. **Pairing guard:** receiver continuation, `<SHARED>`, objective-matched data, and evaluation examples are identical across the objective comparison.
7. **Confirmation guard:** thresholds and layer choices are frozen without reading confirmation informative-MTP-versus-shared-aux effects.

The main falsifier is a valid $\Gamma_{info}\le0$ or control-sized effect. A failed capability or patch-validity guard produces insufficient evidence instead of a mechanism verdict.

## 7. Current Evidence

**Direct result already established:** informative future targets create an earlier current-state signal, and that signal can reach shared parameters under controlled conditions. See the [A11 line registry](../../README.md).

**Observation already established:** local usefulness at $h_T$ was positive in 5/5 seeds for both heads, while usefulness at $h_{T+1}$ was negative in 5/5 for both heads in the existing cross-kernel audit. See [A11_03_01_E01](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E01_head_position_cross_kernel/summary.md).

**Behavioral boundary already established:** bridge-conditioned geometry did not yield stable standard-head behavioral superiority, and the formal end-to-end result was insufficient. See [A11_03_01_E02](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_01_E02_end_to_end_use_boundary/summary.md).

**A11_03_02_E01 direct result:** all five seeds passed the common-capability, cache, self-patch, same-branch, positive-control, and pairing guards. The mean was $\bar\Gamma_{info}=0.01675$, and 0/5 seeds reached `0.10`. Only seed 972 was positive at `0.08374`, concentrated in one branch direction. The frozen strong behavioral information-content hypothesis therefore failed. See the [summary](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md) and [detailed record](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/detailed.md).

**A11_03_02_E02 source-information audit:** same-contract replay reproduced E01. Exact layer-2 `U03` K/V gave held-out branch accuracy and all-class recall `1.0` for every condition and seed, so absolute linear source formation is established. The registered informative-MTP-minus-shared-aux readability increment was negative in 4/5 seeds, with mean `-0.002299` nat/example and 95% CI `[-0.004502,-0.000173]`. The formal verdict is insufficient because the single-shuffle maximum-accuracy guard failed. A secondary Fisher diagnostic was higher under informative-MTP in 5/5 seeds, driven mainly by within-branch nuisance contraction. See the [summary](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md) and [detailed record](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/detailed.md).

## 8. Claim Boundary And Next Decision

Currently supported: MTP can create an earlier direct signal, but formation and local favorable geometry are insufficient to establish later standard-head use.

Now adjudicated: after matching auxiliary training structure and standard-head capability, informative future content did not reliably strengthen strong answer-switching control at this interface. Exact source K/V is branch-readable under all objectives, but the registered audit did not identify an informative-MTP-specific readability increment.

Secondary observations: informative-MTP donor-margin changes exceeded shared-aux in 4/5 seeds, but the mean was dominated by seed 972. Informative-MTP also compacted within-branch nuisance geometry in 5/5 seeds. Both remain candidate mechanisms rather than behavioral-use evidence.

Even a passing result would establish only a controlled causal-use increment for the all-position informative K=2 objective package relative to matched shared-aux at this source-state interface. It would not isolate the `U03` local label from the full objective package, or establish general MTP superiority, a K scaling law, long-range or natural-language value, compositional reasoning, representation disentanglement, or MoE value.

**Exactly one next decision:** validate a `relay-required` carrier with no direct answer bypass and a non-saturated shared-aux baseline before comparing objectives again. K/V/Q/layer and shared-unembedding sweeps remain parked until that carrier passes.
