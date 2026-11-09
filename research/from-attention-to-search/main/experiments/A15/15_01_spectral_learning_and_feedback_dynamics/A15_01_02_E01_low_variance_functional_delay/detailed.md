# Detailed: A15_01_02_E01_low_variance_functional_delay

Primary anchor: [A15_01_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_02_low_variance_functional_delay_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** distinguish random-like low-variance routing from delayed correct
stability.  
**Hypothesis:** strong version predicts native tail remains random-like;
weak version predicts ordered H/M/T delay.  
**Experiment logic:** encode the same label at matched standardized SNR in all
bands, vary only amplitude, and compare equal-energy plus label-free random
controls.  
**Conclusion:** strong Fail, weak Pass; native T is delayed but all seeds
recover.  
**Evidence:** 32 seeds, 9 conditions, zero random false crossings, and all
hard guards passed.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| accuracy | route is correct | held-out binary prediction equals label | fraction | prevents stable-wrong interpretation | expert utility |
| flip rate | route changed since last check | fraction of held-out predictions changed | fraction/evaluation | measures persistence | correctness |
| functional stability | correct and persistent together | accuracy≥0.90 and flip≤0.02 for 3 checks | event | decision target | semantics |
| \(T_{FS}\) | time to functional stability | first step of the 3-check run | optimizer steps | compares learning delay | wall-clock cost |
| right censoring | did not cross by horizon | no invented event time | event status | honest random control | eventual impossibility |
| restricted mean | average time accumulated up to horizon | censored values capped at 4,000 | steps | compares censored groups | beyond-horizon time |

## 2. Anchor Link And Decision Point

The Anchor separates two claims: tail may remain random-like at a fixed horizon,
or may simply take longer to reach the same correct stable route. Both require
matched SNR and a label-free random control; raw churn cannot decide them.

## 3. Protocol Compliance Audit

- approved conditions match actual conditions: **yes**;
- primary metric exists: **yes**, functional stability time;
- central figure/table exists: **yes**;
- formal seeds recorded: **yes**, 2000--2031;
- known good/bad/confusing cases reviewed: **yes**;
- typed criteria applied: **weak Pass / strong Fail**.

## 4. Setup

**Data:** balanced binary label; independent 8-D H/M/T blocks with common
noise SD 0.5 and amplitude 4:2:1; label-free Gaussian controls.  
**Split:** online train batches and fixed 8,192-example held-out panel.  
**Model:** one independent bias-free binary linear Gate per condition.  
**Initialization:** random direction, norm 1.0; native/equal pairs share it.  
**Loss/optimizer:** BCE, SGD LR 0.001, no momentum/weight decay.  
**Training:** batch 512, 4,000 steps, evaluation every 20 steps.  
**Conditions:** native/equal/random × H/M/T.  
**Changed variable:** input amplitude and presence/absence of label signal.  
**Held fixed:** dimension, standardized SNR for signal arms, optimizer, data
stream, evaluation panel, and initialization direction.  
**Seeds:** formal 2000--2031; local smoke 9200/9201; distributed smoke
9210--9217.

## 5. Metrics And Decision Rules

The primary event is

\[
A(k)\ge0.90\quad\land\quad F(k)\le0.02
\]

for three consecutive evaluations. Strong Pass required at least 24/32 native
T seeds censored and near-random final accuracy while equal T crossed. Weak Pass
required eventual native-T recovery, positive paired H→M and M→T delay, and at
least 50% equalized-T restricted-time reduction.

## 6. Main Results

### Decision evidence

| Metric | Result |
| --- | ---: |
| Native H crossing / restricted mean | 32/32 / 551.9 steps |
| Native M crossing / restricted mean | 32/32 / 911.9 steps |
| Native T crossing / restricted mean | 32/32 / 1,937.5 steps |
| Equal T crossing / restricted mean | 32/32 / 615.0 steps |
| Random T crossing / final accuracy | 0/32 / 0.5011 |
| Equalized T reduction | 68.3% |

H→M delay was +360.0 steps with 95% paired-bootstrap interval
[226.9,481.3]. M→T delay was +1,025.6 steps with interval [801.9,1,255.0].

### Stage-level evidence

- Native H median \(T_{FS}\) was 600 steps; M was 1,080; T was 2,130.
- Every native T crossed by step 2,460, so the registered 12,000-step
  continuation was unnecessary.
- Final native accuracies were H 0.9727, M 0.9670, T 0.9534.
- Random H/M/T final accuracies were 0.4991/0.5000/0.5011 and produced no
  false functional-stability events.

### Confusing case resolved

Random T quickly achieved near-zero flip rate while remaining at chance
accuracy. It is stable in a geometric persistence sense but not functionally
stable. This directly validates the two-part metric.

## 7. Visualization Results

### Low variance delays correct stability

![Low variance delays correct stability](figures/functional_stability.png)

**Purpose:** distinguish slower correction from random routing.  
**Setup:** 32 formal seeds, common optimizer and matched SNR.  
**Metrics:** held-out accuracy and flip rate versus optimizer steps.  
**How to read:** a functional route must cross both dashed thresholds.  
**Expected for strong H1:** native T stays near random while equal T crosses.  
**Observed:** native T rises more slowly but crosses in all seeds; random T has
low flip but chance accuracy.  
**Take-home:** low variance changes convergence time, not eventual target, in
this system.  
**Remaining uncertainty:** real representation drift and expert co-adaptation.  
**Cannot prove:** semantic or loss/FLOP value.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| S0 math/tests | 6/6 tests | passed | — | metric/data bugs |
| S1 local full guards | 2 seeds | passed | — | impossible thresholds |
| S2 distributed smoke | 8/8 ranks | passed | — | orchestration mismatch |
| S3 formal | 32/32 all conditions | passed | — | incomplete evidence |
| equal-energy known good | 32/32 each | passed | — | unreadable label |
| random known bad | 0/32 each | passed | — | permissive stability metric |
| strong random-like claim | native T 32/32 | failed | tail recovered | low variance equals random |
| weak delay claim | ordered delays | passed | — | no variance timing effect |

**Falsified mechanism:** low variance alone does not erase learnable route
information or force random-like asymptotic behavior.  
**Remaining rival:** in a co-evolving deep model, representation drift may
refresh the target faster than tail can catch it.

## 9. Full Experiment Record

- Resource profile: `5090-8-spot`.
- Cluster/spec: `computing-cluster-5090-01g` / `n12lp.nn.i10a.8`.
- Worker nodes/processes: 1 / 8.
- Quota/priority: SPOT / NORMAL.
- Remote smoke job: `pt-fei6fz35`, succeeded.
- Formal job: `pt-15rmvipu`, succeeded from 17:33:51 to 17:37:31 UTC.
- Config SHA256:
  `8f6cd8989fe721740aeb76bd73feebc151001c39554f914e38bb468f76b8c34a`.
- Merged-results SHA256:
  `45113082c0b3099a000933c16feb9d4c51378faed2ce6e45f4b27ade8ff76a03`.

## 10. Interpretation

The variance ratio changes how long a random initial direction dominates the
learned classifier. Head corrects first; middle and tail follow. Because the
label remains equally recoverable after standardization, all signal bands
converge. Equalizing tail amplitude largely removes the delay, identifying raw
variance as the timing cause rather than random-basis equivalence.

## 11. Claim Boundary

Established: variance causes ordered finite-time functional-stability delay in
this matched-SNR linear problem, and tail is not random-like. Not established:
natural-language semantics, layer-to-layer basis drift, expert utility,
nonlinear Gate behavior, or real checkpoint convergence time.

## 12. Next Decision

Use correctness-plus-persistence as the stability axis in a controlled
four-layer layer×band portrait. Completion requires a known layer-specific
latent target; otherwise accuracy cannot be defined and churn remains
ambiguous.

## 13. Links And Artifact Map

- anchor: [A15_01_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_02_low_variance_functional_delay_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- historical code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability` (not present in the current checkout)
- runner: `run_full.sh: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/scripts/run_full.sh`
- config: `full.json: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/configs/full.json`
- key code: `stability.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/a15_suite/stability.py`, `analyze.py: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/a15_suite/analyze.py`
- result dir: `formal run: /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_05_feedback_stability/runs/a15-0405-5090x8-formal-20260731T173400Z`
- table: [seed summary](tables/stability_seed_summary.csv), [typed verdict](tables/stability_verdict.json)
- figure: [functional stability](figures/functional_stability.png)
- job id: `pt-15rmvipu`
