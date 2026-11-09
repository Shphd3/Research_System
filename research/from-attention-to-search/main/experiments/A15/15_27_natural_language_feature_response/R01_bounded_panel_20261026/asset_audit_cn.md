# R01 既有资产审计

本轮选择原始 28 层 Qwen3-0.6B official 预训练模型，以及已有 E16 第 27 层 MLP 输入 SAE。四个必要登记资产在北京时间 2026-10-26 18:40:13（UTC 10:40:13）、有效用户 UID 0 下通过当前严格访问检查。选择的是一套匹配接口，没有执行模型比较。

| 资产 ID | 既有对象 |
| --- | --- |
| `model_qwen3_0p6b_base_official_a5` | `/data/250010109/model_cache/Qwen3-0.6B-Base-official/model.safetensors` |
| `tokenizer_qwen3_0p6b_base_official_a5` | 同一 official 目录的分词文件 |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | E16 的 `full-20260903T150734Z/sae_full_final.pt` |
| `representation_qwen3_0p6b_e17_dclm_sparse_activation` | E17 DCLM TRAIN discovery 数组，保留 261,632 个位置 |

## 确切测量接口

模型含 28 个块，隐藏维度 1,024，MLP 中间维度 3,072。Hook 为 `model.model.layers[27].mlp.register_forward_pre_hook`，读取 `args[0]`，即该块 post-attention 归一化后的实际 MLP 输入。它不是 attention 投影输出，也不是未归一化残差。单层 SAE 将这个 1,024 维向量映射到 30,000 个坐标，使用 ReLU 与 Top32。原生 `TopKSAE.from_pretrained` 恢复 `format/config/state_dict/metadata`；四个 FP32 张量分别是 encoder 权重 `[30000,1024]`、encoder 偏置 `[30000]`、decoder 权重 `[1024,30000]`、decoder 偏置 `[1024]`。

编码前不作输入单位范数归一化，也不减 decoder 偏置。重构为每个激活乘相应 decoder 列后求和，再加 decoder 偏置。贡献幅度是激活乘实际保存的 decoder 列 L2 范数，单位对应原生 hook。绝对激活、原始贡献与归一化读数分别保存。贡献向量可以抵消，幅度不是因果或方差分配。

字典在 `dclm_pair_v1` 上训练，父模型冻结，训练时每批去除范数高于 0.999 分位的 token。本轮不会按这个旧筛选静默删除设计好的目标。模型本地 README 说明预训练覆盖 119 种语言；本轮按字典 DCLM 来源采用英文构造，不强制中文。[机器审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/asset_audit.json) 绑定实际 loader 与源文件。

## 身份与历史重构

本轮重新计算的 SHA256 与既有记录一致：

| 对象 | SHA256 |
| --- | --- |
| 模型权重 | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| E16 字典 | `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65` |
| 模型配置 | `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` |
| Tokenizer JSON | `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539` |

其他分词文件及参考数组哈希保留在机器审计。E16 原始 [full summary](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json) 记录验证重构归一化均方误差 0.0533820926、平均 L0 为 32、检查点重新加载差为 0.0。这些历史读数支持尝试 R01 资格检查，不能自动证明本轮文本合格。

## 独立参考频率及限制

只读取 E17 的 `discovery_indices.npy` 与 `discovery_values.npy`。它们有 261,632×32 个条目，激活均为有限正值。每个特征的频率为正激活命中数除以 261,632；平均激活为相应激活和除以同一分母。这是经记录中的范数筛选后得到的历史参考语料命中率。当前面板命中率另列。

来源记录了预期 official 父模型路径／配置和确切 SAE 哈希，但没有记录产生旧缓存的父模型权重哈希。重新计算当前父模型哈希不能修复这个旧绑定缺口。因此，频率匹配比较保留有条件的来源限制。E17 产生时编码采用 BF16 autocast，本轮使用原生 FP32，TopK 临界并列可能不同，匹配另依赖精度可比性。历史 NMSE 不能替代本地资格。不能新增模型前向或重建参考语料来掩盖缺口。E17 既有图表只列选中节点，不是完整频率表；从保存的 discovery 数组推导边际计数属于授权离线工作。E17 replication 数组和封存 TEST 保持未读。

## 环境复用与待检资格

复用既有 `/root/anaconda3/envs/spectral-hier/bin/python`，设置 `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3`。已确认可导入 Torch 2.5.1+cu121、Transformers 4.53.3、tokenizers 0.21.2、safetensors 0.5.3，无需安装包。模型用原生 BF16 eval/no-grad SDPA，SAE 用保存的 FP32 张量和原生 Top32。可用执行面是当前容器的既有 H100 40 GB MIG，实际加载仍需运行核验。

截至资产审计边界，模型前向为零，GPU 模型加载为零，仅作一次字典 CPU 内容检查，无训练、无 TEST。新面板重构、decoder 公式一致及复放检查由 [Protocol](protocol_cn.md) 的事前门槛约束。失败停止依赖假设，不触发字典训练或替换资产。
