# 来源与本次查阅范围

## 用户上传来源

- `03_mini_paper_cn.md`：本次完整读取的探索性中文论文草稿；副本在本目录。它综合既有记录，不包含新的独立模型复现。第2节提供局部公式，第3节区分实验参数位置，第4节提供已报告结果，第5—7节提供边界和建议。
- 当前对话中的导师转写 `0924-指导.md`：明确要求先理解表征结构与参数更新关系，并将SAE定位为分析工具；没有规定唯一统计坐标或正态分布定律。
- 当前对话及其此前上传记录：本次新设计的研究方向和材料分离要求来自用户；精确构造、数字和阈值由本次提出，均有提案标记。
- `loss_conflict_true.png`、`loss_conflict_not_necessary.png`：先前对话生成的直观损失示意，不是实测图，也不证明主实验任务具有共同解。

## 本次实际读取的 Research_System 文件

仓库：Shphd3/Research_System，读取日期2026-09-27。以下均为读操作，未写回。

- `.agents/skills/research-reasoning-auditor/SKILL.md`，blob SHA f6ab2f1678c6ebe3ce67764ba36abe499111fc55。
- `.agents/skills/research-reasoning-auditor/references/reasoning_audit_contract.md`，blob SHA 361e20ae6f770fa3d379d257b9d85aeb711d02fb；重复错误模式的全文已在本对话先前读取并继续可见。
- `.agents/skills/problem-anchor-writer/SKILL.md` 及 `references/anchor_self_containment.md`、`judgment_review.md`、`learnable_research_design.md`。
- `.agents/skills/experiment-card-writer/SKILL.md` 及 `references/protocol_focus_alignment.md`、`blockwise_protocol_audit.md`、`protocol_self_containment_and_freeze.md`。
- `docs/training_observability_contract.md`。
- `daily_research_reports/0926/docs/atom_mechanism/protocol.md`，blob SHA 387d1603c6235003009fb464365540665098670c。读取了修订A2，确认旧正文1024×1024被1024×2048修订；未将旧实验执行授权当成本轮授权。
- `daily_research_reports/0926/docs/atom_mechanism/detailed.md`：本次读取显示的第1—13节相关内容；响应尾部截断，因此不声称全文完整核读。它确认观察attention输出、更新attention输出投影，以及先前down更新不会改变上游SAE表征。
- `daily_research_reports/0926/report_assets/collect_structure_update.py`，blob SHA ce7f97adb75543b15318376979d3396e4f27ecbb。读取加载manifest路径、`load_model`入口、原字段、更新归一化和原下投影数值核验。它是旧下投影实现，不可直接充当新attention-tail适配器。

项目文档的入口：
https://github.com/Shphd3/Research_System/blob/master/daily_research_reports/0926/docs/atom_mechanism/protocol.md
https://github.com/Shphd3/Research_System/blob/master/daily_research_reports/0926/report_assets/collect_structure_update.py

## 外部原始来源：仅用于背景及接口核对

- Tianhe Yu et al., *Gradient Surgery for Multi-Task Learning*, 2020：梯度冲突并非本研究新提出的现象；不将其结果当作本次S7实验的证据。
  https://arxiv.org/abs/2001.06782
- PyTorch 官方 `torch.autograd.grad` 文档，访问2026-09-27：核对它返回输出对输入的梯度求和语义，并据此避免对每样本导数重复除以样本数。采用稳定基本接口，不依赖当日新增的实验性批量功能。
  https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad.html

## 不能被本次查阅替代的核验

本环境没有原S7权重、原GPU计算、其源代码运行上下文和原始大型数组。历史绝对路径只来自已读取项目文件；当前路径是否挂载、运行API是否可用、完整tail及SAE纯编码接口是否一致，仍需执行前核验。所有新假设、构造与阈值不是既有文件已经批准的事实。

## 2026-09-27 后续33B锚点核验

此节记录本轮实际新增的只读检查，不倒改上面原包制作时的环境叙述。当前挂载可读取 `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/manifest.json` 和 `state.pt`。manifest标记完整，精确33,000,000,000训练词元、step 125894；重新计算state SHA256为 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`，与manifest一致。只读mmap载入显示目标矩阵 `blocks.7.attn.o.weight` 为1024×2048、SAE为末块raw Attention输出sidecar，λ_rec=0.1、宽30000、Top-K=32。当前没有完成GPU原生回放或SAE纯编码核验。
