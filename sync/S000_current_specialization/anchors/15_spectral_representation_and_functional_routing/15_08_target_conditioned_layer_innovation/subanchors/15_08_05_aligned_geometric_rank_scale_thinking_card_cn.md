# A15_08_05 Thinking Card：对齐后的几何秩差异

Parent research direction or problem: A15_08 需要区分“对象本身的谱秩”与“目标相关新增可访问性的功能秩”。

Phenomenon: 我们在 Qwen3-8B、2,048 token、$r_{80}$ 下看到 $U$ 或部分 Attention 对象较集中；ZX/CAR 在 Qwen3-0.6B、约百万 token、$r_{90}$ 下报告数百维宽谱。

Mechanism guess: 差异主要来自 token 数、秩阈值和候选对象定义，而不一定来自模型大小。

Strongest rival explanation: 即使把模型、token 和 $r_{90}$ 对齐，Qwen3-0.6B 上 CAR、ZX 和 $R_U$ 仍不会形成稳定的对象间秩差；此前差异可能来自未记录的数据或实现细节。

Most uncertain point: 在同一 Qwen3-0.6B 和同一批百万 token 上，CAR、ZX 与 $R_U$ 的归一化 $r_{90}$ 是否仍显著不同。

Evidence that would change my mind: 用统一流式中心化协方差估计器得到收敛的 $r_{90}$，并显示 CAR/ZX 与 $R_U$ 没有材料性差异。

Current blocking uncertainty: 现有结果不能公平比较，因为模型、样本数、对象和 $r_{80}/r_{90}$ 同时变化。

Why this decision is needed now: 在讨论聚类、语义或 Router 前，必须先知道“低秩/高秩冲突”是否只是测量口径不一致。

Current next decision: 先不聚类；在 Qwen3-0.6B 上扩充 token，以 CAR、ZX 和 $R_U$ 三个对象统一比较 $r_{90}$。

Known source material: 0817 `feature (3).pdf`、0813 `subspace_token_clustering.md`、A15_08_04 E01。
