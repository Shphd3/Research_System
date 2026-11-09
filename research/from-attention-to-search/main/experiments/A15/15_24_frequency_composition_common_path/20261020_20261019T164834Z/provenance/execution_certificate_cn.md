# 执行证书：频率混合表征与高频路径调用

Owner：../protocol_cn.md。原任务FAILED；恢复任务SUCCEEDED；仅工程完成，不授予科学判断。

| 资源字段 | 实际值 |
|---|---|
| profile / surface | h100-4-reserved / ACP |
| workspace / aec2 | share-space / share-cluster |
| spec / nodes / processes | n6ls.iu.i40.4 / 1 / 4 |
| GPU / quota / priority | 4×H100 80GB SXM5 / Reserved / normal |
| image | shphd-lite-0911；URL见提交receipt |
| mount | 01995892-d478-76d8-aec7-13fd8284477e:/data |
| original job | pt-gzle2ypd，FAILED，AFS flock EAGAIN |
| recovery job | pt-4kefocs4，SUCCEEDED，2026-10-20T02:03:08Z—02:05:12Z |
| submission | 官方acp_submit_template，DRY_RUN=0、ALLOW_SUBMIT=1、PROTOCOL_APPROVED=1；原smoke通过后才formal |
| resume command | python -u code/training_recovery_pipeline.py |

冻结配置、原trainer及已完成T_F不变；wrapper仅有界重试blocking文件锁。smoke与T_F复用，六模型补齐，八模型完成后统一DEV。原任务与新任务无重叠GPU预约。最终完整性在final_training_audit.json和final_evaluation_receipt.json；两个job的终态与pod持久日志在执行根provenance/acp和acp_receipts/pod。

有效batch512、micro128、每个条件独立单GPU、4个条件并行；最后batch44。1epoch/168更新/85,548有效答案目标。每种子同初始化与PCG64顺序；里程点0/42/84/126/168对应0/21504/43008/64512/85548目标。TensorBoard位于training/<condition>/seed<seed>/tensorboard，tokens/train_lm_loss使用有效目标均值，验证完整TRAIN/EVAL，原冻结token归一化保持不变。没有路由正则。

初始/工程smoke已实际验证零旁支logits、梯度、下一更新完全恢复；正式endpoint保存完整训练状态但未另做Full续训重演。8个模型均满足保存与指标要求，稀有feature统计/机制资格仍BOUNDED。累计主动远程228.934秒；约9小时对话中断单列，不能声称连续120分钟墙钟完成。
