# 结果摘要：Gate 偏 pooled common 还是 local residual

## 结论

把每个方向放到相同输入能量后，LB 与 decommon 的 Gate 仍给独立 pooled
centered top-64 更大的专家间分数增益，而不是同维 shard-local residual。
拿掉 pooled 方向也会更强地削弱原生获胜专家的 margin。因此这不是输入能量
更大或 Gate 任意各向异性造成的表象。

结合 A15_00_01，允许的结论是：

> 在 40k 和 80k，模型级 Gate 更依赖跨文档稳定的中心化共同成分，而不是较弱
> 迁移的局部 residual。

“等能比”表示给两组方向同样的输入能量后，Gate 每个方向造成的专家间分数
平方变化之比；它排除了大特征值方向天然能量更大的加成。“margin 差”表示
删除 pooled 而非 local residual 后，原生获胜专家多损失多少 logit/token。

| 谱系 | 步数 | pooled/local 等能比 | 比值 95% 区间 | 多损失的 margin | 95% 区间 |
| --- | ---: | ---: | ---: | ---: | ---: |
| LB | 40k | 3.94× | [3.70×, 4.20×] | 1.873 | [1.857, 1.919] |
| LB | 80k | 4.55× | [4.30×, 4.92×] | 1.953 | [1.931, 1.994] |
| decommon | 40k | 2.83× | [2.64×, 3.06×] | 1.998 | [1.948, 2.046] |
| decommon | 80k | 3.08× | [2.83×, 3.34×] | 2.061 | [2.011, 2.120] |

![Gate 等能偏好与原生路由依赖](figures/pooled_vs_local_gate_preference_and_use.png)

所有模型级结果均超过保持 Gate 奇异值的 orientation-null q95。LB 为 12/12
层；decommon 为 11/12 层，第 12 层是明确例外，因此结论是模型级而不是每层
普遍成立。margin 差在四个 endpoint 的 12/12 层均为正。全部对象、重放、
rank、SVD、wrong-layer 和数值护栏通过；30k 按执行修订不进入结论。

## 边界

这只证明当前 Gate 的权重几何与原生路由依赖，不能证明 pooled 方向有语义、
能让专家训练更好，或 residual 无功能信息；也不能把 LB/decommon 差异因果
归于 centering。下一决策是是否做匹配训练，直接比较稳定 residual 坐标与
shard-local residual 对更新冲突和 held-out loss/FLOP 的影响。

