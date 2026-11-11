# Conversation Memory: 1111-A5续训到1B

Conversation name: 1111-A5续训到1B（本线程延续，ID01a1c0ef-9bb0-7640-98f5-54843f460919）
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-11-10T16:20:08.457175+00:00
Latest update at: 2026-11-10T16:20:08.457175+00:00
Continues from: ../1110-蒸馏路由与自举原子路由训练/memory.md；../1109-原子集中正则训练与账本分析/memory.md
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router/experiments/20261111_a5_to_1B

## 2026-11-10T16:20:08.457175+00:00 -- 开始

- Summary: 用户授权唯一A5从R04@2000续到原生baseline1B的manifest步3816；优先4H100Reserved，排队超1h切4RTX5090Reserved，监督到容器结束。
- Current work: prompt与P10/P12已冻结；新目录复用源、完整恢复与实际SHA核对。
- Next action: 本轮SIGKILL恢复门后正式；不重训原生前缀，不改旧产物。
- References: /data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R06_20261111_a5_to_1B/protocol_cn.md；/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/protocol_freeze.json。科学判断Unknown。


## 2026-11-10T16:42:57.803379+00:00 -- 已提交与资源补充

- Summary: 唯一H100Reserved任务pt-4e669gn6，提交16:24:29Z，一小时截止17:24:29Z（北京时间01:24:29）；当前STARTING无GPU。源A5完整状态SHA已核验。
- Current work: supervise.py每60秒查询，超时先停H100再提5090Reserved，不重复运行；runner.py实际G3通过后正式2000→3816，训练后在保留任务里执行analysis/finalize.py才退出。当前MIG只做操作协调和代码准备，不执行本轮科研分析。四图MoE/Dense1B缓存已就绪并登记representation_r06_reused_baseline_1b_20261111，不需额外H100单卡作业。
- Next action: 监督调度、实测SIGKILL恢复门及正式finite更新；随后保留任务内完整分析。P12原生baseline2000状态缺失，代理比较资格已先行写明；P10真实1B端点照常。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/current_job.json；/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/source_checkpoint_verified.json；/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R06_20261111_a5_to_1B/protocol_cn.md；研究者科学判断Unknown。


## 2026-11-10T17:22:49.680257+00:00 -- 研究者改为立即5090及正式提交

- Summary: 最新直接授权取消一小时等待，所有R06后续阶段放一份4RTX5090Reserved按smoke→清理→正式续训→分析→打包顺序执行。H100原pt-4e669gn6未分配即FAILED，自动恢复pt-a726c21b未分配并已SUSPENDED；无H100训练。
- Current work: 唯一新任务pt-sghhdljb于17:20:47Z提交，5090规格n12lp.nn.i10a.4、share-space、Reserved、micro8acc4、SM120 torch2.8cu128。初次5090请求在旧任务SUSPENDING时过早发送，被429成员配额拒绝且未创建作业，证据完整；已确认旧任务终态后重提成功。
- Next action: 监督实际4GPU分配、R06G3外部kill恢复PASS、smoke清理与正式finite更新；实际吞吐更新ETA。当前本地容器到期不影响远端已准备的完整链。四图任务已于16:58Z交付，读取其缓存与分层，不重复跑。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/current_job.json；evidence/immediate_5090_authorization.json；submit_5090_retry1_live.txt；HANDOFF_cn.md；研究者科学判断Unknown。


## 2026-11-10T17:24:32.828427+00:00 -- 更正H100短暂分配及启动错误修复

- Summary: 更正早先仅据APIstart_time=null写“未分配”的结论：持久Pod日志证明pt-4e669gn6于17:07:06Z分配4H100，17:07:16Z在任何模型更新前因硬件回执路径PosixPath+str错误退出。无smoke或正式更新。
- Current work: 已修复R06runner路径f-string；当前唯一5090任务pt-sghhdljb仍排队，新硬件尚无数值资格；必须实际完成G3和清理再正式。H100短暂分配按Pod起点纳入资源记录，不当作纯排队。
- Next action: 监督5090启动与实际smoke；研究者立即5090选择保持，不切回H100。
- References: evidence/H100_startup_incident_repair.json及其中Pod日志。


## 2026-11-10T17:28:24.282529+00:00 -- LAUNCH A5

- Summary: AI执行LAUNCH，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标2020。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:35:44.862939+00:00 -- COMPLETE A5

- Summary: AI执行COMPLETE，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标2020。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:42:04.871095+00:00 -- LAUNCH A5

- Summary: AI执行LAUNCH，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标2020。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:48:30.133512+00:00 -- COMPLETE A5

- Summary: AI执行COMPLETE，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标2020。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:48:48.491441+00:00 -- SMOKE_PASS A5

- Summary: AI执行SMOKE_PASS，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:48:50.819728+00:00 -- SMOKE_DELETED 

- Summary: AI执行SMOKE_DELETED，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:48:50.856283+00:00 -- LAUNCH A5

- Summary: AI执行LAUNCH，job pt-589e1f1c6e744bbe97b0ca36b5a9432a；目标3816。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:50:11.344153+00:00 -- G3通过，正式接续加入平台级恢复

- Summary: 4RTX5090实测10步SIGKILL恢复到20步，与直跑20步CE最大差0，1076状态张量逐位一致；smoke清空含外部位置缓存，回执保留。
- Current work: 用户新要求处理MIG两小时后到期和远端容器失败；旧smoke作业backoff_limit0且API不能原位改此字段，所以正式入口等待marker暂停、无正式更新，handover_formal.py先停止pt-sghhdljb并确认终态，再同规格新建唯一正式作业，启用平台backoff_limit3且201/202不重试。
- Next action: 核验正式新job实际backoff3、4GPU、分析preflight及finite正式更新；所有R06后分析同正式Reserved作业顺序完成。引用监控对话新增适用任务A读数已冻结并接入，原对话任务E不重复。
- References: runs/smoke_summary.json、evidence/smoke_deletion_A5_auxiliary.json、evidence/post_container_autonomy_plan.json、logs/handover_formal.log、analysis/READY.json。科学判断Unknown。


## 2026-11-10T17:51:36.122777+00:00 -- LAUNCH A5

- Summary: AI执行LAUNCH，job om-91a0eb8b4f064e10aa637000ab5031ec；目标3816。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T17:53:13.218578+00:00 -- 唯一正式作业已创建、4GPU与平台重试已核验

- Summary: om-8dy8ynho，17:49:44Z创建，share-space四RTX5090Reserved，原pt-sghhdljb先到SUSPENDED。API实际backoff_limit=3且LMEmax_retries=3；不是本地监视器重试。CLI开容错生成om前缀，初次解析仅匹配pt而断言，随后读取唯一om作业恢复记录，没有重复创建。
- Current work: 17:51:17Z分析运行环境和输入接口PASS；17:51:36Z正式LAUNCH，当前加载完整起点，有限正式更新待核验。全部分析、图、资产登记和ZIP已挂在同一正式作业末尾，不用MIG。
- Next action: 核验实际更新、token、TensorBoard、保存、观察吞吐更新ETA；监督到训练与分析完成。平台默认重试策略rules为空，先前拟定201/202自定义平台规则未应用，实际通过持久科学停止标记阻断训练；原生CLI已直接设backoff3，预备代理没有改写创建请求且已关闭。
- References: evidence/formal_retry_verification.json、analysis_preflight.json、current_job.json、post_container_autonomy_plan.json、logs/supervise_formal.log。科学判断Unknown。


## 2026-11-10T18:24:08.322416+00:00 -- 正式完整存档与分析接口已实测

- Summary: 唯一正式作业om-8dy8ynho，2250步完整恢复状态已原子提交，state6.096GB+4RNG；原来2000步524288000token完整恢复，当前2340步613416960token，finite。TensorBoard在执行根tb/A5；2250同次EVAL NLL3.982984036、2097152位置和八层Top2已保存。smoke共删除20.36GB并清空。
- Current work: 实测端到端每步约4.58秒，主计算约3.39秒，预计北京时间04:30–05:00完成训练与分析，07:30速报在指定目录持续更新。平台backoff3+LME3已核验，rootMIG失效不影响正式pipeline；正式任务末尾运行全部统计、PNG/PDF、资产登记及小于20MB包后退出。
- Next action: 监督到3816步及分析，未来结果通过analysis/READY.json清单核验。源代码最新接口于18:23在同一Reserved作业独立只读进程再次PASS，含新增内容/router相关、十等份和R05q/u代数拆解；没有执行本轮MIG科学分析。
- References: evidence/first_formal_checkpoint_verified.json（滚动状态日后按策略删除不使该历史回执失效）、analysis_preflight_latest_annotated.json、runs/A5/latest_checkpoint.json、evidence/current_job.json、logs/supervise_formal.log。P10待终点，P12精确原生2000起点缺失仍不足；研究者判断Unknown。


## 2026-11-10T20:25:44.917434+00:00 -- COMPLETE A5

- Summary: AI执行COMPLETE，job om-91a0eb8b4f064e10aa637000ab5031ec；目标3816。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T21:35:33.681390+00:00 -- ALL_COMPLETE A5

- Summary: AI执行ALL_COMPLETE，job om-91a0eb8b4f064e10aa637000ab5031ec；目标。
- Current work: 实际事件与回执见/data/250010109/MoE_Router/experiments/20261111_a5_to_1B/evidence/events.jsonl。
- Next action: 沿冻结协议推进；门失败不转正式。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_to_1B/runs/smoke_summary.json；研究者判断Unknown。


## 2026-11-10T21:46:17.392921+00:00 -- 全部统计完成、平台终止与最终分析交接包

- Summary: A5完成3816步1000341504token，训练20:25:44Z结束；全部统计21:35:30Z完成，作业om-8dy8ynho于21:35:43Z为SUCCEEDED且worker Succeeded，四卡已释放。所有模型前向与实验统计在保留5090作业内完成，未在MIG重跑科学分析。
- Current work: P10支持：A5NLL3.763122、原生3.779426、Dense3.871652；A5减原生文档区间[-.019118,-.012673]。A5M1.338417、原生1.049243；q/u均值差代数份额94.87%/5.13%，不作因果归因。8个新学习遗忘区间、10频段、迟滞掌握率与毛流量、内容/router相关均产出。P12严格同轨迹缺原生2000步起点仍不足；代理Jaccard.28125与前段中位.63095已并列。
- Next action: 无训练待自动执行；研究者与AI读包讨论后续架构。保留单种子、teacher泄露、原生硬件及历史mask差异、掌握率快照密度等边界；研究者判断Unknown。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_to_1B/1111-A5续训到1B_结果.zip，12246923字节、191文件，SHA256 7c5fa557e06256fa8fc7f9f89323bb076bced3475a0138bde1138949cd5eaa36；已验CRC、逐文件SHA、内链、原CSV/PNG/PDF逐字节未改，资产strict四项PASS，入口151项PASS。最终包加先读、交接、平台终态及资源回执；CPU阅读版仅渲染现有CE50列的尾段坐标轴，不重算统计。初始生成ZIP已另存delivery_revisions。
- Failures resolved: 来源清单将forward_complete汇总回执当单次前向而KeyError，已限定MoE/Dense实际回执；平台分析恢复2次未重复训练；监督器5位小数时间解析已规范。最终资源跨度约16.49GPUh可能含LME间隙，非账单，H100短暂分配按可见下界计。
