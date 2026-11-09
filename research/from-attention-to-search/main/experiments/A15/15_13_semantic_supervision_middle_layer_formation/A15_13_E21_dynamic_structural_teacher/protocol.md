# A15_13_E21 — Dynamic structural teacher (periodic refresh of the router relation teacher)

Status: `EXECUTION_AUTHORIZED_BY_RESEARCHER_2026-09-10` (design frozen at submission
2026-09-10T18:12Z; the researcher's 0911 instruction explicitly authorised the full
run, so this file records the execution contract rather than a pending approval gate).
Owner: researcher. Drafter: DeepSeek (harness: DeepSeek Harness; model: deepseek-flash).

## Approval snapshot (cold-reader readable without opening a link)

- **One uncertainty:** in the first round the structural teacher was frozen at the
  common t0 readout. Nothing yet separates "the representation drifted away from a
  fixed teacher" from "the teacher itself could follow the representation".
- **Treatment / control:** `dynamic_sae_b_u` and `dynamic_gmm_b_u` re-derive the
  teacher from the current `h` at updates {32, 64, 128, 256}; controls are the
  already-trained `sae_b_u` / `gmm_b_u` (same teacher family, frozen at t0) and
  `task_u` (no structural teacher at all).
- **Changed variable:** whether the relation teacher is refreshed. **Held fixed:**
  backbone, open parameters (last attention only, U), task loss, B-type relation
  loss form, balance bias rule, optimizer, learning rates, gradient clipping,
  sample schedule, seeds (17/29/43), 512 updates, 21 checkpoints, and the t0
  starting point.
- **Primary metric:** the pair-relation change of `h`, `R(t,s)`, and the
  within/between structure `W`,`B`,`B/W` under the fixed t0 partition, measured on
  the frozen development panel (1480 records) with the round-1 ruler.
- **Registered analysis rule:** every effect is a **same-seed paired difference**
  against the matching control; every change must be compared with the same-`h`
  re-analysis noise floor, not with zero.
- **Pass / Fail / Insufficient:**
  - *Pass*: the refreshed teacher differs from the previous one by more than the
    same-`h` re-fit noise floor, AND that difference propagates to router
    probability/actual routing, AND `R`/`W`/`B` diverge from the control arm
    consistently across the three seeds.
  - *Fail*: teacher drift is inside the re-fit noise floor, or the router does not
    respond, or the arms are indistinguishable within seed scatter.
  - *Insufficient*: refresh is not reproducible, coverage collapses, or the run
    does not complete; report the exact gap, never re-label it as Pass.
- **Smallest scope:** 2 conditions × 3 seeds × 512 updates, one reserved 4×H100 node.
- **Cannot claim:** semantic category formation, expert utility, or "better
  representation" from any geometry change; a cleaner cluster is not a better model.

## 1. Question and prior evidence

Round 1 (E20 matrix, `audits/task_u-cluster-evolution-20260911/`) established:
`h` relation drift is real but small and front-loaded (21×21 `R`, local 32-update
change decaying ~7–8×); under the fixed t0 partition `W` and `B` both rise with `B`
faster, so the "within-class tightening" prediction failed; and the fixed K=8
discrete readout does not separate training change from re-analysis noise.

This experiment asks: **does a teacher that follows the representation change the
route/representation trajectory, and do SAE and GMM dynamic teachers differ?**

## 2. Design

| Item | Value |
|---|---|
| New conditions | `dynamic_sae_b_u`, `dynamic_gmm_b_u` |
| Reused baselines | `task_u`, `sae_b_u`, `gmm_b_u` (no retraining) |
| Seeds | 17, 29, 43 |
| Updates / checkpoints | 512 / the 21 matrix checkpoints |
| Refresh schedule | t = 0, 32, 64, 128, 256 (frozen before execution) |
| Teacher at t=0 | the existing common-t0 target cache (block 0 = updates 1–32) |
| Teacher after refresh | derived from the current `h`, frozen for the following block |
| Attention | last layer only (U); task gradient only |
| Structural gradient | Router only, per-parameter-group clipping 1.0 |
| SAE | 1024→30000, top-32 ReLU, warm start from the previous refresh |
| GMM | 64-dim PCA + 8-component diagonal GMM, refit from scratch each refresh |

### 2.1 Refresh procedure (identical for both arms)

1. pause the main optimizer;
2. collect the current `h` at answer-prediction positions, **detached**, into a
   fixed-capacity buffer (≤262144 positions) drawn from the batches of the block;
3. update the dictionary (SAE warm start / GMM refit) on that buffer only;
4. rebuild the atom co-activation φ graph and spectral partition into 8 groups;
5. rebuild the teacher distribution `q` (group mass of top-32 positive activations,
   normalised; zero mass = uncovered, never filled with a uniform value);
6. freeze the teacher and resume training.

### 2.2 Gradient red lines (audited numerically)

- `q` is produced under `torch.no_grad()` from a detached `h`: **no teacher path can
  reach the main model**.
- The SAE/GMM optimiser is separate from the main optimiser; refresh does not touch
  main-model parameters (asserted bitwise in the pilot).
- B-type structural loss reaches the Router and nothing else: the loop captures all
  non-router gradients before injecting the structural gradient and asserts byte
  equality afterwards (`train_dynamic.py`, same construction as `fm/training.py`).

## 3. Execution

```bash
bash dynamic/submit_dynamic.sh full      # job pt-v5d6xo42, reserved n6ls.iu.i40.4
bash dynamic/run_dynamic.sh pilot        # refresh pilot, gate for the full run
bash dynamic/run_dynamic.sh full         # 6 trajectories over 4 GPUs + panel extraction
```

Artifacts: `<run>/dynamic/<condition>__seed<seed>/{checkpoints,training.json,refresh_*.json,progress.json}`,
`<run>/dynamic_qualify_receipt.json` (pilot), `<run>/dynamic_representations/…` (panel shards).
All new code lives in `dynamic/` **outside** `fm/`; `source_hashes()` is untouched.

## 4. Audit blocks

| Block | Item | State |
|---|---|---|
| A | Question and prior evidence | CONFIRMED (round-1 evidence) |
| B | Conditions, seeds, budgets | CONFIRMED (frozen matrix contract inherited) |
| C | Refresh schedule | CONFIRMED — pre-registered {0,32,64,128,256} |
| D | Gradient isolation | CONFIRMED by construction; pilot asserts numerically |
| E | Metrics and ruler | CONFIRMED (round-1 definitions reused verbatim) |
| F | Failure and stopping rules | CONFIRMED (§6) |
| G | Deviations and boundaries | RECORDED (§5) |

## 5. Deviations recorded before execution

1. **SAE auxiliary loss.** The original `a15-e16-full-1b-v1` recipe has
   `aux_k=512`, `aux_weight=1/32` over tracked dead features; the saved checkpoint
   does not carry the dead-feature state, so the auxiliary term uses the top-`aux_k`
   of the non-selected pre-activations as a dead-feature approximation. Learning
   rate, weight decay, clipping, warm-up, outlier quantile and top-k are copied
   verbatim.
2. **Fitting corpus.** The refresh fits on the model's own detached `h` from the
   preceding block (fixed capacity) instead of a full-corpus forward pass; this is
   cheaper and keeps the dictionary tied to the current representation. Coverage and
   used-atom counts are reported every refresh.
3. **Grouping fallback.** If the refreshed φ graph has more than 8 connected
   components, the 7 largest components keep their own group and the remainder are
   merged into the 8th; the fallback flag is recorded per refresh.
4. **Resume.** Cross-refresh resume is not supported in round 2; each trajectory
   runs to completion in one process. `recovery.pt` is still written every update.

## 6. Failure and stopping rules

- Pilot failure ⇒ the full run does not start (`REMOTE_STATUS=PILOT_FAILED`).
- Any `failure.json` ⇒ report the exact stage and completed updates; never overwrite.
- If the same-`h` repeated SAE fit differs more than the cross-refresh difference,
  stop and report dictionary instability before interpreting any arm difference.
- A completed run with indistinguishable arms is a **result**, not a failure.

## 7. Reading order (agreed before execution)

Gate 1 tool reliability (task_f invariance, same-`h` re-analysis noise, SAE
reconstruction/coverage, repeated-fit stability) → Gate 2 did the teacher actually
change (vs the same-`h` refit floor) → Gate 3 did it reach the Router (probability,
actual routing, structural loss and gradient) → Gate 4 did `h` evolution change
(round-1 ruler, same-seed paired) → Gate 5 task cost/benefit (dev/test NLL, load,
expert usage). Task metrics are read **last**; structure is never reported as
performance.

## 8. Claim boundary

Inherited verbatim from the researcher: "这批模型适合观察'预训练模型局部微调中的结构变化'。
固定八簇不能证明自然类别何时诞生，也不能替代语义解释。审计末尾采集仍未齐全，尚不能交完整表征结论。"
