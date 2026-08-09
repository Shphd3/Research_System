# A15_00_03 Thinking Card：带标签条件下的 residual 模式

- **当前判断：** 随机文档分组把多个领域混在一起，因而会把“条件变化但仍位于同一 residual envelope 内”的低维模式平均成一个看似稳定的 residual 子空间。
- **机制理由：** 同一 domain/topic 内，残差 projector 应比不同 domain/topic 之间更重合；不同条件的具体 projector 即使不重合，也可能仍能迁移捕获彼此的 residual 能量。
- **最强 rival：** residual projector 本身就是跨语义条件共享的；此前的高 overlap 不是随机分组造成的。另一个 rival 是每组样本不足，within 与 cross 都低。
- **会改变判断的证据：** 在真实标签上同时测同条件半分片 overlap、跨条件 overlap 和 cross-capture，并超过标签置换、随机匹配分组与 Haar complement 对照。
- **下一决策：** 若出现“within overlap 高于 cross overlap，但 cross-capture 仍超过随机”的模式，把 residual 更新为“共享 envelope 中的条件低维模式”；否则保留全局共享 residual 的认识。

