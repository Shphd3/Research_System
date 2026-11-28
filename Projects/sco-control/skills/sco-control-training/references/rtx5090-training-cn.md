# RTX 5090 多节点训练配方

四卡选型优先用 [单节点四卡 5090 Spot](training-devices-cn.md)。这份配方用于选定双节点 5090 或需要测试跨任务互联时。双节点基线用单个 ACP、两台物理机、每台两张 5090。在已测池中，每个 Worker 使用 `n12lp.nn.i10a.2`，即 **2 张 RTX 5090、28 vCPU、120 GiB**。同一规格用于两个独立 ACP 时，每个 ACP 仍申请两个 Worker，四个 Worker 合为一个八卡训练组。

## 提交和启动

1. 确认四卡轮为一个 ACP、两个不同物理宿主。八卡轮是两个 ACP，每个 ACP 各两个 Worker，跨四个宿主。两轮保持镜像、worker 规格、数据和训练代码一致。用 [ACP 提交模板](run_sco_pattern.md#dry-run) 预览每项任务，设置 `WORKER_NODES=2`、`SPEC=n12lp.nn.i10a.2` 和唯一任务名。跨账号分别使用各自获授权的 profile。
2. 用 `sco --profile "$SCO_PROFILE" acp jobs get-workers --workspace-name "$SCO_WORKSPACE" "$JOB_ID"` 查询 Pod IP 和宿主。将本轮可用的 Pod IPv4 按顺序写入一个 JSON 字符串数组，四卡轮两个地址，八卡轮先放作业 A 的两个地址，再放作业 B 的两个地址。第一个地址是会合端点。用临时文件写完整后重命名发布。所有 Worker 需要获得内容相同的清单和端口。
3. 将 [Worker 启动器](torchrun-worker.py)、训练脚本与会合清单放在 Worker 能读到的位置。每个 Worker 用同一条命令，按清单自动确定节点 rank。下面的环境变量由 Worker 启动命令或项目脚本设置。`ENDPOINTS_JSON`、`TRAIN_SCRIPT` 和 `SCO_TORCHRUN_WORKER` 分别指向容器内路径，`RENDEZVOUS_PORT` 在本轮所有 Worker 上一致且可达。

```bash
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
# 先跑平台默认设置。确认走 Socket 后，在调优组的每个 Worker 上启用下面两项
# export NCCL_SOCKET_NTHREADS=2 NCCL_NSOCKS_PERTHREAD=2
python "$SCO_TORCHRUN_WORKER" --wait-seconds 900 --run-seconds 300 \
  --port "$RENDEZVOUS_PORT" --nproc-per-node 2 "$ENDPOINTS_JSON" "$TRAIN_SCRIPT"
```

启动器为每节点两个 GPU 进程生成不同的全局 rank。训练脚本应按 `LOCAL_RANK` 绑定 GPU，初始化 NCCL，按全局 rank 分片输入。训练代码显式限制 PyTorch CPU 计算线程时，从每进程 2 个线程起步。由全局 rank 0 记录汇总 loss、有效训练 token 和 checkpoint。跨账号的 AFS 输入和结果目录按 [AFS 权限说明](aec2-afs.md#afs-acl) 单独验收。

## 网络验收与已测结果

目录中的 RoCE 标记是规格信息。依次核对作业是否获得 `rdma/hca`、Worker 的 `ibv_devinfo -l` 和链路类型，再查看 NCCL 的跨宿主 all-reduce 通道。八卡轮额外检查一对来自不同 ACP、不同宿主的 rank。会合端口的 TCP 连通性用于启动训练组。

| 实测 | 结果 |
| --- | --- |
| computing 池的同负载四卡和八卡，默认 Socket | 容器均报告 0 个 HCA，跨机走 `NET/Socket/0`。后 8 步吞吐为 8,986 和 7,575 tokens/s，八卡低 15.7%。 |
| debug 池固定宿主的四卡，默认 Socket 与 2×2 | 两组均走 Socket。256 MiB 四秩 all-reduce 中位耗时 263.13 → 87.19 ms。相同约 100M Qwen3、10 步合成数据短训中，后 8 步吞吐 12,977 → 19,555 tokens/s。 |
| computing 池固定宿主的八卡，默认 Socket 与 2×2 | 四台宿主、两个 ACP，固定同一 100M Qwen3 合成负载。八卡吞吐 7,997 → 15,866 tokens/s。同批宿主中取第一份 ACP 的两台机器跑四卡 2×2，吞吐 21,220 tokens/s。 |

实测每步均为 4,080 个有效预测 token。两个池的对照各按默认、2×2 的顺序跑一次。单节点四卡、真实数据吞吐和长跑收益待测。

## 调优顺序

- **先复测 Socket 参数。** 固定节点、镜像、模型、真实训练时用的序列长度、有效 token/步、数据顺序和随机种子。比较默认与 2×2，重复或交换顺序。记录小和大消息的 all-reduce 中位耗时，以及训练 tokens/s、步时 P50/P95、CPU 使用率和数据等待时间。2×2 增加用于 TCP 通信的 CPU 线程和连接数。 [NVIDIA NCCL 参数](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-socket-nthreads)
- **确认目标吞吐再扩到八卡。** 固定全局 batch 时，GPU 数翻倍会减少每卡计算，梯度仍需跨机同步。先在同八卡拓扑上比较默认与 2×2，再和已调优四卡对照。组合使用梯度累积时，仅在累积窗口的最后一次反向同步，另行核对有效全局 batch 与 loss。 [PyTorch DDP no_sync](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html#torch.nn.parallel.DistributedDataParallel.no_sync)
- **CPU 按瓶颈调。** 先用 28 vCPU 和每进程 2 个计算线程。若真实语料出现持续数据等待或 CPU 配额用满，再调整预取、DataLoader worker 数和线程数，每次改变一项并复测。记录具体作业、宿主和传输日志。
