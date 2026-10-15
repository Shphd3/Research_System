# 原始Qwen3-0.6B的SAE与相关资产

本次补登记 **26条资产：25条当前可访问，1条历史数据路径缺失**。
[catalog.json](catalog.json)是唯一地址／身份目录；本文件负责讲清如何选用。
模型、SAE、适配器、数据和数组保留在原存储位置；登记不改变当前研究架构。

[English](qwen3_0p6b_sae.md) · [访问与训练后登记规则](README_cn.md) ·
[本次Qwen可访问资产检查](checks/2026-10-09_qwen3_available_assets.json) ·
[包含缺失项的全库快照](checks/2026-10-09_access_v4.json)

## 先确定模型与张量位置，再选SAE

找到的独立SAE是在冻结的原始28层Qwen模型上训练的。
它在**零起算索引27（第28层，即末层）**的MLP执行前，读取该层经过Attention后归一化的**实际MLP输入**。
输入有1024个坐标；编码器将它映射到30000个特征坐标，经过ReLU和Top-32后，每个token最多保留32个正特征值。
解码器用这些值重构MLP输入。训练时归一化解码器各列；编码前不将每个输入归一到单位长度，也不先减去解码器bias。

| 资产体系 | 父模型与准确读取位置 | 使用边界 |
|---|---|---|
| E16独立SAE | 原始预训练Qwen3-0.6B，28层；零起算索引27的MLP实际输入，1024维 | 有独立最终权重与里程碑文件 |
| 当前fresh S7的SAE | 从头训练的8层S7；零起算索引7（第8层）的Attention投影输出，残差相加前，1024维 | 内嵌对应模型的state.pt |
| SALL的SAE | 另一套从头训练的SALL模型，八层内嵌SAE | 按自身模型／config加载，不能套E16接口 |
| A3路由表征实验 | 另一套12层、hidden512的MoE | 已登记端点不包含SAE |

维数相同不代表特征坐标已经对齐，也不代表加载方式可互换。
将固定SAE用于适配后的模型时，要同时记录**SAE训练时的父模型**和**产生新表征的实际模型**。

## 检查点与基座权重

| 资产ID | 实际文件／对象 |
|---|---|
| `model_qwen3_0p6b_base_official_a5` | [官方模型目录](/data/250010109/model_cache/Qwen3-0.6B-Base-official)，E16及历史A5/A6流程记录的父模型 |
| `tokenizer_qwen3_0p6b_base_official_a5` | 同目录的tokenizer，单独登记 |
| `checkpoint_family_qwen3_0p6b_e16_layer27_sae` | [E16完整运行目录](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z)，含两个轮换恢复槽 |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | [sae_full_final.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt) |
| `sae_qwen3_0p6b_e16_layer27_step_24415` | [sae_step_24415.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_24415.pt)：实际观察100,003,840个raw token |
| `sae_qwen3_0p6b_e16_layer27_step_73243` | [sae_step_73243.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_73243.pt)：实际观察300,003,328个raw token |
| `sae_qwen3_0p6b_e16_layer27_step_244141` | [sae_step_244141.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_244141.pt)：实际观察1,000,001,536个raw token |

最终导出对应step244141。这里“1B”指SAE训练观察的token数，不是模型参数规模，也不是语言模型新训练了1B token。
最终／里程碑导出保存SAE的config、state与metadata，不保存optimizer；两个恢复槽使用含optimizer的另一种格式。
会变化的latest.json不能代替稳定版本身份，也不证明能精确接续训练。

[原full_summary.json](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json)
记录最终权重hash为`e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`，当时重新加载的最大差异为0.0。
本次没有重算这个hash，也没有重新加载。最终与1B里程碑文件大小不同，不能据此说两者tensor相同，也不能说字节相同。
实际加载入口是[sae_core.py](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/sae_core.py)中的TopKSAE.from_pretrained，不能用S7内嵌state的加载方式。

model_cache下的官方父模型与先前登记的/data/share模型保留独立身份。
目录区分原manifest记录的权重hash和本次实际核对的小config hash；不能用今天的目录补齐旧缓存缺失的历史基座身份。

## 已保存的表征、数据与训练产物

| 资产ID／家族 | 保存了什么，主要限制是什么 |
|---|---|
| `representation_qwen3_0p6b_e17_dclm_sparse_activation` | [E17激活缓存](/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/full-20260904T023742Z/activation_cache)：discovery261632行、replication261634行，每行32个特征编号／值；合并数组没有明确token／window／position ID |
| `representation_qwen3_0p6b_e18_semantics_035600`、`_040500`、`_042013` | [E18三个运行版本](/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics/runs)，各有六份稀疏激活缓存；首个版本缺完成总结。最新m2d2_train为196734行，旧版本为65576行 |
| `data_qwen3_0p6b_e18_e14_eight_task_proxy` | [E14 processed.pt](/data/250010109/datasets/a15_e14_benchmark/processed.pt)：含GSM8K的八任务代理；与后来的full八任务缓存分别登记 |
| `data_qwen3_0p6b_e18_m2d2_seq256` | [M2D2 seq256准备数据](/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt)：与后来的N8面板不同 |
| `adapter_family_qwen06b_flat_0907`、`_a5_0908`、`_a6_0908`、`_a6r1_0909` | 15＋15＋12＋12，共54组条件／seed；实际final／update／recovery文件在catalog逐项列出，不含冻结基座权重 |
| `router_family_qwen06b_a5_frozen`、`feature_groups_qwen06b_a5` | 9个拟合后的router，以及历史流程使用的特征组／图；与expert权重是不同对象 |
| `representation_qwen06b_flat_0907_discovery`、`_router`、`_development` | 三组冻结基座缓存，含原始h、SAE稀疏值、记录／分片映射；原状态CACHED_NOT_QUALIFIED，登记不提升其资格 |
| `teacher_cache_qwen06b_a6_0908`、`_a6r1_0909` | SAE/GMM概率目标，供在线router训练使用；不是已训练专家checkpoint |
| `analysis_qwen06b_sae_hierarchy_0909` | 已保存的图、特征映射、共激活与任务组成分析；历史来源只在限定条件下可用，仍有未闭合环节 |

E18的window_ids指筛选后的record／window列表位置，不能直接当原数据全局记录ID；没有保存原始token位置或原始h。
八任务数据含重新分配的官方test来源样本。旧分区和文件名里的confirmation不等于新的未曝光测试集。

E17/E18的父模型引用用于导航到预期输入。早期035600运行缺少可读总结，
其父模型／SAE／tokenizer身份只能按来源推断，不能当作该run已经核实的历史身份。
已查的旧缓存来源没有闭合历史基座权重digest；登记今天的模型文件不能补上这一环。
这些条目的数据ID是来源导航；仅仅读取现有数组，不自动要求重新加载父模型或数据。

9/7的expert读取MLP down_proj前3072维输入，而router读取1024维MLP输入。
A5/A6/A6R1的expert与router都读取同一个1024维MLP输入。
它们包含共享expert与Top-1 expert，不能套成当前S7的“Attention支路、无共享expert”。
A5冻结router权重，但仍更新独立的平衡bias；A6/A6R1训练router，固定的是教师。
准确路由、保存格式和加载定义在每条资产的原源码来源中分别记录。

9/7和A5保存格式没有显式RNG字段；A6/A6R1包含RNG。
有optimizer不等于精确恢复训练已通过；本次没有执行任何恢复验证。

## 本次能访问什么，还缺什么

**2026-10-09 16:02:39，北京时间，有效UID0**：25条可用新增资产均通过登记的访问检查。
本次没有在CPU／GPU完整加载权重；只检查路径、文件头／首字节，未重跑分析或重算大文件hash。

`data_qwen3_0p6b_senior_exact_sft_legacy_missing`保留历史不可用原路径：
`/mnt/workspace/zx_workspace/sae-guided-router/sft_mixture_6000_each_with_mmlu_bbh_mmlu_eval_aligned/train.parquet`。
原E18记录已标NOT_RUN_MISSING_DATA，本次访问也失败；其他外部挂载是否有此数据仍未知。
E14代理单独登记，不能默认为这份原数据的替代身份。

```sh
python tools/check_assets.py --strict \
  --asset model_qwen3_0p6b_base_official_a5 \
  --asset tokenizer_qwen3_0p6b_base_official_a5 \
  --asset sae_qwen3_0p6b_e16_layer27_final_1b \
  --asset dclm_pair_v1
```

只选择当前已授权阶段需要的输入。缺失时按[资产库入口](README_cn.md)先查来源与挂载，再暂停依赖工作。
后续实际产生的checkpoint与可复用分析缓存，按该入口的登记闭环维护。
没有穷尽其他用户共享目录；本次不能宣称已经找齐所有历史Qwen SAE。
