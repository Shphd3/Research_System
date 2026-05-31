# 04 No Router Prior Result

Condition:

```text
router prior: no
expert advantage: yes
seeds: 0,1,2
```

## Result

| seed | pattern | route margin | NMI | accuracy | entropy | max usage | loss |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | separated | 0.1756 | 1.0 | 1.0 | 0.6776 | 0.5022 | 0.000012 |
| 1 | separated | 0.1733 | 1.0 | 1.0 | 0.6779 | 0.5071 | 0.000012 |
| 2 | separated | 0.1700 | 1.0 | 1.0 | 0.6782 | 0.5139 | 0.000013 |

Evidence:

```text
run_no_router_prior.py
tables/no_router_prior/
figures/no_router_prior/
notes/no_router_prior/
```

## Interpretation

```text
router prior is not necessary for top-1 separation.
router prior increases separation margin.
expert advantage remains the key active condition.
```

## Boundary

```text
No utility-aligned claim.
No full NTP claim.
No claim that expert advantage is unnecessary.
```

## Next

```text
Remove expert advantage.
Keep no router prior.
```

