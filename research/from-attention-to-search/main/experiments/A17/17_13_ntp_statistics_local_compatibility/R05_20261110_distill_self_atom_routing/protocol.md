# R05 Distillation and self-atom routing protocol

AI analysis; researcher judgment Unknown. This is an English rendering of the researcher-authorized design. The exact original Chinese prompt was frozen before training, SHA256 `b577ed19ce503fdaa0415e54891faf3f958f470ab7278a77f20a8b9ae76adb30`; its equations and decision thresholds take precedence. See [Chinese protocol and operational additions](protocol_cn.md). R03, R04 and the preceding A5 gain checks remain read-only; no commit or push.

## Question and competing explanations

A5 fixed teacher-atom routing outperformed native A0 at update2000. A8 tests whether distillation into the native router transfers that gain without a teacher at inference. A9/A9d test whether the student's own frozen atom groups can support useful routing. Their fixed-weight switch snapshots distinguish immediate disruption from subsequent recovery. Credible rivals include unavailable information in student representations, insufficient router readout, score scale and bias interference, changed gate weights, early-layer dictionary quality and representation drift. Concentration alone is a geometric readout, not a training benefit or proof of specialization.

## Shared training contract

Use the original R04 implementation and A0 configuration: eight layers, hidden1024,16 attention heads/eight KV heads, eight experts, Top2, expert intermediate1536, vocabulary151936, tied embeddings and507,988,992 parameters. Seed17 and `checkpoint_moe_baseline_dense_aligned_initial_20261030`; unchanged ordered `dclm_pair_v1`, sequence length2048,262144 eligible tokens/update, four ranks × microbatch16 × accumulation2. AdamW: learning rate0.0003, betas0.9/0.95, epsilon1e-8, weight decay0.1,1000-update warmup followed by constant learning rate, gradient clip1. Use bf16, disable TF32, and retain the original sign-based load-bias update with step0.001 and no auxiliary load loss. Every250 updates evaluate the frozen2097152 EVAL positions and save same-forward fp16 losses/uint8 hard Top2 alongside FP32-state aggregate results.

## Interventions

For layer $l$, let $x_t^{(l)}$ be the MoE input (block norm2 output), $W_r^{(l)}$ its native router, $b^{(l)}$ its load bias and $P_t^{(l)}=\operatorname{softmax}(W_r^{(l)}x_t^{(l)})$. Native selection is $\operatorname{Top2}(P+b)$, with the selected probabilities renormalized as gates. Let $s^{A5}_{t,e}=\sum_{j\in G_e}w_jz_{t,j}$ denote the unchanged frozen teacher TopK32 atom-group score. The operator $\operatorname{sg}$ stops input gradients.

**A8:** fresh shared initialization,2000 updates. Reuse `native_distill`, changing the target from A1 token-cluster scores to A5 atom-group scores. Selection and gates stay native; teacher scores never select experts. Set $q_t=\operatorname{softmax}(s_t^{A5}/\tau)$ and minimize CE plus0.1 times the eight-layer mean of $\mathrm{KL}(q_t\Vert\operatorname{softmax}(W_r^{(l)}\operatorname{sg}(x_t^{(l)})))$. The KL gradient updates only routers. Calibrate and freeze $\tau$ on DEV so the mean maximum target probability is0.6; the realized value is12.19546175. Training teacher encoding stays online bf16; evaluation and inference use the student only. Log layerwise KL, target agreement, entropy, loads, biases and CE/auxiliary router-gradient norm ratios every50 updates.

**A9:** fork the complete A0 update1000 state; run1000 additional updates. For each layer, fit an8192-atom TopK32 dictionary to its own norm2 activations, using frozen DEV centering vector/scalar RMS, ReLU encoder, unit-norm decoder columns, Adam0.0003, batch4096,10000 updates and seed20261110. Reuse the existing update1000 L4/L7 dictionaries after SHA verification. Reuse exactly the previous coactivation spectral grouping, minimum atom count20, eight groups, seed2026110902, group-mass adjustment and inverse-log-frequency weights capped at3. Align each layer's group identities to native experts by DEV Hungarian matching. Freeze all packages before self-routing training and preregister reconstruction/dead-atom rates, group sizes/masses, retained slots, teacher-coordinate concentration and SHA256.

At runtime each selected layer encodes its own detached current input in bf16, computes its own frozen group scores, selects Top2(score+bias), and assigns gates0.5/0.5. Exclude that layer's native router from AdamW and clear its load bias at the switch. Preserve all other weights, moments, learning-rate schedule, four-rank RNG, data cursor and token count. Dictionaries receive no gradient. Evaluation and inference use the student and its dictionaries without a teacher. **A9d** makes the same intervention only in layers4–7; layers0–3 retain native routers, biases and optimizer state.

## Execution and gates

One share-cluster four-H100 Reserved allocation runs A8 smoke → A8 → A9 smoke → A9 → A9d. MIG prepares dictionaries and hint supplements. Before submission, require available storage at least1.5 times the estimated single-arm footprint. Keep the last two full recovery states plus the update2000 endpoint and bf16 weight snapshots every250 updates. Validate a new state before deleting superseded recovery states, with deletion receipts. Delete only this task's smoke payloads after durable smoke summaries. Automatic resume waits30 seconds and permits three retries; resubmission after allocation failure is authorized. Inspect job state, actual updates/loss/throughput/log tail/storage every20 minutes. Budget:32 H100 GPU-hours. No new resource pool or duplicate live main job.

- A8 lambda0: first50 CE values must match A0 exactly or within the original resume tolerance (absolute/relative1e-6). The20-update smoke must have finite loss, correct teacher/input identity, TensorBoard and full EVAL. Actually SIGKILL after a complete update10 state, resume to20 and compare uninterrupted loss, model, optimizer, scheduler, cursor and RNG.
- G1: native continuation from the full A0 update1000 state must match original updates1001–1020 within the same tolerance. If unavailable or failing, the explicitly authorized fallback reproduces a common A0 prefix0→1000 within this allocation and verifies all its CE values before branching.
- G2: runtime and offline bias-zero Top2 on the same sampled DEV inputs must agree on at least99.9% of positions. Realized minimum:0.999755859375.
- G3: perform the same actual update10 kill/resume equivalence test for self-routing. Both A9 and A9d must pass20-update finite-loss and EVAL smoke tests before formal self-routing training.
- Nonfinite loss stops an arm immediately. A8 stops if its loss exceeds twice its initial value. After update1100, A9/A9d stop if trailing50 training CE exceeds6.0; record the stop and advance to the next arm. A failed fork gate stops the dependent experiment.
- Before any optimizer update, save each self arm's switched update1000 full EVAL snapshot with new routing and reset bias. Its main weights equal the native branch source.

## Hint supplement

Keep the previous fixed residual probe and hyperparameters. For the frozen A0 update2000 host, hash the next-token vocabulary into28 buckets with seed20261110 and test full and0.1-probability diluted answer-bucket labels, each against shuffled labels. If diluted real-versus-shuffled gain is below0.02nat, rerun A5/A1/A2 and both controls for exactly four epochs and report both runs. For the frozen A0 update500 host, test A5/A1/A2 identically; A5 gain at least0.05nat means detectable early free information, at most0.01 means not detected, otherwise intermediate. No main-model weights update.

## Analysis and fixed decisions

Use2000 paired document-block bootstrap resamples for uncertainty, separately overall and in ten frozen frequency bands. These intervals do not estimate seed variance. After each arm ends, deliver a quick report within30 minutes with actual endpoint NLL, difference/interval versus A0, concentration median and maximum load/mean.

Report learning curves, A8 inheritance fraction, step lead on trailing50 CE and EVAL, layerwise hard concentration in teacher coordinates with both DEV and EVAL frequency denominators, target agreement versus the previous linear probes, loads/bias/combination entropy/route flips, dictionary reconstruction drift, and the unchanged R04 atom learning/forgetting ledger ($n_i\ge50$, BH $q<0.05$, $|\delta_i|\ge0.01$ nat). Analyze A8 learning time and frequency/concentration correlations. For the self-arm switch, report paired loss changes, atom loss increment $\delta_i^{swap}$ versus changed-layer route-change fraction $\chi_i^{swap}$, quartiles, recovery time on the250-update grid and final effects. A9−A9d is the joint addition of early-layer interventions given late-layer changes; it is not an additive decomposition. Optional atom time rescaling follows the original prompt exactly, with right censoring reported.

|Prediction|Support|Weaken|
|---|---|---|
|P5: A8 routing moves toward concentration|Update2000 hard concentration median ≥1.10|Median ≤1.01|
|P6: A8 transfers part of A5's gain|A8−A0 95% interval entirely below0; also report inherited fraction|Interval crosses0 or is entirely above0|
|P7: self routing beats native routing|A9−A0 or A9d−A0 interval entirely below0|Interval entirely above0 and final250-update NLL decrease ≤0.0817|
|P8: forced route changes cause immediate loss|Spearman($\delta^{swap},\chi^{swap}$) ≥0.2 and highest-quartile median loss increment exceeds lowest-quartile median|Absolute correlation <0.05|
|P9: early-layer self grouping is weak|A9d endpoint NLL below A9 with a nonzero paired interval|A9 no worse than A9d|

P7 supplementary rule: if the difference interval is wholly positive but final250-update improvement exceeds0.0817, classify as insufficient evidence (recovery unfinished), not weakening. Other intermediate cases remain insufficient. Single seed; self arms have only1000 additional updates; A8 needs the teacher in training; dictionaries remain frozen; teacher-coordinate concentration is only an external readout for self arms.

## Actual data-availability deviation

The old A0 position arrays/weights were not retained at1250/1750 and old A4 arrays/weights were not retained at1500. Therefore those requested document-paired intervals cannot be computed; preserve aggregate NLL curves and mark the intervals incomplete. Do not interpolate uncertainty, retrain old arms or change old outputs. Endpoint comparisons and fixed P5–P9 rules are unaffected. Detailed dictionary preregistration and implementation deviations are recorded in the Chinese protocol and execution-side evidence.


Actual numerical convention: evaluation reuses the R04 A5/A6 code with FP32-state parameters, bf16 CUDA autocast and float32 per-position CE before fp16 storage. It is not an autocast-disabled all-FP32-operator forward. This operational distinction preserves the original comparison path and does not change frozen decision thresholds.
