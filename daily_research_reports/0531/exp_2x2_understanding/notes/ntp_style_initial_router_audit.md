# NTP-Style Initial Router Audit

For h_A=e1 and h_B=e2, logits are the corresponding router matrix column plus bias.

## ntp_no_router_prior seed 0

```text
W = [[0.002878, 0.018957],
     [-0.019357, -0.011867]]
b = [-0.000104, -0.003592]
logits A=[0.002774, -0.022949], B=[0.018853, -0.015459]
probs  A=[0.506430, 0.493570], B=[0.508577, 0.491423]
delta(E1-E0) A=-0.025723, B=-0.034311; top1=(0, 0); pattern=collapsed
```

## ntp_no_router_prior seed 1

```text
W = [[0.004883, -0.007187],
     [0.020685, 0.037928]]
b = [0.002054, -0.004940]
logits A=[0.006936, 0.015745], B=[-0.005133, 0.032988]
probs  A=[0.497798, 0.502202], B=[0.490471, 0.509529]
delta(E1-E0) A=0.008809, B=0.038122; top1=(1, 1); pattern=collapsed
```

## ntp_no_router_prior seed 2

```text
W = [[-0.007149, 0.003721],
     [0.002339, -0.002411]]
b = [0.002086, 0.005002]
logits A=[-0.005062, 0.007341], B=[0.005807, 0.002591]
probs  A=[0.496899, 0.503101], B=[0.500804, 0.499196]
delta(E1-E0) A=0.012403, B=-0.003216; top1=(1, 0); pattern=split
```

## ntp_no_prior_no_expert_advantage seed 0

```text
W = [[0.002878, 0.018957],
     [-0.019357, -0.011867]]
b = [-0.000104, -0.003592]
logits A=[0.002774, -0.022949], B=[0.018853, -0.015459]
probs  A=[0.506430, 0.493570], B=[0.508577, 0.491423]
delta(E1-E0) A=-0.025723, B=-0.034311; top1=(0, 0); pattern=collapsed
```

## ntp_no_prior_no_expert_advantage seed 1

```text
W = [[0.004883, -0.007187],
     [0.020685, 0.037928]]
b = [0.002054, -0.004940]
logits A=[0.006936, 0.015745], B=[-0.005133, 0.032988]
probs  A=[0.497798, 0.502202], B=[0.490471, 0.509529]
delta(E1-E0) A=0.008809, B=0.038122; top1=(1, 1); pattern=collapsed
```

## ntp_no_prior_no_expert_advantage seed 2

```text
W = [[-0.007149, 0.003721],
     [0.002339, -0.002411]]
b = [0.002086, 0.005002]
logits A=[-0.005062, 0.007341], B=[0.005807, 0.002591]
probs  A=[0.496899, 0.503101], B=[0.500804, 0.499196]
delta(E1-E0) A=0.012403, B=-0.003216; top1=(1, 0); pattern=split
```

