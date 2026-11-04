# 第一条结论：组会图与可直接粘贴文字

先读report_insert_cn.md；两张PNG在figures，可直接插入报告。SVG为文字可编辑源图，*_outlined.svg为字形转轮廓的保真备份，PDF为矢量备份。plot.py与data/可完全重绘；无需模型。若另一台机器没有原中文字体，请用--font指定可用中文字体。字体文件不随包分发。

图一六个均值已从S06稀疏激活集合独立复算；误差线由原8个家族各柱均值新算，不是原主配对差区间。图二是原显式留出F09，Attention输出、同一末尾冒号；an animal/a cat冠词也变，24保留/8换出/8换入。自然补证仅使用S08原数据与S09的自然数据频率零模型，未将后者用于层级实验。

reading_notes_cn.md包含读图顺序、口头讲述与两项Q&A；natural_supplement_audit_cn.md保留自然数据全部6项数值与零模型比值。原模型/SAE/缓存和原实验报告不变，没有重新筛选候选、模型前向或新实验。

重绘：python plot.py --font /path/to/中文字体.otf
原始数据核验：prepare_data.py需要本地原S06/S08/S09源路径；导出的CSV/JSON已经足够独立重绘。evidence/data_verification.json与figure_origin.json记录来源、SHA、分母、种子和显示区间的派生性质。
