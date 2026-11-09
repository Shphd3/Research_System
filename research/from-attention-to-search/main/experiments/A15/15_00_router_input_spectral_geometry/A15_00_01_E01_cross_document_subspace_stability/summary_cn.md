# 结果摘要：去均值后的公共子空间是否跨文档稳定

## 结论

去均值后的 Router 表征不是一组彼此无关的 batch-local residual。无论 LB
还是 decommon，在一组 DCLM 文档上拟合的 centered top-64，都能在独立文档
上稳定捕获远高于随机 64 维方向的变化。独立 pooled top-64 被移除后，local
residual top-64 也能跨文档迁移，但一致更弱。

因此，“减均值后只剩不稳定残差、模型没有完整学习方向”这一强假设被否定。
成立的较窄结论是：去均值后仍有稳定的中心化共同成分，它能迁移更多 held-out
能量；而直接比较 projector 后，局部 residual 的方向本身也高度共享。

这里的跨文档迁移量表示：在源文档拟合的方向，能在未见目标文档中解释多少
中心化变化，并减去同维随机方向的 95% 分位。正数表示超过随机；两者之差为
正，表示 pooled top-64 更稳定。

| 谱系 | 步数 | pooled top-64 | local residual-64 | pooled 多出的迁移量 | 95% 区间 |
| --- | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 0.584 | 0.409 | 0.162 | [0.158, 0.165] |
| LB | 80k | 0.564 | 0.392 | 0.167 | [0.161, 0.169] |
| decommon | 40k | 0.600 | 0.414 | 0.179 | [0.175, 0.182] |
| decommon | 80k | 0.580 | 0.402 | 0.176 | [0.172, 0.179] |

![centered top-64 与 local residual-64 的跨文档迁移](figures/centered_common_vs_residual_transfer.png)

四个保留 endpoint 的 12/12 层均为：pooled 稳定、residual 也稳定、pooled
更强。2,000 次文档 bootstrap 与全部对象、重放、平移不变性、rank、样本量
和数值护栏均通过。按研究者执行修订，30k 不进入结论。

projector overlap 直接比较两个64维空间是否占据相同方向：

\[
O_{s,t}=\frac{\|U_s^\top U_t\|_F^2}{64}.
\]

\(O=1\) 表示两个 projector 完全相同。768维完整空间的匹配随机 q95 为0.086；
704维 residual complement 中为0.094。

| 谱系 | 步数 | centered-top overlap | residual overlap |
| --- | ---: | ---: | ---: |
| LB | 40k | 0.791 | 0.729 |
| LB | 80k | 0.766 | 0.719 |
| decommon | 40k | 0.784 | 0.730 |
| decommon | 80k | 0.760 | 0.704 |

因此，两种 projector 在随机文档 shard 间都高度重合。centered top 的模型级
overlap 只高约0.04--0.05，部分层甚至不高于 residual。前面的能量迁移差不能
解释成“residual 具体方向随 shard 接近随机地旋转”。

## 边界

这里的 “common” 只表示统计上的跨文档稳定，不等于语义 common 或功能有益。
本实验不能证明 residual 无语义、稳定性导致 decommon 的训练结果，或 pooled
成分应被保留/删除。当前 shard 是随机 hash 混合文档，不是语义条件；它不能
排除“全局 residual envelope 中仍有条件特异低维模式”。下一决策是在任何
匹配训练前，是否按 domain/topic 构造条件化 shard，同时测 projector overlap
与 cross-capture。
