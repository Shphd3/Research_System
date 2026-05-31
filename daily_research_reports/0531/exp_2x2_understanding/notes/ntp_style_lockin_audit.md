# NTP-Style Lock-In Audit

Scope: existing NTP-style top-1 runs only: no-router-prior and no-prior/no-expert-advantage.

Main result:

- ntp_no_router_prior seed 0: step0=(0,0), step300=(0,0), NMI_final=0.0, gate_A_final=0.985, gate_B_final=0.986, tag=early_lock_in
- ntp_no_router_prior seed 1: step0=(1,1), step300=(1,1), NMI_final=0.0, gate_A_final=0.986, gate_B_final=0.985, tag=early_lock_in
- ntp_no_router_prior seed 2: step0=(1,0), step300=(1,0), NMI_final=1.0, gate_A_final=0.903, gate_B_final=0.891, tag=success_control
- ntp_no_prior_no_expert_advantage seed 0: step0=(0,0), step300=(0,0), NMI_final=0.0, gate_A_final=0.986, gate_B_final=0.985, tag=early_lock_in
- ntp_no_prior_no_expert_advantage seed 1: step0=(1,1), step300=(1,1), NMI_final=0.0, gate_A_final=0.986, gate_B_final=0.986, tag=early_lock_in
- ntp_no_prior_no_expert_advantage seed 2: step0=(1,0), step300=(1,0), NMI_final=1.0, gate_A_final=0.892, gate_B_final=0.884, tag=success_control
