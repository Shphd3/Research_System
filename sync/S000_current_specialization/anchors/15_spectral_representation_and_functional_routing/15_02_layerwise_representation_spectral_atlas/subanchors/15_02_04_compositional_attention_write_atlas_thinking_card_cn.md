---
thinking_card_id: 15_02_04_compositional_attention_write_atlas
status: human_confirmed_for_execution
human_language: zh
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
documentation_authorized: true
focus_authorized: true
---

# Thinking Card：层级组合语义在 attention write 中的深度与频谱画像

> 本卡依据研究者 2026-08-06 的机制判断整理。研究者已确认主对象是每层 activation data covariance 谱而非参数谱，并确认唯一问题进入正式 Anchor；后续明确要求自行审核、完成全部实验、图与热力图、self-contained 报告和 0807 focus，并授权最多四个独立 8 卡 5090 节点，不再设置额外执行审批。

## 我的判断

- **具体现象：**现有冻结 Qwen3-8B 审计使用的是粗类—细类 taxonomy，而不是真正需要联合多个原子事实的组合语义。自然文本表征还混有模板、句法和共同上下文，原始类别间方差因此可能持续由背景 covariance 的 head 方向主导。当前尚未成对审计不含 residual 的 pre-`o_proj` attention 输出与 isolated post-`o_proj` attention write。
- **机制猜想：**更深层更倾向于形成需要联合更多证据才能确定的语义变量。如果这类条件性组合变量在自然语料中比句法、主题等共同因素更少变化，那么控制模板与共同上下文的加性主效应后，相比原子语义，一级和二级组合语义应在晚层更稳定可分，并在各层自身的 DCLM 背景 covariance 谱中把相对方差质量分配到更大的归一化 rank；其绝对主峰仍可留在 head，右移也可能只到 middle 而非 extreme tail。pre-`o_proj` 表示 attention 内已经形成的信号，post-`o_proj` 表示该信号经线性混合后写入 residual 坐标的几何。
- **最强替代解释（AI 补全）：**更深层只提高组合变量的总体可读性或放大全部谱带，并没有发生语义方差的相对 rank 重分配；表面“右移”也可能只是背景谱变平、总方差尺度不同、路径长度、答案词、token 数、证据位置、模板、实体词或 `o_proj` 线性重标度造成。真正组合还可能主要发生在 MLP。
- **最不确定的一环：**每层的谱方向都会重新定义，因此“跨层右移”能否被严格操作化为语义方差在本层归一化 rank 分布上的变化，而不是同一方向的迁移；同时，大/小组合层级的总类别间方差尺度不同，归一化定位结果只有在原始强度与可靠性门通过后才可解释。
- **什么证据会改变判断（AI 补全）：**若能力与可靠语义强度门通过后，二级相对原子语义的归一化谱秩重心在晚层没有增加，或右移不能跨 held-out world、template、relation-shuffle、同维随机子空间与独立 calibration-half 复现，则否定当前 attention-write 谱右移命题。若只看到区分度增强而没有 rank 右移，则保留“深层更可读”，否定“复杂语义向低背景方差方向重分配”。
- **当前唯一决策：**把上述定义写入正式 Anchor，并审核一套使用随机单-token 实体别名的平衡空间关系图：同一 world 上查询 1-edge、2-edge、4-edge 目标，只做冻结 Qwen3-8B 的 full pre-`o_proj` 与 isolated post-`o_proj` attention write static audit。暂不加入 SAE、完整 residual、MLP、Router 或训练。

## AI 审核

- **唯一未定义对象或隐藏假设：**“更复杂所以向 tail”不是逻辑推论；它额外假设复杂语义是自然分布中的低频、条件性变化，而且模型不会把它放大回高方差方向。跨层可比较对象只能是每层本地谱上的归一化 rank 分布、频带份额和语义/噪声比，不能是某个固定编号的 eigenvector。模板/world 中心化只移除加性主效应，不产生“纯语义”。
- **最小反例或区分实验：**同一关系 world 同时产生 1-edge、2-edge、4-edge 查询，保持事实、token 长度、位置和八类答案空间匹配。分别报告语义总强度、尺度归一化的谱秩分布和频带内语义/噪声比；只有总强度可靠时才解释谱份额。主反例是组合区分度晚层增强但归一化 rank 分布不变。
- **AI 建议：**pursue execution。正式 Anchor 冻结“相对 rank 重分配”而非“同一方向迁移”；Protocol 以完整七节点树、等样本主比较与全节点位置审计消除固定第一条边/左半树的混杂。

## 我的确认

- **保留或修改后的判断：**研究者确认主要看 activation data spectrum，而不是参数 spectrum；唯一研究问题已冻结。进一步把“向右移动”限定为语义方差质量在每层自身 covariance 谱上的归一化 rank 重分配，并要求显式分开大/小组合层级的总强度差异与谱位置差异。
- **是否允许写入正式 anchor：**yes。
- **是否批准 Protocol 与执行：**yes；包含两处 4096 维表征、完整实验、分析、图、self-contained 记录与 0807 focus；不包含 commit、push、graph 或 root sync。
