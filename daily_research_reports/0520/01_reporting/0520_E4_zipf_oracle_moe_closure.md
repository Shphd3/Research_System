# 0520 Closure Brief: E4 Zipf Raw-Attention Oracle-MoE

## 1. Core Purpose And Hypothesis

目的：检查 uniform 中最强的 C7 oracle-init router 在 Zipf 长尾 feature frequency 下是否仍稳定。

假设：如果 C7 是可靠 routing reference，它不应只在均匀频率下有效；在 `10000/5000/500/100` 的长尾数据中也应保持 readback、feature assignment、selected-best expert。

## 2. Closure Decision

Zipf 下 C7d/C7e 仍是最强候选；C7e 可以继续作为 synthetic routing reference，但还需要低频 per-feature 稳定性分析。

## 3. Key Evidence

- C7e: `readback=0.997`、`feature-expert NMI=0.822`、`router_selects_best=0.993`。
- C7d: `readback=0.994`、`feature-expert NMI=0.819`、`router_selects_best=0.990`。
- C7a random prototype: `NMI=0.001`，说明 oracle initialization 是关键，而不是 prototype 形式本身。

## 4. Claim Boundary

可以说：在 controlled Zipf synthetic setting 中，C7d/C7e 仍能保持较强 feature-aligned functional routing。

不能说：低频 feature 已完全稳定；也不能说 boundary 是纯 feature direction 或真实语言可用。

## 5. Next Decision

先做 per-feature / per-seed 稳定性，尤其看最低频 JKL；再决定是否做 Reverse Index smoke。

## 6. 30s Explanation

我们把 uniform 里最强的 C7 router 放到长尾频率下验证。结果是 C7d/C7e 仍明显最好，C7e 的 `readback=0.997`、`NMI=0.822`、`selected-best=0.993`，而随机 prototype C7a 几乎不分 feature。这说明 oracle-init 不是 uniform 偶然现象；但最低频 feature 是否跨 seed 稳定还没完全说清，下一步要专门查低频稳定性。
