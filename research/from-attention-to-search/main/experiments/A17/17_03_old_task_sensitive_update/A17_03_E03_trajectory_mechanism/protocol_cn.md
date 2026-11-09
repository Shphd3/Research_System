# A17_03_E03：中途状态与更新操作检验协议

[English](protocol.md)

## 0. 批准快照

状态：APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FINITE_FULL_ANALYSIS。用户本轮明确要求“请你先完成第一轮任务”。执行范围为已有状态的有限分析，不执行第二轮新任务训练。机制和关闭Unknown。当前问题沿用[旧任务敏感更新Focus](../../../../focus/focus_old_task_sensitive_update_cn.md)，不新建问题。

## 1. 定义

完整更新full=d；删除out=v；删除后放大out_norm=v*s/||v||。历史分普通ordinary与限制protected。原本答错/答对的样本集合，以旧训练终点确定，不根据本轮干预结果选样本。

## 2. Anchor对齐

[子Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/subanchors/17_03_02_trajectory_mechanism_anchor_cn.md)检查中途更新作用如何影响旧错误修复。它补足已有局部干预与100步结果之间的候选连接，不改E01/E02冻结结果。

## 3. 假设

在指定中途状态，删除并放大可能比完整更新少改善原旧错误集的答案优势及修复。先比较同状态操作，再比较两种历史下的操作效应。不预设效果存在或一定有害。

## 4. 竞争解释

累计状态、来源梯度与下游敏感性共同改变；候选词概率适应；全词表其他竞争词；有限步舍入。跨历史不能独立分开梯度改变与下游响应。不同阶段下一批数据不同，不能把跨阶段全部变化归为状态。

## 5. 数据与来源

原登记list_rules_v1：train4000条，dev800条即400对。顺序未见/组合未见各200对，分别及等权合并报告。dev已暴露，不是盲确认；test关闭。保存步t的来源固定为new_order[20*t:20*(t+1)]，即实际下一批20答案。两种历史在相同步数使用同一批。22个必需输入ID见config；当前strict访问快照在执行provenance。

## 6. 任务及允许监督

输入可见FIRST/LAST规则、三个不同词、答案前缀，只预测正确答案词元。不把答案放进前文，不加入旧任务训练目标、SAE、专家或其他监督。

## 7. 模型与冻结

原登记Qwen3-0.6B Base，完整FP32原生eval前向、SDPA。唯一变化参数为model.layers.27.self_attn.o_proj.weight，形状1024×2048。其余参数字节与version不变。恢复各自登记的中途状态，Q为原旧终点秩16固定CE基底，不重拟合。

## 8. 更新构造

来源平均20答案CE，micro5累加。s=0.01*min(原普通轨迹下一步raw_gradient_norm,1)，两种历史共同使用该外部长度。d=-s*g/||g||，u=Q转置Qd，v=d-u。比较d、v、v*s/||v||；仅删除条件不匹配长度，正是用于隔离删除与放大的操作。无动量、衰减或累计新训练。另计算CE三分量梯度只用于资格核验。

## 9. 条件、种子与状态

29/43/71三种子×双顺序×普通/限制双历史×1/16/50三个保存点，36状态案例。3更新×主尺度1，共108Full单元。Smoke为seed29双顺序双历史第16步，共12单元，每未见面板10对；另四次独立进程精确重放。旧轨迹回看包括1/16/50/100步。

## 10. 主要指标与冻结分析

主要比较原旧错误集上out_norm-full的首末优势、全词表最强竞争优势与修复数量变化；同时报告原旧正确集丢失。分别报告删除out-full、放大out_norm-out。每案例均值，再按种子等权，两顺序分别与等权合并，面板分别与等权合并。列表、状态和来源批次不是独立种子。只作描述性符号与计数，不添加p值或显著性门槛、不挑最佳状态/种子。缺失/失败单元保留并阻断依赖比较。

## 11. 次要指标与资格

保留CE、词池logmass、词池条件CE、词对access/selection、b/h、全词表argmax及最强竞争词。基线复现误差<2e-5；CE分解<2e-5；梯度重组相对误差<2e-4；实际位移舍入相对误差<1e-2；基外泄漏<2e-3。要求W/source20恢复精确、no-op一致、冻结字节/version、独立进程精确重放。阈值只用于工程资格。

## 12. 已知正确、错误与易混淆

正确：恢复同一状态并完整读出。错误：相同步数双历史换来源批次、重拟合Q、读取test。有效易混淆情形：CE改善却选错、平均优势上升却没有一步修复。

## 13. 阶段合同

预检绑定资产与文件、冻结代码/config/科学正文。单节点四H100 reserved Smoke12单元与独立重放4单元；失败阻止Full。门槛通过后另行提交同资源Full108单元。独立复算、登记实际产物，完成双语Summary/Detailed。每作业7200秒，不切换资源兜底。本协议不启动额外短训练分支或无限方向扫描。

## 14. 算法、产物与谱系

执行根/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism。唯一runs/trajectory_20261011T090921Z保存source/config/freeze、输入访问、挂载pod日志、提交及环境回执、逐状态基线与来源、逐单元读数/manifest、进度、轨迹和交叉对照。无新增训练检查点。绑定选定状态、manifest、原基底、普通下一步长度及匹配旧读数。资源/镜像具体值由docs/execution_envelope.md展开。

## 15. 支持、不支持、不足

同状态下降的旧错误优势/修复收益支持一个局部候选作用；不存在、相反或异质则限制操作解释。没有argmax变化可能不足以确定修复因果，但仍可报告有限优势变化。来源无效或数值失败是读数不合格，不是假设反驳。工程完成后，100步完整机制仍可Unknown。

## 16. 不能声称

不声称完整100步中介、专家收益、可推广规则算法、任务必然冲突/相容、自然文本推广或容量必要。输出恒等关系不能独立作机制证据。

## 17. 授权、冻结与修订

问题范围来自用户明确完成请求及已粘贴第一轮方案。A-G继承已核验数据/任务/模型和三种操作；具体网格与数值资格是原E01/E02基础上的委托工程选择。启动前科学正文与输入冻结；启动后仅追加回执或说明，不改变条件。此中文表述展开与冻结版本保持相同设定，不改科学或执行合同。


### Completion receipt / 完成回执

2026-10-11: Smoke pt-c1i5f9pl qualified12 cells and4 exact external replays. Full pt-8aoyrzuw completed108/108, independent3888 aggregate and86400 record checks passed. No retry/skip/new training. [Summary](summary_cn.md) and [Detailed](detailed_cn.md) own bounded interpretation; mechanism/closure Unknown.
