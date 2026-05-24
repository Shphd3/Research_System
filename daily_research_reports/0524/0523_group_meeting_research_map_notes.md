# 0523 Group Meeting Research Map Notes

## 1. Main Consensus

当前主线不是先证明 MoE expert id 可以直接作为 KV index，而是先研究：

```text
representation / expert specialization 是否能作为 reverse index、KV cache 压缩、prediction、低干扰学习的上游原因。
```

这仍然只是研究假设，不是已证明结论。

## 2. Large Research Map

组会后的大图应写成：

```text
long-context attention as learned search
  -> learned KV candidate index
    -> representation / expert specialization
      -> specialization measurement
      -> router factor attribution
        -> initialization calibration
        -> frequency / geometry diagnostic
      -> induced specialization candidates
        -> oracle routing
        -> attention-relation constrained routing
        -> hierarchical / frequency-balanced grouping
      -> reverse-index utility
      -> real-data and engineering transfer
```

初始化校准只是 `router factor attribution` 下面的子诊断，不是整条路线。

## 3. What Current Results Cover

当前结果覆盖的是 specialization 诊断的前半段：

- H0521 AB：削弱 clean A/B/AB expert bucket；
- H0521b seq32：削弱稳定 source-token feature bucket；
- H0522 B-context control：说明 B common-feature / identity anchor 多数存在，但有 seed-dependent deviation；
- H0522 SVD：说明 AB-dominant expert 不是独有 functional AB specialist；
- H0522 factor audit：提示 identity、position、target shortcut、second identity 比 rule/function 更能解释 routing；
- E4：说明 feature-aligned routing 可以被构造，但普通 NTP 不会自然稳定得到；
- R0/R1：说明 same-bucket KV 有高于 random 的 retrieval signal，但不足以证明 expert id 是可用 reverse index。

## 4. Claim Boundary

可以说：

```text
vanilla no-load-balance top-1 MoE 在当前 A/B/AB synthetic setup 中没有自然形成稳定、干净、可直接作为 feature-level learned index 的 expert bucket。
```

不能说：

```text
MoE 不能 specialize；
router fail 的本质原因就是 initialization；
attention-relation routing 已经解决 reverse index；
toy synthetic 结论可以直接迁移到真实语言。
```

## 5. Immediate Next Decision

下一步应先完成：

```text
router factor attribution
```

如果发现 seed-dependent deviation 主要来自 router 初始方向，再进入：

```text
router initialization calibration audit
```

如果不是，则转向 frequency / geometry / data distribution 的诊断。
