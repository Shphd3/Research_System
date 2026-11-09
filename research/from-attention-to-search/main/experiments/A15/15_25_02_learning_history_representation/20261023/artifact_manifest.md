# Artifact and reproduction map

Research question: How does learning history change conditional-rule representations, and which directions matter most for answering?

[Summary](summary.md) owns the first result reading; [Detailed](detailed.md) owns conformance and evidence eligibility. Exact files are below; weights and arrays remain execution-side. All four cache hashes are unchanged. Registered asset: `representation_a15_25_02_learning_history_20261023`.

| Artifact | Exact location | SHA256 | Complete / use |
|---|---|---|---|
| Frozen protocol | [protocol.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol.md) | `1772547e999dc40c884aa00d83a1ad9a453c621a1232651316fd251e117bbdf8` | PRESENT; boundary in Detailed |
| Frozen Chinese protocol | [protocol_cn.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol_cn.md) | `c00201fe1265803a41aee9a30458b540ae6cc5065526f55afd60fd6666c36688` | PRESENT; boundary in Detailed |
| Configuration | [config/frozen.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/config/frozen.json) | `8065911de53e1c124044133fd0478c88d5bf472b810aec6358efd66bc9c9cf67` | PRESENT; boundary in Detailed |
| Pre-full hashes | [config/full_frozen_manifest.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/config/full_frozen_manifest.json) | `a787f90b3727979ab5822c931ad7b8380db951b33b6d7a8727b8797b0de7bb98` | PRESENT; boundary in Detailed |
| Final repair hashes | [config/analysis_resume2_manifest.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/config/analysis_resume2_manifest.json) | `02edc52810ea902e4dd509368a4e8a5d4149c87f378cf84b710e7885ea65f60a` | PRESENT; boundary in Detailed |
| Exact extraction source | [source_versions/extraction_v1/run.py](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/source_versions/extraction_v1/run.py) | `0e2c4e93581c977726d76d13efdb82d3757271cbd68d8f8743da66b1280ebc78` | PRESENT; boundary in Detailed |
| Final analysis source | [code/analyze.py](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/code/analyze.py) | `7f1b7a4ae56dceaf496c62c6a53e26f5810d7bf1164d08b08282f9235d233626` | PRESENT; boundary in Detailed |
| Analysis resume entry | [code/resume_analysis.py](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/code/resume_analysis.py) | `1d4e037ac5e80bbddb82d0bdb94f72914541434a6eb9ac9d53406b9fc1d30d6f` | PRESENT; boundary in Detailed |
| Input sample manifest | [data/examples.jsonl](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/data/examples.jsonl) | `78295c96823eddaa361f14b74bb7a9a35519f880847b733af761b56d021eecfe` | PRESENT; boundary in Detailed |
| Extraction receipt | [full/extraction_receipt.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/extraction_receipt.json) | `1bdd5a4abd66399bd02d1f74d948f40d3e4acc810c99e2f89eadd5ba65aac59b` | PRESENT; boundary in Detailed |
| Completion receipt | [full/complete.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/complete.json) | `036d7ac6f0c9040624cf48e9b86328b17f5e54ce5a8be6dfa707880a97f86401` | PRESENT; boundary in Detailed |
| Primary contrasts | [full/primary_results.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/primary_results.json) | `68c946cb7ed56e2e40f5548013b885e85ac3d0a7a1cc6908ca7ddfc7e3406bcc` | PRESENT; boundary in Detailed |
| Selection manifest | [full/selection_frozen.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/selection_frozen.json) | `14a2ec1bb2b302a154ade257c9999c8bd03d3238e7888caf9c6a3caecc12124b` | PRESENT; boundary in Detailed |
| All per-example interventions | [full/interventions.pt](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/interventions.pt) | `7a2355e4f733deecd3871a4f58fd7824fe67449a582cb62ba20ba7c5e38179b2` | PRESENT; boundary in Detailed |
| Independent audit | [full/independent_audit.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/independent_audit.json) | `4a5c5e998a89816773f4108e0b9adbde9935ccfbb19aff084873cb4fc6f829f3` | PRESENT; boundary in Detailed |
| Figure provenance | [full/figures/manifest.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/figures/manifest.json) | `510727c2cc49550c87e1864052d7ed1b349a52c9cb2a8d004a2e51b5c6347ee0` | PRESENT; boundary in Detailed |
| Actual cache registration | [full/cache_asset_manifest.json](/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/full/cache_asset_manifest.json) | `1657fe6d841dcb20f2144d76335b8ffce6fbc1cb063d8aea16dd30a50e96f194` | PRESENT; boundary in Detailed |

## Actual commands and logs

Extraction invocation: `bash /data/250010109/MoE_Router/experiments/20261023_learning_history_representation/run.sh full`. Successful analysis resumption: `bash /data/250010109/MoE_Router/experiments/20261023_learning_history_representation/resume_analysis.sh`. These record actual calls. The scripts refuse to overwrite completed outputs; reproduction requires a fresh output directory with the same frozen inputs.

- `pt-d40a98vs`: extraction PASS, analysis entry FAILED.
- `pt-5wd8maxg`: FAILED at deterministic spectrum accumulation, before full intervention results.
- `pt-mpgpsupe`: platform SUCCEEDED and artifacts COMPLETE.

Receipts remain under `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/receipts`; durable logs under `/data/250010109/MoE_Router/experiments/20261023_learning_history_representation/acp_receipts/pod`. Original versions and failed artifacts are retained. See [amendments](amendments.md).

## Selected reading copies

Only four measured figures and small provenance are retained here; see [payload manifest](payload_manifest.json). Markdown includes metrics, sixteen fixed cards plus one failure, and all 253 conditions, without requiring checkpoint access. The local generated reading package preserves the same scientific owner.
