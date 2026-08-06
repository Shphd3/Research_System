# 03 Known-Good Result

Condition:

```text
router prior: yes
expert advantage: yes
seeds: 0,1,2
```

## Result

| seed | pattern | route margin | NMI | accuracy | entropy | max usage | loss |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | separated | 0.4065 | 1.0 | 1.0 | 0.6081 | 0.5010 | 0.000003 |
| 1 | separated | 0.4048 | 1.0 | 1.0 | 0.6088 | 0.5035 | 0.000003 |
| 2 | separated | 0.4023 | 1.0 | 1.0 | 0.6098 | 0.5067 | 0.000003 |

Evidence:

```text
run_known_good.py
tables/metrics_by_checkpoint.csv
tables/seed_checkpoint_summary.csv
figures/
notes/run_observations.md
```

## Claim

Can claim:

```text
With router prior + expert advantage, the proxy forms stable route-pattern separation.
```

Cannot claim:

```text
utility-aligned specialization
natural emergence without priors
full NTP behavior
ABC failure explanation
```

## Next

```text
Remove router prior.
Keep expert advantage.
```

