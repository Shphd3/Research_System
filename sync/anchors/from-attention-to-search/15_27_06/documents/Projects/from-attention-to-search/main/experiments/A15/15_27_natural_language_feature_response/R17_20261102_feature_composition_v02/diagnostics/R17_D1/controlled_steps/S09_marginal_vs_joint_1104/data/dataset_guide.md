派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/data/dataset_guide.md`。
[精确原始文件](../../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/data/dataset_guide.md)；研究修改仍回到原件。

---

# S09 inputs retained from S08

Same original771question texts and8main positions, no re-sampling. Source raw questions/native sparse arrays portable under inputs; source SHA256 unchanged. NuminaMISSING as in S08bounded audit. New internal document split is128/129per source, frozen prior to joint candidate selection. Model weights not required or included. Full source revisions/fields/hashes:

```json
{
  "Magicoder": {
    "asset": "hf_prepared_ise_uiuc_magicoder_oss_instruct_75_k",
    "repo": "ise-uiuc/Magicoder-OSS-Instruct-75K",
    "revision": "5f839b1f368a76b161028bb9edff055db34022b2",
    "field": "problem",
    "split": "train",
    "file": "/data/share/109_cache_dir/hf_data/datasets/ise-uiuc___magicoder-oss-instruct-75_k/default/0.0.0/5f839b1f368a76b161028bb9edff055db34022b2/magicoder-oss-instruct-75_k-train.arrow",
    "sha256": "d4724bb2a38cb74105dc9034f08117fa60e9de82286a0e6ae32f30b4a3970611"
  },
  "GSM8K": {
    "asset": "hf_prepared_gsm8k",
    "repo": "gsm8k",
    "revision": "e53f048856ff4f594e959d75785d2c2d37b678ee",
    "field": "question",
    "split": "train",
    "file": "/data/share/109_cache_dir/hf_data/datasets/gsm8k/main/0.0.0/e53f048856ff4f594e959d75785d2c2d37b678ee/gsm8k-train.arrow",
    "sha256": "6146bca074f4c6c5e07de7e96cc968adab3833dbdafeda21830f27558eea3d9b"
  },
  "MMLU": {
    "asset": "hf_prepared_cais_mmlu",
    "repo": "cais/mmlu",
    "revision": "c30699e8356da336a370243923dbaf21066bb9fe",
    "field": "question",
    "split": "test",
    "file": "/data/share/109_cache_dir/hf_data/datasets/cais___mmlu/all/0.0.0/c30699e8356da336a370243923dbaf21066bb9fe/mmlu-test.arrow",
    "sha256": "58769d67ced092719390e496f1d4bbf8b99c43b77bba39d054b9a09aecb63cab"
  }
}
```
