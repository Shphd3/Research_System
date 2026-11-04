派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/amendments_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/amendments_cn.md)；研究修改仍回到原件。

---

# 工程偏差与分析续接

科学 Protocol v1 不变。2026-10-23 首次 create 因 ACP 客户端无法解析新增 workspace 字段 `service_time_expression` 而失败，未创建任务。同名任务查询为空后，通过规范提交模板调用 A17 已验证的隔离兼容入口；资源、镜像和命令范围不变。

任务 `pt-d40a98vs` 完成四状态提取，各 1,600 条。原生回放、零修改、完整向量、解析梯度检查通过，此前选定层逐值相同；提取回执记录耗时 77.537657 秒。随后在完整分析任何条件开始前失败：脚本入口中的 `from run import ...` 误解析为复用 A17 目录下的同名文件。本地对照 smoke 先按模块导入本实验 runtime，因此没有覆盖这一入口差异。续接前已核实原任务平台状态为 FAILED。

修复只把本实验 runtime 绑定为唯一名字 `history_runtime`。精确脚本入口导入测试通过；将该一行导入还原后，分析代码 SHA256 与冻结版本逐字节相同。未改选择、估计、对照、阈值、数据、精度或科学判断。保留所有缓存及失败日志。另一个同资源任务只续接分析：重载冻结输出头和字典，校验提取/配置/数据身份及缓存前后 hash，再写剩余产物。续接超时为 3,000 秒，提取加续接计算不超过原 3,600 秒上限。后续绘图不反馈特征选择。

指定修复时，完整分析结果仍不存在。为核对提取完成，已查看总体行为和重建资格；它们没有改变分析计划。研究者科学判断仍为 Unknown。

## A2：确定性谱累计

分析任务 `pt-5wd8maxg` 完成发现选择后，在干预开始前停止：Torch 2.3 的 CUDA 累积求和不支持严格确定性。本地对照启动器此前漏开该设置。失败尝试的选择及基保存在 `full/attempts/analysis1_before_deterministic_fix/`。只将少量奇异值能量的累积求和移到 CPU，公式、原始 SVD 和严格确定性不变。使用严格确定性重新跑完 253 条件工程流程，通过后再同资源续接。缓存不变；最终候选 ID 和随机对照集合须与首次完整发现选择一致。指定修复时尚无完整干预结果。
