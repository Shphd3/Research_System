# ACP 训练设备清单

每行配置对应一个 ACP。节点数填 `WORKER_NODES`（`--worker-nodes`），每节点 GPU 数由 `SPEC`（`--worker-spec`）决定，总卡数为两者相乘。配额填 `QUOTA_TYPE`（`--quota-type`）。

## 未指定设备时的优先级

用当前获授权的 profile 按表从上到下检查，选择第一个满足任务、规格和配额的配置。用户指定 GPU、节点拓扑或配额时，按指定条件选型。

| 顺序 | GPU | 节点数 | 每节点卡数 | 总卡数 | `QUOTA_TYPE` | 已见 `SPEC` |
| --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | H100 | 2 | 2 | 4 | `reserved` | `n6ls.iu.i40.2` |
| 2 | H100 | 1 | 4 | 4 | `reserved` | `n6ls.iu.i40.4` |
| 3 | H100 | 2 | 2 | 4 | `spot` | `n6ls.iu.i40.2` |
| 4 | RTX 5090 | 1 | 4 | 4 | `spot` | `n12lp.nn.i10a.4` |
| 5 | RTX 5090 | 2 | 2 | 4 | `spot` | `n12lp.nn.i10a.2` |

5090 四卡优先放在同一物理机，训练步中的梯度同步可以留在节点内。单节点与双节点的四卡吞吐差值需要同负载实测。双节点 5090 可沿用 [Socket 调优配方](rtx5090-training-cn.md)。

## 其他可选配置

| GPU | 节点数 | 每节点卡数 | 总卡数 | `QUOTA_TYPE` | 已见 `SPEC` |
| --- | ---: | ---: | ---: | --- | --- |
| H100 | 4 | 2 | 8 | `spot` | `n6ls.iu.i40.2` |
| RTX 5090 | 2 | 4 | 8 | `spot` | `n12lp.nn.i10a.4` |
| RTX 5090 | 1 | 8 | 8 | `spot` | `n12lp.nn.i10a.8` |
| H100 | 按任务所需 | 1 | 等于节点数 | `spot` | `n6ls.iu.i40.1` |

每节点一卡的 H100 Spot 用于卡型或配额紧张时。节点数按任务需求填写。

## 提交前核对

这些 SKU 来自曾查询到的规格目录。用当前 profile 查目标池的规格，再确认该配额下每台宿主能提供的卡数和可用宿主数。

```bash
sco --profile "$SCO_PROFILE" aec2 clusters list-workerspec \
  --workspace-name "$SCO_WORKSPACE" --aec2-name "$SCO_AEC2"
```

把选中的 `WORKER_NODES`、`SPEC` 和 `QUOTA_TYPE` 传给 [ACP 提交模板](acp_submit_template.sh)。单节点四卡和八卡分别在本机启动 4 和 8 个训练进程。多节点起跑前用 `get-workers` 确认每个 Worker 的物理宿主。需要 H100 跨机 RDMA 时，在已验证的配置中每个 ACP 都需申请至少两个节点，再按 [RDMA 验收流程](acp.md#multi-node-rdma) 检查设备和 NCCL 通道。
