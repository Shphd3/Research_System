# Training assets and comparison boundary

Native Dense is the eight-layer seed17 trajectory, not official Qwen, S7, SALL or a dictionary. It has281431040total/conventional active parameters, hidden1024,16query/8KV heads of128dimensions, SwiGLU3072,2048context, RoPE theta1000000,vocabulary151936and tied embeddings. Ordinary MoE shares attention/context/tokenizer and uses8experts of1536,top2,507988992total and281496576conventional active parameters. The65536active-parameter difference is eight router matrices. Conventional matrix counts include the shared embedding matrix; they are not the number of embedding rows touched or measured FLOPs. Routing/dispatch, optimizer memory and hardware differ.

Both use DCLM paired view dclm_pair_v1, a30B-token unique view with cycling,262144valid targets per ordinary update, AdamW lr0.0003,betas(0.9,0.95),eps1e-8,weight decay0.1,and1000-update warmup followed by the audited native constant-LR history. Exact milestone boundaries can have shortened updates. These optimizer statements come from stored configs/run audits, not new optimizer experiments. Every checkpoint's actual counter, file SHA and architecture are verified in this evaluation.

Dense original/continuation hardware includes eight RTX5090; MoE uses four H100 and verified continuation/speedup branches. Total capacity, FLOPs and wall time are not matched. Historical sample/mask order matches through22.018691584Bonly; Dense continuation then changed its sampler mapping. The prior full-loss and sampler-root-cause audits are linked in the aligned Chinese asset guide; no sampler or training is rerun here. Unknown training-pattern exposure remains.

[Exact configs and training-log/source audits](training_assets_cn.md) · [Actual snapshot](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/audit/selected.json).

The30Blimit is the logical training subset passed as max_tokens=unique_data_tokens, not the entire physical paired view (approximately302.089Btoken IDs). This task does not rescan or modify training data.
