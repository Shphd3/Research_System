---
experiment_id: A15_05_05_E01_2b_matched_band_dispatch
status: completed_fail_distribution_only
completed: 2026-07-31
canonical: summary.md
---

# 摘要：匹配计算的 2B 固定频带分发

## 结论

固定频带确实能把 token 送往不同专家，但在这条匹配的 2B DCLM 分叉中，没有
任何真实频带改善语言模型训练。head-only 是唯一优于同维随机子空间的真实
频带，但它仍显著落后于使用完整表征的 native Router；middle、tail 和
middle+tail 只产生了新的划分，没有产生功能收益。

正式裁定为：**Fail / distribution-only**。

## 指标先解释

- **Held-out NLL** 是模型对正确下一个 token 的平均“意外程度”，单位是
  nat/token，越低越好。表中正的 \(\Delta\) NLL 表示 treatment 更差。
- **路由分歧率** 是同一批固定 token 中，有多少相对单独训练的 native 模型
  换了专家。它只证明分发真的改变，不能证明改变有益。
- **同维随机子空间** 保留与真实频带相同的维数，但随机旋转方向；它区分
  “频带身份”与“单纯少看一些维度”。

## 主结果

native 的 held-out NLL 为 **4.246669 nat/token**。

| Gate 视图 | 相对 native 换专家 | 相对 native 的 \(\Delta\) NLL，95% CI | 相对同维随机的 \(\Delta\) NLL | 判断 |
| --- | ---: | ---: | ---: | --- |
| head-64 | 4.98% | +0.001784 [0.001359, 0.002202] | -0.004375 [-0.005152, -0.003576] | head 有特殊性，但单独使用信息不足 |
| middle-256 | 19.80% | +0.005600 [0.004656, 0.006498] | +0.002709 [0.001867, 0.003540] | 明显改路由，结果更差 |
| tail-448 | 21.88% | +0.003697 [0.002816, 0.004542] | +0.000765 [-0.000094, 0.001619] | 明显改路由，不优于随机 |
| middle+tail-704 | 13.26% | +0.003308 [0.002567, 0.004019] | +0.001811 [0.001084, 0.002527] | 改路由，结果更差 |

![相对 native 的最终 NLL 变化](figures/final_nll_effects_vs_native.png)

九个 8×RTX5090 任务均训练到 2.000683B tokens；负载、计算时间、checkpoint、
实际路由重放和投影基底护栏全部通过。最终负载熵为 0.9974--0.9983，没有负载
坍塌。中间 checkpoint 也没有显示后期反转。

## 边界与下一步

该结果严格适用于同一四层分叉种子，能证明固定频带会改变分发、但在该分叉中
不能改善 2B NLL。它不能证明 middle/tail 没有任何有用信息，因为没有测试
head+middle、head+tail 等增量读出，也没有学习任务条件化的语义坐标。

**下一决策：** 关闭“固定 covariance rank 的 band-only Router”作为候选；以后
任何大规模训练都必须先由直接的专家更新兼容性或任务效用指标准入。

完整证据见 [detailed.md](detailed.md)。
