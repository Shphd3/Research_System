# Protocol: A11_14 Natural-Language Semantic Learning Efficiency

## 0. Approval Snapshot

**Approval status:** approved for implementation and remote four-GPU execution under the user's standing instruction.  
**Purpose:** compare NTP and K=2 MTP learning curves on the fixed A11_13 downstream semantic-state task.  
**Primary anchor:** `11_14_natural_language_semantic_learning_efficiency_anchor.md`.  
**Decision question:** does K=2 MTP reach a common standard-H1 semantic score earlier than NTP under matched data-token and backbone-update budgets?  
**Primary metric:** $T_{0.9}$ for $Q_{downstream}=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}$, with three consecutive evaluations.  
**Falsifier:** H2 direct recovery without a common-H1 speed/AUC advantage, or MTP local-H1 regression beyond the guard.  
**Conditions:** `ntp_all_h1`, `mtp_all_k2`.  
**Seeds:** `971-975`.  
**Execution:** ten tasks on one four-H100 ACP job after CPU/GPU smoke validation.  
**Cannot claim:** compute efficiency, pretrained-LLM benefit, open-ended quality, external transfer, or universal MTP superiority.

## 1. Data And Split

Source data are regenerated from the frozen A11_13 config. Only `horizon_target=256` is selected.

| Split | Paraphrase IDs | Examples per seed | Purpose |
|---|---|---:|---|
| train | 0, 1 | 160 | learn state-action composition |
| evaluation | 2, 3 | 160 | test unseen wording |

Every split remains balanced across five domains, two states, four requests, two option orders, and answer labels.

Rendered sequence:

```text
<BOS> earlier cue + intervening dialogue + current request/options
<EOP> <DECIDE> <ANS_A or ANS_B>
```

The answer special token never appears in the prompt. Vocabulary construction sees prompt strings from both splits but never answer labels; this is tokenizer coverage, not supervised test exposure.

## 2. Model And Objective

Model:

- deterministic word/punctuation tokenizer;
- learned token and position embeddings;
- two pre-norm causal Transformer layers;
- `d_model=128`, `n_heads=4`, `d_ff=512`, dropout `0`;
- separate bias-free H1 and H2 vocabulary heads;
- H2 initialized as an exact copy of H1;
- all parameters trainable, but H2 receives no gradient in NTP.

Objectives:

$$
L_{NTP}=L_1^{all},
$$

$$
L_{MTP}=L_1^{all}+L_2^{all}.
$$

Each horizon loss is independently averaged over its valid nonpadding positions. H1 keeps coefficient one in both conditions; MTP adds H2 rather than rescaling H1. This matches data-token and backbone-update budgets, not FLOPs or total gradient norm. Those remain explicit limitations.

## 3. Optimization

- AdamW;
- learning rate `3e-4`;
- weight decay `0.01`;
- batch size `16`;
- gradient-norm clip `1.0`;
- maximum `5,000` updates, subject to smoke adjustment before the full run;
- identical sampled batch indices per paired seed;
- checkpoints `0,10,20,50,100,200,500,1000,2000,3000,4000,5000`;
- full evaluation at every checkpoint.

Any smoke adjustment may change the common training horizon or learning rate only before the full run and must be recorded. It may not change the task, split, conditions, primary metric, or decision rules.

## 4. Metrics

### 4.1 Common downstream score

`A_H1`: standard H1 answer accuracy from the `<DECIDE>` hidden state.

$$
C_{para}^{model}
=\frac1{|P|}\sum_{g\in P}
\mathbf1[\text{all predictions in paraphrase group }g\text{ agree}],
$$

$$
S_{cf}^{model}
=\frac1{|F|}\sum_{g\in F}
\mathbf1[\text{the two state-counterfactual predictions differ}].
$$

$$
Q_{downstream}=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}.
$$

### 4.2 Efficiency

$$
T_{0.9}=\inf\{t:Q_{downstream}\ge0.9\text{ for three consecutive evaluations}\}.
$$

Report $T_{0.9}$ in updates and cumulative processed nonpadding tokens. Right-censor unreached runs at the final budget. Report normalized trapezoidal AUC of $Q_{downstream}$ versus processed tokens.

### 4.3 Mechanism and guards

- H2 direct answer accuracy and margin at `<EOP>`;
- H1 answer negative log-likelihood and margin at `<DECIDE>`;
- cosine between H1 and H2 answer contrast rows $(u_A-u_B)$;
- non-answer H1 CE and accuracy on evaluation prompts;
- per-domain H1 answer accuracy;
- initialization hashes for embedding, backbone, H1, and H2;
- train/eval sample hashes, batch-index hash, cumulative token count, and update count;
- wall time and peak GPU memory.

## 5. Decision Rules

**Validity guards:** paired shared-parameter hashes match at step 0; data/split/batch hashes match; cumulative tokens and updates match at every common checkpoint; no answer token appears in prompt; all outputs are finite; ten tasks and all checkpoints are complete.

**Adjudicable:** at least one condition reaches the threshold in at least 4/5 seeds.

**Supported:**

1. adjudicable;
2. MTP has smaller paired $T_{0.9}$ in at least 4/5 seeds, counting an unreached NTP as right-censored;
3. MTP token-AUC exceeds NTP in at least 4/5 seeds;
4. final MTP common-H1 $Q_{downstream}$ is at least NTP in at least 4/5 seeds;
5. every seed passes local H1 accuracy and CE guards.

**Weakened:** both methods are adjudicable but fewer than 4/5 speed or AUC comparisons favor MTP, or the local guard fails.

**Insufficient:** neither condition is adjudicable or any paired validity/coverage guard fails.

**Falsified:** both are adjudicable and MTP is slower in at least 4/5 seeds, or only H2 recovers while H1 remains near chance.

## 6. Stage-Level Plan

| Stage | Question | Pass rule | Artifact |
|---|---|---|---|
| static validation | do tokenizer, indices, masks, and pair hashes hold? | exact assertions | `static_audit.json` |
| CPU smoke | can one paired seed run two updates and emit all metrics? | finite complete tables | smoke directory |
| GPU smoke | does CUDA run one paired seed through an early checkpoint? | same guards, sensible loss | ACP smoke log/result |
| remote full | do ten tasks complete on four GPUs? | full coverage | shard manifests and curves |
| analysis | are threshold/AUC/local rules adjudicable? | complete paired joins | decision JSON and figure |

## 7. Required Outputs

- `curve_metrics.csv`;
- `paired_guards.csv`;
- `per_domain_accuracy.csv`;
- `run_manifest.json` and shard manifests;
- `hypothesis_decision.json`;
- learning-curve and threshold tables;
- one central figure showing common H1 $Q_{downstream}$, component curves, H2 direct diagnostics, and local H1 guard;
- canonical `summary.md` and `detailed.md`.

## 8. Claim Boundary And Next Action

Even a supported result is a small-model controlled natural-language bridge. Because MTP evaluates an extra head during training, matched token/update efficiency is not matched FLOP efficiency. The next anchor may use a pretrained small LLM only after common-H1 transfer is supported here; otherwise diagnose the failure within this fixed task first.

