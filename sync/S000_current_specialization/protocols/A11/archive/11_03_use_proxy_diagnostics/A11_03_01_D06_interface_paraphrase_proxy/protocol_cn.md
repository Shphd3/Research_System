# A11_17 接口 × 同义迁移方向分解实验协议

只跑五条 NTP 轨迹，完全复用 A11_16 的 Qwen3-0.6B、任务、H2 初始化、训练目标、优化器、seed、batch 和 checkpoint。

固定一个训练 H2 loss 的共享梯度 $g_D^S$，分别计算四个方向有效性：

$$
U_{2,tr},\quad U_{2,ev},\quad U_{1,tr},\quad U_{1,ev}.
$$

- H2-train：直接监督是否帮助自己的训练 margin；
- H2-eval：同一 H2 方向是否泛化到未见改写；
- H1-train：是否能跨到标准 H1 与后一位置；
- H1-eval：完整下游传递，复现 A11_16。

每项都使用：

$$
\widehat U_{a,s}
=-\frac{\langle\nabla M_{a,s},g_D^S\rangle}
{\|\nabla M_{a,s}\|\|g_D^S\|}.
$$

在 `0,20,100,200,300` 测量；用相对范数 `1e-6` 的中心差分同时验证四项符号，并精确恢复参数。若 H2-train 正、H1-train 负，定位为接口/位置瓶颈；若同一接口 train 正、eval 负，定位为同义迁移瓶颈；若 H2-train 本身负，则先审计 full-vocabulary CE 与二元 margin 的多类几何。

该实验不增加方法、K、任务或 loss 权重，也不声称全局 MTP 效率。
