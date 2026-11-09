# R03：teacher feature 分发的 1B 训练比较

授权来源：研究者在当前对话明确要求执行所附完整 Prompt，并要求 share-space 和 P12 两边正式训练；share-space 先做 Smoke。原 Prompt 完整字节保存在执行侧 evidence/authorizing_prompt.md。该 Prompt 的第 1–8 节拥有本轮精确设置、假设、对照、冻结规则、判据和运行授权。当前对话要求将次要 A4→A1-deep 从 Spot 改放 P12 Reserved。

执行根：`/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration`。主链 share-space：A0→A1→A2→A1-hi→A0-hi→A3；次链 P12：A4→A1-deep。每臂 3815 步、262144 token/步、单种子。MIG 仅做 teacher 预计算。Smoke 先在 share，全部放行门通过后提交正式任务，不重复 A0 前200步轨迹。禁止 commit/push。

实际原调度：1000步线性预热后恒定，原正式配置 horizon=50B；33B 是所用 teacher 的 checkpoint 进度。保留原调度而非重建余弦。原初始状态、参数构造与优化器、数值内核、4-rank 数据顺序均保留。新 Focus 未创建；研究者科学判断 Unknown。R02 冻结结果不变。

任务状态：IMPLEMENTING；科学结果 NOT RUN。详见执行侧 evidence/ 和逐项运行回执。

## 当前对话修订

2026-11-09 北京时间：研究者明确允许 Smoke 并行提交另一个工作区以加速；share A0 对齐 Smoke 与 P12 恢复/模式 Smoke 并行。正式主链仍 share、次链仍 P12，全部 Reserved。研究者要求先完成训练任务，暂不解读科学结果。

分数领先200步条件在末尾取 min(3814, current_step+200)，避免最后200步出现不可能满足的条件；分片不足时先保存、换可跑臂，必要时按原授权在4卡补算。同一路径使用文件锁，防止与MIG重复写入。

Prompt 未指定达标 loss 的数值，也未指定 feature 家族定义；相关统计保持 Unknown/待定，不凭AI临时阈值判定成败。这不阻止已明确授权的训练。

原训练的 token-addressed 500M/1B 里程碑包含缩短有效监督的 update；本轮按研究者明确的每步262144有效token、3815步=1000079360token执行，保留原输入顺序，但不沿用原里程碑的局部mask。A0前200步完全不受这点影响；不声称后续3815步逐位重放原轨迹。证据：执行侧 evidence/original_milestone_partial_masks.json。

2026-11-09 北京时间00:44：研究者明确同意两边改为四张H10080GB Reserved、16核/256GiB主机资源。使用执行环境键 h100-4-reserved-16c256g 与 p12-h100-4-reserved-16c256g；显卡、镜像、AFS、world=4、每步262144有效token和数值设置不变。后续研究者要求AI自行协调加速、保证完成，不重复请求本范围授权。

执行加速：依据研究者“尽可能加速、自己协调”的当前要求，两项低主机资源ACP任务在全部Smoke门通过后，直接在原allocation内派发正式run_chain，保留独立正式阶段回执和原ACP提交回执，避免释放显卡后再排队。不能称为新的ACP create；只有实际250步评估、有限loss及TensorBoard增长后才记为正式开跑。同一臂始终只有一个写入者。

## 2026-11-09 紧急修订：A1 对 A2 优先（研究者明确授权）

本修订取代原串行 3815 步计划。A0 冻结在已保存的 2000 步；其 2001–2264 日志仅为未保存的历史尾段，不继续训练。A4、A1-deep 冻结在 2573 步。A3、A1-hi、A0-hi 先 PAUSED。全部旧存档与失败日志保留。share 单独从共同随机初始状态训练 A2，P12 单独从同一初始状态训练 A1；首目标均 2000 步（524288000 valid tokens），每 250 步完整评估和存档。1000 步线性预热后恒定的原学习率调度、种子17、全局有效批量262144不变。

关闭自定义 DDP comm hook/每 expert 梯度噪声遥测，在 TensorBoard 记录关闭与原因；评估所有 rank 前后 barrier；保存所有 rank 前后 barrier，改为同步不可变 CPU 快照写盘，不再以异步写线程与 NCCL 重叠。NCCL 超时30分钟，异步错误处理开启。每臂先执行50步独立工程Smoke，再从0正式训练。A1开始前完整核验已存在分片0–2573（包含首2000步及后续2573步对齐所需）：4逻辑rank、2micro/update、input_ids逐micro哈希、frozen身份、形状及有限值。缺分片只补缺段；哈希不一致立即停止，不得绕过。

任务脚本内执行失败等待30秒、最近完整存档--resume auto、最多3次重试；哈希不一致不重试。两臂均到2000步后续到2573步；随后按A1-hi→A0-hi→A3全局顺序执行，各先2000步。跨臂正式比较只报告相同步数≤2000；2573为后续轨迹对齐存档，不扩大本次交付的比较范围。1000/1500/2000步评估后立即运行analyze_morning.py --step <step>，使用A0/A1/A2/A4/A1-deep已到达的同一步结果，未到达者明确缺失，不混用最新步数。交付分频bin NLL、A1−A2、逐feature收益对Δlog M̄和A0实测M̄。单种子；固定路由分支不向表征反传router梯度；科学判断 Unknown。研究者要求每20分钟监督并在任务失败时立即按同一已授权资源重新提交，直至A1/A2均2000步。禁止commit/push。
