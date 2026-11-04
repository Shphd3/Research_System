# R19协议中文阅读

当前用户已直接授权完整有界SAE组合分析及小于20MB结果包，完成后停止；精确合同为[英文Protocol](protocol.md)，冻结于2026-11-04T04:39:28.471464+00:00。科学接受Unknown，无训练／激活干预。

## 文本和划分

292前缀＝144旧主＋48旧相反近处搭配＋96新匹配中性／同向＋4smoke。每个正式家族12行：主d16/64/128×事实A/B，加匹配d128×目标A/B×近处不明/A/B。384干净配对：固定近处改目标、固定事实主距离、固定远事实只改近处词。旧主与旧竞争的填充不同、旧竞争A/B同步改两处，另列48条混杂审计。全长320、p319；远e190，d=p−e−1两端排除。R18全部文件和旧Anchor／Focus保存哈希，不改。

24家族每个旧4家族模板分层前2发现后2留出，各12；同家族所有条件同行。模板在两侧共享，故只是新家族检验。行为已接触，新的留出feature直到候选和联合方向哈希冻结才前向。

## 模型、字典、频率

复用原模型、tokenizer及两处独立30000／Top32 SAE，FP32、CPU2线程、固定2×328。Attention是block27.o_proj残差前输出，MLP输入是post-attention归一化后实际输入。保存真实前缀／端点token、完整Top32 ID和值、cutoff32/33、h和decoder范数；零坐标由稀疏表示精确重建。旧原生完整候选评分重放<2e−5、capture无操作差0、lane差<1e−5、native与手工编码一致。

频率直接沿用原D1各字典300自然发现文档／38400位置，命中≥20且覆盖≥5文档才分档。Attention计数边界35/70，MLP输入33/62；同计数不拆组。高／中／低／不足／零全部保存，从旧原生缓存核验计数与分组，不重分到有利结果。

## 成员和强弱

发现主6行中每feature统计“一个家族六行都活跃”的家族数，≥8/12才能进共同候选。按家族数、归一化事实响应RMS、ID排序；主要固定前6，前3敏感性；至少3才分析组合几何。另选最多6个响应候选，要求≥6家族任一主行出现。严格几何保留全C正值的家族；H1／H3看全部匹配6行，H2看近远4行。至少8/12资格；不合格与全零保留，不用敏感性救回失败主检验。

层1保存全部384配对的交集、换入换出、原值和Jaccard及频率组。层2固定列表分别看原始z与L2相对q。不同家族A/B只是不同物品词，不拟合跨家族共同语义方向。H1比较固定近处A、B时的目标差与近处不明时目标差的方向；H2比较同家族主16→128的A−B差余弦；H3看“1−相反对角差在中性目标差上的投影保留量”与正确候选边际损失的家族Spearman相关。

匹配析因T＝固定近处词的目标A−B差平均；N＝固定目标的近处A−B差平均；I＝两种近处词下目标差的差。相反对角差恒等于T−N，同向为T+N；恒等式只是实现核验。保留T投影但判断错是当前观测量与输出分离，不证明一般目标信息仍在；完整候选分数包含后续token／句号，不能全归于p319。

## 超出单成员边际的检验

U为固定共同与响应列表的并集≤12。仅发现侧各选最多4二值对和4幅值对：至少一个条件中共同出现≥4家族，至少两个条件有非退化零模型变化；按六条件平均残差绝对值排序，正负均可，方向冻结。留出投影到发现残差方向；没有合格对就证据不足，不扩池。

二值Curveball复用S09 C++，每个条件／划分24行上严格保持全30000列出现次数和每行32。4链，burn100、thin10、每链64；检查全部边际、锁定成员、混合Rhat≤1.10／ESS≥100，必要时仅一次预定burn500／thin50重试。强制边际的常数轨迹不是支持。幅值参照在实际支持不变时，逐成员独立重排该条件的正值多重集合；保留出现次数和每行成员数，但不保留每行总幅值。联合强度为两成员各除发现RMS后的乘积，不用行归一化制造依赖。保存256零模型轨迹及逐家族贡献。

## 判定与停止

H1/H2：家族95%区间下界>0、精确家族符号交换经Holm6通过且≥8资格，才支持有界复现。H3还需平均组合损失和行为损失均为正、相关区间正及Holm6通过；中性匹配行为低于80%或资格不足则不足。只有组合变化而行为联系不够，最多局部支持。联合4检验另Holm4，必须零模型／支持合格。4096次家族bootstrap，9999次相关标签置换；六模板整组区间与模板内置换单列。两SAE独立，不据一边显著另一边不显著推位置差。

交付原始配对／稀疏激活／完整评分、固定候选、频率组、所有图、F23预选完整例与反例、中英报告、一个中文组会入口、<20MB可复算ZIP；大权重／大缓存仅路径清单。离线复算、ZIP CRC、解压逐文件SHA与便携链接验证。完成后STOP，等待研究者共同审阅；不自动干预或训练。任何协议修改须追加时间、旧新值、原因、已见数据、范围、授权及资格，保留原正文。

## Amendment A1 / 展示修正：2026-11-04T05:15:11.039407+00:00

After all heldout results were visible, corrected the case-display implementation: comparing only Tprojection sign missed opposite-diagonal counterexamples. Keep preselectedF23; show all heldout failuresF23/F27/F28and first successful nonpositive-diagonalMLPF11. Original figure code/selection are at `/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/evidence/presentation_v1`. Correct plot legend overlap/headroom and verify formal matched rows separately from smoke. No text/token,split,member,frequency group,contrast,null,test or primary verdict changed. This is an in-scope presentation/verification correction under the user's complete-analysis request, not a new experiment or scientific acceptance. Original complete Protocol bytes are preserved at `/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/evidence/pre_result_owners/protocol_cn.md` with the original freeze hash. Full visibility/scope are recorded in `evidence/presentation_amendment.json`.

全部留出已见后，修正只比较T符号而漏反例的展示实现。保留预选F23，另列全部失败F27/F28及首个非正对角仍正确的MLPF11；原展示、原协议字节与时间保留。图例/顶部空间、smoke验证范围属呈现与实现修正。未改文本/token、划分、成员、频率、比较、null、检验或主要判断；不增加实验或科学权限。
