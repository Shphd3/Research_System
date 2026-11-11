# 1109 汇报主线梳理（AI 分析，研究者判断 Unknown）

## 主线一句话
长尾信息学得慢，是因为它在每次更新里的信号太少、被随机梯度噪声淹没（结论 1）；所以分发的设计目标是让每条长尾信号在某个 expert 里“集中”（$\bar M$ 高）；teacher 分发没做到，原因在它的分组目标与这个设计目标不一致，又被硬性施加（结论 2 + 诊断）。

## 分发的设计目标（接在结论 1 之后）
对每个 feature $i$（尤其低频的），在负载均衡和每层容量的约束下：
- 覆盖率高：$i$ 的 token 尽量落进少数几个 expert；
- 纯度高：这些 expert 里少混与 $i$ 无关的 token；
- 不伤总体 NLL。
合起来就是让 $\bar M_i$ 高。由 $\pi_i(e)=c_i(e)p_i/q_e$（$q_e=P(e\in S_t)$ 是 expert 被选中的概率）可化简为 $\bar M_i=\frac1{Lk}\sum_l\sum_e c_i^{(l)}(e)^3/q_e^{(l)}$：它只取决于 $i$ 的 token 在各 expert 上堆得多集中。

## teacher 为什么没达到（D2、D3，探索性）
| 环节 | 数字 | 含义 |
|---|---|---|
| teacher 划分本身（Top-2，$b=0$） | $\bar M$ 中位数 0.697（随机 0.25；A0 单层 0.83–0.97） | 有集中，但每一层都不如原生 router |
| 划分严重不均衡 | Top-1 时 expert 5 拿 32% token、expert 7 拿 4.9%（均衡 12.5%） | 负载均衡必须大量改派 |
| load bias 改派 | bias 极差 0.136 ≫ 分数第 2/3 名差 0.036；$\bar M$ 0.697 → 0.586 | 很多 token 实际由 bias 而非 teacher 决定 |
| 8 层同一划分 | A1 每层 0.586；A0 每层 0.83–0.97，层平均后 1.010 | A0 各层集中不同 feature、互补；A1 没有互补 |
| 按频率看（最常用 expert 拿走的份额） | bin0：teacher 0.325 vs A0 0.351；bin9：teacher 0.386 vs A0 0.277 | teacher 把高频 feature 聚得更紧，把低频的聚得更松——与设计目标相反 |

根因（AI 判断）：teacher 是对整个 token 的 32 维编码做 8 类 K-means，相似度主要由高频 feature 决定，低频 feature 跟着各种上下文散到多个簇；这个目标 ≠ “让低频 feature 集中”。之后又被固定施加：不均衡导致 bias 改派，8 层共用一个划分，也不能被 LM 梯度修正。

## 汇报顺序（建议）
1. 问题与导师此前的问题；2. 结论 1：一步更新的帮助与噪声；3. 设计目标：$\bar M$；4. 五臂结果：NLL 随 $\bar M$ 排序；5. teacher 为什么不够：上表；6. 下一步与需要导师决定的事。

数据：`figures_tables/D2_*`、`figures_tables/D3_*`；脚本在执行侧 `analysis/meeting_1109/d3_root_cause_numbers.py`。
