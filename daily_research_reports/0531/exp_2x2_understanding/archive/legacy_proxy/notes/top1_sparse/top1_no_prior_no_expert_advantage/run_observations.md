# top1_no_prior_no_expert_advantage Observations

Top-1 sparse forward; router gradient through selected softmax gate.

Separated final top-1 routing: 1/3 seeds.
Mean final route margin: 0.5110.
Mean final NMI: 0.3333.

- seed 0: pattern=collapsed, top1_A=1, top1_B=1, margin=0.5863, NMI=0.0000, accuracy=0.5000, selected_gate=0.7931, loss=0.000001
- seed 1: pattern=separated, top1_A=0, top1_B=1, margin=0.3641, NMI=1.0000, accuracy=1.0000, selected_gate=0.6821, loss=0.000033
- seed 2: pattern=collapsed, top1_A=1, top1_B=1, margin=0.5826, NMI=0.0000, accuracy=0.5000, selected_gate=0.7913, loss=0.000001
