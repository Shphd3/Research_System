# Thinking Card：精确源 K/V 是否形成稳定的 branch 信息

状态：**研究者已完成理解审核并批准进入远程四卡 GPU 实验。**
日期：2026-07-16

> 这张卡只定位已完成 K/V 因果干预的失败阶段，不是新 Protocol，也不授权训练、重新运行或结构修改。

## Human Draft

### Phenomenon / 现象

已知：

1. informative-MTP 的第二头能够从 `U03` 最终隐藏状态预测 branch 答案；
2. 最终隐藏状态替换正控制能够使答案切换到供体 branch；
3. 但精确第二层 `U03` 源 K/V 补丁没有产生跨种子、跨 branch 对稳定的标准主头答案切换增量。

当前缺失的事实是：

> 第二层注意力计算前形成的精确
> $S_{2,T}=[K_{2,T};V_{2,T}]$
> 是否已经携带可跨 nuisance 泛化的 branch 信息？

**本卡目的：** 区分“branch 信息没有稳定进入被干预的精确 K/V”与“branch 信息已经进入精确 K/V，但没有转化为稳定的标准主头强行为控制”。

### Mechanism guess / 机制猜想

研究者当前猜想：

> `U03` 最终隐藏状态能够预测 branch，因此精确 K/V 中应当已经含有 branch 信息；这些信息已经进入源 K/V，但标准主通路没有使用。

需要研究者进一步确认：

- “没有使用”是指完全没有因果作用，还是没有形成足以稳定改变最终答案的强因果作用？
- 是否接受“最终隐藏状态可读不保证同层注意力计算前的 K/V 可读”这一时序边界？
  确认：我觉得是没有形成足以改变最终答案的强因果作用和那个
  不太接受可读性不一致

### Strongest rival explanation / 最强替代解释

**Unknown，等待研究者选择或改写。**

候选替代解释仅供思考：
1. 标准主头可能弱使用或冗余使用这条 K/V 路径，但直接 `BR_z` 路径和饱和答案 margin 使 K/V 替换不足以稳定翻转 argmax。
---
1. branch 信息主要在第二层注意力、MLP 与最终归一化之后形成，因此最终隐藏状态可读，但第二层计算前的 K/V 未必可读；
2. NTP、shared-aux 和 informative-MTP 都可能通过更早的 `BR_z` 路径在 K/V 中携带 branch 信息，因此可读性不一定是 MTP 特异增强；
3. 标准主头可能弱使用或冗余使用这条 K/V 路径，但直接 `BR_z` 路径和饱和答案 margin 使 K/V 替换不足以稳定翻转 argmax。

研究者认定的最强替代解释：
1. 标准主头可能弱使用或冗余使用这条 K/V 路径，但直接 `BR_z` 路径和饱和答案 margin 使 K/V 替换不足以稳定翻转 argmax。

### Most uncertain point / 最不确定之处

研究者当前回答：

> 最不确定的是标准主头能否利用 branch 信息。

需要补充：

> 在本次 source-information audit 中，最不确定的是精确 K/V 是否形成稳定 branch 信息，还是形成程度是否具有 informative-MTP 特异增强？
> 
我觉得最不确定的是形成程度具有informative-MTP的特异性增强

### Evidence that would change my mind / 改变判断的证据

**待研究者填写。**

- 若 informative-MTP 的精确 K/V 在 held-out 数据上接近随机且分离很弱，我会如何修改“信息已经进入 K/V”的判断？
信息并未进入
- 若 informative-MTP 的 K/V 稳定可读，但与 shared-aux、NTP 同样可读，我会如何修改“MTP 特异增强”的判断’
那说明共享信息是由attention加入的，并不是MTP特异性增强的
- 若 informative-MTP 的 K/V 比 shared-aux 更稳定可读、分离更强，而原 K/V 补丁仍无稳定强效应，我会如何修改“形成—利用”机制判断？
那说明MTP确实督促了K/V形成了远程监督的特异性信息。

请分别写明：

- 若 informative-MTP 的精确 K/V 在 held-out 数据上接近随机且分离很弱，我会如何修改“信息已经进入 K/V”的判断？
- 若 informative-MTP 的 K/V 稳定可读，但与 shared-aux、NTP 同样可读，我会如何修改“MTP 特异增强”的判断？
- 若 informative-MTP 的 K/V 比 shared-aux 更稳定可读、分离更强，而原 K/V 补丁仍无稳定强效应，我会如何修改“形成—利用”机制判断？

### Current next decision / 当前唯一决策

AI 候选表达，等待研究者确认：

> 在现有能力匹配检查点上，informative-MTP 的精确第二层 `U03` 源 K/V 是否形成了跨 nuisance、跨种子和跨 branch 对稳定的 branch 信息，从而允许把既有强行为干预失败进一步定位到源信息形成之后？

## Optional Formalization / 可选形式化

以下均为 AI 候选定义，尚未批准。

### Key variables / 关键变量

- 训练条件 $o\in\{NTP,shared\text{-}aux,info\text{-}MTP\}$；
- branch 标签 $Z\in\{0,1,2,3\}$；
- 精确源表示 $S_{o,i}=[K_{2,T};V_{2,T}]\in\mathbb R^{128}$；
- calibration 上训练、confirmation 上冻结评估的四分类线性 probe；
- branch 间/branch 内 Fisher 分离比与六个 branch 对的中心距离。

### Causal relation / 因果方向

研究者候选机制：

$$
\text{informative future target}
\rightarrow
\text{branch information in exact source K/V}
\rightarrow
\text{later standard-head behavior}.
$$

本卡只审计中间第一条箭头是否在精确 K/V 上成立，不重新裁决第二条箭头。

### Primary observable metric / 主要观测指标

候选主要指标：

> informative-MTP 模型内部、在独立 confirmation 集上的 branch 线性 probe 准确率；四分类随机水平为 `0.25`。

Fisher 分离比、六个 branch 对中心距离，以及 informative-MTP 相对 shared-aux/NTP 的差异作为阶段定位和特异性诊断，不自动等同于标准主头使用。

### Pass / fail / insufficient evidence

**通过的候选含义：** informative-MTP 的精确 K/V 在 held-out 数据上稳定线性可读，且分离不只集中在单一种子或单一 branch 对；这支持“精确源 K/V 已形成 branch 信息”，不支持“标准主头已经使用”。

**失败的候选含义：** informative-MTP 的精确 K/V 可读性接近随机且分离很弱；这不证明 K/V 完全没有任何信息，只表示没有观察到稳定、线性可泛化的 branch 信号。

**证据不足的候选含义：** 效应只出现在单一种子或 `3↔1` 一对、校准与确认存在泄漏、probe 超参数由 confirmation 选择，或可读性与分离度给出不稳定结论。

## AI Audit Record

### Judgments to preserve / 必须保留的人的判断

- 研究者倾向于认为 branch 信息已经进入精确 K/V；
- 研究者倾向于认为主要瓶颈在标准主通路的利用；
- 研究者认为 informative-MTP 应当产生信息特异性增强；
- 词表输出矩阵共享属于后续结构实验，不属于本次审计。

### Unclear definitions / 未定义对象

- “主通路没有使用”尚未区分完全零使用、弱使用、冗余使用和不足以翻转答案；
- “MTP 特异性增强”尚未给出相对于 shared-aux 的判据；
- “K/V 中必然含有 branch 信息”尚未区分任意非线性信息与稳定线性可读信息。

### Hidden assumptions / 隐含假设

最终隐藏状态位于第二层注意力、残差、MLP 和最终归一化之后；第二层 K/V 在这些计算之前形成。因此：

$$
q_2(h^{final}_{T})\text{ 可预测 branch}
\centernot\Rightarrow
[K_{2,T};V_{2,T}]\text{ 必然可读}.
$$

### Existing positive control / 既有正控制

直接替换最终隐藏状态已经产生 `1.0` 的供体答案切换率。它说明：

- 输出接口和替换实现能够把足够晚、足够强的供体状态变成供体答案；
- 它绕过了源 K/V、接收 query 和注意力检索，因此不能证明标准主头使用了 K/V 通路。

### Unresolved result interpretation / 尚未解决的结果解释

seed 972 的 K/V 补丁效应几乎只在一个替换方向成立，反向与其他 branch 对接近零。该结果最多说明某一初始化和决策边界下存在单向敏感性，不能证明稳定的双向 branch 通道。

### Human decision on the proposal / 人的最终确认

> 研究者确认：精确第二层 K/V 先形成，随后 `U03` 的 query
> 才能在第二层 attention 中读取更早位置并把 branch 信息写入最终
> hidden；calibration 用于训练 probe，confirmation 用于冻结后的最终
> 研究判断。研究者授权在远程四卡 GPU 上执行 same-contract replay。

### 2026-07-16 AI audit verdict / 本轮审核判定

**判定：部分理解，尚未达到正式批准门槛。**

研究者已经正确理解：

- 当前需要判断的是 informative-MTP 是否在精确源 K/V 中产生特异性 branch 表征；
- 既有结果只否定稳定、足以翻转最终答案的强行为作用，不等于完全零使用；
- 若 informative-MTP 的精确 K/V 比 shared-aux 更可读，最多支持源表示的 MTP 特异增强，仍不能证明标准主头使用。

仍需纠正：

1. `U03` 最终隐藏状态在第二层注意力与 MLP 之后，而 $K_{2,T},V_{2,T}$ 在这些计算之前形成；因此最终隐藏状态可读不能逻辑推出精确 K/V 可读。
2. 若 NTP、shared-aux 和 informative-MTP 同样可读，只能否定可观测的 MTP 特异增强；不能进一步归因于“attention 加入”，因为 embedding、第一层、残差路径和直接 `BR_z` 路径都仍是可能来源。
3. 若线性 probe 接近随机，只能写“未观察到稳定、线性可泛化的 branch 信号”，不能写成“K/V 完全没有 branch 信息”。
4. 研究者选择的“弱使用、冗余使用或答案饱和”是既有下游使用结果的替代解释，不是本次源信息形成问题的最强替代解释。本次最直接的替代解释应是“branch 信息主要在精确 K/V 形成之后才进入最终隐藏状态”，或“所有条件通过普通路径形成相同 K/V 信息”。

## Boundary

本卡不是 Anchor、Protocol 或结果报告。即使精确 K/V 稳定可读，也不能据此声称标准主头利用、MTP 普遍优于 NTP、词表共享能够修复该问题，或真实语言任务会受益。

证据来源：

- [既有因果使用 Thinking Card](11_03_02_standard_head_causal_use_thinking_card_cn.md)
- [A11 K/V 因果使用结果](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)
- [A11 K/V 因果使用详细记录](/Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/detailed.md)
