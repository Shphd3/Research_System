# Protocol: A11_03_01_E02 End-to-End Bridge-Conditioned Semantic Efficiency

## 0. Approval Snapshot

**Approval status:** approved under the user's standing instruction for subsequent anchors and remote four-GPU runs.  
**Purpose:** test whether A11_19's bridge-conditioned local transport predicts finite-step standard-H1 semantic learning.  
**Primary anchor:** `../../../../problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_01_cross_position_proxy_falsification_anchor.md`.
**Experiment role:** minimal end-to-end mechanism test.  
**Primary metric:** per-seed objective-by-bridge interaction in held-out $Q_{real}$ AUC over updates `0-300`.  
**Conditions:** `NTP/MTP × Decision/Therefore`, five seeds.  
**Pass:** positive interaction in at least `4/5`, positive MTP gain under `Therefore` in at least `4/5`, and positive mean interaction.  
**Fail:** interaction positive in at most `2/5` or mean interaction non-positive, with all guards valid.  
**Insufficient:** any pairing, schedule, data, finiteness, local-learning, or completeness guard fails.  
**Cannot claim:** general MTP superiority or natural-pretraining benefit.

## 1. Conditions And Fixed Variables

| Condition | Bridge token | Objective | Extra earlier H2 answer loss |
|---|---|---|---:|
| `ntp_decision` | ` Decision` | NTP | no |
| `mtp_decision` | ` Decision` | MTP | yes |
| `ntp_therefore` | ` Therefore` | NTP | no |
| `mtp_therefore` | ` Therefore` | MTP | yes |

Fixed: Qwen3-0.6B Base, A11_13 data, train/eval paraphrase split, H1 answer tokens, optimizer, learning rate, examples, per-seed schedule, 300 updates, and evaluation checkpoints.

## 2. Metrics

The held-out downstream score is

$$
Q_{real}(t)=\min\{A_{H1}(t),C_{para}(t),S_{cf}(t)\}.
$$

For trapezoidal AUC normalized by the interval length,

$$
A_{o,b}^{(s)}=\frac{1}{300}\int_0^{300}Q_{real}^{(s)}(o,b,t)\,dt.
$$

Define

$$
\Delta_b^{(s)}=A_{MTP,b}^{(s)}-A_{NTP,b}^{(s)},
$$

$$
\Delta_{int}^{(s)}=\Delta_{Therefore}^{(s)}-\Delta_{Decision}^{(s)}.
$$

Secondary metrics: $T_{0.9}$, final $Q_{real}$, H1 native accuracy/margin, H2 private accuracy/margin, train/eval gap, local H1 cross-entropy and accuracy, examples and tokens to threshold.

## 3. Falsification Matrix

| Item | Clause tested | Why needed | Pass | Fail / insufficient | Output |
|---|---|---|---|---|---|
| $Q$-AUC interaction | local transport predicts downstream efficiency | main causal prediction | protocol threshold | opposite/weak interaction | interaction table/figure |
| H1-margin interaction | effect reaches standard interface | rejects private-H2-only account | same mean ordering | H2 only changes | margin table |
| Step-0 pairing | fair objective comparison | excludes initialization mismatch | equal within tolerance | mismatch | guard table |
| Matched schedules/data | fair finite-step comparison | excludes sampling effect | hashes equal | mismatch | guard table |
| Local H1 guard | no trivial LM collapse | protects interpretation | both objectives learn locally | collapse | local table |

## 4. Configuration

- seeds: `971,972,973,974,975`;
- updates: `300`;
- batch size: `4`;
- optimizer: AdamW, learning rate `1e-5`, weight decay `0.01`;
- checkpoints: `0,1,2,5,10,20,50,100,200,300`;
- train paraphrases: `0,1`; evaluation paraphrases: `2,3`;
- one worker with four H100 GPUs, four independent task shards.

## 5. Plot Contract

Central figure: four mean $Q_{real}$ curves plus a per-seed interaction panel.

- question: does favorable bridge transport selectively increase MTP's standard-H1 efficiency?
- x-axis: backbone updates;
- y-axis: held-out $Q_{real}$ or per-seed normalized AUC interaction;
- allowed conclusion: bridge-conditioned modulation on this fixed task;
- limitation: one model, two bridges, one output format, and a decision-weighted proxy rather than general pretraining.

## 6. Artifact Contract

Produce `curve_metrics.csv`, `paired_guards.csv`, `per_domain_accuracy.csv`, `interaction_summary.csv`, `hypothesis_decision.json`, one central figure, `summary.md`, and `detailed.md`.
