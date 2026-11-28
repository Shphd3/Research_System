# Protocol：训练后表征与功能测试冻结合同

## 0. 批准与边界

R1，在正式训练前登记；APPROVED_FOR_PREPARATION。本轮准备后测，不提交长时间后测GPU任务。[研究者请求](../../../handoff/researcher_request_cn.md)委托确定后测；[训练Protocol](protocol_cn.md)与[Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor_cn.md)持有上游。科学采用门槛/最强对手Unknown。inputs/analysis_manifest.json冻结面板，docs/analysis_entrypoints.json区分可运行与待实现入口，不等结果后选指标。

## 1. 主要效用、总体与不确定性

独立DCLM global-shard02原文JSONL-zstd，构建时核验源SHA256。顺序选前1024个去重、token数≥257的文档，最多1025token/1024预测目标。seed1005稳定打乱，128FIT/128DEV/128DIAG/640TEST；无文档跨集合。训练来自global-shard01；不证明全语料语义去重。保存截断tokens、来源行/文本hash、原长及可得domain；标签不进入router。FIT词频只定义四分位，缺domain为Unknown。

主要量：step7629的TEST完整负logprob之和/有效target总数，B减A，nat/token。每文档保存sum/count。配对整文档bootstrap5000、seed1005，双侧percentile95%区间；token只作权重，不能当独立样本，也不覆盖seed不确定性。不删outlier，不填缺checkpoint/文档，非有限或缺失则资格失败。只有一个主比较；早期0/64/1024/3814只描述，不选最好。AI建议最小可解释差异0.01nat/token，分别报告相对0和±delta区间，不冒称人工采用门槛。

## 2. 梯度路径

DIAG前32文档，共同prefix/位置，层0/5/11。h专家输入与r Attention reference分别定义，残差保持live。读取真实训练开关下返回各r/主干的梯度。另在同checkpoint临时全部detach=false，离线用hooks/VJP拆gate-edge及expert/residual贡献。报告L2、cosine、gate/other norm，零范数NA。上层切边改变下层adjoint，因此完整网络训练差与局部固定出向adjoint分解分开。离线live-router归因不是B历史训练路径，更不是未来效用。

## 3. 表征几何与组成控制

DIAG128文档；prefix长度256/512/1024，16个位置从32到min(255,有效末位)等距，缺长度排除并计数。层0/5/11取expert_input、live r（router数值input同r）、共享加所选专家输出。各model/layer/object中心化，协方差熵effective rank与linear CKA，仅这两类描述量。raw和逐行unit-L2两版本，零行排除计数。位置/长度严格匹配，FIT词频四分位重加权；domain仅有metadata时分层。CKA只用共同有效行。不加SAE或事后找几何指标，秩/簇不能选优劣。缓存留执行目录。

## 4. 路由与专家功能

全12层counts、熵、零load专家；同模型固定prefix在对齐checkpoint间top2-set churn。跨模型专家编号不当语义对应。可选Hungarian只用FIT功能响应，禁止test最优排列。

主要功能：TEST中≥257tokens文档取256预测目标，固定8文档cohort。每模型由原生因果前向得到每层每位置自身route/gate plan，重放原plan应复现CE。层0/5/11逐层干预：同一token位置，将完整top2分配+gate bundle在8个文档间rotation shifts1/2/3/4，专家仍读接收文档完整h。相对native plan，每层每位置专家次数、gate权重集合和激活计算精确保留；plan只读各自截至当前位置prefix，无target/domain/未来token。跨文档cohort是离线因果干预，不是部署router。其余层固定原自身plan，重新计算激活；因此干预不含后层在线适应，必须保留这个estimand边界。报告真实有限CE增加、整文档配对CI及A/B增加量差。计算核验负载保持；不足cohort/短样本排除计数。12个次要功能对比若作方向判定用Holm，原CI只描述。入口若未实现标PREPARED_NOT_IMPLEMENTED，不能捏造结果。

## 5. 有限更新相容性

DIAG32来源与32不同接收文档，prefix256、16固定评价位置。各模型按末层position127 top2 overlap区分同路由/异路由。greedy匹配可得domain、FIT词频quartile、长度bucket、末层load decile；未匹配排除计数，不按TEST选样。在checkpoint副本对全可训练参数作1次plain SGD：来源LM梯度整体L2归一到1，步长1e-3，不用optimizer moments、不weight decay、不多步，保留真实detach开关。读接收CE_before−CE_after（正为帮助），及来源自读/匹配随机接收对照。保存更新norm、参数名、route变化与真实有限loss。原checkpoint前后hash不变。只回答登记归一SGD一步，不能当Adam长期效用/gradient dot。此后测允许明确PREPARED_NOT_IMPLEMENTED，登记已完成不等于未来结果。

## 6. 判定分支

CE降低且校正后的功能干预支持：有界效用与分配依赖支持，硬件/机制仍未独立识别。只几何：描述，无效用支持。CE差但负载/硬件短窗噪声/幅度或Adam解释未分清：DIFFERENCE_WITH_UNRESOLVED_RIVAL，机制INSUFFICIENT。区间跨±0.01、预算/guard/测试不足：INSUFFICIENT。反向CE超过建议差异削弱对应收益方向。采用、机制、关闭由研究者决定，不自动宣布。

## 7. 入口、冻结与费用

scripts/prepare_inputs.py构建并锁文档/tokenizer；scripts/evaluate.py读checkpoint文档CE；scripts/analyze_tables.py配对CI/几何统计；scripts/post_analysis.py列梯度/功能/有限更新精确输入需求，待实现模式明确返回PREPARED_NOT_IMPLEMENTED。训练weights和终点full-state足够，不增预训练/SAE/全专家穷举或GPU任务。原生面板每模型/checkpoint≤1M预测token；12功能对比每模型≤2M；有限更新每模型32source steps。待测推理吞吐后估时，不伪造ETA。analysis/执行目录保存，训练pair一起锁源/manifest，曝光后变更只能追加amendment。本文件是预登记，不是结果或未来长作业权限。


## 修订A1：共同均衡新条件（2026-10-06）

Protocol A3命名新的一对条件。复用原精确面板、split、终点、CI、功能与有限更新程序，不合并零辅助项失败轨迹。梯度归因分开LM与辅助项；辅助回reference在两臂实际训练中均阻断，router权重接收两项。原有限更新诊断仍为纯LM归一化SGD，不等于AdamW或带均衡目标的完整轨迹。1002历史提示来源敏感性与真实表征位移的价值，但不新增未登记终点、SAE训练或GPU任务。后续分析思路是AI建议，新增程序须在TEST曝光前前瞻登记。
