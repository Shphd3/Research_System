# R17_D1

[English Summary](summary.md) · [中文总认识](summary_cn.md) · [Detailed](detailed.md) · [完整方法](detailed_cn.md) · [Corrections](corrections.md) · [Cases](casebook_cn.md) · [Data](dataset_guide.md) · [Verification](verification.md)

Eight native-SAE hypothesis cells and separate correctedCrossCoder reference are complete. Scientific acceptance/closure remain Unknown. Original R17 retained.

- ATTN_SAE：[H1](ATTN_SAE/H1/conclusion_update.md) · [H2](ATTN_SAE/H2/conclusion_update.md) · [H3](ATTN_SAE/H3/conclusion_update.md) · [H4](ATTN_SAE/H4/conclusion_update.md)
- MLPIN_SAE：[H1](MLPIN_SAE/H1/conclusion_update.md) · [H2](MLPIN_SAE/H2/conclusion_update.md) · [H3](MLPIN_SAE/H3/conclusion_update.md) · [H4](MLPIN_SAE/H4/conclusion_update.md)
- CC_CORRECTED：[H1](CC_CORRECTED/H1/conclusion_update.md) · [H2](CC_CORRECTED/H2/conclusion_update.md) · [H3](CC_CORRECTED/H3/conclusion_update.md) · [H4](CC_CORRECTED/H4/conclusion_update.md)


## 受控小例子第一步：明确奇异性（S01）

目的：先确认模型在性质直接写出时的原生判断。数据为12家族×方阵／奇异方阵／可逆方阵共36英文文本。复用同一冻结0.6B Base，两套预定三候选完整序列评分，无长度／先验校正、无分类器。结果：F1 13/36、F2 12/36；同条首选一致1/36。详细[中文小结](controlled_steps/S01_explicit_singularity_36/summary_cn.md)和[逐家族分数](controlled_steps/S01_explicit_singularity_36/casebook_cn.md)单独记录。只完成原生行为第一步，下一步NOT_RUN，等待研究者共同审阅；R17 D1旧结论不变。


## 受控小例子：普通语言猫狗续写（S02）

S01方阵格式出现近似固定答案偏好后，按用户指定改做6组animal+cat/dog配对共12英文文本，只有一种固定续写后缀及` cat.`/` dog.`两个完整候选，另1个中性前缀。不调整原模型、不做先验／长度校正。结果12/12正确，6/6组切换、6/6组两条都对；中性首选dog。[本步中文小结](controlled_steps/S02_animal_cat_dog_12/summary_cn.md)和[完整12条分数](controlled_steps/S02_animal_cat_dog_12/casebook_cn.md)独立保存。S01原件SHA保持；本步成功仍可能只是复制，不改H1–H4，也不自动进入feature分析。状态：完成S02，等待共同审阅。


## 受控小例子：动物猫狗的H1／H2描述（S03）

用户在S02原生续写12/12后授权本步：原12条猫狗保持，加入P（animal、细类未知）与N（chair）共24条；F01–03探索、F04–06只检查固定候选。两套原生冻结SAE分别读取末尾` a`，候选先冻结再开放检查。观察到共同成员及换入换出、固定列表内比例变化，也保留未复现候选。两接口H2选定6成员支持相同均6/6对，全字典支持相同均0/6对；原H1/H2额外信息与功能未验证，N后缀与指代词差异仍是竞争解释。[中文小结](controlled_steps/S03_animal_H1_H2_24/summary_cn.md) · [24条全文](controlled_steps/S03_animal_H1_H2_24/data_casebook_cn.md) · [完整值与失败](controlled_steps/S03_animal_H1_H2_24/README.md)。S01/S02全部保留，不改假设；仅本步完成，等待共同审阅，不自动继续。


## 受控小例子：统一中性后缀与固定候选（S04）

用户授权在S03后只做下一小步：24正文/标签不变，四条件后缀统一为Description:，沿用两套原SAE和全部冻结候选，不筛选/训练/干预。新末尾冒号ID25，旧space-a ID264，完整语境变化不隔离单个词。原模型猫6/6、狗6/6、配对6/6切换；固定候选大量未再进入Top32，ATTN #14602猫狗全不激活，#3516仅F03/F05双侧激活且相对各自旧归一化方向反向；相对S03冻结探索方向另列。原H1/H2额外信息未验证。[中文小结](controlled_steps/S04_neutral_suffix_fixed_candidates_24/summary_cn.md) · [24条与原始分数](controlled_steps/S04_neutral_suffix_fixed_candidates_24/data_casebook_cn.md) · [指定两原子完整案例](controlled_steps/S04_neutral_suffix_fixed_candidates_24/focused_14602_3516_cn.md)。旧S02/S03原件保持；S04完成后停止，等待共同审阅；不做SVD或后续实验。


## 受控小例子：AC/AD总体方向与父类细类配对几何（S05）

用户授权在已完成S04中性后缀缓存上做本小步，无新模型前向。AC/AD各6×30000探索矩阵独立中心化；只用F01–03拟合均值、前1/2方向与前5系数成员，F04–06仅投影。两字典独立，原始及decoder范数加权尺度均报告。原始PC1绝对余弦Attention0.866、MLPIN0.963，前二维重叠0.726/0.931；探索均值猫−P/狗−P有向余弦0.754/0.773。第一轴大部分投影平方和来自家族中点间变化，不能当作父子差方向；F05沿自身AC第一轴的猫−P分量两接口均反号。成员强弱/支持更替、27成组bootstrap、完整谱/文本/成员值与失败均保留。[中文小结](controlled_steps/S05_AC_AD_svd_paired_geometry_24/summary_cn.md) · [Detailed与反例](controlled_steps/S05_AC_AD_svd_paired_geometry_24/detailed_cn.md) · [完整输入](controlled_steps/S05_AC_AD_svd_paired_geometry_24/data_casebook_cn.md)。仅候选几何现象，原H1/H2不改，未作语义/功能/因果确认。旧S03/S04保持，S05完成后停止等待审阅。
