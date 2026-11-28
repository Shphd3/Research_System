# 两个 ACP 作业组成四卡训练

这个示例使用两个独立 ACP，各申请两副本、每副本一卡。5090 每节点双卡使用 [RTX 5090 配方](rtx5090-training-cn.md)。每个 Worker 有自己的 Pod IP。四个 Worker 通过同一个 `MASTER_ADDR:MASTER_PORT` 加入同一训练组。任务号用于查询和管理任务，训练进程使用 Pod IP 与端口连接。

## 提交资源和分配 rank

1. 选择两个作业可同时使用的同一 AEC2 训练网与 GPU 规格。对 H100，每个作业设置节点数为 2、每节点 1 卡。混合配额时分别选择 Spot 和 Reserved，保持镜像、GPU 规格、框架和训练网一致。确切资源规格以工作空间的规格表为准。
2. 两份 **To run** 可以使用下面的同一条命令。脚本等待这次运行专用的会合清单，并从清单确定本 Worker 的 rank。用 `sco acp jobs get-workers --workspace-name "$WORKSPACE" "$JOB_ID"` 查两个任务的 Worker。只收录本次两个任务中已进入 Running 的 Worker，并核对共有四个不同的 Pod IP 和四台机器。选择第一个 Pod IP 做 master，约定一个可用 TCP 端口，例如 29632。
3. 为四个 Worker 分配互不重复的 `node_rank=0,1,2,3`。如果共用 AFS，由提交方把四个 Pod IP 按 rank 排列为一个 JSON 字符串数组，以临时文件原子重命名发布。每个 Worker 用自己的 Pod IP 查 rank。跨账号不共享 AFS 时，双方可交换本次的四个 Pod IP、端口和 rank 表，分别写到自己账号的可读路径，或在各自 Worker 的终端传参启动。训练时数据与初始权重仍需按同一运行配置准备，梯度通过 NCCL 通信。
4. 每个 Worker 清除平台为各自作业预置的会合参数，再用统一参数启动。以下变量应由脚本从本次清单取得，或在该 Worker 终端显式设置。

正式跨账号联训先选定主账号的 AOSS 桶，同一训练组共用一个运行前缀，并按 [多账号 AOSS 配置](aoss-storage-cn.md#多账号训练指定主账号的-aoss) 验证每个 Worker 的读取和所需的写入权限。

两项作业的 SCO 提交参数均使用 `--worker-nodes 2`，`--worker-spec` 填该池的一卡规格，`--command` 填下文的 To run 命令。分别传入 `--quota-type spot` 和 `--quota-type reserved`，并为每项作业设置不同的 `--job-name`。默认 AFS 挂载参数为 `--storage-mount "<卷 ID>:/data"`。提交一项后记录作业 ID。另一项若被拒绝，可停止这次已提交的探针，释放等待资源。

```bash
unset MASTER_ADDR MASTER_PORT RANK WORLD_SIZE LOCAL_RANK LOCAL_WORLD_SIZE GROUP_RANK
export NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=INIT,NET,GRAPH
torchrun --nnodes=4 --nproc-per-node=1 --max-restarts=0 \
  --node-rank="$THIS_WORKER_RANK" --master-addr="$RENDEZVOUS_IP" \
  --master-port="$RENDEZVOUS_PORT" /data/<项目目录>/train_or_probe.py
```

如果两边的 Worker 都能读取自己的训练脚本及会合清单，可以将 [torchrun-worker.py](torchrun-worker.py) 和训练脚本放入作业可见的目录，提交时将占位目录换成本次运行的实际路径。

```bash
python /data/<项目目录>/torchrun-worker.py \
  --wait-seconds 300 --run-seconds 300 --port 29632 \
  /data/<本次运行目录>/endpoints.json /data/<项目目录>/train_or_probe.py
```

ACP 的平台配网决定容器是否能使用 RDMA。同账号的历史双 Spot 配置中，每个双副本任务获得了 `rdma/hca`，两任务的 NCCL 实际通道出现过 `NET/IBext_v8/.../GDRDMA`。混合配额、其他资源池和跨账号分别验收。容器安装用户态 RDMA 库可提供工具和运行依赖，硬件设备映射和训练网互通由平台提供。 [ACP 高性能网络变量](https://www.sensecore.cn/help/docs/cloud-foundation/compute/acp/acpUserGuide/acpEnvironmentVariable) · [NCCL 网络诊断](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html)

## 验收

- 用平台资源回执核对每个 Worker 的 `rdma/hca`，进容器看 `/dev/infiniband` 和 `ibv_devinfo -l`。会合端口可以走 TCP，随后梯度的数据通道仍可走 RDMA。
- 四秩做多尺寸 all-reduce，核对每秩求和结果，记录各轮最慢秩耗时和中位数。再挑一对来自不同作业、不同宿主机的 rank 检查 NCCL 数据通道。日志里 NCCL bootstrap 的网卡信息只能说明会合路径。使用对应数据通道的 `NET/IB...`、`GDRDMA` 或 `NET/Socket` 判定实际传输。
- 固定模型、优化器、精度、序列长度、全局 batch、热身和计时步数。同规模单 ACP 或双 Spot 用同一训练脚本做对照。记录有效 tokens/s、步时、loss 与同步耗时。合成 DDP 可验证同步更新，实际训练效率以相同训练负载的对照为准。
- 单次短测应有明确截止时间，记录任务 ID、额度、设备、日志、完成或停止状态。若 Spot 回收，该四秩训练组需要从 checkpoint 恢复并重新会合；作业提交与容器会合分别判断。
