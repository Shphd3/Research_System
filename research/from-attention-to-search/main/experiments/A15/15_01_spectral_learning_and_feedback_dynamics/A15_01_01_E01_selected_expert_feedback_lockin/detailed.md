# Detailed: A15_01_01_E01_selected_expert_feedback_lockin

Primary anchor: [A15_01_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_01_selected_expert_feedback_lockin_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** isolate selected-expert feedback from pure covariance-induced slow
learning.  
**Hypothesis:** early head routing trains incumbents and starves the correct
M/T challengers.  
**Experiment logic:** make H/M/T utility true by construction and change only
which expert receives the single update per token.  
**Conclusion:** Pass; oracle coverage increased median fine correction by
0.477 absolute accuracy.  
**Evidence:** 32 paired formal seeds, 32/32 mechanism directions, all guards
passed, and a successful 8×5090 job.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| head-first partition | early route uses only coarse bit | initialized Gate separates \(h\) and favors one expert per half | route accuracy | creates the lock-in opportunity | natural LLM behavior |
| fine correction | M/T refine a correct head route | average M/T bit accuracy conditional on correct head | \(C_{MT}\in[0,1]\) | primary decision outcome | LM utility |
| oracle coverage | correct functional expert gets training | update recipient \(e^*(h,m,t)\) | one update/token | removes challenger starvation | deployable algorithm |
| challenger starvation | correct fine expert rarely learns | correct challenger update share on non-incumbent examples | fraction; threshold 0.25 | mechanism evidence | sole cause of all lock-in |
| utility gap | incumbent versus correct expert current loss | incumbent MSE minus correct MSE | MSE/example | negative value reinforces incumbent | causal mediation by itself |

## 2. Anchor Link And Decision Point

The Anchor asks whether selected-only expert updates are sufficient to prevent
M/T correction beyond variance-only delay. A Pass requires a paired coverage
effect and the registered starvation/utility mechanism direction. The result
does not inherit A15_05's unresolved DCLM M/T utility claim.

## 3. Protocol Compliance Audit

- approved conditions match actual conditions: **yes**;
- primary metric exists: **yes**, final paired \(\Delta C_{MT}\);
- central figures/tables exist: **yes**;
- seeds/checkpoints recorded: **yes**, seeds 1000--1031, no checkpoints reused;
- known good/bad/confusing cases reviewed: **yes**;
- success/failure/insufficient criteria applied: **Pass**.

Pre-formal amendment: the original supervised guard 0.95 exceeded the analytic
exact-route ceiling \(\Phi(2)^3\approx0.933\). Before formal seeds and before any
primary contrast was inspected, the guard became at least 0.90 and within 0.02
of the ceiling. Data and decision thresholds did not change.

## 4. Setup

**Research question:** does expert update coverage change M/T correction when
Router optimization is otherwise identical?  
**Data construction:** independent balanced H/M/T bits, 8-D block per bit,
amplitude ratio 4:2:1, common noise SD 0.5, 8-D Gaussian payload, and eight
fixed orthogonal target maps.  
**Train/eval split:** online train batches; 16,384 fixed held-out examples per
seed.  
**Model:** linear stochastic eight-way Gate and eight trainable 8×8 linear
experts.  
**Loss:** selected-expert MSE supplies Router policy feedback; MSE trains the
single update recipient.  
**Optimizer:** Adam Gate LR 0.003, SGD expert LR 0.01, entropy 0.01.  
**Training:** 6,000 steps, batch 512, evaluation every 100 steps.  
**Seeds:** formal 1000--1031; operationalization 9000/9001; remote smoke
9100--9107.  
**Changed variable:** expert update recipient.  
**Held fixed:** inputs, data, initialization, route uniforms, Router feedback,
forward count, update count, optimizers, and horizon.  
**Known limitation:** oracle coverage uses the synthetic truth and is not a
deployment proposal.

## 5. Metrics And Decision Rules

Primary effect:

\[
\Delta C_{MT}=C_{MT}^{coverage}-C_{MT}^{selected}.
\]

Pass required the paired-bootstrap lower bound above zero, median effect at
least 0.10, positive M and T component effects, and at least 24/32 seeds with
negative early utility gap and challenger update share below 0.25. All
known-good and compute guards also had to pass.

## 6. Main Results

### Decision evidence

| Metric | Result |
| --- | ---: |
| selected-only median \(C_{MT}\) | 0.4995 |
| oracle-coverage median \(C_{MT}\) | 0.9769 |
| median \(\Delta C_{MT}\) | 0.4774 |
| paired-bootstrap 95% interval | [0.4759, 0.4792] |
| median M component effect | 0.4779 |
| median T component effect | 0.4766 |
| mechanism direction | 32/32 seeds |

### Stage-level profiling evidence

- At step 0, head routing passed in 32/32 seeds and M/T were near 0.5.
- By the early mechanism checkpoint, correct challengers received a median
  0.0399 share of eligible updates.
- Incumbent-minus-correct MSE was median -0.1951, so sampled feedback favored
  the already trained incumbent.
- At step 6,000, selected-only exact routing remained 0.244 median, while
  coverage reached 0.9327, the noise-limited exact ceiling.

### Debug-only evidence

The first operationalization guard used an impossible 0.95 supervised target;
no formal seeds ran under it. The correction was ceiling-derived and not
informed by primary results.

## 7. Visualization Results

### Functional coverage restores lower-variance correction

![Functional coverage restores lower-variance correction](figures/feedback_correction.png)

**Purpose:** visualize the primary paired coverage effect.  
**Setup:** 32 formal paired seeds, identical training except update recipient.  
**Metric/unit:** \(C_{MT}\) accuracy and paired absolute difference.  
**How to read:** left compares training paths; right compares final paired
effects against zero and 0.10.  
**Expected if supported:** selected-only stalls and coverage rises.  
**Observed:** 0.500 versus 0.977 with every seed above 0.10.  
**Take-home:** expert co-adaptation is sufficient for lock-in in this system.  
**Remaining uncertainty:** real-model M/T utility and observability.  
**Cannot prove:** DCLM loss/FLOP improvement.

### Incumbent advantage and challenger starvation

![Incumbent advantage and challenger starvation](figures/feedback_mechanism.png)

All seeds lie left of the 0.25 update-share reference and below zero utility
gap. This supports the registered mechanism direction but does not quantify a
formal mediation proportion.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| S0 math/tests | 6/6 tests | passed | — | label/metric/update bugs |
| S1 operationalization | 2/2 controls near ceiling | passed after amendment | impossible original guard | unreadable M/T |
| S2 distributed smoke | 8/8 ranks complete | passed | — | orchestration mismatch |
| S3 formal run | 32/32 seeds | passed | — | incomplete evidence |
| compute audit | 32/32 exact match | passed | — | extra active expert compute |
| mechanism gate | 32/32 direction | passed | — | variance-only explanation |

**Falsified rival:** pure variance delay is insufficient, because identical
variance with changed expert coverage produced a 0.477 effect.  
**Remaining rivals:** oracle coverage may overstate what sparse exploration can
achieve; deeper representations and nonstationary experts may alter the loop.

## 9. Full Experiment Record

- Resource profile: `5090-8-spot`.
- ACP cluster/spec: `computing-cluster-5090-01g` / `n12lp.nn.i10a.8`.
- Worker nodes/processes: 1 / 8.
- Quota/priority: SPOT / NORMAL.
- Remote smoke job: `pt-fei6fz35`, succeeded.
- Formal job: `pt-15rmvipu`, succeeded from 17:33:51 to 17:37:31 UTC.
- Formal config SHA256:
  `8f6cd8989fe721740aeb76bd73feebc151001c39554f914e38bb468f76b8c34a`.
- Selected-config SHA256:
  `cea798cda310389872597d90076f0f93724199b715cff5a45fd4cdca824e9cd6`.
- Merged-results SHA256:
  `45113082c0b3099a000933c16feb9d4c51378faed2ce6e45f4b27ade8ff76a03`.

## 10. Interpretation

Variance gives head an early timing advantage. The new result adds a second
stage: that early decision changes which experts become useful. Because Router
feedback observes selected losses, the trained incumbent becomes the locally
better action and correct challengers receive too little training to expose
the M/T correction. Oracle coverage breaks this loop without changing Router
inputs or update count.

## 11. Claim Boundary

Established: selected-expert co-adaptation is sufficient for head-first lock-in
under this controlled eight-expert linear task. Not established: natural M/T
utility, real checkpoint causality, semantic specialization, deployable oracle
coverage, or held-out language-model loss/FLOP gains.

## 12. Next Decision

Test whether sparse challenger/counterfactual coverage breaks the same loop in
a four-layer controlled hierarchy where each layer's latent variable is known.
Completion requires matched compute, layerwise functional targets, and final
held-out loss rather than route recovery alone.

## 13. Links And Artifact Map

- anchor: [A15_01_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_01_selected_expert_feedback_lockin_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- historical code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability` (not present in the current checkout)
- runner: `run_full.sh: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/scripts/run_full.sh`
- config: `full.json: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/configs/full.json`
- key code: `feedback.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/a15_suite/feedback.py`, `analyze.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/a15_suite/analyze.py`
- result dir: `formal run: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/runs/a15-0405-5090x8-formal-20260731T173400Z`
- tables: [seed summary](tables/feedback_seed_summary.csv), [typed verdict](tables/feedback_verdict.json)
- figures: [primary](figures/feedback_correction.png), [mechanism](figures/feedback_mechanism.png)
- job id: `pt-15rmvipu`
