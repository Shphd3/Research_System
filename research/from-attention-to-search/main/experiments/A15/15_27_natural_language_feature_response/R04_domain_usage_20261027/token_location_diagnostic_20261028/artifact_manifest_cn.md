# 探索性诊断交付证据

执行目录：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/diagnostic_20261028`。登记ID：`analysis_a15_27_r04_token_location_diagnostic_20261028`；这是原R04任务内的离线结果，不是新Work/Codex任务。

- 一页解释、完整证据、固定图注与事前解读规则均在本目录。
- `tables/`包含旧四组核对、DCLM频率、三处覆盖、两套各32候选的逐项支持表。
- 原始非零命中、含零的图示矩阵、token区域/术语注释、每前缀支持、代码和源文件hash在执行侧及诊断zip。
- 原zip hash未变；241项独立CSR/86输入hash/预算审计通过，原R04报告的文件hash均未变。
- 用时、1小时截止与任务覆盖见`provenance/delivery_checks.json`。新增前向0、拟合0、任务0、Attention0。缺缓存0；独立改写、语义/词面/位置因果分离及功能重要性未测。

所有新解释均为探索性，不能当作原留出确认。两套不同hook的贡献不能用于判架构优劣；最后层decoder贡献不叫功能重要性。
