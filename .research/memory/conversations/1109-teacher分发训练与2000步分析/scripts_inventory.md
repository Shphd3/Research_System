# 实验脚本索引：1109-teacher分发训练与2000步分析

这是同一Codex对话的操作索引，不是新Protocol或执行授权。处理者：Codex（harness: Codex desktop；model: unknown）。App标题和memory目录同名，原实验ID、任务ID与Created at未改变。所有源码留在执行目录；这里记录用途、入口、哈希和版本快照，避免把完整代码塞进memory。

执行根（以下称R）：`/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration`。

## 核心入口与实际任务

- share：A2，`pt-4bh1k6uc`；P12：A1，`pt-kw43x8ls`。两个独立Reserved allocation，各4 H10080GB、16核/256GiB。实际提交以 `R/acp_receipts/`、`R/evidence/urgent_jobs.json` 为准，不能用主机allocation UID替代短任务ID。
- 当前任务内入口：`bash scripts/urgent.sh A1` 或 `bash scripts/urgent.sh A2`，由ACP在R执行；这里仅记录入口，不能直接在本地重新运行来重复现有训练。
- 控制器先各自50步Smoke，再从同一seed17初态正式到2000；两臂达标后续2573，之后P12按A1-hi→A0-hi→A3各2000。异常等待30秒、最近完整存档`--resume auto`、每阶段最多3次重试。该接续顺序是用户已有授权，不表示本记录已经核验了后续完成。
- 用户要求停止续训监督后，已停止前台urgent_watch进程；未停止ACP训练。任务内恢复依然存在，当前没有本对话的后台观察/掉线重提守护服务。
- A0冻结2000，旧A4/A1-deep冻结2573，存档保留。结果包统一只取≤2000；不使用旧run_chain恢复3815步旧计划。

## 安全的只读分析复现入口

以下从R运行，只生成分析，不提交训练：

```bash
python analyze_morning.py --step 2000
R03_BUNDLE_DIR=/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z python build_2000_bundle.py
python write_2000_report.py
```

必须显式给analyze_morning.py传`--step`。历史默认会选择其他结果，不能用于本次统一步数比较。build命令重新生成的是草稿文件夹；已交付ZIP不应静默覆盖。finalize_2000_bundle.py仅在目标ZIP尚不存在时创建，需新交付目录才可另做修订版。

teacher分数完整审计入口是 `python validate_scores_urgent.py --end 2574`，exclusive_end=2574，对应step编号0..2573；已有10296分片、20592个micro输入哈希PASS，不需无故重算。配置在 `R/arms/`，环境在 `R/scripts/runtime.sh`。原训练代码、数据、初始checkpoint、老师33B/SAE、冻结feature坐标以Protocol和实际输入资产身份为准。

## 脚本用途与当前版本

下表是本次记录时磁盘版本。历史作业可能加载更早的源码，必须与对应release/日志/分析source版本一起读。

| 脚本/配置 | 用途 | 当前SHA256 |
|---|---|---|
|[analysis_urgent.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis_urgent.py)|严格同一步数五臂表2、A1−A2、图3、A0实测Mbar与来源哈希|`88d3e18c38d8c1535eba6d9cad648ca42c47ab1d3b33f815ab7a75aeadc6d310`|
|[analyze_morning.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analyze_morning.py)|显式--step的分析入口；未带--step的历史默认不得用于本次统一比较|`5c99f5f60a35855c5789a1325fdc03a62a53183872df7860f728dc980c8cc0ce`|
|[arms/A0-hi.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A0-hi.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`8c4684530caa20f724be5e1049688967bc52dc7cea038131d14dcff27c78ced3`|
|[arms/A0.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A0.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`f3d9f13beda01aa51f981abbbcf29e959f7920a8a56800fc8832ff6ce3c2ec4d`|
|[arms/A1-deep.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A1-deep.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`abe831505df7c500dbf192bcc06ba3d040c6163d7fbb047ce138033ee19b8559`|
|[arms/A1-hi.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A1-hi.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`cdfaf86836534156111642200e656cbd6fbd449ac282b0ef0a35e1e7ae058d38`|
|[arms/A1.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A1.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`82ac81271faf3277a1ddc662bad4889b5c24c8307961da192205d74387d9ff43`|
|[arms/A2.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A2.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`9488b8ae6e026d763d6934257b942c160ebfb5c933ecd19308eaecfb2be3c939`|
|[arms/A3.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A3.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`bbb11ee420cedf57b3f4541d71b08f85aff20f6d67c9d637b1c8d1f00d6e2621`|
|[arms/A4.yaml](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/arms/A4.yaml)|配置与原训练器配套实现；以源码/Protocol为准|`70cd266428c70ca634e2aba87276d0d03cd2719f4d9929d57e5b691df87d1af8`|
|[async_checkpoint.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/async_checkpoint.py)|当前执行同步不可变快照保存；名称保留，实际不并发NCCL写盘；保留RNG/数据游标/优化器|`8f6c6a6c34f35c2b365b903d31c93af6131af9aa14e7e9e58d990974e21ec017`|
|[build_2000_bundle.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/build_2000_bundle.py)|只读取≤2000前缀、生成统一CSV与五臂loss/频段曲线，不训练不监督|`8d55be85b799fb154969bbed570f84256dbbd032bfbe914c542334a346411ae9`|
|[evaluation.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evaluation.py)|固定EVAL总体NLL、feature/bin统计与各层实际集中度；不更新load bias|`f626134a13d76b5039425477b8c9acfb5e9a8b1cd90824735dc25a05feb311b4`|
|[finalize_2000_bundle.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/finalize_2000_bundle.py)|逐行复查来源、portable链接、SHA256清单、ZIP CRC与解压后全文件哈希|`aa75ee3f3cd655df5ede5f8935f5283a6c016be3b1c5af1b8873d0f914181d0e`|
|[moe_baseline/__init__.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/moe_baseline/__init__.py)|配置与原训练器配套实现；以源码/Protocol为准|`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|
|[moe_baseline/data_stream.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/moe_baseline/data_stream.py)|配置与原训练器配套实现；以源码/Protocol为准|`2527624b890f94ed3c3852f4e3ed9e8e25a7bf35890d8b3456635b9511701b79`|
|[moe_baseline/model.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/moe_baseline/model.py)|原生、teacher固定、随机固定、deep及router蒸馏路径；保持固定分支无router梯度回流|`4abc965fbafd0fd700a5f88e02c0afdd646130058759e517a7336bdc97d8afe7`|
|[moe_baseline/token_policy.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/moe_baseline/token_policy.py)|配置与原训练器配套实现；以源码/Protocol为准|`53acd94a9298fb11334b62dcff80f0908a7104c0739fef6b0de69c2d13ce8509`|
|[moe_baseline/train.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/moe_baseline/train.py)|原MoE训练器的本轮改版；数据/计数/数值/恢复守卫、评估与保存barrier、关闭梯度噪声hook|`7fd0a90330bb1c59d774d28a584b855d4fe7e3f30b5189038e05c1fb48a17c86`|
|[phase_to_formal.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/phase_to_formal.py)|历史Smoke到正式控制器交接|`58e0d35636e1925749219eef1dc0e9b8d680389042d23fcf6a6aaae4c1081f1e`|
|[precompute_scores.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/precompute_scores.py)|冻结DEV/EVAL编码、8簇与tau，teacher训练分数预计算；只补缺片、原子发布|`dc899500df762deb73873941e1f2ff213ed35788919e89e62c7aed0676608f44`|
|[record_2000_scripts.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/record_2000_scripts.py)|本次用户要求的源码快照、memory脚本清单与完成日志|`45391fb79060154b816095238611a8256b7d043b7531ff7568945039fd141b3c`|
|[register_actual_assets.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/register_actual_assets.py)|仅登记实际完整保存的checkpoint家族/已核验分数前缀；不登记未来状态|`c53029ea344e06074a634652da42dbe782a1ed0013c0e0f2ae39e392f2614a33`|
|[routing.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/routing.py)|teacher分数加载/逐micro输入哈希与可重放随机路由；可选teacher诊断同步限制|`4409e69986a7b83c43ee326448415a2f2e2942f1dbfd28ac9bd9b69b394e25d0`|
|[run_chain.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/run_chain.py)|旧3815步控制器；已对urgent_jobs存在加保护，当前不能用它恢复旧链|`da04017e35e9ea5a1bfbd6b81cbf37c1950641a4ab6b5a4f6b4e2eee02363dff`|
|[scripts/gpu_preflight.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/gpu_preflight.py)|GPU/存储/数值路径的资源资格检查|`6c0ae5678cd43c3761fb63491fd30479db020874b075d7bf942ea01dfe6243e8`|
|[scripts/original_formal.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/original_formal.sh)|配置与原训练器配套实现；以源码/Protocol为准|`eff1465dd9dcdb623a1db8d8b9d85efc6bcc4c3ed142b6c8af3e7caaf5d768f4`|
|[scripts/original_runtime.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/original_runtime.sh)|配置与原训练器配套实现；以源码/Protocol为准|`ae5fc3919ec8c8230266f51bada560846bd3ef83fc1c6d706ca5d11e6156c022`|
|[scripts/run_chain.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/run_chain.sh)|配置与原训练器配套实现；以源码/Protocol为准|`6f9a8d588f4e6ccaf9d1aaa1da963fe53f40c034a04178d66bb294724969c0eb`|
|[scripts/runtime.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/runtime.sh)|运行环境、离线依赖与PYTHONPATH；不安装新依赖|`a00ae8b408d45d698da34d94b7384b7cc2933870310fc40b424573362d2b90d0`|
|[scripts/secondary_wait_full.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/secondary_wait_full.sh)|配置与原训练器配套实现；以源码/Protocol为准|`82752bda30b5ab1eb9a1e90ef98d5c511d29d7e980a57718fa569e538c9052a8`|
|[scripts/smoke.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/smoke.sh)|配置与原训练器配套实现；以源码/Protocol为准|`6fbbde0bcda7602bafd4475cf722fb581d84e10d68766a4f08331509e9c4cbb0`|
|[scripts/smoke_suite.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/smoke_suite.sh)|配置与原训练器配套实现；以源码/Protocol为准|`e58a686c58af7dd33b2fdf22e62cabf2608bbd04b370057ec5c7ba17852e6650`|
|[scripts/submit_low_host.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/submit_low_host.sh)|研究者授权16核/256GiB、4H100 Reserved规格的提交入口；工作区显式选择|`6ff471fae692125daab389e44d1ab50d0bf267a04b823be5af7b5e37a78946ff`|
|[scripts/urgent.sh](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/scripts/urgent.sh)|当前ACP入口；设置NCCL错误处理与退出清理，调用urgent_runner|`7d63b1240cff5cbe139d1795d5272bed17190964c218960beb91488f05d16e93`|
|[smoke_suite.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/smoke_suite.py)|历史四卡、模式与恢复资格检查|`549be4232ce78451df75d5ca59234884ed985fe726c7e544e8eef3a6a123e4d6`|
|[smoke_tree_guard.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/smoke_tree_guard.py)|历史完整torchrun进程树打断检查|`d867ba4f58ce0b34e30bd9f0a8357622c7bc1b6d0b5815d9bb1fc9006b571795`|
|[supervise.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/supervise.py)|历史Smoke/正式交接监督，不是当前续训守护进程|`a4313f3ffbddce6280883126ef9b482c08f4714975386b3a809e59c1a9ab4213`|
|[supplement_rank_correlations.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/supplement_rank_correlations.py)|由已经导出的图3点补全预登记Spearman点估计；不制造CI/p值|`f4661b64bbc66c3ef5bd819b3c65baf0acf31e334316d441734cb3b074b20ab8`|
|[teacher.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/teacher.py)|冻结teacher/SAE装载、特征提取、打分和数据/源文件身份|`5ca42c29f41f9714e3447789878535496be9a82f6c15dc1b3e8d1191f425861f`|
|[urgent_runner.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/urgent_runner.py)|A1/A2独立锁、50步Smoke、从零至2000、auto恢复与任务内接续；每阶段最多三次异常重试|`f13c5cc30a08801e4938eea239f5383dfa719d4384d4134f9636d30ec6839ddb`|
|[urgent_status.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/urgent_status.py)|按需读平台/持久日志、步数/吞吐/ETA；此次已停止继续查询|`454a12f5e3295960047a83378d60850a19f5b10d1402920aede9bf16035037de`|
|[urgent_watch.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/urgent_watch.py)|原前台监督/异常重新提交观察器；研究者要求后已停止，不代表ACP任务停止|`dbfa5e5a7abf76c3e1e557046405932c1273e6ec054a72e64451819569f514f9`|
|[validate_scores_urgent.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/validate_scores_urgent.py)|逐分片、逐rank、逐micro验证输入身份/shape/有限性/冻结身份；发现不一致即失败|`0a2343fb4dc7c881ffcb265cc58c57e5124f8719730a2bbc8408c8bf8e737707`|
|[verify_gates.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/verify_gates.py)|历史启动放行证据核对|`f7df6589343eb55eb70b7ce02ece64af44ce1d077b2853f3f19169cdd0c99cf6`|
|[verify_precision.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/verify_precision.py)|冻结DEV bf16/fp32路由一致率检查|`d67f9a865ee8500e46262b2711d7467d48cd6cad38a931e9e4b09a9273d11717`|
|[write_2000_report.py](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/write_2000_report.py)|从统一表格生成中文趋势/假设对照、可携带阅读入口及R03 Summary|`4ecc2894ee7b1a5333e640de550f832a82b6e1c5964b304eae5a81ac3da344e1`|

## 当前源码快照及历史边界

- [本次源码快照清单](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/script_record_20261109T024017Z/manifest.json)：源文件、完整SHA256和执行侧副本；[本memory机器可读索引](script_sources.json)。

- `R/evidence/release_20261108T174752Z/`：原资格检查后的训练源版本。
- `R/evidence/urgent_before_20261109T002557Z/`、`urgent_release_20261109T002855Z/`、`urgent_teardown_repair_source/`：紧急修改前、首版、NCCL退出清理修复。旧run_chain保护前版本单存`legacy_run_chain_before_urgent_guard.py`。
- 各 `R/analysis/urgent_step*/source/` 保存对应分析实际producer。2000完成证据指向 `urgent_step2000_1794190105831043306`。analysis_urgent.py的2000实际SHA为`88d3e18c38d8c1535eba6d9cad648ca42c47ab1d3b33f815ab7a75aeadc6d310`，分派入口SHA为`5c99f5f60a35855c5789a1325fdc03a62a53183872df7860f728dc980c8cc0ce`。
- 旧hook版本完成过40步直跑/20+20配对；不能借此宣称关闭hook后的新引擎也完成同样外部打断等价性检查。新Smoke/首段重放、真实存档恢复证据分开记录。
- 当前文件含后续修复，不声称历史两个父进程均加载了最新urgent_runner；以release、实际日志和resolved_config/startup证据核对。

## 外部依赖和提交来源

- 规范提交/资源解析：`/data/250010109/Research_System/templates/execution/acp_submit_template.sh`、`resolve_execution_envelope.py`、`docs/execution_envelope.md`。dry-run、Reserved、显式workspace和实际回执为准。
- 工作区CLI辅助：`/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/agent_submission_guide/sco_workspace.py`。
- 原兼容shell：`/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh`。只记录位置，不复制凭据或账户配置。
- 原代码复用与输入身份：`R/evidence/original_code_and_logs_audit.json`、`source_changes.diff`、`R/inputs/initial_identity.json`及R03 Protocol。冻结data/frozen.pt的SHA256为`dd42eb4fec8400615d3b4c64827ac91cd508bc1607d734b15c8088ded370deed`。

## 结果与下一次接续

- [2000步结果入口](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/README.md)、[中文趋势分析](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/01_analysis_cn.md)、[ZIP](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z.zip)。ZIP SHA256：`7d830215c03eb0225eb424d46d58b20e3cd6c4fbc2220af44b9fd208b6807745`。
- 2000步完成证据：`R/evidence/urgent_2000_completion_certificate.json`；包校验：`R/evidence/2000_bundle_final_validation.json`。实际checkpoint已入资产目录，strict回执是 `urgent_assets_2000_access_20261109T0214Z.json`，不是全库strict通过。
- 科学判断Unknown；单种子、≤2000步、固定路由无router梯度回流。AI候选解释已单独标记，不能从memory推定研究者确认。
- 本次不commit/push、不恢复监督、不重新提交任务。下次若用户要求状态，先读现有任务和持久存档；不要因观察器停止就直接创建重复任务。
