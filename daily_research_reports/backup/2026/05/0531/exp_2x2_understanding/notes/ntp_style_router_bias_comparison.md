# Router Bias Comparison

Same conditions, seeds 0-9, 300 training steps.

## with_bias

- ntp_known_good: initial split 10/10, final split 10/10, mean final NMI 1.000
- ntp_no_router_prior: initial split 3/10, final split 3/10, mean final NMI 0.300
- ntp_no_prior_no_expert_advantage: initial split 3/10, final split 3/10, mean final NMI 0.300

## no_bias

- ntp_known_good: initial split 10/10, final split 10/10, mean final NMI 1.000
- ntp_no_router_prior: initial split 6/10, final split 6/10, mean final NMI 0.600
- ntp_no_prior_no_expert_advantage: initial split 6/10, final split 6/10, mean final NMI 0.600

