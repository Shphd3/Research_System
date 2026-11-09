# Protocol: A11_15 Pretrained Semantic-Transfer Efficiency

## 0. Approval Snapshot

**Purpose:** test whether pretrained semantic geometry makes the fixed held-out paraphrase task solvable and, conditional on that, whether an earlier H2 answer loss accelerates the common H1 curve.  
**Model:** Qwen3-0.6B-Base.  
**Conditions:** NTP response-position fine-tuning and K=2 MTP response-position fine-tuning.  
**Seeds:** `971-975`.  
**Primary metric:** evaluation $Q_{downstream}$, then conditional $T_{0.9}$ and token-AUC.  
**Execution:** remote four H100 GPUs.  
**Cannot claim:** pure pretraining or matched-FLOP efficiency.

## 1. Fixed Data Contract

- A11_13 prompts, horizon `256`;
- train cue paraphrases `0,1` and evaluate unseen `2,3`;
- 160 train and 160 evaluation prompts per seed;
- exact A11_13 state, paraphrase, counterfactual, balance, and shortcut properties;
- prompt text is unchanged from A11_14b.

The pretrained tokenizer appends IDs `40425` (` Decision`) and `362/425` (` A/ B`). All are single tokens. No new vocabulary rows are added.

## 2. Model And Objective

- load `/data/share/Qwen3-0.6B-Base` in bfloat16;
- tied embedding/H1 head stays tied;
- instantiate a separate H2 vocabulary head copied exactly from H1;
- train the full backbone, H1/tied embedding, and H2 for MTP;
- instantiate H2 in NTP but leave it gradient-free;
- use no all-position prompt loss in this anchor.

Losses:

$$
L_{NTP}^{pt}=L_S+L_I,
$$

$$
L_{MTP}^{pt}=L_S+L_I+L_D.
$$

The shared-format loss $L_S$ trains the prompt-ending state to predict ` Decision`; $L_I$ trains the common H1 answer after that token; $L_D$ is MTP's earlier answer loss.

## 3. Optimization And Checkpoints

- AdamW learning rate `1e-5`;
- weight decay `0.01`;
- batch size `4`;
- gradient clip `1.0`;
- bfloat16 forward/backward;
- 300 updates;
- checkpoints `0,1,2,5,10,20,50,100,200,300`;
- evaluate train and held-out splits at every checkpoint;
- identical paired batch schedules and processed-token counts.

## 4. Metrics

Primary held-out score:

$$
Q_{eval}=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}.
$$

Also record:

- train $Q$ and train/evaluation gap;
- H1 full-vocabulary answer accuracy, NLL, and A/B margin;
- H2 direct full-vocabulary accuracy, NLL, and margin;
- H1/H2 answer-contrast cosine;
- per-domain H1 accuracy;
- local prompt-token CE/accuracy on eight deterministic positions per example;
- initialization, model-path, tokenizer, sample, batch, token, and update hashes;
- wall time and peak GPU memory.

## 5. Decision Rules

**Valid:** ten tasks complete; paired pretrained/shared/H2 hashes match; data, tokenizer, batch, and processed-token guards match; all metrics finite.

**Adjudicable:** at least one condition reaches evaluation $Q\ge0.9$ for three consecutive evaluations in at least 4/5 seeds.

**Non-ceiling:** if both conditions already have step-0 $Q\ge0.9$ in at least 4/5 seeds, report a solvable but ceiling-limited task and do not adjudicate training efficiency.

**Supported:** adjudicable; MTP has smaller $T_{0.9}$ and larger token-AUC in at least 4/5; final evaluation $Q$ is not lower in at least 4/5; local CE/accuracy guards pass in every seed.

**Weakened:** adjudicable but speed/AUC or local guards do not support MTP.

**Insufficient:** no condition is adjudicable, the task is ceiling-limited at step 0, or implementation guards fail.

**Falsified:** both are adjudicable and MTP is slower in at least 4/5 seeds.

## 6. Required Outputs

- train/evaluation curves;
- paired threshold/AUC and local-drift tables;
- per-domain table;
- validity/coverage manifests;
- central figure separating zero-shot, train fit, held-out transfer, H1/H2, and local drift;
- canonical `summary.md`, `detailed.md`, anchor and story updates.
