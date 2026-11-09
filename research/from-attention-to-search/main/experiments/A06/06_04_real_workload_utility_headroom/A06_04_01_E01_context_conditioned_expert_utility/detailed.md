# A06_04_01_E01 Detailed Evidence Ledger

## 1. Conclusion and Claim Boundary

The registered joint hypothesis failed. The native context-capability guard and
held-out interaction passed, but calibration identity stability and positive
absolute headroom failed. Because all data, numerical, resource, and
completeness guards passed, the outcome is `failed`, not `insufficient`.

The allowed conclusion is:

> On frozen Qwen3-Coder at the final MoE block, CrossCodeEval context changes
> counterfactual expert effects, but the registered evaluation does not find a
> split-stable context-favored expert with positive loss headroom over native
> routing.

It cannot establish Router training benefit, rare/common learning dynamics,
conflict isolation, expert semantics, other-layer behavior, or long-context
scaling.

## 2. Definitions and Decision Roles

- **Target negative log-likelihood (NLL):** mean \(-\log p(y_t)\) over the fixed
  ground-truth target tokens, in nats per target token. Lower is better. It
  measures predictive loss, not generated-code correctness.
- **Matched slot swap:** at target-predicting positions in the final MoE block,
  replace the lowest-weight native top-8 expert by candidate \(e\), retain that
  weight and the other seven experts, and do not renormalize. A natively active
  candidate is a strict no-op at that position.
- **Headroom:** \(H_e^c=L_{native}^c-L_{swap(e)}^c\). Positive values mean the
  candidate improved loss over the native mixture; non-positive values do not
  provide positive Router headroom.
- **Context shift:** \(\delta_e=H_e^{REL}-H_e^{NUIS}\). It measures how relevance
  changes one expert's counterfactual utility; it does not by itself show that
  the expert is useful.
- **Interaction:**
  \(I_{ctx}=(H_a^{REL}-H_b^{REL})-(H_a^{NUIS}-H_b^{NUIS})\). It removes effects
  common to both experts, but can be positive because one expert becomes more
  harmful. The separate \(H_a^{REL}>0\) guard is therefore necessary.
- **Route overlap:** \(\sum_e q_e^{REL}q_e^{NUIS}\) at aligned positions. It is a
  probability-similarity diagnostic whose scale depends on Router sharpness;
  it cannot classify sharing as useful or harmful.

## 3. Frozen Setup

### Model

- Local path: `/data/share/Qwen3-Coder-30B-A3B-Instruct`.
- Loading: `local_files_only=True`, `HF_HUB_OFFLINE=1`,
  `TRANSFORMERS_OFFLINE=1`.
- Dtype and mode: BF16, batch size one, `eval()`, no generation, no update.
- Loaded module tree: 48 decoder layers, all actual MoE blocks; final block at
  zero-based layer 47; 128 routed experts; top-8; no shared expert.
- Indexed tensor bytes: 61,064,245,248. Config, index, and tokenizer hashes are
  frozen in [protocol.md](protocol.md).

### Data

- CrossCodeEval Git revision:
  `40c68d2b7ca2a8eae95d901ac80e6a540a84a53d`.
- Non-oracle file:
  `python/line_completion_rg1_unixcoder_cosine_sim.jsonl`.
- Original samples: 2,665.
- Frozen manifest: 256 samples, SHA256
  `71fbd719a9f401935d909209bf6b195812bbfd37c5b21af017a93ba2a5c60169`.
- Splits: cal-A 64 samples / 46 repositories; cal-B 64 / 43; test 128 /
  83. Repository sets are disjoint.
- Longest target: 35 tokens. Longest complete condition: 3,354 tokens.
- `REL` and `NUIS` cross-file portions have exactly equal Qwen tokenizer length;
  the in-file prefix and target token IDs are identical across all three
  conditions.

### Statistics

- Calibration chooses \((a,b)\) only from cal-A + cal-B.
- Stability requires \(a\) in each half's top eight \(\delta_e\) values and \(b\) in
  each half's bottom eight.
- Test remains untouched until \((a,b)\) is frozen.
- Confidence intervals use repository-clustered paired bootstrap, seed `60402`,
  10,000 replicates.

## 4. Implementation and Self-Checks

Each sample/condition executes one native Transformer forward. Hooks capture
the final MoE input, router logits, native MoE output, and pre-MoE residual.
Candidate expert outputs are evaluated only at target-predicting positions. The
candidate final state is reconstructed in the model's exact BF16 order:

\[
h_{final}^{(e)}=residual+(m_{native}+\Delta m_e).
\]

The final RMSNorm and LM head then recompute target logits. This avoids 128
complete Transformer forwards per condition.

Two early smoke attempts were correctly stopped. They reconstructed
\((residual+m_{native})+\Delta m_e\), which is algebraically equal in real
arithmetic but not numerically associative in BF16. The discrepancy was
0.062--0.115 nats/token. Capturing the residual and restoring exact addition
order reduced both logit and NLL error to zero without relaxing tolerance.

Registered checks after correction:

| Check | Result |
| --- | ---: |
| 4096-token batch-one peak allocation | 57.1084 GiB |
| Free H100 memory after 4096 smoke | 21.3226 GiB |
| Two samples × two conditions × four candidates: max logit error | 0 |
| Same check: max token-NLL error | 0 |
| Formal per-position no-op token-NLL error | 0 |
| Four-GPU smoke shards | 4/4, two samples each |
| Four-GPU smoke peak allocation | 57.0137--57.0922 GiB |

## 5. Execution Ledger

| Job | Resource | State / role |
| --- | --- | --- |
| `pt-mljn674o` | 4×H100, spot | stopped after remaining Pending; no evidence |
| `pt-an3xzwpn` | 4×H100, reserved | stopped while remote PyPI install stalled; no evidence |
| `pt-11i6h4tv` | 4×H100, reserved | succeeded; decisive four-shard smoke |
| `pt-loe1371e` | 4×H100, reserved | succeeded; 256-sample full scoring |

The successful jobs used an offline 21MB wheelhouse for Python dependencies and
never accessed a model registry. Full execution produced four shards of exactly
64 samples. Each sample was appended and `fsync`-ed after completion.

Full-run peak allocated memory by rank was 57.0830, 57.0703, 57.1549, and
57.1439 GiB. The ACP full job ran from 02:37:48 to 02:47:11 UTC on 2026-07-21,
including scheduling, four checkpoint loads, and scoring.

## 6. Completeness Audit

- Unique sample indices: 256/256.
- Conditions per sample: `REL`, `NUIS`, and `LOCAL`, all present.
- Candidate expert IDs per sample/condition: 0--127, all present.
- Total candidate cells: \(256\times3\times128=98{,}304\).
- Duplicate sample indices: none.
- Non-finite native or candidate losses: none.
- Worker completion files: 4/4.

The compact audit is [completeness.json](artifacts/completeness.json); execution
and memory evidence is [execution_audit.json](artifacts/execution_audit.json).

## 7. Primary Results

### Native context-capability guard

Test native mean NLL:

| Condition | Mean NLL |
| --- | ---: |
| LOCAL | 1.97503 |
| REL | 2.12697 |
| NUIS | 2.33067 |

The registered paired contrast is
\(L^{NUIS}-L^{REL}=0.20370\), 95% CI [0.05908, 0.35929], so the guard passes.

`REL` does not establish a net benefit over `LOCAL`:
\(L^{LOCAL}-L^{REL}=-0.15193\), 95% CI [-0.29636, 0.00012]. The relevant snippets
remove much of the nuisance-context penalty but do not beat the shorter local
prompt on this NLL surface.

### Calibration

Calibration selected \(a=49\) and \(b=53\).

| Expert | cal-A \(\delta\) rank | cal-B \(\delta\) rank | Stability requirement |
| ---: | ---: | ---: | --- |
| 49 | 8 / 128 | 16 / 128 | Fail: not top-8 in cal-B |
| 53 | 128 / 128 | 124 / 128 | Pass: bottom-8 in both |

The complete cal-A versus cal-B expert-shift Spearman correlation is 0.083,
which indicates that the context-specific ordering is not reproducible across
the two repository groups.

### Held-out interaction and absolute headroom

| Metric | Estimate | 95% CI | Rule | Result |
| --- | ---: | ---: | --- | --- |
| \(I_{ctx}^{test}\) | 0.01163 | [0.00336, 0.02022] | \(\ge0.01\), CI lower \(>0\) | Pass |
| \(H_{49}^{REL,test}\) | 0.00540 | [-0.00105, 0.01225] | \(\ge0.01\), CI lower \(>0\) | Fail |

Selected-pair test means:

| Expert | \(H^{REL}\) | \(H^{NUIS}\) | \(\delta\) |
| ---: | ---: | ---: | ---: |
| 49 | 0.005397 | 0.004577 | 0.000820 |
| 53 | -0.036005 | -0.025199 | -0.010806 |

Therefore the interaction is dominated by expert 53 becoming more harmful,
not by expert 49 becoming usefully better. Expert 49 has positive headroom on
only 50% of test samples; its median headroom is approximately zero.

## 8. Secondary Diagnostics

- REL/NUIS native top-8 Jaccard: 0.76412.
- Full-probability route overlap \(\sum_e q_e^{REL}q_e^{NUIS}\): 0.03174.
- Final-MoE-input REL/NUIS L2 distance: 26.1267.
- Test aggregate REL/NUIS expert-headroom Spearman: 0.89125.
- Expert 49 native inclusion rate at test target positions: 1.42% under REL and
  1.27% under NUIS; low headroom is therefore not an artifact of most swaps
  becoming no-ops.

These diagnostics indicate large representation change, mostly shared expert
ordering, and substantial native top-8 persistence. None alters the primary
failure verdict.

The optional selected-pair parameter-gradient diagnostic was not executed. It
was secondary, could not change the verdict, and would not repair failed
identity stability or positive-headroom clauses.

## 9. Figure Contracts and Visual Audit

### `primary_context_and_headroom.png`

- Question: does native context work, and is the frozen favored expert useful?
- Data: untouched test split only.
- Left panel: sample-mean native NLL with repository-bootstrap 95% intervals.
- Right panel: selected-pair swap headroom with the registered +0.01 line.
- Allowed conclusion: REL beats NUIS in the paired test, while expert 49's
  positive headroom is below threshold and uncertain.
- Limitation: individual NLL error bars do not replace the paired contrast CI.

The rendered figure was audited for label, unit, condition order, error-bar,
and threshold visibility.

### `calibration_stability.png`

- Question: is expert context shift reproducible between calibration halves?
- Data: all 128 experts, cal-A and cal-B only.
- Axes: mean \(\delta_e\) in nats per target token.
- Highlighted points: preregistered selected experts 49 and 53.
- Allowed conclusion: expert 49 misses the cal-B top-eight guard and global
  ordering is weakly correlated.
- Limitation: the plot is a stability diagnostic, not a held-out effect test.

The rendered figure was audited; selected points, zero axes, equality line, and
labels are visible without overlap.

## 10. Artifact Map

Curated mainline artifacts:

- [primary_metrics.json](artifacts/primary_metrics.json)
- [selected_pair_metrics.csv](artifacts/selected_pair_metrics.csv)
- [calibration_expert_means.csv](artifacts/calibration_expert_means.csv)
- [route_overlap.csv](artifacts/route_overlap.csv)
- [primary_context_and_headroom.png](artifacts/primary_context_and_headroom.png)
- [calibration_stability.png](artifacts/calibration_stability.png)
- [execution_audit.json](artifacts/execution_audit.json)

Remote/raw execution surface:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/
MoE_Routing_Experiments/active/a06_04_context_utility/
  data/sample_manifest.jsonl
  runs/preflight/
  runs/smoke/
  runs/smoke_acp4/
  runs/full/shard_0.jsonl ... shard_3.jsonl
  runs/full/analysis/
```

Raw 98,304 candidate cells and logs remain on the execution surface and are not
duplicated into the research mainline.

## 11. Anchor Update Implication

The result weakens the claim that a frozen final-layer expert pool already
contains stable context-specific positive utility that the native Router simply
fails to select. It supports only a weaker fact: context changes expert
counterfactual effects, including how harmful a mismatched expert can be.

**Next decision:** move the research question from frozen-expert mining to a
training-time test of whether selective sharing can create stable positive
utility while preserving common-information performance.
