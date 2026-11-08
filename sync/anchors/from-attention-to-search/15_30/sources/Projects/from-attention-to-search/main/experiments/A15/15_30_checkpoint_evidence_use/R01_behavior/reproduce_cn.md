# 重放与交付位置

完整执行根为 `/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use`。原始checkpoint保持原路径；代码、配置、文本、分数、表、图与每状态receipt均在该执行根。[英文命令与字段](reproduce.md)逐一给出。不要在原冻结输出上重建数据或重跑已完成状态；脚本拒绝覆盖。重放应复制到独立输出根并核对hash，继续遵守Protocol资产、smoke和预算条件。

本轮系统PyTorch2.3.0、现有H100MIG切片，构造时使用已有隔离tokenizers依赖，无下载或新作业。全部实际命令保存在原日志和Protocol；A01只修正耗时估计公式。原始分数能按样本id连接全文与token位置。PDF/SVG导出留执行侧，项目仅选入主PNG和图源小表，并登记来源hash。
