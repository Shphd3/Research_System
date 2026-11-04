派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/protocol_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/protocol_cn.md)；研究修改仍回到原件。

---

# 协议：Dense权重谱动态（W01）

这是用户明确要求的权重空间扩展，与原文本表征实验分开记录。原protocol保留。现有CPU4线程、GPU0、上限15分钟/3GiB；12个可读checkpoint×57独立二维权重＝684状态，8个缺权重点不插值。不训练、不做模型前向、不新增资源。

对每个原生W[输出,输入]计算不中心化SVD。覆盖embedding及8层Q/K/V/O、gate/up/down；共享输出embedding只计一次。一维norm增益列为排除。完整模块列表/维度/实际训练token见config和manifest。逐checkpoint核对payload哈希与内部tokens_seen/step，只加载一个后释放。

分别报告左右两侧：s1大小、符号不变第一方向夹角、前64维主角度及归一化投影距离，并报告相邻/距33B及实际每B变化率。保存全1024奇异值、前65个U/V、s1占总平方能量比例、1/2和64/65边界间隔、数值残差。无文本样本、无均值、无N−1；参数方向不等于表征方向或功能。

第一方向仅在两端(s1−s2)/s1>=5%且非零时可辨识；否则单向量角度标不可辨识，并补共同领先谱块。前64维边界接近数值误差标不可分辨，较小间隔保留排序切换警告。FP64较小Gram分解后恢复另一侧；已知恒等/符号/旋转/近简并检查与真实Q矩阵直接SVD交叉检查通过后运行。残差和正交误差均须<1e−8。

“何时趋稳”没有研究者给出的普适容差。预先冻结AI建议敏感性网格：s1相对大小变化1/3/5%、每B0.25/1/2%；第一方向5/10/20°、每B1/3/5°；前64维投影距离0.05/0.1/0.2、每B0.005/0.01/0.02。对每一原始阈值×速率阈值组合，找至少连续3个实测区间、持续到末端、同时满足两阈值且无后续反弹的最早起点；不可辨识区间不算通过。报告全部组合，不选能得到“收敛”的阈值。即使通过，也只称该窗口该容差下趋稳，不能称最终收敛；不满足或依赖阈值则报告未建立统一时点。

不对权重条目bootstrap：完整权重是研究对象，不是随机文本样本。单轨迹与训练重复不确定性仍缺失。不能从权重稳定推出语义/行为稳定，也不据方向运动判功能必变。配置、协议、代码在批量前冻结；缓存键包含checkpoint身份、模块、维度、预处理和代码配置，逐矩阵原子保存便于恢复。结果解释及研究者判断保持Unknown，待逐图讨论。

英文protocol.md拥有完整17节执行契约，中文保留同一对象、判据、预算与边界。
