# 05 No Prior / No Expert Advantage Result

Condition:

```text
router prior: no
expert advantage: no
experts: similar weak generalists
seeds: 0,1,2
```

## Result

| seed | pattern | route margin | NMI | accuracy | entropy | max usage | loss |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | collapsed | 0.0162 | 0.0 | 0.5 | 0.6930 | 0.5081 | 0.000046 |
| 1 | collapsed | 0.0188 | 0.0 | 0.5 | 0.6930 | 0.5094 | 0.000046 |
| 2 | collapsed | 0.0371 | 0.0 | 0.5 | 0.6925 | 0.5185 | 0.000046 |

Evidence:

```text
run_no_prior_no_expert_advantage.py
tables/no_prior_no_expert_advantage/
figures/no_prior_no_expert_advantage/
notes/no_prior_no_expert_advantage/
```

## Interpretation

```text
loss decreases, but route-feature separation does not appear.
similar generalist experts give router little reason to split features.
expert advantage / differential utility is likely key in this proxy.
```

## Boundary

```text
This does not prove full NTP cannot specialize.
This does not test cross-entropy next-token prediction.
This does not prove utility-aligned specialization.
```

## Next

```text
Inspect router gradient and expert-output difference.
Test whether random far experts work only when they create crossed utility.
```

