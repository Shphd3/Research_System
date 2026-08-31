---
thinking_card_id: 15_08_09_random_projection_router_preservation
status: HUMAN_CONFIRMED_FOR_FORMALIZATION_AND_EXECUTION
created: 2026-08-24
source:
  - ../../../../../../../daily_research_reports/0824/docs/random_projection_router_proof_protocol%20(1).md
  - ../../../../../../../daily_research_reports/0824/docs/random_projection_router_meeting_report.md
  - referenced conversation 6a8a5ab7-13d8-83ee-8fdd-e6d4f44c6e27
---

# Thinking Card：随机投影保留完整更新表征中的线性结构

## Current judgment

随机投影不是结构来源。只有当完整 $R_U$ 已经具有稳定正 margin 的线性结构时，才有资格检验随机投影能否保留它。

## Reason or mechanism

固定公共成分在样本差分中抵消；有限噪声只有限地恶化类内/类间间隔。对随机矩阵抽取前已经冻结的数据和线性 Router，高斯映射可用内积集中来保留有限样本上的分数差。反过来，线性投影后接线性分类器仍是原空间线性分类器，所以不能创造原本不存在的线性可分性。

## Strongest rival or uncertainty

此前的完整 $R_U$ 现象可能主要来自旧模板、标签词、重复语义种子或简单词袋线索；也可能完整空间虽有较高准确率，却没有跨模板稳定的正低分位数 margin；即使完整空间通过，结构也可能无法在 $m\le d/8$ 时稳定保留。

## Evidence that would change the judgment

冻结 taxonomy 的新数据通过泄漏和词袋守卫后，若 Qwen3-30B-A3B 的注册层仍不能在两个测试集上获得正的 5% margin 置信下界，则停止“随机投影保持”的主线。若完整空间通过而所有注册低维投影失败，则接受“可分但不可由该随机映射强压缩”。

## Next decision

按已批准的 Protocol 顺序执行数据守卫、完整空间门槛和条件化随机投影；科学失败保留，不通过事后改层、改 probe、改阈值或改 taxonomy 挽救。
