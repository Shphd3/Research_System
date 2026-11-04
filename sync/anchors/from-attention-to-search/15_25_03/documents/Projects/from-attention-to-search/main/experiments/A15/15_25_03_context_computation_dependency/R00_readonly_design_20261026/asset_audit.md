派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/asset_audit.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/asset_audit.md)；研究修改仍回到原件。

---

# Asset and measurement audit

Current strict selected input access passes; small config/source/text manifests are freshly hashed. Large Base/coder weights are stat-checked against saved metadata, not rehashed/deserialized. The selected assets are the user's known Base/A22dictionary and original Tulu/DCLM records; no external person's model was searched.

Joint z is not layer-local. Raw source14activation is absent from Tulu cache; raw target28and z exist. Historical geometry/CE does not qualify the current directional readout. Current model/native hook replay is NOT RUN. EVAL is previously exposed, document IDs/prompt hashes are available, near-duplicate independence unknown.

Feasible alternative: nuisance-residualized decoder direction on actual downstream activation, qualified as a score rather than an independent feature. If qualification fails, report prediction-only effects without C→R localization, or declare the independent-local-encoder gap. No new SAE/CrossCoder is trained. Current navigation check found7pre-existing unrelated UNTRACKED paths; these are not scientific or selected-access failures.

See [Chinese details](asset_audit_cn.md) and exact metadata/checks in `provenance/`.
