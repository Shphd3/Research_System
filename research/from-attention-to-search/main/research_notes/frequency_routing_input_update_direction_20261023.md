# Frequency routing: input directions and net parameter changes

[中文](frequency_routing_input_update_direction_20261023_cn.md) · [Owning candidate](frequency_routing_rank_one_20261022_candidate_anchor.md)

This is a completed post hoc diagnostic of saved T_F weights. It adds evidence to the existing AI_PROPOSAL candidate; it is not a new registered Anchor or a training result. No model forward, backward or optimizer step was executed.

## Finding and purpose

Both saved seeds show more gate/up net parameter change along the leading global TRAIN input directions than along the same number of fixed random directions. Across all eight experts, the first 16 input directions account for **15.16% and 15.33%** of squared net change, versus **1.49% and 1.48%** for the random reference. Low-band experts show the same qualitative pattern. This retains an input-direction preference as a concrete candidate, but these 16 directions do not contain most of the net change. The measurement does not establish useful learning, competition or suppression of rare-feature learning.

The researcher proposed that experts receiving full inputs might keep learning common input directions despite frequency-based allocation. The bounded question here is whether that directional alignment is visible in the already saved parameter changes. This question was formulated after the original training, and is not a retrospective preregistered prediction. The scope, matrix types, two seeds, ranks 1/16 and reference bases were fixed before this calculation on 2026-10-23.

## Objects and computation

An expert receives the full hidden vector \(h\), divided by a fixed scalar scale \(s\). Its gate and up matrices both read \(u=h/s\). The down matrix reads their nonlinear product, so its input axis is excluded from this audit.

Let \(V_k\) contain the first \(k\) orthonormal principal directions of centered TRAIN hidden states. These are right singular directions of the centered batch matrix, not singular directions of an individual input or of an expert weight matrix. For each expert and matrix, define the saved endpoint change \(\Delta W=W_{168}-W_0\) and measure

\[
q_k(\Delta W)=\frac{\lVert\Delta W V_k\rVert_F^2}{\lVert\Delta W\rVert_F^2}.
\]

The PCA basis vectors have unit length. Activations were not divided by singular values, and the inputs were not whitened. The ratio normalizes parameter-change magnitude only; it is not a task-effect comparison.

This equals the share of squared matrix norm in the input-axis projection \(\Delta W V_kV_k^\top\). It is not a loss share. The same computation uses the saved random orthonormal basis and initial matrix \(W_0\) as controls. Rank 16 occupies 16/1024 = 1.5625% of input dimensions. A uniformly oriented reference has that expected share; one saved random basis is not a null distribution or a significance test.

The PCA basis was fitted once on the original TRAIN panel of 85,548 targets. No basis was refitted on this result, any expert's selected subset, EVAL or DEV. The first one and 16 directions explain 11.61% and 32.88% of TRAIN input variance. Input variance and parameter-change norm have different denominators; the result does not establish amplification relative to the input distribution.

For each seed, the table pools projection numerators and total squared norms over both matrices and the named experts. It does not treat matrices as independent experimental replications. Every individual expert/matrix row is retained in the CSV.

| Subset and quantity | Seed 11 | Seed 22 |
|---|---:|---:|
| All experts, net change, first PCA direction | 4.345% | 4.384% |
| All experts, net change, one random direction | 0.079% | 0.081% |
| All experts, net change, first 16 PCA directions | 15.163% | 15.326% |
| All experts, net change, 16 random directions | 1.489% | 1.483% |
| Low-band E0/E1, net change, first 16 PCA directions | 14.852% | 14.053% |
| Low-band E0/E1, net change, 16 random directions | 1.484% | 1.516% |
| High-band E6/E7, net change, first 16 PCA directions | 16.120% | 16.660% |
| High-band E6/E7, net change, 16 random directions | 1.485% | 1.482% |
| All experts, initial weights, first 16 PCA directions | 1.561% | 1.565% |
| All experts, initial weights, 16 random directions | 1.553% | 1.565% |

All 32 individual net-change matrices exceed their random reference at both ranks. Their rank-16 PCA shares range from 13.08% to 17.99%. Different experts have different exposure counts, so the low/high rows do not isolate frequency as a cause.

## Why full input does not determine learning direction

For one input matrix, the batch gradient has the form

\[
\nabla_W L=\frac{1}{N}\sum_t \delta_t u_t^\top,
\]

where \(\delta_t\) is the loss derivative with respect to that matrix's output, including the effect of the subsequent computation. Input variation alone does not specify \(\delta_t\); the target, current prediction and model state matter. AdamW then transforms the gradient using its state. Feature activation frequency, input principal directions, weight singular directions and actual optimizer updates are distinct objects.

**Constructed teaching example, not measured evidence:** take the four equally weighted inputs \((\pm10,\pm1)\), target \(y=x_1+x_2\), prediction \(\theta^\top x\) and half squared error. At \(\theta=(1,0)\), input covariance is \(\operatorname{diag}(100,1)\), but the mean gradient is \((0,-1)\). The largest-variance component is already predicted correctly; only the smaller direction needs an update.

The old router also does not estimate loss reduction. It selects frequency bands by normalized activation-contribution scores. Equal scores can hide different combinations, while the full-input expert can still distinguish them internally.

## Why different combinations need not require different experts

**Constructed teaching example:** let inputs be \(x_A=(1,1,0)\) and \(x_B=(1,0,1)\). Their first component is shared; the second and third distinguish the combinations. Use balanced occurrence rates and equal routing contributions. At zero parameters, fitting target \(y_A=1\) with a gradient step of size 0.1 gives \(\theta'=(0.1,0.1,0)\).

- If \(y_B=1\), B's half squared loss falls from 0.5 to 0.405: the A update helps B.
- If \(y_B=-1\), the same update raises B's loss from 0.5 to 0.605: it hurts B locally.

Only the target changes; frequencies and input geometry are unchanged. Combination difference therefore does not imply conflict, and equal frequency does not imply compatibility. Even the second case can ultimately be fitted by one sufficiently expressive expert using the differing coordinates. A local conflict does not prove that separate experts are necessary.

## Boundaries and next discriminating question

This audit uses endpoint displacement, which can cancel earlier updates and includes optimizer and weight-decay effects. Its global basis is not each expert's local input covariance. It does not compare grouping interventions or measure which direction reduced rare-feature loss. The original training results and the untested combination-transfer hypothesis remain unchanged.

**AI proposal:** next distinguish whether the shared-direction change helps rare-feature examples or competes with changes useful to them. A future local functional comparison would start from identical saved model/optimizer states and measure effects on separate samples, with matched perturbation size and a random-direction control. Its exact states, samples, scale, confirmation criteria and run permission are not fixed here. If shared-direction changes help rare and common examples alike, retain useful sharing as the explanation; if a matched reallocation yields reproducibly better rare-example loss without an offsetting loss, consider competition. Sparse support or unstable effects remain insufficient. The current result alone does not select orthogonal training, a new router or separate experts.

The existing combination-transfer question remains a separate alternative: if different same-frequency combinations transfer equally well, that weakens the proposed combination-conflict explanation. To argue that frequency itself is a sufficient grouping rule still requires informative cross-frequency or matched-random comparisons and adequate precision.

## Reproducibility

The two initial/final tensor digests were recomputed with the original producer's byte convention and exactly matched both training receipts. The initial/final normalization scale is unchanged; both endpoints are step 168 with 85,548 valid targets. The script loaded tensors on CPU, checked basis orthonormality, retained all 256 measurement/control rows and algebraically checked the two teaching examples. Peak RSS was about 865 MiB. These checks validate this calculation's identities, not its causal interpretation.

- [Scope fixed before calculation](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/analysis_scope.json)
- [Current input asset access](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/input_access.json)
- [CPU analysis source](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/audit.py)
- [All measurements](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/all_projections.csv)
- [Results, input digests and provenance](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/summary.json)
- [Checked teaching examples](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_rankone_progress/20261023_input_update_direction_audit/teaching_counterexamples.json)
