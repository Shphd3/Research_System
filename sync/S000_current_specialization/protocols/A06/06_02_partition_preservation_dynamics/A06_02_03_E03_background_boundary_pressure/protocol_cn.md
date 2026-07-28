# Protocol（中文 companion）：A06_02_03_E03 Background Bias And Margin Budget

## 0. 审核快照

状态：用户已明确授权。英文 `protocol.md` 为 canonical。

目的：判断 margin crossing 是由 background 数量本身造成，还是需要 background gradient 对 route boundary 有非零均值投影。

设置：长度 32；signal count 为 32/16/8/4/2；冻结 hidden 和 experts；weighted top-1；router-only SGD 500 步；32 seeds。

条件：signal-only、boundary-orthogonal zero-mean、common-balanced、common-biased。

主指标：final margin p05 与 ever-cross rate。

通过：common-biased 出现可复现 crossing threshold，而相同 background ratio 的 zero-mean/balanced controls 不出现；预算精确闭合。

失败：background controls 与 biased 条件表现相同，或 signal-only 自己崩溃。

边界：不能证明真实 DCLM common operator、AdamW 动力学、hidden drift 或 common subtraction 方法。

## 1. 术语解释

- signal fraction：32 个位置中携带 feature target 的比例。
- common-biased background：共同 hidden direction 配合固定 target-0，产生非零均值更新。
- margin budget：初始 pairwise margin 加累计 signal/background margin increments。
- re-entry：margin 越界后重新变正。

## 2. 核心公式

$$
m_{f,a,b}(T)=m_{f,a,b}(0)
+\sum_t\Delta m^{signal}_{f,a,b}(t)
+\sum_t\Delta m^{background}_{f,a,b}(t).
$$

每一步分别反传 signal 与 background loss，并按全位置 loss 的占比加权；两者相加作为真实 SGD update。

## 3. 指标与判定

主指标同时使用 final margin p05 和 ever-cross rate，避免 common feature 的正收益掩盖其他 feature，也避免把 transient crossing 错当最终 collapse。辅助指标包括 crossing step、final matched route 和 budget closure error。

## 4. 不可声称内容

不能把这个受控 bias 直接等同于真实语言的 common component，也不能从该实验直接提出新 gating。

