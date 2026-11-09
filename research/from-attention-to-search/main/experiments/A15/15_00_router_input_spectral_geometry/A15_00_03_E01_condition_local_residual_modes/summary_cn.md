---
experiment_id: A15_00_03_E01_condition_local_residual_modes
status: complete_pass_conditional_modes_shared_envelope
completed: 2026-07-31
canonical: summary.md
---

# 摘要：按领域分层后的 residual projector

## 结论

Residual 几何有两个尺度。把很多文档按 domain/topic 聚合时，basis 高度共享，
同时存在小而可复现的条件旋转；每篇文档各自拟合 projector 时，精确低维模式
会明显随文档改变。因此当前最准确的认识是：**文档局部模式位于一个广泛共享的
residual envelope 内，domain/topic 只解释其中一小部分旋转。**

条件聚合层面，同 domain rank-64 overlap 为 0.754--0.777，跨 domain 为
0.698--0.725；跨 domain basis 仍保留同 domain capture 的 95.1%--96.4%。
文档层面，residual rank-64 overlap 降为同 domain 0.301--0.308、跨 domain
0.295--0.302，但仍远高于 Haar q95 0.094。跨 domain capture 是同 domain 的
97.8%--98.1%，却只达到目标文档自身最优 rank-64 capture 的 32.7%--34.1%。

这不是 128-token 估计噪声造成的假象：同一文档两个不相交 token 半区的
residual rank-32 overlap 为 0.516--0.534；同 domain 不同文档只有
0.173--0.181，跨 domain 为 0.168--0.177。

centered top/common 在两个尺度上都比 residual 更可迁移。因此实验支持弱化的
A14 式“局部模式混合”，但不支持“去掉 common 后得到互不兼容的领域空间”，
也不支持粗 domain 标签已经确定每个局部模式。

## 决策证据

| 条件层级 | residual within overlap | residual cross overlap | 跨条件/同条件 capture | 说明 |
| --- | ---: | ---: | ---: | --- |
| Domain，四端点范围 | 0.754--0.777 | 0.698--0.725 | 0.951--0.964 | 条件改变具体方向，但跨条件迁移仍强 |
| Topic，四端点范围 | 0.673--0.700 | 0.615--0.646 | 0.922--0.938 | 更细标签重复同一方向 |
| 单文档 rank-64 | 0.301--0.308 | 0.295--0.302 | 0.978--0.981 | 精确模式随文档变；跨领域与同领域几乎同样可迁移 |

四个端点的全部 12 层均满足 within-minus-cross gap 为正、cross-capture 超过
complement-Haar q95。实际 Gate 输入重放误差为 0，top-1 一致率为 1.0。

![Residual 模式位于共享 envelope 内](figures/condition_overlap_and_cross_capture.png)

![单文档模式变化与共享 envelope](figures/document_projector_overlap_and_capture.png)

## 边界

本结果只建立 WOS 标签分组下的表征几何。文档级估计仍包含有限 128-token
误差，但 split-half 表明这不是主要原因。它不能证明标签是语义因果变量或条件
residual 路由能改善训练；独立 2B 匹配实验已显示路由改变但 NLL 无收益。

完整证据见 [detailed.md](detailed.md) 与
[条件汇总表](tables/condition_stratified_summary.csv)和
[文档汇总表](tables/document_projector_summary.csv)。
