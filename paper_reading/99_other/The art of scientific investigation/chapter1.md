# Chapter 1 - Preparation

## 1. 本章一句话
科研开始于准备：批判性读文献、收集真实观察、定义问题、提出多个假设，并设计关键实验。

## 2. 作者核心观点
1. 研究者终身学习，但阅读不能只是积累信息。
2. 文献要批判性阅读，尤其要区分 result 和 interpretation。
3. 初学者应选择有兴趣、可执行、能得到指导的问题。
4. 开始实验前，要收集一手观察资料。
5. 研究原因前，必须先定义研究对象。
6. 好实验不是盲目多做，而是回答 crucial questions。
7. crucial experiment 是能区分两个假设的实验。

## 3. 对我的科研的映射
我的长期愿景是“一学就会，永不遗忘”，但当前不能直接研究这个大愿景。
当前更合适的问题是：
在 feature-Zipf synthetic world 中，MoE specialization 是否能对齐层级 sparse mechanism？

我必须先定义 specialization：
- feature-level specialization
- function-level specialization
- routing-level specialization
- frequency-level specialization
- continual-learning specialization

## 4. 当前项目观察
当前实验显示：
- Oracle 证明机制可恢复；
- learned models 比 random 更强；
- Hierarchical MoE 在 function cos 上略高；
- Hierarchical MoE 在 Leaf NMI / feature selectivity 上没有明显超过 flat middle spectral；
- flat middle spectral 在 sparse dict feature division 上更强。

## 5. 当前假设更新
旧假设：
Hierarchical MoE 更会 specialization。

新假设：
H1: Hierarchical MoE 可能更有利于 function-level mechanism recovery。
H2: Middle spectral routing 可能更有利于 feature-level routing separation。
H3: specialization 不是单一概念，需要拆成 feature/function/routing/frequency 几类。

## 6. 下一步关键实验
做 2×2 实验：
architecture: flat vs hierarchical
router input: raw hidden vs middle spectral

目标：
区分 hierarchy 和 spectral signal 哪个才是当前主要机制杠杆。

## 7. 我读完本章后的行动
- 建立 hypothesis_board.md；
- 建立 observation_log.md；
- 每个实验前写清楚：它区分哪两个解释；
- 每次汇报不按实验流水账，而按 claim boundary 汇报。