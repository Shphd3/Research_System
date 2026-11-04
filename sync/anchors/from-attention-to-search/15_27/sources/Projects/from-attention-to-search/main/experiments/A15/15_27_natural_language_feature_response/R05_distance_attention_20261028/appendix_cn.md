# 参数、数据与代码附录

## 固定数值与实际执行

总前向1096/1096；B960、A120、检查及失败16。R04原456/512和更早1500/1500记录未改写，本轮用户明确给出的1096是替换后的新范围，不自动复用剩余额度。

发现/留出均以完整家族、文档为单位；两字典共用Base前向，候选和尺度各自固定。未训练分类器或字典。

## 数值资格

{
  "time_utc": "2026-10-27T18:12:06.245804+00:00",
  "checks": 1937,
  "all_pass": true,
  "ledger": 1096,
  "check_forwards": 16,
  "B_forwards": 960,
  "A_forwards": 120,
  "B": {
    "SAE": {
      "candidates": 20,
      "far": 0,
      "near_attenuation": 0,
      "insufficient": 20
    },
    "CC": {
      "candidates": 25,
      "far": 0,
      "near_attenuation": 0,
      "insufficient": 25
    }
  },
  "attention_output_max_relative_error": 0.0021355559583753347,
  "attention_output_max_absolute_error": 0.125,
  "A_reconstruction": {
    "SAE": {
      "mean": 0.09774206739073432,
      "p90": 0.19256673306226732
    },
    "CC": {
      "mean": 0.1164784962157812,
      "p90": 0.20919909030199058
    }
  },
  "no_model_training": true,
  "no_new_resources": true,
  "no_sealed_TEST": true,
  "source_freezes_preserved": true,
  "engineering_failures_preserved": true
}

概率容差针对概率，不针对BF16表征值；最终概率maxabs<7.4e-7、相对<2.38e-7；原生Attention输出重构相对<0.002136。所有120文档与R04token激活精确一致。初始失败检查见工程修复记录，不能把旧all_pass:false掩盖为全历史检查通过；当前通过的是原生分支与修正后读出。

## 资产身份

Model SHA256 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`

E16 SHA256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`

A22 SHA256 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`

Tokenizer SHA256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`，与旧R04同一资产；当前tokenizer全文件哈希另列identity。

## 可追溯入口

- [build_panel.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/build_panel.py)：事前文本、精确距离与固定查询。

- [configure.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/configure.py)：Anchor/Protocol及数值合同生成。

- [run_forward.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/run_forward.py)：原生双读数、前向记账、因果Attention读取与逐文档校验。

- [analyze_B.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analyze_B.py)：发现选择、尺度、家族差值、全比较校正。

- [analyze_A.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analyze_A.py)：配对、head/query/document等权、固定组统计和逐层量。

- [audit_and_tables.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/audit_and_tables.py)：独立效应/权重/预算/哈希/因果性审计与CSV。

- [render_figures.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/render_figures.py)：图及固定展示规则。

- [write_reports.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/write_reports.py)：本报告生成，不执行模型。


## 完整冻结配置

```json
{
  "seed": 20261028,
  "round": "R05_distance_attention_20261028",
  "authorization": "current user integrated replacement explicitly authorizes continuous B then A and four figures,existing resources only",
  "budget": {
    "B": 960,
    "A": 120,
    "checks_max": 16,
    "total_max": 1096,
    "charge_before_attempt": true,
    "failed_attempts_count": true,
    "old_budgets_unchanged": true
  },
  "distances": [
    16,
    48,
    80,
    112,
    144
  ],
  "bins": [
    [
      1,
      32
    ],
    [
      33,
      64
    ],
    [
      65,
      96
    ],
    [
      97,
      128
    ],
    [
      129,
      160
    ]
  ],
  "B": {
    "families": 24,
    "discovery": 12,
    "heldout": 12,
    "wordings": 2,
    "versions": [
      "X",
      "Y",
      "XU",
      "YU"
    ],
    "target_pos": 239,
    "tokens": 240,
    "measure": "abs(cX-cY) - (abs(cX-cXU)+abs(cY-cYU))/2",
    "scale": "perfeature RMS of target contribution across all480 discovery sequences,including zeros; floor1e-8; no heldout scaling",
    "candidate": "rank positive normalized mean excess,top16 at16 and top16 at144;union in that order,no refill;>=4 discovery families with any target activation across versions/distances/wordings",
    "support_heldout_min": 4,
    "bootstrap": 5000,
    "test": "enumerate4096 family sign flips of(E-.10),one-sided,assumes symmetry; paired near-far uses(E16-E144-.10)",
    "minimum_effect_normalized": 0.1,
    "multiplicity": "one pooled BH family across both dictionaries,each selected feature five distances plus one near-far contrast; all eligible and ineligible hypotheses included(p=1 for missing)",
    "stable": "mean>.10,95%family bootstrap lower>.10,q<.05,>=4active heldout families at tested distance,and separate wording means>0",
    "far": "stable at144",
    "near_decay": "stable at16 and near-minus-far mean>.10,CI lower>.10,q<.05; far label takes precedence",
    "unknown": "all remaining candidates; far nonsignificance not absence"
  },
  "A": {
    "source": "unchanged120R04real192tokenwindows and original splits",
    "block": 27,
    "heads": 16,
    "queries": "seeded8 non-special nonpunctuation tokens with index>=160;max8; preselected without responses",
    "selection": "all non-special past positions in bin,N>=10;drop fully tied weights; sort(-weight,pos);topceil(.1N); middle ranks floor(.4N):ceil(.6N); greedy nearest control without replacement,caliper8tokens,exact same-token-ID-status and sourcepunctuation-status; no replacement of unmatched high pairs",
    "strata": [
      "different_word",
      "same_word",
      "different_punctuation",
      "same_punctuation"
    ],
    "aggregation": "within-query/head matched pairs equal;heads equal withinquery;queries equal withindoc;docs equal;feature averages equal includingzeros; missing strata stay NA,not zero",
    "primary_split": "original40heldoutdocs;discovery60 anddevelopment20 descriptive only",
    "groups": "reference low/middle/high (eligible>=20hits);low-supportseparate;thenBfar/near_decay/unknown/union andR04shared/math/bio roles",
    "reference_bins": "tercile quantiles on continuous eligibleDCLMrates;ties never split",
    "bootstrap": 2000,
    "test": "9999doc sign flips of(delta-.001),one-sided,symmetry assumption,seed20261028",
    "minimum_effect": 0.001,
    "min_documents": 10,
    "multiplicity": "one pooled BH across dictionaries,3frequencygroups+3Bcategories,5bins,2wordIDstrata,and individualBcandidate5bins*2wordIDstrata; missing p1; punctuation/R04role/allcandidate groups descriptive",
    "support": ">=10matched heldout docs,mean>.001,CI lower>.001,q<.05; include perfeature/query activation support",
    "attention": "capture lastblock rotatedQ/K at native SDPA interface; calculate selected-queryQKsoftmax with causal mask; return unmodified native SDPAoutput; engineering eager comparison before main results",
    "interpretation": "same-position native feature cooccurrence at endpoints; neither dictionary latent is an Attention value;no information-flow causality"
  },
  "crosslayer": {
    "layers": [
      1,
      3,
      5,
      7,
      9,
      11,
      13,
      15,
      17,
      19,
      21,
      23,
      25,
      27
    ],
    "raw_decoder_norm": true,
    "native_decoder_norm": "saved TRAIN_RMS_l*||decoder_lf||",
    "contribution": "shared z*native_decoder_norm",
    "reference_RMS": "raw representation vector-L2RMS on A discovery60 documents token32:192,one scale perlayer,fixed forheldout;independent of Btexts,not additionalDCLMfrequency",
    "normalized": "native contribution / raw reference_RMS_l",
    "summary": "mean heldoutBtarget X/Y sharedz at144;all distances available;one feature shape fixed by decoder norms,not independent layer activation"
  },
  "numeric": {
    "replay_rel_z_max": 0.02,
    "support_jaccard_min": 0.95,
    "prefix_h_rel_max": 0.01,
    "attention_weights_rel_max": 0.02,
    "attention_abs_max": 0.005,
    "SAE_nmse_mean_max": 0.15,
    "SAE_nmse_p90_max": 0.3,
    "CC14_nmse_mean_max": 0.3,
    "CC14_nmse_p90_max": 0.5,
    "failed_dictionary": "stop dependent branch,complete independently qualified branch;do not alter objects/gates",
    "checks": "2R04discoverySDPAcapture+2sameeagerlastblock+2Bbaseline+2Breplay+2visibleprefix=10;up to6 spare repairs within16"
  },
  "frozen_objects": {
    "model": "Qwen3-0.6B-Base",
    "SAE": "nativeE16block27MLPinputFP32Top32,F30000",
    "CC": "nativeA22oddblocks1..27residualpost14layerjointBF16encodedsharedz,F16384,savedgate.051281172782182693;notTop256inference",
    "input_length": 256,
    "reference_cache": "R04/forward/reference_{SAE,CC}.npz;65536positions,z>0",
    "model_hash": "cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba",
    "SAE_hash": "e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65",
    "CC_hash": "09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628"
  },
  "forbidden": [
    "training",
    "newresources",
    "newWorkCodextask",
    "sealedTEST",
    "intervention",
    "reclustering",
    "newreferenceforward"
  ]
}
```


## 原始数据在哪里

/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/forward 保存960条B全字典目标z和NMSE；120篇A逐token CSRz、查询Attention及层norm2。/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/data保存全文、线索、token与来源。/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analysis保存全部候选、尺度、家族/文档值、逐head匹配、检验与层贡献。/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/tables为CSV导出。没有模型权重副本。

候选、文本、配置与代码初始哈希在pre_forward_freeze；工程修复接受的代码哈希单独列，未改统计门槛。pre_heldout_freeze在第496次前向后、留出前保存。


## 各阶段重构资格（同各hook原尺度）

|阶段|读数|位置/层位置数|NMSE均值|p90|
|---|---|---:|---:|---:|
|B_discovery|SAE_MLP_input|115200|0.061958|0.095525|
|B_discovery|CC_joint14_reconstruction|1612800|0.102754|0.180351|
|B_discovery|CC_block27_reconstruction|115200|0.053152|0.083163|
|B_heldout|SAE_MLP_input|115200|0.060526|0.093283|
|B_heldout|CC_joint14_reconstruction|1612800|0.102428|0.179479|
|B_heldout|CC_block27_reconstruction|115200|0.052658|0.082112|
|A|SAE_MLP_input|23040|0.097742|0.192567|
|A|CC_joint14_reconstruction|322560|0.116479|0.209199|
|A|CC_block27_reconstruction|23040|0.091924|0.169015|

最后层NMSE是共享z重构最后层的误差，不是最后层独立编码资格。


字段说明：A表中的different_word/same_word实际按token ID是否相同判断，不按完整词或词义；数字、分词片段及空白可能属于非标点集合。层参考RMS只用于展示，未改变编码器的TRAIN归一化。V仅参与工程一致性验证，没有新增Value功能实验。


最初冻结的17份文件原字节另存frozen_sources，逐项通过原始SHA256。两份改过的代码由工程修复反向还原后验证与原哈希精确相同；当前实际修复代码另存，初始失败代码不能冒充最终运行版本。便携阅读副本会改写链接，原字节和便携副本分别有独立哈希清单。
