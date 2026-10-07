# Focus：路由返回表征的直接梯度反馈

problem_key: router_representation_gradient_feedback
task_state: BALANCED_PAIR_TRAINING_COMPLETE_POSTTEST_NOT_RUN
question_state: OPEN
design_state: DELEGATED_DESIGN_REGISTERED
result_state: NOT_RUN

研究者在[直接请求](../../handoff/researcher_request_cn.md)中激活对照并委托具体化实施。科学机制和采用判断仍 Unknown。

1. 核心问题：有限、相同 token 预算下，router 的 LM 梯度返回共享主干是否帮助预测和专家功能分工？一对共同 seed，正式算法与硬件完全混杂。
2. 目的及完成标准：证明受控干预的工程资格，提交两条已授权轨迹；训练前冻结后测。提交完成不等于科学问题已回答。
3. 分析：先读对齐 heldout CE，再做模型内部保持使用率/计算量的因果专家分配置换，最后描述梯度、几何和真实有限更新及替代解释。
4. 分支：定向 CE 与功能证据支持有界继续验证；无效用/反向削弱对应方向；区间、资格、终点不足或对手未分清为 INSUFFICIENT。AI 建议实用阈值不能变成人工科学判断。

下一决定由研究者持有：保留、移除或进一步验证直接反馈。只有一个训练对照及其依赖后测，无额外 seed/臂授权。[Anchor](../problem_anchors/router_representation_gradient_feedback/anchor_cn.md)、[Protocol](../experiments/router_representation_gradient_feedback/protocol_cn.md)。


[Summary](../experiments/router_representation_gradient_feedback/summary_cn.md)记录资格与直接提交回执；任务完成不改变科学问题开放状态和研究者判断。


当前执行修订A3（2026-10-06）：研究者选择共同均衡条件并要求从头重训和监督。本地/新双硬件/交叉资格PASS，新双正式实际4/8卡资格合格，均全预算SUCCEEDED且监督正常结束（终点与有界训练比较见Summary）。问题、主终点与科学状态不变；原零均衡失败历史保留在Detailed，精确合同见Protocol A3，分析思路为AI建议。
