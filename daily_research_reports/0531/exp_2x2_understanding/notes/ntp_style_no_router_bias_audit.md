# NTP-Style No Router Bias Audit

Router uses Linear(2, 2, bias=False). Other settings are unchanged.

- ntp_known_good: initial split 10/10, final split 10/10, mean final NMI 1.000, mean token acc 1.000
- ntp_no_router_prior: initial split 6/10, final split 6/10, mean final NMI 0.600, mean token acc 1.000
- ntp_no_prior_no_expert_advantage: initial split 6/10, final split 6/10, mean final NMI 0.600, mean token acc 1.000

Seed details:

## ntp_known_good

- seed 0: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.921,0.920)
- seed 1: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.922,0.923)
- seed 2: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.919,0.923)
- seed 3: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.919,0.919)
- seed 4: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.922,0.918)
- seed 5: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.920,0.920)
- seed 6: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.919,0.918)
- seed 7: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.920,0.916)
- seed 8: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.921,0.921)
- seed 9: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.917,0.921)
## ntp_no_router_prior

- seed 0: top1=(0,0), NMI=0.0, token_acc=1.0, gate=(0.921,0.927)
- seed 1: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.879,0.879)
- seed 2: top1=(1,1), NMI=0.0, token_acc=1.0, gate=(0.929,0.923)
- seed 3: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.895,0.899)
- seed 4: top1=(0,0), NMI=0.0, token_acc=1.0, gate=(0.922,0.928)
- seed 5: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.901,0.895)
- seed 6: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.900,0.896)
- seed 7: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.894,0.905)
- seed 8: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.876,0.879)
- seed 9: top1=(1,1), NMI=0.0, token_acc=1.0, gate=(0.928,0.920)
## ntp_no_prior_no_expert_advantage

- seed 0: top1=(0,0), NMI=0.0, token_acc=1.0, gate=(0.924,0.925)
- seed 1: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.891,0.889)
- seed 2: top1=(1,1), NMI=0.0, token_acc=1.0, gate=(0.926,0.927)
- seed 3: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.888,0.889)
- seed 4: top1=(0,0), NMI=0.0, token_acc=1.0, gate=(0.926,0.925)
- seed 5: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.891,0.887)
- seed 6: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.890,0.889)
- seed 7: top1=(1,0), NMI=1.0, token_acc=1.0, gate=(0.886,0.895)
- seed 8: top1=(0,1), NMI=1.0, token_acc=1.0, gate=(0.890,0.887)
- seed 9: top1=(1,1), NMI=0.0, token_acc=1.0, gate=(0.925,0.924)
