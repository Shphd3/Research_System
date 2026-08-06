# Long-horizon compositional workload Thinking Card

日期：2026-07-17

所有者：研究者

状态：研究者已于 2026-07-16 授权按本卡方向自主形式化、逐级实验和重复审计。

本文件不是正式 anchor、sub-anchor、Protocol、实验计划或结果报告。文中标记为
“AI proposal”的内容只用于启发，不代表研究者判断。

## Human Draft

### Phenomenon / 现象

我希望解释的核心现象是：

> MTP 在某些代码、规划或长程组合任务上可能比 all-position NTP 更容易学到
> 有效状态，但这种优势明显依赖 workload。我们目前没有在本组实验中干净地
> 建立这个现象：A12 的 carrier 同时存在 learner capability floor 和
> workload-validity 问题，因此不能把 NTP 学不会或表面差异解释成
> NTP/MTP 目标函数的因果差异。

证据状态：

- “MTP 在部分代码类任务上更有优势”目前主要是文献现象与导师机制直觉；
- “A12 E04 不能裁决 NTP/MTP”是本组已有直接结果；
- “哪种任务属性造成 MTP 优势”仍是开放问题。

### Mechanism guess / 机制猜想

我当前确认的机制判断是：

> MTP 是否可能优于 NTP，首先取决于任务本身是否包含一种需要提前形成、
> 持续运输并由标准头使用的状态。我们必须先把这种任务性质分解出来，再用不同
> 层次的模型逐项验证，而不能先构造一个 workload 后直接比较最终 accuracy。

我尚未确认的核心机制：

> `Unknown`：MTP 的候选优势究竟主要来自更短的 direct-credit path、较高的
> useful-gradient SNR、较少的梯度冲突，还是一种不同的表征选择偏置。

> **AI proposal—not yet the researcher’s judgment**
>
> 候选完整因果链是：
>
> ```text
> 早期证据对最终答案具有不可绕过的反事实作用
> -> 多个局部不足证据必须经 state relay 组合
> -> all-position NTP 只能通过 later/indirect path 训练较早状态
> -> informative-MTP 增加更早的 direct credit
> -> direct credit 形成任务必要状态
> -> 状态被运输到答案位置
> -> 标准 next-token 主头因果使用
> -> 在固定训练预算下体现为更快或更好的学习
> ```
>
> 其中任何一个箭头失败，都不能声称完整机制成立。

### Strongest rival explanation / 最强替代解释

我认为当前最强 rival 是：

> 观察到的 NTP/MTP 差异并不是提前监督造成的，而是 carrier 或 learner
> 不合格：NTP 可能因容量、优化难度或训练预算不足而停在 floor；任务也可能因
> answer/branch 泄漏、局部 shortcut、固定表记忆或消元规则而被错误地定义。

这个 rival 正是 A12 的主要教训：

- NTP 没有一个稳定学会两种 task depth 的 eligible scale；
- 删除双射表的一行后，缺失值仍可由“唯一未使用值”恢复；
- 因而结果只能说明 carrier/capability 失败，不能说明 MTP 相对 NTP 的机制。

> **AI proposal—not yet the researcher’s judgment**
>
> 仍需保留的第二 rival：即使 valid carrier 上 MTP 更快，收益也可能只是额外
> CE 项、梯度模长或一般正则化，而不是 future information。未来必须使用
> matched shared-aux 才能区分。

### Most uncertain point / 最不确定之处

我目前最不确定的是：

> 什么是最小但不失真的 long-horizon/compositional 任务属性？怎样同时保证：
> 早期证据和多步 relay 确实必要；任务不存在 bypass、记忆和消元；NTP 至少在
> 一个 scale 上可学习；matched baseline 又没有饱和，从而给目标差异留下
> 可判定的动态范围？

仍需我明确的选择：

1. 第一版最小任务是否必须是“两个证据 + 一个中间状态 + 一个最终答案”；
2. “long-horizon”是否必须包含较长 token distance，还是短序列中的
   relay-required composition 已足够先裁决机制；
3. 第一项要解释的 task property 是 credit-path length、multi-evidence
   necessity、state transport，还是它们的组合。

### Evidence that would change my mind / 改变判断的证据

我会更相信当前研究方向，如果看到：

> 一个 carrier 在目标比较前通过全部结构和 learner validity gates：local
> window 不足；改变早期证据会改变答案；多个证据必须组合；无直接 bypass；
> 无固定表记忆或消元；NTP 至少有一个稳定可学习尺度；matched shared-aux
> 有能力但未饱和；并且破坏 intended relay 会使标准头失败。

我会放弃或显著修改当前 carrier/机制，如果看到：

> local-only、single-evidence、固定表、消元或 generator shortcut 已能解决
> 任务；所有 NTP scale 都处于 capability floor；或 relay ablation 不影响
> 已经具备任务能力的标准头。

边界：

> 这些证据首先决定 carrier 是否有效，不直接决定 MTP 是否优于 NTP。一个
> carrier 失败只能否决该 operationalization，不能否决一般 MTP 假说。

### Current next decision / 当前唯一决策

研究者最新授权后，当前选择更新为：

> **先完成 carrier-validity 与 learner-capability 审计；只有通过后才比较
> NTP、matched shared-aux 和 informative-MTP。主问题拆为一个 parent anchor
> 和串行 subanchors，每个 subanchor 只证伪一个假设。实验以一层和两层小模型
> 为边界，任务定义保持固定；失败必须先分解原因并更新认识，不能靠不断增加任务
> 复杂度修补。**

研究者授权：

- [x] anchors、Protocols 和顺序实验不再逐项等待研究者审核，由 AI 按注册门槛
  自审并执行。
- [x] 仍保持串行 gate：carrier 不合格时不得读取 objective comparison。
- [x] 不因单次失败扩大 workload；只允许针对已定位瓶颈的最小修复。

### Frozen first carrier / 已冻结的第一个载体

第一版不直接声称“多证据组合”或“长 token 距离”，而只隔离最小的
**query-conditioned relay**：

```text
[BOS] [value-A] [value-B] [selector] [RELAY] [ANSWER] -> selected value
```

- `selector` 指定答案是 `value-A` 还是 `value-B`；
- `RELAY` 位置可读取两个值和 selector；
- relay-required 条件下，`ANSWER` 位置只能读取 `RELAY`，不能直接读取值或
  selector；
- 两层模型对应“第一层形成 relay state，第二层由标准头读取”；
- 一层 relay-required 模型是结构性 known-bad；
- 一层 bypass 模型允许答案直接读取证据，是 learner/interface known-good；
- held-out 组合、反事实替换和 relay-state patch 用来排除固定 pair 记忆与直接
  bypass。

这个载体只回答“提前监督在必须形成并使用中继状态时是否更有价值”。它不回答
真正的多证据联合计算、长 token 距离、代码迁移或 MoE。

## Optional Formalization

### Candidate parent hypothesis

> **AI proposal—not yet the researcher’s judgment**
>
> 对一个通过 validity gate 的 relay-required compositional workload，当
> all-position NTP 对必要早期状态的 later credit 在给定 learner 和训练预算下
> 受到衰减、噪声或冲突，而 informative-MTP 的新增 direct credit 与最终标准头
> 风险一致并能被运输时，MTP 将比 matched control 更有效地训练标准头所需状态。

这是一条条件命题，不是“MTP 普遍优于 NTP”。

### Candidate parent decision question

> **AI proposal—not yet the researcher’s judgment**
>
> 哪一组最小 workload 属性，使 informative-MTP 的提前监督相对
> all-position NTP 产生可归因、可运输、并被标准 next-token 主头使用的有限预算
> 优势？

### Candidate minimal variables

| 变量 | 暂定含义 | 当前状态 |
| --- | --- | --- |
| $E_0,E_1$ | 两个单独不足、联合必要的证据 | 待研究者定义 |
| $z_1$ | 必须从较早位置运输到答案位置的中间状态 | 待研究者定义 |
| $Y$ | 普通 next-token 主头预测的最终答案 | 待研究者定义 |
| $w$ | local-window 宽度 | 未冻结 |
| $J$ | later-credit path 的状态 Jacobian 乘积 | AI 候选机制变量 |
| $\Delta g_{\mathrm{info}}$ | informative-MTP 减 matched shared-aux 的信息特异梯度 | AI 候选机制变量 |
| $R_{\mathrm{std}}$ | 普通标准头在 carrier 答案上的风险 | AI 候选功能对象 |

### Candidate primary observable

当前尚不应冻结 NTP/MTP 性能差为主指标。

> **AI proposal—not yet the researcher’s judgment**
>
> 第一个 subproblem 的 primary observable 应是一个串行
> `carrier_validity` verdict：只有全部必要 gate 为 `pass` 才允许进入目标比较。
> 它只能证明 carrier 有资格，不能证明 MTP 机制。

### Pass / fail / insufficient for the first subproblem

- **Pass：**数据结构 gates、NTP capability、baseline dynamic range 和
  standard-head relay necessity 全部通过。
- **Fail：**任一结构性 shortcut、消元、NTP floor、baseline saturation 或
  relay non-use 被确认。
- **Insufficient：**oracle、counterfactual、learner capability 或 causal
  intervention 尚不能可靠判定。

## AI Audit Record

### Judgments to preserve / 必须保留的研究者判断

1. 先定义任务性质，再构造模型和验证假设。
2. 一个大问题必须拆成 parent hypothesis 和有依赖顺序的 subproblems。
3. 每次只关闭一个子问题，不能用最终分数替代机制判定。
4. A12 类 carrier/capability/shortcut 失败必须阻断 objective comparison。
5. NTP 学不会只有在排除 workload 与 learner 失败后，才可能与 MTP 机制有关。

### Unclear definitions / 尚未定义

1. `long-horizon` 的主定义是 token distance、credit distance，还是 state
   transition depth；
2. `compositional` 要求几个证据、何种不可分解性；
3. `relay` 是显式 token、隐藏状态、K/V channel，还是功能充分统计量；
4. “MTP 更好”的单位是 steps、tokens、FLOPs 还是最终风险；
5. 第一版 carrier 需要验证 short-range mechanism，还是直接承载 code-like
   semantics。

### Hidden assumptions / 隐含假设

1. future target 会监督最终任务需要的状态，而不是 nuisance；
2. direct credit 比 later credit 更干净或更强；
3. 形成的状态可以跨位置保存；
4. 标准头没有更便宜的 bypass；
5. valid minimal carrier 的机制会迁移到代码或规划。

### Strongest rival still alive

> carrier/learner invalidity，而不是 objective difference。

### Can the proposed metric separate the rivals?

当前不能。最终 accuracy 或 NTP/MTP gap 会把以下因素混在一起：

```text
task validity
+ learner capability
+ baseline saturation
+ auxiliary structure
+ future information
+ transport/use
```

所以必须先用串行 validity gate 分离前三项。

### Smallest falsifier

> 在不运行 MTP 的情况下，只要 local-only/single-evidence/bypass/elimination
> oracle 中任一个通过，或 NTP 没有 eligible scale，这个 carrier 就应立即
> 淘汰；不能继续解释目标差异。

## Candidate parent/sub-anchor dependency map

以下只是未来结构候选；本轮没有创建任何 anchor。

```text
Parent:
什么任务属性使 MTP 的提前监督形成标准头可用的有限预算优势？

S1. workload definition and carrier validity
    任务是否真的 local-insufficient、counterfactually dependent、
    multi-evidence necessary、无 shortcut？
    失败 -> 重做 carrier；禁止目标比较。

S2. learner capability and dynamic range
    NTP 是否至少有一个可学习尺度？matched shared-aux 是否未饱和？
    失败 -> 只说明 learner/选点无效。

S3. direct-versus-later credit model
    informative target 是否增加任务一致的 direct credit？
    NTP later path 是否真的衰减、噪声更高或冲突更强？

S4. formation, transport, and standard-head use
    新增状态是否形成、跨位置保存，并被普通 q1 因果使用？
    formation pass + use fail -> 只保留形成结论。

S5. objective-by-task-property interaction
    在 S1–S4 通过后，MTP 优势是否随预先定义的 task property 增强？
    这是第一次允许正式比较 NTP/MTP。

S6. code-versus-natural-language transfer
    代码优势是否由上述属性而不是模态、tokenization 或数据重复解释？

Parked bridge:
标准头有用状态是否预测 held-out expert utility，从而连接 A06/MoE Router？
```

## Candidate modeling ladder

> **AI proposal—not yet the researcher’s judgment**

1. **Level 0 — causal task model：**只定义 $E_0,E_1,z_1,Y$ 和反事实关系；
   先证明无 local/bypass/elimination solution。
2. **Level 1 — linear state/credit model：**分析 direct credit、Jacobian
   product、SNR 和 gradient conflict；给出正例、等价反例和负例。
3. **Level 2 — minimal neural carrier：**只在 Level 0–1 通过后，验证
   learner capability、transport 与 standard-head use。
4. **Level 3 — matched workload family：**连续改变一个 task property，
   检查 objective-by-property interaction。
5. **Level 4 — code/text transfer：**匹配长度、频率、tokenization、预算和
   local predictability 后，再谈代码相对自然文本。
6. **Level 5 — MoE bridge：**只有状态能预测 expert utility 时才进入 Router。

## Researcher Revision Checklist

请研究者优先修改以下五处：

1. 把 Phenomenon 改成你真正愿意在组会上承担的一个句子；
2. 选择 long-horizon 的主定义；
3. 选择第一版最小 carrier 的 $E_0,E_1,z_1,Y$；
4. 判断“carrier invalidity”是否确实是最强 rival；
5. 批准或改写唯一下一决策。

签名/时间：`____________________________`

## Boundary

本卡现已授权创建 parent/subanchors、Protocol、实现和顺序实验，并在证据改变
判断时更新项目本地 anchor、story，以及当天的
`daily_research_reports/MMDD/focus.md`。

仍不自动授权：

- 修改 graph 或 root sync；
- external collaborator sync；
- commit 或 push。
