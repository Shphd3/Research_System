派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/artifact_manifest_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/artifact_manifest_cn.md)；研究修改仍回到原件。

---

# 产物与复现追踪

研究问题：学习经历如何改变条件规则的表征，以及哪些方向对任务作答最重要？

可读结论由 [Summary](summary_cn.md) 持有；完整契约对照由 [Detailed](detailed_cn.md) 持有。以下是实际文件身份，原始权重和数组仍归执行目录。全部四缓存通过前后 hash 检查，资产 ID 为 `representation_a15_25_02_learning_history_20261023`。

| Artifact | Exact location | SHA256 | Complete / use |
|---|---|---|---|
| Frozen protocol | [protocol.md](protocol.md) | `1772547e999dc40c884aa00d83a1ad9a453c621a1232651316fd251e117bbdf8` | PRESENT; boundary in Detailed |
| Frozen Chinese protocol | [protocol_cn.md](protocol_cn.md) | `c00201fe1265803a41aee9a30458b540ae6cc5065526f55afd60fd6666c36688` | PRESENT; boundary in Detailed |
| Configuration | [config/frozen.json](../../../../../../../../UNAVAILABLE.md) | `8065911de53e1c124044133fd0478c88d5bf472b810aec6358efd66bc9c9cf67` | PRESENT; boundary in Detailed |
| Pre-full hashes | [config/full_frozen_manifest.json](../../../../../../../../UNAVAILABLE.md) | `a787f90b3727979ab5822c931ad7b8380db951b33b6d7a8727b8797b0de7bb98` | PRESENT; boundary in Detailed |
| Final repair hashes | [config/analysis_resume2_manifest.json](../../../../../../../../UNAVAILABLE.md) | `02edc52810ea902e4dd509368a4e8a5d4149c87f378cf84b710e7885ea65f60a` | PRESENT; boundary in Detailed |
| Exact extraction source | [source_versions/extraction_v1/run.py](../../../../../../../../UNAVAILABLE.md) | `0e2c4e93581c977726d76d13efdb82d3757271cbd68d8f8743da66b1280ebc78` | PRESENT; boundary in Detailed |
| Final analysis source | [code/analyze.py](../../../../../../../../UNAVAILABLE.md) | `7f1b7a4ae56dceaf496c62c6a53e26f5810d7bf1164d08b08282f9235d233626` | PRESENT; boundary in Detailed |
| Analysis resume entry | [code/resume_analysis.py](../../../../../../../../UNAVAILABLE.md) | `1d4e037ac5e80bbddb82d0bdb94f72914541434a6eb9ac9d53406b9fc1d30d6f` | PRESENT; boundary in Detailed |
| Input sample manifest | [data/examples.jsonl](../../../../../../../../UNAVAILABLE.md) | `78295c96823eddaa361f14b74bb7a9a35519f880847b733af761b56d021eecfe` | PRESENT; boundary in Detailed |
| Extraction receipt | [full/extraction_receipt.json](../../../../../../../../UNAVAILABLE.md) | `1bdd5a4abd66399bd02d1f74d948f40d3e4acc810c99e2f89eadd5ba65aac59b` | PRESENT; boundary in Detailed |
| Completion receipt | [full/complete.json](../../../../../../../../UNAVAILABLE.md) | `036d7ac6f0c9040624cf48e9b86328b17f5e54ce5a8be6dfa707880a97f86401` | PRESENT; boundary in Detailed |
| Primary contrasts | [full/primary_results.json](../../../../../../../../UNAVAILABLE.md) | `68c946cb7ed56e2e40f5548013b885e85ac3d0a7a1cc6908ca7ddfc7e3406bcc` | PRESENT; boundary in Detailed |
| Selection manifest | [full/selection_frozen.json](../../../../../../../../UNAVAILABLE.md) | `14a2ec1bb2b302a154ade257c9999c8bd03d3238e7888caf9c6a3caecc12124b` | PRESENT; boundary in Detailed |
| All per-example interventions | [full/interventions.pt](../../../../../../../../UNAVAILABLE.md) | `7a2355e4f733deecd3871a4f58fd7824fe67449a582cb62ba20ba7c5e38179b2` | PRESENT; boundary in Detailed |
| Independent audit | [full/independent_audit.json](../../../../../../../../UNAVAILABLE.md) | `4a5c5e998a89816773f4108e0b9adbde9935ccfbb19aff084873cb4fc6f829f3` | PRESENT; boundary in Detailed |
| Figure provenance | [full/figures/manifest.json](../../../../../../../../UNAVAILABLE.md) | `510727c2cc49550c87e1864052d7ed1b349a52c9cb2a8d004a2e51b5c6347ee0` | PRESENT; boundary in Detailed |
| Actual cache registration | [full/cache_asset_manifest.json](../../../../../../../../UNAVAILABLE.md) | `1657fe6d841dcb20f2144d76335b8ffce6fbc1cb063d8aea16dd30a50e96f194` | PRESENT; boundary in Detailed |

## 实际执行命令与日志

原提取命令为 `bash /data/250010109/MoE_Router/experiments/20261023_learning_history_representation/run.sh full`；末次成功续接为 `bash /data/250010109/MoE_Router/experiments/20261023_learning_history_representation/resume_analysis.sh`。这是实际调用记录；脚本会拒绝覆盖现有结果，重现需新输出目录并保持相同冻结输入。

- 提取任务 `pt-d40a98vs`：提取 PASS，分析入口 FAILED。
- 首次续接 `pt-5wd8maxg`：严格确定性谱累计处 FAILED，未产生完整干预结果。
- 最终续接 `pt-mpgpsupe`：平台 SUCCEEDED，产物 COMPLETE。

提交回执位于 `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/receipts`；持久日志位于 `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/acp_receipts/pod`。工程旧版本与失败产物保留；细节见 [偏差](amendments_cn.md)。

## 选定阅读副本

本目录只保留四张实测图及小 provenance，见 [payload_manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/payload_manifest.json)。原生/重建指标、16 固定样例和一失败例、完整 253 条件表均可在 Markdown 内阅读，不依赖检查点。本地同步的只读阅读包保持同一科学归属。
