# Meeting Brief: Expert-Spectrum Initialization And Early Route Concentration

## **Question**

这次汇报回答一个问题：

上次组会提到的“根据每个 expert 初始化后的主输入方向，并先处理所有 token 共有方向，再做分发”的想法，能否变成一个有效的路由器初始化方法？

**父问题：**  
真实文本中的 top-1 稀疏 MoE 为什么会在训练早期把大量 token 分到少数 experts 上？

**当前子问题：**  
**之前实验发现，即使去掉高频 token 的影响，普通高斯初始化的线性路由器在第 0 步已经有负载偏置，并且训练到第 10 步会明显集中。**

这次我们测试：  
1. 直接用 expert 初始化后的主输入方向初始化路由器；  
2. 先去掉 token 共有方向后，再用 expert 主输入方向初始化；  
3. 只根据初始隐藏表征空间初始化。  

我们想判断：这些初始化是否能减少第 0 步偏置，并进一步阻止第 10 步的路由集中。

这里的“主输入方向”指：每个 expert 初始化参数中，对输入最敏感的几个方向，用大奇异值对应的输入方向估计。  
这里的“共同方向”指：一批 token 进入路由器前，隐藏表征中大家共有的主要方向。

---

## **Conclusion**

> 一句话总结：  
> 我们把上次组会提出的初始化想法做成了几个可计算版本；结果显示，这种router - 专家对齐的初始化能改善第 0 步的分布，但不能阻止第 10 步训练放大。尽管初始化的时候避免了Router对齐Common方向形成负载集中，但是训练中图Router还是存在Router越来越对齐Common方向。

1. **初始化可行性：expert 初始化后的主输入方向存在差异，并且和表征空间共同方向不同。因此能够使得step 0 的负载集中现象减缓**  
   我们用每个 expert 的输入矩阵估计主输入方向。不同 experts 的主子空间平均重合约 `0.0116`，说明随机初始化后的 experts 在参数方向上确实有差异。它们与隐藏表征共同方向的平均重合约 `0.0166`，说明这些方向不是简单等同于共同方向。  
   
   这说明：上次组会提出的“按 expert 初始化方向来分发”的想法有计算基础，值得测试。  
   但这还不能说明：expert 在初始化时已经形成了有任务意义的分工。

2. **方法层面：去掉共同方向后的初始化能改善第 0 步，但不能改善第 10 步。**  
   去掉共同方向后的初始化，确实让第 0 步 token 分布更接近均匀。去掉前 1% 高频 token 后，普通随机初始化的第 0 步最大 expert 负载是 `19.98%`，去共同方向版本是 `13.97%`。  
   
   但是训练 10 步后，去共同方向版本的最大 expert 负载达到 `93.51%`，比随机初始化的 `83.16%` 更严重。  
   
   这说明：当前线性路由器初始化只修正了起点的一部分偏置，但没有阻止训练早期把 token 重新集中到少数 experts。

3. **机制层面：第 10 步集中不能只靠初始化解释，而要看路由器和隐藏表征在训练中的共同变化。**  
   Anchor2 的训练过程审核显示：第 10 步集中不是单纯因为路由器权重自己变了，也不是单纯因为隐藏表征自己漂移，而是二者共同变化后放大了共同方向优势。  
   
   例如第 5 层中，只替换路由器权重的贡献是 `-0.0137`，只替换输入隐藏表征的贡献是 `0.4858`，二者共同变化产生的额外贡献是 `0.8038`。  
   
   因此，这次初始化实验失败的主要解释不是“expert 主输入方向完全没有用”，而是：当前线性初始化版本不足以控制训练前 10 步的放大过程。
---

## **Key Evidence**

1. **expert 主子空间差异是可测的。**  
   不同 experts 的主子空间平均重合约 `0.0116`，说明它们在初始化后不是同一组方向。

2. **expert 主子空间不是 hidden state 的共同方向本身。**  
   expert 主子空间与共同方向子空间的平均重合约 `0.0166`。这说明 raw spectrum 失败不是因为 expert 主子空间本身直接就是共同方向。

3. **expert 主子空间与强制路由效用有弱相关。**  
   raw spectrum 版本的残差谱分数与强制路由效用相关约 `0.2328`，高于 random 的 `0.0952`；top-1 效用匹配约 `0.3889`，高于 random 的 `0.2222`。

4. **当前实现桥很弱。**  
   residual-spectrum oracle 分配很均匀，max load 约 `0.144`，有效 experts 约 `7.96`；但压成线性 router 后，oracle-to-linear agreement 只有约 `0.20--0.25`。这说明子空间投影分数很难直接由当前线性 top-1 router 表达。

5. **common-filtered 初始化改善第 0 步，但第 10 步失败。**  
   去掉前 1% 高频 token 后，late layers 第 0 步 rank-1 expert 负载：random `19.98%`，common-filtered `13.97%`。  
   第 10 步 rank-1 expert 负载：random `83.16%`，common-filtered `93.51%`。

6. **完整训练指标不支持方法结论。**  
   late layers 平均：random 的 step-10 max load 为 `0.8344`，common-filtered 为 `0.9374`；random 的 effective experts 为 `1.5636`，common-filtered 为 `1.2177`。common-filtered 降低了一部分耦合项，但没有降低最终集中。

7. **Anchor2 显示第 10 步集中不是单一因素造成。**  
   第 5 层 cross-checkpoint replay 中，gate-only 贡献为 `-0.0137`，hidden-only 贡献为 `0.4858`，interaction 为 `0.8038`。这说明只看 router 更新或只看 hidden state 漂移都不够，二者共同变化后的相互作用很重要。

---

## **Detailed Setup**

**数据 / 任务：**

- DCLM 打包文本。
- 下一 token 预测。
- 使用固定批次做初始化统计和路由审计。

**模型：**

- 随机初始化 Qwen-style MoE。
- 6 层，8 experts，hidden size 512。
- top-1 路由。
- 训练 0--300 步，3 个随机种子。

**训练变量：**

这次训练比较主要只改变 router 初始化方式。模型结构、数据、训练步数、top-1 路由和损失设置保持一致。

**expert 主输入方向的估计方式：**

对每个 expert，我们用它 FFN 里的 `gate_proj` 和 `up_proj` 两个输入矩阵构造输入侧能量矩阵：

$$
G_e = W_{gate,e}^{\top}W_{gate,e} + W_{up,e}^{\top}W_{up,e}.
$$

然后取 $G_e$ 最大特征值对应的前几个方向，作为这个 expert 初始化后最主要的输入子空间。这对应之前组会里说的“大奇异值方向”。

需要注意：当前最小 MoE 实现中仍包含 shared expert 路径。因此 router 指标对 top-1 gate 是精确的，但 hidden state 训练动力学包含 shared expert 的影响。

**初始化版本：**

- random init：普通随机 router 初始化。
- common-orthogonal random：随机 router，但去掉共同方向投影。
- representation residual：只根据初始隐藏状态的 residual 几何初始化。
- raw spectrum：直接用 expert 主输入方向初始化。
- common-filtered spectrum：先去共同方向，再用 expert 主输入方向初始化。
- hybrid spectrum-to-linear：先用 expert 子空间匹配做 oracle 分配，再压成线性 router。

---

## **Current Interpretation**

之前组会提到的方法可以这样理解：

> expert 初始化后不是完全一样的，所以 router 初始化不应完全随机；它应考虑 expert 参数中的主输入方向。

这里有两个版本：

1. 初始版：直接用各 expert 的大奇异值主方向和 token 表征做匹配，再决定分发。
2. 修正版：先把所有 token 共享的共同方向去掉，再用剩余方向和 expert 主子空间做匹配。

这次实现的是修正版中的“去共同方向”版本；我们没有显式加入一个 common expert，而是先估计共同方向子空间，再把相关投影从初始化计算中去掉。

我们的实验把这个方法推进了一步：

> 这个方法在计算上可以定义，而且 expert 主子空间差异与强制路由效用有弱相关；但直接落到当前线性 top-1 router 上，还不能形成成功方法。

关键解释是：

1. **第 0 步改善有证据支持。** common-filtered 初始化减少了初始负载偏置。
2. **第 10 步失败也有证据支持。** 训练很快把 token 重新集中到少数 experts。
3. **所以瓶颈不只是初始化分布。** 早期 hidden state 变化、router 与共同方向的对齐、以及二者共同变化后的相互作用仍然存在。

因此，这次结果不是“之前组会提到的方法不成立”，而是：

```text
这个方法的线性实现还不够。
更大的问题是训练前 10 步会把初始偏置继续放大。
```

---

## **Boundary**

**现在可以说：**

1. expert 主子空间之间存在可测差异，与 hidden state 共同方向重合低，并且与强制路由效用有弱相关。
2. common-filtered 初始化能改善第 0 步负载分布。
3. 当前线性 top-1 router 初始化不能阻止第 10 步早期集中。
4. 仅仅让第 0 步更均匀，不等于解决 early route concentration。
5. 高频 token 不是第 0 步初始化差异的主要解释。

**现在不能说：**

1. 专家谱没有用。
2. 之前组会提到的方法不成立。
3. oracle router、二次 router 或 learned classifier router 也会失败。
4. 结果能推广到预训练大模型、top-2/top-4 MoE 或带负载均衡损失的训练。
5. 我们已经解释了最终 expert specialization。

---

## **Next Step**

不建议继续只扩大当前线性初始化实验。

下一步应先回答一个主问题，再保留一个分支问题。

### **1. 主问题：训练放大从哪里来？**

结合早期训练监测，继续审计第 0 步的 route winner 是否在前 10 步被 hidden state 变化和 router 更新共同放大。

如果第 0 步更均匀但第 10 步仍集中，说明下一轮方法不能只修 router 初始化，还需要干预早期训练放大路径。

### **2. 分支问题：专家谱匹配是否需要更强实现？**

测试 residual-spectrum oracle router 或更强的 learned classifier bridge，判断 expert 子空间匹配本身是否能减少前 10 步集中。

如果 oracle 有效、linear 无效，说明失败主要来自线性实现桥；如果 oracle 也无效，则应暂停当前 expert-spectrum routing 方向。
