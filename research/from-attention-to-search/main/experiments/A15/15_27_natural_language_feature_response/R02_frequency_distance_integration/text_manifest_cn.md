# R02文本清单：构造、配对与位置

12基础情境全部为人工自然语言构造和受控编辑。R01发现和旧留出均已暴露；新面板只是独立措辞/实体的确认候选，不是未修改自然语料。由于前缀数值资格失败，新增响应不能作为确认性证据。

每例00/10/01/11四组合，各有short/long；另有11_short_position_control和11_short_unrelated，共10条。00是基准，10仅改线索一，01仅改线索二，11联合改变。距离只指线索二结束至最终目标开始的token间隔；线索一的精确间隔在逐序列原件另列。近远最终长度、绝对位置及末五token匹配。阶段一/二的近远绝对位置不同，阶段分析只用short。相同token才直接比较。所有位置从0计。

| 案例 | 关系 | 实体 | 短版三个目标位置 | 长版三个目标位置 | cue2近/远间隔 | 续写候选 |
| --- | --- | --- | --- | --- | --- | --- |
|B01|word_sense_selection|Wrenford|90,106,111|48,64,111|6/48|' swims', ' sounds'|
|B02|word_sense_selection|Oakmere|92,106,111|50,64,111|6/48|' swims', ' sounds'|
|B03|word_sense_selection|Hillcross|99,115,120|57,73,120|6/48|' swims', ' sounds'|
|B04|word_sense_selection|Pinevale|93,108,113|51,66,113|6/48|' swims', ' sounds'|
|B05|word_sense_selection|Ridgehaven|95,109,114|53,67,114|6/48|' swims', ' sounds'|
|B06|word_sense_selection|Fairbridge|92,106,111|50,64,111|6/48|' swims', ' sounds'|
|P01|person_attribute_binding|Westhaven, Alice, Ben, Clara, Dylan|117,131,136|75,89,136|7/49|' Alice', ' Ben', ' Clara', ' Dylan'|
|P02|person_attribute_binding|Elmstead, Olivia, Oscar, Emma, Jack|118,132,137|76,90,137|7/49|' Olivia', ' Oscar', ' Emma', ' Jack'|
|P03|person_attribute_binding|Brookstone, Nina, Noah, Lily, Luke|119,133,138|77,91,138|7/49|' Nina', ' Noah', ' Lily', ' Luke'|
|P04|person_attribute_binding|Northwick, Grace, Henry, Julia, James|119,133,138|77,91,138|7/49|' Grace', ' Henry', ' Julia', ' James'|
|P05|person_attribute_binding|Clearwater, Anna, Adam, Laura, David|119,133,138|77,91,138|7/49|' Anna', ' Adam', ' Laura', ' David'|
|P06|person_attribute_binding|Meadowbank, Rose, Ryan, Sofia, Simon|118,132,137|76,90,137|7/49|' Rose', ' Ryan', ' Sofia', ' Simon'|

词义选择的目标是bass/ID21529，人物交叉指认的目标是is/ID374；两类型单列。bass候选只是词义兼容读数，不是唯一正确下一词。第一位置只使用可见线索允许集合，不用尚未出现的第二线索标签。模板/sourcegroup/entitygroup按基础案例整体隔离，不能将变体拆成独立样本。相同词bass为旧轮已知选择；未按本轮结果选文。

[完整120条文本、token切分、offset、线索、候选和配对](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/tokenized_sequences.jsonl)；[12例包含全部版本的原件](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/qualified_cases.jsonl)；[事前排除与改写记录](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/exclusions.json)；[事前资格](provenance/text_qualification.json)。原文SHA256为`a172212a9f7840ca63a8e84324a5ba01dde129083e80b8ddaae196713eb3e203`。这些原件保留执行侧，不复制原始JSONL到System。
