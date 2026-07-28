# A11_03_02_E01 Protocol: Model-Local K/V Causal Use Under a Matched Auxiliary-Training Control

Status: approved on 2026-07-15. Implementation and a four-GPU ACP run are authorized.

Chinese companion: [protocol_cn.md](protocol_cn.md)
Anchor: [11_03_02 informative-future-target standard-head causal-use audit](/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md)

## 1. Decision Contract

Question: relative to a `shared-aux` condition matched for active head count,
cross-entropy term count, nominal loss coefficients, data, optimizer, and
standard-head capability, does informative K=2 MTP strengthen causal use of
the layer-2 `U03` source K/V by the later ordinary next-token head?

The three training conditions are:

- `ntp`: only the ordinary next-token head is active;
- `shared_aux`: a second trainable head duplicates the next-token target;
- `info_mtp`: a second trainable head predicts the second-future token.

NTP is a secondary system baseline. The primary contrast is `info_mtp` versus
`shared_aux`.

The single primary metric is

$$
\Gamma_{info,s}
=
C_{info\text{-}MTP,s}-C_{shared\text{-}aux,s},
$$

where

$$
C_{o,s}=p_{o,s}^{diff}-p_{o,s}^{same}.
$$

$p^{diff}$ is the probability that a different-branch donor K/V patch switches
the ordinary head to the donor answer. $p^{same}$ is the probability that an
independent same-branch donor patch causes an irrelevant answer change. Units
are probability difference.

## 2. Data

Each example has the form

```text
BR_z F_{n,0} ... F_{n,15} U00 U01 U02 U03 A_SHARED S_z
```

- $z\in\{0,1,2,3\}$ and `BR_z` maps one-to-one to `S_z`;
- $n$ is a branch-independent random permutation of 16 neutral filler tokens;
- every nuisance configuration produces all four branches;
- `U00 U01 U02 U03 A_SHARED` is identical across branches and nuisances;
- train, calibration, and confirmation nuisance manifests are disjoint.

Frozen sizes:

| Split | nuisance configurations | sequences |
|---|---:|---:|
| train | 4,096 | 16,384 |
| calibration | 256 | 1,024 |
| confirmation | 1,024 | 4,096 |

Different-branch donors use the same nuisance configuration and enumerate all
12 ordered branch pairs. Same-branch donors use a frozen derangement of the
nuisance IDs.

## 3. Model and Objectives

Use a two-layer decoder-only pre-LN causal Transformer with `d_model=64`, one
attention head, FFN width `256`, trainable token and position embeddings,
dropout `0`, and two instantiated trainable full-vocabulary linear prediction
heads.

Let

$$
L_1=\frac{1}{|\mathcal T_1|}\sum_{t\in\mathcal T_1}
\operatorname{CE}(q_1(h_t),x_{t+1}).
$$

The objectives are

$$
L_{NTP}=L_1,
$$

$$
L_{shared}=\frac12\left[L_1+
\frac{1}{|\mathcal T_2|}\sum_{t\in\mathcal T_2}
\operatorname{CE}(q_2(h_t),x_{t+1})\right],
$$

and

$$
L_{info\text{-}MTP}=\frac12\left[L_1+
\frac{1}{|\mathcal T_2|}\sum_{t\in\mathcal T_2}
\operatorname{CE}(q_2(h_t),x_{t+2})\right].
$$

Averaging matches the nominal coefficients of the two dual-head conditions; it
does not match realized gradient norms, gradient directions, target difficulty,
or trajectories. Component gradient norms and cosine similarities are
diagnostics only and must not be dynamically normalized.

## 4. Optimization and Seeds

- AdamW, learning rate `3e-4`, betas `(0.9, 0.95)`, weight decay `0.01`;
- batch size `128`, global gradient clipping `1.0`;
- at most `15,000` optimizer steps, evaluation every `100` steps;
- seeds `971, 972, 973, 974, 975`;
- shared initialization, manifests, minibatch order, and optimizer convention
  across the three conditions for each seed.

This gives 15 formal training trajectories.

## 5. Capability-Matched Checkpoint

For each seed, select the earliest common step at which:

1. all three ordinary heads have calibration accuracy `1.0` for three
   consecutive evaluations on `A_SHARED -> S_z`;
2. `shared_aux` and `info_mtp` ordinary-head answer-position CE differ by at
   most `0.05`;
3. at `U03`, both active auxiliary heads have accuracy at least `0.95` on
   their own registered targets for three consecutive evaluations;
4. the step is no later than `15,000`.

If no common checkpoint exists for any seed, the experiment is insufficient.
Do not select independent post-hoc checkpoints.

## 6. Causal Intervention

Patch only the layer-2 attention key and value cached at source position `U03`.
All patches are within the same trained model. Never insert an MTP state into
an NTP or shared-aux model.

Keep both queries fixed:

- source $Q_T$ controls how `U03` reads the earlier prefix;
- receiver $Q_{T+1}$ controls how `A_SHARED` retrieves history;
- source $K_T,V_T$ are the memory tested for later causal use.

After patching, process the receiver `A_SHARED` normally and read `S_z` with the
ordinary next-token head.

Required guards:

- full-sequence and incremental-cache logits agree within `1e-6`;
- self-patching reproduces unpatched logits within `1e-6`;
- same-branch nuisance switch rate is at most `0.05` per condition and seed;
- replacing the ordinary-head input with a real donor answer state switches to
  the donor answer at least `0.95` of the time;
- all 12 ordered different-branch pairs are present;
- thresholds, layer, donors, and confirmation split are frozen before reading
  confirmation effects.

## 7. Decision Rule

Pass only if all guards pass, at least 4/5 seeds satisfy
$\Gamma_{info,s}\ge0.10$, the five-seed mean is at least `0.10`, and no stable
ordered branch-pair group reverses direction.

Fail the registered information-content mechanism if all guards pass and the
mean is nonpositive, or at most 2/5 seeds reach `0.10`.

Return insufficient evidence if exactly 3/5 seeds reach the threshold, the
mean lies in `(0, 0.10)`, no common capability checkpoint exists, or any data,
capability, cache, patch, pairing, or confirmation-isolation guard fails.

Stable logit-margin movement without an answer switch is secondary evidence of
weak or redundant causal influence; it cannot upgrade the primary decision.

## 8. Secondary Diagnostics

- $\Gamma_{system}=C_{info\text{-}MTP}-C_{NTP}$;
- donor-versus-receiver answer logit-margin change;
- layer-2 attention weight from `A_SHARED` to `U03`;
- source K/V branch separation;
- clean accuracy, CE, and margins;
- auxiliary-head accuracy and CE;
- component gradient norms and cosine similarities;
- all ordered branch-pair effects.

No K-only, V-only, source-Q, receiver-Q, layer, horizon, or long-range sweep is
authorized in this run.

## 9. Required Outputs

```text
tables/data_guard.csv
tables/capability_match.csv
tables/cache_audit.csv
tables/patch_controls.csv
tables/causal_use_by_seed.csv
tables/causal_use_by_pair.csv
tables/secondary_margin_metrics.csv
tables/gradient_diagnostics.csv
figures/kv_causal_use_main.png
hypothesis_decision.json
run_manifest.json
```

Raw logs and checkpoints remain in the remote experiment workspace.

### Authorized execution record

- ACP job ID: `pt-pz6zjzzn`
- submitted: `2026-07-15T15:58:51Z`
- worker: one `n6ls.iu.i40.4` node, four N6LS-80GB GPUs
- run name: `a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`
- final state: `SUCCEEDED` at `2026-07-15T15:59:58Z`
- frozen decision: `fail`; $\bar\Gamma_{info}=0.01675$, `0/5` seeds at `0.10`
- result directory: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_03_02_e01_model_local_kv_causal_use/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`
- log directory: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_03_02_e01_model_local_kv_causal_use_4gpu_20260715_1605`

## 10. Claim Boundary

A passing result supports only that the all-position informative K=2 objective
package increases strong standard-head causal dependence on this model-local
K/V channel relative to matched shared-aux in this controlled two-layer task.
It does not isolate the local `U03` label from the full objective package, does
not separate horizon from target content, and does not establish natural-task,
long-context, compositional, scaling, disentanglement, or MoE value.
