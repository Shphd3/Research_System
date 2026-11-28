# ACP 训练网与 AOSS 存储操作指南

检查日期为 2026 年 11 月 16 日（北京时间）。适用范围是本项目的 SenseCore ACP 作业，另列 SSP 的对象存储直挂入口。资源、镜像和默认 AFS 卷配置由 [执行环境注册表](execution_envelope.md) 管理。

## ACP 如何申请 IB/RDMA

1. 在 **AEC2 控制台 → 集群详情 → 训练网** 查看集群的训练网类型。在 **ACP → 创建任务 → 算力配置** 选择有权限的集群，框架选 PyTorch，选择支持的 GPU 规格和副本数。当前公开 ACP 参数提供 `--aec2-name`、`--worker-spec`、`--worker-nodes` 等，训练网由平台按集群及作业配置分配。ACP 公开控件和 CLI 未查到独立的“为这个作业开启 IB/RDMA”开关。 [ACP 创建任务](https://www.sensecore.cn/help/docs/cloud-foundation/compute/acp/acpUserGuide/acpCreateJob) · [ACP 高性能网络变量](https://www.sensecore.cn/help/docs/cloud-foundation/compute/acp/acpUserGuide/acpEnvironmentVariable) · [ACP CLI](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/ACP/instances/create)
2. 本项目在 `share-cluster` 同账号 Spot 下验证过 **两个独立 ACP、每个作业两个副本、每副本一张 H100**。两个作业都获配 RDMA，跨作业真实传输为 `NET/IBext_v8/.../GDRDMA`。同池的单副本测试没有拿到可用设备。这个结果适用于当时的作业及规格。跨账号 Reserved 需要两边分别验证设备和互通。 [四卡网络实测](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/h100_dual_node_single_gpu_pair/compare-740043cdabb0/pair-1/summary.json) · [跨账号操作手册](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/reserved_cross_account/操作手册.md)
3. 创建后用作业回执看每个 worker 是否请求了 `rdma/hca`，进容器用 `ibv_devinfo -l` 确认可用设备。以实际跨机 NCCL `all-reduce` 的通道日志验收，`NET/Socket` 表示该通道用 TCP。若缺设备或跨成员训练网不通，请管理员确认可用的训练网、规格、配额及跨成员互通策略。 [NVIDIA 网络诊断](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html)

若组织已经开通 **SSP**，其公开 CLI 提供 `--rdma-name`，配置文件也支持为任务规格填写 `resource_spec.rdma_name`。网络名必须来自该 SSP 队列的可用列表。此处的字段属于 SSP，已验证的 ACP 提交配置见上文。 [SSP 参数参考](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/SSP/jobs/create-params)

## Reserved 与 Spot 两个 ACP 的会合

同账号、同池的双 Spot 测试此前验证了四个 Worker 上的跨作业 `GDRDMA`。该次 all-reduce 的 4 MB、256 MB 和 1 GB 中位耗时分别为 0.213、8.173 和 31.015 ms。另一份同账号、双 Spot 短训在 30 步内测得 89,063 tokens/s，单 ACP 的 IB 对照为 91,082 tokens/s，双作业 Socket 对照为 52,012 tokens/s。各臂物理宿主机存在差异，结果适用于这组短测。 [all-reduce 回执](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/h100_dual_node_single_gpu_pair/compare-740043cdabb0/pair-1/summary.json) · [短训对照](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/hd4g_cross_job_ib_training/compare-03d83c23cac4/pair-3/comparison.json)

混合配额请求仍采用每作业两节点、每节点一张 H100。2026 年 11 月 16 日，Spot 作业 `pt-n4prpyoo` 创建成功，Reserved 创建返回 `MEMBER_QUOTA_EXCEEDED`，请求两卡、44 核，剩余零卡、零核。Spot 随后停止到 `SUSPENDED`。本轮未组成四秩进程组，混合配额的 RDMA 和训练效率均待验证。 [计划](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/h100-mixed-quota-NSPQOWio/plan.md) · [Reserved 拒绝回执](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/h100-mixed-quota-NSPQOWio/compare-8ef8379672ac/pair-1/create-1.log) · [Spot 终态](/data/250010109/MoE_Router/experiments/1115_acp_independent_jobs/h100-mixed-quota-NSPQOWio/compare-8ef8379672ac/pair-1/terminal-0.json)

提交命令、To run、rank/IP 分配与 NCCL 日志判定见 [SCO 跨作业手册](../Projects/sco-control/skills/sco-control-training/references/acp-distributed-cn.md)。

## AOSS 的入口按产品区分

| 运行环境 | 入口 | 当前证据 |
| --- | --- | --- |
| 本项目使用的 ACP | AFS 可用 `sco acp jobs create` 的 `--storage-mount`；AOSS 可通过 ACP 创建 API 配置 `PV_AOSS` | ACP 创建 API 的公开枚举尚未列出 `PV_AOSS`。本项目的实际后端已经接受带桶名及作业级凭证的直挂创建请求。见下文的 ACP 配置和验收记录。 |
| SSP / `sco ssp jobs create` | 对象存储直挂 `PV_AOSS` | 官方支持用参数或 YAML 配置。具体 SSP 队列、桶权限和容器读写需实际核对。 |
| CCI 容器 | 对象存储直挂 `PV_AOSS` / GeeseFS | 新建单卡 5090 Spot 已验证直挂、写入、独立回读及删除。既有 CCI 另有 1 GB 写入、回读和 SHA-256 校验记录。可作为 AFS 和 AOSS 间的归档执行端。 |

[ACP 控制台说明](https://www.sensecore.cn/help/docs/cloud-foundation/compute/acp/acpUserGuide/acpCreateJob) · [ACP 创建 API](https://www.sensecore.cn/help/docs/API/acp/training-job-service-create-training-job) · [SSP 挂载字段](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/SSP/jobs/create-config) · [CCI 挂载字段](https://www.sensecore.cn/help/docs/API/cci/app-service-update-app) · [CCI 存储实测](/data/250010109/MoE_Router/experiments/1115_cluster_probe/1115-集群互联与存储同步可行性_报告.md)

## 用创建 API 给 ACP 直接挂载 AOSS

2026 年 11 月 16 日，`share-space` 的 ACP 创建 API 接收了以下结构。新任务以一张 H100 Spot 提交，同时挂载 AFS 和 AOSS。AOSS 使用 `mount[].name` 指定桶名，私有桶访问凭证放在**作业级** `metadata.items`。在本次实测中，把凭证放在 `mount[]` 内会收到 `AOSS_CREDENTIAL_VALIDATION_FAILED`。成功创建后的查询回执将密钥字段显示为 `encrypted_secret_key`。以下示例省略了任务的镜像、规格和启动命令，密钥由安全输入提供。 [ACP 创建 API](https://www.sensecore.cn/help/docs/API/acp/training-job-service-create-training-job) · [单卡 Spot 创建回执](/data/250010109/MoE_Router/experiments/acp-aoss-direct-zUd29CKb/public-job-items-response.json)

```yaml
mount:
  - type: PV_AFS
    id: <AFS 卷 ID>
    mount_path: /data
  - type: PV_AOSS
    name: <桶名>
    id: <桶名>
    endpoint: https://<AOSS S3 服务端点>
    zone: <桶所在可用区>
    mount_path: /mnt/aoss
metadata:
  items:
    - key: access_key
      value: <获授权的访问密钥 ID>
    - key: secret_key
      value: <受保护的私密密钥输入>
```

### 单卡 ACP Spot 提交实测

北京时间 01:36，任务 `acp-aoss-direct-zud29ckb` 在 `share-cluster` 按一张 H100 Spot 创建成功，平台回执保留 `PV_AFS` 与 `PV_AOSS` 两个挂载条目。提交约 15 分钟后，单个 Worker 仍为 `Pending` 且未分配节点，随后停止到 `SUSPENDED`。本轮验证了 **ACP 接受直挂配置**。容器内挂载、1 GB S3 往返及 AFS 读写性能均待实测。 [创建回执](/data/250010109/MoE_Router/experiments/acp-aoss-direct-zUd29CKb/public-job-items-response.json) · [挂载配置回执](/data/250010109/MoE_Router/experiments/acp-aoss-direct-zUd29CKb/latest-job.json) · [停机前 Worker](/data/250010109/MoE_Router/experiments/acp-aoss-direct-zUd29CKb/worker-before-close.json) · [任务终态](/data/250010109/MoE_Router/experiments/acp-aoss-direct-zUd29CKb/terminal.json)

## 现有 ACP 将文件保存到 AOSS

在 `debug-cluster-5090`，单卡 RTX 5090 Spot ACP 已通过容器内 GeeseFS 原生挂载和 1 GB 读写验收。AFS 写入／读取为 1.19／7.50 秒，AOSS 原生挂载为 30.27／3.31 秒，S3 PUT／GET 为 35.65／35.70 秒。三条路径完整 SHA-256 一致。GeeseFS 刚写完后的读取可能受缓存影响。首轮 S3 请求遇到 DNS 解析失败，重试完成了测速并清理全部对象。 [首次运行](/data/250010109/MoE_Router/experiments/acp-5090-aoss-ufgJhgb3/benchmark.json) · [完整测速](/data/250010109/MoE_Router/experiments/acp-5090-aoss-retry-9zH6Q6dA/benchmark.json) · [清理](/data/250010109/MoE_Router/experiments/acp-5090-aoss-retry-9zH6Q6dA/cleanup-verification.json) · [终态](/data/250010109/MoE_Router/experiments/acp-5090-aoss-retry-9zH6Q6dA/terminal.json)

1. 在 **AOSS → 存储桶列表** 选已有授权的私有桶，或按项目安排创建一个同区域私有桶。查桶的 **域名信息**，获取当前计算环境可访问的 S3 服务 Endpoint。确定桶、归档前缀和访问身份。归档身份需要写入及校验读取权限，恢复身份可以只授予所需对象的读取权限。跨账号按桶和前缀授权，各用自己的身份。 [AOSS 操作手册](https://console.sensecore.cn/micro/help/docs/cloud-foundation/storage/aoss/)
2. 训练期间照常使用项目已验证的文件路径。若 AFS 紧张，先核对作业容器确实有足够的本地盘。把待上传的文件写到该盘，等训练代码关闭并完成写入后上传。节点本地文件可能随任务回收消失。分片存档应保留全部分片、索引及训练状态，先验证对象齐全再作为恢复点。项目已有 CCI 若能同时读 AFS 和桶，可从 CCI 归档已完成文件。大批量迁移可以用 **ADS → 创建数据同步任务 → 选择 AFS 与 AOSS 之间的方向 → 填来源和目标 → 验收同步结果**。 [ADS 操作说明](https://console.sensecore.cn/micro/help/docs/cloud-foundation/storage/ads/)
3. 用 AWS CLI 或 SDK 从获授权的计算环境直接读写桶。镜像需要有相应客户端，并由运行环境提供有权限的凭证。不要把 AK/SK 放在项目文件、To run、命令日志或归档里。先用已知的小文件验证路径和权限，再传正式数据。下面的例子用一个独立的运行前缀存放成品及校验文件。 [SenseCore 的 S3 传输示例](https://www.sensecore.cn/help/docs/model-as-a-service/AI_Studio/User_Guide/AICL/upload_data)

在安装了 AWS CLI、且凭证已由运行环境提供的 Bash 中执行，替换变量值：

```bash
set -euo pipefail
AOSS_ENDPOINT='https://<本区域 S3 服务 Endpoint>'
AOSS_BUCKET='<已授权的桶名>'
RUN_ID='<唯一运行标识>'
OUTPUT_DIR='<已经写完的本地或 AFS 目录>'
ARTIFACT='step_003816.pt'

cd "$OUTPUT_DIR"
AOSS_VERIFY_DIR=$(mktemp -d)
trap 'rm -f -- "$AOSS_VERIFY_DIR/$ARTIFACT.sha256"; rmdir -- "$AOSS_VERIFY_DIR"' EXIT
sha256sum "$ARTIFACT" > "$AOSS_VERIFY_DIR/$ARTIFACT.sha256"
AOSS_DEST="s3://$AOSS_BUCKET/research-archive/$RUN_ID"

aws --endpoint-url "$AOSS_ENDPOINT" s3 cp "$ARTIFACT" "$AOSS_DEST/$ARTIFACT"
remote_size=$(aws --endpoint-url "$AOSS_ENDPOINT" s3api head-object \
  --bucket "$AOSS_BUCKET" --key "research-archive/$RUN_ID/$ARTIFACT" \
  --query ContentLength --output text)
test "$remote_size" = "$(stat -c %s -- "$ARTIFACT")"
aws --endpoint-url "$AOSS_ENDPOINT" s3 cp \
  "$AOSS_VERIFY_DIR/$ARTIFACT.sha256" "$AOSS_DEST/$ARTIFACT.sha256"
```

上传步骤用 `head-object` 校对对象大小，匹配后才上传校验文件。若打开新终端做恢复，先填写上面同一组 `AOSS_ENDPOINT`、`AOSS_DEST` 和 `ARTIFACT`。释放原文件之前，从目标桶下载到空间足够的另一目录并做 SHA-256 校验。保留对象路径、实际大小、SHA-256 和恢复验证记录，按 [资产生命周期](../assets/README.md) 登记需要复用的输出。

```bash
set -euo pipefail
RESTORE_DIR='<空间足够的恢复目录>'
mkdir -p "$RESTORE_DIR"
cd "$RESTORE_DIR"
aws --endpoint-url "$AOSS_ENDPOINT" s3 cp "$AOSS_DEST/$ARTIFACT" "$ARTIFACT"
aws --endpoint-url "$AOSS_ENDPOINT" s3 cp "$AOSS_DEST/$ARTIFACT.sha256" "$ARTIFACT.sha256"
sha256sum -c "$ARTIFACT.sha256"
```

## 在 CCI 直接挂载 AOSS

在 **云容器实例 CCI → 创建应用 → 容器配置 → 高级配置 → 对象存储（GeeseFS 版）** 选择已有授权的桶，填写桶所在可用区、对应 Endpoint 和容器内挂载路径，例如 `/mnt/aoss`。要把训练产物从 AFS 归档到 AOSS，可以同时把 AFS 挂到 `/data`。 [CCI 控制台操作](https://console.sensecore.cn/micro/help/docs/cloud-foundation/compute/cci/)

用 SCO 提交时，在 CCI 应用的 `template.containers[]` 的对应容器下填写以下字段。将模板中的占位符替换为实际值，用 `sco cci apps create <应用名> -w <工作空间> --config <任务配置>` 创建。私有桶的凭证通过控制台填写或由受保护的临时配置提供。项目记录应只保存脱敏模板。 [CCI 创建 API](https://www.sensecore.cn/help/docs/API/cci/app-service-create-app)

```yaml
volume_mounts:
  - type: PV_AOSS
    name: <桶名>
    mount_path: /mnt/aoss
    zone: <桶所在可用区>
    endpoint: <桶对应的 Endpoint>
metadata:
  items:
    - key: access_key
      value: <获授权的访问密钥 ID>
    - key: encrypted_secret_key
      value: <平台接受的 JWE 加密值>
```

容器启动后用 `findmnt -T /mnt/aoss -o TARGET,SOURCE,FSTYPE` 确认目标目录和 `fuse.geesefs`。在独立的测试路径写入并关闭小文件，从另一个挂载或 S3 客户端回读并核对 SHA-256，再删除测试文件。CLI 可用 `sco cci apps stop <应用名> -w <工作空间>` 停止探针，并用 `describe` 确认就绪副本数为 0。

### 单卡 Spot 挂载验收记录

2026 年 11 月 16 日北京时间 01:14 提交 CCI 应用 `aoss-mount-spot-nwpqxpj2`。工作空间为 `share-space`，资源池为 `debug-cluster-5090`，规格为 `n12lp.nn.i10a.1`，一个 Spot 副本，容器实见一张 NVIDIA GeForce RTX 5090。 [提交回执](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/submission.json)

| 验收项 | 实测结果 |
| --- | --- |
| 直挂 | `shphd-bucket` 以 `PV_AOSS` 挂到 `/mnt/aoss-probe`，容器实见 `fuse.geesefs`。 [容器回执](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/worker.json) |
| 写入与回读 | 创建并关闭一个 65,536 字节对象。新挂载回读、原容器 `/mnt/bucket` 的独立回读、S3 HTTPS GET 的 SHA-256 均一致。新应用沿用同一访问身份的平台加密配置，独立 S3 读取使用本次提供的凭证。 [原容器回执](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/independent.json) · [S3 回执](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/s3-object.json) |
| 清理 | 删除测试对象后，S3 HEAD 返回 HTTP 404。北京时间 01:22 实例为 `SUSPENDED`，就绪副本数为 0。 [对象清理](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/s3-cleanup.json) · [实例终态](/data/250010109/MoE_Router/experiments/aoss-mount-spot-nwpQXpJ2/terminal.json) |

本次验收覆盖 CCI 的小文件挂载读写。ACP 直挂和训练 checkpoint 的吞吐仍待实测。

## 有 SSP 权限时直接挂载 AOSS

在已可提交的 SSP 配置中，向 `spec.volume_mounts` 添加下面的条目。若已挂 AFS 到 `/data`，AOSS 可挂到并列的 `/mnt/aoss`。SSP 的挂载点不能相同或互为父子目录。桶名和 Endpoint 从 AOSS 控制台取值。当前 SSP 公开参数的 `subdir` 只支持一级前缀，省略则使用桶根路径。

```yaml
spec:
  volume_mounts:
    - type: PV_AOSS
      name: <bucket>
      endpoint: https://<endpoint>
      mount_path: /mnt/aoss
      subdir: /research-archive
      metadata:
        access_key: <由运行身份提供的 AK>
        secret_key: <由运行身份提供的 SK>
```

凭证字段按私有桶的鉴权配置填写。含密钥的临时提交配置留在有访问保护的目录，仅保留脱敏模板。SSP 配置提交入口为 `sco ssp jobs create --config <本地任务 YAML> -w <SSP 工作空间>`。参数化方式使用 `--volume-mount 'PV_AOSS:<bucket>:/mnt/aoss:https://<endpoint>:/research-archive'`，所需凭证参数见官方文档。切换到 SSP 前，先确认目标工作空间、队列、资源规格和授权。 [SSP YAML 创建](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/SSP/jobs/create-config) · [SSP 参数化创建](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/SSP/jobs/create-params)

启动后用 `findmnt -T /mnt/aoss -o TARGET,FSTYPE` 核对容器挂载点。在获准的专用前缀做小文件写入、关闭和回读，并从 AOSS 控制台或 S3 客户端确认对象及哈希。只读挂载验证读取即可。用于长期归档时，优先保存已关闭的成品文件。会合信号、文件锁和频繁重写的断点文件继续使用已验证符合所需文件语义的路径。
