# 在 ACP 和 CCI 使用 AOSS

AOSS 是对象存储服务。原生挂载将桶映射为容器内的 GeeseFS 文件路径，S3 API 则按对象键上传和回读。对比两条路径的速度时，应注明走的是原生挂载写入还是 S3 PUT。

## 多账号训练指定主账号的 AOSS

多个账号参与同一批训练时，先指定一个**主账号**和它的 **AOSS 桶**，由主账号管理共享对象、日志及 checkpoint 归档。各参与账号用自己的 SCO profile 提交 ACP、使用自己的配额。为每次运行记录下面四项，凭据通过单独的安全输入提供。

| 配置项 | 填什么 |
| --- | --- |
| `AOSS_OWNER_PROFILE` | 管理共享桶和发布运行清单的主账号 profile |
| `AOSS_BUCKET` | 主账号选定的桶名 |
| `AOSS_ENDPOINT` | 该桶的 S3 服务端点，从所有参与 Worker 验证可达 |
| `AOSS_RUN_PREFIX` | 本次运行独有的对象前缀，例如 `training/<project>/<run-id>` |

1. **先分清挂载。** `/data` 是 AFS 挂载，账号项目目录通常在 `/data/<账号目录>`。AOSS 用桶名、端点和对象前缀定位，容器内直挂路径由作业单独指定。训练输入优先从已授权的 AFS 路径读，跨账号通过实际 Worker 确认读权限。
2. **让各账号接入主桶。** 授权参与 Worker 读取这次运行所需的清单或输入，只给负责上传的进程写入对应对象或前缀的权限。也可以由主账号为明确的对象签发短期预签名 URL。使用原生挂载时，提交前单独核对桶访问权限和作业挂载配置。用每个账号的实际 Worker 读回同一个测试对象，需写入的角色再做独立对象的上传回读。
3. **共享会合信息。** 两个 ACP 组成同一个分布式训练组时，共用一个 `AOSS_RUN_PREFIX`。由主账号发布完整的 `rendezvous.json`（Pod IP、端口、rank），参与作业在各自的就绪对象键回执，主账号验证齐全后发布起跑信号。训练进程按清单会合，梯度同步走 NCCL。并行跑多个独立模型时，各模型使用不同的前缀。
4. **归集结果。** 指定一个全局日志写入者记录汇总 loss。主账号负责归档完整 checkpoint，经常保存时可先写 AFS，再异步归档到该运行的 AOSS 前缀。对分片 checkpoint，所有分片写完校验后再发布完成标记，供恢复时选用。

## ACP 创建 API

一项单卡 Spot 作业的实际 API 回执接受了以下结构。公开 ACP 文档的挂载枚举未同步这一项。已验证的凭证位置是**作业级** `metadata.items`。本地 ACP CLI 的 `--storage-mount` 使用 AFS 卷 ID，该参数不能表达此 AOSS 请求。请求还需包含作业名、调度、规格、镜像和启动脚本等字段。 [ACP 创建 API](https://www.sensecore.cn/help/docs/API/acp/training-job-service-create-training-job)

```yaml
mount:
  - type: PV_AFS
    id: <AFS 卷 ID>
    mount_path: /data
  - type: PV_AOSS
    name: <桶名>
    id: <桶名>
    mount_path: /mnt/aoss
    zone: <桶可用区>
    endpoint: https://<S3 服务端点>
metadata:
  items:
    - key: access_key
      value: <由安全输入提供>
    - key: secret_key
      value: <由安全输入提供>
```

用保护的输入在进程内组装请求。避免将密钥放入 To run、版本库或日志。提交后查询配置确认有 `PV_AOSS`，等 Worker 真正启动再运行 `findmnt -T /mnt/aoss -o TARGET,SOURCE,FSTYPE`。实际目标应为 `/mnt/aoss`，GeeseFS 的文件系统类型为 `fuse.geesefs`。最后在专用对象键写入并回读校验。API 接收配置、容器挂载成功、实际读写通过是三个验收步骤。

## CCI

控制台路径为 **CCI → 创建应用 → 容器配置 → 高级配置 → 对象存储（GeeseFS 版）**。通过 YAML 提交时，将同类 AOSS 卷字段放在 `template.containers[].volume_mounts`，将凭证的 `metadata.items` 放在同一个容器条目下。平台支持 JWE 格式的 `encrypted_secret_key`。AFS 可同时挂载在 `/data`。 [CCI 创建 API](https://www.sensecore.cn/help/docs/API/cci/app-service-create-app)

## 用一个 1 GB 文件对照写入

1. 在同一 Worker 的本地盘或容量足够的 tmpfs 生成一份 1,000,000,000 字节文件，计算 SHA-256。
2. 记录从同一本地文件写到 AFS、关闭并 `fsync` 的时间。记录 S3 PUT 到返回成功的时间。若另测原生挂载，使用另一个唯一对象键并单列该时间。上传端和下载端可用限定到测试对象键的短期预签名 URL。
3. 两条路径读取到同一个本地暂存介质，再核对字节数与 SHA-256。将哈希计算时间单列。AFS 读取可能受缓存影响，应注明读取条件。删除独立测试文件及对象并验证对象不存在。
4. 对 checkpoint 的判断还需要真实 checkpoint 大小、分片数、保存频率和恢复用时。一次 1 GB 文件测速可用于估算归档延迟。同步写入是否挡住训练，应使用实际 checkpoint 保存流程验证。

## 单卡 RTX 5090 Spot 实测

2026 年 11 月 16 日在 `debug-cluster-5090` 的一个 ACP Worker 上，用同一份 1 GB 文件测得以下耗时。AFS 和 GeeseFS 写入包括 `fsync`，S3 PUT 等待 HTTP 200。三条路径均回读并通过 SHA-256，校验时间单列，不计入表中。

| 路径 | 写入 | 回读 |
| --- | ---: | ---: |
| AFS | 1.19 s | 7.50 s |
| AOSS GeeseFS 直挂 | 30.27 s | 3.31 s |
| AOSS S3 API | 35.65 s | 35.70 s |

这是单 Worker 和单文件的观察值。GeeseFS 回读的是刚写完的对象，可能受缓存影响。首轮 S3 上传曾遇到 DNS 解析失败，表中是下一轮同机配对后成功的结果。频繁的训练 checkpoint 可先写 AFS，再将已完成的 checkpoint 异步归档到 AOSS。按实际 checkpoint 的大小和保存频率另外测归档与恢复时间。
