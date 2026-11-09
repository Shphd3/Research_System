# Read-only reproduction

The executed scorer is /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/run.py; config at /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/config.json. The scorer computes the native model's final normalized hidden states, then its frozen lm_head at every candidate-token prediction position, with the candidate's own earlier tokens included. This matches the public full forward within the frozen numerical tolerance. It never extracts SAE activations.

To recompute all point estimates from saved per-token scores, without loading a model or third-party library:

```bash
python /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/replay_metrics.py
```

To also re-tokenize every actual text, check offsets/distances, full candidate chains, pair invariance, priors, all sums, Wilson intervals and preserved frozen inputs:

```bash
env PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3 python /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/verify.py
```

The same processing agent wrote the independent arithmetic implementation; this is numerical validation, not independent scientific review. Original source hashes are preserved in freeze.json. After the factual Anchor update and path repair, frozen_owner_resolution.json maps its original pre-run bytes to immutable execution-side snapshots. Protocol text, input panel and model weights stay unchanged.

Model forwards are already complete. run.py refuses to overwrite scored outputs. Re-running a whole panel is not needed for metric replay and is not launched by either command above. Complete text/tokens in data/panel.jsonl and complete raw scores in results/smoke.jsonl plus heldout.jsonl remain at the execution root. Canonical code copies are reading copies of the actual execution code; use the actual absolute execution path for these commands.
