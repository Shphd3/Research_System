---
experiment_id: A15_01_02_E01_low_variance_functional_delay
verdict: weak_pass_delay_only_strong_fail
completed: 2026-07-31
canonical_language: en
---

# 结果：低方差延迟正确稳定，但不会把 tail 随机化

## 直接结果

**强猜想Fail，弱延迟猜想Pass。** native tail并不接近随机：32/32 tail Gate
最晚在step 2,460前同时达到正确和持续，最终准确率0.953，而匹配无标签random
tail只有0.501。低方差确实造成很大的有限时间延迟，能量均衡消除了其中大部分。

功能稳定时间 \(T_{FS}\) 定义为：held-out准确率至少0.90、route flip不超过0.02，
连续三次评估成立的首次optimizer step。它防止把“稳定地路由错”的随机Gate叫稳定。

| 条件 | 通过/32 | \(T_{FS}\)中位数 | restricted mean | 最终准确率 |
| --- | ---: | ---: | ---: | ---: |
| Native H | 32 | 600 | 552 | 0.973 |
| Native M | 32 | 1,080 | 912 | 0.967 |
| Native T | 32 | 2,130 | 1,938 | 0.953 |
| Equal-energy T | 32 | 660 | 615 | 0.972 |
| Random T | 0 | 删失 | 4,000 | 0.501 |

成对restricted-time差为H→M增加360步（95%区间[227,481]），M→T增加1,026步
（[802,1,255]）；能量均衡将tail restricted mean缩短68.3%。

## 中心图

![低方差延迟正确稳定](figures/functional_stability.png)

左图显示H/M/T的有序学习和equalized T恢复；右图说明只看churn会误判：random T
很快接近零flip，但准确率始终是机会水平。native T最终同时穿过两个功能门。

## 运行有效性

- 每个native/equal/random频带32/32正式种子完成。
- equal H/M/T为32/32通过，random H/M/T为0/32误通过。
- random H/M/T最终准确率为0.499、0.500、0.501。
- 远程job `pt-15rmvipu`上数值、配对、初始条件、正控与负控全部通过。

## 认识更新与边界

准确结论是：

> 小covariance会使可学习路由坐标更晚达到功能稳定，但小方差本身不会使它等价
> 于随机基底；tail最终会收敛到正确且持续的分区，均衡主要改变“何时学会”，
> 不是“学到什么”。

该结果属于matched-SNR线性受控系统。它不能说明自然tail有语义、真实checkpoint
会按相同比例恢复，或稳定路由一定改善专家训练。下一轮逐层谱画像必须联合报告
正确性与持续性，不能只看raw flip或covariance能量。
