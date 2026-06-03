# Random Far Experts Run Observations

Condition: no router prior; experts are random matrices with large initial distance, not hand-coded feature-specific advantages.

Separated final top-1 routing: 4/10 seeds.
Crossed initial expert utility preference: 5/10 seeds.
Mean final route margin: 0.4635.
Mean final NMI: 0.4000.

Final checkpoint summary:

- seed 0: pattern=collapsed, initial_utility=shared, margin=0.7823, NMI=0.0000, accuracy=0.5000, entropy=0.3316, loss=0.000004, expert_gap=2.0935, router_grad_w_norm=0.000125
- seed 1: pattern=collapsed, initial_utility=shared, margin=0.5733, NMI=0.0000, accuracy=0.5000, entropy=0.5038, loss=0.000004, expert_gap=1.5224, router_grad_w_norm=0.000070
- seed 2: pattern=collapsed, initial_utility=shared, margin=0.5232, NMI=0.0000, accuracy=0.5000, entropy=0.5310, loss=0.000005, expert_gap=2.3472, router_grad_w_norm=0.000082
- seed 3: pattern=separated, initial_utility=crossed, margin=0.4545, NMI=1.0000, accuracy=1.0000, entropy=0.5627, loss=0.000007, expert_gap=2.7674, router_grad_w_norm=0.000113
- seed 4: pattern=collapsed, initial_utility=shared, margin=0.4278, NMI=0.0000, accuracy=0.5000, entropy=0.5981, loss=0.000078, expert_gap=1.4328, router_grad_w_norm=0.000330
- seed 5: pattern=separated, initial_utility=crossed, margin=0.2724, NMI=1.0000, accuracy=1.0000, entropy=0.6427, loss=0.000108, expert_gap=1.7403, router_grad_w_norm=0.000303
- seed 6: pattern=collapsed, initial_utility=shared, margin=0.5530, NMI=0.0000, accuracy=0.5000, entropy=0.5300, loss=0.000006, expert_gap=2.2591, router_grad_w_norm=0.000205
- seed 7: pattern=separated, initial_utility=crossed, margin=0.2275, NMI=1.0000, accuracy=1.0000, entropy=0.6643, loss=0.000086, expert_gap=1.4104, router_grad_w_norm=0.001257
- seed 8: pattern=separated, initial_utility=crossed, margin=0.4979, NMI=1.0000, accuracy=1.0000, entropy=0.5488, loss=0.000018, expert_gap=1.6555, router_grad_w_norm=0.001312
- seed 9: pattern=collapsed, initial_utility=crossed, margin=0.3229, NMI=0.0000, accuracy=0.5000, entropy=0.6205, loss=0.000025, expert_gap=1.5893, router_grad_w_norm=0.000396
