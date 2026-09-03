---
anchor_id: 15_06_online_spectral_routing_and_relay
legacy_anchor_id: 15_06_dynamic_online_spectral_routing
parent_line: 15_spectral_representation_and_functional_routing
status: completed_30b_downstream_evaluation_recorded
canonical_language: en
updated: 2026-08-09
---

# A15_06 Online Spectral Routing And Relay


Canonical ownership note: this parent was migrated from the temporary
`A15_00_dynamic_relay_hmt` identifier. Immutable worker jobs and raw artifacts
retain their historical identifiers; the project-local canonical identifier is
now `A15_06`.

## 1. Problem Definition

The decision question is whether online covariance-band routing improves a
matched four-layer DCLM MoE at 10B tokens, and whether a shared block-1
Relay-HMT has covariance-specific value beyond centering, local bands, and an
equal-dimension random Relay.  Head, middle, and tail are nested covariance
rank intervals of 64, 256, and 448 directions.  They are geometric labels,
not semantic hierarchy labels.

The primary metric is held-out next-token negative log-likelihood (NLL) at 10B
tokens, in nat/token; lower is better.  It decides terminal predictive quality
but cannot identify the mechanism by itself.

## 2. Physical Priors

1. A continuously moving representation makes a stale band coordinate a
   changing bottleneck; a deterministic online tracker can reduce this error.
2. A single shallow source gives deeper Routers a shared causal coordinate,
   whereas local coordinates change independently with layer computation.
3. Any stable bottleneck can regularize routing, so covariance identity must be
   compared with a matched random Relay.

These priors are false for this model if Relay-HMT does not reproducibly beat
the matched controls at 10B.

## 3. Falsifiable Hypotheses

- **H1:** Dynamic Local-HMT beats Centered-Full.
- **H2:** Relay-HMT beats Local-HMT because a shared shallow source reduces
  cross-layer search drift.
- **H3, decisive:** Relay-HMT beats Relay-Random, establishing value specific
  to covariance-ranked bands rather than an arbitrary smooth bottleneck.
- **H4:** EMA plus nested-Grassmann backtracking keeps high-confidence refresh
  flips at or below 1% without hard projector replacement.
- **Rival:** Centering or any stable equal-dimension Relay explains the result.

Support for Relay-HMT requires both seeds and paired-document intervals to
favor it over Centered-Full, Local-HMT, and Relay-Random.  Failure is lack of
that reproducible ordering.  Missing or invalid terminal evidence is
insufficient.

## 4. Mathematical Model

For source representation $x_\ell(t)$, the statistics service estimates
$\widehat\Sigma_{\ell,k}$ on fixed disjoint calibration tokens and updates

$$
\overline\Sigma_{\ell,k}
=(1-\rho)\overline\Sigma_{\ell,k-1}
+\rho\widehat\Sigma_{\ell,k},\qquad \rho=0.1.
$$

The target eigenspaces are converted into nested deployed projectors
$P_H=P_{64}$, $P_M=P_{320}-P_{64}$, and $P_T=I-P_{320}$.  Procrustes alignment
and a backtracked Grassmann step update the nested flag without differentiating
through statistics.  The high-confidence set is the top margin quartile on a
fixed guard split.  A candidate is accepted only if high-confidence route
flip is at most 1%, maximum expert share changes by at most 0.01, and

$$
R_{cont}=\mathbb E_{x\in\mathcal H}
\frac{\|C_E(z_{cand}(x)-z_{old}(x))\|_2^2}
{m_{old}(x)^2+\epsilon}\le0.01.
$$

## 5. Computational Realization

Five config-driven arms share a four-layer H768, 8-sparse-plus-1-shared,
top-1 MoE.  Experts always receive full local inputs.  Vanilla-Full uses
uncentered full Gate inputs; Centered-Full uses running-centered full inputs;
Local-HMT uses dynamic local H/M/T in blocks 2/3/4; Relay-HMT uses dynamic
block-1 H/M/T in blocks 2/3/4; Relay-Random uses the same block-1 source and
tracker with a fixed seed-specific Haar mixing.  Block 1 remains trainable and
Relay gradients may reach it; only the source-layer identity is fixed.

Every checkpoint persists model, optimizer, scheduler, RNG, data cursor,
running means, covariance EMA, nested deployed bases, random frame, refresh
counter, and continuity telemetry.  TensorBoard and JSONL expose losses,
loads, route flips, margins, principal angles, gamma, lag, Relay gradients,
throughput, and milestone evaluation status.

## 6. Minimal Falsification Tests

The decisive test is the two-seed paired 10B endpoint ordering.  Required
guards are step-0 identity, paired data hashes, exact resume, nested projector
orthogonality/completeness, statistics/guard split isolation, terminal
per-document NLL, and complete milestone artifacts.  Load concentration,
high flip, or gamma zero are measured scientific outcomes unless they create
NaN, corrupt state, or invalidate reconstruction.

## 7. Current Evidence

Prior A15 evidence establishes finite-time covariance learning-speed bias and
nonzero non-head access.  The matched frozen-band 2B experiment found
Local-HMT worse than native, while block-1 Relay-HMT had a small late endpoint
advantage but worse full-trajectory NLL and lacked a random Relay control.
Those results motivate, but do not establish, online spectral Relay.

The five-arm contract smoke and final-source Relay smoke passed, and all ten
registered jobs completed 10B tokens with zero retries and complete paired
endpoint evidence.  Centered-Full decisively beat Vanilla-Full in both seeds.
Local-HMT had the lowest endpoint point estimate in both seeds, but its paired
advantage over Centered-Full was decisive only in seed 17.  Relay-HMT was
decisively worse than Local-HMT and Centered-Full in both seeds and did not
reproducibly beat Relay-Random.  H2, H3, and the combined Relay-HMT claim are
therefore not supported.

The online updater separately passed H4.  Its deployed HMT flags tracked the
current EMA target much better than never updating, and all registered actual
refreshes had zero high-confidence route flip; direct hard replacement would
have produced large discontinuities.  Smooth tracking therefore works as an
engineering mechanism but did not confer Relay-HMT endpoint utility.

The added two-seed, 10B Local-Random-Matched control is also complete. A fixed
orthogonal rotation removed covariance-rank identity while preserving all
successive target principal-angle motion to numerical precision. Local-HMT
clearly beat this control only in seed 17; seed 29 reversed in point estimate
and crossed zero. The random tracker was not disadvantaged. Fixed H/M/T rank
identity therefore did not obtain a reproducible functional certificate.

The 30B extension exposed a separate Router failure: although all configs and
logs recorded $\lambda_{LB}=0.01$, a later A16 implementation audit showed that
re-entrant checkpointing detached the nested LB auxiliary tensor from backward.
The source trajectories therefore did not receive an effective LB update.
Vanilla deep layers were already near single-expert use by 50M--100M tokens,
while Centered remained broad. The frozen E04 root-cause
audit returned `necessary_only`: subtracting the independently fitted true
mean from Vanilla reduced deep-layer busiest-expert share by 0.68678
[0.68435, 0.68922], above matched-random q95 0.18326; adding the saved center
to a separately trained Centered Router did not exceed its random q95. Thus
the common component immediately sustains current Vanilla collapse, while
learned-path adaptation prevents a bidirectional static-offset explanation.

The seed-17 30B eight-task downstream evaluation is complete. No arm passed the
registered broad-transfer rule over Centered-Full. Local-HMT had the highest
navigation-only macro accuracy and exceeded Centered on ARC-Easy and LAMBADA
with paired intervals above zero, but its covariance identity did not beat the
matched Local-Random control on any task. Relay-HMT had no reliable positive
task versus Local-HMT or Relay-Random and was reliably worse on ARC-Easy. The
downstream reading is therefore task-specific and does not rescue H2 or H3.

Protocol: [A15_06_E01](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/protocol.md)

Identity-control result: [A15_06_E02](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)

30B downstream result: [A15_06_E04](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E04_30b_downstream_evaluation/summary.md)

Migrated load-control result: [A16_00_01_E01](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md)

## 8. Claim Boundary And Next Decision

The completed experiments establish four-layer DCLM, two-seed 10B terminal
effects and a seed-17 30B downstream vector under the registered tracker. They cannot establish universal
H/M/T semantics, universal scale transfer, compositional computation, or
expert specialization as the unique cause of an NLL change. E02 closes the
Local-Random gap and does not support attributing the weak Local-HMT point
estimate to covariance-rank identity.

A15 does not own the next load-control intervention and continues independently
in its own task. [A16_00](../../16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md)
owns only the harmful-interference versus regularization versus ineffective-
control decision; its outcome does not pause or gate A15's next spectral or
Relay experiment.
