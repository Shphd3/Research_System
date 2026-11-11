# Conversation Memory: 1111-A5持续续训

接续 `1111-A5续训到1B`（R06）。研究者判断 Unknown。

## 2026-11-11 06:23:23Z
- Summary: 研究者确认按附件启动 A5 R07。复用 R06，调整资源拓扑、总体评估、存档和续提。
- Current work: R06 起点 3816 步 SHA 已核对，原生 3B/5B/10B 存档步数 11446/19076/38150。预留 45 GB。
- Next action: 在 share-space 先尝试两台各两卡的正式任务，若失败在授权窗口内回退到单机四卡。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/inputs.json

## 2026-11-11T06:34:46Z

- Summary: 研究者明确指定两台各两卡 H100 Reserved 并要求尽量优化速度。停止 5090 作业 om-5a7km9c8 和旧监督进程。
- Current work: 继续使用 R06 冻结训练条件。H100 候选 n6ls.iu.i40.2 ×2，share-space Reserved。
- Next action: 提交 H100 正式作业，监督其前 20 步。MIG 测量只由 H100 验收触发。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/stop_5090_user_request.txt

## 2026-11-11 06:38:34Z
- Summary: H100 Reserved 任务 om-8v93ahuv 已提交。5090 前序任务已 SUSPENDED，未产生优化器更新。H100 两 worker 已各见 2 张 H100。
- Current work: 等四 rank 恢复及前 20 步；MIG 分析随 H100 验收启动。
- References: /data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/supervision.jsonl

## 2026-11-11T06:41:23.390894+00:00

- Summary: STARTUP_PASS {"filesystem_free_bytes": 95972339875840, "first_step": 3817, "job": "r07-a5-h100-2x2-01", "last_step": 3836, "layout": "2x2", "median_step_seconds": 2.9261176586151123, "r06_step_seconds": 3.3852412700653076, "r06_training_ce50": 3.7230505944788455, "ranks": [{"gpu": "NVIDIA H100 80GB HBM3", "hostname": "om-c7c92e15cc7c44f3b34d9436667e8af6-worker-0", "local_rank": 0, "rank": 0, "teacher_positions": 16384, "teacher_top_k": 32}, {"gpu": "NVIDIA H100 80GB HBM3", "hostname": "om-c7c92e15cc7c44f3b34d9436667e8af6-worker-0", "local_rank": 1, "rank": 1, "teacher_positions": 16384, "teacher_top_k": 32}, {"gpu": "NVIDIA H100 80GB HBM3", "hostname": "om-c7c92e15cc7c44f3b34d9436667e8af6-worker-1", "local_rank": 0, "rank": 2, "teacher_positions": 16384, "teacher_top_k": 32}, {"gpu": "NVIDIA H100 80GB HBM3", "hostname": "om-c7c92e15cc7c44f3b34d9436667e8af6-worker-1", "local_rank": 1, "rank": 3, "teacher_positions": 16384, "teacher_top_k": 32}], "reasons": [], "status": "PASS", "step_time_ratio": 0.8643749219560537, "tokens_seen": 1005584384, "training_ce20": 3.764426005631685}
- References: /data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/supervision.jsonl

## 2026-11-11 07:04:04Z
- Summary: 双机 H100 正式 20 步验收通过，首次可恢复存档第 3836 步。R04 历史单机 H100 更新约 2.79 秒，R07 双机约 2.88 秒，差约 +3% 至 +4%。两者微批及累积不同。
- Current work: MIG 测量 B 初始六存档完成。1B 整个参数块低频比 1.203、高频比 0.936，逐专家加权比 0.925／0.813。A 已接入 1B。研究者判断 Unknown。
- Next action: 继续监督 om-8v93ahuv，3B、5B、10B 的存档与测量自动落盘。若控制宿主被换，使用执行目录下 scripts/start_observers.sh 恢复观察。
- References: /data/250010109/Research_System/daily_research_reports/1113/meeting_report/a5_continue/README_cn.md

## 2026-11-11T14:45:38.792470+00:00

- Summary: MILESTONE {"step": 11446, "tokens_seen": 3000500224, "nll": 3.3959549877406885, "baseline_tokens": 3000000000, "native_nll": 3.3942828329868777, "checkpoint": "/data/250010109/MoE_Router/experiments/20261111_a5_continue/runs/A5/milestones/token_003000500224"}
- References: /data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/supervision.jsonl
