# feature

# 共识假设\&目标

**目标****：****找到深层和浅层之间有差别的信息来指导分发**

**假设1****：****模型深层在浅层基础上学到新信息**

**假设2****：****表征是低秩的**

## zx

**分析方法**：找到一组公共基来分析不同层feature的方差分布是否位于不同方向，更深层的方差是不是更位于靠后的方向

**公共基的定义方式**：

1. 最后一层表征的谱空间（intuition：最后一层的表征包含浅层到深层的所有信息）

2. 词表头的输入空间（intuition：词表头编码了表征将会被如何影响模型输出）

3. 不同层的表征拼在一起做 SVD（intuition：这是数学上各个层表征可以共享的基）

**实验结果**：三种定义方式下都没有观察到我们期待的方差后移现象，并且残差表征在所有方向上的方差都大于包含新信息的attention输出表征的方差

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NmE2NjIyM2IyMzljNjcyZGMyMjQ1YzBkYmRmZDI0MmJfMjA3N2UzNWQ0Y2EwMTc4MGI1NWY4MTYxYTY1OGU2NTdfSUQ6NzY3Mjk4MjM5NDAzODgzMjExNl8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDkxMjdkNTFhZjM2ODVkZmM2YzUyZjE4NDM4ZjQ0NzZfNmM1ZmZiMjRjY2MzNDVjZjY3ODk4ZTIyYjVkYjhlNWVfSUQ6NzY3Mjk4MjM5MjAwOTE4MjQ0NF8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YmQ0MmM3OWIyZTNmYjI3M2ExMWMxM2ExNDg0ZDRlOWRfMmI4Yzg1OWYwM2FkNjlkZWMyYTI3NzE1MjgyYzVkOGNfSUQ6NzY3Mjk4MjM5MzMwOTIwMzc1Nl8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTc5MTM1MWRmZWViMTQxZTM4ZTMzOWY5NWRlZjVhNzhfY2Q1OTc2ZTQ4YmQ2MGQ3MzJlNjc5ZmU1NGY1NTcyYzhfSUQ6NzY3Mjk4MjM5MDI3MzIzMTgxNF8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

**原因分析**：目标没问题，我们也尝试了各种公共基的定义方式都没看到期望的结果。我现在怀疑原因是我们的分析方法有局限性，我们的分析方法里其实局限了两个条件：需要用不同层表征之间的比较来定位新信息、比较的方式是用一组共享正交基。但是也许有可能这两个条件都是不必要、甚至错误的。

- 比如说要用一组共享正交基来比较不同层的表征，我认为是错误的，原因是组合信息，或者说feature的总量肯定是远远大于表征维度的，所以一个正交基不可能只代表一种组合信息。那么对于任意一组正交基，它的每一个方向，不同层的表征在这个方向上可能编码的是不同的信息，因此即使方差一样，也不能说明这个方向编码的是全局的浅层语义。

- 再说是否真的需要在不同层的表征之间来比较？我认为也是不必要的，因为深层表征包含了浅层语义，所以我们只需要在每一层的表征上面构造出层级结构，然后我们去掉叶子节点，这样非叶子节点就是本层新产生的高级组合语义

## Hrj

**分析方法： **定义一种跨层比较方式，找到浅层和深层中表示相同信息的子空间，再分析深层表征在这些共同信息子空间之外的分量的语义信息。

**结论：没有观察到新信息空间在不同方法和不同表征上稳定具有更强的domain区分性。**

**浅层表征 \(X\)：** 第 \(n\) 层的 attention输出表征。**深层表征 \(Y\)：** 第 \(n\+1\) 层的 attention输出表征。

例如，如果数学 token 在浅层的某个方向上取值较大，在深层的另一个方向上也取值较大，那么这种对应关系所在的子空间就应当是旧信息所在的子空间，而新信息落在无法找到这种关系的子空间中。

数学上，通过求解下面的优化问题寻找成对方向 $u_i$ 和 $v_i$： $\arg\max_{u,v}
\operatorname{Corr}(Xu,Yv).$

- 浅层共同信息子空间：$\mathcal S_X=\operatorname{span}(u_1,\ldots,u_r)$；

- 深层共同信息子空间：$\mathcal S_Y=\operatorname{span}(v_1,\ldots,v_r)$。

然后使用浅层共同信息的投影值重构深层表征：

$\widehat Y=XU B+\mu_Y.$

其中，$\widehat Y$ 是浅层共同信息能够解释的深层部分。深层中不能被这些共同信息解释的部分为：

$R_Y=Y-\widehat Y.$

因此，我们暂时认为新的信息可能位于 $R_Y$ 中。这里不认为 $R_Y$ 全部都是新信息，只把它作为候选区域。

最后对 $R_Y$ 做PCA，取方差最大的若干方向作为新信息空间，并与以下空间进行同维比较：

- **旧信息空间：** 深层共同信息子空间 $\mathcal S_Y$；

- **新信息补空间：** 去掉新信息分量后，深层剩余表征中方差最大的方向；

- **Random：** 随机选择的同维方向。Í

### 实验结果1：相邻层MLP输入表征

这里的 $X$ 和 $Y$ 分别是相邻两层的MLP输入表征。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NzJhZTAxM2JiZTljMTBjM2I0ZTFiZDRmYzlhYjNmZTRfOGQ4N2QwMmEyNWRjODMzMGUzNjAwNGFiMTExMGJhNWRfSUQ6NzY3MzAxMDE1MzMyNzQxNDQ1M18xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)



**结论：** Candidate明显高于random和shared old，并与backbone接近。说明相邻层MLP表征中，浅层共同信息解释不了的部分包含非随机的domain信息，并且更接近跨层发生替换的turnover feature。

### 实验结果2：相邻层Attention输出表征

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDQ0MjUyOGI0MWI0ODU0ODBkYmYxNjk5ODQ0YzU0YTZfODYyY2RlOWY0NWU4ZDVmMTg5NGU4MTQ0YTkwOTNlNTJfSUQ6NzY3MzAxMDIxNDYzMDkxOTE1MV8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

这里的 $X$ 和 $Y$ 分别是相邻两层的raw attention output。

**结论：** Candidate与random基本相同，并明显低于shared old和backbone。说明在相邻层attention输出中，不能由浅层共同信息解释的部分没有表现出更强的domain信息。

### 实验结果3：同层Residual与Attention输出

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjQxNzQ2NzA2YjAyNjRjOTU1OGVkMWY3YWViODk1YjlfNzkwMTY4YWIwMmQzNDgxMGRjMTMyMjkwODRiMzBmNThfSUQ6NzY3MzAxMDI1NDI0NjM1MDAxMl8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

这里的 $X$ 是进入本层attention前的residual，$Y$ 是本层raw attention output。

**结论：** Residual与attention之间确实存在高度相关的共同信息，但这些共同信息只能解释attention总变化的约17%–30%。剩余candidate略高于random，但明显低于shared old和backbone，因此没有证据说明attention中无法由residual解释的部分具有更强的domain信息。

## car

**分析目标**

我们希望区分：第 $n$ 层 Attention 输出中的哪些信息可以由该层输入预测，哪些变化可能是 Attention 新引入的。

**输入表征**

$X$：模型第 $n$ 层的输入表征；

$Y$：模型第 $n$ 层 Attention 模块的输出，不加 residual。

**寻找公共坐标**

由于 $X$ 和 $Y$ 位于不同的表征空间中，我们不能直接比较它们的对应维度。

CCA 分别在两个空间中寻找一组相互对应的投影方向：

$z_x=(X-\mu_x)A_x\\\\z_y=(Y-\mu_y)A_y$

使同一个 token 在对应坐标上的 $z_x$ 与 $z_y$ 尽可能同步变化，相关性高的坐标认为是可靠的公共坐标。



**我们从 Attention 输出中识别两类坐标：**

1. 公共坐标：$z_x$ 与 $z_y$ 相关性较高；

2. Attention\-private 候选坐标：与 $X$ 的相关性较低，但在 Attention 输出中具有较大能量。



**新信息可能出现在哪里**

1. $z_y$中无法被$z_x$表示的部分。

在每个公共坐标上，先根据输入预测 Attention 输出：

$z_{\mathrm{predictable}}=\beta\odot z_x$

再计算实际 Attention 输出与预测值之差：

$z_{\mathrm{update}} = z_y-\beta\odot z_x$

它表示 Attention 在已有公共坐标上额外产生的变化。

2. Attention\-private 坐标中表示的部分



![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODc4NmMxMjYwOTM5MjIzMzc0NDc4ZTEzMDNkYjY2YWRfNDJkMWFjNDg1NjYzMjFhYzM1ZTYzMGRkODk2ZjBkZWJfSUQ6NzY3Mjk4NTQwNDE4MjEwNTA1Nl8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

实验结果：

1. 公共坐标占整个表征空间的比例

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTZlMTcwYzc3ZTIzNGYxOTg1Mzc0MTFiMjA5NTJlNDBfZjUxZGZhYzlhZTgzNjU5MmQ1NmQ3NzQxODkwYWQwMTdfSUQ6NzY3MzAwMDYyMTE1ODY5ODE2NV8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

2. 定义的“新信息”没表现出比“旧信息”更高的domain区分性

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Mzg4ZmFkMmU4ZGRlNjBmMWFiNGMxYzE0YzlhOTg4MTRfNjE0Y2U2ZWM3ZjNjNTYyM2Q5OTQ4NTIyN2E4NWYzODhfSUQ6NzY3MzAwMjc1MzM3NTE2MTU1NF8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)



## dxy

**分析方法：**

我们的目的是，找到与参数矩阵相关的不同层的一组公共基，然后再把这组公共基上新信息所在的方向投射回每层的参数矩阵中

**公共基选取：**

我们选择了一个最直观的公共坐标。具体地，将不同层MLP参数矩阵的$G_l = W_{g,l}^{\top}W_{g,l} + W_{u,l}^{\top}W_{u,l}$ 进行一个跨层聚合：$\bar G = \frac1L\sum_l \tilde G_l$, 其中$\tilde G_l=\frac{G_l}{\operatorname{tr}(G_l)}$是每一层矩阵的尺度归一化矩阵。这样得到的方向可以理解为：从整个模型MLP平均参数矩阵来看，哪些方向参数响应更强哪些更弱，包含了所有层参数矩阵的信息。缺点是不同参数矩阵的信息可能会发生冲突，相加后会发生方向相消。

**方向分析思路是：**

1. 先把第 L\+1层和第 L 层的 Attention 输出分别投影到完全相同的公共方向上；然后分别统计每个方向上的跨样本方差；最后把每层方差谱归一化，再比较第 L\+1层减第 L层。 

2. 再通过公共的方向与各层方向的关系，来看新增信息都落在每一层参数矩阵的哪些方向上。

**目前为止的结论是：**

1. 在平均矩阵共同基上，谱能量后移，但是不是逐层趋势。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MmM2Y2I2ZDAwZTc1OTBjMzFjM2VlMzFmNjYyODQzYmNfYzU4YmZmOGY2MTNkNGQzY2ExOTM3NTc0NDJmOGJmZjJfSUQ6NzY3Mjk5MDcyNjg1ODgyMDU3MF8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

2. 平均矩阵公共基下，语义越细，Attention 输出的方差分布统计上越偏后，因此谱位置确实包含一定的语义粒度信息。如下图所示，在谱的中带，更细粒度的信息相比粗粒度信息方差激活普遍更大（表现为在x=0上方）。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzBhZjQxZWZkMjhlOGViYmNjMzg2MWMxNjI5MjQxNjRfYmRiM2EzNDhiYjA0MGNmMWJkZjA0ZmNjMDE4OTk3NzRfSUQ6NzY3MzAxNjM3NzM2ODE2OTQ2MF8xNzg2NTg5OTUxOjE3ODY2NzYzNTFfVjM)

左图：纵轴表示两个语义层级的质心差；右图：纵轴表示预先固定的谱段（50%\-75%）中的归一化方差的占比差

C、M、F分别代表粗粒度、中间粒度和细粒度



