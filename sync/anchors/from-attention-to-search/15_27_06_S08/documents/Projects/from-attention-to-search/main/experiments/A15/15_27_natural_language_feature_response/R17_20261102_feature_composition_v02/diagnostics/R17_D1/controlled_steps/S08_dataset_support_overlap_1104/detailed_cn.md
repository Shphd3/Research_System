派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/detailed_cn.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/detailed_cn.md)；研究修改仍回到原件。

---

# S08 详细结果与审计


在本轮3个可读数据集、每组257篇问题、两套原生 SAE 的6个比较中，6/6 满足预设的“双侧内部高于跨域”判据。成立条件：ATTN_SAE:Magicoder/GSM8K; ATTN_SAE:Magicoder/MMLU; ATTN_SAE:GSM8K/MMLU; MLPIN_SAE:Magicoder/GSM8K; MLPIN_SAE:Magicoder/MMLU; MLPIN_SAE:GSM8K/MMLU。其余比较：无。这描述数据集条件下的激活成员相似性；来源、格式、题型与词面仍可能参与形成差异，不能直接归因于领域知识，也不证明功能机制。

本轮事实分析路径：行为与因素控制只检查文本长度、格式和词面，没有答案正确率；表征分析比较固定 Qwen3-0.6B 的二值激活成员；功能干预与训练均 NOT_RUN，本轮只审核采集接口和数值可信度。科研接受与问题关闭 Unknown。

| SAE | pair | A_within | B_within | cross | pooled_difference_95CI | Holm_p | both_sides |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | 0.0351 | 0.0171 | 0.0122 | 0.0139 [0.0129,0.0149] | 0.006 | BOTH_WITHIN_HIGHER |
| ATTN_SAE | Magicoder/MMLU | 0.0351 | 0.0256 | 0.0206 | 0.0098 [0.0086,0.0111] | 0.006 | BOTH_WITHIN_HIGHER |
| ATTN_SAE | GSM8K/MMLU | 0.0171 | 0.0256 | 0.0118 | 0.0096 [0.0084,0.0109] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | Magicoder/GSM8K | 0.1187 | 0.0968 | 0.0627 | 0.0450 [0.0433,0.0468] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | Magicoder/MMLU | 0.1187 | 0.0796 | 0.0707 | 0.0284 [0.0268,0.0302] | 0.006 | BOTH_WITHIN_HIGHER |
| MLPIN_SAE | GSM8K/MMLU | 0.0968 | 0.0796 | 0.0620 | 0.0262 [0.0242,0.0282] | 0.006 | BOTH_WITHIN_HIGHER |


表中 A/B 顺序见 pair 列。Jaccard=两位置共同激活成员数÷两位置并集成员数；每个文档对平均8个相同分位位置。pooled difference=两侧内部均值的平均−跨域均值。每组257篇，内部与跨域各32896个不同文档对，但独立统计单位是文档。区间来自1999次文档级 bootstrap；999次整篇标签置换，6个主要合并差检验 Holm 校正。每侧差值及95%区间、实际比较数在[完整统计表](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/tables/overlap_summary.csv)，不能只用合并差替代两侧判断。


## 实验做法和每项比较的含义

每个源完整读取指定 Arrow 表并使用指定问题字段。规范化 NFKC/casefold/空白折叠哈希用于去重，推理仅strip边缘并统一CRLF，保留内部格式；跨源精确重复对称排除，本次为0。MMLU14042行→13866唯一问题，176重复；Magicoder75197、GSM8K7473均未减少。从均匀打乱的唯一题干候选逐条 tokenize 到257篇合格；MMLU检查359篇，其中102篇不足16token。没有声称对全语料做完token长度筛选。最低样本可用量足够，本轮为快速分析预先定额257；不冒充分析全部75K/14K问题。

每篇实际推理 min(全长,128) token；位置 floor((j+.5)L/8)，j=0..7，L≥16确保8个不同位置。对齐相同分位的8对token，而不是8×8全配对。文档对内平均后再对文档对取均值，文档等额；不同文档的token从不当成独立文档。无后缀、无chat模板、无答案。Magicoder较长且大部分截断，因此主结果是这些问题前缀的局部状态统计。

模型 official Qwen3-0.6B-Base，28block、宽1024；使用FP32 CPU2线程、固定8×128物理批形状，尾批填充但只保存真文档。两个block27原生SAE均30000维ReLU-Top32，激活定义为所选z>0。Attention读self_attn.o_proj输出、残差之前；MLPIN读mlp实际输入，残差相加和post_attention_layernorm之后。二者各用自己的encoder/decoder，直接输入原表征，无额外归一化或偏置减法。配置、权重与加载器SHA见frozen_plan。抽取仅加载模型主体，避免无关词表logits成本。本轮无候选答案评分任务。

配对：每源按SHA256('S08'+文档ID)固定顺序。内部全体i<j；跨域对A_i与B_(i+offset mod N)，offset=1..(N−1)/2。奇数N使两种各N(N−1)/2对，跨域每篇度数相同。保存pair_graphs.npz的整数边端点及全局ID表。主分析每组32896对、每对8个位置，共263168位置比较；这个数不是独立样本量。

文档 bootstrap1999次，每源独立multinomial重采样N篇，原边乘文档重数c_i c_j后加权求均值。同篇所有位置和重复配对同步移动；原自配对不新增。保存所有重采样统计向量。999次整篇标签置换保留两组N，重新按同一固定配对规则计算，不把原边作为独立可交换项。主要零假设为源标签与整篇表征可交换；这是关联性零假设，不是领域内容的随机因果实验。主要6个pooled单侧检验Holm校正，95%区间为边际区间；两侧各自区间不另作独立阳性筛选。每配对、每控制的实际种子见CSV，基种子20261104。

完整题干长度分箱用[16,32,48,64,96,128,192,256,512,1024,2048,∞)，各箱两源取最小数量，并在同箱两侧各去一篇使总数为奇数。分箱内进行标签置换，保留每箱两侧数量。它是粗粒度长度匹配，不是逐字相等长度。固定31位置只用≥32token文档；固定15位置所有文档可用。后者在激活读取前因Magicoder/GSM8K完整长度匹配仅11篇追加，原协议/计划/面板原字节保留，见amendment_fixed16与时间戳。两个前缀控制均不等于完整问题长度匹配。

词面控制：发现激活前按8个位置中的文档覆盖选每源均≥20篇、最多3种相同token，token表见lexical_control_tokens.json。每文档对仅对相同所选token的位置两两比较后均值；没有匹配的位置对保留缺失。仍用原文档图，不补抽文档或挑激活好的词。这个条件统计中的有效边数和端点文档覆盖见CSV；只报告文档bootstrap，不赋予标签置换意义。它改变被比较的token/上下文分布，不能将与主结果的差直接当作去掉词面因素后的因果净效应。

幅值补充：每位置只在共同正成员上计算sqrt(sum((z_i−z_j)^2)/共同成员数)，共同数为0则缺失，文档对平均可用8位置，再平均边。它混合规模和搭配差异，不替代二值成员J。质量表另列z向量L2、原hL2、重构相对误差以及decoder列范数。

## 全部对照结果

| site | A | B | mode | N_A | within_A | within_B | cross | A_minus_cross_lo | B_minus_cross_lo | pooled_minus_cross | pooled_minus_cross_lo | pooled_minus_cross_hi | p_pooled_one_sided | cross_actual_pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | length_matched | 11 | 0.035245 | 0.016378 | 0.006829 | 0.021827 | 0.004165 | 0.018982 | 0.013988 | 0.024113 | 0.001000 | 55 |
| ATTN_SAE | Magicoder | GSM8K | fixed32 | 249 | 0.028491 | 0.016681 | 0.009676 | 0.016888 | 0.004906 | 0.012911 | 0.011225 | 0.014575 | 0.001000 | 30876 |
| ATTN_SAE | Magicoder | GSM8K | fixed16 | 257 | 0.033622 | 0.013091 | 0.010012 | 0.021110 | 0.001486 | 0.013345 | 0.011689 | 0.015133 | 0.001000 | 32896 |
| ATTN_SAE | Magicoder | GSM8K | same_token | 257 | 0.052522 | 0.023681 | 0.013058 | 0.034029 | 0.007781 | 0.025044 | 0.021773 | 0.028822 | nan | 4587 |
| ATTN_SAE | Magicoder | MMLU | length_matched | 59 | 0.035417 | 0.023546 | 0.018960 | 0.013491 | 0.003018 | 0.010521 | 0.008763 | 0.012644 | 0.001000 | 1711 |
| ATTN_SAE | Magicoder | MMLU | fixed32 | 161 | 0.029206 | 0.054011 | 0.018493 | 0.008776 | 0.017648 | 0.023116 | 0.014116 | 0.035825 | 0.001000 | 12880 |
| ATTN_SAE | Magicoder | MMLU | fixed16 | 257 | 0.033622 | 0.033182 | 0.019690 | 0.011753 | 0.006077 | 0.013712 | 0.009939 | 0.019301 | 0.001000 | 32896 |
| ATTN_SAE | Magicoder | MMLU | same_token | 257 | 0.064403 | 0.041122 | 0.024099 | 0.033369 | 0.012223 | 0.028664 | 0.024375 | 0.033504 | nan | 6457 |
| ATTN_SAE | GSM8K | MMLU | length_matched | 121 | 0.017526 | 0.033174 | 0.012440 | 0.003748 | 0.013957 | 0.012910 | 0.009431 | 0.017582 | 0.001000 | 7260 |
| ATTN_SAE | GSM8K | MMLU | fixed32 | 161 | 0.016032 | 0.054011 | 0.009522 | 0.004415 | 0.025918 | 0.025500 | 0.015954 | 0.037989 | 0.001000 | 12880 |
| ATTN_SAE | GSM8K | MMLU | fixed16 | 257 | 0.013091 | 0.033182 | 0.009172 | 0.002359 | 0.016596 | 0.013964 | 0.010066 | 0.019039 | 0.001000 | 32896 |
| ATTN_SAE | GSM8K | MMLU | same_token | 257 | 0.019675 | 0.047413 | 0.015204 | 0.001877 | 0.023393 | 0.018341 | 0.013819 | 0.024579 | nan | 5284 |
| MLPIN_SAE | Magicoder | GSM8K | length_matched | 11 | 0.115964 | 0.102870 | 0.062023 | 0.041962 | 0.033384 | 0.047394 | 0.039790 | 0.055556 | 0.001000 | 55 |
| MLPIN_SAE | Magicoder | GSM8K | fixed32 | 249 | 0.116079 | 0.097801 | 0.065890 | 0.045359 | 0.027907 | 0.041050 | 0.038081 | 0.044231 | 0.001000 | 30876 |
| MLPIN_SAE | Magicoder | GSM8K | fixed16 | 257 | 0.120424 | 0.094315 | 0.061787 | 0.053655 | 0.028828 | 0.045582 | 0.042498 | 0.048534 | 0.001000 | 32896 |
| MLPIN_SAE | Magicoder | GSM8K | same_token | 257 | 0.213164 | 0.153879 | 0.099114 | 0.101724 | 0.047563 | 0.084407 | 0.077263 | 0.092115 | nan | 4587 |
| MLPIN_SAE | Magicoder | MMLU | length_matched | 59 | 0.116656 | 0.074691 | 0.064262 | 0.047124 | 0.006512 | 0.031412 | 0.027735 | 0.035166 | 0.001000 | 1711 |
| MLPIN_SAE | Magicoder | MMLU | fixed32 | 161 | 0.119839 | 0.103416 | 0.074078 | 0.040093 | 0.012671 | 0.037549 | 0.029332 | 0.048526 | 0.001000 | 12880 |
| MLPIN_SAE | Magicoder | MMLU | fixed16 | 257 | 0.120424 | 0.082234 | 0.071220 | 0.044612 | 0.003995 | 0.030109 | 0.025845 | 0.035735 | 0.001000 | 32896 |
| MLPIN_SAE | Magicoder | MMLU | same_token | 257 | 0.214227 | 0.122789 | 0.117402 | 0.086728 | 0.000601 | 0.051107 | 0.045623 | 0.057156 | nan | 6457 |
| MLPIN_SAE | GSM8K | MMLU | length_matched | 121 | 0.097815 | 0.086297 | 0.064823 | 0.029623 | 0.014378 | 0.027233 | 0.022915 | 0.032394 | 0.001000 | 7260 |
| MLPIN_SAE | GSM8K | MMLU | fixed32 | 161 | 0.097955 | 0.103416 | 0.061523 | 0.032081 | 0.023537 | 0.039163 | 0.029377 | 0.052070 | 0.001000 | 12880 |
| MLPIN_SAE | GSM8K | MMLU | fixed16 | 257 | 0.094315 | 0.082234 | 0.058106 | 0.032573 | 0.016976 | 0.030168 | 0.025779 | 0.035367 | 0.001000 | 32896 |
| MLPIN_SAE | GSM8K | MMLU | same_token | 257 | 0.134127 | 0.132462 | 0.092911 | 0.034107 | 0.028765 | 0.040383 | 0.033725 | 0.049058 | nan | 5284 |

## 实际来源与格式

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

| dataset | N | median_full_tokens | min_full_tokens | max_full_tokens | median_visible_tokens | truncated | code_fence | with_newline | with_question_mark |
|---|---|---|---|---|---|---|---|---|---|
| Magicoder | 257 | 252.000000 | 62 | 793 | 128.000000 | 248 | 158 | 257 | 9 |
| GSM8K | 257 | 56.000000 | 28 | 168 | 56.000000 | 4 | 0 | 0 | 249 |
| MMLU | 257 | 50.000000 | 16 | 613 | 50.000000 | 50 | 0 | 27 | 179 |

## 字典规模和重构限制

| site | dataset | N | positions_per_doc | active_min | active_max | active_mean | z_L2_mean | z_L2_doc_SD | h_L2_mean | relative_reconstruction_error_mean | relative_reconstruction_error_p95 | decoder_norm_min | decoder_norm_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | 257 | 8 | 32 | 32 | 32.000000 | 38.945469 | 4.912744 | 66.669350 | 0.535184 | 0.637810 | 0.999999 | 1.000001 |
| ATTN_SAE | GSM8K | 257 | 8 | 32 | 32 | 32.000000 | 50.016098 | 8.426587 | 98.497192 | 0.705962 | 0.818755 | 0.999999 | 1.000001 |
| ATTN_SAE | MMLU | 257 | 8 | 32 | 32 | 32.000000 | 52.429012 | 7.733827 | 81.478737 | 0.455528 | 0.603645 | 0.999999 | 1.000001 |
| MLPIN_SAE | Magicoder | 257 | 8 | 32 | 32 | 32.000000 | 87.849968 | 5.517982 | 110.716728 | 0.312248 | 0.431924 | 0.999999 | 1.000001 |
| MLPIN_SAE | GSM8K | 257 | 8 | 32 | 32 | 32.000000 | 119.931221 | 25.402987 | 148.492889 | 0.401202 | 0.521990 | 0.999999 | 1.000001 |
| MLPIN_SAE | MMLU | 257 | 8 | 32 | 32 | 32.000000 | 86.108810 | 9.080378 | 114.101753 | 0.281253 | 0.443278 | 0.999999 | 1.000001 |

## 幅值补充（非Jaccard）

| site | A | B | within_A | within_B | cross | pooled_minus_cross |
|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder | GSM8K | 5.916856 | 9.218238 | 11.070833 | -3.503286 |
| ATTN_SAE | Magicoder | MMLU | 5.916856 | 10.275075 | 10.538594 | -2.442629 |
| ATTN_SAE | GSM8K | MMLU | 9.218238 | 10.275075 | 16.251305 | -6.504649 |
| MLPIN_SAE | Magicoder | GSM8K | 13.780904 | 27.680134 | 37.648341 | -16.917822 |
| MLPIN_SAE | Magicoder | MMLU | 13.780904 | 17.141076 | 20.144026 | -4.683036 |
| MLPIN_SAE | GSM8K | MMLU | 27.680134 | 17.141076 | 36.533608 | -14.123003 |

## 指回原文和坐标的例子

预先按ID哈希顺序选择的例子（不是挑最高重叠）：Magicoder:train:row28229 / GSM8K:train:row563，ATTN_SAE，首个分位。前者位置8 token=' that'，后者位置3 token='8'。交集1、并集63，J=0.015873。共同ID=[23899]；前者幅值=[21.290346145629883]；后者幅值=[21.925743103027344]。

A全文：

> You are tasked with creating a Python function that simulates a simplified version of the `sys.path.append()` method. The `sys.path` variable in Python is a list of strings that specifies the search path for modules. When a module is imported, Python searches for it in the directories listed in `sys.path`. The `sys.path.append()` method is used to add a directory to this search path.
> 
> Your task is to create a function `custom_path_append(directory: str, search_path: List[str]) -> List[str]` that takes a directory string and a list of strings representing the current search path. The function should return a new list representing the updated search path after appending the given directory. If the directory is already present in the search path, it should not be duplicated.
> 
> Example:
> ```python
> current_path = ['/usr/lib/python3', '/usr/local/lib/python3']
> new_path = custom_path_append('/home/user/custom', current_path)
> print(new_path)  # Output: ['/usr/lib/python3', '/usr/local/lib/python3', '/home/user/custom']
> ```

B全文：

> There are 84 people waiting in line to ride a roller coaster at an amusement park.  The roller coaster has 7 cars, and each car seats 2 people.  How many times will the ride operator have to run the roller coaster to give everyone in line a turn?

其余同源和跨源例子、每个共同ID的两侧幅值、换入换出集合在tables/deterministic_examples.jsonl。该文件包括反例可能出现的全部预定例子，未按结果筛选。

## 竞争解释与边界

主数据集差异同时包含题型、格式、词面、来源、主题；两个控制不能唯一裁决知识解释。代码围栏及换行尤其不平衡；Numina缺失，学长版本未复现。精确去重不排除近重复；MMLU混合学科、问题省略选项；未检验模型预训练污染。Top32强制限制激活名额，重叠变化不等于新增语义容量；不同SAE ID不对应，重构误差限制将字典当真实feature。单一固定模型、block27、前128token和有限文档采样只支持本条件的观察。小样本长度对照或区间跨0为证据不足；不能升级为不存在差异。控制是探索性的，不救主要失败。

## 数值审核和复现

先校验hook零扰动与第32token前缀等价，再用直接Python集合运算独立复核200文档对、重放90个已存边均值、核对所有图的边数/文档度数及六个Holm值。独立脚本和evidence/independent_verification.json保留结果。每篇原文、source row/字段/revision、ID、token和位置在data/panel.jsonl，原生Top32 ID/激活值在cache/activations.npz；大kernel缓存见large_files_index。训练/功能干预均NOT_RUN，科学接受Unknown。

主题和来源构成：Magicoder为编程问题，lang是编程语言（样本python139/257），不是英文识别；GSM8K为小学数学故事题；MMLU混合学科，均匀按题干抽样而非学科平衡，样本professional_law36/257、moral_scenarios30/257。相同源可以包含与另一来源主题更近的题干，因此不能用数据集标签替代细粒度语义类别。

## 认识更新和个体反例（事后描述）


认识更新：H1中“同条件文本的成员更相似”这一重叠子预测，从构造家族扩展到了三种自然题干来源。四类对照的两侧差值95%区间也都大于0；未观察到这些有限对照消除差异。它没有验证父子成员换入换出的语义规律。共同成员幅值只是补充，不构成本轮H2裁决。

均值规律不覆盖每篇文档。事后描述性检查中，MLPIN的MMLU文档相对Magicoder有57/257篇自身内部邻居均值低于跨域；Attention的GSM8K相对Magicoder有48/257篇。例子 MMLU:test:row6874：Statement 1| The softmax function is commonly used in mutliclass logistic regression. Statement 2| The temperature of a nonuniform softmax distribution affects its entropy. 其MMLU内部均值0.071092，跨Magicoder均值0.086829，差-0.015738。这是事后展示的反例，不重新筛选数据或变更主要检验，也不能仅凭词语为其指定feature语义。见[逐文档反例图](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/figures/05_document_counterexamples.png)与[tables/per_document_counts.csv](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/tables/per_document_counts.csv)。

相同token后MLPIN的MMLU相对Magicoder这一侧差仅0.005388，95%区间[0.000601,0.011027]，比主分析0.008862更接近边界；不能将有限词面控制写成彻底排除词面。控制使用不同token分布；长度/32token控制还改变文档子集，不能将其相对主分析的数值变化解释为某个因素的因果贡献。
| site | pair | dataset | N | negative_documents | zero_documents | min_advantage | median_advantage |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | Magicoder | 257 | 0 | 0 | 0.003836 | 0.021865 |
| ATTN_SAE | Magicoder/GSM8K | GSM8K | 257 | 48 | 0 | -0.008484 | 0.005147 |
| ATTN_SAE | Magicoder/MMLU | Magicoder | 257 | 0 | 0 | 0.003483 | 0.013272 |
| ATTN_SAE | Magicoder/MMLU | MMLU | 257 | 32 | 0 | -0.007512 | 0.002211 |
| ATTN_SAE | GSM8K/MMLU | GSM8K | 257 | 37 | 0 | -0.009199 | 0.005114 |
| ATTN_SAE | GSM8K/MMLU | MMLU | 257 | 0 | 0 | 0.002435 | 0.010754 |
| MLPIN_SAE | Magicoder/GSM8K | Magicoder | 257 | 0 | 0 | 0.012105 | 0.057365 |
| MLPIN_SAE | Magicoder/GSM8K | GSM8K | 257 | 2 | 0 | -0.012561 | 0.035947 |
| MLPIN_SAE | Magicoder/MMLU | Magicoder | 257 | 0 | 0 | 0.019018 | 0.048364 |
| MLPIN_SAE | Magicoder/MMLU | MMLU | 257 | 57 | 0 | -0.015738 | 0.008748 |
| MLPIN_SAE | GSM8K/MMLU | GSM8K | 257 | 1 | 0 | -0.001421 | 0.036533 |
| MLPIN_SAE | GSM8K/MMLU | MMLU | 257 | 29 | 0 | -0.024747 | 0.017546 |
