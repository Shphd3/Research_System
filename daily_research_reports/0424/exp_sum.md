## 证据 1：模型里确实有“通用成分”
**假设：**
模型内部混着一块很多 token 都会共享的通用信息，和一块更偏长尾、领域相关的信息。
**实验：**
我们对真实模型第 8 层的表征做谱分解，先找出最强的共享高方差方向，再分别看不同部分对语义区分和下一词预测的影响。
**结果：**
真实 hidden 中确实存在 shared head；去掉这个 shared head 后，剩余表征更适合作为 expert 的输入。前面联合报告也把这点总结为：真实 hidden 中存在 shared head，single-layer tail-conditioned block 在真实模型上成立。
**说明：**
所以“通用信息”和“长尾可塑信息”不是完全一锅粥，分开处理是有依据的。
## 证据 2：分开学更能让模型看到长尾语义
**假设：**
如果 expert 直接学原始表征，它会同时看到通用成分和长尾成分，容易学成普通 dense 模块；如果让 expert 学去掉通用成分后的 residual，它应该更稳。
**实验：**
我们把真实模型第 8 层前馈模块换成几种结构，比较普通前馈、普通 MoE、以及让 expert 学去掉通用成分后表征的结构。
普通前馈是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F(x)$$
普通 MoE 是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + \sum_e g_e(x)F_e(x)$$
expert 学 residual 的结构是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{\mathrm{residual}})$$
**结果：**
真实单层实验里，让 expert 看 residual 的结构更稳、更好；机制拆解也说明，当前最关键的收益来自：
$$F_e(x) \rightarrow F_e(x_{\mathrm{residual}})$$
而不是单纯让 router 换输入。
**说明：**
所以“分开学”不是只停留在想法或 toy setting，而是已经在真实模型上看到了收益。

## 证据 3：`u50_ext` 是当前更合适的候选输入，但不是唯一被证明可行的输入
**假设：**
去掉 spike 后的 residual 里面不全是同一种长尾信息。full tail 可能有用，但太粗；真正适合少样本更新的输入，可能是其中功能更集中的一段。
**实验：**
我们先把 residual 拆成 mid 和 ext，看移除不同部分对下一词预测 loss 的影响；再继续把 mid 细分，比较 `u25`、`u50`、`u50_ext` 等候选输入在静态训练和 CL smoke 中的表现。
`u50_ext` 的定义是：
$$x_{u50_ext} = P_{[17,398]}(x-\mu) + 0.25P_{[782,d]}(x-\mu)$$
也就是：
> mid 前半段的功能区域，加上一点极低方差 residual 的弱补充。
**结果：**
移除 mid 的 loss 增量是：
$$0.0542$$
移除 ext 的 loss 增量是：
$$0.0038$$
说明主要功能不在极低方差尾端，而在 mid / upper-mid。进一步实验中，静态 old-stage 更偏 `u25`，但进入 CL 后更偏 `u50_ext`。联合报告明确总结为：`full PCA tail residual` 不再适合作为 CL-MoE 第一版 expert input，真正更有前景的是 mid / upper-mid family；进入 CL 后更偏向更完整的 functional span，也就是 `u50_ext`。
**说明：**
这里不能说其他输入都不适合。更准确地说：full tail 不是没用，而是太粗；`u25` 也有静态训练价值；但在当前 CL 主线里，`u50_ext` 是证据最稳的阶段性候选输入。
## 证据 4：expert 的专一性不能只看下一词预测优势，还要防止路由坍塌
**假设：**
如果 expert 真学到了有用分工，那么被选中的 expert 应该比其他 expert 更适合当前 token。但这个定义必须排除一种假象：如果路由坍塌，只有一个 expert 被充分训练，它当然可能比其他 expert 强。
**实验：**
我们对同一个 token，直接比较“被选中的 expert”和“替代 expert”谁的下一词预测损失更低：
$$G_{\mathrm{cf}}(t,e') = \ell_t(e') - \ell_t(e^\star)$$
如果 $G_{\mathrm{cf}}>0$，说明被选 expert 在这个 token 上有功能优势。
但下一步还需要同时检查 expert load、有效 expert 数，以及 own-region advantage，防止把单一 dominant expert 误判成 specialization。
**结果：**
之前的实验显示，被选中的 expert 在中频和稀有 token 上确实有正的下一词预测优势，说明 tail-conditioned block 已经出现了一定的 LM-relevant specialization。
**说明：**
这说明 expert 分工已经不只是表面聚类，但还不能作为最终 CL-specialization 定义。后续必须升级为三层判断：
1. 路由不能坍塌；
2. 被选 expert 在自己的 token 区域有 next-token 优势；
3. 更新后新知识学得更多、旧知识忘得更少。
---
## 证据 5：持续学习实验中，过长更新会冲坏前面学到的收益
**假设：**
进入持续学习后，如果失败，不一定是输入选错，也可能是更新过程本身出了问题。
**实验：**
我们固定更合理的输入候选 `u50_ext`，比较不同 adaptation steps 下的新知识 learning gain 和旧知识 forgetting cost。
**结果：**
短步数 $U=4/8$ 时，多组已经进入 $LG\geq 0$ 的区间；但 $U=16/32$ 后，几乎系统性转负。联合报告总结为：当前 CL 失败的第一原因不是 band 选错，而是 adaptation horizon 过长，长步数会 over-update。
**说明：**
所以当时的瓶颈不是继续盲目切表征空间，而是先固定 `u50_ext` 和短步数，进入正式 matched forgetting 比较。
---
## 证据 6：固定 `u50_ext` 和短步数后，分离式结构已经有正式 CL 收益
**假设：**
如果 common branch 保存通用能力，plastic branch 只在 `u50_ext` 上更新，那么模型应该更适合少样本学习，并且更少遗忘。
**实验：**
我们固定 `u50_ext`，固定 $U=8$，比较普通 dense、分离式结构、带 router 的 expert 结构，以及 dense + replay。
普通 dense 是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F(x)$$
分离式结构是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + F_p(x_{u50_ext})$$
带 router 的 expert 结构是：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50_ext})$$
**结果：**
在稳定的 $0.5\times$ 设置下，普通 dense 的 learning gain 是：
$$-0.000251$$
forgetting cost 是：
$$0.000786$$
分离式结构的 learning gain 变成：
$$0.000803$$
forgetting cost 降到：
$$0.000082$$
matched forgetting 也从：
$$-0.000017$$
改善到：
$$-0.000212$$
因此正式报告的 Gate A 是：
$$G2_{u50_ext} > G0$$
成立。
**说明：**
这说明 `u50_ext` 上的分离式 common/plastic 结构不只是静态表征猜想，而是已经给出了真实 CL 价值。

## 证据 7：当前瓶颈是 router 还没有稳定带来额外 CL 收益
**假设：**
如果 router 真有用，带 router 的 expert 结构应该稳定超过不带 router 的分离式结构。
**实验：**
我们比较：
分离式结构：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + F_p(x_{u50_ext})$$
和带 router 的 expert 结构：
$$h_{\mathrm{out}} = h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50_ext})$$
**结果：**
带 router 的结构 fixed-budget RAS 略高：
$$0.000671 \quad\text{vs}\quad 0.000503$$
但 matched forgetting 没有更好：
$$-0.000184 \quad\text{vs}\quad -0.000212$$
ReachRate 也没有更高：
$$0.200 \quad\text{vs}\quad 0.217$$
所以正式报告的 Gate B 是：
$$G4_{u50_ext} > G2_{u50_ext}$$
当前不能成立。
**说明：**
这说明“把数据分开”还不能推出“expert 已经形成 CL 意义上的专门化”。下一步应该检查 router 是否真的选到了功能最优、更新后更少遗忘的 expert，而不是直接进入更复杂的 hierarchy。
