# 在 ACP 和 CCI 使用 AOSS

AOSS 是对象存储服务。原生挂载将桶映射为容器内的 GeeseFS 文件路径，S3 API 则按对象键上传和回读。对比两条路径的速度时，应注明走的是原生挂载写入还是 S3 PUT。

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
