# share 和 P12 的 Reserved 训练调用方法

[English](sco_reserved_training_guide.md)

你可以通过同一个账号，在 `share-space` 或 P12 工作空间提交单机四卡 H100 Reserved 任务。P12 的真实测试 `pt-mqi6ojfn` 已于北京时间 2026 年 11 月 9 日成功结束：四卡计算、四进程 NCCL 通信和原 AFS 存储双向读写全部通过。它证明这条运行路径已接通；具体模型仍使用自己的训练启动脚本和训练 Smoke。

后续 Agent 使用本文第 3 节的统一入口。不同的已授权实验可以分别放在两边；同一个正式主任务只提交到选定的一边。已有任务排队时，继续检查原任务 ID，不向另一边复制完整主任务。

## 1. 工作空间和资源池的区别

工作空间决定任务归属、访问权限和配额记账；资源池提供实际节点。你说的“两边”在这里是两个工作空间，它们会调用相同的底层 H100 池。

| 项目 | share | P12 |
|---|---|---|
| 命令中的简写 | `share` | `p12` |
| 完整工作空间名 | `share-space` | `p12-large-model-training-platform-on-domestic-computing` |
| 正式提交配置键 | `h100-4-reserved` | `p12-h100-4-reserved` |
| 本文已验证的资源池 | `share-cluster` | `share-cluster` |
| 四卡规格 | `n6ls.iu.i40.4` | `n6ls.iu.i40.4` |
| 配额类型 | `reserved` | `reserved` |

这两条路径都使用一个节点、四张 H100 80GB SXM5、88 vCPU、960 GiB 主机内存。主机内存与每张 GPU 的显存分开计算。

资源参数、镜像和挂载的当前来源是 [执行环境注册表](execution_envelope.md)。全局默认仍为 share 的 `h100-4-reserved`；P12 必须明确选择，不能把“选了四张卡”当作已经选了 P12。

### Reserved 的含义与额度

Reserved 是提交时明确指定的资源类别。配额允许请求资源，实际启动还需要节点同时满足 GPU、CPU 和主机内存要求。Reserved 不意味着提交后立即获得空闲节点。

2026 年 11 月 8 日至 9 日的接口核查显示：

- share 正式计算资源组默认成员设置为合计 4 卡、88 vCPU。
- P12 的默认成员 Reserved 设置为 192 卡，工作空间 Reserved 总上限也为 192 卡。这个上限由 P12 的两个 H100 池合计共享，不是每池 192 卡，也不是你个人独占 192 卡。
- 本次 P12 四卡请求计入 P12 的 4 卡、88 vCPU、960 GiB 用量；同时 share 正式计算组仍显示 0 卡。两边分别记账。

配额分开记账不增加底层物理卡数，也不证明两边能够同时获得全部上限。本次没有做“两边同时各运行四卡”的测试。

## 2. 镜像、存储和已完成的验证

当前默认镜像键为 `shphd-lite-0911`。提交脚本从注册表解析完整镜像地址，不通过列举私有镜像猜地址。P12 实测环境是 Python 3.10、PyTorch `2.3.0a0+6ddf5cf85e.nv24.04`、CUDA 12.4。

两边使用同一个原 AFS 卷：

```text
volume ID: 01995892-d478-76d8-aec7-13fd8284477e
volume name: afs-share-01g
container mount: /data
user directory: /data/250010109
```

因此，从 share 切到 P12 不要求复制整份用户存储。任务必须显式挂载这个卷；控制台自动选择的其他存储卷不能替代它。命令必须显式进入任务目录，不能依赖远端容器的初始目录。

P12 测试读取了当前容器写出的 256 KiB 随机文件，核对随机文件和源代码哈希，再写入带唯一标记的响应文件；当前容器回读并验证了响应哈希。四个不同 GPU UUID、每卡矩阵乘法和四进程 NCCL all-reduce 也全部通过。测试实际运行约 14.25 秒，平台最终状态为 `SUCCEEDED`。

证据位于：

```text
/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/20261108T155519Z/
```

读取 `execution_certificate_completed.json`、`local_verification.json`、`result.json` 和 `pod.log`。同目录的 `execution_certificate.json` 是较早的五分钟启动观察快照，保留了当时尚未执行的状态；它不替代完成记录。

## 3. 推荐的训练提交入口

使用新增的工作空间选择器，它复用原有提交模板、注册表解析、授权检查、持久日志和 JSON 回执：

```bash
SUBMIT=/data/250010109/Research_System/templates/execution/acp_submit_reserved_workspace.sh
```

选择器只接受 `RESERVED_WORKSPACE=share` 或 `RESERVED_WORKSPACE=p12`。它分别解析上述两个资源配置键，不自动换到 Spot，不自动换规格，也不同时向两边提交。

### 3.1 准备任务目录和启动脚本

把代码、配置、日志和检查点放在 `/data` 下任务自己的执行目录。下面的路径只是填写示例，应替换成已存在的具体任务目录和真实启动脚本；不要用示例路径直接提交。

```bash
export REMOTE_DIR=/data/250010109/MoE_Router/experiments/YOUR_EXPERIMENT
export REMOTE_CMD='bash scripts/run_authorized_training.sh'
```

`REMOTE_CMD` 会在 `REMOTE_DIR` 内执行。启动脚本负责激活该任务已验证的软件环境、加载配置并启动训练。例如，一个已实现数据并行的四卡训练程序通常由启动脚本调用：

```bash
torchrun --standalone --nnodes=1 --nproc_per_node=4 train.py --config configs/approved.json
```

这只是启动形式，不能替代实际任务的参数。已经自行调用 `torchrun` 的启动脚本，不要再套一层 `torchrun`。不要把来自两个工作空间的独立任务当作一个八卡分布式任务。

### 3.2 在 share 预览一次提交

```bash
export RESERVED_WORKSPACE=share
export JOB_NAME=YOUR_UNIQUE_SHARE_JOB_NAME
export RUN_ROOT="$REMOTE_DIR/acp_receipts/$JOB_NAME"
bash "$SUBMIT"
```

默认只打印解析结果和远端命令，不创建任务。检查输出中的工作空间必须为 `share-space`，资源配置为 `h100-4-reserved`，配额类型为 `reserved`，节点为 1，规格为 `n6ls.iu.i40.4`。

### 3.3 在 P12 预览一次提交

```bash
export RESERVED_WORKSPACE=p12
export JOB_NAME=YOUR_UNIQUE_P12_JOB_NAME
export RUN_ROOT="$REMOTE_DIR/acp_receipts/$JOB_NAME"
bash "$SUBMIT"
```

检查工作空间必须为 `p12-large-model-training-platform-on-domestic-computing`，资源配置为 `p12-h100-4-reserved`。其余硬件、镜像和原存储与 share 的四卡配置一致。

### 3.4 执行选定一边的已授权任务

先在当前 shell 中保留选定一边的 `RESERVED_WORKSPACE`、唯一 `JOB_NAME`、`REMOTE_DIR`、`REMOTE_CMD`、`RUN_ROOT`。以下标记表示该具体任务确实已有执行授权、且适用的训练 Smoke 已通过；不能仅因为示例里写了 `1` 就把未完成的检查算作通过。

```bash
DRY_RUN=0 \
ALLOW_SUBMIT=1 \
PROTOCOL_APPROVED=1 \
SMOKE_GATE_PASSED=1 \
bash "$SUBMIT"
```

执行后记录返回的 `pt-...` 任务 ID。提交模板把准确参数和平台原文写入 `RUN_ROOT/submit-*.json` 与对应 `.txt`；远端完整输出写入 `REMOTE_DIR/acp_receipts/pod/`。选择器会拒绝在同一回执目录重复提交同一个任务名。

若创建调用超时或返回不明确，先按工作空间、提交者和唯一任务名检查是否已创建，再决定如何处理。不要把客户端超时当成“没有提交成功”而直接再提交一次。

## 4. 查询两边的任务

统一查询入口会启动当前兼容桥，并明确选择工作空间。已验证两边的只读调用均能返回对应工作空间的数据。

```bash
TOOL=/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/agent_submission_guide/sco_workspace.py
```

share：

```bash
python "$TOOL" --workspace share jobs list --user-name 250010109 --page-size 20 -o json
python "$TOOL" --workspace share jobs describe -o json YOUR_SHARE_JOB_ID
python "$TOOL" --workspace share jobs get-workers YOUR_SHARE_JOB_ID
python "$TOOL" --workspace share jobs stream-logs YOUR_SHARE_JOB_ID
```

P12：

```bash
python "$TOOL" --workspace p12 jobs list --user-name 250010109 --page-size 20 -o json
python "$TOOL" --workspace p12 jobs describe -o json YOUR_P12_JOB_ID
python "$TOOL" --workspace p12 jobs get-workers YOUR_P12_JOB_ID
python "$TOOL" --workspace p12 jobs stream-logs YOUR_P12_JOB_ID
```

已完成的 P12 测试可以直接查询：

```bash
python "$TOOL" --workspace p12 jobs describe -o json pt-mqi6ojfn
```

完成任务的临时容器输出可能已不保留，优先读取 AFS 中的持久日志和结果。任务列表可能包括其他用户；使用自己的用户名过滤，不操作其他人的任务。

## 5. 截图里的调度错误怎么处理

本次测试先排队，后来成功启动。截图里的 `FailedScheduling` 是此前调度尝试的事件，不是训练代码已经运行后报错。

| 事件内容 | 含义与检查方式 |
|---|---|
| `insufficient nodeSpec quota: cpu ..., memory ...` | 节点或规格的可分配 CPU、主机内存暂时不能满足请求。本次同时申请四卡、88 vCPU、960 GiB 主机内存。主机内存不足与 GPU 显存不足分开处理。 |
| `cpu 34000m` | `1000m` 等于 1 个 CPU 核，因此 `34000m` 是 34 核的数量。不能把它读作任务已使用 34,000 核。 |
| `112/116 nodes ... match job` | 说明节点匹配条件的统计，不代表有 112 个空闲节点。 |
| `4 node(s) cordon` | 这四个节点暂时不接收新任务。 |
| `unbound immediate PersistentVolumeClaims` | 该次调度时存储声明尚未绑定。结合最新事件和实际挂载确认；本次后续双向读写已通过。 |

当前资源池还展示了四卡低主机资源规格：`n6ls.iu.i40.4.16c256g` 为 16 vCPU、256 GiB，`n6ls.iu.i40.4.32c512g` 为 32 vCPU、512 GiB。它们可以在明确选择并更新任务配置后使用，但本文没有实测这些规格，也没有把它们设为自动回退。降低主机资源会影响数据加载或 CPU 分析，不能保证立即调度成功。

P12 还关联 `computing-cluster-01g-02`。其常规四卡规格为区分大小写的 `N6lS.Iu.I10.4`，88 vCPU、920 GiB 主机内存；这不是本文已经跑通的 `share-cluster` 路径。若之后明确选择它，先登记完整资源配置并做该池的运行检查，不把规格字符串直接套用过去。

## 6. 训练与恢复需要保留什么

本次工程验证允许你使用这条资源路径；它没有替某个新模型验证 loss、显存峰值、数据顺序、优化器恢复或长期稳定性。

具体训练沿用所属任务的启动脚本、Protocol 和 [训练观测约定](training_observability_contract.md)。比较实验保留全局有效 token batch、数据顺序和 loss 归一化；显式记录 `tokens/train_lm_loss`、累计有效目标 token、学习率、实际总 loss 及启用的辅助项。检查点和数据使用前按 [资产注册表](../assets/README.md) 查找并验证所需 ID。

两边使用同一 AFS，因此可以访问相同的已保存检查点。恢复仍由训练程序显式加载模型、优化器、调度器、随机状态、数据位置和 token/update 计数。平台的 `jobs start` 不自动证明这些状态已恢复；不要用它代替训练程序的恢复入口。

切换工作空间前先检查原任务是否还在运行，避免同一轨迹出现两个同时写入相同目录的任务。新的已授权恢复任务使用独立回执和输出段，保留原检查点及其来源。改变 GPU 数量或微批量时，遵守已有的全局 batch 和运行资格检查。

## 7. 给后续 Agent 的执行规则

1. 先读本文和当前执行环境注册表，选择 `share` 或 `p12`。同一个正式主任务只选一边；不同的已授权实验可以分配到两边。
2. P12 已完成四卡与存储工程验证，不要重复提交 `pt-mqi6ojfn` 对应的小测试。新的具体训练仍检查自己的 Smoke 和恢复条件。
3. 用第 3 节入口先预览，核对完整元组，再执行已有授权的任务。保持 `reserved`，不自动改 Spot、资源池或规格。
4. 保存回执和任务 ID。检查已有任务，不因排队或查询错误重复提交。首次启动观察后按用户要求结束轮询；持续监控另按已授权范围执行。
5. 用 AFS 中的持久日志、实际检查点和结果交付；完成训练时登记实际保存的检查点。不要把提交成功、平台状态或本次工程 PASS 当成科学结果。

## 8. 相关文件

- [执行环境注册表](execution_envelope.md)：资源配置、镜像、存储和原始提交入口的当前来源。
- [工作空间选择器](../templates/execution/acp_submit_reserved_workspace.sh)：预览及正式提交 share/P12 四卡 Reserved 任务。
- [原始提交模板](../templates/execution/acp_submit_template.sh)：持久日志、授权标记和提交回执。
- [训练代码复用索引](training_reuse_index.md)：需要实现或改动训练程序时读取。
- [P12 完成证据](/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/20261108T155519Z/execution_certificate_completed.json)。
