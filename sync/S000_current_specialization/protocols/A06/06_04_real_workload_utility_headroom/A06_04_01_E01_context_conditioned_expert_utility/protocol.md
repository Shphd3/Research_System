# Protocol: A06_04_01_E01 Context-Conditioned Expert Utility

## 0. Approval Snapshot

**Approval status:** Approved by the user on 2026-07-21 for implementation,
self-check, smoke testing, and four-H100 execution.

**Execution status:** Complete. Four-GPU smoke job `pt-11i6h4tv` and full job
`pt-loe1371e` succeeded. The registered verdict is recorded in `summary.md` and
`detailed.md`.

**Decision question:** holding the in-file prefix and target tokens fixed, does
relevant cross-file evidence create a split-stable change in relative expert
utility at the final MoE block, together with positive loss headroom over the
native Router?

**Experiment role:** a frozen-model mechanism test on a real code workload. It
is not a Router-training experiment and cannot establish faster rare learning,
common-information preservation, or conflict isolation.

**Primary metric:** held-out expert-by-context difference-in-differences
$I_{ctx}^{test}$, in nats per target token, guarded by positive relevant-context
headroom $H_a^{rel,test}$.

**Main falsifier:** the native model benefits from relevant context, but no
split-stable expert pair shows registered held-out interaction and absolute
headroom.

## 1. Operational Definitions

| Term | Concrete definition | Decision role | Cannot prove |
| --- | --- | --- | --- |
| Context-paired example | Identical in-file prefix and target under relevant (`REL`), local-only (`LOCAL`), and token-length-matched irrelevant (`NUIS`) cross-file evidence | Controls target and local-token identity | An unfiltered repository distribution |
| Native routing | The checkpoint's unmodified top-8 routed experts; this checkpoint has no shared expert | Real baseline | Native selection is functionally optimal |
| Matched slot swap | Replace the lowest-weight routed slot by candidate expert $e$, retain that slot's weight, the other seven routed experts, and active expert count | Isolates routed expert identity | A deployable Router |
| Expert headroom | $H_e^c=L_{native}^c-L_e^{swap,c}$ | Measures native-Router loss opportunity | Expert $e$ can be predicted from input |
| Context utility shift | $\delta_e=H_e^{REL}-H_e^{NUIS}$ | Calibrates context-favored experts | Generalization without held-out testing |
| Context-expert interaction | $I_{ctx}=(H_a^{REL}-H_b^{REL})-(H_a^{NUIS}-H_b^{NUIS})$ | Primary functional measure | Semantic meaning of experts |
| Route overlap | $O(c_1,c_2)=\sum_e q(e\mid c_1)q(e\mid c_2)$, averaged over aligned target-predicting positions | Secondary routing sensitivity diagnostic | Whether sharing is helpful or harmful |

## 2. Hypothesis and Rivals

**Primary hypothesis:** relevant cross-file evidence changes which expert
function is useful for the same completion target; the effect is stable across
two calibration halves and leaves positive headroom on repository-disjoint
test data.

Registered rivals are target-token identity, local syntax, prompt length and
absolute position, a generic context benefit shared by all experts, selection
overfitting across 128 experts, activated-compute mismatch, and routing changes
without functional utility changes.

## 3. Data Contract

- Source: CrossCodeEval Git revision
  `40c68d2b7ca2a8eae95d901ac80e6a540a84a53d`.
- Archive blob: `d838b2795a5b314fb7580c652c4df98f4c61d2c9`.
- File: `python/line_completion_rg1_unixcoder_cosine_sim.jsonl`; oracle
  retrieval files are forbidden.
- Fields: `prompt`, `groundtruth`, `metadata.task_id`,
  `metadata.repository`, and `crossfile_context.text`.
- Deterministic sample: 256 examples. Compute
  `SHA256(repository + "|60401") mod 4`: bucket 0 is calibration-A, bucket 1
  calibration-B, and buckets 2/3 test. Sort each pool by
  `SHA256(task_id + "|60401")` and take 64, 64, and 128 examples. A repository
  cannot cross splits, and model loss or routing cannot influence selection.
- Integrity exclusions only: empty target or relevant context; target longer
  than 128 model tokens; no same-split different-repository nuisance donor;
  or inability to satisfy the frozen 4096-token budget. A deficient split is
  `insufficient`, not an invitation to relax rules.

Prompt construction:

1. `REL = relevant_crossfile_context + in_file_prompt`.
2. `LOCAL = in_file_prompt`.
3. `NUIS = different_repository_context + in_file_prompt`, with nuisance
   context truncated to exactly the same tokenizer-token count as the relevant
   cross-file part.
4. Keep at most 128 target, 2304 most recent in-file, and 1536 earliest
   cross-file tokens within a total length of 4096.

## 4. Model and Intervention Contract

- Primary checkpoint: local
  `/data/share/Qwen3-Coder-30B-A3B-Instruct`.
- Offline-only loading is mandatory:
  `local_files_only=True`, `HF_HUB_OFFLINE=1`, and
  `TRANSFORMERS_OFFLINE=1`. Missing files stop execution; network fallback is
  forbidden.
- Local checkpoint fingerprint:
  `config.json` SHA256
  `e2c8d8eea39471785cd93379d8b48241ad7dcda299013155dd02526e34a0de62`,
  `model.safetensors.index.json` SHA256
  `8dde190b862c7c80ec7403c6495de00c60bbaf246ed479cee4506284989c584c`,
  tokenizer SHA256
  `19564a48c4f71a2a1b937cce34c737a1e662b171c5f5d7edf641a15cd896f07d`,
  and indexed tensor bytes `61,064,245,248`.
- BF16, `eval()`, batch size one, no generation and no parameter updates.
- Architecture verified from the local config and module implementation: 48
  decoder layers; every layer is an MoE layer; 128 routed experts; top-8
  normalized routed activation; no shared expert. The preregistered block is
  the last actual `Qwen3MoeSparseMoeBlock`, expected at zero-based layer 47.
  Module-tree discovery, rather than the expected index, is authoritative.
- Intervene only at positions whose logits predict target tokens. For each
  candidate $e\in\{0,\ldots,127\}$, replace the lowest-weight native routed
  expert by $e$ while retaining its weight and without renormalization. If $e$
  is already active, that position is a formal no-op. All other positions and
  layers remain native.
- OOM fallback is permitted only after a recorded batch-one, 4096-token BF16
  smoke on one H100 80GB. The fallback is local `/data/share/gpt-oss-20b`,
  whose actual module tree must verify 32 experts and top-4 before a separate
  protocol branch is executed. Results from the two checkpoints must never be
  pooled.

For example $i$, condition $c$, and target $y_i$:

$$
L_i^c(e)=-\frac{1}{|y_i|}\sum_j\log p_e(y_{i,j}\mid x_i^c,y_{i,<j}).
$$

The implementation may cache the native final-layer MoE input and decoder
output, then exactly replay each candidate expert and the final norm/LM head.
This is operationally equivalent because the intervention is in the final MoE
block after the last token-mixing operation. A literal patched full forward is
the required equivalence oracle in smoke testing.

## 5. Split, Selection, and Statistics

Using calibration data only:

$$
(a,b)=\arg\max_{e\ne e'}(\delta_e-\delta_{e'}),
\qquad H_a^{REL,cal}>0.
$$

Expert $a$ must be in the top eight $\delta_e$ values and $b$ in the bottom
eight in both calibration halves. Freeze $(a,b)$ before opening test metrics.

On test data:

$$
I_{ctx}^{test}
=(H_a^{REL,test}-H_b^{REL,test})
-(H_a^{NUIS,test}-H_b^{NUIS,test}).
$$

Use a paired repository-level bootstrap with seed `60402` and 10,000
replicates. Report point estimate and two-sided 95% percentile interval. Data
ordering seed is `60401`.

## 6. Execution Contract and Self-Checks

Execution workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a06_04_context_utility
```

Resources: one ACP worker with four H100 80GB GPUs, worker spec
`n6ls.iu.i40.4`, workspace `share-space`, AEC2 `share-cluster`, spot quota,
image `registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-private-lite:container1-20260523142552`,
and mount `01995892-d478-76d8-aec7-13fd8284477e:/data`.

Four model replicas shard examples by deterministic sample index and each
evaluates all 128 candidates. This replaces the earlier expert-ID sharding
draft because exact final-layer caching avoids redundant Transformer forwards;
it changes neither prompts, candidates, losses, nor estimands.

Required guards:

1. Weight bytes plus empirical peak allocated memory leave at least 8 GiB free
   on every H100 during smoke.
2. Native cached replay and native model NLL differ by at most
   $2\times10^{-4}$ nats/token.
3. At least four candidate interventions on at least two examples agree with
   literal patched full forwards within $2\times10^{-4}$ nats/token.
4. Formal no-op candidates agree with native NLL within the same tolerance.
5. All `(task_id, condition, expert_id)` rows are finite and complete before
   calibration or test analysis.

Smoke uses eight samples and candidates `[0,32,64,96,127]`. Exact replay
validation uses at least two samples, two context conditions, and four
candidates including native-active no-ops and non-active swaps. Full execution starts
only after every guard available at smoke scale passes.

## 7. Decision Rules

**Pass** requires all of:

1. native context gain
   $G_{ctx}=L_{native}^{NUIS}-L_{native}^{REL}$ has 95% CI lower bound $>0$;
2. calibration identity stability for $a$ and $b$;
3. $I_{ctx}^{test}\ge0.01$ nats/token and CI lower bound $>0$;
4. $H_a^{REL,test}\ge0.01$ nats/token and CI lower bound $>0$;
5. all numerical and completeness guards pass.

**Fail** means the context-capability guard passes but stability, interaction,
or absolute-headroom criteria fail.

**Insufficient** means model context capability, data pairing, numerical
equivalence, complete four-way execution, or infrastructure is unavailable.

## 8. Secondary Diagnostics and Claim Boundary

Secondary diagnostics are native `REL`/`NUIS`/`LOCAL` loss, full-gate route
overlap, top-8 Jaccard, candidate inclusion/no-op rate, hidden-state shift,
128-dimensional utility-vector rank correlation, and a selected-pair gradient
audit on 32 fixed test examples. None may override the primary decision.

Even a pass establishes only context-conditioned final-layer expert utility
and native-Router headroom on this frozen CrossCodeEval Python surface. It does
not establish learned-Router effectiveness, expert semantics, rare/common
training gains, conflict isolation, unfiltered repository generality, other
layers, or million-token context utilization.

## 9. Review Record

- 2026-07-20: AI draft froze paired targets, length-matched nuisance context,
  final-layer matched slot swaps, 256 examples, and held-out thresholds.
- 2026-07-21: user explicitly approved execution and self-check.
- 2026-07-21: implementation refinement changed only the four-GPU partition
  from expert sharding to sample sharding and registered exact cached-vs-full
  forward equivalence checks.
- 2026-07-21: user prohibited new checkpoint downloads and replaced the model
  contract with the local Qwen3-Coder checkpoint above. The local config and
  weight index changed the registered architecture from 64/top-6/layer-26 to
  128/top-8/the last discovered MoE block. GPT-OSS is an OOM-only, separately
  reported fallback.
- 2026-07-21 preflight: the local checkpoint loaded strictly offline on one
  H100. Static allocation was 56.87 GiB. The registered 4096-token BF16 forward
  plus five candidate replays peaked at 57.11 GiB and left 21.32 GiB free, so
  the GPT-OSS fallback was not activated. The loaded module tree exactly
  matched 48 MoE layers, final layer 47, 128 experts, top-8, and no shared
  expert.
- 2026-07-21 implementation audit: two smoke attempts were stopped before any
  scientific scoring because the first replay formula changed BF16 addition
  association from `residual + (moe_output + delta)` to
  `(residual + moe_output) + delta`, producing 0.06--0.115 nats/token mismatch.
  Capturing the exact residual and restoring the model's addition order reduced
  the maximum cached-vs-literal logit and token-NLL error to exactly zero on two
  samples, two conditions, and four candidates; formal no-op error was also
  zero. The corrected two-GPU, eight-sample smoke completed with finite losses.
- 2026-07-21 four-GPU smoke submission: ACP job `pt-mljn674o`, one
  `n6ls.iu.i40.4` worker in `share-cluster`, writing only to
  `runs/smoke_acp4`.
- 2026-07-21 execution closure: the initial spot smoke remained Pending and was
  stopped; the first reserved smoke was stopped while remote PyPI dependency
  installation stalled. An offline wheelhouse removed that infrastructure
  dependency. Reserved smoke `pt-11i6h4tv` and full run `pt-loe1371e` then
  succeeded. The scientific verdict is `failed`: context capability and
  $I_{ctx}$ passed, but calibration identity stability and
  $H_a^{REL}$ failed.
