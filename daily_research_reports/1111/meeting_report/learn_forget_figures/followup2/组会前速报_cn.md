# 1111 组会前补图

AI 分析；研究者判断 Unknown。只用本地 MIG 和 CPU，没有更新参数。[跑前协议](protocol_cn.md)。

## 1｜两种差距放在一起

![0–10B 损失差](01_两种损失差_0到10B.png)

[主图 PDF](01_两种损失差_0到10B.pdf) · [0–1B 线性放大 PNG](01_两种损失差_0到1B放大.png) / [PDF](01_两种损失差_0到1B放大.pdf) · [点值与区间](01_损失差.csv)

**读图：** 蓝线（Dense − 原生 MoE）从 0.5B 到 10B 一直约为 0.09 nat；紫线（原生 MoE − A5）到约 1B 仍为正，但优势由 500/1000/1500/2000 步的 0.180/0.086/0.065/0.044 降到 **0.016 nat**。误差棒是配对文档 95% 区间。紫色虚线提醒：1B 改用正式原生 baseline；A5 实际 1.000341504B。500 步用既有逐位置 loss 补算区间。

## 2｜专家输入谱：只留条件有效秩

![每层条件有效秩比](02_专家输入有效秩.png)

[投屏 PDF](02_专家输入有效秩.pdf) · [逐层中位数和分位数](02_逐层有效秩比.csv)

**读图：** 横轴是层号，纵轴是每个 expert 输入的有效秩除以该层全体输入的有效秩；点为 8 个 expert 的中位数，阴影为专家间 10%–90% 分位。原生 MoE 和 A5 多数层低于随机分发，A5 并非逐层低于原生。三臂均为各自 2000 步训练表征，沿用 F 的既有 EVAL 面板；Dense 虚线 1 是所有输入进入同一个 FFN 时的定义参照。

## 3｜原生路由的输入方向减少，何时形成？

![专家输入秩比随训练变化](03_专家输入有效秩随训练变化.png)

[投屏 PDF](03_专家输入有效秩随训练变化.pdf) · [逐层表](03_逐层有效秩与比值.md) / [CSV](03_逐层有效秩与比值.csv) · [逐 expert 表](03_逐专家有效秩.csv) · [画图点值](03_层段曲线.csv)

**读图：** 先看蓝线与 0.90/0.95 参考线；每个点先在每层取八个 expert 的秩比中位数，再在四层内等权平均。**按预设判据：输入方向的减少在早期形成并保持。** 原生 MoE（0–3 层／4–7 层）：第 500 步：0.745/0.812；第 1000 步：0.742/0.822；第 2000 步：0.744/0.836；1B：0.755/0.832；10B：0.790/0.853；33B：0.813/0.866。A0 的 2000 步及以前与 1B 起正式原生 baseline 的存档来源不同；点间只连已测点，不表示持续观测。Dense 只提供绝对全局秩，见表。

已完成 11/11 个检查点。缺失：无。

**A5 续训对照：** 2000 步的前四层／后四层秩比为 **0.856／0.840**，约 1B（3816 步）为 **0.854／0.842**。两点都是同一套 A5 分发下的实际存档；这一段秩比几乎不变，图 1 中的损失领先却缩小了。

**“方向减少”是相对量。** 从 500 步到 10B，原生 MoE 的全局绝对有效秩，前四层均值从 **122** 增至 **601**，后四层从 **157** 增至 **669**。专家输入相对同阶段全体输入更集中，不代表绝对有效秩越训越低。

## 4｜3B→5B 两种模型共同遗忘了什么

![共同遗忘内容粗分](04_共同遗忘网页模板粗分.png)

[投屏 PDF](04_共同遗忘网页模板粗分.pdf) · [分类汇总](04_模板粗分汇总.csv) · [3169 条代表上下文](04_3169个feature代表上下文.csv)

**读图：** 每个 feature 只用一个代表窗口做关键词粗分，421/3,169（**13.3%**）命中网页模板词，2,748（86.7%）未命中。模板类、其他类的 EVAL 正激活支持位置分别是 **347,504**、**1,180,971** 个；两个集合重叠 316,766 个，并集 1,211,709 个。图右的两个比例以同一个并集作分母，可以合计超过 100%。按 feature×位置计分别为 760,164、4,770,769 次。分类不是人工标注，整个 feature 的所有激活位置并非都包含模板词。

**例子（⟦ ⟧ 标记代表位置的输入 token）：**

- 网页模板文字 · feature 40 · 命中「Categories」： your kid back because of your fears they’d be injured?⏎⏎Categories: Activities⏎Jennifer Gish⏎⏎⟦7⟧ Responses⏎⏎  1. Emalie says:⏎⏎    I was a cheerleader from high school through
- 网页模板文字 · feature 258 · 命中「PingBack」： and on, not to mention VMsafe..etc⏎⏎  • PingBack from http://wareserver⟦.c⟧ouchfan.com/2008/03/14/quick-roundup/⏎⏎ 
- 网页模板文字 · feature 302 · 命中「EditText of this page」：edVerbs⏎⏎EditText of this page (last edited May 18, 201⟦2⟧) or FindPage with title or text search‹¦im_end¦›Record Set⏎⏎An in-memory or transient representation of
- 其他（未命中） · feature 1 ·  of the "flowchart". I remember one time I simply wrote "Returning dd-mmm-yy⟦.⟧ You'll just have to cope until then."⏎⏎The "flowchart" section of the OOF is
- 其他（未命中） · feature 19 ·  in US history:  that known as the "Tri-State" tornado of 18 March ⟦1⟧925.  We talked with living survivors who still have vivid, terrible memories of that day
- 其他（未命中） · feature 21 ·  author,⏎  2. (2) Choose a search parameter,⏎  3. (3⟦)⟧ Click to implement‹¦im_end¦›⏎⏎⏎⏎“Up to 30 million textile and clothing manufacturing workers will lose their
