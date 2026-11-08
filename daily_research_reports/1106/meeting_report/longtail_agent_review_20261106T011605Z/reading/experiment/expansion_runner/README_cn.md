# 耐久整套扩量执行器

这里只新增执行root下runner，不改冻结source/plan/core/stats，不提交新作业，不写catalog，不按准确率/loss选臂或调参。开发测试没有GPU动作。

入口run_expansion.py：--root R --gpus 2 --out R/expansion_runner/runtime_0044 --controller-start 2026-11-05T16:48:33.980235+00:00 --max-hours 28 --reserve-hours 2 --cost-safety-factor 1.25 --dry-run。审核后才改--execute，由当前worker直接调用；已有out需--resume-existing。执行会核父PID为worker_live.pid、同资源profile和两张可见GPU。没有submit命令。

初始不是36个阶段，而是队列0032–0036五阶段；逐项核实际子任务4/12/36/12/76全部COMPLETE/exit0、计划SHA及训练证书。再核0037–0043、三mode完整20k合并、expanded_greedy_semantic_v4冻结manifest。Protocol锁定e92dd33c7f3ce1c17f98efd8b3b224450005e1cff5f91e0de684797a82acbe01。选8192和最大balanced eligible<=20000，排除已完成2048，不复制“最好一臂”。

每规模15步：新cache32GiB→学生/教师NPROC2→完整verify→复用完全相同128sentinel和192诊断事实→生成三评测/两训练计划→pre、trainA、afterA、trainB、afterB整套执行。scale参数是数字字符串；路径保持plans/N、runs/N/seed/arm/A或B、batch_logs/N_stage。新数据只复制事实及原问题，不生成新问法或按成绩选案例。

预算只读墙钟、缓存/准备耗时、实际文件大小和df。最多控制器28h，始终保留2h验证。首次max暂DEFER并非永久：8192完整后，用其真实15步耗时、规模、存储和当前剩余时间重新预算所有未跑规模；可以转为ADMIT。每次decision追加历史，不覆盖旧判断。若8192不fit就整套延期，不换成部分优胜臂。

每步记录完整argv、输入/源码哈希、日志、开始结束、exit、耗时及输出身份。完成步骤重新核对后跳过，不重复进程；已有输出无可靠receipt、RUNNING中断、失败或身份变化都要求显式recovery，绝不force覆盖。启动的子进程独立process group，超时只TERM/KILL自身组；父worker和其他任务不杀。STOP文件在后续步骤前生效。

state.json、steps/*.receipt.json和runner_receipt.json是纯runtime监控；runtime_calibration按完成规模存成本。registration_requests保存实际cache/dataset/checkpoint引用给root登记，失败阶段已保存部分明确标记，不写全局catalog、不编asset ID。大payload按完成SHA+大小/mtime链及一次深校验，不重复全量hash；这种边界明确记录。

9项CPU/假进程测试通过，包含8k后重新放行max、完成步骤不重复、孤儿/失败要求恢复、固定sentinel/diag、15步CLI顺序、2h余量/预算追加，以及只终止自身CPU睡眠子进程而不影响旁边测试进程。没有训练或模型推理。
