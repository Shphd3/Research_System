# 0520 Closure Brief: E4 Uniform Raw-Attention Oracle-MoE

## 1. Core Purpose And Hypothesis

目的：判断 raw-attention Oracle-MoE 是否能把 synthetic trigram feature 稳定分给不同 experts，并排除 prefix token / target token shortcut。

假设：如果 `attention_output` 中已有 feature-related regions，则 Dingyi-style oracle-initialized prototype router 应比普通 router 更稳定地形成 feature-aligned functional specialization。

## 2. Closure Decision

均匀分布下，C7e 是当前最强 routing reference；普通 C0-C6 不能稳定支持 one-feature-one-expert。zipf 长尾版本尚未闭环。

## 3. Key Evidence

- `crossed_factorial_uniform` 中，C7e 达到 `readback=1.000`、`feature-expert NMI=0.834`、`router_selects_best=1.000`。
- `shared_b_uniform` 与 `shared_target_uniform` 中，C7e 仍保持 NMI 约 0.9，说明不只是简单 prefix-end token 或 target token shortcut。
- D* audit 显示 C7e 仍有较高 top-shared boundary energy，因此不能说是纯 feature direction 切分。

## 4. Claim Boundary

可以说：在 controlled uniform synthetic setting 中，oracle-initialized C7e 可以构造接近 one-feature-one-expert 的功能性 routing reference。

不能说：自然 router 会自发发现 relation-level feature；也不能说真实语言或 zipf 长尾已经成立。

## 5. Next Decision

继续监督 zipf C0-C7e full run；若 C7e 在长尾下仍稳定，再考虑作为 Reverse Index 前的 routing reference。

## 6. 30s Explanation

我们这轮是在问：MoE router 能不能真的按 synthetic feature 分 expert，而不是靠 token 捷径。结果是，普通 router 不稳定；但 Dingyi-style oracle-init 的 C7e 在 shared-token、shared-target、crossed-factorial 控制下仍能 readback，并保持较高 feature-expert 对齐。最强证据是 crossed-factorial 里 `readback=1.000`、`NMI=0.834`、`selected-best=1.000`。边界是它不是自然发现机制，而且 boundary 仍混有 common directions；下一步看 zipf 长尾是否保持。
