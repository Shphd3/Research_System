# Daily Card - 0522

## 1. Today's Purpose

完成 H0522 `seq_len=32` router factor audit，判断 ordinary top-1 MoE 的 expert id 更受 rule/function 还是 shortcut factors 影响。

## 2. Mainline Anchor

主线问题：

```text
expert id 能不能作为 learned Reverse Index 的稳定 feature/function bucket？
```

## 3. Task Conclusions

### Task 1

Did:

完成 ACP 四卡 job `pt-xceqs84c`，跑完 Stage 1-5，四个 seed 全部完成。

Conclusion:

Stage 1/2 显示 source-position 和 token-id 对 router 的解释力强于 rule/class。

### Task 2

Did:

完成 factor-disentangled seq_len=32 synthetic task。

Conclusion:

模型 accuracy 为 1.0，但 rule_label 没有稳定胜过 identity；target/second-token shortcut 更强。

## 4. Mainline Update

H0522 更新主线：

```text
ordinary top-1 expert id 目前不能作为 clean rule/function Reverse Index。
```

更精确地说，当前 evidence 支持 position/token-id/target-shortcut modulated mixed routing。

## 5. What I Cannot Claim Yet

不能说 MoE routing 一般无效，也不能说真实语言模型中一定同样失败。

Stage 5 仍有 target/second-token shortcut，所以下一步必须做更严格的 anti-shortcut 构造。

## 6. Next Decision

设计下一版 anti-shortcut synthetic：

```text
balance identity x position x target;
test rule/function -> expert_id after shortcuts are controlled.
```

## 7. 30s Explanation

我们今天把 router 分发拆成几个可能因素看：token、位置、左上下文、rule/function、target。结果是，旧 seq_len=32 模型里位置和具体 token 更能解释 expert id；新解耦任务里模型能做对任务，但 router 更贴近 target/second-token shortcut，而不是稳定 rule/function。所以现在不能把 ordinary top-1 expert id 当作干净的检索索引，下一步要做去 shortcut 的 synthetic。

## 8. Recording / Class Notes

无。

## 9. Small Thought Parking Lot

暂无。
