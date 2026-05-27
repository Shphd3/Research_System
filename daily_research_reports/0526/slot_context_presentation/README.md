# 0526 Slot-Context 汇报包

最重要的文件，先打开：

```text
anchor/slot_context_dominance_router_specialization_anchor.md
```

30 秒汇报时只看：

```text
talk_track.md
```

实验细节，需要 audit 时看：

```text
slot_context_dominance_router_specialization/detailed.md
slot_context_bridge_abcd_context_length/detailed.md
```

备份/同步材料：

```text
docs/
```

三张主图：

```text
figures/discussion_random_vs_slot_init_init_final_route_heatmaps.png
figures/bridge_abcd_final_nmi_by_seed_heatmap.png
figures/bridge_abcd_short_long_init_final_route_heatmaps.png
```

30 秒结论：

```text
slot 变长增强了 B hidden state 中的 slot feature，所以 router 更容易按 slot 分；
但 multi-B 里 B identity 仍然干扰，所以只得到部分 specialization。
```
