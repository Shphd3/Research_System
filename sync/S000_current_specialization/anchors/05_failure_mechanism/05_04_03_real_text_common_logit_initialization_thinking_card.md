# Thinking Card — 05_04_03 Real-Text Common-Logit Initialization Anchor

> Migrated from [05_04_03_real_text_common_logit_initialization_anchor.md](05_04_03_real_text_common_logit_initialization_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

父问题：为什么 sparse top-1 MoE router 在早期进入 route concentration / expert underuse？
当前子问题：DCLM real text 上，随机初始化线性 top-1 router 是否在 step 0 就被 common-logit offset 主导？
实验结论：step 0 的 common-logit dominance 被削弱；common component 不是最大 logit-margin 来源，但 centering 明显降低 max load。
关键转向：训练 10 步后 common 通道快速放大，route concentration 更像早期训练反馈问题，而不是纯随机初始化几何必然。
当前边界：只裁定该小型 Qwen-style top-1 MoE、DCLM packed text、随机初始化和 300-step 早期训练。
下一步决策：做 early-training causal split，分别冻结 gate、hidden-state producer 和 expert-output feedback。
