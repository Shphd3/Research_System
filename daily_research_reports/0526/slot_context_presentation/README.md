# 0526 Slot-Context 汇报包

入口文档：

```text
talk_track.md
```

核心材料：

```text
docs/anchor_slot_context_signal_and_route_utility_binding.md
docs/slot_context_summary.md
docs/bridge_abcd_summary.md
```

三张主图：

```text
figures/01_short_vs_long_routing_init_final.png
figures/02_fixed_multi_bridge_nmi_by_seed.png
figures/03_bridge_short_long_route_heatmaps.png
```

一句话结论：

```text
slot 变长增强了 B hidden state 中的 slot feature，所以 router 更容易按 slot 分；
但 multi-B 里 B identity 仍然干扰，所以只得到部分 specialization。
```
