派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/detailed_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/detailed_cn.md)；研究修改仍回到原件。

---

# W01实际执行记录

状态：有界权重分析完成，研究者逐图解释待讨论。原始表征protocol与冻结字节均保留；本轮新protocol记录权重对象与所有阈值。

实际执行：本机CPU4线程，GPU0；684矩阵状态；权重分解耗时529.2秒，跨checkpoint比较耗时20.4秒；57×23对×2侧=2622行配对结果；全谱700416行留执行侧；容差3078行。完整输入payload与内部token/step逐点核验，模型参数未更新、无forward。

原计划/实际对照：全部12可读点完成；全部57唯一二维权重完成；左右第一方向和前64空间均独立测量；所有九档容差完成；8个缺权重点未执行；单方向间隔不足标UNIDENTIFIABLE而非强行追踪；没有新训练重复或功能测试。只复用已有checkpoint和模型身份，未复用表征统计或分类器。

代码复用决定：沿用此前严格hash/计数及谱比较思想，适配新W的非中心化SVD；不把activation covariance当权重谱。每矩阵较小Gram为1024×1024，FP64 eigh给全部奇异值，另一侧仅恢复前65方向。测量代码与配置在正式分解前freeze；配对/绘图代码在其阶段前另存hash。一次绘图前表达修正增加不裁切的色阶上界与区分灰色含义，旧hash留在plot_freeze.previous；无数值或阈值改动。

可信度：smoke含真实0.5B Q直接SVD与恒等/符号/等谱旋转/近简并例；所有684cache哈希、维度、s1/能量通过独立检查；所有114末区间左右空间距离经等价投影公式重建；33B末层Q的两个奇异方程残差通过；3078个条件起点从原pair表重新计算一致。未对684逐个重跑独立全SVD；无独立模型重复。

没有文本采样，不能挪用原文档半集误差条或对权重条目bootstrap。第一方向5%间隔门槛是保守解释规则，不是数学上无法精确算出特征向量的声明。参数原坐标变化可能包含等效或协同重参数化，缺乏原生功能反事实。条件起点随容差变化而变化，不能包装成最终收敛时间。

数值、具体模块和允许解释见summary_cn.md及tables；代码/来源/protocol/缓存identity由artifact_manifest与freeze拥有。没有改划分、挑正例、增补GPU或为了得到正结论选择阈值。
