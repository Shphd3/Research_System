# Result CSV Schema

Every metrics row should include:

```text
exp_id
seed
method
method_label
data_regime
d
E
n_cal
n_holdout
run_mode
```

Static metrics:

```text
cal_loadcv
holdout_loadcv
holdout_max_abs_error
holdout_gap
margin_p05
tie_rate
max_atom_mass
```

Feature metrics:

```text
route_feature_nmi
feature_purity
within_cell_var
cell_proto_alignment
```

Expert metrics:

```text
proto_spread
nearest_neighbor_cosine
max_pairwise_cosine
effective_proto_rank
```

Training metrics:

```text
epoch
train_loss
val_loss
route_flip_rate
representation_drift
accepted_update_count
```
