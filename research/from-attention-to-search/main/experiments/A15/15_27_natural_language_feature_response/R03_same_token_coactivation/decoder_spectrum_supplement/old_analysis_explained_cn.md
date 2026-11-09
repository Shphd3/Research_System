# 先读懂旧分析：一条输入、两个feature、一个簇

我们把“哪些feature常在同一token一起活动”分组，再单独问前文编辑如何改变这些feature；没有用这条句子重新分组。

**输入与每token输出。** 实际执行S01_A_far的可见前缀是：

> A naturalist and an engineer use the same heading in a shared notebook. The entry is dated Tuesday. The subject was a wild bird with long legs and broad wings. An unrelated note records that the meeting began at nine. The printed page has a wide margin and a date in the top corner. The assistant checked the spelling in the heading and placed a small pencil mark beside the number. According to this account, the crane

末尾crane是token72947、零起始位置84，关键线索距它50token。B版本只把鸟描述换成“a tall machine with strong ropes and steel hooks”；U版本只改星期。模型在每个token产出各层隐藏向量；A22 CrossCoder把14个同位置的向量联合编码成16384维稀疏共享z。z是feature活动，不是每层独立读数。后文不能解释更早位置。

| 同一crane处的共享z | 鸟线索A | 机器线索B | 无关星期U |
| --- | --- | --- | --- |
| f12277 | 0.01908765 | 0.01139722 | 0.01859937 |
| f5409 | 0.03462873 | 0.04097639 | 0.03389631 |

**聚类输入究竟是什么？** 聚类点是feature，实际算法接收加权图；没有逐feature的句向量接口。在另一个参考语料的65464个位置，先记录每个feature是否z>0，再数共同活动。f12277活动1520次、f5409活动18574次、共同625次：在f12277活动时f5409的比例为625/1520=0.411184，减去f5409平时比例18574/65464=0.283728，得到有向增量0.127456。反向增量0.010430未过门槛；无向边取合格方向的最大值。

所以一条feature的“一串数字”是它与其他512候选坐标的边权行。f12277对f5409的一维为0.127456、对f1478为0.083712；每维代表另一feature，既不是decoder权重，也不是这条句子的编辑差值。完整非零行和源表见[旧说明](../artifact_manifest_cn.md)。

**为什么同组？** 两个节点都在冻结的校正共激活簇C03（72成员）。预处理要求双方各至少200次、共同至少20次、增量至少0.05；最大值对称化后按加权模块度贪心合并，resolution=1，保留至少3成员的社区。没有使用两feature向量的cosine，也没有预设簇数。f1478与f12277有边却在C02：边过门槛不等于同组，社区由全图决定。逐步合并轨迹未保存，不能事后编造某一条边就是原因。代码为`R03/offline/coactivation.py:35–63`，没有重新执行。

| 名称 | 实际关系 | 本次能否混称 |
| --- | --- | --- |
| 原始共激活簇R | 高条件共现概率构图后分社区 | 不能与C混名；C先扣除节点基准率 |
| 校正共激活簇C03 | 超基准共激活边构图后分社区 | 本例真实簇；不是“语义第三级” |
| 上下文变化响应簇G02/G04 | 旧E16字典上编辑差值轨迹的相关距离、平均连接层次聚类 | 不同字典、不同关系；不是C03 |
| decoder方向几何簇 | 按decoder向量夹角分组 | 本任务从未构造，本补测也不构造 |

**图说明什么？** 图边说明参考语料中的共同活动关系；图3另外画固定C03在近远编辑中的成员变化幅度。这里两个成员同簇，鸟→机器时一个下降、一个上升，已经是“同簇不等于同向响应”的真实反例。人物案例R01中贡献坐标cosine为0.99655、B却偏好错误人名，又说明高相似不保证关系理解正确。旧token目标细图的top12均在512候选外，不能把那12行当作C03成员。

只允许说：参考共激活分组中的部分坐标会随可见前文变化。不能说整簇表达整句、方向相似已经成立、长程专属、图箭头传递信息或已证明专家。f12277与f5409的decoder方向是否相近，留给随后真正的新测量。

来源：[实际例子](../examples_cn.md)、[完整边表](../tables/edges_D_frozen.csv)、[冻结组成员](../provenance/observed_graphs.json)。数字由既有NPZ/CSV读取；没有新模型前向、训练或聚类。
