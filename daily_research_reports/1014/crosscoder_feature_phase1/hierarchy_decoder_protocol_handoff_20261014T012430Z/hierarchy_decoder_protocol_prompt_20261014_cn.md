# 发给原科研线程的指令：只写Protocol，不运行分析

目标线程：`01a1343f-32aa-7500-9835-000956218089`。
目标host：`remote-ssh-codex-managed:mig`。
此前已核实标题：`1013-CrossCoder 分析目的讨论`。

用户已授权我转交完整anchor并请你核对实现、写protocol。本轮授权仅为读取现有文件、核对代码及编写方案；尚未授权新的正式跨层分析。请先核对你当前线程是否有冲突任务；有冲突就报告实际状态，不中断或覆盖用户工作。继续同一个线程，不fork、不另建执行线程。

用户最新明确要求本次protocol撰写turn使用`gpt-6.1-sol`、reasoning effort=`high`。发起方应在受支持的正式turn/start字段设置`model: "gpt-6.1-sol"`与`effort: "high"`，并保存本次实际接受/运行配置回执。仅改未来默认值不能声称本轮已经使用。若已有冲突任务运行，不为换配置中断它；若本轮无法切换则明确报告，不另建线程。

完整用户anchor在：
`/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/hierarchy_decoder_distribution_anchor_user_20261014_cn.md`

这是用户提供的完整原文，含已核验的全部图深度分布；请保留问题与假设，不把允许写方案当作允许运行。请读适用AGENTS.md、仓库research-reasoning-auditor、experiment-card-writer及必要协议契约。复用现成记录，不重复完整审计或重建执行代码。

请用清楚中文写精简但可执行的`protocol_cn.md`，状态必须为`DRAFT_NOT_EXECUTABLE`／`ANALYSIS_NOT_RUN`；最后返回全文供父对话和用户审阅，等待明确的执行批准。至少包含：

1. 唯一主问题：较高统计图层级是否整体对应更偏深层的解码分布；经验H、频率／尺度／重构质量竞争解释及支持、削弱、证据不足分支。
2. 完整图定义：到出度0节点最长距离，叶0、0—5六档；采用V为主、D为固定定义敏感性；复用anchor已有16,384全节点及15,537双侧支持≥200节点统计，不只看最高级937、3461。主集合与全部合格集合已核实相同，记录相同即可，不重复统计/图。
3. 共享z下单特征解码分量幅度z乘decoder范数，归一化时z约掉；p和L严格由decoder几何决定。不得用不同文本解释为不同p，也不得把幅度当独立预测贡献或干预响应。零总范数NA，层号固定为一基2、4、…、28并查已存身份元数据。
4. 复用精确资产路径/字段/维度：原run_root下graphs/reduced_D.json、reduced_V.json，feature_frequency.npz的n/zsum，decoder_geometry.npz的norm/raw_norm/rms/train_mean，已有文本/CSR与位置索引。主分析无需加载checkpoint、更不需要前向Base。最低源绑定/维度/p行和检查即可。
5. 三张图分开：统计层级关联图；同批Feature ID的14层p热图；全部合格节点h—L分布及描述性Spearman。最高h5两个节点仅用于个案和明确两点标示，不作独立层级推断；不按是否支持趋势选择代表。
6. 频率竞争解释：在看h—L诊断前明确D log频率5分位分组、重复边界合并、共同支持范围定义、每h/频率组实际样本量及不足分支。分位组内仍可能不平衡，不强行称匹配；无共同范围不能区分层级与频率解释，不外推、训练复杂预测器或追结果调参。
7. 主坐标为训练归一化坐标；raw恢复乘每层RMS，raw与norm分析分开且预先指定角色，不能事后挑正向版本。D/V来自同bin且是同一decoder，D/V不是独立试验；节点也不是独立重复，不报告独立总体p值。
8. 代表图节点过多时给具体、确定性裁剪规则（锚点/层次/邻居顺序/节点与边上限/省略计数/分面），保留完整机器列表与原图h；不能裁剪后重定义深度。
9. 文本节点范围、每节点5随机/3高激活及总数量上限、随机种子/去重/短缺处理、复用位置映射与读取成本。数量少不保证I/O小；缺失937/3461等文本时可能需扫描大CSR，预估成本并设置时间/I/O停止点，不能重跑模型或全量关系计数。语义仍只是人工阅读辅助，不认证单义。
10. 预计时间、CPU/内存/I/O与新增磁盘，区分几何表/图计算和文本取样成本。只给预估，不运行性能smoke或科学分析；列原第28层FVE86.4722%、替换CE+0.305962nats的工具边界。逐项列计划交付的小表、三图源表、一页结果与未答；当前一律NOT RUN。

若anchor有歧义或统计风险，先列最小修正建议及理由，标为AI建议，不默默改问题。重点防止频率耦合被叫独立层级机制、归一几何被叫功能、两点被叫整体趋势，以及小数量文本掩盖大读取成本。不要把科学判断升级成研究者确认。

允许在该独立handoff目录下写protocol和简短修正说明，保留用户anchor原文。不修改旧Anchor/Focus/正式结论或旧图，不commit/push。**禁止运行新的跨层h—L比较、Spearman/频率对照、正式作图、文本提取、推理、训练、新GPU/付费资源或全量计数。** 只写方案并交付全文，等待执行批准。

交付路径建议：
`/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/protocol_cn.md`

请返回实际路径、完整protocol文本、最重要的修正建议及明确停止状态。不要只说能够完成或只列计划；本轮做到方案可供审阅为止。
