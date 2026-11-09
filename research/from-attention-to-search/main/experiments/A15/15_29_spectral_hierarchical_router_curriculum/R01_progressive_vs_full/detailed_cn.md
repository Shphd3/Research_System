# R01 执行记录

截至 2026-10-31T18:14:22.824788+00:00，**P 已提交正式作业 om-867vcrpa，平台 STARTING；F 未提交**。P 实际请求单机8卡RTX5090spot，终点50B有效预测token。两组的离线目标、smoke和真实进程退出恢复已全部通过。原定“双正式job ID”完成标准仍未达成：当前接口和项目记录中未核实可保障共享8卡上限的依赖／专属队列；单作业内P→F替代方式尚未收到用户答复。没有同时申请16卡。科研比较结果仍为Unknown。

模型507,988,992参数：共享205,933,568、专家301,989,888、router65,536。保留修正baseline的共同随机初态、seed17、真实架构、tokenizer、DCLM顺序／packing／mask、全局262144有效token batch、AdamW、1000步warmup后恒定LR、精确保存里程碑。2卡和8卡分别匹配历史Dense前10B全部38150个样本／mask指纹。资源差异为4H100／micro16／acc2／Torch2.3变为8RTX5090／micro8／acc2／Torch2.8cu128；低精度与微批次归约可能产生数值差异，P/F采用相同配置。

最终v5使用精确33B Dense的实际逐层norm2输出。A/B/C5各262144／262144／16384位置，覆盖1152／1174／72物理文档。所有节点统一一次有界加权中心更新；A/B独立拟合，新C5独立检查。8层JS为0.04918–0.09531，叶一致率62.5%–73.9%，分支／文档支持和熵均过门。v1–v4失败和数值修复记录保留。此树是人为监督目标，不是天然语义层级；物理文档分离不代表语义近重复分离，小校准面板也不能证明完整50B分布覆盖。

实际两卡smoke作业om-to4cwwnz已成功结束。GPU因果性误差均0、目标重算最大概率误差约1.8e-6；LM路径与辅助分支停梯度位置均通过。micro2／4／8稳态约31.7k／38.3k／41.9k有效token/s；micro16显存不足排除。采用micro8，含恢复段峰值allocated25.71／reserved27.25GiB，实际余量4.10GiB。teacher与目标投影约0.53秒／步，占该两卡训练步8.4%，不含载入、离线拟合及teacher既有训练成本；不是8卡吞吐预测。

P/F各自完成“连续4步”对照“2步保存→退出全部训练进程→新进程恢复2步”。loss轨迹逐值一致；样本ID／mask、LR、bias、计数、RNG、数据位置与阶段一致，完整model／Adam／scheduler张量通过atol1e-7、rtol1e-6；loss门槛atol／rtol1e-6。teacher／树指纹恢复一致。TensorBoard必需坐标和损失tags通过。额外检查28次实际更新：bias精确按全局有效分配更新一次，全部选中分配执行，最小每层每专家5792分配，无丢token。这是实际2卡恢复资格，不声称另做过8卡恢复试验。

正式从共同初态重置，不继承smoke。P目录runs/formal_P；F计划目录runs/formal_F，尚无job。完整原子checkpoint保存模型／bias、Adam、scheduler、8个rank的RNG、数据／shuffle／计数与teacher／树／源代码指纹。恢复点每1000完整更新保留2个，另保留共同初态及长期里程碑。第一恢复点step1000／262144000token，首个非零永久点0.5B。平台最多重试3次，分配内最多再试一次；50B目标不因中断改变。workspace禁止手工start旧job；如耗尽重试，需检查后以同一完整run状态发替代job。

最后检查P为STARTING且分配副本0，尚无已确认正式checkpoint，不能把计划文件当实际保存。9个真实507Msmoke完整状态已登记。精确fingerprint、完整失败边界与证据见[英文记录](detailed.md)，小证据及来源见evidence/payload_manifest.json。TensorBoard持久脚本analysis/tensorboard_spectral.sh；恢复时未提交的JSONL尾段会隔离，metrics.jsonl为计数权威。

[协议](protocol_cn.md) · [P](P.md) · [F](F.md)。
