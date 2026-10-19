# 本轮执行证书：完成

终态：pt-falmqs6x平台SUCCEEDED（UTC18:02:26），内部20训练/20功能/20谱/8适配全部完成。下方保留启动与修复历史；以本段及完成回执为最终状态。

- 授权：2026-10-19 用户 Anchor/Protocol v1 与四种评分补充；允许一次4卡H100 Reserved，不扩大预约。
- 任务：pt-r697pchx；提交UTC 2026-10-18 17:44:27；最新只读平台状态 STARTING。尚未作为训练启动证据。
- 资源：h100-4-reserved；share-space/share-cluster；n6ls.iu.i40.4，1节点4GPU，Reserved/normal；挂载已有/data。
- 镜像：shphd-lite-0911，既定Python3.10/Torch2.3/CUDA12.4镜像。
- 提交：使用系统模板解析资源元组；传输入口为本轮兼容副本，只过滤旧客户端不能解析的新响应字段service_time_expression。首次创建在资源分配前失败；本次仅一个任务创建成功。未修改旧入口或旧结果。
- 模型：1024维输入/中间/输出，8个无偏置SwiGLU，25,165,824专家参数；学习路由参考另加8192参数。原基座、CrossCoder、final RMSNorm、输出头冻结。
- 训练：每模型3epoch、392136有效预测位置、768步；有效batch512、micro128、尾批152；两seed11/22的初始化和PCG64数据顺序配对。主坐标为累计有效预测位置。
- CE：micro实际数/完整有效batch实际数加权；LB由完整有效batch计算一次。E系数.01；D系数0；固定路由无LB。
- 保存：step0/每epoch末完整模型、优化器、RNG、数据顺序/游标、累计位置与配置身份；latest每64步可恢复。TensorBoard在每训练目录tensorboard/。
- 门槛：任务内部先跑零旁支等价、梯度、64位置拟合、一次更新的保存恢复一致性与10步计时。未将提交回执等同门槛通过。
- 时间：主训练截止UTC22:24:39，报告截止UTC23:09:39；不因结果调预算。未完成项明确PARTIAL/NOT RUN。
- 执行目录：/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/normalized_route_learning/20261018T173143Z
- 同题检查：本轮提交前，仅发现父任务pt-vv7zkyxf已SUCCEEDED；未见本轮同题运行或已完成产物。
- 导航检查：101个入口检查有2个既有、无关缺项，本轮不修其他项目。

状态需由实际runtime/smoke/训练与平台终态回执补全，科学判断保持Unknown。

## 工程修复1

原任务pt-r697pchx已终态SUCCEEDED，但本轮工程门槛BLOCKED：标量scale不能直接view uint8作哈希。8.0秒sanity分支停止；画像32.1秒完成。修复为reshape(-1)后哈希，未改模型或科学参数。平台wsImmutableJobEnabled拒绝重启，因此终态确认后替换为pt-falmqs6x；始终最多同一4卡资源，画像/统计复用。门槛成功与否仍以新smoke回执为准。

## 最终完成

- 工程：零旁支logits误差0；首次expert更新后router CE梯度非零；64位置拟合到约1e-6；保存恢复下一更新逐位相同。
- 主训练：20/20，各768步、392136位置，配对初始化/PCG64顺序/原h-z-c冻结核对通过；完整位置轴TensorBoard通过。
- 附加：同输入功能20/20、完整参数/响应谱20/20；目标背景510步、8适配各32步。
- 18张图，PNG/SVG/PDF；全部条件与配对表、逐feature与逐步精选日志、固定文本及图外解释完整。24项输出资产访问检查通过。
- 时间：替换任务内部计算615.875秒；原失败工程32.139秒。计时为进程墙钟，不是纯GPU kernel时间。原始限时未到，无PARTIAL/NOT RUN的协议必需分支。
- 科学：H1接收方向支持；H2联合学习门槛不支持；目标安全集合为空。研究者机制判定Unknown，未扩成容量或φ学习结论。
- 本轮停止，无追加训练、无新GPU预约、无commit/push。
