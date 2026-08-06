# top1_no_router_prior Observations

Top-1 sparse forward; router gradient through selected softmax gate.

Separated final top-1 routing: 1/3 seeds.
Mean final route margin: 0.4841.
Mean final NMI: 0.3333.

- seed 0: pattern=collapsed, top1_A=1, top1_B=1, margin=0.5661, NMI=0.0000, accuracy=0.5000, selected_gate=0.7831, loss=0.000003
- seed 1: pattern=separated, top1_A=0, top1_B=1, margin=0.3223, NMI=1.0000, accuracy=1.0000, selected_gate=0.6612, loss=0.000013
- seed 2: pattern=collapsed, top1_A=1, top1_B=1, margin=0.5640, NMI=0.0000, accuracy=0.5000, selected_gate=0.7820, loss=0.000003
