# P_rel_v2：模型盲态语义审核

审核人：Codex；2026-09-20。研究者本轮明确委托 AI 自行严格判定。此审核**不是独立人工标注**，也不是任何模型的成绩。输入为 [v1 的 64 个正反例](/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/review/p_precheck_v1/p_template_review_cn.md) 和 [修改后的 64 个正反例](/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/review/p_v2_precheck_v1/p_template_review_cn.md)。审查时未读取本轮任一模型输出。

## 标签规则与判定

固定参考顺序为 `box 0236; box 0376`。方向 0 逐一表示“0236 相对 0376：左于、上于、先于、在其内部”；方向 1 表示相反。每个模板的两个方向须各自表达该关系，不允许靠编号大小或正文主语猜标签。

v1 有三个不放行点：`containment.t3` 的 *surrounding* 可能只表示环绕而未必完全包含；`sequence.t6/t7` 的 *has ... earlier/later in the sequence* 虽可猜测意图，但语法别扭，给模板泛化添了不必要的句法异常。三项在任何模型读出之前修为 `The box that fully contains {A} is {B}.`、`In the sequence, {A} appears earlier than {B}.`、`In the sequence, {B} appears later than {A}.`，并命名 **P_rel_v2**。其余模板不变。

下面每行是两个逐例判定，`0/1=正确`意为两条各自通过，不是只给整组打分。

| 家族 | 模板 | 方向0 | 方向1 | 审核理由 |
|---|---|---|---|---|
| 左右 | horizontal.t0 | 正确 | 正确 | `left of` 的主宾明确 |
| 左右 | horizontal.t1 | 正确 | 正确 | `right of` 与左于互逆 |
| 左右 | horizontal.t2 | 正确 | 正确 | 前置地点短语明确左者 |
| 左右 | horizontal.t3 | 正确 | 正确 | 前置地点短语明确右者 |
| 左右 | horizontal.t4 | 正确 | 正确 | 关系句明确 B 左方是 A |
| 左右 | horizontal.t5 | 正确 | 正确 | 关系句明确 A 右方是 B |
| 左右 | horizontal.t6 | 正确 | 正确 | `has ... on its left` 绑定明确 |
| 左右 | horizontal.t7 | 正确 | 正确 | `has ... on its right` 绑定明确 |
| 上下 | vertical.t0 | 正确 | 正确 | `above` 主宾明确 |
| 上下 | vertical.t1 | 正确 | 正确 | `below` 与上于互逆 |
| 上下 | vertical.t2 | 正确 | 正确 | 前置 `Above B` 明确上者 |
| 上下 | vertical.t3 | 正确 | 正确 | 前置 `Below A` 明确下者 |
| 上下 | vertical.t4 | 正确 | 正确 | `higher than` 主宾明确 |
| 上下 | vertical.t5 | 正确 | 正确 | `lower than` 主宾明确 |
| 上下 | vertical.t6 | 正确 | 正确 | `above it` 指向句中 B |
| 上下 | vertical.t7 | 正确 | 正确 | `below it` 指向句中 A |
| 先后 | sequence.t0 | 正确 | 正确 | `comes before` 主宾明确 |
| 先后 | sequence.t1 | 正确 | 正确 | `comes after` 与先于互逆 |
| 先后 | sequence.t2 | 正确 | 正确 | 前置 `Before B` 明确先者 |
| 先后 | sequence.t3 | 正确 | 正确 | 前置 `After A` 明确后者 |
| 先后 | sequence.t4 | 正确 | 正确 | `precedes` 主宾明确 |
| 先后 | sequence.t5 | 正确 | 正确 | `follows` 主宾明确 |
| 先后 | sequence.t6 | 正确 | 正确 | 新版 `earlier than` 明确先者 |
| 先后 | sequence.t7 | 正确 | 正确 | 新版 `later than` 明确后者 |
| 包含 | containment.t0 | 正确 | 正确 | `inside` 明确内部关系 |
| 包含 | containment.t1 | 正确 | 正确 | `contains` 明确容器 |
| 包含 | containment.t2 | 正确 | 正确 | 前置 `Inside B` 明确内部者 |
| 包含 | containment.t3 | 正确 | 正确 | 新版 `fully contains` 排除仅邻近环绕 |
| 包含 | containment.t4 | 正确 | 正确 | `contained within` 明确内部关系 |
| 包含 | containment.t5 | 正确 | 正确 | `has ... inside it` 指向句中 B |
| 包含 | containment.t6 | 正确 | 正确 | `encloses` 表示封闭包围；在“两个盒子”的受控语境中指向内部关系 |
| 包含 | containment.t7 | 正确 | 正确 | `enclosed by` 与 t6 互逆 |

**结论：**新版 64/64 标准例子的方向标签在受控“两盒子”语境下语义可判，旧版 3 个模板不放行。`encloses` 在此处按“完整包围”理解；若后续自然语境或独立标注者认为它只表示外周环绕，应另立敏感性版本，不事后更改确认标签。生成器的正反对词袋不变量和实际 Qwen3 分词检查通过：12,800 句、6,400 对、每句 33–39 词元；正反对在词元多重集、长度、末词元上均无不匹配。该检查没有证明受控格式等于自然关系理解，也不证明不存在位置或句式捷径。

审核及生成过程只改变 P 的模板，不改变 N8 或 PAWS。P_rel_v2 的生成代码和未冻结数据位于 `/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/`；P_rel_v1 候选保留不覆写。下一步仍须完成来源组、正文掩码、数据分割和 fit/dev/test 隔离的执行清单，才能标记整套面板冻结。
