# ntp_no_prior_no_expert_advantage Observations

NTP-style top-1 sparse audit with fixed orthogonal hidden states.

Separated final top-1 routing: 1/3 seeds.
Mean final NMI: 0.3333.
Mean final CE loss: 0.000040.
Mean final per-feature accuracy: 1.0000.

- seed 0: pattern=collapsed, top1_A=0, top1_B=0, margin=0.9709, NMI=0.0000, route_acc=0.5000, CE=0.000056, token_acc=1.0000
- seed 1: pattern=collapsed, top1_A=1, top1_B=1, margin=0.9721, NMI=0.0000, route_acc=0.5000, CE=0.000056, token_acc=1.0000
- seed 2: pattern=separated, top1_A=1, top1_B=0, margin=0.7761, NMI=1.0000, route_acc=1.0000, CE=0.000008, token_acc=1.0000
