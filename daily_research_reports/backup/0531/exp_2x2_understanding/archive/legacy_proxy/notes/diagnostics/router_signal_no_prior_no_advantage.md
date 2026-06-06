# Router Signal Diagnostic

Condition: no router prior and no feature-specific expert advantage.

Initial checkpoint:

- seed 0: expert_gap=0.0143, router_grad_w_norm=0.001565, mean_grad_logit_norm=0.002204, loss=0.149980
- seed 1: expert_gap=0.0222, router_grad_w_norm=0.002897, mean_grad_logit_norm=0.003583, loss=0.150200
- seed 2: expert_gap=0.0393, router_grad_w_norm=0.005294, mean_grad_logit_norm=0.007061, loss=0.150678

Final checkpoint:

- seed 0: expert_gap=0.0219, router_grad_w_norm=0.000055, mean_grad_logit_norm=0.000061, loss=0.000046
- seed 1: expert_gap=0.0310, router_grad_w_norm=0.000077, mean_grad_logit_norm=0.000097, loss=0.000046
- seed 2: expert_gap=0.0580, router_grad_w_norm=0.000137, mean_grad_logit_norm=0.000189, loss=0.000046
