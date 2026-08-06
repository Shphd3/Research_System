# Reliability Checklist - Gating Mainline

## P0: Code correctness

- [ ] Gate input hook 确认是 attention output。
- [ ] Expert input hook 确认仍是 original hidden/residual representation。
- [ ] Router logits 与 expert outputs 的 batch/time positions 对齐。
- [ ] Causal mask 正确；router 不读未来 token。
- [ ] top-1 / top-k gating 的 straight-through 或 gradient path 明确。
- [ ] load-balance / supervised / inhibition loss 开关可单独关闭。

## P1: Metric correctness

- [ ] Routing analysis 不只报 NMI；必须报 expert cell examples、route flip、utility gap。
- [ ] Feature label 只作为 synthetic annotation，不作为唯一解释变量。
- [ ] 每个诊断都要有 random / token / local / feature-oracle baseline。
- [ ] 多 seed；至少报告 mean/std 或标注 single-seed limitation。

## P2: Claim safety

- [ ] 不把 supervised clean routing 说成 natural specialization。
- [ ] 不把 inhibition partition 说成模型自然学到。
- [ ] 不把 expert id 的可解释性等同于 expert causal mechanism。
