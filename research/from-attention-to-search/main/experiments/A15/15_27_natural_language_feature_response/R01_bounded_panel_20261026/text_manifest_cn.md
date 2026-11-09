# 文本清单：A15_27 R01

完整文本、配对和精确 token ID 由 [qualified_cases.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/qualified_cases.jsonl) 与 [tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/panel/tokenized_sequences.jsonl) 保存；首次前向前已冻结原始字节。[72案例索引](case_index.csv) 和 [token资格](provenance/qualification.json) 可核查模板、来源组和实体组合的分割。英文指南 [text_manifest.md](text_manifest.md) 逐字展示 A01/B01/C01 的预固定原文。

三类各24基础案例，发现／留出各12，每例4版，共288前缀，最长77token。所有文本是Codex助手构造的自然语言与受控编辑，不是未经修改的真实语料。单一样本由目标位置与其可见前缀组成，不提供后文。发现／留出不共享模板、实体组合或来源组；单一构造过程仍限制跨作者及真实语料外推。

A改变局部搭配；少数a/an随语法改变，不能声称只替换一个词。B改变前文明确词义线索并保持目标局部措辞。C移动同一中性块，保留线索与目标；近远四版同长度、同目标位置和ID。距离定义为保存的完整线索span末端与目标之间的token数：近1，远40/41/45/46；线索宽度另存。句序与距离同时变化。

B/C的候选下一token是事前固定的语义兼容性诊断，没有唯一正确后文，不代表理解成功。A无可靠标签，保留NA。排除条件在观察feature前记录。独立参考频率来自历史DCLM TRAIN discovery的261632位置，不是本面板命中率；历史骨干哈希缺口与BF16/本轮FP32编码差异一并限制频率匹配结论。

唯一清单SHA256：`945914b9007a4a576f6de99b00b791af56e8daf4464de9169959e733b20d2246`。[前向前冻结记录](provenance/pre_forward_freeze.json) 同时绑定协议、文本、代码与参数。
