# R03资产：原同token图与匹配CrossCoder

已找到与本轮观测单位一致的原图：同一token处一个共享CrossCoder z的二值共激活。以**O**保留原件；本轮原始/校正图及community另记R/C，不与E16差值组G02/G04混名。本审计没有前向，也不修改旧资产。

## 匹配主资产

| 注册ID | 实际对象与绑定 |
| --- | --- |
| `model_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base`，固定预训练Qwen3，28层、hidden1024 |
| `tokenizer_qwen3_0p6b_base` | 原父模型本地tokenizer与保存哈希 |
| `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013` | A22 final，F16384、999997440训练位置、244140更新；分析不加载optimizer |
| `dclm_crosscoder_direct_bins_1b_a15_20261013` | 原direct-bin来源/index；此VAL已暴露，只是复核材料，不是封存TEST |
| `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` | 10485760位置、640个CSR chunk的完整共享z缓存 |
| `analysis_crosscoder_feature_relation_phase1_20261013t173130z` | 原完整计数、图、decoder几何、分割与代码/来源身份 |
| `data_same_token_coactivation_panel_r03_20261027` | 新固定12情境/72文本，预算内先选六完整案例/36输入；文本SHA256为`57c1d0358b5128a116128f73514d6d855454bdb689e706c941ed76f6a27e01b9` |

六项复用主资产当前严格访问通过，见[访问收据](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/main_input_access.json)；新登记面板也由本文作者作当前严格检查并通过。另有原图审计含旧E17共核验7个ID、17个小来源文件哈希及所有chunk保存的存在/字节数；没有重哈希全部16GB。实际选中chunk读取时再完整核验哈希。严格访问不证明可加载、数值合格、文档独立或科学接受。

模型SHA256：`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`。

字典SHA256：`09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`。

上述权重哈希已在前一同会话R02流式检查；本轮runner在新推理前重核。首次冻结收据拥有本轮源文件哈希。[完整原图核验](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_graph_audit_cn.md)及JSON保存详细来源。

## 测量接口与尺度

同token提取零起始1,3,…,27层residual-post、最终global norm之前的张量。用原TRAIN均值/向量RMS归一化为`[位置,14,1024]`；各层编码投影求和加共享偏置再ReLU。Base为BF16 SDPA，coder为BF16 GEMM、FP32状态/分数。严格保存TRAIN门槛为0.051281172782182693，分数是正编码值乘各层decoder范数之和，不是逐token Top256。不重拟合归一化或门槛。

只有一个共享z。逐层原尺度贡献是z×TRAIN RMS×本层decoder范数；均值/decoder偏置另列。拼接原尺度贡献范数、原z、hook范数归一化量分别保存。解码贡献不是各层独立激活、语义高度或浅到深生成证据。

复用原checkpoint、normalizer、threshold、decoder、缓存与图；将原native loader/提取接口适配短输入和预算账本；只新写离线计数、随机化、图分组、控制与报告代码。不训练模型、字典、专家或router；E16与CrossCoder编号不对齐。

## 原图保留

O有全部16384节点，D raw214711边；V只复核D候选并保留206136边。A→B要求nA,nB≥200、nAB≥20、P(B|A)≥0.8、P(A|B)≤0.5、nB≥2nA。DeltaP/lift虽有保存，却未入原接受条件。每箭头频率至少倍增，所以DAG是规则强制；约简后最长向外路径深5不是语义高度。“Composition list”是约简后的出邻居，不是community算法或已验证父子关系。

完整D/V `(16384,16384)` int64计数、feature/block计数及旧边逐block计数均存在。固定512坐标的R/C直接读精确缓存行。即使随机子图漏掉全局hub，O完整图与高频节点仍保留。

## 来源单位与精度边界

CSR为uint64 ptr、排序uint16 ID、正FP32 z。Index可精确恢复token ID、绝对offset和context内位置，却不能恢复原文档ID。10249个1024-token context只在同bin内分D/V；文档/近重复独立Unknown。前8窗口文本可精确往返，但im_end仅能作为来源段代理，标点规则会误切缩写。因此缺经验证句/文档重采样单位，context区间只描述；文本类型也缺。

旧E17另属E16单层F30000、27层MLP输入，BF16编码、FP16导出且过滤异常范数。其编号、父模型及原文位置映射不能与R02 FP32或CrossCoder偷偷混用；旧图只保留为历史背景。

## 新面板资格仍待执行

旧cache的Base batch16×1024、coder batch1024；新面板Base batch1、右pad256、coder batch1024。形状变化需按[Protocol](protocol_cn.md)做2旧cache、2同条件、8可见前缀和重构检查。旧cache与R02另一E16的失败都不预先决定当前接口通过或失败。本文不冒称新推理已发生；资格缺失或失败具体报告，不以训练/新资源补齐。
