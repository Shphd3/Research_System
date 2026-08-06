# NTP Conditional Low-Rank Theory Package

这是 `Research_System` 中 A14 条件低秩理论的唯一可编辑版本。原始 zip 只保留为
不可变来源；`kv_cache/xyDeng` 中的 theory-only 目录是 2026-07-24 的发布快照，
不在本仓库另建第二套同步备份。

## 包内容与状态

| 文件 | 作用 | 状态 |
|---|---|---|
| [04_物理先验与假设审计.md](04_物理先验与假设审计.md) | 区分语言先验、数学假设、测量守卫与开放桥 | 已纳入 E04–E06 的 local/finite 双桥审计 |
| [01_理论论文_共享组合结构与条件低有效秩.md](01_理论论文_共享组合结构与条件低有效秩.md) | self-contained 建模、T0–T9 定理链与 claim boundary | 本地 v1.2；有限训练桥改为 secant/path-integrated image |
| [02_证明附录.md](02_证明附录.md) | 集中界、参数子空间、Jacobian、secant、effective-rank 与流程图 | 本地 v1.2；新增有限路径积分证明与实验依赖图 |
| [references.bib](references.bib) | 参考文献 | 与 `xyDeng` 同步版一致 |
| [03_实验协议.md](03_实验协议.md) | 原包提出的后续实验合同 | 历史设计；H9 部分已由项目内 E04–E06 替代 |
| [05_审核清单.md](05_审核清单.md) | 原包的协议审核清单 | 历史审核清单；未同步 |

推荐按 `04 → 01 → 02` 阅读理论；只有需要审议新实验时才读取 `03 → 05`。

## 当前条件结论

在简化一层 NTP Transformer 中，若共享任务映射、概率稀疏调用、独立 context
消噪、受控任务参数更新和共享 ROOT path image 同时成立，则固定读出任务功能秩
在显式误差预算下以高概率受 $sr$ 控制。对有限训练位移，`path image` 现在
明确指精确 learned secant／路径积分像；单点 Jacobian 版本只适用于 Taylor
余项已经显式测得很小的局部更新。

这不是“NTP 自动产生低秩”的无条件结论。E04 在 5/5 seeds 支持训练点的局部
共享 Jacobian 像；E05/E06 又表明实际八维参数位移和精确有限 ROOT 效应都低维，
但单点线性化在 5/5 seeds 失效。因此当前开放条件不再是“局部 H9 是否可能”，
而是何时 NTP 动力学会产生共享的 finite secant/path-integrated image。

## 来源与同步边界

- 原始来源：
  `daily_research_reports/0724/NTP_conditional_low_rank_theory_package.zip`
- 原始 zip SHA-256：
  `9f16514854e10299d25ebf0358f519a77eef9b4b3a19698a2d4dfd00b5056746`
- 2026-07-24 theory-only 发布快照：
  `Projects/kv_cache/xyDeng/sync/2026-07-24/a14_ntp_conditional_low_rank_theory/`
- 发布分支与 commit：
  `xyDeng` / `efd91334458bc301f608e2800f54d83625df7830`

该 commit 对应 v1.1，不含 2026-07-25 的 E04–E06 认识更新。本地 v1.2 继续
使用 `$$...$$` 展示公式和 `$...$` 行内公式，并新增 local H9-L 与 finite H9-F
双桥、路径积分充分条件、H11 失效证据和新的证明流程图。除非用户再次明确要求，
本轮不向 `kv_cache` 发布、提交或推送。
