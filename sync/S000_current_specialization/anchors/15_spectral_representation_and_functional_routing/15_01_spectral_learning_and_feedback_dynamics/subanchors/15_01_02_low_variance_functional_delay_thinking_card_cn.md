---
thinking_card_id: 15_01_02_low_variance_functional_delay
status: human_authorized_full_cycle
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
source: /daily_research_reports/backup/2026/07/0731/conjectures.md
created: 2026-07-31
---

# Thinking Card：低方差频带路由是否退化为随机漂移

> 本卡从研究者的 `conjectures.md` 提取判断。人类判断与 AI 操作化分开记录。

## 人类判断

- **现象：** 小方差方向可能像随机基底一样难以形成稳定路由，并在训练中发生
  严重漂移。
- **机制猜想：** head、middle、tail 的方差差异不仅改变学习速度，也可能改变
  路由分区的稳定性。
- **最不确定的一环：** 目前尚未分别量化 H/M/T 路由稳定性，也没有排除随机
  基底或纯有限时间慢学习。
- **授权：** 研究者允许 AI 自行修正问题、写 Anchor/Protocol、实现并完成正式
  运行，不再要求中间审批。

## AI 操作化提案

- **定义“稳定”：** 不能只看 flip 少；随机 Router 也可能稳定地路由错。使用
  “同时达到 held-out 正确率门和低 flip 门所需时间”定义功能稳定时间。
- **最强 rival：** 小方差只延迟收敛，最终仍形成正确稳定分区，并不退化到随机。
- **最小区分实验：** 将同一个平衡标签以相同维度和相同标准化信噪比分别编码
  到 H/M/T，只改变整体方差；另设等方差与无标签信息的同维随机方向。
- **会改变判断的证据：** 若 native tail 在注册时限内与随机方向同样不能达到
  功能稳定，而等方差 tail 恢复，则支持强猜想；若 native tail 最终稳定且明显
  超过随机，则否定“随机化”强版本，即便速度更慢。
- **当前决策：** pursue；把“速度延迟”和“随机漂移”分别报告。

