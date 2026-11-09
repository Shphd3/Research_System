# 三个实测例子与一个反例

例子在统计结束后为解释而选，不参与候选、方向或检验的选择。没有自动把feature命名为生物专家。

## 例1：CrossCoder共享z到最后层重构贡献

F09最后目标为 `the method`，完整目标IDs=[279,1714]，测末token1714（` method`），零起始位置30。先看同目标、不同前文：

- **M1**：Everyone listened quietly. The note was dated Monday. The proof established a statement for the first integer and then for each successive integer. The review evaluated the method
- **B1**：Everyone listened quietly. The note was dated Monday. The experiment marked a protein with a fluorescent dye and observed it inside living cells. The review evaluated the method
- **M2**：Everyone listened. The note was dated Monday. The mathematician used induction, beginning with one case and extending it to the next. The review evaluated the method
- **B2**：Everyone listened quietly. The note was dated Monday. The biologist attached a glowing label to a protein and followed it through a cell. The review evaluated the method

在固定生物偏向候选 **CC f12314** 上，先取得原14层输入的共享z。最后层decoder方向的归一化空间范数是 **1.48414743**，原TRAIN RMS27是 **374.34951210**，所以回到原空间的范数为 **555.58986611**。该位置的贡献向量是z乘最后层原空间decoder方向，其长度才是下表的“重构贡献幅度”。

| 版本 | 原共享z | 最后层原空间贡献幅度 | 除发现RMS后的量 |
|---|---:|---:|---:|
| 数学措辞1 | 0 | 0 | 0 |
| 生物措辞1 | 0.03484364 | 19.35877 | 3.53007 |
| 数学措辞2 | 0 | 0 | 0 |
| 生物措辞2 | 0.03191395 | 17.73107 | 3.23326 |
| 数学无关编辑 | 0 | 0 | 0 |
| 生物无关编辑 | 0.02849598 | 15.83208 | 2.88698 |

可以观察到这个固定候选在本家族、两种措辞下响应生物前文；不能说只由最后层编码得出，也不能把19.36说成19.36%的解释方差或功能作用。最后层重构还包含其他feature叠加与decoder bias，向量可能相消。F09偏向32维集合只有**1个成员**随相关编辑改变，组级E=0.09563，不能写成32个共同模块同时响应。组级总体确认仍未过预设标准。

## 例2：SAE局部读数

F11目标末token为 ` difference`，ID6672，零起始位置30。数学前文讲数列收敛/增长，生物前文讲细菌抗药性。

**M1**：The note was read. The note was dated Monday. One sequence converged to zero, whereas the other grew without any finite bound. The author highlighted the difference


**B1**：The note was read aloud. The note was dated Monday. One bacterial strain survived the antibiotic, whereas the other strain stopped growing. The author highlighted the difference


生物偏向候选 **SAE f12478** 在数学两措辞均z=0，在生物两措辞为 **5.27339/2.54142**；decoder原空间范数为1，所以重构贡献幅度也是这两个值。其发现token贡献RMS=1.16135，归一化后为4.54075/2.18834。生物无关编辑为5.18066。它在留出生物文档命中579/3200位置、数学4/3200；独立DCLM为122/65536。这个局部实例不改变SAE偏向组总体q=0.375的结果。

## 例3：文档可分与固定目标是两件事

数学偏向候选 **SAE f9730** 在留出数学命中363/3200位置、生物0/3200；在16/20数学文档出现。最高响应留出文本为 `DOC_math_43665`，来源是Positive-definite kernel网页，测量窗口命中74/160，平均原空间贡献5.21571。其DCLM参考频率仅132/65536=0.2014%。

但它在6个留出家族所有目标token版本中都没有响应。这说明“在数学文档中常出现”并不保证“换到任一普通目标词仍会响应数学上下文”。它也可能依赖数学术语、格式或更具体条件，当前没有进一步干预鉴别。

## 反例：同一个候选换目标即不出现

F08的目标为 `the example`，末token ID3110，零起始位置32。数学前文说明质数，生物前文说明蜜蜂授粉；两种措辞及无关编辑都对齐。**CC f12314在六个版本全部z=0，最后层贡献也全部0**。该家族整个偏向集合的D=U=E=0。

更直接的组级反例：CC共享集合在F08的E=**−0.08341**；而F07为+0.08900。两种关系方向不同，不能凭一张好看的个例图认定所有家族稳定。图3必须和这些反例一起读。

精确原始z、范数与归一化量：执行侧 `analysis/*_context_feature_effects.npz`；完整前缀与实际token IDs见[texts_cn.md](texts_cn.md)及`data/context_panel.jsonl`。
