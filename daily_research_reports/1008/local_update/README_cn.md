# 局部更新报告：阅读、证据与复现

[一分钟稿](../meeting_report/meeting_brief_local_update_cn.md) · [完整版](full_report_cn.md) · [当天入口](../README_cn.md)

先读完整版第1—5节建立目的、模型、测量量、假设与认识更新，再读第6节数据分析。本文与附件是派生读本，不修改原始结果和科学设计。

## 图的顺序

组会配图优先：[四张简洁版图与图外解释](conclusion_figures_cn.md)：受控条件 → 自然跨域收益 → SAE领域差异 → 更新方向与loss影响。新图统一留白、配色、必要标注，提供300 dpi PNG及SVG；[新图来源](evidence/report_figures_provenance.json)。SAE重构图不再进入组会配图。

附件的辅助图完整保留：aux01受控两点曲线、aux02自然均值与位置比例、aux03 SAE三项检查。每张图同时提供同名PNG/SVG；详见[图来源记录](evidence/figures_provenance.json)。正文解释决定性数字，缺少图片时仍能阅读。

## 复现

- [现有证据绘图脚本](scripts/build_existing_figures.py)：使用执行侧原CSV和冻结字典/激活缓存；图源记录保存列映射、单位、死区、样本与hash。
- [新增梯度审计脚本](scripts/gradient_component_audit.py)：读取计算前冻结recipe后运行；每个完成目录禁止覆盖。原幅度/等范数两个基底，k=1—4及全/半步全部保留。
- 新审计原始目录：`/data/250010109/MoE_Router/experiments/20261008_local_update_component_audit/runs/full_cpu_01/`。原component_arrays.npz与日志留该目录，报告只复制小型表与收据。
- [梯度审计recipe](evidence/gradient_component_recipe.json)、[完成收据](evidence/gradient_component_receipt.json)、[独立复算](evidence/gradient_component_independent_audit.json)。原始四来源梯度、旧R与有限效果的身份均检查；不重拟合LM或SAE。
- [推理审计及修订记录](evidence/reasoning_audit_cn.md)：核查数学闭环、原假设裁决、代理指标和结论条件；数值核查与科学判断分别记录。
- [payload清单](payload_manifest.json)记录本次选择的图表证据；[交付检查](delivery_checks.json)记录实际检查范围，不把源码检查当数学渲染或科学确认。

绘图脚本的CLI以其`--help`为准。需要重复新分析时新建run目录、复制冻结recipe，不能覆盖已经完成的run；方向与候选选择规则不得按接收结果改写。

## 来源与边界

System与独立项目均已执行`git pull --ff-only`，两者均已是远端最新版本。System基准为`6838ffb759b1d0e9a8dd6b042ada9c5f6a649094`，项目Xingyu基准为`0959b841cb82997f8c845b3e871a0d978cf36db4`。两份用户附件保留原文、不照搬其中过时的缺项说明；最新用户明确授权新增梯度审计及必要4H100 reserved，本次已有缓存足够，实际仅做CPU诊断。

原受控Summary的强净伤害预测未实现，原自然测量的曝光/固定源边界保留。梯度审计的方向只由四个来源平均梯度选取，有限响应由原模型历史测量提供；它支持局部关系，不证明共同语义、目标前预测或长期共享效用。原字典列能量、参数梯度能量和损失作用各有分母，不互称解释率。
