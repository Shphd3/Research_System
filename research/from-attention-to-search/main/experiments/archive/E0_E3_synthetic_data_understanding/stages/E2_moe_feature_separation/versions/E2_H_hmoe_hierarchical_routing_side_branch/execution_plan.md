# Execution Plan: E2-H H-MoE Hierarchical Routing Side Branch

## 1. Plan Comparison

Compared with the earlier side-branch sketch, the `0515_hierarchical_synthetic_hmoe_plan.md` version is the one implemented here because it better matches the purpose.

Same direction:

- both test H-MoE as a side branch;
- both compare H-MoE against Flat-MoE;
- both avoid claiming real-language expert semantics.

Important differences:

- the 0515 plan starts from data audit, then dense baseline, then Flat/H-MoE;
- the 0515 plan explicitly separates L1 phrase readback and L2 event readback;
- the 0515 plan uses a 4-root x 2-leaf H-MoE with 8 active leaf experts total, matching Flat-MoE's 8 experts;
- the earlier sketch focused more on routing structure and less on proving the hierarchical data and dense learnability first.

Decision: implement the 0515 plan, with one clarification: each L2 event is made an exact entity-action-object triple so L2 readback has a unique correct target.

## 2. Data

Config:

```text
configs/e2_h_hmoe_hierarchical_side_branch.json
```

Main settings:

```text
vocab_size = 128
corpus_length = 1,000,000
p_event = 0.35
p_l1 = 0.20
seq_len = 64
seeds = 20260513..20260517
```

L1 phrases:

```text
E1=[1,2], E2=[3,4], E3=[5,6], E4=[7,8]
A1=[17,18], A2=[19,20], A3=[21,22], A4=[23,24]
O1=[25,26], O2=[27,28], O3=[29,30], O4=[31,32]
```

L2 events:

```text
F1_E1_A1_O1=[1,2,17,18,25,26]
F1_E2_A1_O2=[3,4,17,18,27,28]
F2_E1_A2_O3=[1,2,19,20,29,30]
F2_E3_A2_O4=[5,6,19,20,31,32]
F3_E2_A3_O1=[3,4,21,22,25,26]
F3_E4_A3_O3=[7,8,21,22,29,30]
F4_E3_A4_O2=[5,6,23,24,27,28]
F4_E4_A4_O4=[7,8,23,24,31,32]
```

## 3. Models

Dense:

```text
1-layer causal Transformer + dense FFN
```

Flat-MoE:

```text
1-layer causal Transformer + top-1 8-expert FFN
load-balance coef = 0.01
```

H-MoE:

```text
1-layer causal Transformer + top-1 root router + top-1 leaf router
root_groups = 4
leaf_per_group = 2
total leaf paths = 8
load-balance coef = 0.01
```

Shared settings:

```text
d_model = 64
n_heads = 4
expert_ffn_dim = 32
dense_ffn_dim = 128
batch_size = 128
steps = 5000
lr = 0.0006
dense_lr = 0.0003
```

## 4. Metrics

Readback:

- `L1 probability`: probability of phrase second token after phrase first token.
- `L2 probability`: probability of correct object first token after entity+action prefix.
- `margin`: target logit minus strongest wrong logit.

Routing:

- `NMI`: how strongly expert/root/path id and planted label share information; higher means stronger alignment.
- `purity`: for each routed bucket, the dominant planted label fraction; higher means cleaner buckets.
- `event root consistency`: within one 6-token event, how often H-MoE root choices stay in one root group.

## 5. Commands

Smoke:

```bash
python scripts/run_hmoe_hierarchical_side_branch.py \
  --config configs/e2_h_hmoe_hierarchical_side_branch.json \
  --smoke
```

Full run:

```bash
python scripts/run_hmoe_hierarchical_side_branch.py \
  --config configs/e2_h_hmoe_hierarchical_side_branch.json
```

## 6. Output Contract

Ignored runnable outputs:

```text
outputs/e2_h_hmoe_hierarchical_side_branch/
figures/e2_h_hmoe_hierarchical_side_branch/
```

Report figures copied here:

```text
figures/
```

## 7. Pass / Fail Criteria

Support for H-MoE:

- dense, Flat-MoE, and H-MoE all read back L1/L2;
- H-MoE root vs L2 family alignment is stronger and more stable than Flat expert vs L2 family;
- H-MoE path/leaf vs L1 phrase alignment is stable;
- event root consistency is high.

Weak or no support:

- readback succeeds but H-MoE routing is not cleaner than Flat-MoE;
- H-MoE alignment has large seed variance;
- root choices do not stay consistent inside events.

