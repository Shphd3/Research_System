# 三张主图的证据、单位和读法

共同设置：原生普通8层MoE33B训练token、同一末层router输入SAE；旧CONF显式冒号1152位置、48家族16场景24类。图均为实际测量，后写绘图不冒充预注册。

| 图 | 源表、分母与单位 | 汇总/观察 | 最大结论与边界 |
| --- | --- | --- | --- |
| 01_frequency_and_roles | frequency_ecdf、role_frequency_joint、sharing_range_frequency；成员权1或实际36,864激活事件；Q/G频率0–1 | 上CDF保留0，symlog展开低频，inputevents=E6恒等；下角色确切交集和G频率×DEV标签使用范围 | 共同接触的输入组成；不能推高频压低频或知识长尾。0覆盖标签是未达DEV阈值，不是成员未出现。expert7仅23位置 |
| 02_enrichment_and_alignment | candidate_enrichment与fixed_pair_alignment；左P(feature|expert)-同类比例背景的百分点，显示9对DEV端点，完整53/全坐标表保留；右DEVφ与CONFTV×100 | 左全部对照不合格，E6为恒等0、E7原始大差；右圈硬ID、方gate，颜色高/低DEV固定组 | 原始差不是显著性；不把9边当独立实验。低相似仍硬共路由，但权重可变，不能称完全无组织或学习损害 |
| 03_input_overlap_and_support | expert_overlap、main_route_exceptions、leave_one_scene_and_family；实位置数 | E1独有0/共同1129/E6独有23；22N029、1N051fork；16场景LOSO剩余N1080 | 两expert接收相同样本是重复输入，不是语义相似发现；不代表expert函数相同、整个模型坍缩或计算无用 |

三PNG已实际打开核查。图一图例初稿覆盖柱面、图二高相似标签接近，做一次布局修复后重新查看；数值与已冻主代码不改。SVG与PNG同源，未声称所有外部阅读器渲染验证。body四条件仅列表，不用冒号参考图替代正文原生分析。所有图的生产者code/figures.py和源表摘要在artifact_manifest。
