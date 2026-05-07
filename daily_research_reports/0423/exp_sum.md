# Prompt

我需要你遵循以下原则，为我将整个研究串起来：

1. 首先，我们的最终目的是，做一个能够适应我们终极目标 “一学就会，永不遗忘”的Hierarchical MoE，因此，我需要你为我们的每一步骤定下基调。
2. 在我们的组会汇报中，我们只有 30s - 1min 的时间叙述我们的观点，所以我们必须要遵循一个汇报原则，大致按照以下语句组织成一个汇报的说辞：
    我汇报的主题是……
    本阶段更新，我的核心结论是……
    证据是……
    我现在的理解是……
    还不确定的是……
    下一步我想做……，
3. 然后我需要你按照学长的这个模版，整理最重要的实验和证据：

    ```text
        假设：每个数据表征包含的信息是高维空间中的低维信息
        结论：现有的基于svd奇异向量定义的feature看不到这种性质

        实验：训练一套sparse dictionary，约束每个数据表征使用的基数量，训练目标是表征重构
        结论：
        1. 在模型浅层和中间层，训出的sparse dictionary有比svd奇异向量好得多的重构效果；在深层这种差距在缩小
        2. 观察了sparse dictionary的数学性质（相比于svd奇异向量）：
        3. 每个sparse dictionary 里的向量被更少的数据激活【&SVD： SVD的基在不同数据间激活情况很离散： 所有数据都激活了很少的几个SVD基，剩下的SVD基基本没有数据用】
        4. 不同sparse dictionary向量之间不正交，平均的cosine similarity小于0.1，随着从模型浅层到深层相似度逐渐升高
    ```

    这是之前整理的版本，你可以参考一下其中的内容：

    ```text
    实验
    我们把 Qwen3-0.6B 的第 8 层 FFN block 替换成几种不同结构，在 DCLM + WoS 的混合数据上训练，然后比较主任务表现。
    最核心的几种结构是：
    1. baseline_ffn
        $$h_{\text{out}} = h_{\text{in}} + E(x)$$
    2. flat_moe_raw_uniform
        $$h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x)E_i(x)$$
    3. split_dense_tail_uniform
        $$h_{\text{out}} = h_{\text{in}} + E_c(x) + E_t(x_t)$$
    4. router_raw_expert_tail_uniform
        $$h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x)E_i(x_t)$$
    5. hier_moe_tail_uniform
        $$h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x_t)E_i(x_t)$$
    然后我们主要看了三类证据：
    第一类：真实 hidden 的几何证据
    我们先在 Qwen3-8B 上进行表征探查 + probe实验，真实 hidden 里确实存在一个 共享高方差 head。  
    去掉这个 head 以后得到的
    $$x_t = P_t(x-\mu)$$
    在 probe / purity / NMI 上都比 raw hidden 更可分。
    所以这一步说明：
    raw hidden 里确实混着一块 shared/common 成分，直接拿它做 tail learning 不太合理。
    第二类：真实单层 block replacement 的主结果
    在真实 Qwen3-0.6B 上，单层替换实验里：
    - baseline_ffn = 84.0007
    - flat_moe_raw_uniform = 85.0412
    - hier_moe_tail_uniform = 81.5287
    这里看的是 WoS rare-token PPL，越低越好。
    所以这一步说明：
    单层 tail-conditioned hierarchical block 确实已经优于 baseline 和 flat raw MoE。
    第三类：机制拆解
    我们把 hier 的收益拆开以后发现：
    - flat_moe_raw_uniform = 472.3493
    - router_tail_expert_raw_uniform = 471.7282
    - router_raw_expert_tail_uniform = 448.6350
    - hier_moe_tail_uniform = 447.1932
    所以最关键的模式是：
    $$\text{full hier} \approx \text{expert-only} \ll \text{router-only} \approx \text{flat}$$
    这说明当前最稳定的单因素增益来自：
    $$E_i(x) \rightarrow E_i(x_t)$$
    而不是：
    $$g_i(x) \rightarrow g_i(x_t)$$
    也就是：
    现在更重要的是“expert 看 tail residual”，而不是“router-only 看 tail residual”。
    第四类：功能性 specialization 证据
    我们没有再只看 purity / NMI，而是直接做了 token-level 的反事实比较：
    $$G_{\mathrm{cf}}(e') = \ell(e') - \ell(e^\star)$$
    如果这个量大于零，就说明当前被选中的 expert 比替代 expert 更适合当前 token。
    结果是：
    - hier 在 middle / rare token 上的 G(second) 都明显大于零
    - expert-tail 也明显大于零
    - flat 基本接近零，甚至略负
    所以这一步说明：
    当前单层 tail-conditioned block 已经出现了真正对 next-token prediction 有帮助的功能性 specialization。
    第五类：recursive 的瓶颈诊断
    对于recursive架构，我们的判断是基于一个toy model 来构建的。我们在 synthetic recursive setting 里比较了：
    - R5: learned coarse + learned fine
    - R5c: oracle coarse + learned fine
    - R5d: learned coarse + oracle fine
    - R6: oracle coarse + oracle fine
    结果是：
    - R5 = 8775.19
    - R5c = 2951.38
    - R5d = 9121.51
    - R6 = 1057.94
    最关键的关系是：
    $$R5c \ll R5,\qquad R5d \not< R5$$
    所以这一步说明：
    recursive 没起来的第一瓶颈在 coarse routing，而不是 fine-local routing。

    ```

---

然后还有以下任务需要仔细完成：

1. 然后我们要整理：
   - 写提纲，以“读者一秒钟就能明白”为目标写提纲，不写实验过程，但是写实验结论证明了什么。
   - 预判防守：提纲旁边Shang老师最可能问的两个问题，准备好引导式回答：“尚老师，正如我们之前讨论的【之前讨论的相关问题】，我这次顺着思路做了验证，发现【现象】” 预判防守一定要充分，这是我们自己的课题，我们自身一定要勇于担当，着手推进。
2. 请注意，上述所有内容，你给我的回复都要清晰，一定不要用一些难懂的英文短语来替代对于一个具体单词的解释。组织语言一定要符合正常人类的说话方式。
3. 同时你要按照：Hypothesis - mathematical modeling - empirical study - next iterations 的结构，也整理一个详细的文档，这个文档的结构请万万全全参照main (6).tex. 同样，要遵循上述写作原则。
4. 最后，请给我一个markdown文档，这个markdown文档是帮助我们继续推进的下一步计划。今晚我们会让Agent执行，持续推进我们的课题。