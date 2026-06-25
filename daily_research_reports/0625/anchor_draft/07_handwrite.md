# Thinking Card Handwrite Draft

This is rough user thinking for AI audit. It is not a final anchor, protocol,
or experiment plan. Fill only the Thinking Card. Do not hand-write the full
0-8 anchor here.

## User Control

**Preserve:**

**Do not silently change:**

**Unclear / risky:**

**Candidate priors:**

## 0. Thinking Card

**Phenomenon:**

长尾信息被学到了common信息的方向，common信息如果与长尾信息有方向冲突，那么长尾信息会被common给冲淡。我们想要的是，moe能够将rare冲突项与common方向分开来学，从而能够提高学习的相关效率！

**Mechanism guess:**

根据导师的草稿，应该是A-AB-ABC这种nested的结构导致的学习问题。

1. 由于语义的嵌套结构，长尾信息受到干扰被学到了
2. common信息会在hidden state中形成一个方向偏置

**Key variables:**

通过梯度进行的建模。

**Causal relation:**

这些变量之间的方向关系是什么？

**Observable metric:**

哪个数能看到这个关系？

**Alternative explanation:**

还有什么 rival explanation？

**Decision:**

看到什么结果后，我会 pursue / revise / park？
