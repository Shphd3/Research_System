派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/dataset_guide_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/dataset_guide_cn.md)；研究修改仍回到原件。

---

# A15_24_01 数据身份与评价口径

[English](dataset_guide.md) · [结果](summary_cn.md) · [过程与证据](../../../../../../../../UNAVAILABLE.md)

本轮复用原频率路由实验的 Tulu SFT 数据与冻结 Qwen3-0.6B 第 28 块 residual-post 缓存。沿用原数据划分、feature 名单与 CrossCoder；训练对象为残差适配器中的路由专家和 common 分支，缓存输入、末层归一化和预测 head 均保持冻结。

| 数据划分 | 对话数 | 有效回答目标数 | 输入 JSON 的 SHA256 |
|---|---:|---:|---|
| train | 1024 | 85548 | `5530f9676c3d7941150e404c045ad62815a11310d8b1ec4904c209121ddb8ad5` |
| eval | 256 | 22446 | `63a31b625a8b55c709c777d50f12db44fa8ca05d6b611f8a1d2998485d320962` |
| dev | 128 | 10340 | `56d6f03425dafffe7b5345e472a4e3d7c932a5914761d6867ef9791e07ac5b0a` |

目标只包含回答内容，恰好移位一次；检查未发现 prompt 或 padding 目标。三个划分之间的归一化 prompt 重复为零。近重复独立性以及与 Base 预训练的重叠为 Unknown。DEV 在此前工作中已经暴露，本轮按探索性评价处理，没有新确认集。

每个训练模型恰好消费 85,548 个目标一次：前 167 步各 512 个目标，末步 44 个。四个模型全部完成后，统一评价预先固定的第 168 步 DEV，不按结果选择 checkpoint。

TRAIN 定义的低频名单包含 1,694 个 CrossCoder feature。DEV 中 838 个至少有一个激活位置，另 856 个无支持并保留 NA；没有低频 feature 的支持达到 20 个位置。其并集覆盖 10,340 个目标中的 1,701 个不重复位置。feature 宏平均先计算每个有支持 feature 的位置平均损失，再对 838 个 feature 等权平均；位置并集平均对每个覆盖位置只计一次。同一对话和交叠 feature 的观测不应当作统计独立样本。

已登记的输入身份：

- `data_tulu_sft_route_20261019t012300z`
- `representation_tulu_sft_route_20261019t012300z`
- `model_qwen3_0p6b_base`
- `tokenizer_qwen3_0p6b_base`
- `analysis_crosscoder_frequency_composition_common_path_20261019t164834z`

本轮实际访问与标签检查见[输入回执](../../../../../../../../UNAVAILABLE.md)、[工程资格检查](../../../../../../../../UNAVAILABLE.md)与[独立复算](../../../../../../../../UNAVAILABLE.md)。原始文本、激活和检查点保留在执行存储；上表的哈希锁定输入 JSON 身份，不在阅读包中分发这些载荷。
