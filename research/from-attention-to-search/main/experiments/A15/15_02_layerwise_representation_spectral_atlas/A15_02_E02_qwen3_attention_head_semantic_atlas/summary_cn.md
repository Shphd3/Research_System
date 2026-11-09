# A15_02_E02 修正结果摘要：Qwen3-8B 单注意力头的粗细语义区分画像

> 2026-08-05 修正：旧分析在选择模板子集时混用了 NumPy 基本索引与高级索引，模板轴在 reshape 前被移到首维，打乱了父类与模板的层级顺序。修正为沿模板轴显式 `take` 并加入轴顺序回归测试后，本页及配套表图取代旧结果。

## 结论

修正后的正式裁定为 **`attention_depth_pass_head_localization_pass_spectral_fail`**：

- **Attention 深度效应 Pass：**32 个 `o_proj` 前注意力头拼接后的全宽输出，细粒度语义相对粗粒度语义的区分优势从早层到晚层显著增加。
- **单头定位 Pass：**9 个晚层 layer-head 单元通过覆盖 352 个候选单元的全局置换最大值校正。
- **单头固定频带 Fail：**合格单头的 16 带审计中，没有任何频带同时超过配对不确定性、基底稳定性和同头随机 8 维方向 q95。

因此：

> Qwen3-8B 的晚层 attention 在 `o_proj` 之前已经形成细粒度相对区分信号，并存在经过全局选择校正的突出单头；但没有证据把该信号概括为某个固定 head/middle/tail 频带。

## 指标与数据

直接捕获每个 block 的 `self_attn.o_proj` 输入并重排为 32×128。数据复用 E01 的 8 粗类×8 细类×4 模板×2 事实组，共 512 条文本；自然 covariance 来自独立 DCLM 128 文档、65,536 token。

\[
D=\frac{\text{类别间方差}}{\text{类别内模板/措辞方差}},
\qquad
R=\log(D_{fine}/D_{coarse}).
\]

\(R>0\) 表示细类相对更容易区分，不表示细类具有更大的绝对激活，也不证明 attention 头被模型因果使用。

## 决定性结果

全宽 pre-`o_proj` attention 的早晚差分为

\[
T_{attention}=0.6106,
\qquad 95\%\ \text{basic-bootstrap interval}=[0.6039,1.2096].
\]

四个模板与八次父类留一全部同向。

全局晚层 layer-head 置换 q95 为 1.746。9 个合格单元为：L30H27、L30H5、L32H15、L31H8、L30H25、L33H10、L32H20、L31H11、L34H14；最强 L30H27 的 \(R=2.425\)，即细/粗区分度比约 11.30。

![层×单头区分画像](figures/figure1_layer_head_discriminability_atlas.png)

![全局选择校正后的单头](figures/figure2_head_localization_and_global_null.png)

合格单头各自拟合 128 维自然背景 covariance，并切为 16 个 8 维带。修正后通过频带数为 0；旧 `L32H27-F1` 结论已撤回。

![合格单头的 16 带画像](figures/figure3_selected_head_16band_atlas.png)

## 边界与下一决策

- 修正不改变“细粒度相对区分信号在 `o_proj` 前存在”的结论，也不改变单头定位 Pass。
- 修正否定了旧的“一处 F1 固定频带通过”窄结论；固定 middle/tail 更没有获得证据。
- 结果仍限于一个模型和一套 taxonomy，不证明 attention 的因果必要性、跨层头身份、Router 效用或训练收益。
- 唯一下一决策仍是用独立 taxonomy 复现全宽深度效应和经过全局校正的晚层单头；固定频带不进入 Router。

完整文本：[actual_semantic_text_sequences.json](../A15_02_E01_qwen3_residual_semantic_variance_atlas/provenance/actual_semantic_text_sequences.json)。完整修正记录见 [detailed.md](detailed.md)。
