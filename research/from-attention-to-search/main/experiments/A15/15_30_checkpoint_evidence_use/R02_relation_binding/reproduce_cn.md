# 完成后如何复查

本轮已完成，无需继续推理或训练。以下只在CPU读取保留的原分数，重建统计和图，并校验冻结、标签、距离、分数算术与R01原字节；只写R02分析产物，不加载底模。

```bash
cd /data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/code
python analyze.py
python verify.py
```

common.py管理路径、hash与R01保护快照；audit_inputs.py复算R01并选择精确状态；prepare.py生成冻结面板与标签／token校验；run.py只读适配R01原生加载器，禁止写入其cache，新增FP32评分和greedy生成，smoke／full都已完成。analyze.py输出全部家族、配对统计和实测图；verify.py重放检查。report.py及finish_docs.py仅写阅读材料，report.py还登记精选图载荷，不是需要重复执行的推理命令。第一条新分数前冻结的代码／数据／协议hash与事后分析／报告文件分开记录。

不要重跑audit_inputs.py覆盖事前保护快照，也不要重新prepare覆盖冻结数据。未来独立重复应由研究者决定，在新输出位置冻结并重新核查输入，不覆盖本轮或R01；现在没有启动。

验证通过六状态、576绑定及576旧参照、全部世界翻转／标签／距离、冻结计划与模型数值校准；308条可直接对齐的生成首token概率最大误差1.69e-5nat。所有R01非cache字节及文件集合一致。它是工程复核，不是独立科学复现。[Detailed](detailed_cn.md)保留成本、边界与NOT RUN；[来源manifest](artifact_manifest.json)链接全部执行代码／配置／文本／分数／receipt／表图hash；[R01事前快照](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use_r02_relation_binding/audit/r01_before.json)。
