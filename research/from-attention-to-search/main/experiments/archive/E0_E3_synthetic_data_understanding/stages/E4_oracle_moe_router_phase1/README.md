# E4 Oracle-MoE Router Phase 1

E4 是 router failure mode 主线的统一阶段。它回答：

```text
当 router 输入改成 raw attention_output、expert 输入保持 original hidden / residual 时，
MoE 能不能形成稳定的 one-feature-one-expert routing reference？
```

## Read Order

1. `summary.md`：E4 总览闭环，先读这个。
2. `versions/E4_1_raw_attention_shortcut_controls/summary.md`：uniform + shortcut controls。
3. `versions/E4_2_zipf_raw_attention/summary.md`：Zipf / long-tail controls。
4. `versions/E4_3_simple_unsupervised_center_control/summary.md`：random-position KMeans 无监督对照。
5. `versions/D_star_boundary_direction_audit/summary.md`：router boundary 到底沿什么方向切。
6. `detailed.md`：运行记录和长表格。
7. `versions/E4_LN_legacy_20260519/`：旧 `LN(attention_output)` router-space 结果，仅作历史对照。

## Logic Chain

| version | question | status |
|---|---|---|
| E4.0 / C0-C6 | ordinary / center / inhibition router 是否自然 clean？ | readback 成功，但 feature routing 不稳定 |
| E4.1 | shortcut controls 后，C7 是否仍保持 feature alignment？ | C7e 最强 |
| E4.2 | Zipf 长尾频率下，C7 是否仍有效？ | C7d/C7e 仍最强，但低频稳定性待查 |
| E4.3 | random-position KMeans 能否替代 oracle feature-prefix init？ | 不能，NMI 和 expert load collapse |
| D* | router boundary 到底沿 feature、common 还是 utility 方向切？ | 普通 router 偏 common direction；C7 更 feature-related 但不是纯 feature boundary |

## Current Conclusion

E4 支持：

```text
feature-aligned routing 是可构造的；
但它依赖正确采样 rule-context 表征，再用 center init + 正则/utility feedback 稳住。
Natural NTP 或无倾向 random-position KMeans 不能自动得到 clean routing。
```

## Claim Boundary

可以说：C7d/C7e 是当前最强 synthetic routing reference。

不能说：自然 MoE 已经无监督发现 relation-level feature routing，也不能说 C7 已经可直接迁移到真实语言。
