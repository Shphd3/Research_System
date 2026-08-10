> 主线结论：conditional-fine 的本地参数秩后移成立，但没有进入全局共享 F9--F16 tail。
> 保留现象：晚层方差更靠后的是“各层自己的排序位置”，不是已确认的跨层共同 tail 方向。
> 当前障碍：共享 middle 的正变化究竟是真实内部结构，还是归一化与宽 band 平均造成的表象。
> 当前研究锚点：A15_04 已以稳定 Fail 闭环；A15_03 是唯一待审核的独立几何问题。
> 允许范围：只解释 conditional-fine 几何；不判断 MLP 使用、任务功能或 Router 收益。
> 关闭规则：不得事后挑 F9--F13 挽救 tail，也不得由 shared-middle 正变化直接开启功能实验。

# 本地参数秩后移是否进入跨层共享的广义 tail？

状态：A15_04_E01 已完成；以下认识更新为 AI 初稿，等待研究者纠正表述。

## 1. 本日唯一回答的问题

对冻结 Qwen3-8B 的实际 attention 引起的 MLP 输入增量 $\Delta n$，大类内部的小类中心差异是否从早层到晚层更富集于跨层共享的 F9--F16 tail，并超过同维随机空间、F1 head 与 F2--F8 middle？

## 2. 认识更新

**回答：没有。**“本地参数秩重心”确实从早层 0.3699 增到晚层 0.4711；它表示 conditional-fine 方差在每层自己的参数增益排序中向后移动。可是把不同层放回共同隐状态坐标、用另一组层构造共享空间后，广义 tail 的维度归一化富集反而从 1.0536 降到 0.9501。

“维度归一化富集”是共享空间捕获的方差比例，除以同维随机空间的期望捕获；1 表示随机基准。因此 H/M/T 虽然维度不同，变化可以公平比较。共享 middle 增加 0.2284，共享 tail 减少 0.1035，tail 相对最强非 tail 区域的主统计量为 $D_T=-0.3319$，95% 区间完全小于 0。

这不是不稳定：奇层、偶层和两组封存表达中的 tail 变化都为负，32 次坐标量化扰动也不改变符号。完整 F1--F16 显示 F9--F13 增加、F14--F16 下降，尤其 F16；注册对象是整个 F9--F16，不能事后缩窄 tail。

![A15_04 全局主裁定](../../Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/figures/figure0_broad_tail_decision.png)

## 3. 最小证据表

| 对象 | 早层到晚层变化 | 95% 区间 | 判断 |
|---|---:|---:|---|
| 本地参数秩重心 | +0.1012 | [0.0873, 0.1139] | 本地后移成立 |
| 本地 F9--F16 富集 | +0.2476 | [0.2103, 0.2768] | 本层 tail 份额增加 |
| 全局共享 middle | +0.2284 | [0.1932, 0.2783] | 值得独立审计 |
| 全局共享 tail | -0.1035 | [-0.1421, -0.0768] | 广义 tail 假设失败 |
| tail 特异性 $D_T$ | -0.3319 | [-0.4129, -0.2711] | tail 明确输给 middle |

早晚 tail 参数投影仍比随机空间更重合，但 late-internal 与 early-to-late 的 conditional-fine 富集没有超过随机，因此分层标签是 `mixed_stage_geometry`。它只说明“共享参数 tail 存在，但晚层细类方差没有在其中增强”，不能挽救全局 Fail。

## 4. 解释流程图（AI 初稿，研究者修改）

```mermaid
flowchart LR
    A["观察：本地秩重心后移"] --> B["竞争解释：跨层共享 tail 或仅本地重排"]
    B --> C["共同坐标 + 奇偶层互斥 + 同维随机"]
    C --> D["共享 middle 增加；共享 tail 稳定下降"]
    D --> E["关闭全局共享 tail 解释"]
    E --> F["只审核 middle 内部结构；不进入功能或 Router"]
```

## 5. 边界与唯一下一步

- **直接结果：**A15_04 的注册 verdict 是 `LOCAL_RANDOM_OR_NONTAIL_RELOCATION`。
- **不能声称：**tail 是随机空间、MLP 不使用 tail、middle 具有任务功能、信息必然非线性，或应设计 nonlinear Router。
- **完整证据：**[结果摘要](../../Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/summary.md)；逐方向原方差与归一化平滑展示见其中 figure 3。平滑只为压低 4,096 个方向的视觉噪声，所有统计与裁定都使用未平滑值。
- **唯一下一决策：**是否批准现有 A15_03 middle-band Protocol，检验 shared-middle 正变化是内部稳定结构，还是归一化、抵消或秩平均的产物。
- **完成判据：**A15_03 保持独立对象并区分上述竞争解释；不得把 A15_04 的 tail 失败当作 middle 功能证据。
- **恢复动作：**打开 A15_03 的 `DRAFT_NOT_EXECUTABLE` Protocol，只审核对象、主统计量与停止规则。
