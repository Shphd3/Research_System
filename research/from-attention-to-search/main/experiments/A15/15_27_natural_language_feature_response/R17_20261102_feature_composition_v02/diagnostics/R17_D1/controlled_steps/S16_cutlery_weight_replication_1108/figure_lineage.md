# S16 图证据与实际渲染核查

共同设置：同一普通8层MoE33B训练token／原生末层SAE，最终冒号；新24场景×2家族，两表达各96文本。英文图注稳定绘制，中文Summary逐图定义。图一是示意，其余为实际数据。

| 图 | 问题与源数据 | 单位／汇总／读法 | 允许结论及边界 |
| --- | --- | --- | --- |
| 01_analysis_structure | h如何同时接SAE和实际router；来自冻结protocol/config，非测量值 | 一条输入分成两平行支路，合流到逐成员条件均值与Q3；下方为null与资格检查 | 解释计算，不是SAE驱动router的机制图；未训练或干预 |
| 02_replication_contrast | 旧餐具候选是否在新条件复现；旧S15gate表、新results/replication.csv | TV×100；蓝点、2000场景原TV区间；橙条件null均值；空心为覆盖/行为不足 | 新显式1.808vs1.923null；新改写3.738vs1.928；旧6.511是探索候选，不代表已全校正确认；CI不是null差值CI |
| 03_member_coverage | 固定八成员有没有足够新场景支持；results/member_expert.csv目标侧 | 左48家族，右24场景；虚线各12；蓝圆显式，橙方改写；两项都达标才实心；组门槛80%另由结果表判断 | 显式0/3和1/5；改写1/3和1/5；不能删除稀有成员后自称复现 |
| 04_category_baseline | 成员组差异中类别总体负载有多大；category_loads/group_profiles | expert6百分比；各类48token普通均值vs固定成员等权条件均值；全部token为1/6，E1为余量 | 类别差1.584pp，成员差1.808pp；描述性，不等于成员因果贡献或完整组已可靠 |

已实际打开四张PNG检查。首次图二/四脚注与横轴靠近、图三共享纵轴被重复反转，已预留底部空白并只反向一次；修后再次打开核查。数值和主代码不改。PNG/SVG同源，SVG外部渲染未声称跨阅读器验证。producer为code/figures.py，精确hash见manifest。
