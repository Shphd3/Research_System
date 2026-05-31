# 06 Router Signal / Random Far Experts Result

## A. Router Signal Diagnostic

Condition:

```text
no router prior
no expert advantage
similar generalist experts
```

Initial signal:

| seed | expert-output gap | router grad W norm | loss |
|---:|---:|---:|---:|
| 0 | 0.0143 | 0.001565 | 0.149980 |
| 1 | 0.0222 | 0.002897 | 0.150200 |
| 2 | 0.0393 | 0.005294 | 0.150678 |

Final signal:

| seed | expert-output gap | router grad W norm | loss |
|---:|---:|---:|---:|
| 0 | 0.0219 | 0.000055 | 0.000046 |
| 1 | 0.0310 | 0.000077 | 0.000046 |
| 2 | 0.0580 | 0.000137 | 0.000046 |

Interpretation:

```text
experts are too similar;
router differential gradient is weak;
loss converges before router learns feature split.
```

Evidence:

```text
tables/diagnostics/router_signal_no_prior_no_advantage.csv
notes/diagnostics/router_signal_no_prior_no_advantage.md
```

## B. Random Far Experts

Condition:

```text
no router prior
random expert matrices with large parameter distance
10 seeds
```

Summary:

```text
separated final top-1 routing: 4/10
crossed initial expert utility: 5/10
mean final NMI: 0.4
```

Key table:

| seed | initial utility | pattern | margin | NMI | accuracy | loss |
|---:|---|---|---:|---:|---:|---:|
| 0 | shared | collapsed | 0.7823 | 0.0 | 0.5 | 0.000004 |
| 1 | shared | collapsed | 0.5733 | 0.0 | 0.5 | 0.000004 |
| 2 | shared | collapsed | 0.5232 | 0.0 | 0.5 | 0.000005 |
| 3 | crossed | separated | 0.4545 | 1.0 | 1.0 | 0.000007 |
| 4 | shared | collapsed | 0.4278 | 0.0 | 0.5 | 0.000078 |
| 5 | crossed | separated | 0.2724 | 1.0 | 1.0 | 0.000108 |
| 6 | shared | collapsed | 0.5530 | 0.0 | 0.5 | 0.000006 |
| 7 | crossed | separated | 0.2275 | 1.0 | 1.0 | 0.000086 |
| 8 | crossed | separated | 0.4979 | 1.0 | 1.0 | 0.000018 |
| 9 | crossed | collapsed | 0.3229 | 0.0 | 0.5 | 0.000025 |

Evidence:

```text
run_router_signal_and_random_far.py
tables/random_far_experts/
figures/random_far_experts/
notes/random_far_experts/
```

## Claim

Can claim:

```text
In this proxy, parameter distance alone is not sufficient.
Route-pattern separation mainly appears when experts provide crossed
feature-specific utility.
```

Cannot claim:

```text
full NTP behavior
utility-aligned specialization
random far initialization is reliable
```

## Next

```text
Build minimal NTP-style 2x2 task where next-token target creates
feature-specific utility pressure.
Do not run broad random sweeps.
```

