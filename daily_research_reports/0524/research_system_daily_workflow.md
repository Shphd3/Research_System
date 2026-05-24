# Research System Daily Workflow

## 1. Core Rule

每天的研究过程只维护一条链：

```text
purpose -> hypothesis -> execution -> result -> interpretation -> hypothesis update -> sync/report
```

不要把实验记录、汇报、sync、mainline 写成四套互相竞争的入口。一个实验只允许一个第一阅读路径。

## 2. Before Running

先写或更新：

```text
Projects/from-attention-to-search/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/from-attention-to-search/main/experiments/<experiment_id>/execution_plan.md
```

`purpose_card.md` 写研究判断：

- 目的：这个实验要决定哪个问题；
- 假设：主假设和 rival explanation；
- 数学建模：对象、变量、期望关系；
- 预期结果：每种结果如何更新假设；
- 结论边界：即使实验成功也不能 claim 什么。

`execution_plan.md` 写运行细节：

- 数据构造；
- 模型和训练配置；
- metrics；
- commands；
- expected artifacts；
- pass/fail criteria。

## 3. During Running

运行过程不要直接写进 sync。先放在实验 workspace 或 experiment `detailed.md`。

只在下面情况更新主线文件：

- 结果改变 safest claim；
- 结果改变 hypothesis status；
- 结果改变 next decision；
- 结果改变 not-claimable boundary。

如果只是跑完但没有改变判断，daily card 写：

```text
No mainline update today.
```

## 4. After Results

先写：

```text
Projects/from-attention-to-search/main/experiments/<experiment_id>/summary.md
Projects/from-attention-to-search/main/experiments/<experiment_id>/detailed.md
```

`summary.md` 必须自包含：

```markdown
## 1. 目的
## 2. 假设
## 3. 实验设置
## 4. 结果
## 5. 解释
## 6. 结论边界
## 7. 下一步决策
## 8. 结果文档
```

`detailed.md` 放长表、失败 run、seed 差异、命令、artifact map。

然后回头更新：

```text
Projects/from-attention-to-search/main/hypotheses/<hypothesis_id>/purpose_card.md
Projects/from-attention-to-search/main/hypotheses/<hypothesis_id>/hypothesis_closure.md
```

更新重点不是复述结果，而是写清：

```text
原假设现在变强、变弱、被拆分，还是需要换 rival explanation？
```

## 5. Mainline Files

只有结论真的改变时，才更新：

```text
Projects/from-attention-to-search/main/current_mainline.md
Projects/from-attention-to-search/main/status.md
Projects/from-attention-to-search/main/roadmap.md
Projects/from-attention-to-search/main/consensus.md
Projects/from-attention-to-search/graph.yaml
```

文件职责：

- `current_mainline.md`：当前一句话主线、最安全 claim、下一步；
- `status.md`：今天/本阶段的 active task state；
- `roadmap.md`：gate 顺序和 stop rules；
- `consensus.md`：可以暂时当作共识使用的前提；
- `graph.yaml`：Sidecar 里的薄地图，只放节点和链接。

## 6. Daily Card

每天结束时写：

```text
daily_research_reports/MMDD/daily_card.md
```

建议固定结构：

```markdown
# Daily Card - MMDD

## 1. Today's Purpose

## 2. Mainline Anchor

## 3. Task Conclusions

### Task 1
Did:
Conclusion:

## 4. Mainline Update

## 5. What I Cannot Claim Yet

## 6. Next Decision

## 7. 30s Explanation

## 8. Recording / Class Notes

## 9. Small Thought Parking Lot
```

Daily card 是给自己收束判断，不是给同门协作的第一入口。

## 7. Closure Document

闭环文档分成两段：

1. 顶部是你会前填写的 oral card；
2. 后面是基于证据的正式 closure。

模板：

```markdown
# <Hypothesis ID> Closure

## Oral Report Card - Fill Before Meeting

目的：

假设：

结论：

证据：

## 1. 目的

## 2. 假设

## 3. 数学建模

## 4. 实验设置

## 5. 结果

## 6. 解释

## 7. 结论边界

## 8. 下一步决策

## 9. Artifact / Repro Map
code workspace:
runner:
config:
data / manifest:
result dir:
figure dir:
key files:
checkpoints / logs:
repro command:
```

顶部 oral card 可以留空让你填写；下面的证据区必须能链接到
`summary.md`、`detailed.md`、关键 figure、remote code path、config、result dir
和 repro command。

## 8. Sync File For Collaborators

sync 文件放在：

```text
Projects/from-attention-to-search/XingyuD/sync/MMDD_topic/
```

每个 sync folder 至少有：

```text
README.md
<topic>_sync.md
figures/
```

sync 必须 self-contained，且只引用项目仓库内可见路径。不要引用 root-level `daily_research_reports/`。

sync 更偏向把多个闭环文档连成 trajectory，方便同门理解你为什么从一个问题走到下一个问题。推荐结构：

```markdown
# <Topic> Sync - MMDD

## 0. Reading Path
This sync connects:
- closure / experiment A:
- closure / experiment B:
- current next decision:

## 1. 目的
这个同步要让同门理解哪个问题、为什么现在要看它。

## 2. 假设
主假设：
Rival explanations：

## 3. 数学建模
变量、对象、metric decision rule。

## 4. 实验设置
数据、模型、seed、配置、候选方法。

## 5. 结论
一句话结论。

## 6. 证据
关键图，每张图一句解释。

## 7. 结论边界
不能 claim 什么。

## 8. 下一步决策
同门接下来该看什么、做什么、确认什么。

## 9. Artifact / Repro Map
Code workspace:
Runner:
Config:
Data / manifest:
Result dir:
Figure dir:
Key files:
Checkpoints / logs:
Repro command:
```

这里的 `Artifact / Repro Map` 是和同门沟通的关键。没有代码和 repro 链接，sync 就只是汇报稿，不是协作文档。

## 9. Group Meeting Report

group meeting report 从 sync 汇总，不从聊天记录重写。

建议位置：

```text
daily_research_reports/MMDD/meeting/
daily_research_reports/MMDD/meeting/prism/
```

报告只保留最少但完整的判断链：

```markdown
## 1. Research Question
## 2. Why This Matters
## 3. Current Hypothesis
## 4. Experiment Setup
## 5. Key Result
## 6. Interpretation
## 7. What We Cannot Claim
## 8. Next Decision
## 9. Backup Figures / Artifact Map
```

group meeting 报告的第一原则：

```text
没有看过前一周材料的人，也能在 3 分钟内知道问题、证据、边界、下一步。
```

## 10. Current Project-Specific Advice

当前 `from-attention-to-search` 项目里，初始化校准应只是 `specialization -> router factor attribution` 下的一个节点。

不要把路线写成：

```text
initialization -> whole project
```

应该写成：

```text
specialization quality
  -> router factor attribution
    -> seed-dependent initialization calibration
```

当前能 claim 的是：

```text
B common-feature / identity anchor 在多数 seeds 存在，但 seed-dependent deviation 说明 router 初始边界可能影响最终 routing basin。
```

当前不能 claim：

```text
router fail 的本质原因就是 initialization。
```

下一步最干净的实验是：

```text
固定数据、模型、训练预算和非 router 随机性；
只改变 router/gating initialization；
检查 B identity-anchor stability、factor NMI、router-logit R2、component removal flip rate。
```
