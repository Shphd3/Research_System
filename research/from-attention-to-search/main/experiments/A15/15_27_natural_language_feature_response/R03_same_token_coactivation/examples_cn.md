# 固定句子的正例、反例与原图边界

[完整统计](detailed_cn.md)说明资格。以下两个句子在响应前固定；具体展示坐标由固定案例中C03的最大相关减无关分量事后挑出，只解释实例，不作feature层面的新确认。

## S01：词义兼容读数正例

目标 `crane`，token ID72947，零起始位置84，线索间隔50。C03的f12277：A/B/U共享z为0.01908765/0.01139722/0.01859937；D尺度的B−A为-2.0658，无关变化-0.1312。72成员中仅4个变化，不表示整簇意义。

A可见前缀：

> A naturalist and an engineer use the same heading in a shared notebook. The entry is dated Tuesday. The subject was a wild bird with long legs and broad wings. An unrelated note records that the meeting began at nine. The printed page has a wide margin and a date in the top corner. The assistant checked the spelling in the heading and placed a small pencil mark beside the number. According to this account, the crane

B可见前缀：

> A naturalist and an engineer use the same heading in a shared notebook. The entry is dated Tuesday. The subject was a tall machine with strong ropes and steel hooks. An unrelated note records that the meeting began at nine. The printed page has a wide margin and a date in the top corner. The assistant checked the spelling in the heading and placed a small pencil mark beside the number. According to this account, the crane

A/B的flies/lifts兼容候选边际分别+5.1875/+0.5625，均为正；全贡献坐标cosine=.92162。f12277贡献了本例约86.25%的C03平方变化，但未被功能验证。

## R01：高相似但人名不对应的反例

目标 `was`，token ID572，零起始位置82，线索间隔51。C03的f2174：A/B/U共享z为0.04339544/0.04241887/0.04315130；D尺度的B−A为-0.2028，无关变化-0.0507。72成员中仅4个变化，不表示整簇意义。

A可见前缀：

> A delivery log records one parcel and two people waiting in a hallway. The entry is dated Tuesday. The courier handed the parcel to Nora instead of Felix. An unrelated note records that the meeting began at nine. The printed page has a wide margin and a date in the top corner. The assistant checked the spelling in the heading and placed a small pencil mark beside the number. According to this account, the recipient was

B可见前缀：

> A delivery log records one parcel and two people waiting in a hallway. The entry is dated Tuesday. The courier handed the parcel to Felix instead of Nora. An unrelated note records that the meeting began at nine. The printed page has a wide margin and a date in the top corner. The assistant checked the spelling in the heading and placed a small pencil mark beside the number. According to this account, the recipient was

A/B目标贡献坐标cosine=.99655，但Nora/Felix预定候选边际为+0.875/−0.875；B仍偏Nora。高整体相似和feature变化不能替代人物关系成功。

## 原图与命名的反例

f13964基准活动率约99.3%，15469条旧入边都不够delta=.05；这不证明它无功能。C03中f14035曾在context3356/token769的“ in”单独活动，其余71成员未活动；community不要求每次全员出现。原逐句pooled-max图又被首token主导，目标12坐标全零；目标细节附图说明其他坐标确实改变。三个反例分别约束条件概率、群体命名与幅度展示，不拼成同一机制。

[原始例值与未执行预测](provenance/worked_examples.json)保存精确z、贡献、参考支持、前缀与剂量；所有语义解释止于目标位置。
