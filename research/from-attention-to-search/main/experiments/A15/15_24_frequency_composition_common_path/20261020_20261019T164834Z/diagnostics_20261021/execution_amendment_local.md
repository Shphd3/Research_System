# Execution amendment: user-requested local frozen inference

Scope: the [three frozen diagnostics](analysis_contract.md), using the same data, step168 checkpoints, seeds, coefficients and NLL comparisons.

The researcher asked, “是否可以在本地冻结诊断？远端似乎资源不足。” The assistant accepted this as an instruction to execute the bounded frozen diagnostic locally. This supplies a stage-specific resource exception to the default execution envelope.

Current read-only device probe found one CUDA device: NVIDIA H100 80GB HBM3 MIG 3g.40gb, reported memory42,412,802,048 bytes, compute capability9.0. Runtime: PyTorch2.3.0a0+6ddf5cf85e.nv24.04. Execute four checkpoint workers sequentially on cuda:0, with at most16GiB allocated GPU memory per worker and at most8 aggregate CPU threads. Record actual runtime, numerical replay gates and source identity.

Use a separate `ablation/local_gpu` output root. Keep the full DEV order, original batch128, native actual expert dispatch shapes, same cached residual components across contrasts, original final RMSNorm/LM head and BF16 inference. No parameter updates, new targets or model selection.

Earlier GPU creation failed for member quota. The researcher then explicitly selected “优先完成冻结诊断，再重提普通 MoE”. A remote diagnostic was accepted as pt-t9lutqt0 after the unstarted ordinary-MoE job pt-50sa30mo was stopped; the subsequent local request supersedes that diagnostic transport. Preserve all receipts and avoid duplicate diagnostic execution. Restore the ordinary-MoE job under its unchanged original configuration and h100-4-reserved profile; record its replacement ID and absence/presence of any old training progress.

This amendment changes only execution location and task ordering. Required asset, identity, numerical and scientific-boundary checks remain in force. Actual job/device state and completion are owned by execution receipts.
